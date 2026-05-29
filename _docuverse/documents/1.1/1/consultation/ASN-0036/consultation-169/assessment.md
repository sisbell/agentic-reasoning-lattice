# Channel Assignment — ASN-0036 review-169

**Date:** 2026-05-29 05:08

## Issue 1: Revision-history meta-prose in the Properties table
Reason: Pure editorial removal of edit-history meta-prose; the fix is derivable from the ASN alone — delete the note (or renumber S0–S6 contiguously). No design intent or implementation evidence bears on whether a retired-label annotation belongs in the text.

## Issue 2: S4 proof restates a decidability claim already made in prose, and proves a property outside its contract
Reason: Internal structural fix — either drop the decidability sentence or promote it to a postcondition and prove it once. The contract, prose, and proof are all present in the ASN; deciding where the claim lives requires no external channel.

## Issue 3: S7 "Permanence" paragraph invokes S4 for a case the setup already excludes
Reason: The Permanence argument's sufficiency (fixed tumbler via S0 + deterministic origin) is fully established within the ASN; whether the S4 sentence is redundant is judged against the note's own invariant chain, so no channel is needed.
