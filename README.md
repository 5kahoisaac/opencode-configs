# OpenCode Configuration

## Table of Contents

- [Overview](#overview)
- [Roadmap](#roadmap)
- [Available Makefile Commands](#available-makefile-commands)
- [Configuration](#configuration)
    - [Providers](#providers)
        - [Provider List](#provider-list)
        - [Provider Blacklist Strategy](#provider-blacklist-strategy)
        - [Models Configuration](#models-configuration)
    - [Plugins](#plugins)
    - [MCPs](#mcps)
    - [Commands](#commands)
        - [TUI Configuration](#tui-configuration)
    - [Agents](#agents)
- [Team Mode](#team-mode)
- [Reference Links](#reference-links)

---

## Overview

This project contains a comprehensive OpenCode configuration setup designed to enhance AI-assisted development
workflows. OpenCode is an open-source AI coding assistant that provides intelligent code completion, refactoring
capabilities, and seamless integration with various development tools and platforms.

The configuration includes carefully selected plugins, commands, and agents that extend OpenCode's functionality
to support complex development tasks, improve code quality, and streamline development workflows. This setup is
particularly focused on providing enterprise-grade features while maintaining flexibility for personal and team use
cases.

OpenCode serves as a powerful alternative to traditional IDE-based AI assistants, offering features such as
context-aware code generation, multi-file refactoring, intelligent code search, and integration with popular development
tools like GitHub, Jira, and Figma. The configuration files in this project customize OpenCode's behavior to match
specific workflow requirements and preferences.

---

## Roadmap

This repository is being simplified around three directions:

1. **Move skills into Skillless.** Skills and skill presets are moving to
   [skillless](https://github.com/5kahoisaac/skillless), so this repository can stay focused on OpenCode configuration
   instead of becoming a mixed skill/config bundle.

2. **Remove Anthropic-specific OpenCode paths.** The `anthropic` provider and `opencode-with-claude` plugin have
   been removed from this setup as a personal workflow decision. Claude models currently run better in Claude Code
   than in OpenCode with Oh-My-OpenAgent, and Claude Code gives smoother control for Claude-centric work.

3. **Centralize MCPs through MCPProxy and prefer CLIs where possible.** Most direct MCP configuration is being removed
   so
   multiple coding agents do not each maintain their own MCP setup. Shared MCPs now live behind MCPProxy, using the
   `retrieve_tools` routing mode to search tools on demand and lazy-load only the tools matching the current keyword or
   task instead of injecting every MCP tool into context. Over time, some MCPs are also being replaced with CLI-based
   presets from Skillless, such as the
   [CLI preset list](https://github.com/5kahoisaac/skillless/blob/main/lists/cli.csv). The goal is to replace high-token
   MCP flows such as Exa `websearch` and Context7 with CLI workflows where they save tokens and perform better.

### Recent Transitions

The current cycle is removing legacy surfaces and consolidating code intelligence onto faster backends:

- **Consolidated routed providers behind OmniRoute.** The direct `nvidia`, `github-copilot`, `codex`, `opencode-zen`,
  and `openai` providers (and the separate accounts and API keys each required) have all been removed from this setup.
  Their model surface is now served through a single OmniRoute provider (`omni`) declared in `opencode.json`:
    - `nvidia/*` → `omni/nvidia/*` (NVIDIA-hosted MiniMax and GPT-OSS builds)
    - `github-copilot/*` → `omni/github/*` (GitHub-hosted GPT and Gemini variants)
    - `codex/*` → `omni/codex/*` (OpenAI GPT-5.x family hosted via Codex)
    - `opencode-zen/*` → `omni/opencode-zen/*` (Zen free-tier; retained as fallback-only sub-namespace under `omni/`)
    - `openai/*` → `omni/openai/*` (direct OpenAI models fronted by OmniRoute)
    - Google Gemini Flash models → `omni/gemini/*`
    - Zhipu GLM models → `omni/glm/*`

  OmniRoute fronts these multiple upstream provider services behind one endpoint and one API key
  (`OMNI_OPENCODE_API_KEY`) for centralized management, unified cost tracking, and load balancing across per-account
  rate limits. It also exposes an `auto/best-free` "combo" router that auto-selects the best available free model at
  request time. Agent and task-category routing in `oh-my-openagent.json` now references every model with the `omni/`
  prefix (for example `omni/nvidia/minimaxai/minimax-m3` and `omni/auto/best-free`), and the `git` and `writing`
  categories lean on the combo router for cost-free fallbacks.

  **Why this saves tokens:** centralizing every upstream behind one router lets OmniRoute apply router-level compression
  (headroom-style pruning, RTK-style token-killing filters on tool output, and dedup of repeated system prompts) before
  a request ever reaches the upstream model. A direct multi-provider setup cannot do this — each provider sees the full
  raw payload. Consolidation also means a single billed surface for cost tracking and a single rate-limit pool to load
  balance across, instead of N separate accounts each with their own quota ceiling.

- **Removed `opencode-historian`.** The historian plugin and agent have been removed from this setup. The
  memory-management workflow it provided is no longer used in this configuration, and the plugin does not need to be
  re-added from another source.

- **Added `codebase-memory-mcp` to MCPProxy.**
  [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) was added as a new MCPProxy upstream for
  better performance on semantic code intelligence. It builds a persistent tree-sitter knowledge graph and answers
  structural queries in under a millisecond. It runs **alongside** `serena` and `ast_grep`, not as a replacement — the
  three backends are complementary and routed by intent through MCPProxy's `retrieve_tools` mode, with per-tool
  on/off toggling used to avoid duplicate tool surfaces during a session. See
  [Code Intelligence](#code-intelligence-mcpproxy-retrieve_tools-mode) for the routing rules.

**Moved OmniRoute access to Tailscale MagicDNS.** OmniRoute Base URL changed from `https://omniroute.isaac.ng/v1` (
public Cloudflare Tunnel) to `http://rk3528:20128/v1` (Tailscale MagicDNS hostname). The Tailscale tailnet keeps
OpenCode-to-OmniRoute traffic private, skips the TLS hop, and has lower latency than round-tripping through Cloudflare.
The public `omniroute.isaac.ng` domain is retained via Cloudflare Tunnel for non-Tailscale hosts (CI runners, external
services) and is preferred over opening inbound ports to direct internet exposure.
See [Network Architecture](#network-architecture).

---

## Available Makefile Commands

Makefile provides essential commands manage OpenCode configuration:

| Command      | Description                                                                                                                                                                                             |
|:-------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make sync`  | Sync OpenCode configuration to `~/.config/opencode/`. Copies `AGENTS.md`, `oh-my-openagent.json`, `opencode.json`, and `tui.json`; mirrors root `./agents/` and `./commands/` directories when present. |
| `make check` | Validate config cross-references and drift using `scripts/check-config.py`.                                                                                                                             |
| `make help`  | Display available targets descriptions.                                                                                                                                                                 |

**Workflow:**

1. Run `make sync` copy configuration files and any root-level `agents/` / `commands/` files to OpenCode user config.
2. Run `make check` validate routed models, provider coverage, concurrency keys, and deployed-copy drift.
3. Use `make help` see all available commands.

Current repository stores project-scoped commands under `.opencode/commands/`; no root-level `agents/` or `commands/`
directories are present.

---

Configuration

### Providers

Configuration uses two explicitly enabled provider routes in `opencode.json`: local `omlx` and remote `omni`. Default
model is `omni/glm/glm-5.2`; small model is `omni/codex/gpt-5.4-mini`.

Core runtime settings:

| Setting           | Current value                                                                                                                   |
|:------------------|:--------------------------------------------------------------------------------------------------------------------------------|
| Default model     | `omni/glm/glm-5.2`                                                                                                              |
| Small model       | `omni/codex/gpt-5.4-mini`                                                                                                       |
| Enabled providers | `omlx`, `omni`                                                                                                                  |
| Skill permissions | `*` allowed                                                                                                                     |
| Todo tools        | `todoread`, `todowrite` allowed                                                                                                 |
| Compaction        | `auto: true`, `prune: true`                                                                                                     |
| Watcher ignores   | `node_modules/**`, `dist/**`, `.git/**`, `*.lock`, `**/*.log`, `.cache/**`, `build/**`, `__pycache__/**`, `.venv/**`, `venv/**` |

#### Provider List

**oMLX**

`omlx` is local OpenAI-compatible provider for MLX-hosted models.

| Field    | Value                       |
|:---------|:----------------------------|
| Package  | `@ai-sdk/openai-compatible` |
| Name     | `oMLX`                      |
| Base URL | `http://127.0.0.1:8080/v1`  |
| API key  | `sk_live_dummy`             |

Configured models:

| Model ID                        | Display name                  | Context |  Input | Output |
|:--------------------------------|:------------------------------|--------:|-------:|-------:|
| `gemma-4-26b-a4b-it-mlx-8bit`   | Gemma 4 26B A4B MLX 8-bit     |  262144 | 160000 |  16384 |
| `qwen3.6-35b-a3b-ud-mlx-4bit`   | Qwen3.6 35B A3B MLX 4-bit     |  262144 | 160000 |  16384 |
| `qwythos-9b-claude-mythos-5-1m` | Qwythos 9B Claude Mythos 5 1M | 1000000 | 160000 |  16384 |

**OmniRoute**

`omni` is the primary routed OpenAI-compatible provider. It centralizes hosted Codex, GLM, Gemini, GitHub, NVIDIA, and
free-model routes behind one endpoint.

| Field    | Value                         |
|:---------|:------------------------------|
| Package  | `@ai-sdk/openai-compatible`   |
| Name     | `OmniRoute`                   |
| Base URL | `http://rk3528:20128/v1`      |
| API key  | `{env:OMNI_OPENCODE_API_KEY}` |

##### Network Architecture

OmniRoute is reachable over **Tailscale MagicDNS**, not the public internet:

- `rk3528` is the Tailscale MagicDNS hostname of the OmniRoute host (port `20128`).
- `omniroute.isaac.ng` is the public domain; a Cloudflare Tunnel terminates internet traffic to the host.
- OpenCode hits `rk3528:20128` directly over the Tailscale tailnet, bypassing Cloudflare Tunnel. Private tailnet traffic
  stays off the public internet, with no TLS termination hop and lower latency.
- The Cloudflare Tunnel front door exists only when the tailnet is unreachable (e.g. CI runners on non-Tailscale hosts).
  This is the preferred path over direct internet exposure (port forwarding) because Cloudflare Tunnel never opens
  inbound ports on the host.

##### OmniRoute Model Catalog

| Model ID                        | Display name           | Reasoning | Attachments | Context |   Input | Output | Variants                      |
|:--------------------------------|:-----------------------|:---------:|:-----------:|--------:|--------:|-------:|:------------------------------|
| `auto/best-free`                | Best Free Combo        |    yes    |     no      |  262144 |  262144 | 131072 | —                             |
| `nvidia/minimaxai/minimax-m2.7` | MiniMax M2.7           |    yes    |     no      |  204800 |  204800 | 131072 | —                             |
| `nvidia/minimaxai/minimax-m3`   | MiniMax M3             |    yes    |     yes     | 1000000 | 1000000 |  16384 | —                             |
| `nvidia/openai/gpt-oss-120b`    | GPT OSS 120B           |    yes    |     no      |  128000 |  128000 |   8192 | —                             |
| `codex/gpt-5.4`                 | GPT5.4                 |    yes    |     yes     |  200000 |  200000 | 128000 | low, medium, high, xhigh      |
| `codex/gpt-5.4-mini`            | GPT5.4Mini             |    yes    |     yes     |  409600 |  409600 | 131072 | low, medium, high, xhigh      |
| `codex/gpt-5.5`                 | GPT5.5                 |    yes    |     yes     |  400000 |  272000 | 128000 | low, medium, high, xhigh      |
| `codex/gpt-5.6-luna`            | GPT5.6Luna             |    yes    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `codex/gpt-5.6-sol`             | GPT5.6Sol              |    yes    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `codex/gpt-5.6-terra`           | GPT5.6Terra            |    yes    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `github/gpt-4o-mini`            | GPT 4o Mini            |    no     |     yes     |  128000 |  128000 |   4096 | —                             |
| `github/gemini-3.5-flash`       | Gemini3.5Flash         |    yes    |     yes     |  200000 |  128000 |  64000 | low, medium, high, xhigh      |
| `gemini/gemini-2.5-flash`       | Gemini2.5Flash         |    yes    |     yes     | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-2.5-flash-lite`  | Gemini2.5Flash Lite    |    yes    |     yes     | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3-flash-preview` | Gemini 3 Flash Preview |    yes    |     yes     | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3.1-flash-lite`  | Gemini3.1Flash Lite    |    yes    |     yes     | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3.5-flash`       | Gemini3.5Flash         |    yes    |     yes     | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `glm/glm-4.5`                   | GLM4.5                 |    yes    |     no      |  131072 |  131072 |  98304 | —                             |
| `glm/glm-4.5-air`               | GLM4.5Air              |    yes    |     no      |  131072 |  131072 |  98304 | —                             |
| `glm/glm-4.6`                   | GLM4.6                 |    yes    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-4.7`                   | GLM4.7                 |    yes    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-5`                     | GLM 5                  |    yes    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-5-turbo`               | GLM 5 Turbo            |    yes    |     no      |  200000 |  200000 | 131072 | —                             |
| `glm/glm-5.1`                   | GLM5.1                 |    yes    |     no      |  200000 |  200000 | 131072 | —                             |
| `glm/glm-5.2`                   | GLM5.2                 |    yes    |     no      | 1000000 | 1000000 | 131072 | high, max                     |

##### Provider Services

OmniRoute is a single OpenAI-compatible endpoint that fronts multiple upstream provider services behind one API key.
This is the official OmniRoute architecture — every entry in the Model Catalog above is an upstream service namespace
served through the `omni` provider, not a separate provider declaration in `opencode.json`.

**Upstream provider services fronted by `omni`:**

| Namespace             | Upstream service                                              | Origin of the surface                                            |
|:----------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------|
| `omni/codex/*`        | OpenAI GPT-5.x family (hosted via Codex)                      | Migrated from the direct `codex` provider                        |
| `omni/github/*`       | GitHub-hosted GPT and Gemini variants (former Copilot models) | Migrated from the direct `github-copilot` provider               |
| `omni/openai/*`       | Direct OpenAI models fronted by OmniRoute                     | Migrated from the direct `openai` provider                       |
| `omni/gemini/*`       | Google Gemini Flash models                                    | Migrated from the direct `gemini` provider                       |
| `omni/glm/*`          | Zhipu GLM models                                              | Migrated from the direct `glm` provider                          |
| `omni/nvidia/*`       | NVIDIA-hosted MiniMax and GPT-OSS builds                      | Migrated from the direct `nvidia` provider                       |
| `omni/opencode-zen/*` | Zen free-tier models                                          | Migrated from the direct `opencode-zen` provider (fallback-only) |
| `omni/auto/best-free` | Combo router — auto-selects best available free model         | Native OmniRoute router; no upstream equivalent                  |

**Removed direct providers.** The following direct providers previously declared in `opencode.json` have been removed
and migrated under `omni/` as the namespaces above:

- `nvidia` — separate NVIDIA build account and API key removed
- `github-copilot` — separate GitHub Copilot account and token removed
- `codex` — separate Codex/OpenAI account and API key removed
- `opencode-zen` — separate Zen account removed; retained only as `omni/opencode-zen/big-pickle` fallback reference in
  `oh-my-openagent.json`

`opencode.json` now declares only two enabled providers: `omlx` (local MLX host) and `omni` (OmniRoute). Every agent
and category in `oh-my-openagent.json` references models using the `omni/<namespace>/<model>` form.

**Why centralize behind OmniRoute:**

- **Token savings at the router level.** OmniRoute applies router-level compression — headroom-style prompt pruning,
  RTK-style token-killing filters on tool output, and deduplication of repeated system prompts — before a request
  reaches the upstream model. Direct multi-provider setups cannot do this; each provider sees the full raw payload.
- **Centralized management.** One API key (`OMNI_OPENCODE_API_KEY`), one endpoint, one auth surface to rotate.
- **Cost tracking.** A single billed surface for all model usage, instead of N separate billing dashboards.
- **Load balancing.** OmniRoute balances requests across upstream accounts behind the same namespace, so per-account
  rate-limit ceilings no longer cap a single OpenCode session.

#### Provider Blacklist Strategy

Project command `/blacklist-sync` keeps Zen provider free-tier routing safe by refreshing provider/model blacklist data.
Current `opencode.json` uses direct `omlx` and `omni` providers, while Oh-My-OpenAgent fallback model IDs may still
reference `omni/opencode-zen/big-pickle` as a fallback target.

#### Models Configuration

`oh-my-openagent.json` contains model assignments for specialized agents and category-routed background tasks. Model IDs
below include their provider prefix exactly as configured.

**Agent-Specific Model Assignments**

| Agent               | Role                | Primary model                      | Variant  | Fallback models                                                                                          | Notes                                                                                                            |
|:--------------------|:--------------------|:-----------------------------------|:---------|:---------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| `sisyphus`          | Orchestrator        | `omni/glm/glm-5.2`                 | `max`    | `omni/glm/glm-5.1`, `omni/opencode-zen/big-pickle`                                                       | Ultrawork: `omni/codex/gpt-5.5` (`medium`). Prompt: delegate heavily to hephaestus and parallelize exploration.  |
| `metis`             | Scope analysis      | `omni/glm/glm-5.2`                 | `max`    | `omni/codex/gpt-5.5` (`high`)                                                                            | Pre-planning consultation.                                                                                       |
| `prometheus`        | Planning            | `omni/codex/gpt-5.5`               | `high`   | `omni/glm/glm-5.2` (`max`)                                                                               | Prompt: keep plans concise and focus file structure / key decisions.                                             |
| `atlas`             | Codebase mapping    | `omni/codex/gpt-5.5`               | `medium` | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`                                 | Broad codebase analysis and mapping.                                                                             |
| `hephaestus`        | Implementation      | `omni/codex/gpt-5.6-sol`           | `medium` | `omni/codex/gpt-5.5` (`medium`)                                                                          | Primary implementation agent. Prompt: own codebase, explore, decide, execute; use LSP and ast-grep aggressively. |
| `oracle`            | Strategic reasoning | `omni/codex/gpt-5.5`               | `high`   | `omni/glm/glm-5.2` (`max`)                                                                               | High-stakes architecture and reasoning.                                                                          |
| `momus`             | Review              | `omni/codex/gpt-5.6-sol`           | `xhigh`  | `omni/codex/gpt-5.5` (`xhigh`), `omni/glm/glm-5.2` (`max`)                                               | Plan and implementation critique.                                                                                |
| `explore`           | Codebase analysis   | `omni/nvidia/minimaxai/minimax-m3` | —        | `omni/nvidia/minimaxai/minimax-m2.7`, `omni/gemini/gemini-3-flash-preview`, `omni/codex/gpt-5.4-mini`    | Fast contextual search and code navigation.                                                                      |
| `librarian`         | Research            | `omni/nvidia/minimaxai/minimax-m3` | —        | `omni/nvidia/minimaxai/minimax-m2.7`, `omni/gemini/gemini-3-flash-preview`, `omni/codex/gpt-5.4-mini`    | Documentation and external code research.                                                                        |
| `multimodal-looker` | Visual analysis     | `omni/codex/gpt-5.5`               | `medium` | `omni/glm/glm-5-turbo`, `omni/codex/gpt-5.4-mini`                                                        | Image and multimodal interpretation.                                                                             |
| `sisyphus-junior`   | Category executor   | `omni/codex/gpt-5.5`               | `medium` | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`, `omni/opencode-zen/big-pickle` | Backs `task()` category delegation.                                                                              |

**Task Category Model Assignments**

| Category             | Primary model                        | Variant | Fallback models                                                                                                                                 | Notes                                                                              |
|:---------------------|:-------------------------------------|:--------|:------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
| `visual-engineering` | `omni/glm/glm-5.2`                   | `max`   | `omni/glm/glm-5.1`                                                                                                                              | Frontend, UI/UX, styling, animation.                                               |
| `artistry`           | `omni/codex/gpt-5.5`                 | `high`  | `omni/glm/glm-5.2` (`max`)                                                                                                                      | Creative problem-solving.                                                          |
| `ultrabrain`         | `omni/codex/gpt-5.6-sol`             | `xhigh` | `omni/codex/gpt-5.5` (`xhigh`), `omni/glm/glm-5.2` (`max`)                                                                                      | Hard logic-heavy tasks.                                                            |
| `deep`               | `omni/codex/gpt-5.6-terra`           | `xhigh` | `omni/codex/gpt-5.6-sol` (`high`), `omni/glm/glm-5.2` (`max`)                                                                                   | Deep autonomous problem-solving.                                                   |
| `quick`              | `omni/codex/gpt-5.4-mini`            | —       | `omni/gemini/gemini-3-flash-preview`, `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`                                  | Simple edits and fast tasks.                                                       |
| `unspecified-high`   | `omni/codex/gpt-5.5`                 | `high`  | `omni/glm/glm-5.1`, `omni/glm/glm-5.2` (`max`)                                                                                                  | Higher-effort uncategorized tasks.                                                 |
| `unspecified-low`    | `omni/codex/gpt-5.6-luna`            | `xhigh` | `omni/codex/gpt-5.5` (`medium`), `omni/gemini/gemini-3-flash-preview`, `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7` | Lower-effort uncategorized tasks.                                                  |
| `writing`            | `omni/gemini/gemini-3-flash-preview` | —       | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`, `omni/auto/best-free`                                                 | Documentation and prose.                                                           |
| `git`                | `omni/auto/best-free`                | —       | `omni/glm/glm-4.7`, `omni/glm/glm-4.5-air`, `omni/opencode-zen/big-pickle`                                                                      | All git operations. Prompt: focus atomic commits, clear messages, safe operations. |

**Runtime and Background Task Configuration**

| Area                         | Current configuration                                                                                                                                                          |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Team mode                    | Enabled with tmux visualization                                                                                                                                                |
| Codegraph                    | Disabled (`enabled: false`, `auto_init: false`, `auto_provision: false`)                                                                                                       |
| Disabled OMO MCPs            | `context7`, `websearch`, `ast_grep`, `grep_app`, `codegraph`                                                                                                                   |
| Claude Code plugin overrides | `ecc@ecc`, `codex@openai-codex`, `andrej-karpathy-skills@karpathy-skills`, `claude-code-setup@claude-plugins-official`, and `understand-anything@understand-anything` disabled |
| Git master                   | No commit footer, no co-authored-by, `GIT_MASTER=1` prefix                                                                                                                     |
| Background task concurrency  | Default 5; provider concurrency `omlx: 1`, `omni: 20`                                                                                                                          |
| Runtime fallback             | Enabled; retries `400`, `401`, `429`, `503`, `529`; max 3 fallback attempts; 60s cooldown; 30s timeout; notifications enabled                                                  |

**Model Concurrency Caps**

| Model prefix               | Concurrency |
|:---------------------------|------------:|
| `omni/codex/gpt-5.6-sol`   |           1 |
| `omni/codex/gpt-5.6-terra` |           2 |
| `omni/codex/gpt-5.6-luna`  |           4 |
| `omni/codex/gpt-5.5`       |           2 |
| `omni/codex/gpt-5.4`       |           4 |
| `omni/codex/gpt-5.4-mini`  |           6 |
| `omni/glm/glm-4.5`         |          10 |
| `omni/glm/glm-4.5-air`     |           5 |
| `omni/glm/glm-4.6`         |           3 |
| `omni/glm/glm-4.7`         |           2 |
| `omni/glm/glm-5`           |           2 |
| `omni/glm/glm-5-turbo`     |           1 |
| `omni/glm/glm-5.1`         |          10 |
| `omni/glm/glm-5.2`         |          10 |

### Plugins

`opencode.json` currently enables two plugins:

| Plugin                                 | Purpose                                                                                                  | Notes                                            |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|:-------------------------------------------------|
| `@nick-vi/opencode-type-inject@latest` | Type injection support for OpenCode workflows.                                                           | Installed through OpenCode plugin configuration. |
| `oh-my-openagent@latest`               | Provides Sisyphus, task categories, team mode, background tasks, model routing, and agent orchestration. | Configured through `oh-my-openagent.json`.       |

### MCPs

`opencode.json` configures a single manual MCP entry:

| MCP         | Enabled | Type     | URL                         | Purpose                                                                      |
|:------------|:-------:|:---------|:----------------------------|:-----------------------------------------------------------------------------|
| `mcp-proxy` |   yes   | `remote` | `http://127.0.0.1:8081/mcp` | Central MCPProxy endpoint for routed tool discovery and upstream MCP access. |

Direct OpenCode MCP surface is intentionally minimal. Shared MCPs are centralized behind MCPProxy and discovered through
`retrieve_tools` / routed tool search instead of injecting every upstream tool into every OpenCode session.

#### Disabled Oh-My-OpenAgent MCPs

`oh-my-openagent.json` disables these plugin-provided MCPs: `context7`, `websearch`, `ast_grep`, `grep_app`, and
`codegraph`. This keeps context lighter and avoids duplicate MCP surfaces when MCPProxy or CLI equivalents are
preferred.

Commands

Project-scoped commands currently live under `.opencode/commands/`.

| Command           | Purpose                                                                                            |
|:------------------|:---------------------------------------------------------------------------------------------------|
| `/blacklist-sync` | Dynamically synchronize the OpenCode blacklist for the Zen provider, preserving free-tier routing. |
| `/readme-sync`    | Synchronize `README.md` with actual configuration files.                                           |

There is no root-level `commands/` directory currently. `make sync` still supports mirroring one if added later.

### TUI Configuration

`tui.json` currently selects the standard OpenCode terminal theme:

| Setting | Value      |
|:--------|:-----------|
| Theme   | `opencode` |

Additional TUI customization can be added to `tui.json` when needed.

Agents

OpenCode uses plugin-provided agents from Oh-My-OpenAgent. There are currently no repo-local `agents/` or
`.opencode/agents/` files in this project.

#### Oh-My-OpenAgent Agents

Configured agents and roles:

| Agent               | Role                                                               |
|:--------------------|:-------------------------------------------------------------------|
| `sisyphus`          | Primary orchestrator for complex, multi-step tasks and delegation. |
| `sisyphus-junior`   | Lightweight backing agent for `task()` category delegation.        |
| `hephaestus`        | Implementation-focused agent for code edits and execution.         |
| `oracle`            | Strategic reasoning and architecture advisor.                      |
| `momus`             | Review and critique agent.                                         |
| `metis`             | Pre-planning scope-analysis agent.                                 |
| `prometheus`        | Planning agent for concise implementation plans.                   |
| `atlas`             | Codebase mapping and structure analysis.                           |
| `explore`           | Fast contextual code search and navigation.                        |
| `librarian`         | Documentation, external source, and library research.              |
| `multimodal-looker` | Image, PDF, and multimodal analysis.                               |

Model assignments for these agents are documented in [Models Configuration](#models-configuration).

Team Mode

Team mode is enabled by `oh-my-openagent.json`:

| Setting                        | Value  |
|:-------------------------------|:-------|
| `team_mode.enabled`            | `true` |
| `team_mode.tmux_visualization` | `true` |

This enables parallel team orchestration with tmux visualization for agent workflows.

Reference Links

### Plugins

- [OpenCode configuration schema](https://opencode.ai/config.json)
- [OpenCode docs](https://opencode.ai/docs/)
- [@nick-vi/opencode-type-inject on npm](https://www.npmjs.com/package/@nick-vi/opencode-type-inject)
- [Oh-My-OpenAgent repository](https://github.com/code-yeongyu/oh-my-openagent)
- [Oh-My-OpenAgent schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json)

### MCPs and Tools

- [MCPProxy](https://github.com/sparfenyuk/mcp-proxy)
- [Model Context Protocol](https://modelcontextprotocol.io/)

### Providers and Services

- [OpenAI-compatible provider package](https://www.npmjs.com/package/@ai-sdk/openai-compatible)
- [Skillless repository](https://github.com/5kahoisaac/skillless)
- [Skillless CLI preset list](https://github.com/5kahoisaac/skillless/blob/main/lists/cli.csv)

### Notes

Reference links reflect currently documented configuration surfaces only. Direct MCPs and providers removed from
`opencode.json` should not be reintroduced here unless configuration changes add them back.
