# Move Stage

You are moving a deal to a different stage within its pipeline. Validate the stage exists and show the before/after state.

## Input

The user will provide:
- **Deal ID** or deal title/company to identify the deal
- **Target stage** name (e.g., "qualified", "proposal", "negotiation")
- **Notes** (optional) about why the deal is moving

## Process

### Step 1: Identify the Deal

If the user provides an ID, use it directly. If they provide a name or company, use `search_deals` to find the matching deal and confirm with the user if multiple matches.

### Step 2: Show Current State

Call `get_deal` to show the current stage and recent history:

```
## Deal #[id]: [title]
- **Current Stage**: [stage]
- **Pipeline**: [pipeline]
- **Value**: $[value]
- **Last Activity**: [date]
```

### Step 3: Move the Deal

Call `move_stage` with the deal ID, target stage, and any notes:

```
move_stage(deal_id=[id], to_stage="[stage]", notes="[notes]")
```

### Step 4: Confirm Move

```
## Stage Updated

**[title]**
[from_stage] --> [to_stage]

Notes: [notes]

### Pipeline Progress
[visual representation of stages with current position marked]
lead > qualified > proposal > **negotiation** > closed
```

## Rules

- If the target stage doesn't exist, show available stages from the error response
- Always show before and after states
- Include a visual pipeline progress indicator
- Suggest recording an outcome if moving to the final stage
