---
name: synthesis-methodology
description: |
  Cumulative intelligence synthesis methodology for the intel-briefing plugin.
  Contains incremental synthesis algorithm, consensus detection rules, conflict
  identification, delta annotation patterns, and briefing structuring guidelines.
  Load when generating or updating master briefings.
triggers:
  - "synthesis methodology"
  - "master briefing"
  - "cumulative synthesis"
  - "consensus detection"
  - "briefing generation"
  - "intelligence synthesis"
version: 1.0
author: ROK Agency
---

# Synthesis Methodology Skill

## When to Use This Skill

Load when generating master briefings, performing cumulative synthesis, or structuring intelligence reports.

## Incremental Synthesis Algorithm

The key scalability insight: don't re-process all documents every time. Only process the delta.

```
1. Get last_briefing_date from most recent rok_intel_briefings entry
2. Query rok_intel_claims WHERE extraction_date > last_briefing_date
3. If no new claims -> return current briefing with "No new intelligence" note
4. Group new claims by category
5. For each category with new claims:
   a. Load previous section from last briefing
   b. Dispatch specialist agent with ONLY new claims + previous section
   c. Agent identifies what changed, what's reinforced, what's contradicted
6. Dispatch briefing-synthesizer with all updated sections
7. Store new briefing version (increment version number)
```

## Consensus Detection

A theme reaches "consensus" when:

1. **2+ documents** from **different sources** assert similar claims
2. Claims share the same **subcategory** AND same directional conclusion
3. Combined confidence (average of claim confidences x source weights) >= 0.6

Consensus format:

```json
{
  "theme": "Dollar losing reserve currency status",
  "source_count": 3,
  "sources": ["Andrei Jikh", "Ray Dalio quote", "WEF discussion"],
  "average_confidence": 0.75,
  "supporting_claims": ["claim_id_1", "claim_id_2", "claim_id_3"]
}
```

## Conflict Detection

A topic is "contested" when:

1. **2+ claims** exist with same **subcategory** but **opposite conclusions**
2. OR a validated claim has status `contradicted`

Contested format:

```json
{
  "topic": "Dollar weakness impact",
  "view_a": {
    "position": "Weaker dollar rebuilds American industry",
    "sources": ["Source 1"],
    "confidence": 0.65
  },
  "view_b": {
    "position": "Weaker dollar causes painful inflation",
    "sources": ["Source 2"],
    "confidence": 0.60
  },
  "assessment": "Both views have merit - outcome likely K-shaped with different impacts by economic segment"
}
```

## Delta Annotation

When updating sections from previous briefing:

- **NEW**: Claim/theme not in previous briefing
- **REINFORCED**: Existing theme with new supporting evidence (boost confidence)
- **REVISED**: Existing claim updated with new information
- **CONTRADICTED**: New evidence contradicts previous claim
- **EXPIRED**: Time-sensitive claim past its expiry date

## Briefing Versioning

```
Version 1: Initial briefing (all documents treated as new)
Version N+1: Incremental update (only delta processed)
```

Each version stores:
- trigger_document_id: which document triggered this update
- document_count: cumulative total
- claim_count: cumulative total
- What changed (in key_developments)

## Section Structuring Guidelines

**Executive Summary** (2-3 paragraphs):
- Lead with the single most important change since last briefing
- Second paragraph: other significant developments
- Third paragraph: overall direction and confidence level

**Financial Section**:
- Open with market regime narrative (what phase are we in)
- Sector-by-sector views with scored confidence
- Predictions table with timeframes
- Contrarian indicator callout if detected

**Geopolitical Section**:
- Open with the biggest power dynamics shift
- Regional breakdown (only regions with new activity)
- Risk matrix (probability x impact)
- Predictions table

**Labor Section**:
- Open with the most significant workforce shift since last briefing
- Sector-by-sector AI exposure views with scored confidence
- AI displacement indicators with timelines
- Predictions table
- Highlight where labor trends drive or are driven by financial/geopolitical dynamics

**Cross-Domain Themes**:
- Where financial, geopolitical, and labor dynamics intersect (they ALWAYS do)
- Example: "Dollar weakness" is both financial (market impact) AND geopolitical (power shift)
- Example: "AI automation" is financial (productivity/tech stocks) AND geopolitical (tech supremacy) AND labor (job displacement)

**Prediction Tracking**:
- Only show predictions due for review (target_date within 30 days)
- Show recent outcomes (scored in last 30 days)
- Accuracy summary by category

## Contrarian Detection

When >80% of sources agree on a prediction:

```
WARNING - CONTRARIAN INDICATOR: [N] of [M] sources predict [X].
High consensus in prediction markets often precedes reversals.
Consider: What would cause this consensus to be wrong?
```

## Quality Thresholds

| Element | Minimum Required |
|---------|-----------------|
| Claims per document | At least 3 |
| Predictions per briefing | At least 1 financial + 1 geopolitical + 1 labor |
| Consensus themes | Only include if 2+ sources |
| Contested topics | Only include if genuinely opposing views |
| Watch items | 3-5 per briefing |
