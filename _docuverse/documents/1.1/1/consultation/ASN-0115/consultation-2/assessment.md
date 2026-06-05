# Channel Assignment — ASN-0115 review-2

**Date:** 2026-06-05 05:48

## Issue 1: V-spec definition admits subspace-straddling spans, contradicting R10
Reason: The math (an `actionPoint(ℓ)=1` span straddling `s_C`→`s_L`) is internal, but choosing between "tighten V-spec to ordinal-level" and "confront straddling here" depends on whether RETRIEVEV's spec-set was designed to admit only ordinal/deepest-action spans (Nelson) and whether the implementation actually constrains the spans it resolves (Gregory).
Nelson question: Was RETRIEVEV's spec-set intended to designate only ordinal, deepest-action-point spans (one position per deepest digit), or may a single span name a coarser tumbler range that spans a subspace boundary?
Gregory question: Do the spans fed into `specset2ispanset` carry a deepest-level action point (ordinal spans), or can the resolution chain receive a non-ordinal span whose interval crosses from the content subspace into the link subspace?

## Issue 2: R7 proof invokes store monotonicity for two states it treats as unordered
Reason: The fix is fully derivable from the ASN's own substrate — invoke ASN-0047 SequentialTransitionAxiom to pick a direction WLOG, or argue from global content/link immutability using S3★ to place `a` in both stores. No external evidence or design intent is required.
