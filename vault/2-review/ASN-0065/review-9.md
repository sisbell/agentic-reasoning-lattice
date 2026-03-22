# Review of ASN-0065

## REVISE

No issues found.

Every proof is explicit and correct. I verified the following in detail:

**R-PIV / R-SWP (well-definedness).** The tiling arguments are shown explicitly — R-PIV decomposes V_S(d) into three pairwise-disjoint ranges whose union is V_S(d); R-SWP does the same with four ranges. The tiling for R-SWP is computed in the paragraph preceding the proof ("The total width is w_β + w_μ + w_α..."), so the abbreviated proof statement ("Identical in structure to R-PIV") references work already shown, not deferred.

**R-PPERM / R-SPERM (permutation correctness).** Each case of the bijection is verified against the corresponding postcondition clause. Injectivity within cases follows from distinct j yielding distinct images. Cross-case disjointness follows from the tiling. Surjectivity follows from the image sets covering V_S(d). All four verification steps are present for both permutations.

**R-CP (content preservation).** The multiset argument is sound: π bijective and M'(d)(π(v)) = M(d)(v) give |{v : M'(d)(v) = a}| = |{u : M(d)(u) = a}| for every I-address a.

**R-CF / coupling constraints.** J3 gives R' = R directly. J0, J1, J1' are shown vacuous with the correct justification (dom(C') \ dom(C) = ∅; ran(M'(d)) \ ran(M(d)) = ∅ for all d; R' \ R = ∅).

**Invariant preservation.** S2, S3, S8a, S8-depth, S8-fin all follow from dom(M'(d)) = dom(M(d)) and ran(M'(d)) = ran(M(d)). P4 follows from Contains(Σ') = Contains(Σ) ⊆ R = R'. P6, P7, P7a, P8 follow from C' = C, E' = E, R' = R. D-CTG follows from V_S'(d) = V_S(d).

**R-BLK (block decomposition).** The commutativity claim π(vⱼ + k) = π(vⱼ) + k is proved using M-aux associativity and natural-number commutativity at depth 2. B3 for reassembled blocks follows from this commutativity composed with the original B3 and the permutation property. B1 and B2 follow from π being a bijection on V-extents.

**Worked examples.** Both the 3-cut and 4-cut examples trace every postcondition clause position-by-position. The R-CP, R-PPERM/R-SPERM, displacement, and block decomposition verifications are all independently confirmable. The 4-cut example exercises the asymmetric case (w_α = 2 ≠ w_β = 3), including the nonzero middle displacement and the post-rearrangement merge of previously separated blocks.

**Boundary cases.** Single-position documents are excluded by R-PRE(v) (w_α ≥ 1 ∧ w_β ≥ 1 requires at least 2 positions in the affected range). The 4-cut case on a 2-position document is excluded because w_μ ≥ 1 (from CS2) forces at least 3 positions. Cuts at block boundaries produce no split in Phase 1 (the condition cᵢ ≠ vₖ is not satisfied). The exclusive upper bound c_{n-1} potentially outside V_S(d) is handled correctly by R-PRE(iv) requiring only positions in [c₀, c_{n-1}).

**Cross-subspace positions.** At depth 2, positions in subspace S' ≠ S satisfy [S', k] < c₀ (when S' < S) or [S', k] > c_{n-1} (when S' > S) by T1(i), so they fall under the exterior clause of R-PPERM/R-SPERM and are fixed by π, consistent with R-XS.

## OUT_OF_SCOPE

### Topic 1: Composability of rearrangements
**Why out of scope**: Whether the composition of two rearrangements is expressible as a single rearrangement, and what permutation group the cut-point operations generate, is a new algebraic question. Already listed in Open Questions.

### Topic 2: Block count bounds after rearrangement
**Why out of scope**: The worked examples show both increase (3-cut: 2 → 4 blocks) and stability (4-cut: 4 → 4 blocks after merge). Characterizing the worst-case block count increase as a function of cut count requires analysis beyond what REARRANGE itself needs to specify. Already listed in Open Questions.

### Topic 3: Depth generalization beyond depth 2
**Why out of scope**: D-CTG-depth reduces contiguity at depth m ≥ 3 to the last component, and D-SEQ gives the same sequential structure. The displacement arithmetic depends only on the last component, so generalization is structurally immediate. The depth-2 restriction is presentational, not fundamental. Already acknowledged in Open Questions.

VERDICT: CONVERGED
