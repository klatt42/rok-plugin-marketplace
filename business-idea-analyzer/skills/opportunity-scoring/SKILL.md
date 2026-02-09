---
name: opportunity-scoring
description: |
  Business opportunity scoring methodology for the business-idea-analyzer plugin.
  Contains composite score formula, dimension weights, verdict determination,
  solopreneur feasibility assessment, and confidence scoring guidelines. Load
  on-demand when detailed scoring context is needed during analysis orchestration.
triggers:
  - "opportunity scoring"
  - "business scoring"
  - "idea scoring"
  - "TAM calculation"
  - "solopreneur assessment"
  - "business verdict"
version: 1.0
author: ROK Agency
---

# Opportunity Scoring Methodology

## Composite Score Formula

Weighted score across 5 dimensions with risk penalties and solopreneur bonus:

```
weighted_score = (
  market_demand * 0.25 +
  competitive_landscape * 0.20 +
  financial_viability * 0.20 +
  execution_feasibility * 0.20 +
  risk_assessment * 0.15
)

risk_penalty = (critical_kill_criteria_count * 15) + (high_risk_count * 5)
solo_bonus = 5 if (execution.solopreneur_viable == true AND market_demand >= 70)

final_score = max(0, min(100, round(weighted_score - risk_penalty + solo_bonus)))
```

## Dimension Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Market Demand | 25% | No market = no business, highest weight |
| Competitive Landscape | 20% | Must have differentiation to survive |
| Financial Viability | 20% | Must generate revenue |
| Execution Feasibility | 20% | Solopreneur must be able to build it |
| Risk Assessment | 15% | Important but partially controllable |

## Verdict Determination

| Score Range | Kill Criteria | Verdict | Badge Color | Recommended Action |
|-------------|---------------|---------|-------------|-------------------|
| >= 80 | 0 critical | STRONG_GO | Green #059669 | Proceed to /idea-deep-dive |
| 65-79 | 0 critical | GO | Teal #0D9488 | Proceed with caution, validate key assumptions |
| 50-64 | 0 critical | CONDITIONAL | Amber #D97706 | Run /idea-validate first |
| < 50 | any | NO_GO | Red #DC2626 | Redirect effort elsewhere |
| any | >= 1 critical | BLOCKED | Red #DC2626 | Must resolve kill criteria before proceeding |

## Confidence Scoring

All findings scored 0-100 for confidence:

| Range | Meaning | Action |
|-------|---------|--------|
| 0-49 | Low confidence, likely noise | Discard |
| 50-69 | Moderate, may be real | Discard (below threshold) |
| 70-84 | Good confidence, likely real | Include in report |
| 85-100 | High confidence, well-sourced | Include with emphasis |

**Threshold**: Only findings with confidence >= 70 appear in the final report. This is lower than the code-review plugin's 80 threshold because market research is inherently less precise than code analysis.

## Solopreneur Assessment Criteria

A business idea is classified as **solopreneur-viable** when:
- MVP can be built in <= 8 weeks by one developer
- Tech stack uses familiar, well-documented frameworks (Next.js, Supabase, Tailwind, etc.)
- No critical platform dependencies that require enterprise partnerships
- Ongoing maintenance <= 10 hours/week
- No regulatory compliance requiring legal team
- Customer support can be handled with documentation + email

## Source Trust Hierarchy

| Source Type | Trust Weight | Examples |
|-------------|-------------|----------|
| Official platform data | 1.0 | API docs, official statistics, SEC filings |
| Industry reports | 0.9 | Statista, Gartner, IBISWorld |
| Product review aggregators | 0.85 | G2, Capterra, Product Hunt, TrustRadius |
| Expert commentary | 0.8 | YC partners, established founders, industry analysts |
| Community discussion (high engagement) | 0.7 | Reddit threads with 50+ upvotes, HN front page |
| General web sources | 0.6 | Blog posts, news articles |
| Community discussion (low engagement) | 0.5 | Small forum threads, low-vote Reddit posts |
| Single anecdotal sources | 0.4 | Individual tweets, single user complaints |
