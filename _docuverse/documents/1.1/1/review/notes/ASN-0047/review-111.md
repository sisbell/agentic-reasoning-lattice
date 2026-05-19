# Review of ASN-0047

## REVISE

### Issue 1: Foundation axioms claimed as new in Properties Introduced table

**ASN-0047, "New properties introduced by this ASN" table**: Lists `SubspaceConventionAxiom`, `SequentialTransitionAxiom`, and `SubAllocatorAxiom` as introduced by this ASN.

**Problem**: All three are foundation invariants in ASN-0093 (verified against the ASN-0093 listings):
- `SubAllocatorAxiom — ContentLinkSubAllocatorExistence` is in ASN-0093
- `SubspaceConventionAxiom — FixedSubspaceIdentifiers` is in ASN-0093  
- `SequentialTransitionAxiom — SequentialAtomicTransitions` is in ASN-0093

The body text correctly attributes `SubAllocatorAxiom` to ASN-0093 ("SubAllocatorAxiom (per ASN-0093, ContentLinkSubAllocatorExistence). The axiom is taken from ASN-0093 directly."), but the summary table is inconsistent with this attribution.

**Required**: Move these three axioms out of "New properties introduced by this ASN" and into a separate "Inherited from foundation" table or annotate them with their foundation source. Distinguish (a) genuinely new properties, (b) foundation restated for narrative continuity, and (c) local extensions/strengthenings.

### Issue 2: L0 C-clause attribution

**ASN-0047, "Local extensions and strengthenings" table**: "L0 | ... | L-clause from ASN-0043's L0 (SubspacePartition); the C-clause is the new content-side companion required by the extended state"

**Problem**: ASN-0093's L0 already contains BOTH clauses:
```
(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)
(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)
```

The body text correctly notes: "L0 (SubspacePartition, per ASN-0093). Both clauses are foundation invariants." The table contradicts this by claiming the C-clause is new.

**Required**: Update the Local extensions table entry to attribute both clauses to ASN-0093, not just the L-clause to ASN-0043.

### Issue 3: K.δ k=0 frontier requirement under-specified for K.δ discharge

**ASN-0047, K.δ case (ii) k=0**: "inc(t, 0) ∉ E. ... the freshness conjunct `inc(t, 0) ∉ E` is the case-level `e ∉ E` specialised to `e = inc(t, 0)` — stated locally to record that the caller's operand selection must observe it (operationally: pick `t` on the frontier of its own T10a sub-allocator's sibling chain, so that `(t, 0)` has not yet fired on that chain)."

**Problem**: The discharge prose says "T10a's per-`(t, 0)` uniqueness on t's own sub-allocator chain (the `(t, 0)` pair has fired at most once across the system, and it has not fired previously when the operand `t` is the frontier of that chain)". The parenthetical condition — "when the operand `t` is the frontier of that chain" — is the load-bearing premise, but the precondition as stated only requires `inc(t, 0) ∉ E`. Operationally these coincide, but the proof obligation needs operand `t` to be the *current frontier*, not merely some operand satisfying `inc(t, 0) ∉ E`. The discharge route relies on this implicit identification.

**Required**: Make the frontier identification explicit. Either strengthen the precondition to require `t` is the unique element of its sub-allocator's tracked domain with no `(t, 0)` successor yet emitted, or substantiate that `inc(t, 0) ∉ E` plus the other K.δ k=0 conjuncts forces `t` to be the frontier.

### Issue 4: Initial state existential consistency

**ASN-0047, Definition of Initial state**: "C₀ = ∅ (no content allocated); E₀ = {n₀} where n₀ = `[1]`"

**Problem**: P6 (Existential coherence) requires `(A a ∈ dom(C) :: origin(a) ∈ E_doc)`. At Σ₀, dom(C₀) = ∅ so vacuous. But P8 requires `(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`, and the verification for the bootstrap is silent. Specifically, n₀ = [1] has IsNode(n₀) so falls outside P8's quantifier. NodeLineage at Σ₀ requires `n₀ ≼ n₀` (reflexivity). Both are noted in the proof but the Initial state definition would benefit from an explicit clause verifying all invariants hold at Σ₀.

**Required**: Add an "Initial state invariant verification" subsection (analogous to how the worked examples verify state invariants) listing each Class (a) per-state invariant against Σ₀, showing each holds (most vacuously). The current treatment is scattered across the proof.

### Issue 5: Bijection equation interpretation needs disambiguation for empty domains

**ASN-0047, K.μ~ bijection equation**: "`(E π : π is a bijection dom(M(d)) → dom(M'(d)) : (A v ∈ dom(M(d)) :: M'(d)(π(v)) = M(d)(v)))`"

**Problem**: When `dom(M(d)) = ∅`, the empty function is a vacuous bijection ∅ → ∅, satisfying the equation trivially with π = id (the empty identity). Admissibility clause (iii) (`π ≠ id`) would then be unsatisfiable, but this is not explicitly excluded — the existence condition `|dom_C(M(d))| ≥ 2` derivation discusses singleton case but not the empty case. K.μ~ should be unfirable on empty arrangements; this should be stated.

**Required**: State explicitly that K.μ~ requires `dom_C(M(d)) ≠ ∅` as a derived necessary condition (singleton and empty cases both excluded by clause (iii)), and that the empty-arrangement case is excluded both by the bijection vacuity and by the K.μ⁻ + K.μ⁺ decomposition (K.μ⁻ requires `dom(M(d)) ≠ ∅`).

### Issue 6: V-position uniqueness check at link arrangement

**ASN-0047, K.μ⁺_L verification of `v_ℓ ∉ dom(M(d))`**: "subspace(v_ℓ) = s_L and s_L ≠ s_C (SC-NEQ) ensures no collision with text-subspace positions (T3, CanonicalRepresentation, ASN-0034: tumblers are extensionally identified by their component sequence, so two tumblers differing in their first component are distinct)."

**Problem**: The argument shows v_ℓ ∉ V_{s_C}(d). But V-positions can have arbitrary depth; this argument needs `subspace(v_text) = s_C` for all V-positions in dom(M(d)) under S3★-aux. S3★-aux is established inductively, so its application here is sound. However, the inductive base requires V_{s_L}(d) = ∅ initially (the "V_{s_L}(d) = ∅" case in K.μ⁺_L), and the prose case for "V_{s_L}(d) ≠ ∅" relies on TS4 showing `v_ℓ > max(V_{s_L}(d))`, which is correct, but the prose conflates the link-subspace disjointness check with the content-subspace check, making the proof harder to follow.

**Required**: Separate the two disjointness checks explicitly: (a) v_ℓ ∉ V_{s_L}(d) by TS4 strict monotonicity (non-empty case) or vacuously (empty case); (b) v_ℓ ∉ V_{s_C}(d) by SC-NEQ + T3 plus S3★-aux's subspace partitioning.

## OUT_OF_SCOPE

### Topic 1: ASN-0040 integration

**Why out of scope**: ASN-0040 (BaptismalRegistry) defines a Σ.B component and baptize operations, while ASN-0047 uses K.δ with T10a discharge directly. Whether and how the two should integrate (does Σ in ASN-0047 also carry Σ.B from ASN-0040?) is an open architectural question, properly deferred. The current ASN-0047 stands on its own without needing ASN-0040.

### Topic 2: Concurrency model beyond sequential atomicity

**Why out of scope**: The ASN's SequentialTransitionAxiom forces total ordering of transitions. Real-world concurrent allocation, contention resolution, and serializability are properly listed under Open Questions and Scope exclusions.

### Topic 3: Link withdrawal and tombstoning reconciliation

**Why out of scope**: The tension between D-CTG★/D-MIN★ (per-subspace contiguity) and Nelson's tombstoning design for deleted links is explicitly raised in Open Questions. Resolution requires a future ASN introducing a status-flag or tombstone mechanism outside K.μ⁻'s presentational-removal contract.

### Topic 4: Operation-level specifications (INSERT, DELETE, etc.)

**Why out of scope**: The Scope statement explicitly excludes named operations. ASN-0047 provides the elementary transition vocabulary from which such operations would compose; their specifications belong in dependent ASNs.

VERDICT: REVISE
