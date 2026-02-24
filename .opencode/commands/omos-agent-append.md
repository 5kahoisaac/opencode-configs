---
description: Create oh-my-opencode-slim agent append files with historian plugin integration via `@historian` subagent or the **mnemonics** skill
---

# Create Oh-My-Opencode-Slim Agent Append Files

This command creates `{agent}_append.md` files for oh-my-opencode-slim agents, adding historian plugin and mnemonics skill instructions for compounded engineering. These append files extend the default agent prompts without replacing them.

## Access Methods

There are two ways to use the historian plugin:

1. **Load the mnemonics skill**: Use `skill(name: "mnemonics")` to load detailed guidance
2. **Invoke @historian directly**: Use `@historian` subagent for direct memory operations

**Available memory commands** (via @historian):
- `memory_recall <query>` — Search memories by keyword/semantic query (e.g., `memory_recall "authentication flow"`)
- `memory_remember <content>` — Create new memories or update existing ones
- `memory_forget <query>` — Delete memories matching the query
- `memory_list_types` — List available memory types in the project
- `memory_sync` — Reindex after manual file changes

**Memory types** (kebab-case): architectural-decision, design-decision, learning, issue, conventions-pattern, recurring-pattern, project-preference, context

Projects may define custom memory types (e.g., `government-policy`, `security-requirement`, `compliance-rule`). These provide domain-specific context that should be considered by relevant agents.

## Arguments

- **agent-name** (optional): Specific agent to create append file for (orchestrator, explorer, oracle, librarian, designer, fixer). If omitted, all agents will be processed.

## Workflow

### Step 1: Determine Target Agents

If `<agent-name>` is provided:
- Validate it is one of: orchestrator, explorer, oracle, librarian, designer, fixer
- Process only that agent

If no argument provided:
- Process all six agents: orchestrator, explorer, oracle, librarian, designer, fixer

### Step 2: Create Output Directory

Create the directory `./oh-my-opencode-slim/` if it doesn't exist.

### Step 3: Generate Mnemonics Append Content

For each target agent, create agent-specific mnemonics instructions:

**For Orchestrator:**
```markdown
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
```

**For Explorer:**
```markdown
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
```

**For Oracle:**
```markdown
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
```

**For Librarian:**
```markdown
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
```

**For Designer:**
```markdown
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
```

**For Fixer:**
```markdown
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
```

### Step 4: Write Append Files

For each agent, write the mnemonics section to:
`./oh-my-opencode-slim/{agent}_append.md`

### Step 5: Report Results

Provide a summary:
- List all agents that were successfully processed
- Show the output directory path
- Explain how to use: Copy files to `~/.config/opencode/oh-my-opencode-slim/`
- Note that `{agent}_append.md` extends the default prompt (unlike `{agent}.md` which replaces it)

## Example Output Files

After running this command, you will have files like:
```
./oh-my-opencode-slim/
  ├── orchestrator_append.md
  ├── explorer_append.md
  ├── oracle_append.md
  ├── librarian_append.md
  ├── designer_append.md
  └── fixer_append.md
```

Each file contains historian plugin integration instructions including memory commands, recall patterns, and documentation guidelines to be appended to the default agent prompts.

## Memory Types Quick Reference

### Standard Memory Types

| Memory Type              | Use Case                                                     | Example Content                                                  |
|--------------------------|--------------------------------------------------------------|------------------------------------------------------------------|
| `architectural-decision` | High-level architecture, design patterns, tech stack choices | "We use hexagonal architecture with ports/adapters pattern"      |
| `design-decision`        | UI/UX choices, component patterns, visual standards          | "Modal dialogs should use the Dialog component from @radix-ui"   |
| `learning`               | Lessons learned, library usage patterns, debugging insights  | "Zod validation should use `.strict()` for API inputs"           |
| `issue`                  | Known bugs, blockers, workarounds                            | "Avoid using React.useLayoutEffect in SSR components"            |
| `conventions-pattern`    | Coding standards, naming conventions, file organization      | "API routes use kebab-case: `/api/user-profile.ts`"              |
| `recurring-pattern`      | Common implementation patterns, repeated solutions           | "Error handling pattern: log → notify user → degrade gracefully" |
| `project-preference`     | Team-wide preferences, style choices                         | "Prefer early returns over nested conditionals"                  |
| `context`                | Business context, domain knowledge, requirements             | "User authentication must support OAuth2 providers"              |

### Custom Memory Types

Projects can define custom memory types in kebab-case for domain-specific context:

| Example Custom Type         | Use Case                              |
|-----------------------------|---------------------------------------|
| `government-policy`         | Regulatory compliance requirements    |
| `security-requirement`      | Security standards and constraints    |
| `compliance-rule`           | Industry-specific compliance rules    |
| `accessibility-requirement` | Accessibility standards (WCAG, etc.)  |
| `performance-sla`           | Performance guarantees and thresholds |

Custom memory types are discovered via `memory_list_types` and should be considered by all agents when relevant to their tasks.

## Error Handling

- If the output directory cannot be created, report the error and stop
- If an invalid agent name is provided, show the valid options and stop
- If a file already exists, overwrite it with the new content
