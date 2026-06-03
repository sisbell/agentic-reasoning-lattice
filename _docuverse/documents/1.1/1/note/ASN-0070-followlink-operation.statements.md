# ASN-0070 Claim Statements

*Source: ASN-0070-followlink-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## Definition — Coverage

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```

where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). `e` is a finite set of well-formed I-spans (L3, ASN-0043). The coverage is a subset of `T`.

## Definition — SubspaceRestriction

```
R(d, e)|_S := {v ∈ R(d, e) : subspace(v) = S}    for S ∈ {s_C, s_L}
```

## Definition — VRestrictedDenotation

When `m_S(d)` is defined, for a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
```

**Vacuous-subspace convention.** When `m_S(d)` is undefined (i.e., `V_S(d) = ∅`): `Σ_V^S = ⟨⟩` and `⟦⟨⟩⟧_V := ∅`.

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

The two subspace components are disjoint by `s_C ≠ s_L` (SC-NEQ) together with the V-restriction filter's subspace clause.

## Definition — BlockExtents

For a mapping block `β = (v, a, n)`:

- `I(β) = {a + k : 0 ≤ k < n}` — I-extent (the contribution of this block to `ran(M(d))`)
- `V(β) = {v + k : 0 ≤ k < n}` — V-extent

By B3 (Consistency, ASN-0058), every `v + k ∈ V(β)` lies in `dom(M(d))`; M-int (TumblerIntervalCharacterization, ASN-0058) gives `subspace(v + k) = subspace(v)`, so each block lives in one V-subspace.

## Definition — ConsecutiveTumblers

For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, we say `t, t'` are *consecutive* iff no depth-`m_S(d)` subspace-`S` tumbler `t''` satisfies `t < t'' < t'` under T1.

**Characterisation.** For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, consecutivity holds iff `t_i = t'_i` for `1 ≤ i < m_S(d)` and `t'_m = t_m + 1`.

A *maximal run* in a set `X` of such tumblers is a maximal subset of `X` that forms a chain under the consecutivity relation — its elements can be ordered `t_0 < t_1 < ... < t_{c-1}` with each `t_i` consecutive to `t_{i+1}`. Maximal runs partition `X`.

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

The definition is *abstract*: `R(d, e)` is a function of coverage and arrangement alone, so two endsets with the same coverage produce the same `R(d, e)` regardless of how `M(d)` is stored or how spans within `e` are structured.

---

## F1 — FollowOperation (DEF, function)

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)` (well-defined when `V_S(d) ≠ ∅`), and the empty component `Σ_V^S = ⟨⟩` is admissible, satisfying:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**V-restricted denotation:**

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
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

---

## F-canon-form — CanonicalForm (DEF, predicate)

The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component span in each `Σ_V^S` is a level-uniform span `σ = (s, δ(c, m_S(d)))` whose start `s` is a depth-`m_S(d)` tumbler satisfying `subspace(s) = S` and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (so `s` is an admissible V-position by S8a), and whose width is an ordinal displacement `δ(c, m_S(d)) = [0, ..., 0, c]` of depth `m_S(d)` with `c ≥ 1`.

(ii) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(iii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second.

In the vacuous case (`V_S(d) = ∅`), `Σ_V^S = ⟨⟩` (V-Restricted Denotation).

---

## F-canonical — CanonicalExistenceAndUniqueness (THM, theorem)

Given `R(d, e)`, there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form.

---

## F-det — DenotationalDeterminism (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** For two evaluations of `follow(ℓ, d, i)` against the same state `Σ`, returning `(d, Σ_V)` and `(d, Σ_V')`: `⟦Σ_V^S⟧_V = ⟦Σ_V'^S⟧_V` for each subspace `S`. The V-restricted denotation `⟦Σ_V^S⟧_V` is uniquely determined by `Σ`, `ℓ`, `d`, `i`.

---

## F-sound — Soundness (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** Every `v ∈ ⟦Σ_V^S⟧_V` (any subspace `S`) satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`.

---

## F-complete — Completeness (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies `v ∈ ⟦Σ_V^S⟧_V` for `S = subspace(v)`.

---

## F-empty — EmptyAdmissibility (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`; additionally `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅` in `Σ`.

**Postcondition.** `⟦Σ_V^{s_C}⟧_V = ∅` and `⟦Σ_V^{s_L}⟧_V = ∅`. Under canonical form, both components are the empty span-set: `Σ_V^{s_C} = ⟨⟩` and `Σ_V^{s_L} = ⟨⟩`. The operation succeeds and returns `(d, (Σ_V^{s_C}, Σ_V^{s_L}))` with both V-restricted denotations empty — empty resolution is a normal result, not an error.

---

## F-multi — MultiplicityPreservation (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`; additionally `a ∈ dom(Σ.C)` (a content I-address, so `subspace_I(a) = s_C` by K.α, ASN-0047), and `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** With `S = s_C`, both `v₁ ∈ ⟦Σ_V^{s_C}⟧_V` and `v₂ ∈ ⟦Σ_V^{s_C}⟧_V` — the two distinct V-positions inhabit the content subspace and both appear in the result.

---

## F-slot — SlotUniformity (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `i, i' ∈ {1, ..., |L(ℓ)|}`.

**Postcondition.** For any two slot indices `i, i'`, `follow(ℓ, d, i)` and `follow(ℓ, d, i')` are computed by the same definition: `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` and `⟦Σ_V'^S⟧_V = R(d, L(ℓ).eᵢ')|_S` respectively. The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing.

The outcome `R(d, eᵢ) = ∅` is uniformly admissible whether the cause is `eᵢ = ∅` (vacuous coverage) or coverage that misses the arrangement; the result form does not distinguish them.

---

## F-contig — Contiguity (LEMMA, lemma)

**Preconditions.** A mapping block `β = (v, a, n)` of `M(d)` (ASN-0058) and an endset I-span `σ = (s, ℓ_σ)` satisfying T12 (SpanWellDefinedness, ASN-0034).

**Postcondition.** `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression `{a + j + k : 0 ≤ k < c}` of `I(β)`, for some offset `j` and width `c`; the corresponding V-positions `v + j, ..., v + j + c − 1` form a single contiguous V-run within `β`.

---

## F-origin — OriginSymmetry (LEMMA, lemma)

**Preconditions.** `v ∈ R(d, L(ℓ).eᵢ)`.

**Postcondition.** Membership of `v` in `R(d, L(ℓ).eᵢ)` is determined by `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` alone. The home of `M(d)(v)` — `origin(M(d)(v))` for content addresses (S7, ASN-0036), `home(M(d)(v))` for link addresses (Definition Home, ASN-0043) — does not appear in the membership condition.

---

## F-persist — LinkPersistence (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)` at state `Σ`; `Σ → Σ'` is a valid transition.

**Postcondition.** `ℓ ∈ dom(Σ'.L)` regardless of any reach condition on `coverage(L(ℓ).eᵢ)` versus `ran(M(d))`.

---

## F-state — StateDependenceCorollary (COROLLARY, lemma)

**Preconditions.** `Σ → Σ'` reachable.

**Postcondition.** `R_Σ(d, L(ℓ).eᵢ)` and `R_{Σ'}(d, L(ℓ).eᵢ)` may differ even though `L_Σ(ℓ) = L_{Σ'}(ℓ)` (by L12). The difference, when present, originates entirely in `M_Σ(d) ≠ M_{Σ'}(d)`.

---

## F-multidoc — NoPreferredDocument (LEMMA, lemma)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism. The home document `home(ℓ)` (Definition Home, ASN-0043) — the allocator of `ℓ`'s address, which need not be where the endset's content lives nor where the link is encountered — plays no privileged role.

No precondition of `follow` references `home(ℓ)`.
