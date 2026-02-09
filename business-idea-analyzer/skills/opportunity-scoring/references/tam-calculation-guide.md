# TAM/SAM/SOM Calculation Guide

## The Waterfall

```
TAM (Total Addressable Market)
  └─ Everyone who could theoretically use this type of product
     Example: All 250M FB Marketplace users worldwide

SAM (Serviceable Addressable Market)
  └─ TAM filtered by your actual reach and product fit
     Example: 5M "serious sellers" (>$1K/mo revenue) in English-speaking markets

SOM (Serviceable Obtainable Market)
  └─ SAM filtered by realistic capture rate in Year 1/3
     Example: 5K users Year 1 (0.1% of SAM), 50K users Year 3 (1% of SAM)
```

## Bottom-Up TAM Formula

The most reliable approach for solopreneur SaaS:

```
Step 1: Identify total platform/market users
  Total Users = [platform monthly active users or industry participant count]

Step 2: Apply engagement filter
  Engaged Users = Total Users x [engagement rate: typically 20-40%]

Step 3: Segment by buyer type
  Target Segment = Engaged Users x [segment %]
  Segments: casual (70%), serious (20%), high-volume (8%), professional (2%)

Step 4: Apply tools adoption rate
  Tool Adopters = Target Segment x [tools penetration: 2-5% for new category, 10-20% for established]

Step 5: Calculate revenue
  TAM = Tool Adopters x ARPU x 12

Step 6: Apply realistic capture
  SOM Year 1 = TAM x [0.001 to 0.005 for new product]
  SOM Year 3 = TAM x [0.005 to 0.02 with traction]
```

## ARPU Benchmarks (Monthly, SaaS B2B/Prosumer)

| Category | Low | Mid | High |
|----------|-----|-----|------|
| Micro-SaaS / Solo tools | $9 | $19 | $39 |
| SMB SaaS | $29 | $49 | $99 |
| Mid-market SaaS | $99 | $299 | $999 |
| Enterprise SaaS | $999 | $5,000 | $50,000+ |

**For solopreneur products, target $19-49/mo ARPU.**

## SaaS Benchmark Ranges

| Metric | Conservative | Average | Optimistic |
|--------|-------------|---------|------------|
| Free-to-paid conversion | 2% | 5% | 10% |
| Monthly churn (SMB) | 8% | 5% | 3% |
| Monthly churn (prosumer) | 10% | 7% | 4% |
| Trial-to-paid (14-day trial) | 10% | 20% | 35% |
| Annual plan discount uptake | 20% | 40% | 60% |
| Customer Acquisition Cost (organic) | $5 | $20 | $50 |
| Customer Acquisition Cost (paid) | $30 | $100 | $300 |
| LTV:CAC ratio (healthy) | 3:1 | 5:1 | 10:1 |

## Revenue Projection Template

```
Year 1 Projection:
  Target users (end of year): [X]
  Paying users (at conversion rate): [X * conversion%]
  MRR: [paying users * ARPU]
  ARR: [MRR * 12]
  Infrastructure costs: [$X/mo]
  Marketing costs: [$X/mo]
  Net annual: [ARR - (infra + marketing) * 12]

Year 3 Projection:
  Target users: [X, accounting for growth + churn]
  Paying users: [X * improved conversion%]
  MRR: [paying * ARPU (may increase with expansion revenue)]
  ARR: [MRR * 12]
  Net annual: [ARR - costs * 12]
```

## Cost Structure for Solopreneur SaaS

| Item | Typical Monthly Cost |
|------|---------------------|
| Hosting (Vercel/Netlify) | $0-20 |
| Database (Supabase/PlanetScale) | $0-25 |
| Authentication (Clerk/Auth0) | $0-25 |
| Email (Resend/Postmark) | $0-20 |
| Analytics (PostHog/Plausible) | $0-25 |
| Domain + DNS | $1-5 |
| AI API costs (Claude/OpenAI) | $10-100 |
| Payment processing (Stripe) | 2.9% + $0.30/txn |
| **Total baseline** | **$20-200/mo** |

Break-even users = Total monthly costs / ARPU

Example: $100/mo costs / $29 ARPU = 4 paying users to break even
