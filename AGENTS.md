# AGENTS.md - Agents' Basic Accomplishments and Rules

---

## Maximum Truth Seeking

- Pursue optimal solutions relentlessly; never abandon search for better practices/fixes.
- Absolute honesty: State problems/flaws/uncertainties openly and immediately.
- Emotion-free cognition: Eliminate emotional bias from all reasoning.
- Perfection commitment: Verify every claim; execute with maximum accuracy.

---

## Precision Code Operations

Prioritize **Serena MCP** for code symbol navigation, reference finding, renaming,
targeted inserts/deletes/edits.

> CRITICAL: Use `@historian` subagent directly or the **mnemonics** skill for memory operations.
> Serena memory tools are INTERNAL to Serena — NEVER use them for project memories.

### Serena MCP – Code Precision (LSP-powered)

**Session Startup**
1. `activate_project` — connect to project (required first)
2. `check_onboarding_performed` — verify project is initialized
3. `initial_instructions` — load Serena manual if agent seems "lost"

**Symbol Tools (LSP/JetBrains)**
- `find_symbol` — global/local search for classes, methods, functions
- `find_referencing_symbols` — find all usages of a symbol
- `rename_symbol` — safe codebase-wide rename
- `get_symbols_overview` — quick summary of top-level symbols in a file

**Targeted Edit Tools**
- `replace_symbol_body` — replace entire function/class definition
- `insert_after_symbol` / `insert_before_symbol` — add code relative to symbols
- `replace_lines` / `delete_lines` — line-based editing (fallback for non-symbolic)

**File Operations**
- `list_dir` — list directory contents (with recursion option)
- `find_file` — find files by name/pattern
- `search_for_pattern` — regex search (fallback when symbols don't work)

**Thinking Tools (Meta-cognition)**
- `think_about_collected_information` — verify enough data gathered
- `think_about_task_adherence` — check if drifted from goal
- `think_about_whether_you_are_done` — final completion verification

**Memory Tools (INTERNAL to Serena)**
- `write_memory` / `read_memory` / `list_memories` — for Serena's own bookkeeping
- **NOT for project memories** — use `@historian` instead

**Serena Best Practices**
- Prefer `replace_symbol_body` over `replace_lines` for structured code
- Use `restart_language_server` if files modified outside Serena
- Use `think_about_*` tools before committing to complex refactors
- Use `open_dashboard` to monitor logs and tool usage in real-time

### Memory & Semantic Search – Use @historian or mnemonics skill

Memory tools are **ONLY available via the historian subagent**. You have two options:

1. **Direct invocation:** `@historian remember that we use PostgreSQL`
2. **Load mnemonics skill:** Use the skill for detailed guidance on memory types

> **NEVER confuse Serena memory tools with historian memory tools.**
> - `serena_write_memory` / `serena_read_memory` → INTERNAL to Serena for code navigation
> - `memory_remember` / `memory_recall` → Available ONLY via @historian subagent

**Memory Tools (via @historian only)**
- `memory_remember` — create new memories or update existing ones
- `memory_recall` — search and retrieve memories (keyword or semantic)
- `memory_forget` — delete memories by file path
- `memory_list_types` — list available memory types in the project
- `memory_sync` — reindex after manual file changes (rarely needed)

**When to Use @historian**
- Storing project knowledge, decisions, or learnings
- Recalling relevant context from past sessions
- Semantic search across docs, notes, or transcripts
- Reindexing after manual external file modifications

### Tool Selection Table

| Task                                              | Use This                            |
|---------------------------------------------------|-------------------------------------|
| Code symbol navigation (find, rename, references) | Serena                              |
| Code edits (insert, replace, delete)              | Serena                              |
| Store/recall project memories                     | `@historian` or **mnemonics** skill |
| Semantic search across docs/notes                 | `@historian` or **mnemonics** skill |
| Reindex after manual file changes                 | `@historian sync`                   |

### Best Practices

**Serena (Code):**
1. Start sessions: `activate_project` → `check_onboarding_performed`
2. Prefer symbol tools (`replace_symbol_body`) over line edits
3. Use `restart_language_server` if files changed externally
4. Use `think_about_*` tools before finishing complex refactors

**Memory (@historian):**
1. Use `@historian` or load **mnemonics** skill for memory operations
2. **NEVER** use `serena_*_memory` tools for project memories
3. Recall before deciding — check if decision already exists

**General:**
1. Minimize broad searches; target narrow queries
2. Verify edits: read_file or symbol overview before/after changes
3. Fallback: shell only when MCPs cannot help

---
