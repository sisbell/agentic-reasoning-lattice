# Channel Assignment — ASN-0134 review-10

**Date:** 2026-06-13 21:40

## Issue 1: H1/W1 anchor-incomparability is justified by an argument that fails for nesting homes
Reason: Internal — the conclusion is unchanged and both replacement justifications are already present in the ASN. The origin projection (`origin(a) = d`, already used in H0's proof as a structural projection fixed per address) gives `a ≠ a'` for `d ≠ d'` regardless of subspace with no anchor reasoning; alternatively `CrossDocumentDisjointness`'s own separator-vs-nonzero-continuation argument handles the cross-subspace case. Whether documents may nest is settled by ASN-0093's `K.σ` precondition (`zeros(d) = 2`, T4-valid) cited in the dependency stack, not by Nelson's intent or udanax-green evidence — and the origin-projection fix is valid either way, so no new assumption about home incomparability is needed.

## Issue 2: A6's "per-state canonicity package" is presented as exhaustive but enumerates a subset
Reason: Internal — the reviewer's "easy route" is derivable from machinery already in A6's proof: redefine "structurally canonical" as "satisfies every per-state invariant of the stack" and lean on the reachability + `B2`/`RP-a` transfer the proof already invokes, which yields all per-state invariants, not just the five listed. The omitted invariants (`C2`, `L0`, `L1a`, `M0`, `M2`, `L-fin`, `C-fin`) are ASN-0093/0126 spec content in the declared dependencies, not questions about udanax-green or design intent.
