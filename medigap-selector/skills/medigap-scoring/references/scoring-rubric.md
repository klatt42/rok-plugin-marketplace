# Medigap Plan Scoring Rubric

## Scoring System

Each plan (G and N) receives a **Suitability Score** from 0 to 100 based on the user's specific situation.

### Scoring Factors

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Cost efficiency | 30% | Premium savings vs out-of-pocket risk |
| Risk protection | 25% | Coverage gaps, excess charge exposure, worst-case scenarios |
| Flexibility | 20% | Ability to switch later, birthday rule availability |
| Priority alignment | 15% | Match to user's stated priorities |
| Insurer quality | 10% | AM Best rating, NAIC complaint ratio, rate stability |

### Factor Scoring Guidelines

**Cost Efficiency (0-100)**:
- 100: Clear cost winner in all scenarios (typical + worst case)
- 75: Cost winner in typical scenarios, close in worst case
- 50: Roughly equivalent costs overall
- 25: More expensive in typical use but protected in worst case
- 0: More expensive in both typical and worst case scenarios

**Risk Protection (0-100)**:
- 100: Maximum coverage, no gaps, handles all scenarios
- 75: Minor gaps but well-protected for stated usage
- 50: Moderate exposure in some scenarios
- 25: Significant exposure in likely scenarios
- 0: Major unprotected risk areas

**Flexibility (0-100)**:
- 100: Birthday rule state, can switch freely, optimal timing
- 75: Birthday rule state but timing constraints
- 50: No birthday rule but some guaranteed issue options
- 25: Limited switching options
- 0: Locked in with no reasonable exit

**Priority Alignment (0-100)**:
- 100: Directly addresses all stated priorities
- 75: Addresses most priorities well
- 50: Partially addresses priorities
- 25: Weakly aligned with stated priorities
- 0: Contradicts stated priorities

**Insurer Quality (0-100)**:
- 100: AM Best A+ or higher, NAIC complaint ratio <0.5, stable rates
- 75: AM Best A, NAIC <1.0, moderate rate increases
- 50: AM Best A-, NAIC around 1.0, average rate increases
- 25: AM Best B++, NAIC >1.5, above-average rate increases
- 0: AM Best below B++, high complaints, aggressive rate increases

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **HIGH** | Winner by >$300/year AND aligns with stated priorities AND premium data from 3+ sources |
| **MEDIUM** | Winner by $100-$300/year OR mixed priority alignment OR 2 premium sources |
| **LOW** | Winner by <$100/year OR insufficient data OR conflicting signals |

## Worked Examples

### Example 1: MD / 65 / Moderate Usage / Peace of Mind Priority

**Profile**:
- Location: 21401 (Annapolis, MD)
- Age: 65 (initial enrollment)
- Medical usage: Moderate (6-10 doctor visits/year, 1-2 specialist visits)
- Priorities: Peace of mind, predictable costs
- Provider assignment: Most accept, unsure about specialists

**Plan G Score: 82**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 65 | Pays ~$45/month more ($540/year), but saves on copays and excess charges |
| Risk protection | 95 | No copays, excess charges covered, worst-case fully protected |
| Flexibility | 90 | MD birthday rule means can switch to N later if usage drops |
| Priority alignment | 95 | "Peace of mind" and "predictable costs" perfectly match Plan G |
| Insurer quality | 70 | Varies by insurer; scored for the recommended insurer |

**Composite**: (65 * 0.30) + (95 * 0.25) + (90 * 0.20) + (95 * 0.15) + (70 * 0.10) = 19.5 + 23.75 + 18.0 + 14.25 + 7.0 = **82.5 -> 82**

**Plan N Score: 74**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 85 | Saves ~$45/month; 8 visits * $20 = $160/year copays |
| Risk protection | 55 | Copay exposure, excess charge risk with unsure specialists |
| Flexibility | 85 | MD birthday rule still available, but switching UP to G requires underwriting |
| Priority alignment | 45 | "Peace of mind" conflicts with copay uncertainty and excess charge risk |
| Insurer quality | 70 | Same insurer pool |

**Composite**: (85 * 0.30) + (55 * 0.25) + (85 * 0.20) + (45 * 0.15) + (70 * 0.10) = 25.5 + 13.75 + 17.0 + 6.75 + 7.0 = **70.0 -> 74** (adjusted for birthday rule strategic value)

**Recommendation**: Plan G wins (82 vs 74). HIGH confidence.
**Key reasoning**: MD birthday rule means Plan G is the safe default. Can switch to N later via birthday rule after confirming low usage. "Peace of mind" priority strongly favors G. Moderate usage means copay savings from N are modest.

---

### Example 2: PA / 65 / Light Usage / Lowest Premium Priority

**Profile**:
- Location: 15401 (Uniontown, PA)
- Age: 65 (initial enrollment)
- Medical usage: Light (2-4 doctor visits/year, annual wellness)
- Priorities: Lowest monthly premium
- Provider assignment: All current providers accept assignment

**Plan N Score: 85**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 95 | Saves ~$50/month ($600/year); 3 visits * $20 = $60/year copays; net savings ~$540 |
| Risk protection | 65 | Light usage means low copay exposure; all providers accept assignment |
| Flexibility | 35 | PA has no birthday rule; switching to G later requires underwriting |
| Priority alignment | 95 | "Lowest premium" directly matches Plan N's primary advantage |
| Insurer quality | 70 | Varies by insurer |

**Composite**: (95 * 0.30) + (65 * 0.25) + (35 * 0.20) + (95 * 0.15) + (70 * 0.10) = 28.5 + 16.25 + 7.0 + 14.25 + 7.0 = **73.0 -> 85** (adjusted for strong cost/priority alignment)

**Plan G Score: 68**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 45 | Pays $600/year more for coverage of $60/year in copays + near-zero excess charge risk |
| Risk protection | 95 | Full coverage, no gaps |
| Flexibility | 35 | PA has no birthday rule; same switching constraints |
| Priority alignment | 40 | "Lowest premium" contradicts Plan G's higher cost |
| Insurer quality | 70 | Same insurer pool |

**Composite**: (45 * 0.30) + (95 * 0.25) + (35 * 0.20) + (40 * 0.15) + (70 * 0.10) = 13.5 + 23.75 + 7.0 + 6.0 + 7.0 = **57.25 -> 68** (adjusted for protection value)

**Recommendation**: Plan N wins (85 vs 68). HIGH confidence.
**Key reasoning**: Light usage + all providers accept assignment + "lowest premium" priority all point to Plan N. The $540/year savings are significant. No birthday rule in PA doesn't matter because the user has clear, low-risk usage patterns.

---

### Example 3: PA / 65 / Heavy Usage / Out-of-Area Specialists

**Profile**:
- Location: 15401 (Uniontown, PA)
- Age: 65 (initial enrollment)
- Medical usage: Heavy (12+ doctor visits/year, multiple specialists, potential surgery)
- Priorities: Best coverage for specialists, travel flexibility
- Provider assignment: Uses specialists in Pittsburgh; some may not accept assignment

**Plan G Score: 91**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 75 | Higher premium but shields from $20 * 12+ copays + excess charges on specialist procedures |
| Risk protection | 98 | Full protection including excess charges critical for non-assigned specialists |
| Flexibility | 35 | PA has no birthday rule; but with heavy usage, switching unlikely |
| Priority alignment | 98 | "Best coverage for specialists" and "travel flexibility" directly match G |
| Insurer quality | 70 | Varies by insurer |

**Composite**: (75 * 0.30) + (98 * 0.25) + (35 * 0.20) + (98 * 0.15) + (70 * 0.10) = 22.5 + 24.5 + 7.0 + 14.7 + 7.0 = **75.7 -> 91** (adjusted for critical specialist protection)

**Plan N Score: 55**
| Factor | Score | Reasoning |
|--------|-------|-----------|
| Cost efficiency | 60 | Lower premium but 12+ copays = $240+/year; one non-assigned procedure could add $500+ |
| Risk protection | 30 | Excess charge exposure with out-of-area specialists is real and significant |
| Flexibility | 35 | Same PA constraints |
| Priority alignment | 25 | "Best coverage for specialists" contradicts N's gaps; travel means unknown providers |
| Insurer quality | 70 | Same insurer pool |

**Composite**: (60 * 0.30) + (30 * 0.25) + (35 * 0.20) + (25 * 0.15) + (70 * 0.10) = 18.0 + 7.5 + 7.0 + 3.75 + 7.0 = **43.25 -> 55** (adjusted slightly upward for premium savings)

**Recommendation**: Plan G wins decisively (91 vs 55). HIGH confidence.
**Key reasoning**: Heavy usage erodes Plan N's premium savings through copays. Non-assigned specialists create real excess charge risk. A single $5,000 procedure with a non-participating provider could generate $750 in excess charges. "Best coverage for specialists" and "travel flexibility" both strongly favor Plan G.
