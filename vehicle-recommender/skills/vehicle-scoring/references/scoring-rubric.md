# Scoring Rubric — Worked Examples and Edge Cases

## Example 1: TOP_PICK (Composite 91)

**User Profile**: SUV/Crossover, $30K-$50K new, must-have AWD + tech, priorities: reliability + resale

**Vehicle**: 2026 Toyota RAV4 Hybrid XLE Premium ($37,500)

**Fit Score: 94**
- Requirements match (30%): 100 — AWD standard, TSS 3.0 standard, all must-haves met = 30
- Budget alignment (25%): 90 — $37,500 in $30K-$50K range, well within budget = 22.5
- Priority alignment (25%): 95 — #1 reliability brand, top resale in class = 23.75
- Lifestyle fit (20%): 90 — Excellent family SUV, great road trip vehicle = 18

**Market Score: 87**
- Reliability (30%): 95 — CR 5/5, minimal recalls, proven hybrid system = 28.5
- Value/TCO (25%): 80 — Low fuel cost (40 MPG), but not cheapest to insure = 20
- Resale (20%): 92 — 72% residual at 3 years, best in class = 18.4
- Feature value (15%): 78 — Good value but competitors offer more tech per dollar = 11.7
- Market timing (10%): 75 — Normal incentives, good inventory = 7.5

**Composite**: (94 * 0.55) + (87 * 0.45) = 51.7 + 39.15 = **90.85 -> 91**

---

## Example 2: RECOMMENDED (Composite 78)

**User Profile**: Same as above

**Vehicle**: 2026 Mazda CX-50 Turbo Premium ($41,000)

**Fit Score: 76**
- Requirements match (30%): 85 — AWD standard, good tech but no radar cruise on base = 25.5
- Budget alignment (25%): 75 — $41K is mid-range in budget, getting up there = 18.75
- Priority alignment (25%): 65 — Good reliability but not Toyota-level, average resale = 16.25
- Lifestyle fit (20%): 80 — Great SUV, slightly more adventure-oriented = 16

**Market Score: 80**
- Reliability (30%): 75 — CR 4/5, Mazda improving but less proven = 22.5
- Value/TCO (25%): 75 — Premium fuel required, moderate maintenance costs = 18.75
- Resale (20%): 70 — 65% residual at 3 years, above average = 14
- Feature value (15%): 88 — Excellent interior quality for the price, great driving dynamics = 13.2
- Market timing (10%): 80 — Good incentives on outgoing inventory = 8

**Composite**: (76 * 0.55) + (80 * 0.45) = 41.8 + 36.0 = **77.8 -> 78**

---

## Example 3: CONSIDER (Composite 64)

**User Profile**: Same as above

**Vehicle**: 2026 Chevrolet Equinox RS ($35,000)

**Fit Score: 68**
- Requirements match (30%): 75 — AWD available ($1,600 extra), decent tech = 22.5
- Budget alignment (25%): 95 — Well under budget = 23.75
- Priority alignment (25%): 45 — Average reliability, below-average resale = 11.25
- Lifestyle fit (20%): 55 — Adequate SUV but not standout in any area = 11

**Market Score: 59**
- Reliability (30%): 50 — CR 3/5, GM has mixed reliability record = 15
- Value/TCO (25%): 70 — Low purchase price offsets average running costs = 17.5
- Resale (20%): 45 — 55% residual at 3 years, below average = 9
- Feature value (15%): 75 — Good features for the price point = 11.25
- Market timing (10%): 85 — Strong incentives, dealer discounts common = 8.5

**Composite**: (68 * 0.55) + (59 * 0.45) = 37.4 + 26.55 = **63.95 -> 64**

---

## Edge Cases

### Must-Have Miss = Fit Score Cap
If a vehicle MISSES a stated must-have, the Requirements Match factor is capped at 50 regardless of other strengths. Example: User needs towing, vehicle has 1,500 lb capacity (insufficient) -> Requirements Match = 40, which drags down the entire Fit Score.

### Over-Budget Penalty
Vehicles exceeding the stated budget range:
- 0-10% over: Budget alignment = 40-50
- 10-20% over: Budget alignment = 20-30
- 20%+ over: Budget alignment = 0-10

### New Model / No Data
For vehicles too new to have reliability data:
- Set Reliability factor to 50 (neutral) with confidence = "low"
- Note in the output that data is projected/estimated
- Never assign TOP_PICK tier to a vehicle with no reliability track record

### Single-Agent Data
If a vehicle only appears in 1 agent's output (e.g., only market-researcher found it), flag confidence as "low" and cap composite at 70 regardless of calculated score.
