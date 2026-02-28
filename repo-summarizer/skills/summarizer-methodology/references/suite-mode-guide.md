# Suite Mode Guide

## Overview

Suite mode analyzes multiple related repositories together, identifying cross-repo dependencies, version mismatches, API contract matching, and integration gaps. Designed for analyzing related app suites (e.g., FBM apps, microservices).

## When to Use Suite Mode

- Analyzing a set of related apps that share users, data, or APIs
- Planning integration work across multiple repos
- Auditing a microservices architecture
- Pre-merger analysis of acquired codebases

## Workflow

### Phase 0S: Resolve Multiple Sources

Accept repos as:
```
/repo-summarizer:summarize --mode=suite ~/app1,~/app2,~/app3
/repo-summarizer:summarize --mode=suite user/repo1,user/repo2
/repo-summarizer:summarize --mode=suite https://github.com/org/repo1,https://github.com/org/repo2
```

Mixed sources are supported:
```
/repo-summarizer:summarize --mode=suite ~/local-app,user/remote-app
```

### Phase 1-3: Per-Repo Analysis

Run the standard single-repo analysis (Phase 1-3) for each repo independently. This produces per-repo analysis results including purpose, features, stack, gaps, and architecture.

### Phase 2S: Cross-Repo Integration Analysis

After all per-repo analyses complete, dispatch a cross-repo analysis that examines:

#### 1. Shared Dependencies
Compare package manifests across repos. For each dependency that appears in 2+ repos:
- Record the versions used in each repo
- Flag version mismatches (different major/minor versions)
- Note shared but different lock files

#### 2. API Contract Matching
For each repo that has API endpoints (from feature-enumerator):
- Extract endpoint paths and methods
- Search other repos for fetch/axios calls to those paths
- Match provider endpoints to consumer calls
- Flag mismatches (path differences, missing endpoints)

#### 3. Shared Data Models
For each repo that has database models (from architecture-mapper):
- Extract model/entity names
- Search other repos for the same model names
- Compare field definitions if possible
- Flag models that exist in multiple repos but differ

#### 4. Integration Gaps
Identify missing glue between repos:
- Shared auth but different session handling
- Common data models but no shared schema
- API providers with no corresponding consumers
- Missing shared utilities that are duplicated

#### 5. Cross-Repo Recommendations
Generate actionable recommendations for integration:
- "Align TypeScript versions: repo-a uses 5.2, repo-b uses 5.4"
- "Extract shared User model into a shared package"
- "repo-a's /api/users returns different fields than repo-b expects"

## Suite Export

The suite export extends the standard single-repo export:

1. Each repo gets its own standard export (MD + PDF + HTML)
2. A suite-level summary combines all repos with the integration analysis
3. Output folder structure:
   ```
   Repo_Summaries/
     2024-01-15_my-suite_Suite_Summary.html
     2024-01-15_my-suite_Suite_Summary.pdf
     2024-01-15_my-suite_Suite_Summary.md
     2024-01-15_repo-a_Repo_Summary.html
     2024-01-15_repo-a_Repo_Summary.pdf
     2024-01-15_repo-a_Repo_Summary.md
     2024-01-15_repo-b_Repo_Summary.html
     ...
   ```

## Limitations

- Suite mode multiplies token cost by number of repos
- Cross-repo analysis adds ~15K tokens on top
- Maximum recommended suite size: 5 repos (beyond that, context becomes unwieldy)
- Monorepos are better analyzed in single mode -- they're already one repo
