# Channel Assignment — ASN-0130 review-4

**Date:** 2026-06-12 09:56

## Issue 1: The discipline-scope list omits PR-SIG, PR3, and PR3a, which consume discipline-dependent facts without carrying the qualifier
Reason: The fix is internal scope bookkeeping — the dependency chain the reviewer traces (PR-SIG's induction consuming PR0 (iv), PR3 routing through PR1/PR2(a), PR3a inheriting both) is already established by the note's own text, and the repair is to propagate the registration-discipline qualifier the note already defines. Neither design intent nor implementation behavior bears on which formal claims need an existing qualifier attached.

## Issue 2: "expand(a) ∈ ST" is undefined for parameterized expansions — PD0's classes are stated for state-predicates, and the certified object has free parameters
Reason: The fix is a definitional stipulation mirroring the note's own PR-VIEW well-posedness move: run PD0's rules with parameters as bound constants of their declared sorts, and read the certificate as asserting ⊤-stability of every `Γ_D`-instantiation — a reading already forced by PS2's shape (G = ∅ leaves no slot to record arguments, so the certificate cannot be per-instance). PD0/ST is an ASN-0129 construct with no counterpart in Nelson's writings or the udanax-green code, so neither channel can speak to it; adequacy is checkable against the PD0 rule families the note already summarizes, including the worked example's `t`.
