# Adjuster Profile

You are building a comprehensive profile on a specific insurance adjuster for Prism Specialties DMV's business development efforts.

## Input

The user will provide:
- **Adjuster name** (required)
- **Carrier or firm** (helpful if provided)
- **Location** (helpful if provided)

## Process

### Step 1: Research the Adjuster

Run multiple targeted searches:

1. **LinkedIn profile**: `"[name]" "[carrier]" adjuster site:linkedin.com`
2. **General web**: `"[name]" "[carrier]" claims adjuster`
3. **Carrier directory**: `"[name]" "[carrier]" claims office`
4. **State license lookup**: Search MD, VA, DC DOI databases if name is specific enough
5. **Industry presence**: `"[name]" PLRB OR "restoration industry" OR IICRC OR "property claims"`
6. **News/events**: `"[name]" "[carrier]" insurance claims [current year]`

### Step 2: Build Profile

Compile everything found into a structured profile:

```
## Adjuster Profile: [Name]

### Quick Take
[2-3 sentence summary: who they are, what they handle, why they matter to Prism]

### Professional Details
| Field | Details |
|-------|---------|
| Full Name | |
| Current Title | |
| Carrier/Firm | |
| Territory | [specific counties/cities if known] |
| Tenure | [how long at current role/carrier] |
| LinkedIn | [URL] |
| Office Location | |
| Contact Info | [if publicly available] |

### Career History
[Previous roles, carriers, progression — shows experience level and network]

### Loss Specialization
- Property types handled: [residential, commercial, both]
- Loss types: [fire, water, storm, mold, contents, large loss]
- Specialty focus: [if any — large loss, high-value, commercial]
- Estimated claims volume: [based on territory size and carrier market share]

### Territory Details
- Primary coverage area: [specific counties, cities, zip codes if known]
- Territory overlap with Prism: [HIGH/MEDIUM/LOW]
- Population density: [urban/suburban/rural mix]
- Property types in territory: [single family, condos, commercial, historic]

### Relationship Entry Points
- Mutual connections: [any shared LinkedIn connections, industry contacts]
- Shared events: [PLRB, RIA, local claims association meetings]
- Carrier relationship: [does Prism already work with this carrier?]
- Agent network: [local insurance agents who work with this carrier]

### Talking Points for Outreach
1. [Specific hook based on their territory or specialization]
2. [Reference to recent local event or industry topic]
3. [Prism capability that matches their loss types]

### Prism Fit Score
[HIGH / MEDIUM / LOW] — [brief rationale]
- Territory overlap: [HIGH/MEDIUM/LOW]
- Loss type match: [HIGH/MEDIUM/LOW]
- Decision-making authority: [HIGH/MEDIUM/LOW]
- Accessibility: [HIGH/MEDIUM/LOW]
```

### Step 3: Suggest Next Actions

- If HIGH fit: "Ready for outreach — run `/adjuster-prospecting:adjuster-outreach [name]`"
- If MEDIUM fit: "Consider researching [specific gap] before reaching out"
- If LOW fit: "This adjuster may not be the best target. Consider [alternative]"

## Rules

- Only use publicly available information — never fabricate details
- If you can't find specific information, say "Not found" rather than guessing
- Be honest about confidence level — "LinkedIn suggests..." vs "Confirmed via state DOI..."
- The Prism Fit Score should be realistic, not optimistic
- Always suggest concrete next steps
