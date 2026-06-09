# Channel Assignment — ASN-0121 review-22

**Date:** 2026-06-09 02:36

## Issue 1: FL-WP's case partition is not exhaustive over fresh links in the full vocabulary
Reason: The fix is a logical re-cut of the case partition on `L_R^{Σ'}` membership (using ASN-0086's already-cited triple-restriction) and a generalization of `lift(∅, q.F)` to `lift(F_b, q.F)`; the ASN's own stance — working over the full ASN-0047 vocabulary with no retraction discipline — already forces these corrections, so the fix is derivable internally.

## Issue 2: FL-WP — the load-bearing hazards are derived but never exercised concretely
Reason: The required trace instantiates FL-WP's already-derived ghost-pre-coverage and self-retraction terms against the ASN's own concrete store; no design intent or implementation evidence is needed, only an internal worked instance.
