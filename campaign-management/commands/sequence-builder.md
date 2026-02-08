# Sequence Builder

You are creating multi-step drip sequences with delays and conditional triggers.

## Input

The user will provide:
- **Sequence name**: Descriptive name
- **Channel**: email, sms, or linkedin
- **Steps**: Template assignments with delays and conditions

## Process

### Step 1: Gather Information

Help the user design their sequence:

1. Ask for the channel and purpose (outreach, nurture, re-engagement)
2. List available templates with `list_templates(channel="...")`
3. Design the step flow with the user

### Step 2: Create or Select Templates

If the user needs new templates for any step, create them first using `create_template`.

### Step 3: Build the Sequence

```
create_sequence(
  name="...",
  channel="email",
  description="...",
  steps_json='[
    {"step_number": 1, "template_id": 1, "delay_days": 0, "condition": "always"},
    {"step_number": 2, "template_id": 2, "delay_days": 3, "condition": "if_not_responded"},
    {"step_number": 3, "template_id": 3, "delay_days": 7, "condition": "if_not_opened"}
  ]'
)
```

### Step 4: Confirm Creation

```
## Sequence Created

- **ID**: #[id]
- **Name**: [name]
- **Channel**: [channel]
- **Steps**: [count]

### Sequence Flow
| Step | Template | Delay | Condition | Preview |
|------|----------|-------|-----------|---------|
| 1 | Initial Outreach | Day 0 | Always | "Hi {{name}}..." |
| 2 | Follow-Up | Day 3 | If not responded | "Following up..." |
| 3 | Value-Add | Day 7 | If not opened | "I wanted to share..." |

### Next Steps
- Check sequence status: Use `get_sequence_status` tool
- Create a campaign using one of the sequence templates
```

## Conditions

| Condition | Meaning |
|-----------|---------|
| `always` | Send regardless of previous step outcome |
| `if_not_responded` | Only send if contact hasn't responded to any previous step |
| `if_not_opened` | Only send if contact hasn't opened any previous message |

## Rules

- Step numbers must be sequential starting from 1
- Delay days are cumulative from enrollment date (Day 0, Day 3, Day 7)
- Each step must reference an existing template
- Recommend 3-5 steps for outreach sequences
- Suggest increasing delay between steps (2-3 days, then 5-7 days)
- All templates in a sequence should use the same channel
