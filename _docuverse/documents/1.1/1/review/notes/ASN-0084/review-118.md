# Review of ASN-0084

I checked the well-definedness lemmas (R-PIV, R-SWP), the two permutation constructions (R-PPERM, R-SPERM), the commutation lemma (R-COMM), the run-transformation (R-BLK), canonicality (R-CANON), and the invariant audit, against the foundations and the depth-2 scope.

Key obligations that hold up under scrutiny:
- **Tiling/coverage** (the hardest invariant): R-BLK's coverage argument is genuinely proven — π is a bijection on V_S(d), maps the post-split partition to a partition, R-COMM makes images contiguous, and cross-group disjointness rests on T10 with non-nesting prefixes [1], [2]. Not hand-waved.
- **Region exhaustiveness/disjointness**: both the n=3 (three sub-cases) and n=4 (five sub-cases) trichotomy splits are shown explicitly, not deferred.
- **Surjectivity of π**: correctly grounded in finite-self-injection after verifying π maps into dom(M(d)).
- **R-CANON forward/backward extension**: both directions argued in full via predecessor/successor uniqueness and disjointness — no "by symmetry" shortcut on the load-bearing step.
- **μ sub-cases** (forward/fixed/backward) all exercised by distinct worked examples (2/3/4), plus the boundary/empty-exterior edge (example 5) and the non-S pass-through (example 6).
- **S8 discharge** for the post-state correctly verifies every foundation precondition (S8-fin, S2, S3 via R-RI, S8a, S8-depth) holds for M'(d).
- The two exterior pieces (left/right) collapse safely in R-COMM because π is identity on both; R-BLK independently prevents straddling runs via the split at c₀.

The depth-2 restriction, singleton/ℕ identification, truncated subtraction, and identity convention `shift(t,0):=t` are all consistently applied and foundation-cited.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: k-cut generalization (k > 4)
**Why out of scope**: The natural permutation class expressible by cut-point rearrangement for k > 4 is new territory; the ASN correctly defers it to Open Questions.

### Topic 2: Composition of rearrangements
**Why out of scope**: Whether composed rearrangements are themselves single rearrangements is a property of operation sequences, not of this single operation.

### Topic 3: Cut-point/run-boundary constraints and run-count growth bounds
**Why out of scope**: Bounding the canonical run-count increase relative to cut count is a quantitative follow-on, not a correctness gap in REARRANGE_K.

### Topic 4: Weakest precondition for a post-state invariant suite Q
**Why out of scope**: The ASN establishes invariant preservation directly; a wp characterization is a separate analytical layer.

VERDICT: CONVERGED
