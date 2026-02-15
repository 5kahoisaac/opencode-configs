# AGENTS.md - Agents' Basic Accomplishments and Rules

---

## Maximum Truth Seeking

- Pursue optimal solutions relentlessly; never abandon search for better practices/fixes.
- Absolute honesty: State problems/flaws/uncertainties openly and immediately.
- Emotion-free cognition: Eliminate emotional bias from all reasoning.
- Perfection commitment: Verify every claim; execute with maximum accuracy.

---

## Precision Code Operations

Prioritize **Serena MCP** for code symbol navigation, reference finding, renaming, targeted inserts/deletes/edits.  
Use **QMD MCP** exclusively for non-code knowledge retrieval (notes, .md files, docs, transcripts).  
Avoid shell/grep/read_file unless both MCPs unavailable or inadequate.

>CRITICAL: Differentiate strictly to avoid redundant calls and token waste.

### Serena MCP – Code Precision (LSP-powered)

Call **activate_project** first on new sessions.  
Verify with **check_onboarding_performed**.

**Core Symbol Tools**
- **find_symbol** — precise global/local symbol location
- **find_referencing_symbols** — all references/uses
- **rename_symbol** — safe codebase-wide rename
- **replace_symbol_body** — replace entire symbol definition

**Targeted Edit Tools**
- **insert_after_symbol** — add content after symbol end
- **insert_before_symbol** — add content before symbol start
- **replace_lines** — replace specific line range
- **delete_lines** — remove specific line range

**Analysis Tools**
- **get_symbols_overview** — top-level symbols in file
- **search_for_pattern** — regex fallback (non-symbol cases only)

**Memory Tools**
- **write_memory** / **read_memory** — store/retrieve code patterns

### QMD MCP – Knowledge / Semantic Search

Use **qmd_status** first to confirm collections/index health.

**Search Tools**
- **qmd_search** — fast BM25 keyword/exact match (e.g. file names, phrases)
- **qmd_vector_search** — semantic similarity (conceptual/natural language)
- **qmd_deep_search** — hybrid + rerank (highest quality, slowest)

**Retrieval Tools**
- **qmd_get** — single document by path or docid
- **qmd_multi_get** — multiple documents (list/glob)

**When to Use QMD**  
Only for .md/docs/notes/transcripts/non-code content.  
Never for symbol definitions, references, renames or code edits — route those to Serena.

### MCP Selection Rules (Eliminate Redundancy)

- **Non-code / fuzzy / conceptual / notes / docs** → QMD first (`qmd_vector_search` or `qmd_deep_search`)
- **Code symbols / definitions / references / renames / inserts** → Serena exclusively
- **Hybrid workflow** → QMD for discovery/context → Serena for precise navigation/edits
- **Efficiency** — Prefer QMD speed for knowledge; Serena precision for code surgery

### Best Practices

1. Start sessions: `activate_project` (Serena) + `qmd_status` (QMD)
2. Before tool use: Explicitly decide "QMD or Serena?" in thinking
3. Minimize broad searches; target narrow queries
4. Verify edits: read_file or symbol overview before/after changes
5. Fallback: shell only when MCPs cannot help

---