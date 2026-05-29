# Channel Assignment — ASN-0036 review-117

**Date:** 2026-05-28 20:54

## Issue 1: S8a dependency contradiction between proof and table
Reason: Internal consistency fix — the proof and contract already disclaim T4; the table just needs to match. Resolvable from the ASN's own dependency reasoning without external evidence.

## Issue 2: "axiomatic state component, not a derived property" rationale paragraphs
Reason: Pure prose cut — the Nelson quote and Formal Contract already carry the content; removing motivation essay needs no design intent or implementation evidence.

## Issue 3: "Persistence independence" section is meta-commentary with no new content
Reason: Collapse/fold of redundant prose that re-argues what S0 already states; entirely internal to the ASN's existing logic.

## Issue 4: subspace-identifier-as-structural-context restated repeatedly
Reason: Deduplication — the mechanism is proved once in OrdAddHom; consolidating restatements is internal editing.

## Issue 5: S8-depth explanatory paragraph re-derives proven facts inline
Reason: The re-derivation duplicates ShiftPreservation/OrdShiftHom already in the ASN; reducing to a pointer is internal.

## Issue 6: essay flourish and archaeology in S1's proof region
Reason: Dropping the "four decades" flourish is editorial. The refcount/subtreefree evidence is already present and cited; trimming it to one sentence requires no new implementation lookup.

## Issue 7: repeated deferral of link-subspace to a future ASN
Reason: Removing duplicate deferrals to the same downstream location is a structural edit internal to the ASN.

## Issue 8: S8 "Corollary" restates ShiftPreservation
Reason: Collapsing triplicate statements of one preservation result into a citation-plus-aggregation is internal deduplication.
