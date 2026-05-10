# Revision Categorization — ASN-0048 review-2

**Date:** 2026-03-18 12:08

## Issue 1: TA7a (SubspaceClosure) applied to I-addresses without justification
Category: INTERNAL
Reason: Both fix options use existing foundation properties. Option (b) derives contiguity from TA5(c) and inc(·, 0) already cited in the ASN; option (a) parallels TA7a's structure using definitions already present in ASN-0034.

## Issue 2: I0(d) derivation from T9 alone is insufficient
Category: INTERNAL
Reason: The reviewer sketches the complete fix via T1 lexicographic ordering (ASN-0034): P.(x+1) exceeds all P.x.* at the divergence point. Alternatively, the ASN's own description of INSERT using only inc(·, 0) establishes the single-stream constraint directly.

## Issue 3: Incomplete invariant verification
Category: INTERNAL
Reason: The reviewer provides complete proofs for P6, P7, and P7a using only properties already established in the ASN (I0(b), I-pre, I-post(b), Phase 1, Phase 4, pre-state invariants). Alternatively, citing ReachableStateInvariants from ASN-0047 suffices.

## Issue 4: Coalescing claim contradicts I7 and I8
Category: INTERNAL
Reason: Both fix options are internal. Option (a) removes an implementation detail that contradicts the formal analysis. Option (b) reconciles using existing properties — the missing I-address contiguity condition follows from the allocation discipline already specified in I0, and the non-uniqueness of run decompositions is a mathematical observation about S8.
