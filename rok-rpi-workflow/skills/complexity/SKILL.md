---
name: complexity
description: |
  Assess task complexity and recommend the appropriate cognitive protocol
  depth. Analyzes signals for SIMPLE, MEDIUM, or COMPLEX classification
  to determine required workflow rigor.
triggers:
  - "complexity"
  - "assess complexity"
  - "task complexity"
  - "how complex"
  - "complexity check"
version: 1.2
author: ROK Agency
---

# Complexity

Assess task complexity and recommend the appropriate cognitive protocol

## Usage

```
/rok-rpi-workflow:complexity add user authentication
/rok-rpi-workflow:complexity                        # Assess current task
```

## When to Use

- When you need to invoke /rok-rpi-workflow:complexity
- When the user's request matches the trigger keywords above
