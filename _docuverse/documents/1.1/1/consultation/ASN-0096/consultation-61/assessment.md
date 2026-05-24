# Channel Assignment — ASN-0051 review-61

**Date:** 2026-05-16 09:48

## Issue 1: T-interleaving structural argument under-justified
Reason: The fix replaces informal tumbler notation with an explicit T1-based case analysis on length-and-prefix configurations of disjoint sibling chains. This is purely structural tumbler arithmetic derivable from T1 (ASN-0034), which the ASN already cites; no design intent or implementation evidence is required.

## Issue 2: Pigeonhole sub-argument in T-interleaving is condensed
Reason: The fix expands a combinatorial case split on a 2-element boundary set, using span convexity (S0) and within-block ordinal adjacency — both already established in the ASN. Pure structural combinatorics, no external channels needed.

## Issue 3: SV6 sub-claim (i) hypothesis well-formedness
Reason: The fix rephrases the hypothesis to use T1(i)'s witness clause directly, eliminating apparent circularity in the #t ≥ j derivation. T1 is already cited from ASN-0034; this is internal logical restructuring.

## Issue 4: (m ≥ 3, p ≥ 3) attainment witness gap
Reason: Either constructing an explicit (m=3, p=3) witness or revising the scope summary uses only M7/M12 (ASN-0058), T4/OrdinalShiftBase (ASN-0034), and S5 (ASN-0036) — all already cited. The nesting pattern from the (m=2, p=3) witness in the ASN provides the template; no new design or implementation facts are needed.

## Issue 5: SV11 attainment-or-not at single disjoint pair within p ≥ 3
Reason: The fix adds one sentence noting that per-block fragment counts are independently capped at m, which follows directly from the attainment biconditional already proven in SV11. Internal clarification.

## Issue 6: Worked example two-span variant — fragment-attribution claim
Reason: The fix cites the maximal-fragment definition's per-block confinement — a definition already stated in the ASN ("within a single mapping block's ordinal sequence"). Pure internal cross-reference.
