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

### Phase 2: Free Tier Verification (MANDATORY)

**Zen support BYOK, you MUST cross-check provider's official pricing to identify free-tier models.**

**Process:**
1. Take each Zen model ID from your candidate list
2. Map it to the official provider's model naming (e.g., `gemini-3.1-pro` → Google Gemini)
3. Check the official pricing page for that provider
4. Look for "Free" tier, "Free of charge", or "$0.00" pricing
5. If found → **REMOVE from blacklist candidate list**

**Critical provider checks:**

- **Google Gemini**: `https://ai.google.dev/gemini-api/docs/pricing` (MUST get the data!!!, DO NOT SKIP this step)
    - Look for models marked "Free of charge" in the pricing table
    - Be careful with variant names: `gemini-3-flash` vs `gemini-3-flash-preview` vs `gemini-3.1-flash-lite-preview`
    - If uncertain about a variant, check if the base model name has a free tier

**Rule:** If ANY model ID (or close variant) has a free tier on the provider pricing page, **REMOVE it from the blacklist candidate list**.

**When uncertain:** Default to **REMOVE** from blacklist. It is better to accidentally allow a paid model than to block a free one.

### Phase 3: Update opencode.json

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

## Historical Incident

**Date:** 2026-04-19
**Issue:** `gemini-3-flash` was incorrectly added to blacklist
**Root Cause:** Trusted incomplete librarian result showing only paid pricing rows, missed free tier
**Fix:** Removed `gemini-3-flash`, created this documentation
**Lesson:** Always verify official pricing. When uncertain, remove from blacklist.
