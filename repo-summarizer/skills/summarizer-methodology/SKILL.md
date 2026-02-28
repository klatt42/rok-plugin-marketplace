---
name: summarizer-methodology
description: |
  Detailed scoring formulas, gap classification taxonomy, and maturity
  assessment methodology for the repo-summarizer plugin. Load on-demand
  when you need to understand how scores are calculated.
triggers:
  - "summarizer methodology"
  - "maturity scoring"
  - "repo scoring formula"
version: 1.0
author: ROK Agency
---

# Repo Summarizer Methodology

## Maturity Score Formula

```
maturity_score = (
  documentation      * 0.15 +
  feature_completeness * 0.30 +
  infrastructure      * 0.20 +
  test_presence       * 0.15 +
  architecture_clarity * 0.20
)
```

## Dimension Scoring

### Documentation (15%)
Source: purpose-analyzer readme_quality.score
- has_readme: +20
- has_install_instructions: +20
- has_usage_examples: +20
- has_api_docs: +20
- has_contributing_guide: +20
- Default if missing: 30

### Feature Completeness (30%)
Source: feature-enumerator status_breakdown
```
score = (complete * 100 + partial * 50 + stub * 15 + planned * 0) / total
```
- Bonus +5 if has_tests_percentage > 60
- Bonus +5 if has_api_percentage > 70
- Default if missing: 50

### Infrastructure (20%)
Source: gap-finder infrastructure_checklist
Items: error_handling, logging, input_validation, rate_limiting, health_check,
       cors, env_config, ci_cd, migrations, secrets
```
score = (complete_items * 10) + (partial_items * 5)
```
- Penalty -10 per CRITICAL gap
- Penalty -5 per HIGH gap
- Default if missing: 50

### Test Presence (15%)
Source: feature-enumerator coverage_assessment.has_tests_percentage
- Direct percentage (0-100)
- Bonus +10 if CI/CD detected
- Default if missing: 0

### Architecture Clarity (20%)
Source: architecture-mapper
- Base 60 if architecture_style identified
- +10 if 3+ distinct layers
- +10 if 10+ key files identified
- +10 if 3+ navigation tips
- +10 if data flow documented
- Cap at 100
- Default if missing: 50

## Maturity Levels

| Score | Level | Color | Meaning |
|-------|-------|-------|---------|
| >= 80 | MATURE | Green | Production-ready, well-documented, tested |
| >= 60 | DEVELOPING | Amber | Core features work, needs polish |
| >= 40 | EARLY STAGE | Blue | Functional prototype, significant gaps |
| < 40 | PROTOTYPE | Purple | Initial implementation, many stubs |

## Gap Classification Taxonomy

### Gap Types
- **missing_feature**: Feature referenced but not implemented
- **incomplete_implementation**: Partially built, needs completion
- **infrastructure_gap**: Missing standard infrastructure (logging, error handling)
- **ux_gap**: Missing UX pattern (loading states, error states, 404)
- **todo_marker**: TODO/FIXME/HACK in code
- **documentation_gap**: README/docs inaccurate or missing
- **security_gap**: Security vulnerability or missing protection

### Severity Rules
- **CRITICAL**: Hardcoded secrets, security vulnerabilities, data loss risks
- **HIGH**: Missing auth, broken features, infrastructure essentials
- **MEDIUM**: TODO markers, partial implementations, missing UX patterns
- **LOW**: Documentation gaps, minor UX polish, nice-to-have features

### Effort Estimates
- **small**: < 1 hour (add a health check endpoint, fix a TODO)
- **medium**: 1-4 hours (implement error boundary, add logging)
- **large**: 4+ hours (build auth system, implement testing)

## Reference Documents

For full JSON schema documentation, load: `references/output-schema.md`
For multi-repo suite analysis patterns, load: `references/suite-mode-guide.md`
