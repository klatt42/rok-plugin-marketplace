# Pain Point Hierarchization Framework

## Overview

Systematizes the discovery and ranking of user pain points to identify the highest-value problems to solve. Based on the methodology used in the Facebook Marketplace opportunity analysis.

## Pain Point Discovery Sources

| Source | How to Search | Trust Weight |
|--------|--------------|--------------|
| Reddit subreddits | `site:reddit.com "[market] pain OR frustrating OR "wish there was"` | 0.7 |
| Product Hunt comments | `site:producthunt.com "[competitor]" OR "[market]" complaints` | 0.85 |
| G2/Capterra reviews | `site:g2.com "[competitor]" cons OR "doesn't have" OR "missing"` | 0.85 |
| Twitter/X threads | `site:twitter.com "[market]" frustrating OR broken OR "need a"` | 0.5 |
| Forum discussions | `"[market]" forum OR community pain OR problem` | 0.6 |
| YouTube comments | Comments on competitor tutorials or market overview videos | 0.5 |

## Pain Point Scoring Card

For each identified pain point, fill out:

```json
{
  "description": "Clear description of the pain point",
  "severity": 0-100,
  "frequency": "daily|weekly|monthly|per_transaction|occasional",
  "affected_segment": "Who experiences this (role, size, behavior)",
  "affected_percentage": "Estimated % of target market",
  "economic_impact": {
    "time_wasted": "X hours/week",
    "money_lost": "$X per occurrence",
    "opportunity_cost": "$X unrealized revenue"
  },
  "addressable": true|false|"partial",
  "existing_workarounds": "How users currently cope",
  "willingness_to_pay": "Would users pay to solve this?",
  "sources": ["URL1", "URL2"],
  "confidence": 0-100
}
```

## Severity Scale

| Severity | Description | Example |
|----------|-------------|---------|
| 90-100 | Causes financial loss or prevents core activity | Fraud causing $500+ losses per incident |
| 70-89 | Major time waste or significant frustration | 2+ hours/day on manual workarounds |
| 50-69 | Notable inconvenience, users complain regularly | Missing feature forces spreadsheet tracking |
| 30-49 | Mild annoyance, some users notice | UI clunky but functional |
| 0-29 | Minor, rarely mentioned | Cosmetic issues, edge cases |

## Frequency Multiplier

Frequency amplifies the severity impact:

| Frequency | Multiplier | Rationale |
|-----------|-----------|-----------|
| daily | 1.0x | Maximum recurring impact |
| weekly | 0.8x | Regular but not constant |
| monthly | 0.5x | Periodic but manageable |
| per-transaction | 0.7x | Depends on transaction volume |
| occasional | 0.3x | Rare enough to tolerate |

**Effective Score** = severity x frequency_multiplier

Pain points with effective score >= 50 are candidates for product features.

## Ranking Output Format

Present pain points as a ranked table:

| Rank | Pain Point | Severity | Frequency | Affected % | Addressable | Effective Score |
|------|-----------|----------|-----------|-----------|------------|-----------------|
| 1 | Buyer ghosting / fraud | 95 | per-transaction | 62% | Yes | 66.5 |
| 2 | Message chaos | 85 | daily | 95% | Yes | 85.0 |
| 3 | No analytics | 75 | weekly | 70% | Yes | 60.0 |

## Decision Logic

- **Effective score >= 70**: Strong product opportunity, prioritize
- **Effective score 50-69**: Good opportunity if competitive gap exists
- **Effective score 30-49**: Feature candidate but not standalone product
- **Effective score < 30**: Not worth pursuing independently
