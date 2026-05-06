# /zen-blacklist-sync Command

## Purpose

Synchronizes the OpenCode Zen blacklist by fetching the latest paid models and excluding any with accessible free tiers.

## Critical Rule

**NEVER add models with accessible free tiers to the blacklist.**

The blacklist is for **paid-only** models. Free-tier models must remain available for low-cost workflows.

## Execution Steps

### Phase 1: Fetch Latest Paid Model IDs

**Sources (check in this order):**
1. `https://opencode.ai/zen/v1/models` (API endpoint - preferred)
2. `https://opencode.ai/docs/zen/` (human-readable fallback)

**Extract:**
- All paid model IDs
- Explicitly free model IDs (to cross-check)

**Identify explicitly free models by these patterns in the Zen pricing data:**
- Model names containing "free" (e.g., `*-free`)
- Models marked as "Free" in pricing tables
- Models with "$0.00" or "Free of charge" for input/output/cached read

**Always cross-reference with official provider pricing** - do not rely solely on Zen's classification.

### Phase 2: Update opencode.json

1. Read `./opencode.json`
2. Update `provider.opencode.blacklist`
3. Replace with final cleaned list
4. Preserve formatting and other settings

## Verification

After updating:
1. Run `python3 -m json.tool opencode.json` to validate JSON
2. Review diff to confirm only intended changes
3. Double-check no free-tier models were added

## Common Mistakes

1. **Trusting incomplete evidence** - Always verify pricing from official sources, not just Zen model listings
2. **"Keep if uncertain" bias** - When uncertain about free tier, default to **REMOVE** from blacklist, not keep
3. **Mixing paid and free variants** - A model family may have both paid and free variants. Check each specific model ID
4. **Not checking official pricing** - Never rely solely on Zen model list; always cross-check official provider pricing
5. **Hardcoding model lists** - Model availability and pricing change. Always extract fresh data from authoritative sources

## Example Final Blacklist Structure

```jsonc
{
  "provider": {
    "opencode": {
      "blacklist": [
        // Dynamically generated from Zen paid models minus free-tier models
        // See Phase 1 and Phase 2 above for extraction process
      ]
    }
  }
}
```
