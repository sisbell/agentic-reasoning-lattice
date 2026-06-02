# Channel Assignment — ASN-0098 review-42

**Date:** 2026-06-02 14:58

## Issue 1: LP11 is a composite-level lemma but the completeness claim treats it as per-step atomic
Reason: The fix is a structural reclassification: classify LP11 as composite-level and state that K.μ~ in a sequence is analysed via its K.μ⁻+K.μ⁺ decomposition with LP11 supplying the net effect. The decomposition fact (K.μ~ = K.μ⁻ + K.μ⁺) is already quoted from ASN-0047 in the finding, and the LP11 proof via the bijection is already present — no channel needed.

## Issue 2: LP12a labels a postcondition pullback as "the weakest precondition" but omits K.μ⁻ enabledness
Reason: K.μ⁻'s applicability conditions (`d ∈ E_doc`, `dom(M(d)) ≠ ∅`, strict-shrink, valid D-SEQ★ prefix) are already referenced in the ASN and listed in the finding; the fix is to conjoin enabledness into the wp or reframe as a pullback under an explicit enabledness hypothesis. Pure logic correction, derivable internally.

## Issue 3: `project` definition carries defensive rationale for its own convention
Reason: Pure editorial trim — delete the justification clause and keep the convention. Internal.

## Issue 4: LP8 carries a use-site inventory and a claim-consolidation justification
Reason: Pure editorial trim — remove the consolidation defense and collapse the K.δ routing to a single clause if load-bearing. Internal.

## Issue 5: LP12a restates its result a second way and then declares the forms interchangeable
Reason: Pure editorial trim — keep one form, delete the restatement and interchangeability note. Internal.

## Issue 6: the link-canonical class is deferred to future work in two separate locations
Reason: Pure editorial trim — keep the deferral in Open Questions, strip the duplicate from the LP12b table entry, and tighten the LP-Fin intro. Internal.
