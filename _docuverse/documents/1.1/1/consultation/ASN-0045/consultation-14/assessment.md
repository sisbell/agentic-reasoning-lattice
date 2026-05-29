# Channel Assignment — ASN-0045 review-14

**Date:** 2026-05-28 19:50

## Issue 1: "At-least-one" is grounded in the bijection's domain instead of the arithmetic bound — a circular/non-sequitur derivation
Reason: Internal. The required fix re-routes at-least-one through T4's axiom `zeros(t) ≤ 3` and T0's `zeros(t) ∈ ℕ` — both already cited as dependencies in the ASN — to get `zeros(t) ∈ {0,1,2,3}`, then attaches T4c level names. No design intent or implementation evidence is needed; it is a logical re-grounding using facts the ASN already states.

## Issue 2: "At-most-one" and the Depends clauses over-attribute disjointness to T4c's injectivity
Reason: Internal. Disjointness follows from functionality of `zeros(·)` (T4) and distinctness of 0,1,2,3 in ℕ (T0), both already present; the fix is to strike the spurious T4c-injectivity dependence from prose and Depends. This is an internal correction to the proof's attribution, derivable from the ASN's own definitions.
