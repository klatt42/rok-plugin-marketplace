# Digital Estate Snapshot - Output Document Template

This document defines the 10 sections that the estate-synthesizer agent must produce for each snapshot. The `full_estate_md` field in the synthesizer's JSON output must follow this structure exactly.

---

## Template Structure

```markdown
# Digital Estate Snapshot v[N]
**Generated:** [YYYY-MM-DD HH:MM] | **Projects:** [count] | **Deployments:** [count]
**Monthly Burn:** $[total] | **Items Needing Attention:** [count]

**CONFIDENTIAL** - Contains access methods and infrastructure details.

---

## 1. Executive Summary

[1-page overview for someone in a hurry. Lead with urgent items, then overall estate health, then key changes since last snapshot.]

- **Estate Health:** [HEALTHY / NEEDS ATTENTION / CRITICAL ITEMS]
- **Total Projects:** [N] (Active: [n], Recent: [n], Dormant: [n], Abandoned: [n])
- **Live Deployments:** [N] across [providers]
- **Monthly Burn:** $[total]
- **Critical Items:** [count] requiring action within 30 days
- **Changes Since Last:** [bullet list of what changed]

---

## 2. Bus Factor Dashboard

Items sorted by urgency (days until risk). This is the "what breaks first" view.

### CRITICAL (Action Required Within 30 Days)
| Item | Type | Days Left | Risk | Action Needed |
|------|------|-----------|------|---------------|
| [item] | [domain/subscription/deliverable/ssl] | [N] | [description] | [specific action] |

### ATTENTION (Review Within 60 Days)
| Item | Type | Days Left | Risk | Action Needed |
|------|------|-----------|------|---------------|

### MONITOR (Check Within 90 Days)
| Item | Type | Days Left | Risk | Action Needed |
|------|------|-----------|------|---------------|

### STABLE (No Immediate Action)
[Count] items are auto-renewing and stable.

---

## 3. Project Inventory

| # | Project | Status | Tech Stack | Local Path | Repo | Deployment | Last Activity |
|---|---------|--------|------------|------------|------|------------|---------------|
| 1 | [name] | [Active/Recent/Dormant/Abandoned] | [stack] | [path] | [repo URL or "local only"] | [URL or "none"] | [date] |

### Cross-Reference Notes
- **Orphan repos** (on GitHub but not local): [list]
- **Local-only projects** (not on GitHub): [list]
- **Dirty repos** (unpushed changes): [list]

---

## 4. Deployment Map

| Site | Provider | URL | Custom Domain | SSL | Repo | Build Status | Last Deploy |
|------|----------|-----|---------------|-----|------|-------------|-------------|
| [name] | [Netlify/Vercel] | [url] | [domain or "none"] | [valid/expiring/expired] | [repo] | [success/failed] | [date] |

### Orphaned Deployments
[Sites that exist but have no matching local project or repo]

### Domain Routing
| Domain | Points To | Provider | SSL Expiry |
|--------|-----------|----------|------------|

---

## 5. Infrastructure & Hosting

### Hostinger
- **Account:** [email]
- **Domains:** [count] ([auto-renew count] auto-renewing)
- **VPS:** [count] ([total monthly cost])

### DNS Routing Summary
| Domain | Registrar | DNS Provider | Points To |
|--------|-----------|-------------|-----------|

### Service Health
| Service | URL | Status | Last Checked |
|---------|-----|--------|-------------|

---

## 6. Subscriptions & Costs

### Monthly Burn Summary
| Category | Monthly Cost | Annual Cost |
|----------|-------------|-------------|
| Hosting & Domains | $[X] | $[X*12] |
| Developer Tools | $[X] | $[X*12] |
| APIs & Services | $[X] | $[X*12] |
| Marketing/CRM | $[X] | $[X*12] |
| **Total** | **$[total]** | **$[total*12]** |

### Subscription Details
| Service | Cost/mo | Renewal Date | Auto-Renew | Payment | Status |
|---------|---------|-------------|------------|---------|--------|
| [service] | $[cost] | [date] | [yes/no] | [card last 4] | [active/expiring] |

### Payment Methods
| Card | Last 4 | Expiry | Services |
|------|--------|--------|----------|
| [type] | [XXXX] | [MM/YY] | [list] |

---

## 7. Access Guide

**DO NOT include actual passwords, API keys, or tokens in this document.**

| Service | URL | Login Method | Credential Location |
|---------|-----|-------------|-------------------|
| GitHub | github.com | [method] | [location reference] |
| Hostinger | hpanel.hostinger.com | [method] | [location reference] |
| Netlify | app.netlify.com | [method] | [location reference] |
| Vercel | vercel.com | [method] | [location reference] |
| Supabase | supabase.com | [method] | [location reference] |
| GHL | app.gohighlevel.com | [method] | [location reference] |

### SSH Keys
| Key | Location | Services |
|-----|----------|----------|
| [name] | [path] | [what it unlocks] |

### Environment Variables
| Variable | Purpose | Location |
|----------|---------|----------|
| [var] | [what it does] | [where it's set] |

---

## 8. ROK Memory Highlights

### Key Architectural Decisions
| Decision | Context | Date |
|----------|---------|------|
| [decision] | [why this was chosen] | [when] |

### Active Patterns
[Patterns that define how the system works]

### Known Gotchas
| Gotcha | Impact | Workaround |
|--------|--------|------------|
| [issue] | [what breaks] | [how to fix] |

### Port Assignments
| Project | Port Range | Status |
|---------|-----------|--------|
| [project] | [low]-[high] | [active/dormant] |

---

## 9. Contact List

| Name | Role | Email | Phone | Projects |
|------|------|-------|-------|----------|
| [name] | [role] | [email] | [phone] | [projects] |

---

## 10. "If Something Happens" Quick Start

**For Ron's sons - numbered steps in priority order:**

1. **Secure credentials:** Go to [credential master location]. This notebook has every password and recovery code.

2. **Check CRITICAL items:** Look at Section 2 (Bus Factor Dashboard). Anything in the CRITICAL tier needs action within 30 days.

3. **Protect active domains:** Log into Hostinger ([login method]). Ensure auto-renew is ON for all domains you want to keep.

4. **Backup all code:** Run `gh repo list --json name,url | jq` and clone any repos not already local.

5. **Review subscriptions:** Check Section 6. Cancel any services not needed. Total monthly burn is $[X].

6. **Contact clients:** See Section 9 for contact list. Notify active clients of the situation.

7. **Secure SSH access:** SSH keys are at [locations]. These are needed for VPS and deployment access.

8. **Check live sites:** All live URLs are in Section 4. Ensure they're still running.

9. **Review costs:** Look at payment methods in Section 6. Decide which to keep active.

10. **Long-term:** Consider whether to maintain, sell, or archive each project. Section 3 has the full inventory.

---
*Digital Estate Snapshot v[N] | Generated [timestamp] | rok-digital-estate plugin*
```

## Section Rules

1. **Executive Summary** must be readable standalone by a non-technical person
2. **Bus Factor Dashboard** sorts by days_until_risk ascending (most urgent first)
3. **Project Inventory** includes cross-reference notes for orphaned/local-only projects
4. **Deployment Map** flags any orphaned deployments (site without matching repo)
5. **Infrastructure** includes service health checks (reachable or not)
6. **Subscriptions** always shows total monthly and annual burn
7. **Access Guide** NEVER contains actual credentials - only references to where they're stored
8. **ROK Memory** surfaces the most important institutional knowledge
9. **Contact List** is pulled from estate-config.json
10. **Quick Start** is written for a non-technical reader in an emergency situation
