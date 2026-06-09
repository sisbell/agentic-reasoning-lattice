# Channel Assignment — ASN-0121 review-22

**Date:** 2026-06-09 02:36

## Issue 1: FL-WP's case partition is not exhaustive over fresh links in the full vocabulary
Reason: The fix re-cuts the case partition on `L_R^{Σ'}` membership and corrects the from-slot lift — both follow mechanically from definitions already in the ASN (the slot-3 retraction-class test, `L_R`'s triple-restriction, and FL-DEF's `sat`). No design intent or implementation evidence is at stake; the corrected wp forms are derivable from the ASN's own content plus the cited ASN-0086 facts.

## Issue 2: FL-WP — the load-bearing hazards are derived but never exercised concretely
Reason: Adding worked traces for the ghost-pre-coverage and self-retraction terms only instantiates the existing FL-WP derivation against the existing concrete store; all machinery (ghost addresses, retraction tuples, `coverage`) is already specified. Purely internal construction, no channel needed.
