---
description: Synchronizes README.md with configuration files
agent: sisyphus
model: opencode/big-pickle
---

# OpenCode Command: README Synchronizer

This command ensures that `README.md` documentation remains perpetually synchronized with actual project configuration. As your OpenCode setup evolves—with new plugins, MCPs, providers, skills, agents, and model configurations—this command automatically detects changes and updates corresponding documentation sections to maintain accuracy and prevent documentation drift.

## Command Execution Strategy

You must execute this command with a strategic approach, carefully analyzing the current state before making modifications. Follow these phases:

### Phase 1: Command Location Detection

1. Check if running from within a git repository: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Determine default location:
   - Inside git repo → Project-level: `.opencode/commands/`
   - Not in git repo → Global: `~/.config/opencode/commands/`
3. Report the chosen location to the user before proceeding
4. Create directory if it doesn't exist: `mkdir -p [directory-path]`

### Phase 2: Configuration Analysis and Change Detection

You must analyze the project structure to identify what needs synchronization:

**Primary Configuration Files to Monitor:**
- `*.jsonc` files in project root
  - Specifically: `opencode.jsonc`, `oh-my-opencode.jsonc`, `supermemory.jsonc`
  - Any additional JSONC files

**Component Directories to Scan:**
- `agents/` directory for custom agent configurations
- `skills/` directory for skill definitions
- `commands/` directory for custom command files

**For `opencode.jsonc` Changes:**

Use the **Task tool** to orchestrate parallel scanning and analysis:

1. Launch parallel exploration tasks to analyze configuration structure:
   - Task: Scan `opencode.jsonc` plugins section and detect changes
   - Task: Scan `opencode.jsonc` MCPs section and detect changes
   - Task: Scan `opencode.jsonc` providers section and detect changes
   - Task: Scan `oh-my-opencode.jsonc` for model configuration changes

2. Wait for all exploration tasks to complete and collect their findings

3. Launch parallel directory scanning tasks:
   - Task: Scan `skills/` directory and enumerate all skills
   - Task: Scan `agents/` directory and enumerate all custom agents
   - Task: Scan `commands/` directory and enumerate all custom commands

4. Synthesize all findings and determine what README.md sections need updates

### Phase 3: README.md Synchronization

Based on detected changes, update the appropriate sections:

**For `opencode.jsonc` Plugin Changes:**
- Navigate to **Plugins** section in README.md
- Parse current plugin configurations from `opencode.jsonc`
- Update plugin documentation with current configurations
- Extract documentation URLs from plugin names/versions
- Add or update corresponding links in **Reference Links** section
- Validate that all documentation links are accessible

**For `opencode.jsonc` MCP Changes:**
- Navigate to **Manually Configured MCPs** subsection
- Parse current MCP configurations from `opencode.jsonc`
- Update MCP documentation to match current configurations
- Extract MCP documentation URLs or repository links
- Add or update corresponding links in **Reference Links** section
- Validate link accessibility

**For `opencode.jsonc` Provider Changes:**
- Navigate to **Provider List** subsection within **Providers** section
- Parse current provider configurations from `opencode.jsonc`
- Update provider list to reflect currently enabled providers
- Document provider details: API endpoints, authentication, models, capabilities

**For Directory Synchronization:**

Skills Documentation:
- Compare skills found in `skills/` directory with Skills section in README.md
- Identify missing skills (installed but not documented)
- Identify outdated skills (documented but missing or with wrong descriptions)
- Update Skills section to reflect complete, current state

Custom Agents Documentation:
- Compare agents found in `agents/` directory with Custom Agents section
- Identify missing agents (installed but not documented)
- Update Custom Agents documentation with current configurations
- Ensure accurate model assignments and descriptions

Custom Commands Documentation:
- Compare commands found in `commands/` directory with Commands section
- Verify all custom commands are documented
- Update documentation as needed

**Models Configuration:**
- Scan `oh-my-opencode.jsonc` and compare against Models Configuration section
- Verify all agent-specific model assignments match
- Verify all task category model configurations match
- Check model variant specifications are accurate
- Verify provider mappings and aliases are consistent

### Phase 4: Validation and Output

After completing updates, perform comprehensive validation:

1. Use **Bash tool** to validate README.md structure if needed
2. Generate a clear change summary with:
   - Modified files detected
   - Affected documentation sections
   - Changes applied
   - Any errors or warnings
3. Use **Write tool** to save the updated README.md
4. Provide a final status report with checkmarks for each action completed

## Tool Usage Guidelines

When analyzing and updating documentation:

**Use Task Tool for Complex Operations:**
- Parallel file scanning and analysis
- Multi-step synchronization workflows
- Complex directory enumeration tasks

**Use Bash Tool for Direct Operations:**
- Creating or checking directories
- Reading and writing files
- Command execution (git, file tests)
- Simple text processing and validation

**Use Write Tool for File Modifications:**
- Writing updated README.md
- Creating backup files
- Writing any new configuration files

**Error Handling:**
- Always check tool return values and handle errors gracefully
- Provide clear, actionable error messages
- Suggest resolution steps when operations fail

## Expected Output Format

```
📋 README Synchronization Report
==============================

Detected Changes:
  ✓ opencode.jsonc (MCPs section updated)
  ✓ oh-my-opencode.jsonc (agents modified)
  ✓ skills/ (new skills detected)

Documentation Sections Updated:
  → Plugins: Added 1 plugin, updated 2
  → MCPs: Updated 3 MCP configurations
  → Provider List: Synchronized with 5 providers
  → Skills: Added 2 missing skills
  → Custom Agents: Updated 1 agent configuration
  → Models Configuration: Synchronized agent and task category assignments

Reference Links Validation:
  ✓ All 8 documentation links verified and accessible
  ⚠️ 1 link returned 404 (needs correction)

✅ Synchronization complete - 4.2s elapsed
```

## Important Notes

1. **Non-Destructive by Default**: Only modify README.md when actual configuration changes are detected
2. **Preserve Formatting**: Maintain existing structure, headings, and formatting style
3. **Respect Existing Content**: Preserve explanatory text and usage notes
4. **Validation First**: Always validate reference links before considering complete
5. **Atomic Updates**: Group related changes into single updates when possible
6. **Backup Before Changes**: Always create a README.md backup before modifications

## Quality Checklist

Before considering the task complete, verify:

- [ ] All configuration files were scanned
- [ ] Only relevant README.md sections were modified
- [ ] Reference links were validated
- [ ] Clear summary was provided
- [ ] All directory enumerations were accurate
- [ ] Model configurations were synchronized correctly
- [ ] No unintended formatting changes were introduced
