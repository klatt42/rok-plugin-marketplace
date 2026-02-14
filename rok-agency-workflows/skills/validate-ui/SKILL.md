---
name: validate-ui
description: |
  Validate UI implementation against design expectations using browser
  automation. Supports agent-browser CLI, Claude in Chrome, and Playwright
  MCP methods with screenshots and console monitoring.
triggers:
  - "validate ui"
  - "ui validation"
  - "visual validation"
  - "browser test"
  - "ui check"
version: 1.2
author: ROK Agency
---

# Validate Ui

Validate UI implementation against design expectations using browser

## Usage

```
/rok-agency-workflows:validate-ui url:http://localhost:3000
/rok-agency-workflows:validate-ui method:chrome-debug
```

## When to Use

- When you need to invoke /rok-agency-workflows:validate-ui
- When the user's request matches the trigger keywords above
