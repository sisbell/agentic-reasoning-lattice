# Channel Assignment — ASN-0036 review-164

**Date:** 2026-05-29 04:31

## Issue 1: S8a is a tautological restatement of the domain-restriction axiom
Reason: Fix is internal — `zeros(v) = 0` over the ℕ-carrier is definitionally equivalent to componentwise positivity (per T4's definition of `zeros`, already cited in the ASN). Collapsing the proof block or folding positivity into the axiom note requires no design intent or implementation evidence.

## Issue 2: S5 restates its own formal claim in prose
Reason: Fix is internal — deleting a redundant prose sentence that duplicates the formal property line above it. No external input needed.

## Issue 3: S7d carries document-lifecycle detail S7 does not consume
Reason: Fix is internal — the ASN's own S7 proof shows it consumes only "distinct documents have distinct `zeros = 2` tumblers via GlobalUniqueness," so trimming the owning-user-prefix clause is determined by the dependency structure already present in the text.
