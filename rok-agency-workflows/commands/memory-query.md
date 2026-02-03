# /memory-query - Query Persistent Memory

Retrieve stored memories from Supabase to inform current work.

## Usage

```
/memory-query                                    # Recent memories for current project
/memory-query project:"rok-copilot"              # Specific project
/memory-query category:"decision"                # All decisions
/memory-query key:"auth"                         # Search by key (partial match)
/memory-query hours:24                           # Session logs from last 24 hours
/memory-query type:"index"                       # Query memory index
/memory-query type:"logs"                        # Query session logs
/memory-query --synthesize                       # Return synthesized summary (NEW)
/memory-query category:"gotcha" --synthesize     # Synthesized gotchas
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `type` | No | "index" (default) or "logs" |
| `category` | No | Filter by category (decision, pattern, gotcha, preference) |
| `project` | No | Filter by project (defaults to current directory) |
| `key` | No | Search key (partial match supported) |
| `hours` | No | For logs: time window in hours (default: 24) |
| `limit` | No | Max results (default: 20) |
| `--synthesize` | No | Return synthesized summary instead of raw entries (Pseudo-RLM) |

## Query Types

### Memory Index (type:"index")
Structured knowledge that persists indefinitely.
```sql
SELECT category, key, value, project, updated_at
FROM rok_memory_index
WHERE project = $project OR project IS NULL
ORDER BY updated_at DESC
LIMIT $limit;
```

### Session Logs (type:"logs")
Continuous action log from recent sessions.
```sql
SELECT action_type, file_path, summary, decision, timestamp
FROM rok_session_logs
WHERE project = $project
AND timestamp > NOW() - INTERVAL '$hours hours'
ORDER BY timestamp DESC
LIMIT $limit;
```

## Synthesis Mode (--synthesize)

When `--synthesize` is provided, transform raw query results into actionable context summaries.

### Why Synthesis? (Pseudo-RLM Pattern)

Based on MIT's Recursive Language Models research:
- **Without synthesis**: Raw data fills context window (100+ entries = 10K+ tokens)
- **With synthesis**: Actionable summary returned (<1K tokens)
- **Benefit**: Main agent context stays clean for actual work

### Synthesis Behavior

When `--synthesize` flag is present:

1. **Query normally** - Execute the same Supabase query
2. **Analyze results** - Identify patterns, themes, key points
3. **Prioritize by relevance** - Recent > old, specific > generic
4. **Deduplicate** - Same info from multiple sources = one mention
5. **Return summary** - Prose format, not tables

### Synthesis Output Format

**For Memory Index with --synthesize:**
```markdown
## Context Summary: [category/project]

**Key Decisions:**
- Use JWT for auth (stateless API, easier scaling)
- Vitest over Jest (native ESM support)

**Patterns to Apply:**
- Always use `.maybeSingle()` for optional Supabase rows
- Wrap external API calls in try-catch with specific error types

**Gotchas to Avoid:**
- Create RLS policies AFTER enabling RLS, not before
- GHL webhooks require exact URL match (no trailing slash)

**Relevant to Current Task:** [If task context available]
The auth decisions suggest using JWT middleware pattern.
```

**For Session Logs with --synthesize:**
```markdown
## Recent Activity Summary (last [hours]h)

**Work Completed:**
- Implemented damage control hooks (3 files)
- Created context-library command and agent

**Decisions Made:**
- Python hooks over TypeScript (broader compatibility)
- Defense-in-depth approach for security

**Currently In Progress:**
- Enhancing memory-query with synthesis mode

**Blockers Noted:**
- Docker networking blocking Archon RAG
```

### Synthesis Guidelines

| Do | Don't |
|----|-------|
| Summarize into actionable points | Return raw JSON/tables |
| Group related items together | List every entry separately |
| Note what's relevant to current work | Include irrelevant details |
| Keep under 1000 tokens | Exceed 2000 tokens ever |
| Use prose for context | Use verbose formatting |

### Example: Synthesized vs Raw

**Raw (default):**
```
| Key | Value | Updated |
|-----|-------|---------|
| auth-method | JWT over sessions | 2026-01-01 |
| auth-provider | Supabase Auth | 2026-01-01 |
| session-storage | Not using sessions | 2025-12-30 |
| token-refresh | Proactive refresh | 2025-12-28 |
```

**Synthesized (--synthesize):**
```
Auth approach: Using JWT with Supabase Auth (no sessions).
Tokens refresh proactively before expiry.
```

## Behavior

When invoked, Claude should:

### 1. Parse Query Parameters
- Determine query type (index or logs)
- Build appropriate SQL filter

### 2. Execute Query
Using Supabase MCP or direct REST API:
```bash
curl -s "https://[project].supabase.co/rest/v1/rok_memory_index?select=*&project=eq.$project" \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY"
```

### 3. Format Results
Display in readable format:

**For Memory Index:**
```markdown
## Memories for [project]

### Decisions
| Key | Value | Updated |
|-----|-------|---------|
| auth-method | JWT over sessions | 2026-01-01 |

### Patterns
| Key | Value | Updated |
|-----|-------|---------|
| error-handling | Try-catch with specific types | 2025-12-30 |

### Gotchas
| Key | Value | Updated |
|-----|-------|---------|
| supabase-rls | Create policies AFTER enabling | 2025-12-28 |
```

**For Session Logs:**
```markdown
## Recent Activity (last 24 hours)

| Time | Action | Summary |
|------|--------|---------|
| 10:30 | edit | Added auth middleware to api/route.ts |
| 10:25 | decision | Use JWT for stateless API |
| 10:15 | test | All 24 tests passing |
```

### 4. Provide Context
If memories are relevant to current work, summarize key points.

## Example Sessions

### Query Recent Decisions
```
User: /memory-query category:"decision"

Claude: Found 5 decisions for rok-copilot:

| Key | Value | Updated |
|-----|-------|---------|
| auth-method | JWT over sessions for stateless API | 2026-01-01 |
| testing-framework | Vitest - faster than Jest, native ESM | 2025-12-30 |
| state-management | Zustand over Redux - simpler for this scope | 2025-12-28 |
```

### Query Session Activity
```
User: /memory-query type:"logs" hours:8

Claude: Session activity (last 8 hours):

| Time | Action | File | Summary |
|------|--------|------|---------|
| 14:30 | edit | src/api/auth.ts | Added JWT validation |
| 14:15 | test | - | Auth tests passing |
| 13:45 | decision | - | Use RS256 for JWT signing |

Key decisions made: Use RS256 algorithm for JWT signing.
```

### Search by Key
```
User: /memory-query key:"supabase"

Claude: Found 3 memories matching "supabase":

1. **gotcha:supabase-rls** - RLS policies must be created AFTER enabling
2. **pattern:supabase-query** - Always use .maybeSingle() for optional results
3. **decision:supabase-auth** - Use Supabase Auth over custom JWT
```

### Synthesized Query (Pseudo-RLM)
```
User: /memory-query category:"decision" --synthesize

Claude: ## Decision Summary for rok-copilot

**Architecture:**
- JWT-based auth with Supabase (stateless, scalable)
- Zustand for state management (simpler than Redux for this scope)

**Testing & Quality:**
- Vitest for unit tests (faster, native ESM)
- Defense-in-depth security with Python hooks

**Infrastructure:**
- Supabase for database and auth
- Netlify for deployment
- N8N for workflow automation

These decisions prioritize simplicity and developer experience
while maintaining production-grade security.
```

### Synthesized Gotchas for Current Task
```
User: /memory-query category:"gotcha" --synthesize

Claude: ## Gotchas to Watch

**Supabase:**
- RLS policies must be created AFTER enabling RLS
- Use .maybeSingle() not .single() for optional rows
- Service role key bypasses RLS (use anon key in client)

**GHL Integration:**
- Webhook URLs must match exactly (no trailing slash)
- API rate limits: 100 req/min per location

**General:**
- Always quote file paths with spaces in bash
- Never force-push to main without explicit approval
```

## Integration with Session Start

The `/session-start` command automatically runs:
```
/memory-query type:"logs" hours:24
/memory-query type:"index" limit:20
```

This provides immediate context when starting a session.

## Environment Variables Required

- `ROK_SUPABASE_URL`: Supabase project URL
- `ROK_SUPABASE_KEY`: Supabase service role key

## Related Commands

- `/memory-write` - Write new memories
- `/session-start` - Loads memories automatically
- `/sync-context` - Syncs with GitHub rok-memory
- `/context-library` - Full pseudo-RLM retrieval with subagent synthesis

## Notes

- Global memories (project IS NULL) appear in all project queries
- Recent memories are prioritized in results
- Use specific category filters for focused queries
- Session logs auto-expire after 30 days (future: configurable)
