# Medigap Insurer Comparison

Display-only command that loads the most recent Medigap selection results from `/tmp/medigap_selection.json` and presents a side-by-side insurer comparison for the recommended plan.

## Usage

```
/medigap-selector:medigap-compare                             # Show all insurers
/medigap-selector:medigap-compare AARP vs Mutual of Omaha     # Compare specific insurers
```

## Arguments

- **Insurer names** (optional): One or more insurer names separated by "vs" to filter the comparison.

Initial request: $ARGUMENTS

## Workflow

### Step 1: Load Results

Read `/tmp/medigap_selection.json`. If the file doesn't exist or is invalid, inform the user:
```
No recent Medigap selection results found. Run /medigap-selector:select-medigap first.
```

### Step 2: Parse Arguments

If $ARGUMENTS contains insurer names (e.g., "AARP vs Mutual of Omaha"), filter the comparison to only those insurers. Match case-insensitively and partially (e.g., "AARP" matches "AARP/UnitedHealthcare").

### Step 3: Display Comparison

Present the insurer comparison for the winning plan:

```
## Medigap Insurer Comparison: Plan [G/N] — [State] ([Zip])

**Date**: [generated_date] | **Recommended Plan**: [winner]

### Side-by-Side Comparison

| Metric | [Insurer 1] | [Insurer 2] | [Insurer 3] |
|--------|-------------|-------------|-------------|
| Monthly Premium | $[X] | $[X] | $[X] |
| Annual Premium | $[X] | $[X] | $[X] |
| AM Best Rating | [rating] | [rating] | [rating] |
| NAIC Complaint Ratio | [ratio] | [ratio] | [ratio] |
| Avg Annual Increase | [%] | [%] | [%] |
| Rating Method | [method] | [method] | [method] |
| Household Discount | [Yes/No] | [Yes/No] | [Yes/No] |

### Insurer Notes
- **[Insurer 1]**: [Why recommended / key differentiator]
- **[Insurer 2]**: [Key differentiator]
- **[Insurer 3]**: [Key differentiator]

### Key Takeaways
- Lowest premium: [Insurer] at $[X]/month
- Strongest financially: [Insurer] (AM Best [rating])
- Fewest complaints: [Insurer] (NAIC [ratio])
- Best rate stability: [Insurer] ([%]/year average increase)

### Next Steps
- Full results: `/medigap-selector:medigap-results`
- New selection: `/medigap-selector:select-medigap`
- Export to PDF/HTML: Request export
```

## Rules

- This is a display-only command. No web searches or agent dispatches.
- Only show data from the cached results file — do not fabricate or supplement.
- If specific insurers are requested but not found in results, list available insurers.
- Include both Plan G and Plan N data if the user asks for cross-plan comparison.
