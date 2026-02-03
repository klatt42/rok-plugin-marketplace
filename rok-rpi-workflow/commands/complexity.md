# /complexity Command

Assess the complexity of a task and recommend the appropriate cognitive protocol depth.

**Version**: 2.0 (ROK 3.6-Feynman)

## Usage

```
/complexity [task description]
```

Or invoke without arguments to assess the current task context.

## Execution Steps

### 1. Gather Task Signals

Analyze the task for complexity indicators:

**SIMPLE Signals** (each match: -1 complexity point)
- [ ] Single file modification
- [ ] Well-documented API or established pattern in codebase
- [ ] Clear, unambiguous success criteria
- [ ] Low blast radius (isolated change)
- [ ] Similar to existing patterns already in codebase
- [ ] No external dependencies involved
- [ ] Estimated <50 lines of code

**MEDIUM Signals** (each match: +1 complexity point)
- [ ] Multiple files need coordination
- [ ] Introducing a new pattern to codebase
- [ ] External API integration
- [ ] Some ambiguity in requirements
- [ ] Moderate blast radius
- [ ] Requires understanding system beyond immediate scope
- [ ] User expressed uncertainty ("I'm not sure how to...")

**COMPLEX Signals** (each match: +2 complexity points)
- [ ] Architecture decisions required
- [ ] Unfamiliar domain or technology
- [ ] High uncertainty in approach
- [ ] Cross-cutting concerns (affects multiple systems)
- [ ] Significant refactoring needed
- [ ] Production risk / high blast radius
- [ ] Security, auth, or payment related
- [ ] Data migration or schema changes
- [ ] Multiple valid interpretations of requirements
- [ ] Previous attempts have failed

### 2. Calculate Complexity Score

```
Raw Score = (SIMPLE matches × -1) + (MEDIUM matches × 1) + (COMPLEX matches × 2)

Normalized Score = (Raw Score + 7) / 14  → Range: 0.0 to 1.0
```

### 3. Determine Category

| Score Range | Category | Protocol |
|-------------|----------|----------|
| 0.0 - 0.3 | SIMPLE | Skip full protocol, document assumptions inline |
| 0.3 - 0.6 | MEDIUM | Essential Puzzle Reduction + 2 approaches minimum |
| 0.6 - 1.0 | COMPLEX | Full Pre-Implementation Protocol |

### 4. Output Assessment

```
═══════════════════════════════════════════════════════
COMPLEXITY ASSESSMENT
═══════════════════════════════════════════════════════

Task: [description]

SIGNALS DETECTED:

SIMPLE signals matched:
  [list or "None"]

MEDIUM signals matched:
  [list or "None"]

COMPLEX signals matched:
  [list or "None"]

CALCULATION:
  SIMPLE: [count] × -1 = [value]
  MEDIUM: [count] × +1 = [value]
  COMPLEX: [count] × +2 = [value]
  Raw Score: [sum]
  Normalized: [0.0-1.0]

═══════════════════════════════════════════════════════
RESULT: [SIMPLE | MEDIUM | COMPLEX]
═══════════════════════════════════════════════════════

RECOMMENDED PROTOCOL:
[Specific steps to take based on category]

OVERRIDE RECOMMENDATION:
[Conditions that might warrant treating this as higher complexity]

═══════════════════════════════════════════════════════
```

### 5. Override Guidance

Even if scored as SIMPLE, escalate to higher protocol if:
- User seems uncertain or hesitant
- This is the third+ attempt at this task
- Similar "simple" tasks have failed recently
- Gut feeling says "something's off"

Use `/feynman` to force full protocol regardless of score.

## Special Signals

These signals automatically elevate complexity:

| Signal | Minimum Category |
|--------|------------------|
| User says "I'm not sure how to..." | COMPLEX |
| Involves auth, payments, data migration | COMPLEX |
| Multiple valid interpretations exist | MEDIUM |
| "Quick fix" or "simple change" claimed | Verify (often MEDIUM) |

## Examples

### Example 1: Clearly Simple
```
/complexity Add a console.log statement to debug the user ID

═══════════════════════════════════════════════════════
COMPLEXITY ASSESSMENT
═══════════════════════════════════════════════════════

Task: Add a console.log statement to debug the user ID

SIGNALS DETECTED:

SIMPLE signals matched:
  ✓ Single file modification
  ✓ Clear success criteria
  ✓ Low blast radius
  ✓ Less than 50 lines

MEDIUM signals matched:
  None

COMPLEX signals matched:
  None

CALCULATION:
  SIMPLE: 4 × -1 = -4
  MEDIUM: 0 × +1 = 0
  COMPLEX: 0 × +2 = 0
  Raw Score: -4
  Normalized: 0.21

═══════════════════════════════════════════════════════
RESULT: SIMPLE
═══════════════════════════════════════════════════════

RECOMMENDED PROTOCOL:
Proceed directly. Document: "Assuming user ID is available in this scope."

OVERRIDE RECOMMENDATION:
None - this is genuinely simple.

═══════════════════════════════════════════════════════
```

### Example 2: Deceptively Complex
```
/complexity Fix the login bug users are reporting

═══════════════════════════════════════════════════════
COMPLEXITY ASSESSMENT
═══════════════════════════════════════════════════════

Task: Fix the login bug users are reporting

SIGNALS DETECTED:

SIMPLE signals matched:
  None

MEDIUM signals matched:
  ✓ Some ambiguity in requirements
  ✓ Requires understanding beyond immediate scope

COMPLEX signals matched:
  ✓ Auth-related (automatic elevation)
  ✓ High uncertainty in approach
  ✓ Production risk

CALCULATION:
  SIMPLE: 0 × -1 = 0
  MEDIUM: 2 × +1 = 2
  COMPLEX: 3 × +2 = 6
  Raw Score: 8
  Normalized: 1.0 (capped)

═══════════════════════════════════════════════════════
RESULT: COMPLEX
═══════════════════════════════════════════════════════

RECOMMENDED PROTOCOL:
Full Pre-Implementation Protocol required.
Start with: What exactly is the bug? What should happen vs. what happens?

OVERRIDE RECOMMENDATION:
None - this correctly identified as complex.

═══════════════════════════════════════════════════════
```

### Example 3: Medium Complexity
```
/complexity Add a dark mode toggle to the settings page

═══════════════════════════════════════════════════════
COMPLEXITY ASSESSMENT
═══════════════════════════════════════════════════════

Task: Add a dark mode toggle to the settings page

SIGNALS DETECTED:

SIMPLE signals matched:
  ✓ Similar patterns exist in codebase

MEDIUM signals matched:
  ✓ Multiple files need coordination
  ✓ Introducing new pattern (theme switching)
  ✓ Moderate blast radius

COMPLEX signals matched:
  None

CALCULATION:
  SIMPLE: 1 × -1 = -1
  MEDIUM: 3 × +1 = 3
  COMPLEX: 0 × +2 = 0
  Raw Score: 2
  Normalized: 0.64

═══════════════════════════════════════════════════════
RESULT: MEDIUM
═══════════════════════════════════════════════════════

RECOMMENDED PROTOCOL:
1. Complete Essential Puzzle Reduction
2. Generate 2 approaches minimum
3. Verify: Where is theme state stored? How do components access it?

OVERRIDE RECOMMENDATION:
Consider COMPLEX if theme needs to persist across sessions (storage decision).

═══════════════════════════════════════════════════════
```

## Integration

- Run at session start for incoming tasks
- Feeds into Pre-Implementation Protocol decision
- Logged for `/reflect` pattern analysis
- Use `/feynman` to override and force full protocol

---

**Complexity Command v2.0** | ROK 3.6-Feynman
