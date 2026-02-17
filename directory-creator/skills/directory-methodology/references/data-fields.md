# Data Fields Reference

Complete field definitions matching the DirectoryGenius `businesses` table schema. All fields are included in the CSV export for direct import.

## Core Fields (Required)

| Field | Type | Max Length | Description | CSV Column |
|-------|------|-----------|-------------|------------|
| name | string | 255 | Legal business name | name |
| slug | string | 255 | URL-safe identifier (auto-generated) | slug |
| city | string | 100 | City name | city |
| state | string | 2 | 2-letter state abbreviation | state |
| status | enum | - | verified, needs_verification, removed | status |
| quality_score | integer | - | 0-100 quality score | quality_score |

## Contact Fields (Preferred)

| Field | Type | Max Length | Description | CSV Column |
|-------|------|-----------|-------------|------------|
| address | string | 255 | Street address (including suite/unit) | address |
| zip_code | string | 10 | ZIP or ZIP+4 | zip_code |
| phone | string | 20 | E.164 format (+15125551234) | phone |
| email | string | 255 | Contact email (lowercase) | email |
| website | string | 500 | Full URL with https:// | website |

## Detail Fields (Optional)

| Field | Type | Max Length | Description | CSV Column |
|-------|------|-----------|-------------|------------|
| category | string | 100 | Subcategory within niche | category |
| description | text | 500 | 1-3 sentence business description | description |
| hours | string | 255 | Standardized hours format | hours |
| service_radius | integer | - | Service area radius in miles | service_radius |
| rating | decimal | - | Aggregate rating (1.0-5.0) | rating |
| review_count | integer | - | Total review count | review_count |

## Array Fields (Optional)

These are stored as JSON arrays in the JSON export and as semicolon-delimited strings in CSV.

| Field | Type | Description | CSV Column | CSV Format |
|-------|------|-------------|------------|------------|
| services | string[] | List of services offered | services | "service1; service2; service3" |
| amenities | string[] | Features/amenities | amenities | "amenity1; amenity2" |
| service_areas | string[] | Cities/areas served | service_areas | "City1; City2; City3" |

## Social/Source Fields (Optional)

| Field | Type | Description | CSV Column |
|-------|------|-------------|------------|
| social_links | object | Social media URLs | facebook, instagram, linkedin, twitter (separate columns) |
| source | string | Discovery source(s) | source |

## DirectoryGenius CSV Column Order

For direct import into DirectoryGenius, the CSV must use this exact column order:

```
name, slug, category, description, address, city, state, zip_code, phone, email, website, hours, service_radius, rating, review_count, services, amenities, service_areas, facebook, instagram, linkedin, twitter, quality_score, status, source
```

## Field Validation Rules

- **phone**: Must match pattern `+1[0-9]{10}` or be empty
- **email**: Must match pattern `.*@.*\..*` or be empty
- **website**: Must start with `http://` or `https://` or be empty
- **rating**: Must be between 1.0 and 5.0 or null
- **review_count**: Must be >= 0 or null
- **quality_score**: Must be between 0 and 100
- **state**: Must be valid 2-letter US state abbreviation
- **zip_code**: Must match pattern `[0-9]{5}(-[0-9]{4})?` or be empty
- **slug**: Must match pattern `[a-z0-9-]+` (auto-generated from name)
