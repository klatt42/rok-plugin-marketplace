---
name: memory-write
description: |
  Write important decisions, patterns, or learnings to persistent memory
  in Supabase with GitHub sync. Supports categories: decision, pattern,
  gotcha, preference.
triggers:
  - "memory write"
  - "save memory"
  - "persist memory"
  - "store memory"
  - "remember this"
version: 1.2
author: ROK Agency
---

# Memory Write

Write important decisions, patterns, or learnings to persistent memory

## Usage

```
/rok-agency-workflows:memory-write category:"decision" key:"auth" value:"Use JWT"
/rok-agency-workflows:memory-write category:"gotcha" key:"rls" value:"Enable RLS first"
```

## When to Use

- When you need to invoke /rok-agency-workflows:memory-write
- When the user's request matches the trigger keywords above
