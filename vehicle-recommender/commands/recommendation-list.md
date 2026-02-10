# Recommendation List — Recall Last Results

Recall and display the most recent vehicle recommendation results. No new research — display only.

## Usage

```
/vehicle-recommender:recommendation-list                        # Show full last recommendation list
/vehicle-recommender:recommendation-list --tier=TOP_PICK        # Filter to TOP_PICK tier only
/vehicle-recommender:recommendation-list --tier=RECOMMENDED     # Filter to RECOMMENDED tier
```

## Arguments

- **--tier** (optional): Filter by tier — `TOP_PICK`, `RECOMMENDED`, `CONSIDER`, `PASS`

Initial request: $ARGUMENTS

## Workflow

1. **Load recommendations**: Read `/tmp/vehicle_recommendations.json`. If not found, inform the user: "No recommendations found. Run `/vehicle-recommender:recommend-vehicle` first."

2. **Apply filters**: If `--tier` flag is provided, filter the recommendations to only show vehicles matching that tier.

3. **Display**:
   - Show the requirements profile summary
   - Show the filtered recommendation table (same format as recommend-vehicle output)
   - Show detail for top 3 in the filtered set
   - Include the `finder_prompt` for each so the user can copy-paste

4. **Offer actions**:
```
### Actions
- Compare vehicles: `/vehicle-recommender:vehicle-compare [Vehicle1] vs [Vehicle2]`
- Find inventory: Copy a finder_prompt above for the future `/vehicle-finder` plugin
- Re-run with different requirements: `/vehicle-recommender:recommend-vehicle`
- Export to PDF/HTML/MD: Request export
```

## Rules

- This is a display/filter command only. No new research.
- If the recommendations JSON is missing or corrupt, suggest re-running the recommender.
- Preserve the original scores — do not re-score on recall.
- Always show the requirements profile so the user remembers what they asked for.
