---
name: move-stage
description: |
  Move a deal to a different stage within its pipeline. Validates the stage
  exists and shows before/after state with optional notes.
triggers:
  - "move stage"
  - "advance deal"
  - "change stage"
  - "deal stage"
  - "update stage"
version: 1.2
author: ROK Agency
---

# Move Stage

Move a deal to a different stage within its pipeline. Validates the stage

## Usage

```
/deal-management:move-stage deal:123 stage:"proposal"
/deal-management:move-stage deal:"Acme Corp" stage:"negotiation"
```

## When to Use

- When you need to invoke /deal-management:move-stage
- When the user's request matches the trigger keywords above
