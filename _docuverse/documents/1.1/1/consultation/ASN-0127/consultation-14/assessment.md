# Channel Assignment — ASN-0127 review-14

**Date:** 2026-06-10 03:18

## Issue 1: D-CWP's "weakest precondition" is written over post-state quantities and omits the R = ∅ boundary — both present in the LP12a it claims to mirror
Reason: Internal — the pre-state bridge `image(W, d_q, Σ') = {Σ.M(d_q)(v) : v ∈ W ∩ R}` restates the retained-domain agreement `Σ'.M(d_q) = Σ.M(d_q) ↾ R` already given in F-IMG-CONTR's own derivation (with `R = dom(Σ'.M(d_q))`), the `R = ∅` specialisation reduces to `findlinks_disc(W, d_q, Σ) = ∅` by F-FIND's `findlinks(∅, Σ) = ∅`, and the LP12a form/enabledness predicate to mirror live in the cited sibling specs (ASN-0098/ASN-0047). No design intent or implementation evidence is at stake.
