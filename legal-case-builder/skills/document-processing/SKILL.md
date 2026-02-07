---
name: document-processing
description: |
  Document ingestion and categorization patterns for legal case building.
  Email parsing from Outlook PDF exports, document type classification,
  tag taxonomy for landlord-tenant disputes, thread reconstruction logic,
  and timeline event extraction rules. Used during document ingestion
  and categorization workflows.
triggers:
  - "ingest"
  - "categorize"
  - "email parsing"
  - "document tags"
  - "PDF extraction"
  - "document type"
  - "thread"
version: 1.0
author: ROK Agency
---

# Document Processing Skill

## Document Type Classification

| Type | Indicators | Priority Fields |
|------|-----------|-----------------|
| `email` | From:/To:/Subject:/Sent: headers in first 500 chars | sender, date, subject, thread_id |
| `lease` | "Lease Agreement", tenant/landlord definitions | sections, provisions, effective date |
| `invoice` | Invoice number, amount due, billing address | vendor, amount, date, services |
| `letter` | Formal salutation, letterhead, demand language | sender, recipient, date, demands |
| `analysis` | Section headings, recommendations, strategy | author, conclusions, recommendations |
| `proposal` | Scope of work, pricing, terms | vendor, scope, price, timeline |
| `contract` | Parties, terms, signatures | parties, effective date, obligations |
| `work_order` | WO number, technician, service date | vendor, tech, date, work performed |
| `estoppel` | Estoppel certificate language, certifications | certifications, exceptions, date |
| `other` | None of the above | basic metadata |

## Outlook PDF Email Parsing

### Header Patterns
Outlook PDF exports follow these common patterns:

```
From: Display Name <email@domain.com>
Sent: Monday, January 15, 2024 2:30 PM
To: Recipient Name <recipient@domain.com>
Cc: CC Name <cc@domain.com>
Subject: Re: FW: Original Subject Line
Attachments: file1.pdf; file2.xlsx
```

### Date Formats (in order of frequency)
1. `Monday, January 15, 2024 2:30 PM`
2. `January 15, 2024 2:30 PM`
3. `1/15/2024 2:30:00 PM`
4. `2024-01-15 14:30:00`

### Thread Normalization
Strip prefixes recursively: RE:, FW:, Fwd:, Re:, Fw:
Lowercase the result for grouping.

Example: `RE: FW: RE: HVAC Issue at 12040` → `hvac issue at 12040`

### Direction Detection
- **Outbound**: Sender domain contains rok, rokmaryland, ronklatt
- **Inbound**: All other senders
- **Internal**: Both sender and recipient are ROK domains

## Tag Taxonomy

### HVAC Issues
| Tag | When to Apply |
|-----|--------------|
| `hvac_defect` | Manufacturing or installation defect identified |
| `hvac_repair` | Repair was performed or discussed |
| `hvac_failure` | System stopped working or performed inadequately |
| `hvac_emergency` | Emergency situation (no heat in winter, extreme temps) |
| `propress_fittings` | References ProPress fitting defects specifically |
| `vrv_unit1` | References VRV Unit #1 (main office) |
| `vrv_unit2` | References VRV Unit #2 (secondary) |
| `compressor` | References compressor issues |
| `supplemental_heat` | References temporary/supplemental heating |
| `office_temperatures` | References temperature complaints or measurements |

### Financial
| Tag | When to Apply |
|-----|--------------|
| `opex_dispute` | Dispute over operating expense charges |
| `opex_allocation` | Discussion of OPEX calculation methodology |
| `insurance_cost` | Insurance-related charges or disputes |
| `tax_bill` | Property tax charges or disputes |
| `rent_credit` | Rent credit requested or applied |
| `invoice_reimbursement` | Request for reimbursement of expenses |

### Party Actions
| Tag | When to Apply |
|-----|--------------|
| `landlord_refusal` | Landlord explicitly refuses a request |
| `landlord_deflection` | Landlord redirects, delays, or avoids addressing |
| `landlord_response` | Any landlord response (neutral tag) |
| `tenant_complaint` | Tenant raises an issue or complaint |
| `tenant_notice` | Formal notice from tenant |
| `tenant_request` | Tenant makes a specific request |

### Legal
| Tag | When to Apply |
|-----|--------------|
| `attorney_correspondence` | Communication involving attorneys |
| `legal_notice` | Formal legal notice or demand |
| `legal_strategy` | Discussion of legal strategy or options |

### Vendor/Property
| Tag | When to Apply |
|-----|--------------|
| `pm_contract` | Property management contract discussion |
| `vendor_quote` | Vendor provides a quote or estimate |
| `vendor_invoice` | Vendor submits an invoice |
| `construction_defect` | Building construction defect identified |
| `phase2_construction` | Related to Phase 2 construction specifically |
| `estoppel` | Estoppel certificate related |
| `lease_provision` | References specific lease section |
| `property_management` | General property management topic |
| `building_maintenance` | Building maintenance topic |

## Timeline Event Extraction Rules

### What Constitutes an Event
- A communication with a specific date and identifiable action
- A repair, failure, or inspection with a date
- A payment, invoice, or financial transaction
- A legal action (demand letter, notice, filing)

### Event Type Classification
| Type | Examples |
|------|---------|
| `communication` | Email sent, letter received, phone call noted |
| `repair` | HVAC repair performed, work order completed |
| `failure` | System failed, outage reported, emergency declared |
| `refusal` | Request denied, obligation rejected |
| `payment` | Invoice paid, rent credit applied, reimbursement |
| `legal_action` | Demand letter sent, attorney engaged, notice served |
| `inspection` | Site visit, system inspection, assessment |

### Significance Rules
- **Critical**: Events that directly prove or disprove a claim element
- **Supporting**: Events that corroborate or provide context for critical events
- **Context**: Background events that establish the timeline but don't directly impact claims

### Extraction Priority
1. Explicit dates mentioned in document text
2. Email date (from metadata)
3. File modification date (last resort)
