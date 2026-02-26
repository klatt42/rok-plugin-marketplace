---
name: code-review-methodology
description: |
  Production code review methodology for the production-code-review plugin.
  Contains scoring formulas, verdict determination, severity classification,
  and confidence scoring guidelines. Supports 6 static dimensions + optional
  E2E browser validation (7th dimension). Load on-demand when detailed
  methodology context is needed during review orchestration.
triggers:
  - "review methodology"
  - "scoring formula"
  - "production readiness"
  - "code review scoring"
  - "e2e scoring"
version: 2.0
author: ROK Agency
---

# Code Review Methodology

## Production Readiness Score

Weighted score across 6 static dimensions (+ optional E2E) with penalty system:

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

### Without E2E (default, backward compatible)

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Code Quality | 20% | Foundation of maintainability |
| Testing | 20% | Safety net for production |
| Security | 20% | Non-negotiable for production |
| UI/UX | 15% | Direct user experience impact |
| Responsive | 15% | Multi-device requirement |
| Performance | 10% | Important but measurable post-deploy |

### With E2E (--e2e flag, 7 dimensions)

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Code Quality | 15% | Reduced slightly to accommodate E2E |
| Testing | 15% | Reduced slightly to accommodate E2E |
| Security | 20% | Non-negotiable, unchanged |
| UI/UX | 10% | E2E partially validates UX in practice |
| Responsive | 10% | E2E responsive checks complement this |
| Performance | 10% | Unchanged |
| E2E Validation | 20% | Live user journey validation is high-value |

**Note**: If E2E returns `score: null` (skipped), the 6-dimension weights are used automatically.

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

## Multi-Model Scoring (v2.0)

When `review_mode` is `"multi"`, the scoring formula extends to handle consensus across Claude, Codex, and Gemini.

### Per-Dimension Consensus Score

```
consensus_score[d] = mean(model_scores[d] for each model that successfully reported)

If all 3 models agree within 10 points: consensus_score[d] += 2 (harmony bonus, cap 100)
If model score spread > 25 points: flag "model_disagreement" for dimension d
```

### Issue Confidence Boost

Issues found by multiple models receive a confidence boost:

```
boosted_confidence = base_confidence + (model_agreement - 1) * 5
Capped at 100
```

| Models Agree | Confidence Boost | Significance |
|-------------|-----------------|--------------|
| 1 model | +0 | Unique finding -- still valuable |
| 2 models | +5 | Likely real issue |
| 3 models | +10 | High-confidence consensus |

### Final Score Formula (Multi-Model)

Same weighted formula as single-model, using consensus_score[d] for each dimension.
Uses 6-dimension or 7-dimension weights depending on whether E2E is included:

```
# Without E2E:
weighted = consensus_code_quality*0.20 + consensus_testing*0.20 +
           consensus_ui_ux*0.15 + consensus_responsive*0.15 +
           consensus_security*0.20 + consensus_performance*0.10

# With E2E (note: E2E is Claude-only in multi-model, consensus = Claude score):
weighted = consensus_code_quality*0.15 + consensus_testing*0.15 +
           consensus_ui_ux*0.10 + consensus_responsive*0.10 +
           consensus_security*0.20 + consensus_performance*0.10 +
           e2e_validation*0.20

penalties = (critical * 10) + (high * 3)
final = max(0, min(100, round(weighted - penalties)))
```

Verdict thresholds unchanged from single-model.

### Issue Sorting (Multi-Model)

1. By model_agreement DESC (consensus findings first)
2. By severity: CRITICAL > HIGH > MEDIUM > LOW
3. By confidence DESC

## E2E Validation Scoring (v3.0)

### E2E Dimension Score

Start at 100, deduct:

| Issue Type | Deduction |
|-----------|-----------|
| Critical journey FAILED (auth, payment, core CRUD) | -15 |
| Secondary journey FAILED (settings, profile, about) | -8 |
| Journey PARTIAL (some steps pass, some fail) | -5 |
| Responsive viewport fails (per viewport) | -10 |
| Console error found (per unique error) | -3 |

Floor at 0.

### E2E Severity Classification

| Severity | Criteria | Example |
|----------|----------|---------|
| CRITICAL | Core user journey completely blocked | Signup form throws unhandled error, login redirect fails |
| HIGH | Secondary journey fails or data validation mismatch | Settings page crashes, DB record not created after form submit |
| MEDIUM | Partial journey failure, cosmetic issues in flow | Form submits but success message missing, slow page transition |
| LOW | Console warnings, minor viewport issues | Non-critical JS warning, slight layout shift on tablet |

### E2E in Multi-Model Mode

- E2E validation is **only dispatched to Claude** (Codex/Gemini CLIs cannot control browsers)
- In multi-model consensus analysis, E2E findings are tagged as "Claude E2E" (not consensus)
- E2E issues do not receive model_agreement boost since only one model runs them
- E2E score is included in the weighted formula at 20% weight

### E2E Prerequisites

E2E is gracefully skipped (score = null, excluded from weights) when:
- No browser tool installed (playwright-cli or agent-browser)
- No frontend detected in project
- Dev server fails to start
- Platform is Windows native (not WSL)
