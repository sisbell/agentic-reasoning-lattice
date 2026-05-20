# Review of ASN-0047

This is a substantial and largely rigorous ASN. The proofs are detailed, the decomposition of K.μ~ is carefully constructed, and the verification matrix provides comprehensive coverage. However, several issues warrant attention.

## REVISE

### Issue 1: Properties Introduced table — inconsistent frame descriptions

**ASN-0047, Properties Introduced table**: K.α entry says "frame holds E, M, R" — omits L. K.μ⁺ entry has no explicit frame statement. K.ρ entry has no frame statement. K.δ entry has no frame statement. Meanwhile K.μ⁻ and K.μ~ entries do mention L explicitly.

**Problem**: The body shows K.α's extended-state frame includes `L' = L; E' = E; (A d :: M'(d) = M(d)); R' = R`. The table doesn't reflect this. Inconsistency could mislead readers comparing the summary to the body.

**Required**: Update each transition's table entry to consistently state the full frame conditions in the extended state. K.α should include L. K.μ⁺, K.ρ, K.δ should have explicit frame statements.

### Issue 2: K.μ~ matrix entries terse for S8★ and several other invariants

**ASN-0047, verification matrix**: Many K.μ~ cells read "inherits via K.μ⁻ + K.μ⁺ decomposition" or just "inherits via decomposition" without articulating per-step contribution. In particular, S8★ under K.μ~ says "inherits via decomposition" but doesn't distinguish per-subspace handling.

**Problem**: S8★ has two clauses (content-subspace via ASN-0036's S8, link-subspace via trivial length-1 decomposition). Under K.μ~ in full-clearance form, link-subspace fixity preserves the link-subspace decomposition pointwise; the content-subspace decomposition is rebuilt at K.μ⁺. The matrix should specify this rather than say "inherits via decomposition."

**Required**: Expand the S8★ K.μ~ cell to: "link-subspace via fixity (trivial decomposition preserved pointwise); content-subspace decomposition rebuilt at K.μ⁺ post-state via trivial form."

### Issue 3: NodeRegistryBootstrap vs NodeUniqueAllocation clause (c) redundancy unclear

**ASN-0047, NodeRegistryBootstrap and NodeUniqueAllocation clause (c)**: NodeUniqueAllocation clause (c) states "for every reachable state Σ and every t ∈ Σ.E_node, t inhabits the external node-allocation registry's tracked domain." NodeRegistryBootstrap states n₀ is committed to the registry at Σ₀.

**Problem**: At Σ₀, n₀ ∈ E_node, so clause (c) at Σ₀ already implies n₀ is in the registry. NodeRegistryBootstrap appears redundant unless clause (c) is interpreted as derivable only from prior K.δ events. The bracketed prose at clause (c) acknowledges this interpretation, but the relationship between the two axioms is left implicit.

**Required**: Explicitly state that NodeRegistryBootstrap grounds the structural derivation chain for n₀ at Σ₀ (no prior K.δ event exists), while clause (c) is a closure that holds inductively for all subsequent E_node entries. Or, alternatively, fold NodeRegistryBootstrap into clause (c) as an explicit base case.

### Issue 4: K.μ⁻ "Per-subspace consequence of the effect clause" — empty subspace handling

**ASN-0047, K.μ⁻ amendment**: The per-subspace consequence states `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)`.

**Problem**: The derivation doesn't explicitly trace the asymmetric case where one subspace is empty in pre-state. If V_{s_L}(d) = ∅ and V_{s_C}(d) ≠ ∅, the K.μ⁻ must contract V_{s_C}(d). The empty-subspace boundary should be more explicit in the consequence's derivation: which subspace is forced to contract depends on which subspaces are non-empty in pre-state.

**Required**: Add a brief case analysis: (a) both subspaces non-empty — at least one contracts; (b) only V_{s_C}(d) non-empty — V_{s_C}(d) must contract; (c) only V_{s_L}(d) non-empty — V_{s_L}(d) must contract.

### Issue 5: Worked example "fork with subsequent insertion" — incomplete invariant verification on d₂

**ASN-0047, worked example "fork with subsequent insertion"**: The fork step verifies J0, J1★, J1'★, J4, S3★, P4★, P7a, P8, and L-invariants for d₂. However, D-CTG★, D-MIN★, D-SEQ★, S2, and S4 for d₂'s post-state are not explicitly verified.

**Problem**: d₂'s new content subspace V_{s_C}(d₂) = {[1,1], [1,2]} should be verified against the contiguity, minimum, and sequential-shape invariants. The example is illustrative and these are implicit, but explicit verification would catch any subtle issue (e.g., did the V-position choice satisfy D-MIN★?).

**Required**: Add explicit verification lines for D-CTG★ (V_{s_C}(d₂) contiguous), D-MIN★ (min = [1,1] = [s_C,1]), D-SEQ★ (matches {[s_C, k] : 1 ≤ k ≤ 2}), S2 (disjoint extension), and S4 (a₁ ≠ a₂ from pre-state distinctness).

### Issue 6: K.δ k=1 case dispatch hidden in discharge

**ASN-0047, K.δ definition Case (ii) k = 1**: The precondition is uniformly `t ∈ E_doc`. The discharge then distinguishes original document (case (a) of Sub-allocator names) vs version document (case (b)) via T10a.6.

**Problem**: The K.δ definition is operationally uniform across (a)/(b), but the discharge prose introduces the (a')/(b') case-split as if it were operationally relevant. A reader could be confused whether K.δ k=1 has different behavior in the two cases. It does not — the operation is uniform; only the verification routes differ.

**Required**: Add a clarifying note at K.δ k=1's definition: "The operation is uniform across original and version operands; T10a.6 dispatches the verification through the operand's actual provenance, not through any explicit case-split in the operation itself."

### Issue 7: J1' description predates extension; relationship to J1'★ could be clearer

**ASN-0047, J1' section**: J1' is defined for the four-component state (`ran(M'(d)) \ ran(M(d))`). J1'★ is the scoped version. The body uses J1'★ in the extended state.

**Problem**: J1' is still in the Properties Introduced table without indicating it's superseded by J1'★ in the extended state. A reader could conflate the two.

**Required**: Mark J1' in the table as "superseded by J1'★ in the extended state" similar to how J1 is described.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal mechanism

The Open Questions section catalogues interior link withdrawal (preserving V-positions of trailing links while marking an interior link as withdrawn) as future work. The ASN's K.μ⁻ under D-CTG★/D-MIN★/D-SEQ★ admits only suffix truncations on each subspace. This is correctly out of scope — an interior-withdrawal mechanism would be a separate ASN.

### Topic 2: External node-allocation registry protocol specification

The K.δ case (i) discharge relies on NodeUniqueAllocation as an axiom about an external registry. The protocol details (issuing mechanism, persistence, concurrency) are out of scope for this ASN. Correctly deferred to a future ASN.

### Topic 3: Account-level depth-1 extension

The Open Questions section notes the possibility of admitting K.δ k=1 for account operands (creating account-shaped siblings). The ASN correctly excludes this at the precondition based on current design intent. Future extension is appropriately scoped.

VERDICT: REVISE
