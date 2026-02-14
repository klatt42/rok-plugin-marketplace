---
name: memory-query
description: |
  Retrieve stored memories from Supabase to inform current work. Query by
  category, project, key, or time range. Supports synthesized summaries
  for pattern recognition.
triggers:
  - "memory query"
  - "query memory"
  - "recall memory"
  - "search memory"
  - "get memory"
version: 1.2
author: ROK Agency
---

# Memory Query

Retrieve stored memories from Supabase to inform current work. Query by

## Usage

```
/rok-agency-workflows:memory-query category:"decision"
/rok-agency-workflows:memory-query key:"auth" --synthesize
```

## When to Use

- When you need to invoke /rok-agency-workflows:memory-query
- When the user's request matches the trigger keywords above
