# Find Contractors

You are searching for general contractors, restoration contractors, and construction companies that could become referral partners for Prism Specialties DMV. The goal is to find contractors who handle insurance losses and could refer specialty contents restoration work.

## Input

The user will provide one or more of:
- **Contractor type** (restoration, GC, mitigation, roofing, plumbing, property management)
- **Geographic area** (default: DMV — DC, Northern Virginia, Maryland)
- **Specific county or city** (narrows the search)
- **Brand/franchise** (SERVPRO, ServiceMaster, Paul Davis, etc.)

## Process

### Step 1: Construct Search Queries

Based on input, build targeted searches:

**LinkedIn search** (for decision makers):
```
"[contractor type]" AND ("owner" OR "operations manager" OR "estimator")
AND ("[location]") site:linkedin.com
```

**Google Maps / Business search**:
```
"[contractor type]" "[city/county]" "restoration" OR "insurance" OR "mitigation"
```

**License lookup**:
- VA: Search DPOR at dpor.virginia.gov for contractor licenses by name or city
- MD: Search MHIC at labor.maryland.gov/license/mhic
- DC: Search DCRA at dcra.dc.gov

**Franchise search** (if applicable):
```
"[franchise name]" "owner" OR "franchise" "[location]" site:linkedin.com
```

**Industry directory search**:
```
"[company name]" site:restoreation.org OR site:iicrc.org OR site:bbb.org
```

### Step 2: Execute Searches

Run multiple searches in parallel:
1. LinkedIn search for decision makers at target contractor types
2. Google/Maps search for contractors in specified area
3. State license lookup for verified contractors
4. Industry directory check (RIA, IICRC, BBB)
5. Review site for reputation (Google reviews, Yelp, Angi)

### Step 3: Compile Results

For each contractor found, gather:
- Company name
- Key contact (owner, ops manager, estimator)
- Location / service area
- Contractor type (restoration, GC, mitigation, etc.)
- License status (if found)
- Insurance work focus (yes/no/unclear)
- Website
- LinkedIn URL (company or contact)
- Google review rating and count
- Referral potential (HIGH/MEDIUM/LOW)

### Step 4: Present Results

```
## Contractor Search Results: [Type] in [Area]

### Search Summary
- Searches conducted: [count]
- Contractors found: [count]
- High-potential referral partners: [count]

### Results

| # | Company | Contact | Type | Area | Insurance Focus | Reviews | Referral Potential |
|---|---------|---------|------|------|----------------|---------|-------------------|
| 1 | [Name] | [Person, Title] | Restoration | [City/County] | Yes | 4.5 (120) | HIGH |
| 2 | [Name] | [Person, Title] | GC | [City/County] | Yes | 4.2 (85) | MEDIUM |

### Top Picks (Recommended for Outreach)

1. **[Company Name]** — [Why they're a good fit for Prism]
2. **[Company Name]** — [Why they're a good fit for Prism]
3. **[Company Name]** — [Why they're a good fit for Prism]

### Search Gaps
- [What information couldn't be found]
- [Suggested follow-up searches]

### Suggested Next Steps
- Profile top picks: `/contractor-prospecting:contractor-profile [company name]`
- Draft outreach: `/contractor-prospecting:contractor-outreach [company name]`
```

## Rules

- Only use publicly available information — never fabricate details
- If you can't find specific information, say "Not found" rather than guessing
- Prioritize contractors who explicitly mention insurance work or restoration
- Franchise owners are often the best contacts (they're local decision makers)
- A contractor doing 50+ Google reviews likely has volume (good referral potential)
- Rate referral potential based on: territory overlap + insurance focus + no contents capability + volume indicators
- Always suggest concrete next steps
