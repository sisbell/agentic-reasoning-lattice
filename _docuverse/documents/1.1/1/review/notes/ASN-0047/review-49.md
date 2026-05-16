# Review of ASN-0047

## REVISE

### Issue 1: `parent(e)` defined by informal pattern matching, not T4b projections
**ASN-0047, §The state model**: "If `IsAccount(e)` with form `N.0.U`, then `parent(e) = N`. If `IsDocument(e)` with form `N.0.U.0.D`, then `parent(e) = N.0.U`."
**Problem**: `parent` is load-bearing for P8 and the K.δ k=2 precondition, but the definition uses verbal pattern matching against tumbler shapes. T4b (UniqueParse) already supplies formal partial functions `N, U, D, E`. The current definition does not say what `parent` is as a function, only what its value would be on two specific structural forms.
**Required**: State `parent` using T4b. For `IsAccount(e)`, `parent(e) = N(e)`; for `IsDocument(e)`, `parent(e) = N(e).0.U(e)` (or the equivalent in terms of T4b's projections). Then `zeros(parent(e)) = zeros(e) − 1` becomes a derivable property, not a stipulation.

### Issue 2: L1b derivation in Foundation invariants misdescribes K.λ
**ASN-0047, ExtendedReachableStateInvariants proof, Foundation invariants subsection**: "K.λ's address construction via `inc(t, k)` chains (k₁ = 2 followed by k₂ = 0 sibling extensions in the first-link case, or k = 1 in subsequent cases) guarantees the link-prefix base t has #E(t) ≥ 1 and the link allocation step (inc(t, 1) for the first link, inc(prev, 0) for siblings) produces #E(ℓ) ≥ 2."
**Problem**: This contradicts K.λ's own definition. The first-link case in K.λ emits `ℓ = [d.0.s_L.1]` directly via SubAllocatorAxiom — no `inc(t, k₁=2)` step is invoked, and there are no "k₂ = 0 sibling extensions" before the first emission. The subsequent case uses `inc(t, 0)` (TA5(c)), not `k = 1`. Two of the three k-values cited are wrong.
**Required**: Rewrite the L1b discharge to match K.λ as defined. First-link case: `ℓ = [d.0.s_L.1]` has element field `[s_L, 1]`, so `#E(ℓ) = 2` by construction. Subsequent case: `ℓ = inc(prev, 0)` preserves `#E` from prev = 2 by TA5(c)'s length-preservation clause.

### Issue 3: L-fin proof attribution is wrong
**ASN-0047, §Link store and extended system state**: "ASN-0043 establishes L-fin by induction over K.λ (the only link-allocating elementary transition)..."
**Problem**: K.λ is an elementary transition introduced in *this* ASN. ASN-0043 contains no K.λ; whatever induction underwrites L-fin in ASN-0043 is over ASN-0043's own link-creation primitive. The proof sketch is then continued correctly *in this ASN's* model, so the substance is fine, but the attribution is incoherent.
**Required**: Drop the "ASN-0043 establishes..." sentence and present the induction as this ASN's own (which it is): base `dom(L₀) = ∅` finite; K.λ extends by one; all other transitions hold L in frame.

### Issue 4: K.μ⁻ case (b) gap argument fails when no position below `k₀` is retained
**ASN-0047, §Elementary transitions, K.μ⁻ admissibility, case (b)**: "[S, 1, ..., 1, k₀] lies strictly between min(V_S(d')) (some [S, 1, ..., 1, k_min] with k_min ≤ k₀) and [S, 1, ..., 1, k']..."
**Problem**: The parenthetical `k_min ≤ k₀` is not always true under the stated case (b) hypothesis ("any removal leaving any position above the removed position"). Counterexample: `n_S = 5`, remove `{1, 2}`, retain `{3, 4, 5}`, take `k₀ = 2, k' = 3`. Then `k_min = 3 > k₀ = 2`, so `[S, 1, ..., 1, k₀]` lies *below* `min(V_S(d'))`, not between it and `k'`. D-CTG★ does not fire on this pattern; D-MIN★ does. The case (b) argument as written does not cover this configuration.
**Required**: Either (i) split case (b) by whether some `k < k₀` is retained (so D-CTG★ catches the "true interior" subcase and D-MIN★ catches the "below-min" subcase), or (ii) restate (b)'s coverage and rely on (c) to discharge the remaining subcase explicitly. Currently (b) and (c) overlap on some configurations while jointly missing others without a stated argument.

### Issue 5: K.μ⁻ admissibility derivation invokes D-CTG before D-CTG★ exists
**ASN-0047, §Elementary transitions, K.μ⁻ admissibility derivation**: "We state and derive this structural form locally — relying only on the per-state invariants D-CTG, D-MIN, S8-depth, S8-fin, and S8a..."
**Problem**: K.μ⁻ is defined in §Elementary transitions, before §Amendments establishes D-CTG★/D-MIN★. At K.μ⁻'s definition site, D-CTG and D-MIN are ASN-0036's forms, which explicitly exempt the link subspace. The local derivation therefore establishes the structural form only for the text subspace, but K.μ⁻'s admissibility precondition is stated `(A S : V_S(d) ≠ ∅ : ...)` — quantified over all non-empty subspaces. In the five-component state the precondition is meaningless on V_{s_L}(d) under the cited invariants.
**Required**: Either defer K.μ⁻'s definition until D-CTG★/D-MIN★ are in scope, or have the local derivation appeal to the *strengthened* forms (with a forward pointer to where they are established) so that the per-subspace precondition is supported across both subspaces.

### Issue 6: Worked example "Step 2" header missing
**ASN-0047, §Worked example: link allocation and arrangement**: After "Post-state verification" of Step 1, the text proceeds directly into "Precondition verification:" for K.μ⁺_L without a header, then later jumps to "**Step 3: K.μ~ — reorder text...**"
**Problem**: A reader following the three-step structure cannot tell that the unlabeled paragraph block *is* Step 2. The verification check that K.μ⁺_L preserves L1b, L-fin, S7c, etc. lives inside this unlabeled block and is easy to miss when scanning.
**Required**: Insert "**Step 2: K.μ⁺_L — arrange the link in d.**" before the precondition verification.

### Issue 7: NodeUniqueAllocation handwaves "protocol-determined ancestor"
**ASN-0047, NodeUniqueAllocation axiom**: "every node address descends from a single root (the bootstrap node n₀, or its protocol-determined ancestor)..."
**Problem**: The axiom is the ASN's load-bearing premise for `e ∉ E` at every K.δ node event, but the "or its protocol-determined ancestor" clause is undefined. Σ₀ fixes a single bootstrap n₀; the structural mechanism the axiom invokes is a single-root descent tree under n₀. The "or its protocol-determined ancestor" phrasing introduces an unspecified second root option without saying what it is, who chooses it, or how it relates to n₀.
**Required**: Either drop the "or its protocol-determined ancestor" clause (the bootstrap-rooted descent already covers the cited Nelson/Gregory mechanisms) or define what such an ancestor would be and how the freshness property survives its introduction.

### Issue 8: K.δ k=1 "harmlessness" claim is sketched, not derived
**ASN-0047, §Elementary transitions, K.δ k=1 "Scope and harmlessness"**: "We claim that this omission is *harmless within this ASN's scope*: no invariant introduced in this ASN — P0–P8, S0–S9, L0–L14, J0–J4, D-CTG, D-MIN, D-SEQ, P3★, P7a, S3★, GlobalUniqueness, NodeUniqueAllocation, SubAllocatorAxiom — refers to a base-to-version relationship..."
**Problem**: The claim is then sketched at three invariants (P8, P1, S2/S3, T10a) and asserted for the rest. For a result this load-bearing — admitting `[N, 0, U, 0, D, k]` as a K.δ output when `[N, 0, U, 0, D]` ∉ E_doc, contrary to Gregory's `docreatenewversion` — a per-invariant check is warranted. In particular, P6 (origin coherence) for content allocated under such a version, and J0/J1★ when the version is freshly K.δ'd with content, are not addressed.
**Required**: Either complete the per-invariant check or scope the claim ("no invariant *of the entity-hierarchy and arrangement layers* refers to base-version") and acknowledge what is not checked.

### Issue 9: Transition properties mixed into per-state invariant theorem
**ASN-0047, ExtendedReachableStateInvariants**: "Every state reachable from Σ₀ ... satisfies S0 ∧ S1 ∧ S2 ∧ S3★ ∧ ... ∧ P3★ ∧ P4★ ∧ P5★ ∧ ..."
**Problem**: P3★ and P5★ are per-transition properties — their formal statements quantify over `(A Σ → Σ' :: ...)`. P0, P1, P2 likewise. Stating that a *state* "satisfies" a transition property is type-incorrect; one means that every transition *out of* the state preserves the property. The Reachable-state invariants theorem (four-component) makes the same conflation. The proofs do the right thing, but the theorem statement misdescribes what is established.
**Required**: Either split the theorem into per-state invariants and per-transition invariants, or recast P0/P1/P2/P3★/P5★ in per-state form (e.g., "every state's outgoing transitions preserve...") so that the conjunction is well-typed.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism reconciling D-CTG★ with Nelson's tombstoning
**Why out of scope**: The ASN flags the conflict between D-CTG★ (no link-subspace gaps) and Nelson's "not currently addressable" tombstone design, and defers the resolution to the explicit Open Question on withdrawal invariants. The deferral is appropriate; this is a follow-on ASN, not a defect in the current one.

### Topic 2: Multi-version sequencing and inheritance under K.δ with k=1
**Why out of scope**: Beyond admissibility (Issue 8), the questions about whether `[d, k]` requires `[d, k−1]`, whether content-allocators of base and version are linked, and how provenance flows across versions are listed in the Open Questions and reserved for a version-management ASN.

### Topic 3: Concurrent allocation discipline
**Why out of scope**: Whether two concurrent K.λ events can produce distinct addresses without coordination is flagged as an Open Question and overlaps with replication/BEBE — explicitly listed in the Scope exclusion.

### Topic 4: Specific operations (INSERT, DELETE, COPY, REARRANGE, MAKELINK)
**Why out of scope**: The Scope section excludes named operations. The ASN supplies the elementary transitions from which these compose; specifying the operations themselves is a downstream ASN.

VERDICT: REVISE
