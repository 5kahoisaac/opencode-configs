## Memory Integration (Mnemonics)

Before delegating tasks, use the mnemonics skill to recall relevant project knowledge:

- **recall "architectural decision"**: Understand high-level architecture and design patterns
- **recall "conventions pattern"**: Follow established coding standards and naming conventions
- **recall "project preference"**: Respect team-wide conventions and preferences
- **recall "context"**: Access business context and domain knowledge

**Pass Context to Subagents**: When delegating to @explorer, @fixer, or other agents, include relevant recalled memories in your delegation prompt. For example:
- "@explorer - Find all API route handlers. Note: We use the conventions pattern [recalled content] for file organization."
- "@fixer - Implement this change. Be aware of architectural decision [recalled content] regarding this module."

This prevents duplicate memory recalls and ensures subagents have the context they need.
