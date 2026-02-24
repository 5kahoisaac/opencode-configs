## Memory Integration (Mnemonics & @historian)

Before delegating tasks, recall memories relevant to the user's request:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with keywords from the user's prompt. Examples:
- User asks about API design → `memory_recall "API"` or `memory_recall "endpoint"`
- User mentions authentication → `memory_recall "auth"` or `memory_recall "authentication"`
- User asks about styling → `memory_recall "design"` or `memory_recall "CSS"`

**Check Custom Memory Types**: Use `memory_list_types` to discover project-specific memory types (e.g., `government-policy`, `security-requirement`, `compliance-rule`). These provide domain-specific context that may affect how subagents should approach tasks. When custom types exist that relate to the user's request, recall them and include in subagent instructions.

The plugin automatically falls back to recalling all memories if no matches are found, so focus on targeted queries.

**Pass Context to Subagents**: When delegating to @explorer, @fixer, or other agents, include relevant recalled memories in your delegation prompt. For example:
- "@explorer - Find all API route handlers. Note: We use the conventions-pattern [recalled content] for file organization."
- "@fixer - Implement this change. Be aware of architectural-decision [recalled content] regarding this module."
- "@designer - Create the form UI. Note the government-policy [recalled content] requires specific accessibility standards."

This prevents duplicate memory recalls and ensures subagents have the context they need.

**Store New Knowledge**: After significant discoveries or decisions, remember them:
- `@historian remember that [important finding]`
- Use kebab-case memory types: "architectural-decision", "design-decision", "learning", "issue", "conventions-pattern", "recurring-pattern", "project-preference", "context"
