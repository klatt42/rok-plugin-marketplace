# Create Campaign

You are creating a new outreach campaign that links a template to a contact list and generates draft messages for each contact.

## Input

The user will provide some or all of:
- **Campaign name**: Descriptive name for the campaign
- **Channel**: email, sms, or linkedin (default: email)
- **Template**: Template name or ID to use
- **Contact list**: List name or ID to target
- **Scheduled date**: When to send (optional)

## Process

### Step 1: Gather Information

If the user hasn't specified all required fields:
1. List available templates using `list_templates` (filtered by channel if specified)
2. List available contact lists — query contact_lists from search_contacts or create_contact_list
3. Ask which template and list to use

### Step 2: Create the Campaign

Call `create_campaign` with the gathered information:

```
create_campaign(
  name="...",
  channel="email",
  template_id=...,
  contact_list_id=...,
  scheduled_at="YYYY-MM-DD",
  notes="..."
)
```

This automatically generates draft messages for each active contact in the list, with placeholders rendered from contact data.

### Step 3: Confirm Creation

Present the result:

```
## Campaign Created

- **ID**: #[id]
- **Name**: [name]
- **Channel**: [channel]
- **Template**: [template_name]
- **Contact List**: [list_name]
- **Messages Generated**: [count]
- **Status**: Draft

### Sample Messages
[Show 2-3 rendered message previews]

### Next Steps
- View campaign: `/campaign-management:campaign-dashboard`
- Update message statuses: Use `update_message_status` as you send/track
- View analytics: `/campaign-management:campaign-analytics`
```

## Rules

- Default channel is `email` unless specified
- Only active contacts (not unsubscribed/bounced/invalid) get messages
- Always show a few sample rendered messages so the user can verify personalization
- Campaign starts in `draft` status
