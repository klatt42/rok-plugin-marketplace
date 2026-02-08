# Create Deal

You are adding a new deal to a pipeline. Gather the required information and create the deal using the MCP tool.

## Input

The user will provide some or all of:
- **Pipeline**: Which pipeline (general_sales, partnership, insurance_claim, or custom)
- **Title**: Deal name/description
- **Company**: Company or organization
- **Contact**: Primary contact person
- **Value**: Dollar amount
- **Probability**: Win probability (0-100%)
- **Expected close**: Target close date
- **Source**: Where the lead came from

## Process

### Step 1: Gather Information

If the user hasn't provided all key fields, prompt for:
1. Pipeline (suggest `general_sales` if unclear)
2. Title (required)
3. Company name
4. Estimated value

Don't require every field — create with what's available.

### Step 2: Create the Deal

Call the `create_deal` MCP tool with the gathered information:

```
create_deal(
  pipeline="general_sales",
  title="...",
  company="...",
  contact="...",
  value=...,
  probability=...,
  expected_close="YYYY-MM-DD",
  source="...",
  notes="..."
)
```

### Step 3: Confirm Creation

Present the result:

```
## Deal Created

- **ID**: #[id]
- **Title**: [title]
- **Pipeline**: [pipeline] > [stage]
- **Company**: [company]
- **Value**: $[value]
- **Probability**: [probability]%

### Next Steps
- Move to next stage: `/deal-management:move-stage [id] [stage]`
- View pipeline: `/deal-management:pipeline-view [pipeline]`
- Add notes: Use `add_deal_note` tool
```

## Rules

- Default pipeline is `general_sales` unless the user specifies otherwise
- Default probability is 50% unless stated
- Always confirm the deal was created with its ID
- Suggest relevant next steps based on the pipeline
