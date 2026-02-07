---
name: creator-profiles
description: |
  Trusted YouTube creator registry and authority weighting system for video
  analysis. Defines trust tiers (HIGH, MEDIUM, STANDARD) with domain-specific
  expertise mapping. Pre-configured with Cole Medin (AI agents, Claude Code,
  MCP), IndyDevDan (agentic workflows, Claude Code CLI), and Chris Koerner
  (AI tools, agentic workflows). Trust level affects recommendation confidence
  scoring in /yt-analyze output.
triggers:
  - "trusted creator"
  - "cole medin"
  - "indydevdan"
  - "chris koerner"
  - "creator profile"
  - "youtube channel trust"
version: 1.0
author: ROK Agency
---

# Creator Profiles & Trust Weighting

## When to Use This Skill

Use when `/yt-analyze` needs to weight recommendations based on creator authority, or when managing the creator registry via `/yt-creators`.

## Trust Tiers

| Tier | Weight Range | Criteria | Assignment |
|------|-------------|----------|------------|
| **HIGH** | 0.85 - 1.0 | Domain authority, proven track record, patterns already adopted by ROK | Creator's work is foundational to ROK or user has explicitly designated them |
| **MEDIUM** | 0.55 - 0.75 | Known expert, consistent quality, relevant domain | User follows and trusts this creator |
| **STANDARD** | 0.25 - 0.45 | Unknown or new creator, no track record established | Default for any unrecognized channel |

## Default Creator Registry

| Channel | Aliases | Domain Expertise | Trust | Rationale |
|---------|---------|-----------------|-------|-----------|
| Cole Medin | coleam00 | AI agents, Claude Code, MCP, PRD methodology, Bolt.new, Windsurf | HIGH | ROK methodology source. Quoted in CLAUDE.md. "The PRD is the north star." |
| IndyDevDan | - | Agentic workflows, Claude Code CLI, CLAUDE.md patterns, task automation | HIGH | Agentic patterns authority. Quoted in CLAUDE.md. "Agents + code beats agents alone." |
| Chris Koerner | - | AI tools, agentic workflows, AI automation | HIGH | Trusted source for cutting-edge AI developments and tool evaluations. |

## Weighting Formula

```
recommendation_confidence = creator_trust_weight * validation_score * relevance_score
```

Where:
- `creator_trust_weight` = Trust tier value (see table above)
- `validation_score` = External research confirmation (0.0 - 1.0)
  - Confirmed by 2+ sources: 1.0
  - Partially confirmed: 0.7
  - Unconfirmed (no sources found): 0.4
  - Contradicted by sources: 0.1
- `relevance_score` = How relevant to current ROK needs (0.0 - 1.0)
  - Directly applicable to active project/workflow: 1.0
  - Generally useful for ROK methodology: 0.7
  - Interesting but tangential: 0.4
  - Not relevant to ROK: 0.1

### Confidence Labels

| Combined Score | Label | Action |
|---------------|-------|--------|
| 0.7 - 1.0 | **HIGH** | Strong recommendation - implement or plan |
| 0.4 - 0.69 | **MEDIUM** | Worth considering - research further |
| 0.1 - 0.39 | **LOW** | Note for awareness - do not act without more evidence |

## Domain Matching

When a trusted creator speaks **within their domain of expertise**, their trust weight applies fully. When speaking **outside their primary domain**, reduce the trust weight by 0.2 (floor at STANDARD tier minimum).

**Example:**
- Cole Medin on MCP servers = full HIGH weight (0.9)
- Cole Medin on Kubernetes networking = HIGH - 0.2 = 0.7 (still strong, but noted as out-of-domain)

Domain matching is fuzzy - adjacent domains (e.g., "Claude Code" creator discussing "AI agents" broadly) should still get full weight. Only reduce for clearly unrelated domains.

## Creator Registry Storage

**Location:** `~/.claude/youtube-intelligence/creators.json`

**Schema:**
```json
{
  "channels": [
    {
      "name": "Channel Name",
      "aliases": ["alt-name1"],
      "domains": ["domain-1", "domain-2"],
      "trust": "HIGH|MEDIUM",
      "notes": "Why this creator is trusted",
      "added": "YYYY-MM-DD",
      "videos_analyzed": 0
    }
  ]
}
```

## Channel Name Matching

When identifying a creator from video metadata:
1. Exact match on `name` field (case-insensitive)
2. Exact match on any `aliases` entry (case-insensitive)
3. Partial match (channel name contains creator name or vice versa)
4. If no match found, assign STANDARD trust tier

## Updating Creator Stats

After each `/yt-analyze` run, increment `videos_analyzed` for the matched creator. This tracks engagement with each creator over time for `/yt-library stats`.
