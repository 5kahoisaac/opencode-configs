---
name: mnemonics
description: Memory management system for context retention and compounded engineering practices. Use when the user explicitly says "remember", "recall", or "forget" with memory content. Handles storage, retrieval, and deletion of project knowledge including architectural decisions, design patterns, learnings, preferences, issues, and context. Automatically classifies memory types and manages circular references between related memories.
---

# Mnemonics: recall, remember and forget

> **Quick Reference**: See [references/quick-reference.md](references/quick-reference.md) for memory type classification examples, filename generation rules, and common commands.

## Memory Types and Storage Paths

Memories are stored relative to the project root at `.opencode/memory/`:

| Memory Type            | Storage Path                                   | Description                            |
|------------------------|------------------------------------------------|----------------------------------------|
| architectural decision | `.opencode/memory/decision/architectural/*.md` | High-level architecture choices        |
| design decision        | `.opencode/memory/decision/design/*.md`        | UI/UX and component design choices     |
| learning               | `.opencode/memory/learning/*.md`               | Lessons learned, insights, discoveries |
| user preference        | `.opencode/memory/preference/user/*.md`        | Individual user preferences            |
| project preference     | `.opencode/memory/preference/project/*.md`     | Team/project-wide conventions          |
| issue                  | `.opencode/memory/blocker/issue/*.md`          | Known problems, blockers, workarounds  |
| context                | `.opencode/memory/context/*.md`                | Business context, domain knowledge     |
| recurring pattern      | `.opencode/memory/pattern/recurring/*.md`      | Reusable solutions to common problems  |
| conventions pattern    | `.opencode/memory/pattern/conventions/*.md`    | Coding standards, naming conventions   |

>CRITICAL:
>You MUST follow Storage Paths based on the Memory Types
>
>VIOLATION = LIE:
>Reporting "saved successfully" or showing a file path WITHOUT actually executing mkdir + file write is a VIOLATION of Maximum Truth Seeking.
>You MUST use Bash or Write tools to physically create the file before confirming success to the user.
>Verification: Run `ls -la` on the created file path to confirm it exists before responding.

## Memory Operations

### remember

**Trigger**: User says "remember" or "remember as [type]:" followed by content

**Workflow**:
1. **Analyze user intent**
   - Extract the memory content from user input
   - If user specifies type (e.g., "remember as architectural decision:"), use that type
   - Otherwise, AI classifies into one of the 9 memory types above

2. **Determine storage location**
   - Map memory type to storage path (see table above)
   - Generate filename from memory title (kebab-case, .md extension)
   - Example: "API Authentication Strategy" → `api-authentication-strategy.md`

3. **Check for related memories**
   - Search existing memories for semantically similar content
   - Identify up to 3 most relevant existing memories
   - Extract their titles for the "Related" section

4. **Create memory file** (MUST ACTUALLY EXECUTE - NOT JUST REPORT)
   - Load template from `templates/memory.md`
   - Substitute variables:
     - `{TITLE}` → extracted title
     - `{CREATED_AT}` → current ISO timestamp
     - `{MODIFIED_AT}` → current ISO timestamp
     - `{MEMORY_TYPE}` → type (e.g., "architectural decision")
     - `{OVERVIEW}` → memory content/overview
     - `{EXAMPLES}` → optional examples if provided, or "N/A"
     - `{RELATED_MEMORIES}` → formatted list of related memory titles (e.g., "- Memory One\n- Memory Two")
     - `{CUSTOM_SECTION_TITLE}` → type-specific section title (e.g., "Technical Details" for architectural decisions)
     - `{CUSTOM_SECTION_CONTENT}` → type-specific content
   - **EXECUTE** using Bash tool:
     ```bash
     mkdir -p .opencode/memory/FOLDER_PATH
     cat > .opencode/memory/FOLDER_PATH/filename.md << 'EOF'
     {substituted_memory_content}
     EOF
     ```
   - **VERIFY** file exists:
     ```bash
     ls -la .opencode/memory/FOLDER_PATH/filename.md
     ```
   - **ONLY AFTER VERIFICATION**: Confirm success to user with actual path

5. **Update related memories** (if applicable) - MUST VERIFY BACKLINKS
   - For each related memory found, add backlink to this new memory
   - **EXECUTE** using Bash tool to insert within "Related Memories" section (after the header):
     ```bash
     sed -i '' '/^## Related Memories$/a\
- {NEW_MEMORY_TITLE}' .opencode/memory/path/to/related-memory.md
     ```
   - **VERIFY** backlink was added in correct section:
     ```bash
     grep -A 5 "^## Related Memories$" .opencode/memory/path/to/related-memory.md | grep "{NEW_MEMORY_TITLE}"
     ```
   - **ONLY AFTER VERIFICATION**: Continue to next related memory

6. **Render response**
   - Load `templates/remember.response.md`
   - Substitute variables with plain text values
   - Display confirmation to user

### recall

**Trigger**: User asks to "recall" or "find" memories, or asks about stored knowledge

**Workflow**:
1. **Analyze user intent**
   - Determine what memories the user is looking for
   - Identify relevant memory types based on query context

2. **Search memories**
   - If type is specified, search only that type's directory
   - Otherwise, search all `.opencode/memory/` subdirectories
   - List all `.md` files in target directories

3. **AI-driven relevance scoring**
   - Read each candidate memory file
   - Compare content semantic similarity to user query
   - Score relevance (0-100)
   - Sort by relevance, keep top results

4. **Prevent circular reference loops**
   - Track visited memory titles during processing
   - When rendering related memories, skip if already displayed
   - Maximum depth: 1 level of related memories

5. **Render response**
   - Load `templates/recall.response.md`
   - For each found memory:
     - Extract title, type, timestamps, content
     - Format related memories list
   - Substitute array items by generating list text
   - Display results to user

### forget

**Trigger**: User says "forget" followed by memory identifier or description

**Workflow**:
1. **Identify target memory**
   - Parse user input to identify which memory to forget (title, path, or description)
   - Search for matching memory file

2. **Check for dependencies**
   - Extract memory filename
   - Search all other memory files for references in their "Related" section
   - Use grep to find filename mentions
   - If found in other memories, collect list of dependent memories

3. **Handle dependencies** - MUST VERIFY ALL BACKLINKS REMOVED
   - If dependencies exist:
     - Show warning with list of memories that reference this one
     - Option to force delete (remove backlinks first) or cancel
   - If force deleting:
     - For each dependent memory, **EXECUTE** using Bash tool to remove backlink:
       ```bash
       sed -i '' '/^- {MEMORY_TITLE_TO_DELETE}$/d' .opencode/memory/path/to/dependent-memory.md
       ```
     - **VERIFY** all backlinks removed:
       ```bash
       grep -r "{MEMORY_TITLE_TO_DELETE}" .opencode/memory/ --include="*.md" || echo "All backlinks removed successfully"
       ```
     - **ONLY AFTER VERIFICATION**: Proceed to step 4

4. **Delete memory file** (MUST ACTUALLY EXECUTE - NOT JUST REPORT)
   - **EXECUTE** using Bash tool:
     ```bash
     rm .opencode/memory/path/to/memory-file.md
     ```
   - **VERIFY** file is deleted:
     ```bash
     ls -la .opencode/memory/path/to/ 2>&1 | grep memory-file.md || echo "File deleted successfully"
     ```
   - **ONLY AFTER VERIFICATION**: Confirm deletion to user

5. **Render response**
   - Load `templates/forget.response.md`
   - Substitute variables with deletion details
   - Display confirmation to user

## Template Variable Substitution

All templates use plain text substitution (no template engines like Handlebars):

- Replace exact placeholder strings (e.g., `{TITLE}`) with actual values
- For arrays (like related memories): generate formatted markdown list before substitution

**Example transformation:**
```
Template: Related Memories: {RELATED_MEMORIES}
Values: ["Database Schema", "Security Best Practices"]
Result: Related Memories: - Database Schema
                           - Security Best Practices
```

**Substitution map for remember.response.md:**
- `{TITLE}` → memory title
- `{TYPE}` → memory type
- `{TOPIC}` → topic/category
- `{CREATED_AT}` → timestamp
- `{PATH}` → file path
- `{CONTENT}` → memory overview content (truncated if needed)
- `{RELATED_MEMORIES_LIST}` → formatted bullet list or "None"

**Substitution map for recall.response.md:**
- `{MEMORIES_LIST}` → formatted list of all found memories with details
- `{COUNT}` → number of memories found

**Substitution map for forget.response.md:**
- `{TITLE}` → memory title
- `{MEMORY_TYPE}` → type of deleted memory
- `{STATUS}` → "deleted" or "blocked (has dependencies)"
- `{PATH}` → file path
- `{DETAILS}` → deletion details or dependency warnings

## Example Memory Output

A created memory file (`.opencode/memory/decision/architectural/api-authentication-strategy.md`):

```markdown
# API Authentication Strategy

- created at: 2024-01-15T10:30:00Z
- last modified at: 2024-01-15T10:30:00Z
- memory type: architectural decision

## Overview

We decided to use JWT tokens with refresh token rotation for API authentication. 
Access tokens expire in 15 minutes, refresh tokens expire in 7 days.

## Examples

N/A

## Technical Details

- Algorithm: RS256
- Token storage: HttpOnly cookies
- Rotation: Single-use refresh tokens

## Related Memories

- Database Schema Design
- Security Best Practices
```

## Implementation Notes

### File Operations
- Use `mkdir -p` to create directory structure before writing files
- Read templates using file read tools
- Write memory files using file write tools
- Use `glob` to list memory files for searching

### Semantic Search for Recall
When scoring relevance:
- Extract keywords from user query
- Check for keyword matches in memory title and overview
- Consider recency (newer memories may be more relevant)
- Consider memory type alignment with query context

### Dependency Check for Forget
```bash
# Example grep command to find references
grep -r "memory-filename" .opencode/memory/ --include="*.md"
```

If results found in other memory files, those memories depend on this one.

## Circular Reference Handling

When processing related memories:
- Maintain a "visited" set of memory titles
- Before including a related memory, check if already visited
- Skip if visited to prevent infinite loops
- Maximum related memories to display: 5 per memory