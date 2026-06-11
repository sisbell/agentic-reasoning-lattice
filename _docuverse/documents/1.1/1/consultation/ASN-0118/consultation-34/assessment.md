# Channel Assignment — ASN-0118 review-34

**Date:** 2026-06-11 00:33

## Issue 1: Level-uniformity is a precondition with no consumer
Reason: Whether to drop the `#s = #ℓ` conjunct or keep it as a deliberate alignment turns on design intent — whether Nelson's span concept structurally ties the width tumbler's shape to the start's. The implementation side is already settled in the ASN (udanax-green performs no depth or shape check anywhere in span validation or classification), so Gregory adds nothing.
Nelson question: In Nelson's span design, is the width tumbler intended to carry the same structural shape (tumbler length) as the start tumbler, or is it merely a difference/offset whose shape is unconstrained — i.e., is level-uniformity part of what a span *is*, or an artifact of one formalization?

## Issue 2: The `enabled(COPY)` enumeration in the wp formula omits state-dependent spec-set admissibility
Reason: The fix is internal: the missing conditions (`d_s ∈ dom(Σ.M)`, T12 well-formedness, the second admissibility condition, non-empty source subspace) are already defined in the ASN's own V-spec admissibility section, and the required change is to fold them into the enumerated predicate. No design-intent or implementation question is open.

## Issue 3: CP3c is never explicitly discharged in the composite exhibition
Reason: The fix is internal: the discharge already follows from facts the exhibition states — K.μ⁻'s retained prefix, K.μ⁺'s exactly-specified additions, and the vacated positions removed in step (i) — and only needs one explicit sentence per case. Neither design intent nor implementation evidence bears on it.
