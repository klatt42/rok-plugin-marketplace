---
name: dispatch
description: |
  Dispatch specialized subagents to work on tasks in parallel using async
  background agents, then synthesize results. Supports predefined patterns
  and custom agent selection.
triggers:
  - "dispatch"
  - "multi-agent"
  - "parallel agents"
  - "agent dispatch"
  - "orchestrate agents"
version: 1.2
author: ROK Agency
---

# Dispatch

Dispatch specialized subagents to work on tasks in parallel using async

## Usage

```
/rok-agency-workflows:dispatch                      # Interactive mode
/rok-agency-workflows:dispatch task:"Review this PR"
```

## When to Use

- When you need to invoke /rok-agency-workflows:dispatch
- When the user's request matches the trigger keywords above
