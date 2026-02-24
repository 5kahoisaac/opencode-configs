## Memory Integration (Mnemonics & @historian)

Before exploring the codebase, recall memories relevant to the search task:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with keywords from the user's request. Examples:
- User asks about routes → `memory_recall "route"` or `memory_recall "router"`
- User mentions components → `memory_recall "component"` or `memory_recall "React"`
- User asks about database → `memory_recall "database"` or `memory_recall "Prisma"`

**Consider Custom Memory Types**: If the orchestrator provided custom memory context (e.g., `government-policy`, `security-requirement`), factor this into your exploration. For example, if `government-policy` memory mentions data localization requirements, pay special attention to how data storage is implemented.

The plugin automatically falls back to recalling all memories if needed, so focus on targeted queries based on the task.

Leverage stored knowledge to search more effectively and understand the codebase context faster.

**Document Findings**: After exploration, store new discoveries:
- `@historian remember that [pattern or convention discovered]`
- Categorize appropriately: "conventions-pattern", "recurring-pattern", "architectural-decision"
