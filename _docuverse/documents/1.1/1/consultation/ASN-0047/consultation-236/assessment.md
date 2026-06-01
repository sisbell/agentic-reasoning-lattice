# Channel Assignment — ASN-0047 review-236

**Date:** 2026-06-01 10:52

## Issue 1: K.μ⁺_L empty-subspace case references an undefined depth `m_L(d)`
Reason: Internal. The fix mirrors the content subspace's existing `ValidFirstInsertionPosition(d, v, m)` parameterization; the free-choice intent (`m ≥ 2` by S8a) is already stated in the worked example, so the non-circular restatement is derivable from the ASN's own content.

## Issue 2: Unused partial-suffix expansion machinery in the K.μ~ decomposition
Reason: Internal. The ASN itself establishes that every proof and matrix cell uses the full-clearance form and that the partial-suffix form discharges nothing; deciding to drop or reduce it is an editorial judgment requiring no design intent or implementation evidence.

## Issue 3: Duplicated default-value / `E_doc`-membership discrimination prose
Reason: Internal. Pure deduplication — consolidating the discrimination rationale at the Notational convention site and trimming the K.δ frame to its effect requires only the ASN's existing text.

## Issue 4: Use-site inventory prose attached to discharge routes
Reason: Internal. Removing the consumer-inventory back-pointers is an editorial cleanup fully derivable from the ASN; the matrix cells already name their own discharge routes.
