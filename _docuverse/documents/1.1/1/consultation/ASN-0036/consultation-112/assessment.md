# Channel Assignment — ASN-0036 review-112

**Date:** 2026-05-28 20:07

## Issue 1: Citation-bookkeeping meta-prose in the S8 existence proof
Reason: Pure editorial deletion of housekeeping prose; no design intent or implementation evidence needed — the cut is justified by the ASN's own structure (Non-canonicality remark and run-corollary preconditions already carry the distinction).

## Issue 2: Derivation-route justification in the S1 discussion
Reason: The fix trims counterfactual prose to the load-bearing fact, all of which is internal to the ASN — S1 is already proved as the domain conjunct of S0 and the T8 specialization is stated in the surrounding text.

## Issue 3: Repeated deferral to the "Persistence independence" section
Reason: Consolidating three identical cross-pointers into one statement is an internal editing decision; the fact (S0 forbids reclamation, orphans persist) is already established in the ASN.

## Issue 4: S7 section preamble explains why downstream citations are made
Reason: Choosing between inlining the justification or deleting the preamble plus back-pointers is an internal restructuring; the dependency content (S0 fixes components) is already present in the ASN.

## Issue 5: S7a forward-references S7b, which is stated afterward
Reason: Reordering S7b before S7a (or merging the domain restriction) is a purely structural rearrangement of existing axioms; no external input needed.

## Issue 6: Definition contracts assert postconditions established only by downstream lemmas
Reason: Dropping the duplicated postcondition (c) is internal — OrdShiftHom (b) and ShiftPreservation (iv) already state the same fact within the ASN.

## Issue 7: S8-depth dependency list disagrees with itself
Reason: Reconciling the contract and the table is derivable from the ASN's own prose — the surrounding text invokes OrdinalShift/TumblerAdd to define "consecutive positions," so the contract should be corrected to match, but this is internal to the document.
