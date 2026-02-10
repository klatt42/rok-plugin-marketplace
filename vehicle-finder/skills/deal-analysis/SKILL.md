name: deal-analysis
description: |
  Deal analysis methodology for vehicle inventory listings. How to assess a
  listing's value, validate pricing against fair market value (FMV), interpret
  dealer behavior, and identify negotiation opportunities. Use when running
  /find-vehicle, /inventory-search, or discussing vehicle deal quality.

## Deal Analysis Methodology

### Fair Market Value (FMV) Validation

FMV is established by averaging prices from multiple authoritative sources. No single source is definitive — the average of KBB Fair Purchase Price, Edmunds True Market Value, TrueCar Market Average, and CarGurus Instant Market Value provides the most reliable baseline.

**Key distinction**: MSRP is what the manufacturer suggests. FMV is what buyers are actually paying. For popular vehicles, FMV may exceed MSRP (market adjustment). For slow sellers, FMV is often well below MSRP.

### Deal Rating System

| Rating | Criteria | What It Means |
|--------|----------|---------------|
| GREAT_DEAL | >5% below FMV | Exceptional value — act quickly, these don't last |
| GOOD_DEAL | 0-5% below FMV | Solid deal — worth pursuing, especially at good dealers |
| FAIR_PRICE | 0-5% above FMV | Market rate — acceptable but room to negotiate |
| OVERPRICED | >5% above FMV | Above market — negotiate hard or look elsewhere |

### Dealer Behavior Signals

**Positive signals**: Transparent internet pricing, no mandatory add-ons, high Google/DealerRater ratings (4.0+), high review volume (200+), responsive to online inquiries.

**Warning signs**: "Call for price" on every listing, mandatory dealer add-on packages (paint protection, nitrogen tires, VIN etching, fabric protection), market adjustments above MSRP, low review ratings, BBB complaints.

### Negotiation Intelligence

- **Invoice price** is typically 3-6% below MSRP. A fair new car deal is $500-1,500 above invoice.
- **Days on market** is leverage: 30+ days means the dealer is more motivated. Under 7 days means high demand.
- **End of month/quarter** gives dealers incentive to move inventory for manufacturer bonuses.
- **Multiple identical vehicles** in stock means competition within the dealer's own inventory.

### Reference Documents

Load `references/pricing-sources.md` for the complete list of trusted pricing sources and search query patterns for each.
