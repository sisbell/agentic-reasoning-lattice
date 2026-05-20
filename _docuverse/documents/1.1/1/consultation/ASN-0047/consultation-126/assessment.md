# Channel Assignment — ASN-0047 review-126

**Date:** 2026-05-19 18:59

## Issue 1: K.μ⁻'s precondition uses circular post-state formulation
Reason: The constructive shape characterization (per-subspace suffix removal under D-CTG★ + D-MIN★ + D-SEQ★) is already derived in the ASN's "K.μ⁻ admissible contraction shape" paragraph. The fix is purely a presentational refactor — moving the derived constructive form into the precondition statement — and requires no design intent or implementation evidence beyond what the ASN already contains.

## Issue 2: Verification matrix cells are non-uniform in elaboration depth
Reason: The discharge mechanisms (full-clearance form convention, decomposition routes, frame entries) are all already established in the ASN body and matrix preamble notes. Elaborating terse cells or adding a matrix legend is purely an editorial uniformity fix internal to the ASN.

## Issue 3: Sprawl — 30,000+ word ASN risks unreviewable state
Reason: Splitting the ASN into four-component and extended-state pieces is a structural organization decision about how the formalization is packaged. The split-point (link store introduction) is already a natural seam in the ASN; no design intent or implementation evidence is needed to decide whether to materialize it as separate documents.

## Issue 4: K.μ~ admissibility clause (i) explicitly retained as "redundant for clarity"
Reason: The redundancy of clause (i) against clauses (ii)+(iii) is already proven inline in the ASN. Whether to remove the clause or flag it inline at the admissibility statement is a purely internal contract-shape decision derivable from the ASN's own derivation.
