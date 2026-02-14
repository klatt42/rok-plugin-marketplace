# /intel-creators - Creator Watch List Management

Manage the watch list of content creators whose work is tracked for intelligence gathering. Creators on this list are prioritized during `/intel-scout` automated content discovery runs.

## Usage

```
/intel-briefing:intel-creators                                    # List all active creators
/intel-briefing:intel-creators list                               # Same as above
/intel-briefing:intel-creators stats                              # Aggregate statistics
/intel-briefing:intel-creators add "Name" --platform youtube --handle @handle --expertise "AI,Technology"
/intel-briefing:intel-creators remove "Name"                      # Deactivate creator (soft delete)
/intel-briefing:intel-creators update "Name" --trust-tier HIGH    # Update metadata
```

### Parameters
- **list** (default) - Show all active creators with ingestion stats
- **stats** - Show aggregate statistics across all creators
- **add** - Add new creator to watch list
  - Required: name, --platform (youtube, twitter, substack, blog, podcast, research)
  - Optional: --handle, --channel-url, --expertise (comma-separated), --trust-tier (HIGH/MEDIUM/STANDARD/LOW), --notes
- **remove** - Deactivate creator (soft delete, preserves history)
- **update** - Update creator metadata fields

Initial request: $ARGUMENTS

## Execution Steps

### Determine Mode

Parse $ARGUMENTS to determine which mode to execute:
- No args or "list" → Mode: List
- "stats" → Mode: Stats
- "add" followed by a name → Mode: Add
- "remove" followed by a name → Mode: Remove
- "update" followed by a name → Mode: Update

### Mode: List (default)

1. Query active creators from Supabase. Write a Python script to `/tmp/intel_creators_list.py`:

```python
import json, os, subprocess

url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_creators?active=eq.true&order=documents_ingested.desc,name',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
data = json.loads(result.stdout) if result.stdout else []

if isinstance(data, list):
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {data}")
```

Execute with `python3 /tmp/intel_creators_list.py` and parse the JSON response.

2. Display formatted table:

```
CREATOR WATCH LIST
==================
Active Creators: [N]

| # | Name           | Platform | Handle          | Expertise                    | Trust | Docs | Last Checked |
|---|----------------|----------|-----------------|------------------------------|-------|------|-------------|
| 1 | Andrei Jikh    | YouTube  | @AndreiJikh     | financial, geopolitical      | HIGH  | 4    | 2026-02-11  |
| 2 | Matt Berman    | YouTube  | @matthew_berman | technology, ai               | HIGH  | 2    | 2026-02-14  |
| 3 | Wes Roth       | YouTube  | @WesRoth        | technology, ai, policy       | MED   | 1    | 2026-02-14  |
| 4 | Nate Jones     | YouTube  | @NateBJones     | technology, ai               | MED   | 1    | 2026-02-12  |

Total documents from watched creators: [sum of documents_ingested]

COMMANDS:
  /intel-briefing:intel-creators add "Creator Name" --platform youtube --expertise "AI,Financial"
  /intel-briefing:intel-creators update "Andrei Jikh" --trust-tier HIGH
  /intel-briefing:intel-scout                    # Search for new content from these creators
```

3. If no active creators found:
```
No creators on watch list.

Add one with:
  /intel-briefing:intel-creators add "Creator Name" --platform youtube --handle @handle --expertise "Financial,AI"
```

### Mode: Stats

1. Query all active creators (same query as List mode).

2. Compute aggregated statistics from the response:
   - Count by platform
   - Count by trust tier
   - Sum documents_ingested
   - List domain expertise coverage (union of all expertise arrays)
   - Identify expertise gaps (check if financial, geopolitical, technology, labor are all covered)

3. Display:

```
CREATOR STATISTICS
==================
Total Active Creators: [N]

By Platform:
  YouTube:  [n]
  Twitter:  [n]
  Substack: [n]
  Blog:     [n]
  Podcast:  [n]
  Research: [n]

By Trust Tier:
  HIGH:     [n]
  MEDIUM:   [n]
  STANDARD: [n]
  LOW:      [n]

Top Creators by Documents:
  1. [Name] - [n] documents ([platform])
  2. [Name] - [n] documents ([platform])
  ...

Domain Expertise Coverage:
  Financial:    [n] creators  [✓ or ⚠ gap]
  Geopolitical: [n] creators  [✓ or ⚠ gap]
  Technology:   [n] creators  [✓ or ⚠ gap]
  AI:           [n] creators  [✓ or ⚠ gap]
  Labor:        [n] creators  [✓ or ⚠ gap]

Total Documents from Watched Creators: [total]

RECOMMENDATIONS:
  [If gaps found: "Consider adding creators covering [gap area] to strengthen [pillar] analysis."]
```

### Mode: Add

1. Parse the arguments:
   - Name: first quoted or unquoted argument after "add"
   - --platform: required (youtube, twitter, substack, blog, podcast, research)
   - --handle: optional @username
   - --channel-url: optional full URL
   - --expertise: optional comma-separated list (stored lowercase)
   - --trust-tier: optional (HIGH, MEDIUM, STANDARD, LOW; default STANDARD)
   - --notes: optional freeform text

2. Validate inputs:
   - Name must not be empty
   - Platform must be one of: youtube, twitter, substack, blog, podcast, research
   - Trust tier must be one of: HIGH, MEDIUM, STANDARD, LOW (if provided)

3. Check for duplicate. Write a Python script to `/tmp/intel_creators_check.py`:

```python
import json, os, subprocess, sys, urllib.parse

name = sys.argv[1]
url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

encoded_name = urllib.parse.quote(name)
cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_creators?name=ilike.{encoded_name}&active=eq.true&select=id,name,platform',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}'
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
data = json.loads(result.stdout) if result.stdout else []
if isinstance(data, list) and len(data) > 0:
    print(f"DUPLICATE:{json.dumps(data[0])}")
else:
    print("OK")
```

If duplicate found:
```
Creator "[name]" already exists on watch list (ID: [uuid]).
Use /intel-briefing:intel-creators update "[name]" to modify.
```

4. Insert new creator. Write a Python script to `/tmp/intel_creators_add.py`:

```python
import json, os, subprocess, sys

payload = json.loads(sys.argv[1])
url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

payload_path = '/tmp/creator_add_payload.json'
with open(payload_path, 'w') as f:
    f.write(json.dumps(payload))

cmd = [
    'curl', '-s',
    f'{url}/rest/v1/rok_intel_creators',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}',
    '-H', 'Content-Type: application/json',
    '-H', 'Prefer: return=representation',
    '-d', f'@{payload_path}'
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print(result.stdout)
```

The payload JSON should include:
```json
{
  "name": "[name]",
  "platform": "[platform]",
  "handle": "[handle or null]",
  "channel_url": "[url or null]",
  "domain_expertise": ["expertise1", "expertise2"],
  "trust_tier": "[tier]",
  "notes": "[notes or null]",
  "active": true,
  "documents_ingested": 0
}
```

5. Display confirmation:
```
CREATOR ADDED
=============
Name:      [name]
Platform:  [platform]
Handle:    [handle or "Not provided"]
URL:       [url or "Not provided"]
Expertise: [expertise list or "General"]
Trust:     [tier]
ID:        [uuid from response]

The scout will search for content from this creator during /intel-scout runs.

NEXT STEPS:
  /intel-briefing:intel-scout               # Search for new content now
  /intel-briefing:intel-creators list       # View updated watch list
```

### Mode: Remove

1. Parse the creator name from arguments.

2. Find the creator. Write a script similar to the duplicate check that searches by name (case-insensitive partial match).

3. If multiple matches, display them and ask user to specify:
```
Multiple creators match "[search]":
  1. [Creator A] (YouTube, 5 docs)
  2. [Creator B] (Twitter, 2 docs)

Which one to deactivate? (1/2/cancel)
```

4. Ask for confirmation:
```
Deactivate "[name]" from watch list?
  Platform: [platform]
  Documents Ingested: [n]

This will NOT delete their existing documents -- only stop tracking new content.
Proceed? (yes/no)
```

5. Set active=false. Write a Python script to `/tmp/intel_creators_remove.py`:

```python
import json, os, subprocess, sys

creator_id = sys.argv[1]
url = os.environ.get('ROK_SUPABASE_URL', '')
key = os.environ.get('ROK_SUPABASE_KEY', '')

cmd = [
    'curl', '-s', '-X', 'PATCH',
    f'{url}/rest/v1/rok_intel_creators?id=eq.{creator_id}',
    '-H', f'apikey: {key}',
    '-H', f'Authorization: Bearer {key}',
    '-H', 'Content-Type: application/json',
    '-H', 'Prefer: return=representation',
    '-d', json.dumps({"active": False})
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
print(result.stdout)
```

6. Display confirmation:
```
CREATOR DEACTIVATED
===================
[name] removed from active watch list.

Their [n] existing documents remain in the library.
To reactivate: /intel-briefing:intel-creators add "[name]" --platform [platform]
```

### Mode: Update

1. Parse the creator name and update flags:
   - --trust-tier: new trust tier value
   - --notes: new notes text
   - --expertise: new expertise list (replaces existing)
   - --handle: new handle
   - --channel-url: new URL
   - --platform: new platform

2. Find the creator (same logic as Remove mode).

3. Build update payload with only the provided fields. Write a Python script to `/tmp/intel_creators_update.py` that PATCHes only the changed fields.

4. Display confirmation:
```
CREATOR UPDATED
===============
[name] updated:
  [field]: [old value] -> [new value]
  [field]: [old value] -> [new value]
```

## Important Rules

- All Supabase operations MUST use Python scripts written to /tmp with `os.environ.get()` for credentials (damage control hooks block inline curl with env vars)
- Creators are ALWAYS soft-deleted (active=false), never hard-deleted
- All expertise keywords are stored LOWERCASE for consistency
- Platform values must match the CHECK constraint: youtube, twitter, substack, blog, podcast, research
- Trust tier values must match: HIGH, MEDIUM, STANDARD, LOW
- The `last_checked` field is updated by `/intel-scout`, not by this command
- The `documents_ingested` and `last_ingested` fields are updated by `/intel-ingest`, not by this command
- When listing, always order by documents_ingested DESC to show most-used creators first
