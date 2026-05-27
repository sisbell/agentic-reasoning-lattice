# Review of ASN-0100

## REVISE

### Issue 1: P6 (ExistentialCoherence) not explicitly verified
**ASN-0100, §Verifying the Invariants and §Atomicity and Canonical Order**: ASN-0047's ExtendedReachableStateInvariants lists P6 as a Class (a) per-state invariant. The §Verifying the Invariants section addresses S2, S3★, S0/P0, D-CTG★, D-MIN★, D-SEQ★, S8a, S8-depth, S8-fin, S8★, S7a-d, L0, L1-L14, etc., but never verifies P6: `(A a ∈ dom(C) :: origin(a) ∈ E_doc)`. The §Atomicity section's per-step intermediate analysis (e.g., "Per-state invariants on C (C-fin, S7a, S7b, S7c) hold...") omits P6 from the list.
**Problem**: Each freshly allocated `a_k` extends dom(C), so P6 must be discharged at every K.α intermediate. The discharge is one line (origin(a_k) = d ∈ dom(M) by precondition, with E_doc unchanged across the composite by INS.frame.E), but it must be made explicit.
**Required**: Add P6 verification under §Verifying the Invariants or in the §Atomicity per-step list.

### Issue 2: P7 (ProvenanceGrounding) not explicitly verified
**ASN-0100, §Verifying the Invariants**: P7, `(A (a, d) ∈ R :: a ∈ dom(C))`, is a Class (a) per-state invariant in ASN-0047 distinct from P7a (covered in §Provenance). The ASN never addresses P7 directly. At intermediate states after K.ρ firings but before the composite boundary, new (a_k, d) pairs are added to R; preservation of P7 requires a_k ∈ dom(C) at that intermediate (discharged by step 1 having completed before step 4).
**Required**: Add P7 verification, noting it follows from the forced ordering K.α(a_k) before K.ρ(a_k, d) combined with P0 inheritance for pre-state R entries.

### Issue 3: TS2 invocation depends implicitly on S8-depth
**ASN-0100, §Arrangement functionality (S2)**: "source uniqueness follows from TS2 (ShiftInjectivity; ASN-0034): distinct sources `v₁ ≠ v₂` yield `shift(v₁, n) ≠ shift(v₂, n)`."
**Problem**: TS2 (ASN-0034) requires `#v₁ = #v₂ = m` as a precondition. This equal-depth precondition is supplied by S8-depth (FixedDepthVPositions; ASN-0036) on the pre-state V_{s_C}(d), which fixes all positions to depth m_C. The dependency is unstated.
**Required**: Cite S8-depth alongside TS2: "by S8-depth (ASN-0036) all pre-state s_C positions share depth m_C, so TS2's equal-length precondition is met; TS2 then yields injectivity."

### Issue 4: INS.M-exhaustive verification for K.μ⁻-omitted cases is implicit
**ASN-0100, INS.M-exhaustive justification under Effect — Arrangement of d**: "The exhaustiveness clause follows from the substrate decomposition: step 3's K.μ⁺ adds *precisely* the Insertion and Shifted-right positions...; step 2's K.μ⁻ (when fired) retains *only* the Left positions in `s_C`; and no other elementary step modifies `s_C` positions."
**Problem**: When K.μ⁻ does *not* fire (cases i.a, i.b, ii), the Left region's preservation in V_{s_C}(d') comes not from K.μ⁻ retention but from no step removing those positions. The justification reads as though K.μ⁻ is always responsible for the Left region, which it isn't.
**Required**: Strengthen to: "When K.μ⁻ fires, it retains exactly the Left prefix; when K.μ⁻ is omitted (cases i.a, i.b, ii), pre-state V_{s_C}(d) positions are preserved unchanged because no other step removes them. K.μ⁺ adds only Insertion + Shifted-right per the K.μ⁺ amendment. So V_{s_C}(d') = Left ∪ Insertion ∪ Shifted-right in all cases."

### Issue 5: §Coverage and link discoverability gives the per-subspace partition formula but does not verify subspace closure of the shift map
**ASN-0100, §Coverage and link discoverability, projection-shift correspondence derivation**: π is described as "identity on the Left region (v < p) and shift(·, n) on the Right region (v ≥ p)" plus identity on link-subspace contributions.
**Problem**: For π to be the bijection witness that LP11-style reasoning needs, the derivation should explicitly note that shift(·, n) maps Right (subspace s_C) into V_{s_C}(d') (closure within subspace s_C), invoking OrdAddHom (b) for subspace preservation. The derivation step "{shift(v, n) : v ∈ P_0^R}" assumes but doesn't verify that these images live in V_{s_C}(d').
**Required**: Add one sentence citing OrdAddHom (b clause, ASN-0036) to justify subspace preservation of the shift on Right.

### Issue 6: Atomicity discussion of "K.ρ commutes with K.μ⁻ and K.μ⁺" needs the J1★ caveat made explicit
**ASN-0100, §Atomicity and Canonical Order**: "K.ρ commutes with K.μ⁻ and K.μ⁺. K.ρ's precondition depends only on C and the entity set..."
**Problem**: Commutativity at the per-state level is correct, but the reader could read this as saying any ordering of K.ρ relative to K.μ⁻ and K.μ⁺ is admissible at the composite level. The composite-boundary couplings J0, J1★, J1'★ are evaluated at the boundary, but their satisfaction requires K.ρ to fire before the boundary regardless of position relative to K.μ⁺. This is implicit but worth stating: K.ρ may fire before K.μ⁺ (placing a_k); J1★ at the boundary is satisfied either way because the boundary observes the final state where both have committed.
**Required**: Add a clarifying sentence stating that K.ρ-before-K.μ⁺ is admissible because the composite-boundary couplings see the final state regardless of intermediate order.

### Issue 7: Empty-case worked example handles only sub-case (i.a)
**ASN-0100, §A Worked Example, "Empty-document first insertion"**: The worked example assumes V_{s_L}(d) = ∅ along with V_{s_C}(d) = ∅, which is case (i.a) of the substrate decomposition.
**Problem**: Case (i.b) — V_{s_C}(d) = ∅ but V_{s_L}(d) ≠ ∅ — is structurally distinct and is exactly the case the general substrate-decomposition discussion devotes the most space to. A worked example for (i.b) would concretely illustrate why K.μ⁻ omission is the canonical choice (and why the alternative requires K.μ⁺_L).
**Required**: Extend the empty-case worked example with a brief case (i.b) variant, or explicitly note that case (i.b) is conceptually identical to (i.a) for the INSERT specification (since V_{s_C}(d') depends only on the empty-content-subspace precondition, not on the link subspace's status).

### Issue 8: §Sequential text-subspace structure empty-case verification doesn't cite OrdinalShiftBase for the shift(p, 0) = p step
**ASN-0100, §Sequential text-subspace structure**: "the Insertion positions are `shift(p, k) = [s_C, 1, …, 1, 1 + k]` for `0 ≤ k < n`, by OrdAddHom"
**Problem**: OrdAddHom (b clause) gives `shift(v, n) = v ⊕ δ(n, m)` for n ≥ 1; the k=0 case requires OrdinalShiftBase's convention shift(t, 0) = t to give [s_C, 1, ..., 1, 1]. The derivation of "{1, 2, …, n}" as last components correctly includes k=0 yielding 1, but OrdinalShiftBase isn't cited at the k=0 step.
**Required**: Cite OrdinalShiftBase (ASN-0058) explicitly when handling k=0 in the empty-case derivation (it is cited elsewhere in the ASN, so consistency would help here).

## OUT_OF_SCOPE

None. The ASN correctly identifies link-subspace insertion, COPY, DELETE, REARRANGE, version derivation, and inter-server replication as out of scope, and does not attempt to specify them.

VERDICT: REVISE
