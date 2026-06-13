# Channel Assignment — ASN-0133 review-2

**Date:** 2026-06-13 10:54

## Issue 1: Q5a does not discharge H-W; it establishes the strictly weaker real-fires bound
Reason: Pure logical-restructuring fix derivable from the note alone — H-W, `W(σ)`, Q5, Q5a, and Q6 are all defined here, the refuting counterexample is built entirely from RG's no-op clause and the `W` definition, and the repair (name "finitely many real fires," route Q6 through it, drop the discharge-H-W claims, fix the "unbounded-work route" wording) follows from the note's own proofs. No design intent or implementation evidence is at stake.

## Issue 2: Scope is defined over addresses, but rule domains can be tuple-valued
Reason: Internal type-correctness fix — the note already applies `addr` to tuple-valued PL arguments (in `T_R` and `Post_R`) and builds QD filters via ASN-0129's filtering former, so specifying the scope restriction as `S(addr(x))` (or a named projection) and confirming it types at `D`'s sort follows from machinery already present. Scopes (SC) are the note's own construct, absent from both Nelson's design corpus and udanax-green, so neither channel bears on the choice.
