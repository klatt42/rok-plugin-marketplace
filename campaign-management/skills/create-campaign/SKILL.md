---
name: create-campaign
description: |
  Create a new outreach campaign linking a template to a contact list.
  Generates draft messages for each contact with personalization variables.
triggers:
  - "create campaign"
  - "new campaign"
  - "start campaign"
  - "launch campaign"
  - "setup campaign"
version: 1.2
author: ROK Agency
---

# Create Campaign

Create a new outreach campaign linking a template to a contact list.

## Usage

```
/campaign-management:create-campaign                # Interactive mode
/campaign-management:create-campaign name:"Q1 Outreach" channel:email
```

## When to Use

- When you need to invoke /campaign-management:create-campaign
- When the user's request matches the trigger keywords above
