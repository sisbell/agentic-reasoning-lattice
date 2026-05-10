# Revision Categorization — ASN-0006 review-3

**Date:** 2026-03-06 22:20

## Issue 1: Ordering of copied addresses not established
Category: INTERNAL
Reason: The ASN's prose and concrete trace already assume order preservation; the fix is to strengthen the formal set equality to a pointwise mapping consistent with what the ASN already describes.

## Issue 2: TC8 derivation from TC7 is unsound
Category: INTERNAL
Reason: This is a logical error in the derivation — TC7 quantifies over text_subspace but is applied to link positions. The fix (broaden TC7 or state TC8 independently) is derivable from the ASN's own definitions.

## Issue 3: AX1 claims universality but verifies only four operations
Category: GREGORY
Reason: The key question is whether MAKELINK modifies POOMs of multiple documents (e.g., registering link ISAs in each endpoint document's link subspace), which would falsify AX1. This requires implementation evidence.
Gregory question: Does MAKELINK modify the POOM of more than one document — specifically, does it register link ISAs in the link subspace of each document whose content appears in the link's endsets, or only in a single document's POOM?

## Issue 4: Frame conditions omit the links set
Category: INTERNAL
Reason: COPY clearly does not create or modify links; the fix is to add the missing `links' = links` frame condition, which is implied by the ASN's own description of COPY's effects.

## Issue 5: Concrete trace addresses violate Element subspace encoding
Category: INTERNAL
Reason: The ASN defines the encoding rule ("Element field's first component identifies its subspace") and the trace just needs to be made consistent with it — either by using multi-component Element addresses or noting the simplification.

## Issue 6: TC11 is a restatement of the definition, not a derived property
Category: INTERNAL
Reason: The fix is to restate TC11 as the non-trivial derived property (COPY causes links to become discoverable through the target), combining TC1 with the existing definition of discoverable_links. All needed material is in the ASN.

## Issue 7: Source specification inconsistency
Category: GREGORY
Reason: TC3 describes COPY as operating on a multi-document specset while all other formal properties use a single source_span from a single source_doc. Resolving the inconsistency requires knowing whether the implementation's COPY primitive accepts multi-document specsets or only single-span sources.
Gregory question: Does the COPY implementation accept a multi-document, multi-span specset as its source argument, or does it operate on a single contiguous V-span from a single source document (with multi-span COPY being a caller-level composition)?

## Issue 8: Missing TC12
Category: INTERNAL
Reason: This is a purely editorial numbering gap; the fix is to renumber or add a note, requiring no external consultation.
