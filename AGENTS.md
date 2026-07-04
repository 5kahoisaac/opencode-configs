# Agent Guidelines

## Working Style

* Think before coding: restate the goal, identify the smallest change that achieves it, and state your plan in one or two sentences before editing.
* Simplicity first: prefer the boring, direct solution; no speculative abstractions, options, or config flags nobody asked for.
* Surgical changes: touch only what the task requires; match the surrounding code's style; leave unrelated cleanup out of the diff.
* Verify before declaring done: run the narrowest command that proves the change works, and report what you ran and what it showed.
* If requirements are ambiguous, resolve what you can from the codebase and ask one precise question about the rest — don't guess silently.

## Truthfulness

* State blockers, risks, missing information, and uncertainty early.
* Separate facts, assumptions, and guesses.
* Be clear about confidence. Qualify weak evidence; commit when evidence is strong.
* Verify important factual claims with primary or current sources.
* Follow the evidence. Drop bad plans without defending them.

## Communication

* Lead with the result, decision, or blocker.
* Think fully. Explain briefly.
* Use direct sentences.
* Keep caveats that matter.
* Cut filler, repetition, and process narration.
* Use fragments when they are clearer.
* Do not make blunt writing less precise.

**Compression test:** Cut any sentence that does not change the decision, action, or understanding.

---

## Code Intelligence (mcp-proxy, retrieve_tools mode)

Tools are hidden behind `retrieve_tools`. Names are not visible upfront. Search by intent, then call. Never assume a tool name.

**Query by intent — the right backend surfaces via BM25:**

* Exact symbol, references, implementations, rename, safe-delete, diagnostics → query `"symbol references rename diagnostics"` (Serena, LSP-precise).
* Fuzzy / natural-language / semantic discovery ("where do we send email") → query `"search code graph semantic"` (codebase-memory).
* Callers, callees, data-flow, cross-service, blast-radius, complexity hot-paths → query `"trace callers impact cyclomatic data-flow"` (codebase-memory).
* Structural AST pattern, find-by-shape, debug a pattern → query `"ast pattern syntax-tree structural"` (ast-grep).
* Architecture overview, clusters, ADR → query `"architecture overview ADR"` (codebase-memory).

**Pick the call variant by effect — wrong variant gets blocked by permissions:**

* Reads (find / search / trace / diagnostics / architecture) → `call_tool_read`.
* Edits (replace_symbol_body, insert_*, rename_symbol) → `call_tool_write`.
* Destructive (safe_delete_symbol, delete_project) → `call_tool_destructive`.

**Init once per repo before any code-intel query — otherwise results come back empty:**

* Serena: `activate_project`. One project at a time; re-activate on repo switch.
* codebase-memory: `index_repository`.
* ast-grep: no init.

**Routing rules:**

* Know the exact symbol → Serena. Don't know the name → codebase-memory search first.
* Caller/callee only → either. Data-flow, cross-service, or complexity → codebase-memory.
* Editing code → Serena symbol tools, not regex replace.
* Structural shape, not a name → ast-grep.
* If a query returns nothing, re-query with different keywords before falling back to grep/read.

---

## OpenCode Delegation (Oh-My-OpenAgent)

Model routing lives in `oh-my-openagent.json` — do not hardcode model choices in prompts; pick the right agent or category and let routing work.

* Complex multi-step work → delegate to **@sisyphus** (orchestrator).
* Codebase navigation / symbol lookup → **@explore**. External docs / library research → **@librarian**.
* High-stakes architecture or hard debugging → **@oracle**. Plan review / quality gate → **@momus**.
* For `task()` categories: `visual-engineering` (UI), `ultrabrain` (hard logic), `quick` (trivial edits), `writing` (docs), `git` (all git ops).
* High-effort variants (`high`, `xhigh`, `max`, ultrawork) cost real money/rate budget — reserve them for work where quality is critical.
* If a model route fails, runtime fallback handles it — do not manually retry the same model in a loop.

---

<!-- headroom:rtk-instructions -->
# RTK (Rust Token Killer) - Token-Optimized Commands

When running shell commands, **always prefix with `rtk`**. This reduces context
usage by 60-90% with zero behavior change. If rtk has no filter for a command,
it passes through unchanged — so it is always safe to use.

## Key Commands
```bash
# Git (59-80% savings)
rtk git status          rtk git diff            rtk git log

# Files & Search (60-75% savings)
rtk ls <path>           rtk read <file>         rtk grep <pattern>
rtk find <pattern>      rtk diff <file>

# Test (90-99% savings) — shows failures only
rtk pytest tests/       rtk cargo test          rtk test <cmd>

# Build & Lint (80-90% savings) — shows errors only
rtk tsc                 rtk lint                rtk cargo build
rtk prettier --check    rtk mypy                rtk ruff check

# Analysis (70-90% savings)
rtk err <cmd>           rtk log <file>          rtk json <file>
rtk summary <cmd>       rtk deps                rtk env

# GitHub (26-87% savings)
rtk gh pr view <n>      rtk gh run list         rtk gh issue list

# Infrastructure (85% savings)
rtk docker ps           rtk kubectl get         rtk docker logs <c>

# Package managers (70-90% savings)
rtk pip list            rtk pnpm install        rtk npm run <script>
```

## Rules
- In command chains, prefix each segment: `rtk git add . && rtk git commit -m "msg"`
- For debugging, use raw command without rtk prefix
- `rtk proxy <cmd>` runs command without filtering but tracks usage
<!-- /headroom:rtk-instructions -->