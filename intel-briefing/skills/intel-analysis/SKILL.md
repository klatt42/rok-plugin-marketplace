---
name: intel-analysis
description: |
  Core intelligence analysis methodology for the intel-briefing plugin. Contains
  claim extraction patterns, category taxonomy, confidence scoring rubrics,
  source reliability weighting, and document classification rules. Load when
  processing documents or reviewing claim extraction quality.
triggers:
  - "intel analysis"
  - "claim extraction"
  - "document analysis"
  - "confidence scoring"
  - "source reliability"
  - "intel methodology"
version: 1.0
author: ROK Agency
---

# Intel Analysis Skill

## When to Use This Skill

Load when performing document analysis, reviewing claim quality, or calibrating confidence scores.

## Document Classification

| Type | Signals | Analysis Focus |
|------|---------|---------------|
| `news` | Recent events, dates, "just announced" | Facts, timeline, implications |
| `analysis` | "I think", data interpretation, frameworks | Thesis, evidence, counterpoints |
| `opinion` | "I believe", personal views, speculation | Author position, bias indicators |
| `report` | Data-heavy, structured, institutional | Key findings, methodology, data quality |
| `tutorial` | "How to", step-by-step, instructions | Actionable steps, tools, dependencies |
| `discussion` | Multiple speakers, Q&A, debate | Each position, areas of agreement/disagreement |

## Category Taxonomy

| Category | Subcategories | Example Claims |
|----------|--------------|----------------|
| `financial` | dollar-policy, gold-silver, crypto, equities, bonds, commodities, monetary-policy, fed-policy, inflation, interest-rates | "Gold has overtaken treasuries in CB reserves" |
| `geopolitical` | us-hegemony, china-trade, russia-relations, middle-east, monroe-doctrine, brics, sanctions, alliances | "US moved into Venezuela to prevent China foothold" |
| `technology` | ai-impact, automation, digital-currency, surveillance | "AI will freeze economic mobility within 5 years" |
| `economic` | k-shaped-economy, keynesian, austrian, debt-cycle, trade-deficit | "The debt-based system requires constant expansion" |
| `market` | stock-market, real-estate, commodity-prices | "Markets priced in dollars mask real value loss" |
| `policy` | trade-policy, tariffs, regulation, fiscal-policy | "Weaker dollar policy deliberate to rebuild industry" |
| `military` | military-industrial, power-projection, choke-points | "Strait of Hormuz control is strategic priority" |
| `social` | wealth-inequality, economic-mobility, labor-market | "Top 10% account for half of consumer spending" |
| `labor` | ai-displacement, automation-impact, workforce-participation, wage-dynamics, skills-gap, remote-work, gig-economy, labor-shortage, union-activity, employment-trends | "AI will displace 40% of knowledge workers within 5 years" |
| `energy` | oil-reserves, energy-independence, critical-minerals | "US is 100% import reliant for 12 critical minerals" |

## Confidence Scoring Rubric

| Score Range | Label | Criteria |
|-------------|-------|----------|
| 0.85-1.00 | Very High | Author states as established fact with data/citation; matches known reality |
| 0.70-0.84 | High | Author states confidently; reasonable evidence provided |
| 0.50-0.69 | Medium | Author presents as likely; some evidence but caveats exist |
| 0.30-0.49 | Low | Author speculates or presents as possibility; limited evidence |
| 0.10-0.29 | Very Low | Pure speculation, future unknowns, author explicitly uncertain |

## Claim Type Classification

| Type | Definition | Example |
|------|-----------|---------|
| `fact` | Verifiable assertion about current/past state | "Venezuela has 300B barrels of oil reserves" |
| `prediction` | Forward-looking forecast | "Iran will be the next target" |
| `analysis` | Interpretation of facts | "Dollar weakness signals industrial rebuilding" |
| `opinion` | Personal view, value judgment | "Bitcoin is a way to opt-out of the system" |
| `recommendation` | Explicit advice to audience | "Own productive assets before AI freezes mobility" |

## Source Reliability Weighting

| Trust Tier | Weight | Criteria |
|-----------|--------|----------|
| HIGH | 0.85-1.0 | Domain authority, track record, institutional backing |
| MEDIUM | 0.55-0.75 | Known expert, generally reliable but occasional errors |
| STANDARD | 0.25-0.45 | Unknown source, first-time analysis, no track record |
| LOW | 0.10-0.20 | Known bias, poor track record, tabloid-quality |

**Composite confidence formula:**

```
effective_confidence = claim_confidence x source_trust_weight x validation_score
```

## Deduplication Rules

1. Same claim, same conclusion from multiple sources -- Merge, cite all sources, boost confidence
2. Same topic, different perspectives -- Keep both as separate claims
3. Contradictory claims -- Keep both, flag as contested
4. Time-sensitive claims with newer data -- Supersede older claim (set superseded_by)
