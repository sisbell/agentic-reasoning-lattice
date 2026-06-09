# Channel Assignment — ASN-0126 review-5

**Date:** 2026-06-08 21:32

## Issue 1: "Binary" registration does not entail the unit-depth retraction discipline
Reason: Derivable internally — the note's own Binary definition (`|F|=1 ∧ |G|=1`, no depth constraint) versus ASN-0086's Nullify construction (`δ(1,#a)`) already shows unit-depth comes from the operation, not the shape; the fix is to recharacterize the overclaim, and the note already cites Gregory's "single (stream, width) span" evidence.

## Issue 2: `K.λ_sh` has no arity precondition, but `Sh-conf` is defined only on triples
Reason: Pure formal fix derivable from the ASN — `Sh-conf(K, F, G)` reads two content slots and the Single-source section already routes higher arity to direct link-store interaction, so adding a `|value| = 3` precondition (or `⊥` on non-triples) follows from the note's own commitments.

## Issue 3: The disciplined-domain wp simplification relies on layer-reachability that `→_sh` does not establish
Reason: Internal — the gap between `→_sh`-reachability and ASN-0086 layer-reachability is a formal property of the note's own projection argument `π`, and the fix (conditionalize the simplification, or chain it on Issue 1's unit-depth fix) is derivable without external evidence.
