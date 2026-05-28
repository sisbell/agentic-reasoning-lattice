# Review of ASN-0100

## REVISE

### Issue 1: L0's content-subspace clause is treated as "a property of L alone" — but INSERT mutates dom(C)

**ASN-0100, §"Link store unchanged (L12, L0, L1, L3)"**: "The subspace partition L0, the element-level structure L1, and the N-endset structure L3 are all properties of `L` alone and so hold of `L'` trivially."

**Problem**: L0 (SubspacePartition, ASN-0047/ASN-0093) has *two* conjuncts: `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` **and** `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`. The second conjunct ranges over `dom(C)`, which INSERT extends by the fresh `a_0, …, a_{n−1}` (INS.C). L0 is therefore *not* a property of `L` alone, and its content clause is not discharged "trivially." The same omission recurs in §Atomicity: the "link-store invariants" grouping lists L1, L1a, L1b, L1c, L3, L-fin, L12, CL-OWN, CL-UNIQ but **omits L0 entirely**, and the per-K.α-intermediate analysis verifies L14 (`a_k ∉ dom(L)`) without ever establishing `subspace_I(a_k) = s_C`. Since L0 appears in ASN-0047's ExtendedReachableStateInvariants conjunction, it must be preserved at every state.

**Required**: Verify L0's content clause for each freshly allocated `a_k`: `subspace_I(a_k) = s_C` holds by SubAllocatorAxiom.Subspace (ASN-0047) / DisjointSubAllocatorChains (ASN-0093), since `a_k` is produced by `A_C(d)`. State this explicitly (the fact is true; the justification "property of L alone" is wrong) and add L0 to the atomicity grouping with the correct discharge.

### Issue 2: INS.inv.func cites a lemma the proof does not use

**ASN-0100, Claims table, INS.inv.func**: "Left, Insertion, Shifted-right regions are pairwise disjoint by TS2 and TS4 (ASN-0034)."

**Problem**: The body proof of pairwise disjointness uses TumblerAdd's component arithmetic (last-component comparisons `p_m + k` vs `< p_m` vs `≥ p_m + n`) for the three disjointness claims, and TS2 (ShiftInjectivity) for within-region source uniqueness of Shifted-right. TS4 (ShiftStrictIncrease) is never invoked in the disjointness argument. The citation is inaccurate.

**Required**: Either correct the table entry to cite TumblerAdd + TS2, or point to where TS4 is actually load-bearing.

### Issue 3: Case (i.b) decomposition analysis introduces a non-load-bearing, environment-dependent alternative that obscures the contract

**ASN-0100, §"Substrate Decomposition", step 2, case (i.b)**: "an alternative decomposition becomes available *only when the substrate environment retains the pre-state's link arrangement information across the K.μ⁻ step* … the implementation must record the ordered sequence `⟨ℓ_1, ℓ_2, …, ℓ_{n_{s_L}}⟩` … as a side channel."

**Problem**: The canonical decomposition simply *omits* K.μ⁻ in case (i.b) (V_{s_C}(d) = ∅ means Insertion via K.μ⁺ alone suffices, leaving V_{s_L}(d) untouched). The post-state is fully determined without any of this. The multi-paragraph exploration of an alternative decomposition that shrinks `s_L` and rebuilds it via sequential K.μ⁺_L firings — conditioned on the substrate "retaining pre-state link ordering as a side channel" — is not load-bearing for INSERT's correctness and reasons about implementation state-retention mechanics rather than system guarantees. It risks drifting the operation spec into substrate-implementation territory.

**Required**: Trim case (i.b) to the load-bearing fact (K.μ⁻ is omitted because no admissible firing strictly shrinks `s_C` while preserving `s_L`), matching the treatment that case (i.a) already receives. If the symmetry observation with case (ii) is worth keeping, state it without the side-channel implementation reasoning.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L semantics)
**Why out of scope**: The ASN correctly restricts to the content subspace and defers link-subspace insertion to a future ASN; link semantics is explicitly out of scope.

### Topic 2: Concurrent-INSERT serialization basis and partial-failure recovery
**Why out of scope**: Raised in Open Questions; the composite-atomicity precondition is correctly stated as an environmental assumption, and the minimum machinery to secure it is future work, not an error here.

VERDICT: REVISE
