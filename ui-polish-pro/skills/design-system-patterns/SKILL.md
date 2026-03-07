---
name: design-system-patterns
description: |
  Patterns for extracting and generating design token systems from existing
  codebases. Covers color extraction, typography auditing, spacing analysis,
  Tailwind config integration, and design system JSON schema. Reference when
  running /design-system or during Phase 2 of the polish pipeline.
triggers:
  - "design system"
  - "design tokens"
  - "extract colors"
  - "typography audit"
  - "spacing consistency"
version: 1.0
author: ROK Agency
---

# Design System Patterns

## Design System JSON Schema

Every design system produced by ui-polish-pro follows this schema:

```json
{
  "designSystem": {
    "colors": {
      "primary": { "DEFAULT": "string", "light": "string", "dark": "string" },
      "secondary": { "DEFAULT": "string", "light": "string", "dark": "string" },
      "accent": { "DEFAULT": "string", "light": "string", "dark": "string" },
      "success": "string",
      "warning": "string",
      "error": "string",
      "info": "string",
      "background": { "DEFAULT": "string", "subtle": "string", "muted": "string" },
      "foreground": { "DEFAULT": "string", "muted": "string", "subtle": "string" }
    },
    "typography": {
      "fontFamily": { "heading": "string", "body": "string", "mono": "string" },
      "scale": {
        "display": "string (Tailwind classes)",
        "h1": "string",
        "h2": "string",
        "h3": "string",
        "h4": "string",
        "body": "string",
        "small": "string",
        "micro": "string"
      }
    },
    "spacing": {
      "scale": "string (base unit description)",
      "sectionGap": "string (Tailwind classes)",
      "cardPadding": "string",
      "elementGap": "string",
      "containerMax": "string"
    },
    "borderRadius": {
      "sm": "string",
      "DEFAULT": "string",
      "lg": "string",
      "xl": "string",
      "full": "string"
    },
    "shadows": {
      "sm": "string",
      "DEFAULT": "string",
      "lg": "string",
      "xl": "string",
      "glow": "string"
    },
    "transitions": {
      "fast": "string",
      "DEFAULT": "string",
      "slow": "string",
      "spring": "string (framer-motion config)"
    }
  },
  "migrations": [
    {
      "description": "string",
      "find": "string",
      "replace": "string",
      "fileCount": "number"
    }
  ]
}
```

## Color Extraction Patterns

### Grep Commands for Color Inventory

```bash
# Find all Tailwind color class usage
grep -roh 'bg-[a-z]*-[0-9]*' src/ | sort | uniq -c | sort -rn | head -20
grep -roh 'text-[a-z]*-[0-9]*' src/ | sort | uniq -c | sort -rn | head -20
grep -roh 'border-[a-z]*-[0-9]*' src/ | sort | uniq -c | sort -rn | head -20

# Find hex colors in CSS
grep -roh '#[0-9a-fA-F]\{3,8\}' src/ | sort | uniq -c | sort -rn
```

### Color Role Assignment

| Role | How to Identify |
|------|----------------|
| Primary | Most frequent action/button color (bg-{color}-600 on buttons) |
| Secondary | Second most frequent, used for backgrounds/borders |
| Accent | Used sparingly for highlights, badges, or emphasis |
| Neutral | Gray scale used for text, borders, backgrounds |
| Semantic | Success=green/emerald, Warning=amber/yellow, Error=red, Info=blue/sky |

### Common Inconsistencies

| Issue | Detection | Fix |
|-------|-----------|-----|
| Multiple primaries | blue-500, blue-600, blue-700 all on buttons | Pick one (usually -600) |
| Semantic confusion | Red used for non-error elements | Reserve red for errors/destructive |
| No accent color | Everything is primary or gray | Add indigo/violet/emerald accent |
| Dark mode mismatch | Light colors used in dark:, no dark: prefix | Add dark: variants |

## Typography Patterns

### Font Detection

```bash
# Next.js font imports
grep -r "next/font" src/ app/
grep -r "google.*font\|@font-face\|font-family" src/ app/ styles/

# Tailwind font config
grep -A5 "fontFamily" tailwind.config.*
```

### Typography Scale (Recommended)

| Level | Size | Weight | Tracking | Use |
|-------|------|--------|----------|-----|
| Display | text-5xl md:text-7xl | font-bold | tracking-tight | Hero headlines |
| H1 | text-3xl md:text-4xl | font-bold | tracking-tight | Page titles |
| H2 | text-2xl md:text-3xl | font-semibold | default | Section titles |
| H3 | text-xl | font-semibold | default | Card titles |
| H4 | text-lg | font-medium | default | Subsection titles |
| Body | text-base | font-normal | default | Default text |
| Small | text-sm | font-normal | default | Captions, metadata |
| Micro | text-xs | font-medium | tracking-wide | Labels, badges |

### Common Font Pairings

| Heading | Body | Vibe |
|---------|------|------|
| Inter | Inter | Clean, professional |
| Plus Jakarta Sans | Inter | Modern startup |
| DM Sans | DM Sans | Friendly, rounded |
| Instrument Serif | Inter | Editorial, premium |
| Space Grotesk | Inter | Technical, developer |

## Spacing Patterns

### Spacing Audit

```bash
# Count padding usage
grep -roh 'p-[0-9]*\|px-[0-9]*\|py-[0-9]*' src/ | sort | uniq -c | sort -rn

# Count gap usage
grep -roh 'gap-[0-9]*' src/ | sort | uniq -c | sort -rn
```

### Recommended Spacing Rhythm

| Context | Value | When |
|---------|-------|------|
| Section padding | py-16 md:py-24 | Between major page sections |
| Card padding | p-6 | Inside cards and panels |
| Element gap | gap-4 | Between sibling elements |
| Stack gap | space-y-2 | Between list items, form fields |
| Container | max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 | Page width constraint |
| Dense gap | gap-2 | Icon + text, badge groups |

### Inconsistency Detection

If a codebase uses 5+ different padding values with no pattern, it needs normalization. The fix:
1. Map current values to nearest system value
2. Generate find/replace migrations
3. Apply in a single pass

## Border Radius Patterns

### Recommended Scale

| Token | Value | Use |
|-------|-------|-----|
| sm | rounded-md | Small buttons, badges, inputs |
| DEFAULT | rounded-lg | Standard cards, panels |
| lg | rounded-xl | Feature cards, modals |
| xl | rounded-2xl | Hero cards, large panels |
| full | rounded-full | Avatars, pills, FABs |

### Common Issue

Mixing rounded-lg, rounded-xl, and rounded-2xl randomly. Pick one default (rounded-xl is modern and professional) and use the scale above for variation.

## Shadow Patterns

### Recommended Scale

| Token | Value | Use |
|-------|-------|-----|
| sm | shadow-sm | Subtle elevation (cards at rest) |
| DEFAULT | shadow-md | Standard elevation (dropdowns, popovers) |
| lg | shadow-lg | Elevated elements (modals, drawers) |
| xl | shadow-xl | High elevation (floating CTAs) |
| glow | shadow-[0_0_30px_rgba(color,0.15)] | Brand-colored glow effect |

## Tailwind Config Integration

When writing tokens to tailwind.config.ts:

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  // ... existing config
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb', // blue-600
          light: '#dbeafe',   // blue-100
          dark: '#1e40af',    // blue-800
        },
        // ... other custom colors
      },
      borderRadius: {
        DEFAULT: '0.75rem', // 12px - rounded-xl equivalent
      },
      boxShadow: {
        glow: '0 0 30px rgba(37, 99, 235, 0.15)',
      },
    },
  },
}
```

## Pre-Built Design Systems (Templates)

### Minimal Clean
- Primary: blue-600, Accent: indigo-500
- Font: Inter, Radius: rounded-xl, Shadows: subtle

### Bold Startup
- Primary: violet-600, Accent: amber-500
- Font: Plus Jakarta Sans, Radius: rounded-2xl, Shadows: prominent

### Enterprise Professional
- Primary: blue-700, Accent: emerald-600
- Font: Inter, Radius: rounded-lg, Shadows: minimal

### Dark Glassmorphism
- Primary: blue-500, Accent: cyan-400
- Font: DM Sans, Radius: rounded-2xl, Shadows: glow effects
- Background: gray-950, glass: bg-white/5 backdrop-blur-xl
