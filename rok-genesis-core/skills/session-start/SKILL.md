---
name: session-start
description: |
  Harness-pattern session initialization implementing Anthropic's agent startup
  ritual. Confirms directory, loads progress, runs init script, validates
  previous work, and selects next task.
triggers:
  - "session start"
  - "start session"
  - "begin session"
  - "session startup"
  - "session init"
version: 1.2
author: ROK Agency
---

# Session Start

Harness-pattern session initialization implementing Anthropic's agent startup

## Usage

```
/rok-genesis-core:session-start                     # Current project
/rok-genesis-core:session-start project:rok-copilot
```

## When to Use

- When you need to invoke /rok-genesis-core:session-start
- When the user's request matches the trigger keywords above
