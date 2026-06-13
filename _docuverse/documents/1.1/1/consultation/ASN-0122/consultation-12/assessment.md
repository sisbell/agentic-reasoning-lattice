# Channel Assignment — ASN-0122 review-12

**Date:** 2026-06-13 10:52

## Issue 1: X5's "none of the four is redundant" is false for P, Q and unproven
Reason: Internal. The error is purely logical and self-contained: `res_Σ|P` is by definition a function with domain `P`, so `P = dom(res_Σ|P)` and `Q = dom(res_Σ|Q)` are recoverable — a fact derivable from the ASN's own definition of `res` and standard function restriction. The note even contradicts its own Claims-Introduced table ("the two restrictions"), so the fix is to align prose with the table; no design intent or implementation evidence bears on it.

## Issue 2: X6(c) parenthetical recaps X6(b)'s premise rather than adding reasoning
Reason: Internal. This is an anti-bloat deletion — the parenthetical re-states X6(b)'s already-discharged "interleaved intermediate edits" premise, verifiable by reading the two passages against each other. No external channel needed.

## Issue 3: meta-signpost in the region definition
Reason: Internal. Pure editorial deletion of an announcing sentence; the clipping rationale and the `σ = ([1,5], [3])` example that follow stand on their own. No channel needed.
