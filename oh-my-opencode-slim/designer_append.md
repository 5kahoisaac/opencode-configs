## Memory Integration (Mnemonics & @historian)

Before creating UI/UX, recall memories relevant to the design task:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with design-related keywords. Examples:
- User asks about forms → `memory_recall "form"` or `memory_recall "input"`
- User mentions colors → `memory_recall "color"` or `memory_recall "theme"`
- User asks about responsive design → `memory_recall "responsive"` or `memory_recall "mobile"`

**Consider Custom Memory Types**: If the orchestrator provided custom memory context (e.g., `government-policy`, `accessibility-requirement`), incorporate these constraints into your designs. For example, if `government-policy` memory specifies WCAG 2.1 AA compliance requirements, ensure your designs meet these accessibility standards.

The plugin automatically falls back to recalling all memories if needed, so focus on targeted queries.

Maintain visual consistency by building upon documented design decisions.

**Document Design Decisions**: Store new design choices:
- `@historian remember that [design-decision with rationale]`
- Use "design-decision" type for UI/UX choices, "conventions-pattern" for reusable patterns
