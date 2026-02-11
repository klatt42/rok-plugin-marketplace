name: deal-analysis
description: |
  RV and camper deal analysis methodology. FMV validation using NADA Guides
  (RV edition), deal rating system, dealer behavior signals, negotiation
  intelligence for RV-specific margin structures (25-35% vs 5-10% for vehicles).
  Used by the listing-ranker and price-validator agents.

## RV/Camper Deal Analysis Methodology

### FMV Validation

Fair Market Value (FMV) for RVs must use RV-specific sources. KBB and Edmunds do NOT cover RVs.

**Primary FMV source**: NADA Guides (RV edition) — the gold standard for RV values, comparable to KBB for vehicles. Provides low retail, average retail, and high retail values by year, make, model, and floorplan.

**Secondary sources**: RVTrader market data (average listing prices), JD Power RV values (depreciation projections), PPL Motor Homes sold listings (actual transaction prices for consignment).

**FMV calculation**: Average across available authoritative sources, weighted toward NADA when available.

### Deal Rating System

| Rating | Criteria | Color | Signal |
|--------|----------|-------|--------|
| GREAT_DEAL | >5% below FMV | Green (#059669) | Strong buy — below market, act quickly |
| GOOD_DEAL | 0-5% below FMV | Blue (#2563EB) | Competitive pricing, room to negotiate further |
| FAIR_PRICE | 0-5% above FMV | Amber (#D97706) | At market — negotiate down or wait |
| OVERPRICED | >5% above FMV | Red (#DC2626) | Above market — significant negotiation needed |

### RV-Specific Pricing Intelligence

RV dealer margins are fundamentally different from auto dealer margins:

| Factor | Vehicles | RVs |
|--------|----------|-----|
| Dealer margin | 5-10% off MSRP | 25-35% off MSRP |
| Negotiation room | $500-$2,000 | $3,000-$15,000 |
| Prep/delivery fees | $0-$500 | $1,000-$3,000 |
| Seasonal pricing impact | Minimal | Significant ($3,000-$8,000 swing) |
| Days on market norm | 30-60 days | 45-120 days |

**Key insight**: Because RV margins are 25-35%, buyers should NEVER pay MSRP. Aim for 20-25% below MSRP on new units.

### Dealer Behavior Signals

**Green flags**: Transparent internet pricing, willing to itemize prep fees, responsive to email quotes, good Google reviews (4.0+), RV Insider recommended.

**Yellow flags**: Price only available by phone, vague about prep fees, pressure tactics, mixed reviews (3.5-4.0).

**Red flags**: Mandatory add-on packages, "market adjustment" above MSRP, BBB complaints, below 3.5 Google rating, history of bait-and-switch complaints.

### Seasonal Buying Guide

| Season | Pricing | Strategy |
|--------|---------|----------|
| Jan-Mar (Show Season) | Best deals | Attend RV shows for show-only specials ($3K-$8K off) |
| Apr-Jun (Spring Rush) | Higher prices | Dealers less motivated, inventory moving |
| Jul-Aug (Peak Season) | Highest prices | Worst time to buy, demand peaks |
| Sep-Oct (End of Season) | Good deals | Clearance on current model year |
| Nov-Dec (Winter) | Variable | Dealers motivated but less inventory |

### Reference Documents

Load `references/pricing-sources.md` for the complete list of RV-specific pricing and valuation sources.
