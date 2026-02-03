# /feynman Command

Override the complexity router and force full Pre-Implementation Protocol for the current task.

**Version**: 2.0 (ROK 3.6-Feynman)

## When to Use

- Task seems simple but feels risky
- You want to ensure thorough analysis
- Previous "simple" approaches have failed
- Exploring unfamiliar territory
- High-stakes changes (auth, payments, data migration)
- When you catch yourself pattern-matching
- When user explicitly requests thorough analysis

## Usage

```
/feynman <task description>
```

## Execution Steps

### 1. Acknowledge Override
```
FEYNMAN PROTOCOL ACTIVATED
Complexity router overridden → Treating as COMPLEX
Full Pre-Implementation Protocol required before any implementation.
```

### 2. Essential Puzzle Reduction (MANDATORY)

Do not proceed until these are answered clearly:

```
═══════════════════════════════════════════════════════
ESSENTIAL PUZZLE REDUCTION
═══════════════════════════════════════════════════════

PROBLEM STATEMENT (one sentence a junior dev would understand):
→

SIMPLEST POSSIBLE EXAMPLE of this problem:
→

SUCCESS CRITERIA (how to verify the solution works):
→

THE CORE PUZZLE (what makes this actually hard?):
→

═══════════════════════════════════════════════════════
```

**Checkpoint**: If any answer is vague or uses jargon without explanation, STOP.
Rephrase until a non-expert would understand.

### 3. Multi-Angle Decomposition (MANDATORY)

Generate THREE distinct approaches. Do not proceed with fewer.

```
═══════════════════════════════════════════════════════
APPROACH A: [Name - Most Obvious/Conventional]
═══════════════════════════════════════════════════════
Description:

Key Assumptions:
1.
2.
3.

What Could Go Wrong:
1.
2.

Testing Strategy:


═══════════════════════════════════════════════════════
APPROACH B: [Name - Alternative Architecture/Pattern]
═══════════════════════════════════════════════════════
Description:

Key Assumptions:
1.
2.
3.

What Could Go Wrong:
1.
2.

Testing Strategy:


═══════════════════════════════════════════════════════
APPROACH C: [Name - What Would a Different Expert Suggest?]
═══════════════════════════════════════════════════════
Consider: What would a security expert suggest? A performance engineer?
         A UX designer? Someone from a different tech stack?

Description:

Key Assumptions:
1.
2.
3.

What Could Go Wrong:
1.
2.

Testing Strategy:

═══════════════════════════════════════════════════════
```

### 4. Assumption Verification (MANDATORY)

List ALL implicit assumptions across all approaches:

```
═══════════════════════════════════════════════════════
ASSUMPTION VERIFICATION
═══════════════════════════════════════════════════════

| # | Assumption | Status | Evidence/Risk |
|---|------------|--------|---------------|
| 1 | | [ ] Verified in code / [ ] Verified in docs / [ ] Needs clarification / [ ] Assumed | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

UNVERIFIED ASSUMPTIONS ACCEPTED:
- [assumption]: Risk level [LOW/MEDIUM/HIGH], because [rationale]

═══════════════════════════════════════════════════════
```

### 5. Approach Selection (MANDATORY)

```
═══════════════════════════════════════════════════════
APPROACH SELECTION
═══════════════════════════════════════════════════════

SELECTED: Approach [A/B/C]

WHY THIS APPROACH:


WHY NOT APPROACH [X]:


WHY NOT APPROACH [Y]:


RISKS ACCEPTED:


CONDITIONS THAT WOULD TRIGGER RECONSIDERATION:


═══════════════════════════════════════════════════════
```

### 6. Proceed to Implementation

Only after completing Steps 2-5:
```
PRE-IMPLEMENTATION PROTOCOL COMPLETE
Proceeding with: [Selected Approach]
Key risks to monitor: [list]
```

### 7. Log Protocol Invocation

Record that /feynman was manually invoked for /reflect analysis:
- Append to session notes
- Include in next /diary entry
- Note: "Full Feynman protocol manually invoked for: [task description]"

## Example

```
User: /feynman Add caching to the API

Claude: FEYNMAN PROTOCOL ACTIVATED
Complexity router overridden → Treating as COMPLEX

═══════════════════════════════════════════════════════
ESSENTIAL PUZZLE REDUCTION
═══════════════════════════════════════════════════════

PROBLEM STATEMENT:
→ API responses are slow because each request queries the database

SIMPLEST POSSIBLE EXAMPLE:
→ GET /users makes a DB query even when data hasn't changed

SUCCESS CRITERIA:
→ Response times drop from ~500ms to <50ms for cached hits

THE CORE PUZZLE:
→ Knowing when cached data is stale without adding complexity

═══════════════════════════════════════════════════════

═══════════════════════════════════════════════════════
APPROACH A: Redis Cache
═══════════════════════════════════════════════════════
Description: Add Redis as external cache layer

Key Assumptions:
1. Redis is available in infrastructure
2. Servers are stateless
3. Cache invalidation patterns are simple

What Could Go Wrong:
1. Cache invalidation complexity
2. Redis operational overhead

Testing Strategy: Compare response times with/without cache

═══════════════════════════════════════════════════════
APPROACH B: In-Memory LRU
═══════════════════════════════════════════════════════
Description: Node.js Map with TTL

Key Assumptions:
1. Single server or sticky sessions
2. Memory is sufficient

What Could Go Wrong:
1. Memory pressure
2. No persistence across restarts

Testing Strategy: Load test memory usage

═══════════════════════════════════════════════════════
APPROACH C: HTTP Caching Headers
═══════════════════════════════════════════════════════
Description: ETags + Cache-Control headers

Key Assumptions:
1. Clients respect headers
2. Data changes infrequently

What Could Go Wrong:
1. Dynamic data gets stale
2. Not all clients support ETags

Testing Strategy: Verify browser caching behavior

═══════════════════════════════════════════════════════

═══════════════════════════════════════════════════════
ASSUMPTION VERIFICATION
═══════════════════════════════════════════════════════

| # | Assumption | Status | Evidence/Risk |
|---|------------|--------|---------------|
| 1 | Redis available | [x] Verified | docker-compose.yml has redis service |
| 2 | Multi-server | [ ] Needs clarification | Asked user |
| 3 | TTL 5min acceptable | [ ] Assumed | LOW - easily adjusted |

═══════════════════════════════════════════════════════

═══════════════════════════════════════════════════════
APPROACH SELECTION
═══════════════════════════════════════════════════════

SELECTED: Approach A (Redis)

WHY THIS APPROACH:
Multi-server deployment confirmed, need shared cache across instances

WHY NOT APPROACH B:
Won't work across servers - each server has own memory

WHY NOT APPROACH C:
Data changes frequently - browser caching would serve stale content

RISKS ACCEPTED:
Redis operational overhead - acceptable given benefits

CONDITIONS THAT WOULD TRIGGER RECONSIDERATION:
- If Redis proves too complex, consider simpler in-memory for MVP
- If data rarely changes, reconsider HTTP caching

═══════════════════════════════════════════════════════

PRE-IMPLEMENTATION PROTOCOL COMPLETE
Proceeding with: Redis Cache
Key risks to monitor: Cache invalidation, Redis availability
```

## Integration

- Works with R-P-I workflow (use in `/2_plan` phase)
- Captured in `/diary` for pattern learning
- Feeds into `/reflect` anti-pattern detection
- Logs invocation for learning loop

---

**Feynman Command v2.0** | ROK 3.6-Feynman Full Cognitive Protocol
