---
description: Dynamically synchronizes the OpenCode blacklist for the Zen provider. For Zen, blacklists paid models (preserving free-tier). Sources are queried fresh on every run.
---

# OpenCode Command: Provider Blacklist Synchronizer (Zen)

This command keeps `./opencode.json` in sync for **OpenCode Zen**. It builds an **exclusion list** so that newly
released models stay available by default — the safer property when providers ship faster than this sync runs.

The blacklist criteria:

| Provider   | Blacklist Criteria                                                           |
|------------|------------------------------------------------------------------------------|
| `opencode` | Paid Zen models (any model with an accessible free tier is always preserved) |

## Core Principles

- **Nothing is hardcoded.** Pricing is re-derived from official sources on every run.
- **Free-tier models are never blacklisted.** The blacklist is for paid-only models; free-tier models must remain
  available for low-cost workflows.
- **Blacklist semantics favor availability.** A model not yet classified stays available. When uncertain whether to add
  a model to the blacklist, prefer to **leave it off** — accidentally hiding a useful new model is worse than briefly
  exposing one that should be filtered.

---

## OpenCode Zen

### Phase 1 — Fetch model + pricing data

Check these sources in order, stopping at the first that returns usable data:

1. `https://opencode.ai/zen/v1/models` (API endpoint — preferred, structured)
2. `https://opencode.ai/docs/zen/` (human-readable fallback)

Extract every model ID along with its pricing fields. Note explicitly free model IDs separately for cross-checking.

### Phase 2 — Identify free-tier models (to exclude from the blacklist)

A Zen model qualifies as free-tier if **any** of the following hold in the Zen data:

- Model ID contains `free` (e.g. `*-free`)
- Pricing table marks it as "Free"
- Input, output, **and** cached-read prices are all `$0.00` or "Free of charge"

**Cross-reference with the official upstream provider's pricing** before classifying. Zen's classification can lag; the
upstream provider is the source of truth. If the two disagree, trust the upstream provider.

**When uncertain whether a model has a free tier, default to keeping it OFF the blacklist** — leaving it available is
the safer error.

### Phase 3 — Build the Zen blacklist

The blacklist is: every Zen model from Phase 1 **except** confirmed free-tier models from Phase 2.

A model family may ship both free and paid variants — evaluate each model ID individually, not by family.

### Phase 4 — Write to `opencode.json`

Update the key `provider.opencode.blacklist` with the resulting array. Replace, do not merge.

```jsonc
{
  "provider": {
    "opencode": {
      "blacklist": [
        // Dynamically generated: paid Zen model IDs (free-tier models excluded)
      ]
    }
  }
}
```

---

## Writing `opencode.json` (procedure)

1. Read the existing `./opencode.json`.
2. Update or create `provider.opencode.blacklist`. Leave all other keys (including unrelated providers) untouched.
3. Preserve formatting: same indentation, no reordering of unrelated keys, trailing newline as before.
4. Validate: `python3 -m json.tool opencode.json` must succeed.
5. Review the diff and confirm only the intended keys changed.

## Common Mistakes

1. **Trusting incomplete evidence.** Always verify pricing from official upstream sources, not just the Zen model
   listing.
2. **"Add if uncertain" bias.** When uncertain whether a model belongs on the blacklist, default to **leaving it off**,
   not adding it. Blacklist errors-of-commission hide useful models; errors-of-omission are self-correcting on the next
   run.
3. **Mixing paid and free variants on Zen.** A model family may have both. Check each specific model ID.