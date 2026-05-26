# Channel Assignment — ASN-0076 review-11

**Date:** 2026-05-25 21:58

## Issue 1: Composite notation makes outputs look like inputs
Reason: Fix is a notational rewrite to match K.λ's allocator-rule semantics already established in ASN-0047 and used correctly throughout the proof body. No external evidence or design intent is needed.

## Issue 2: Ownership prose unsupported by formalism
Reason: Fix is an editorial labeling choice — either tag the passages as informal motivation or restate them as the formal claim about `d_new ∈ E_doc`. The formal model and its limits are already established in the ASN and ASN-0047; the gap is acknowledged, not researched.

## Issue 3: E5 inductive hypothesis omits invariant preservation
Reason: Pure proof-structure fix. ExtendedReachableStateInvariants from ASN-0047 (already cited in §The Composite for invariant inheritance) supplies the needed closure; the induction just needs to carry the hypothesis explicitly.

## Issue 4: E2 proof structure is imprecise about intermediate states
Reason: Pure proof-structure fix. The K.λ precondition semantics and L12 are already cited and sufficient; the two K.λ steps simply need to be separated rather than collapsed under one L12a appeal.

## Issue 5: E5 theorem statement leaves ℓ_old unbound
Reason: Pure quantifier-binding fix to the theorem statement, fully internal to the ASN.

## Issue 6: ℓ_sup ≠ ℓ_old in E2 needs the post-step-1 state
Reason: Pure proof-reorganization fix. Both L11a (ASN-0043) and SequentialTransitionAxiom (ASN-0047) are already cited in the ASN; the fix only reorders the argument to lead with the cleaner L11a path.

## Issue 7: Appendix conflates concepts deferred to future ASNs
Reason: Editorial choice between cutting the appendix or adding caveats that reference the Open Questions section already present. No external input needed.

## Issue 8: Element-field length preservation under inc(·, 0) is glossed
Reason: Pure citation fix. TA5-SigValid (ASN-0034) is already invoked nearby in the same proof; the fix just makes its application to the field-decomposition argument explicit.
