---
name: intel-creators
description: |
  Creator watch list management for the intel-briefing system. Manage the list
  of content creators whose work is tracked for intelligence gathering. Creators
  on this list are prioritized during /intel-scout automated discovery runs.
triggers:
  - "intel creators"
  - "creator watch list"
  - "manage creators"
  - "add creator"
  - "content sources"
  - "watched creators"
version: 1.2
author: ROK Agency
---

# Intel Creators

Manage the creator watch list for intelligence gathering.

## Usage

```
/intel-briefing:intel-creators                                    # List all active creators
/intel-briefing:intel-creators stats                              # Aggregate statistics
/intel-briefing:intel-creators add "Name" --platform youtube --handle @handle --expertise "AI,Technology"
/intel-briefing:intel-creators remove "Name"                      # Deactivate creator
/intel-briefing:intel-creators update "Name" --trust-tier HIGH    # Update metadata
```

## When to Use

- Adding new content creators to the intelligence watch list
- Reviewing which creators are being tracked and their reliability
- Updating trust tiers based on prediction accuracy
