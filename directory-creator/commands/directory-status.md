# Directory Status

View, filter, and manage the last generated directory data.

## Usage

```
/directory-creator:directory-status                      # Show summary of last directory
/directory-creator:directory-status --filter=verified     # Show only verified listings
/directory-creator:directory-status --city=Austin         # Filter by city
/directory-creator:directory-status --category=Residential # Filter by category
/directory-creator:directory-status --min-score=70        # Show high-quality listings only
```

## Arguments

- **--filter=** (optional): Status filter — `verified`, `needs_verification`, or `all` (default: all)
- **--city=** (optional): Filter by city name (case-insensitive partial match)
- **--category=** (optional): Filter by category/subcategory (case-insensitive partial match)
- **--min-score=** (optional): Minimum quality score threshold (0-100)

Initial request: $ARGUMENTS

## Workflow

### Step 1: Load Data

Read `/tmp/directory_data.json`. If the file doesn't exist, inform the user:
```
No directory data found. Run `/directory-creator:create-directory` first to generate a directory.
```

### Step 2: Apply Filters

Parse $ARGUMENTS for filter flags. Apply all provided filters (AND logic):
1. Status filter (`--filter=`)
2. City filter (`--city=`) — case-insensitive partial match on the `city` field
3. Category filter (`--category=`) — case-insensitive partial match on the `category` field
4. Minimum score (`--min-score=`) — only listings with `quality_score >= N`

### Step 3: Display Results

Show a summary header and filtered results table:

```
## Directory: [Directory Name]

**Niche**: [niche] | **Geography**: [geography] | **Generated**: [date] | **Depth**: [depth]

### Statistics
| Metric | All | Filtered |
|--------|-----|----------|
| Total | [N] | [M] |
| Verified | [N] | [M] |
| Needs Verification | [N] | [M] |
| Avg Score | [N] | [M] |

### Active Filters
- Status: [filter or "all"]
- City: [city or "any"]
- Category: [category or "any"]
- Min Score: [score or "none"]

### Listings ([M] matching)

| # | Name | Category | City | Phone | Rating | Score | Status |
|---|------|----------|------|-------|--------|-------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

(Show up to 30 rows. If more, note: "Showing 30 of [M] matching listings. Export for full list.")
```

### Step 4: Offer Actions

After displaying results, offer available actions using AskUserQuestion:

1. **Re-export** — Regenerate CSV/Excel/PDF/HTML with current filters applied
2. **Re-enrich** — Run data-enricher on listings that have `needs_verification` status
3. **Generate landing content** — Run `/directory-creator:generate-landing-content` for this directory
4. **Clear** — Delete `/tmp/directory_data.json` and start fresh

If user selects **Re-export**:
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_dir]/scripts/directory_export.py --input /tmp/directory_data.json
```

If user selects **Re-enrich**: Dispatch the data-enricher agent with the `needs_verification` businesses.

If user selects **Generate landing content**: Invoke `/directory-creator:generate-landing-content`.

If user selects **Clear**: Delete `/tmp/directory_data.json` and confirm deletion.

## Rules

- This command is read-only by default. Only modify data if user explicitly requests re-enrich.
- Show the full phone number in the table (don't mask it).
- Sort results by quality_score descending by default.
- If no filters match any listings, show "No listings match your filters" with the current filter values.
