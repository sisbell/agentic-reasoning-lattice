# Channel Assignment — ASN-0086 review-66

**Date:** 2026-05-19 14:49

## Issue 1: R6c-Corollary's induction hypothesis is too weak to apply R6c's induction step
Reason: Fix is internal — the corollary's proof needs either IH strengthening or restructuring around the fact that L12 + L12a (already cited in the ASN's BroadExtension paragraph) make A_K pointwise constant across arrangement-modifying steps. No design intent or implementation evidence is needed; the fix is mechanical proof rephrasing using invariants already in scope.

## Issue 2: R0's "(IH)" labels without an explicit outer induction
Reason: Fix is internal — the "(IH)" annotations are a presentation issue about how to refer to L-invariants at the prior state Σ. The substrate-level invariant preservation chain is already implicit in ASN-0043's L-invariants and ASN-0093's substrate machinery; the fix is to either frame R0 as an induction step explicitly or replace each "(IH)" with a direct invariant citation.
