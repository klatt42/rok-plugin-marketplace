# Quality Scoring Rubric

Detailed breakdown of the 0-100 quality scoring system used to evaluate business directory listings.

## Scoring Categories

### Data Completeness (60 points max)

| Criteria | Points | Description |
|----------|--------|-------------|
| Name present | 10 | Business name is non-empty |
| Address present | 10 | Street address with city and state |
| Phone present | 10 | Valid phone number (any format) |
| Website present | 10 | Valid URL |
| Description present | 10 | At least 20 characters of descriptive text |
| Email present | 5 | Valid email address |
| Hours present | 5 | Operating hours in any format |

### Enrichment Quality (25 points max)

| Criteria | Points | Description |
|----------|--------|-------------|
| Rating available | 10 | Star rating from any review platform |
| 10+ reviews | 5 | Minimum review count threshold |
| Services listed | 5 | At least 2 services/specializations |
| Social links | 5 | At least 1 social media profile |

### Verification (15 points max, deep mode only)

| Criteria | Points | Description |
|----------|--------|-------------|
| Cross-validated | 10 | Data confirmed by 2+ independent sources |
| Phone confirmed | 5 | Phone number matches across sources |

### Penalty Adjustments

| Finding | Adjustment | Description |
|---------|------------|-------------|
| Business appears closed | -30 | Permanently closed or inactive indicators |
| Phone mismatch | -10 | Different phone numbers across sources |
| Address mismatch | -5 | Conflicting address information |
| Category mismatch | -20 | Business doesn't match the directory niche |
| No independent verification | -10 | Only found in a single source (deep mode) |

## Status Thresholds

| Score Range | Status | Display | Export Behavior |
|-------------|--------|---------|-----------------|
| 50-100 | `verified` | Green badge | Included in all exports |
| 30-49 | `needs_verification` | Yellow badge | Included with flag |
| 0-29 | `removed` | Red / hidden | Excluded from exports |

## Scoring Examples

### High Score (85-100)
```
ABC Heating & Cooling
- Name: ABC Heating & Cooling (+10)
- Address: 123 Main St, Austin, TX 78701 (+10)
- Phone: +15125551234 (+10)
- Website: https://abchvac.com (+10)
- Description: "Full-service HVAC..." (42 chars) (+10)
- Email: info@abchvac.com (+5)
- Hours: Mon-Fri 8am-6pm (+5)
- Rating: 4.8 (+10)
- Reviews: 156 (+5)
- Services: 4 listed (+5)
- Social: Facebook, Instagram (+5)
Total: 85 -> verified
```

### Medium Score (50-65)
```
Joe's Plumbing
- Name: Joe's Plumbing (+10)
- Address: Austin, TX (city only, no street) (+5, partial)
- Phone: +15125559876 (+10)
- Website: none (0)
- Description: none (0)
- Email: none (0)
- Hours: none (0)
- Rating: 4.2 (+10)
- Reviews: 23 (+5)
- Services: none (0)
- Social: none (0)
Total: 50 -> verified (barely)
```

### Low Score (25-35)
```
Quick Fix Services
- Name: Quick Fix Services (+10)
- Address: none (0)
- Phone: (512) 555-0000 (+10)
- Website: none (0)
- Description: none (0)
- Email: none (0)
- Hours: none (0)
- Rating: none (0)
- Reviews: 0 (0)
- Services: none (0)
- Social: none (0)
Total: 20 -> removed
```

### Verification Bonus Example (Deep Mode)
```
Starting score: 70
+ Cross-validated on Yelp + Google Maps: +10
+ Phone confirmed on Google Maps: +5
Final: 85 -> verified
```

### Penalty Example
```
Starting score: 65
- Google Maps shows "Permanently Closed": -30
Final: 35 -> needs_verification
```
