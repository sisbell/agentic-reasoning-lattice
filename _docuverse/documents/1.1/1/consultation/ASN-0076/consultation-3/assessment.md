# Channel Assignment — ASN-0076 review-3

**Date:** 2026-05-25 20:03

## Issue 1: E0 admissibility proof is hand-waved
Reason: All preconditions and axioms cited (SubAllocatorAxiom, L11a, K.λ preconditions, link allocation discipline) are in foundation ASNs already in the recap. The discharge is a mechanical expansion using existing definitions.

## Issue 2: T12 satisfaction for supersession spans not verified
Reason: T12 and OrdinalDisplacement's postconditions on `Pos(δ(n, m))` and `actionPoint(δ(n, m)) = m` are foundation facts. Discharging T12 is a direct application of these to the three constructed spans — no design intent or implementation evidence required.

## Issue 3: K.λ emission case not addressed in composite
Reason: K.λ's first-emission vs subsequent-emission cases are defined in ASN-0047. Addressing both sub-cases for `ℓ_new` and identifying `ℓ_sup` as subsequent is a mechanical expansion of K.λ's allocation rule against the composite's pre-states.

## Issue 4: Worked example covers only a subset of claims
Reason: Extending the existing worked example to cover E0, E3, E5, E6, E8, E9 is purely internal — it reuses the same tumbler values and applies the proofs already in the ASN to the concrete scenario.

## Issue 5: "Supersession link" structural identification conflates structure with semantics
Reason: This is a rewording task to sharpen the distinction the ASN itself already articulates (τ_sup convention deferred to a future ASN). No external evidence is needed; the structure/semantics split is internal to the construction.

## Issue 6: Invariant inheritance from K.λ not made explicit
Reason: ExtendedReachableStateInvariants is defined in ASN-0047 and ValidComposite★ inheritance is established there. Adding the citation is a direct reference to existing foundation material.
