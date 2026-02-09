# Assumption Validation Gates

## Overview

Every business idea rests on assumptions. This framework catalogs assumptions, defines verification methods, sets pass/fail criteria, and establishes kill conditions. Based on the validation methodology from the Facebook Marketplace VouchedMarket analysis.

## Assumption Categories

| Category | Examples |
|----------|---------|
| **Market** | "Users will pay for this", "Demand exists beyond early adopters", "Market is growing" |
| **Technical** | "API access is available", "Data can be scraped legally", "Performance is achievable" |
| **Financial** | "Users will pay $29/mo", "CAC < $50", "Churn < 8%/mo" |
| **Competitive** | "No incumbent will copy this", "Switching costs protect us", "First-mover matters" |
| **Regulatory** | "No legal barriers", "Terms of service allow our approach", "Data privacy compliant" |

## Assumption Inventory Template

For each critical assumption:

```json
{
  "id": "A-001",
  "category": "market|technical|financial|competitive|regulatory",
  "assumption": "Clear statement of what you're assuming is true",
  "confidence": "LOW|MEDIUM|HIGH",
  "verification_method": "How to test this assumption",
  "pass_criteria": "Quantified threshold for success",
  "fail_criteria": "Quantified threshold for failure",
  "kill_condition": "If true, abandon the idea entirely",
  "current_status": "unverified|partially_verified|verified|failed",
  "evidence": "What we know so far",
  "estimated_cost_to_verify": "$X and Y hours",
  "priority": "Must verify before MVP | Should verify before launch | Can verify after launch"
}
```

## Confidence Levels

| Level | Meaning | Verification Need |
|-------|---------|-------------------|
| HIGH | Multiple data points confirm, industry standard | Monitor only |
| MEDIUM | Some evidence supports, but incomplete | Verify before significant investment |
| LOW | Gut feeling or single anecdote only | Must verify before any build work |

## Kill Criteria Examples

| Type | Kill Condition | Example |
|------|---------------|---------|
| Market kill | < 15% of surveyed users express interest | "Only 5% of sellers would pay for analytics" |
| Technical kill | Core feature is technically impossible or illegal | "Facebook actively blocks all extension approaches" |
| Financial kill | Unit economics don't work at any scale | "Infrastructure costs exceed possible revenue per user" |
| Competitive kill | Incumbent launches identical product | "Shopify releases free version of your exact idea" |
| Regulatory kill | Legal barrier prevents operation | "Platform TOS explicitly prohibits your approach" |

## Verification Methods

| Method | Cost | Speed | Reliability |
|--------|------|-------|------------|
| **WebSearch** (this plugin) | Free | Minutes | Moderate (directional) |
| **Landing page + waitlist** | $50-200 | 1-2 weeks | Good |
| **User interviews (5-10)** | $0-500 | 1-2 weeks | Very good |
| **Survey (50+ responses)** | $100-500 | 1-2 weeks | Good (if well-designed) |
| **Prototype/MVP test** | $0-2000 | 2-6 weeks | Excellent |
| **Paid ad test** | $100-500 | 3-7 days | Good for demand validation |
| **Competitor analysis** (this plugin) | Free | Minutes | Good for competitive assumptions |

## Strictness Levels

The `/idea-validate` command accepts a `--strictness` parameter:

| Level | Kill threshold | Pass threshold | Use when |
|-------|---------------|---------------|----------|
| lenient | Only critical kills | > 40% pass criteria | Early brainstorming |
| standard | Critical + high kills | > 60% pass criteria | Default analysis |
| strict | All severity kills | > 80% pass criteria | Before investing $$$  |

## Output Format

Present as a checklist:

```
## Assumption Validation Checklist

### Must Verify Before MVP
- [ ] A-001 [MARKET] Users will pay $29/mo for this tool
  - Method: Landing page + pricing test
  - Pass: > 3% click "Buy Now"
  - Kill: < 1% engagement
  - Status: UNVERIFIED

- [ ] A-002 [TECHNICAL] Platform API allows data access
  - Method: Build proof-of-concept
  - Pass: Core data accessible
  - Kill: All approaches blocked
  - Status: UNVERIFIED

### Should Verify Before Launch
- [ ] A-003 [FINANCIAL] CAC < $50 via content marketing
  - Method: Run $500 test campaign
  - Pass: CAC < $50
  - Kill: CAC > $200
  - Status: UNVERIFIED
```
