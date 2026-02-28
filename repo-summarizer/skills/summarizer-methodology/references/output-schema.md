# Repo Summary Output Schema Reference

## Export Payload (summary-synthesizer output)

The summary-synthesizer agent produces a JSON payload that drives the export script. This document details every field.

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Always "repo_summary" |
| mode | string | Yes | "single" or "suite" |
| project_name | string | Yes | Repository name |
| project_path | string | Yes | Absolute path to analyzed repo |
| repo_url | string | No | GitHub URL if remote |
| date | string | Yes | ISO date (YYYY-MM-DD) |
| maturity_level | string | Yes | MATURE, DEVELOPING, EARLY_STAGE, PROTOTYPE |
| maturity_score | integer | Yes | 0-100 |

### dimension_scores

Object with 5 keys, each containing:

```json
{
  "documentation": {"score": 65, "weight": 0.15},
  "feature_completeness": {"score": 78, "weight": 0.30},
  "infrastructure": {"score": 60, "weight": 0.20},
  "test_presence": {"score": 45, "weight": 0.15},
  "architecture_clarity": {"score": 85, "weight": 0.20}
}
```

### purpose

```json
{
  "statement": "One-line purpose",
  "extended": "2-4 sentence detailed description",
  "project_type": "web_app | api | cli | library | monorepo | mobile | desktop | other",
  "target_users": [{"persona": "Developer", "description": "..."}],
  "deployment_model": {"type": "SaaS", "platform": "Vercel"}
}
```

### features (array)

Each feature:

```json
{
  "id": "F-001",
  "name": "User Authentication",
  "category": "auth | api | ui | data | integration | infrastructure | background",
  "status": "complete | partial | stub | planned",
  "completeness": 85,
  "has_tests": true,
  "has_ui": true,
  "has_api": true,
  "related_gaps": ["GAP-003"]
}
```

### feature_summary

```json
{
  "total": 22,
  "complete": 12,
  "partial": 5,
  "stub": 3,
  "planned": 2
}
```

### stack

```json
{
  "primary_language": "TypeScript",
  "framework": "Next.js 14",
  "database": "PostgreSQL via Prisma",
  "deployment": "Vercel",
  "key_dependencies": ["next", "prisma", "tailwindcss", "zod"]
}
```

### gaps (array)

Each gap:

```json
{
  "id": "GAP-001",
  "type": "missing_feature | incomplete_implementation | infrastructure_gap | ux_gap | todo_marker | documentation_gap | security_gap",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW",
  "title": "No rate limiting on API endpoints",
  "recommendation": "Add rate limiting middleware using express-rate-limit",
  "effort_estimate": "small | medium | large"
}
```

### gap_summary

```json
{
  "critical": 0,
  "high": 3,
  "medium": 7,
  "low": 4,
  "total": 14
}
```

### architecture

```json
{
  "style": "layered | feature-based | MVC | clean | hexagonal | route-based | flat | monorepo",
  "pattern": "Next.js App Router with Prisma data layer",
  "key_files": [
    {"path": "src/app/layout.tsx", "role": "Root layout", "importance": "critical"}
  ],
  "navigation_tips": ["Start at src/app/layout.tsx for the app shell"],
  "data_flow": "Form -> API route -> Zod validation -> Service -> Prisma -> PostgreSQL"
}
```

### infrastructure_checklist

```json
{
  "error_handling": "complete | partial | missing",
  "logging": "complete | partial | missing",
  "input_validation": "complete | partial | missing",
  "rate_limiting": "complete | partial | missing",
  "health_check": "complete | partial | missing",
  "cors": "complete | partial | missing",
  "env_config": "complete | partial | missing",
  "ci_cd": "complete | partial | missing",
  "migrations": "complete | partial | missing",
  "secrets": "complete | partial | missing"
}
```

### Other Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| recommendations | string[] | Prioritized action items (5-10) |
| handoff_brief | string | Full Markdown handoff document |
| executive_summary | string | 2-3 sentence overall assessment |
| suite_context | object/null | Cross-repo analysis (suite mode only) |

### suite_context (when mode="suite")

```json
{
  "repos_analyzed": ["repo-a", "repo-b"],
  "shared_dependencies": [{"name": "react", "versions": {"repo-a": "18.2.0", "repo-b": "18.3.1"}}],
  "version_mismatches": [{"dep": "typescript", "repo-a": "5.2", "repo-b": "5.4"}],
  "api_contracts": [{"provider": "repo-a", "consumer": "repo-b", "endpoint": "/api/users"}],
  "shared_models": [{"model": "User", "repos": ["repo-a", "repo-b"], "identical": false}],
  "integration_gaps": ["repo-a exports /api/users but repo-b fetches /api/user (singular mismatch)"],
  "cross_repo_recommendations": ["Align TypeScript versions across all repos"]
}
```

## Agent-Specific Output Schemas

Each analysis agent returns a different schema. See the agent definition files in `agents/` for their exact JSON output formats:

- `purpose-analyzer.md` -> dimension: "purpose"
- `feature-enumerator.md` -> dimension: "features"
- `stack-analyzer.md` -> dimension: "stack"
- `gap-finder.md` -> dimension: "gaps"
- `architecture-mapper.md` -> dimension: "architecture"
