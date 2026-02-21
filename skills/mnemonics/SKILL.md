---
name: mnemonics
description: Memory management by using the historian subagent to store, recall, and manage persistent memories across conversations. Use when you need to remember decisions, preferences, learnings, or retrieve stored context.
license: MIT
compatibility: opencode, opencode-historian plugin and qmd CLI.
metadata:
    author: Isaac Ng, Ka Ho
    version: "1.0.0"
---

# Mnemonics: Memory Management via Historian

## CRITICAL: You Must Use @historian

Memory tools are **ONLY available via the @historian subagent**. You CANNOT call these tools directly:

- `memory_remember` - Create or update memories
- `memory_recall` - Search and retrieve memories
- `memory_forget` - Delete memories
- `memory_list_types` - List available memory types
- `memory_sync` - Rebuild the search index

**Always delegate to historian:**

```
@historian remember that we decided on PostgreSQL for the database
@historian what did we decide about authentication?
```

## Memory Types

| Type                     | Use For                     | Example                                              |
|--------------------------|-----------------------------|------------------------------------------------------|
| `architectural-decision` | System architecture choices | "Using PostgreSQL with read replicas for scaling"    |
| `design-decision`        | UI/UX decisions             | "Card layout for dashboard, 3 columns on desktop"    |
| `learning`               | Lessons and discoveries     | "Bun's native TS support removes build step need"    |
| `user-preference`        | User preferences            | "User prefers dark mode, tabs not spaces"            |
| `project-preference`     | Team conventions            | "We use conventional commits, PR reviews required"   |
| `issue`                  | Known problems              | "Rate limiting not implemented yet, tracking in #42" |
| `context`                | General context (default)   | "Project started Feb 2026, MVP target Q2"            |
| `recurring-pattern`      | Reusable patterns           | "Error handling: wrap in try/catch, return {error}"  |
| `conventions-pattern`    | Coding standards            | "Use named exports, avoid default exports"           |

> **Note:** Projects may define custom memory types via configuration. Always use `@historian list all memory types available` to see the complete list for the current project.

## When to Delegate to Historian

**Remember (create/update):**
- After making a significant architectural or design decision
- User states a preference about how they work
- Discovering something important about the codebase or tools
- Learning a lesson that should persist across sessions

**Recall (search/retrieve):**
- Starting a new session → recall relevant context
- User asks "what did we decide about X?"
- Need to check if a decision was already made
- Looking for known issues or patterns

**Forget (delete):**
- User wants to remove outdated or incorrect memories
- Cleaning up duplicated or irrelevant entries

**Sync (reindex):**
- After manually editing memory files in `.mnemonics/`
- When search results seem outdated

## Example Prompts

### Remembering

```
@historian remember that we decided on JWT auth with 15-min expiry
@historian save this learning: Bun handles TypeScript natively without compilation
@historian note that the user prefers minimal UI animations
@historian store this as an architectural-decision: we're using event sourcing for the audit log
```

### Recalling

```
@historian what did we decide about authentication?
@historian recall any known issues with the API
@historian what are my preferences for this project?
@historian show all architectural decisions
@historian find memories about database choices
```

### Managing

```
@historian list all memory types available
@historian forget the memory about the old API design
@historian sync the index to include recent memory files
```

## How It Works

1. **Memories are stored** in `.mnemonics/{type}/{title}.md` as markdown files with YAML frontmatter
2. **Indexing is automatic** via qmd (hybrid BM25 + vector search)
3. **Historian handles** classification, deduplication, and semantic search
4. **Files are git-friendly** - commit them to share across team

## Best Practices

1. **Be specific in titles** - "qmd-cli-for-writes" not "important decision"
2. **Let historian classify** - it will search first to avoid duplicates
3. **Recall before deciding** - check if a decision already exists
4. **Commit memory files** - they're part of project knowledge
