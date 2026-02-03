# /session-end - Harness-Pattern Session Completion

Implements Anthropic's agent harness shutdown protocol for reliable handoff to next session.

## What This Does

1. **Summarizes Work**: Documents what was accomplished
2. **Updates Progress File**: Appends structured entry to `claude-progress.txt`
3. **Updates Feature List**: Marks features done/in-progress in `feature_list.json`
4. **Commits Checkpoint**: Creates git commit with session work
5. **Captures Learnings**: Triggers `/diary` for pattern extraction
6. **Validates Handoff**: Confirms next session can recover context

## Usage

```
/session-end
```

Or with summary provided:
```
/session-end summary:"Completed OAuth flow, tests passing"
```

## The 7-Step Shutdown Protocol

### Step 1: Work Summary

Analyze the current session to identify:

**What was completed?**
- Features finished and passing validation
- Bugs fixed
- Refactoring done

**What's in progress?**
- Features started but not complete
- Percentage estimate
- What remains to be done

**What blockers exist?**
- External dependencies
- Unclear requirements
- Technical issues

**What decisions were made?**
- Architecture choices
- Library selections
- Approach changes

### Step 2: Update Progress File

Append a structured entry to `claude-progress.txt`:

```markdown
[YYYY-MM-DD HH:MM] Session Summary
- Completed: <feature-ids, comma-separated>
- In Progress: <feature-id> (<percentage>%, <what's pending>)
- Blockers: <any blocking issues or "None">
- Decisions: <key choices with brief rationale>
- Next Session: <specific action items>
```

**Example:**
```markdown
[2025-12-19 16:45] Session Summary
- Completed: session-start-cmd, session-end-cmd
- In Progress: init-sh-template (70%, needs service health checks)
- Blockers: None
- Decisions: Using Anthropic's exact progress file format for compatibility
- Next Session: Complete init.sh, create claude-progress.txt for rok-copilot, test full workflow
```

### Step 3: Update Feature List

Modify `feature_list.json` to reflect current status:

```javascript
// Mark completed features
feature.status = "done"
feature.session_completed = "YYYY-MM-DD"

// Update in-progress features
feature.status = "in-progress"
feature.session_started = "YYYY-MM-DD"  // if newly started
// Add notes about progress if helpful
```

**Validation:**
- Only mark "done" if ALL validation steps pass
- If validation steps fail, keep as "in-progress"
- Never mark done without testing

### Step 4: Create Git Checkpoint

Commit all work with descriptive message:

```bash
git add .
git commit -m "[ROK] Session: <brief summary>

Completed:
- <feature or task>
- <feature or task>

In Progress:
- <feature> (<what remains>)

Next: <what the next session should do>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit conventions:**
- Prefix: `[ROK]` for session commits
- Include completion status
- Note what's next for future context
- Always include Co-Author

### Step 5: Update Active Projects Registry

Update `~/.claude/active-projects.json` with session information:

```bash
# Find and update the current project entry
# Update lastSessionEnd timestamp
# Update lastContext with brief summary
```

**Fields to update:**
```json
{
  "lastSessionEnd": "2025-12-26T16:45:00Z",
  "lastContext": "Completed OAuth flow, tests passing"
}
```

**How to update (without jq):**
Use sed to update the fields for the current project:

```bash
# Get current timestamp
TIMESTAMP=$(date -Iseconds)

# Update lastSessionEnd for current project
# (Manual edit or sed replacement)
```

**Why this matters:**
- `rok-init` shows last session dates
- `rok-restore` uses this for prioritization
- Cross-session tracking without reading progress files

### Step 6: Capture Learnings (Optional)

If the session involved:
- Solving difficult problems
- Making important decisions
- Discovering new patterns
- Learning about user preferences

Then run:
```
/diary
```

This captures learnings for `/reflect` to synthesize later.

### Step 7: Validate Handoff

Confirm the next session can recover context:

```
Handoff Validation Checklist

[x] claude-progress.txt updated with this session
[x] feature_list.json reflects current status
[x] Git commit created with session work
[x] active-projects.json updated with session end time
[x] No uncommitted changes remain
[x] Services can be restarted via init.sh
[x] Next session has clear action items

Session End Complete

Next session should run:
  /session-start

Expected behavior:
  - Will load progress from claude-progress.txt
  - Will select: <feature-id> as next task
  - Will run init.sh to start services
  - Ready to continue: <specific next step>
```

## Progress File Maintenance

### Entry Format

Each session appends one entry:

```markdown
[YYYY-MM-DD HH:MM] Session Summary
- Completed: <feature-ids>
- In Progress: <feature-id> (<details>)
- Blockers: <issues or "None">
- Decisions: <choices made>
- Next Session: <action items>
```

### File Size Management

When `claude-progress.txt` exceeds 500 lines:

1. Archive older entries to `claude-progress-archive-YYYY.txt`
2. Keep last 10 sessions in main file
3. Maintain header with project name

```bash
# Archive old entries
tail -n +50 claude-progress.txt >> claude-progress-archive-2025.txt
head -n 50 claude-progress.txt > claude-progress.txt.tmp
mv claude-progress.txt.tmp claude-progress.txt
```

### Git Tracking

The progress file should be committed:
```bash
git add claude-progress.txt
git commit -m "[ROK] Progress update: session end"
```

This allows git log to show session history:
```bash
git log --oneline --grep="ROK" -- claude-progress.txt
```

## Feature List Updates

### Marking Features Complete

Only mark a feature "done" when:

1. **All validation steps pass** - manually tested or automated
2. **No regressions** - existing features still work
3. **Code committed** - changes are in git

```json
{
  "id": "auth-oauth",
  "status": "done",
  "session_completed": "2025-12-19",
  "validation_notes": "All 4 steps passing, tested with Google account"
}
```

### Updating In-Progress Features

For partially complete work:

```json
{
  "id": "dashboard-analytics",
  "status": "in-progress",
  "session_started": "2025-12-19",
  "progress_notes": "60% - Charts rendering, need to add date filters"
}
```

### Adding New Features

If you discovered new requirements during the session:

```json
{
  "id": "auth-refresh-token",
  "category": "authentication",
  "description": "Automatically refresh OAuth tokens before expiry",
  "validation_steps": [
    "Token expires after 1 hour",
    "Background refresh happens at 55 minutes",
    "User session continues without interruption"
  ],
  "dependencies": ["auth-oauth"],
  "priority": 2,
  "status": "todo",
  "discovered": "2025-12-19",
  "discovery_context": "Found during OAuth implementation - tokens expire"
}
```

## Integration with ROK 3.0

### Command Sequence

```
/session-start → Work → /diary (optional) → /session-end
      ↓                                           ↓
Load context                              Save context
Select task                               Update progress
Start services                            Commit checkpoint
```

### Cross-Platform Continuity

Since `claude-progress.txt` is:
- A plain text file in the project
- Committed to git
- Read by `/session-start`

Any Claude interface can:
1. Pull latest from git
2. Run `/session-start`
3. Have full context

### Relationship to /diary

| Command | When | What |
|---------|------|------|
| `/session-end` | Every session end | Progress tracking, handoff |
| `/diary` | When learning occurred | Pattern capture, decisions |

Both can run at session end:
```
/diary
/session-end
```

## Output Format

```
Session End Summary

Project: rok-copilot
Duration: ~2 hours
Date: 2025-12-19

Completed This Session:
- [x] session-start command created
- [x] session-end command created

In Progress:
- [ ] init.sh template (70%)

Blockers:
- None

Decisions Made:
- Using Anthropic's progress file format for harness compatibility
- Keeping feature_list.json separate from rok_tasks.json for now

Progress File Updated:
- claude-progress.txt: Entry appended

Feature List Updated:
- session-start-cmd: todo → done
- session-end-cmd: todo → done
- init-sh-template: todo → in-progress

Git Commit:
- Hash: abc1234
- Message: [ROK] Session: Harness pattern commands

Next Session Should:
1. Run /session-start
2. Complete init.sh template
3. Create claude-progress.txt for rok-copilot
4. Test full startup/shutdown workflow

Handoff: READY
```

## Troubleshooting

### Uncommitted Changes

If git shows uncommitted changes:
```bash
git status
git add .
git commit -m "[ROK] Session work in progress"
```

### Feature List Missing

Create minimal feature list:
```bash
echo '{"project": "'$(basename $PWD)'", "features": []}' > feature_list.json
```

### Progress File Corrupted

Reset with clean header:
```bash
echo "# Claude Progress Log - $(basename $PWD)" > claude-progress.txt
```

### Services Still Running

Document in progress file for next session:
```
- Note: Dev server left running on :3006
```

Or stop them:
```bash
pkill -f "next dev" 2>/dev/null
```

## Why This Matters

From Anthropic's harness research:

> "Agents are stateful and errors compound. Build systems that can resume from where the agent was when errors occurred."

Without clean session ends:
- Progress is lost in context compaction
- Next session starts from scratch
- Features incorrectly marked complete
- Handoff between tools fails

With clean session ends:
- Every session builds on the last
- Clear trail of decisions and progress
- Reliable cross-platform continuity
- Errors caught before they compound

---

**Session End Command v1.1** | ROK 3.0 Harness Pattern + Multi-Terminal Restoration
