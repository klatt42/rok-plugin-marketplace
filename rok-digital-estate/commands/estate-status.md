# /estate-status - Quick Estate Status Check

Quick read-only status from the most recent digital estate snapshot. Does not run any agents or scan any sources -- just reads the latest snapshot file.

## Usage

```
/rok-digital-estate:estate-status                # Full summary
/rok-digital-estate:estate-status section:1      # Executive Summary only
/rok-digital-estate:estate-status section:2      # Bus Factor Dashboard only
/rok-digital-estate:estate-status section:3      # Project Inventory only
/rok-digital-estate:estate-status section:4      # Deployment Map only
/rok-digital-estate:estate-status section:5      # Infrastructure & Hosting only
/rok-digital-estate:estate-status section:6      # Subscriptions & Costs only
/rok-digital-estate:estate-status section:7      # Access Guide only
/rok-digital-estate:estate-status section:8      # ROK Memory Highlights only
/rok-digital-estate:estate-status section:9      # Contact List only
/rok-digital-estate:estate-status section:10     # Quick Start only
```

### Parameters
- **section** - Display only the specified section number (1-10)

Initial request: $ARGUMENTS

## Execution Steps

### Phase 1: Find Latest Snapshot

1. Find the most recent snapshot file:
   ```bash
   LATEST=$(ls ~/projects/rok-copilot/estate-snapshots/*_estate-snapshot_v*.md 2>/dev/null | sort -V | tail -1)
   echo "FILE: $LATEST"
   ```

2. If no snapshot found:
   ```
   No estate snapshot found.
   Generate one: /rok-digital-estate:generate-snapshot
   ```
   Stop here.

3. Extract metadata from filename:
   - Version number from `_v[N].`
   - Date from `YYYY-MM-DD_` prefix
   - File age from modification time

### Phase 2: Display Status

1. Read the snapshot file:
   ```bash
   cat "$LATEST"
   ```

2. If `section:` parameter is specified:
   - Parse the markdown and extract only the requested section (by `## N.` header)
   - Display that section only

3. If no section specified, display a condensed summary:
   ```
   =========================================
   ESTATE STATUS
   =========================================
   Version: v[N]
   Generated: [date]
   Age: [X days/hours ago]

   Estate Health: [from executive summary]
   Total Projects: [count]
   Live Deployments: [count]
   Monthly Burn: $[total]
   Critical Items: [count]

   Quick Actions Needed:
   - [CRITICAL item 1]
   - [CRITICAL item 2]

   To view full snapshot: /rok-digital-estate:estate-status section:1
   To regenerate: /rok-digital-estate:generate-snapshot refresh
   =========================================
   ```

## Important Rules

- This is a READ-ONLY command -- no agents, no scanning, no modifications
- If no snapshot exists, suggest generating one
- Parse the markdown carefully to extract section boundaries
- Display file age to help user decide if regeneration is needed
- Show CRITICAL tier items prominently in the summary view
