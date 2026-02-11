# Scoring Rubric — Worked Examples and Edge Cases (RV/Camper)

## Example 1: TOP_PICK (Composite 88)

**User Profile**: Travel Trailer, $25K-$50K new or used, must-have slide-out + full bathroom, priorities: build quality + lightweight, tow vehicle: half-ton truck

**Camper**: 2025 Grand Design Imagine 2500RL ($42,500 MSRP)

**Fit Score: 91**
- Requirements match (30%): 95 — 1 slide standard, full dry bath standard, all must-haves met = 28.5
- Budget alignment (25%): 85 — $42,500 within $25K-$50K range, upper half = 21.25
- Priority alignment (25%): 90 — Grand Design = above-average build quality, 5,800 lbs dry = half-ton friendly = 22.5
- Lifestyle fit (20%): 95 — Perfect couple's trailer, manageable size, tow vehicle compatible with margin = 19

**Market Score: 84**
- Build quality (30%): 85 — Grand Design top 5, Azdel composite, aluminum frame = 25.5
- Value/TCO (25%): 72 — Average for quality level, storage + insurance are standard costs = 18
- Resale (20%): 80 — Grand Design holds value better than average (~65% at 3yr) = 16
- Feature value (15%): 88 — Good features for price, Azdel and MORryde suspension = 13.2
- Market timing (10%): 75 — Normal pricing, occasional show specials = 7.5

**Composite**: (91 * 0.55) + (84 * 0.45) = 50.05 + 37.8 = **87.85 -> 88**

---

## Example 2: RECOMMENDED (Composite 76)

**User Profile**: Same as above

**Camper**: 2025 Jayco Jay Flight 264BH ($32,000 MSRP)

**Fit Score: 78**
- Requirements match (30%): 80 — 1 slide standard, full bathroom... but it's a bunkhouse (user didn't need bunks) = 24
- Budget alignment (25%): 95 — $32,000 well under budget ceiling = 23.75
- Priority alignment (25%): 60 — Jayco = average build quality, 5,400 lbs dry = lightweight = 15
- Lifestyle fit (20%): 70 — Bunkhouse layout wastes space for couple, but functional = 14

**Market Score: 74**
- Build quality (30%): 60 — Jayco average tier, wood frame construction, more warranty claims = 18
- Value/TCO (25%): 80 — Lower purchase price helps TCO despite average build = 20
- Resale (20%): 55 — Jayco average retention (~55% at 3yr) = 11
- Feature value (15%): 82 — Good features for the price point = 12.3
- Market timing (10%): 85 — Dealer discounts common, good inventory = 8.5

**Composite**: (78 * 0.55) + (74 * 0.45) = 42.9 + 33.3 = **76.2 -> 76**

---

## Example 3: CONSIDER (Composite 62)

**User Profile**: Same as above

**Camper**: 2024 Forest River Rockwood Mini Lite 2109S ($26,000 MSRP)

**Fit Score: 65**
- Requirements match (30%): 50 — NO slide-out (must-have miss!), wet bath only (must-have miss!) = 15
- Budget alignment (25%): 100 — $26,000 well under budget = 25
- Priority alignment (25%): 65 — Rockwood = average build, 3,800 lbs dry = very lightweight = 16.25
- Lifestyle fit (20%): 50 — Very compact, limited living space, but ultra-towable = 10

**Market Score: 58**
- Build quality (30%): 50 — Forest River average quality, some reported issues = 15
- Value/TCO (25%): 85 — Low purchase price, lightweight = less fuel, cheap insurance = 21.25
- Resale (20%): 45 — Forest River below-average retention (~50% at 3yr) = 9
- Feature value (15%): 60 — Basic features, limited amenities = 9
- Market timing (10%): 80 — Discounts available, dealer wants to move inventory = 8

**Composite**: (65 * 0.55) + (58 * 0.45) = 35.75 + 26.1 = **61.85 -> 62**

Note: This camper MISSES two must-haves (slide-out, full bathroom), so the Requirements Match is capped at 50 despite budget savings. The cap correctly prevents an otherwise cheap camper from ranking too high.

---

## Edge Cases

### Must-Have Miss = Fit Score Cap
If a camper MISSES a stated must-have, the Requirements Match factor is capped at 50 regardless of other strengths. Example: User needs slide-out, camper has no slide -> Requirements Match = 40-50 max.

### Tow Vehicle Overweight = Hard Cap at 25
If a camper's GVWR exceeds the user's tow vehicle maximum towing capacity, Requirements Match is capped at 25. This is a SAFETY issue, not a preference. Example: User has half-ton truck (max 10,000 lbs), camper GVWR is 11,500 lbs -> Requirements Match = 25 max, and the output must include a safety warning.

### Over-Budget Penalty
Campers exceeding the stated budget range:
- 0-10% over: Budget alignment = 40-50
- 10-20% over: Budget alignment = 20-30
- 20%+ over: Budget alignment = 0-10

### New Model / No Data
For campers too new to have owner feedback:
- Set Build Quality factor to 50 (neutral) with confidence = "low"
- Note in the output that data is projected/estimated from manufacturer reputation
- Never assign TOP_PICK tier to a camper with no owner track record

### Single-Agent Data
If a camper only appears in 1 agent's output (e.g., only feature-matcher found it), flag confidence as "low" and cap composite at 70 regardless of calculated score.

### Motorhome vs Towable
For motorhomes (Class A, B, C), the tow vehicle question is N/A. Instead, evaluate:
- Chassis reliability (Ford, Freightliner, Mercedes)
- Fuel economy (6-10 MPG Class A, 10-14 MPG Class C, 18-22 MPG Class B)
- Drivability (length, turning radius, parking difficulty)
