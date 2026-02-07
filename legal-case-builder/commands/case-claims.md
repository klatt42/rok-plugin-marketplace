# /case-claims - Build and Review Legal Claims

Create, review, and strengthen legal claims with linked evidence documents. Each claim maintains an auditable chain from legal argument to specific documents and excerpts.

## Usage

```
/case-claims                                     # Review all claims
/case-claims action:review                       # Same as above
/case-claims action:build type:breach_of_contract
/case-claims action:strengthen id:3              # Find more evidence for claim #3
/case-claims type:gross_negligence               # Review specific claim type
```

### Parameters
- **action** - `review` (default) | `build` | `strengthen`
- **type** - Claim type filter: `breach_of_contract`, `gross_negligence`, `constructive_eviction`, `opex_fraud`, `failure_to_repair`, `habitability`
- **id** - Specific claim ID (for strengthen action)

## Execution Steps

### Action: `review` (default)

Call the `get_claims_summary` MCP tool:

```
Tool: mcp__legal-case-builder__get_claims_summary
Parameters:
  claim_type: [type parameter if provided]
```

Present all claims with their evidence:

```
═══════════════════════════════════════════════════════
LEGAL CLAIMS SUMMARY
═══════════════════════════════════════════════════════

## Breach of Contract (2 claims)

### Claim #1: [claim text]
Strength: [strong/moderate/supporting]
Evidence: [count] documents
  - Doc #12 (email): [relevance note]
  - Doc #45 (lease): [relevance note]
  - Doc #67 (invoice): [relevance note]

### Claim #2: ...

## Gross Negligence (1 claim)
...

---

Total claims: [count]
Total evidence links: [count]

═══════════════════════════════════════════════════════
```

### Action: `build`

Guide the user through claim creation:

1. If `type:` not provided, ask the user which claim type to build
2. Ask for the claim text (description of the legal argument)
3. Use `find_evidence_for` to search for supporting documents:

```
Tool: mcp__legal-case-builder__find_evidence_for
Parameters:
  argument: [claim text / argument description]
  min_relevance: 0.5
```

4. Present the top evidence candidates with relevance scores
5. Ask the user to confirm which documents to link
6. Call `build_claim`:

```
Tool: mcp__legal-case-builder__build_claim
Parameters:
  claim_type: [type]
  claim_text: [claim description]
  evidence_document_ids: [selected doc IDs]
  evidence_notes: [relevance notes per doc]
```

7. Confirm the claim was created with its evidence chain

### Action: `strengthen`

Find additional evidence for an existing claim:

1. Call `get_claims_summary` to get the claim details
2. Use `find_evidence_for` with the claim text
3. Filter out documents already linked to the claim
4. Present new evidence candidates
5. Ask user to confirm additions
6. Create a new evidence link via `build_claim` (or direct DB update)

## Claim Types Reference

| Type | Description | Key Evidence |
|------|-------------|--------------|
| `breach_of_contract` | Landlord failed to meet lease obligations | Lease provisions, repair requests, refusal emails |
| `gross_negligence` | Reckless disregard (e.g., ProPress fittings) | Inspection reports, expert opinions, failure patterns |
| `constructive_eviction` | Conditions make space uninhabitable | Temperature logs, complaint emails, HVAC failure timeline |
| `opex_fraud` | Improper operating expense allocation | OPEX statements, lease calculation provisions, audit requests |
| `failure_to_repair` | Landlord did not make required repairs | Repair requests, response delays, work order gaps |
| `habitability` | Space does not meet commercial habitability standards | Inspection reports, temperature records, code violations |

## Important Rules

- Every claim MUST have at least one evidence document
- Evidence excerpts should be actual quotes from documents, not fabricated
- Claim strength assessment should be conservative
- Always show the evidence chain when presenting claims
- When building claims, search broadly — evidence may come from unexpected document types
- Do NOT create duplicate claims — check existing claims first
