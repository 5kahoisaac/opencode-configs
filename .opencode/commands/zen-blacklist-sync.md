---
description: Synchronizes OpenCode Zen Blacklist configuration with latest models list
---

# OpenCode Command: OpenCode Zen Blacklist Synchronizer

This command extracts the list of paid models from OpenCode Zen, removes any that belong to Gemini's free tier, and updates the blacklist in `./opencode.json`.

## Command Execution Strategy

You must execute this command with a strategic approach, carefully analyzing the current state before making modifications. Follow these phases:

### Phase 1: Extract the full list of **paid** model IDs from OpenCode Zen

Extract the full list of **paid** model IDs from https://opencode.ai/docs/zen/ as a string array.

> Extracted Paid Model IDs simple from Zen at 2026-04-15
> ```json
> [
>   "gpt-5.4",
>   "gpt-5.4-pro",
>   "gpt-5.4-mini",
>   "gpt-5.4-nano",
>   "gpt-5.3-codex",
>   "gpt-5.3-codex-spark",
>   "gpt-5.2",
>   "gpt-5.2-codex",
>   "gpt-5.1",
>   "gpt-5.1-codex",
>   "gpt-5.1-codex-max",
>   "gpt-5.1-codex-mini",
>   "gpt-5",
>   "gpt-5-codex",
>   "gpt-5-nano",
>   "claude-opus-4-6",
>   "claude-opus-4-5",
>   "claude-opus-4-1",
>   "claude-sonnet-4-6",
>   "claude-sonnet-4-5",
>   "claude-sonnet-4",
>   "claude-haiku-4-5",
>   "claude-3-5-haiku",
>   "gemini-3.1-pro",
>   "gemini-3-flash",
>   "qwen3.6-plus",
>   "qwen3.5-plus",
>   "minimax-m2.5",
>   "glm-5.1",
>   "glm-5",
>   "kimi-k2.5",
>   "big-pickle",
>   "nemotron-3-super-free"
> ]
> ```
> IMPORTANT: You MUST fetch the latest data and get the list in every run, DO NOT reuse this simple!

### Phase 2: Gemini Free Tier Filter

Check https://ai.google.dev/gemini-api/docs/pricing:
- If any extracted model (or its close variant) has a **free tier** with rate limits → **remove** it from the model IDs list.
- Otherwise → keep it.


### Phase 3: opencode.json Synchronization

Update the `provider.opencode.blacklist` array in `./opencode.json` with the final cleaned list.