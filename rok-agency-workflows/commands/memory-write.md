# /memory-write - Persist Important Memory

Write important decisions, patterns, or learnings to persistent memory (Supabase + GitHub).

## Usage

```
/memory-write category:"decision" key:"auth-method" value:"JWT over sessions for stateless API"
/memory-write category:"pattern" key:"error-handling" value:"Always wrap async calls in try-catch with specific error types"
/memory-write category:"gotcha" key:"supabase-rls" value:"RLS policies must be created AFTER enabling RLS"
/memory-write category:"preference" key:"commit-style" value:"Use conventional commits with emoji prefix"
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `category` | Yes | Type of memory: decision, pattern, gotcha, preference |
| `key` | Yes | Unique identifier for this memory (snake_case) |
| `value` | Yes | The actual content/knowledge to store |
| `project` | No | Project name (defaults to current directory) |

## Categories

- **decision**: Architectural/design decisions with rationale
- **pattern**: Reusable code patterns or approaches
- **gotcha**: Pitfalls to avoid, learned the hard way
- **preference**: User preferences for tools, style, workflow

## Behavior

When invoked, Claude should:

### 1. Validate Input
- Ensure category is one of: decision, pattern, gotcha, preference
- Ensure key is provided and snake_case
- Ensure value is provided

### 2. Write to Supabase
```sql
INSERT INTO rok_memory_index (category, project, key, value, source_session)
VALUES ($category, $project, $key, $value, $session_id)
ON CONFLICT (category, project, key)
DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();
```

### 3. Write to rok-memory GitHub (Critical Memories)
For decisions and patterns, also append to the appropriate rok-memory file:
- Decisions → `~/projects/rok-memory/decisions/YYYY-MM-DD.md`
- Patterns → `~/projects/rok-memory/learnings/patterns.md`

Format for GitHub:
```markdown
## [key] - [timestamp]
**Category**: [category]
**Project**: [project or "global"]

[value]

---
```

### 4. Confirm Write
Display confirmation with:
- Where data was stored (Supabase, GitHub, or both)
- The full entry for verification

## Example Session

```
User: /memory-write category:"decision" key:"testing-framework" value:"Use Vitest for unit tests - faster than Jest, native ESM support"

Claude: Memory written successfully.

**Category**: decision
**Key**: testing-framework
**Project**: rok-copilot
**Value**: Use Vitest for unit tests - faster than Jest, native ESM support

Stored to:
- Supabase rok_memory_index table
- ~/projects/rok-memory/decisions/2026-01-01.md
```

## Environment Variables Required

- `ROK_SUPABASE_URL`: Supabase project URL (from rok-copilot/.env.local)
- `ROK_SUPABASE_KEY`: Supabase service role key
- `ROK_SESSION_ID`: Current session identifier (auto-generated if not set)

## Related Commands

- `/memory-query` - Query existing memories
- `/session-start` - Loads recent memories at session start
- `/sync-context` - Syncs memories between Supabase and GitHub

## Notes

- Memories persist across sessions and projects
- Global memories (no project) apply to all projects
- Use specific keys to avoid overwriting unrelated memories
- The GitHub backup provides durability and human readability
