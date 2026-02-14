---
name: idea-shortlist
description: |
  Recall and filter the most recently generated plugin idea shortlist.
  Supports filtering by tier (BUILD_NOW, STRONG, BACKLOG, PASS),
  product pathway, and top N results.
triggers:
  - "idea shortlist"
  - "view ideas"
  - "plugin shortlist"
  - "recall ideas"
  - "filter ideas"
version: 1.2
author: ROK Agency
---

# Idea Shortlist

Recall and filter the most recently generated plugin idea shortlist.

## Usage

```
/plugin-idea-generator:idea-shortlist               # Show full list
/plugin-idea-generator:idea-shortlist --tier=BUILD_NOW
```

## When to Use

- When you need to invoke /plugin-idea-generator:idea-shortlist
- When the user's request matches the trigger keywords above
