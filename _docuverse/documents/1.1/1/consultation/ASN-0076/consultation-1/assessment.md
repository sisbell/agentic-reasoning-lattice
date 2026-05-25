# Channel Assignment — ASN-0076 review-1

**Date:** 2026-05-25 10:47

## Issue 1: τ_sup underspecified
Reason: τ_sup's structural form involves both design intent (what does the type registry concept mean in Nelson's architecture) and implementation evidence (how does udanax-green represent type addresses for link types).
Nelson question: Does the design include a "type registry" concept for link types, and what structural form (element-level vs document-level tumbler, content vs link subspace) was intended for type-address tumblers like τ_sup?
Gregory question: How does udanax-green represent link types and type designators — are type addresses element-level tumblers, content addresses, or some other convention, and what stability guarantees does the implementation provide for them?

## Issue 2: E10 frame statement is wrong on two counts
Reason: K.λ's frame is precisely defined in ASN-0047 and the fix is a mechanical correction to align with that frame. Derivable from the ASN's own foundation references.

## Issue 3: No verification against ValidComposite★
Reason: ValidComposite★ and its coupling constraints J0, J1★, J1'★ are defined in ASN-0047; discharging them for EDITLINK is a mechanical verification using foundation already cited.

## Issue 4: Missing formal preconditions
Reason: The required preconditions are simply the union of K.λ's preconditions evaluated at the initial state, plus any τ_sup constraints. Mechanical formalization from existing K.λ definition.

## Issue 5: E2 cites "L12 monotonicity" instead of L12a
Reason: Pure lemma-naming correction; L12a is defined in ASN-0043 as cited.

## Issue 6: ℓ_sup distinctness from ℓ_old and ℓ_new not stated
Reason: L11a applied to the two K.λ events of the composite directly yields the needed distinctness; no external input required.

## Issue 7: E7 depends on undefined discovery operation
Reason: Reframing as a structural property of the coverage relation is internal to the ASN — the witness via PrefixSpanCoverage is already present.

## Issue 8: No concrete worked example
Reason: The K.λ allocation rule and sub-allocator behavior are defined in ASN-0047; constructing a concrete example with specific tumbler values is derivable from the existing foundation.

## Issue 9: "Failures and resumptions" language inconsistent with foundation
Reason: SequentialTransitionAxiom in ASN-0047 directly specifies the correct vocabulary; mechanical rewording.

## Issue 10: "Concurrent users" language imprecise
Reason: Same as Issue 9 — SequentialTransitionAxiom dictates the correct framing as "either order"; internal correction.

## Issue 11: "Reader's Perspective" section is informal
Reason: The fix is an editorial decision (formalize as lemma vs. move to appendix as illustration), and the existing open question list already defers chain semantics, supporting the appendix choice without external input.
