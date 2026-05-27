# Review of ASN-0101

## REVISE

### Issue 1: D1 justification cites wrong lemmas
**ASN-0101, §"What shifts: closing the gap", D1 justification**: "Order preservation and injectivity follow from TS1 and TS2 applied to the equal-length, last-component-only shift produced by `σ_d`."

**Problem**: TS1 (ShiftOrderPreservation) and TS2 (ShiftInjectivity) are properties of `shift(v, n) = v ⊕ δ(n, #v)` — addition-based. But the operation defines `σ_d(v) = vpos(S, ord(v) ⊖ δ(n, m_S)_{ord})` — subtraction-based. The cited lemmas do not apply to subtraction-based maps.

**Required**: Replace with TA3-strict (which gives `a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b ⟹ a ⊖ w < b ⊖ w`), composed with OrdinalOrderEquivalence to lift to V-positions. Verify the preconditions of TA3-strict — `ord(v) ≥ δ(n)_{ord}` from `v ≥ r` in R, and `#ord(v₁) = #ord(v₂) = m_S − 1` from S8-depth. Or cite ASN-0082's D-BJ analogously and explain the extension from m = 2 to general m_S ≥ 2.

### Issue 2: D7 statement omits link store membership
**ASN-0101, §"Attribution survival"**: "`a ∈ dom(C')  ∧  origin(a) at Σ' = origin(a) at Σ`"

**Problem**: The premise is "I-address `a` that appeared in `ran(M(d))`". When the deleted span is in the link subspace (S = s_L), the V-positions map into `dom(L)`, not `dom(C)`. The justification correctly derives `a ∈ dom(C') ∪ dom(L')`, but the stated postcondition `a ∈ dom(C')` is false for link-subspace I-addresses by L14 (disjointness).

**Required**: Strengthen the statement to `a ∈ dom(C') ∪ dom(L') ∧ origin(a) at Σ' = origin(a) at Σ`, or split into two clauses by subspace.

### Issue 3: D0 frame omits E and R
**ASN-0101, §"The operation", D0 frame**: Only frames `C`, `L`, `dom(M)`, and `M(d')` for `d' ≠ d`.

**Problem**: The foundation state space includes `Σ.E` (entity set) and `Σ.R` (provenance relation) from ASN-0047. The analogous K.μ⁻ in ASN-0047 (J2) explicitly states `C' = C ∧ L' = L ∧ E' = E ∧ R' = R`. ASN-0101's frame is silent on E and R, leaving unspecified whether DELETE could affect entity allocation or provenance recording.

**Required**: Add `E' = E` and `R' = R` to D0's frame clause. Adjust D2/D3-style preservation claims for these components if appropriate.

### Issue 4: D8 missing invariants
**ASN-0101, §"Well-formedness preservation"**: D8 addresses S2, S8-fin, S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★.

**Problem**: Several foundation invariants the operation must preserve are not addressed:
- CL-OWN, CL-UNIQ (ASN-0047): link subspace ownership and injectivity
- S7a, S7b, S7c, S7d (ASN-0036): content allocation discipline
- L0, L1, L1a–c, L3, L12 (ASN-0043/0093): link well-formedness
- S8★ (ASN-0047): per-subspace span decomposition
- P0, P1, P2, P3, P4★, P4a, P6, P7, P7a, P8 (ASN-0047): permanence and existence

Each is in scope because each is a per-state or per-transition invariant of `Σ`. Most are trivially preserved (DELETE doesn't touch C, L, E, R), but trivial preservation still needs to be asserted — that's the point of the well-formedness theorem.

**Required**: Extend D8 to cover all foundation invariants of ASN-0047's ExtendedReachableStateInvariants, or state a meta-lemma "all foundation invariants preserved" with a structural argument grounded in D2, D3, D5, D6, and the framing of E and R.

### Issue 5: Relationship to foundation transition vocabulary unspecified
**ASN-0101, throughout**: DEL[d, σ] is specified as "an atomic state transition" without stating whether it extends ASN-0047's transition vocabulary or decomposes into existing operations.

**Problem**: ASN-0047's ValidComposite★ enumerates K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ. K.μ⁻ is suffix truncation only; K.μ~ permutes without removing. Neither directly produces middle-span deletion with shift. ASN-0101 introduces an operation whose relationship to the foundation transition vocabulary is unclear, leaving open whether (a) DEL is a new atomic transition extending the vocabulary, (b) DEL is a derived composite (e.g., K.μ⁻ + K.μ~ in some pattern), or (c) DEL replaces K.μ⁻.

**Required**: State explicitly whether DEL extends the transition vocabulary as a new atomic kind, or how DEL decomposes into existing transitions. If it extends, the ASN must update or supplement ValidComposite★'s coupling constraints (J0, J1★, J1'★) for DEL.

### Issue 6: D8 cites OrdShiftHom incorrectly
**ASN-0101, §"Well-formedness preservation", D8 justification**: "positions in `Q` are shifts at the same depth by OrdShiftHom"

**Problem**: OrdShiftHom (ASN-0036) gives `ord(shift(v, n)) = shift(ord(v), n)` — an addition-based homomorphism. The σ_d function uses subtraction; OrdShiftHom does not apply.

**Required**: Replace the citation with TumblerSub's result-length identity (`#(a ⊖ w) = max(#a, #w)`), combined with vpos's length-preserving construction (`#vpos(S, o) = #o + 1`), to conclude depth preservation under σ_d.

### Issue 7: No concrete worked example
**ASN-0101, throughout**: The ASN gives prose discussion and abstract claims but no specific numeric scenario.

**Problem**: Per review standards, a specification should verify its key postconditions against at least one concrete example. As written, the reader must construct examples mentally to check that the effect, the bijection σ_d, and the post-state structure are coherent.

**Required**: Add at least one worked example showing input state, parameters, and step-by-step verification of D1, D8, D9. For instance: "d with V_1(d) = {[1,1,1], [1,1,2], [1,1,3], [1,1,4]} (n_S = 4, m_S = 3), mapping to I-addresses (a₁, a₂, a₃, a₄). DELETE at s = [1,1,2] with ℓ = δ(2, 3). Verify L = {[1,1,1]}, X = {[1,1,2], [1,1,3]}, R = {[1,1,4]}, σ_d([1,1,4]) = [1,1,2], post-state V_1 = {[1,1,1], [1,1,2]} mapping to (a₁, a₄)."

### Issue 8: Boundary cases not systematically addressed
**ASN-0101**: D8 establishes well-formedness "by D1" but doesn't walk through edge configurations.

**Problem**: Boundary cases stress different parts of the specification:
- Deletion emptying V_S (n = n_S, p = 1): D-MIN★ becomes vacuous; need to verify other subspace untouched
- Deletion at start (p = 1, n < n_S): L = ∅, Q maps to L's positions, D-MIN★ holds via σ_d(r) = [S, 1, ..., 1]
- Deletion at end (p + n = n_S + 1): R = ∅, no shift occurs
- Singleton deletion (n_S = 1, n = 1): both L and R empty
- Cross-region deletion of single position (n = 1, interior): shifts everything to the right

These appear casually in prose but no section systematically verifies D0's effect and D8's preservation for each.

**Required**: Add a boundary cases subsection enumerating these configurations and confirming D0–D8 hold for each.

### Issue 9: D1's contiguity claim has an undefined edge case
**ASN-0101, §"What shifts: closing the gap", D1**: "(L ∪ Q) is contiguous with minimum [S, 1, ..., 1]"

**Problem**: When n_S' = 0 (deletion empties the subspace), V_S(M'(d)) = ∅, and "minimum" is undefined. The parenthetical aside "(empty when n_S' = 0)" handles the form but the prose statement asserts a minimum that doesn't exist in the empty case.

**Required**: Reword: "When V_S(M'(d)) is non-empty, it is contiguous with minimum [S, 1, ..., 1] of depth m_S; otherwise V_S(M'(d)) = ∅ and D-CTG★, D-MIN★, D-SEQ★ hold vacuously."

### Issue 10: D9's third clause uses inconsistent quantification
**ASN-0101, §"Link discoverability", D9 third clause**: "the projection equals `(project(L(ℓ).eᵢ, d, Σ) ∩ L) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ R}`"

**Problem**: The expression `project(L(ℓ).eᵢ, d, Σ) ∩ L` mixes a set of V-positions in `dom(M(d))` (left-hand side) with the region `L ⊆ V_S(d)` (right-hand side). The intersection is meaningful only because both inhabit `dom(M(d))`, but the reader has to derive that — the projection ranges over all subspaces, while L is subspace-S-restricted. The clause is implicitly restricted to subspace S but doesn't say so.

**Required**: Either restrict the LHS to subspace S explicitly: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ V_S(d) ∩ L) ∪ ...`, or redefine L, X, R as subsets of `dom(M(d))` rather than V_S(d).

## OUT_OF_SCOPE

### Topic 1: Versioning mechanism for arrangement reconstruction
The ASN raises (as an open question) how the post-DELETE state plus a versioning mechanism enables reconstruction of pre-DELETE arrangements. This is genuine future work — versioning is a separate concern from DELETE itself.

### Topic 2: Orphan I-address enumeration
The ASN observes that after DELETE, some I-addresses may be unreferenced by any arrangement. No operation to enumerate or discover these orphans is specified. This is a future ASN, not a defect in DELETE's specification.

### Topic 3: Causal ordering across documents
DELETE on `d` followed by DELETE on a transcluding `d'` raises causal ordering questions noted in the Open Questions. This is foundational to the broader transition model, not specific to DELETE.

VERDICT: REVISE
