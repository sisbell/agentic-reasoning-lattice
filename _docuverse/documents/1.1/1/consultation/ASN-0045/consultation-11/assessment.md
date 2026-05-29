# Channel Assignment — ASN-0045 review-11

**Date:** 2026-05-28 19:35

## Issue 1: The lower bound `0 ≤ zeros(t)` is asserted, not discharged
Reason: Both fix options (state a cited lemma that `zeros` lands in ℕ with `zeros(t) ≥ 0`, or derive `0 ≤ n` for all naturals via well-ordering/induction) operate entirely over the NAT foundation axioms and the cardinality definition already in ASN-0034. This is a proof-theoretic choice about cited foundation content, not design intent or implementation behavior.

## Issue 2: The `3 ≤ zeros(t) ≤ 3 ⟹ zeros(t) = 3` collapse skips antisymmetry
Reason: The required one-line discharge uses NAT-order transitivity and irreflexivity — both already cited and applied elsewhere in this same proof. Fully internal.

## Issue 3: Imprecise foundation citation "T4(i)"
Reason: T4's axiom is stated as `zeros(t) ≤ 3` in ASN-0034 (the cited foundation), and the ASN itself restates this bound throughout. Correcting the citation label to its content is derivable from already-referenced material.
