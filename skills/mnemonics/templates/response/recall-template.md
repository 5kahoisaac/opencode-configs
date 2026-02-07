📋 Memory Recall Results

{{#each memories}}
✓ {{this.title}}
  - Type: {{this.type}}
  - Topic: {{this.topic}}
  - Created: {{this.created_at}}
  - Last Modified: {{this.last_modified_at}}

{{this.content}}

{{#if this.related_memories}}
**Related Memories:**
{{#each this.related_memories}}
- {{this}}
{{/each}}
{{/if}}

---

{{/each}}

✅ Recall complete.
