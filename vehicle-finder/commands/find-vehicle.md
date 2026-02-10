# Vehicle Finder

Search real vehicle inventory from major aggregator sites. Takes a `finder_prompt` from vehicle-recommender output (or freeform search text) and finds actual listings with pricing, dealer info, and deal ratings. The downstream partner to `/vehicle-recommender:recommend-vehicle`.

## Usage

```
/vehicle-finder:find-vehicle 2026 Toyota RAV4 Hybrid XLE, new, within 50 miles, under $38,000, AWD
/vehicle-finder:find-vehicle --from-recommendations                    # Load from last recommender run
/vehicle-finder:find-vehicle --from-recommendations --top=3            # Search for top 3 recommendations
/vehicle-finder:find-vehicle 2025 Honda CR-V Hybrid, used, under $32,000 --radius=100
```

## Arguments

- `$ARGUMENTS` — Either a freeform finder prompt OR `--from-recommendations` flag
- `--radius` (optional): Search radius in miles (default: 50)
- `--from-recommendations`: Load finder_prompts from `/tmp/vehicle_recommendations.json`
- `--top=N`: When using `--from-recommendations`, search for top N vehicles (default: 1)

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Parse Input

**If `--from-recommendations` is in $ARGUMENTS:**
1. Read `/tmp/vehicle_recommendations.json`
2. Validate it has `type: "vehicle_recommendations"` and a `recommendations` array
3. Extract the `--top=N` value (default: 1)
4. For each of the top N recommendations, extract the `finder_prompt` field
5. If no `finder_prompt` field exists, construct one from `make_model`, `trim`, `year`, and `msrp_range`
6. Process each finder_prompt through the search pipeline below (sequentially for multiple vehicles)

**If freeform text:**
Parse the text into structured search parameters. Extract these fields using the text content:
```json
{
  "year": "2026",
  "make": "Toyota",
  "model": "RAV4 Hybrid",
  "trim_preferences": ["XLE", "XLE Premium"],
  "condition": "new",
  "radius_miles": 50,
  "max_price": 38000,
  "features": ["AWD"],
  "zip_code": "20147"
}
```

**Parsing rules:**
- Year: Look for 4-digit number starting with 20
- Make/Model: Common vehicle makes (Toyota, Honda, Ford, Chevy, etc.) followed by model name
- Trim: After model name, common trims (XLE, EX, Limited, Sport, etc.)
- Condition: "new", "used", "certified", "CPO" — default to "new" if not specified
- Radius: "within X miles" or `--radius=X` — default to 50
- Price: "under $X", "below $X,000", "$X" — extract numeric value
- Features: Known keywords like "AWD", "4WD", "hybrid", "leather", "sunroof"
- Zip code: 5-digit number, or extract from "near [city]"

**If zip_code is missing**, use AskUserQuestion:
```
header: "Location"
question: "What's your zip code for the inventory search?"
options:
  - label: "20147"
    description: "Ashburn, VA (Northern Virginia)"
  - label: "20001"
    description: "Washington, DC"
  - label: "21201"
    description: "Baltimore, MD"
```

### Phase 2: Search Brief

Display the search parameters and proceed immediately (no approval gate):

```
VEHICLE INVENTORY SEARCH
========================
Vehicle: [year] [make] [model]
Trims: [trim_preferences joined]
Condition: [condition]
Budget: Under $[max_price]
Radius: [radius_miles] miles from [zip_code]
Features: [features joined]

Searching: Cars.com, AutoTrader, CarGurus, Edmunds, TrueCar
Dispatching 2 research agents + 1 ranker...
```

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
- The ranker writes results to `/tmp/vehicle_inventory_results.json`

Collect the ranker output with `TaskOutput` (block=true).

### Phase 5: Display Results

Present ranked results in chat:

```
## Inventory Results: [year] [make] [model]

**Search**: [trims] | [condition] | Under $[max_price] | Within [radius]mi of [zip]
**Found**: [total_listings_found] listings -> [unique_listings] unique -> Top [N] shown

### Listings

| # | Deal | Vehicle | Price | vs FMV | Miles | Dealer | Rating |
|---|------|---------|-------|--------|-------|--------|--------|
| 1 | GREAT | [year] [model] [trim] | $XX,XXX | -$X,XXX | XXmi | [dealer] | X.X* |
| 2 | GOOD | [year] [model] [trim] | $XX,XXX | -$XXX | XXmi | [dealer] | X.X* |
| ... |

### Best Deal Detail

**#1: [year] [make] [model] [trim]** (GREAT_DEAL)
> $X,XXX below fair market value at a top-rated dealer XX miles away
- Price: $XX,XXX (MSRP $XX,XXX | FMV ~$XX,XXX)
- Color: [exterior] / [interior]
- Key Features: [features list]
- Dealer: [name] ([rating]*, [review_count] reviews)
- Source: [source] | [listing_url]
- **Action**: Call [phone] or request internet price

### Market Context
- Average asking price: $XX,XXX
- Fair market value: ~$XX,XXX
- Listings found: [total] within [radius] miles
- Best time to buy: [insight from price-validator]
- Current incentives: [incentives list]

### Next Steps
- Deep-dive on a listing: `/vehicle-finder:listing-details #1`
- Expand search: `/vehicle-finder:find-vehicle [original prompt] --radius=100`
- Compare recommendations: `/vehicle-recommender:vehicle-compare`
```

For the top 3 listings, show the expanded detail block. For listings 4+, the table row is sufficient.

### Phase 6: Export (optional)

If the user requests export OR if results were loaded from recommendations (suggesting a complete workflow):
```bash
~/.claude/scripts/.venv/bin/python3 [plugin_scripts_dir]/vehicle_finder_export.py --input /tmp/vehicle_inventory_results.json
```

Where `[plugin_scripts_dir]` is the path to this plugin's `scripts/` directory.

Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Inventory/`

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- All research uses WebSearch. Do not fabricate listings, prices, VINs, or dealer names.
- No approval gate — this is a quick search, not a 30-minute research session. Show the brief and proceed.
- Handle agent failures gracefully — proceed with available results and note gaps.
- The `deal_rating` must be based on actual FMV comparison, not subjective judgment.
- Always show both the asking price AND the FMV comparison so the user can assess value.
- Include dealer contact info (phone, listing URL) for actionable next steps.
- If searching multiple vehicles from `--from-recommendations`, process them sequentially and present results grouped by vehicle.
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Inventory/`
