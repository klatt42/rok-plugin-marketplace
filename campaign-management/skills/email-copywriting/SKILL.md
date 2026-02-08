---
name: email-copywriting
description: |
  Email and SMS copywriting methodology for outreach campaigns.
  Subject line formulas, body structure, personalization levels (L1-L3),
  SMS character constraints, CTA rules, tone calibration, and A/B testing
  strategy for campaign message drafts.
triggers:
  - "email copy"
  - "subject line"
  - "write outreach"
  - "sms copy"
  - "write email"
  - "draft message"
  - "campaign copy"
  - "linkedin message"
version: 1.0
author: ROK Agency
---

# Email & SMS Copywriting

## Subject Line Formulas

### High-Performance Patterns (Email)

| Formula | Example | Open Rate Lift |
|---------|---------|---------------|
| Question + Name | "{{name}}, quick question?" | +15-20% |
| Company Reference | "Idea for {{company}}" | +10-15% |
| Mutual Connection | "Referred by [name]" | +25-30% |
| Curiosity Gap | "Noticed something about {{company}}" | +10-15% |
| Value Lead | "3 ways to improve [specific metric]" | +8-12% |
| Time-Bound | "This week only — for {{company}}" | +12-18% |

### Subject Line Rules
- **Length**: 4-7 words (mobile-optimized)
- **Personalization**: Always include `{{name}}` or `{{company}}`
- **Avoid**: ALL CAPS, excessive punctuation (!!!), spam words (FREE, URGENT)
- **Test**: Always A/B test subject lines before full send

## Body Structure

### Email Template (Cold Outreach)

```
[Opening — 1 sentence, personalized]
Hi {{name}}, I noticed {{company}} recently [specific observation].

[Value Proposition — 1-2 sentences]
We help [similar companies] achieve [specific result] by [method].

[Social Proof — 1 sentence, optional]
[Client name] saw a [metric]% improvement in [timeframe].

[CTA — 1 sentence, specific ask]
Would you have 15 minutes on [day] to discuss?

[Sign-off]
Best,
[Name]
```

### Word Count Targets

| Channel | Cold Outreach | Follow-Up | Nurture |
|---------|--------------|-----------|---------|
| Email | 50-100 words | 30-60 words | 100-200 words |
| SMS | 100-160 chars | 80-120 chars | N/A |
| LinkedIn | 100-200 chars | 80-150 chars | 200-300 chars |

## Personalization Levels

### L1 — Basic (Score: 40-60)
- Uses `{{name}}` and `{{company}}`
- Generic value proposition
- Suitable for large-scale campaigns

### L2 — Contextual (Score: 60-80)
- L1 + industry-specific language
- References company type or market position
- Includes role-appropriate content

### L3 — Research-Based (Score: 80-100)
- L2 + specific company observation
- References recent news, projects, or achievements
- Tailored value proposition to their situation
- Best for high-value targets

## CTA Rules

### Effective CTAs (Ranked)

1. **Specific time**: "Are you free Tuesday at 2pm?" (Best)
2. **Binary choice**: "Would a 15-min call or email exchange work better?"
3. **Low-commitment**: "Would it make sense to connect?"
4. **Interest check**: "Is this something {{company}} is exploring?"

### Weak CTAs (Avoid)
- "Let me know" (passive, no urgency)
- "Feel free to reach out" (puts burden on recipient)
- "I'd love to chat" (about you, not them)
- No CTA at all (what should they do?)

## SMS-Specific Constraints

- **160 character limit** for single segment
- Lead with value, not introduction
- Include clear CTA
- Avoid links in cold SMS (spam filters)
- Best for follow-ups and time-sensitive messages

### SMS Template
```
Hi {{name}}, [value statement in 1 line]. [Specific CTA]? - [Your name]
```

## Tone Calibration

| Audience | Tone | Language |
|----------|------|----------|
| C-Suite | Professional, concise, ROI-focused | "Revenue impact", "strategic advantage" |
| Managers | Helpful, solution-oriented | "Save time", "streamline", "team efficiency" |
| Technical | Direct, specific, proof-based | "Implementation", "integration", "metrics" |
| Small Business | Friendly, practical | "Grow", "simplify", "customers" |

## A/B Testing Strategy

### What to Test (Priority Order)
1. **Subject line** — Highest impact on opens
2. **CTA** — Highest impact on responses
3. **Opening line** — Affects read-through
4. **Length** — Short vs. detailed
5. **Send time** — Day of week and hour

### Testing Rules
- Only test ONE variable per test
- Minimum 20 sends per variant for meaningful data
- Winner = >10% lift in target metric
- Run test for minimum 48 hours before declaring winner
- Use `variant_group` and `variant_label` in template creation
