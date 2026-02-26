---
name: review
description: |
  Comprehensive multi-dimensional code review before production deployment.
  Reviews entire repository across 7 dimensions: security, performance, code
  quality, tests, UI/UX, responsive design, and optional E2E browser validation.
  Supports single or multi-model modes. E2E validation launches the app and
  tests user journeys via browser automation.
triggers:
  - "code review"
  - "production review"
  - "pre-deploy review"
  - "security review"
  - "review code"
  - "e2e review"
  - "end to end review"
version: 2.0
author: ROK Agency
---

# Review

Comprehensive multi-dimensional code review before production deployment.

## Usage

```
/production-code-review:review                      # Full review of cwd (6 static dimensions)
/production-code-review:review --mode=multi         # Multi-model review
/production-code-review:review --e2e                # Include E2E browser validation (7th dimension)
/production-code-review:review --include=security,e2e_validation  # Only specific dimensions
```

## Flags

- `--e2e`: Include E2E browser validation as 7th dimension (opt-in, default OFF)
- `--mode=single|multi`: Single or multi-model review
- `--model=claude|codex|gemini`: Model selection (single mode only)
- `--scope=full|focused`: Review scope
- `--include=dim1,dim2`: Only run specific dimensions (use `e2e_validation` for E2E)

## E2E Validation

When `--e2e` is passed, the review additionally:
1. Discovers app structure and user journeys
2. Starts the dev server
3. Runs browser-qa agents through each journey in parallel
4. Takes screenshots at every step
5. Reports pass/fail per journey with screenshot evidence

**Requirements for E2E**: Linux/WSL/macOS, playwright-cli or agent-browser installed, project has a browser-accessible frontend. If requirements are not met, E2E is gracefully skipped.

**Note**: E2E defaults to OFF because it requires a running server and adds significant time. Weights are rebalanced when E2E is included.

## When to Use

- When you need to invoke /production-code-review:review
- When the user's request matches the trigger keywords above
