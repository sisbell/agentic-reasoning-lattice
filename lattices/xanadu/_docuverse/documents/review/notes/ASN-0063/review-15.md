# Review of ASN-0063

## REVISE

### Issue 1: CL11 misclassifies S8 and gives incorrect justification
**ASN-0063, CL11 "Trivially preserved invariants"**: "Content-store invariants S4 (OriginBasedIdentity), S5 (UnrestrictedSharing), S6 (PersistenceIndependence), S7/S7a/S7b (StructuralAttribution), S8 (SpanDecomposition), S9 (TwoStreamSeparation) hold since C' = C — no content is allocated or modified, so all properties of the content store are preserved identically."
**Problem**: S8 (SpanDecomposition) is not a content-store invariant — it is about the arrangement M(d), specifically its decomposition into correspondence runs. The justification "C' = C" is irrelevant to S8. CREATELINK adds one link-subspace mapping to M(d), which changes the set that S8 quantifies over (all V-positions with v₁ ≥ 1, which includes v₁ = s_L ≥ 1). The new mapping ([s_L, 1, ...] ↦ ℓ) forms a width-1 correspondence run that must be accounted for.
**Required**: Move S8 to the per-subspace arrangement invariants paragraph and justify it correctly. Either: (a) note that S8 is derived from S8-fin, S8a, S2, S8-depth — all verified in the preceding paragraph — so S8 follows; or (b) show directly that the new link-subspace mapping forms a trivial width-1 correspondence run and existing runs are unchanged.

### Issue 2: S3★-aux proof omits K.λ
**ASN-0063, S3★ analysis, S3★-aux proof**: "Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.ρ hold M in frame."
**Problem**: The inductive step enumerates seven transition kinds but omits K.λ, which is introduced in this ASN. K.λ holds M in frame — it belongs with K.α, K.δ, K.ρ — but its absence makes the proof formally incomplete over the extended transition set.
**Required**: Add K.λ to the M-in-frame group: "K.α, K.δ, K.λ, K.ρ hold M in frame."

### Issue 3: Orphan link composite — coupling constraints verified but state invariants not
**ASN-0063, "Extending the Transition Framework"**: "A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an orphan link. This is a valid system state, not an error condition."
**Problem**: The ASN verifies the coupling constraints (J0, J1★, J1'★) for K.λ alone, establishing it as a valid composite. It does not verify that the resulting state satisfies the state invariants. Since the orphan link state is presented as architecturally intentional and the ASN explicitly discusses its properties (disc still includes orphan links, parallels to deleted bytes), the invariant preservation should be shown. The argument is straightforward — M, C, E, R are all in K.λ's frame, and L grows with a well-formed entry whose preconditions satisfy L0, L1, L1a, L12, L14 — but it is absent.
**Required**: After the coupling constraint verification, add a brief invariant verification: state that M, C, E, R are unchanged (frame), so all arrangement, content, entity, and provenance invariants hold; and that L grows with an entry satisfying K.λ's preconditions, preserving L0 (subspace partition — ℓ ∉ dom(C)), L1, L1a, L12 (existing entries unchanged), and L14 (disjointness).

### Issue 4: No extended reachable-state invariants theorem
**ASN-0063, throughout**: The ASN amends five foundation properties (S3 → S3★, P4 → P4★, J1/J1' → J1★/J1'★, P3 → P3★, P5 → P5★), amends K.μ⁺ with a content-subspace restriction, and introduces two new elementary transitions (K.λ, K.μ⁺_L). Each piece is verified — existing transitions against the new invariants (§ Extending the Transition Framework), CREATELINK against all invariants (CL11), the initial state (extended initial state paragraph). But the complete invariant set for the extended state is never stated as a theorem.
**Problem**: ASN-0047 states a ReachableStateInvariants theorem: "Every state reachable from Σ₀ ... satisfies P4 ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ S2 ∧ S3 ∧ S8a ∧ S8-depth ∧ S8-fin." This ASN replaces S3 with S3★ and P4 with P4★, adds link invariants (L0, L1, L1a, L12, L14), and introduces transitions that the original theorem does not cover. The reader must reconstruct the updated invariant landscape from scattered arguments across four sections.
**Required**: State an extended ReachableStateInvariants theorem for Σ = (C, L, E, M, R), listing the full invariant set — including S3★ (replacing S3), P4★ (replacing P4), the link invariants, and noting which transitions are covered. The proof can reference the preservation arguments already in the ASN.

## OUT_OF_SCOPE

### Topic 1: Link indexing mechanism
**Why out of scope**: The ASN correctly defines the abstract discovery function disc(a, r) and its properties (CL7–CL9). The concrete indexing mechanism (enfilade, range queries, performance guarantees) is implementation-level specification for a future ASN.

### Topic 2: Link withdrawal invariants
**Why out of scope**: The ASN identifies the constraint that K.μ~ fixes link-subspace mappings and that K.μ⁻ on interior link-subspace positions violates D-CTG. It correctly defers the withdrawal mechanism (whether links transition to inactive status vs. being removed from M) as an open question.

### Topic 3: Concurrent CREATELINK semantics
**Why out of scope**: Serialization and coordination of concurrent link allocation are inter-server protocol concerns, not single-operation specification.

VERDICT: REVISE
