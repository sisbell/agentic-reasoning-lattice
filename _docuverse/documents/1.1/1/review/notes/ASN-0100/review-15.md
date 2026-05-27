# Review of ASN-0100

## REVISE

### Issue 1: S8a argument's set-membership is imprecise for the append case

**ASN-0100, §Effect Two: Placement**: "Each shift(p, k) satisfies S8a (VPositionWellFormedness, ASN-0036): zero-free, depth ≥ 2, all components positive (since p satisfies S8a by virtue of p ∈ V_{s_C}(d) ∪ {[s_C, 1, …, 1]} and the shift's tail component p_{m_C} + k ≥ 1)."

**Problem**: For the append case (j = N), p = shift(min, N) has last component N+1, which places p outside V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}, and p is not [s_C, 1, …, 1] either (unless N = 0). The set-membership phrasing fails to capture this case.

**Required**: Replace with the direct justification: p satisfies S8a by ValidInsertionPosition postcondition (b) (non-empty case) or ValidFirstInsertionPosition postcondition (b) (empty case). Both predicates assert S8a as their (b) postcondition; the set-membership formulation is unnecessary.

### Issue 2: Composite-atomicity precondition wording is ambiguous

**ASN-0100, §The Operation: Formal Contract — Environmental Assumptions**: "No elementary transition of any other composite interleaves between INSERT's elementaries... Where this assumption fails — concurrent INSERTs on the same document, for example — the chain index m_d consulted by K.α can advance mid-composite via another composite's K.α on the same A_C(d)..."

And later: "preventing inter-composite elementary interleaving on the affected document and its allocator chain".

**Problem**: "Its allocator chain" is ambiguous between A_C(d) (which INSERT depends on) and the full allocator subtree of d (which would include A_L(d) and version sub-allocators). By the body's own analysis, concurrent K.λ on the same d does not affect INSERT's correctness (a_k's chain elements have subspace_I = s_C, disjoint from K.λ's link emissions by L0 + SC-NEQ). The precondition over-specifies what atomicity INSERT actually needs.

**Required**: Specify that composite-atomicity is required against concurrent operations that modify (i) A_C(d)'s chain emission state (specifically, dom(C) entries with origin = d), and (ii) M(d)'s text subspace. Concurrent operations affecting A_L(d), M(d)'s link subspace, or unrelated documents are not within the required atomicity scope.

### Issue 3: Exhaustiveness clause's K.μ⁻-fired case relies on a glossed argument

**ASN-0100, §The Operation: Formal Contract — Effect — Arrangement of d, text subspace**: "When K.μ⁻ fires (the canonical interior and j = 0 cases), it retains exactly the Left prefix of V_{s_C}(d) and removes the Right region; step 3's K.μ⁺ then adds *precisely* the Insertion and Shifted-right positions (per the K.μ⁺ amendment, only s_C positions are added), so V_{s_C}(d') = Left ∪ Insertion ∪ Shifted-right by direct union."

**Problem**: The phrase "K.μ⁺ then adds *precisely* the Insertion and Shifted-right positions" is the load-bearing step but isn't proved. K.μ⁺'s precondition (ASN-0047) is permissive — it allows the implementation to add *any* new V-positions in s_C with images in dom(C). The exhaustiveness conclusion requires that *this particular* K.μ⁺ firing in INSERT's decomposition adds *exactly* Insertion ∪ Shifted-right, no more and no fewer. This is a property of INSERT's contract specification (a constraint on the implementation), not of K.μ⁺'s vocabulary.

**Required**: State this as an explicit constraint on step 3 — K.μ⁺ adds exactly the Insertion and Shifted-right V-positions with the specified images, no other s_C V-positions — and derive the exhaustiveness clause from that constraint plus K.μ⁻'s removal of the Right region.

### Issue 4: P6 preservation argument elides a subtle case

**ASN-0100, §Post-state V-position well-formedness (S8-depth, S8a, S8-fin) and S7 invariants**: "P6 (ExistentialCoherence, ASN-0047). (A a ∈ dom(C') :: origin(a) ∈ E') ... Every pre-state a ∈ dom(C) inherits P6 from the pre-state because dom(C) ⊆ dom(C') and origin(a) is a property of the address a itself..."

**Problem**: The reasoning is correct, but the chain of reasoning conflates dom(M) and E_doc without explicit identification. Under ValidComposite★ (ASN-0047), P6 ranges over E_doc, not over dom(M) — the substrate distinguishes the entity set from the document arrangement. INSERT's frame INS.frame.E claims E' = E, and INS.frame.dom claims dom(M') = dom(M), but the ASN doesn't explicitly state that these coincide for document entities.

**Required**: Make the identification explicit: under ValidComposite★, E_doc = dom(M) (the document subset of E is exactly the documents with arrangements). Then origin(a) ∈ E_doc transfers to origin(a) ∈ E'_doc under INS.frame.E. Without this identification, the P6 inheritance argument relies on undefined coincidence between E (entity set) and dom(M) (arrangement domain).

### Issue 5: The K.α ordering proof has a subtle circularity

**ASN-0100, §Atomicity and Canonical Order**: "K.α(a_k) before K.α(a_{k+1}). By K.α's allocation discipline (ASN-0093), the k-th K.α firing produces the k-th element of the chain A_C(d)... There is no freedom to fire K.α producing a_1 before K.α producing a_0, because a_1 = inc(a_0, 0) is *defined* in terms of a_0's prior commitment to dom(C)."

**Problem**: The claim "a_1 = inc(a_0, 0) is *defined* in terms of a_0's prior commitment to dom(C)" runs the argument in the wrong direction. The chain element t_{m_d + 2} is *fixed* by the chain enumeration (ChainEnumerationInjectivity), independent of which K.α firing produces it. The forced ordering is rather: K.α's subsequent-emission predicate computes its output as inc(max{a' ∈ dom(C) : origin(a') = d}, 0), which at the time of the first INSERT K.α firing yields t_{m_d + 1}, and at the time of the second K.α firing (after the first commits) yields t_{m_d + 2}. The ordering is forced by the side-effect dependency through dom(C), not by definitional dependency.

**Required**: Reframe as: the k-th K.α firing in INSERT's composite computes its output by consulting the current dom(C) state. The first firing sees dom(C) without a_0 and produces a_0 = t_{m_d + 1}. The second firing requires dom(C) updated with a_0 (committed by step 1's atomicity, SequentialTransitionAxiom) and produces a_1 = t_{m_d + 2}. The ordering is forced by K.α's consultation of dom(C), not by definitional precedence.

### Issue 6: Missing concrete trace for the alternative decomposition in case (i.b)

**ASN-0100, §The Operation: Formal Contract — substrate decomposition, Case (i.b)**: "Under ValidComposite★'s full vocabulary, however, an alternative decomposition is admissible: K.μ⁻ shrinks V_{s_L}(d) to some n'_{s_L} < n_{s_L}, K.μ⁺ adds the Insertion region (subspace s_C), and successive K.μ⁺_L firings then restore the discarded s_L positions..."

**Problem**: The claim that K.μ⁺_L firings can restore the original V_{s_L}(d) arrangement requires more analysis. K.μ⁺_L's V-position selection is determined by D-CTG★ (places at shift(max(V_{s_L}(d)), 1)), but to replicate the original arrangement the implementation must re-add links in the original order — first the link that was at [s_L, 1], then the one at [s_L, 2], etc. K.μ⁺_L's first-arrangement constraint (ℓ ∉ ran(M(d))) is satisfied after K.μ⁻ removes the links, but the ASN doesn't argue that the implementation has the necessary state to choose the correct order.

**Required**: Either trace through the alternative decomposition concretely (specifying which link is re-added at each K.μ⁺_L step, and arguing that the order is recoverable from pre-state information) or note explicitly that the alternative decomposition is admissible only if the substrate environment retains pre-state link ordering information across the K.μ⁻ step.

### Issue 7: K.ρ commutativity claim contradicts its own forced-ordering analysis

**ASN-0100, §Atomicity and Canonical Order**: First states "K.α(a_k) before K.ρ(a_k, d)" as a forced ordering, then later: "K.ρ commutes with K.μ⁻ and K.μ⁺. K.ρ's precondition depends only on C and the entity set; its effect modifies only R."

And: "K.ρ(a_k, d) may fire *before* K.μ⁺ places a_k at shift(p, k): the composite-boundary couplings J0, J1★, J1'★ are evaluated at the final state Σ', at which both the K.ρ-deposited pair (a_k, d) ∈ R' and the K.μ⁺-deposited placement shift(p, k) ↦ a_k ∈ M'(d) have committed, irrespective of their intermediate order."

**Problem**: J1'★ (ProvenanceRequiresExtensionContentSubspace) requires every new R' entry to correspond to a newly-arranged content-subspace I-address. At a state where K.ρ(a_k, d) has fired but K.μ⁺ has not yet placed a_k, the pair (a_k, d) is in R but a_k is not yet in ran(M(d)). If this intermediate state is a composite-boundary candidate (e.g., another composite checks Σ between INSERT's elementaries), J1'★ fails. The ASN's argument that J1'★ is only checked at Σ' assumes composite-level atomicity — which is consistent with INS.pre's composite-atomicity precondition, but the ASN should make this dependency explicit rather than presenting K.ρ-before-K.μ⁺ as freely admissible.

**Required**: Note that the K.ρ-before-K.μ⁺ alternative ordering relies on composite-level atomicity (INS.pre) — under that precondition, intermediate states are not externally observable as composite boundaries, so J1'★ violation at an intermediate doesn't constitute a boundary violation. Without composite-atomicity, the K.ρ-after-K.μ⁺ ordering is the only safe choice.

### Issue 8: Tight endset trace's "tightness precondition" inserted late

**ASN-0100, §A Worked Example — Projection-shift correspondence**: "*Tightness precondition of the trace below.* We assume tight(e_1, Σ_{e_1}) (ASN-0098) — e_1's coverage was tight at the state Σ_{e_1} of its incorporation into ℓ. This is the load-bearing assumption that makes N_I = ∅ concrete; we trace the non-tight alternative at the end of this example."

**Problem**: The trace develops as though tightness is a property that can be assumed at will. But for the example to be a valid verification, the construction of e_1 (with coverage {a₂, a₃, a₄}) must actually be tight at some realistic state Σ_{e_1}. The ASN should either construct Σ_{e_1} explicitly (e.g., "e_1 was incorporated at a state in which {a₂, a₃, a₄} were all in dom(C)") or argue that the tightness predicate is independent of the example's specific construction.

**Required**: Construct Σ_{e_1} explicitly. For instance: "At the state Σ_{e_1} when e_1 was incorporated into ℓ via K.λ, dom(Σ_{e_1}.C) ⊇ {a₂, a₃, a₄} and the span (a_2, δ(3, #a_2)) is canonical with all three F-candidates a_2, a_3, a_4 in dom(Σ_{e_1}.C). Therefore tight(e_1, Σ_{e_1}) holds." This grounds the assumption in the example's substrate state, rather than leaving it as a free parameter.

## OUT_OF_SCOPE

(None — the ASN appropriately bounds its scope to INSERT for the content subspace, with explicit notes on what is excluded.)

VERDICT: REVISE
