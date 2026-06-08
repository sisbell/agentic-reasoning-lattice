# Channel Assignment — ASN-0112 review-16

**Date:** 2026-06-08 08:47

## Issue 1: "level-uniform" conflated with "endpoint-level-compatible" in V3 and V6
Reason: The fix is purely a precision correction over the note's own definitions (S6 level-uniform `#s=#ℓ` vs endpoint-level-compatible `#start=#reach`), and the note already contains the counterexample (the `m_C=3>m_L=2` variant giving `extent_d=[1,2,0]` level-uniform) that settles the corrected conditions. No design intent or implementation evidence is needed — only internal consistency.

## Issue 2: single-span structural impossibility stated twice (anti-bloat)
Reason: Pure anti-bloat de-duplication of the note's own prose — collapse the V6-closing essay and V7 restatement into a single statement. No external channel bears on which sentence survives.
