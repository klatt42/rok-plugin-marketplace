# Listing Details

Deep-dive on a specific listing from the last camper/RV inventory search results. Provides full camper details, dealer reputation analysis, price negotiation intelligence, comparable listings, and applicable promotions.

## Usage

```
/camper-finder:listing-details #1                    # Deep-dive on listing rank #1
/camper-finder:listing-details #3                    # Deep-dive on listing rank #3
/camper-finder:listing-details GR12345               # Search by stock number
```

## Arguments

- `$ARGUMENTS` — Listing number (`#1`, `#3`) or stock number string

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Load Listing

1. Read `/tmp/camper_inventory_results.json`
2. Validate it has `type: "camper_inventory"` and a `listings` array
3. Find the target listing:
   - If `$ARGUMENTS` starts with `#`, match by `rank` field
   - Otherwise, match by stock_number (case-insensitive match on `stock_number` field)
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
   - RV Insider dealer reviews: Sales and service ratings
   - BBB: Accreditation status, complaints filed, response rate
   - Known issues (lawsuits, complaints, mandatory add-ons, prep fee practices)

2. **Price Negotiation Intelligence**
   - How much room between MSRP and asking price (RV margins are 25-35%)
   - Typical dealer prep and delivery fees ($1,000-$3,000)
   - Days on market impact on negotiation leverage
   - Current manufacturer promotions that may stack
   - Whether this dealer negotiates or has fixed pricing

3. **Comparable Listings**
   - Same camper/floorplan at 2-3 nearby dealers for price comparison
   - Same make/model with different floorplans at similar prices
   - Any consignment listings (PPL Motor Homes) for used

4. **Camper-Specific Intel**
   - If used: Condition concerns to inspect (roof, slides, water damage, tires)
   - NHTSA recalls for this make/model year
   - Known issues or common problems from owner forums
   - If new: Current model year updates, any mid-year changes

5. **Pre-Purchase Checklist**
   - Independent inspection recommended? (YES for used, recommended for new)
   - Key items to verify during PDI (Pre-Delivery Inspection)
   - Warranty coverage details and extended warranty options
   - What to negotiate beyond price (extended warranty, hitch, weight distribution)

### Phase 3: Display Detail

```
## Listing Deep-Dive: #[rank] [year] [make] [model] [floorplan]

### Camper Summary
- **Price**: $XX,XXX ([deal_rating])
- **vs FMV (NADA)**: [price_vs_fmv] ([price_vs_fmv_pct]%)
- **Type**: [rv_type] | [length]ft | [dry_weight] lbs dry | GVWR [gvwr] lbs
- **Layout**: [slides] slide(s) | Sleeps [capacity] | [bathroom type]
- **Tanks**: [fresh]gal fresh / [gray]gal gray / [black]gal black
- **Stock #**: [stock_number]
- **Source**: [source] | [listing_url]

### Dealer Profile: [dealer_name]
- **Google**: [rating]* ([review_count] reviews) — [trend: improving/stable/declining]
- **RV Insider**: [summary of dealer quality]
- **BBB**: [accreditation status] — [complaints in last 3 years]
- **Prep Fees**: [typical prep fee for this dealer]
- **Style**: [negotiable / fixed price / aggressive add-ons]
- **Phone**: [phone]
- **Distance**: [distance] miles

### Price Analysis
- **Asking**: $XX,XXX
- **MSRP**: $XX,XXX
- **FMV (NADA)**: ~$XX,XXX
- **Typical Margin**: 25-35% below MSRP for new RVs
- **Room to Negotiate**: ~$X,XXX based on [reasoning]
- **Prep Fee**: ~$X,XXX (negotiable)

### Promotions & Stacking
| Promotion | Value | Eligibility | Notes |
|-----------|-------|-------------|-------|
| [type] | $X,XXX | [who qualifies] | [stackable?] |

**Best-Case OTD**: ~$XX,XXX (asking - negotiation - promotions + tax/fees + prep)

### Comparable Listings
| Dealer | Floorplan | Price | Distance | Rating | Source |
|--------|-----------|-------|----------|--------|--------|
| [dealer] | [floorplan] | $XX,XXX | XXmi | X.X* | [source] |

### Camper Intelligence
- **Recalls**: [open recalls or "None open"]
- **Known Issues**: [common problems from forums for this model/year]
- **Build Quality**: [manufacturer reputation tier and notes]
- **Inspection**: [used: MUST get independent inspection | new: request PDI walkthrough]

### Pre-Purchase Checklist
- [ ] Independent inspection (used) / PDI walkthrough (new)
- [ ] Check roof sealant and condition
- [ ] Operate all slide-outs, verify seals
- [ ] Run all appliances (AC, furnace, fridge, water heater)
- [ ] Check all plumbing connections, fill tanks, check for leaks
- [ ] Verify tires (age, tread, matching set)
- [ ] Check underbelly for damage or moisture
- [ ] Test all electrical (shore power, 12V, generator if applicable)

### Recommendation
> [1-2 sentence actionable recommendation: buy/negotiate/skip and why]

### Next Steps
- Search more inventory: `/camper-finder:find-camper [original search prompt]`
- Expand search radius: `/camper-finder:find-camper [prompt]` with wider radius
- Back to recommendations: `/camper-recommender:camper-list`
```

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate dealer reviews, prices, or inspection findings.
- The recommendation must be honest — if the deal is bad, say so. If the dealer has red flags, flag them.
- Always include comparable listings so the user can assess relative value.
- The "Best-Case OTD" estimate should be realistic — factor in tax, prep fees, and typical dealer fees.
- RV prep fees ($1,000-$3,000) are almost always negotiable — always mention this.
- The pre-purchase checklist is critical for RVs — always include it. Roof condition and water damage are the #1 concern.
- If the listing is no longer available (search suggests it was sold), note this and suggest alternatives.
