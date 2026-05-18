# Review of ASN-0047

## REVISE

### Issue 1: K.δ k = 0 maximality conjunct conflates allocator sub-streams

**ASN-0047, K.δ case (ii) k = 0 sub-case**: "`t = max{t' ∈ E : parent(t') = parent(e) ∧ zeros(t') = zeros(t)}`"

**Problem**: The maximality conjunct takes lex-max over T4b-children sharing `parent(e)` and `zeros(t)`. But T4b-parent groups together entities from *different* allocator sub-streams. Concrete counterexample under account A = [1.0.1]:
- d₁ = [1.0.1.0.1] (document)
- d₂ = [1.0.1.0.2] (sibling document, allocated via K.δ k=0 from d₁)
- d₁.1 = [1.0.1.0.1.1] (version of d₁, allocated via K.δ k=1 from d₁)

All have T4b-parent = A and zeros = 2. Lex compare d₂ and d₁.1: agree on positions 1-4; at position 5, d₂ has 2 > 1 = d₁.1's value. So d₂ > d₁.1, and lex-max over {d₁, d₂, d₁.1} = d₂.

Once d₂ ∈ E, K.δ k = 0 with t = d₁.1 (intended to allocate d₁.2 = [1.0.1.0.1.2]) fails the maximality conjunct (max forces t = d₂, not d₁.1). Other routes to d₁.2:
- K.δ k = 1 with t = d₁: T10a per-(t, 1) uniqueness blocks (already fired producing d₁.1)
- K.δ k = 1 with t = d₁.1: produces inc(d₁.1, 1) = [1.0.1.0.1.1.1], not d₁.2
- K.δ k = 0 with t = d₂: produces d₃ = [1.0.1.0.3], not d₁.2
- K.δ k = 2: produces zeros = zeros(t)+1, never zeros = 2 from a zeros-2 operand

So d₁.2 = [1.0.1.0.1.2] becomes unreachable via any K.δ case once d₂ exists. The prose invokes "*the* parent allocator's sibling stream" (singular) and frames t as the "frontier", but the math allows multiple streams under the same T4b-parent. This contradicts Nelson's CREATENEWVERSION (LM 4/29) and Gregory's `docreatenewversion`, both of which admit repeated versioning of any document independent of sibling-document allocation.

**Required**: Sharpen the maximality conjunct to be allocator-specific. Options: (a) add `#t' = #t` to separate sub-streams by depth — since K.δ k=0 preserves length (TA5(c)), this aligns with the per-allocator partition; (b) replace maximality with `inc(t, 0) ∉ E` directly — inc is invertible at sig(t), so t is uniquely determined by e, making maximality structurally unnecessary; (c) document the restriction as an Open Question if intentional. The current formulation creates a reachability gap that an alternative implementation would not need to satisfy.

### Issue 2: Matrix entry for S3★ under K.μ~ misorders the dependency

**ASN-0047, ExtendedReachableStateInvariants verification matrix, S3★ row, K.μ~ column**: "both clauses preserved via decomposition + link-subspace fixity"

**Problem**: The "+ link-subspace fixity" suggests fixity contributes to S3★ preservation. But the K.μ~ section establishes that subspace preservation (used to derive link-subspace fixity) is *itself* derived from S3★(Σ'): "were π to map a content-subspace v to s_L, the post-state would have `M'(d)(π(v)) ∈ dom(C) ∩ dom(L) = ∅`, contradicting L14". The actual dependency order is: (1) S3★(Σ') from K.μ⁻ + K.μ⁺ decomposition alone (K.μ⁻ restricts, K.μ⁺ amended adds only content-subspace positions); (2) subspace preservation from S3★(Σ'); (3) link-subspace fixity from subspace preservation + K.μ~-FIX + CL-UNIQ. The matrix collapses this into "decomposition + fixity", giving fixity prerequisite status when it is actually a derived consequence.

**Required**: Reword to "both clauses preserved via decomposition" without invoking fixity, or restate the K.μ~ subspace-preservation argument to derive subspace preservation directly from the K.μ⁻/K.μ⁺ amendments (K.μ⁺ amended can only add s_C positions; K.μ⁻ doesn't add positions; surviving positions retain their subspace by frame). This breaks the apparent circularity.

### Issue 3: D-SEQ★ derivation Step 2 leaves m = 2 specialisation implicit

**ASN-0047, D-SEQ★ derivation, Step 2**: "Restricted to terminal-varying tuples `[S, 1, ..., 1, k]`, the V-ordering coincides with the natural order on `k`."

**Problem**: Step 1 base case (m = 2) correctly notes that the inner-positions claim is vacuous. But Step 2's prose uses the `[S, 1, ..., 1, k]` form throughout, which degenerates to `[S, k]` at m = 2 only by silent collapse of the "1, ..., 1" segment of length m − 2 = 0. The reader must infer that Step 2 applies uniformly, and that v_max = [S, 1, ..., 1, k_max] reduces to v_max = [S, k_max] at m = 2. The base case prose explicitly states the m = 2 form (`V_S(d) = {[S, k] : 1 ≤ k ≤ n_S}`), but Step 2 doesn't restate this — it proceeds with general-m notation only.

**Required**: Either rewrite Step 2 to handle m = 2 and m ≥ 3 explicitly (the m = 2 specialisation has empty inner range, so v_min = [S, 1] and v_max = [S, k_max] without "..." segments), or add a brief reminder at Step 2's outset that the `[S, 1, ..., 1, k]` notation degenerates at m = 2.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism with interior tombstoning
**Why out of scope**: K.μ⁻'s suffix-only restriction (forced by D-CTG★/D-MIN★) prevents interior link withdrawal. The Open Questions section correctly flags this; tombstoning would require a separate mechanism (status flag, marker link, etc.) outside K.μ⁻'s presentational-removal contract.

### Topic 2: Allocator activation protocol details beyond NodeUniqueAllocation
**Why out of scope**: NodeUniqueAllocation is the axiomatic boundary between the docuverse layer and the node-registry layer. Implementation details (issuing protocol, persistence model, concurrency discipline) are appropriately deferred. The Open Questions section flags this.

### Topic 3: Element-field depth beyond #E(a) = 2 for content addresses
**Why out of scope**: K.α uses A_C(d)'s sibling-increment chain, producing #E(a) = 2 for all content addresses. Support for deeper E-fields (#E(a) ≥ 3) would require K.α to invoke inc(·, k) with k > 0 within the content sub-allocator, which is not part of this ASN's scope.

VERDICT: REVISE
