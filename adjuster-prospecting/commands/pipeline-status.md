# Pipeline Status

You are managing the adjuster relationship pipeline for Prism Specialties DMV. This command tracks outreach progress and surfaces follow-up actions.

## Pipeline Data

The pipeline is stored in `adjuster-pipeline.json` in the current working directory. If the file doesn't exist, create it when the user adds their first contact.

### Schema

```json
{
  "pipeline": [
    {
      "name": "John Smith",
      "carrier": "State Farm",
      "title": "Senior Field Adjuster",
      "territory": "Fairfax County, VA",
      "loss_types": ["fire", "water", "contents"],
      "stage": "outreach_sent",
      "linkedin_url": "https://linkedin.com/in/...",
      "contact_info": "jsmith@statefarm.com",
      "notes": "Handles large residential losses in NoVA",
      "outreach_channel": "linkedin",
      "date_identified": "2026-02-03",
      "date_last_action": "2026-02-03",
      "date_next_followup": "2026-02-06",
      "history": [
        {"date": "2026-02-03", "action": "Identified via LinkedIn search"},
        {"date": "2026-02-03", "action": "Sent LinkedIn connection request"}
      ]
    }
  ],
  "last_updated": "2026-02-03"
}
```

### Pipeline Stages

| Stage | Key |
|-------|-----|
| Identified | `identified` |
| Researched | `researched` |
| Outreach Sent | `outreach_sent` |
| Connected | `connected` |
| Meeting Scheduled | `meeting_scheduled` |
| Active Relationship | `active` |

## Commands

The user may ask to:

### View Pipeline
Show a summary dashboard:

```
## Adjuster Pipeline — [Date]

### By Stage
| Stage | Count | Names |
|-------|-------|-------|
| Identified | X | ... |
| Researched | X | ... |
| Outreach Sent | X | ... |
| Connected | X | ... |
| Meeting Scheduled | X | ... |
| Active | X | ... |

### By Carrier
| Carrier | Count | Stages |
|---------|-------|--------|
| State Farm | X | 2 outreach, 1 connected |
| ... | ... | ... |

### Overdue Follow-Ups
| Name | Carrier | Stage | Last Action | Overdue By |
|------|---------|-------|-------------|------------|
| ... | ... | ... | ... | X days |

### Suggested Next Actions
1. [Name] — Follow up (overdue by X days)
2. [Name] — Ready for outreach (researched, no contact yet)
3. [Name] — Schedule meeting (connected, no meeting set)

Total: [X] contacts across [Y] carriers
```

### Add Contact
When the user says "add [name] to the pipeline":
1. Create or update the entry in adjuster-pipeline.json
2. Set stage to `identified` (or whatever stage they specify)
3. Add a history entry with today's date
4. Set date_next_followup based on stage

### Update Contact
When the user says "move [name] to [stage]" or "update [name]":
1. Update the stage
2. Add a history entry
3. Recalculate next follow-up date:
   - `outreach_sent` → follow up in 3 days
   - `connected` → schedule meeting within 7 days
   - `meeting_scheduled` → follow up day after meeting
   - `active` → quarterly check-in (90 days)

### Remove Contact
When the user says "remove [name]":
1. Remove from pipeline
2. Confirm removal

## Follow-Up Rules

| Current Stage | Follow-Up Interval | Action |
|--------------|-------------------|--------|
| outreach_sent | 3 days | Send follow-up message |
| outreach_sent (2nd) | 7 days after first | Send second follow-up |
| outreach_sent (3rd) | 14 days after first | Final follow-up |
| connected | 7 days | Schedule intro call |
| meeting_scheduled | 1 day after meeting | Send thank you + recap |
| active | 90 days | Check-in, share relevant news |

## Rules

- Always read the existing `adjuster-pipeline.json` before making changes
- Never overwrite the file — merge changes with existing data
- Dates use ISO format (YYYY-MM-DD)
- When showing the pipeline, always highlight overdue follow-ups first
- Suggest specific actions, not generic reminders
- If the pipeline is empty, guide the user: "No contacts yet. Run `/adjuster-prospecting:find-adjusters [carrier]` to start building your pipeline."
