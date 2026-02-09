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

4. **Present the Idea Context Brief** to the user. Always show this regardless of depth.

5. **APPROVAL GATE 1** (standard/deep only): Ask the user to confirm or refine the scope before proceeding to Phase 2. For `quick` depth, show the brief but do NOT wait for approval — proceed directly to Quick Mode Protocol (Phase 3).

### Phase 2: Parallel Agent Dispatch

Launch 5 analysis agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Dimension | Model Rationale |
|-------|--------------|-------|-----------|-----------------|
| market-demand-analyst | general-purpose | opus | Market Demand (25%) | Needs nuanced judgment to distinguish genuine demand signals from noise in unstructured Reddit/forum data |
| competitive-landscape-analyst | general-purpose | opus | Competitive Landscape (20%) | Requires strategic reasoning to identify indirect competitors and assess moat potential |
| financial-viability-analyst | general-purpose | sonnet | Financial Viability (20%) | Primarily formula-driven (TAM waterfall, ARPU calc); structured math doesn't need opus-level reasoning |
| execution-feasibility-analyst | general-purpose | sonnet | Execution Feasibility (20%) | Tech stack assessment and timeline estimation follow well-defined heuristics |
| risk-analyst | general-purpose | opus | Risk Assessment (15%) | Devil's advocate reasoning, historical analogy identification, and black swan thinking require strongest reasoning |

**For each agent prompt, include**:
1. The full Idea Context Brief
2. The agent's specific instructions (read from the agent definition file at `agents/[agent-name].md` relative to this command)
3. Depth-specific guidance:
   - `standard`: "Perform 6-10 WebSearch queries. Focus on the most impactful findings."
   - `deep`: "Perform 10-15 WebSearch queries. Be thorough — explore edge cases, adjacent markets, historical precedents, and contrarian perspectives."

**Quick Mode** (depth=quick): Skip agents entirely. Perform 5-8 WebSearch queries directly and produce a rough assessment. See Quick Mode Protocol below.

### Phase 3: Synthesis & Scoring

1. **Collect results**: Use `TaskOutput` with `block=true` for each of the 5 agents. Handle failures gracefully -- if an agent fails, assign that dimension a default score of 50 and note "analysis unavailable" in the summary.

2. **Launch report-synthesizer**: You MUST launch the report-synthesizer agent. Do NOT synthesize the results yourself — the synthesizer agent has specific scoring logic, cross-agent consistency checks, and export payload construction that must be executed.

   Use `Task` (subagent_type: `general-purpose`, model: `sonnet`) with this prompt structure:
   ```
   You are the report-synthesizer agent. Read your instructions from:
   [path to agents/report-synthesizer.md relative to this command]

   Here are the 5 research agent outputs to synthesize:

   === MARKET DEMAND ===
   [paste market-demand-analyst JSON output]

   === COMPETITIVE LANDSCAPE ===
   [paste competitive-landscape-analyst JSON output]

   === FINANCIAL VIABILITY ===
   [paste financial-viability-analyst JSON output]

   === EXECUTION FEASIBILITY ===
   [paste execution-feasibility-analyst JSON output]

   === RISK ASSESSMENT ===
   [paste risk-analyst JSON output]

   Idea Context Brief:
   [paste the Idea Context Brief from Phase 1]

   Export script path: [absolute path to scripts/business_analysis_export.py]

   Follow your instructions to identify 3-5 opportunities, score each, build the export JSON, write it to /tmp/business_analysis_export.json, and execute the export script.
   ```

   **IMPORTANT**: The synthesizer's export JSON schema MUST match the schema in this command (see Export JSON Schema below). The synthesizer has been updated with the authoritative schema.

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
solo_bonus = 5 if (solopreneur_viable AND raw_demand_score >= 70)
  # NOTE: Use the RAW market_demand dimension score (0-100), NOT adjusted for competition.
  # Competition is already captured in the competitive_landscape dimension.
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

## Quick Mode Protocol (depth=quick)

Quick mode skips agents entirely for a fast directional assessment in 5-10 minutes.

**Process**:
1. Run 5-8 WebSearch queries directly (demand signals, competitors, pricing, market size)
2. Score each dimension 0-100 based on search results alone (less precise, wider confidence intervals)
3. Apply the same composite formula and verdict thresholds
4. Present results in chat only — no export, no file generation

**Quick Mode Output** (display in chat):
```
## Quick Assessment: [Idea]

| Dimension | Score | Confidence | Notes |
|-----------|-------|------------|-------|
| Market Demand | 72 | Low | Some Reddit signals, unvalidated |
| Competitive Landscape | 65 | Medium | 3 competitors found |
| Financial Viability | 60 | Low | No detailed TAM calc |
| Execution Feasibility | 75 | Medium | Standard tech stack |
| Risk Assessment | 55 | Low | Surface-level only |

**Composite**: 66 | **Verdict**: GO (low confidence)

**Caveat**: Quick assessments have wider error margins (+/-15 points).
Run with --depth=standard for validated scoring with full agent analysis.

**Key Findings**: [3-5 bullets from search results]
**Obvious Risks**: [2-3 bullets]
**Recommendation**: [1 sentence: worth deeper analysis or redirect effort]
```

**Quick mode does NOT produce**:
- Export files (MD/PDF/HTML)
- Pain point severity scores
- TAM/SAM/SOM calculations
- Feature matrices
- Kill criteria inventories

## Deep Mode Deliverables (depth=deep)

Deep mode extends standard mode with additional research and an automatic deep-dive on the top opportunity.

**Additional vs Standard**:
| Feature | Standard | Deep |
|---------|----------|------|
| Queries per agent | 6-10 | 10-15 |
| Agent instructions | "Focus on most impactful" | "Explore edge cases, adjacent markets, historical precedents, contrarian views" |
| Opportunities identified | 3-5 | 3-5 (with more nuance) |
| Auto deep-dive | No | Yes — top opportunity gets /idea-deep-dive treatment |
| Export | MD + PDF + HTML | MD + PDF + HTML (richer content) |

**Deep Mode Auto Deep-Dive** (after Phase 4 export):
After the standard export completes, automatically produce a deep-dive section for the #1 ranked opportunity:
1. Competitive feature matrix with 8+ features and all identified competitors
2. Pain point severity ranking (top 5 by severity score)
3. MVP specification: core features (must-have) vs nice-to-have vs v2
4. Pricing tier analysis: Free, Pro, Enterprise with feature breakdown
5. Go-to-market strategy outline (4 phases: pre-launch, launch, growth, scale)
6. "Build first" list: the 3 things to build/validate before anything else

This deep-dive content is appended to the export JSON under an `"auto_deep_dive"` key and included in the exported files.

## Token Budget

| Depth | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Deep-Dive | Total |
|-------|---------|---------|---------|---------|-----------|-------|
| quick | ~2K | 0 | ~2K | ~1K | 0 | ~5K |
| standard | ~2K | ~60K | ~5K | ~2K | 0 | ~69K |
| deep | ~2K | ~100K | ~8K | ~3K | ~15K | ~128K |

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data or statistics.
- Present approval gates and wait for user response before proceeding.
- Handle agent failures gracefully with default scores.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Business_Analysis/`
