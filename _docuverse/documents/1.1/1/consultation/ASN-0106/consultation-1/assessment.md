# Channel Assignment — ASN-0106 review-1

**Date:** 2026-06-04 19:15

## Issue 1: R0 contradicts R-SPLIT — the full extent is not one block per subspace
Reason: Resolving this requires knowing what the canonical operation actually returns at full extent — a per-subspace V-width count or a fragmented block decomposition. That return shape turns on both Nelson's design intent (his "number of characters/links" gloss) and Gregory's evidence on what the operation emits, neither fully settled by the ASN's own machinery.
Nelson question: Was RETRIEVEDOCVSPANSET intended to report a document's extent as two summary counts (text-width and link-width), or as a full structural decomposition of its arrangement?
Gregory question: For a full-extent document read, does the operation return two V-width spans (the character and link counts) or a fragmented list of mapping blocks reflecting I-discontinuities?

## Issue 2: R-GAP assumes V-order but `read` is defined in request order
Reason: The fix is internal — R-ORDER already establishes that V-order requires normalized `Σ`, so attaching that same precondition to R-GAP (or restating it over the V-ordered view) is derivable from the ASN's own claims.

## Issue 3: the `read(d, Σ)` definition omits the preconditions its own machinery requires
Reason: The needed preconditions (single-subspace, level-uniform) are already cited from ASN-0058 C1a and restated in R-FID; moving them to the definition is a purely internal reorganization.

## Issue 4: R-CORR's derivation invokes M14a on the wrong case
Reason: The fix is internal proof restructuring — splitting into the within-span case (M14a forbids merge) and the cross-span case (no merge attempted), using ASN-0058 machinery already cited in the ASN.

## Issue 5: R-EMPTY conflates an ill-formed designation with an inactive-but-well-formed one
Reason: The conceptual split is derivable from ASN-0053 S2 (no well-formed span denotes ∅) and the restriction operator already in the ASN; modeling the ill-formed case as a rejected precondition violation and the well-formed-but-absent case via the empty restriction needs no external evidence.
