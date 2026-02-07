# Your Role

You're an expert on Software Development with solid knowledge of programming, system design, and workflow design. You are also familiar with agentic AI.

To achieve a maximum truth-seeking purpose, please:
- Pursue optimal solutions relentlessly: Never abandon the search for better practices or fixes; always ask probing questions until certainty is achieved.
- Absolute honesty: Identify and openly state any problems, flaws, or uncertainties without hesitation or concealment.
- Emotion-free cognition: Maintain detached, logical thinking; strip all emotional bias from reasoning processes.
- Perfection commitment: Uphold claims only when verified; strive for flawless execution and accuracy in every operation.

From now on, I'm going to ask your opinion and ideas about my thinking. Please help me figure out my mind mess and provide possible suggestions.

---

# Task

I'm a user of OpenCode with the "oh-my-opencode" plugin. Now, I plan to reference the plugin "@knikolov/opencode-plugin-simple-memory",
and develop a logic to handle the compounded engineering stuff.

Recently, I read some articles about compounded engineering and context engineering.
I found that the compounded engineer is perhaps the suitable way to achieve the context engineer principle in agentic programming.
It helps the agents reducing time to figure out the issue by viewing the recorded formed finding.
And a solid indexing of recorded findings helps agent avoid overthinking (reduce tokens) and avoid overhead cost.

The workflow of the compounded engineering is like: Plan → Work → Review → Compound → Repeat

And actually, the "oh-my-opencode" plugin already helps the "Plan" and "Work" steps (you can refer to its orchestration guide).
For my side, I just need to answer the question from "Prometheus" agent,
then "Prometheus" agent will help writing a detailed plan for me.
Reviewing the plan in ".sisyphus/plans/" and tell them to "/start-work".
Observing the tasks complete with verification and **review** the result.

The current workflow in "oh-my-opencode" is just missing the "Compound" step after the revision is completed.
Therefore, I'm willing to fill the missing piece (Compound" step) by referring to the idea of the "opencode-plugin-simple-memory" plugin and,
build a feature "mnemonics".

---

# Concept and Requirements

## How to store the memories

"opencode-plugin-simple-memory" will store the memories in ".opencode/memory/" as daily logfmt files. 

For my plugin, I want the store the memory folder structure with grouping by the following "Memory Types" and stored as *.md format as:
- architectural decision → ".opencode/memory/decision/architectural/*.md "
- design decision → ".opencode/memory/decision/design/*.md"
- unclassified decision → ".opencode/memory/decision/*.md"
- learning → ".opencode/memory/learning/*.md"
- user preference → ".opencode/memory/preference/user/*.md"
- project preference → ".opencode/memory/preference/project/*.md"
- blocker → ".opencode/memory/blocker/*.md"
- issue → ".opencode/memory/blocker/issue/*.md"
- context (some business context etc.) → ".opencode/memory/context/*.md "
- recurring pattern → ".opencode/memory/pattern/recurring/*.md"
- conventions pattern → ".opencode/memory/pattern/conventions/*.md"
- unclassified pattern → ".opencode/memory/pattern/*.md"

## Research Techniques

### File-based
- README.md, CONTRIBUTING.md, AGENTS.md, CLAUDE.md
- Package manifests (package.json, Cargo.toml, pyproject.toml, go.mod)
- Config files (.eslintrc, tsconfig.json, .prettierrc)
- CI/CD configs (.github/workflows/)

### Git-based
- `git log --oneline -20` - Recent history
- `git branch -a` - Branching strategy
- `git log --format="%s" -50` - Commit conventions
- `git shortlog -sn --all | head -10` - Main contributors

### Explore Agent
Fire parallel explore queries for broad understanding:
```
@explore What is the tech stack and key dependencies?
@explore What is the project structure? Key directories?
@explore "How do you build, test, and run this project?
@explore What are the main architectural patterns?
@explore What conventions or patterns are used?
```

## How to Allocate the memories

Create a catalog at ".opencode/memory/MEMORIES.md" and do indexing for serval memories followed, 
by the below template example (please help complete the full version, the below is just a rough idea):

```markdown
# MEMORIES.md - Memories Catalog

You are initializing persistent memory for this codebase. This is not just data collection - you're building context that will make you significantly more effective across all future sessions.

---

<!-- Table of Contents MUST not be edited as it is the foundation of the memory type -->
## Table of Contents

- [Decision](#decision)
  - [Architectural Decision](#architectural-decision)
  - [Design Decision](#design-decision)
  - [Unclassified Decision](#unclassified-decision)
- [Learning](#learning)
- [Preference](#preference)
  - [User Preference](#user-preference)
  - [Project Preference](#project-preference)
- [Blocker](#blocker)
- [Issue](#issue)
- [Context](#context)
- [Pattern](#pattern)
  - [Recurring Pattern](#recurring-pattern)
  - [Conventions Pattern](#conventions-pattern)
  - [Unclassified Pattern](#unclassified-pattern)

---

<!-- Each section below order by the memory type of the "Table of Contents" -->
### Decision

<!-- Description of the memory type -->
Decision made in this project

#### Architectural Decision

<!-- Description of the memory type -->
Architectural decision made in this project

<!-- Short description of the memory and reference file path -->
- [**Architectural Principle**](./decision/architectural/priciple.md)
- [**Variable Naming Rules**](./decision/architectural/variable-naming.md)

...

---

...
```

## Available Tools

According to "opencode-plugin-simple-memory" document, it provides five tools:

| Tool              | Description                                       |
|-------------------|---------------------------------------------------|
| `memory_remember` | Store a new memory                                |
| `memory_recall`   | Retrieve memories by scope, type, or search query |
| `memory_update`   | Update an existing memory                         |
| `memory_forget`   | Delete a memory (with audit logging)              |
| `memory_list`     | List all scopes and types for discovery           |

For my plugin, I don't need the `memory_list` as the catalog `.opencode/memory/MEMORIES.md` already provided a clear listing of existing memories,
I would like to combine the idea of `memory_update` and `memory_remember`.

My detailed idea as below:
- `memory_remember`: Identify and analyze the input → classify the memory type, topic, content → Check is there any memory is similar or not → if yes, combine the previous memory; otherwise create the memory with memory template → update the memories catalog if needed → report the result
- `memory_recall`: Scan the memories catalog and find the related memories that related to your "topic" → gather the reference and report the result
- `memory_forget`: Scan the memories and find the matches that willing to delete → if found, delete the related memories (can be a paragraph inside a memory or whole memory file); otherwise do nothing → report the result

**Guidelines**
- Save each distinct insight as a separate memory
- Be concise but include enough context to be useful
- Include the "why" not just the "what" when relevant
- Update memories incrementally as you research (don't wait until the end)

**Good memories examples**
- "Uses Bun runtime and package manager. Commands: bun install, bun run dev, bun test"
- "API routes in src/routes/, handlers in src/handlers/. Hono framework."
- "Auth uses Redis sessions, not JWT. Implementation in src/lib/auth.ts"
- "Never use `any` type - strict TypeScript. Use `unknown` and narrow."
- "Database migrations must be backward compatible - we do rolling deploys"

For the format of each memory, here's the template example:
```markdown
# Project and user coding style <!-- The title of the memory -->

<!-- ↓ The details of the memory, including ↓ -->
- created at: <!-- The file created time -->
- last modified at: <!-- The file last modified time -->

## Overview <!-- The overview of the memory, describing the topic and type of the memory file -->
Project and user coding style:
- "Prefer functional components over class components"
- "Use early returns instead of nested conditionals"
- "Always add JSDoc to exported functions"

---

<!-- ↓ The main content of the memory, including situation that I need to remember this memory, the finding/ details of the memory ↓ -->
## Examples
...

```

## Expected Output Format

Simple of recall:
```
📋 Memories Recall
==============================

Recalled:
  ✓ Basic Coding practice
    → "./opencode/memory/decision/project/basic-coding-practice.md"
  ✓ DatePicker component error message handling
    → "./opencode/memory/issue/date-picker-error-mesage.md"
  ✓ Missing translation files
    → "./opencode/memory/blocker/missing-translation-files.md"

✅ Complete - 4.2s elapsed
```

Simple of remember:
```
📋 Memories Remember
==============================

Changes:
  ✓ Updated: Basic Coding practice
    → "./opencode/memory/decision/project/basic-coding-practice.md"
  ✓ Added: System Error
    → "./opencode/memory/issue/system-error.md"

✅ Complete - 4.2s elapsed
```

Simple of forget:
```
📋 Memories Forgot
==============================

Changes:
  ✓ Updated: Basic Coding practice
    → "./opencode/memory/decision/project/basic-coding-practice.md"
  ✓ Removed: System Error
    → "./opencode/memory/issue/system-error.md"

✅ Complete - 4.2s elapsed
```


## Reflection Phase

Before finishing, reflect:
1. **Completeness**: Did you cover commands, architecture, conventions, gotchas?
2. **Quality**: Are memories concise and searchable?


## Hard Rules

- `memory_recall` is READ ONLY, do not do any modification
- `memory_remember` and `memory_forget` will make changes in the memories, so you MUST always seek confirmation with user, e.g.: Memory of "xxxx" is xxxxx, please confirm the action by [Y/N] or other instruction.

---

# Implementation Plan

Develop "mnemonics" as skill.

Rough idea of the folder structure:
```text
skills/
└── mnemonics/
    ├── SKILL.md
    ├── scripts/
    │   ├── memory-remember.py
    │   ├── memory-recall.py
    │   ├── memory-delete.py
    │   └── catalog-update.py
    └── templates/
        ├── memory-catalog-template.md
        ├── memory-template.md
        └── memory-response-template.md
```

**mnemonics/SKILL.md**
- The skill description of "mnemonics"
- Refer to the **templates** folder and create template for tool or response to other agent
- Using script from **scripts** folder to achieve the tools

**mnemosyne/templates/*.md**
- Templates of different purpose
- Have placeholder to do string replacement

**mnemosyne/scripts/*.py**
- Scripts written in *.py from internal usage
- Scripts to achieve the available tools
- Some script will load the template from **mnemosyne/templates/*.md** and concat the content with string replacement, and then store as memory
- Some script will help the skills to scan the memories catalog and the memory's content, in order to find the matches

---

# Additional Reading & Reference Links
- [A simplified Chinese article related to Compounding Engineering](https://zhuanlan.zhihu.com/p/1993009461451831150)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Simple Memory document and repo](https://github.com/cnicolov/opencode-plugin-simple-memory)
- [OhMyOpenCode documents](https://github.com/code-yeongyu/oh-my-opencode/tree/dev/docs)
- [OhMyOpenCode orchestration guide](https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/understanding-orchestration-system.md)
- [OpenCode plugin development guide](https://gist.github.com/rstacruz/946d02757525c9a0f49b25e316fbe715)