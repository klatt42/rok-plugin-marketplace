---
name: idea-export
description: |
  Re-export business idea analysis data from the current session to MD, PDF,
  and HTML files. Packages results from analyze-idea, idea-deep-dive, or
  idea-matrix into formatted documents on the Desktop.
triggers:
  - "idea export"
  - "export analysis"
  - "export report"
  - "save analysis"
  - "download report"
version: 1.2
author: ROK Agency
---

# Idea Export

Re-export business idea analysis data from the current session to MD, PDF,

## Usage

```
/business-idea-analyzer:idea-export                 # Export all formats
/business-idea-analyzer:idea-export --format=pdf    # PDF only
```

## When to Use

- When you need to invoke /business-idea-analyzer:idea-export
- When the user's request matches the trigger keywords above
