---
name: manage-contacts
description: |
  Manage the contact database: search, create, import, and organize contacts
  into lists. Supports bulk import and tag-based organization.
triggers:
  - "manage contacts"
  - "contact list"
  - "add contact"
  - "import contacts"
  - "search contacts"
version: 1.2
author: ROK Agency
---

# Manage Contacts

Manage the contact database: search, create, import, and organize contacts

## Usage

```
/campaign-management:manage-contacts search:"John"  # Search contacts
/campaign-management:manage-contacts                # Interactive mode
```

## When to Use

- When you need to invoke /campaign-management:manage-contacts
- When the user's request matches the trigger keywords above
