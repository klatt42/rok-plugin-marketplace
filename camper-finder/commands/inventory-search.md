# Inventory Search

Standalone camper/RV inventory search without needing a prior camper-recommender run. Uses a quick 2-question interview to gather search parameters, then finds real listings with deal ratings.

## Usage

```
/camper-finder:inventory-search                        # Start with interview
```

## Arguments

- `$ARGUMENTS` — Optional flags only (no freeform camper text — use `find-camper` for that)

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Quick Interview

Conduct a 2-round interview using `AskUserQuestion`.

**Round 1** — Two questions in a single `AskUserQuestion` call:

**Question 1: What Camper/RV?**
```
header: "Camper"
question: "What camper or RV are you looking for?"
multiSelect: false
options:
  - label: "Specific model"
    description: "I know exactly what I want (e.g., 2025 Grand Design Imagine 2500RL)"
  - label: "Browse a type"
    description: "Show me what's available (e.g., travel trailers under $40K)"
```

**Question 2: New or Used?**
```
header: "Condition"
question: "New, used, or either?"
multiSelect: false
options:
  - label: "New only"
    description: "Factory new, full warranty"
  - label: "Used / Pre-owned"
    description: "Used, possibly dealer-inspected"
  - label: "Either"
    description: "Show both new and used options"
```

**After Round 1:**

If user selected "Specific model", ask a follow-up with `AskUserQuestion`:

**Question 3: Camper Details**
```
header: "Details"
question: "Tell me the year, make, model, floorplan, and your budget. (Example: 2025 Grand Design Imagine 2500RL, under $45,000)"
options:
  - label: "I'll type it"
    description: "Enter year, make, model, floorplan, and budget"
```

The user will type in the "Other" freeform field with their specific camper details.

If user selected "Browse a type", ask:

**Question 3 (Browse):**
```
header: "Type"
question: "What type of RV and budget?"
multiSelect: false
options:
  - label: "Travel trailer under $40K"
    description: "Most popular type — towable, 15-35ft"
  - label: "Travel trailer under $60K"
    description: "Premium travel trailers with more features"
  - label: "Fifth wheel under $60K"
    description: "Larger towable, requires 3/4-ton+ truck"
  - label: "Class C motorhome under $120K"
    description: "Drivable, cab-over bed, 20-33ft"
```

**Question 4: Location & Radius** — Single `AskUserQuestion` with 2 questions:

```
header: "Location"
question: "What zip code should we search from?"
options:
  - label: "20147"
    description: "Ashburn, VA (Northern Virginia)"
  - label: "20001"
    description: "Washington, DC"
  - label: "21201"
    description: "Baltimore, MD"
```

```
header: "Radius"
question: "How far are you willing to travel?"
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

### Phase 2: Build Search Parameters

From the interview answers, construct the search_params JSON:
```json
{
  "year": "2024-2025",
  "make": "Grand Design",
  "model": "Imagine",
  "floorplan": "2500RL",
  "rv_type": "Travel Trailer",
  "condition": "New",
  "radius_miles": 100,
  "max_price": 45000,
  "features": [],
  "zip_code": "20147"
}
```

If the user selected "Browse a type", select 3-4 popular models in that category and search for the top-selling one first.

### Phase 3-6: Same as find-camper

From this point, follow the exact same Phase 3 (Agent Dispatch), Phase 4 (Ranking), Phase 5 (Display Results), and Phase 6 (Export) workflow as defined in `find-camper.md`.

Read the agent files relative to this command:
- `agents/inventory-searcher.md`
- `agents/price-validator.md`
- `agents/listing-ranker.md`

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- The interview is intentionally short — 2-3 questions max. Don't over-interview.
- For "Browse a type", pick the most popular camper in that category as the primary search target.
- All other rules from `find-camper.md` apply (no fabricated data, approval gate, follow-up questions, handle failures gracefully, etc.).
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Inventory/`
