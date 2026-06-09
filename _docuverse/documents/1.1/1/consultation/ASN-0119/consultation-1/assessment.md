# Channel Assignment — ASN-0119 review-1

**Date:** 2026-06-08 18:54

## Issue 1: No concrete worked example
Reason: Adding a numerical pivot/swap that exercises P1, P2, P3 and the `w_β − w_α` displacement is pure instantiation of the note's own equations (R-P1/R-P2, R-S1–S3, π). No design intent or implementation evidence is required.

## Issue 2: Atomicity claims P8a/P8b are asserted, not derived
Reason: Defining a "two-move composite," decomposing a specific π into two realizable moves, and computing the intermediate arrangement is a self-contained construction over the permutation π already specified here; the consultation answers (Q6, Q19) are already incorporated. Internal.

## Issue 3: Scope inconsistency — general subspace S vs. text-only/depth-2 foundations
Reason: Whether D-CTG/D-SEQ/D-MIN and R-PPERM/R-SPERM are established only for the text subspace at depth 2 is fixed by the cited spec ASNs (0034, 0036, 0084); resolving the scope is editorial against those definitions. Internal.

## Issue 4: Restatement of and label collision with the existing REARRANGE specification
Reason: The fix is to import the existing REARRANGE_K/R-PPERM/R-SPERM/R-RI definitions from the prior ASN and rename colliding labels — a corpus-citation and self-containment edit, not a question of design intent or code behavior. Internal.

## Issue 5: S2 (functionality) and S3 (referential integrity) preservation not discharged as named invariants
Reason: Single-valuedness (S2) follows from the disjoint tiling already proved, and `ran(M'(d)) ⊆ dom(C)` (S3) follows from P1 plus `ran(M(d)) ⊆ dom(C)`; both are one-line consequences of material already in the note. Internal.
