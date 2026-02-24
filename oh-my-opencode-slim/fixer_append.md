## Memory Integration (Mnemonics & @historian)

Before implementing changes, recall memories relevant to the fix/task:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with keywords from the bug/feature description. Examples:
- User reports auth bug → `memory_recall "auth"` or `memory_recall "login"`
- User mentions performance issue → `memory_recall "performance"` or `memory_recall "slow"`
- User asks about error handling → `memory_recall "error"` or `memory_recall "exception"`

**Consider Custom Memory Types**: If the orchestrator provided custom memory context (e.g., `government-policy`, `security-requirement`), ensure your implementation adheres to these constraints. For example, if `compliance-rule` memory requires audit logging for all data changes, implement appropriate logging mechanisms.

The plugin automatically falls back to recalling all memories if needed, so focus on targeted queries.

Ensure implementations align with project conventions and avoid known issues.

**Document Solutions**: After fixing issues, store lessons learned:
- `@historian remember that [solution or workaround found]`
- Store critical fixes as "issue" type with workaround details, or as "learning" for general knowledge
