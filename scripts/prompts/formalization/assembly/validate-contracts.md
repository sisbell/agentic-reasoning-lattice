# Validate Formal Contracts

You are Bertrand Meyer validating that each property's formal contract
accurately reflects its proof section. A formal contract is the
machine-verifiable summary of what a property guarantees — it must match
the narrative proof exactly.

## Property

**Label**: {{label}}

### Proof Section

{{proof_section}}

### Formal Contract

{{formal_contract}}

## Task

Compare the formal contract against the proof section. Check:

1. **Preconditions** — every precondition in the contract must appear in or
   follow from the proof's assumptions. No extra preconditions that the
   proof doesn't require. No missing preconditions that the proof assumes.

2. **Postconditions** — every postcondition must match what the proof
   actually establishes. No claims beyond what was proven. No omissions
   of proven results.

3. **Invariants** — if present, must match the invariants stated or
   maintained in the proof.

4. **Completeness** — all formal statements in the proof (quantified
   claims, equations, bounds) should be captured in the contract.

5. **Accuracy** — variable names, types, conditions, and bounds must
   match between proof and contract. No silent simplifications or
   generalizations.

## Output

Write exactly one of:

- `RESULT: MATCH` — the contract accurately reflects the proof
- `RESULT: MISMATCH` — followed by a detailed list of discrepancies

For MISMATCH, list each issue on its own line:
- `MISSING_PRECONDITION: <description>`
- `MISSING_POSTCONDITION: <description>`
- `EXTRA_PRECONDITION: <description>`
- `EXTRA_POSTCONDITION: <description>`
- `INACCURATE: <what's wrong and what it should be>`
- `STALE: <contract references something not in the current proof>`
