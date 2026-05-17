# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=1 ghost-base case's reliance on T10a is formally imprecise

**ASN-0047, K.δ definition (Elementary transitions)**: "By T10a's GlobalUniqueness (ASN-0034) — the same result that governs K.α — every inc-produced address is distinct from every previously allocated address, so `e ∉ E` for case (ii)."

**ASN-0047, ghost-base worked example**: "We take `T₆` (T10a's universe of allocated tumblers) to include `t` — the address has been issued at the tumbler-allocation layer (so T10a's GlobalUniqueness governs subsequent inc operations on it) without the corresponding entity record being created in E."

**Problem**: T10a (ASN-0034) is structured around per-allocator domains: each non-root allocator A has spawning triple `(parent(A), spawnPt(A), spawnParam(A))` with `spawnPt(A) ∈ dom(parent(A))`, and GlobalUniqueness establishes distinctness of *outputs of T10a-conforming allocators*. A ghost document tumbler `t` was never emitted by any allocator and therefore is not in any allocator's domain. T10a's discipline does not formally apply to `inc(t, 1)` when t is a ghost. The "tumbler-allocation layer vs entity-allocation layer" distinction is informal stipulation introduced only in a worked-example footnote, not a formal construction grounded in any axiom of this ASN or its foundations.

The actual operative guarantee for `e ∉ E` in the k=1 ghost-base case comes from K.δ's explicit `e ∉ E` precondition combined with `inc`'s determinism (TA5, ASN-0034) — not from T10a's GlobalUniqueness on a ghost spawn point.

**Required**: Either (a) replace the T10a citation in the k=1 sub-case with the K.δ precondition + TA5 determinism as the operative uniqueness mechanism (parallel to how NodeUniqueAllocation handles the node case where T10a does not apply), or (b) introduce a separate axiom for ghost-base allocation events. The pattern for case (a) is already established in the ASN's own treatment of node allocation: "K.δ for nodes therefore imposes no inc-conformance requirement... NodeUniqueAllocation alone guarantees `e ∉ E`."

### Issue 2: T10a citation chain imprecision in cross-document disjointness derivation

**ASN-0047, *Allocator hierarchy under documents***: "By T10a.6 (DomainDisjointness, ASN-0034), distinct allocators have disjoint domains — applied at the document level, the allocator hierarchy underwriting `d₁` and the one underwriting `d₂` produce prefix-incomparable tumblers (case 2 of T10a.6's proof for non-ancestor–descendant allocator pairs, or case 1 reduced to length-separation contradiction for ancestor–descendant pairs)"

**Problem**: T10a.6 (DomainDisjointness) concludes `dom(A₁) ∩ dom(A₂) = ∅` — domain disjointness, not prefix-incomparability of outputs. Reaching into "T10a.6's proof cases" pulls the underlying facts from T10a.5 (CrossAllocatorIncomparability) and T10a.3 (LengthSeparation), which are the load-bearing invariants. Additionally, two distinct sibling documents under the same account are produced by the *same* allocator via inc(·, 0); they are not outputs of "different allocators" in T10a.6's sense, so case (2) of T10a.6's proof does not apply directly — T10a.2 (NonNestingSiblingPrefixes) does.

**Required**: Cite T10a.2 for the same-account sibling case and T10a.5 for the different-account case explicitly; T10a.6 can stand as the packaging citation but should not be the sole reference for prefix-incomparability.

### Issue 3: K.δ k=1 invariant verification claimed but not explicit

**ASN-0047, K.δ *Scope and base-liveness***: "The per-invariant verification above establishes that omitting `t ∈ E_doc` for k = 1 leaves every clause of P0–P8, S0–S9, L0–L14, J0–J4, and their starred forms invariant-safe."

**Problem**: The "per-invariant verification above" is not enumerated in the K.δ section. The body of the discussion treats P8 specifically (parent(e) = parent(t) at k=1, so parent(e) ∈ E discharges P8 independently of t ∈ E) and gestures at "a routine frame argument" for the rest, but does not show the named invariant set is preserved. The worked example *Ghost-base document versioning* verifies invariants on a single concrete state, not in general. The claim that *every clause* of P0–P8, S0–S9, L0–L14, J0–J4 (and starred forms) is invariant-safe is load-bearing for the decision to admit ghost-base versioning at the abstract level.

**Required**: Either enumerate the per-invariant check at the K.δ k=1 sub-case (showing that each named invariant is either preserved by K.δ's frame, vacuously satisfied on the new entity's empty arrangement, or independent of t's E-membership), or downgrade the claim to "by frame on every state component except E, plus parent-spine independence for P8" with the understanding that detailed verification appears in the worked example.

### Issue 4: K.μ~ worked example does not trace the intermediate state

**ASN-0047, *Worked example: link allocation and arrangement*, Step 3**: "M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ}" — output stated directly, without tracing the K.μ⁻ + K.μ⁺ decomposition.

**Problem**: K.μ~ is defined as a distinguished composite whose contract is a *derived theorem* from its K.μ⁻ + K.μ⁺ decomposition. The worked example's stated purpose is to verify the central postconditions on concrete tumbler values, and the link-subspace fixity argument is one of the most intricate derivations in the ASN. The example skips the intermediate state (after K.μ⁻ removes both content positions, before K.μ⁺ re-adds them swapped), bypassing the central verification target — that the intermediate state has admissible D-CTG★/D-MIN★ on the link subspace (vacuous on the cleared content subspace) and that K.μ⁺'s preconditions hold at that intermediate state.

**Required**: Add the intermediate state to Step 3: after K.μ⁻ removes {[1,1], [1,2]}, M_int(d) = {[2,1] ↦ ℓ}. Verify K.μ⁻'s admissibility (content-subspace n'_{s_C} = 0, link-subspace n'_{s_L} = n_{s_L} = 1), then K.μ⁺'s preconditions at M_int (the rebuilt positions [1,1], [1,2] are content-subspace, addresses a₁, a₂ ∈ dom(C_int) = dom(C), etc.).

### Issue 5: K.μ~ definition's forward-reference architecture

**ASN-0047, K.μ~ definition (Elementary transitions)**: "The contract stated immediately below is a *theorem* describing what any such decomposition achieves... The decomposition account... is deferred to the dedicated *Decomposition of K.μ~* section below, placed after the per-state invariants S3★-aux... and CL-UNIQ... on which it depends."

**Problem**: K.μ~'s contract is stated upfront and described as a theorem of a decomposition that appears later, after per-state invariants S3★-aux and CL-UNIQ (themselves defined still further along). A reader encountering K.μ~ in the *Elementary transitions* section cannot verify the contract without jumping ahead. The acknowledgement that the structure is "non-circular" (because S3★-aux and CL-UNIQ are inductively established without appeal to K.μ~'s contract) is correct but does not help with first-read comprehension. The structure obscures that K.μ~ depends on three later-defined predicates.

**Required**: Either (a) move the *Decomposition of K.μ~* section (with S3★-aux and CL-UNIQ inlined as preliminaries) before the K.μ~ elementary-transition definition, or (b) restructure K.μ~'s initial introduction as a brief informal placeholder ("reordering via a subspace-preserving bijection — formal contract and decomposition treated below") and defer the contract statement entirely to the Decomposition section. The current structure pays the cost of forward references twice (definition + Case 2 of the decomposition).

## OUT_OF_SCOPE

The ASN's *Open Questions* section already enumerates the appropriate deferred topics (tombstone-style link withdrawal, version-management semantics, account-level k=1, cross-document arrangement effects, concurrent operations). No additional out-of-scope items.

VERDICT: REVISE
