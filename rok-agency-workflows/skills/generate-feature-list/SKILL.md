---
name: generate-feature-list
description: |
  Generate a feature_list.json from PRDs, task lists, or project requirements.
  Extracts features, creates validation steps, maps dependencies, assigns
  priorities, and outputs harness-compatible JSON.
triggers:
  - "generate feature list"
  - "feature list"
  - "feature tracking"
  - "extract features"
  - "feature json"
version: 1.2
author: ROK Agency
---

# Generate Feature List

Generate a feature_list.json from PRDs, task lists, or project requirements.

## Usage

```
/rok-agency-workflows:generate-feature-list         # From context
/rok-agency-workflows:generate-feature-list source:PRD.md
```

## When to Use

- When you need to invoke /rok-agency-workflows:generate-feature-list
- When the user's request matches the trigger keywords above
