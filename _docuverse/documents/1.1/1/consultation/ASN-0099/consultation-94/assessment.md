# Channel Assignment — ASN-0099 review-94

**Date:** 2026-06-07 22:17

## Issue 1: F4 Strengthening 1 uses an over-engineered witness
Reason: Purely an internal anti-bloat simplification — the minimal one-slot witness is already present in Strengthenings 2/3 of the same ASN, and the disagreement between `coverage ⊆ I` and F1's overlap test is fully derivable from F1, PrefixSpanCoverage, and T0 as already cited. No design intent or implementation evidence is at stake.

## Issue 2: Imprecise "V-extents partition R ∩ dom(Σ.M(d))"
Reason: A precision fix about what ASN-0058's B1/B2 actually deliver (partition of `dom(M(d))`, not of `R ∩ dom(M(d))`); resolvable from the cited claims' own statements within the lattice. No question of designer intent or udanax-green behavior arises.
