---
description: Create oh-my-opencode-slim agent append files with mnemonics memory integration
argument-hint: courier
---

# Create Oh-My-Opencode-Slim Agent Append Files

This command creates `{agent}_append.md` files for oh-my-opencode-slim agents, adding mnemonics skill instructions for compounded engineering. These append files extend the default agent prompts without replacing them.

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
```

**For Explorer:**
```markdown
## Memory Integration (Mnemonics)

Before exploring the codebase, use the mnemonics skill to recall:

- **recall "conventions pattern"**: Understand file naming conventions, directory structures, and coding standards
- **recall "architectural decision"**: Know the high-level architecture to navigate efficiently
- **recall "project preference"**: Be aware of team conventions for file organization
- **recall "recurring pattern"**: Recognize common code patterns used in the project

Leverage stored knowledge to search more effectively and understand the codebase context faster.
```

**For Oracle:**
```markdown
## Memory Integration (Mnemonics)

Before providing strategic advice, use the mnemonics skill to recall:

- **recall "architectural decision"**: Review past architecture choices and their rationale
- **recall "design decision"**: Understand UI/UX decisions and component design patterns
- **recall "learning"**: Access lessons learned from previous debugging sessions
- **recall "issue"**: Check for known problems, blockers, and workarounds
- **recall "context"**: Access business context for informed recommendations

Base your strategic guidance on accumulated project knowledge to avoid repeating past mistakes.
```

**For Librarian:**
```markdown
## Memory Integration (Mnemonics)

When researching libraries and external documentation, use the mnemonics skill to:

- **recall "learning"**: Check for previously documented library usage patterns
- **recall "recurring pattern"**: See if similar integration patterns were used before
- **recall "architectural decision"**: Understand how external libraries fit into the architecture

Store new findings as "learning" memories for future reference.
```

**For Designer:**
```markdown
## Memory Integration (Mnemonics)

Before creating UI/UX, use the mnemonics skill to recall:

- **recall "design decision"**: Review existing UI/UX decisions and design patterns
- **recall "project preference"**: Understand team preferences for visual style
- **recall "conventions pattern"**: Follow established styling and component conventions

Maintain visual consistency by building upon documented design decisions.
```

**For Fixer:**
```markdown
## Memory Integration (Mnemonics)

Before implementing changes, use the mnemonics skill to recall:

- **recall "issue"**: Check for known blockers or workarounds that might affect implementation
- **recall "conventions pattern"**: Follow established coding standards and patterns
- **recall "architectural decision"**: Respect high-level architecture constraints
- **recall "learning"**: Apply lessons learned from similar past implementations

Ensure implementations align with project conventions and avoid known issues.
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

Each file contains only the mnemonics memory integration instructions to be appended to the default agent prompts.

## Installation

To apply these append files to your oh-my-opencode-slim setup:

```bash
# Copy to the oh-my-opencode-slim config directory
cp ./oh-my-opencode-slim/*_append.md ~/.config/opencode/oh-my-opencode-slim/
```

The `_append.md` files will be automatically loaded and appended to the default agent prompts.

## Error Handling

- If the output directory cannot be created, report the error and stop
- If an invalid agent name is provided, show the valid options and stop
- If a file already exists, overwrite it with the new content
