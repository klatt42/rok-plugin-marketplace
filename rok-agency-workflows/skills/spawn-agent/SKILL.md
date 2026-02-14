---
name: spawn-agent
description: |
  Deploy specialized sub-agents for parallel or sequential task execution
  with complexity-aware protocol routing. Supports listing, creating,
  and deploying custom agent definitions.
triggers:
  - "spawn agent"
  - "deploy agent"
  - "launch agent"
  - "create agent"
  - "agent deploy"
version: 1.2
author: ROK Agency
---

# Spawn Agent

Deploy specialized sub-agents for parallel or sequential task execution

## Usage

```
/rok-agency-workflows:spawn-agent security-reviewer
/rok-agency-workflows:spawn-agent --parallel builder validator
```

## When to Use

- When you need to invoke /rok-agency-workflows:spawn-agent
- When the user's request matches the trigger keywords above
