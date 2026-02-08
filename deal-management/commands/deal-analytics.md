# Deal Analytics

You are analyzing pipeline health: win rates, cycle times, stage velocity, bottlenecks, and value metrics.

## Input

The user may provide:
- **Pipeline name** (default: all pipelines)
- **Period** (7d, 30d, 90d, all — default: 30d)

## Process

### Step 1: Get Analytics Data

Call `get_analytics` with the specified parameters:

```
get_analytics(pipeline="general_sales", period="30d")
```

### Step 2: Render Analytics Dashboard

```
## Pipeline Analytics — [Pipeline] ([Period])

### Performance Summary
| Metric | Value |
|--------|-------|
| Total Deals | [total] |
| Active | [active] |
| Won | [won] |
| Lost | [lost] |
| Stalled | [stalled] |
| **Win Rate** | **[rate]%** |

### Value Metrics
| Metric | Value |
|--------|-------|
| Active Pipeline Value | $[value] |
| Won Revenue | $[won_value] |
| Average Deal Size | $[avg] |

### Stage Distribution
| Stage | Deals | Value | Bottleneck? |
|-------|-------|-------|-------------|
| [stage] | [count] | $[value] | [Yes/No] |

### Velocity
- **Average Cycle Time**: [days] days (lead to close)
- **Stage Velocity**:
  - lead: [days] days avg
  - qualified: [days] days avg
  - proposal: [days] days avg
  - negotiation: [days] days avg

### Stalled Deals (14+ days no activity)
| Deal | Company | Stage | Value | Days Stale |
|------|---------|-------|-------|------------|
| [title] | [company] | [stage] | $[value] | [days] |
```

### Step 3: Provide Recommendations

Based on the data, suggest:
- Stages with unusually high deal counts (bottlenecks)
- Deals that need attention (stalled)
- Win rate trends (if data allows)
- Pipeline coverage ratio (active value vs. targets)

## Rules

- Default to 30d period if not specified
- Flag bottleneck stages (disproportionate deal count vs. neighbors)
- Highlight stalled deals that need attention
- Format all dollar values with commas
- Show "Insufficient data" for metrics that can't be calculated
