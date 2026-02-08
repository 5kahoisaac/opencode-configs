# Mnemonics Memory System

- created at: 2026-02-08T12:00:00Z
- last modified at: 2026-02-08T12:00:00Z
- memory type: project preference

## Overview

Complete Mnemonics system specification for OpenCode config project. Defines 9 memory types with storage paths, remember/recall/forget workflows, template substitution rules, and dependency handling. CRITICAL: Must follow exact storage paths from memory type table.

## Examples

```
remember as architectural decision: Use JWT with refresh token rotation
→ .opencode/memory/decision/architectural/jwt-authentication-strategy.md
```

## Related Memories

None

## Conventions

- Storage: `.opencode/memory/{category}/{type}/*.md`
- Filename: kebab-case from title + .md
- Templates: Load from `templates/memory.md`, substitute {TITLE}, {CREATED_AT}, etc.
- Operations: remember → classify+write, recall → semantic search, forget → dependency check+delete

