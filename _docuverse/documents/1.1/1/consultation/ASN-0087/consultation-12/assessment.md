# Channel Assignment — ASN-0087 review-12

**Date:** 2026-05-26 15:09

## Issue 1: Weakest precondition statements omit document-membership precondition
Reason: The fix is derivable from the ASN's own content. ASN-0098's definition of `discoverable_from` already requires `d ∈ dom(Σ.M)`, and MAKELINK's frame on `dom(M)` is stated in M-Frame. Adding the conjunct is a formal correction, not a question about design intent or implementation.

## Issue 2: "Caller knowledge" framing in Reflexive Endsets misrepresents substrate behavior
Reason: The fix is internal — both the determinism of `A_L(d)`'s next emission (from ASN-0093) and the structural defense via standard authoring are already established in this ASN. The required change is reordering and demoting the caller-knowledge framing; no external evidence is needed.

## Issue 3: Bidirectional coupling between dom(M) and E_doc is a framework reconciliation done within an operation ASN
Reason: This is a scoping/editorial decision about where framework-reconciliation work belongs, not a question about design intent or implementation. The required fix (cite a reconciliation source or qualify analysis as modulo a future reconciliation) is derivable from the project's ASN organization principles already invoked in the review.

## Issue 4: L1c uniqueness derivation is correct but unnecessarily dense
Reason: The fix is purely presentational — the four prose paragraphs share a tabular structure already implicit in the argument. Reformatting to a table or compact corollary requires no new content from Nelson or Gregory.
