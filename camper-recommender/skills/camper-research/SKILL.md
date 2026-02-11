name: camper-research
description: |
  Multi-dimensional RV and camper research methodology for personalized recommendations.
  Four research agents (market, reliability, cost, features) with configurable
  depth levels. Interview-driven requirements gathering with AskUserQuestion.
  Use when running /recommend-camper or discussing camper/RV research strategy.

## Camper/RV Research Methodology

### Four Research Dimensions

**Market Research**: Analyze current pricing, dealer incentives, show season deals, supply levels, and depreciation trends. RVs depreciate faster than vehicles (15-25% year 1, 40-60% over 5 years), making market timing and brand selection crucial. Key sources are RVTrader, NADA Guides (RV edition), and Camping World for real-time market data.

**Reliability Analysis**: Evaluate build quality using RV Insider ratings, manufacturer reputation tiers, owner forum consensus, and warranty coverage. The RV industry has wider quality variance than the auto industry — premium brands (Airstream, Oliver) vs mass-market (Forest River, Coachmen) differ dramatically. Roof leaks, water damage, and slide mechanism failures are the top concerns.

**Cost Analysis**: Calculate total cost of ownership (TCO) across specialty RV insurance, storage fees, maintenance (roof resealing, winterization), campground costs, towing fuel costs, and steep depreciation. RV ownership has significant hidden costs that first-time buyers consistently underestimate. Good Sam Insurance and KOA campground rates are primary data sources.

**Feature Matching**: Map user must-haves and priorities against each camper's floorplan, weight specs, tank capacities, and amenities. The best recommendation isn't the "best RV" — it's the one whose floorplan and weight fit what the user actually needs. Tow vehicle compatibility is safety-critical.

### Depth Levels

| Depth | Time | Searches/Agent | Shortlist | Cross-Ref |
|-------|------|---------------|-----------|-----------|
| quick | 5-10 min | 5-8 | 5-6 | No |
| standard | 15-25 min | 10-15 | 6-8 | Yes (ranker) |
| deep | 30-45 min | 15-20 | 8-10 | Yes + follow-up |

### Interview-First Approach

Unlike profile-hardcoded plugins, camper-recommender uses `AskUserQuestion` to gather requirements dynamically. This means every run is personalized:
1. RV/camper type & purpose
2. Budget & buying preference
3. Must-have features (multi-select)
4. Priorities (multi-select)
5. Tow vehicle (conditional — towable types only)

The Requirements Profile JSON drives all agent research and scoring.

### Reference Documents

Load `references/source-map.md` for the complete source list with trusted sites per research dimension.
