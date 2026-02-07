# AGENTS.md - Agents' Basic Accomplishments and Rules


---

## Maximum Truth Seeking

- Pursue optimal solutions relentlessly: Never abandon the search for better practices or fixes; always ask probing questions until certainty is achieved.
- Absolute honesty: Identify and openly state any problems, flaws, or uncertainties without hesitation or concealment.
- Emotion-free cognition: Maintain detached, logical thinking; strip all emotional bias from reasoning processes.
- Perfection commitment: Uphold claims only when verified; strive for flawless execution and accuracy in every operation.

---

## Precision Code Operations

For tasks needing precise code access or edits: use Serena MCP tools unless the MCP is down. Avoid noisy or inefficient methods like full-file read() or grep.

>CRITICAL:
>When you have doubts about the tools, you can always refer to [full list of Serena’s tools](https://oraios.github.io/serena/01-about/035_tools.html). 
>If no need, then do not refer, as reading external documents requires more tokens.

### Key Tools

**Symbol Operations**

- **find_symbol**: Performs global or local search for code symbols using language server backend. Ideal for locating classes, functions, and variables with precise name matching and optional depth control.
- **find_referencing_symbols**: Finds all references to a specific symbol throughout the codebase. Essential for understanding usage patterns and impact analysis before refactoring.
- **replace_symbol_body**: Replaces the full definition of a symbol using language server refactoring capabilities. Provides safe, context-aware modifications that maintain code integrity.
- **rename_symbol**: Renames a symbol throughout the entire codebase using language server refactoring. Ensures all references are updated consistently across all files.

**File Operations**

- **replace_lines**: Replaces a range of lines within a file with new content. Requires prior verification through read operations to ensure correctness.
- **insert_after_symbol**: Inserts content after the end of a symbol's definition. Perfect for adding methods to classes or appending code after functions.
- **insert_before_symbol**: Inserts content before the beginning of a symbol's definition. Useful for adding imports before the first symbol or prepending code to functions.
- **delete_lines**: Deletes a specified range of lines from a file. Enables precise code removal while maintaining overall file structure.

**Analysis & Navigation**

- **get_symbols_overview**: Retrieves a high-level overview of all symbols in a file, grouped by kind. Provides quick understanding of file structure before targeted operations.
- **search_for_pattern**: Flexible regex-based pattern search across the codebase. Supports context lines, glob patterns, and file filtering for powerful code discovery.

**Project Management**

- **activate_project**: Activates a project by name or path, setting the working context for all Serena operations. Essential step before working with any codebase.
- **check_onboarding_performed**: Verifies whether project onboarding was completed. Ensures Serena has necessary context about build commands, testing setup, and project structure.

**Memory System**

- **write_memory**: Stores project-specific knowledge as named memories. Enables persistent context for future sessions about architecture patterns, conventions, or learned solutions.
- **read_memory**: Retrieves stored project memories. Allows agents to access previously learned information about the codebase without re-analysis.

### Usage Guidelines

**When to Use Serena Tools**

Always prefer Serena tools over generic file operations for symbol-level tasks. Use **find_symbol** and **find_referencing_symbols** instead of grep for locating code. Use **replace_symbol_body**, **insert_after_symbol**, and **insert_before_symbol** instead of full file edits for targeted modifications. Reserve generic tools like **read_file** and **search_for_pattern** for scenarios where symbol-based operations are insufficient.

**Best Practices**

1. **Activate First**: Always call **activate_project** before any Serena operations to establish proper project context.
2. **Verify Onboarding**: Use **check_onboarding_performed** at conversation start to ensure Serena has project-specific knowledge.
3. **Think Before Acting**: Leverage **think_about_task_adherence** and **think_about_whether_you_are_done** at critical checkpoints to maintain task alignment and completion verification.
4. **Memory for Efficiency**: Use **write_memory** to store learned patterns and **read_memory** to avoid re-exploration in subsequent sessions.
5. **Minimal Changes**: Prefer targeted symbol operations over broad file edits to reduce token consumption and improve precision.

**Tool Selection Priority**

- **Symbol location**: **find_symbol** → **get_symbols_overview** → **search_for_pattern**
- **Code modification**: **replace_symbol_body** → **replace_lines** → **read_file** + **edit**
- **Reference analysis**: **find_referencing_symbols** → **search_for_pattern** → manual inspection
- **New code insertion**: **insert_after_symbol** / **insert_before_symbol** → manual edit → full file rewrite

---