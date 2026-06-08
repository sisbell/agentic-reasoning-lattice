# Channel Assignment — ASN-0107 review-14

**Date:** 2026-06-08 10:52

## Issue 1: R6's retention set is characterized as an arbitrary subset, not K.μ⁻'s canonical form
Reason: The fix is to restrict `R` to K.μ⁻'s canonical per-subspace prefix form, which is already defined in ASN-0047 (cited by the ASN) and already used correctly in the worked instance's contraction. No design intent or implementation evidence is needed — only conformance to the substrate operation the ASN already references.

## Issue 2: The "no store-level retraction / k=1 specialization" point is restated across four claims
Reason: Purely an editorial deduplication — the no-removal fact is just L12 + E2 (both already in the ASN) and the k=1/k-general relationship is internal to R1/R2. Consolidating phrasings requires nothing beyond the ASN's own content.

## Issue 3: Defensive parenthetical referencing prior "concerns"
Reason: The fix is to delete a parenthetical; totality and the `num = 0` cases are already established positively in the same section. Wholly internal.
