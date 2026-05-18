# Review of ASN-0047

## REVISE

### Issue 1: K.δ k = 1 discharge fails for versions of versions

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation"**: "*k = 1 (version under existing document allocator):* … *Parent-allocator relationship in T10a's allocator tree:* `A_v(t)` is a child of `A_doc(parent(t))` — the document sub-allocator under t's account that minted t. T10a T2 admissibility requires the spawnPt `t` to inhabit `dom(A_doc(parent(t)))`, which K.δ k = 1's precondition `t ∈ E_doc` discharges directly: every `t ∈ E_doc` was minted by a prior K.δ event that placed t into `A_doc(parent(t))`'s tracked domain"

**Problem**: The claim "every t ∈ E_doc was minted by a prior K.δ event that placed t into A_doc(parent(t))'s tracked domain" is false for versions. If `t = inc(t', 1)` is a version (minted by a prior K.δ k = 1 event on t'), then `t ∈ dom(A_v(t'))`, the version sub-allocator activated by that prior event. By T10a.6 (DomainDisjointness), `dom(A_v(t')) ∩ dom(A_doc(parent(t))) = ∅` since `A_v(t') ≠ A_doc(parent(t))`. So `t ∉ dom(A_doc(parent(t)))`, and T10a T2 admissibility fails when K.δ k = 1 attempts to spawn A_v(t).

This is a soundness issue: S4 (Origin-based identity) in the matrix discharges via "T10a GlobalUniqueness on parent allocator (¬IsNode)" for K.δ events, but for K.δ k = 1 on versions the parent-allocator membership isn't satisfied.

**Required**: Case-split the K.δ k = 1 discharge by whether t is an original or a version: for original `t`, `parent(A_v(t)) = A_doc(parent(t))`; for version `t = inc(t', 1)`, `parent(A_v(t)) = A_v(t')`. Update Sub-allocator-names accordingly so that version sub-allocators nest within each other along the version chain.

### Issue 2: ValidComposite★ clause (1) inline existence condition is imprecise

**ASN-0047, "Scoped coupling constraints" (ValidComposite★)**: "K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (per its definition above): admissibility clause (iii) requires `π ≠ id` (and hence `dom_C(M(d)) ≠ ∅`), so K.μ~ always expands into two consecutive elementary steps"

**Problem**: The parenthetical "and hence dom_C(M(d)) ≠ ∅" is necessary but not sufficient. The §Decomposition of K.μ~ section correctly states "the necessary-and-sufficient existence condition is |dom_C(M(d))| ≥ 2"; the singleton case |dom_C(M(d))| = 1 also forces π = id. The inline statement in ValidComposite★'s clause (1) reads as the operative condition for a reader following the composite-validity rules directly.

**Required**: State the existence condition at this inline site as `|dom_C(M(d))| ≥ 2`, matching the strength established in §Decomposition.

### Issue 3: K.μ~ subspace-preservation argument uses S3★(Σ') and S3★(Σ) without flagging dependency order

**ASN-0047, "Decomposition of K.μ~"**: "Subspace preservation — `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))` — follows from S3★(Σ') + L14 + the bijection equation: were π to map a content-subspace v to s_L, the post-state would have `M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅`, contradicting L14"

**Problem**: Two implicit dependencies are not flagged. (a) The argument needs `M(d)(v) ∈ dom(C)` to chain through to `M'(d)(π(v)) ∈ dom(C)`, which requires S3★(Σ) at the pre-state (the inductive hypothesis) — not stated. (b) S3★(Σ') is itself derived in the ExtendedReachableStateInvariants matrix via K.μ⁻ + K.μ⁺ decomposition (the matrix's S3★/K.μ~ cell says "preserved via K.μ⁻ restriction + K.μ⁺ amendment alone (link-subspace fixity is downstream, not prerequisite)"), so this section's framing of subspace preservation as "following from S3★(Σ')" presents the consequence before the foundation. A reader who treats this section as the primary subspace-preservation argument may wrongly conclude that subspace preservation is required to establish S3★(Σ').

**Required**: State both dependencies explicitly: "by S3★(Σ) (inductive hypothesis) and the bijection equation, M'(d)(π(v)) ∈ dom(C)"; and note that S3★(Σ') is independently established by K.μ⁻ + K.μ⁺ preservation (matrix entry) before subspace preservation is derived.

### Issue 4: NodeRegistryBootstrap references an unmodelled "node-allocation registry"

**ASN-0047, "Elementary transitions" (K.δ axioms) and "K.δ case (ii) discharge and parent-allocator activation"**: NodeRegistryBootstrap commits `n₀ ∈ dom(node-allocation registry)` at Σ₀; the K.δ case (ii) k = 2 discharge with operand t = n₀ cites NodeRegistryBootstrap "to satisfy the spawnPt premise on the registry side."

**Problem**: The "node-allocation registry" is treated as a state-bearing entity (with a `dom`) in both axioms but is not a component of `Σ = (C, L, E, M, R)`. The discharge of T10a T2 admissibility for the first K.δ case (ii) k = 2 event (creating the first account under n₀) appeals to membership in this registry. As stated, T2 admissibility on K.δ events involving n₀ has no anchor in the formal state model. Either the registry is part of the state (and should appear in Σ's definition), or the K.δ k = 2 discharge for t = n₀ needs to identify a different mechanism.

**Required**: Either (i) extend `Σ` with a node-registry component and let NodeUniqueAllocation / NodeRegistryBootstrap operate on it as a formal predicate, or (ii) explicitly mark these registry-membership facts as external commitments and revise the K.δ case (ii) k = 2 discharge to either side-step T2 admissibility for `t = n₀` or to discharge via a different axiomatic route that does not reference an unmodelled state component.

### Issue 5: D-SEQ★ base case for m = 2 is brief and the degenerate notation is handled parenthetically

**ASN-0047, "Amendments to existing transitions" (D-SEQ★ derivation)**: "*Base case (m = 2).* The inner-position range `2 ≤ j ≤ m - 1 = 1` is empty, so the inner-positions-fixed claim is vacuously satisfied… Step 2 below then directly identifies V_S(d) with `{[S, k] : 1 ≤ k ≤ n_S}`, the m = 2 specialisation of D-SEQ★."

**Problem**: D-SEQ★'s post-condition reads `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`. At m = 2 this degenerates: the "1, ..., 1" segment has length m − 2 = 0, so the canonical form is `[S, k]`. This degeneracy is acknowledged in Step 2 ("at m = 2 that segment has length m − 2 = 0 and the notation degenerates to `[S, k]`") but the base case itself just defers to Step 2. The two worked examples (text content at depth 2) rely on the m = 2 form — the most important practical case — and the derivation reads as if m = 2 is a corner.

**Required**: Either lead with the m = 2 case explicitly (showing the derivation directly at m = 2 with [S, k] notation), or restructure D-SEQ★'s statement so the canonical form at m = 2 is visible without unpacking degenerate notation.

### Issue 6: Cross-document disjointness chain — Case A's length-bound discharge is implicit

**ASN-0047, "Allocator hierarchy under documents" (Cross-document disjointness chain lemma)**: "*Case A — Prefix-comparable* (WLOG `e₁ ≺ e₂`, so `#e₁ < #e₂`)… Position-divergence at index `#e₁+1 ≤ min(#p₁, #p₂)` witnesses `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` by Prefix."

**Problem**: The bound `#e₁ + 1 ≤ min(#p₁, #p₂)` is asserted without derivation. `#p₁ = #e₁ + 2` and `#p₂ = #e₂ + 2` are not stated; the reader must infer them from the prefix shape `[eᵢ.0.s]`. While straightforward, the bound's validity is load-bearing for invoking Prefix's positional-disagreement clause.

**Required**: Make `#p₁ = #e₁ + 2` and `#p₂ = #e₂ + 2` explicit and derive `#e₁ + 1 ≤ #e₁ + 2 ≤ #e₂ + 2` (using `#e₁ ≤ #e₂` from `e₁ ≺ e₂`) so the position-divergence index sits inside both prefixes.

## OUT_OF_SCOPE

### Topic 1: Mechanism specification for the node-allocation registry

**Why out of scope**: The ASN's own Open Questions section asks "What is the minimal protocol that a node-allocation registry must implement to satisfy NodeUniqueAllocation?" The registry mechanism (issuing protocol, persistence model, concurrency discipline) is deferred. Issue 4 above asks for the abstraction boundary to be made cleaner within this ASN; the mechanism itself remains future work.

### Topic 2: Link withdrawal mechanism reconciling with D-CTG★ / D-MIN★

**Why out of scope**: K.μ⁻ under D-CTG★/D-MIN★ admits only link-subspace suffix truncations, preventing interior link withdrawal. The ASN's Open Questions identify this as a deferred design question (tombstoning per Nelson LM 4/9). Not a flaw of the present ASN.

### Topic 3: Concurrent operations on the same home document for link allocation

**Why out of scope**: SequentialTransitionAxiom commits to total ordering of transitions. Concurrency is explicitly deferred per the Open Questions.

### Topic 4: Account-level depth-1 tumbler extension (K.δ k = 1 with IsAccount(t))

**Why out of scope**: The ASN excludes this at the K.δ k = 1 precondition (`t ∈ E_doc`) and records the question in Open Questions for future relaxation. Not relevant to the present ASN's correctness.

### Topic 5: Transitive provenance under chains of transclusion

**Why out of scope**: P4★/P4a record direct content-subspace containment events. Transitive provenance (when a is in d which transcludes from d') is a deferred question and is not in scope for the transition model.

VERDICT: REVISE
