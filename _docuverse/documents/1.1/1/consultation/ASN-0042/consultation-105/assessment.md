# Channel Assignment — ASN-0042 review-105

**Date:** 2026-05-30 03:32

## Issue 1: O1a mislabeled as "AccountPrefix" in the Delegation section
Reason: Pure label correction — the ASN already names O1a "AccountOwnershipBoundary" and AccountPrefix is a distinct lemma defined elsewhere in the same document. No design intent or implementation evidence is needed.

## Issue 2: `pfx(π)` axiom introduction enumerates downstream consumers
Reason: Editorial trim — the codomain constraint is already stated in the contract's postcondition (b); removing the consumer inventory is a prose-structure fix derivable from the ASN.

## Issue 3: Rationale prose around the O5 axiom
Reason: Editorial removal of a self-explanatory gloss; the quantifier scope and its bootstrap exclusion are already legible from the formal statement. No external channel needed.

## Issue 4: Repeated motif "refinement-only regime of O3 and irrevocability of O8"
Reason: De-duplication of an internal cross-section restatement — consolidating to one site at O8 is a structural edit derivable from the ASN's own content.

## Issue 5: Defensive exhaustiveness claim in O10(a) entailment
Reason: Deletion of a reassurance sentence that adds no reasoning; the biconditional already quantifies over all principals. Internal.

## Issue 6: Forward/backward deferral accretion
Reason: Reorganization of where O1a is proved and how worked-example milestones are ordered — both are internal structural decisions resolvable from the ASN's existing proofs.

## Issue 7: O7(c) per-state-obligation prose duplicated
Reason: De-duplication between proof body and Formal Contract; the load-bearing statement and its proof both already exist in the ASN, so the fix is purely editorial.

## Issue 8: Foundation-notation rename `s.B → Σ.B`
Reason: The fix is a notational-justification choice (retain `s.B` or state `Σ.B` as the projection of ownership state onto ASN-0040's registry component); both options are derivable from the ASN's own state model without consulting design intent or implementation.
