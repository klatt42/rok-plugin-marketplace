# Camper Compare — Side-by-Side Comparison

Compare 2-3 campers/RVs from your most recent recommendation run side-by-side. Highlights where each camper wins or loses based on your stated priorities.

## Usage

```
/camper-recommender:camper-compare Grand Design Imagine vs Jayco Jay Flight
/camper-recommender:camper-compare Imagine vs Jay Flight vs Rockwood
/camper-recommender:camper-compare #1 vs #2                    # Use rank numbers
/camper-recommender:camper-compare #1 vs #2 vs #3
```

## Arguments

- **campers** (required): 2-3 camper names or rank numbers separated by "vs". Can use partial names or rank numbers from the last recommendation run.

Initial request: $ARGUMENTS

## Workflow

1. **Load recommendations**: Read `/tmp/camper_recommendations.json`. If not found, inform the user: "No recommendations found. Run `/camper-recommender:recommend-camper` first."

2. **Parse camper selections**: Extract 2-3 camper identifiers from $ARGUMENTS. Match against the recommendations list by:
   - Rank number (e.g., "#1", "#2")
   - Exact make_model match
   - Partial name match (e.g., "Imagine" matches "Grand Design Imagine")

   If a camper isn't found in the recommendations, inform the user and list available campers.

3. **Build comparison table**:

```
## Camper/RV Comparison

### Your Priorities: [priorities from requirements_profile]

| Category | [Camper 1] | [Camper 2] | [Camper 3] | Winner |
|----------|------------|------------|------------|--------|
| **Tier** | TOP_PICK | RECOMMENDED | CONSIDER | - |
| **Composite Score** | 88 | 79 | 68 | [C1] |
| **Fit Score** | 91 | 82 | 72 | [C1] |
| **Market Score** | 84 | 75 | 63 | [C1] |
| **Year** | 2025 | 2025 | 2024 | - |
| **MSRP Range** | $42,000-$48,000 | $35,000-$40,000 | $28,000-$33,000 | [C3] |
| **Build Quality** | Above Average | Average | Below Average | [C1] |
| **TCO (5yr)** | $52,000 | $48,000 | $44,000 | [C3] |
| **Resale (3yr)** | 65% | 58% | 50% | [C1] |
| **Length** | 29.6 ft | 26.5 ft | 24 ft | - |
| **Dry Weight** | 5,800 lbs | 4,900 lbs | 4,200 lbs | [C3] |
| **GVWR** | 7,600 lbs | 6,500 lbs | 5,800 lbs | - |
| **Slides** | 1 | 1 | 0 | - |
| **Sleeping Capacity** | 4 | 6 | 4 | [C2] |
| **Fresh Water** | 48 gal | 40 gal | 30 gal | [C1] |

### Must-Have Check

| Must-Have | [Camper 1] | [Camper 2] | [Camper 3] |
|-----------|------------|------------|------------|
| Slide-out(s) | 1 slide (standard) | 1 slide (standard) | None |
| Full bathroom | Full dry bath | Full dry bath | Wet bath only |

### Tow Vehicle Compatibility

| Spec | [Camper 1] | [Camper 2] | [Camper 3] | Your Truck |
|------|------------|------------|------------|------------|
| GVWR | 7,600 lbs | 6,500 lbs | 5,800 lbs | [max tow] |
| Hitch Weight | 680 lbs | 580 lbs | 490 lbs | [max payload] |
| Margin | XX% | XX% | XX% | - |

### Strengths & Weaknesses

**[Camper 1]**
- Wins on: [categories where this camper scores highest]
- Loses on: [categories where this camper scores lowest]
- Best for: [user priorities this camper excels at]

**[Camper 2]**
- Wins on: ...
- Loses on: ...
- Best for: ...

### Verdict

Based on your priorities ([priority list]), **[Camper Name]** is the strongest match because [1-2 sentence reasoning].

However, **[Camper Name]** is worth considering if [specific trade-off scenario].

### Find Deals
- [Camper 1]: `/camper-finder:find-camper [finder_prompt]`
- [Camper 2]: `/camper-finder:find-camper [finder_prompt]`
```

4. **Highlight priority alignment**: Bold or annotate the categories that align with the user's stated priorities from the requirements profile.

## Rules

- This is a display/comparison command only. No new research.
- All data comes from `/tmp/camper_recommendations.json` — do not fabricate or supplement with new searches.
- The "Winner" column should only declare a winner when there's a meaningful difference, not marginal differences.
- Always include the must-have check table — this is critical for decision-making.
- Always include the tow vehicle compatibility table if a tow vehicle was specified.
- The verdict must reference the user's stated priorities, not generic advice.
- If comparing a TOP_PICK against a CONSIDER, be honest about the gap but note what the lower-tier camper does well.
- Weight and towing compatibility are safety-critical — always highlight if any camper is close to or exceeds tow vehicle limits.
