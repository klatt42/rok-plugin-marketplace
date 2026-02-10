name: vehicle-research
description: |
  Multi-dimensional vehicle research methodology for personalized recommendations.
  Four research agents (market, reliability, cost, features) with configurable
  depth levels. Interview-driven requirements gathering with AskUserQuestion.
  Use when running /recommend-vehicle or discussing vehicle research strategy.

## Vehicle Research Methodology

### Four Research Dimensions

**Market Research**: Analyze current pricing, dealer incentives, supply levels, and depreciation trends. Key sources are Edmunds, KBB, and Cars.com for real-time market data. The goal is understanding what a vehicle costs today and what it will cost to own over time from a market perspective.

**Reliability Analysis**: Evaluate dependability using Consumer Reports ratings, JD Power studies, NHTSA recall data, and long-term owner experiences. This dimension separates vehicles that will be trouble-free from those with known issues. First-year models and new platforms warrant extra scrutiny.

**Cost Analysis**: Calculate total cost of ownership (TCO) across insurance, fuel/energy, maintenance, repairs, and depreciation. TCO often reveals surprising differences — a cheaper purchase price can mean a more expensive vehicle to own. EPA fuel economy and Edmunds True Cost to Own are primary data sources.

**Feature Matching**: Map user must-haves and priorities against each vehicle's trim levels, standard equipment, and available packages. The best recommendation isn't the "best vehicle" — it's the one that best fits what the user actually needs. Always recommend a specific trim.

### Depth Levels

| Depth | Time | Searches/Agent | Shortlist | Cross-Ref |
|-------|------|---------------|-----------|-----------|
| quick | 5-10 min | 5-8 | 5-6 | No |
| standard | 15-25 min | 10-15 | 6-8 | Yes (ranker) |
| deep | 30-45 min | 15-20 | 8-10 | Yes + follow-up |

### Interview-First Approach

Unlike profile-hardcoded plugins, vehicle-recommender uses `AskUserQuestion` to gather requirements dynamically. This means every run is personalized:
1. Vehicle type & purpose
2. Budget & buying preference
3. Must-have features (multi-select)
4. Priorities (multi-select)

The Requirements Profile JSON drives all agent research and scoring.

### Reference Documents

Load `references/source-map.md` for the complete source list with trusted sites per research dimension.
