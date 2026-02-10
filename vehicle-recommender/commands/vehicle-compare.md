# Vehicle Compare — Side-by-Side Comparison

Compare 2-3 vehicles from your most recent recommendation run side-by-side. Highlights where each vehicle wins or loses based on your stated priorities.

## Usage

```
/vehicle-recommender:vehicle-compare Toyota RAV4 Hybrid vs Mazda CX-50
/vehicle-recommender:vehicle-compare RAV4 vs CX-50 vs Tucson
/vehicle-recommender:vehicle-compare #1 vs #2                    # Use rank numbers
/vehicle-recommender:vehicle-compare #1 vs #2 vs #3
```

## Arguments

- **vehicles** (required): 2-3 vehicle names or rank numbers separated by "vs". Can use partial names or rank numbers from the last recommendation run.

Initial request: $ARGUMENTS

## Workflow

1. **Load recommendations**: Read `/tmp/vehicle_recommendations.json`. If not found, inform the user: "No recommendations found. Run `/vehicle-recommender:recommend-vehicle` first."

2. **Parse vehicle selections**: Extract 2-3 vehicle identifiers from $ARGUMENTS. Match against the recommendations list by:
   - Rank number (e.g., "#1", "#2")
   - Exact make_model match
   - Partial name match (e.g., "RAV4" matches "Toyota RAV4 Hybrid")

   If a vehicle isn't found in the recommendations, inform the user and list available vehicles.

3. **Build comparison table**:

```
## Vehicle Comparison

### Your Priorities: [priorities from requirements_profile]

| Category | [Vehicle 1] | [Vehicle 2] | [Vehicle 3] | Winner |
|----------|-------------|-------------|-------------|--------|
| **Tier** | TOP_PICK | RECOMMENDED | CONSIDER | - |
| **Composite Score** | 91 | 83 | 72 | [V1] |
| **Fit Score** | 94 | 80 | 75 | [V1] |
| **Market Score** | 87 | 87 | 68 | Tie |
| **Year** | 2026 | 2026 | 2025 | - |
| **MSRP Range** | $35,500-$38,200 | $37,000-$41,000 | $32,000-$35,000 | [V3] |
| **Reliability** | 4.5/5 | 4/5 | 3.5/5 | [V1] |
| **TCO (5yr)** | $45,200 | $48,500 | $43,000 | [V3] |
| **Resale (3yr)** | 72% | 68% | 60% | [V1] |
| **Recommended Trim** | XLE Premium | Turbo Premium | SEL | - |

### Must-Have Check

| Must-Have | [Vehicle 1] | [Vehicle 2] | [Vehicle 3] |
|-----------|-------------|-------------|-------------|
| AWD/4WD | Standard | Standard | Available ($1,500) |
| Tech & safety | TSS 3.0 standard | i-Activsense std | SmartSense std |

### Strengths & Weaknesses

**[Vehicle 1]**
- Wins on: [categories where this vehicle scores highest]
- Loses on: [categories where this vehicle scores lowest]
- Best for: [user priorities this vehicle excels at]

**[Vehicle 2]**
- Wins on: ...
- Loses on: ...
- Best for: ...

### Verdict

Based on your priorities ([priority list]), **[Vehicle Name]** is the strongest match because [1-2 sentence reasoning].

However, **[Vehicle Name]** is worth considering if [specific trade-off scenario].

### Find Deals
- [Vehicle 1]: `/vehicle-finder:find-vehicle [finder_prompt]`
- [Vehicle 2]: `/vehicle-finder:find-vehicle [finder_prompt]`
```

4. **Highlight priority alignment**: Bold or annotate the categories that align with the user's stated priorities from the requirements profile.

## Rules

- This is a display/comparison command only. No new research.
- All data comes from `/tmp/vehicle_recommendations.json` — do not fabricate or supplement with new searches.
- The "Winner" column should only declare a winner when there's a meaningful difference, not marginal differences.
- Always include the must-have check table — this is critical for decision-making.
- The verdict must reference the user's stated priorities, not generic advice.
- If comparing a TOP_PICK against a CONSIDER, be honest about the gap but note what the lower-tier vehicle does well.
