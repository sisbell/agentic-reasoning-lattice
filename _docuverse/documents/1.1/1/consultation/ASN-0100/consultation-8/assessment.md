# Channel Assignment — ASN-0100 review-8

**Date:** 2026-05-27 14:48

## Issue 1: K.μ⁻ omission case (ii) rationale doesn't cover V_{s_L}(d) = ∅ sub-sub-case
Reason: Purely an internal logic refinement about K.μ⁻'s precondition arithmetic in ℕ when n_{s_L} = 0. The fix splits or unifies sub-sub-case wording using K.μ⁻'s already-cited semantics from ASN-0047 and INSERT's own frame INS.frame.subspace.

## Issue 2: K.μ⁻ omission framed as forced when it is a canonical choice in case (ii)
Reason: Internal distinction between forced-by-precondition and canonical-decomposition-choice; the ASN already acknowledges decomposition non-uniqueness later, and K.μ⁻ semantics from ASN-0047 plus INS.frame.subspace settle which sub-cases force vs. permit omission.

## Issue 3: Empty-case worked example is brief and lacks composite-boundary discharge trace
Reason: Elaboration of an already-specified composite using cited machinery (K.α, K.μ⁺, K.ρ from ASN-0047; J0/J1★/J1'★ discharge already worked out for the interior case). The empty-arrangement-but-non-empty-allocator-state sub-case is already characterized in the ASN's empty-case paragraph; making it concrete is mechanical.

## Issue 4: "V_{s_C}(d') = exact union of three regions" is in narrative, not a labeled postcondition
Reason: Pure structural-format fix — promote the narrative exhaustiveness sentence to a labeled postcondition or footnote tracing exhaustiveness to step-3 K.μ⁺'s precise additions per ASN-0047.

## Issue 5: Insertion-region S8a argument elides the k = 0 case
Reason: Internal precondition bookkeeping; the ASN already adopts the `shift(p, 0) = p` convention via OrdinalShiftBase (ASN-0058) and OrdinalShift's n ≥ 1 domain via ASN-0034. Split the verification at k=0 (inherit from ValidInsertionPosition postcondition (d)) vs. k≥1 (TumblerAdd).

## Issue 6: Worked-example projection trace assumes tight endset without explicit precondition
Reason: Presentational fix — state the tightness assumption as a precondition of the worked example or run two parallel traces, both using LP19a (ASN-0098) already cited in INS.identity.tightsurv and INS.proj.
