# Review of ASN-0051

## REVISE

### Issue 1: SV6 proof cites wrong foundation and skips a non-trivial step

**ASN-0051, SV6 (CrossOriginExclusion)**: "Since origin(s) is a prefix of both s and s ⊕ ℓ, by T5 (ContiguousSubtrees) every tumbler t with s ≤ t ≤ s ⊕ ℓ satisfies origin(s) ≼ t, **hence origin(t) = origin(s)**. In particular, every t ∈ ⟦(s, ℓ)⟧ shares origin(s). Since origin(b) ≠ origin(s), b cannot be equal to any such tumbler **(T10, PartitionIndependence)**."

**Problem**: Two gaps.

(a) The "hence origin(t) = origin(s)" step is non-trivial and unconstrained. It holds only for element-level t (zeros(t) = 3), which is what matters since b is element-level by S7b — but the proof claims it for all t in the span. The argument: when the action point is within the element field, all positions through the 3rd separator are fixed by TumblerAdd. Any element-level t in [s, s ⊕ ℓ) must agree with s on all those positions (otherwise t would exceed s ⊕ ℓ at a position before the divergence, violating the upper bound). Since t has exactly 3 zero separators at the same positions as s, its field decomposition matches and origin(t) = origin(s). This multi-step structural argument is collapsed into "hence."

(b) The T10 (PartitionIndependence) citation is incorrect. T10 requires the two prefixes to be incomparable (neither a prefix of the other). Document-level tumblers can have prefix relationships — e.g., origin(s) = N.0.U.0.D₁ and origin(b) = N.0.U.0.D₁.D₂. The actual justification is the contrapositive of what was shown: every element-level t in the span has origin(t) = origin(s), so any element-level b with origin(b) ≠ origin(s) is not in the span. T10 is not needed.

**Required**: Restrict the "hence" to element-level tumblers with explicit reasoning (field structure agreement through the 3rd separator forces origin equality). Replace the T10 citation with the direct contrapositive argument.


### Issue 2: SV10 formal statement has an unbound variable

**ASN-0051, SV10 (DiscoveryResolutionIndependence)**: "`(E Σ, a, d, s :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ ...)`"

**Problem**: V is free — not quantified and not defined. The existential quantifies Σ, a, d, s but not V. The prose describes V as "some V-region of document d" but the formal statement doesn't bind it.

**Required**: Either quantify V inside the existential or replace the discover_s argument with a concrete set (e.g., `ran(M(d))` or an explicit subset).


### Issue 3: SV11 incorrectly equates projection with span-set denotation

**ASN-0051, SV11 (PartialSurvivalDecomposition)**: "Therefore π(e, d) is a finite union of level-uniform spans."

**Problem**: π(e, d) = coverage(e) ∩ ran(M(d)) is a finite set of I-addresses — actual allocated element-level tumblers. A span denotation ⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ} includes *all* tumblers in the interval, including child-depth tumblers between consecutive ordinal increments. Concretely: if a is an element-level I-address and c = inc(a, 1), then a < c < a+1 (c has a as prefix), c is element-level (zeros(c) = 3 since TA5(d) with k=1 appends nonzero component), and c ∈ ⟦(a, ℓ_a)⟧ but c is not necessarily in ran(M(d)). So {a} ≠ ⟦(a, ℓ_a)⟧ and more generally the projection is strictly smaller than any non-trivial union of span denotations.

The upstream analysis is correct: each ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is contiguous within the ordinal sequence of I(β_k), by convexity (S0) and order preservation (TA-strict). The error is in translating "contiguous ordinal subsequence" to "span denotation."

**Required**: State the correct conclusion: π(e, d) decomposes into finitely many fragments, each a contiguous ordinal subsequence within a mapping block's I-extent (a compact description via start/width triples), but not a union of span denotations. Or introduce the notion of a *covering* span-set (⟦Σ⟧ ⊇ π(e, d)) if the intent is to connect to ASN-0053's algebra. The distinction matters for anyone applying span algebra operations to projections.


### Issue 4: SV4 label does not match scope

**ASN-0051, SV4**: Labeled "ContractionIsolation" but quantifies over K.μ⁺, K.μ⁻, and K.μ~.

**Problem**: The label implies the property is specific to contraction. A reader searching for the isolation property of extension would not find it under this name.

**Required**: Rename to "ArrangementIsolation" or similar, matching the actual scope.


### Issue 5: State-subscript ambiguity in SV2 and SV4

**ASN-0051, SV2**: "`π(e, d) ⊆ π(e, d')` where π(e, d') denotes π in the successor state"

**ASN-0051, SV4**: "`(A ... d, d' : d ≠ d' :: π(e, d') is unchanged)`"

**Problem**: d' means "d in the successor state Σ'" in SV2 but "a different document" in SV4. The notation collision forces the reader to disambiguate from context. Since SV2 and SV4 are adjacent properties making the same kind of claim (projection behaviour under arrangement changes), the collision is actively confusing.

**Required**: Use state subscripts for the state-dependent interpretation: π_Σ(e, d) and π_{Σ'}(e, d), or similar. Reserve d' exclusively for a distinct document.


## OUT_OF_SCOPE

### Topic 1: Formal allocation discipline that closes same-origin coverage growth

The ASN correctly observes that byte-level coverage closure is "architectural, not definitional" and depends on text allocators using only sibling increment (TA5(c)). The counterexample (child-depth address entering an existing span via inc(aₙ, 1)) demonstrates the gap is real. Formalizing a per-subspace allocation discipline axiom (e.g., "text-subspace allocators never invoke inc(·, k) with k > 0 within the element field") belongs in an allocation or content-mapping ASN, not here.

**Why out of scope**: SV6 correctly states the cross-origin exclusion; the same-origin case requires constraints on allocator behaviour that are outside link survivability's jurisdiction.

### Topic 2: Link creation as a state transition

ASN-0047's state Σ = (C, E, M, R) does not include the link store L. Link creation is not modelled as an elementary transition. The ASN correctly relies on L12 (LinkImmutability) from ASN-0043 for permanence, but cannot express "after link creation" within ASN-0047's transition framework. Extending the state model to include L (and defining K.λ or equivalent) is necessary for a complete operational semantics.

**Why out of scope**: This is a gap in the state-transition framework (ASN-0047), not in the survivability analysis.

VERDICT: REVISE
