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

This project contains a comprehensive OpenCode configuration setup designed to enhance AI-assisted development workflows. OpenCode is an open-source AI coding assistant that provides intelligent code completion, refactoring capabilities, and seamless integration with various development tools and platforms.

The configuration includes carefully selected plugins, skills, commands, and agents that extend OpenCode's functionality to support complex development tasks, improve code quality, and streamline development workflows. This setup is particularly focused on providing enterprise-grade features while maintaining flexibility for personal and team use cases.

OpenCode serves as a powerful alternative to traditional IDE-based AI assistants, offering features such as context-aware code generation, multi-file refactoring, intelligent code search, and integration with popular development tools like GitHub, Jira, and Figma. The configuration files in this project customize OpenCode's behavior to match specific workflow requirements and preferences.

---


## Available Makefile Commands

The Makefile provides essential commands to build, clean, and manage the OpenCode configuration:

| Command        | Description                                                                                                                             |
|:---------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| `make build`   | Build OpenCode configuration. Creates `./dist/` directory, copies JSON files, and copies agents/commands/skills directories             |
| `make clean`   | Remove the `./dist` directory and all generated files                                                                                   |
| `make migrate` | Deploy built configuration to global OpenCode locations (`~/.config/opencode/` and `~/.agents/skills/`). Must be run after `make build` |
| `make help`    | Display available targets and their descriptions                                                                                        |

**Workflow:**
1. Run `make build` to process configuration files with environment variables
2. Run `make migrate` to install the configuration to system locations
3. Use `make clean` to start fresh when needed

---


## Configuration

### Providers

This configuration integrates multiple AI model providers to offer a diverse range of capabilities, from lightweight fast responses to deep reasoning tasks. The provider setup is designed to balance cost-effectiveness with performance, utilizing both free and premium models across different use cases.

**Default Model:** `zai-coding-plan/glm-5` (configured as a primary model in `opencode.json`)

#### Provider List

The following AI providers are **enabled** in this setup (configured in `opencode.json`):

**OpenCode**

OpenCode's built-in model hub offers several free models optimized for different task types. The configuration utilizes `opencode/kimi-k2.5-free` for orchestration and complex reasoning tasks, and `opencode/gemini-3-flash` for research and documentation tasks. These models provide a reliable, cost-effective foundation for everyday development workflows.

**Z.ai Coding Plan**

Z.ai provides access to advanced GLM models including GLM-5 and GLM-4.7. These models offer excellent performance for planning, reasoning, and implementation tasks. The configuration uses `zai-coding-plan/glm-5` for high-level strategic reasoning and `zai-coding-plan/glm-4.7` for implementation tasks, balancing capability and efficiency.

**xAI (Grok)**

xAI provides the Grok family of models, specifically `xai/grok-code-fast-1` for exploration tasks and `xai/grok-4-1-fast-reasoning` for visual engineering and design tasks. These models excel at code understanding and fast reasoning, making them ideal for tasks requiring quick analysis and pattern recognition.

**Kimi for Coding**

Kimi for Coding provides the K2.5 model optimized specifically for coding tasks. The `kimi-for-coding/k2p5` model delivers excellent performance for code generation, refactoring, and technical implementation tasks with high accuracy and efficiency.


#### Models Configuration

The `oh-my-opencode.json` file contains a sophisticated model assignment system that maps specialized agents to appropriate models based on their specific functions. This configuration represents a carefully tuned balance between API rate limits, response quality, and cost management.

**Agent-Specific Model Assignments**

Individual agents from the oh-my-opencode plugin receive specialized model assignments optimized for their specific functions:

| Source                 | Agent Name          | Role                      | Model                     | Fallback Models                                                              | Description                                                                                       |
|:-----------------------|:--------------------|:--------------------------|:--------------------------|:-----------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|
| **oh-my-opencode**     | `sisyphus`          | Orchestrator              | `kimi-for-coding/k2p5`    | `zai-coding-plan/glm-5`, `opencode/big-pickle`                               | Primary orchestrator for complex, multi-step tasks and agent coordination                         |
| **oh-my-opencode**     | `hephaestus`        | Implementation Specialist | `kimi-for-coding/k2p5`    | `zai-coding-plan/glm-4.7`                                                    | Executes implementation tasks with balanced capability and efficiency                             |
| **oh-my-opencode**     | `oracle`            | Strategic Advisor         | `kimi-for-coding/k2p5`    | `zai-coding-plan/glm-5`                                                      | Provides high-level architectural guidance and complex reasoning for critical decisions           |
| **oh-my-opencode**     | `librarian`         | Research Specialist       | `opencode/gemini-3-flash` | `opencode/big-pickle`                                                        | Handles documentation lookup, external research, and information retrieval tasks                  |
| **oh-my-opencode**     | `explore`           | Codebase Analysis         | `xai/grok-code-fast-1`    | `opencode/gpt-5-nano`                                                        | Performs rapid codebase navigation, pattern detection, and symbol exploration                     |
| **oh-my-opencode**     | `multimodal-looker` | Visual Analysis           | `kimi-for-coding/k2p5`    | `opencode/gemini-3-flash`, `zai-coding-plan/glm-4.6v`, `opencode/gpt-5-nano` | Analyzes visual content, images, and multimodal inputs for comprehensive understanding            |
| **oh-my-opencode**     | `prometheus`        | Planning Specialist       | `zai-coding-plan/glm-5`   | `kimi-for-coding/k2p5`, `zai-coding-plan/glm-4.7`                            | Creates detailed plans and work breakdowns for complex projects and feature implementations       |
| **oh-my-opencode**     | `metis`             | Scope Analysis            | `zai-coding-plan/glm-5`   | `kimi-for-coding/k2p5`, `zai-coding-plan/glm-4.7`                            | Analyzes task scope, identifies ambiguities, and provides pre-planning consultation               |
| **oh-my-opencode**     | `momus`             | Quality Review            | `kimi-for-coding/k2p5`    | `zai-coding-plan/glm-5`, `zai-coding-plan/glm-4.7`                           | Reviews work plans and implementations for quality, completeness, and adherence to best practices |
| **oh-my-opencode**     | `atlas`             | Knowledge Specialist      | `zai-coding-plan/glm-5`   | `kimi-for-coding/k2p5`                                                       | Manages and retrieves contextual knowledge, architectural decisions, and project conventions      |
| **opencode-historian** | `historian`         | Memory Management         | `kimi-for-coding/k2p5`    | -                                                                            | Manages persistent memories, context retention, and semantic search across project knowledge base |

**Currency API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Free providers (OpenCode) are used for routine tasks to preserve quota on premium providers (Z.ai, xAI) for complex operations.

2. **Cost Optimization**: The configuration prioritizes free models (`opencode/*-free`) for everyday tasks while reserving premium models for tasks requiring their specific strengths.

3. **Performance Tiering**: Models are tiered by capability and speed:
   - **Flash Variants** (`*-flash`): Fastest responses, lowest cost, ideal for quick lookups and simple tasks
   - **Standard Variants** (no suffix): Balanced performance for general-purpose work
   - **High/Max Variants**: Enhanced capability for complex reasoning tasks

4. **Suggested Usage Pattern**:
   - Use **@sisyphus** for complex, multi-step tasks requiring coordination and agent delegation
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
   - Reserve **Premium Models** (Z.ai, xAI) for tasks where quality is critical

This configuration represents a personalized setup balancing performance, cost, and reliability based on individual usage patterns and provider strengths.

**Task Category Model Assignments**

The `oh-my-opencode.json` configuration also defines task category model assignments that automatically route tasks to appropriate models based on their category:

| Category             | Model                            | Fallback Models                                                | Description                                                         |
|:---------------------|:---------------------------------|:---------------------------------------------------------------|:--------------------------------------------------------------------|
| `visual-engineering` | `xai/grok-4-1-fast-reasoning`    | `zai-coding-plan/glm-4.6v`, `zai-coding-plan/glm-4.5v`         | Frontend, UI/UX, design, styling, and animation tasks               |
| `ultrabrain`         | `kimi-for-coding/k2p5`           | `zai-coding-plan/glm-5`, `zai-coding-plan/glm-4.7`             | Hard logic-heavy tasks requiring deep reasoning                     |
| `deep`               | `zai-coding-plan/glm-4.7`        | `zai-coding-plan/glm-4.6`, `zai-coding-plan/glm-4.5`           | Goal-oriented autonomous problem-solving with thorough research     |
| `artistry`           | `xai/grok-4-1-fast-reasoning`    | `kimi-for-coding/k2p5`, `zai-coding-plan/glm-4.7-flashx`       | Complex problem-solving with unconventional, creative approaches    |
| `quick`              | `zai-coding-plan/glm-4.6`        | `zai-coding-plan/glm-4.5-flash`, `zai-coding-plan/glm-4.5-air` | Trivial tasks, single file changes, typo fixes                      |
| `unspecified-low`    | `zai-coding-plan/glm-4.7-flashx` | `zai-coding-plan/glm-4.6`, `zai-coding-plan/glm-4.5-flash`     | Low-effort tasks that don't fit other categories                    |
| `unspecified-high`   | `zai-coding-plan/glm-5`          | `kimi-for-coding/k2p5`, `zai-coding-plan/glm-4.7`              | High-effort tasks that don't fit other categories                   |
| `writing`            | `opencode/gemini-3-flash`        | `kimi-for-coding/k2p5`, `zai-coding-plan/glm-4.5`              | Documentation, prose, and technical writing tasks                   |
| `git`                | `opencode/gpt-5-nano`            | `opencode/big-pickle`, `zai-coding-plan/glm-4.5-air`           | All git operations with focus on atomic commits and safe operations |

These category assignments enable intelligent task routing, ensuring each type of work is handled by the most suitable model for optimal results.


### Plugins

The OpenCode configuration utilizes several plugins to extend its core functionality. These plugins are defined in `opencode.json` configuration file and provide integration with external services and additional features.

**oh-my-opencode@latest**

The oh-my-opencode plugin is a comprehensive agent collection for OpenCode that provides a full suite of specialized agents for various development tasks. This plugin delivers a robust set of agents optimized for efficient task delegation, complex problem solving, and comprehensive development workflows. The oh-my-opencode suite includes agents for orchestration, exploration, strategic decision-making, visual engineering, research, and more, providing enterprise-grade capabilities for demanding development scenarios.

**@nick-vi/opencode-type-inject@latest**

The type-inject plugin provides advanced type inference and injection capabilities for OpenCode. This plugin enhances the AI's understanding of type systems across different programming languages, enabling more accurate code completion and type-aware refactoring operations. It integrates with OpenCode's language server protocol to provide real-time type information and suggestions.

**opencode-historian@latest**

The historian plugin provides persistent memory management capabilities for OpenCode, enabling context retention and compounded engineering practices across sessions. This plugin allows agents to store, recall, and manage memories including architectural decisions, design patterns, learnings, preferences, issues, and contextual information. The historian system automatically classifies memory types and manages circular references between related memories, creating a knowledge base that persists beyond individual conversations.

---


## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations.
This configuration includes manually configured MCPs and pre-installed MCPs from the oh-my-opencode and opencode-historian plugins.

### Manually Configured MCPs

The following MCPs are explicitly configured in `opencode.json` file:

**figma-desktop** *(disabled)*

The Figma Desktop MCP enables seamless integration with Figma for design-related operations.
This MCP allows OpenCode to interact with Figma's desktop application, enabling design context retrieval,
UI code generation, and design system exploration directly from Figma files. Currently disabled in configuration.

**github**

The GitHub MCP provides comprehensive integration with GitHub for repository operations,
pull request management, issue tracking, and code search.
This MCP enables OpenCode to interact with GitHub's API for various development workflows directly from the conversation interface.

**jira** *(disabled)*

The Jira MCP integrates with Atlassian Jira for project management operations including issue tracking,
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

- **websearch** - Provides real-time web search capabilities via Exa AI. This MCP enables agents to search for current information, documentation, and code examples from across the web.

- **context7** - Provides access to up-to-date official documentation and code examples for various libraries and frameworks. This MCP fetches version-specific documentation directly from the source, ensuring accurate and current information for library usage and API references.

- **grep_app** - Enables ultra-fast code search across millions of public GitHub repositories. This MCP allows agents to search for code patterns, find real-world implementation examples, and discover how others have solved similar problems.

These pre-installed MCPs are automatically available when the oh-my-opencode plugin is enabled. MCP access is controlled via per-agent permissions in the configuration. See the [official documentation](https://github.com/alvinunreal/oh-my-opencode/blob/master/docs/quick-reference.md) for details on MCP assignment syntax and configuration options.

---


## Skills

The skills system in OpenCode provides a modular way to extend the assistant's capabilities with specialized knowledge and workflows. This configuration includes skills installed via Vercel's official skills.sh system and pre-installed skills from the opencode-historian plugin. Note that skills are installed to `~/.agents/skills/` via the skills.sh system, not in the local `skills/` directory of this repository.

#### Custom Skills (by Isaac Ng)

The following custom skills are maintained in the `./skills/` directory:

**Memory Management**
- **mnemonics** *(custom skill by Isaac Ng)* - Memory management by using the historian subagent to store, recall, and manage persistent memories across conversations. Use when you need to remember decisions, preferences, learnings, or retrieve stored context. Compatible with opencode, opencode-historian plugin and qmd CLI.

#### Skills List

The following skills are available in this configuration, organized by category:

**Document & File Processing**
- **docx** *(Proprietary)* - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when OpenCode needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
- **xlsx** *(Proprietary)* - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Use when OpenCode needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc.) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modifying existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas
- **pdf** *(Proprietary)* - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Use when OpenCode needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale
- **pptx** *(Proprietary)* - Presentation creation, editing, and analysis. When OpenCode needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks

**Development Workflow**
- **receiving-code-review** - Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
- **requesting-code-review** - Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- **simplify** - Simplify and refine recently modified code for clarity and consistency. Use after writing code to improve readability without changing functionality

**Skill & Command Management**
- **find-skills** - Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Use when the user is looking for functionality that might exist as an installable skill
- **skill-creator** *(Proprietary)* - Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends OpenCode's capabilities with specialized knowledge, workflows, or tool integrations
- **command-creator** - Guide for creating effective OpenCode slash commands. Use when users ask to "create a command", "make a slash command", "add a command", or want to document a workflow as a reusable command. Essential for creating optimized, agent-executable slash commands with proper structure and best practices

**Frontend & Design**
- **frontend-design** *(Proprietary)* - Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI)
- **web-design-guidelines** - Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices"

**Automation & Integration**
- **agent-browser** - Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task

**Creative & Other**
- **algorithmic-art** *(Proprietary)* - Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations

---


## Commands

The commands directory is available for custom slash commands that extend OpenCode's interaction capabilities. Currently, no custom commands are configured in this setup. Commands can be added to the `./commands/` directory and will be migrated along with other configuration files during the build process.


### TUI Configuration

The `tui.json` file contains the Terminal User Interface configuration for OpenCode:

**Current Configuration:**
- **Theme**: `opencode` - Uses the default OpenCode theme for the terminal interface

This minimal configuration enables the standard OpenCode TUI experience. Additional TUI customization options can be added to this file as needed.

---


## Agents

OpenCode employs a sophisticated agent system where specialized AI agents handle different types of tasks. The agent architecture enables parallel task execution, context-aware processing, and delegation based on task complexity and requirements.

#### Oh-My-Opencode Agents

The oh-my-opencode plugin provides a comprehensive suite of specialized agents designed for various development tasks:

**Core Agents:**

- **@sisyphus** - The primary orchestrator that coordinates complex, multi-step tasks with heavy planning and parallel execution potential. Sisyphus manages agent delegation workflows and ensures tasks are routed to the most appropriate specialist agents.

- **@hephaestus** - Implementation specialist that executes well-defined coding tasks with efficiency and precision. Hephaestus excels at translating plans into working code and handling technical implementations.

- **@oracle** - Strategic advisor that provides high-level architectural guidance and complex reasoning for high-stakes decisions. Oracle is consulted for critical architectural choices and difficult technical problems.

- **@librarian** - Research specialist that handles external documentation lookup, API research, and library information retrieval. Librarian maintains up-to-date knowledge of libraries, frameworks, and best practices.

- **@explore** - Codebase analysis agent that performs rapid navigation, pattern detection, and symbol exploration across the entire codebase. Explore is optimized for finding code patterns and understanding existing implementations.

- **@multimodal-looker** - Visual analysis agent specialized in processing images, screenshots, diagrams, and visual content. This agent enables understanding of visual inputs alongside code and text.

**Planning & Quality Agents:**

- **@prometheus** - Planning specialist that creates detailed work breakdowns and project plans for complex implementations. Prometheus structures tasks into manageable units with clear dependencies and execution order.

- **@metis** - Scope analysis agent that analyzes task requirements, identifies ambiguities, and provides pre-planning consultation. Metis helps clarify requirements before implementation begins.

- **@momus** - Quality review agent that evaluates work plans and implementations against rigorous standards. Momus ensures completeness, verifiability, and adherence to best practices.

- **@atlas** - Knowledge specialist that manages and retrieves contextual information, architectural decisions, and project conventions. Atlas maintains the project's accumulated wisdom and helps agents access relevant context.

These agents work together to provide comprehensive coverage of development tasks through a sophisticated orchestration system that matches tasks to the most appropriate specialist.


#### OpenCode-Historian Agent

The opencode-historian plugin provides a specialized agent for persistent memory management:

**@historian - Memory Management Specialist**

The historian agent manages persistent memories, enabling context retention and compounded engineering practices across sessions. It stores, recalls, and manages project knowledge including architectural decisions, design patterns, learnings, preferences, issues, and contextual information.

**Key capabilities:**
- **Memory Storage**: Stores project decisions, learnings, and context that persist across sessions
- **Semantic Search**: Retrieves relevant memories using keyword or semantic search
- **Memory Classification**: Automatically categorizes memories by type (architectural decisions, conventions, preferences, context)
- **Cross-Reference Management**: Handles circular references between related memories

The historian agent uses the `kimi-for-coding/k2p5` model configured in `opencode-historian.json` for fast, efficient memory operations.


---


## Reference Links

The following resources provide additional information about skills, plugins, and the Vercel skills.sh system referenced in this configuration:

- **Vercel Skills.sh**: https://skills.sh - The official skills installation and management system for OpenCode, providing community-maintained skills for various development tasks and domains.
- **OpenCode Documentation**: https://opencode.ai/docs - Official documentation for OpenCode configuration, plugin development, and usage guides.
- **Oh-My-Opencode Plugin**: https://github.com/alvinunreal/oh-my-opencode - A comprehensive agent collection providing a full suite of specialized agents for complex development tasks, available through the OpenCode plugin registry.
- **Type-Inject Plugin**: https://github.com/nick-vi/opencode-type-inject - Advanced type inference and injection capabilities for OpenCode, enhancing type system understanding across programming languages.
- **Historian Plugin**: https://github.com/5kahoisaac/opencode-historian - Persistent memory management for OpenCode, enabling context retention and compounded engineering practices across sessions.
- **Figma Desktop MCP**: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server - Official MCP server for Figma integration, enabling design context retrieval and UI code generation.
- **GitHub MCP**: https://github.com/github/github-mcp-server - Official MCP server for GitHub API integration, enabling repository operations and issue management.
- **Jira MCP**: https://github.com/sooperset/mcp-atlassian - Official MCP server for Atlassian Jira and Confluence integration, enabling project management workflows.
- **Serena MCP**: https://github.com/oraios/serena - Advanced code intelligence MCP providing precise symbol navigation and AST-aware operations.
- **Vision MCP**: https://github.com/z-ai-org/mcp-server - Visual analysis MCP powered by Z.ai vision models for image understanding and visual content analysis.
- **OpenRouter**: https://openrouter.ai - Unified API for accessing multiple AI models from various providers through a single interface.
