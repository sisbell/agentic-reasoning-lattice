# Review of ASN-0051

## REVISE

### Issue 1: SV10 prose conflates "resolution" with "projection"
**ASN-0051, SV10 (DiscoveryResolutionIndependence)**: "A link may be discoverable through a set of I-addresses A yet have only partial resolution in a particular document — the projection covers a proper subset of the endset's full coverage:"
**Problem**: The Definitions section explicitly defines "resolution" as the locate function (`locate(e, d)`) and "projection" as π(e, d). The formal claim states `π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s)` — a projection assertion — but the prose calls this "partial resolution". This is exactly the terminology distinction the Definitions section was at pains to draw. SV13(e) likewise uses "Resolution" as a section header for bullets that reason about both π and locate.
**Required**: Rename the SV10 prose hook to "partial projection" (matching the formal claim), or expand to "partial resolution and partial projection" if both are intended. Apply the same clarification to SV13(e)'s heading or its body bullets.

### Issue 2: SV11 attainment witnesses do not cover p ≥ 3
**ASN-0051, SV11 (PartialSurvivalDecomposition)**: "*Conclusion.* The witnessed attainment scope spans three configurations: (i) `(m ≥ 1, p = 1)` ..., (ii) `(m = 1, p ≥ 2)` ..., and (iii) `(m ≥ 2, p ≥ 2)` with overlapping I-extents and `min_k n_k ≥ 2m − 1` via the multi-block overlap witness above."
**Problem**: The (iii) witness is explicit only for p = 2 (β₁ and β₂ overlapping). The text's "The same construction generalises" remark does not exhibit a p ≥ 3 attainment witness, and the non-attainment case analysis (disjoint extents, small blocks) does not address mixed configurations where some block pairs overlap and others are disjoint at p ≥ 3. For p = 3 with all three blocks pairwise overlapping (admitted under S5), is attainment achievable? The disjoint-extent argument's "every span contributes non-empty to both blocks" assumption needs to be applied per-pair to settle the mixed case.
**Required**: Either (a) provide a concrete (m ≥ 2, p = 3) witness with pairwise-overlapping I-extents, or (b) record explicitly that whenever a p ≥ 3 configuration contains at least one disjoint pair of blocks, the suffix-coalescence argument kills attainment via that pair, leaving "all pairs overlap" as the residual case. Without one or the other, the claimed exhaustiveness of "witnessed attainment scope" is overstated.

### Issue 3: SV11 fragment-count analysis omits one strictness mechanism in the worked example
**ASN-0051, Worked Example "Two-span, non-injective scenario"**: "The fragment count is 2 — strictly less than the non-empty-term count (4) and the m · p upper bound (4) — because adjacency within blocks merges term-level contiguous regions, while non-injective sharing introduces no new fragments beyond those each block independently contributes."
**Problem**: The phrase "non-injective sharing introduces no new fragments" is correct but does not establish what readers expect from the surrounding analysis: that the non-injective configuration is *not* itself the cause of the strictness here. The strictness is mechanism (b) alone (within-block coalescence at a₂↔a₃ in β₁ and at a₂↔a₃ in β₂). A reader following the cover-not-partition discussion may infer that overcounting at shared addresses is contributing to the gap — it is not. The text should disentangle.
**Required**: Add one sentence clarifying that the 4 → 2 gap is entirely mechanism (b) coalescence within each block (independently), and that non-injective sharing only inflates the *width sum* (6 versus |π| = 4) without changing the fragment count.

### Issue 4: Sub-claim (i) proof obligation about t_j defined
**ASN-0051, SV6 proof, sub-claim (i)**: "Suppose the first position where tⱼ ≠ sⱼ is some j with j < k. Then #t ≥ j and tⱼ > sⱼ."
**Problem**: The proof of `#t ≥ j` argues by contradiction from `#t < j`. The contradiction step says "Then t and s agree on every position 1 through #t (because j is the *first* position of divergence and #t < j)". But the very phrase "the first position where tⱼ ≠ sⱼ" presupposes t_j is defined — if j > #t, the supposition is vacuous, not a claim with content. The contradiction the proof wants is: "if t agrees with s on all 1..#t with #t < #s, then t is a proper prefix of s by T1(ii), so t < s, contradicting s ≤ t". The "agreement on 1..#t" step is the load-bearing inference and deserves its own line rather than being parenthetically attributed to a supposition that's vacuous at #t < j.
**Required**: Restructure the #t ≥ j argument to read: "Suppose for contradiction #t < j ≤ #s. Then no position 1..#t can witness a divergence between t and s (since j is the minimum divergence index and #t < j), so t agrees with s on all of 1..#t, making t a proper prefix of s. By T1(ii), t < s — contradicting s ≤ t." The order of reasoning is the same; the rewrite makes the load-bearing step explicit.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to π(e, d)
**Why out of scope**: The ASN explicitly defers endsets whose coverage references link addresses (via L4 + L13) to a future Link Subspace ASN. The SV11 decomposition is correctly scoped to π_text, and SV2 is stated uniformly across K.μ⁺ and K.μ⁺_L without committing to a particular subspace analysis. This is appropriate.

### Topic 2: Broader-level span survivability (k ≤ p₃)
**Why out of scope**: SV6's element-field exclusion is scoped to k > p₃ by design. The "Note on scope" correctly defers cross-prefix span coverage behaviour to ASN-0034's allocator and address-hierarchy machinery, citing Nelson's intent that broader-level spans admit future content.

### Topic 3: Same-origin coverage growth disciplines
**Why out of scope**: The "Content Allocation and Coverage Stability" section is descriptive and makes no formal SV claim. Sequential overshoot, child-depth entry, and the byte-level vs broader-level architectural distinction are presented as motivation for SV6's cross-origin focus, with the formal allocator-discipline conditions deferred to ASN-0034. This is the right scope split.

VERDICT: REVISE
