---
name: select-medigap
description: |
  Interview-driven Medigap Plan G vs Plan N selection. Asks clarifying
  questions about location, age, medical usage, and priorities, then
  dispatches 3 research agents for premium, regulatory, and cost analysis.
triggers:
  - "select medigap"
  - "choose medigap"
  - "medigap selection"
  - "medigap help"
version: 1.0
author: ROK Agency
---

# Select Medigap

Interview-driven Medigap Plan G vs Plan N selection with 3-agent research pipeline.

## Usage

```
/medigap-selector:select-medigap                    # Full interview
/medigap-selector:select-medigap --zip=21401         # Pre-fill location
/medigap-selector:select-medigap --zip=21401 --age=65 # Pre-fill location + age
```

## When to Use

- When you need to invoke /medigap-selector:select-medigap
- When the user's request matches the trigger keywords above
