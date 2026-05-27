# Channel Assignment — ASN-0099 review-19

**Date:** 2026-05-26 22:02

## Issue 1: A1's discharge is informal, not substrate-derived
Reason: Choosing among the three offered fixes (substrate amendment vs. explicit hypothesis vs. weakening F9) depends on whether A1 holds as a binding design axiom and as a structurally-enforced implementation property. Both authorities are needed to assess strength of the existing informal grounding.
Nelson question: Is reservation of link allocation to MAKELINK an architectural axiom of the design — such that K.μ⁺, K.μ⁻, and K.ρ are constitutionally forbidden from allocating links — or is it a convention that happens to hold but isn't axiomatic, leaving the substrate spec free to allow incidental link allocation by non-allocating operations?
Gregory question: In udanax-green, is the invariant "only CREATELINK writes LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN records" structurally enforced (e.g., by code architecture, access patterns, or module boundaries that make non-CREATELINK writes impossible), or merely a behavioral convention that no current routine violates?

## Issue 2: F12 mislabeled in claims table

## Issue 3: Empty scope boundary not surfaced alongside other empty cases

## Issue 4: Multi-step survivability lemmas lack worked-example coverage

## Issue 5: F4's first witness uses `α.0` as a coverage point — non-T4 tumblers in coverage need explicit acknowledgment

## Issue 6: Worked example's depth-2 V-position for link subspace introduces a state inconsistency

## Issue 7: Filtered + scoped composition not formally addressed
