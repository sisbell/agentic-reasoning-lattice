# Revision Categorization — ASN-0040 review-1

**Date:** 2026-03-15 12:33

## Issue 1: No closure property on Σ.B
Category: INTERNAL
Reason: The ASN already assumes baptism is the sole growth mechanism for Σ.B — the closure axiom is implicit in B1's proof and B2's definition. The fix is to make this assumption an explicit axiom using machinery already present.

## Issue 2: B4 is vacuously true
Category: INTERNAL
Reason: The ASN's prose already articulates the correct requirement (per-namespace serialization of read-compute-write). The fix is reformulating the formal statement to match the prose — no external evidence needed.

## Issue 3: B₀ initial conditions leave B1 ungrounded
Category: INTERNAL
Reason: The fix is adding "B₀ satisfies B1 for all namespaces" as an explicit precondition. This is a logical requirement derivable from the inductive structure of the B1 proof itself.

## Issue 4: B3 fourth case claimed "excluded by construction" without the construction
Category: INTERNAL
Reason: The fix is rewording from "excluded by construction" to a stated requirement on future content operations. The ASN already identifies content storage as out of scope — this is just correcting the epistemic status of the claim.

## Issue 5: B5 does not cover sibling increments
Category: INTERNAL
Reason: The ASN already notes that TA5(c) preserves length and modifies only the last significant component. The zeros-preservation lemma for sibling increments follows directly from this — it just needs to be stated explicitly.

## Issue 6: No concrete worked example
Category: INTERNAL
Reason: All definitions (inc, zeros, sibling stream, hwm, next) and properties (B1, B5, B6, B7) are already specified. Tracing a sequence like B₀ = {[1]} → baptize user → baptize second user is mechanical evaluation of existing formalism.

## Issue 7: wp analysis is trivial
Category: INTERNAL
Reason: Computing wp(baptize(p,d), B1 holds) uses only the ASN's own definitions of baptize, B1, and the closure property from Issue 1. The interesting preconditions are already latent in the formal framework.
