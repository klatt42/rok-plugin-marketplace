# Vehicle Recommender

Interview-driven vehicle recommendation engine. Gathers your requirements through structured questions, then dispatches 4 parallel research agents to analyze pricing, reliability, cost-of-ownership, and feature matching. Produces ranked recommendations with ready-to-paste finder prompts for future `/vehicle-finder` plugin handoff.

## Usage

```
/vehicle-recommender:recommend-vehicle                          # Standard depth, full interview
/vehicle-recommender:recommend-vehicle --depth=quick            # Quick scan, fewer searches
/vehicle-recommender:recommend-vehicle --depth=deep             # Deep research, more thorough
```

## Arguments

- **--depth** (optional): `quick` (5-10 min), `standard` (15-25 min, default), `deep` (30-45 min).

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Interview

Conduct a structured interview using `AskUserQuestion` to gather the user's vehicle requirements. Present questions in 2 rounds.

**Round 1** — Two questions in a single `AskUserQuestion` call:

**Question 1: Vehicle Type & Purpose**
```
header: "Vehicle type"
question: "What type of vehicle are you looking for and what's the primary use?"
multiSelect: false
options:
  - label: "SUV / Crossover"
    description: "Family hauler, road trips, cargo space"
  - label: "Truck"
    description: "Work truck, towing, hauling"
  - label: "Sedan / Hatchback"
    description: "Daily commuter, efficiency, city driving"
  - label: "Other"
    description: "Specify: minivan, sports car, EV, etc."
```

**Question 2: Budget & Buying Preference**
```
header: "Budget"
question: "What's your budget range and buying preference?"
multiSelect: false
options:
  - label: "Under $30K — New or Used"
    description: "Value-focused, open to certified pre-owned"
  - label: "$30K-$50K — New preferred"
    description: "Mid-range, new with warranty preferred"
  - label: "$50K-$80K — New"
    description: "Premium segment, features matter"
  - label: "$80K+ — Luxury/Performance"
    description: "Top tier, no budget constraints"
```

**Round 2** — Two multi-select questions in a single `AskUserQuestion` call:

**Question 3: Must-Haves**
```
header: "Must-haves"
question: "Which features are must-haves? Select all that apply."
multiSelect: true
options:
  - label: "AWD/4WD"
    description: "All-wheel or four-wheel drive capability"
  - label: "Towing capacity"
    description: "Need to tow trailers, boats, equipment"
  - label: "Fuel efficiency / Hybrid / EV"
    description: "Prioritize MPG or electric range"
  - label: "Tech & safety package"
    description: "Latest driver assist, infotainment, cameras"
```

**Question 4: Priorities**
```
header: "Priorities"
question: "Which priorities matter most to you? Select all that apply."
multiSelect: true
options:
  - label: "Reliability & low maintenance"
    description: "Minimize breakdowns and repair costs"
  - label: "Resale value & depreciation"
    description: "Hold value over time"
  - label: "Comfort & interior quality"
    description: "Ride comfort, materials, noise"
  - label: "Performance & driving dynamics"
    description: "Power, handling, acceleration"
```

**Round 2.5 (Conditional)** — If the user selected "Towing capacity" in Q3 OR selected "Truck" in Q1, present this follow-up question:

**Question 5: Towing Requirements**
```
header: "Towing"
question: "What do you need to tow and approximately how heavy?"
multiSelect: false
options:
  - label: "Light (under 3,500 lbs)"
    description: "Small utility trailer, jet skis, lightweight camper"
  - label: "Medium (3,500-7,000 lbs)"
    description: "Boat, travel trailer, car on open trailer"
  - label: "Heavy (7,000-10,000 lbs)"
    description: "Large boat, fifth wheel, heavy equipment trailer"
  - label: "Max (10,000+ lbs)"
    description: "Horse trailer, large RV, heavy commercial loads"
```

If towing was NOT selected and vehicle type is not Truck, skip this question entirely.

After all rounds, build a **Requirements Profile** JSON:
```json
{
  "vehicle_type": "[answer from Q1]",
  "budget_range": "[answer from Q2, e.g. '$30K-$50K']",
  "buying_preference": "[extracted from Q2, e.g. 'New preferred']",
  "must_haves": ["[selected items from Q3]"],
  "priorities": ["[selected items from Q4]"],
  "towing_requirement": "[answer from Q5, e.g. 'Medium (3,500-7,000 lbs)' or null if not asked]",
  "additional_notes": "[any freeform text if 'Other' was chosen]"
}
```

### Phase 2: Discovery Brief & Approval

1. **Parse depth**: Extract `--depth` flag from $ARGUMENTS. Default: `standard`.

2. **Show Discovery Brief**:
```
VEHICLE RECOMMENDATION BRIEF
=============================
Vehicle Type: [from Q1]
Budget: [from Q2]
Must-Haves: [from Q3]
Priorities: [from Q4]
Depth: [quick | standard | deep]
Estimated time: [5-10 min | 15-25 min | 30-45 min]

Research agents will analyze:
- Market pricing, incentives & depreciation (market-researcher)
- Reliability ratings, recalls & owner experiences (reliability-analyst)
- Insurance, fuel, maintenance & total cost of ownership (cost-analyst)
- Feature matching, safety ratings & trim recommendations (feature-matcher)
```

3. **APPROVAL GATE** (standard/deep only): Ask the user to confirm before proceeding. For `quick` depth, show brief but proceed immediately.

### Phase 3: Agent Dispatch

#### Quick Mode (depth=quick)
Launch all 4 agents but with reduced search counts (5-8 per agent). No cross-referencing.

#### Standard Mode (depth=standard, default)
Launch 4 research agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Searches | Focus |
|-------|--------------|-------|----------|-------|
| market-researcher | general-purpose | opus | 10-15 | MSRP, dealer pricing, incentives, supply, depreciation |
| reliability-analyst | general-purpose | opus | 10-15 | Consumer Reports, JD Power, NHTSA recalls, owner forums |
| cost-analyst | general-purpose | sonnet | 10-15 | Insurance, fuel costs, maintenance, TCO over 3/5/7 years |
| feature-matcher | general-purpose | sonnet | 10-15 | Must-have matching, trim analysis, safety ratings, features |

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The Requirements Profile JSON from the interview
3. Depth-specific search count guidance
4. List of 8-12 candidate vehicles appropriate for the user's type + budget (research these briefly before dispatch)
5. Instruction to return structured JSON with per-vehicle findings

#### Deep Mode (depth=deep)
Same as standard but:
- Each agent gets 15-20 searches instead of 10-15
- After the 4 primary agents complete, the ranker agent does follow-up searches to cross-reference and validate

### Phase 4: Ranking

1. **Collect results**: Use `TaskOutput` with `block=true` for each agent. Handle failures gracefully — if an agent fails, note it in the final output and proceed with available results.

2. **Launch recommendation-ranker**: Use `Task` (subagent_type: `general-purpose`, model: `sonnet`) with:
   - The ranker's full instructions (read from `agents/recommendation-ranker.md`)
   - All 4 agent outputs concatenated
   - The Requirements Profile JSON
   - Depth level (determines shortlist size)

3. **Collect ranked recommendations**: The ranker writes to `/tmp/vehicle_recommendations.json`.

### Phase 5: Display Results

Present the ranked recommendations in chat:

```
## Vehicle Recommendations: [Vehicle Type] under [Budget]

**Date**: YYYY-MM-DD | **Depth**: standard | **Vehicles analyzed**: [N] -> [M] ranked

### Your Requirements
- Type: [vehicle_type] | Budget: [budget_range] ([buying_preference])
- Must-haves: [must_haves joined]
- Priorities: [priorities joined]

### Recommendations

| # | Vehicle | Tier | Score | Fit | Market | Year | MSRP |
|---|---------|------|-------|-----|--------|------|------|
| 1 | [make_model trim] | TOP_PICK | 91 | 94 | 87 | 2026 | $36,500 |
| 2 | [make_model trim] | RECOMMENDED | 83 | 80 | 87 | 2026 | $39,950 |
| ... | ... | ... | ... | ... | ... | ... | ... |

### Top 3 Detail

**#1: [Make Model Trim]** (TOP_PICK — 91)
> [One-sentence summary of why this is the top pick]
- Reliability: [rating] | TCO (5yr): [$XX,XXX] | Resale (3yr): [XX%]
- Pros: [2-3 key strengths]
- Cons: [1-2 honest weaknesses]
- Best trim: [trim — adds ...]
- **Find deals**: `/vehicle-finder:find-vehicle [finder_prompt]`

**#2: [Make Model Trim]** (RECOMMENDED — 83)
> [Summary]
...

**#3: [Make Model Trim]** (RECOMMENDED/CONSIDER — XX)
> [Summary]
...

### Segment Insights
- **Best value**: [themes.best_value]
- **Reliability leader**: [themes.reliability_leader]
- **Rising star**: [themes.rising_star]

### Next Steps
- Compare top picks: `/vehicle-recommender:vehicle-compare [Vehicle1] vs [Vehicle2]`
- Find inventory/deals: Use the finder_prompt for any vehicle above
- Recall this list: `/vehicle-recommender:recommendation-list`
- Export to PDF/HTML: Request export and the script will generate files
```

### Phase 6: Export (optional)

If the user requests export, or for deep depth:
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/vehicle_recommender_export.py --input /tmp/vehicle_recommendations.json
```

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Recommendations/`

## Depth Reference

| Depth | Searches/agent | Agents | Cross-ref | Time |
|-------|---------------|--------|-----------|------|
| quick | 5-8 | 4 parallel | No | 5-10 min |
| standard | 10-15 | 4 parallel | Yes (ranker) | 15-25 min |
| deep | 15-20 | 4 parallel + ranker follow-up | Yes | 30-45 min |

## Candidate Vehicle Selection

Before dispatching agents, select 8-12 candidate vehicles appropriate for the user's type + budget using 2-3 quick WebSearch queries:
- `"best [vehicle_type]" [budget_range] 2025 OR 2026`
- `"top rated [vehicle_type]" under [price] [must_haves]`
- `"[vehicle_type] comparison" [budget_range] [priorities]`

This initial candidate list guides the research agents — they should focus on these vehicles but can add others they discover.

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data, statistics, prices, or ratings.
- Present the Discovery Brief and wait for approval (standard/deep) before dispatching agents.
- Handle agent failures gracefully — proceed with available results and note gaps.
- The `finder_prompt` in each recommendation must be a ready-to-paste search string for the future `/vehicle-finder` plugin.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Recommendations/`
- Always include both pros AND cons for every vehicle — no vehicle is perfect.
- Scoring must be honest. A vehicle that misses a must-have should score low on fit regardless of other strengths.
