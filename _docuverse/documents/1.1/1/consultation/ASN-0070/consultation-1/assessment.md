# Channel Assignment — ASN-0070 review-1

**Date:** 2026-05-25 04:25

## Issue 1: Result form cannot accommodate cross-subspace R values
Reason: The fix depends on whether endsets crossing content and link subspaces are an intended design case or an edge to restrict. Nelson informs the design stance; Gregory shows what the implementation does.
Nelson question: Did the design contemplate endsets whose coverage spans both content and link subspaces, and was FOLLOWLINK expected to return cross-subspace results?
Gregory question: Does udanax-green permit endsets with coverage in both content and link subspaces, and if so what representation does the follow-equivalent operation return?

## Issue 2: F-det proof relies on canonical form, but operation does not commit to canonical form
Reason: The choice between representation-determinism and denotation-determinism is partly informed by what the implementation actually returns. Gregory's evidence helps decide whether the operation should commit to canonical form.
Gregory question: Does the udanax-green follow-equivalent operation normalize its result to a canonical span-set form, or return whatever decomposition the computation produces?

## Issue 3: No concrete worked example
Reason: The example is fully derivable from definitions already in the ASN and the cited foundations. Internal.

## Issue 4: Claims lack formal contract structure
Reason: Reformatting existing claims into the foundation-convention contract blocks is a presentational change requiring no external evidence. Internal.

## Issue 5: Missing proof that I(β) ∩ ⟦σ⟧ yields a contiguous arithmetic sub-progression
Reason: The proof sketch is supplied in the review itself and uses only TS5 and T12, both already cited. Internal.

## Issue 6: F-sound and F-complete proofs are tautological restatements
Reason: This is a framing decision — either drop them as restatements or reframe as implementation obligations against the decomposition computation. Internal.

## Issue 7: Missing weakest precondition analysis
Reason: The wp computation reduces to checking that the stated preconditions plus reachable-state invariants (already cited from ASN-0047) suffice. Internal.

## Issue 8: F-det requires explicit canonical form definition for multi-subspace results
Reason: Resolution depends on Issue 1's outcome. If multi-subspace is admitted, the canonical ordering choice could be informed by what the implementation uses.
Gregory question: If udanax-green's follow-equivalent returns results spanning multiple subspaces, in what order are the per-subspace components emitted?

## Issue 9: Origin terminology applied to link addresses without grounding
Reason: The fix is to invoke `home(a)` from ASN-0043 or note the structural equivalence with S7's `origin`. Both ASNs are already cited. Internal.

## Issue 10: Slot uniformity claim (F8) does not address L3's e₃ asymmetry
Reason: The L3 constraint (`e₃ ≠ ∅`) is in ASN-0043, already cited. The fix is just to state the asymmetric well-formedness explicitly. Internal.

## Issue 11: F11 (state-dependence) is not formalized as a property of follow
Reason: Either restating F11 as a corollary of L12 + statelessness or dropping it is a formalization choice using already-cited claims. Internal.

## Issue 12: "Essentially forced" claim about span-set representation is unjustified
Reason: The fix is to weaken the language or supply a stated constraint. Gregory could confirm whether span-sets are the implementation's chosen representation, which would support framing it as a convention informed by practice.
Gregory question: What concrete data structure does the udanax-green follow-equivalent operation use to represent its V-position result?

## Issue 13: F-multi proof too brief
Reason: The expansion uses only set-theoretic identity plus S5 from ASN-0036, already cited. Internal.
