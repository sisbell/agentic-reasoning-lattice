# ASN-0070 Claim Statements

*Source: ASN-0070-followlink-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

## Definition — Coverage

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```
where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). `e` is a finite set of well-formed I-spans. The coverage is a subset of `T`.

## Definition — VRestrictedDenotation

When `m_S(d)` is defined, for a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
```

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

When `m_S(d)` is undefined (only `S = s_C` when `V_{s_C}(d) = ∅`): `Σ_V^S = ⟨⟩` and `⟦⟨⟩⟧_V := ∅`.

## Definition — BlockIExtent

Each block `β = (v, a, n)` describes a contiguous mapping run: V-positions `v, v+1, ..., v+n−1` map to I-addresses `a, a+1, ..., a+n−1`. The I-extent:

```
I(β) = {a + k : 0 ≤ k < n}
```

---

## F0 — InverseImageRelation (DEF, function)

**Domain.** `d ∈ E_doc`; `e` is an endset — a finite set of well-formed I-spans (L3, ASN-0043). `coverage(e) ⊆ T` is the union of span coverages.

**Definition.**

```
R(d, e) := M(d)⁻¹(coverage(e)) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e) }
```

**Subspace partition.** Writing `R(d, e)|_S := {v ∈ R(d, e) : subspace(v) = S}` for `S ∈ {s_C, s_L}`:

```
R(d, e) = R(d, e)|_{s_C} ⊎ R(d, e)|_{s_L}
```

The partition is disjoint (subspace is single-valued per the first-component projection) and exhaustive (every `v ∈ dom(M(d))` has `subspace(v) ∈ {s_C, s_L}` by S3★-aux of ASN-0047).

**Well-definedness.** By S2 (ArrangementFunctionality, ASN-0036), `M(d)` is a partial function — every V-position in its domain has exactly one image. The inverse image of `coverage(e)` is therefore a uniquely determined subset of `dom(M(d))`.

**Frame.** State-pure: `R` reads `M(d)` and `coverage(e)`; modifies nothing.

---

## F1 — FollowOperation (DEF, function)

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)`, and:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**Frame.** `Σ' = Σ`. No component of state is modified.

---

## F-subspace — IOSubspaceCorrespondence (LEMMA, lemma)

**Preconditions.** `v ∈ dom(M(d))`.

**Postcondition.** `subspace(v) = subspace_I(M(d)(v))`. In particular:
- `subspace(v) = s_C ⟹ subspace_I(M(d)(v)) = s_C`
- `subspace(v) = s_L ⟹ subspace_I(M(d)(v)) = s_L`

**Consequence.** The subspace projection of `R` decomposes by I-subspace:

```
R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))
R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))
```

The biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` for `v ∈ dom(M(d))` holds by case analysis:

— *Forward* (`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`): direct from S3★ (GeneralizedReferentialIntegrity, ASN-0047).

— *Reverse* (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`): by S3★-aux (SubspaceExhaustiveness, ASN-0047), `subspace(v) ∈ {s_C, s_L}`. Suppose for contradiction `subspace(v) = s_L`; then by S3★'s second clause `M(d)(v) ∈ dom(L)`; by L14 (StoreDisjointness, ASN-0047), `dom(C) ∩ dom(L) = ∅`, contradicting `M(d)(v) ∈ dom(C)`.

The `s_L` case is symmetric.

**Frame.** State-pure.

---

## F-canonical — CanonicalForm (DEF, function)

The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component span in each `Σ_V^S` has start `s` with `#s = m_S(d)`, `subspace(s) = S`, and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (so `s` is an admissible V-position by S8a), and width of the form `δ(c, m_S(d)) = [0, ..., 0, c]` — an *ordinal displacement* of depth `m_S(d)`.

(ii) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(iii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second.

When `m_S(d)` is undefined (only `S = s_C` with `V_{s_C}(d) = ∅`), the canonical form is `Σ_V^S = ⟨⟩` by the V-restricted denotation convention.

---

## F-det — DenotationalDeterminism (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** For two evaluations of `follow(ℓ, d, i)` against the same state `Σ`, returning `(d, Σ_V)` and `(d, Σ_V')`: `⟦Σ_V^S⟧_V = ⟦Σ_V'^S⟧_V` for each subspace `S`. The V-restricted denotation is uniquely determined by `Σ`, `ℓ`, `d`, `i`. The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide.

**Depends.** S2 (ArrangementFunctionality, ASN-0036); S3★-aux (SubspaceExhaustiveness, ASN-0047); S9 (NormalizationUniqueness, ASN-0053); F-canonical.

**Frame.** No state modification.

---

## F-sound — Soundness (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** Every `v ∈ ⟦Σ_V^S⟧_V` (any subspace `S`) satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`.

This is the `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S` direction of the postcondition's set equality.

**Depends.** Postcondition of `follow` (F1); definition of `R(d, e)` (F0).

**Frame.** No state modification.

---

## F-complete — Completeness (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies `v ∈ ⟦Σ_V^S⟧_V` for `S = subspace(v)`.

This is the `R(d, L(ℓ).eᵢ)|_S ⊆ ⟦Σ_V^S⟧_V` direction of the postcondition's set equality.

**Depends.** Postcondition of `follow` (F1); definition of `R(d, e)` (F0).

**Frame.** No state modification.

---

## F-empty — EmptyAdmissibility (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`; additionally `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅` in `Σ`.

**Postcondition.** `⟦Σ_V^{s_C}⟧_V = ∅` and `⟦Σ_V^{s_L}⟧_V = ∅`. Under canonical form, both components are the empty span-set: `Σ_V^{s_C} = ⟨⟩` and `Σ_V^{s_L} = ⟨⟩`. The operation succeeds and returns `(d, (Σ_V^{s_C}, Σ_V^{s_L}))` with both V-restricted denotations empty.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-canonical; S9 (NormalizationUniqueness, ASN-0053).

**Frame.** No state modification.

---

## F-multi — MultiplicityPreservation (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`; additionally `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)` and `subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a)`, so `subspace(v₁) = subspace(v₂) = subspace_I(a)` — both V-positions inhabit the same subspace. Writing `S := subspace_I(a)`, both `v₁ ∈ ⟦Σ_V^S⟧_V` and `v₂ ∈ ⟦Σ_V^S⟧_V`.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-subspace; S3★-aux (SubspaceExhaustiveness, ASN-0047); S5 (UnrestrictedSharing, ASN-0036) ensures the hypothesis is structurally realisable.

**Frame.** No state modification.

---

## F-frame — Frame (INV, predicate)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `Σ' = Σ`. Specifically: `C' = C`, `M' = M`, `L' = L`, `E' = E`, `R' = R`.

**Depends.** Definition of `follow` as a query (no effect clause).

---

## F-slot — SlotUniformity (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `i, i' ∈ {1, ..., |L(ℓ)|}`.

**Postcondition.** For any two slot indices `i, i'`, `follow(ℓ, d, i)` and `follow(ℓ, d, i')` are computed by the same definition: `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` and `⟦Σ_V'^S⟧_V = R(d, L(ℓ).eᵢ')|_S` respectively. The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing.

**Depends.** Slot accessor L6 (SlotDistinction, ASN-0043); L3's asymmetric well-formedness (`e₃ ≠ ∅` required, others may be empty) constrains link construction, not resolution.

**Frame.** No state modification.

---

## F-origin — OriginSymmetry (LEMMA, lemma)

**Preconditions.** `v ∈ R(d, L(ℓ).eᵢ)`.

**Postcondition.** Membership of `v` in `R(d, L(ℓ).eᵢ)` is determined by `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` alone. The home of `M(d)(v)` — `origin(M(d)(v))` for content addresses (S7, ASN-0036), `home(M(d)(v))` for link addresses (Definition LinkHome, ASN-0043) — does not appear in the membership condition.

**Depends.** Definition of `R(d, e)`.

**Frame.** No state modification.

---

## F-persist — LinkPersistence (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)` at state `Σ`; `Σ → Σ'` is a valid transition.

**Postcondition.** `ℓ ∈ dom(Σ'.L)` regardless of any reach condition on `coverage(L(ℓ).eᵢ)` versus `ran(M(d))`.

**Depends.** L12 (LinkImmutability, ASN-0043) — the link store is monotonic and value-preserving; L12a (LinkStoreMonotonicity, ASN-0043).

**Frame.** No state modification by `follow` itself; the persistence is a property of `Σ.L` across transitions.

---

## F-state — StateDependenceCorollary (COROLLARY, lemma)

**Preconditions.** `Σ → Σ'` reachable.

**Postcondition.** `R_Σ(d, L(ℓ).eᵢ)` and `R_{Σ'}(d, L(ℓ).eᵢ)` may differ even though `L_Σ(ℓ) = L_{Σ'}(ℓ)` (by L12). The difference, when present, originates entirely in `M_Σ(d) ≠ M_{Σ'}(d)`.

**Depends.** L12 (link state-invariance); the transition semantics of ASN-0047 that admit `M(d)` to vary across transitions.

**Frame.** No state modification.

---

## F-multidoc — NoPreferredDocument (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism. The home document `home(ℓ)` (Definition LinkHome, ASN-0043) plays no privileged role.

**Depends.** No precondition of `follow` references `home(ℓ)`.

**Frame.** No state modification.

---

## F-contig — Contiguity (LEMMA, lemma)

**Statement.** For any mapping block `β = (v, a, n)` and endset I-span `σ = (s, ℓ_σ)` with coverage `⟦σ⟧`: `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` where `j` is the smallest qualifying index and `j + c − 1` is the largest.

**Sub-claims:**

(a) *Strict monotonicity of the index-to-tumbler map.* For `0 ≤ k₁ < k₂ < n`: `a + k₁ < a + k₂`. Case `1 ≤ k₁ < k₂`: by TS5 (ShiftAmountMonotonicity, ASN-0034). Case `k₁ = 0, k₂ ≥ 1`: by OrdinalShiftBase (`a + 0 = a`) and TS4 (ShiftStrictIncrease, ASN-0034), `a < a + k₂`.

(b) *Order-convexity of `⟦σ⟧`.* For `t₁, t₂ ∈ ⟦σ⟧` and `t₁ ≤ t' ≤ t₂`: `t' ∈ ⟦σ⟧` — by T12 (SpanWellDefinedness order-convexity postcondition (c), ASN-0034).

(c) *Contiguity.* Suppose `a + k₁, a + k₂ ∈ I(β) ∩ ⟦σ⟧` with `0 ≤ k₁ ≤ k₂ < n`. For any `k` with `k₁ ≤ k ≤ k₂`: by (a), `a + k₁ ≤ a + k ≤ a + k₂`; by (b) and both endpoints in `⟦σ⟧`, `a + k ∈ ⟦σ⟧`; since `0 ≤ k < n`, also `a + k ∈ I(β)`. Hence `a + k ∈ I(β) ∩ ⟦σ⟧`. The intersection contains every index between its minimum and maximum.

**Depends.** TS5 (ShiftAmountMonotonicity, ASN-0034); TS4 (ShiftStrictIncrease, ASN-0034); OrdinalShiftBase (ASN-0058); T12 (SpanWellDefinedness, ASN-0034).

**Frame.** No state modification.
