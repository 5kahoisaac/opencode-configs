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
you can pass argument like: memory type, content etc.
with this format: ``python memory-remember.py learning arg2``

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

You can compare the similarity by following steps
(it's a rough idea, you can enhance it, let's discuss if needed):

1. Always exclude the memories in different "Memory type" to avoid useless comparison.
2. Scans catalog, classifies via regex/LLM
3. Embedding python script to do semantic search over the corresponding memory type's folder
4. Semantic search usually provide score:
   - if the score is high enough then consider similar → combine their content → ensure no duplicate content after modifications;
   - Otherwise, consider as a new memory and store in the corresponding memory type's folder

P.S. I can accept replacing the semantic search by:
simply ask the agent to loop though files of the corresponding memory type's folder,
and determine the similarity by reading the details of the memory

---

## Memory catalog synchronization: How to keep MEMORIES.md in sync with actual memory files? Need automatic catalog update.

I'm thinking about remove the `MEMORIES.md` as the folder structure already do a great indexing by memory type.

---

## Search/recall strategy: How does memory_recall work? Full-text search? By type? By topic? Need to define this.

You can recall the memory by following the steps
(it's a rough idea, you can enhance it, let's discuss if needed):

1. Classify the type first
2. Embedding python script to do semantic search over the corresponding memory type's folder with the related topic 

P.S. I can accept replacing the semantic search by:
simply ask the agent to loop though files of the corresponding memory type's folder,
and match the related memory by reading the details of the memory

---

## Integration with orchestration: How does this skill get triggered in the oh-my-opencode workflow? After what event?

For the trigger part, 
we can just design a prompt to describable the skill "mnemonics"
and append into the AGENTS.md or attach the via "prompt_append" field for oh-my-opencode orchestrator (agent)

The details of the prompt (rough idea):

```markdown
# When to trigger recall:

## Automatically recall when doing planning/ reviewing works
After parsing the human prompt and identified the intention of the user,
"recall" related memory of the intention by memory type and the topic. 
Pass the received report from the skill "mnemonics" to the next agent.

## Remember and forgot are always trigger by user
For example, after resolving issue and problem. Remember the memory only if the user say something like "Remember this bugs", "Remember xxxx.", "Forget xxxx as it resolved" or etc.

```

---

## Memory deduplication: The document mentions "if yes, combine with previous memory" - but how do we determine similarity?

Make a confirmation with the user, and pending the result before next step.

---

## Template system: The templates folder structure is mentioned but need actual template content defined.

```text
.
└── mnemonics/
├── SKILL.md
├── scripts/
│   ├── memory-remember.py
│   └── memory-delete.py
├── templates/
│   ├── response/
│   │   ├── recall-template.md
│   │   ├── remember-template.md
│   │   └── forget-template.md
│   └── memory/
└── record-template.md
```

**mnemonics/SKILL.md**
- the main entry of the skill
  - Including all the instruction of the skill, e.g. when to use, how to recall, or etc.
  - Refer to the **templates/response/*.md** template to standardize the response format
  - Refer script from **scripts** folder to create, update or delete memory
  - etc.

**templates/response/*.md**
- The response template of the skill

**templates/memory/*.md**
- The standard template format of the memory

**mnemosyne/scripts/*.py**
- Scripts written in *.py from internal usage
- Aims to resolve simple usage, e.g. create, update or delete of memory record
- etc

---

Apart from your question,
I also prepared the example format of the memory *.md file:

```markdown
# naming-standard.md

## Overview
Describe the variable naming standard for file, variables, function or etc.

## When to use/ apply? What's the related Topic?
- Create new function
- Create new variables
- etc.

## How to apply/ use?
- Always naming with camel case

## Verification
- Check whether all function, variable, folder, filename have no "space", "symbol"
- Naming match /^[a-z]+(?:[A-Z][a-z0-9]*)*$/ pattern

## Related memory
- project-preference/component-development.md
```
