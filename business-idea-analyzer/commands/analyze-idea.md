---
description: Analyze a business idea through multi-dimensional research with parallel agents, producing a ranked opportunity report with scores, ROI projections, and go/no-go recommendations
argument-hint: <business idea description> [--depth=quick|standard|deep] [--focus=solopreneur|enterprise|both]
allowed-tools: Bash(ls:*), Bash(python3:*), Bash(rm:*), Read, Glob, Grep, Write, WebSearch, WebFetch, Task, TaskOutput, TodoWrite
---

# Business Idea Analyzer

Analyze a business idea through multi-dimensional market research, competitive analysis, financial modeling, execution assessment, and risk evaluation. Produces a ranked report of 3-5 opportunities with composite scores and go/no-go verdicts.

## Usage

```
/business-idea-analyzer:analyze-idea tools for Facebook Marketplace sellers
/business-idea-analyzer:analyze-idea AI-powered inventory management for eBay sellers --depth=deep
/business-idea-analyzer:analyze-idea SaaS for freelance photographers --focus=solopreneur --depth=standard
```

## Arguments

- **idea description** (required): The business idea to analyze. Can be vague or specific.
- **--depth** (optional): `quick` (5-10 min, no agents), `standard` (15-30 min, default), `deep` (45-60 min, auto deep-dive on top result).
- **--focus** (optional): `solopreneur` (default), `enterprise`, `both`.

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Idea Intake & Scoping

Before launching any agents, understand the idea space:

1. **Parse input**: Extract the idea description and any flags (--depth, --focus) from $ARGUMENTS. Default: depth=standard, focus=solopreneur.

2. **Discovery search**: Run 3-5 WebSearch queries to understand the idea space:
   - `"[idea keywords]" market OR industry OR tools`
   - `"[idea keywords]" pain points OR problems OR gaps`
   - `"[idea keywords]" SaaS OR tool OR platform competitor`
   Build initial understanding of the market.

3. **Build Idea Context Brief**:
```
IDEA CONTEXT BRIEF
==================
Idea: [user's description]
Category: [SaaS | Marketplace | Tool | Service | Content | Chrome Extension | Mobile App]
Target Market: [who would pay for this]
Geographic Scope: [local | national | global]
Operator Profile: [solopreneur | small-team | enterprise]
Depth: [quick | standard | deep]
Date: [YYYY-MM-DD]
Initial Signals:
- [3-5 bullet points from discovery searches]
```

4. **APPROVAL GATE 1**: Present the Idea Context Brief to the user. Ask them to confirm or refine the scope before proceeding. If `quick` depth, skip to Phase 3 Quick Mode.

### Phase 2: Parallel Agent Dispatch

Launch 5 analysis agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Dimension |
|-------|--------------|-------|-----------|
| market-demand-analyst | general-purpose | opus | Market Demand (25%) |
| competitive-landscape-analyst | general-purpose | opus | Competitive Landscape (20%) |
| financial-viability-analyst | general-purpose | sonnet | Financial Viability (20%) |
| execution-feasibility-analyst | general-purpose | sonnet | Execution Feasibility (20%) |
| risk-analyst | general-purpose | opus | Risk Assessment (15%) |

**For each agent prompt, include**:
1. The full Idea Context Brief
2. The agent's specific instructions (read from the agent definition file)
3. Depth-specific guidance:
   - `standard`: "Perform 6-10 WebSearch queries. Focus on the most impactful findings."
   - `deep`: "Perform 10-15 WebSearch queries. Be thorough and explore edge cases."

**Quick Mode** (depth=quick): Skip agents entirely. Instead, perform 5-8 WebSearch queries directly and produce a rough scoring based on search results alone. Output a simple table in chat (no export).

### Phase 3: Synthesis & Scoring

1. **Collect results**: Use `TaskOutput` with `block=true` for each of the 5 agents. Handle failures gracefully -- if an agent fails, assign that dimension a default score of 50 and note "analysis unavailable" in the summary.

2. **Launch report-synthesizer**: Use `Task` to launch the report-synthesizer agent (model: sonnet) with:
   - All 5 agent JSON outputs concatenated
   - The export script path: the plugin's `scripts/business_analysis_export.py` located relative to this command file
   - Instructions to identify 3-5 distinct opportunities, score each, and produce the export JSON

3. **APPROVAL GATE 2** (standard/deep only): Before final export, present the ranked opportunities:

```
OPPORTUNITY ANALYSIS COMPLETE

| # | Opportunity | Score | Verdict | Solo? |
|---|-------------|-------|---------|-------|
| 1 | [Name]      | 82    | STRONG GO | Yes |
| 2 | [Name]      | 71    | GO        | Yes |
| 3 | [Name]      | 55    | CONDITIONAL | No |

Options:
a) Export full report (MD + PDF + HTML)
b) Deep-dive into a specific opportunity (/idea-deep-dive)
c) Validate assumptions for top opportunities (/idea-validate)
d) Adjust scope and re-analyze
```

Wait for user response before proceeding.

### Phase 4: Export & Display

1. **Verify export**: The report-synthesizer agent should have written the JSON and run the export script. If not, do it now:
   ```bash
   ~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/business_analysis_export.py --input /tmp/business_analysis_export.json
   ```

2. **Clean up**: Remove `/tmp/business_analysis_export.json`

3. **Display summary in chat**:

```
## Business Idea Analysis: [Idea Description]

**Date**: [YYYY-MM-DD] | **Depth**: [standard] | **Focus**: [solopreneur]

### Opportunity Rankings

| # | Opportunity | Score | Verdict |
|---|-------------|-------|---------|
| 1 | [Name] | [XX] | [VERDICT] |
| 2 | [Name] | [XX] | [VERDICT] |

### Top Opportunity: [Name] (Score: XX)

**Dimensions**:
| Dimension | Score |
|-----------|-------|
| Market Demand | XX |
| Competitive Landscape | XX |
| Financial Viability | XX |
| Execution Feasibility | XX |
| Risk Assessment | XX |

**Key Findings**: [3-5 bullet points]
**Top Risks**: [2-3 bullet points]
**Next Steps**: [3-5 actionable items]

### Files Generated
- MD: [path]
- PDF: [path]
- HTML: [path]
```

## Scoring Formula

```
weighted = (demand * 0.25) + (competitive * 0.20) + (financial * 0.20) + (execution * 0.20) + (risk * 0.15)
risk_penalty = (critical_kill_criteria * 15) + (high_risks * 5)
solo_bonus = 5 if (solopreneur_viable AND demand >= 70)
final = max(0, min(100, round(weighted - risk_penalty + solo_bonus)))
```

## Verdicts

| Score | Kill Criteria | Verdict |
|-------|---------------|---------|
| >= 80 | 0 critical | STRONG_GO |
| 65-79 | 0 critical | GO |
| 50-64 | 0 critical | CONDITIONAL |
| < 50 | any | NO_GO |
| any | >= 1 critical | BLOCKED |

## Export JSON Schema

The report-synthesizer produces JSON with this structure:

```json
{
  "type": "business_analysis",
  "idea_description": "...",
  "date": "YYYY-MM-DD",
  "depth": "standard",
  "operator_profile": "solopreneur",
  "executive_summary": "2-3 paragraph overview",
  "opportunities": [
    {
      "rank": 1,
      "name": "Opportunity Name",
      "description": "1-2 sentence description",
      "verdict": "STRONG_GO",
      "composite_score": 82,
      "dimensions": [
        {"name": "Market Demand", "key": "market_demand", "score": 85, "weight": 0.25, "summary": "...", "key_findings": ["finding1", "finding2"]}
      ],
      "tam": {"total_addressable": "$500M", "serviceable_addressable": "$120M", "obtainable_y1": "$210K", "obtainable_y3": "$2.1M"},
      "solopreneur_viable": true,
      "mvp_timeline": "4-6 weeks",
      "recommended_pricing": "$29-49/mo",
      "top_risks": [{"risk": "...", "severity": "high", "mitigation": "..."}],
      "kill_criteria": [{"assumption": "...", "kill_condition": "...", "status": "unverified"}],
      "next_steps": ["Step 1", "Step 2", "Step 3"]
    }
  ],
  "market_research": {
    "pain_points": [{"description": "...", "severity": 85, "frequency": "daily", "affected_segment": "...", "economic_impact": "..."}],
    "demand_signals": [{"signal": "...", "strength": "strong", "source": "Reddit", "confidence": 90}],
    "sources_consulted": 25
  },
  "competitive_analysis": {
    "competitors": [{"name": "...", "pricing": "$39/mo", "strengths": ["..."], "weaknesses": ["..."]}],
    "feature_matrix": {"features": ["F1", "F2"], "competitors": {"Comp A": [true, false], "Proposed": [true, true]}},
    "gap_summary": "..."
  },
  "risk_register": [{"id": "RISK-001", "category": "platform", "severity": "high", "description": "...", "mitigation": "..."}],
  "methodology": {"depth": "standard", "agents_dispatched": 5, "web_searches_performed": 48, "confidence_threshold": 70}
}
```

## Token Budget

| Depth | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|-------|---------|---------|---------|---------|-------|
| quick | ~2K | 0 | ~2K | ~1K | ~5K |
| standard | ~2K | ~60K | ~5K | ~2K | ~69K |
| deep | ~2K | ~100K | ~8K | ~3K | ~113K |

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data or statistics.
- Present approval gates and wait for user response before proceeding.
- Handle agent failures gracefully with default scores.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Business_Analysis/`
