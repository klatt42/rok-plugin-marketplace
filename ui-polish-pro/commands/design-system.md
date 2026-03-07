---
name: design-system
description: |
  Extract or generate a design token system from an existing codebase.
  Analyzes Tailwind config, CSS, and component classes to produce a unified
  set of colors, typography, spacing, radius, and shadow tokens. Standalone
  command that can be used independently of the polish pipeline.
user_invocable: true
---

# /ui-polish-pro:design-system

## Usage

```
/ui-polish-pro:design-system [repo_path] [--generate] [--output path/to/output.json]
```

- `repo_path` — path to the project root (defaults to current directory)
- `--generate` — generate a new design system rather than extracting from existing code
- `--output` — write the design system JSON to a specific file (default: `design-system.json` in project root)

## Workflow

### Mode: Extract (Default)

Extract a design system from what already exists in the codebase.

1. Dispatch the `design-extractor` agent with `mode: extract`
2. Wait for the proposed design system JSON
3. Present it to the user in a readable format:

```
## Extracted Design System: {projectName}

### Colors
- Primary: {primary} (used {N} times)
- Secondary: {secondary} (used {N} times)
- Accent: {accent}
- Semantic: success={success}, warning={warning}, error={error}

### Typography
- Heading font: {font}
- Body font: {font}
- Scale: display / h1 / h2 / h3 / h4 / body / small / micro

### Spacing
- Base unit: 4px (Tailwind default)
- Most common: {top_3_values}
- Inconsistencies found: {count}

### Border Radius
- Standard: {value}
- Cards: {value}
- Buttons: {value}

### Shadows
- {shadow_scale}

### Migrations Needed
{count} inconsistencies to normalize:
1. {migration_1}
2. {migration_2}
```

4. **HITL Gate**: Ask the user to approve or modify the system
5. Write the approved system to the output path

### Mode: Generate (`--generate`)

Generate a new design system from user preferences.

1. Ask the user for preferences:
   - **Style**: minimal / bold / glassmorphism / enterprise / startup
   - **Primary color**: blue / indigo / purple / emerald / rose / custom
   - **Typography**: Inter / Plus Jakarta Sans / DM Sans / system
   - **Vibe**: clean / warm / dark / vibrant

2. Generate a complete design system based on their choices
3. Present for approval
4. Write to output path

### Tailwind Config Integration

If the user approves, offer to update `tailwind.config.ts` with the design system tokens:

```typescript
// Add to theme.extend
colors: {
  primary: { DEFAULT: '#2563eb', light: '#dbeafe', dark: '#1e40af' },
  // ...
},
borderRadius: {
  DEFAULT: '0.5rem',
  lg: '0.75rem',
  xl: '1rem',
},
```

This is an **explicit permission** action — ask before modifying tailwind config.

## Output

The design system JSON is written to `{output_path}` and can be referenced by:
- `/ui-polish-pro:polish` (passed to route-polisher agents)
- `/ui-polish-pro:polish-route --design-system {output_path}`
- Other tools or manual reference

## Rules

- In extract mode, preserve the existing design intent — normalize, don't redesign
- In generate mode, create a professional, production-quality system
- Always present the system to the user before writing any files
- The JSON format must match the design-extractor agent's output schema
- Keep migration suggestions actionable (find/replace patterns)
