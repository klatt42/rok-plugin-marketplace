---
name: genesis-core
description: |
  Master decision tree for Genesis project type selection and initialization.
  Guides choice between Landing Page, SaaS App, or Hybrid projects using
  Next.js 14 + Tailwind + Supabase + Netlify stack. Includes ROK integration
  setup with CLAUDE.md, task tracking, and git conventions.
triggers:
  - "new project"
  - "create project"
  - "genesis template"
  - "which template"
  - "landing page or saas"
version: 1.0
author: ROK Copilot
---

# Genesis Core

## When to Use This Skill

Load this skill when user mentions:
- "new project" OR "start project" OR "create project"
- "genesis project" OR "genesis template" OR "use genesis"
- "which template" OR "which boilerplate"
- "landing page or saas" OR "should I use landing page"
- "best practices" OR "genesis patterns"

## Key Patterns

### Pattern 1: Project Type Decision

**Landing Page** → Choose when:
- Goal: Lead generation / conversion
- Timeline: Days to 1 week
- User flow: Single-page or simple multi-page
- Need: Forms + CRM integration (GHL)
- Examples: Service landing page, product launch, event registration

**SaaS Application** → Choose when:
- Goal: User management / ongoing usage
- Timeline: Weeks (iterative development)
- User flow: Protected dashboard + features
- Need: Authentication + multi-tenant + subscriptions
- Examples: Project management tool, analytics platform, collaboration app

**Hybrid (Landing + SaaS)** → Start with Landing Page:
- Build landing page first for lead capture
- Add SaaS features after user acquisition
- Use genesis-landing-page → then genesis-saas-app

### Pattern 2: Core Stack (Always)

```bash
# Standard Genesis setup
npx create-next-app@latest [name] --typescript --tailwind --app
npm install @supabase/supabase-js
```

Stack: Next.js 14 + Tailwind + Supabase + Netlify

### Pattern 3: Type-Specific Additions

**Landing Page**:
```bash
npm install react-hook-form @hookform/resolvers/zod zod
```
Then: **genesis-landing-page** skill

**SaaS App**:
```bash
npm install @supabase/auth-helpers-nextjs
```
Then: **genesis-saas-app** skill

## Quick Reference

| Project Type | Timeline | Key Need | Next Skill |
|--------------|----------|----------|------------|
| Landing Page | Days | Lead capture | genesis-landing-page |
| SaaS App | Weeks | User auth | genesis-saas-app |

### First Milestones

**Landing Page**:
- [ ] Hero + lead form
- [ ] GHL integration
- [ ] Deploy to Netlify

**SaaS App**:
- [ ] Auth flow complete
- [ ] Dashboard created
- [ ] Database schema

## Command Templates

```bash
# Quick start any Genesis project
npx create-next-app@latest my-project --typescript --tailwind --app
cd my-project
npm install @supabase/supabase-js
```

### Pattern 4: ROK Integration (MANDATORY)

Every Genesis project MUST include CLAUDE.md, rok_tasks.json, and git hooks.
For full ROK setup commands, CLAUDE.md template, and verification checklist:

**Load reference**: `read_reference("genesis-core", "ROK_SETUP.md")`

## Integration with Other Skills

After project type is selected:
- **genesis-stack-setup** for detailed integration setup
- **genesis-landing-page** for landing page patterns
- **genesis-saas-app** for SaaS architecture
- **genesis-commands** for complete command workflows

## Reference Documents

| Document | Purpose | When to Load |
|----------|---------|--------------|
| **ROK_SETUP.md** | Full ROK integration commands, CLAUDE.md template, verification checklist | When creating a new project |
