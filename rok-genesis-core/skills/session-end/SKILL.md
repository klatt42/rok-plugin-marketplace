---
name: session-end
description: |
  Harness-pattern session completion implementing Anthropic's agent shutdown
  protocol. Summarizes work, updates progress file, marks features, commits
  checkpoint, captures learnings, and validates handoff.
triggers:
  - "session end"
  - "end session"
  - "close session"
  - "session shutdown"
  - "wrap up"
version: 1.2
author: ROK Agency
---

# Session End

Harness-pattern session completion implementing Anthropic's agent shutdown

## Usage

```
/rok-genesis-core:session-end                       # Interactive shutdown
/rok-genesis-core:session-end summary:"Completed OAuth flow"
```

## When to Use

- When you need to invoke /rok-genesis-core:session-end
- When the user's request matches the trigger keywords above
