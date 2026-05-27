# Channel Assignment — ASN-0100 review-6

**Date:** 2026-05-27 14:06

## Issue 1: K.ρ ordering claim misrepresents substrate semantics
Reason: The fix concerns precise statement of substrate semantics — distinguishing J1★ (composite-boundary set membership requirement) from P4a (historical fidelity), and reading off ordering constraints from elementary preconditions in ASN-0047. All material is in the ASN's own references; no design intent or implementation evidence is needed.

## Issue 2: Per-state invariant verification at intermediates is not exhaustive
Reason: The fix is a completeness pass over ASN-0047's ExtendedReachableStateInvariants list, classifying each by which state component is touched (E, L, C, M) and noting frame-based preservation. Entirely derivable from ASN-0047's catalog and INSERT's frame conditions already stated.

## Issue 3: Projection-shift correspondence derivation under-detailed
Reason: The required derivation walks each intermediate state through LP9, LP10, LP6 (all from ASN-0098) — purely a per-step composition exercise using lemmas already cited. No design intent or implementation evidence enters the derivation.

## Issue 4: "Strengthened by P0" wording suggests P0 ⊋ S0
Reason: Wording correction prescribed by the reviewer; the equivalence between S0 (ASN-0036) and P0 (ASN-0047) and P0's subsumption of S1 are facts about the referenced ASNs' definitions.

## Issue 5: Composite atomicity assumption listed as state precondition
Reason: Structural reorganization of the formal contract — separating state preconditions from environmental assumptions. The distinction is already articulated in the ASN's prose; the fix moves the bullet to a new heading.

## Issue 6: "K.α and K.ρ do not commute with K.μ⁺ and K.μ⁻" — overbroad claim
Reason: The fix follows directly from inspecting K.α, K.μ⁻, K.μ⁺, K.ρ preconditions in ASN-0047 and identifying which transitions read which state components. Pure substrate-semantics correction, no external channels needed.
