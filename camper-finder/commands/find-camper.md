# Camper Finder

Search real camper/RV inventory from major aggregator sites. Takes a `finder_prompt` from camper-recommender output (or freeform search text) and finds actual listings with pricing, dealer info, and deal ratings. The downstream partner to `/camper-recommender:recommend-camper`.

## Usage

```
/camper-finder:find-camper 2025 Grand Design Imagine 2500RL, travel trailer, new, under $45,000, 1 slide-out
/camper-finder:find-camper --from-recommendations                    # Load from last recommender run
/camper-finder:find-camper --from-recommendations --top=3            # Search for top 3 recommendations
/camper-finder:find-camper 2024 Jayco Jay Flight 264BH, used, under $28,000
```

## Arguments

- `$ARGUMENTS` — Either a freeform finder prompt OR `--from-recommendations` flag
- `--from-recommendations`: Load finder_prompts from `/tmp/camper_recommendations.json`
- `--top=N`: When using `--from-recommendations`, search for top N campers (default: 1)

Note: Zip code and search radius are always collected via follow-up questions (Phase 1b), not from command-line flags.

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Parse Input

**If `--from-recommendations` is in $ARGUMENTS:**
1. Read `/tmp/camper_recommendations.json`
2. Validate it has `type: "camper_recommendations"` and a `recommendations` array
3. Extract the `--top=N` value (default: 1)
4. For each of the top N recommendations, extract the `finder_prompt` field
5. If no `finder_prompt` field exists, construct one from `make_model`, `floorplan`, `rv_type`, `year`, and `msrp_range`
6. Show the user which camper(s) will be searched, then proceed to Phase 1b (follow-up questions for zip/radius) and Phase 2 (confirmation) before dispatching agents
7. Process each finder_prompt through the search pipeline below (sequentially for multiple campers)

**If freeform text:**
Parse the text into structured search parameters. Extract these fields using the text content:
```json
{
  "year": "2025",
  "make": "Grand Design",
  "model": "Imagine",
  "floorplan": "2500RL",
  "rv_type": "Travel Trailer",
  "condition": "new",
  "max_price": 45000,
  "features": ["1 slide-out", "half-ton towable"],
  "zip_code": "20147",
  "radius_miles": 100
}
```

**Parsing rules:**
- Year: Look for 4-digit number starting with 20
- Make/Model: Common RV makes (Grand Design, Jayco, Forest River, Keystone, Winnebago, Airstream, Coachmen, Thor, etc.) followed by model name
- Floorplan: Alphanumeric code after model name (e.g., 2500RL, 264BH, 24D, 2400BH)
- RV Type: "travel trailer", "fifth wheel", "class a", "class b", "class c", "toy hauler", "pop-up", "truck camper"
- Condition: "new", "used", "pre-owned" — default to "new" if not specified
- Price: "under $X", "below $X,000", "$X-$Y" — extract numeric value(s)
- Features: Known keywords like "slide-out", "bunk beds", "outdoor kitchen", "solar", "off-grid", "half-ton towable"
- Additional constraints: weight limits, length limits, sleeping capacity — preserve these as-is in a `notes` field

**Do NOT parse radius from the prompt text.** Ignore phrases like "within X miles" in the freeform input. Radius is always collected via the follow-up questions below.

### Phase 1b: Follow-Up Questions (REQUIRED)

After parsing the freeform text, you MUST ask follow-up questions before proceeding. Use a SINGLE `AskUserQuestion` call with 2 questions:

**Question 1: Zip Code**
```
header: "Location"
question: "What zip code should we search from?"
multiSelect: false
options:
  - label: "20147"
    description: "Ashburn, VA (Northern Virginia)"
  - label: "20001"
    description: "Washington, DC"
  - label: "21201"
    description: "Baltimore, MD"
```

**Question 2: Search Radius**
```
header: "Radius"
question: "How far are you willing to travel? (RV dealers are spread out — wider radius recommended)"
multiSelect: false
options:
  - label: "50 miles"
    description: "Local dealers only"
  - label: "100 miles (Recommended)"
    description: "Good balance of selection and travel"
  - label: "200 miles"
    description: "Wider net — RV selection varies by region"
  - label: "500 miles"
    description: "Nationwide search — willing to travel or arrange transport"
```

**CRITICAL**: You MUST stop and WAIT for the user's answers before continuing. Do NOT proceed to Phase 2 until you have received the zip code and radius responses. Do NOT dispatch agents, display the brief, or take any other action while waiting.

After receiving answers, update `zip_code` and `radius_miles` in the search parameters.

If the user provided a zip code in the original prompt text (a 5-digit number), pre-select it as the first option but still ask for confirmation.

### Phase 2: Search Summary & Confirmation

Display a summary of ALL parsed search parameters for the user to review:

```
CAMPER/RV INVENTORY SEARCH
============================
Camper: [year] [make] [model] [floorplan]
RV Type: [rv_type]
Condition: [condition]
Budget: $[min_price]-$[max_price] (or "Under $[max_price]")
Radius: [radius_miles] miles from [zip_code]
Features: [features joined]
Notes: [any additional constraints like weight limits, sleeping capacity]

Sources: RVTrader, Camping World, General RV, RVUSA, PPL Motor Homes
Agents: 2 searchers + 1 ranker
```

Then use `AskUserQuestion` to confirm:

```
header: "Confirm"
question: "Does this search look correct? I'll dispatch agents to find matching inventory."
multiSelect: false
options:
  - label: "Search now"
    description: "Looks good — find matching listings"
  - label: "Edit search"
    description: "I need to change something first"
```

**CRITICAL**: You MUST stop and WAIT for confirmation before dispatching agents. If the user selects "Edit search", ask what they want to change and re-display the updated summary for another confirmation. Only proceed to Phase 3 when the user selects "Search now".

### Phase 3: Agent Dispatch

Read the agent instruction files:
- Read `agents/inventory-searcher.md` relative to this command file
- Read `agents/price-validator.md` relative to this command file

Launch 2 agents in parallel via `Task` with `run_in_background: true`:

| Agent | Subagent Type | Model | Prompt Content |
|-------|--------------|-------|----------------|
| inventory-searcher | general-purpose | sonnet | Full agent instructions + search_params JSON |
| price-validator | general-purpose | sonnet | Full agent instructions + search_params JSON |

**Each agent prompt must include:**
1. The agent's full instructions from its `.md` file
2. The structured search parameters JSON
3. Instruction to return structured JSON output (no markdown wrapping)

Use `TaskOutput` with `block=true` to collect results from both agents. Handle failures gracefully — if an agent fails, note it and proceed with available results.

### Phase 4: Ranking

Read `agents/listing-ranker.md` relative to this command file.

Launch the listing-ranker agent via `Task`:
- Subagent type: `general-purpose`
- Model: `haiku`
- Prompt: Full ranker instructions + both agent outputs concatenated + search_params JSON
- The ranker writes results to `/tmp/camper_inventory_results.json`

Collect the ranker output with `TaskOutput` (block=true).

### Phase 5: Display Results

Present ranked results in chat:

```
## Inventory Results: [year] [make] [model] [floorplan]

**Search**: [rv_type] | [condition] | Under $[max_price] | Within [radius]mi of [zip]
**Found**: [total_listings_found] listings -> [unique_listings] unique -> Top [N] shown

### Listings

| # | Deal | Camper | Price | vs FMV | Specs | Dealer | Rating |
|---|------|--------|-------|--------|-------|--------|--------|
| 1 | GREAT | [year] [model] [floorplan] | $XX,XXX | -$X,XXX | [length]ft / [weight]lbs / [slides]sl | [dealer] | X.X* |
| 2 | GOOD | [year] [model] [floorplan] | $XX,XXX | -$XXX | [length]ft / [weight]lbs / [slides]sl | [dealer] | X.X* |
| ... |

### Best Deal Detail

**#1: [year] [make] [model] [floorplan]** (GREAT_DEAL)
> $X,XXX below fair market value at a dealer XX miles away
- Price: $XX,XXX (MSRP $XX,XXX | FMV ~$XX,XXX)
- Specs: [length]ft | [dry_weight] lbs dry | GVWR [gvwr] lbs | [slides] slide(s) | Sleeps [capacity]
- Tanks: [fresh]gal fresh / [gray]gal gray / [black]gal black
- Key Features: [features list]
- Dealer: [name] ([rating]*, [review_count] reviews)
- Source: [source] | [listing_url]
- **Action**: Call [phone] or request internet price
- **Negotiation**: [negotiation_notes]

### Market Context
- Average asking price: $XX,XXX
- Fair market value (NADA): ~$XX,XXX
- Listings found: [total] within [radius] miles
- Best time to buy: [insight from price-validator]
- Current promotions: [incentives list]
- Dealer prep fees: [typical prep fee info]

### Next Steps
- Deep-dive on a listing: `/camper-finder:listing-details #1`
- Expand search: `/camper-finder:find-camper [original prompt]` with wider radius
- Compare recommendations: `/camper-recommender:camper-compare`
```

For the top 3 listings, show the expanded detail block. For listings 4+, the table row is sufficient.

### Phase 6: Export (optional)

If the user requests export OR if results were loaded from recommendations (suggesting a complete workflow):
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/camper_finder_export.py --input /tmp/camper_inventory_results.json
```

Where `[plugin_scripts_dir]` is the path to this plugin's `scripts/` directory.

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Inventory/`

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate listings, prices, stock numbers, or dealer names.
- **APPROVAL GATE REQUIRED**: Always show the search summary and wait for user confirmation before dispatching agents. Never skip the confirmation step.
- **FOLLOW-UP QUESTIONS REQUIRED**: Always ask for zip code and radius via AskUserQuestion, even if hints appear in the prompt text. Wait for answers before proceeding.
- **NO DOUBLE-EXECUTION**: Each AskUserQuestion call must be followed by a full stop. Do not continue processing until the user has responded. Do not call AskUserQuestion and then also dispatch agents in the same turn.
- Handle agent failures gracefully — proceed with available results and note gaps.
- The `deal_rating` must be based on actual FMV comparison (NADA Guides preferred), not subjective judgment.
- Always show both the asking price AND the FMV comparison so the user can assess value.
- Include dealer contact info (phone, listing URL) for actionable next steps.
- Include negotiation notes — RV dealer margins (25-35%) are much larger than auto margins (5-10%).
- If searching multiple campers from `--from-recommendations`, process them sequentially and present results grouped by camper.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Inventory/`
