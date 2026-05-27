# Channel Assignment — ASN-0099 review-6

**Date:** 2026-05-26 17:52

## Issue 1: F4 (PartialOverlapSuffices) uses informal phrasing
Reason: Pure formalization fix — the precise restatement is given in the review itself and is mechanically derivable from F1's existing quantifier form.

## Issue 2: Effect-clause exhaustivity is load-bearing but undocumented
Reason: The convention can be promoted to a named assumption internally, but Gregory can support an alternative derivation path by confirming whether K.μ⁺/K.μ⁻ actually leave the link store untouched in the implementation, which would let us replace the meta-convention with empirical evidence about these operations.
Gregory question: In the udanax-green implementation, do the K.μ⁺ (content extension) and K.μ⁻ (content contraction) code paths ever modify the link store L, or are their state mutations confined strictly to the per-document arrangement M(d)?

## Issue 3: F8 (Determinism) not exercised in the worked example
Reason: Adding a query that exhibits two states agreeing on Σ.L but differing in Σ.M follows the existing example template directly from F8's hypothesis and the definitions already in the ASN.

## Issue 4: Query 4 in worked example inherits the effect-clause exhaustivity gap
Reason: Pure cascade from Issue 2 — once effect-clause exhaustivity is formalized (or replaced by an evidence-based derivation), Query 4 just cites the new foundation.

## Issue 5: F9's "pure K.μ-family sequences" multi-step lift is academic
Reason: The decision to characterize the operational scenario or demote the claim to a structural remark is a content judgment the author can make from the ASN's existing framing of F9 vs. F11; no external evidence sharpens the call.

## Issue 6: Behavior of findlinks_V on R ⊄ dom(Σ.M(d)) is deliberately ambiguous
Reason: The disambiguation depends both on what Nelson's design intent was for out-of-domain V-queries and on how the udanax-green implementation actually behaves — together these inform whether to require rejection, projection, or formalized partiality.
Nelson question: When a reader queries V-positions that lie outside the document's arrangement domain, was FINDLINKS designed to (a) reject the query, (b) silently project onto the in-domain subset, or (c) leave the handling to a higher protocol layer above the abstract operation?
Gregory question: What does the udanax-green implementation do when a FINDLINKS-equivalent query nominates V-positions outside dom(M(d)) — reject with an error, silently filter to in-domain positions, or rely on the caller to pre-validate?
