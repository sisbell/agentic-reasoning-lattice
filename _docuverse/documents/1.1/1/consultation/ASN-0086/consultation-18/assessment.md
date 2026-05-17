# Channel Assignment — ASN-0086 review-18

**Date:** 2026-05-16 23:36

## Issue 1: "Sparse-allocator interpretation" is a substrate-level commitment that strengthens ASN-0034 but its relationship is under-specified
Reason: The fix requires both design intent (was this layering meant to be canonical?) and implementation evidence (does udanax-green expose intermediate allocator-state transitions or commit atomically at the link-store level?).
Nelson question: Was the substrate-level transition relation in Literary Machines / the design intent meant to be a canonical equivalence-class projection over allocator-state transitions, or were multiple coarsenings intended to be admissible as conforming implementations?
Gregory question: In udanax-green's link-emission path (`docreatelink`, `findisatoinsertmolecule`, granf2.c:170–175), is the allocator-state evolution (`Act(s)`, `n_s` updates per allocator on the L1c chain) atomic with the link-store deposit, or are there observable intermediate states between the allocator updates and the deposit?

## Issue 2: R0 Step 2 Case A's "subspace 1" labeling implicitly assumes `s_C = 1`
Reason: To choose between fixing `s_C = 1` as a convention (which the review hints is udanax-green-consistent) versus rewriting without subspace labels, evidence from the implementation about its actual subspace assignment is needed.
Gregory question: In udanax-green, what are the literal first-element-field subspace identifiers for content addresses and link addresses (i.e., what are the concrete values of `s_C` and `s_L` in the substrate's tumbler conventions)?

## Issue 3: R0 Step 4's L11a verification is redundant
Reason: The fix is a local prose simplification — freshness (`a ∉ dom(Σ.L)`) already establishes distinctness directly, and the rewrite is derivable from the ASN's own R0 Step 2 freshness witness without consulting design intent or implementation.

## Issue 4: R6c's bridge to broader transition vocabulary is buried in a parenthetical
Reason: The technical content (the four-step dependency chain through the arrangement-modification frame inherited from ASN-0036) is already fully derived in the ASN; the fix is purely a structural promotion of the parenthetical to a labeled corollary.

## Issue 5: R0a's statement omits the antichain's failure mode under the substrate primitive in isolation
Reason: Both failure-mode claims are derivable from existing ASN content — (a) follows from L12 (LinkImmutability) preserving any prefix-comparable pair forever once emitted, and (b) follows from R0a's reachable-state antichain being the precondition Nullify's single-tuple-scope argument depends on (per the existing "Remark on the role of P3").
