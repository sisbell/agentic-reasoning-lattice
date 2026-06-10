# Channel Assignment — ASN-0115 review-44

**Date:** 2026-06-10 03:39

## Issue 1: R7 proof omits the operative sub-case of the non-empty-restriction branch
Reason: The fix is a mechanical proof completion — adding the fails-branch consequence using the `act` override definition, depth-compatibility, and S8-depth, all already present in the ASN. No design intent or implementation evidence bears on whether the override forces `act = ∅` identically at both states; it follows from the ASN's own definitions.

## Issue 2: R8 restates the non-disclosure conclusion and adds out-of-scope positioning
Reason: The fix is purely subtractive prose-trimming — drop the R0/R1 restatement and the cross-operation positioning sentence, keep the per-position-resolution observation. What remains is already grounded in R0/R1/R4 within the ASN; removing the redundant and out-of-scope material needs no external channel.

## Issue 3: pure-query purity stated four ways with a component inventory
Reason: The fix is editorial condensation of five overlapping purity statements into one, with the collapsed form already supplied in the Required note. No design intent or implementation evidence is at stake — RETRIEVEV's purity is fixed by the ASN's own `deliver`-is-a-function-of-state framing.
