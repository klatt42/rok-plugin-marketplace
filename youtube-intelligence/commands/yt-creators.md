# /yt-creators - Manage Trusted Creator Profiles

View, add, update, and remove trusted YouTube creator profiles. Creator trust levels affect how recommendations are weighted in `/yt-analyze` output.

## Usage

```
/yt-creators                                          # List all creators
/yt-creators add channel:"Matt Wolfe" domain:"AI news, tool reviews" trust:"medium"
/yt-creators remove channel:"Matt Wolfe"
/yt-creators update channel:"Chris Koerner" domain:"AI tools, claude code, automation"
```

### Parameters
- **(no args)** - Display all configured creators
- **add** - Add a new creator: `channel:"Name" domain:"domain1, domain2" trust:"high|medium"` notes:"optional notes"
- **remove** - Remove a creator: `channel:"Name"`
- **update** - Update a creator: `channel:"Name"` plus any fields to change (`domain:`, `trust:`, `notes:`, `aliases:`)

## Execution Steps

### Step 1: Load Creator Registry

Read `~/.claude/youtube-intelligence/creators.json`.

If the file does not exist, create it with the default registry:
```json
{
  "channels": [
    {
      "name": "Cole Medin",
      "aliases": ["coleam00"],
      "domains": ["ai-agents", "claude-code", "mcp", "prd-methodology", "bolt-new", "windsurf"],
      "trust": "HIGH",
      "notes": "ROK methodology source. Quoted in CLAUDE.md. 'The PRD is the north star.'",
      "added": "2026-02-06",
      "videos_analyzed": 0
    },
    {
      "name": "IndyDevDan",
      "aliases": [],
      "domains": ["agentic-workflows", "claude-code-cli", "claude-md-patterns", "task-automation", "ai-agents"],
      "trust": "HIGH",
      "notes": "Agentic patterns authority. Quoted in CLAUDE.md. 'Agents + code beats agents alone.'",
      "added": "2026-02-06",
      "videos_analyzed": 0
    },
    {
      "name": "Chris Koerner",
      "aliases": [],
      "domains": ["ai-tools", "agentic-workflows", "ai-automation"],
      "trust": "HIGH",
      "notes": "AI tools and agentic workflow insights.",
      "added": "2026-02-06",
      "videos_analyzed": 0
    }
  ]
}
```

### Step 2: Execute Action

#### List (no args)

Display all creators in a formatted table:

```markdown
## Trusted Creator Profiles

| # | Channel | Trust | Domains | Videos Analyzed | Added |
|---|---------|-------|---------|-----------------|-------|
| 1 | Cole Medin | HIGH | AI agents, Claude Code, MCP, PRD | 0 | 2026-02-06 |
| 2 | IndyDevDan | HIGH | Agentic workflows, Claude Code CLI | 0 | 2026-02-06 |
| 3 | Chris Koerner | HIGH | AI tools, agentic workflows | 0 | 2026-02-06 |

### Trust Levels
- **HIGH** (0.85-1.0): Recognized authority. Patterns already adopted into ROK.
- **MEDIUM** (0.55-0.75): Known expert, consistent quality, relevant domain.
- **STANDARD** (0.25-0.45): Default for unrecognized creators. Not listed here.

### Quick Actions
- Add a creator: `/yt-creators add channel:"Name" domain:"domains" trust:"high"`
- Update a creator: `/yt-creators update channel:"Name" domain:"new domains"`
- Remove a creator: `/yt-creators remove channel:"Name"`
```

#### Add

1. Validate required fields: `channel` and `domain` are required, `trust` defaults to "MEDIUM"
2. Check for duplicates (case-insensitive name match)
3. If duplicate found, suggest using `update` instead
4. Create new entry:
   ```json
   {
     "name": "[channel value]",
     "aliases": [],
     "domains": ["[parsed from domain value]"],
     "trust": "[HIGH or MEDIUM]",
     "notes": "[notes value or empty]",
     "added": "[today's date]",
     "videos_analyzed": 0
   }
   ```
5. Append to channels array
6. Save the file
7. Display confirmation with the new creator's entry

#### Remove

1. Find the creator by name (case-insensitive)
2. If not found, list available creators and ask which to remove
3. Confirm before removing: "Remove [name] from trusted creators? This does not delete any analysis history."
4. Remove from channels array
5. Save the file
6. Display confirmation

#### Update

1. Find the creator by `channel` name (case-insensitive)
2. If not found, list available creators
3. Update only the specified fields (leave others unchanged)
4. Parse domain string into array if domain is updated
5. Save the file
6. Display the updated entry

### Step 3: Persist Changes

Write the updated registry back to `~/.claude/youtube-intelligence/creators.json`.

### Step 4: Suggest Memory Sync

After any change, offer:
```
Save creator preferences to ROK memory?
/memory-write category:"preference" key:"yt-trusted-creators" value:"[creator list summary]"
```

## Important Rules

- Never delete the registry file, only modify entries within it
- Always confirm before removing a creator
- Domain values should be lowercase, hyphenated (e.g., "ai-agents", "claude-code")
- Trust values are case-insensitive on input but stored as uppercase
- The `videos_analyzed` counter is managed by `/yt-analyze`, not by this command
