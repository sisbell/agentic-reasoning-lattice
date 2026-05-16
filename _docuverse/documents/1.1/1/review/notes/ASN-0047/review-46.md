# Review of ASN-0047

## REVISE

### Issue 1: TA5 sub-clause miscitation in K.λ first-link case
**ASN-0047, Link allocation**: "ℓ = inc(t, 1) = [d.0.s_L.1] — descent into the element subspace by TA5(b)"
**Problem**: TA5(b) is the agreement clause (preservation of positions 1..#t). The "append `.1`" structure is established by TA5(d), which states for k > 0: "#t' = #t + k, positions #t + 1 ... #t + k - 1 are 0, position #t + k is 1". Citing TA5(b) alone is wrong — TA5(b) does not establish the appended-position structure.
**Required**: Cite TA5(d) (or TA5(b)/TA5(d) like K.δ does) at the k = 1 appendage. Also clarify K.δ's "Descent case (k ∈ {1, 2}, TA5(b)/TA5(d))" — k = 1 (TA5(b)) appends `.1` is misleading since TA5(b) at k > 0 is the agreement clause, not the append clause.

### Issue 2: NodeUniqueAllocation not formally introduced as axiom
**ASN-0047, K.δ entity creation**: "treats the resulting `e ∉ E` as the operative axiom (NodeUniqueAllocation)"
**Problem**: NodeUniqueAllocation is named as an axiom load-bearing for K.δ on nodes — it closes the GlobalUniqueness chain for nodes where T10a's discipline does not apply. But it is mentioned only in parenthesis without a labeled definition like SC-NEQ receives. The ASN explicitly elevates SC-NEQ to axiom status ("stands alongside NoDeallocation and S0 as a load-bearing axiomatic premise") and should treat NodeUniqueAllocation with the same care.
**Required**: Formally introduce NodeUniqueAllocation in a labeled definition with the same structure used for SC-NEQ, listing its load-bearing role and stating it as an axiomatic premise of the abstract specification.

### Issue 3: D-SEQ★ derivation hand-waves on inner-1 components
**ASN-0047, Amendments**: "the unique contiguous range of length n_S starting at [S, 1, ..., 1] under that ordering with all-1 inner components and varying terminal component is `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`"
**Problem**: The claim that inner components must all be 1 is asserted without derivation. The required argument: if some `v ∈ V_S(d)` has `v_j ≥ 2` at minimal `j` with `2 ≤ j ≤ m_S - 1`, then between `[S, 1, ..., 1]` and `v` lie positions `[S, 1, ..., 1, 1, M, 1, ..., 1]` for every `M ∈ ℕ⁺` at position `j+1`, all forced into `V_S(d)` by D-CTG★, contradicting S8-fin. The derivation says "parallels ASN-0036's derivation of D-SEQ for V_1(d)", but ASN-0036's argument relies on D-CTG-depth, which is stated for V_1 specifically. The generalization to arbitrary S requires either explicit derivation here or a derived per-subspace D-CTG-depth.
**Required**: Either spell out the infinite-cardinality contradiction explicitly, or derive a per-subspace D-CTG-depth analog and invoke it in the D-SEQ★ derivation.

### Issue 4: K.δ "descent" terminology conflates k=1 and k=2
**ASN-0047, K.δ entity creation**: "Descent case (k ∈ {1, 2}, TA5(b)/TA5(d))"
**Problem**: For k = 1, `zeros(e) = zeros(t)` — e is at the *same hierarchical level* as t (sibling at deeper tumbler depth, the version case). For k = 2, `zeros(e) = zeros(t) + 1` — e is at the next level down (true descent). Lumping these as "Descent case" obscures the structural distinction. The version-semantics note acknowledges that the version-to-base relationship "lies outside the entity-hierarchy spine that P8 governs", confirming that k = 1 is not descent in the zeros-count sense. Subsequent references to "descent" elsewhere in the ASN may inherit this confusion.
**Required**: Either split into "Sibling-at-deeper-tumbler-depth (k = 1)" and "Descent (k = 2)" cases with separate descriptions, or retain the joint label but clearly state that "descent" here means tumbler-depth descent (length extension), not zeros-count descent.

### Issue 5: K.μ⁻ frame in extended state does not explicitly include L
**ASN-0047, K.μ⁻**: "*Frame:* C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))."
**Problem**: This frame is stated at the operator's original definition site, before the link store is introduced. In the extended state Σ = (C, L, E, M, R), K.μ⁻ must also hold L in frame. The ExtendedReachableStateInvariants proof says "For K.μ⁻: holds L in frame" but the operator definition is never updated. The K.μ⁻ amendment section confirms multi-subspace behavior but does not extend the frame statement to include `L' = L`. The same omission affects K.α (C-side amendment only addresses subspace), K.δ, K.μ⁺, K.μ~, K.ρ — none of their frame statements are explicitly updated in the Amendments section.
**Required**: Add an explicit statement at the K.μ⁻ amendment (and equivalents for other transitions in the Amendments section) extending the frame to include `L' = L`, parallel to how K.λ's frame `(A d' :: M'(d') = M(d'))` and K.μ⁺_L's frame `L' = L` are stated.

### Issue 6: ExtendedReachableStateInvariants theorem missing several invariants
**ASN-0047, ExtendedReachableStateInvariants**: "Every state reachable ... satisfies: S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN"
**Problem**: Several foundation invariants are preserved by valid composites but not listed in the conjunction: L1b (LinkElementFieldDepth — preserved by K.λ's structural preconditions and L12); S7a, S7b, S7c, S7d (preserved by K.α's preconditions); S4 (OriginBasedIdentity — preserved by allocation discipline); S9 (TwoStreamSeparation — derived from S0 + arrangement frames); D-SEQ★ (derived from D-CTG★ + D-MIN★ + S8-*). The theorem claims comprehensive coverage of reachable-state invariants; omitting these leaves the theorem incomplete and weakens its load-bearing role as the central correctness claim.
**Required**: Either extend the conjunction to include the missing invariants with verification in the proof, or explicitly state which invariants are out of scope for this theorem and why.

### Issue 7: K.μ⁻ admissibility precondition references D-SEQ★ before its derivation
**ASN-0047, K.μ⁻ definition**: "by D-SEQ★ at the input state (per-subspace, derived below), each non-empty subspace has V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}"
**Problem**: The K.μ⁻ admissibility precondition appeals to a structural form named D-SEQ★ that is derived later in the Amendments section. The ASN acknowledges this is "intentional" — the operator's contract must be stated before the derivation — but the self-containedness claim ("a structural property established self-containedly in this precondition by the conjunction of D-CTG, D-MIN, S8-depth, S8-fin, and S8a") is weakened by the same gap noted in Issue 3: D-SEQ★ itself is not fully derived from these five properties without invoking a D-CTG-depth analog for non-text subspaces.
**Required**: Either complete D-SEQ★'s derivation (per Issue 3) so the self-contained claim holds, or restate K.μ⁻'s precondition without forward reference to a named theorem (state the structural form directly without claiming it is "D-SEQ★").

### Issue 8: Treatment of K.μ⁻ removing a per-subspace prefix vs suffix
**ASN-0047, K.μ⁻ definition**: "the removed positions, partitioned by subspace, form a suffix of each subspace's range"
**Problem**: The admissibility specification asserts suffix removal but does not derive why prefix removal (removing the minimum and contiguous positions above it) is forbidden. The implicit argument is: removing `[S, 1, ..., 1]` while retaining `[S, 1, ..., 1, k]` for `k ≥ 2` produces `min(V_S(d')) = [S, 1, ..., 1, 2]`, violating D-MIN★'s requirement that `min(V_S(d')) = [S, 1, ..., 1]` of depth m_S. But D-MIN★ is *required at the post-state*, and a contraction that violates it would not satisfy the K.μ⁻ admissibility derivation — yet the ASN never explicitly says "prefix removal violates D-MIN★ at the output". The derivation that suffix removal is necessary (not merely sufficient) is missing.
**Required**: Add explicit argument that prefix removal would violate D-MIN★ at the output state, completing the case analysis on admissibility (suffix removal sufficient, prefix removal forbidden, interior removal forbidden by D-CTG★).

### Issue 9: K.μ~ degenerate case clarification on link-subspace-only arrangements
**ASN-0047, K.μ~**: "When π = id — including the case dom(M(d)) = ∅ (empty bijection) and the case dom(M(d)) ≠ ∅ ∧ dom_C(M(d)) = ∅ (link-subspace-only arrangements, where link-subspace fixity forces π = id)"
**Problem**: The text argues that when dom_C(M(d)) = ∅, link-subspace fixity forces π = id. The argument cited is the K.μ⁻ + K.μ⁺ decomposition with `r = 0` derivation, but that derivation assumes π is given and shows link-subspace fixity follows. To conclude π = id from dom_C(M(d)) = ∅ alone, one must show that π's restriction to link-subspace positions is the identity, and then since dom(M(d)) = dom_L(M(d)) entirely, π is everywhere the identity. The chain "dom_C empty ⟹ all positions link-subspace ⟹ all permuted to identity by fixity ⟹ π = id" needs to be explicit rather than gestured at.
**Required**: Either prove this case directly (link-subspace fixity gives π|_{dom_L} = id, dom_C = ∅ implies dom = dom_L, so π = id everywhere) or remove the claim that π = id is forced in this case (the K.μ~ definition admits π = id by direct precondition without requiring derivation).

### Issue 10: K.λ first-link case requires a multi-step inc chain that is not fully derived
**ASN-0047, K.λ first link case**: "the link-prefix base is t = [d.0.s_L] — the single-component element-field address with `fields(t).E₁ = s_L`, itself reached from d by the chained inc applications underwriting L1c (k₁ = 2 from d into the element field, then k₂ = 0 sibling steps to advance the first element-field component to s_L)"
**Problem**: The chain `inc(d, 2)` gives `[d, 0, 1]` (element-field base with subspace identifier 1). To advance to `s_L`, the text says "k₂ = 0 sibling steps". But k₂ = 0 means sibling-in-place: inc([d, 0, 1], 0) = [d, 0, 2], inc([d, 0, 2], 0) = [d, 0, 3], etc. The chain length is `s_L - 1`. Moreover, [d, 0, 1] is the content allocator's *base*, which itself is not in dom(C) (content addresses have element field [1, k] with k ≥ 1, not just [1]). Whether [d, 0, 1] is "previously allocated" for T10a's inc to apply is ambiguous. The conceptual hierarchy — d → element-field allocator → content allocator + link allocator as sibling sub-allocators — is implicit but never formalized.
**Required**: Either formalize the allocator hierarchy under documents (parent element-field allocator, child content and link allocators), or explicitly state that the link-prefix base derivation assumes such a hierarchy and treat it as part of T10a-conformance.

## OUT_OF_SCOPE

(None — all topics covered remain within the abstract transition-model scope. Out-of-scope topics — operations, authorization, concurrency, version semantics, link withdrawal mechanism — are appropriately deferred to open questions.)

VERDICT: REVISE
