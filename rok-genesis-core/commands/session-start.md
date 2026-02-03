# /session-start - Harness-Pattern Session Initialization

Implements Anthropic's agent harness startup ritual for reliable context recovery across sessions.

## What This Does

0. **ROK Infrastructure Check**: Verify CLAUDE.md and core files exist (run `/project-init` if missing)
1. **Documentation Currency Check**: Verify Claude Code version and scan for new capabilities
2. **Confirms Working Directory**: Verifies you're in the right project
3. **Loads Progress State**: Reads `claude-progress.txt` for last session context
3. **Loads Feature List**: Reads `feature_list.json` for current priorities
4. **Runs Init Script**: Executes `./init.sh` to start services
5. **Validates Previous Work**: Quick smoke test that existing features still work
6. **Selects Next Task**: Identifies highest-priority incomplete feature

## Usage

```
/session-start
```

Or with specific project:
```
/session-start project:rok-copilot
```

## The 8-Step Startup Ritual

### Step 0: ROK Infrastructure Check (CRITICAL - First Session Only)

**Before ANY other steps**, verify ROK infrastructure exists:

```bash
# Check for required files
ls -la CLAUDE.md claude-progress.txt 2>/dev/null
```

**If CLAUDE.md is MISSING:**
```
╔═══════════════════════════════════════════════════════════════════╗
║  ⚠️  ROK INFRASTRUCTURE MISSING                                   ║
║  ─────────────────────────────                                    ║
║  This project lacks CLAUDE.md and other ROK files.                ║
║                                                                   ║
║  REQUIRED ACTION: Run /project-init first                         ║
║                                                                   ║
║  This ensures:                                                    ║
║  - CLAUDE.md is created with project context                      ║
║  - claude-progress.txt tracks session handoffs                    ║
║  - ROK Brain integration is configured                            ║
║  - Memory system can track this project                           ║
╚═══════════════════════════════════════════════════════════════════╝
```

**STOP and run `/project-init` before continuing.**

This check prevents the issue where projects created via scaffolding tools (create-next-app, Claude Desktop PRDs) bypass ROK infrastructure setup.

---

### Step 0.5: Documentation Currency Check (Daily/Weekly)

Before diving into project work, ensure you're leveraging the latest capabilities.

**Quick Version Check:**
```bash
claude --version
# Current as of 2025-12-25: 2.0.76
```

**If version is behind:**
```bash
claude update
```

**Capability Awareness (run weekly or after major updates):**

1. **Check CHANGELOG for new features:**
   ```
   WebFetch https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
   # Focus on: new tools, MCP updates, workflow improvements
   ```

2. **Verify MCP servers are current:**
   ```bash
   # Check configured servers
   cat ~/.claude/mcp.json

   # For Docker MCP, check catalog
   docker mcp catalog ls
   ```

3. **Key capabilities to be aware of (Dec 2025):**

   | Feature | Shortcut/Command | Purpose |
   |---------|------------------|---------|
   | Model switching | `Alt+P` | Switch models mid-prompt |
   | Thinking toggle | `Alt+T` | Enable/disable extended thinking |
   | Claude in Chrome | `claude --chrome` | Browser control for UI debugging |
   | Background agents | `run_in_background: true` | Parallel async tasks |
   | Named sessions | `/rename`, `--resume <name>` | Session management |
   | LSP tools | Built-in | Go-to-definition, find refs |
   | MCP wildcards | `mcp__server__*` | Bulk tool permissions |

4. **Project-specific service docs (as needed):**
   - Supabase: Check for API changes, new features
   - GHL: Verify integration endpoints still valid
   - External APIs: Confirm rate limits, auth methods

**Output to include in session summary:**
```
CC Version: 2.0.76 (current)
Last Doc Review: 2025-12-25
New Capabilities Noted: Supabase MCP added, LSP tools available
```

**When to do full doc review:**
- First session of the day (quick version check)
- After `claude update` (full capability scan)
- Weekly (comprehensive review)
- When hitting unexpected limitations

---

### Step 0.5: Load Persistent Memory (ENHANCED - ROK 3.8 Pseudo-RLM)

**SYNTHESIZED MEMORY LOADING** - Claude MUST query and SYNTHESIZE results.

Before diving into project work, automatically query Supabase and return a **synthesized summary** (not raw data).

#### Query Method (Internal - Don't Show Raw Output)

Claude should run these queries but **synthesize results before display**:

```bash
PROJECT_NAME=$(basename "$PWD")
# Query memory index
curl -s "https://nvlumjwaooloycfeafvb.supabase.co/rest/v1/rok_memory_index?or=(project.eq.${PROJECT_NAME},project.is.null)&order=updated_at.desc&limit=30" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"

# Query session logs
curl -s "https://nvlumjwaooloycfeafvb.supabase.co/rest/v1/rok_session_logs?project=eq.${PROJECT_NAME}&order=timestamp.desc&limit=20" \
  -H "apikey: ${ROK_SUPABASE_KEY}" \
  -H "Authorization: Bearer ${ROK_SUPABASE_KEY}"
```

#### Required Output: SYNTHESIZED Format (Pseudo-RLM)

Claude MUST **synthesize** raw query results into actionable prose:

```
╔═══════════════════════════════════════════════════════════════════╗
║  CONTEXT SUMMARY (Synthesized)                                    ║
╠═══════════════════════════════════════════════════════════════════╣
║  WHAT WE KNOW                                                     ║
║  ─────────────                                                    ║
║  Architecture: JWT-based auth with Supabase (stateless, scales    ║
║  well). State managed via Zustand for simplicity. Testing with    ║
║  Vitest for native ESM support.                                   ║
║                                                                   ║
║  PATTERNS TO APPLY                                                ║
║  ─────────────────                                                ║
║  Auth implementation should start with middleware, then routes.   ║
║  Write tests first when touching existing code.                   ║
║  Use .maybeSingle() for optional Supabase queries.                ║
║                                                                   ║
║  GOTCHAS TO AVOID                                                 ║
║  ────────────────                                                 ║
║  - RLS policies: Create AFTER enabling RLS, not before            ║
║  - NextAuth callbacks: Must return user object                    ║
║  - GHL webhooks: URL must match exactly (no trailing slash)       ║
║                                                                   ║
║  RECENT WORK (last 24h)                                           ║
║  ──────────────────────                                           ║
║  Implemented damage control hooks (Python-based PreToolUse).      ║
║  Created pseudo-RLM context library with synthesis mode.          ║
║  Working on: N8N workflow integration (deferred).                 ║
║                                                                   ║
║  BLOCKERS                                                         ║
║  ────────                                                         ║
║  - Docker networking blocking Archon RAG (Tier 2)                 ║
║  - GHL ticket #4516767 pending for funnel tracking                ║
╚═══════════════════════════════════════════════════════════════════╝
```

**Key Difference from v3.5:**
- OLD: Display raw entries in tables (10+ items = context pollution)
- NEW: Synthesize into prose summary (<500 tokens regardless of entry count)

#### Synthesis Guidelines

| Do | Don't |
|----|-------|
| Group related items into narrative | List every entry separately |
| Use prose sentences | Use tables with raw values |
| Summarize patterns and themes | Show individual timestamps |
| Note blockers prominently | Bury important warnings |
| Keep under 500 tokens | Exceed 800 tokens ever |

#### Actionable Context (Required)

After synthesis, provide task-relevant recommendations:

```
Based on stored context:
- Continue with: [highest-priority in-progress item]
- Watch for: [relevant gotchas for that task]
- Apply: [patterns that help with that task]
```

#### Fallback (No Supabase Key)

If `ROK_SUPABASE_KEY` is not set:
```
╔═══════════════════════════════════════════════════════════════════╗
║  MEMORY SYSTEM OFFLINE                                            ║
║  ────────────────────                                             ║
║  ROK_SUPABASE_KEY not set. Memory queries skipped.                ║
║  Set in ~/.bashrc: export ROK_SUPABASE_KEY="<key>"                ║
║  Falling back to file-based context loading.                      ║
╚═══════════════════════════════════════════════════════════════════╝
```

#### Why Synthesis Matters (Pseudo-RLM)

> "Don't force all the context into the model's neural network at once.
> Instead, treat the context as an environment the model can interact with
> programmatically." - MIT RLM Research

**Context Window Impact:**
- Without synthesis: 30 entries × 100 tokens = 3000 tokens burned
- With synthesis: Same 30 entries = ~400 tokens of actionable prose
- **Savings: 87% token reduction**

**Quality Impact:**
- Raw data: User must scan and interpret
- Synthesized: Ready-to-use recommendations

---

### Step 1: Directory Confirmation

Run `pwd` and verify you're in the expected project directory.

```bash
pwd
# Expected: ~/projects/<project-name>
```

If not in correct directory, navigate first:
```bash
cd ~/projects/<project-name>
```

### Step 2: Load Progress State

Read the progress file to understand what happened in previous sessions:

```bash
cat claude-progress.txt
```

**Progress File Format:**
```
[2025-12-19 14:30] Session Summary
- Completed: feature-auth-login, feature-dashboard-layout
- In Progress: feature-auth-oauth (60% done, OAuth callback pending)
- Blockers: GHL API rate limiting
- Decisions: Using NextAuth.js instead of custom auth
- Next Session: Complete OAuth callback handler, add refresh token logic
```

### Step 3: Load Feature List

Read structured feature tracking:

```bash
cat feature_list.json | jq '.features | map(select(.status != "done")) | sort_by(.priority) | .[0:5]'
```

Or if `jq` not available:
```bash
cat feature_list.json
```

**Identify highest-priority incomplete feature for this session.**

### Step 4: Run Init Script

Execute project initialization:

```bash
./init.sh
```

**Init script responsibilities:**
- Start dev server(s)
- Verify environment variables loaded
- Check database connectivity
- Start any required services (Redis, etc.)
- Run quick health checks

**Wait for services to be ready before proceeding.**

### Step 5: Validate Previous Work

Before adding new features, verify existing work still functions:

```bash
# Run smoke tests if available
npm run test:smoke 2>/dev/null || echo "No smoke tests configured"

# Or manual validation
curl -s http://localhost:3006/api/health | jq .
```

**If previous features are broken:**
1. Fix them FIRST before starting new work
2. Update `claude-progress.txt` with the regression
3. Do not mark broken features as "done"

### Step 6: Select Next Task

Based on feature list and progress file:

1. Choose the **highest-priority incomplete feature**
2. If in-progress feature exists, continue it
3. Announce your selection to the user

**Output to User:**
```
╔═══════════════════════════════════════════════════════════════════╗
║                    SESSION START SUMMARY                          ║
╠═══════════════════════════════════════════════════════════════════╣
║  Project: rok-copilot                                             ║
║  Directory: ~/projects/rok-copilot                                ║
║  Branch: main                                                     ║
╠═══════════════════════════════════════════════════════════════════╣
║  TOOLING STATUS                                                   ║
║  ──────────────                                                   ║
║  CC Version: 2.0.76 (current)                                     ║
║  Last Doc Review: 2025-12-25                                      ║
║  MCP Servers: supabase, docker-mcp-toolkit, playwright            ║
╠═══════════════════════════════════════════════════════════════════╣
║  SERVICES                                                         ║
║  ────────                                                         ║
║  Dev Server: http://localhost:3006 ✓                              ║
║  Archon: http://localhost:3737 ✓                                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  PREVIOUS SESSION                                                 ║
║  ────────────────                                                 ║
║  Date: 2025-12-19 10:30                                           ║
║  Completed: auth-login, dashboard-layout                          ║
║  In Progress: auth-oauth (60%)                                    ║
╠═══════════════════════════════════════════════════════════════════╣
║  SELECTED TASK                                                    ║
║  ─────────────                                                    ║
║  ID: feature-auth-oauth                                           ║
║  Priority: 1 (Critical)                                           ║
║  Description: Complete OAuth callback handler                     ║
║  Validation Steps:                                                ║
║    1. User clicks "Sign in with Google"                           ║
║    2. Redirect to Google OAuth                                    ║
║    3. Callback returns to /api/auth/callback                      ║
║    4. Session created, user redirected to dashboard               ║
╚═══════════════════════════════════════════════════════════════════╝

Ready to continue implementation.
```

## Progress File Format

The `claude-progress.txt` file is the handoff mechanism between sessions:

```markdown
# Claude Progress Log - <project-name>

## Latest Session
[YYYY-MM-DD HH:MM] Session Summary
- Completed: <feature-ids that were finished>
- In Progress: <feature-id> (<percentage>%, <what's pending>)
- Blockers: <any blocking issues>
- Decisions: <key choices made with brief rationale>
- Next Session: <specific action items for continuation>

## Session History
[Previous entries, newest first...]
```

**Rules:**
- Append new entries at top (newest first)
- Keep last 10 sessions in history
- Archive older entries if file exceeds 500 lines

## Feature List Format

The `feature_list.json` provides structured requirements:

```json
{
  "project": "rok-copilot",
  "created": "2025-12-19",
  "features": [
    {
      "id": "auth-login",
      "category": "authentication",
      "description": "User can log in with email/password",
      "validation_steps": [
        "Navigate to /login",
        "Enter valid credentials",
        "Verify redirect to dashboard",
        "Verify session cookie set"
      ],
      "dependencies": [],
      "priority": 1,
      "status": "done",
      "session_completed": "2025-12-18"
    },
    {
      "id": "auth-oauth",
      "category": "authentication",
      "description": "User can log in with Google OAuth",
      "validation_steps": [
        "Click 'Sign in with Google'",
        "Complete Google OAuth flow",
        "Verify callback creates session",
        "Verify user profile populated"
      ],
      "dependencies": ["auth-login"],
      "priority": 1,
      "status": "in-progress",
      "session_started": "2025-12-19"
    }
  ]
}
```

**Status values:** `todo`, `in-progress`, `done`, `blocked`

## Integration with ROK 3.0

### Relationship to Existing Commands

| Command | When to Use | Purpose |
|---------|-------------|---------|
| `/session-start` | Beginning of every session | Context recovery, task selection |
| `/rok-clean-session` | First session on a project | Full context load from /tmp/ |
| `/diary` | During/after complex work | Capture learnings |
| `/session-end` | End of every session | Clean handoff |

### Workflow

```
/session-start → Work on selected feature → /diary (if learning) → /session-end
```

### Cross-Platform Handoff

Since Claude Desktop, Claude Code, and Browser Agent don't share sessions:

1. All interfaces read `claude-progress.txt` via this command
2. All interfaces update it via `/session-end`
3. Git sync keeps file consistent across machines

## Files Created/Used

| File | Location | Purpose |
|------|----------|---------|
| `claude-progress.txt` | Project root | Session handoff log |
| `feature_list.json` | Project root | Structured requirements |
| `init.sh` | Project root | Environment startup |
| `CLAUDE.md` | Project root | Project context |

## Troubleshooting

### No init.sh Found
```bash
# Create minimal init.sh
cat > init.sh << 'EOF'
#!/bin/bash
echo "Starting $(basename $PWD)..."
# Add project-specific startup here
EOF
chmod +x init.sh
```

### No feature_list.json Found
Run `/generate-feature-list` to create one from existing tasks.

### Services Won't Start
Check `claude-progress.txt` for previous session's blockers. May need manual intervention.

### Progress File Missing
Start fresh:
```bash
echo "# Claude Progress Log - $(basename $PWD)" > claude-progress.txt
echo "" >> claude-progress.txt
echo "[$(date '+%Y-%m-%d %H:%M')] Initial Session" >> claude-progress.txt
echo "- Starting project work" >> claude-progress.txt
```

## Why This Matters

From Anthropic's research on long-running agents:

> "The key insight was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history."

Without this ritual:
- Agents waste time figuring out project state
- Previous work may be incorrectly assumed complete
- Environment issues compound across sessions
- Context is rebuilt from scratch each time

With this ritual:
- 5-second context recovery instead of 5-minute exploration
- Clear task selection based on priorities
- Guaranteed working environment before new development
- Reliable handoff between Claude interfaces

---

**Session Start Command v1.3** | ROK 3.8 Harness Pattern
*Updated: 2026-01-06 - Step 0.5 now uses Pseudo-RLM synthesis (87% token reduction)*
