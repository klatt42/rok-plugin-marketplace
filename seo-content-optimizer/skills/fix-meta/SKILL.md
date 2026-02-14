---
name: fix-meta
description: |
  Analyze and fix the title tag and meta description of a specific URL.
  Fetches current metadata, evaluates against best practices, generates
  improved versions, and presents before/after comparison.
triggers:
  - "fix meta"
  - "fix title"
  - "fix description"
  - "meta tags"
  - "improve meta"
version: 1.2
author: ROK Agency
---

# Fix Meta

Analyze and fix the title tag and meta description of a specific URL.

## Usage

```
/seo-content-optimizer:fix-meta url:https://example.com/page
/seo-content-optimizer:fix-meta url:https://example.com keyword:"water damage"
```

## When to Use

- When you need to invoke /seo-content-optimizer:fix-meta
- When the user's request matches the trigger keywords above
