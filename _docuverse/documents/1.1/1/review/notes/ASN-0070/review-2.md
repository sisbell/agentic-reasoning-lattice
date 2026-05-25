# Review of ASN-0070

## REVISE

### Issue 1: Postcondition strict equality is too strong
**ASN-0070, Result Form and the Operation**: "`⟦Σ_V^S⟧ = R(d, L(ℓ).eᵢ)|_S`"
**Problem**: `⟦·⟧` is defined in ASN-0053 over all of T as `⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}`. For the worked example's span `([1, 4], δ(2, 2))` with reach `[1, 6]`, the denotation under T1 includes every tumbler `[1, 4, x_3, ...]` and `[1, 5, x_3, ...]` of depth > 2, in addition to `[1, 4]` and `[1, 5]`. But `R(d, e)|_S` is a set of V-positions, all of depth `m_S`. So `⟦Σ_V^S⟧ ⊋ R(d, e)|_S` strictly. The asserted set equality fails.
**Required**: Either define a V-restricted denotation `⟦Σ_V^S⟧_V := ⟦Σ_V^S⟧ ∩ {t : #t = m_S ∧ subspace(t) = S}` and use that in the postcondition, or restate the postcondition as an intersection equality. The worked example's verification of F-sound/F-complete silently uses the V-restricted reading; the postcondition should match.

### Issue 2: Contiguity proof's TS5 citation doesn't cover k₁ = 0
**ASN-0070, Computation via Decomposition**: "By TS5 (ShiftAmountMonotonicity), the mapping `k ↦ a + k` is strictly monotone: `k₁ < k₂ ⟹ a + k₁ < a + k₂` under T1."
**Problem**: TS5 requires `n₂ > n₁ ≥ 1`. The indices range `0 ≤ k₁ ≤ k₂ < n` and include `k₁ = 0`. When `k₁ = 0`, the inequality `a + 0 < a + k₂` (for `k₂ ≥ 1`) needs TS4 (ShiftStrictIncrease) combined with the OrdinalShiftBase convention `a + 0 = a` — not TS5.
**Required**: Cite TS4 + OrdinalShiftBase for the `k₁ = 0` case alongside TS5 for `k₁ ≥ 1`.

### Issue 3: V-subspace / I-subspace correspondence not derived
**ASN-0070, The Inverse-Image Relation**: "`R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L}`"
**Problem**: The ASN partitions R by V-subspace but doesn't derive the structural correspondence to I-subspace. By S3★ (ASN-0047) and L0 (ASN-0047): `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C) ⟹ subspace_I(M(d)(v)) = s_C`, and symmetrically for `s_L`. Therefore `R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` and `R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))`. This is load-bearing — it pins which portion of coverage contributes to which subspace component — and the ASN treats it implicitly. Open question 6 (subspace straddling) is in fact answered by this derivation.
**Required**: State and derive the correspondence as a lemma; remove or revise the corresponding open question.

### Issue 4: F-multi proof is over-engineered
**ASN-0070, F-multi**: "Unpack the inverse image as a union of singleton pre-images: `R(d, coverage(e)) = M(d)⁻¹(coverage(e)) = ⋃_{a ∈ coverage(e)} M(d)⁻¹({a})` ... By S5, the cardinality of this set is unbounded above..."
**Problem**: The conclusion (`v₁, v₂ ∈ R(d, e)`) follows directly from the inverse-image definition once the hypothesis (`M(d)(v_i) = a ∈ coverage(e)`) is given. The set-theoretic identity is not load-bearing; S5 establishes that the hypothesis is *structurally admissible*, not that the conclusion follows. The proof conflates two roles.
**Required**: Separate the admissibility argument (S5 — there exist states with this configuration) from the implication argument (definition of `R` — when the hypothesis holds, the conclusion follows).

### Issue 5: F-empty derivation not shown
**ASN-0070, F-empty**: "Depends. Definition of `R(d, e)`; vacuous inverse image of an empty intersection."
**Problem**: "Vacuous inverse image" is asserted, not derived. The actual chain is: `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅ ⟹ (A v ∈ dom(M(d)) :: M(d)(v) ∉ coverage(L(ℓ).eᵢ)) ⟹ R(d, L(ℓ).eᵢ) = ∅ ⟹ R(d, L(ℓ).eᵢ)|_S = ∅ ⟹ ⟦Σ_V^S⟧ = ∅ ⟹ Σ_V^S = ⟨⟩` (this last step using S2's normalization existence — only the empty span-set has empty denotation under canonical form).
**Required**: Write out the chain explicitly; the last step (`⟦Σ_V^S⟧ = ∅ ⟹ Σ_V^S = ⟨⟩`) needs the canonical-form assumption or an extra step.

### Issue 6: F-canonical uniqueness not derived
**ASN-0070, F-canonical**: "A given `R(d, e)` admits exactly one canonical form, by S9 applied per subspace and the fixed external ordering."
**Problem**: This is a one-line gesture toward a derivation that should be explicit. The chain is: (i) per-subspace level-uniformity from S8-depth and LinkVPositionDepthAxiom (so S9's precondition is met), (ii) S9 gives per-subspace uniqueness among equivalent span-sets, (iii) fixed external ordering removes ambiguity at the family level. Each step should be stated.
**Required**: Write out the derivation, including the verification of S9's level-uniformity precondition.

### Issue 7: F-det derivation chain not formalized
**ASN-0070, F-det Depends**: lists S2, S3★-aux, S9 individually.
**Problem**: "Depends" lists the foundations but no chain is written. The argument is: S2 ⟹ `M(d)⁻¹(coverage(e))` is uniquely determined ⟹ `R(d, e)` is unique ⟹ (by S3★-aux exhaustiveness) `R(d, e)|_S` is unique per subspace ⟹ (by S9 + external ordering) the canonical form is unique. The dependencies are correctly listed but the chain composing them is left implicit.
**Required**: Write out the inference chain.

### Issue 8: F-sound/F-complete categorization conflicts with role
**ASN-0070, F-sound / F-complete**: tagged "(IMPLEMENTATION OBLIGATION)"
**Problem**: The Claims Introduced table lists these as "OBLIGATION" — a kind not used elsewhere in the spec family. Either they are consequences of the postcondition (in which case they are derived lemmas, and verifying an implementation discharges them automatically by proving the postcondition), or they are independent requirements (in which case they need their own status). The "obligation" framing — "what a verifier must check" — is meta-level guidance, not a claim about the system. Mixing levels makes the claim ledger harder to verify.
**Required**: Either reclassify as LEMMA (derived from postcondition by set-equality unpacking) or move the verification-obligation guidance to a separate section so the claim table records only system-level claims.

### Issue 9: Open question already answered in body
**ASN-0070, Open Questions**: "Must the system distinguish the case where `L(ℓ).eᵢ = ∅` (the endset itself is empty) from the case where `L(ℓ).eᵢ ≠ ∅` but `R(d, L(ℓ).eᵢ) = ∅` ..."
**Problem**: The Slot Uniformity section already answers this: "The operation does not distinguish these cases in its result form." Either the answer is wrong and the question is genuinely open, or the question should be removed.
**Required**: Resolve the inconsistency — either remove the open question or qualify the body's claim.

### Issue 10: F0 and F1 not labeled in body
**ASN-0070, Claims Introduced table**: lists F0 (the R relation) and F1 (the follow operation).
**Problem**: Every other claim (F-det, F-sound, ..., F-contig) is introduced via an explicit `### F-name — Name (KIND)` heading in the body. F0 and F1 are introduced via prose ("The Inverse-Image Relation", "Result Form and the Operation") with no label. A reader looking up F0 or F1 must infer from context.
**Required**: Add explicit F0 and F1 headings in the body, parallel to the other claims.

## OUT_OF_SCOPE

The remaining open questions (partial-reach reporting, concurrency semantics, transclusion-lineage relationships, ordering guarantees, representational compactness, content-retrieval coupling, canonicalisation-procedure exposure) are appropriate territory for future ASNs — they extend rather than fix the FOLLOWLINK specification.

VERDICT: REVISE
