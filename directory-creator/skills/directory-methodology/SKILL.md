---
name: directory-methodology
description: |
  Core methodology for niche business directory creation. Covers the
  7-step interview protocol, data source prioritization (aggregators
  over industry directories over local sources), quality scoring
  thresholds, and depth level configuration. Used by create-directory
  command and all directory agents.
triggers:
  - "directory methodology"
  - "directory quality"
  - "directory standards"
version: 1.0
author: ROK Agency
---

# Directory Creation Methodology

## Interview Protocol

The 6-question interview collects the minimum viable parameters to scope a directory build:

1. **Niche** — The business category. Maps to search terms, industry directories, and subcategories.
2. **Geography** — Determines search scope, result volume, and geographic filtering.
3. **Subcategories** — Optional specialization within the niche. Auto-detect is preferred.
4. **Target count** — Sets agent search depth and quality threshold expectations.
5. **Depth** — Controls agent count, search volume, and enrichment thoroughness.
6. **Name** — Branding for the directory. Auto-generated format: "[Geography] [Niche] [Suffix]"

## Data Source Priority

Search sources in this priority order for maximum data quality:

| Priority | Source Type | Examples | Data Quality |
|----------|-----------|----------|-------------|
| 1 | Major aggregators | Yelp, Google Maps, YellowPages | High — structured, verified |
| 2 | Review platforms | BBB, Angi, Thumbtack | High — includes ratings |
| 3 | Industry directories | Avvo (legal), Healthgrades (medical) | Medium-High — niche-specific |
| 4 | Local directories | Chamber of Commerce, local associations | Medium — may be outdated |
| 5 | Business websites | Direct WebFetch | Variable — richest details |

## Quality Scoring (0-100)

See `references/quality-rubric.md` for detailed breakdown.

**Thresholds**:
- **Verified** (>= 50): Include in all exports, displayed as confirmed
- **Needs Verification** (30-49): Include but flag, may need manual review
- **Removed** (< 30): Exclude from exports, kept in JSON for reference

## Depth Levels

| Depth | Agents | Searches | Enrichment | Time | Best For |
|-------|--------|----------|------------|------|----------|
| Quick | 0 | 8-12 | None | ~10 min | Quick scan, small area |
| Standard | 2 | 12-18 | Top 50% | ~20 min | Most directories |
| Deep | 3 | 20-30 | All + verify | ~40 min | Publication-quality |

## Reference Documents

Load these on-demand:
- `references/niche-profiles.md` — Pre-configured settings for common niches
- `references/data-fields.md` — Complete field definitions (DirectoryGenius schema)
- `references/quality-rubric.md` — Detailed scoring rubric with examples
