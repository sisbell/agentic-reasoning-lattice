# Review of ASN-0084

## REVISE

### Issue 1: Split B3 verification for the second piece is proof by assertion
**ASN-0084, Block Decomposition Transformation, Split definition**: "both satisfy B3 (the correspondence relation restricts to each sub-range)"
**Problem**: For the first split piece `(v, a, c)`, B3 follows by restricting the index range — trivially a subset of the original. For the second piece `(v + c, a + c, n − c)`, B3 requires showing `M(d)((v + c) + k) = (a + c) + k` for `0 ≤ k < n − c`. This needs associativity `(v + c) + k = v + (c + k)` (TS3, requiring `c ≥ 1` and `k ≥ 1`; identity convention for `k = 0`) and then the original B3 at index `c + k < n`. The two pieces are structurally different — the first is a restriction, the second requires an index-shifting argument — so "restricts to each sub-range" does not cover the second case.
**Required**: Show the second-piece derivation explicitly: `M(d)((v + c) + k) = M(d)(v + (c + k))` by TS3/identity convention, `= a + (c + k)` by original B3 (since `c + k < n`), `= (a + c) + k` by TS3/identity convention.

### Issue 2: Merge B3 not verified
**ASN-0084, Block Decomposition Transformation, Merge definition**: "The merged block is (v₁, a₁, n₁ + n₂)."
**Problem**: The definition introduces the merged block without verifying that it satisfies B3 (the consistency condition that makes it a valid block). R-BLK's Phase 3 note about maximal merging relies on the merge producing valid blocks. The two-case argument is standard but not trivial — it requires associativity and index shifting across the block boundary.
**Required**: State and prove B3 for the merged block. For `0 ≤ k < n₁`: `M(d)(v₁ + k) = a₁ + k` by B3 of the first block. For `n₁ ≤ k < n₁ + n₂`: write `k = n₁ + k'` with `0 ≤ k' < n₂`; then `v₁ + k = v₁ + (n₁ + k') = (v₁ + n₁) + k' = v₂ + k'` and `a₁ + k = (a₁ + n₁) + k' = a₂ + k'`, so `M(d)(v₁ + k) = M(d)(v₂ + k') = a₂ + k' = a₁ + k` by B3 of the second block. Both associativity steps invoke TS3 (for `n₁ ≥ 1`, `k' ≥ 1`) or the identity convention (for `k' = 0`).

### Issue 3: Invariant preservation claim omits S7a, S7b, S7c
**ASN-0084, State and Vocabulary, Invariant preservation**: "Together with R-RI (S3), the well-definedness lemmas R-PIV/R-SWP (S2), and C' = C (S0, S1), every ASN-0036 invariant is maintained by an arrangement rearrangement."
**Problem**: The enumeration explicitly names the invariants preserved by domain invariance (D-CTG, D-MIN, S8-fin, S8a, S8-depth) and those preserved by dedicated proofs (S2, S3) and C' = C (S0, S1). However, S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), and S7c (ElementFieldDepth) are ASN-0036 invariants that constrain `dom(C)` and are not mentioned. They are preserved by `C' = C` (which implies `dom(C') = dom(C)` and all structural properties carry over), but the claim "every ASN-0036 invariant" requires either exhaustive enumeration or a structural argument that accounts for all invariants, not just the ones named.
**Required**: Add S7a, S7b, S7c to the "C' = C" group. For example: "C' = C preserves S0, S1, S7a, S7b, S7c (all properties constraining the content store and its domain carry over from the identity C' = C)."

## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depth > 2
**Why out of scope**: The ASN restricts to depth-2 V-positions and notes the generalization is "structurally identical by D-CTG-depth." Formalizing the general case — where ordinals are tuples and displacement analysis requires tumbler subtraction rather than integer subtraction — is new work that belongs in a future ASN or a revision of this one once the depth-2 case is validated.

### Topic 2: The open questions listed in the ASN
**Why out of scope**: k-cut generalization, composition of rearrangements, block count bounds, and cut-block boundary interactions are explicitly flagged as future work and do not affect the correctness of the depth-2, 3/4-cut results established here.

VERDICT: REVISE
