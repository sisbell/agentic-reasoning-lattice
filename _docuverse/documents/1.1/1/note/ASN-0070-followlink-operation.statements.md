# ASN-0070 Claim Statements

*Source: ASN-0070-followlink-operation.md (revised 2026-05-25) — Extracted: 2026-06-02*

## Definition — Coverage

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```

where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). The coverage is a subset of `T`, fixed at link creation and immutable thereafter.

## Definition — SubspaceProjection

For `S ∈ {s_C, s_L}`:

```
R(d, e)|_S := {v ∈ R(d, e) : subspace(v) = S}
```

## Definition — VRestrictedDenotation

When `m_S(d)` is defined, for a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
```

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

When `m_S(d)` is undefined (i.e., `V_S(d) = ∅`): `Σ_V^S = ⟨⟩` and `⟦⟨⟩⟧_V := ∅`.

## Definition — ConsecutiveTumblers

For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, `t` and `t'` are *consecutive* iff no depth-`m_S(d)` subspace-`S` tumbler `t''` satisfies `t < t'' < t'` under T1.

**Characterisation.** For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, consecutivity holds iff `t_i = t'_i` for `1 ≤ i < m_S(d)` and `t'_m = t_m + 1`.

## Definition — MaximalRun

A *maximal run* in a set `X` of depth-`m_S(d)` subspace-`S` tumblers is a maximal subset of `X` that forms a chain under the consecutivity relation — its elements can be ordered `t_0 < t_1 < ... < t_{c-1}` with each `t_i` consecutive to `t_{i+1}`.

---

## F0 — InverseImageRelation (DEF)

**Domain.** `d ∈ E_doc`; `e` is an endset — a finite set of well-formed I-spans. `coverage(e) ⊆ T` is the union of span coverages.

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

## F1 — FollowOperation (DEF)

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)` when `V_S(d) ≠ ∅`; when `V_S(d) = ∅` (so `m_S(d)` is undefined), `Σ_V^S = ⟨⟩` by the V-restricted denotation convention. In either case:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**V-restricted denotation.**

```
⟦Σ_V^S⟧_V := {t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1)}
```

**Frame.** `Σ' = Σ`. No component of state is modified.

---

## F-subspace — IOSubspaceCorrespondence (LEMMA)

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
- *Forward* (`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`): direct from S3★ (GeneralizedReferentialIntegrity, ASN-0047).
- *Reverse* (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`): by S3★-aux, `subspace(v) ∈ {s_C, s_L}`; if `subspace(v) = s_L` then by S3★, `M(d)(v) ∈ dom(L)`, contradicting `M(d)(v) ∈ dom(C)` via L14 (StoreDisjointness: `dom(C) ∩ dom(L) = ∅`).

**Frame.** State-pure.

---

## F-canon-form — CanonicalForm (DEF)

The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component span in each `Σ_V^S` has start `s` with `#s = m_S(d)`, `subspace(s) = S`, and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (so `s` is an admissible V-position by S8a), and width of the form `δ(c, m_S(d))` — an *ordinal displacement* of depth `m_S(d)`.

(ii) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(iii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second.

When `m_S(d)` is undefined (either subspace `S ∈ {s_C, s_L}` with `V_S(d) = ∅`), the canonical form is `Σ_V^S = ⟨⟩` by the V-restricted denotation convention.

---

## F-canonical — CanonicalUniqueness (THM)

Given `R(d, e)`, there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form.

**Existence.** Each subspace component is built by partitioning `R(d, e)|_S` into maximal runs of consecutive tumblers and mapping each run to an ordinal-displacement span; the normalised existence of which S8 (NormalizationExistence, ASN-0053) underwrites.

**Uniqueness.** Ordinal-displacement widths are forced by finite V-restricted denotation + subspace confinement (case analysis on `actionPoint(ℓ)`: only `k = m_S(d)` produces finite `⟦σ⟧_V`); the bridge `⟦·⟧_V` determines `⟦·⟧` (for canonical-form spans, `s = min(⟦σ⟧_V)` and `c = |⟦σ⟧_V|` are recoverable), lifting S9 to V-restricted equivalence; fixed external ordering (`s_C` first, `s_L` second) pins down family form.

**Ordinal displacement characterisation.** For `σ = (s, δ(c, m_S(d)))` with `#s = m_S(d)`, `subspace(s) = S`, and `s` positive:

```
⟦σ⟧_V = {[s_1, ..., s_{m-1}, s_m + j] : 0 ≤ j < c}
```

with `|⟦σ⟧_V| = c` (finite), and `s = min(⟦σ⟧_V)`.

---

## F-det — DenotationalDeterminism (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** For two evaluations of `follow(ℓ, d, i)` against the same state `Σ`, returning `(d, Σ_V)` and `(d, Σ_V')`:

```
⟦Σ_V^S⟧_V = ⟦Σ_V'^S⟧_V    for each subspace S
```

The V-restricted denotation is uniquely determined by `Σ`, `ℓ`, `d`, `i`. The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide.

**Depends.** S2 (ArrangementFunctionality, ASN-0036); S3★-aux (SubspaceExhaustiveness, ASN-0047); S8 (NormalizationExistence, ASN-0053); S9 (NormalizationUniqueness, ASN-0053); F-canonical.

**Frame.** No state modification.

---

## F-sound — Soundness (LEMMA)

**Preconditions.** As `follow`.

**Postcondition.** Every `v ∈ ⟦Σ_V^S⟧_V` (any subspace `S`) satisfies:

```
v ∈ dom(M(d))  ∧  M(d)(v) ∈ coverage(L(ℓ).eᵢ)
```

Equivalently: `⟦Σ_V^S⟧_V ⊆ R(d, L(ℓ).eᵢ)|_S`.

**Depends.** Postcondition of `follow` (F1); definition of `R(d, e)` (F0).

**Frame.** No state modification.

---

## F-complete — Completeness (LEMMA)

**Preconditions.** As `follow`.

**Postcondition.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies:

```
v ∈ ⟦Σ_V^S⟧_V    for S = subspace(v)
```

Equivalently: `R(d, L(ℓ).eᵢ)|_S ⊆ ⟦Σ_V^S⟧_V`.

**Depends.** Postcondition of `follow` (F1); definition of `R(d, e)` (F0).

**Frame.** No state modification.

---

## F-empty — EmptyAdmissibility (LEMMA)

**Preconditions.** As `follow`; additionally `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅` in `Σ`.

**Postcondition.**

```
⟦Σ_V^{s_C}⟧_V = ∅  ∧  ⟦Σ_V^{s_L}⟧_V = ∅
```

Under canonical form, both components are the empty span-set:

```
Σ_V^{s_C} = ⟨⟩  ∧  Σ_V^{s_L} = ⟨⟩
```

The operation succeeds and returns `(d, (Σ_V^{s_C}, Σ_V^{s_L}))` with both V-restricted denotations empty.

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-canonical; S9 (NormalizationUniqueness, ASN-0053).

**Frame.** No state modification.

---

## F-multi — MultiplicityPreservation (LEMMA)

**Preconditions.** As `follow`; additionally `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** By F-subspace:

```
subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)
subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a)
```

so `subspace(v₁) = subspace(v₂) = subspace_I(a)`. Writing `S := subspace_I(a)`:

```
v₁ ∈ ⟦Σ_V^S⟧_V  ∧  v₂ ∈ ⟦Σ_V^S⟧_V
```

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-subspace; S3★-aux (SubspaceExhaustiveness, ASN-0047); K.μ⁺ (ArrangementExtension, ASN-0047) — content-side non-injectivity ensures hypothesis is reachable; S5 (UnrestrictedSharing, ASN-0036) — abstract-cardinality point only.

**Frame.** No state modification.

---

## F-frame — Frame (INV)

**Preconditions.** As `follow`.

**Postcondition.** `Σ' = Σ`. Specifically:

```
C' = C  ∧  M' = M  ∧  L' = L  ∧  E' = E  ∧  R' = R
```

**Depends.** Definition of `follow` as a query (no effect clause).

**Frame.** The frame condition itself.

---

## F-slot — SlotUniformity (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `i, i' ∈ {1, ..., |L(ℓ)|}`.

**Postcondition.** For any two slot indices `i, i'`, `follow(ℓ, d, i)` and `follow(ℓ, d, i')` are computed by the same definition:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S
⟦Σ_V'^S⟧_V = R(d, L(ℓ).eᵢ')|_S
```

respectively for each `S ∈ {s_C, s_L}`. The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing.

**Depends.** Slot accessor L6 (SlotDistinction, ASN-0043). L3's asymmetric well-formedness (`e₃ ≠ ∅` required, others may be empty) constrains link construction, not resolution.

**Frame.** No state modification.

---

## F-origin — OriginSymmetry (LEMMA)

**Preconditions.** `v ∈ R(d, L(ℓ).eᵢ)`.

**Postcondition.** Membership of `v` in `R(d, L(ℓ).eᵢ)` is determined by:

```
M(d)(v) ∈ coverage(L(ℓ).eᵢ)
```

alone. The home of `M(d)(v)` — `origin(M(d)(v))` for content addresses (S7, ASN-0036), `home(M(d)(v))` for link addresses (Definition Home, ASN-0043) — does not appear in the membership condition.

**Depends.** Definition of `R(d, e)`.

**Frame.** No state modification.

---

## F-persist — LinkPersistence (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)` at state `Σ`; `Σ → Σ'` is a valid transition.

**Postcondition.**

```
ℓ ∈ dom(Σ'.L)
```

regardless of any reach condition on `coverage(L(ℓ).eᵢ)` versus `ran(M(d))`.

**Depends.** L12 (LinkImmutability, ASN-0043) — the link store is monotonic and value-preserving. L12a (LinkStoreMonotonicity, ASN-0043).

**Frame.** No state modification by `follow` itself; the persistence is a property of `Σ.L` across transitions, observed via `follow`.

---

## F-state — StateDependenceCorollary (COROLLARY)

**Preconditions.** `Σ → Σ'` reachable.

**Postcondition.**

```
R_Σ(d, L(ℓ).eᵢ)  and  R_{Σ'}(d, L(ℓ).eᵢ)  may differ
```

even though `L_Σ(ℓ) = L_{Σ'}(ℓ)` (by L12). The difference, when present, originates entirely in `M_Σ(d) ≠ M_{Σ'}(d)`.

**Depends.** L12 (link state-invariance); the transition semantics of ASN-0047 that admit `M(d)` to vary across transitions (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L).

**Frame.** No state modification.

---

## F-multidoc — NoPreferredDocument (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S
⟦Σ_V'^S⟧_V = R(d', L(ℓ).eᵢ)|_S
```

The home document `home(ℓ)` (Definition Home, ASN-0043) plays no privileged role; no precondition of `follow` references `home(ℓ)`.

**Frame.** No state modification.

---

## F-contig — Contiguity (LEMMA)

**Preconditions.** A mapping block `β = (v, a, n)` of `M(d)` (ASN-0058) and an endset I-span `σ = (s, ℓ_σ)` satisfying T12 (SpanWellDefinedness, ASN-0034).

**Postcondition.** `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression:

```
{a + j + k : 0 ≤ k < c}
```

of `I(β)`, for some offset `j` and width `c`. The corresponding V-positions `v + j, ..., v + j + c − 1` form a single contiguous V-run within `β`, recorded as the V-span `(v + j, δ(c, m_S))` where `m_S` is the V-depth of `v`.

**Depends.** M1 (OrderPreservation, ASN-0058) — strict monotonicity of `k ↦ a + k` for `0 ≤ k₁ < k₂ < n`: `a + k₁ < a + k₂`; T12 (SpanWellDefinedness, ASN-0034) — order-convexity of `⟦σ⟧` under T1 (postcondition (c)): for any `t₁, t₂ ∈ ⟦σ⟧` and `t₁ ≤ t' ≤ t₂`, we have `t' ∈ ⟦σ⟧`.

**Frame.** No state modification.
