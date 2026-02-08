# Mnemonics Quick Reference

## Memory Types Quick Lookup

| Type                   | Path                                       | Use When                                         |
|------------------------|--------------------------------------------|--------------------------------------------------|
| architectural decision | `.opencode/memory/decision/architectural/` | System design choices, tech stack selection      |
| design decision        | `.opencode/memory/decision/design/`        | UI patterns, component structure, UX choices     |
| learning               | `.opencode/memory/learning/`               | Lessons learned, debugging insights, discoveries |
| user preference        | `.opencode/memory/preference/user/`        | Personal coding style, individual preferences    |
| project preference     | `.opencode/memory/preference/project/`     | Team conventions, agreed standards               |
| issue                  | `.opencode/memory/blocker/issue/`          | Known bugs, workarounds, limitations             |
| context                | `.opencode/memory/context/`                | Business logic, domain knowledge, requirements   |
| recurring pattern      | `.opencode/memory/pattern/recurring/`      | Reusable solutions, common implementations       |
| conventions pattern    | `.opencode/memory/pattern/conventions/`    | Naming standards, file organization              |

## Filename Generation

Convert title to kebab-case:
- "API Authentication Strategy" → `api-authentication-strategy.md`
- "Database Schema Design" → `database-schema-design.md`
- "User Preferences for UI" → `user-preferences-for-ui.md`

Rules:
- Lowercase everything
- Replace spaces with hyphens
- Remove special characters except hyphens
- Add `.md` extension

## User Intent Classification Examples

**→ architectural decision**
- "We should use PostgreSQL instead of MongoDB"
- "Let's go with a microservices architecture"
- "I think we need a message queue for this"

**→ design decision**
- "The modal should slide in from the right"
- "Let's use a card-based layout"
- "The color scheme should be dark mode by default"

**→ learning**
- "I found that the issue was caused by..."
- "Turns out React hooks behave differently when..."
- "The solution was to use Promise.all instead of..."

**→ user preference**
- "I prefer 2-space indentation"
- "I like to use single quotes for strings"
- "My preferred import order is..."

**→ project preference**
- "Our team uses conventional commits"
- "We agreed to use TypeScript strict mode"
- "The project uses kebab-case for filenames"

**→ issue**
- "There's a bug in the auth flow that..."
- "The API sometimes returns 500 when..."
- "We need to work around the library limitation..."

**→ context**
- "The business requires audit logging for..."
- "In this domain, customers are called 'subscribers'"
- "The compliance requirement states that..."

**→ recurring pattern**
- "We keep needing to handle form validation like..."
- "The pattern for API error handling is..."
- "For every component, we should..."

**→ conventions pattern**
- "Files should be named in kebab-case"
- "Components go in the components folder"
- "Environment variables should be prefixed with..."

## Common Commands

**List all memories:**
```bash
find .opencode/memory -name "*.md" -type f
```

**Search memories by content:**
```bash
grep -r "search term" .opencode/memory/ --include="*.md"
```

**Check dependencies before forget:**
```bash
# Replace <filename> with the memory filename (without .md)
grep -r "<filename>" .opencode/memory/ --include="*.md" | grep -v "^Binary"
```

## Response Template Variables

### remember.response.md
- `{TITLE}` - Memory title
- `{TYPE}` - Memory type classification
- `{TOPIC}` - Topic/category
- `{CREATED_AT}` - ISO timestamp
- `{PATH}` - Full storage path
- `{CONTENT}` - Overview content (truncated to ~500 chars if long)
- `{RELATED_MEMORIES_LIST}` - Bullet list or "None"

### recall.response.md
- `{MEMORIES_LIST}` - Full formatted list of memories
- `{COUNT}` - Number of memories found

### forget.response.md
- `{TITLE}` - Memory title
- `{MEMORY_TYPE}` - Type of memory
- `{STATUS}` - "deleted" or "blocked (has dependencies)"
- `{PATH}` - File path
- `{DETAILS}` - Additional info

## Memory Template Sections

Standard sections in memory.md:
1. Title (H1)
2. Metadata (created at, modified at, memory type)
3. Overview - Main content
4. Examples - Code samples, usage examples
5. Custom Section - Type-specific details (e.g., "Technical Details")
6. Related Memories - Linked references (ALWAYS LAST)
