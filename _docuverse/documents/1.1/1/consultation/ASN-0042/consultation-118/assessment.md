# Channel Assignment — ASN-0042 review-118

**Date:** 2026-05-30 04:51

## Issue 1: "Σ.B is an ASN-0040-reachable registry" is load-bearing but never discharged as a named invariant
Reason: The fix is purely internal restructuring — both the base case (O14's bootstrap-registry clause) and the inductive step (O17b restricting changes to `Bop(p,d)` edges) are already present in the ASN, as is ASN-0040's closure over reachable registries. Promoting them to a named invariant reassembles existing content; no design intent or implementation evidence is required.

## Issue 2: O7(c) restates the binding/auto-discharged split three times with a cross-slot deferral
Reason: Editorial deduplication — the (ii)/(iv) auto-discharge is already derived in the proof; the fix removes redundant restatements in the postcondition and Formal Contract. Fully derivable from the ASN's own structure.

## Issue 3: Worked Example closing paragraph re-derives O10's general mechanism instead of checking the concrete instance
Reason: The general Form-A/Form-B argument is already proved in O10's body and the concrete checks already appear above the paragraph; the fix only cuts duplication. Internal editorial.

## Issue 4: OwnershipDomainPermanence opens with generality/motivation meta-prose
Reason: The fix deletes a sentence whose content (general quantification, Nelson's "forevermore" motivation) is already carried by the formula's quantifier and the *Permanence and Refinement* section. Purely internal.

## Issue 5: O8 "Design confirmation" is defensive epistemic prose about what the implementation does *not* establish
Reason: The fix reduces meta-commentary to the already-present, already-Gregory-attributed fact that the implementation provides no revocation path; no new implementation evidence is needed since the `validaccount` stub fact is already stated. Internal trim.
