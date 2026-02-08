# Campaign Analytics

You are analyzing campaign performance: funnel metrics, channel comparison, A/B test results, and trends.

## Input

The user may provide:
- **Campaign ID** (specific campaign) or omit for aggregate
- **Channel** (email, sms, linkedin, or all — default: all)
- **Period** (7d, 30d, 90d, all — default: all)

## Process

### Step 1: Get Analytics Data

```
get_campaign_analytics(campaign_id=null, channel=null, period="all")
```

### Step 2: Render Analytics

```
## Campaign Analytics ([Period])

### Funnel Metrics
| Stage | Count | Rate |
|-------|-------|------|
| Total Messages | [total] | — |
| Sent | [sent] | [send_rate]% |
| Delivered | [delivered] | [delivery_rate]% |
| Opened | [opened] | [open_rate]% |
| Responded | [responded] | [response_rate]% |
| Converted | [converted] | [conversion_rate]% |
| Bounced | [bounced] | [bounce_rate]% |

### Channel Comparison
| Channel | Sent | Response Rate | Conversion Rate |
|---------|------|---------------|-----------------|
| Email | [sent] | [rate]% | [rate]% |
| SMS | [sent] | [rate]% | [rate]% |
| LinkedIn | [sent] | [rate]% | [rate]% |

### Campaign Performance
| Campaign | Channel | Sent | Responded | Converted | Response Rate |
|----------|---------|------|-----------|-----------|---------------|
| [name] | email | 45 | 12 | 5 | 26.7% |

### A/B Test Results
**Test Group: [group_name]**
| Variant | Template | Sent | Responded | Rate | Winner? |
|---------|----------|------|-----------|------|---------|
| A | [name] | 25 | 8 | 32.0% | WINNER (+15% lift) |
| B | [name] | 25 | 5 | 20.0% | |
```

### Step 3: Insights & Recommendations

Based on the data:
- Compare response rates across channels
- Identify best-performing campaigns and templates
- Report A/B test winners (>10% lift = statistically meaningful)
- Suggest optimizations for underperforming campaigns
- Recommend template changes based on open/response patterns

## Benchmarks

| Metric | Email | SMS | LinkedIn |
|--------|-------|-----|----------|
| Open Rate | 20-25% | N/A | N/A |
| Response Rate | 5-15% | 10-20% | 15-30% |
| Conversion Rate | 2-5% | 5-10% | 5-15% |
| Bounce Rate | <5% | <2% | <1% |

## Rules

- Always compare against benchmarks when data is available
- Flag campaigns performing 2x below benchmark
- A/B test winner requires >10% lift AND at least 10 sends per variant
- Format all rates as percentages with 1 decimal
- Show "Insufficient data" for metrics with <5 data points
