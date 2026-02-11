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

| Command | Description |
|:--------|:------------|
| `make build` | Build OpenCode configuration with .env variables substitution. Creates `./dist/` directory, processes JSONC files with environment variable substitution, and copies agents/commands/skills directories |
| `make clean` | Remove the `./dist` directory and all generated files |
| `make migrate` | Deploy built configuration to global OpenCode locations (`~/.config/opencode/` and `~/.agents/skills/`). Must be run after `make build` |
| `make help` | Display available targets and their descriptions |

**Workflow:**
1. Run `make build` to process configuration files with environment variables
2. Run `make migrate` to install the configuration to system locations
3. Use `make clean` to start fresh when needed

---


## Configuration

### Providers

This configuration integrates multiple AI model providers to offer a diverse range of capabilities, from lightweight fast responses to deep reasoning tasks. The provider setup is designed to balance cost-effectiveness with performance, utilizing both free and premium models across different use cases.

**Default Model:** `zai-coding-plan/glm-5` (configured as the primary model in `opencode.jsonc`)

#### Provider List

The following AI providers are **enabled** in this setup (configured in `opencode.jsonc`):

**OpenCode**

OpenCode's built-in model hub offers several free models optimized for different task types. The configuration utilizes `opencode/kimi-k2.5-free` for orchestration and complex reasoning tasks, and `opencode/gemini-3-flash` for research and documentation tasks. These models provide a reliable, cost-effective foundation for everyday development workflows.

**Z.ai Coding Plan**

Z.ai provides access to advanced GLM models including GLM-5 and GLM-4.7. These models offer excellent performance for planning, reasoning, and implementation tasks. The configuration uses `zai-coding-plan/glm-5` for high-level strategic reasoning and `zai-coding-plan/glm-4.7` for implementation tasks, balancing capability and efficiency.

**xAI (Grok)**

xAI provides the Grok family of models, specifically `xai/grok-code-fast-1` for exploration tasks and `xai/grok-4-1-fast-reasoning` for visual engineering and design tasks. These models excel at code understanding and fast reasoning, making them ideal for tasks requiring quick analysis and pattern recognition.


#### Models Configuration

The `oh-my-opencode-slim.jsonc` and `./agents/*.md` files contain a sophisticated model assignment system that maps specialized agents to appropriate models based on their specific functions. This configuration represents a carefully tuned balance between API rate limits, response quality, and cost management.

**Agent-Specific Model Assignments**

Individual agents from the oh-my-opencode-slim plugin receive specialized model assignments optimized for their specific functions:

| Source                  | Agent Name     | Role                      | Model                                 | Variant  | Description                                                                                            |
|:------------------------|:---------------|:--------------------------|:--------------------------------------|:---------|:-------------------------------------------------------------------------------------------------------|
| **oh-my-opencode-slim** | `orchestrator` | Task Orchestration        | `opencode/kimi-k2.5-free`             | -        | Coordinates complex, multi-step tasks and manages agent delegation workflows                           |
| **oh-my-opencode-slim** | `oracle`       | Strategic Advisor         | `zai-coding-plan/glm-5`               | `high`   | Provides high-level architectural guidance and complex reasoning for critical decisions                |
| **oh-my-opencode-slim** | `librarian`    | Research Specialist       | `opencode/gemini-3-flash`             | `low`    | Handles documentation lookup, external research, and information retrieval tasks                       |
| **oh-my-opencode-slim** | `explorer`     | Codebase Analysis         | `xai/grok-code-fast-1`                | `medium` | Performs rapid codebase navigation, pattern detection, and symbol exploration                          |
| **oh-my-opencode-slim** | `designer`     | UI/UX Design              | `xai/grok-4-1-fast-reasoning`         | `medium` | Creates polished frontend interfaces, handles visual design, animations, and responsive layouts        |
| **oh-my-opencode-slim** | `fixer`        | Implementation Specialist | `zai-coding-plan/glm-4.7`             | `high`   | Executes well-defined coding tasks with efficiency and precision                                       |
| **custom**              | `courier`      | Primary Router            | `xai/grok-4-1-fast-non-reasoning`     | -        | Ultra-fast task router that answers simple queries directly and delegates complex tasks to specialists |

**Currency API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Free providers (OpenCode) are used for routine tasks to preserve quota on premium providers (Z.ai, xAI) for complex operations.

2. **Cost Optimization**: The configuration prioritizes free models (`opencode/*-free`) for everyday tasks while reserving premium models for tasks requiring their specific strengths.

3. **Performance Tiering**: Models are tiered by capability and speed:
   - **Flash Variants** (`*-flash`): Fastest responses, lowest cost, ideal for quick lookups and simple tasks
   - **Standard Variants** (no suffix): Balanced performance for general-purpose work
   - **High/Max Variants**: Enhanced capability for complex reasoning tasks

4. **Suggested Usage Pattern**:
   - Use **@orchestrator** for complex, multi-step tasks requiring coordination and planning
   - Use **@explorer** for codebase navigation, pattern detection, and symbol lookup
   - Use **@librarian** for documentation research and external API lookup
   - Use **@oracle** for high-stakes architectural decisions and complex reasoning
   - Use **@designer** for UI/UX tasks, frontend components, and visual design
   - Use **@fixer** for straightforward coding tasks and implementations
   - Reserve **Premium Models** (Z.ai, xAI) for tasks where quality is critical

This configuration represents a personalized setup balancing performance, cost, and reliability based on individual usage patterns and provider strengths.


### Plugins

The OpenCode configuration utilizes several plugins to extend its core functionality. These plugins are defined in the `opencode.jsonc` configuration file and provide integration with external services and additional features.

**oh-my-opencode-slim@latest**

The oh-my-opencode-slim plugin is a lightweight, focused agent collection for OpenCode that provides essential development capabilities without the overhead of the full oh-my-opencode suite. This slim edition delivers a curated set of specialized agents optimized for efficient task delegation and rapid development workflows. Unlike the full version, the slim plugin offers a streamlined agent architecture designed for users who need core agent functionality with minimal resource consumption and faster initialization times.

**@nick-vi/opencode-type-inject@latest**

The type-inject plugin provides advanced type inference and injection capabilities for OpenCode. This plugin enhances the AI's understanding of type systems across different programming languages, enabling more accurate code completion and type-aware refactoring operations. It integrates with OpenCode's language server protocol to provide real-time type information and suggestions.

---


## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations.
This configuration includes both manually configured MCPs and pre-installed MCPs from the oh-my-opencode-slim plugin.

### Manually Configured MCPs

The following MCPs are explicitly configured in the `opencode.jsonc` file:

**figma-desktop**

The Figma Desktop MCP enables seamless integration with Figma for design-related operations. 
This MCP allows OpenCode to interact with Figma's desktop application, enabling design context retrieval, 
UI code generation, and design system exploration directly from Figma files.

**github**

The GitHub MCP provides comprehensive integration with GitHub for repository operations, 
pull request management, issue tracking, and code search. 
This MCP enables OpenCode to interact with GitHub's API for various development workflows directly from the conversation interface.

**jira**

The Jira MCP integrates with Atlassian Jira for project management operations including issue tracking, 
sprint management, and workflow automation. This MCP connects to both Jira and Confluence, 
enabling seamless access to project management data.

**serena**

The Serena MCP server provides advanced code intelligence capabilities including precise symbol navigation,
semantic search, and AST-aware code operations. This MCP is essential for the Serena agent's functionality,
enabling token-efficient code retrieval and modifications.

**vision**

The Vision MCP provides visual analysis capabilities through Z.ai's vision models. This MCP enables image understanding,
visual content analysis, and image-based reasoning tasks. It connects to Z.ai's vision API to process and analyze
visual inputs alongside code and text.

### Pre-installed MCPs from Oh-My-Opencode-Slim

The oh-my-opencode-slim plugin includes three pre-configured MCP servers that provide essential development tools:

| MCP         | Purpose                         | Default Assignment          |
|-------------|---------------------------------|-----------------------------|
| `websearch` | Real-time web search via Exa AI | `orchestrator`, `librarian` |
| `context7`  | Official library documentation  | `librarian`                 |
| `grep_app`  | GitHub code search via grep.app | `librarian`                 |

**MCP Descriptions:**

- **websearch** - Provides real-time web search capabilities via Exa AI. This MCP enables agents to search for current information, documentation, and code examples from across the web.

- **context7** - Provides access to up-to-date official documentation and code examples for various libraries and frameworks. This MCP fetches version-specific documentation directly from the source, ensuring accurate and current information for library usage and API references.

- **grep_app** - Enables ultra-fast code search across millions of public GitHub repositories. This MCP allows agents to search for code patterns, find real-world implementation examples, and discover how others have solved similar problems.

These pre-installed MCPs are automatically available when the oh-my-opencode-slim plugin is enabled. MCP access is controlled via per-agent permissions in the configuration. See the [official documentation](https://github.com/alvinunreal/oh-my-opencode-slim/blob/master/docs/quick-reference.md#mcp-servers) for details on MCP assignment syntax and global disabling options.

---


## Skills

The skills system in OpenCode provides a modular way to extend the assistant's capabilities with specialized knowledge and workflows. This configuration includes skills installed via Vercel's official skills.sh system. Note that skills are installed to `~/.agents/skills/` via the skills.sh system, not in the local `skills/` directory of this repository.

#### Skills List

The following skills are available in this configuration, organized by category:

**Document & File Processing**
- **docx** - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when OpenCode needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
- **xlsx** - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. Use when OpenCode needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modifying existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas
- **pdf** - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. Use when OpenCode needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale
- **pptx** - Presentation creation, editing, and analysis for PowerPoint (.pptx) files including layouts, comments, and speaker notes. Use when OpenCode needs to work with presentations for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks

**Development Workflow**
- **receiving-code-review** - Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
- **requesting-code-review** - Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- **vercel-react-best-practices** - React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements

**Skill Management**
- **find-skills** - Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Use when the user is looking for functionality that might exist as an installable skill
- **skill-creator** - Guide for creating effective skills. Use when users want to create a new skill (or update an existing skill) that extends OpenCode's capabilities with specialized knowledge, workflows, or tool integrations
- **command-creator** - Guide for creating effective OpenCode slash commands. Use when users ask to "create a command", "make a slash command", "add a command", or want to document a workflow as a reusable command. Essential for creating optimized, agent-executable slash commands with proper structure and best practices

**Programming Language Patterns**
- **async-python-patterns** - Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations
- **python-packaging** - Create distributable Python packages with proper project structure, setup.py/pyproject.toml, and publishing to PyPI. Use when packaging Python libraries, creating CLI tools, or distributing Python code
- **python-performance-optimization** - Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance
- **python-testing-patterns** - Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices
- **rust-best-practices** - Guide for writing idiomatic Rust code based on Apollo GraphQL's best practices handbook. Use when writing, reviewing, or refactoring Rust code, implementing error handling, or optimizing performance
- **golang-pro** - Use when building Go applications requiring concurrent programming, microservices architecture, or high-performance systems. Invoke for goroutines, channels, Go generics, gRPC integration
- **javascript-testing-patterns** - Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows
- **modern-javascript-patterns** - Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns for writing clean, efficient JavaScript code. Use when refactoring legacy code, implementing modern patterns, or optimizing JavaScript applications
- **typescript-advanced-types** - Master TypeScript's advanced type system including generics, conditional types, mapped types, template literals, and utility types for building type-safe applications. Use when implementing complex type logic, creating reusable type utilities, or ensuring compile-time type safety in TypeScript projects

**Memory Management**
- **mnemonics** - Memory management system for context retention and compounded engineering practices. Use when the user explicitly says "remember", "recall", or "forget" with memory content. Handles storage, retrieval, and deletion of project knowledge including architectural decisions, design patterns, learnings, preferences, issues, and context. Automatically classifies memory types and manages circular references between related memories

**Other**
- **algorithmic-art** - Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations
- **web-design-guidelines** - Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices"
- **next-best-practices** - Next.js best practices - file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, image/font optimization, and bundling
- **agent-browser** - Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task
- **simplify** - Simplify and refine recently modified code for clarity and consistency. Use after writing code to improve readability without changing functionality
- **frontend-design** - Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications

---


## Commands

The commands directory is available for custom slash commands that extend OpenCode's interaction capabilities. Currently, no custom commands are configured in this setup. Commands can be added to the `./commands/` directory and will be migrated along with other configuration files during the build process.

---


## Agents

OpenCode employs a sophisticated agent system where specialized AI agents handle different types of tasks. The agent architecture enables parallel task execution, context-aware processing, and delegation based on task complexity and requirements.

#### Oh-My-OpenCode-Slim Agents

The oh-my-opencode-slim plugin provides a focused suite of six specialized agents that form the backbone of OpenCode's autonomous capabilities:

- **@orchestrator** - Coordinates complex, multi-step tasks with heavy planning and parallel execution potential
- **@oracle** - Provides strategic architectural guidance and complex reasoning for high-stakes decisions
- **@librarian** - Handles external documentation lookup, API research, and library information retrieval
- **@explorer** - Performs rapid codebase navigation, pattern detection, and symbol exploration
- **@designer** - Creates polished UI/UX designs, frontend components, and visual experiences
- **@fixer** - Executes well-defined coding tasks with speed and precision

These agents work together to provide comprehensive coverage of development tasks while maintaining efficiency through the slim architecture.

#### Custom Agents

This configuration includes a custom primary agent designed to enhance OpenCode's task routing capabilities:

**Courier - Ultra-Fast Task Router**

Courier serves as the primary agent for intelligent task routing. It is an ultra-lightweight and fast task router optimized for oh-my-opencode-slim. Courier excels at responding quickly to simple queries while intelligently delegating complex tasks to appropriate specialized agents.

**Key characteristics:**
- **Direct First**: Answers simple/trivial prompts directly with concise responses (including short code snippets when needed)
- **Smart Delegation**: Only delegates when truly necessary, following a strict preference order: direct answer > single delegation > ask for clarification
- **Speed Optimized**: Prioritizes response speed above all else, keeping all communication extremely concise
- **Specialist Routing**: Routes to @orchestrator (complex coordination), @explorer (codebase context), @librarian (research), @oracle (strategic decisions), @designer (UI/UX), or @fixer (implementation) based on task requirements

Courier is configured as the primary agent (`mode: primary`) with low temperature (0.3) for consistent, fast routing decisions using the `xai/grok-4-1-fast-non-reasoning` model.

---


## Reference Links

The following resources provide additional information about skills, plugins, and the Vercel skills.sh system referenced in this configuration:

- **Vercel Skills.sh**: https://skills.sh - The official skills installation and management system for OpenCode, providing community-maintained skills for various development tasks and domains.
- **OpenCode Documentation**: https://opencode.ai/docs - Official documentation for OpenCode configuration, plugin development, and usage guides.
- **Oh-My-OpenCode-Slim Plugin**: https://github.com/alvinunreal/oh-my-opencode-slim - A lightweight, focused agent collection providing essential development capabilities without the overhead of the full suite, available through the OpenCode plugin registry.
- **Type-Inject Plugin**: https://github.com/nick-vi/opencode-type-inject - Advanced type inference and injection capabilities for OpenCode, enhancing type system understanding across programming languages.
- **Figma Desktop MCP**: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server - Official MCP server for Figma integration, enabling design context retrieval and UI code generation.
- **GitHub MCP**: https://github.com/github/github-mcp-server - Official MCP server for GitHub API integration, enabling repository operations and issue management.
- **Jira MCP**: https://github.com/sooperset/mcp-atlassian - Official MCP server for Atlassian Jira and Confluence integration, enabling project management workflows.
- **Serena MCP**: https://github.com/oraios/serena - Advanced code intelligence MCP providing precise symbol navigation and AST-aware operations.
- **Vision MCP**: https://github.com/z-ai-org/mcp-server - Visual analysis MCP powered by Z.ai vision models for image understanding and visual content analysis.
- **OpenRouter**: https://openrouter.ai - Unified API for accessing multiple AI models from various providers through a single interface.
