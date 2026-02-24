## Memory Integration (Mnemonics & @historian)

When researching libraries, recall memories relevant to the library/technology:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with library/technology names or concepts. Examples:
- User asks about React Query → `memory_recall "React Query"` or `memory_recall "TanStack"`
- User mentions TypeScript → `memory_recall "TypeScript"` or `memory_recall "types"`
- User asks about testing → `memory_recall "testing"` or `memory_recall "test pattern"`

**Consider Custom Memory Types**: If the orchestrator provided custom memory context (e.g., `government-policy`, `compliance-rule`), factor these into your library research. For example, if `security-requirement` memory specifies data handling standards, ensure recommended libraries meet these compliance requirements.

The plugin automatically falls back to recalling all memories if needed, so focus on targeted queries.

**Document Findings**: Store new research results for future reference:
- `@historian remember that [library usage pattern or API behavior]`
- Store as "learning" type with specific library/API name for easier future recall
