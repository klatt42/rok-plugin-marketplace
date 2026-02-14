---
name: review
description: |
  Comprehensive multi-dimensional code review before production deployment.
  Reviews entire repository for security, performance, code quality, tests,
  UI/UX, and responsive design. Supports single or multi-model modes.
triggers:
  - "code review"
  - "production review"
  - "pre-deploy review"
  - "security review"
  - "review code"
version: 1.2
author: ROK Agency
---

# Review

Comprehensive multi-dimensional code review before production deployment.

## Usage

```
/production-code-review:review                      # Full review of cwd
/production-code-review:review --mode=multi         # Multi-model review
```

## When to Use

- When you need to invoke /production-code-review:review
- When the user's request matches the trigger keywords above
