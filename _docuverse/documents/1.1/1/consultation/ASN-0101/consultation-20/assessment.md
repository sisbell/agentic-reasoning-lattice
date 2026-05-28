# Channel Assignment — ASN-0101 review-20

**Date:** 2026-05-27 20:55

## Issue 1: History-sequence formal predicate is not the load-bearing discriminator
Reason: The fix is a logical reformulation using ASN-0093's SequentialAtomicTransitions: replace the membership-predicate framing with explicit sequence-length counting (3 vs 2 states from Σ_pre). Nelson's design intent (DEL as primitive) and Gregory's run-to-completion realisation are unchanged; only the formal articulation needs recasting.

## Issue 2: D11 omits cross-document cardinality wp
Reason: Derivable from D9's first bullet (cross-document projection invariance) — the cardinality wp for d'' ≠ d reduces immediately to the pre-state predicate. Pure completeness extension internal to the ASN.

## Issue 3: Relationship between ASN-0098 LP-family and DEL not made explicit
Reason: The mapping from D-claims to LP-claims is mechanical: LP2★/LP3★/LP13 follow from D3, LP4–LP11 from D5/D6/D9, LP12/LP12a are supplanted by D11. All LP-family lemmas and their case-analysis structure are already documented in ASN-0098; the bridging paragraph requires only the D-claims already present in this ASN.

## Issue 4: "K.μ⁻ + K.μ~" naming is order-ambiguous
Reason: Pure notational fix — replace "+" with sequence notation consistently. No design or implementation question.

## Issue 5: D8 Group (iii) P4★ discharge chain is compressed
Reason: Pure expansion — make the three-step chain Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R' explicit. Internal correction.

## Issue 6: Empty arrangement / freshly-registered document case not addressed
Reason: Derivable from D0's precondition `s ∈ V_S(d)`: a document with M(d) = ∅ has V_S(d) = ∅ for both subspaces, making the precondition unsatisfiable. The relationship to K.σ (ASN-0093) and K.δ-IsDocument (ASN-0047) is structural — they produce empty arrangements and thus require at least one K.μ⁺/K.μ⁺_L step before DEL becomes applicable. Internal clarification.
