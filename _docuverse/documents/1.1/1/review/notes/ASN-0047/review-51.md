# Review of ASN-0047

## REVISE

### Issue 1: CL-UNIQ is not preserved by K.μ⁺_L
**ASN-0047, K.μ⁺_L definition and Link-subspace ownership (CL-UNIQ proof)**: K.μ⁺_L's precondition admits the same link ℓ being arranged at multiple V-positions.

**Problem**: The precondition checks `v_ℓ ∉ dom(M(d))` but not `ℓ ∉ ran(M(d))`. Concrete violation:
- Σ₀: M(d) = {[s_L, 1] ↦ ℓ_1}
- Apply K.μ⁺_L with target = ℓ_1 at v_ℓ = shift([s_L, 1], 1) = [s_L, 2]
- All preconditions hold: d ∈ E_doc, ℓ_1 ∈ dom(L), origin(ℓ_1) = d, subspace([s_L, 2]) = s_L, [s_L, 2] = shift(max(V_{s_L}(d)), 1), [s_L, 2] ∉ dom(M(d))
- Result: M'(d) = {[s_L, 1] ↦ ℓ_1, [s_L, 2] ↦ ℓ_1} — two positions mapping to ℓ_1

The CL-UNIQ inductive proof asserts "this duplicate-add scenario is precluded by the K.μ⁺_L admissibility on `v_ℓ ∉ dom(M(d))`", but this premise only excludes V-position reuse, not link-value reuse. The proof step that handles "pre-state had one" simply dismisses the case as "contradicting our inductive aim" without showing impossibility.

**Required**: Add precondition `ℓ ∉ ran(M(d))` to K.μ⁺_L (or equivalent constraint ensuring first-arrangement). This propagates to the redundancy argument for K.μ~'s link-subspace identity clause, which depends on CL-UNIQ at the output state.

### Issue 2: ASN-0047's L3 contradicts ASN-0043's L3 (foundation)
**ASN-0047, Link store and extended system state, L3**: "ASN-0043's non-empty type-endset clause (`Σ.L(a).e₃ ≠ ∅`) is dropped."

**Problem**: ASN-0043's L3 (foundation): `(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ ... ∧ Σ.L(a).e₃ ≠ ∅)`. ASN-0047 claims its L3 is "a stronger property than the foundation's" but the empty-Θ relaxation is strictly weaker. The ASN's L3 is incomparable with the foundation's — states satisfying ASN-0047's L3 (e.g., with `(F, G, ∅)`) violate ASN-0043's L3. Foundation invariants are listed as verified and stable; a downstream ASN cannot relax them.

**Required**: Either keep ASN-0043's non-empty constraint (require `Θ ≠ ∅`), or propose this as an ASN-0043 revision before relying on it here. The downstream L8 domain-restriction discussion compounds the same problem.

### Issue 3: Worked example notational error in K.μ⁻ counterfactual
**ASN-0047, Step 5 (counterfactual)**: "min(V_{s_L}(d')) = [s_L, 1, 1, 2] ≠ [s_L, 1, 1, 1] = [s_L, 1, ..., 1] of depth m_{s_L} = 2"

**Problem**: At m_{s_L} = 2, the form `[S, 1, ..., 1, k]` collapses to `[S, k]` — no intermediate 1's. The expressions `[s_L, 1, 1, 2]` and `[s_L, 1, 1, 1]` have depth 4, not 2. The example's pre-state shows `V_{s_L}(d) = {[2,1], [2,2]}` (depth 2), so the surviving position after the counterfactual would be `[2, 2]`, and the violated D-MIN★ target is `[2, 1]`.

**Required**: Correct to `min(V_{s_L}(d')) = [2, 2] ≠ [2, 1] = [s_L, 1] of depth m_{s_L} = 2`.

### Issue 4: S0 and S1 are per-transition properties listed in the per-state theorem
**ASN-0047, ExtendedReachableStateInvariants**: "S0 ∧ S1 ∧ S2 ∧ S3★ ∧ ..."

**Problem**: ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) are universally quantified over transitions `Σ → Σ'` — properties of the transition system, not of a single state. They cannot meaningfully appear in a per-state conjunction. The companion theorem ExtendedTransitionInvariants correctly captures per-transition properties (P0, P1, P2, P3★, P5★, L12), and S0 (≡ P0) and S1 (≡ part of P0) belong there instead.

**Required**: Move S0, S1 to ExtendedTransitionInvariants, or explicitly redefine what "state Σ satisfies S0" means in this context.

### Issue 5: P4a is not adapted to the extended state
**ASN-0047, P4a (Historical fidelity)**: Stated before the extended state, derived using J1'.

**Problem**: In the extended state, J1' is replaced by J1'★ (content-subspace scoped). P4a's derivation cites J1' directly. The theorem is not re-derived or re-stated, leaving its status in the extended state unclear — does P4a still hold, and under what reading (any past arrangement, or specifically content-subspace arrangement)?

**Required**: Either re-derive P4a in the extended state with J1'★, or restate it as a corollary of the inductive proof.

### Issue 6: NodeUniqueAllocation does not constrain node hierarchy structurally
**ASN-0047, K.δ case (i) and NodeUniqueAllocation axiom**: "No parent is required... The Xanadu design admits node creation beyond the bootstrap n₀."

**Problem**: K.δ for `IsNode(e)` admits any T4-valid e with `zeros(e) = 0` and `e ∉ E`. The axiom guarantees `e ∉ E` but imposes no structural relation between e and existing nodes. The cited protocol mechanisms (Nelson's baptism, Gregory's granfilade) all require new nodes to descend from a single root — but the abstract axiom captures only namespace uniqueness, not lineage. Without a structural constraint, the abstract model permits arbitrary, unrelated node addresses.

**Required**: Either add a lineage axiom (e.g., new nodes share a prefix with n₀), or explicitly state that node lineage is out of scope and document the consequence (e.g., that nodes form an unstructured collection at the abstract level).

### Issue 7: Bootstrap node n₀ is underspecified
**ASN-0047, Initial state definition**: "E₀ = {n₀} for a designated bootstrap node n₀ with IsNode(n₀)."

**Problem**: The structural form of n₀ (whether single-component `[1]`, multi-component `[1.1]`, etc.) is unspecified. This affects what subsequent K.δ node allocations can validly produce, and what cross-node disjointness arguments can rely on. The ASN says "The choice of n₀ is a system parameter" but doesn't bound the choice.

**Required**: At least bound n₀ structurally (e.g., "n₀ is any T4-valid tumbler with zeros(n₀) = 0"); ideally state whether multi-component n₀ is admissible and what the consequence is for future node allocations.

### Issue 8: K.μ~ frame is stated as "derived below" without inline derivation
**ASN-0047, K.μ~ definition**: "Frame (derived below): C' = C; E' = E; R' = R; ..."

**Problem**: The frame is asserted at the definition site but the derivation appears in the K.μ⁻ + K.μ⁺ decomposition section that follows. This creates a forward dependency for readers and obscures whether the frame is part of K.μ~'s contract or follows from decomposition. Compare with K.μ⁺_L's frame, stated directly.

**Required**: Either state the frame as part of K.μ~'s contract (and prove it from the decomposition), or note explicitly that K.μ~ has no independent frame and inherits everything from its decomposition.

### Issue 9: Decomposition of K.μ~ over-restricts the choice of intermediate state
**ASN-0047, K.μ~ decomposition Case 3**: "The K.μ⁻ step. Remove V_{s_C}(d) entirely from M(d) — i.e., full content-subspace clearance with n'_{s_C} = 0."

**Problem**: The ASN's decomposition uses full content-subspace clearance for every non-trivial K.μ~. This produces a valid decomposition, but it suggests K.μ~ must always clear everything and rebuild — when in practice, many useful reorderings (e.g., swapping two specific positions) could be decomposed more economically. More importantly, the proof of intermediate-state admissibility verifies a specific decomposition shape, not "some valid decomposition exists for any π." This conflates existence with construction.

**Required**: Either prove that for every valid bijection π there exists SOME admissible decomposition (not just the full-clearance one), or explicitly state that K.μ~ is defined as "full clear-and-rebuild of the content subspace" semantically (so the bijection π and the decomposition are tightly coupled).

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
The ASN flags this as an open question. The tension between D-CTG★ and Nelson's tombstoning is acknowledged, and resolution is properly deferred.

### Topic 2: Version semantics for k = 1
The ASN admits the k = 1 case structurally and defers semantic richness (sequential lineage, version-derivation invariants, etc.) to a future version-management ASN. Properly out of scope.

### Topic 3: Account-level depth-1 extension
The ASN excludes this at the K.δ precondition with documented justification (Nelson reserves versioning to documents). Whether to admit it is appropriately open.

### Topic 4: Discovery-layer same_type domain
The L8 (TypeByAddress) domain restriction question, while raised by L3's empty-Θ admission, belongs to a discovery-layer ASN. (However, see Issue 2 — the underlying L3 inconsistency with the foundation must be resolved here, even if the discovery-layer consequences are deferred.)

VERDICT: REVISE
