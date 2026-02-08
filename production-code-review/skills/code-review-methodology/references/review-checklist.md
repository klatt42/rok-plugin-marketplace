# Detailed Review Checklists

Reference document for production code review agents. Load on-demand only.

## Code Quality Checklist

### DRY Violations
- [ ] No copy-pasted code blocks > 10 lines
- [ ] Shared utilities extracted for common patterns
- [ ] API call patterns abstracted
- [ ] Error handling patterns consistent

### SOLID Principles
- [ ] Single Responsibility: No file > 300 lines, no function > 50 lines
- [ ] Open/Closed: Extensible without modification
- [ ] Liskov Substitution: Interface contracts honored
- [ ] Interface Segregation: No unused imports from large modules
- [ ] Dependency Inversion: Business logic decoupled from infrastructure

### Naming
- [ ] Consistent casing (camelCase or snake_case, not mixed)
- [ ] Descriptive names (no data, info, handler, manager, utils)
- [ ] Booleans prefixed (is/has/can/should)
- [ ] Components match file names

### Structure
- [ ] No circular dependencies
- [ ] No god objects/components
- [ ] Deep nesting avoided (max 3 levels)
- [ ] Consistent file organization

## Testing Checklist

### Coverage Priorities
- [ ] CRITICAL: All API endpoints have tests
- [ ] CRITICAL: Auth/authorization logic tested
- [ ] HIGH: Data validation functions tested
- [ ] HIGH: Custom hooks tested
- [ ] MEDIUM: Utility functions tested
- [ ] MEDIUM: Components with logic tested

### Test Quality
- [ ] Tests test behavior, not implementation
- [ ] Error/failure paths covered
- [ ] Edge cases covered (null, empty, boundary)
- [ ] Integration tests exist for critical flows
- [ ] E2E tests cover happy path
- [ ] No tests with zero assertions
- [ ] No snapshot test abuse

## UI/UX Checklist

### WCAG 2.1 AA Contrast Ratios
- Normal text (< 18px): 4.5:1 minimum
- Large text (>= 18px or >= 14px bold): 3:1 minimum

### Common Tailwind Contrast Issues
| Class on White BG | Ratio | Pass? |
|-------------------|-------|-------|
| text-gray-300 | ~2.6:1 | FAIL |
| text-gray-400 | ~2.7:1 | FAIL |
| text-gray-500 | ~4.6:1 | PASS |
| text-gray-600 | ~5.7:1 | PASS |
| text-gray-700 | ~9.1:1 | PASS |

### Font Minimums
- Body text: >= 16px (mobile), >= 14px (desktop)
- Secondary: >= 12px
- Captions: >= 11px

### Interactive Elements
- Touch targets: 44x44px minimum (mobile)
- Click targets: 24x24px minimum (desktop)
- Gap between targets: 8px minimum

## Responsive Design Checklist

### Breakpoints (Tailwind Default)
| Name | Width | Usage |
|------|-------|-------|
| sm | 640px | Small tablets |
| md | 768px | Tablets |
| lg | 1024px | Small laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large displays |

### Must-Have
- [ ] Viewport meta tag (width=device-width, initial-scale=1)
- [ ] No user-scalable=no
- [ ] Mobile navigation pattern
- [ ] Responsive tables (scroll or restructure)
- [ ] Full-width forms on mobile
- [ ] No horizontal overflow

## Security Checklist (OWASP Top 10)

### A01: Broken Access Control
- [ ] Auth middleware on all protected routes
- [ ] Role-based access checks
- [ ] No IDOR (indirect object references)

### A03: Injection
- [ ] Parameterized SQL queries
- [ ] No string interpolation in queries
- [ ] No dynamic code evaluation (eval, Function constructor)
- [ ] Input sanitization on user content

### A05: Security Misconfiguration
- [ ] No debug mode in production config
- [ ] CORS properly configured (not origin: *)
- [ ] Security headers (helmet)
- [ ] Error messages don't leak internals

### Secrets
- [ ] No hardcoded API keys/passwords
- [ ] .env in .gitignore
- [ ] Environment variables for all secrets

## Performance Checklist

### Bundle
- [ ] Tree-shakeable imports (named, not default)
- [ ] No full lodash/moment imports
- [ ] Route-level code splitting
- [ ] Dynamic imports for heavy components

### Data
- [ ] No N+1 query patterns
- [ ] Data caching (SWR, React Query)
- [ ] Pagination on list endpoints
- [ ] Request deduplication

### React
- [ ] React.memo on expensive list items
- [ ] useMemo/useCallback for expensive computations
- [ ] No inline objects/arrays in JSX props
- [ ] Large lists virtualized (> 100 items)
- [ ] Proper key props (not index)

### Memory
- [ ] useEffect cleanup for listeners
- [ ] Subscriptions unsubscribed
- [ ] Timers cleared
- [ ] AbortController for fetch in effects
