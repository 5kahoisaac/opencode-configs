---
description: Dynamically synchronizes the OpenCode blacklist for the xAI, Zen, and DigitalOcean providers. For xAI, blacklists non-LLM models and outdated families (preserving coding models). For Zen, blacklists paid models (preserving free-tier). For DigitalOcean, blacklists premium Anthropic and OpenAI models that require higher account tiers (preserving open-source variants like gpt-oss). Sources are queried fresh on every run.
---

# OpenCode Command: Provider Blacklist Synchronizer (xAI + Zen + DigitalOcean)

This command keeps `./opencode.json` in sync for three providers: **xAI**, **OpenCode Zen**, and **DigitalOcean**. It builds an **exclusion list** so that newly released models stay available by default — the safer property when providers ship faster than this sync runs.

Each provider has its own blacklist criteria:

| Provider       | Blacklist Criteria                                                                                                                                              |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `xai`          | Non-LLM/multimodal models + models from outdated families (coding models always preserved)                                                                      |
| `opencode`     | Paid Zen models (any model with an accessible free tier is always preserved)                                                                                    |
| `digitalocean` | Premium Anthropic Claude models + premium OpenAI GPT/o-series models that require higher account tiers (open-source variants like `gpt-oss-*` always preserved) |

## Core Principles (apply to all providers)

- **Nothing is hardcoded.** Flagship status, family membership, and pricing are re-derived from official sources on every run.
- **Coding models are never blacklisted** (xAI). They are exempt from the "outdated family" filter — a coding-specialized model from an older line is still worth keeping.
- **Free-tier models are never blacklisted** (Zen). The blacklist is for paid-only models; free-tier models must remain available for low-cost workflows.
- **Open-source models are never blacklisted** (DigitalOcean). Models distributed with open weights (e.g. `gpt-oss-*`) are not subject to DigitalOcean's premium-tier restrictions and stay available regardless of vendor prefix.
- **Blacklist semantics favor availability.** A model not yet classified stays available. When uncertain whether to add a model to the blacklist, prefer to **leave it off** — accidentally hiding a useful new model is worse than briefly exposing one that should be filtered.
- **Non-LLM / multimodal models are always blacklisted** (xAI). Vision, image-gen, video, voice, TTS, audio — none of these belong in a code-assistant config.

---

## Provider 1: xAI

### Phase 1 — Identify current flagship families

Fetch and parse: **https://docs.x.ai/developers/models**

From the page, identify the model families currently presented as **flagship / latest** (e.g. Grok-4.20 family, Grok-4.1 fast variants, Grok-4 family, Grok-Beta). Any family not shown as current is treated as outdated.

The definition of "latest" is not hardcoded — as new major versions ship (e.g. Grok-5), previous generations will automatically be reclassified as outdated on the next run.

### Phase 2 — Enumerate all xAI model IDs

Fetch the full model list from:
**https://github.com/anomalyco/models.dev/tree/dev/providers/xai/models**

Extract the model IDs from the TOML filenames.

### Phase 3 — Build the xAI blacklist

Walk every model from Phase 2 and **add it to the blacklist** if any of these are true:

1. It is a non-LLM / multimodal model — ID contains `vision`, `imagine`, `image`, `video`, `voice`, `audio`, or `tts`. Examples: `grok-*-vision*`, `grok-vision-beta`, `grok-imagine-*`. **OR**
2. It belongs to a family that is **not** in the current flagship set from Phase 1.

**Exception — always preserve coding models.** Any model that is clearly coding-focused (e.g. `grok-code-fast-1`, `grok-build-0.1` and future equivalents) is excluded from the blacklist regardless of its family's flagship status. Coding models still get blacklisted if they're multimodal, but that's a rare combination.

### Phase 4 — Write to `opencode.json`

Update the key `provider.xai.blacklist` with the resulting array. Replace, do not merge.

**Example output** (dynamic — actual contents depend on what's current):

```jsonc
{
  "provider": {
    "xai": {
      "blacklist": [
        "grok-2",
        "grok-2-latest",
        "grok-2-1212",
        "grok-2-vision",
        "grok-2-vision-latest",
        "grok-3",
        "grok-3-latest",
        "grok-3-fast",
        "grok-3-mini",
        "grok-3-mini-fast",
        "grok-vision-beta",
        "grok-imagine-image",
        "grok-imagine-image-pro",
        "grok-imagine-video"
      ]
    }
  }
}
```

---

## Provider 2: OpenCode Zen

### Phase 1 — Fetch model + pricing data

Check these sources in order, stopping at the first that returns usable data:

1. `https://opencode.ai/zen/v1/models` (API endpoint — preferred, structured)
2. `https://opencode.ai/docs/zen/` (human-readable fallback)

Extract every model ID along with its pricing fields. Note explicitly free model IDs separately for cross-checking.

### Phase 2 — Identify free-tier models (to exclude from the blacklist)

A Zen model qualifies as free-tier if **any** of the following hold in the Zen data:

- Model ID contains `free` (e.g. `*-free`)
- Pricing table marks it as "Free"
- Input, output, **and** cached-read prices are all `$0.00` or "Free of charge"

**Cross-reference with the official upstream provider's pricing** before classifying. Zen's classification can lag; the upstream provider is the source of truth. If the two disagree, trust the upstream provider.

**When uncertain whether a model has a free tier, default to keeping it OFF the blacklist** — leaving it available is the safer error.

### Phase 3 — Build the Zen blacklist

The blacklist is: every Zen model from Phase 1 **except** confirmed free-tier models from Phase 2.

A model family may ship both free and paid variants — evaluate each model ID individually, not by family.

### Phase 4 — Write to `opencode.json`

Update the key `provider.opencode.blacklist` with the resulting array. Replace, do not merge.

```jsonc
{
  "provider": {
    "opencode": {
      "blacklist": [
        // Dynamically generated: paid Zen model IDs (free-tier models excluded)
      ]
    }
  }
}
```

---

## Provider 3: DigitalOcean

DigitalOcean's Gradient AI Platform restricts certain premium foundation models (such as Claude Opus) and advanced features (like AI judge / evaluation datasets) to higher account tiers. Lower tiers and accounts without a prepaid balance are blocked from using them. This blacklist excludes those premium models so the config only surfaces what the account can actually call.

### Phase 1 — Enumerate all DigitalOcean model IDs

Fetch the full model list from:
**https://github.com/anomalyco/models.dev/tree/dev/providers/digitalocean/models**

Model IDs are the **filename stems** (the TOML files do not contain an `id` field — the filename is authoritative). Examples: `anthropic-claude-opus-4.7`, `openai-gpt-5.5`, `openai-gpt-oss-120b`, `deepseek-v3`.

### Phase 2 — Build the DigitalOcean blacklist

Walk every model from Phase 1 and **add it to the blacklist** if any of these are true:

1. The model ID starts with `anthropic-` (all Claude variants on DigitalOcean are premium-tier, including Haiku and Sonnet — none are open-source). **OR**
2. The model ID starts with `openai-` **AND** does **not** contain `oss` anywhere in the ID.
    - This catches GPT-4*, GPT-5*, o1, o3*, codex, pro, mini, nano, and image-generation variants.
    - It preserves `openai-gpt-oss-*` (the open-weights releases — currently `openai-gpt-oss-20b` and `openai-gpt-oss-120b`).

**Do not blacklist** anything else — Qwen, DeepSeek, Llama, Mistral, Gemma, Kimi, Nemotron, GLM, MiniMax, Arcee, fal-ai, and other open or partner models stay available. They are not subject to DigitalOcean's premium-tier restriction.

The `openai-` rule is intentionally substring-based on `oss` rather than a hardcoded list of OSS model IDs. If OpenAI releases additional open-weights variants under the `gpt-oss-*` naming convention, the next sync run will preserve them automatically without a code change.

### Phase 3 — Write to `opencode.json`

Update the key `provider.digitalocean.blacklist` with the resulting array. Replace, do not merge.

**Example output** based on the current model list (dynamic — will grow as new premium models are added):

```jsonc
{
  "provider": {
    "digitalocean": {
      "blacklist": [
        "anthropic-claude-3-opus",
        "anthropic-claude-3.5-haiku",
        "anthropic-claude-3.5-sonnet",
        "anthropic-claude-3.7-sonnet",
        "anthropic-claude-4.1-opus",
        "anthropic-claude-4.5-haiku",
        "anthropic-claude-4.5-sonnet",
        "anthropic-claude-4.6-sonnet",
        "anthropic-claude-haiku-4.5",
        "anthropic-claude-opus-4",
        "anthropic-claude-opus-4.5",
        "anthropic-claude-opus-4.6",
        "anthropic-claude-opus-4.7",
        "anthropic-claude-sonnet-4",
        "openai-gpt-4.1",
        "openai-gpt-4o",
        "openai-gpt-4o-mini",
        "openai-gpt-5",
        "openai-gpt-5-mini",
        "openai-gpt-5-nano",
        "openai-gpt-5.1-codex-max",
        "openai-gpt-5.2",
        "openai-gpt-5.2-pro",
        "openai-gpt-5.3-codex",
        "openai-gpt-5.4",
        "openai-gpt-5.4-mini",
        "openai-gpt-5.4-nano",
        "openai-gpt-5.4-pro",
        "openai-gpt-5.5",
        "openai-gpt-image-1",
        "openai-gpt-image-1.5",
        "openai-gpt-image-2",
        "openai-o1",
        "openai-o3",
        "openai-o3-mini"
      ]
    }
  }
}
```

---

## Writing `opencode.json` (shared procedure)

1. Read the existing `./opencode.json`.
2. Update or create `provider.xai.blacklist`, `provider.opencode.blacklist`, and/or `provider.digitalocean.blacklist` depending on which provider(s) the run covered. Leave all other keys (including unrelated providers) untouched.
3. Preserve formatting: same indentation, no reordering of unrelated keys, trailing newline as before.
4. Validate: `python3 -m json.tool opencode.json` must succeed.
5. Review the diff and confirm only the intended keys changed.

## Common Mistakes

1. **Trusting incomplete evidence.** Always verify pricing from official upstream sources for Zen, not just the Zen model listing.
2. **"Add if uncertain" bias.** When uncertain whether a model belongs on the blacklist, default to **leaving it off**, not adding it. Blacklist errors-of-commission hide useful models; errors-of-omission are self-correcting on the next run.
3. **Mixing paid and free variants on Zen.** A model family may have both. Check each specific model ID.
4. **Family-level reasoning when ID-level is required.** Don't blacklist `grok-3*` wholesale if a `grok-3-code-*` exists — coding models are preserved individually.
5. **Hardcoding flagship families for xAI.** "Grok-4 is flagship" will be wrong the day Grok-5 ships. The docs page is the source of truth on every run.
6. **Blacklisting coding models because their family is old.** Coding models are exempt from the outdated-family filter.
7. **Blacklisting `gpt-oss-*` on DigitalOcean.** The `openai-` prefix alone isn't enough — check for `oss` in the ID before adding. Open-weights models aren't subject to the premium-tier restriction.
8. **Hardcoding the DigitalOcean OSS allowlist.** Use the `oss`-substring rule, not a literal list like `["openai-gpt-oss-20b", "openai-gpt-oss-120b"]`. Future OSS releases following the same naming convention will then preserve themselves automatically.
9. **Over-extending the DigitalOcean rule to other vendor prefixes.** Only `anthropic-*` and premium `openai-*` are restricted. Don't sweep up `deepseek-*`, `qwen-*`, `mistral-*`, etc. — those stay available.