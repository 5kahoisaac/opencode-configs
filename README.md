# OpenCode Configuration

## Table of Contents

- [Overview](#overview)
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

## Project Scope

This project scope reminder applies after `v0.5.0`.

The original sync skills feature has been removed from this repository because it has been split into a dedicated
repository: [skillless](https://github.com/5kahoisaac/skillless). This repository only retains OpenCode-specific
configuration files and commands.

The `anthropic` provider and `opencode-with-claude` plugin are increasingly out of scope. **Claude** access is shifting away
from SDK-based integrations, and workflows tend to be more effective when run through **Everything Claude Code (ECC)**
rather than the **Oh-My-OpenAgent** + **Claude** integration.

**Claude** models perform best with a lighter control layer and minimal orchestration. They handle open-ended reasoning well
without heavy prompt scaffolding, and additional orchestration can introduce unnecessary token overhead. In contrast,
**Oh-My-OpenAgent**’s more complex prompt and routing stack may be excessive for **Claude**-centric workflows.

**GPT**-family models remain better suited for structured, bounded tasks where explicit routing, delegation, and tighter
control loops provide clear benefits. Their behavior aligns well with systems that rely on defined task decomposition
and orchestration layers.

---

## Available Makefile Commands

The Makefile provides essential commands to manage the OpenCode configuration:

| Command     | Description                                                                                                                                                                   |
|:------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make sync` | Sync OpenCode configuration into `~/.config/opencode/`. Copies `AGENTS.md`, JSON config files, and mirrors root `./agents/` and `./commands/` directories if they are present |
| `make help` | Display available targets and their descriptions                                                                                                                              |

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

**GitHub Copilot**

GitHub Copilot is used as a routed model provider for selected task categories and fallbacks. The current
`oh-my-openagent.json` configuration references `github-copilot/gemini-3.1-pro-preview`,
`github-copilot/gemini-3-flash-preview`, and `github-copilot/gpt-5-mini`.

These routes give the setup Gemini-backed high-effort coverage plus a lightweight Git-focused model path.

**OpenCode**

OpenCode's built-in model hub offers several models optimized for different task types. The configuration keeps
`opencode/big-pickle` available as a large-context fallback for selected agents and task categories while filtering
paid Zen models from routine provider selection. These models provide a reliable, cost-effective foundation for
high-frequency workflows.

**Z.ai Coding Plan**

Z.ai provides access to advanced GLM models. In this configuration, the GLM family is used for strategic reasoning,
planning, visual fallback coverage, and multimodal fallback coverage, with `zai-coding-plan/glm-5.1`,
`zai-coding-plan/glm-5v-turbo`, and lightweight 4.x variants such as
`zai-coding-plan/glm-4.5-air` assigned across specialist agents and task categories.

**xAI (Grok)**

xAI provides the Grok family of models. In this configuration, non-LLM Grok Imagine image and video generation models
are filtered via `provider.xai.blacklist` so text and coding workflows only see suitable LLM choices.

**oMLX**

oMLX is configured as a local OpenAI-compatible provider served from `http://127.0.0.1:8080/v1`. It exposes two
manually named MLX-hosted Qwen variants in `provider.omlx.models`, giving this setup a local inference path alongside
hosted providers.

**OpenAI**

OpenAI provides direct API access to GPT-5 family models including `openai/gpt-5.5`, `openai/gpt-5.4`,
`openai/gpt-5.4-mini`, `openai/gpt-5.4-nano`, and `openai/gpt-5.3-codex`. These models serve as primary and fallback
models for several agents including `hephaestus` (primary: `openai/gpt-5.4` medium, ultrawork: `openai/gpt-5.5`
medium), `oracle` (primary: `openai/gpt-5.5` high), `momus` (primary: `openai/gpt-5.5` xhigh), and
`multimodal-looker` (primary: `openai/gpt-5.5` medium). Authentication is handled via the `opencode-openai-codex-auth`
plugin.

**NVIDIA**

NVIDIA provides access to models hosted on the NVIDIA AI platform. This configuration uses
`nvidia/minimaxai/minimax-m2.7` as the primary model for `explore` and `librarian`, with additional fallback use in
`atlas`, `sisyphus-junior`, `quick`, `unspecified-low`, and `writing` routes. It also uses
`nvidia/models/z-ai/glm-5.1` as a reasoning fallback for `oracle`, `momus`, and `ultrabrain`.

**DigitalOcean**

DigitalOcean's AI platform provides access to open and partner models used heavily by this configuration. It serves
`digitalocean/kimi-k2.6` as the primary model for `sisyphus`, `atlas`, and `sisyphus-junior`,
`digitalocean/kimi-k2.5` for writing and fallback routes, `digitalocean/glm-5` for visual and high-effort fallbacks,
and `digitalocean/deepseek-3.2` as the fallback for `explore` and `librarian`. Premium `anthropic-*` and `openai-*`
DigitalOcean models are filtered via `provider.digitalocean.blacklist`, while open-source `openai-gpt-oss-*` variants
and other open or partner model families remain available.

#### Provider Blacklist Strategy

The provider configuration also uses blacklist rules to keep model selection focused and predictable.

**OpenCode Zen blacklist (`provider.opencode.blacklist`)**

This blacklist is maintained to filter paid OpenCode Zen models from the general OpenCode provider roster while keeping
free-tier models available. It is synchronized via `/blacklist-sync` and currently filters 41 paid Zen models across
families including Claude (Fable, Opus, Sonnet, Haiku 4.x), GPT (5.x, Codex, Nano), Gemini (3.1 Pro, 3 Flash), Grok
Build, DeepSeek V4, GLM 5.x, MiniMax M2.x, Kimi K2.x, and Qwen 3.x so routine workflows stay on the free/default
OpenCode path.

**xAI blacklist (`provider.xai.blacklist`)**

This blacklist is maintained to keep the xAI model list focused on text and coding workflows. It is synchronized via
`/blacklist-sync` and currently removes 3 non-LLM models: `grok-imagine-image`, `grok-imagine-image-quality`, and
`grok-imagine-video`. Retired Grok 2/3/4 families are not listed because they no longer appear in current authoritative
catalog sources.

**DigitalOcean blacklist (`provider.digitalocean.blacklist`)**

This blacklist filters premium models that require higher account tiers on DigitalOcean's AI platform. It is
synchronized via `/blacklist-sync` and currently blocks 36 models: 15 `anthropic-*` Claude variants and 21 `openai-*`
models. Open-source `openai-gpt-oss-*` variants are preserved through the `oss` substring rule, and open or partner
models from Qwen, DeepSeek, Llama, Mistral, Kimi, GLM, and similar families remain available.

#### Models Configuration

The `oh-my-openagent.json` file contains a sophisticated model assignment system that maps specialized agents to
appropriate primary models, fallback models, and optional `ultrawork` models for enhanced capability when needed. This
configuration represents a carefully tuned balance between API rate limits, response quality, and cost management.

**Agent-Specific Model Assignments**

Individual agents from the oh-my-openagent plugin receive specialized model assignments optimized for their specific
functions:

| Source                 | Agent Name          | Role                      | Model                           | Variant  | Fallback Models                                                                                         | Description                                                                                                 |
|:-----------------------|:--------------------|:--------------------------|:--------------------------------|:---------|:--------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|
| **oh-my-openagent**    | `sisyphus`          | Orchestrator              | `digitalocean/kimi-k2.6`        | —        | `openai/gpt-5.5` (medium), `digitalocean/glm-5`, `opencode/big-pickle`                                  | Primary orchestrator for complex, multi-step tasks                                                          |
| **oh-my-openagent**    | `metis`             | Scope Analysis            | `openai/gpt-5.5`                | `high`   | `zai-coding-plan/glm-5.1`, `digitalocean/kimi-k2.5`                                                     | Pre-planning consultation and scope analysis                                                                |
| **oh-my-openagent**    | `prometheus`        | Planning Specialist       | `openai/gpt-5.5`                | `high`   | `zai-coding-plan/glm-5.1`, `github-copilot/gemini-3.1-pro-preview`                                      | Detailed plans and work breakdowns                                                                          |
| **oh-my-openagent**    | `atlas`             | Knowledge Specialist      | `digitalocean/kimi-k2.6`        | —        | `openai/gpt-5.5` (medium), `nvidia/minimaxai/minimax-m2.7`                                              | Knowledge retrieval and architectural context                                                               |
| **oh-my-openagent**    | `sisyphus-junior`   | Lightweight Orchestrator  | `digitalocean/kimi-k2.6`        | —        | `openai/gpt-5.5` (medium), `nvidia/minimaxai/minimax-m2.7`, `opencode/big-pickle`                       | Category-optimized task delegation                                                                          |
| **oh-my-openagent**    | `hephaestus`        | Implementation Specialist | `openai/gpt-5.4`                | `medium` | —                                                                                                       | Executes implementation tasks with balanced capability and efficiency. Ultrawork: `openai/gpt-5.5` (medium) |
| **oh-my-openagent**    | `oracle`            | Strategic Advisor         | `openai/gpt-5.5`                | `high`   | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.1`, `nvidia/models/z-ai/glm-5.1` | Provides high-level architectural guidance and complex reasoning for critical decisions                     |
| **oh-my-openagent**    | `momus`             | Quality Review            | `openai/gpt-5.5`                | `xhigh`  | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.1`, `nvidia/models/z-ai/glm-5.1` | Reviews work plans and implementations for quality, completeness, and adherence to best practices           |
| **oh-my-openagent**    | `multimodal-looker` | Visual Analysis           | `openai/gpt-5.5`                | `medium` | `digitalocean/kimi-k2.6`, `zai-coding-plan/glm-5v-turbo`                                                | Analyzes visual content, images, and multimodal inputs for comprehensive understanding                      |
| **oh-my-openagent**    | `explore`           | Codebase Analysis         | `nvidia/minimaxai/minimax-m2.7` | —        | `digitalocean/deepseek-3.2`, `openai/gpt-5.4-mini`, `openai/gpt-5.4-nano`                               | Performs rapid codebase navigation, pattern detection, and symbol exploration                               |
| **oh-my-openagent**    | `librarian`         | Research Specialist       | `nvidia/minimaxai/minimax-m2.7` | —        | `digitalocean/deepseek-3.2`, `openai/gpt-5.4-mini`, `openai/gpt-5.4-nano`                               | Handles documentation lookup, external research, and information retrieval tasks                            |
| **opencode-historian** | `historian`         | Memory Management         | `openai/gpt-5.4-mini`           | —        | —                                                                                                       | Manages persistent memories, context retention, and semantic search across project knowledge base           |

**Current API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Higher-concurrency providers such as
   DigitalOcean, OpenCode, and Z.ai handle broader fallback coverage, while tighter limits protect heavier OpenAI,
   NVIDIA, and GitHub Copilot routes.

2. **Cost Optimization**: The configuration keeps free OpenCode models available, uses DigitalOcean open and partner
   models heavily, and blacklists paid Zen plus premium DigitalOcean models that should not be selected routinely.

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

| Category             | Model                                   | Variant  | Fallback Models                                                                                           | Description                                                         |
|:---------------------|:----------------------------------------|:---------|:----------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------|
| `visual-engineering` | `github-copilot/gemini-3.1-pro-preview` | `high`   | `digitalocean/glm-5`, `zai-coding-plan/glm-5.1`, `nvidia/models/z-ai/glm-5.1`, `digitalocean/kimi-k2.5`   | Frontend, UI/UX, design, styling, and animation tasks               |
| `artistry`           | `github-copilot/gemini-3.1-pro-preview` | `high`   | `openai/gpt-5.5`                                                                                          | Complex problem-solving with unconventional, creative approaches    |
| `ultrabrain`         | `openai/gpt-5.5`                        | `xhigh`  | `github-copilot/gemini-3.1-pro-preview` (high), `zai-coding-plan/glm-5.1`, `nvidia/models/z-ai/glm-5.1`   | Hard logic-heavy tasks requiring deep reasoning                     |
| `deep`               | `openai/gpt-5.5`                        | `medium` | `github-copilot/gemini-3.1-pro-preview` (high)                                                            | Goal-oriented autonomous problem-solving with thorough research     |
| `quick`              | `openai/gpt-5.4-mini`                   | —        | `github-copilot/gemini-3-flash-preview`, `nvidia/minimaxai/minimax-m2.7`, `opencode/big-pickle`           | Trivial tasks, single file changes, typo fixes                      |
| `unspecified-low`    | `digitalocean/kimi-k2.6`                | —        | `openai/gpt-5.3-codex` (medium), `github-copilot/gemini-3-flash-preview`, `nvidia/minimaxai/minimax-m2.7` | Low-effort tasks that don't fit other categories                    |
| `unspecified-high`   | `openai/gpt-5.5`                        | `high`   | `digitalocean/glm-5`, `digitalocean/kimi-k2.5`                                                            | High-effort tasks that don't fit other categories                   |
| `writing`            | `digitalocean/kimi-k2.5`                | —        | `github-copilot/gemini-3-flash-preview`, `digitalocean/kimi-k2.6`, `nvidia/minimaxai/minimax-m2.7`        | Documentation, prose, and technical writing tasks                   |
| `git`                | `github-copilot/gpt-5-mini`             | —        | `opencode/big-pickle`, `zai-coding-plan/glm-4.5-air`                                                      | All git operations with focus on atomic commits and safe operations |

These category assignments enable intelligent task routing, ensuring each type of work is handled by the most suitable
model for optimal results.

**Background Task Configuration**

The `oh-my-openagent.json` file includes sophisticated background task management settings:

| Setting                        | Value | Description                                               |
|:-------------------------------|:------|:----------------------------------------------------------|
| `defaultConcurrency`           | 5     | Default number of concurrent background tasks             |
| `staleTimeoutMs`               | 60000 | Timeout in milliseconds before a task is considered stale |
| **Provider Concurrency**       |       | Per-provider task limits for rate limit management        |
| `omlx`                         | 1     | Maximum concurrent tasks for oMLX provider                |
| `xai`                          | 5     | Maximum concurrent tasks for xAI provider                 |
| `nvidia`                       | 3     | Maximum concurrent tasks for NVIDIA provider              |
| `openai`                       | 5     | Maximum concurrent tasks for OpenAI provider              |
| `opencode`                     | 10    | Maximum concurrent tasks for OpenCode provider            |
| `zai-coding-plan`              | 10    | Maximum concurrent tasks for Z.ai provider                |
| `digitalocean`                 | 3     | Maximum concurrent tasks for DigitalOcean provider        |
| `github-copilot`               | 5     | Maximum concurrent tasks for GitHub Copilot provider      |
| **Model Concurrency**          |       | Per-model fine-grained concurrency limits                 |
| `openai/gpt-5.5`               | 1     | Concurrency limit for OpenAI GPT-5.5                      |
| `openai/gpt-5.4`               | 2     | Concurrency limit for OpenAI GPT-5.4                      |
| `openai/gpt-5.3-codex`         | 3     | Concurrency limit for OpenAI GPT-5.3-codex                |
| `openai/gpt-5.4-mini`          | 5     | Concurrency limit for OpenAI GPT-5.4-mini                 |
| `openai/gpt-5.4-nano`          | 8     | Concurrency limit for OpenAI GPT-5.4-nano                 |
| `zai-coding-plan/glm-4.5-air`  | 5     | Concurrency limit for GLM-4.5-air model                   |
| `zai-coding-plan/glm-4.7`      | 2     | Concurrency limit for GLM-4.7 model                       |
| `zai-coding-plan/glm-5-turbo`  | 1     | Concurrency limit for GLM-5-turbo model                   |
| `zai-coding-plan/glm-5v-turbo` | 1     | Concurrency limit for GLM-5v-turbo model                  |
| `zai-coding-plan/glm-5.1`      | 10    | Concurrency limit for GLM-5.1 model                       |

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
|                         | 400, 429, 503, 529 | Bad Request, Rate Limited, Service Unavailable, Overloaded |

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

**opencode-openai-codex-auth@latest**

The `opencode-openai-codex-auth` plugin provides authentication for the OpenAI provider, enabling direct API access to
OpenAI's GPT-5 family models. This plugin handles API key management and authentication flows required for the `openai`
provider configured in `opencode.json`, which is used as the primary model source for several agents including
`hephaestus`, `oracle`, `momus`, and `multimodal-looker`.

**opencode-historian@latest**

The historian plugin provides persistent memory management capabilities for OpenCode, enabling context retention and
compounded engineering practices across sessions. This plugin allows agents to store, recall, and manage memories
including architectural decisions, design patterns, learnings, preferences, issues, and contextual information. The
historian system automatically classifies memory types and manages circular references between related memories,
creating a knowledge base that persists beyond individual conversations.

---

## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations.
This configuration includes manually configured MCPs and pre-installed MCPs from the oh-my-openagent and
opencode-historian plugins.

### Manually Configured MCPs

The following MCPs are explicitly configured in `opencode.json` file:

**figma** *(disabled)*

The Figma MCP enables seamless integration with Figma for design-related operations.
This MCP allows OpenCode to interact with Figma's desktop application, enabling design context retrieval,
UI code generation, and design system exploration directly from Figma files. Currently disabled in configuration.

**github**

The GitHub MCP provides comprehensive integration with GitHub for repository operations,
pull request management, issue tracking, and code search.
This MCP enables OpenCode to interact with GitHub through the GitHub Copilot MCP remote endpoint
(`https://api.githubcopilot.com/mcp`) for repository and development workflows directly from the conversation
interface.

**atlassian** *(disabled)*

The Atlassian MCP integrates with Atlassian Jira for project management operations including issue tracking,
sprint management, and workflow automation. This MCP connects to both Jira and Confluence,
enabling seamless access to project management data. Currently disabled in configuration.

**vision**

The Vision MCP provides visual analysis capabilities through Z.ai's vision models. This MCP enables image understanding,
visual content analysis, and image-based reasoning tasks. It connects to Z.ai's vision API to process and analyze
visual inputs alongside code and text.

### Pre-installed MCPs from opencode-historian

The opencode-historian plugin includes the Serena MCP server:

**serena**

The Serena MCP server provides advanced code intelligence capabilities including precise symbol navigation,
semantic search, and AST-aware code operations. This MCP is essential for code symbol manipulation and
enables token-efficient code retrieval and modifications. It is automatically available when the
opencode-historian plugin is enabled.

### Pre-installed MCPs from Oh-My-OpenAgent

The oh-my-openagent plugin includes three pre-configured MCP servers that provide essential development tools:

| MCP         | Purpose                         | Default Assignment                    |
|-------------|---------------------------------|---------------------------------------|
| `websearch` | Real-time web search via Exa AI | `sisyphus`, `librarian`, `prometheus` |
| `context7`  | Official library documentation  | `librarian`                           |
| `grep_app`  | GitHub code search via grep.app | `oracle`                              |

**MCP Descriptions:**

- **websearch** - Provides real-time web search capabilities via Exa AI. This MCP enables agents to search for current
  information, documentation, and code examples from across the web.

- **context7** - Provides access to up-to-date official documentation and code examples for various libraries and
  frameworks. This MCP fetches version-specific documentation directly from the source, ensuring accurate and current
  information for library usage and API references.

- **grep_app** - Enables ultra-fast code search across millions of public GitHub repositories. This MCP allows agents to
  search for code patterns, find real-world implementation examples, and discover how others have solved similar
  problems.

These pre-installed MCPs are automatically available when the oh-my-openagent plugin is enabled. MCP access is
controlled
via per-agent permissions in the configuration. See
the [official documentation](https://github.com/code-yeongyu/oh-my-openagent/blob/master/docs/configurations.md) for
details on MCP assignment syntax and configuration options.

---

## Commands

Project-scoped custom slash commands live in `.opencode/commands/`. The current repository has two project-scoped
commands and no root-level `./commands/` directory. The `make sync` command will still mirror a root `./commands/`
directory into the system config if one is added later.

### /blacklist-sync

The `/blacklist-sync` command dynamically synchronizes the OpenCode provider blacklists for xAI, OpenCode Zen, and
DigitalOcean. On each run it re-derives flagship status, pricing, and model membership from official sources so the
blacklist stays accurate as providers ship new models without requiring manual updates.

| Provider       | Blacklist Criteria                                                                                                |
|:---------------|:------------------------------------------------------------------------------------------------------------------|
| `xai`          | Non-LLM/multimodal models + models from outdated families (coding models always preserved)                        |
| `opencode`     | Paid Zen models (free-tier models always preserved)                                                               |
| `digitalocean` | Premium Anthropic Claude + premium OpenAI GPT/o-series models (open-source `gpt-oss-*` variants always preserved) |

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

#### OpenCode-Historian Agent

The opencode-historian plugin provides a specialized agent for persistent memory management:

**@historian - Memory Management Specialist**

The historian agent manages persistent memories, enabling context retention and compounded engineering practices across
sessions. It stores, recalls, and manages project knowledge including architectural decisions, design patterns,
learnings, preferences, issues, and contextual information.

**Key capabilities:**

- **Memory Storage**: Stores project decisions, learnings, and context that persist across sessions
- **Semantic Search**: Retrieves relevant memories using keyword or semantic search
- **Memory Classification**: Automatically categorizes memories by type (architectural decisions, conventions,
  preferences, context)
- **Cross-Reference Management**: Handles circular references between related memories

The historian agent uses the `openai/gpt-5.4-mini` model configured in `opencode-historian.json` for fast,
efficient memory operations.


---

## Reference Links

Comprehensive reference mapping for plugins, MCPs, external services, and related resources used in this OpenCode
configuration.

### Plugins

| Plugin Name                       | Status | Official Repository                                      | Version | Purpose                                                                   |
|:----------------------------------|:-------|:---------------------------------------------------------|:--------|:--------------------------------------------------------------------------|
| **oh-my-openagent**               | Active | https://github.com/code-yeongyu/oh-my-openagent          | Latest  | Multi-agent orchestration suite for task delegation and complex workflows |
| **@nick-vi/opencode-type-inject** | Active | https://github.com/nick-vi/type-inject                   | Latest  | Advanced type inference and language-aware code completion                |
| **opencode-openai-codex-auth**    | Active | https://github.com/numman-ali/opencode-openai-codex-auth | Latest  | OpenAI provider authentication for direct API access                      |
| **opencode-historian**            | Active | https://github.com/5kahoisaac/opencode-historian         | Latest  | Persistent memory management and semantic search across project knowledge |

### Manually Configured MCPs

| MCP Name      | Status   | Source Type     | Source Location                                                                       | Purpose                                                                        |
|:--------------|:---------|:----------------|:--------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| **figma**     | Disabled | Official Docs   | https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server | Figma design integration and UI code generation                                |
| **github**    | Enabled  | Remote Endpoint | api.githubcopilot.com (GitHub Copilot MCP)                                            | GitHub API integration for repository operations, PRs, issues, and code search |
| **atlassian** | Disabled | Community Fork  | https://github.com/sooperset/mcp-atlassian                                            | Atlassian Jira and Confluence integration (maintained community fork)          |
| **vision**    | Active   | Official Docs   | https://docs.z.ai/devpack/mcp/vision-mcp-server                                       | Z.ai vision MCP for image understanding and visual analysis                    |

### Pre-installed MCPs (oh-my-openagent)

| MCP Name      | Purpose                        | Service Provider | Documentation/Source                                                                             |
|:--------------|:-------------------------------|:-----------------|:-------------------------------------------------------------------------------------------------|
| **websearch** | Real-time web search           | Exa AI           | https://exa.ai/docs/reference/exa-mcp - Official Exa MCP documentation                           |
| **context7**  | Official library documentation | Upstash          | https://context7.com/docs  - Official Context7 documentation and MCP reference                   |
| **grep_app**  | GitHub code search             | grep.app         | https://vercel.com/blog/grep-a-million-github-repositories-via-mcp - Grep MCP overview and setup |

### Pre-installed MCPs (opencode-historian)

| MCP Name   | Purpose                                                  | Source Repository                |
|:-----------|:---------------------------------------------------------|:---------------------------------|
| **serena** | Advanced code intelligence (LSP, symbol navigation, AST) | https://github.com/oraios/serena |

### External Services & Platforms

| Service                    | URL                                                                        | Purpose                                                                   |
|:---------------------------|:---------------------------------------------------------------------------|:--------------------------------------------------------------------------|
| **OpenCode Platform**      | https://opencode.ai                                                        | Main OpenCode AI coding assistant platform                                |
| **OpenCode Models**        | https://opencode.ai/docs/models                                            | Official reference for model configuration and provider selection         |
| **OpenCode Zen**           | https://opencode.ai/docs/zen                                               | Official Zen model hub and pricing roster documentation                   |
| **GitHub Copilot Docs**    | https://docs.github.com/en/copilot                                         | Official GitHub Copilot setup and usage documentation                     |
| **GitHub Models Catalog**  | https://docs.github.com/en/rest/models/catalog                             | Canonical API reference for GitHub-hosted model catalog metadata          |
| **NVIDIA NIM Docs**        | https://docs.nvidia.com/nim/large-language-models/latest/introduction.html | Official NVIDIA NIM documentation for hosted LLM access and model serving |
| **OpenAI Platform**        | https://developers.openai.com/api/docs/models                              | Official OpenAI model documentation for GPT-5 family and API reference    |
| **Kimi API Platform**      | https://platform.kimi.ai/docs/models                                       | Official model documentation for Kimi K2.6, K2.5, and related families    |
| **Z.ai Developer Docs**    | https://docs.z.ai/guides/overview/quick-start                              | Official Z.ai documentation for GLM model families and APIs               |
| **xAI Developer Docs**     | https://docs.x.ai/developers/models                                        | Official xAI model catalog and pricing overview                           |
| **Model Context Protocol** | https://modelcontextprotocol.io/docs/getting-started/intro                 | Open standard for AI-LLM context and tool integration (Anthropic)         |

### Notes

- **Figma MCP**: No public implementation repository exists; reference is official Figma documentation only
- **GitHub MCP**: `opencode.json` currently points at the remote GitHub Copilot MCP endpoint
  `https://api.githubcopilot.com/mcp`
- **Atlassian MCP**: Community fork maintained by sooperset; official Atlassian server exists but uses remote HTTP
- **Vision MCP**: Connects directly to Z.ai vision API endpoints for image analysis

All URLs verified as of June 2026. Refer to individual repository documentation for latest API changes and version
compatibility.
