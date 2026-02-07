# Response to Prometheus

## Memory classification logic: How to automatically classify input into memory types? This needs to be in the skill or scripts.

I think we're better using the "skill" to determine the "Memory Types".
As the changes and findings are always refer to git changes and user inputs,
It usually some human prompt, and it's hard to classify in script level,
as we can't define all the keywords to match the "Memory Types".

Therefore, I think we're better using "skills" to analyze the memory with agent and then,
gather the "Memory type", content and the needed information.
On the script side, accepting different arguments when skill trigger it.

Rough idea for "memory-remember" script,
you can pass argument like: memory type, content and etc.
with this format: ``python memory-remember.py arg1 arg2``

To sum up,
the scripts are internal tools,
to standardize the process, like saving file, remove file, extract keywords etc.
And the decision-making and thinking parts are all rely on the skill to guide the agent.

P.S. The skill level must define the "Memory Types", including:
- architectural decision
- design decision
- unclassified decision
- learning
- user preference
- project preference
- blocker
- issue
- context
- recurring pattern
- conventions pattern
- unclassified pattern

---

## Similarity detection: How to determine if memories are similar enough to be combined? This requires semantic similarity or pattern matching.

You can compare the similarity by following the below steps
(it's a rough idea, you can enhance it, let's discuss if needed):

1. Always exclude the memories in different "Memory type" to avoid useless comparison.
2. Create a python script `memory-compare.py` with [difflib](https://docs.python.org/3/library/difflib.html),
   using `SequenceMatcher` to compare the similarity ratio.
3. Compare the filename of all memories in corresponding memory type's folder
- if the filename almost the same with "pending store memory" (ratio >= 0.75) → combine their content → ensure no duplicate content after modifications;
- if no existing memories filename



---

## Memory catalog synchronization: How to keep MEMORIES.md in sync with actual memory files? Need automatic catalog update.

<!-- TODO -->

---

## Search/recall strategy: How does memory_recall work? Full-text search? By type? By topic? Need to define this.

<!-- TODO -->

---

## Integration with orchestration: How does this skill get triggered in the oh-my-opencode workflow? After what event?

<!-- TODO -->

---

## Memory deduplication: The document mentions "if yes, combine with previous memory" - but how do we determine similarity?

<!-- TODO -->

---

## Template system: The templates folder structure is mentioned but need actual template content defined.

<!-- TODO -->

---
