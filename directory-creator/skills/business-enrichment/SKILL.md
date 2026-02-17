---
name: business-enrichment
description: |
  Website extraction techniques for enriching business directory
  listings. Covers homepage/about/contact/services page patterns,
  data normalization rules for phone (E.164), address parsing, URL
  standardization, and hours formatting. Used by the data-enricher agent.
triggers:
  - "business enrichment"
  - "data enrichment"
  - "website extraction"
version: 1.0
author: ROK Agency
---

# Business Enrichment Techniques

## Website Extraction Patterns

### Homepage Extraction
The homepage typically contains: business name, tagline/description, phone, address, hours, social links in header/footer.

**WebFetch prompt**: "Extract the following from this business website: business name, phone number, physical address, hours of operation, a 1-2 sentence description of services, and any social media links (Facebook, Instagram, LinkedIn, Twitter/X) found in the header or footer."

### Services/About Page
Usually linked as "Services", "What We Do", "About Us", or "Our Work" in the main navigation.

**WebFetch prompt**: "Extract: complete list of services offered, specializations or certifications mentioned, years in business, number of employees or team members, service areas or coverage map details, any guarantees or warranties."

### Contact Page
Usually linked as "Contact", "Get in Touch", "Request a Quote", or "Book Now".

**WebFetch prompt**: "Extract: phone number, email address, physical address with suite/unit number, hours of operation, service area list, booking or scheduling URL."

## Data Normalization Rules

### Phone Numbers
- Target format: E.164 (`+15125551234`)
- Strip: parentheses, dashes, spaces, dots, "tel:", "phone:"
- Add +1 prefix if 10 digits (US number)
- If extension present, append `;ext=XXX`
- If multiple phones found, use the first (main) number

### Address Parsing
- Separate into: address (street), city, state, zip_code
- Use 2-letter state abbreviations (TX, not Texas)
- Include suite/unit numbers in the address field
- If PO Box only, note in enrichment_notes

### URL Standardization
- Ensure `https://` prefix (try https first)
- Strip trailing slashes
- Remove UTM parameters and tracking fragments
- Lowercase the domain portion
- Keep path case as-is

### Hours Formatting
- Target format: `Mon-Fri 8am-6pm, Sat 9am-2pm`
- Use 12-hour format with am/pm (lowercase)
- Combine consecutive days with same hours (Mon-Fri, not Mon, Tue, Wed, Thu, Fri)
- Use "24/7" for always-open businesses
- Use "By appointment" if applicable
- If closed on specific days, omit them (don't write "Sun: Closed")

### Email
- Lowercase
- Validate: must contain @ and at least one . after @
- Prefer info@, contact@, hello@ over personal email addresses

### Services Array
- Each service as a separate string
- Title Case formatting
- Remove duplicates
- Sort alphabetically
- Max 15 services per listing (summarize if more)

### Description
- 1-3 sentences, max 250 characters
- Should mention: what they do, location, key differentiator
- Remove marketing superlatives ("the absolute best", "#1 in the world")
- Keep factual claims ("serving since 2005", "licensed and insured")
