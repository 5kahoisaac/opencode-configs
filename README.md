# OpenCode Configuration

## Table of Contents

- [Overview](#overview)
- [Available Makefile Commands](#available-makefile-commands)
- [Configuration](#configuration)
    - [Providers](#providers)
        - [Provider List](#provider-list)
        - [Models Configuration](#models-configuration)
    - [Plugins](#plugins)
    - [MCPs](#mcps)
    - [Skills](#skills)
    - [Commands](#commands)
    - [Agents](#agents)
- [Reference Links](#reference-links)

---

## Overview

This project contains a comprehensive OpenCode configuration setup designed to enhance AI-assisted development
workflows. OpenCode is an open-source AI coding assistant that provides intelligent code completion, refactoring
capabilities, and seamless integration with various development tools and platforms.

The configuration includes carefully selected plugins, skills, commands, and agents that extend OpenCode's functionality
to support complex development tasks, improve code quality, and streamline development workflows. This setup is
particularly focused on providing enterprise-grade features while maintaining flexibility for personal and team use
cases.

OpenCode serves as a powerful alternative to traditional IDE-based AI assistants, offering features such as
context-aware code generation, multi-file refactoring, intelligent code search, and integration with popular development
tools like GitHub, Jira, and Figma. The configuration files in this project customize OpenCode's behavior to match
specific workflow requirements and preferences.

---

## Available Makefile Commands

The Makefile provides essential commands to manage the OpenCode configuration:

| Command                   | Description                                                                                                                                |
|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| `make sync`               | Sync OpenCode configuration (`~/.config/opencode/`) and skills (`~/.agents/skills/`). Copies all configuration files, agents, and commands |
| `make sync SKIP_SKILLS=1` | Sync configuration only, skipping the skills sync step                                                                                     |
| `make sync-skills`        | Sync skills from `skills.csv` to global scope. Removes obsolete skills, installs missing ones, and updates all installed skills            |
| `make help`               | Display available targets and their descriptions                                                                                           |

**Workflow:**

1. Run `make sync` to copy configuration files, agents, and commands to system locations
2. The `sync` command automatically calls `sync-skills` to manage skills installation — pass `SKIP_SKILLS=1` to skip
   this step
3. Use `make help` to see all available commands

---

## Configuration

### Providers

This configuration integrates multiple AI model providers to offer a diverse range of capabilities, from lightweight
fast responses to deep reasoning tasks. The provider setup is designed to balance cost-effectiveness with performance,
utilizing both free and premium models across different use cases.

**Default Model:** `github-copilot/claude-opus-4.6` (configured as a primary model in `opencode.json`)

**Small Model:** `github-copilot/claude-sonnet-4.6` (configured for quick tasks in `opencode.json`)

#### Provider List

The following AI providers are **enabled** in this setup (configured in `opencode.json`):

**GitHub Copilot**

GitHub Copilot provides access to a broad range of frontier models including Claude (Anthropic), GPT-5 (OpenAI),
Gemini (Google), and Grok (xAI) through a unified API. This provider serves as the primary model source in this
configuration, with `github-copilot/claude-opus-4.6` used as the default model and `github-copilot/claude-sonnet-4.6` as
the small model for quick tasks. GitHub Copilot's multi-model access enables flexible routing across different model
families based on task requirements.

**OpenCode**

OpenCode's built-in model hub offers several free models optimized for different task types. The configuration utilizes
`opencode/gpt-5-nano` for git and quick tasks, and `opencode/gemini-3-flash` for writing and research tasks. These
models provide a reliable, cost-effective foundation for high-frequency, low-complexity workflows.

**Z.ai Coding Plan**

Z.ai provides access to advanced GLM models. These models are used primarily as fallbacks in this configuration, with
`zai-coding-plan/glm-5.1` available for agents requiring strong reasoning and `zai-coding-plan/glm-4.5` for lighter
tasks.

**xAI (Grok)**

xAI provides the Grok family of models, specifically `xai/grok-code-fast-1` as the primary model for the `explore`
agent. These models excel at fast code understanding and pattern recognition.

**Kimi for Coding**

Kimi for Coding provides the K2.5 model optimized specifically for coding tasks. The `kimi-for-coding/k2p5` model is
used as a fallback across multiple agents and categories, delivering strong performance for code generation and
technical implementation tasks.

#### Models Configuration

The `oh-my-opencode.json` file contains a sophisticated model assignment system that maps specialized agents to
appropriate models based on their specific functions. This configuration represents a carefully tuned balance between
API rate limits, response quality, and cost management.

**Agent-Specific Model Assignments**

Individual agents from the oh-my-opencode plugin receive specialized model assignments optimized for their specific
functions:

| Source                 | Agent Name          | Role                      | Model                              | Variant  | Ultrawork                              | Fallback Models                                                                             | Description                                                                                       |
|:-----------------------|:--------------------|:--------------------------|:-----------------------------------|:---------|:---------------------------------------|:--------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|
| **oh-my-opencode**     | `sisyphus`          | Orchestrator              | `kimi-for-coding/k2p5`             | —        | `github-copilot/claude-opus-4.6` (max) | `github-copilot/gpt-5.4` (medium), `zai-coding-plan/glm-5.1`, `opencode/big-pickle`         | Primary orchestrator for complex, multi-step tasks and agent coordination                         |
| **oh-my-opencode**     | `metis`             | Scope Analysis            | `zai-coding-plan/glm-5-turbo`      | —        | `github-copilot/claude-opus-4.6` (max) | `github-copilot/gpt-5.4` (high), `github-copilot/gemini-3.1-pro-preview`                    | Analyzes task scope, identifies ambiguities, and provides pre-planning consultation               |
| **oh-my-opencode**     | `prometheus`        | Planning Specialist       | `zai-coding-plan/glm-5.1`          | —        | `github-copilot/claude-opus-4.6` (max) | `github-copilot/gpt-5.4` (high), `github-copilot/gemini-3.1-pro-preview`                    | Creates detailed plans and work breakdowns for complex projects and feature implementations       |
| **oh-my-opencode**     | `atlas`             | Knowledge Specialist      | `github-copilot/claude-sonnet-4.6` | —        | —                                      | `kimi-for-coding/k2p5`, `github-copilot/gpt-5.4` (medium)                                   | Manages and retrieves contextual knowledge, architectural decisions, and project conventions      |
| **oh-my-opencode**     | `sisyphus-junior`   | Lightweight Orchestrator  | `kimi-for-coding/k2p5`             | —        | `github-copilot/claude-opus-4.6`       | `github-copilot/gpt-5.4` (medium), `opencode/big-pickle`                                    | Lightweight orchestrator for category-optimized task delegation via the task() system             |
| **oh-my-opencode**     | `hephaestus`        | Implementation Specialist | `github-copilot/gpt-5.4`           | `medium` | —                                      | —                                                                                           | Executes implementation tasks with balanced capability and efficiency                             |
| **oh-my-opencode**     | `oracle`            | Strategic Advisor         | `zai-coding-plan/glm-5`            | —        | `github-copilot/gpt-5.4` (high)        | `github-copilot/gemini-3.1-pro-preview` (high), `github-copilot/claude-opus-4.6` (max)      | Provides high-level architectural guidance and complex reasoning for critical decisions           |
| **oh-my-opencode**     | `momus`             | Quality Review            | `zai-coding-plan/glm-5`            | —        | `github-copilot/gpt-5.4` (xhigh)       | `github-copilot/claude-opus-4.6` (max), `github-copilot/gemini-3.1-pro-preview` (high)      | Reviews work plans and implementations for quality, completeness, and adherence to best practices |
| **oh-my-opencode**     | `multimodal-looker` | Visual Analysis           | `kimi-for-coding/k2p5`             | —        | `github-copilot/gpt-5.4` (medium)      | `zai-coding-plan/glm-4.6v`, `opencode/gpt-5-nano`                                           | Analyzes visual content, images, and multimodal inputs for comprehensive understanding            |
| **oh-my-opencode**     | `explore`           | Codebase Analysis         | `xai/grok-code-fast-1`             | —        | —                                      | `github-copilot/grok-code-fast-1`, `github-copilot/claude-haiku-4.5`, `opencode/gpt-5-nano` | Performs rapid codebase navigation, pattern detection, and symbol exploration                     |
| **oh-my-opencode**     | `librarian`         | Research Specialist       | `opencode/gemini-3-flash`          | —        | —                                      | `github-copilot/claude-haiku-4.5`, `opencode/gpt-5-nano`                                    | Handles documentation lookup, external research, and information retrieval tasks                  |
| **opencode-historian** | `historian`         | Memory Management         | `kimi-for-coding/k2p5`             | —        | —                                      | —                                                                                           | Manages persistent memories, context retention, and semantic search across project knowledge base |

**Currency API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Free providers (OpenCode) are used for
   routine tasks to preserve quota on premium providers (Z.ai, xAI) for complex operations.

2. **Cost Optimization**: The configuration prioritizes free models (`opencode/*-free`) for everyday tasks while
   reserving premium models for tasks requiring their specific strengths.

3. **Performance Tiering**: Models are tiered by capability and speed:
    - **Flash Variants** (`*-flash`): Fastest responses, lowest cost, ideal for quick lookups and simple tasks
    - **Standard Variants** (no suffix): Balanced performance for general-purpose work
    - **High/Max Variants**: Enhanced capability for complex reasoning tasks

4. **Suggested Usage Pattern**:
    - Use **@sisyphus** for complex, multi-step tasks requiring coordination and agent delegation
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
    - Reserve **Premium Models** (GitHub Copilot max/xhigh variants) for tasks where quality is critical

This configuration represents a personalized setup balancing performance, cost, and reliability based on individual
usage patterns and provider strengths.

**Task Category Model Assignments**

The `oh-my-opencode.json` configuration also defines task category model assignments that automatically route tasks to
appropriate models based on their category:

| Category             | Model                                   | Variant  | Fallback Models                                                                                                                      | Description                                                         |
|:---------------------|:----------------------------------------|:---------|:-------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------|
| `visual-engineering` | `github-copilot/gemini-3.1-pro-preview` | `high`   | `zai-coding-plan/glm-5.1`, `github-copilot/claude-opus-4.6` (max), `kimi-for-coding/k2p5`                                            | Frontend, UI/UX, design, styling, and animation tasks               |
| `ultrabrain`         | `github-copilot/gpt-5.4`                | `xhigh`  | `github-copilot/gemini-3.1-pro-preview` (high), `github-copilot/claude-opus-4.6` (max), `zai-coding-plan/glm-5.1`                    | Hard logic-heavy tasks requiring deep reasoning                     |
| `deep`               | `github-copilot/gpt-5.3-codex`          | `medium` | `github-copilot/claude-opus-4.6` (max), `github-copilot/gemini-3.1-pro-preview` (high)                                               | Goal-oriented autonomous problem-solving with thorough research     |
| `artistry`           | `github-copilot/gemini-3.1-pro-preview` | `high`   | `github-copilot/claude-opus-4.6` (max), `github-copilot/gpt-5.4`                                                                     | Complex problem-solving with unconventional, creative approaches    |
| `quick`              | `opencode/gpt-5-nano`                   | —        | `opencode/gemini-3-flash`, `github-copilot/gpt-5.4-mini`, `github-copilot/claude-haiku-4.5`, `github-copilot/gemini-3-flash-preview` | Trivial tasks, single file changes, typo fixes                      |
| `unspecified-low`    | `github-copilot/claude-sonnet-4.6`      | —        | `github-copilot/gpt-5.3-codex` (medium), `kimi-for-coding/k2p5`, `opencode/gemini-3-flash`, `github-copilot/gemini-3-flash-preview`  | Low-effort tasks that don't fit other categories                    |
| `unspecified-high`   | `github-copilot/claude-opus-4.6`        | `max`    | `github-copilot/gpt-5.4` (high), `zai-coding-plan/glm-5.1`, `kimi-for-coding/k2p5`                                                   | High-effort tasks that don't fit other categories                   |
| `writing`            | `opencode/gemini-3-flash`               | —        | `github-copilot/gemini-3-flash-preview`, `kimi-for-coding/k2p5`, `github-copilot/claude-sonnet-4.6`                                  | Documentation, prose, and technical writing tasks                   |
| `git`                | `opencode/gpt-5-nano`                   | —        | `opencode/big-pickle`, `zai-coding-plan/glm-4.5-air`                                                                                 | All git operations with focus on atomic commits and safe operations |

These category assignments enable intelligent task routing, ensuring each type of work is handled by the most suitable
model for optimal results.

**Background Task Configuration**

The `oh-my-opencode.json` file includes sophisticated background task management settings:

| Setting                                 | Value | Description                                               |
|:----------------------------------------|:------|:----------------------------------------------------------|
| `defaultConcurrency`                    | 5     | Default number of concurrent background tasks             |
| `staleTimeoutMs`                        | 60000 | Timeout in milliseconds before a task is considered stale |
| **Provider Concurrency**                |       | Per-provider task limits for rate limit management        |
| `xai`                                   | 5     | Maximum concurrent tasks for xAI provider                 |
| `opencode`                              | 10    | Maximum concurrent tasks for OpenCode provider            |
| `kimi-for-coding`                       | 3     | Maximum concurrent tasks for Kimi provider                |
| `zai-coding-plan`                       | 10    | Maximum concurrent tasks for Z.ai provider                |
| `github-copilot`                        | 3     | Maximum concurrent tasks for GitHub Copilot provider      |
| **Model Concurrency**                   |       | Per-model fine-grained concurrency limits                 |
| `kimi-for-coding/k2p5`                  | 3     | Concurrency limit for K2.5 model                          |
| `zai-coding-plan/glm-5`                 | 2     | Concurrency limit for GLM-5 model                         |
| `zai-coding-plan/glm-5-turbo`           | 1     | Concurrency limit for GLM-5-turbo model                   |
| `zai-coding-plan/glm-5.1`               | 1     | Concurrency limit for GLM-5.1 model                       |
| `zai-coding-plan/glm-4.7`               | 2     | Concurrency limit for GLM-4.7 model                       |
| `zai-coding-plan/glm-4.7-flash`         | 1     | Concurrency limit for GLM-4.7-flash                       |
| `zai-coding-plan/glm-4.7-flashx`        | 3     | Concurrency limit for GLM-4.7-flashx                      |
| `zai-coding-plan/glm-4.6`               | 3     | Concurrency limit for GLM-4.6 model                       |
| `zai-coding-plan/glm-4.6v`              | 10    | Concurrency limit for GLM-4.6v model                      |
| `zai-coding-plan/glm-4.5`               | 10    | Concurrency limit for GLM-4.5 model                       |
| `zai-coding-plan/glm-4.5v`              | 10    | Concurrency limit for GLM-4.5v model                      |
| `zai-coding-plan/glm-4.5-air`           | 5     | Concurrency limit for GLM-4.5-air model                   |
| `zai-coding-plan/glm-4.5-flash`         | 2     | Concurrency limit for GLM-4.5-flash model                 |
| `github-copilot/claude-opus-4.6`        | 2     | Concurrency limit for Claude Opus 4.6                     |
| `github-copilot/claude-opus-4.5`        | 2     | Concurrency limit for Claude Opus 4.5                     |
| `github-copilot/claude-opus-41`         | 2     | Concurrency limit for Claude Opus 4.1                     |
| `github-copilot/claude-sonnet-4.6`      | 3     | Concurrency limit for Claude Sonnet 4.6                   |
| `github-copilot/claude-sonnet-4.5`      | 3     | Concurrency limit for Claude Sonnet 4.5                   |
| `github-copilot/claude-haiku-4.5`       | 5     | Concurrency limit for Claude Haiku 4.5                    |
| `github-copilot/gpt-5.4`                | 3     | Concurrency limit for GPT-5.4                             |
| `github-copilot/gpt-5.3-codex`          | 3     | Concurrency limit for GPT-5.3-codex                       |
| `github-copilot/gpt-5.4-mini`           | 5     | Concurrency limit for GPT-5.4-mini                        |
| `github-copilot/gpt-5-mini`             | 5     | Concurrency limit for GPT-5-mini                          |
| `github-copilot/gpt-4o`                 | 4     | Concurrency limit for GPT-4o                              |
| `github-copilot/gemini-3-flash-preview` | 6     | Concurrency limit for Gemini 3 Flash                      |
| `github-copilot/gemini-3.1-pro-preview` | 3     | Concurrency limit for Gemini 3.1 Pro                      |
| `github-copilot/grok-code-fast-1`       | 4     | Concurrency limit for Grok Code Fast 1                    |
| `opencode/gemini-3-flash`               | 5     | Concurrency limit for OpenCode Gemini 3 Flash             |
| `opencode/gpt-5-nano`                   | 20    | Concurrency limit for OpenCode GPT-5 Nano                 |

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

**oh-my-opencode@latest**

The oh-my-opencode plugin is a comprehensive agent collection for OpenCode that provides a full suite of specialized
agents for various development tasks. This plugin delivers a robust set of agents optimized for efficient task
delegation, complex problem solving, and comprehensive development workflows. The oh-my-opencode suite includes agents
for orchestration, exploration, strategic decision-making, visual engineering, research, and more, providing
enterprise-grade capabilities for demanding development scenarios.

**@nick-vi/opencode-type-inject@latest**

The type-inject plugin provides advanced type inference and injection capabilities for OpenCode. This plugin enhances
the AI's understanding of type systems across different programming languages, enabling more accurate code completion
and type-aware refactoring operations. It integrates with OpenCode's language server protocol to provide real-time type
information and suggestions.

**opencode-historian@latest**

The historian plugin provides persistent memory management capabilities for OpenCode, enabling context retention and
compounded engineering practices across sessions. This plugin allows agents to store, recall, and manage memories
including architectural decisions, design patterns, learnings, preferences, issues, and contextual information. The
historian system automatically classifies memory types and manages circular references between related memories,
creating a knowledge base that persists beyond individual conversations.

---

## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations.
This configuration includes manually configured MCPs and pre-installed MCPs from the oh-my-opencode and
opencode-historian plugins.

### Manually Configured MCPs

The following MCPs are explicitly configured in `opencode.json` file:

**figma** *(disabled)*

The Figma MCP enables seamless integration with Figma for design-related operations.
This MCP allows OpenCode to interact with Figma's desktop application, enabling design context retrieval,
UI code generation, and design system exploration directly from Figma files. Currently disabled in configuration.

**github** *(disabled)*

The GitHub MCP provides comprehensive integration with GitHub for repository operations,
pull request management, issue tracking, and code search.
This MCP enables OpenCode to interact with GitHub's API for various development workflows directly from the conversation
interface. Currently disabled in configuration.

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

### Pre-installed MCPs from Oh-My-Opencode

The oh-my-opencode plugin includes three pre-configured MCP servers that provide essential development tools:

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

These pre-installed MCPs are automatically available when the oh-my-opencode plugin is enabled. MCP access is controlled
via per-agent permissions in the configuration. See
the [official documentation](https://github.com/code-yeongyu/oh-my-openagent/blob/master/docs/quick-reference.md) for
details on MCP assignment syntax and configuration options.

---

## Skills

The skills system in OpenCode provides a modular way to extend the assistant's capabilities with specialized knowledge
and workflows. This configuration includes skills installed via Vercel's official skills.sh system and pre-installed
skills from the opencode-historian plugin. Note that skills are installed to `~/.agents/skills/` via the skills.sh
system, not in the local `skills/` directory of this repository.

The following **83 skills** are available in this configuration, organized by category:

### Custom Skills

| Skill Name    | Source                        | Description                                                                                                                                                                                                                                                                                                         |
|:--------------|:------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **mnemonics** | 5kahoisaac/opencode-historian | Memory management by using the historian subagent to store, recall, and manage persistent memories across conversations. Use when you need to remember decisions, preferences, learnings, or retrieve stored context. Compatible with opencode, opencode-historian plugin and qmd CLI. *(custom skill by Isaac Ng)* |

### Everything Claude Code Skills

| Skill Name                         | Description                                                                                                                                                                                                                                 |
|:-----------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ai-regression-testing**          | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check workflows, and patterns to catch AI blind spots where the same model writes and reviews code.        |
| **android-clean-architecture**     | Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data layer patterns.                                                                            |
| **api-design**                     | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.                                                                                |
| **backend-patterns**               | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.                                                                                              |
| **coding-standards**               | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development.                                                                                                                        |
| **compose-multiplatform-patterns** | Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI.                                                                                         |
| **configure-ecc**                  | Interactive installer for Everything Claude Code — guides users through selecting and installing skills and rules to user-level or project-level directories, verifies paths, and optionally optimizes installed files.                     |
| **continuous-learning**            | Automatically extract reusable patterns from Claude Code sessions and save them as learned skills for future use.                                                                                                                           |
| **continuous-learning-v2**         | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into skills/commands/agents. v2.1 adds project-scoped instincts to prevent cross-project contamination. |
| **cpp-coding-standards**           | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce modern, safe, and idiomatic practices.                                                            |
| **cpp-testing**                    | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sanitizers.                                                                                            |
| **django-patterns**                | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django apps.                                                                                                 |
| **django-tdd**                     | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs.                                                                                                      |
| **django-verification**            | Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deployment readiness checks before release or PR.                                                                                      |
| **e2e-testing**                    | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies.                                                                                                       |
| **eval-harness**                   | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles.                                                                                                                                 |
| **frontend-patterns**              | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices.                                                                                                                        |
| **frontend-slides**                | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch.                           |
| **golang-patterns**                | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications.                                                                                                                    |
| **golang-testing**                 | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices.                                                                                    |
| **iterative-retrieval**            | Pattern for progressively refining context retrieval to solve the subagent context problem.                                                                                                                                                 |
| **java-coding-standards**          | Java coding standards for Spring Boot services: naming, immutability, Optional usage, streams, exceptions, generics, and project layout.                                                                                                    |
| **kotlin-coroutines-flows**        | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing.                                                                                                   |
| **kotlin-exposed-patterns**        | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern.                                                                                    |
| **kotlin-ktor-patterns**           | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing.                                                                                               |
| **kotlin-patterns**                | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coroutines, null safety, and DSL builders.                                                             |
| **kotlin-testing**                 | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with idiomatic Kotlin practices.                                                                         |
| **laravel-patterns**               | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps.                                                                                           |
| **laravel-plugin-discovery**       | Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess Laravel/PHP compatibility.                                                                          |
| **laravel-tdd**                    | Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes, and coverage targets.                                                                                                                        |
| **laravel-verification**           | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness.                                                                                                |
| **mcp-server-patterns**            | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or official MCP docs for latest API.                                                                         |
| **perl-patterns**                  | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications.                                                                                                                              |
| **perl-testing**                   | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology.                                                                                                                  |
| **plankton-code-quality**          | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks.                                                                                                       |
| **project-guidelines-example**     | Example project-specific skill template based on a real production application.                                                                                                                                                             |
| **python-patterns**                | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications.                                                                                                      |
| **python-testing**                 | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements.                                                                                                                     |
| **rust-patterns**                  | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications.                                                                                                     |
| **rust-testing**                   | Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD methodology.                                                                                       |
| **springboot-patterns**            | Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java Spring Boot backend work.                                                                           |
| **springboot-tdd**                 | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bugs, or refactoring.                                                                                 |
| **springboot-verification**        | Verification loop for Spring Boot projects: build, static analysis, tests with coverage, security scans, and diff review before release or PR.                                                                                              |
| **strategic-compact**              | Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction.                                                                                                      |
| **tdd-workflow**                   | Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.                                                                 |
| **verification-loop**              | A comprehensive verification system for Claude Code sessions.                                                                                                                                                                               |

### Anthropic Skills

| Skill Name          | Description                                                                                                                                                                                                                         |
|:--------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **algorithmic-art** | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems.          |
| **docx**            | Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when OpenCode needs to work with professional documents (.docx files).         |
| **frontend-design** | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications.                                           |
| **pdf**             | Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Use when OpenCode needs to fill in a PDF form or programmatically process PDF documents. |
| **pptx**            | Presentation creation, editing, and analysis. When OpenCode needs to work with presentations (.pptx files) for creating, modifying, or adding content.                                                                              |
| **skill-creator**   | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends OpenCode's capabilities with specialized knowledge.                                 |
| **xlsx**            | Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Use when OpenCode needs to work with spreadsheets (.xlsx, .csv, .tsv, etc.).                     |

### Other Skills

| Skill Name                           | Source                         | Description                                                                                                                                                                                                                                  |
|:-------------------------------------|:-------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **async-python-patterns**            | wshobson/agents                | Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications.                                                      |
| **copywriting**                      | coreyhaines31/marketingskills  | Write, rewrite, or improve marketing copy for homepages, landing pages, pricing pages, feature pages, about pages, or product pages.                                                                                                         |
| **create-readme**                    | github/awesome-copilot         | Create comprehensive and well-structured README.md files with clear formatting and informative content.                                                                                                                                      |
| **documentation-writer**             | github/awesome-copilot         | Create high-quality software documentation using Diátaxis framework with tutorials, how-to guides, references, and explanations.                                                                                                             |
| **figma-create-design-system-rules** | figma/mcp-server-guide         | Generates custom design system rules for your codebase. Use when establishing project-specific conventions for Figma-to-code workflows. *(requires Figma MCP)*                                                                               |
| **figma-implement-design**           | figma/mcp-server-guide         | Translates Figma designs into production-ready application code with 1:1 visual fidelity. Use when implementing UI code from Figma files. *(requires Figma MCP)*                                                                             |
| **git-commit**                       | github/awesome-copilot         | Execute git commits with conventional commit message analysis, intelligent staging, and automatic message generation.                                                                                                                        |
| **rust-best-practices**              | apollographql/skills           | Guide for writing idiomatic Rust code based on Apollo GraphQL's best practices handbook.                                                                                                                                                     |
| **seo-audit**                        | coreyhaines31/marketingskills  | Audit and diagnose SEO issues including technical SEO, on-page optimization, meta tags, page speed, and indexing problems.                                                                                                                   |
| **simplify**                         | brianlovin/claude-config       | Simplify and refine recently modified code for clarity and consistency. Use after writing code to improve readability without changing functionality.                                                                                        |
| **stock-analysis**                   | gracefullight/stock-checker    | Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, crypto analysis, and periodic performance reports. *(custom skill by Isaac Ng)*                                                                 |
| **golang-pro**                       | jeffallan/claude-skills        | Implements concurrent Go patterns using goroutines and channels, designs and builds microservices with gRPC or REST, optimizes Go application performance.                                                                                   |
| **laravel-specialist**               | jeffallan/claude-skills        | Build and configure Laravel 10+ applications, including creating Eloquent models, implementing Sanctum authentication, configuring Horizon queues, and building Livewire components.                                                         |
| **javascript-testing-patterns**      | microck/ordinary-claude-skills | Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing.                                                                                                |
| **next-best-practices**              | vercel-labs/next-skills        | Next.js best practices including file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, and optimization.                                                                                    |
| **receiving-code-review**            | obra/superpowers               | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable.                                                                                                  |
| **requesting-code-review**           | obra/superpowers               | Use when completing tasks, implementing major features, or before merging to verify work meets requirements.                                                                                                                                 |
| **remotion-best-practices**          | remotion-dev/skills            | Best practices for Remotion - Video creation in React.                                                                                                                                                                                       |
| **lesson-learned**                   | softaworks/agent-toolkit       | Analyze recent code changes via git history and extract software engineering lessons.                                                                                                                                                        |
| **agent-browser**                    | vercel-labs/agent-toolkit      | Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. |
| **vercel-react-best-practices**      | vercel-labs/agent-skills       | React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code.                                                                                               |
| **vercel-react-native-skills**       | vercel-labs/agent-skills       | React Native and Expo best practices for building performant mobile apps including list performance, animations, and native module integration.                                                                                              |
| **web-design-guidelines**            | vercel-labs/agent-skills       | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".                                                     |
| **find-skills**                      | vercel-labs/skills             | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...".                                                                                            |
| **modern-javascript-patterns**       | wshobson/agents                | Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns.                                                                 |
| **python-packaging**                 | wshobson/agents                | Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI.                                                                                                                         |
| **python-performance-optimization**  | wshobson/agents                | Profile and optimize Python code using cProfile, memory profilers, and performance best practices.                                                                                                                                           |
| **python-testing-patterns**          | wshobson/agents                | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development.                                                                                                                                      |
| **typescript-advanced-types**        | wshobson/agents                | Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types.                                                                                                          |

---

## Commands

The commands directory is available for custom slash commands that extend OpenCode's interaction capabilities.
Currently, no custom commands are configured in this setup. Commands can be added to the `./commands/` directory and
will be migrated along with other configuration files during the build process.

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

#### Oh-My-Opencode Agents

The oh-my-opencode plugin provides a comprehensive suite of specialized agents designed for various development tasks:

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

The historian agent uses the `kimi-for-coding/k2p5` model configured in `opencode-historian.json` for fast, efficient
memory operations.


---

## Reference Links

The following resources provide additional information about skills, plugins, and the Vercel skills.sh system referenced
in this configuration:

- **Vercel Skills.sh**: https://skills.sh - The official skills installation and management system for OpenCode,
  providing community-maintained skills for various development tasks and domains.
- **OpenCode Documentation**: https://opencode.ai/docs - Official documentation for OpenCode configuration, plugin
  development, and usage guides.
- **GitHub Copilot**: https://github.com/features/copilot - Unified API providing access to frontier models including
  Claude, GPT-5, Gemini, and Grok through a single provider interface.
- **Oh-My-Openagent Plugin**: https://github.com/code-yeongyu/oh-my-openagent - A comprehensive agent collection
  providing a full suite of specialized agents for complex development tasks, available through the OpenCode plugin
  registry.
- **Type-Inject Plugin**: https://github.com/nick-vi/opencode-type-inject - Advanced type inference and injection
  capabilities for OpenCode, enhancing type system understanding across programming languages.
- **Historian Plugin**: https://github.com/5kahoisaac/opencode-historian - Persistent memory management for OpenCode,
  enabling context retention and compounded engineering practices across sessions.
- **Figma MCP**: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server - Official MCP
  server for Figma integration, enabling design context retrieval and UI code generation.
- **GitHub MCP**: https://github.com/github/github-mcp-server - Official MCP server for GitHub API integration, enabling
  repository operations and issue management.
- **Atlassian MCP**: https://github.com/sooperset/mcp-atlassian - Official MCP server for Atlassian Jira and Confluence
  integration, enabling project management workflows.
- **Serena MCP**: https://github.com/oraios/serena - Advanced code intelligence MCP providing precise symbol navigation
  and AST-aware operations.
- **Vision MCP**: https://github.com/z-ai-org/mcp-server - Visual analysis MCP powered by Z.ai vision models for image
  understanding and visual content analysis.
