# Channel Assignment — ASN-0121 review-8

**Date:** 2026-06-09 01:41

## Issue 1: The worked example never exercises the residence axis — FL-RES has no concrete witness
Reason: The fix only adds a trace built from machinery already in the ASN — FL-DEF, `athome`/`liftH`, PrefixSpanCoverage (ASN-0043), and T5 (ASN-0034) — plus the given store. No design-intent question is open (FL-RES is already stated) and no new implementation evidence is needed (the Q12 divergence is already documented); the witness is a mechanical construction.

## Issue 2: FL-STB's precondition is redundant by the ASN's own argument
Reason: The redundancy is established entirely by the ASN's own monotonicity discussion (`nullified` is a function of `Σ.L` alone, so `Σ'.L = Σ.L` entails `nullified(Σ') = nullified(Σ)`); restating the hypothesis is a purely internal logical simplification.
