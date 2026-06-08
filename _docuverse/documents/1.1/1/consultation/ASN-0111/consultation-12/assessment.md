# Channel Assignment — ASN-0111 review-12

**Date:** 2026-06-07 23:57

## Issue 1: "no reachable state realizes an N = 4 link" contradicts the ASN's own definition of reachable
Reason: The contradiction is internal: the ASN already states both that the abstract `→*`-reachable model admits `N ≥ 3` (L3, ASN-0093's K.λ) and that udanax-green caps at three; resolving it requires only disambiguating the two senses of "reachable" the note itself supplies. Both the abstract admission and the implementation cap (with its enforcement points) are already on the page, so no new design intent or implementation evidence is needed — only a logical/presentational fix to the standing precondition's scope.

## Issue 2: over-broad `subspace_I` universal in the RL8 orphan proof
Reason: The required narrowing — quantify over `t ∈ coverage(·) ∩ dom(Σ.L)`, use L1 for `zeros(t)=3`, then T7 with L0 — is fully derivable from foundation theorems already cited in the note (T4, L0, L1, T7). No channel is needed; only the proof's intermediate quantifier needs restricting.
