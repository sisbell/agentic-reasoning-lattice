# Channel Assignment — ASN-0118 review-2

**Date:** 2026-06-08 21:31

## Issue 1: CP1 is stipulated, not derived — the "necessity" claim is unsupported
Reason: Internal. The fix is a logical recasting of the ASN's own argument — relabel CP1 as COPY's defining frame condition and reframe S3-dischargeability as conditional on it, using only CP0(a), S1, and the REPLICATE contrast already present in the text.

## Issue 2: Empty-destination boundary case omitted from the contiguity/tiling derivation
Reason: Internal. The missing `V_{s_C}(d) = ∅` case is derivable from primitives already cited (ValidFirstInsertionPosition, D-MIN, D-SEQ); CP3a/CP3b go vacuous and the post-state run establishes D-MIN/D-SEQ directly.

## Issue 3: Missing precondition that the spec-set's active positions lie in the content subspace
Reason: Internal. The ASN already scopes itself to content spec-sets and defers link-subspace transclusion to its own Open Questions; the fix is promoting that stated scope to an explicit precondition, which needs no design intent or implementation evidence.

## Issue 4: CP8 provenance — J1★ cited as if it produces the record, and self-transclusion "already held" relies on an uncited invariant
Reason: Internal. The fix turns on ASN-0047's own coupling machinery (K.μ⁺/K.ρ decomposition, J1★/J1'★ as obligation/uniqueness, P4★ for prior membership, P2 for persistence) — all formal content available in the cited foundation ASN, not contingent on Nelson's intent or Gregory's code.
