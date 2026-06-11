# Channel Assignment — ASN-0128 review-20

**Date:** 2026-06-11 05:04

## Issue 1: "no query could select" in I0 is a multi-step claim argued from an incomplete inventory
Reason: The fix is internal — the closing argument the review sketches ((a) `|F| = 1` forces single-span F, and two single spans with equal coverage are the same span by span arithmetic; (b) Binary's `|G| = 1` likewise; (c) Multi G-slots are consulted only in aggregate by `targets_of`) uses only facts already committed in the ASN (the gate via RP, AM's matching rule, D3's union) and span definitions from the cited dependencies. No design-intent or implementation question remains open.

## Issue 2: "surface-emitted" and SD are derivation properties phrased as state predicates, where the foundation already supplies the correct idiom
Reason: The fix is internal — it is a reformalization instantiating ASN-0086's RelationalLayer/LayerReachable step-classification idiom, which the review identifies precisely; the proofs (I1a's induction, DR's per-tuple deposit-time reasoning) already operate over derivations, so restating the hypotheses there requires no new evidence or intent.

## Issue 3: the idem=⊥ half of the exposed surface has no consolidated postcondition or wp
Reason: The fix is internal — the idem=⊥ wp is I6's formula with `hit ≡ ⊥`, derivable mechanically from the existing I5/I6 content, plus a citation update in "The operation set."

## Issue 4: the Φ-grounding is stated in full twice (anti-bloat)
Reason: The fix is internal — it is an editorial consolidation assigning ownership of the Φ-nonemptiness and coincidence analysis to BH1's Rewrite scope and reducing View selection to a citation; no semantic content changes.
