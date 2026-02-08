---
name: campaign-strategy
description: |
  Campaign strategy methodology for segmentation, drip sequence design,
  A/B testing methodology, send time optimization, response handling,
  and channel benchmarks for email, SMS, and LinkedIn campaigns.
triggers:
  - "campaign strategy"
  - "drip sequence"
  - "ab test"
  - "segmentation"
  - "campaign plan"
  - "outreach strategy"
  - "send timing"
  - "response handling"
version: 1.0
author: ROK Agency
---

# Campaign Strategy

## Segmentation Dimensions

### Primary Segments

| Dimension | Values | Use Case |
|-----------|--------|----------|
| Relationship Stage | Cold, Warm, Hot, Customer | Message tone and depth |
| Role/Title | C-Suite, Manager, IC, Owner | Language and value prop |
| Industry | Restoration, Insurance, Construction | Industry-specific references |
| Company Size | Enterprise, Mid-Market, SMB | Solution positioning |
| Engagement Level | New, Engaged, Dormant, Churned | Re-engagement strategy |

### Segmentation Rules
- Start broad, narrow based on response data
- Minimum segment size: 20 contacts (for meaningful metrics)
- Tag contacts with segments using the `tags` field: `["warm_lead", "c_suite", "restoration"]`
- Create dedicated contact lists per segment for targeted campaigns

## Drip Sequence Design

### Standard Outreach (Cold)

| Step | Day | Template Type | Condition | Purpose |
|------|-----|--------------|-----------|---------|
| 1 | 0 | Introduction | Always | Open the door |
| 2 | 3 | Follow-Up | If not responded | Show persistence |
| 3 | 7 | Value-Add | If not responded | Provide value, different angle |
| 4 | 14 | Social Proof | If not responded | Build credibility |
| 5 | 21 | Breakup | If not responded | Create urgency, graceful close |

### Warm Outreach (Referral/Inbound)

| Step | Day | Template Type | Condition | Purpose |
|------|-----|--------------|-----------|---------|
| 1 | 0 | Personal Connect | Always | Leverage warm intro |
| 2 | 2 | Value Proposition | If not responded | Share specific value |
| 3 | 5 | Case Study | If not responded | Provide social proof |

### Re-Engagement (Dormant)

| Step | Day | Template Type | Condition | Purpose |
|------|-----|--------------|-----------|---------|
| 1 | 0 | Check-In | Always | Reconnect casually |
| 2 | 5 | New Value | If not responded | Share something new |
| 3 | 12 | Final Touch | If not responded | Last attempt |

### Cadence Rules
- **Email**: Minimum 2-3 days between touches
- **SMS**: Minimum 5-7 days between touches
- **LinkedIn**: Minimum 3-5 days between touches
- **Multi-channel**: Alternate channels for variety
- **Max sequence length**: 5-7 steps (beyond that, diminishing returns)

## A/B Testing Methodology

### Test Design

1. **Hypothesis**: "Changing [variable] will improve [metric] because [reason]"
2. **Variable**: Only ONE change per test
3. **Sample size**: Minimum 20 per variant (ideally 50+)
4. **Duration**: Run for 48-72 hours minimum
5. **Winner criteria**: >10% lift in target metric

### What to Test (Priority)

| Priority | Variable | Metric to Watch |
|----------|----------|----------------|
| 1 | Subject line | Open rate |
| 2 | CTA phrasing | Response rate |
| 3 | Send time | Open rate |
| 4 | Body length | Response rate |
| 5 | Personalization level | Response rate |

### Implementation
- Use `variant_group` to link related templates
- Use `variant_label` (A, B, control) to identify variants
- Create separate campaigns per variant with similar-sized list segments
- Analytics tool automatically groups and compares variants

## Send Time Optimization

### Best Send Times by Channel

| Channel | Best Days | Best Times | Worst Times |
|---------|-----------|------------|-------------|
| Email | Tue, Wed, Thu | 9-11am, 1-3pm | Mon AM, Fri PM, Weekends |
| SMS | Tue, Wed | 10-11am, 2-3pm | Before 9am, After 6pm |
| LinkedIn | Tue, Wed, Thu | 8-10am, 5-6pm | Weekends, Late night |

### Time Zone Considerations
- Default to recipient's local time zone
- If unknown, use ET for East Coast, PT for West Coast
- Schedule sends to arrive during business hours

## Response Handling

### Status Flow

```
pending → sent → delivered → opened → responded → converted
                                   ↘ bounced
                                   ↘ failed
```

### Response Actions

| Response Type | Status Update | Next Action |
|---------------|--------------|-------------|
| Positive reply | responded | Move to conversion flow |
| Meeting request | responded → converted | Schedule and confirm |
| Question/interest | responded | Answer and follow up |
| Not interested | responded | Mark, pause sequence |
| Out of office | Keep current | Retry after return date |
| Bounce | bounced | Verify email, update contact |
| No response (3+ steps) | Keep pending | Move to re-engagement |

## Channel Benchmarks

### Email Benchmarks

| Metric | Cold Outreach | Warm Outreach | Nurture |
|--------|--------------|---------------|---------|
| Open Rate | 15-25% | 30-45% | 20-35% |
| Response Rate | 5-15% | 15-30% | 10-20% |
| Conversion Rate | 2-5% | 8-15% | 5-10% |
| Bounce Rate | <5% | <2% | <2% |
| Unsubscribe | <1% | <0.5% | <0.5% |

### SMS Benchmarks

| Metric | Cold | Warm | Re-engagement |
|--------|------|------|---------------|
| Response Rate | 10-20% | 25-40% | 15-25% |
| Conversion Rate | 5-10% | 15-25% | 8-15% |
| Opt-Out Rate | <3% | <1% | <2% |

### LinkedIn Benchmarks

| Metric | Cold | Warm (2nd degree) | InMail |
|--------|------|-------------------|--------|
| Accept Rate | 20-35% | 40-60% | 15-25% |
| Response Rate | 15-30% | 30-50% | 10-20% |
| Conversion Rate | 5-15% | 15-25% | 5-10% |

## Campaign Planning Checklist

1. Define goal (meetings booked, responses, conversions)
2. Select and segment target audience
3. Choose channel(s) based on audience preference
4. Design sequence with appropriate cadence
5. Write templates with L2+ personalization
6. Set up A/B test for subject line or CTA
7. Create campaign and review draft messages
8. Track progression through funnel
9. Analyze results against benchmarks
10. Iterate based on performance data
