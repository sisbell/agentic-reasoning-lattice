# Channel Assignment — ASN-0036 review-198

**Date:** 2026-05-30 00:11

## Issue 1: S5 treats transition invariants S0/S1 as state predicates, and the rescue is misjustified
Reason: Fix is internal — the ASN already defines S0/S1 as transition-level invariants and S2/S3 as state predicates, so option (a) (restate S5 as demonstrating only that state-level S2/S3 admit unbounded multiplicity, and replace "vacuously") is derivable from the ASN's own definitions without external evidence or intent.

## Issue 2: S7b carries "why the axiom is needed" prose in an axiom slot
Reason: Fix is purely editorial anti-bloat — drop the container/content rationale sentence and keep only the `zeros(a) = 3` axiom and the T4 field-correspondence consequence already present in the ASN; no design intent or implementation evidence is needed.
