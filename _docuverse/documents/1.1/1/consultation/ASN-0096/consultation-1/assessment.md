# Revision Categorization — ASN-0051 review-1

**Date:** 2026-03-20 19:54

## Issue 1: SV6 (BoundaryExclusion) proof is wrong and the theorem is likely false
Category: BOTH
Reason: The counterexample is mathematically valid from the tumbler algebra, but deciding whether to salvage SV6 (by finding a missing allocator constraint) or abandon it requires both Nelson's design intent about coverage closure and evidence of how the green allocator actually behaves with child-depth addresses.
Nelson question: Does the Xanadu design intend that new content can never enter an existing link's endset coverage — i.e., is the "strap between bytes" meant to be literally closed to future allocations — and if so, what mechanism or constraint on allocation was meant to guarantee this?
Gregory question: Does the udanax-green allocator ever use child-spawning (inc(t, 1) producing addresses like [D.0.n.1]) within I-address ranges that are already covered by existing link endset spans, or does the implementation constrain allocation patterns to prevent this?

## Issue 2: SV11 (PartialSurvivalDecomposition) proof invokes S1 without verifying its precondition
Category: INTERNAL
Reason: The review itself supplies the correct replacement argument — monotonicity of ordinal increment within a mapping block's same-length tumblers — so the fix is derivable from existing definitions without external evidence.

## Issue 3: SV10 (DiscoveryResolutionIndependence) uses informal language in its formal statement
Category: INTERNAL
Reason: The review identifies the informal phrase and suggests the formal replacement predicate; this is a straightforward notation correction within the ASN's own definitions.

## Issue 4: SV9 (DiscoveryMonotonicity) applies "dom" to a set
Category: INTERNAL
Reason: The review identifies the type error and provides the exact fix (drop "dom" from both sides); this is a mechanical notation correction.

## Issue 5: No concrete worked example
Category: INTERNAL
Reason: All definitions needed (π, resolve, discover, vitality, arrangement operations) are already present in this ASN and its dependencies; constructing a scenario with explicit tumbler values requires only applying these definitions, not external evidence.
