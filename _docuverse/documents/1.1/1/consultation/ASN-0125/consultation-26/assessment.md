# Channel Assignment — ASN-0125 review-26

**Date:** 2026-06-13 17:10

## Issue 1: DC's `[K_sup]` trigger and EL7(vi) ignore claim arity
Reason: Internal. The fix reconciles DC's slot-3-coverage trigger with the claim definition already imported into the ASN — Df-CLS sets `S^Σ := L_{K_sup}^Σ`, and the `L_K^Σ` slice stated in "The substrate we build on" carries `|Σ.L(b)| = 3` exactly, while Df-DISC(ii) constrains only members of that slice. Choosing between tightening DC's trigger to `|ℓ'| = 3 ∧ coverage = K_sup ⟹ schema` and splitting EL7(vi)'s case uses only these existing definitions and EL7's own proof; the arity bound on claims, the scope of edit-discipline, and L3's `N ≥ 3` admission are all already in the note, so no design intent or implementation evidence is needed.

## Issue 2: motivational restatement and forward-reference meta-prose
Reason: Internal. This is a pure prose-economy trim — the reviewer has already named the load-bearing sharpening to retain in EL1 and the factual clause to keep in EL7(ii) — requiring no design intent or implementation evidence, only removal of non-advancing interpretation.
