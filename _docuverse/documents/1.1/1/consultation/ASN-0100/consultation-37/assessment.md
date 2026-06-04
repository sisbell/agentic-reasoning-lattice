# Channel Assignment — ASN-0100 review-37

**Date:** 2026-06-04 13:02

## Issue 1: The I3-disclaimer subsection is meta-prose about a foreign ASN's siblings
Reason: Internal. The fix is a pure prose collapse — the set of cited vs. disclaimed I3 clauses is already enumerated in the ASN; no design intent or implementation evidence is needed to drop the per-clause failure derivations.

## Issue 2: The cross-composite reordering refutation imagines a case the precondition excludes
Reason: Internal. INS.pre already states composite atomicity makes intermediates non-observable; the refutation contradicts the ASN's own precondition, so the fix is derivable from the ASN's existing content.

## Issue 3: Repeated deferral to the same downstream location
Reason: Internal. Reorganizing forward pointers (inline the short result or cite the claim label once) is an editorial restructuring with no semantic question for either channel.

## Issue 4: Use-site inventory attached to a lemma
Reason: Internal. Deleting the use-site sentence leaves INS.chain-shift's statement and proof intact; no external input required.

## Issue 5: wp subsection mislabels the postcondition
Reason: Internal. The body already computes `wp(INSERT, (a,d) ∈ R')` and the actual P4★ definition (`Contains_C(Σ) ⊆ R`) is stated in the ASN; renaming the heading to match the computed postcondition is derivable from existing content.
