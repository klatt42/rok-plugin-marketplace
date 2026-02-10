# Listing Details

Deep-dive on a specific listing from the last inventory search results. Provides full vehicle details, dealer reputation analysis, price negotiation intelligence, comparable listings, and applicable incentives.

## Usage

```
/vehicle-finder:listing-details #1                    # Deep-dive on listing rank #1
/vehicle-finder:listing-details #3                    # Deep-dive on listing rank #3
/vehicle-finder:listing-details 2T3                   # Search by partial VIN
```

## Arguments

- `$ARGUMENTS` — Listing number (`#1`, `#3`) or partial VIN string

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Load Listing

1. Read `/tmp/vehicle_inventory_results.json`
2. Validate it has `type: "vehicle_inventory"` and a `listings` array
3. Find the target listing:
   - If `$ARGUMENTS` starts with `#`, match by `rank` field
   - Otherwise, match by partial VIN (case-insensitive prefix match on `vin` field)
4. If no match found, show available listings and ask the user to clarify

### Phase 2: Deep Research

Launch 1 agent via `Task` (subagent_type: `general-purpose`, model: `sonnet`) to deep-research this specific listing:

**Agent prompt includes:**
1. The listing JSON from the search results
2. The search_params from the results file
3. The market_context from the results file

**Agent research tasks (8-12 WebSearch queries):**

1. **Dealer Reputation Deep-Dive**
   - Google Reviews: Rating, review count, recent review trends
   - DealerRater: Detailed reviews, sales and service ratings separately
   - BBB: Accreditation status, complaints filed, response rate
   - Any known issues (lawsuits, complaints, mandatory add-ons)

2. **Price Negotiation Intelligence**
   - Invoice price estimate for this specific trim
   - How much room between invoice and asking price
   - Days on market impact on negotiation leverage
   - Current manufacturer incentives that stack (APR + cash + loyalty)
   - Whether this dealer negotiates (some are "no-haggle")

3. **Comparable Listings**
   - Same vehicle at 2-3 nearby dealers for price comparison
   - Any private party listings if used
   - Price trend for this specific model/trim in the area

4. **Vehicle-Specific Intel**
   - If used: Vehicle history summary (Carfax/AutoCheck availability)
   - Open recalls for this model year (NHTSA)
   - Known issues or TSBs for this specific model/year
   - If new: Factory order vs. dealer stock availability

5. **Incentive Stacking**
   - All current manufacturer incentives
   - Which incentives can stack (e.g., APR + loyalty but not cash + APR)
   - Dealer-specific promotions if visible
   - Best total out-the-door price estimate

### Phase 3: Display Detail

```
## Listing Deep-Dive: #[rank] [year] [make] [model] [trim]

### Vehicle Summary
- **Price**: $XX,XXX ([deal_rating])
- **vs FMV**: [price_vs_fmv] ([price_vs_fmv_pct]%)
- **Color**: [exterior] / [interior]
- **Mileage**: [mileage]
- **VIN**: [vin]
- **Source**: [source] | [listing_url]

### Dealer Profile: [dealer_name]
- **Google**: [rating]* ([review_count] reviews) — [trend: improving/stable/declining]
- **DealerRater**: [rating]* — [summary of common praise/complaints]
- **BBB**: [accreditation status] — [complaints in last 3 years]
- **Style**: [negotiable / no-haggle / aggressive add-ons]
- **Phone**: [phone]
- **Distance**: [distance] miles

### Price Analysis
- **Asking**: $XX,XXX
- **MSRP**: $XX,XXX
- **Invoice Est.**: $XX,XXX
- **FMV**: ~$XX,XXX
- **Room to Negotiate**: ~$X,XXX based on [reasoning]

### Incentive Stacking
| Incentive | Value | Eligibility | Stackable? |
|-----------|-------|-------------|------------|
| [type] | $X,XXX | [who qualifies] | Yes/No |

**Best-Case OTD**: ~$XX,XXX (asking - negotiation - stackable incentives + tax/fees)

### Comparable Listings
| Dealer | Trim | Price | Distance | Rating | Source |
|--------|------|-------|----------|--------|--------|
| [dealer] | [trim] | $XX,XXX | XXmi | X.X* | [source] |

### Vehicle Intelligence
- **Recalls**: [open recalls or "None open"]
- **Known Issues**: [common complaints for this model/year]
- **History**: [if used: Carfax/AutoCheck summary; if new: "Factory new"]

### Recommendation
> [1-2 sentence actionable recommendation: buy/negotiate/skip and why]

### Next Steps
- Search more inventory: `/vehicle-finder:find-vehicle [original search prompt]`
- Expand search radius: `/vehicle-finder:find-vehicle [prompt] --radius=100`
- Back to recommendations: `/vehicle-recommender:recommendation-list`
```

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate dealer reviews, prices, or vehicle history.
- The recommendation must be honest — if the deal is bad, say so. If the dealer has red flags, flag them.
- Always include comparable listings so the user can assess relative value.
- The "Best-Case OTD" estimate should be realistic, not optimistic — factor in tax and typical fees.
- If the listing is no longer available (search suggests it was sold), note this and suggest alternatives.
