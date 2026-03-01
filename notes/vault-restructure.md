# Vault Directory Restructure

*2026-03-01 — implemented*

Follows Abrial's framework (requirements → modeling → coding). The vault groups
artifacts by their role: **modeling** (primary artifacts), **discovery** (working
artifacts of building the model), and **formalization** (working artifacts of
encoding the model for verification).

## Structure

```
vault/
  modeling/         — the model artifacts
    asns/           — Abstract Specification Notes
    dafny/          — verified specification modules
    vocabulary.md   — shared vocabulary

  discovery/        — working artifacts of building the model
    inquiries.yaml  — inquiry definitions
    consultations/  — orchestrated consultation output
    transcripts/    — individual agent call logs
    reviews/        — review outputs
    triage/         — triage decisions

  formalization/    — working artifacts of encoding the model
    contracts/      — property contracts (type + Dafny name mappings)
    extracts/       — extracted formal properties

  usage-log.jsonl   — API call tracking
```

## Implementation

All vault paths centralized in `scripts/paths.py`. Scripts import from
`paths` instead of hardcoding vault subdirectory paths.

## Naming decisions

- **modeling** (not "model") — follows Abrial's terminology
- **discovery** (not "requirements") — these are working artifacts of the
  discovery process, not requirements themselves
- **formalization** (not "formal") — noun form, consistent with other directory names
- **extracts** (not "properties") — files contain both properties AND definitions
