# Review of ASN-0100

## REVISE

### Issue 1: D-CTG★ proof glosses the depth ≥ 3 case

**ASN-0100, §Verifying the Invariants → "Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)"**: "The integer range `{1, …, N + n}` of last-component values is contiguous, so D-CTG★ holds." And in the empty case: "the last-component values `{1, 2, …, n}` form a contiguous integer range with no gaps; T1 makes the V-ordering on a fixed-prefix, fixed-depth subspace agree with the integer ordering on the last component, so contiguity holds."

**Problem**: D-CTG★ (ASN-0047) does not quantify over the fixed-prefix family `{[s_C,1,…,1,k]}`. It requires closed-interval membership over the *entire* depth-`m_C`, subspace-`s_C` slice — every positive-component tuple whose first component is `s_C`. For `m_C ≥ 3` that slice contains off-prefix tuples such as `[s_C, 2, 1, …, 1]`. The proof must establish that any slice element `z` with `min ≤ z ≤ max` lies in `V_{s_C}(d')`, i.e., that off-prefix tuples fall strictly outside `[min, max]` under T1 (e.g., `[s_C,2,1,…,1] > [s_C,1,…,1,N+n]` at component 2). The phrase "on a fixed-prefix … subspace" silently restricts the slice to the prefix the conclusion wants — but the slice's prefix is *not* fixed. This is exactly the reduction SharedPrefixReduction (D-CTG-depth, ASN-0036) supplies, yet it is neither cited nor argued. The case is reachable: the empty-case caller may choose `m ≥ 3`, and a non-empty `m_C` may already be `≥ 3`. For `m_C = 2` the assertion is trivially adequate; for `m_C ≥ 3` it is a proof by assertion.

**Required**: Invoke D-CTG-depth (ASN-0036), or explicitly show that any depth-`m_C` slice element between `min = [s_C,1,…,1]` and `max = [s_C,1,…,1,N+n]` must share the prefix `[s_C,1,…,1]` (off-prefix tuples either exceed `max` or precede `min` under T1), thereby reducing D-CTG★ to the last-component contiguity actually demonstrated.

### Issue 2: S8★ existence/uniqueness applied to a restriction without the bridging lemma

**ASN-0100, §Verifying the Invariants → "Per-subspace span decomposition (S8★)"**: "the existence of a block decomposition for `M'(d)|_{V_{s_C}(d')}` follows from M2 directly" and "M12 therefore makes the maximal-run decomposition of `M'(d)|_{V_{s_C}(d')}` unique, closing condition (c) on the content subspace."

**Problem**: M2 (DecompositionExistence) and M12 (CanonicalUniqueness) in ASN-0058 are stated for whole arrangements `M(d)`, not for a restriction to a single subspace. `M'(d)|_{V_{s_C}(d')}` is a restriction, and the lemma that lifts M11/M12 to restrictions is C1a (RestrictionDecomposition, ASN-0058) — "M11 and M12 hold for any restriction `f = M(d_s)|X` ... whose induced domain lies within a single subspace." The ASN never cites C1a; it applies M2 and M12 to the restriction as if they were stated for it. The substance is recoverable (C1a's preconditions — functional restriction, finite domain, single common depth — are all discharged in the surrounding prose), but the derivation chain skips the one foundation result that authorizes the move.

**Required**: Route the content-subspace existence and uniqueness through C1a (RestrictionDecomposition, ASN-0058), discharging its preconditions, rather than citing M2/M12 directly on the restriction.

## OUT_OF_SCOPE

### Topic 1: Recovery to canonical order after a partial composite failure
**Why out of scope**: The ASN's first open question (minimum substrate machinery for composite atomicity / recovery after partial failure) is correctly deferred — it concerns the substrate execution environment, not INSERT's per-state contract.

### Topic 2: Link-subspace insertion (K.μ⁺_L semantics)
**Why out of scope**: The ASN explicitly restricts to the content subspace and notes the link-subspace extension is a structurally distinct operation; this is properly future territory, not a defect here.

VERDICT: REVISE
