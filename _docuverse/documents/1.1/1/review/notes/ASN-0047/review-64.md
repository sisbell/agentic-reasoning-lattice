# Review of ASN-0047

## REVISE

### Issue 1: Foundation S8 precondition cannot be discharged in extended state
**ASN-0047, ExtendedReachableStateInvariants proof, multiple sites (K.μ⁺, K.μ⁻, K.μ~ cases):** "S8 holds at the post-state by *S8 (Finite span decomposition)* of ASN-0036, applied at Σ'... S3 is supplied by the stronger S3★ established above"
**Problem:** ASN-0036's S8 names S3 (all V-positions target dom(C)) as a precondition. S3★ does NOT subsume S3 in the extended state — link-subspace V-positions target dom(L), which directly violates S3. The handwave "S3 is supplied by S3★" is wrong for the link subspace.
**Required:** Either (a) explicitly restate S8 for the extended state with S3★ in place of S3, verifying the proof carries through to link-subspace correspondence runs; (b) scope S8 to the content subspace only; or (c) provide separate verification for link-subspace correspondence runs invoking L1 + L1b in place of S7b + S7c.

### Issue 2: K.μ⁻ case analysis routing in case (b) is obscure
**ASN-0047, K.μ⁻ precondition, case (b):** "The complementary subcase — `k₀` removed, some `k' > k₀` retained, but *no* `k'' < k₀` retained — implies every index strictly below `min{k : [S, 1, ..., 1, k] ∈ V_S(d')}` is removed; since `1 ≤ k₀ < min{k : ...}`, the index 1 lies in that removed range, so `[S, 1, ..., 1, 1]` is itself removed. That subcase therefore falls under (c) below..."
**Problem:** The three-case split is correct but the routing argument is buried in a parenthetical. A reader has to reconstruct what "case (b) proper" excludes and what gets routed to (c). The exhaustiveness — that every non-suffix removal falls under (b) or (c) — is verified only by these implicit splits.
**Required:** Either consolidate the case analysis into a cleaner partition (e.g., (a) suffix removal admissible; (b) any removal leaving a hole — covering both interior and prefix violations) or factor the subcase routing out as a labeled lemma so exhaustiveness is explicit.

### Issue 3: J0 declared axiomatic but missing from axiom catalogue
**ASN-0047, Coupling and isolation, J0:** "This is an axiom of the state transition model, not a theorem of ASN-0036."
**Problem:** J0 is load-bearing — P7a's derivation depends on it, and the ASN distinguishes axiomatic J0 from derived J1 explicitly ("J0 is *axiomatic*... J1★ is *derived*"). But the *Properties Introduced* table lists J0 under "new properties" without flagging its axiomatic status, and the load-bearing-axiom enumeration in the body (SC-NEQ, NodeUniqueAllocation, NodeLineage, SubAllocatorAxiom, NoDeallocation, S0) does not mention J0.
**Required:** Add J0 to the named axiom catalogue alongside the other load-bearing axioms, with the same "stands alongside..." language used for SC-NEQ etc.

### Issue 4: Worked-example invariant labels use four-component forms instead of starred forms
**ASN-0047, Worked example: fork with subsequent insertion:** Verification lines use `P4` and `Contains(Σ)` rather than `P4★` and `Contains_C(Σ)`.
**Problem:** The example illustrates this ASN's elementary transitions and is presented as part of the *extended-state* discussion (after K.λ, S3★, etc. are introduced). The labels should be the extended-state forms. The example happens to be in a content-subspace-only state where P4 and P4★ coincide, but using the original labels obscures the per-state invariant set the example is meant to demonstrate.
**Required:** Restate verification lines using P4★, P5★, Contains_C, J1★, J1'★, S3★ as appropriate; note that these reduce to the four-component-state forms because the example's arrangement is content-subspace-only.

### Issue 5: S4 verification for K.λ is one-line; cross-document disjointness chain not explicitly invoked
**ASN-0047, ExtendedReachableStateInvariants proof, "Foundation invariants previously implicit," S4 entry:** "Each K.α produces `a` via the T10a allocator under origin(a) (S7a, ASN-0036)... K.λ produces `ℓ` via the inc chain under origin(ℓ), with GlobalUniqueness giving `ℓ ∉ dom(L) ∪ dom(C)` (jointly with L14)."
**Problem:** S4 requires distinctness across *all* allocation events globally, not just within a single allocator's domain. For K.λ, distinctness across documents (two K.λ events under different documents producing different ℓ) requires the *Cross-document disjointness chain* lemma, not bare GlobalUniqueness on a single allocator. The K.λ first-link case additionally requires SubAllocatorAxiom (T10a alone is insufficient at first emission). The verification elides both.
**Required:** Expand the S4 K.λ verification to explicitly cite SubAllocatorAxiom for first-emission cases and the Cross-document disjointness chain lemma for cross-document cases, paralleling the depth given to K.α + S7a.

### Issue 6: K.δ ghost-base discharge wording understates the gate
**ASN-0047, K.δ Scope and base-liveness paragraph:** "Discharge of `e ∉ E` in the ghost-operand case proceeds via the K.δ precondition itself rather than via T10a... TA5 (ASN-0034) supplies the structural fact that `inc(t, 1) = t.1` is deterministically determined by t..."
**Problem:** TA5 supplies the candidate address; it does not supply freshness. The actual discharge of `e ∉ E` is the K.δ precondition checked against the current entity set by inspection. The phrasing "K.δ precondition + TA5 determinism" reads as if these two together produce freshness, but TA5's contribution is only structural — naming what address to check.
**Required:** Rephrase to "K.δ precondition `e ∉ E` is verified by inspection against the current entity set, where TA5 determines the candidate address `inc(t, 1) = t.1` from t alone." Apply the same correction in the *ghost-base document versioning* worked example, Step 1 precondition discharge.

### Issue 7: D-CTG★ closed-interval definition has implicit dependencies
**ASN-0047, Amendments to existing transitions, D-CTG★:** "*contiguous* unpacks as closed-interval membership: for every `v_lo, v_hi ∈ V_S(d)` and every depth-m_S positive tuple `z`..."
**Problem:** The closed-interval formulation references `m_S` and "positive tuple" — these depend on S8-depth and S8a respectively. The amendment definition introduces D-CTG★ without explicitly noting these dependencies, which matters because the K.μ⁻ admissibility case analysis (case b interior removal) cites the closed-interval form before the per-state derivation of D-SEQ★ (which collects all four together).
**Required:** Add a one-line dependency note to D-CTG★'s definition: "Reading: `m_S` is fixed per non-empty subspace by S8-depth; 'positive tuple' is the S8a-compatible domain of V-positions." Without this, the closed-interval form is only well-defined once S8-depth and S8a have been established.

### Issue 8: ExtendedReachableStateInvariants does not verify P4★ behavior across composite boundary in the interior-replacement worked example
**ASN-0047, Worked example: interior content replacement, *Composite verification at Σ → Σ'*:** Lists P4★ verification as "Contains_C(Σ') ⊇ {...}; each pair is in R'."
**Problem:** The example's strength is exhibiting the asymmetric J1★/J1'★ handling of re-added addresses. But P4★ at the intermediate state M_int (after K.μ⁻, before K.μ⁺ + K.ρ) is not exhibited. At M_int, `Contains_C(Σ_int) ⊂ Contains_C(Σ) ⊆ R = R_int`, so P4★ is preserved — but this is the crux of how the elementary K.μ⁻ + K.μ⁺ + K.ρ sequence stays consistent with P4★ even though J1★ is only checked at the composite boundary. Missing the intermediate-state check obscures why the composite, not the elementary K.μ⁺ alone, is what J1★ governs.
**Required:** Add a P4★-at-M_int verification line ("Contains_C(M_int) ⊆ R holds because K.μ⁻ can only shrink Contains_C and R is unchanged"). Same pattern in the link-allocation example Step 3's K.μ~ M_int verification.

### Issue 9: K.μ~ contract bijection ambiguity under S5 transclusion not addressed
**ASN-0047, Decomposition of K.μ~, contract:** "(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))"
**Problem:** ASN-0036 S5 (UnrestrictedSharing) admits multiple V-positions in M(d) mapping to the same I-address. Under such sharing, multiple bijections π can satisfy the contract equation (any permutation of the V-positions sharing a given target). The decomposition proof's claim "Write `vᵢ = π(uᵢ)` for unique `uᵢ`" uses π's bijectivity to identify the inverse, which is fine — but the contract itself does not pick out a canonical π. This is benign for the post-state M'(d) (which is uniquely determined by the multiset structure) but obscures whether the contract is a relation on (Σ, Σ') or specifies the choice of π.
**Required:** Either explicitly note that the contract specifies (Σ, Σ') pairs and π is existentially quantified (any witness suffices), or restrict the contract to settle π canonically (e.g., the identity on shared-target sub-permutations). Currently the under-determination is silent.

## OUT_OF_SCOPE

### Topic 1: Account-level versioning semantics (k=1 with IsAccount(t))
**Why out of scope:** The ASN explicitly excludes account-level depth-1 extension and defers the question to the Open Questions section. The structural form `[N, 0, U, 1]` is well-typed; admitting it would require future design work on account-version semantics. The exclusion is a deliberate scope decision, properly recorded.

### Topic 2: Link withdrawal mechanism and tombstoning
**Why out of scope:** Nelson's "not currently addressable" link withdrawal (LM 4/9) is not expressible as K.μ⁻ under D-CTG★. The ASN names this as a structural gap, documents it in *Structural sufficiency and known gaps*, and defers the resolution to a future ASN with explicit per-link liveness or tombstone state.

### Topic 3: Version-management invariants (relationship between version lineage and arrangement transitions)
**Why out of scope:** K.δ admits depth-1 tumbler extension (versioning) at the document level but leaves the version-arrangement contract — what arrangement invariants must hold between successive versions, content-allocator linkage, provenance flow across versions, version-lineage acyclicity — to a subsequent ASN. The deferral is explicit.

### Topic 4: Non-T10a allocator admissibility for content/links/non-node entities
**Why out of scope:** The ASN's elementary set assumes T10a-conforming allocation. Implementation-specific address reuse or externally-injected non-inc-derived addresses would require a separate axiomatization. The exclusion is named in *Structural sufficiency and known gaps*.

VERDICT: REVISE
