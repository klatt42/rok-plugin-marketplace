---
name: code-review-methodology
description: |
  Production code review methodology for the production-code-review plugin.
  Contains scoring formulas, verdict determination, severity classification,
  and confidence scoring guidelines. Load on-demand when detailed methodology
  context is needed during review orchestration.
triggers:
  - "review methodology"
  - "scoring formula"
  - "production readiness"
  - "code review scoring"
version: 1.0
author: ROK Agency
---

# Code Review Methodology

## Production Readiness Score

Weighted score across 6 dimensions with penalty system:

```
weighted_score = (
  code_quality * 0.20 +
  testing * 0.20 +
  ui_ux * 0.15 +
  responsive * 0.15 +
  security * 0.20 +
  performance * 0.10
)

penalties = (critical_issues * 10) + (high_issues * 3)

final_score = max(0, min(100, round(weighted_score - penalties)))
```

## Dimension Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Code Quality | 20% | Foundation of maintainability |
| Testing | 20% | Safety net for production |
| Security | 20% | Non-negotiable for production |
| UI/UX | 15% | Direct user experience impact |
| Responsive | 15% | Multi-device requirement |
| Performance | 10% | Important but measurable post-deploy |

## Verdict Determination

| Score | Critical Issues | Verdict |
|-------|----------------|---------|
| >= 85 | 0 | PASS |
| >= 70 | 0 | PASS_WITH_WARNINGS |
| < 70 | any | FAIL |
| any | > 0 | FAIL |

## Confidence Scoring

All issues scored 0-100 for confidence:

| Range | Meaning | Action |
|-------|---------|--------|
| 0-49 | Not confident, likely false positive | Discard |
| 50-79 | Moderate confidence, may be real | Discard (below threshold) |
| 80-89 | High confidence, likely real issue | Include in report |
| 90-100 | Certain, verified finding | Include with emphasis |

**Threshold**: Only issues with confidence >= 80 appear in the final report.

## Severity Classification

| Severity | Criteria | Production Impact |
|----------|----------|-------------------|
| CRITICAL | Exploitable vulnerability, data loss risk, crash | Block deployment |
| HIGH | Significant bug, missing validation, poor UX | Should fix first |
| MEDIUM | Code quality issue, missing test, UX improvement | Fix soon |
| LOW | Style issue, minor optimization, nice-to-have | Backlog |

## Non-Web Project Handling

For backend-only or non-UI projects:
- Skip UI/UX and Responsive dimensions
- Redistribute weights: Quality 25%, Testing 25%, Security 30%, Performance 20%
- Adjust scoring formula accordingly
