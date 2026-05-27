# Review of ASN-0100

## REVISE

### Issue 1: Substrate model conflation (K.σ vs K.δ)
**ASN-0100, Substrate Decomposition & Frame Conditions**: "no K.δ or K.σ fires in the decomposition (dom(M) is governed via K.δ-IsDocument or K.σ for document registration; INSERT registers no new document and creates no new node, account, or non-document entity)"
**Problem**: ValidComposite★ (ASN-0047) admits K.δ but not K.σ in its transition vocabulary. ASN-0093 introduces K.σ as a *separate* document-registration operation. The ASN invokes ValidComposite★ (ASN-0047's composite framework) yet also references K.σ (ASN-0093). The reader cannot tell which substrate is operative — is K.σ part of the same vocabulary admitted by ValidComposite★, or is it a parallel mechanism? This affects what "no K.σ fires" means structurally.
**Required**: Pick one substrate model and use it consistently. Either (a) state INSERT operates over ASN-0047's vocabulary and remove K.σ references, or (b) state how ASN-0093's K.σ composes with ASN-0047's ValidComposite★ framework and justify why both are needed.

### Issue 2: K.μ⁻ omission case (i.b) argument elides a step
**ASN-0100, Substrate Decomposition step 2**: "(i.b) when V_{s_C}(d) = ∅ and V_{s_L}(d) ≠ ∅ — K.μ⁻'s dom(M(d)) ≠ ∅ precondition holds, but its strict-shrinkage clause (E S :: n'_S < n_S) cannot be satisfied without shrinking V_{s_L}(d), which would violate INS.frame.subspace"
**Problem**: The reasoning skips the load-bearing intermediate step. With n_{s_C} = 0, the retention parameter n'_{s_C} ∈ {0, …, n_{s_C}} = {0} is forced to 0 = n_{s_C} — no strict shrinkage possible in s_C. *Therefore* the strict-shrinkage clause requires n'_{s_L} < n_{s_L}, which violates frame.subspace. Without spelling out the forced equality on s_C, the reader cannot reconstruct the chain.
**Required**: Add the explicit step that n_{s_C} = 0 forces n'_{s_C} = 0, after which strict shrinkage is unavailable in s_C and must come from s_L if at all.

### Issue 3: Intermediate state invariant verification incomplete
**ASN-0100, Atomicity and Canonical Order**: "After step 2's K.μ⁻ (when fired). V_{s_C}(d_intermediate) reduces to the Left prefix..., which is sequential, contiguous, and starts at the minimum — D-SEQ★, D-CTG★, D-MIN★ all hold."
**Problem**: The walkthrough of intermediate states verifies D-CTG★, D-MIN★, D-SEQ★, S2, S3★ but does *not* explicitly verify S8-depth (per-subspace depth uniformity) or S8a (well-formedness — zero-free, depth ≥ 2, positive components) at intermediate states. After K.μ⁻ shrinks V_{s_C}(d) to a prefix, every retained position has depth m_C and satisfies S8a, but this is asserted by "per-state invariants hold" rather than checked. After K.μ⁺ re-adds Insertion + Shifted-right, the same applies to the newly added positions. These invariants are load-bearing for Class (a) preservation under ValidComposite★.
**Required**: Explicitly verify S8-depth and S8a at each intermediate state in the canonical decomposition, especially: (i) after K.μ⁻ when V_{s_C}(d_intermediate) is the Left prefix; (ii) after K.μ⁺ for the Insertion positions shift(p, k); (iii) for Shifted-right positions shift(v, n).

### Issue 4: Cross-chain disjointness in freshness argument is implicit
**ASN-0100, Effect One: Allocation**: "The freshness of each a_k is established against the state immediately preceding its K.α firing... K.α's precondition requires a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L). This holds by ChainEnumerationInjectivity (ASN-0093)..."
**Problem**: K.α's precondition is `a ∉ dom(C) ∪ dom(L)`. ChainEnumerationInjectivity (ASN-0093) establishes within-chain distinctness — a_k is distinct from prior emissions of A_C(d) — but does *not* directly establish a_k ∉ dom(L). The latter relies on L14 (StoreDisjointness) or DisjointSubAllocatorChains (ASN-0093): a_k has subspace_I = s_C while every ℓ ∈ dom(L) has subspace_I = s_L, and s_C ≠ s_L by SC-NEQ. This step is load-bearing for K.α's precondition but unstated.
**Required**: Add citation of L14 (or DisjointSubAllocatorChains) when discharging the dom(L) half of K.α's freshness precondition. The dom(C) half is correctly handled by ChainEnumerationInjectivity + FirstEmissionFreshness.

### Issue 5: I3 preconditions not explicitly discharged
**ASN-0100, Effect Three: Shift**: "This clause is exactly the I3 postcondition (PostInsertionShift) of ASN-0082, instantiated for the text subspace S = s_C of d."
**Problem**: I3 (ASN-0082) has its own precondition list including "depth-compatible: if {v ∈ dom(M(d)) : subspace(v) = S} ≠ ∅ then #p = #v for any such v". The ASN-0100 does not explicitly verify this — it holds because S8-depth fixes #v = m_C across V_{s_C}(d) and INSERT's precondition requires #p = m_C, but this discharge is implicit. The ASN cites I3 as a known result without showing that INSERT's preconditions imply I3's preconditions.
**Required**: Add a brief discharge of I3's preconditions: (i) d is a document (from INSERT's `d ∈ dom(M)`); (ii) #p ≥ 2 ∧ subspace(p) = s_C ≥ 1 (from INSERT's precondition `subspace(p) = s_C` and `#p = m_C ≥ 2`); (iii) depth-compatibility (from S8-depth and INSERT's #p = m_C); (iv) n ≥ 1 (matches).

### Issue 6: Alternative decomposition Σ' uniqueness asserted without proof
**ASN-0100, Atomicity and Canonical Order**: "The post-state Σ' of the canonical decomposition above. Such alternative decompositions are admissible and reach the same Σ'."
**Problem**: The claim that all admissible decompositions (varying n'_{s_C} in {0, …, p_m − 1}, splitting K.μ⁺ across multiple firings, reordering K.α + K.ρ) "reach the same Σ'" is asserted but not justified. For different n'_{s_C} values, the intermediate states differ; the K.μ⁺ steps add different sets of positions. Without verifying that the post-state arrangement, content store, and provenance relation are identical across decompositions, the uniqueness claim is unsupported.
**Required**: Either (a) verify Σ' uniqueness by direct comparison of the final M'(d), C', R' across two representative decompositions (e.g., n'_{s_C} = p_m − 1 vs. n'_{s_C} = 0), or (b) cite a general uniqueness property of ValidComposite★ that handles this.

### Issue 7: Composite-level atomicity not adequately distinguished from per-step atomicity
**ASN-0100, Atomicity and Canonical Order**: "SequentialTransitionAxiom (ASN-0093) guarantees only that each *elementary* transition is atomic — no elementary transition of another composite can split an elementary transition of INSERT. Composite-level atomicity — the guarantee that no elementary transition of another composite interleaves between INSERT's elementaries — is not entailed by SequentialTransitionAxiom; it is an implementation concern (see Open Questions)."
**Problem**: The ASN acknowledges that INSERT's substrate composite may interleave with elementary transitions from other composites in the substrate's transition vocabulary. But the operation contract (the INS.* postconditions) is stated as if Σ →* Σ' is observed contiguously. If another composite's K.α fires for the same document d between INSERT's K.α firings, the chain index m_d changes mid-INSERT, and the supposedly "fresh" a_k could collide with another composite's allocation. The ASN should either rule out such interleaving as part of INSERT's contract or specify what happens when interleaving occurs. Leaving this to "implementation concern" leaves the abstract specification incomplete — concurrent INSERTs on the same document have undefined behavior at the abstract level.
**Required**: Either (a) explicitly add a composite-atomicity precondition (no other composite's transitions interleave during Σ →* Σ' for the same d), or (b) state the contract more carefully in terms that handle interleaving (e.g., by parameterizing a_k as "the addresses produced by INSERT's K.α firings in their committed order, against the substrate state at each firing").

## OUT_OF_SCOPE

None — the ASN explicitly carves out link-subspace INSERT, COPY, DELETE, REARRANGE, version creation, and replication; its Open Questions list (composability, concurrency, atomicity environment, depth update, K.α/K.ρ ordering, chunking, metadata) appropriately flags forward work.

VERDICT: REVISE
