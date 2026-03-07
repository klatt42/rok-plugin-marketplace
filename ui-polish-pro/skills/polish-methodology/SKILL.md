---
name: polish-methodology
description: |
  Scoring rubric and methodology for UI polish assessment. Defines the 8
  dimensions scored 0-10 each, letter grade mapping, before/after comparison
  criteria, and quality thresholds. Reference when running audits or evaluating
  polish results.
triggers:
  - "polish score"
  - "ui scoring"
  - "visual quality rubric"
  - "before after comparison"
version: 1.0
author: ROK Agency
---

# Polish Methodology - Scoring Rubric

## 8 Dimensions of Visual Quality

Each dimension scored 0-10. A professional, ship-ready app scores 7+ on every dimension.

---

### 1. Layout & Spacing (0-10)

**What it measures**: Consistent spacing scale, grid alignment, visual rhythm, whitespace usage.

| Score | Description |
|-------|-------------|
| 0-2 | No spacing system. Random padding/margin values. Elements crammed or floating. |
| 3-4 | Some spacing exists but inconsistent. Mix of 3+ padding values. Poor whitespace. |
| 5-6 | Mostly consistent spacing. Minor inconsistencies. Adequate whitespace. |
| 7-8 | Clean spacing rhythm. Consistent scale. Good use of whitespace. Grid-aligned. |
| 9-10 | Perfect spatial hierarchy. Intentional whitespace. Every element precisely placed. |

**Key checks**:
- Does the page use a consistent spacing scale (4/8/12/16)?
- Are section gaps consistent?
- Is there enough whitespace between elements?
- Do grids align properly at all breakpoints?

---

### 2. Typography (0-10)

**What it measures**: Heading hierarchy, font pairing, line heights, letter spacing, text contrast.

| Score | Description |
|-------|-------------|
| 0-2 | No heading hierarchy. Single font size. Poor readability. |
| 3-4 | Some size variation but no clear hierarchy. Default line heights. |
| 5-6 | Clear heading levels. Decent readability. Minor inconsistencies. |
| 7-8 | Strong typographic hierarchy. Good font pairing. Proper line heights. |
| 9-10 | Professional typography. Perfect hierarchy. Optimal readability. Refined tracking/spacing. |

**Key checks**:
- Is there a clear size hierarchy (display > h1 > h2 > h3 > body > small)?
- Are font weights used intentionally (not just bold/normal)?
- Are line heights appropriate for the font size?
- Is text contrast sufficient (4.5:1 for body, 3:1 for large)?

---

### 3. Color System (0-10)

**What it measures**: Palette consistency, contrast ratios, semantic color usage, dark mode support.

| Score | Description |
|-------|-------------|
| 0-2 | Random colors. No palette. Poor contrast. No semantic meaning. |
| 3-4 | Some color consistency. Missing semantic colors. Occasional contrast issues. |
| 5-6 | Identifiable palette. Decent contrast. Some semantic colors (error, success). |
| 7-8 | Unified palette. Good contrast. Full semantic set. Consistent hover/active states. |
| 9-10 | Professional palette with primary/secondary/accent/semantic. Perfect contrast. Dark mode. |

**Key checks**:
- Is there a single primary color used consistently?
- Are error/success/warning states color-coded?
- Do all text/background combinations meet WCAG AA contrast?
- Is dark mode supported (or at least not broken)?

---

### 4. Animation & Motion (0-10)

**What it measures**: Entrance animations, hover states, transitions, scroll reveals, loading states.

| Score | Description |
|-------|-------------|
| 0-2 | No animations. Static page. Instant state changes. |
| 3-4 | CSS transitions on some hover states. No entrance animations. |
| 5-6 | Some entrance animations. Hover transitions on buttons. Basic loading states. |
| 7-8 | Scroll-triggered reveals. Staggered card entrances. Spring-based hover. Loading skeletons. |
| 9-10 | Cinema-quality motion. Purposeful animation on every interaction. Reduced-motion respect. Page transitions. |

**Key checks**:
- Do sections animate in on scroll?
- Do cards/lists stagger their entrance?
- Do buttons have hover/tap feedback?
- Are loading states animated (skeleton shimmer)?
- Is `prefers-reduced-motion` respected?

---

### 5. Interactivity (0-10)

**What it measures**: Hover feedback, focus rings, loading states, error states, empty states.

| Score | Description |
|-------|-------------|
| 0-2 | No hover feedback. No focus indicators. No loading/error states. |
| 3-4 | Basic cursor:pointer. Some hover color changes. Missing focus rings. |
| 5-6 | Hover states on most interactive elements. Some focus rings. Basic loading spinner. |
| 7-8 | Comprehensive hover states. Focus-visible rings. Loading skeletons. Error states with recovery. |
| 9-10 | Every interactive element has clear feedback. Empty states designed. Optimistic UI. Undo support. |

**Key checks**:
- Does every clickable element change on hover?
- Can keyboard users see where they are (focus-visible rings)?
- What happens during loading? (spinner, skeleton, or nothing?)
- What happens on error? (message, retry button, or silent failure?)
- What does an empty list/table look like? (designed empty state or blank?)

---

### 6. Responsiveness (0-10)

**What it measures**: Mobile-first design, breakpoint consistency, touch targets, viewport handling.

| Score | Description |
|-------|-------------|
| 0-2 | Broken on mobile. Horizontal scroll. Tiny text. Overlapping elements. |
| 3-4 | Mostly readable on mobile but not optimized. Some layout breaks. |
| 5-6 | Responsive layout works. Some mobile optimizations. Minor issues at certain widths. |
| 7-8 | Clean responsive behavior. Proper breakpoints. Touch-friendly targets. No layout breaks. |
| 9-10 | Mobile-first design. Optimal at every breakpoint. Touch targets 44px+. Responsive images. |

**Key checks**:
- Does the layout work at 375px (mobile), 768px (tablet), 1024px (laptop), 1440px (desktop)?
- Are touch targets at least 44x44px?
- Do tables and data-heavy sections adapt to mobile?
- Are images properly sized for each breakpoint?

---

### 7. Accessibility (0-10)

**What it measures**: ARIA labels, focus management, reduced-motion support, color contrast, semantic HTML.

| Score | Description |
|-------|-------------|
| 0-2 | No ARIA labels. No focus management. Div soup. No semantic HTML. |
| 3-4 | Some alt text on images. Basic semantic elements. No focus management. |
| 5-6 | ARIA labels on key elements. Some semantic HTML. Basic keyboard navigation. |
| 7-8 | Comprehensive ARIA. Semantic HTML structure. Focus-visible rings. Reduced-motion support. |
| 9-10 | Full WCAG AA compliance. Skip links. Landmark roles. Managed focus. Reduced-motion. Screen reader tested. |

**Key checks**:
- Do icon-only buttons have `aria-label`?
- Does the page use `<nav>`, `<main>`, `<section>`, `<header>`, `<footer>`?
- Are focus rings visible on keyboard navigation?
- Is `prefers-reduced-motion` supported?
- Do all images have alt text?

---

### 8. Visual Polish (0-10)

**What it measures**: Border radius consistency, shadow depth, micro-interactions, overall fit and finish.

| Score | Description |
|-------|-------------|
| 0-2 | Default browser styling. No shadows. Mixed/sharp corners. No polish. |
| 3-4 | Some rounded corners. Minimal shadows. Looks like a prototype. |
| 5-6 | Consistent radius. Some shadows. Looks functional but not refined. |
| 7-8 | Unified radius scale. Shadow depth hierarchy. Micro-interactions. Professional feel. |
| 9-10 | Pixel-perfect. Intentional shadow depth. Glassmorphism/blur effects. Feels premium. |

**Key checks**:
- Is border-radius consistent across the app?
- Do shadows create meaningful depth hierarchy?
- Are there micro-interactions (button press, toggle switch, etc.)?
- Does the overall aesthetic feel intentional and cohesive?

---

## Letter Grade Mapping

Total score = sum of all 8 dimensions (max 80).

| Grade | Total Score | Description |
|-------|-------------|-------------|
| A+ | 72-80 | Ship it. Production-ready premium quality. |
| A | 64-71 | Excellent. Minor polish remaining. |
| B | 56-63 | Good. Solid foundation, some dimensions need attention. |
| C | 48-55 | Needs work. Several dimensions below standard. |
| D | Below 48 | Significant work needed across most dimensions. |

## Quality Thresholds

| Context | Minimum Grade |
|---------|---------------|
| Public marketing site | A (64+) |
| SaaS dashboard | B+ (60+) |
| Internal tool | B (56+) |
| MVP / prototype | C (48+) |

## Before/After Comparison

When reporting results, always show:

1. **Per-dimension delta**: `Animation: 2 -> 7 (+5)`
2. **Overall delta**: `Total: 32 -> 62 (+30), Grade: D -> B`
3. **Key changes**: What specifically improved each dimension
4. **Remaining gaps**: What still needs work to reach the next grade

## What "Ship It" Looks Like

A route scores A+ when:
- Every section animates in smoothly on scroll
- Every button has hover lift + tap press
- Typography has clear hierarchy with proper weights
- Colors are from a unified palette with semantic meaning
- Spacing follows a consistent rhythm
- Mobile layout is intentional, not just "responsive"
- Keyboard users can navigate with visible focus
- Reduced-motion users get a functional but static experience
- Shadows create meaningful depth
- The overall feel is cohesive and professional
