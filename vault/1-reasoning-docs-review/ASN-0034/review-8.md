# Review of ASN-0034

## REVISE

(none)

Every proof was checked case-by-case against the constructive definitions. Specific verifications performed:

- **T5 proof**: Both cases (length ≥ prefix, length < prefix) are complete. Case 2's contradiction via the prefix rule is valid — the key step `bⱼ > pⱼ = cⱼ` at the forced divergence point holds because `j < #p` guarantees `aⱼ = pⱼ` and `cⱼ = pⱼ`.
- **TA1 verification**: All three cases (k < divergence, k = divergence, k > divergence) correctly handle the tail-replacement semantics. The prefix-divergence case is correctly excluded from TA1-strict since `divergence(a,b) = min(#a,#b)+1 > min(#a,#b) ≥ k`.
- **TA3 verification**: Case 0 (prefix-related operands) is the most complex — five sub-cases traced through zero-padding, divergence propagation (`d_b = d_a` follows because `b_i = a_i` for all `i ≤ #a` and `d_a ≤ #a`), and result-length comparison. Case 2 impossibility (`a_{d_a} ≥ w_{d_a}` from `a ≥ w` contradicts `a_{d_a} < b_{d_a} = w_{d_a}`) is correct. TA3-strict's equal-length condition correctly eliminates Case 0, leaving only strictly-ordered cases.
- **TA4 verification**: Both sub-cases (a_k > 0 and a_k = 0) verified. Each precondition justified by counterexample showing failure without it.
- **Reverse inverse corollary**: The contradiction argument via TA3-strict is valid — all four prerequisites (`y ⊕ w ≥ w`, `a ≥ w`, `#(y ⊕ w) = #a`, and strict ordering of the assumed-unequal pair) are independently established.
- **Partition monotonicity**: The non-nesting argument for sibling prefixes (same length from TA5(c), unequal from increment at sig(t)) is correct. The prefix ordering extension lemma's application is valid.
- **Global uniqueness**: All four cases verified. Case 4's length-separation argument (`γ₁ + k' > γ₁` with additive accumulation across nesting) correctly handles arbitrary descendant depths. Cross-branch descendants at equal output lengths fall into Case 2 via divergence at the ancestor branching point.
- **TA5 T4-preservation**: The adjacent-zeros argument for k ≥ 3 is the binding constraint, correctly identified as independent of zero-count.
- **Associativity**: All three sub-cases (`k_b < k_c`, `k_b = k_c`, `k_b > k_c`) produce identical results on both sides. The `k_b > k_c` case correctly shows `b`'s contribution is overwritten by the shallower `c` in both evaluation orders.
- **Worked example**: All computations verified against the constructive definitions, including the TA4 round-trip failure (divergence at position 1 rather than position 8 due to nonzero prefix) and the ordinal-only recovery.

## OUT_OF_SCOPE

### Topic 1: Span algebra (split, merge, intersection)
**Why out of scope**: T12 defines span well-formedness and denotation but not operations on spans. Splitting a span at an interior address, computing the intersection of two overlapping spans, or the set difference — these build on the tumbler algebra but require their own definitions, preconditions, and closure proofs.

### Topic 2: Allocation protocol formalization
**Why out of scope**: T9, T10, T10a characterize allocation *properties* (monotonicity, partition independence, sibling discipline) but not the *protocol* — allocator initialization, parent-to-child prefix delegation, persistent state, crash recovery. The open question about counter durability points here.

VERDICT: CONVERGED
