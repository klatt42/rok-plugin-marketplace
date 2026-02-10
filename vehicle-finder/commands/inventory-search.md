# Inventory Search

Standalone vehicle inventory search without needing a prior vehicle-recommender run. Uses a quick 2-question interview to gather search parameters, then finds real listings with deal ratings.

## Usage

```
/vehicle-finder:inventory-search                        # Start with interview
/vehicle-finder:inventory-search --radius=100           # Custom search radius
```

## Arguments

- `$ARGUMENTS` — Optional flags only (no freeform vehicle text — use `find-vehicle` for that)
- `--radius` (optional): Search radius in miles (default: 50)

Initial request: $ARGUMENTS

## Workflow

### Phase 1: Quick Interview

Conduct a 2-round interview using `AskUserQuestion`.

**Round 1** — Two questions in a single `AskUserQuestion` call:

**Question 1: What Vehicle?**
```
header: "Vehicle"
question: "What vehicle are you looking for?"
multiSelect: false
options:
  - label: "Specific model"
    description: "I know exactly what I want (e.g., 2026 Toyota RAV4)"
  - label: "Browse a type"
    description: "Show me what's available (e.g., compact SUVs under $35K)"
```

**Question 2: New or Used?**
```
header: "Condition"
question: "New, used, or either?"
multiSelect: false
options:
  - label: "New only"
    description: "Factory new, full warranty"
  - label: "Certified Pre-Owned"
    description: "Used with manufacturer certification"
  - label: "Either"
    description: "Show both new and used options"
```

**After Round 1:**

If user selected "Specific model", ask a follow-up with `AskUserQuestion`:

**Question 3: Vehicle Details**
```
header: "Details"
question: "Tell me the year, make, model, and your budget. (Example: 2026 Toyota RAV4 Hybrid, under $38,000)"
options:
  - label: "I'll type it"
    description: "Enter year, make, model, and budget"
```

The user will type in the "Other" freeform field with their specific vehicle details.

If user selected "Browse a type", ask:

**Question 3 (Browse):**
```
header: "Type"
question: "What type of vehicle and budget?"
multiSelect: false
options:
  - label: "Compact SUV under $35K"
    description: "RAV4, CR-V, Tucson, CX-50 size"
  - label: "Midsize SUV under $45K"
    description: "Highlander, Pilot, Telluride size"
  - label: "Truck under $50K"
    description: "Tacoma, Ranger, Colorado, Frontier"
  - label: "Sedan under $30K"
    description: "Camry, Accord, Civic, Corolla"
```

**Question 4: Location**
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

### Phase 2: Build Search Parameters

From the interview answers, construct the search_params JSON:
```json
{
  "year": "2026",
  "make": "Toyota",
  "model": "RAV4 Hybrid",
  "trim_preferences": [],
  "condition": "New",
  "radius_miles": 50,
  "max_price": 38000,
  "features": [],
  "zip_code": "20147"
}
```

If the user selected "Browse a type", select 3-4 popular models in that category and search for the top-selling one first.

### Phase 3-6: Same as find-vehicle

From this point, follow the exact same Phase 3 (Agent Dispatch), Phase 4 (Ranking), Phase 5 (Display Results), and Phase 6 (Export) workflow as defined in `find-vehicle.md`.

Read the agent files relative to this command:
- `agents/inventory-searcher.md`
- `agents/price-validator.md`
- `agents/listing-ranker.md`

## Rules

- This is a READ-ONLY research tool. Never create apps, write code, or modify repositories.
- The interview is intentionally short — 2-3 questions max. Don't over-interview.
- For "Browse a type", pick the most popular vehicle in that category as the primary search target.
- All other rules from `find-vehicle.md` apply (no fabricated data, handle failures gracefully, etc.).
- Export files go to: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Inventory/`
