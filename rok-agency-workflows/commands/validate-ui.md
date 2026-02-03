# /validate-ui - Visual UI Validation

Validates UI implementation against design expectations using multiple browser automation methods.

**NEW (Jan 2026)**: Primary method is now **Vercel agent-browser CLI** for automated validation (95% first-try success). Claude in Chrome for live debugging. Playwright MCP for CI/CD.

## Method Priority

| Priority | Tool | Best For | Reliability |
|----------|------|----------|-------------|
| 1 | **agent-browser** | Post-implementation validation | 95% first-try |
| 2 | **Claude in Chrome** | Live debugging, interactive | Real-time visual |
| 3 | **Playwright MCP** | CI/CD pipelines, scripted | 80% first-try |

## What This Does

1. **Opens Browser**: Navigates to target URL
2. **Takes Snapshot**: Gets element references (@refs) for deterministic interaction
3. **Interactive Testing**: Click, type, scroll using refs
4. **Visual Capture**: Screenshots for verification
5. **Console Monitoring**: Read errors and warnings
6. **Reports Differences**: Details issues with specific fixes

## Usage

### agent-browser (Default - Automated Validation)

```
/validate-ui url:/projects                   # Uses agent-browser (default)
/validate-ui url:/projects mode:agent        # Explicit agent-browser
/validate-ui url:/projects full:true         # Full page screenshot
/validate-ui url:/projects flow:login        # Test specific user flow
```

### Claude in Chrome (Interactive Debugging)

```
/validate-ui url:/projects mode:chrome       # Live visual inspection
/validate-ui url:/projects mock:design.png   # Compare to mockup visually
/validate-ui url:/projects fix:true          # Inspect and suggest fixes
```

### Playwright MCP (CI/CD Automation)

```
/validate-ui url:/projects mode:playwright   # Screenshot-based
/validate-ui suite:all mode:playwright       # CI/automated testing
/validate-ui baseline:true mode:playwright   # Compare to baseline
```

## Prerequisites

### agent-browser Setup (Default)

Already installed globally. Verify with:
```bash
agent-browser --version  # Should show 0.6.0+
```

Skill loaded from `~/.claude/skills/agent-browser/SKILL.md`

## agent-browser Validation Process (Default)

### Step 1: Open and Snapshot

```bash
agent-browser open http://localhost:3007/projects
agent-browser snapshot -i  # Returns interactive elements with @refs
```

Output shows elements like:
```
button "New Project" [ref=e1]
link "Dashboard" [ref=e2]
textbox "Search" [ref=e3]
```

### Step 2: Interact Using Refs

```bash
agent-browser click @e1           # Click button by ref
agent-browser fill @e3 "test"     # Fill input by ref
agent-browser press Enter         # Submit
```

### Step 3: Verify and Capture

```bash
agent-browser snapshot -i         # Re-snapshot after interaction
agent-browser screenshot page.png # Capture for review
agent-browser get title           # Verify page title
agent-browser get url             # Verify URL changed
```

### Step 4: Check for Errors

```bash
agent-browser console             # View console messages
agent-browser errors              # View page errors
```

### Step 5: Close

```bash
agent-browser close
```

### Full Validation Example

```bash
# Navigate
agent-browser open http://localhost:3007/projects

# Get elements
agent-browser snapshot -i

# Test interactions
agent-browser click @e1  # Click first button
agent-browser wait --load networkidle

# Capture result
agent-browser screenshot validation-result.png

# Check for errors
agent-browser errors

# Close
agent-browser close
```

---

### Claude in Chrome Setup (Interactive)

1. **Update Claude Code**:
```bash
claude update  # Requires v2.0.73+
```

2. **Install Chrome Extension**:
- Install "Claude in Chrome" from Chrome Web Store
- Requires Chrome browser
- Requires paid Claude plan (Pro, Team, or Enterprise)

3. **Launch with Chrome**:
```bash
claude --chrome
# Or enable permanently:
/chrome  # Then select "Enabled by default"
```

4. **Verify Connection**:
```
/chrome  # Should show "Connected"
```

### Playwright MCP (Fallback)

Still configured in `.mcp.json` for automated testing:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "type": "stdio"
    }
  }
}
```

## Claude in Chrome Validation Process

### Step 1: Navigate to Page

```
"Open http://localhost:3007/projects in Chrome"

Claude will:
- Navigate to the URL
- Wait for page to fully load
- See the page visually in real-time
```

### Step 2: Visual Inspection

Claude can now SEE the page and identify:
- Layout issues (without screenshots)
- Color mismatches
- Spacing problems
- Missing elements
- Broken components
- Console errors

### Step 3: Interactive Testing

```
"Click the 'New Project' button and check if the modal opens correctly"
"Fill in the form with test data and verify validation messages"
"Scroll to the bottom and check if the footer is visible"
```

### Step 4: Console & DOM Inspection

```
"Check the console for any errors on this page"
"Inspect the .project-card element and show me its computed styles"
"What's the DOM structure of the navigation component?"
```

### Step 5: Live Fix Verification

```
"I'll change the button color - watch the page and tell me if it looks right"
[Make code change]
"Does the button now match the design?"
```

## Report Format

```markdown
## UI Validation Report (Claude in Chrome)

**Page**: /projects
**URL**: http://localhost:3007/projects
**Method**: Claude in Chrome (Live Inspection)
**Timestamp**: 2025-12-19 19:30

### Status: NEEDS_FIXES

### Visual Inspection Findings

| Issue | Severity | Element | Problem | Fix |
|-------|----------|---------|---------|-----|
| 1 | High | `.project-card` | Cards not aligned in grid | Add `grid-cols-3` to parent |
| 2 | Medium | `.btn-primary` | Color too dark (#0284c7) | Change to `bg-cyan-500` |
| 3 | Low | `.footer` | Missing bottom padding | Add `pb-8` |

### Console Errors Found

```
- Warning: Each child should have a unique "key" prop (ProjectList.tsx:42)
- Error: Failed to load resource: /api/metrics (404)
```

### Interactive Tests

| Test | Result | Notes |
|------|--------|-------|
| New Project button | PASS | Modal opens correctly |
| Form validation | FAIL | No error message for empty title |
| Pagination | PASS | Page 2 loads correctly |

### Accessibility Notes
- All buttons have accessible names
- Color contrast meets WCAG AA on most elements
- Skip navigation link missing

### Fixes Applied This Session
1. ✅ Fixed card grid alignment
2. ✅ Updated button color
3. ⏳ Footer padding pending

### Remaining Issues
- Form validation error messages
- /api/metrics endpoint returning 404
```

## Comparison: Chrome vs Playwright

| Capability | Claude in Chrome | Playwright MCP |
|------------|------------------|----------------|
| **Visual Inspection** | Real-time, continuous | Screenshot snapshots |
| **Console Errors** | Live monitoring | Not available |
| **DOM Inspection** | Live, interactive | Via accessibility tree |
| **Fix Verification** | Instant feedback | Requires re-screenshot |
| **Interaction** | Natural language | Selector-based |
| **Automation** | Manual/interactive | Scriptable, CI-ready |
| **Speed** | Faster for debugging | Faster for suites |
| **Best For** | Development, debugging | CI/CD, regression |

## Common Workflows

### Debug a Visual Bug

```
User: The cards on /projects look broken

Claude: I'll open that page and take a look.
[Opens http://localhost:3007/projects]

I can see the issue - the cards are stacking vertically instead of
in a grid. Looking at the DOM, the parent container is missing the
grid class.

The fix is to change line 24 in ProjectList.tsx:
- <div className="flex flex-col">
+ <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

Want me to make this change? I'll watch the page and confirm it fixes the layout.
```

### Verify Design Implementation

```
User: /validate-ui url:/dashboard mock:design-mocks/dashboard-v2.png

Claude: I'll open the dashboard and compare it to the mockup.
[Opens dashboard, views mockup image]

Comparing to the mockup, I see these differences:

1. Header height: Mockup shows 64px, current is ~80px
2. Sidebar width: Should be 240px, currently 280px
3. Card shadows: Mockup has subtle shadow, current has none
4. Font weight: Titles should be semibold (600), currently normal (400)

Match percentage: ~75%

Shall I fix these one by one? I can verify each change in real-time.
```

### Test Form Validation

```
User: Test the login form validation

Claude: I'll interact with the login form and test validation.
[Opens login page]

Testing empty submission:
- Clicked "Sign In" with empty fields
- Result: Form submitted without errors ❌ (Bug: No validation)

Testing invalid email:
- Entered "notanemail" in email field
- Result: No error shown ❌ (Bug: Email validation missing)

Testing valid credentials:
- Entered valid test credentials
- Result: Redirected to dashboard ✅

Found 2 validation bugs that need fixing.
```

## Mode Selection

### Use Chrome Mode When:
- Actively developing UI
- Debugging visual issues
- Need to see console errors
- Verifying design implementation
- Testing interactive flows
- Quick fix verification

### Use Playwright Mode When:
- Running automated test suites
- CI/CD pipeline testing
- Baseline comparison testing
- Need programmatic control
- Chrome extension not available

## Session Integration

### With /session-start

```
/session-start
→ Context loaded
→ Dev server on http://localhost:3007

/validate-ui url:/projects
→ Opens in Chrome, Claude sees current state
→ Reports any issues from previous session
```

### With /session-end

```
/validate-ui suite:all mode:chrome
→ Quick visual review of all pages
→ Confirm no regressions before ending

/session-end
```

## Troubleshooting

### Chrome Extension Not Connected

```bash
# Verify Claude Code version
claude --version  # Need v2.0.73+

# Check Chrome connection
/chrome

# Restart with Chrome flag
claude --chrome
```

### Can't See the Page

```
# Ensure dev server is running
curl http://localhost:3007/api/health

# Start if needed
./init.sh
```

### Extension Not Installed

1. Open Chrome Web Store
2. Search "Claude in Chrome"
3. Install extension
4. Restart Claude Code with `claude --chrome`

### Fallback to Playwright

If Chrome isn't available:
```
/validate-ui url:/projects mode:playwright
```

---

**Validate UI Command v2.0** | ROK 3.1 Claude in Chrome Integration
