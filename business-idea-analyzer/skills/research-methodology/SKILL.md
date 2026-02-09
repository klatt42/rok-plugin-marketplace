---
name: research-methodology
description: |
  Multi-source research pipeline for business idea analysis. Defines source
  hierarchy with trust weighting, WebSearch query construction patterns,
  pain point hierarchization framework, competitive gap analysis methodology,
  and assumption validation gates. Systematizes the research templates from
  the Facebook Marketplace opportunity analysis workflow.
triggers:
  - "business research"
  - "market research"
  - "competitive analysis"
  - "pain point analysis"
  - "assumption validation"
  - "kill criteria"
  - "demand signals"
version: 1.0
author: ROK Agency
---

# Research Methodology

## Depth Levels

| Depth | Duration | Agents | Queries/Agent | Token Budget | Export |
|-------|----------|--------|---------------|-------------|--------|
| quick | 5-10 min | 0 (direct WebSearch) | 5-8 total | ~12K | Chat summary only |
| standard | 15-30 min | 5 parallel | 6-10 each | ~70K | MD + PDF + HTML |
| deep | 45-60 min | 5 parallel | 10-15 each | ~120K | Full report + auto deep-dive |

## WebSearch Query Patterns

### Demand Discovery
```
"[idea keywords]" site:reddit.com pain OR frustrating OR "wish there was"
"[idea keywords]" site:reddit.com tool OR app OR "I use" OR "I need"
"[target market]" "how do you" OR "what tool" OR "best way to"
"[idea keywords]" review OR alternative OR "looking for"
```

### Market Sizing
```
"[market]" "market size" OR "TAM" OR "billion" OR "million users"
"[market]" report OR statistics OR "industry report" 2025 OR 2026
"[platform]" "monthly active users" OR "active sellers" OR "active users"
```

### Competitive Discovery
```
"[idea keywords]" tool OR software OR platform OR SaaS
"[idea keywords]" alternative OR "instead of" OR "better than" OR "vs"
"[competitor name]" pricing OR plans OR "how much"
"[competitor name]" site:g2.com OR site:capterra.com OR site:producthunt.com
"[competitor name]" review OR complaints OR "doesn't have" OR "missing"
```

### Risk Research
```
"[platform]" API OR "terms of service" OR "developer policy" changes
"[market]" "shut down" OR "failed" OR "pivoted" OR "lessons learned"
"[idea keywords]" regulation OR compliance OR legal OR "cease and desist"
```

## Pain Point Hierarchization

For each pain point discovered:

| Step | Action | Output |
|------|--------|--------|
| 1 | Identify pain point from user research | Description |
| 2 | Score severity (0-100) | How painful is this? |
| 3 | Score frequency | daily / weekly / monthly / per-transaction |
| 4 | Segment affected users | What % of target market experiences this? |
| 5 | Calculate economic impact | $X hours/week x $Y/hour x Z% of users |
| 6 | Validate addressability | Can software solve this? Yes / No / Partial |

Pain points scoring >= 70 severity with daily/weekly frequency and > 30% affected segment are **high-priority targets**.

## Competitive Gap Analysis Template

```
Step 1: List all competitors (direct + indirect + adjacent)
Step 2: Create feature matrix (capabilities across competitors)
Step 3: Identify "your market" column (often blank = gap)
Step 4: Score each competitor's depth (surface / moderate / deep)
Step 5: Note price points and value propositions
Step 6: Highlight YOUR unique differentiation opportunity
Step 7: Assess market maturity (nascent / growing / mature / saturated)
```

## Approval Gate Protocol

### Gate 1: After Idea Scoping (before agent dispatch)
Present to user:
- Idea Context Brief (category, target market, scope, operator profile)
- 3-5 initial signals from discovery searches
- Confirm depth level before launching expensive parallel agents

### Gate 2: After Ranking (before export, standard/deep only)
Present to user:
- Ranked opportunities table (3-5 rows with scores and verdicts)
- Options: export all, deep-dive specific opportunity, validate assumptions, adjust scope

## Research Quality Indicators

Report these metrics in every analysis:
- `sources_consulted`: Total unique sources referenced
- `web_searches_performed`: Number of WebSearch queries executed
- `confidence_threshold`: The minimum confidence for included findings (70)
- `agents_dispatched`: Number of parallel analysis agents used
- `data_freshness`: Most recent source date found
