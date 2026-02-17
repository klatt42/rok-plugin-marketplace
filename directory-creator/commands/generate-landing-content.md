# Generate Landing Content

Generate SEO-optimized landing page content for a business directory. Produces hero, services, about, FAQ, and SEO configuration sections.

## Usage

```
/directory-creator:generate-landing-content                          # Use last directory data, authority style
/directory-creator:generate-landing-content --style=local-seo        # Local SEO focused content
/directory-creator:generate-landing-content --style=lead-gen         # Conversion-focused content
/directory-creator:generate-landing-content --style=minimal          # Clean, brief content
```

## Arguments

- **--style=** (optional): Content style — `authority` (default), `local-seo`, `lead-gen`, `minimal`

Initial request: $ARGUMENTS

## Workflow

### Step 1: Load Directory Data

Read `/tmp/directory_data.json`. If not found:
```
No directory data found. Run `/directory-creator:create-directory` first to generate a directory.
```

Extract key metrics for content generation:
- Directory name, niche, geography
- Total verified business count
- Top-rated businesses (top 5 by rating)
- Subcategories and their counts
- Average rating across all verified listings

### Step 2: Dispatch Content Generator

Read the agent definition from `agents/content-generator.md`.

Launch the content-generator agent using `Task` (subagent_type: `general-purpose`, model: `sonnet`):

Pass to the agent:
1. Full agent instructions from `agents/content-generator.md`
2. Directory data summary:
   - Directory name, niche, geography, subcategories
   - Verified business count, average rating
   - Top 5 business names (for social proof context, not to include in content)
3. Style preference from `--style=` argument

Collect results with `TaskOutput` (block=true).

### Step 3: Present Content

Parse the agent's JSON output and present each section in chat:

```
## Landing Page Content: [Directory Name]

**Style**: [authority/local-seo/lead-gen/minimal]

---

### Hero Section
**Headline (H1)**: [headline]
**Subheadline**: [subheadline]
**CTA**: [cta_text]

---

### Services Section

**[Subcategory 1 Title]** (H2)
[Description]
- [Service 1]
- [Service 2]
- [Service 3]

**[Subcategory 2 Title]** (H2)
[Description]
- [Service 1]
...

---

### About Section
**Title (H2)**: [title]

[Body paragraphs]

---

### FAQ Section

**Q: [question 1]**
A: [answer 1]

**Q: [question 2]**
A: [answer 2]

...

---

### SEO Configuration

| Element | Value |
|---------|-------|
| Title Tag | [title_tag] ([X] chars) |
| Meta Description | [meta_description] ([X] chars) |
| H1 | [h1] |
| Schema Type | [schema_type] |

**Target Keywords**:
- Primary: [primary]
- Secondary: [list]
- Long-tail: [list]

**Internal Linking Suggestions**:
- [suggestion 1]
- [suggestion 2]

---

### Schema Markup (JSON-LD)
```json
[schema_template]
```
```

### Step 4: Save Content

Write the full content output to `/tmp/directory_landing_content.json` for reference.

Offer to export:
```
Landing content saved to /tmp/directory_landing_content.json

Would you like to:
1. Copy specific sections (hero, about, FAQ, etc.)
2. Generate HTML file with all sections
3. Adjust style and regenerate
```

## Rules

- Content must use actual business counts and geography from the directory data, not placeholders.
- Title tags must be 50-60 characters. Meta descriptions must be 140-160 characters. Verify exact lengths.
- Do not include specific business names in the generated content (the directory listing handles that).
- Schema markup must be valid JSON-LD that can be directly embedded in an HTML page.
- FAQ answers should provide genuine practical advice, not just marketing copy.
