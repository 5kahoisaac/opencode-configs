# Courier Mnemonic Override Failure

- created at: 2026-02-08T12:05:00Z
- last modified at: 2026-02-08T12:05:00Z
- memory type: project preference

## Overview

Courier routing instructions conflicted with mnemonics skill. Failed to execute actual file write despite explicit "Create memory file" instruction. Only reported path without mkdir+write operations.

## Examples

```
User: "remember context: ..."
AI: "✅ Memory created: .opencode/... (NO ACTUAL WRITE)"
→ Violates workflow step #4: "Write to determined storage path"
```

## Related Memories

- Mnemonics Memory System

## Lessons Learned

- Skills take precedence over Courier routing patterns
- "remember" trigger → BYPASS all delegation/reporting → IMMEDIATE mkdir+cat>file
- No preambles, no verifications → direct filesystem mutation

