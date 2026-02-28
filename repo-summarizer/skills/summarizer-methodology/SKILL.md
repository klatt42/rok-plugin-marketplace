---
name: summarizer-methodology
description: |
  Detailed scoring formulas, gap classification taxonomy, and maturity
  assessment methodology for the repo-summarizer plugin v1.1. Includes
  semantic analysis signals (implementation depth, test runner data,
  integration chains, recency), floor rules, and the handoff/gap split.
  Load on-demand when you need to understand how scores are calculated.
triggers:
  - "summarizer methodology"
  - "maturity scoring"
  - "repo scoring formula"
version: 1.1
author: ROK Agency
---

# Repo Summarizer Methodology (v1.1)

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
Source: feature-enumerator status_breakdown + implementation_depth

**Base formula**:
```
score = (complete * 100 + partial * 50 + stub * 15 + planned * 0) / total
```

**Depth verification (v1.1)**:
- For each "complete" feature: verify `has_io_operations=true` AND `avg_handler_loc>=20`
  - If not -> treat as partial for scoring
- For each "stub" feature: if `recency_signal=="active"` with 10+ recent changes
  - Treat as partial for scoring (actively being built)

**Bonuses**:
- +5 if has_tests_percentage > 60
- +5 if has_api_percentage > 70
- +5 if complete_chains / total_traced > 0.7 (chain bonus)
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

**Primary signal (v1.1) -- Phase 1 test runner data**:
```
if test_results.total_tests > 0:
    base = min(100, (passed / total) * 100)
    volume_bonus = min(20, total_tests / 5)
    score = min(100, base + volume_bonus)
else:
    Fall back to feature enumerator has_tests_percentage
```

**Adjustments**:
- +10 if CI/CD detected with test step
- +5 if total_test_cases > 50
- +5 if features_with_mapped_tests / total_features > 0.5

**Floor rule**: If Phase 1 shows 100+ passing tests with 90%+ pass rate, score CANNOT be below 70.

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

## Semantic Analysis Signals (v1.1)

### Implementation Depth
For each feature's handlers, the feature-enumerator reads function bodies:
- **STUB**: 0-5 meaningful LOC + placeholder returns (501, pass, throw)
- **PARTIAL**: 6-20 meaningful LOC + basic logic
- **COMPLETE**: 20+ meaningful LOC + I/O operations (DB, HTTP, file)

Key checks:
- Import/usage verification (imported != used)
- Scaffold detection (50+ LOC of type exports with no logic = stub)
- I/O operation presence (DB queries, HTTP calls, file ops)

### Integration Chains
Architecture-mapper traces 5-10 feature chains:
```
entry_point -> validation -> service -> data_layer -> response
```
- Complete chain: entry_point + (validation OR processing) + data_layer + response
- Broken chain: any layer stubs out or is missing

Cross-reference with feature status:
- Chain complete + feature "stub" -> override to "partial" minimum
- Chain broken + feature "complete" -> downgrade to "partial"

### Recency Signals
From git log (last 30 days):
- `active`: File changed in last 30 days
- `stable`: Unchanged but complete
- `stale`: Unchanged and incomplete

### Test Mapping
Test files mapped to features by imports, naming conventions, descriptions.
Coverage metrics per feature: test_file_count, test_case_count, test_files[].

## Output Documents (v1.1 Split)

### Handoff Brief (Evergreen)
Stays useful for months. Contains:
- Quick start, navigation, purpose, architecture, feature map
- Key decisions, integration points, conventions

### Gap Analysis (Time-Sensitive)
Goes stale in ~2 weeks. Contains:
- Current maturity score, test status
- Critical/high gaps, infrastructure status
- Feature completion with depth/recency/chain signals
- Recommendations

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
