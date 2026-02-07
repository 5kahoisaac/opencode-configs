# Classification

## Classification Logic (HIGH PRIORITY)

- Option A: Agent-driven classification at skill level (LLM analyzes user intent) 
- Option B: Explicit type specification (user says "Remember as architectural decision: ...")

I think both of approach are nice and acceptable. You can do it hybridly. If LLM can not analyze user intent, then ask for further explicit type specification.

---

## Semantic Search vs Agent-Based (HIGH PRIORITY)

- Option A: Embedding-based semantic search (requires embedding model + vector storage)
- Option B: Agent-based similarity (LLM reads files and compares)

I pick Option B (agent-based) initially for simplicity.

---

## Memory Catalog (MEMORIES.md)

- Option A: Keep catalog file (manual or auto-synced) for quick overview
- Option B: Remove catalog entirely (folder structure is sufficient indexing)
- Option C: Hybrid: Catalog exists but only for human reference, not agent operations

I pick Option B

---

## Similarity Threshold

Question: What qualifies as "similar"?

- Same topic with different details? (combine)
- Same type with minor overlap? (create separate)
- Completely different but semantically related? (link? separate?)

Example scenario:

Memory 1: "Authentication uses JWT tokens stored in Redis"
Memory 2: "Session management: Redis stores JWT with 30min expiry"

Should these be:
- Option A: Combined (same topic)
- Option B: Separate (different aspects)
- Option C: Linked (reference each other)

I pick Option C, but avoid causing any circular dependency problem on linkage

---

## Orchestration Integration

Your Scenario is wrong. It depends on the actions of the skills: recall, remember or forget

No actual "compound" step is defined, orchestrator originally loaded the "skill".

After orchestrator parsing the human prompt and identified the intention of the user,
it MUST **recall** the "memory" automatically and find any matches.

For **remember** and **forget**, it always triggered by user prompt manually.

---

## Template Content

Memory Template must include metadata fields (created at, modified at).
Sections like "Overview", "Examples", "Related" sections MUST be required,
and other section is flexible based on memory type.

Response Template remain fixed format like my examples (checkmark style),
it will be more standardize while switching model.
Coz everyone follow the same standard

---

## Error Handling

It depends on situation: 
- Memory file already exists (same name)? → Ask user how to proceed
- Memory folder doesn't exist (first-time setup)? → Auto-fix (create folders, overwrite with confirmation)
- Similar memories found but user says "NO, they're different"? → Ask user how to proceed
- No memories found during recall? → No memory matched is fine, then process to next step.

---

