# Campaign Dashboard

You are presenting an overview of all campaigns with their status, funnel metrics, and actionable flags.

## Input

The user may provide:
- **Channel filter** (email, sms, linkedin, or all — default: all)
- **Status filter** (draft, active, paused, completed — default: all)

## Process

### Step 1: Get Campaign Data

Use `get_campaign_analytics` for the aggregate view, then `get_campaign` for individual campaigns that need detail.

```
get_campaign_analytics(channel="email", period="all")
```

### Step 2: Render Dashboard

```
## Campaign Dashboard

### Overview
| Metric | Value |
|--------|-------|
| Total Campaigns | [count] |
| Total Messages | [count] |
| Sent | [sent] |
| Response Rate | [rate]% |
| Conversion Rate | [rate]% |

### Campaigns
| # | Campaign | Channel | Status | Sent | Opened | Responded | Converted |
|---|----------|---------|--------|------|--------|-----------|-----------|
| 1 | [name]   | email   | active | 45   | 28     | 12        | 5         |

### Funnel
Sent → Delivered → Opened → Responded → Converted
[count] → [count] → [count] → [count] → [count]
([rate]%) → ([rate]%) → ([rate]%) → ([rate]%)

### Flags
- [Campaign X]: High bounce rate (15%) — check contact list quality
- [Campaign Y]: 0 responses — review template or subject line
```

### Step 3: Recommendations

Based on the data, suggest:
- Campaigns with low open rates (subject line issues)
- Campaigns with low response rates (body/CTA issues)
- High bounce rates (list quality issues)
- Campaigns stuck in draft status

## Rules

- Show all campaigns in a single table for quick scanning
- Flag any campaign with bounce rate > 5%
- Flag any campaign with 0 responses after 10+ sends
- Format rates as percentages with 1 decimal
- Group by status (active first, then draft, paused, completed)
