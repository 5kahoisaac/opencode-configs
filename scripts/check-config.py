#!/usr/bin/env python3
"""Config consistency checker for the opencode configuration repo.

Validates cross-references between opencode.json and oh-my-openagent.json
(routed models must be reachable through enabled providers and whitelist/
blacklist filters), checks that concurrency-map keys refer to live
providers/models, warns about models missing from the models.dev catalog,
and warns about drift between the repo copy and the deployed copy under
~/.config/opencode/.

Python 3 stdlib only.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEPLOY_DIR = Path(os.path.expanduser("~/.config/opencode"))
CATALOG_URL = "https://models.dev/api.json"
CATALOG_TIMEOUT_SECONDS = 5

errors = []
warnings = []


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_provider_model(ref):
    """Split 'provider/model-id' on the FIRST slash only.

    nvidia model IDs contain slashes themselves (e.g.
    'nvidia/minimaxai/minimax-m2.7'), so the model-id may still contain '/'.
    """
    if "/" not in ref:
        return ref, ""
    provider, model_id = ref.split("/", 1)
    return provider, model_id


def collect_routed_refs(oh_my):
    """Collect every routed model ref from agents.* and categories.* blocks.

    Returns a set of 'provider/model-id' strings, covering `model`, each
    `fallback_models` entry (string or {"model": ...} object form), and
    `ultrawork.model`.
    """
    refs = set()

    def collect_from_block(block):
        if not isinstance(block, dict):
            return
        model = block.get("model")
        if isinstance(model, str):
            refs.add(model)
        fallback_models = block.get("fallback_models")
        if isinstance(fallback_models, list):
            for entry in fallback_models:
                if isinstance(entry, str):
                    refs.add(entry)
                elif isinstance(entry, dict):
                    entry_model = entry.get("model")
                    if isinstance(entry_model, str):
                        refs.add(entry_model)
        ultrawork = block.get("ultrawork")
        if isinstance(ultrawork, dict):
            ultrawork_model = ultrawork.get("model")
            if isinstance(ultrawork_model, str):
                refs.add(ultrawork_model)

    for section in ("agents", "categories"):
        section_dict = oh_my.get(section, {})
        if not isinstance(section_dict, dict):
            continue
        for _name, block in section_dict.items():
            collect_from_block(block)

    return refs


def check_routed_model_reachability(oh_my, opencode, routed_refs):
    """ERROR level: every routed model must resolve to a live provider/model."""
    enabled_providers = set(opencode.get("enabled_providers", []))
    provider_cfg = opencode.get("provider", {})
    omlx_models = set(provider_cfg.get("omlx", {}).get("models", {}).keys())

    for ref in sorted(routed_refs):
        provider, model_id = split_provider_model(ref)

        if provider not in enabled_providers:
            errors.append(
                "ERROR: routed model '{}' uses provider '{}' which is not in "
                "enabled_providers".format(ref, provider)
            )
            continue

        if provider == "omlx":
            if model_id not in omlx_models:
                errors.append(
                    "ERROR: routed model '{}' is not a key of "
                    "provider.omlx.models".format(ref)
                )
            continue

        provider_entry = provider_cfg.get(provider, {})
        whitelist = provider_entry.get("whitelist")
        blacklist = provider_entry.get("blacklist")

        if whitelist is not None and model_id not in whitelist:
            errors.append(
                "ERROR: routed model '{}' is not in provider.{}.whitelist".format(
                    ref, provider
                )
            )
        if blacklist is not None and model_id in blacklist:
            errors.append(
                "ERROR: routed model '{}' is in provider.{}.blacklist".format(
                    ref, provider
                )
            )


def check_concurrency_liveness(oh_my, opencode, routed_refs):
    """WARN level: concurrency-map keys should reference live providers/models."""
    enabled_providers = set(opencode.get("enabled_providers", []))
    background_task = oh_my.get("background_task", {})

    model_concurrency = background_task.get("modelConcurrency", {})
    if isinstance(model_concurrency, dict):
        for key in sorted(model_concurrency.keys()):
            if key not in routed_refs:
                warnings.append(
                    "WARN: modelConcurrency key '{}' is not a routed model".format(
                        key
                    )
                )

    provider_concurrency = background_task.get("providerConcurrency", {})
    if isinstance(provider_concurrency, dict):
        for key in sorted(provider_concurrency.keys()):
            if key not in enabled_providers:
                warnings.append(
                    "WARN: providerConcurrency key '{}' is not in "
                    "enabled_providers".format(key)
                )


def fetch_catalog():
    request = urllib.request.Request(
        CATALOG_URL, headers={"User-Agent": "check-config.py"}
    )
    with urllib.request.urlopen(request, timeout=CATALOG_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def check_catalog_existence(routed_refs):
    """WARN level, network-tolerant: routed hosted models should exist in
    the models.dev catalog."""
    try:
        catalog = fetch_catalog()
    except Exception:
        print("catalog check skipped (offline)")
        return

    for ref in sorted(routed_refs):
        provider, model_id = split_provider_model(ref)
        if provider == "omlx":
            continue

        provider_entry = catalog.get(provider)
        if provider_entry is None:
            warnings.append(
                "WARN: routed model '{}' uses provider '{}' missing from "
                "models.dev catalog".format(ref, provider)
            )
            continue

        catalog_models = provider_entry.get("models", {})
        if model_id not in catalog_models:
            warnings.append(
                "WARN: routed model '{}' has model-id missing from "
                "models.dev catalog for provider '{}'".format(ref, provider)
            )


def check_deploy_drift():
    """WARN level: repo config files should match their deployed copies."""
    files = ["AGENTS.md", "opencode.json", "oh-my-openagent.json", "tui.json"]
    for filename in files:
        deployed_path = DEPLOY_DIR / filename
        repo_path = REPO_ROOT / filename
        if not deployed_path.exists():
            continue
        if not repo_path.exists():
            continue
        try:
            deployed_bytes = deployed_path.read_bytes()
            repo_bytes = repo_path.read_bytes()
        except OSError:
            continue
        if deployed_bytes != repo_bytes:
            warnings.append(
                "WARN: drift: {} differs from deployed copy (run make sync "
                "or reconcile)".format(filename)
            )


def main():
    opencode_path = REPO_ROOT / "opencode.json"
    oh_my_path = REPO_ROOT / "oh-my-openagent.json"

    try:
        opencode = load_json(opencode_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append("ERROR: failed to parse {}: {}".format(opencode_path, exc))
        opencode = {}

    try:
        oh_my = load_json(oh_my_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append("ERROR: failed to parse {}: {}".format(oh_my_path, exc))
        oh_my = {}

    routed_refs = set()
    if opencode and oh_my:
        routed_refs = collect_routed_refs(oh_my)
        check_routed_model_reachability(oh_my, opencode, routed_refs)
        check_concurrency_liveness(oh_my, opencode, routed_refs)
        check_catalog_existence(routed_refs)

    check_deploy_drift()

    for line in errors:
        print(line)
    for line in warnings:
        print(line)

    print(
        "check-config: {} errors, {} warnings".format(len(errors), len(warnings))
    )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
