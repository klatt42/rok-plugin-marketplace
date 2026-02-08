# Manage Contacts

You are managing the contact database: searching, creating, importing, and organizing contacts into lists.

## Input

The user will request one of:
- **Search**: Find contacts by name, email, company, tags
- **Create**: Add a new contact
- **Import**: Bulk import from a list or JSON
- **List management**: Create lists, add contacts to lists

## Process

### Search Contacts

```
search_contacts(query="...", company="...", tags="...", status="active", limit=50)
```

Present results in a table:

```
## Contacts Found ([count])

| # | Name | Email | Company | Title | Status | Tags |
|---|------|-------|---------|-------|--------|------|
| 1 | [name] | [email] | [company] | [title] | active | [tags] |
```

### Create Contact

Gather required fields and call:

```
create_contact(
  name="...",
  email="...",
  phone="...",
  company="...",
  title="...",
  tags='["tag1", "tag2"]',
  source="manual",
  notes="..."
)
```

### Import Contacts

For bulk import, format the data as JSON and call:

```
import_contacts(
  contacts_json='[{"name": "...", "email": "...", "company": "...", ...}]',
  source="import",
  auto_create_list=true,
  list_name="Import - [date]"
)
```

### Create Contact List

```
create_contact_list(
  name="...",
  description="...",
  contact_ids='[1, 2, 3]'
)
```

### Add to List

```
add_to_list(list_id=..., contact_ids='[1, 2, 3]')
```

## Rules

- Always show contact count in search results
- When importing, suggest creating an auto-list for easy campaign targeting
- Tags should be JSON arrays: `["decision_maker", "warm_lead"]`
- Default source is "manual" for individual creates, "import" for bulk
- Warn if importing contacts without email addresses (needed for email campaigns)
