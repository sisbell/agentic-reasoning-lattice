# Channel Assignment — ASN-0100 review-80

**Date:** 2026-06-05 05:12

## Issue 1: Atomicity over-claims that intermediate states are unobservable
Reason: Internal fix. The ASN already proves the per-state-invariant/boundary-coupling guarantee; the revision only requires deleting the unproven unobservability assertion, which is purely editorial and consistent with the ASN's own open question.

## Issue 2: INS.C1a-app claim entry is a use-site inventory
Reason: Internal fix. The lemma's precondition→conclusion content (S2 ∧ S8-fin ∧ S8-depth ⇒ unique maximally-merged decomposition) is already stated in §S8★; removing the "instantiated at each discharge site" use-site inventory needs no external input.

## Issue 3: Implementation-mechanism enumeration in an abstract slot
Reason: Internal fix. The abstract point (Σ' is determined, the realizing decomposition is not) is already established by the uniqueness-of-Σ' argument; replacing the mechanism catalog with that point is derivable from the ASN alone.
