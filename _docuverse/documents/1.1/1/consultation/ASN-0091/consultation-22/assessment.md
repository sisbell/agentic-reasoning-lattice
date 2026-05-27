# Channel Assignment — ASN-0091 review-22

**Date:** 2026-05-26 20:15

## Issue 1: R-SP application to the unified state needs clarification
Reason: The fix is about correctly partitioning which ASN-0036 invariants R-SP discharges versus which are superseded by S3★/S8★ in the unified state. All needed material is in ASN-0084 (R-SP's Q), ASN-0036 (invariant list), and ASN-0047 (starred replacements); no design intent or implementation evidence required.

## Issue 2: Forward reference to RE-sub in early derivations
Reason: Purely an organizational/dependency-order issue. The substantive justification (CS3 + R-FRAME-P/S(a)) is already established in ASN-0084 and cited elsewhere in this ASN; the fix is reorganization or direct citation, derivable internally.

## Issue 3: E_doc / dom(M) identification asserted parenthetically
Reason: The identification concerns how ASN-0047's K.δ-IsDocument and ASN-0093's K.σ interact in the unified state — both are formally defined in the project's existing ASNs, and the reviewer's suggested fix paths (cite convention, derive from K.σ/K.δ semantics, or state as axiom) are all internal to the substrate. No appeal to Nelson's design intent or Gregory's implementation is required.
