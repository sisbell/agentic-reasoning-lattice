# Channel Assignment — ASN-0108 review-44

**Date:** 2026-06-13 07:05

## Issue 1: W5's no-skip guarantee is headlined over a two-state condition but proved only over a whole-pass one
Reason: Internal — the correct scope (links that *remain* matching until a window can reach them, under an explicit termination hypothesis) is already stated in W9b and proved in W5's own body; the fix only aligns the headline with reasoning the note already contains.

## Issue 2: the matched-content key is defined as "least covered I-address" but referred to as "matched content's I-address," which breaks the permanence the proofs rely on
Reason: Internal — the key introduction already defines the key as the "least covered I-address read from the immutable endset" and argues why the fixed selection (not the currently-matched endpoint) is necessary for state-stability; the fix is terminological consistency with that definition across W6/W8/W9b.

## Issue 3: W8 disclaims two always-true conditions (defensive over-listing)
Reason: Internal — both vacuous disclaimers reduce to facts the note already relies on: address persistence (the W8 walk itself cites LP13/T8 for the cursor address persisting in `dom(Σ'.L)`) and unique permanent addresses (presupposed by W0/W1's injectivity of the address key, and stated in W6a's "addresses are never reused"); dropping non-load-bearing prose needs no external evidence.

## Issue 4: the W6 caveat reopens by restating the within-home-document scope already in W6's body
Reason: Internal — both the within-document scope (W6 body) and the cross-document consequence (the caveat's second half) are already present; the fix is purely editorial restructuring to remove the restatement.
