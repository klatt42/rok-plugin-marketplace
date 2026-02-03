# /generate-feature-list - Create Structured Feature Tracking

Generates a `feature_list.json` from PRDs, task lists, or project requirements.

## What This Does

1. **Analyzes Input**: Reads PRD, task files, or requirements
2. **Extracts Features**: Identifies discrete deliverables
3. **Creates Validation Steps**: Defines how to verify each feature
4. **Sets Dependencies**: Maps feature relationships
5. **Assigns Priorities**: Orders by importance/urgency
6. **Outputs JSON**: Creates harness-compatible feature list

## Usage

```
/generate-feature-list
```

With specific source:
```
/generate-feature-list source:PRD.md
/generate-feature-list source:rok_tasks.json
/generate-feature-list source:requirements.txt
```

## Feature List Schema

```json
{
  "project": "project-name",
  "version": "1.0",
  "created": "YYYY-MM-DD",
  "description": "Purpose of this feature list",
  "features": [
    {
      "id": "unique-kebab-case-id",
      "category": "functional|infrastructure|integration|testing|standards",
      "description": "What this feature does",
      "validation_steps": [
        "Step 1 to verify feature works",
        "Step 2 to verify",
        "Step 3 to verify"
      ],
      "dependencies": ["other-feature-id"],
      "priority": 1,
      "status": "todo|in-progress|blocked|done",
      "session_started": "YYYY-MM-DD",
      "session_completed": "YYYY-MM-DD",
      "blocked_by": "reason if blocked",
      "notes": "Additional context"
    }
  ],
  "categories": {
    "category-name": "Description of category"
  },
  "status_values": {
    "todo": "Not started",
    "in-progress": "Currently being worked on",
    "blocked": "Waiting on external dependency",
    "done": "Complete and all validation steps pass"
  },
  "agent_instructions": {
    "selecting_task": "How to choose next task",
    "marking_done": "Rules for completion",
    "updating_progress": "What to update",
    "adding_features": "How to add discovered features"
  }
}
```

## Generation Process

### Step 1: Identify Source Material

Look for these files in order:
1. `PRD.md` or `REQUIREMENTS.md` - Product requirements
2. `rok_tasks.json` - Existing ROK task tracking
3. `TODO.md` or `TASKS.md` - Task lists
4. `CLAUDE.md` - Project context with feature mentions
5. User-provided input

### Step 2: Extract Features

For each requirement/task, create a feature with:

**ID**: Kebab-case unique identifier
```
auth-login
dashboard-analytics
api-rate-limiting
```

**Category**: One of:
- `functional` - User-facing features
- `infrastructure` - System/tooling
- `integration` - Third-party services
- `testing` - Test capabilities
- `standards` - Documentation/conventions
- `framework` - Framework enhancements

**Description**: One sentence explaining the feature

**Validation Steps**: 3-5 concrete verification steps
- Must be testable (manually or automated)
- Should cover the happy path
- Include edge cases for critical features

### Step 3: Map Dependencies

Identify which features must be complete before others:
```json
{
  "id": "auth-oauth",
  "dependencies": ["auth-login"]
}
```

**Rules:**
- Features with no dependencies can start immediately
- Blocked features should have `blocked_by` explanation
- Circular dependencies are errors

### Step 4: Assign Priorities

Priority scale (1-5, 1 is highest):

| Priority | Meaning | Example |
|----------|---------|---------|
| 1 | Critical path, blocks others | Auth system |
| 2 | Important, should do soon | Dashboard features |
| 3 | Nice to have | Performance optimizations |
| 4 | Future enhancement | Advanced analytics |
| 5 | Backlog | Ideas to explore |

### Step 5: Set Initial Status

- `todo` - Not started (default)
- `in-progress` - Already being worked on
- `blocked` - External dependency
- `done` - Already complete

### Step 6: Generate JSON

Output to `feature_list.json` in project root.

## Example Generation

**Input (from PRD):**
```markdown
## Requirements

1. User Authentication
   - Email/password login
   - OAuth with Google
   - Session management

2. Dashboard
   - Project overview
   - Analytics charts
```

**Output (feature_list.json):**
```json
{
  "project": "example-app",
  "version": "1.0",
  "created": "2025-12-19",
  "features": [
    {
      "id": "auth-email-password",
      "category": "functional",
      "description": "User can log in with email and password",
      "validation_steps": [
        "Navigate to /login",
        "Enter valid email and password",
        "Verify redirect to dashboard",
        "Verify session cookie is set"
      ],
      "dependencies": [],
      "priority": 1,
      "status": "todo"
    },
    {
      "id": "auth-oauth-google",
      "category": "functional",
      "description": "User can log in with Google OAuth",
      "validation_steps": [
        "Click 'Sign in with Google' button",
        "Complete Google OAuth flow",
        "Verify redirect to dashboard",
        "Verify user profile is populated"
      ],
      "dependencies": ["auth-email-password"],
      "priority": 1,
      "status": "todo"
    },
    {
      "id": "auth-session-management",
      "category": "functional",
      "description": "Sessions persist and can be invalidated",
      "validation_steps": [
        "Log in and close browser",
        "Reopen browser, verify still logged in",
        "Click logout, verify session cleared",
        "Verify cannot access protected routes"
      ],
      "dependencies": ["auth-email-password"],
      "priority": 1,
      "status": "todo"
    },
    {
      "id": "dashboard-project-overview",
      "category": "functional",
      "description": "Dashboard shows list of user's projects",
      "validation_steps": [
        "Log in and navigate to /dashboard",
        "Verify project list is displayed",
        "Verify project cards show name and status",
        "Click project to navigate to detail"
      ],
      "dependencies": ["auth-session-management"],
      "priority": 2,
      "status": "todo"
    },
    {
      "id": "dashboard-analytics",
      "category": "functional",
      "description": "Dashboard displays analytics charts",
      "validation_steps": [
        "Navigate to /dashboard",
        "Verify analytics section is visible",
        "Verify charts render with data",
        "Verify date range filter works"
      ],
      "dependencies": ["dashboard-project-overview"],
      "priority": 2,
      "status": "todo"
    }
  ]
}
```

## Migrating from rok_tasks.json

If `rok_tasks.json` exists, use it as source:

**Mapping:**
| rok_tasks.json | feature_list.json |
|----------------|-------------------|
| `id` | `id` |
| `title` | `description` |
| `verification_steps` | `validation_steps` |
| `priority` (critical/high/medium/low) | `priority` (1/2/3/4) |
| `status` | `status` (with mapping) |
| `notes` | `notes` |

**Status mapping:**
- `pending` → `todo`
- `in_progress` → `in-progress`
- `waiting` → `blocked`
- `completed` → `done`

## Integration with Session Commands

The feature list integrates with `/session-start`:

```bash
# Session start reads feature list
cat feature_list.json | jq '.features | map(select(.status != "done")) | sort_by(.priority) | .[0]'
```

And `/session-end` updates it:
```bash
# Mark feature complete
jq '.features |= map(if .id == "auth-login" then .status = "done" | .session_completed = "2025-12-19" else . end)' feature_list.json > tmp.json && mv tmp.json feature_list.json
```

## Best Practices

### Writing Good Validation Steps

**Good:**
```json
"validation_steps": [
  "Navigate to /login",
  "Enter 'test@example.com' and 'password123'",
  "Verify redirect to /dashboard",
  "Verify welcome message shows user email"
]
```

**Bad:**
```json
"validation_steps": [
  "Login works",
  "User can see dashboard"
]
```

### Feature Granularity

- Features should be completable in 1-3 sessions
- If a feature takes >5 sessions, break it down
- Each feature should have a clear "done" state

### Handling Discovered Work

When you discover new requirements during implementation:

```json
{
  "id": "auth-token-refresh",
  "description": "Automatically refresh OAuth tokens before expiry",
  "discovered": "2025-12-19",
  "discovery_context": "Found during OAuth implementation - tokens expire after 1 hour",
  "status": "todo"
}
```

## Output Confirmation

```
Feature List Generated

Project: rok-copilot
Location: ./feature_list.json

Features Created:
- 5 functional features
- 3 infrastructure features
- 2 integration features

Priority Distribution:
- Priority 1 (Critical): 4 features
- Priority 2 (Important): 3 features
- Priority 3 (Nice to have): 3 features

Next Steps:
1. Review generated feature list
2. Adjust priorities if needed
3. Run /session-start to begin work
```

---

**Generate Feature List Command v1.0** | ROK 3.0 Harness Pattern
