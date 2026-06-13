# Channel Assignment — ASN-0133 review-6

**Date:** 2026-06-13 12:06

## Issue 1: The worked example assigns two incompatible views to one QD filter
Reason: The fix is a formal view-consistency correction entirely within ASN-0129's PC3 machinery — the view-parameterized list, the fixed-slice rebuild `⋃(L_tgt, addrs_F)`, and the audit/active grow-only behaviors (PD0/PD1) are all established in the cited dependency, and the reviewer has fully specified both repair options plus the Q0/Q7 criterion correction. No design intent or implementation evidence is needed.

## Issue 2: "names an empty case" is false for non-concurrent registries
Reason: A pure logic correction — the note's own H-W section already supplies the qualifier ("essentially every registry that does concurrent work") that Q6 dropped, and the single-rule counterexample plus the H-W ⟹ H-RF subsumption fix follow from the note's existing definitions. Internal.

## Issue 3: "each bounds real fires" is proven only for Q5a, and is false for acyclicity
Reason: A pure logic correction derivable from the note's own Q5a/H-RF framework — the acyclicity counterexample (single rule on an unboundedly growing domain) and the observation that "per-stratum bounds" smuggles in a per-stratum H-RF are both internal to the existing reasoning. No external channel needed.
