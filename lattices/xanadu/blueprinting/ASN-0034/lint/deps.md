# Dependency Lint — ASN-0034

Declared depends: []


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B1, B2, B3, B4]

## LLM Verification

## Classification: ASN-0040 — [B1, B2, B3, B4]

Searching the ASN-0034 text for these labels.

They appear in the **Verification of TA3** section, under "Case B: Component divergence at `j`":

> *Sub-case B1: `a` is zero-padded-equal to `w`.*
> *Sub-case B2: `dₐ = d_b = d`.*
> *Sub-case B3: `dₐ < d_b`.*
> *Sub-case B4: `dₐ > d_b`.*

These are internal proof case labels — named sub-cases in the exhaustive case analysis for the TA3 verification. They have no referential relationship to any property in ASN-0040; the scan matched the label text mechanically but B1–B4 here are just proof-structuring names, not citations of external properties.

| Label | Classification | Reason |
|-------|---------------|--------|
| B1 | CLEAN | Proof sub-case label in TA3 verification ("a zero-padded-equal to w"), not a property reference |
| B2 | CLEAN | Proof sub-case label in TA3 verification ("dₐ = d_b = d"), not a property reference |
| B3 | CLEAN | Proof sub-case label in TA3 verification ("dₐ < d_b"), not a property reference |
| B4 | CLEAN | Proof sub-case label in TA3 verification ("dₐ > d_b"), not a property reference |

`RESULT: 0 MISSING, 0 COLLISION, 0 LOCAL, 4 CLEAN`
