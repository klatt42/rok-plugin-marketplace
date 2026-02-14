---
name: project-init
description: |
  Initialize ROK infrastructure for any project. Creates CLAUDE.md,
  claude-progress.txt, feature_list.json, init.sh, and ROK Brain
  integration. Run FIRST when CC touches any project.
triggers:
  - "project init"
  - "initialize project"
  - "setup project"
  - "rok init"
  - "project setup"
version: 1.2
author: ROK Agency
---

# Project Init

Initialize ROK infrastructure for any project. Creates CLAUDE.md,

## Usage

```
/rok-genesis-core:project-init                      # Current directory
/rok-genesis-core:project-init project:my-app
```

## When to Use

- When you need to invoke /rok-genesis-core:project-init
- When the user's request matches the trigger keywords above
