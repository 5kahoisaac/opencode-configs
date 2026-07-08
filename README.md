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

---

## Available Makefile Commands

The Makefile provides essential commands to manage the OpenCode configuration:

| Command      | Description                                                                                                                                                                   |
|:-------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make sync`  | Sync OpenCode configuration into `~/.config/opencode/`. Copies `AGENTS.md`, JSON config files, and mirrors root `./agents/` and `./commands/` directories if they are present |
| `make help`  | Display available targets and their descriptions                                                                                                                              |
| `make check` | Validate that routed models are reachable through enabled providers and filters, concurrency keys are live, and repo config matches the deployed copy                         |

**Workflow:**

1. Run `make sync` to copy configuration files and any root-level `agents/` or `commands/` files to system locations
2. Use `make help` to see all available commands

The current repository stores project-scoped commands under `.opencode/commands/`; there are no root-level `agents/` or
`commands/` directories at the moment.

---

## Configuration

### Providers

This configuration integrates multiple AI model providers to offer a diverse range of capabilities, from lightweight
fast responses to deep reasoning tasks. The provider setup is designed to balance cost-effectiveness with performance,
utilizing both free and premium models across different use cases.

**Default Model:** `openai/gpt-5.4` (configured in `opencode.json`)

**Small Model:** `openai/gpt-5.4-mini` (configured in `opencode.json`)

#### Provider List

The following AI providers are documented for this setup because they are used by model routing or explicit provider
configuration:

**OpenAI**

OpenAI provides direct API access to GPT-5 family models including `openai/gpt-5.5`, `openai/gpt-5.4`, and
`openai/gpt-5.4-mini`. These models serve as primary and fallback models for several agents including
`hephaestus` (primary: `openai/gpt-5.4` medium, ultrawork: `openai/gpt-5.5` medium), `oracle` (primary:
`openai/gpt-5.5` high), `momus` (primary: `openai/gpt-5.5` xhigh), `prometheus` (primary: `openai/gpt-5.5` high),
`multimodal-looker` (primary: `openai/gpt-5.5` medium), and `sisyphus-junior` (primary: `openai/gpt-5.5` medium),
as well as the `quick`, `writing`, and `unspecified-low` (primary: `openai/gpt-5.4` medium) task categories.

**OpenCode**

OpenCode's built-in model hub offers several models optimized for different task types. The configuration keeps
`opencode/big-pickle` available as a large-context fallback for selected agents and task categories while filtering
paid Zen models from routine provider selection. These models provide a reliable, cost-effective foundation for
high-frequency workflows.

**Z.ai Coding Plan**

Z.ai provides access to advanced GLM models. In this configuration, the GLM family is the primary strategic reasoning
and planning backbone: `zai-coding-plan/glm-5.2` leads for `sisyphus` and `metis` and anchors high-effort fallbacks;
`zai-coding-plan/glm-5.1` backs `atlas` and secondary fallbacks; `zai-coding-plan/glm-5v-turbo` covers multimodal
fallback; and lightweight 4.x variants anchor git workflows, with `zai-coding-plan/glm-4.7` now primary for the
`git` category and `zai-coding-plan/glm-4.5-air` as its fallback.

**NVIDIA**

NVIDIA provides access to models hosted on the NVIDIA AI platform. This configuration uses
`nvidia/minimaxai/minimax-m3` as the primary model for `explore` and `librarian`, with `nvidia/minimaxai/minimax-m2.7`
as the leading fallback and additional fallback use across
`atlas`, `sisyphus-junior`, `quick`, `unspecified-low`, and `writing` routes.

**GitHub Copilot**

GitHub Copilot is used as a routed model provider for selected task categories and fallbacks. The current
`oh-my-openagent.json` configuration references `github-copilot/gemini-3.1-pro-preview` (primary for the
`visual-engineering`
and `artistry` categories, plus high-effort fallbacks for `prometheus`, `oracle`, `momus`, `ultrabrain`, and `deep`),
`github-copilot/gemini-3-flash-preview` (for `explore` and `librarian` fallbacks), and `github-copilot/gpt-5-mini`
(for `quick` and `multimodal-looker` fallbacks). The `github-copilot` whitelist also enables `gpt-4.1`,
`gpt-5.3-codex`, and `gemini-2.5-pro` for direct selection.

**oMLX**

oMLX is configured as a local OpenAI-compatible provider served from `http://127.0.0.1:8080/v1`. It exposes three
manually named MLX-hosted models in `provider.omlx.models` — a Gemma variant (`gemma-4-26b-a4b-it-mlx-8bit`), a Qwen
variant (`qwen3.6-35b-a3b-ud-mlx-4bit`), and a long-context Qwythos build (`qwythos-9b-claude-mythos-5-1m`) — giving
this setup a local inference path alongside hosted providers.

#### Provider Blacklist Strategy

The provider configuration also uses blacklist rules to keep model selection focused and predictable.

**OpenCode Zen blacklist (`provider.opencode.blacklist`)**

This blacklist is maintained to filter paid OpenCode Zen models from the general OpenCode provider roster while keeping
free-tier models available. It is synchronized via `/blacklist-sync` and currently filters 45 paid Zen models across
families including Claude (Fable, Opus, Sonnet 4.x and 5, Haiku 4.x), GPT (5.x, Codex, Nano), Gemini (3.5 Flash,
3.1 Pro, 3 Flash), Grok Build, DeepSeek V4, GLM 5.x, MiniMax M2.x and M3, Kimi K2.x (including K2.7 Code), and
Qwen 3.x so routine workflows stay on the free/default OpenCode path.

#### Models Configuration

The `oh-my-openagent.json` file contains a sophisticated model assignment system that maps specialized agents to
appropriate primary models, fallback models, and optional `ultrawork` models for enhanced capability when needed. This
configuration represents a carefully tuned balance between API rate limits, response quality, and cost management.

**Agent-Specific Model Assignments**

Individual agents from the oh-my-openagent plugin receive specialized model assignments optimized for their specific
functions:

| Source              | Agent Name          | Role                      | Model                         | Variant  | Fallback Models                                                                                            | Description                                                                                                 |
|:--------------------|:--------------------|:--------------------------|:------------------------------|:---------|:-----------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|
| **oh-my-openagent** | `sisyphus`          | Orchestrator              | `zai-coding-plan/glm-5.2`     | `max`    | `openai/gpt-5.5` (medium), `zai-coding-plan/glm-5.1`, `opencode/big-pickle`                                | Primary orchestrator for complex, multi-step tasks                                                          |
| **oh-my-openagent** | `metis`             | Scope Analysis            | `zai-coding-plan/glm-5.2`     | `max`    | `openai/gpt-5.5` (high)                                                                                    | Pre-planning consultation and scope analysis                                                                |
| **oh-my-openagent** | `prometheus`        | Planning Specialist       | `openai/gpt-5.5`              | `high`   | `zai-coding-plan/glm-5.2` (max), `github-copilot/gemini-3.1-pro-preview` (high)                            | Detailed plans and work breakdowns                                                                          |
| **oh-my-openagent** | `atlas`             | Knowledge Specialist      | `zai-coding-plan/glm-5.1`     | `high`   | `openai/gpt-5.5` (medium), `nvidia/minimaxai/minimax-m3`, `nvidia/minimaxai/minimax-m2.7`                  | Knowledge retrieval and architectural context                                                               |
| **oh-my-openagent** | `hephaestus`        | Implementation Specialist | `openai/gpt-5.4`              | `medium` | —                                                                                                          | Executes implementation tasks with balanced capability and efficiency. Ultrawork: `openai/gpt-5.5` (medium) |
| **oh-my-openagent** | `oracle`            | Strategic Advisor         | `openai/gpt-5.5`              | `high`   | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.2` (max), `zai-coding-plan/glm-5.1` | Provides high-level architectural guidance and complex reasoning for critical decisions                     |
| **oh-my-openagent** | `momus`             | Quality Review            | `openai/gpt-5.5`              | `xhigh`  | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.2` (max), `zai-coding-plan/glm-5.1` | Reviews work plans and implementations for quality, completeness, and adherence to best practices           |
| **oh-my-openagent** | `multimodal-looker` | Visual Analysis           | `openai/gpt-5.5`              | `medium` | `zai-coding-plan/glm-5v-turbo`, `github-copilot/gpt-5-mini`                                                | Analyzes visual content, images, and multimodal inputs for comprehensive understanding                      |
| **oh-my-openagent** | `explore`           | Codebase Analysis         | `nvidia/minimaxai/minimax-m3` | —        | `nvidia/minimaxai/minimax-m2.7`, `openai/gpt-5.4-mini`, `github-copilot/gemini-3-flash-preview`            | Performs rapid codebase navigation, pattern detection, and symbol exploration                               |
| **oh-my-openagent** | `librarian`         | Research Specialist       | `nvidia/minimaxai/minimax-m3` | —        | `nvidia/minimaxai/minimax-m2.7`, `openai/gpt-5.4-mini`, `github-copilot/gemini-3-flash-preview`            | Handles documentation lookup, external research, and information retrieval tasks                            |
| **oh-my-openagent** | `sisyphus-junior`   | Lightweight Orchestrator  | `openai/gpt-5.5`              | `medium` | `nvidia/minimaxai/minimax-m3`, `nvidia/minimaxai/minimax-m2.7`, `opencode/big-pickle`                      | Category-optimized task delegation                                                                          |

**Current API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Higher-concurrency providers such as
   OpenCode, Z.ai, and GitHub Copilot handle broader fallback coverage, while tighter limits protect heavier OpenAI
   and NVIDIA routes.

2. **Cost Optimization**: The configuration keeps free OpenCode models available and blacklists paid Zen models that
   should not be selected routinely.

3. **Performance Tiering**: Models are tiered by capability and speed:
    - **Flash Variants** (`*-flash`): Fastest responses, lowest cost, ideal for quick lookups and simple tasks
    - **Standard Variants** (no suffix): Balanced performance for general-purpose work
    - **High/Max Variants**: Enhanced capability for complex reasoning tasks

4. **Suggested Usage Pattern**:
    - Use **@sisyphus** for complex, multistep tasks requiring coordination and agent delegation
    - Use **@sisyphus-junior** for category-optimized task delegation via the task() system
    - Use **@prometheus** for detailed project planning and work breakdowns
    - Use **@explore** for codebase navigation, pattern detection, and symbol lookup
    - Use **@librarian** for documentation research and external API lookup
    - Use **@oracle** for high-stakes architectural decisions and complex reasoning
    - Use **@metis** for task scope analysis and pre-planning consultation
    - Use **@momus** for quality reviews and adherence verification
    - Use **@hephaestus** for implementation tasks and coding workflows
    - Use **@atlas** for knowledge retrieval and architectural context
    - Use **@multimodal-looker** for visual content analysis and image understanding
    - Use **Task Categories** (`visual-engineering`, `ultrabrain`, `quick`, `writing`) for automatic model routing
    - Reserve **High-effort Routes** (`high`, `xhigh`, `max`, and `ultrawork`) for tasks where quality is critical

This configuration represents a personalized setup balancing performance, cost, and reliability based on individual
usage patterns and provider strengths.

**Task Category Model Assignments**

The `oh-my-openagent.json` configuration also defines task category model assignments that automatically route tasks to
appropriate models based on their category:

| Category             | Model                                   | Variant  | Fallback Models                                                                                                                      | Description                                                         |
|:---------------------|:----------------------------------------|:---------|:-------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------|
| `visual-engineering` | `github-copilot/gemini-3.1-pro-preview` | `high`   | `zai-coding-plan/glm-5.2` (max), `zai-coding-plan/glm-5.1`                                                                           | Frontend, UI/UX, design, styling, and animation tasks               |
| `artistry`           | `github-copilot/gemini-3.1-pro-preview` | `high`   | `openai/gpt-5.5`                                                                                                                     | Complex problem-solving with unconventional, creative approaches    |
| `ultrabrain`         | `openai/gpt-5.5`                        | `xhigh`  | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.2` (max), `zai-coding-plan/glm-5.1`                           | Hard logic-heavy tasks requiring deep reasoning                     |
| `deep`               | `openai/gpt-5.5`                        | `medium` | `github-copilot/gemini-3.1-pro-preview` (high)                                                                                       | Goal-oriented autonomous problem-solving with thorough research     |
| `quick`              | `openai/gpt-5.4-mini`                   | —        | `github-copilot/gemini-3-flash-preview`, `nvidia/minimaxai/minimax-m3`, `nvidia/minimaxai/minimax-m2.7`, `github-copilot/gpt-5-mini` | Trivial tasks, single file changes, typo fixes                      |
| `unspecified-low`    | `openai/gpt-5.4`                        | `medium` | `nvidia/minimaxai/minimax-m3`, `nvidia/minimaxai/minimax-m2.7`                                                                       | Low-effort tasks that don't fit other categories                    |
| `unspecified-high`   | `openai/gpt-5.5`                        | `high`   | `zai-coding-plan/glm-5.2` (max), `zai-coding-plan/glm-5.1`                                                                           | High-effort tasks that don't fit other categories                   |
| `writing`            | `openai/gpt-5.4-mini`                   | —        | `zai-coding-plan/glm-5.1`, `nvidia/minimaxai/minimax-m3`, `nvidia/minimaxai/minimax-m2.7`                                            | Documentation, prose, and technical writing tasks                   |
| `git`                | `zai-coding-plan/glm-4.7`               | —        | `zai-coding-plan/glm-4.5-air`, `opencode/big-pickle`                                                                                 | All git operations with focus on atomic commits and safe operations |

These category assignments enable intelligent task routing, ensuring each type of work is handled by the most suitable
model for optimal results.

**Background Task Configuration**

The `oh-my-openagent.json` file includes sophisticated background task management settings:

| Setting                                 | Value | Description                                               |
|:----------------------------------------|:------|:----------------------------------------------------------|
| `defaultConcurrency`                    | 5     | Default number of concurrent background tasks             |
| `staleTimeoutMs`                        | 60000 | Timeout in milliseconds before a task is considered stale |
| **Provider Concurrency**                |       | Per-provider task limits for rate limit management        |
| `omlx`                                  | 1     | Maximum concurrent tasks for oMLX provider                |
| `nvidia`                                | 3     | Maximum concurrent tasks for NVIDIA provider              |
| `openai`                                | 5     | Maximum concurrent tasks for OpenAI provider              |
| `opencode`                              | 10    | Maximum concurrent tasks for OpenCode provider            |
| `zai-coding-plan`                       | 10    | Maximum concurrent tasks for Z.ai provider                |
| `github-copilot`                        | 10    | Maximum concurrent tasks for GitHub Copilot provider      |
| **Model Concurrency**                   |       | Per-model fine-grained concurrency limits                 |
| `openai/gpt-5.5`                        | 2     | Concurrency limit for OpenAI GPT-5.5                      |
| `openai/gpt-5.4`                        | 5     | Concurrency limit for OpenAI GPT-5.4                      |
| `openai/gpt-5.4-mini`                   | 10    | Concurrency limit for OpenAI GPT-5.4-mini                 |
| `github-copilot/gemini-2.5-pro`         | 2     | Concurrency limit for GitHub Copilot Gemini 2.5 Pro       |
| `github-copilot/gemini-3-flash-preview` | 5     | Concurrency limit for GitHub Copilot Gemini 3 Flash       |
| `github-copilot/gemini-3.1-pro-preview` | 2     | Concurrency limit for GitHub Copilot Gemini 3.1 Pro       |
| `zai-coding-plan/glm-4.5-air`           | 5     | Concurrency limit for GLM-4.5-air model                   |
| `zai-coding-plan/glm-4.7`               | 2     | Concurrency limit for GLM-4.7 model                       |
| `zai-coding-plan/glm-5-turbo`           | 1     | Concurrency limit for GLM-5-turbo model                   |
| `zai-coding-plan/glm-5v-turbo`          | 1     | Concurrency limit for GLM-5v-turbo model                  |
| `zai-coding-plan/glm-5.1`               | 10    | Concurrency limit for GLM-5.1 model                       |
| `zai-coding-plan/glm-5.2`               | 10    | Concurrency limit for GLM-5.2 model                       |

**Runtime Fallback Configuration**

Automatic fallback system for handling API errors and maintaining workflow continuity:

| Setting                 | Value              | Description                                                |
|:------------------------|:-------------------|:-----------------------------------------------------------|
| `enabled`               | true               | Enable automatic fallback on errors                        |
| `max_fallback_attempts` | 3                  | Maximum number of fallback attempts per request            |
| `cooldown_seconds`      | 60                 | Cooldown period between fallback attempts                  |
| `timeout_seconds`       | 30                 | Request timeout threshold                                  |
| `notify_on_fallback`    | true               | Notify user when fallback occurs                           |
| **Retry on Errors**     |                    | HTTP status codes that trigger fallback                    |
|                         | 400, 401, 429, 503, 529 | Bad Request, Unauthorized, Rate Limited, Service Unavailable, Overloaded |

This configuration ensures robust operation by automatically switching to fallback models when primary models encounter
rate limits or service issues, maintaining workflow continuity without manual intervention.

### Plugins

The OpenCode configuration utilizes several plugins to extend its core functionality. These plugins are defined in
`opencode.json` configuration file and provide integration with external services and additional features.

**oh-my-openagent@latest**

The oh-my-openagent plugin is a comprehensive agent collection for OpenCode that provides a full suite of specialized
agents for various development tasks. This plugin delivers a robust set of agents optimized for efficient task
delegation, complex problem-solving, and comprehensive development workflows. The oh-my-openagent suite includes agents
for orchestration, exploration, strategic decision-making, visual engineering, research, and more, providing
enterprise-grade capabilities for demanding development scenarios.

**@nick-vi/opencode-type-inject@latest**

The type-inject plugin provides advanced type inference and injection capabilities for OpenCode. This plugin enhances
the AI's understanding of type systems across different programming languages, enabling more accurate code completion
and type-aware refactoring operations. It integrates with OpenCode's language server protocol to provide real-time type
information and suggestions.

---

## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations.
This repository now keeps OpenCode's local MCP surface intentionally small. OpenCode connects to two local MCPs:
the `mcp-proxy` endpoint for shared MCP servers used across OpenCode, Claude Code, Codex, and other AI agents, and a
`headroom` MCP for content compression that shrinks large tool outputs before they reach the model context. The one
intentional exception is Oh-My-OpenAgent's custom `lsp` MCP, which remains plugin-managed because it does not have a
public standalone MCPProxy configuration.

### Manually Configured MCPs

The following MCPs are explicitly configured in `opencode.json`:

**mcp-proxy**

OpenCode connects to MCPProxy through the local remote endpoint `http://127.0.0.1:8081/mcp`. MCPProxy is the shared MCP
control plane for this workstation and exposes the actual upstream MCP servers through one OpenCode entrypoint. This
avoids duplicating MCP configuration across multiple AI coding tools.

The proxy configuration currently includes these upstream MCP servers:

| Upstream MCP      | Status   | Protocol | Purpose                                                                              |
|:------------------|:---------|:---------|:-------------------------------------------------------------------------------------|
| `ast_grep`        | Enabled  | stdio    | AST-aware code search and structural matching                                        |
| `atlassian`       | Enabled  | stdio    | Jira and Confluence access through `mcp-atlassian`                                   |
| `codebase-memory` | Enabled  | stdio    | Knowledge-graph code intelligence: semantic search, trace, and architecture overview |
| `figma`           | Disabled | HTTP     | Figma desktop MCP endpoint at `http://127.0.0.1:3845/mcp`                            |
| `github`          | Enabled  | HTTP     | GitHub Copilot MCP remote endpoint at `https://api.githubcopilot.com/mcp`            |
| `grep_app`        | Enabled  | HTTP     | Public GitHub code search through grep.app                                           |
| `serena`          | Enabled  | stdio    | LSP-precise code intelligence: exact symbols, references, rename, diagnostics        |
| `vision`          | Enabled  | stdio    | Z.ai vision MCP for image and visual-content analysis                                |

MCPProxy also enables management, keyword-based tool search/routing, quarantine, metrics, observability, OAuth support,
sensitive-data detection, and registry discovery. The search layer acts as a real lazy-load mechanism: agents retrieve
only the MCP tools needed for the current task instead of loading every available tool into the prompt. Docker isolation
is configured but disabled globally in the proxy configuration.

**headroom**

OpenCode also runs a local `headroom` MCP (stdio, launched via `headroom mcp serve`) backed by the `headroom-ai`
Python package. It exposes compression, retrieval, and stats tools that shrink large tool outputs (file contents,
search results, command logs) into token-optimized summaries before they are injected into the model context, with
the original content retrievable on demand by hash. This keeps long sessions within context limits without losing
access to the underlying evidence. Unlike `mcp-proxy`, headroom is a single-purpose local MCP and does not proxy
upstream MCP servers.

#### Code Intelligence (MCPProxy `retrieve_tools` mode)

Three code-intelligence upstreams (`ast_grep`, `serena`, `codebase-memory`) coexist behind MCPProxy. They are
complementary, not overlapping, and the `retrieve_tools` routing mode surfaces the right backend per query. To avoid
duplicate tool surfaces during a session, individual tools are toggled on/off as needed. The routing rules below mirror
`AGENTS.md`:

**Query by intent — the right backend surfaces via BM25:**

| Intent                                                                      | Backend                |
|:----------------------------------------------------------------------------|:-----------------------|
| Exact symbol, references, implementations, rename, safe-delete, diagnostics | `serena` (LSP-precise) |
| Fuzzy / natural-language / semantic discovery                               | `codebase-memory`      |
| Callers, callees, data-flow, cross-service, blast-radius, complexity        | `codebase-memory`      |
| Structural AST pattern, find-by-shape, debug a pattern                      | `ast_grep`             |
| Architecture overview, clusters, ADR                                        | `codebase-memory`      |

**Init once per repo before any code-intel query:**

- `serena`: `activate_project` (one project at a time; re-activate on repo switch)
- `codebase-memory`: `index_repository`
- `ast_grep`: no init required

`codebase-memory-mcp` was added to MCPProxy for its persistent tree-sitter knowledge graph and sub-millisecond
structural queries, giving better performance and token efficiency on semantic and architectural queries while `serena`
remains the source of truth for LSP-precise symbol edits.

### Plugin-Provided MCP Status

The oh-my-openagent plugin MCPs have been removed from normal local ownership and moved to
MCPProxy where possible. The retained exception is Oh-My-OpenAgent's custom `lsp` MCP.

| Source               | Configuration File     | Current Routing                                      |
|:---------------------|:-----------------------|:-----------------------------------------------------|
| oh-my-openagent      | `oh-my-openagent.json` | Use MCPProxy for moved MCPs; keep plugin `lsp` MCP   |
| Claude Code override | `oh-my-openagent.json` | Avoid duplicate Claude Code plugin bridge activation |

This means the plugin agents remain available, MCPProxy is the source of truth for shared MCP server configuration, and
`lsp` remains the only intentionally plugin-managed OMO MCP.

#### Disabled OMO MCPs

The `disabled_mcps` array in `oh-my-openagent.json` explicitly turns off MCPs that Oh-My-OpenAgent would otherwise
activate internally. Each entry is disabled because the same capability is now provided through MCPProxy or a CLI
preset, avoiding duplicate tool surfaces across coding agents.

| Disabled MCP | Reason                                                                                      |
|:-------------|:--------------------------------------------------------------------------------------------|
| `context7`   | Replaced by CLI-based library documentation lookup (Skillless CLI preset)                   |
| `websearch`  | Replaced by CLI-based web search workflows (Skillless CLI preset)                           |
| `ast_grep`   | Provided by MCPProxy upstream `ast_grep`                                                    |
| `grep_app`   | Provided by MCPProxy upstream `grep_app`                                                    |
| `codegraph`  | Disabled in favor of the knowledge-graph backend exposed through MCPProxy `codebase-memory` |

---

## Commands

Project-scoped custom slash commands live in `.opencode/commands/`. The current repository has two project-scoped
commands and no root-level `./commands/` directory. The `make sync` command will still mirror a root `./commands/`
directory into the system config if one is added later.

### /blacklist-sync

The `/blacklist-sync` command dynamically synchronizes the OpenCode Zen provider blacklist. On each run it re-derives
pricing and model membership from official sources so the blacklist stays accurate as the provider ships new models
without requiring manual updates.

| Provider   | Blacklist Criteria                                  |
|:-----------|:----------------------------------------------------|
| `opencode` | Paid Zen models (free-tier models always preserved) |

**Source:** `.opencode/commands/blacklist-sync.md`

### /readme-sync

The `/readme-sync` command synchronizes this README with the current OpenCode configuration files. It scans
`opencode.json`, `oh-my-openagent.json`, root JSON files, the Makefile, and local command or agent directories, then
updates only the README sections that drift from the actual configuration.

**Source:** `.opencode/commands/readme-sync.md`

### TUI Configuration

The `tui.json` file contains the Terminal User Interface configuration for OpenCode:

**Current Configuration:**

- **Theme**: `opencode` - Uses the default OpenCode theme for the terminal interface

This minimal configuration enables the standard OpenCode TUI experience. Additional TUI customization options can be
added to this file as needed.

---

## Agents

OpenCode employs a sophisticated agent system where specialized AI agents handle different types of tasks. The agent
architecture enables parallel task execution, context-aware processing, and delegation based on task complexity and
requirements.

There are no repo-local `agents/` or `.opencode/agents/` files in this project at the moment. The agents documented
below are provided by configured plugins.

#### Oh-My-OpenAgent Agents

The oh-my-openagent plugin provides a comprehensive suite of specialized agents designed for various development tasks:

**Core Agents:**

- **@sisyphus** - The primary orchestrator that coordinates complex, multi-step tasks with heavy planning and parallel
  execution potential. Sisyphus manages agent delegation workflows and ensures tasks are routed to the most appropriate
  specialist agents.

- **@sisyphus-junior** - Lightweight orchestrator that serves as the backing agent for all `task()` category
  delegations (e.g., `visual-engineering`, `ultrabrain`, `quick`). Runs on a faster model than the full Sisyphus,
  optimized for category-specific task execution.

- **@hephaestus** - Implementation specialist that executes well-defined coding tasks with efficiency and precision.
  Hephaestus excels at translating plans into working code and handling technical implementations.

- **@oracle** - Strategic advisor that provides high-level architectural guidance and complex reasoning for high-stakes
  decisions. Oracle is consulted for critical architectural choices and difficult technical problems.

- **@librarian** - Research specialist that handles external documentation lookup, API research, and library information
  retrieval. Librarian maintains up-to-date knowledge of libraries, frameworks, and best practices.

- **@explore** - Codebase analysis agent that performs rapid navigation, pattern detection, and symbol exploration
  across the entire codebase. Explore is optimized for finding code patterns and understanding existing implementations.

- **@multimodal-looker** - Visual analysis agent specialized in processing images, screenshots, diagrams, and visual
  content. This agent enables understanding of visual inputs alongside code and text.

**Planning & Quality Agents:**

- **@prometheus** - Planning specialist that creates detailed work breakdowns and project plans for complex
  implementations. Prometheus structures tasks into manageable units with clear dependencies and execution order.

- **@metis** - Scope analysis agent that analyzes task requirements, identifies ambiguities, and provides pre-planning
  consultation. Metis helps clarify requirements before implementation begins.

- **@momus** - Quality review agent that evaluates work plans and implementations against rigorous standards. Momus
  ensures completeness, verifiability, and adherence to best practices.

- **@atlas** - Knowledge specialist that manages and retrieves contextual information, architectural decisions, and
  project conventions. Atlas maintains the project's accumulated wisdom and helps agents access relevant context.

These agents work together to provide comprehensive coverage of development tasks through a sophisticated orchestration
system that matches tasks to the most appropriate specialist.

---

## Team Mode

Oh-My-OpenAgent's team mode is **enabled** in `oh-my-openagent.json`, turning on multi-agent team orchestration on top
of the default `task()` delegation system. When enabled, the `team_*` tool family becomes available and the lead agent
(including Sisyphus) can spawn named agent teams, assign tasks, exchange messages, and shut members down through a
structured closure contract.

**Current Configuration:**

| Setting              | Value | Description                                                                          |
|:---------------------|:------|:-------------------------------------------------------------------------------------|
| `team_mode.enabled`  | true  | Activates `team_*` orchestration tools (team_create, team_task_*, team_send_message) |
| `tmux_visualization` | true  | Renders active team state and member activity in a tmux pane for live observability  |

**What team mode adds:**

- **Named agent teams**: `team_create` spins up a team from a named spec or inline member list, with an optional lead
  agent and per-member category or `subagent_type` routing.
- **Task tracking**: `team_task_create`, `team_task_update`, and `team_task_list` manage per-team work items with owner
  and status fields (`pending`, `claimed`, `in_progress`, `completed`, `deleted`).
- **Member messaging**: `team_send_message` supports direct messages and broadcasts with optional file references.
- **Lifecycle control**: `team_shutdown_request`, `team_approve_shutdown`, and `team_reject_shutdown` implement a
  controlled shutdown flow; `team_delete` tears down completed runs; `team_status` and `team_list` inspect state.
- **Closure contract**: every team the lead opens must be closed by the lead. After each task reaches a terminal state,
  the lead re-checks `team_task_list` and, once all tasks are terminal, runs the full closure sequence (shutdown
  request + approval per active member, then `team_delete`) in the same turn.

Team mode is complementary to the existing `task()` category delegation — category tasks still route through
Sisyphus-Junior, while team mode is used for explicit multi-member orchestration that needs shared task boards and
message passing between agents.

---

## Reference Links

Comprehensive reference mapping for plugins, MCPs, external services, and related resources used in this OpenCode
configuration.

### Plugins

| Plugin Name                       | Status | Official Repository                             | Version | Purpose                                                                   |
|:----------------------------------|:-------|:------------------------------------------------|:--------|:--------------------------------------------------------------------------|
| **oh-my-openagent**               | Active | https://github.com/code-yeongyu/oh-my-openagent | Latest  | Multi-agent orchestration suite for task delegation and complex workflows |
| **@nick-vi/opencode-type-inject** | Active | https://github.com/nick-vi/type-inject          | Latest  | Advanced type inference and language-aware code completion                |

### OpenCode MCP Entrypoint

| MCP Name      | Status  | Source Type     | Source Location             | Documentation                         | Purpose                                                                            |
|:--------------|:--------|:----------------|:----------------------------|:--------------------------------------|:-----------------------------------------------------------------------------------|
| **mcp-proxy** | Enabled | Local HTTP MCP  | `http://127.0.0.1:8081/mcp` | https://docs.mcpproxy.app/            | Shared MCPProxy endpoint for OpenCode and other tools                              |
| **headroom**  | Enabled | Local stdio MCP | `headroom mcp serve`        | https://headroom-docs.vercel.app/docs | Token-optimization MCP for compressing large tool outputs before context injection |

### MCPProxy-Managed Upstreams

| MCP Name            | Status   | Source Type         | Documentation/Source                                                                  | Purpose                                                                       |
|:--------------------|:---------|:--------------------|:--------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|
| **ast_grep**        | Enabled  | Git repository      | https://github.com/ast-grep/ast-grep-mcp                                              | AST-aware code search and structural matching                                 |
| **atlassian**       | Enabled  | Python package      | https://github.com/sooperset/mcp-atlassian                                            | Atlassian Jira and Confluence integration                                     |
| **codebase-memory** | Enabled  | Static binary (C)   | https://github.com/DeusData/codebase-memory-mcp                                       | Knowledge-graph code intelligence: semantic search, trace, architecture       |
| **figma**           | Disabled | Local HTTP endpoint | https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server | Figma design integration and UI code generation                               |
| **github**          | Enabled  | Remote endpoint     | https://api.githubcopilot.com/mcp                                                     | GitHub repository operations, pull requests, issues, and code search          |
| **grep_app**        | Enabled  | Remote endpoint     | https://vercel.com/blog/grep-a-million-github-repositories-via-mcp                    | GitHub code search through grep.app                                           |
| **serena**          | Enabled  | Git repository      | https://github.com/oraios/serena                                                      | LSP-precise code intelligence: exact symbols, references, rename, diagnostics |
| **vision**          | Enabled  | npm package         | https://docs.z.ai/devpack/mcp/vision-mcp-server                                       | Z.ai vision MCP for image understanding and visual analysis                   |

### Plugin-Retained MCPs

| MCP Name | Status  | Source          | Documentation/Source | Purpose                                                                      |
|:---------|:--------|:----------------|:---------------------|:-----------------------------------------------------------------------------|
| **lsp**  | Enabled | oh-my-openagent | Internal plugin MCP  | OMO custom LSP MCP retained because no public standalone proxy config exists |

### External Services & Platforms

| Service                    | URL                                                                        | Purpose                                                                          |
|:---------------------------|:---------------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| **OpenCode Platform**      | https://opencode.ai                                                        | Main OpenCode AI coding assistant platform                                       |
| **OpenCode Models**        | https://opencode.ai/docs/models                                            | Official reference for model configuration and provider selection                |
| **OpenCode Zen**           | https://opencode.ai/docs/zen                                               | Official Zen model hub and pricing roster documentation                          |
| **GitHub Copilot Docs**    | https://docs.github.com/en/copilot                                         | Official GitHub Copilot setup and usage documentation                            |
| **GitHub Models Catalog**  | https://docs.github.com/en/rest/models/catalog                             | Canonical API reference for GitHub-hosted model catalog metadata                 |
| **NVIDIA NIM Docs**        | https://docs.nvidia.com/nim/large-language-models/latest/introduction.html | Official NVIDIA NIM documentation for hosted LLM access and model serving        |
| **OpenAI Platform**        | https://developers.openai.com/api/docs/models                              | Official OpenAI model documentation for GPT-5 family and API reference           |
| **Z.ai Developer Docs**    | https://docs.z.ai/guides/overview/quick-start                              | Official Z.ai documentation for GLM model families and APIs                      |
| **Model Context Protocol** | https://modelcontextprotocol.io/docs/getting-started/intro                 | Open standard for AI-LLM context and tool integration (Anthropic)                |
| **MCPProxy Docs**          | https://docs.mcpproxy.app/                                                 | Official MCPProxy documentation for shared MCP server management and tool search |
| **MCPProxy Routing Modes** | https://docs.mcpproxy.app/features/routing-modes/                          | `retrieve_tools` routing mode docs for token-saving lazy tool retrieval          |
| **MCPProxy Config Gist**   | https://gist.github.com/5kahoisaac/319e1eb499fe5902a93dbe3d7cb0bf1a        | User-maintained MCPProxy upstream configuration reference                        |

### Notes

- **MCPProxy**: `opencode.json` points only at the local MCPProxy endpoint. Upstream MCP details live in the proxy
  configuration, not in OpenCode's local config.
- **MCPProxy Config Gist**: Reference link only; secret values should stay managed by keyring or local MCPProxy config,
  not copied into this README.
- **Figma MCP**: No public implementation repository exists; reference is official Figma documentation only.
- **GitHub MCP**: MCPProxy points at the remote GitHub Copilot MCP endpoint `https://api.githubcopilot.com/mcp`.
- **Atlassian MCP**: Community fork maintained by sooperset; official Atlassian server exists but uses remote HTTP.
- **Vision MCP**: Connects through Z.ai's MCP package for image analysis.
- **OMO `lsp` MCP**: Retained as a plugin-managed MCP because it is custom to Oh-My-OpenAgent and has no public
  standalone MCPProxy configuration.

All URLs verified as of June 2026. Refer to individual repository documentation for latest API changes and version
compatibility.
