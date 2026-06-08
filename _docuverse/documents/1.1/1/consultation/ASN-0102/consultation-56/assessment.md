# Channel Assignment — ASN-0102 review-56

**Date:** 2026-06-08 01:22

## Issue 1: P4★ / J1'★ discharge assumes containment-in-R at a state that may not be a composite boundary
Reason: The fix is a proof restructuring: recast the discharge as step-local preservation of `Contains_C ⊆ R` using an inductive hypothesis, rather than invoking P4★ at an arbitrary `Σ`. The classification of P4★ as a composite-boundary property is already established in ASN-0047 (cited) and the corrected derivation uses only COPY's own effect clauses and X1/X7 already present in the ASN — no design intent or implementation evidence is needed.

## Issue 2: Duplicated statement that COPY is added to the transition vocabulary
Reason: Purely editorial deduplication — collapse two adjacent sentences asserting the same vocabulary amendment into one, retaining only the non-redundant "changing `M` and `R`" content. Fully internal.
