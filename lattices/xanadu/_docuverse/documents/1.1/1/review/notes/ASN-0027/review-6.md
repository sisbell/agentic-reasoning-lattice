# Review of ASN-0027

Based on Dafny verification — 32/32 properties verified, 1 divergence reported.

## REVISE

No genuine spec issues.

## QUALITY

### Missing abstraction: DeleteV duplication — SIMPLIFY

`DeleteV` is defined identically in 6 files: DeleteCompaction, DeleteLeftFrame, DeleteLength, FullRestoration, IdentityRestoringCopy, NonInvertibility. `InsertOps` already exists as a shared module and is imported by three of these files. Extract `DeleteV` into a parallel `DeleteOps` module.

Similarly, `CopyV` is defined identically in 4 files: CopyIdentitySharing, CopyLeftFrame, CopyLength, CopyRightShift. Extract into a `CopyOps` module.

### Missing abstraction: RearrangeRangePreservation.dfy — SIMPLIFY

Duplicates `ValidPivotCuts`, `ValidSwapCuts`, `PivotRearrangeV`, and `SwapRearrangeV` from RearrangePermutation. Should import RearrangePermutation instead of redefining.

### All other files — PASS

The remaining 26 files are clean: predicates are minimal, lemma bodies are empty or contain only necessary witness assertions (e.g., RearrangeRangePreservation's inverse-mapping hints). ReferencePermanence's inductive proof is well-structured. NonInvertibility's bridge lemma `DeleteInsertPositions` is a reasonable decomposition.

## SKIP

### ReachabilityDecay divergence — proof artifact

The Dafny proof constructs an empty state `State(iota := s.iota, docs := {}, vmap := map[])` to witness unreachability, rather than formalizing the iterated-DELETE trace the ASN describes. This proves a weaker existential (some unreachable state exists) rather than the ASN's constructive claim (a specific sequence of DELETEs reaches such a state). The ASN property A9 is correctly stated — the proof simply defers the operational trace formalization. No spec change needed.

### 31 clean verifications — no divergences

All other properties verified without modification. The Dafny statements faithfully encode the ASN properties: operation specs (A2-A5), frame conditions, NonInvertibility (A6), IdentityRestoringCopy (A7), ReferencePermanence (A8), and the Reachable definition.

VERDICT: SIMPLIFY
