# Deal Forecast

You are generating a weighted revenue forecast based on deal probabilities and expected close dates.

## Input

The user may provide:
- **Pipeline name** (default: all pipelines)
- **Months** (forecast horizon, default: 3)

## Process

### Step 1: Get Forecast Data

Call `get_forecast` with the specified parameters:

```
get_forecast(pipeline="general_sales", months=3)
```

### Step 2: Render Forecast

```
## Revenue Forecast — [Pipeline] ([months]-Month Outlook)

### Summary
| Metric | Value |
|--------|-------|
| Active Deals | [count] |
| Raw Pipeline Value | $[raw] |
| **Weighted Forecast** | **$[weighted]** |
| Unforecasted Deals | [count] (no close date) |

### Monthly Projections

#### [Month 1]
| Deal | Company | Value | Probability | Weighted |
|------|---------|-------|-------------|----------|
| [title] | [company] | $[value] | [prob]% | $[weighted] |
| **Total** | | **$[raw]** | | **$[weighted]** |

#### [Month 2]
...

### By Stage
| Stage | Deals | Raw Value | Weighted Value |
|-------|-------|-----------|----------------|
| lead | [n] | $[raw] | $[weighted] |
| qualified | [n] | $[raw] | $[weighted] |
| proposal | [n] | $[raw] | $[weighted] |
```

### Step 3: Provide Context

```
### Forecast Notes
- Weighted forecast applies each deal's probability to its value
- Deals without expected close dates are not included in monthly projections
- [count] deals have no close date — consider updating them for better forecasting
```

## Rules

- Always show both raw (unweighted) and weighted values
- Format dollar amounts with commas
- Note deals missing expected close dates as forecast gaps
- Default to 3-month horizon if not specified
