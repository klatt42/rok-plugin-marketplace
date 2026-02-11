# Camper Recommender

Interview-driven camper and RV recommendation engine. Gathers your requirements through structured questions, then dispatches 4 parallel research agents to analyze market pricing, build quality, cost-of-ownership, and floorplan/feature matching. Produces ranked recommendations with ready-to-paste finder prompts for `/camper-finder` plugin handoff.

## Usage

```
/camper-recommender:recommend-camper                          # Standard depth, full interview
/camper-recommender:recommend-camper --depth=quick            # Quick scan, fewer searches
/camper-recommender:recommend-camper --depth=deep             # Deep research, more thorough
```

## Arguments

- **--depth** (optional): `quick` (5-10 min), `standard` (15-25 min, default), `deep` (30-45 min).

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Interview

Conduct a structured interview using `AskUserQuestion` to gather the user's camper/RV requirements. Present questions in 2-3 rounds.

**Round 1** — Two questions in a single `AskUserQuestion` call:

**Question 1: Camper/RV Type**
```
header: "RV type"
question: "What type of camper or RV are you looking for?"
multiSelect: false
options:
  - label: "Travel Trailer"
    description: "Towable, 15-35ft, most popular type"
  - label: "Class C Motorhome"
    description: "Drivable, cab-over bed, 20-33ft"
  - label: "Class A Motorhome"
    description: "Full-size drivable, bus-style, 25-45ft"
  - label: "Other"
    description: "Fifth wheel, pop-up, truck camper, Class B van, toy hauler"
```

**Question 2: Budget & Buying Preference**
```
header: "Budget"
question: "What's your budget range and buying preference?"
multiSelect: false
options:
  - label: "Under $25K — Used"
    description: "Entry-level, value-focused, used market"
  - label: "$25K-$50K — New or Used"
    description: "Mid-range, good selection both new and used"
  - label: "$50K-$100K — New preferred"
    description: "Premium features, newer models"
  - label: "$100K+ — New luxury"
    description: "Top-tier brands, full-time livability"
```

**Round 2** — Two multi-select questions in a single `AskUserQuestion` call:

**Question 3: Must-Haves**
```
header: "Must-haves"
question: "Which features are must-haves? Select all that apply."
multiSelect: true
options:
  - label: "Slide-out(s)"
    description: "Expandable living space when parked"
  - label: "Full bathroom"
    description: "Shower, toilet, sink — not just a wet bath"
  - label: "Bunk beds / sleeps 6+"
    description: "Family-sized sleeping capacity"
  - label: "Off-grid capable"
    description: "Solar, lithium batteries, dry camping ready"
```

**Question 4: Priorities**
```
header: "Priorities"
question: "Which priorities matter most to you? Select all that apply."
multiSelect: true
options:
  - label: "Build quality & durability"
    description: "Solid construction, minimal warranty issues"
  - label: "Lightweight / easy towing"
    description: "Under 5,000 lbs, half-ton towable"
  - label: "Resale value"
    description: "Hold value over time"
  - label: "Livability & comfort"
    description: "Full-time living potential, residential features"
```

**Round 2.5 (Conditional)** — If Q1 answer is "Travel Trailer", "Fifth Wheel", "Toy Hauler", or any other towable type from the "Other" option (pop-up, truck camper), present this follow-up question. Skip for Class A and Class C motorhomes (they are self-propelled).

**Question 5: Tow Vehicle**
```
header: "Tow vehicle"
question: "What are you towing with?"
multiSelect: false
options:
  - label: "Half-ton truck (F-150, Ram 1500, Silverado 1500)"
    description: "Max ~9,000-12,000 lbs towing capacity"
  - label: "Three-quarter or one-ton truck (F-250/350, Ram 2500/3500)"
    description: "Max ~15,000-25,000 lbs towing capacity"
  - label: "SUV or midsize truck"
    description: "Max ~5,000-8,500 lbs towing capacity"
  - label: "Don't have one yet"
    description: "Need guidance on tow vehicle matching"
```

If the camper type is a motorhome (Class A, Class B, Class C), skip this question entirely.

After all rounds, build a **Requirements Profile** JSON:
```json
{
  "camper_type": "[answer from Q1]",
  "budget_range": "[answer from Q2, e.g. '$25K-$50K']",
  "buying_preference": "[extracted from Q2, e.g. 'New or Used']",
  "must_haves": ["[selected items from Q3]"],
  "priorities": ["[selected items from Q4]"],
  "tow_vehicle": "[answer from Q5, e.g. 'Half-ton truck (F-150, Ram 1500, Silverado 1500)' or null if motorhome]",
  "additional_notes": "[any freeform text if 'Other' was chosen]"
}
```

### Phase 2: Discovery Brief & Approval

1. **Parse depth**: Extract `--depth` flag from $ARGUMENTS. Default: `standard`.

2. **Show Discovery Brief**:
```
CAMPER/RV RECOMMENDATION BRIEF
================================
RV Type: [from Q1]
Budget: [from Q2]
Must-Haves: [from Q3]
Priorities: [from Q4]
Tow Vehicle: [from Q5, or "N/A (motorhome)" if not asked]
Depth: [quick | standard | deep]
Estimated time: [5-10 min | 15-25 min | 30-45 min]

Research agents will analyze:
- Market pricing, incentives & depreciation (market-researcher)
- Build quality, recalls & owner experiences (reliability-analyst)
- Insurance, storage, maintenance & total cost of ownership (cost-analyst)
- Floorplan matching, weight, amenities & livability (feature-matcher)
```

3. **APPROVAL GATE** (standard/deep only): Ask the user to confirm before proceeding. For `quick` depth, show brief but proceed immediately.

### Phase 3: Agent Dispatch

#### Quick Mode (depth=quick)
Launch all 4 agents but with reduced search counts (5-8 per agent). No cross-referencing.

#### Standard Mode (depth=standard, default)
Launch 4 research agents simultaneously in a SINGLE message using `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Searches | Focus |
|-------|--------------|-------|----------|-------|
| market-researcher | general-purpose | opus | 10-15 | MSRP by floorplan, dealer pricing, show season deals, depreciation |
| reliability-analyst | general-purpose | opus | 10-15 | Build quality, common issues, warranty, manufacturer reputation |
| cost-analyst | general-purpose | sonnet | 10-15 | Insurance, storage, maintenance, campground costs, TCO |
| feature-matcher | general-purpose | sonnet | 10-15 | Floorplan matching, weight vs tow vehicle, tanks, amenities |

**For each agent prompt, include**:
1. The agent's full instructions (read from `agents/[agent-name].md` relative to this command)
2. The Requirements Profile JSON from the interview
3. Depth-specific search count guidance
4. List of 8-12 candidate campers/RVs appropriate for the user's type + budget (research these briefly before dispatch)
5. Instruction to return structured JSON with per-camper findings

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

3. **Collect ranked recommendations**: The ranker writes to `/tmp/camper_recommendations.json`.

### Phase 5: Display Results

Present the ranked recommendations in chat:

```
## Camper/RV Recommendations: [RV Type] under [Budget]

**Date**: YYYY-MM-DD | **Depth**: standard | **Campers analyzed**: [N] -> [M] ranked

### Your Requirements
- Type: [camper_type] | Budget: [budget_range] ([buying_preference])
- Must-haves: [must_haves joined]
- Priorities: [priorities joined]
- Tow vehicle: [tow_vehicle or "N/A (motorhome)"]

### Recommendations

| # | Camper | Tier | Score | Fit | Market | Year | MSRP | Weight |
|---|--------|------|-------|-----|--------|------|------|--------|
| 1 | [make floorplan] | TOP_PICK | 88 | 91 | 84 | 2025 | $42,000 | 5,800 lbs |
| 2 | [make floorplan] | RECOMMENDED | 79 | 82 | 75 | 2025 | $38,000 | 5,200 lbs |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Top 3 Detail

**#1: [Make Model Floorplan]** (TOP_PICK — 88)
> [One-sentence summary of why this is the top pick]
- Build Quality: [rating] | TCO (5yr): [$XX,XXX] | Resale (3yr): [XX%]
- Specs: [length]ft | [weight] lbs dry | [slides] slide(s) | Sleeps [N]
- Tanks: [fresh]gal fresh / [gray]gal gray / [black]gal black
- Pros: [2-3 key strengths]
- Cons: [1-2 honest weaknesses]
- Best floorplan: [floorplan — description of layout]
- **Find deals**: `/camper-finder:find-camper [finder_prompt]`

**#2: [Make Model Floorplan]** (RECOMMENDED — 79)
> [Summary]
...

**#3: [Make Model Floorplan]** (RECOMMENDED/CONSIDER — XX)
> [Summary]
...

### Segment Insights
- **Best value**: [themes.best_value]
- **Quality leader**: [themes.quality_leader]
- **Rising star**: [themes.rising_star]

### Next Steps
- Compare top picks: `/camper-recommender:camper-compare [Camper1] vs [Camper2]`
- Find inventory/deals: Use the finder_prompt for any camper above
- Recall this list: `/camper-recommender:camper-list`
- Export to PDF/HTML: Request export and the script will generate files
```

### Phase 6: Export (optional)

If the user requests export, or for deep depth:
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/camper_recommender_export.py --input /tmp/camper_recommendations.json
```

Where `[plugin_scripts_dir]` is the path to this plugin's `scripts/` directory (relative to this command file, go up one level then into `scripts/`).

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Recommendations/`

## Depth Reference

| Depth | Searches/agent | Agents | Cross-ref | Time |
|-------|---------------|--------|-----------|------|
| quick | 5-8 | 4 parallel | No | 5-10 min |
| standard | 10-15 | 4 parallel | Yes (ranker) | 15-25 min |
| deep | 15-20 | 4 parallel + ranker follow-up | Yes | 30-45 min |

## Candidate Camper Selection

Before dispatching agents, select 8-12 candidate campers/RVs appropriate for the user's type + budget using 2-3 quick WebSearch queries:
- `"best [rv_type]" [budget_range] 2025 OR 2026`
- `"top rated [rv_type]" under [price] [must_haves]`
- `"[rv_type] comparison" [budget_range] [priorities]`

This initial candidate list guides the research agents — they should focus on these campers but can add others they discover.

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate data, statistics, prices, or ratings.
- Present the Discovery Brief and wait for approval (standard/deep) before dispatching agents.
- Handle agent failures gracefully — proceed with available results and note gaps.
- The `finder_prompt` in each recommendation must be a ready-to-paste search string for the `/camper-finder` plugin.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Recommendations/`
- Always include both pros AND cons for every camper — no camper is perfect.
- Scoring must be honest. A camper that misses a must-have should score low on fit regardless of other strengths.
- If the user specified a tow vehicle, treat exceeding tow capacity as a must-have miss.
- RV depreciation is steeper than vehicles — always note this in market context.
