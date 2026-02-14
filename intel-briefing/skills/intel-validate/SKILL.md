---
name: intel-validate
description: |
  Validate claims against external sources using the research-validator agent.
  Searches for corroborating evidence, contradicting perspectives, and additional
  context to update claim confidence scores. Supports filtering by category or document.
triggers:
  - "intel validate"
  - "validate claims"
  - "claim validation"
  - "external validation"
  - "verify claims"
  - "fact check"
version: 1.2
author: ROK Agency
---

# Intel Validate

Validate claims against external sources.

## Usage

```
/intel-briefing:intel-validate                      # Validate up to 10 unvalidated claims
/intel-briefing:intel-validate all                  # Validate all (in batches)
/intel-briefing:intel-validate category:financial    # Only financial claims
/intel-briefing:intel-validate limit:5              # Limit to 5 claims
/intel-briefing:intel-validate document:[doc_id]    # Validate from specific document
```

## When to Use

- After ingesting new documents to validate extracted claims
- Periodically validating claims that haven't been checked
- Focusing validation on a specific category or document
