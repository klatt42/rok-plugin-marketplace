# Camper List — Recall Last Results

Recall and display the most recent camper/RV recommendation results. No new research — display only.

## Usage

```
/camper-recommender:camper-list                        # Show full last recommendation list
/camper-recommender:camper-list --tier=TOP_PICK        # Filter to TOP_PICK tier only
/camper-recommender:camper-list --tier=RECOMMENDED     # Filter to RECOMMENDED tier
```

## Arguments

- **--tier** (optional): Filter by tier — `TOP_PICK`, `RECOMMENDED`, `CONSIDER`, `PASS`

Initial request: $ARGUMENTS

## Workflow

1. **Load recommendations**: Read `/tmp/camper_recommendations.json`. If not found, inform the user: "No recommendations found. Run `/camper-recommender:recommend-camper` first."

2. **Apply filters**: If `--tier` flag is provided, filter the recommendations to only show campers matching that tier.

3. **Display**:
   - Show the requirements profile summary
   - Show the filtered recommendation table (same format as recommend-camper output)
   - Show detail for top 3 in the filtered set
   - Include the `finder_prompt` for each so the user can copy-paste

4. **Offer actions**:
```
### Actions
- Compare campers: `/camper-recommender:camper-compare [Camper1] vs [Camper2]`
- Find inventory: `/camper-finder:find-camper [finder_prompt]`
- Search from recommendations: `/camper-finder:find-camper --from-recommendations`
- Re-run with different requirements: `/camper-recommender:recommend-camper`
- Export to PDF/HTML/MD: Request export
```

## Rules

- This is a display/filter command only. No new research.
- If the recommendations JSON is missing or corrupt, suggest re-running the recommender.
- Preserve the original scores — do not re-score on recall.
- Always show the requirements profile so the user remembers what they asked for.
