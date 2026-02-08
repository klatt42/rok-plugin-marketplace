# Campaign Export

You are exporting campaign results to professional Excel and PDF reports with orange branding.

## Input

The user may provide:
- **Campaign ID** or campaign name
- **Format**: Excel, PDF, or both (default: both)

## Process

### Step 1: Get Campaign Data

Call `get_campaign` with messages and `get_campaign_analytics`:

```
get_campaign(campaign_id=..., include_messages=true)
get_campaign_analytics(campaign_id=...)
```

### Step 2: Prepare Export Data

Construct a JSON payload for the export script:

```json
{
  "type": "campaign",
  "campaign_name": "[name]",
  "carrier": "[Campaign Name]",
  "region": "Campaign Report",
  "date": "[YYYY-MM-DD]",
  "report_type": "Campaign",
  "search_summary": "Campaign export: [name] — [sent] sent, [response_rate]% response rate",
  "campaign": {
    "id": 1,
    "name": "[name]",
    "channel": "[channel]",
    "status": "[status]",
    "template_name": "[template]",
    "contact_list_name": "[list]",
    "created_at": "[date]"
  },
  "funnel": {
    "total": 50,
    "sent": 45,
    "delivered": 42,
    "opened": 28,
    "responded": 12,
    "converted": 5,
    "bounced": 3,
    "failed": 2
  },
  "messages": [
    {
      "contact_name": "[name]",
      "contact_email": "[email]",
      "contact_company": "[company]",
      "status": "[status]",
      "rendered_subject": "[subject]",
      "sent_at": "[date]",
      "opened_at": "[date]",
      "responded_at": "[date]"
    }
  ],
  "ab_tests": {},
  "analysis": "[Summary of campaign performance]",
  "next_steps": ["[action 1]", "[action 2]"]
}
```

### Step 3: Run Export

Write the JSON to a temp file and run the export:

```bash
cat > /tmp/campaign_export.json << 'EXPORT_EOF'
{ ... the JSON payload ... }
EXPORT_EOF

~/.claude/scripts/.venv/bin/python3 ~/.claude/scripts/prospecting_export.py \
  --input /tmp/campaign_export.json

rm /tmp/campaign_export.json
```

### Step 4: Report Output

```
## Export Complete

- **Excel**: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Campaign_Reports/[filename].xlsx
- **PDF**: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Campaign_Reports/[filename].pdf
- **Messages Exported**: [count]
- **Response Rate**: [rate]%
```

## Rules

- Include full message-level detail in the Excel export
- Group messages by status in the Excel sheet
- Include funnel visualization in the PDF
- Show A/B test results if variants were used
- Use campaign orange branding (#EA580C)
