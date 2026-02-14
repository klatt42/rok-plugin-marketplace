---
name: create-prd
description: |
  Synthesize conversation context into a comprehensive Product Requirements
  Document. Creates PRD.md as the project's single source of truth and
  optionally generates feature_list.json.
triggers:
  - "create prd"
  - "product requirements"
  - "prd document"
  - "requirements doc"
  - "project spec"
version: 1.2
author: ROK Agency
---

# Create Prd

Synthesize conversation context into a comprehensive Product Requirements

## Usage

```
/rok-agency-workflows:create-prd                    # Output to PRD.md
/rok-agency-workflows:create-prd output:docs/PRD.md
```

## When to Use

- When you need to invoke /rok-agency-workflows:create-prd
- When the user's request matches the trigger keywords above
