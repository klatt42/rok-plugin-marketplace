---
name: pipeline-view
description: |
  Display a visual pipeline board showing all deals grouped by stage with
  counts and values. ASCII Kanban-style board with status filtering.
triggers:
  - "pipeline view"
  - "view pipeline"
  - "deal board"
  - "kanban"
  - "pipeline board"
version: 1.2
author: ROK Agency
---

# Pipeline View

Display a visual pipeline board showing all deals grouped by stage with

## Usage

```
/deal-management:pipeline-view                      # Default pipeline
/deal-management:pipeline-view pipeline:general_sales status:active
```

## When to Use

- When you need to invoke /deal-management:pipeline-view
- When the user's request matches the trigger keywords above
