# Manage Templates

You are managing the template library: creating, listing, previewing templates, and setting up A/B test variants.

## Input

The user will request one of:
- **Create**: Write a new template
- **List**: Browse available templates
- **Preview**: See a rendered template with real or sample data
- **A/B Setup**: Create variant templates for testing

## Process

### Create Template

Gather the content and call:

```
create_template(
  name="...",
  channel="email",
  body="Hi {{name}},\n\n...",
  subject="Subject line for {{company}}",
  category="outreach",
  variant_group=null,
  variant_label=null
)
```

**Placeholder reference**: `{{name}}`, `{{email}}`, `{{phone}}`, `{{company}}`, `{{title}}`

### List Templates

```
list_templates(channel="email", category="outreach")
```

Present in a table:

```
## Templates ([count])

| # | Name | Channel | Category | Variant | Placeholders |
|---|------|---------|----------|---------|-------------|
| 1 | Initial Outreach | email | outreach | — | name, company |
```

### Preview Template

```
preview_template(
  template_id=1,
  contact_id=5
)
```

Or with sample data:

```
preview_template(
  template_id=1,
  sample_data='{"name": "Sarah Johnson", "company": "Acme Corp"}'
)
```

### A/B Test Setup

Create two (or more) variants with the same `variant_group`:

```
create_template(
  name="Outreach - Subject A",
  channel="email",
  subject="Quick question about {{company}}",
  body="...",
  variant_group="outreach_test_1",
  variant_label="A"
)

create_template(
  name="Outreach - Subject B",
  channel="email",
  subject="{{name}}, can we connect?",
  body="...",
  variant_group="outreach_test_1",
  variant_label="B"
)
```

## Rules

- Email templates should always have a subject line
- SMS templates should keep body under 160 characters
- LinkedIn templates should keep body under 300 characters
- Always show which placeholders are detected in the template
- For A/B tests, keep the body the same and vary only subject (or vice versa) for clean testing
- Category values: outreach, follow_up, nurture, conversion
