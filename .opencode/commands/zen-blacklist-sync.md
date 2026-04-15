---
description: Dynamically synchronizes the OpenCode Zen Blacklist by fetching the latest paid models and excluding any with accessible free tiers (especially Gemini).
---

# OpenCode Command: OpenCode Zen Blacklist Synchronizer

This command keeps the local OpenCode configuration up-to-date by extracting the current list of **paid** models from OpenCode Zen, filtering out models (or close variants) that offer a usable free tier, and updating the blacklist in `./opencode.json`.

The goal is to prevent accidental use of free-tier models that may have strict rate limits or lower priority in a paid workflow.

## Command Execution Strategy

Always execute this command with a careful, state-aware approach. Analyze the current configuration and fetched data before applying changes.

### Phase 1: Fetch the Latest Paid Model IDs from OpenCode Zen

Dynamically fetch the complete list of available models from OpenCode Zen.

**Primary sources** (check in this order):
- https://opencode.ai/docs/zen/ (for human-readable list and pricing)
- https://opencode.ai/zen/v1/models (API endpoint for structured machine-readable data — preferred when possible)

Extract **only paid model IDs** as a clean string array. Exclude explicitly free models such as:
- `big-pickle`
- `nemotron-3-super-free`
- `minimax-m2.5-free`
- `gpt-5-nano` (and any other models marked as free input/output/cached read)

**Example of current paid models** (for reference only — **never hardcode**; always fetch fresh data):

```json
[
  "gpt-5.4",
  "gpt-5.4-pro",
  "gpt-5.4-mini",
  "gpt-5.4-nano",
  "gpt-5.3-codex",
  "gpt-5.3-codex-spark",
  "gpt-5.2",
  "gpt-5.2-codex",
  "gpt-5.1",
  "gpt-5.1-codex",
  "gpt-5.1-codex-max",
  "gpt-5.1-codex-mini",
  "gpt-5",
  "gpt-5-codex",
  "claude-opus-4-6",
  "claude-opus-4-5",
  "claude-opus-4-1",
  "claude-sonnet-4-6",
  "claude-sonnet-4-5",
  "claude-sonnet-4",
  "claude-haiku-4-5",
  "claude-3-5-haiku",
  "gemini-3.1-pro",
  "gemini-3-flash",
  "qwen3.6-plus",
  "qwen3.5-plus",
  "minimax-m2.5",
  "glm-5.1",
  "glm-5",
  "kimi-k2.5"
]
```

> Critical: Fetch fresh data on every run. Do not reuse cached or example lists.

### Phase 2: Gemini Free Tier Filter (and Other Free Tiers)

Cross-reference against official pricing pages to remove models with accessible free tiers that could interfere with paid usage.

#### Primary check:
- https://ai.google.dev/gemini-api/docs/pricing

#### Rules:
- If any extracted model (or its close variant) has a **free tier** with rate limits → **remove** it from the model IDs list.
- Otherwise → keep it.

### Phase 3: Update opencode.json

1. Read the existing `./opencode.json` file.
2. Update or create the path: provider.opencode.blacklist (or the exact equivalent path used in your config schema).
3. Replace the array with the final cleaned list of paid model IDs (without free-tier entries).
4. Write the file back cleanly (preserve formatting and other settings).

Example final blacklist structure:
```jsonc
{
  // ... other configuration
  "provider": {
    "opencode": {
      "blacklist": [
        "gpt-5.4",
        "gpt-5.4-pro",
        // ... remaining paid models
      ]
    }
  }
}
```