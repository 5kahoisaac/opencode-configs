# OpenCode Configuration

## Table of Contents

- [Overview](#overview)
- [Available Makefile Commands](#available-makefile-commands)
  - [Build Command](#build-command)
  - [Clean Command](#clean-command)
  - [Help Command](#help-command)
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

The Makefile provides a set of commands to build, clean, and manage the OpenCode configuration. These commands handle the processing of configuration files and prepare them for use with OpenCode.

### Build Command

The build command is the default target that processes all configuration files and prepares them for deployment. When executed, it performs the following operations:

1. Creates and cleans the `./dist` directory to ensure a fresh build environment
2. Loads environment variables from the `.env` file
3. Processes each JSONC file by substituting environment variables using a custom substitution script that only replaces `$VAR` patterns when the corresponding key exists in `.env`
4. Copies the `agents`, `commands`, and `skills` directories to the output location
5. Displays a summary of all generated files in the `./dist` directory

The build process ensures that all sensitive information like API tokens and configuration values are properly injected from environment variables, making the configuration secure and portable across different environments.

### Clean Command

The clean command removes the entire `./dist` directory and all its contents. This command is useful when you want to start fresh with a new build or when you need to remove all generated files from the system. The command simply executes `rm -rf ./dist` and displays a confirmation message indicating that the directory has been cleaned.

### Help Command

The help command displays a comprehensive list of available Makefile targets along with their descriptions. This command provides quick access to documentation without requiring users to read the Makefile directly. The help output includes basic usage examples and explains the overall workflow of the build system.

---


## Configuration

### Providers

This configuration integrates multiple AI model providers to offer a diverse range of capabilities, from lightweight fast responses to deep reasoning tasks. The provider setup is designed to balance cost-effectiveness with performance, utilizing both free and premium models across different use cases.

#### Provider List

The following AI providers are configured in this setup:

**Ollama Cloud**

Ollama Cloud provides local model inference capabilities with excellent privacy and performance characteristics. This configuration uses `ollama-cloud/gemini-3-flash-preview:latest` for writing and content generation tasks, offering fast response times and reasonable context windows at no cost.

**OpenCode**

OpenCode's built-in model hub offers several free models optimized for different task types. The configuration utilizes `opencode/kimi-k2.5-free` for complex reasoning and `opencode/glm-4.7-free` for general-purpose tasks. These models provide a reliable fallback when premium providers are unavailable or exhausted.

**Zen (z.ai)**

Zen (accessible via `zai-coding-plan/` prefix) provides access to advanced GLM models including GLM-4.7 and GLM-4.6 variants. These models offer excellent performance for planning, reasoning, and orchestration tasks. The configuration uses various Zen models for different agent categories, balancing between flash variants for speed and full variants for depth.

**xAI (Grok)**

xAI provides the Grok family of models, specifically `xai/grok-code-fast-1` for exploration tasks and `grok-4-1-fast-reasoning` for visual engineering. These models excel at code understanding and fast reasoning, making them ideal for tasks requiring quick analysis and pattern recognition.


#### Models Configuration

The `oh-my-opencode.jsonc` file contains a sophisticated model assignment system that categorizes tasks and assigns appropriate models based on complexity and requirements. This configuration represents a carefully tuned balance between API rate limits, response quality, and cost management.

**Task Categories and Model Selection**

The configuration defines several task categories in the `categories` section, each optimized for specific workload types:

- **Visual Engineering Tasks** (`visual-engineering`): Uses `grok-4-1-fast-reasoning` for UI/UX design tasks that benefit from rapid pattern recognition and spatial reasoning capabilities.

- **Ultra-Brain Tasks** (`ultrabrain`): Deploys `opencode/kimi-k2.5-free` with `xhigh` variant for mathematically intensive or deeply logical problems requiring extensive reasoning chains.

- **Artistry Tasks** (`artistry`): Leverages `zai-coding-plan/glm-4.7` with `max` variant for creative tasks that benefit from higher token generation and imaginative output.

- **Quick Tasks** (`quick`): Utilizes `zai-coding-plan/glm-4.5-flash` for simple, straightforward tasks that benefit from minimal latency and reduced cost.

- **Unspecified Low Complexity** (`unspecified-low`): Assigns `zai-coding-plan/glm-4.6` for routine tasks without specific categorization needs.

- **Unspecified High Complexity** (`unspecified-high`): Uses `zai-coding-plan/glm-4.7` with `max` variant for complex, uncategorized tasks requiring comprehensive analysis.

- **Writing Tasks** (`writing`): Employs `ollama-cloud/gemini-3-flash-preview:latest` for documentation and content generation, taking advantage of its strong writing capabilities.

**Agent-Specific Model Assignments**

Individual agents in the `agents` section receive specialized model assignments optimized for their specific functions:

- **Sisyphus** (Orchestration): `zai-coding-plan/glm-4.7` for complex task planning and delegation
- **Hephaestus** (Build): `opencode/kimi-k2.5-free` for code generation and implementation
- **Oracle** (High-Level Reasoning): `opencode/glm-4.7-free` with `high` variant for complex problem analysis
- **Librarian** (Research): `opencode/glm-4.7-free` for documentation lookup and information retrieval
- **Explore** (Codebase Analysis): `xai/grok-code-fast-1` for rapid code navigation and pattern detection
- **Multimodal Looker**: `zai-coding-plan/glm-4.6-v` for image and document analysis
- **Prometheus** (Planning): `zai-coding-plan/glm-4.7` with `max` variant for comprehensive planning tasks
- **Metis** (Pre-Planning): `zai-coding-plan/glm-4.6-v` with `max` variant for preliminary analysis
- **Momus** (Review): `zai-coding-plan/glm-4.6-v` with `medium` variant for balanced review tasks
- **Atlas** (Context): `zai-coding-plan/glm-4.7-flash` for quick context retrieval and summarization
- **Sisyphus Junior** (Focused Task Executor): `opencode/gpt-5-nano` for single, straightforward tasks with disciplined execution and no delegation

**Currency API Rate Limits and Suggested Setup**

The provider configuration considers several factors for optimal performance:

1. **Rate Limit Management**: Different providers have varying rate limits. Free providers (OpenCode) are used for routine tasks to preserve quota on premium providers (Zen/z.ai, xAI) for complex operations.

2. **Cost Optimization**: The configuration prioritizes free models (`opencode/*-free`) for everyday tasks while reserving premium models for tasks requiring their specific strengths.

3. **Performance Tiering**: Models are tiered by capability and speed:
   - **Flash Variants** (`*-flash`): Fastest responses, lowest cost, ideal for quick lookups and simple tasks
   - **Standard Variants** (no suffix): Balanced performance for general-purpose work
   - **High/Max Variants**: Enhanced capability for complex reasoning tasks

4. **Suggested Usage Pattern**:
   - Use **Quick** category for simple edits, typo fixes, and basic queries
   - Use **Visual Engineering** for frontend and UI tasks requiring spatial reasoning
   - Use **Ultrabrain** for algorithm design and complex logical problems
   - Use **Unspecified-High** for ambiguous tasks that might require deep analysis
   - Reserve **Premium Models** (Zen, xAI) for tasks where quality is critical

This configuration represents a personalized setup balancing performance, cost, and reliability based on individual usage patterns and provider strengths.


### Plugins

The OpenCode configuration utilizes several plugins to extend its core functionality. These plugins are defined in the `opencode.jsonc` configuration file and provide integration with external services and additional features.

**oh-my-opencode@latest**

The oh-my-opencode plugin serves as the foundational extension for OpenCode, providing essential agent capabilities and workflow enhancements. This plugin introduces a comprehensive set of specialized agents designed to handle various development tasks autonomously. The plugin enables advanced orchestration features, allowing OpenCode to delegate complex tasks to appropriate agents based on the nature of the request. It includes agents for codebase exploration, documentation lookup, planning, and handling both conventional and non-conventional development challenges.

**@nick-vi/opencode-type-inject@latest**

The type-inject plugin provides advanced type inference and injection capabilities for OpenCode. This plugin enhances the AI's understanding of type systems across different programming languages, enabling more accurate code completion and type-aware refactoring operations. It integrates with OpenCode's language server protocol to provide real-time type information and suggestions.

**opencode-supermemory@latest**

The supermemory plugin introduces persistent memory capabilities to OpenCode, allowing the AI assistant to maintain context and learn from previous interactions within a session. This plugin enables OpenCode to store and retrieve information about the project, development patterns, and user preferences across different sessions, significantly improving the assistant's ability to provide personalized and context-aware assistance.

---


## MCPs

Model Context Protocol (MCP) servers extend OpenCode's capabilities by providing specialized tools and integrations. This configuration includes both manually configured MCPs and pre-installed MCPs from the oh-my-opencode plugin.

### Manually Configured MCPs

The following MCPs are explicitly configured in the `opencode.jsonc` file:

**figma-desktop**

The Figma Desktop MCP enables seamless integration with Figma for design-related operations. This MCP allows OpenCode to interact with Figma's desktop application, enabling design context retrieval, UI code generation, and design system exploration directly from Figma files.

**github**

The GitHub MCP provides comprehensive integration with GitHub for repository operations, pull request management, issue tracking, and code search. This MCP enables OpenCode to interact with GitHub's API for various development workflows directly from the conversation interface.

**jira**

The Jira MCP integrates with Atlassian Jira for project management operations including issue tracking, sprint management, and workflow automation. This MCP connects to both Jira and Confluence, enabling seamless access to project management data.

**serena**

The Serena MCP server provides advanced code intelligence capabilities including precise symbol navigation, semantic search, and AST-aware code operations. This MCP is essential for the Serena agent's functionality, enabling token-efficient code retrieval and modifications.

### Pre-installed MCPs from Oh-My-Opencode

The oh-my-opencode plugin includes several pre-configured MCP servers that provide essential development tools:

- **Context7** - Provides access to official documentation and code examples for various libraries and frameworks
- **Code Search (Exa)** - Enables real-time web search for programming-related queries and code examples
- **Web Search** - Provides general web search capabilities for current information and documentation
- **Google Search** - Enables Google-powered web search with URL analysis capabilities

These pre-installed MCPs are automatically available when the oh-my-opencode plugin is enabled, providing a comprehensive set of tools for research, documentation lookup, and web-based information retrieval without additional configuration.

---


## Skills

The skills system in OpenCode provides a modular way to extend the assistant's capabilities with specialized knowledge and workflows. This configuration includes skills installed via Vercel's official skills.sh system, located in the `skills` directory.

#### Skills List

The following skills are available in this configuration:

- **algorithmic-art** - Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Enables generation of original algorithmic art, flow fields, and particle systems.
   
- **command-creator** - Guide for creating effective OpenCode slash commands. Essential for creating optimized, agent-executable slash commands with proper structure and best practices.

- **docx** - Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction.

- **find-skills** - Helps users discover and install agent skills when looking for functionality that might exist as an installable skill.

- **pdf** - Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.

- **pptx** - Presentation creation, editing, and analysis for PowerPoint (.pptx) files including layouts, comments, and speaker notes.

- **receiving-code-review** - Use when receiving code review feedback, before implementing suggestions. Requires technical rigor and verification.

- **requesting-code-review** - Use when completing tasks, implementing major features, or before merging to verify work meets requirements.

- **skill-creator** - Guide for creating effective skills. Used when users want to create a new skill that extends OpenCode's capabilities.

- **vercel-react-best-practices** - React and Next.js performance optimization guidelines from Vercel Engineering. Ensures optimal performance patterns for React components, data fetching, and bundle optimization.

- **web-design-guidelines** - Review UI code for Web Interface Guidelines compliance. Use when asked to review UI, check accessibility, audit design, or check site against best practices.

- **xlsx** - Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization.

- **next-best-practices** - Next.js best practices - file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, image/font optimization, bundling.

---


## Commands

The commands directory contains custom slash commands that extend OpenCode's interaction capabilities:

**supermemory-init**

A comprehensive command for initializing persistent memory with comprehensive codebase knowledge. This command performs deep research on the project including tech stack, architecture, build commands, conventions, and team workflows. It systematically saves memories across project-scoped and user-scoped contexts, enabling OpenCode to maintain context across sessions and become more effective over time.

---


## Agents

OpenCode employs a sophisticated agent system where specialized AI agents handle different types of tasks. The agent architecture enables parallel task execution, context-aware processing, and delegation based on task complexity and requirements.

#### Oh-My-OpenCode Agents

The oh-my-opencode plugin provides a comprehensive suite of agents that form the backbone of OpenCode's autonomous capabilities. For detailed documentation on all available agents and their features, please refer to the official documentation:

- [Oh-My-OpenCode Features Documentation](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/features.md)

The plugin includes agents for various development tasks including codebase exploration, documentation lookup, planning, and handling both conventional and non-conventional development challenges.

#### Custom Agents

This configuration includes custom agents designed to enhance OpenCode's orchestration and code analysis capabilities:

**Hermes - Orchestration Router Agent**

Hermes serves as the router agent for intelligent task orchestration. It analyzes user prompts and determines the most efficient handling strategy using a structured decision flow. Hermes excels at classifying tasks and delegating them to appropriate specialized agents without unnecessary overhead. The agent follows a minimalist approach, avoiding aggressive parallel execution and prioritizing direct responses when possible. Hermes uses the `xai/grok-4-1-fast-non-reasoning` model with optimized temperature settings for consistent routing decisions. This agent is particularly valuable for maintaining clean task delegation patterns and preventing unnecessary agent spawns.

---


## Reference Links

The following resources provide additional information about skills, plugins, and the Vercel skills.sh system referenced in this configuration:

- **Vercel Skills.sh**: https://skills.sh - The official skills installation and management system for OpenCode, providing community-maintained skills for various development tasks and domains.
- **OpenCode Documentation**: https://opencode.ai/docs - Official documentation for OpenCode configuration, plugin development, and usage guides.
- **Oh-My-OpenCode Plugin**: https://github.com/code-yeongyu/oh-my-opencode - The foundational plugin providing comprehensive agent capabilities, available through the OpenCode plugin registry.
- **OpenSupermemory Plugin**: https://github.com/supermemoryai/opencode-supermemory - The opencode-supermemory plugin repository providing persistent memory capabilities for OpenCode.
- **Figma Desktop MCP**: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server - Official MCP server for Figma integration, enabling design context retrieval and UI code generation.
- **GitHub MCP**: https://github.com/github/github-mcp-server - Official MCP server for GitHub API integration, enabling repository operations and issue management.
- **Jira MCP**: https://github.com/sooperset/mcp-atlassian - Official MCP server for Atlassian Jira and Confluence integration, enabling project management workflows.
- **Serena MCP**: https://github.com/oraios/serena - Advanced code intelligence MCP providing precise symbol navigation and AST-aware operations.
