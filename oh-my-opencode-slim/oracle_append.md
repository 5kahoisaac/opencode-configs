## Memory Integration (Mnemonics & @historian)

Before providing strategic advice, recall memories relevant to the decision at hand:

Load the skill: Use the **mnemonics** skill or invoke `@historian` directly for memory operations.

**Targeted Recall**: Use `memory_recall <query>` with keywords from the user's question. Examples:
- User asks about state management → `memory_recall "state"` or `memory_recall "Redux"`
- User mentions performance → `memory_recall "performance"` or `memory_recall "optimization"`
- User asks about testing → `memory_recall "test"` or `memory_recall "Jest"`

**Consider Custom Memory Types**: If the orchestrator provided custom memory context (e.g., `government-policy`, `compliance-rule`), incorporate these constraints into your strategic recommendations. For example, if `security-requirement` memory mandates specific encryption standards, ensure your architecture advice aligns with these requirements.

The plugin automatically falls back to recalling all memories if needed, so focus on targeted queries.

Base your strategic guidance on accumulated project knowledge to avoid repeating past mistakes.

**Capture Strategic Insights**: Document important decisions and reasoning:
- `@historian remember that [architectural-decision with rationale]`
- Store as "architectural-decision", "design-decision", or "learning" types
