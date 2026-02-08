# Pipeline View

You are displaying a visual pipeline board showing all deals grouped by stage with counts and values.

## Input

The user may provide:
- **Pipeline name** (default: general_sales)
- **Status filter** (active, won, lost, stalled — default: active)

## Process

### Step 1: Get Pipeline Data

Call `get_pipeline` with the specified pipeline and optional status filter:

```
get_pipeline(pipeline="general_sales", status_filter="active")
```

### Step 2: Render Pipeline Board

Display an ASCII Kanban-style board:

```
## [Pipeline Name] Pipeline

Total Deals: [count] | Pipeline Value: $[total] | Weighted: $[weighted]

### [Stage 1: Lead] (3 deals | $45,000)
  1. [Deal Title] — [Company] — $15,000 (60%)
  2. [Deal Title] — [Company] — $20,000 (40%)
  3. [Deal Title] — [Company] — $10,000 (30%)

### [Stage 2: Qualified] (2 deals | $80,000)
  4. [Deal Title] — [Company] — $50,000 (70%)
  5. [Deal Title] — [Company] — $30,000 (65%)

### [Stage 3: Proposal] (1 deal | $120,000)
  6. [Deal Title] — [Company] — $120,000 (80%)

### [Stage 4: Negotiation] (0 deals | $0)
  (empty)

### [Stage 5: Closed] (0 deals | $0)
  (empty)
```

### Step 3: Highlight Key Insights

```
### Quick Insights
- **Heaviest Stage**: [stage] with [count] deals
- **Largest Deal**: [title] at $[value]
- **Closest to Close**: [title] — [expected_close]
- **Stalled**: [count] deals with no activity in 14+ days
```

### Step 4: Suggest Actions

```
### Actions
- Create deal: `/deal-management:create-deal`
- Move a deal: `/deal-management:move-stage [id] [stage]`
- Analytics: `/deal-management:deal-analytics [pipeline]`
- Forecast: `/deal-management:deal-forecast [pipeline]`
```

## Rules

- Default to `general_sales` pipeline if none specified
- Default to `active` status filter
- Show dollar values formatted with commas
- Empty stages should show "(empty)" not be hidden
- Sort deals within each stage by value descending
