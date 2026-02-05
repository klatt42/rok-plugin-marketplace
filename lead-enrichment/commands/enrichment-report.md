# Enrichment Report

You are generating a detailed single-company enrichment report for Prism Specialties DMV. This is a deeper analysis than `/enrich-lead` — it includes competitive positioning, technology analysis, financial signals, and a recommended approach with talking points.

## Input

The user will provide:
- **Company name** (required) — if not provided, ask for it
- **Depth level** (optional) — `standard` (default) or `deep`

## Process

### Step 1: Full Company Research

Execute all four tiers from the company-research skill, with expanded searches:

**Tier 1 — Identity** (standard searches)
**Tier 2 — Business Intel** (standard searches + additional):
- `"[company]" "revenue" OR "million" OR "annual" OR "growth"` — financial signals
- `"[company]" "technology" OR "software" OR "platform" OR "app"` — tech stack
- `"[company]" "acquisition" OR "merger" OR "partnership"` — strategic moves

**Tier 3 — Engagement Signals** (standard searches + additional):
- `"[company]" "complaint" OR "lawsuit" OR "violation"` — risk signals
- `"[company]" site:reddit.com OR site:glassdoor.com` — employee sentiment
- `"[company]" "expanding" OR "new office" OR "new location"` — expansion signals

**Tier 4 — Relationship Context** (standard + competitive analysis):
- `"[company]" vs OR versus OR competitor OR alternative` — competitive landscape
- `"[company]" "partner" OR "subcontractor" OR "referral"` — partnership signals

### Step 2: Competitive Positioning

Analyze how this company compares to Prism Specialties DMV:

| Dimension | [Company] | Prism DMV |
|-----------|-----------|-----------|
| Services | ... | Contents, electronics, art, textile, pack-out |
| Territory | ... | DC, MD, VA |
| Certifications | ... | IICRC certified |
| Insurance Focus | ... | Carrier relationships |
| Size | ... | ... |
| Specialty | ... | Contents restoration specialist |

Determine relationship type:
- **Potential Partner**: Complementary services, shared territory
- **Competitor**: Overlapping services, same carriers
- **Referral Source**: Different specialty, could refer contents work
- **Vendor**: Provides services Prism needs (supplies, equipment, etc.)

### Step 3: Contact Discovery & Validation

Follow the same contact discovery and validation process as `/enrich-lead` Steps 2-4, including the APPROVAL GATE.

### Step 4: Generate Deep Report

```
# Lead Enrichment Report: [Company Name]
## Generated: [Date] | Depth: [Standard/Deep]

---

### Executive Summary
[2-3 sentence overview of the company and the opportunity for Prism]

### Company Profile
| Field | Detail |
|-------|--------|
| Legal Name | ... |
| DBA | ... |
| Website | ... |
| Founded | ... |
| Size | ... |
| Service Area | ... |
| Annual Revenue (est.) | ... |

### Services & Capabilities
- [Detailed service list with specialties noted]

### Certifications & Credentials
- [Full certification list]

### Insurance & Claims Relationships
- Carrier relationships: [list]
- TPA affiliations: [list]
- Xactimate usage: [yes/no]
- Insurance work percentage: [estimate]

### Technology & Operations
- Estimating software: [Xactimate, other]
- CRM / job management: [if known]
- Drying / monitoring tech: [if applicable]
- Fleet / equipment: [if known]

### Key Contacts
| # | Name | Title | Email | Phone | Status | Score | Category |
|---|------|-------|-------|-------|--------|-------|----------|
| 1 | ... | ... | ... | ... | ... | ... | ... |

### Financial Signals
- Revenue indicators: [awards, rankings, growth]
- Hiring trends: [expanding, stable, contracting]
- Investment signals: [new equipment, locations, acquisitions]

### Engagement Signals
| Type | Detail | Date | Source |
|------|--------|------|--------|
| News | ... | ... | ... |
| Job Posting | ... | ... | ... |
| Award | ... | ... | ... |

### Competitive Positioning
[Positioning analysis relative to Prism]
- Relationship type: [Partner / Competitor / Referral Source / Vendor]
- Overlap areas: [where services compete]
- Complementary areas: [where services complement]

### Recommended Approach

**Best First Contact**: [Name, Title] — [why this person]

**Talking Points**:
1. [Specific to their business — e.g., "Your water mitigation expertise pairs well with our contents pack-out capability"]
2. [Reference a signal — e.g., "Congratulations on the Inc. 5000 recognition"]
3. [Value proposition — e.g., "We help contractors offer a complete restoration solution to carriers"]

**Timing**: [Best time to reach out based on signals]

**Channel**: [LinkedIn / Email / Phone / In-person — based on what's available]

**Next Steps**:
1. [Specific action]
2. [Follow-up plan]
3. [Long-term relationship goal]

### Quality Score: [X]/100
- Data Completeness: [X]%
- Sources Used: [X]
- Confidence: HIGH / MEDIUM / LOW
- Gaps: [what couldn't be found]
```

### Step 5: Export to PDF

After presenting the report, offer:

"Would you like to export this report to PDF and/or Excel?"

If yes, construct the full JSON payload with all sections including `company_overview`, `signals`, and the detailed `analysis` section. Use `report_type: "Report"` to distinguish from standard enrichment exports.

```bash
cat > /tmp/enrichment_report_export.json << 'EXPORT_EOF'
{ ... json payload ... }
EXPORT_EOF

~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/enrichment_report_export.json

rm /tmp/enrichment_report_export.json
```

## Rules

- Only use publicly available information
- Never fabricate data — clearly mark estimates as estimates
- Include the APPROVAL GATE before contact validation
- Record sources for all data points
- If a search returns nothing, note the gap — don't skip the section
- The competitive positioning should be honest — if they're a strong competitor, say so
- Talking points should be specific and actionable, not generic
- The PDF export uses the standard export script with `type: "leads"`
