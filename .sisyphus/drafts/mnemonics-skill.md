# Draft: Mnemonics Skill Development

## User's Decisions

### Classification Logic (Hybrid Approach)
- Primary: Agent-driven classification at skill level (LLM analyzes user intent)
- Fallback: If LLM cannot analyze user intent, ask for explicit type specification
- Example: "Remember as architectural decision: ..." or prompt user to specify type

### Similarity Detection (Agent-Based)
- **Option B chosen**: Agent-based similarity comparison (LLM reads files and compares)
- No embedding model or vector storage required initially
- Can evolve to embedding-based later if needed

### Memory Catalog Strategy
- **Option B chosen**: Remove MEMORIES.md catalog entirely
- Folder structure provides sufficient indexing
- Human can browse directories directly for overview

### Similarity Threshold (Linked Memories)
- **Option C chosen**: Related memories reference each other (links)
- Must avoid circular dependency problems
- Example: "Authentication uses JWT tokens" ←→→ "Session management: Redis stores JWT with 30min expiry"

### Orchestration Integration (CRITICAL CORRECTION)
- **Automatic Recall**: After orchestrator parses human prompt, it MUST automatically recall related memories and pass to next agent
- **Manual Remember/Forget**: Triggered by user prompt explicitly
- No separate "compound" step in orchestration - memory recall IS the compound step

### Template Content
**Memory Template** (`templates/memory/*.md`):
- **Required metadata**: created at, last modified at
- **Required sections**: Overview, Examples, Related
- **Flexible sections**: Other sections based on memory type

**Response Template** (`templates/response/*.md`):
- Fixed checkmark format for standardization
- Ensures consistency across models

### Error Handling
- Same name exists → Ask user how to proceed
- Folder doesn't exist → Auto-fix (create folders, confirm with user)
- User rejects similarity → Ask user how to proceed
- No memories found → Acceptable, proceed to next step

## Technical Approach

### Memory Types (10 categories)
1. architectural decision → `.opencode/memory/decision/architectural/*.md`
2. design decision → `.opencode/memory/decision/design/*.md`
3. unclassified decision → `.opencode/memory/decision/*.md`
4. learning → `.opencode/memory/learning/*.md`
5. user preference → `.opencode/memory/preference/user/*.md`
6. project preference → `.opencode/memory/preference/project/*.md`
7. blocker → `.opencode/memory/blocker/*.md`
8. issue → `.opencode/memory/blocker/issue/*.md`
9. context → `.opencode/memory/context/*.md`
10. recurring pattern → `.opencode/memory/pattern/recurring/*.md`
11. conventions pattern → `.opencode/memory/pattern/conventions/*.md`
12. unclassified pattern → `.opencode/memory/pattern/*.md`

### Tool Surface (3 main operations)
1. **memory_remember**: Classify → check similar → create/update → report
2. **memory_recall**: Scan catalog → find related → report (READ ONLY)
3. **memory_forget**: Scan → find matches → delete → report

### Research Techniques (auto-discovery)
- File-based: README.md, package.json, config files, CI/CD
- Git-based: git log, git branch, commit conventions
- Explore agent: Parallel queries for project understanding

## Output Format Standards

### Recall Response
```
📋 Memories Recall
==============================

Recalled:
  ✓ [Memory Title]
    → "./opencode/memory/[type]/[file].md"
  ✓ [Another Memory]
    → "./opencode/memory/[type]/[file].md"

✅ Complete - X.Xs elapsed
```

### Remember Response
```
📋 Memories Remember
==============================

Changes:
  ✓ Updated: [Memory Title]
    → "./opencode/memory/[type]/[file].md"
  ✓ Added: [Memory Title]
    → "./opencode/memory/[type]/[file].md"

✅ Complete - X.Xs elapsed
```

### Forget Response
```
📋 Memories Forgot
==============================

Changes:
  ✓ Updated: [Memory Title]
    → "./opencode/memory/[type]/[file].md"
  ✓ Removed: [Memory Title]
    → "./opencode/memory/[type]/[file].md"

✅ Complete - X.Xs elapsed
```

## Folder Structure
```
skills/mnemonics/
├── SKILL.md
├── scripts/
│   ├── memory-remember.py
│   ├── memory-recall.py
│   └── memory-delete.py
└── templates/
    ├── response/
    │   ├── recall-template.md
    │   ├── remember-template.md
    │   └── forget-template.md
    └── memory/
        ├── memory-template.md
```

## Open Questions

1. Should skill be registered in opencode.jsonc for automatic loading?
2. How should skill handle memory file naming (auto-generate vs user-specified)?
3. Should "related memories" include bidirectional references?
