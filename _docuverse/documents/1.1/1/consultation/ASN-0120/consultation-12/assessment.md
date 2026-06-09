# Channel Assignment — ASN-0120 review-12

**Date:** 2026-06-09 11:44

## Issue 1: Composite validity is asserted but not verified
Reason: Internal — ML10 already establishes `Σ'.C = Σ.C` (no fresh content address, no content-subspace range-new I-address), which is exactly what makes J0/J1★/J1'★ vacuous; the ASN's own claims supply the one-liner.

## Issue 2: V-spec resolution silently excludes ghost/foreign endsets
Reason: The acknowledgment that V-spec resolution confines all endsets to `dom(Σ.C)` is internal (it follows from ML1's proof), but deciding whether ghost-type creation is a legitimately *separate* operation to mark OUT_OF_SCOPE — versus an unhandled expressiveness gap — needs design intent and implementation evidence.
Nelson question: Did the design intend MAKELINK to be the sole link-creation primitive, or did it contemplate a distinct facility for creating type endsets that reference ghost/non-content addresses (L9)?
Gregory question: Does udanax-green provide any link-creation path that accepts direct I-addresses (bypassing V-span resolution), thereby able to record ghost-type or non-content endsets?

## Issue 3: ML7 and ML8 assert the same guarantee
Reason: Internal — the redundancy and the unique survivability content of ML8 are both visible from ML7, ML1, and the ASN's own narrative; folding or restating is an editorial fix requiring no external evidence.

## Issue 4: Open Question 1 is already answered by the ASN's own claims
Reason: Internal — `Endset = 𝒫_fin(Span)` is unordered, L5 supplies no span-positional accessor, and ML2 establishes representation-independence, so within-endset run order is definitionally non-observable from the ASN's own definitions.
