---
description: Dynamically synchronizes the OpenCode xAI Blacklist by first consulting official xAI documentation to identify current flagship model families, then blacklisting non-LLM models and models from older/outdated families. Coding models are always preserved.
---

# OpenCode Command: OpenCode xAI Blacklist Synchronizer

This command keeps the local OpenCode configuration up-to-date for the **xAI** provider.  
It prioritizes the official documentation to determine which model families are currently the **latest/flagship** ones, then builds a blacklist that excludes:

- Non-LLM / multimodal models (vision, image generation, video, voice, etc.)
- Models belonging to older or outdated families

**Key Principles** (future-proof):
- The definition of "latest" is **not hardcoded** — it is dynamically determined from https://docs.x.ai/developers/models on every run.
- As new major versions (e.g. Grok-5) are released, the command will automatically treat previous generations as outdated.
- Coding-specific models are **never** added to the blacklist, regardless of version.

## Command Execution Strategy

### Phase 1: Determine Current Flagship Models from Official Documentation (Primary Source)

1. Fetch and analyze: **https://docs.x.ai/developers/models**
2. Identify the current **flagship / latest model families** (e.g. Grok-4.20 family, Grok-4.1 fast variants, Grok-4 family, etc.).
3. Any model family that is **not** listed as current flagship/latest is considered **outdated** for the purpose of blacklisting.

### Phase 2: Fetch Complete List of xAI Models

Fetch all available model identifiers from:
- https://github.com/anomalyco/models.dev/tree/dev/providers/xai/models

Extract model IDs from the TOML filenames.

### Phase 3: Build the Blacklist

Apply the following filters to the full list of models:

1. **Blacklist non-LLM / multimodal models**
    - Any model containing keywords such as: `vision`, `imagine`, `image`, `video`, `voice`, `audio`, `tts`, etc.
    - Examples: `grok-*-vision*`, `grok-vision-beta`, `grok-imagine-*`

2. **Blacklist models from outdated families**
    - Any model whose major version/family is **not** part of the current flagship families identified in Phase 1.
    - (For example: all `grok-2*` and `grok-3*` models are typically outdated when Grok-4.20+ is the latest.)

3. **Always preserve coding models**
    - Never blacklist models that are clearly coding-focused (e.g. `grok-code-fast-1` or future equivalents).

4. **Keep current flagship models**
    - All models belonging to the latest families (Grok-4.20*, Grok-4.1*, Grok-4*, etc.) are **excluded** from the blacklist.

### Phase 4: Update opencode.json

1. Read the existing `./opencode.json` file.
2. Update or create the key: `provider.xai.blacklist`
3. Replace the array with the final blacklist.
4. Save the file cleanly while preserving formatting and other settings.

**Example of a generated blacklist** (actual content is dynamic):

```jsonc
{
  "provider": {
    "xai": {
      "blacklist": [
        "grok-2",
        "grok-2-latest",
        "grok-2-1212",
        "grok-2-vision",
        "grok-2-vision-latest",
        "grok-3",
        "grok-3-latest",
        "grok-3-fast",
        "grok-3-mini",
        "grok-3-mini-fast",
        "grok-vision-beta",
        "grok-imagine-image",
        "grok-imagine-image-pro",
        "grok-imagine-video"
      ]
    }
  }
}