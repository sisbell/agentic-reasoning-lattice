# Revision Categorization — ASN-0048 review-1

**Date:** 2026-03-18 11:47

## Issue 1: I0 provides ordering but I7(d) requires contiguity
Category: INTERNAL
Reason: Contiguity is derivable from T10a (AllocatorDiscipline) and TA5(c) already established in ASN-0034. The reviewer provides the full derivation chain; the fix is adding an explicit clause or derivation using existing properties.

## Issue 2: S8-depth preservation assumes what the precondition does not guarantee
Category: INTERNAL
Reason: The fix is either adding a depth-compatibility clause to I-pre or explicitly invoking TA7a's ordinal-only formulation (uniform depth 1), both already established in ASN-0034. No external evidence needed.

## Issue 3: Subspace ordering claim in I5 is backwards
Category: INTERNAL
Reason: The shared vocabulary's subspace assignments (text=1, links=0) and T1 ordering are already established in the spec. The formal property I5 is correct; only the supporting prose contains a factual error that can be corrected or removed from existing definitions.

## Issue 4: No concrete worked example
Category: INTERNAL
Reason: A worked example is constructed entirely from the ASN's own definitions (I0, σ, I-post, I7). The reviewer even provides a complete scenario; no design intent or implementation evidence is needed.

## Issue 5: I9 R-recovery cites J1' but relies on P7
Category: INTERNAL
Reason: P7 (ProvenanceGrounding) is established in ASN-0047 and is the correct citation for the contrapositive argument. This is a citation correction using an existing property.

## Issue 6: Weakest-precondition analysis is only trivial
Category: INTERNAL
Reason: The non-trivial wp(INSERT, S3) is derivable from the ASN's own phase structure — Phase 1 precedes Phase 3, and frame conditions keep C stable across Phases 2–4. All required reasoning is present in the ASN.
