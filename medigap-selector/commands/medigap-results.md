# Medigap Results

Display-only command that loads and redisplays the most recent Medigap plan selection results from `/tmp/medigap_selection.json`.

## Usage

```
/medigap-selector:medigap-results
```

Initial request: $ARGUMENTS

## Workflow

### Step 1: Load Results

Read `/tmp/medigap_selection.json`. If the file doesn't exist or is invalid, inform the user:
```
No recent Medigap selection results found. Run /medigap-selector:select-medigap first.
```

### Step 2: Display Full Results

Present the complete results in the same format as the select-medigap command's Phase 6 output:

```
## Medigap Plan Selection: [State] ([Zip])

**Date**: [generated_date] | **Age**: [age] | **Usage**: [usage level]

### Your Profile
- Location: [state] ([zip]) | Age: [age] ([enrollment status])
- Usage: [medical_usage] (~[visits] visits/year)
- Priorities: [priorities joined]
- Provider Assignment: [assignment status]

### Recommendation

**Winner: Plan [G/N]** — Suitability Score: [score]/100 (Confidence: [HIGH/MEDIUM/LOW])

> [one_line_summary]

| Factor | Plan G | Plan N |
|--------|--------|--------|
| Cost Efficiency (30%) | [score] | [score] |
| Risk Protection (25%) | [score] | [score] |
| Flexibility (20%) | [score] | [score] |
| Priority Alignment (15%) | [score] | [score] |
| Insurer Quality (10%) | [score] | [score] |
| **Composite** | **[G score]** | **[N score]** |

### Premium Comparison

| Insurer | Plan G | Plan N | Spread | AM Best | NAIC |
|---------|--------|--------|--------|---------|------|
| [insurer] | $[G]/mo | $[N]/mo | $[diff] | [rating] | [ratio] |

### Break-Even Analysis
- Monthly premium spread: $[spread]
- Office visits to break even: [N] visits/year
- Your estimated visits: [N]/year
- Excess charge risk: [level]

### Scenario Comparison

| Scenario | Plan G | Plan N | Winner | Savings |
|----------|--------|--------|--------|---------|
| Healthy Year | $[cost] | $[cost] | [winner] | $[amount] |
| Typical Year | $[cost] | $[cost] | [winner] | $[amount] |
| Bad Year | $[cost] | $[cost] | [winner] | $[amount] |
| Worst Case | $[cost] | $[cost] | [winner] | $[amount] |

### State Rules: [State]
- Birthday Rule: [Yes/No] — [explanation]
- Switching Strategy: [recommendation]

### Top Insurer Recommendation
**#1: [Insurer Name]** — $[premium]/month ([Plan])

### Strategic Advice
1. [Advice item 1]
2. [Advice item 2]
3. [Advice item 3]

### Next Steps
- Compare insurers: `/medigap-selector:medigap-compare`
- New selection: `/medigap-selector:select-medigap`
- Export to PDF/HTML: Request export

> **Disclaimer**: This is not financial or medical advice. Consult with a licensed insurance agent or Medicare counselor.
```

### Step 3: Offer Export

After displaying results, offer:
```
Want me to export these results to PDF/HTML? I can generate files to:
/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Medigap_Selection/
```

## Rules

- This is a display-only command. No web searches or agent dispatches.
- Reproduce the data exactly as stored in the JSON — do not modify or supplement.
- Always include the disclaimer about not being financial/medical advice.
- If the JSON is malformed, report the error and suggest re-running select-medigap.
