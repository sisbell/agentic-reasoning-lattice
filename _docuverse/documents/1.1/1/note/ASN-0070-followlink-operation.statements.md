# ASN-0070 Claim Statements

*Source: ASN-0070-followlink-operation.md (revised 2026-05-25) — Extracted: 2026-06-02*

## Definition — EndsetCoverage

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```

where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). The coverage is a subset of `T`, fixed at link creation and immutable thereafter.

---

## Definition — SubspaceProjection

For `R(d, e)`, the per-subspace restriction:

```
R(d, e)|_S := {v ∈ R(d, e) : subspace(v) = S}    for S ∈ {s_C, s_L}
```

---

## Definition — VRestrictedDenotation

When `m_S(d)` is defined (subspace `S` non-empty), for a span-set `Σ_V^S` whose components are level-uniform at V-position depth `m_S(d)` in subspace `S`:

```
⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }
```

When `m_S(d)` is undefined (`V_S(d) = ∅`), `⟦⟨⟩⟧_V := ∅`.

For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`:

```
⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V
```

---

## Definition — ConsecutiveTumblers

For depth-`m_S(d)` subspace-`S` tumblers `t < t'`, `t` and `t'` are *consecutive* iff no depth-`m_S(d)` subspace-`S` tumbler `t''` satisfies `t < t'' < t'` under T1.

Characterisation: consecutivity holds iff `t_i = t'_i` for `1 ≤ i < m_S(d)` and `t'_m = t_m + 1`.

---

## Definition — MaximalRun

A *maximal run* in a set `X` of depth-`m_S(d)` subspace-`S` tumblers is a maximal subset of `X` whose elements can be ordered `t_0 < t_1 < ... < t_{c-1}` with each `t_i` consecutive to `t_{i+1}`. Every element of `X` lies in exactly one maximal run (the consecutivity relation decomposes `X` into disjoint chains).

---

## F0 — InverseImageRelation (DEF)

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

## F1 — FollowOperation (DEF)

**Signature.** `follow : (ℓ, d, i) → (d, Σ_V)` where `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is a per-subspace family of finite V-span-sets.

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, (Σ_V^{s_C}, Σ_V^{s_L}))` where each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)` when `V_S(d) ≠ ∅`; when `V_S(d) = ∅` (so `m_S(d)` is undefined), `Σ_V^S = ⟨⟩` by the V-restricted denotation convention. In either case:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S    for each S ∈ {s_C, s_L}
```

**Frame.** `Σ' = Σ`. No component of state is modified.

---

## F-subspace — IOSubspaceCorrespondence (LEMMA)

**Preconditions.** `v ∈ dom(M(d))`.

**Postcondition.** `subspace(v) = subspace_I(M(d)(v))`. In particular:
- `subspace(v) = s_C ⟹ subspace_I(M(d)(v)) = s_C`
- `subspace(v) = s_L ⟹ subspace_I(M(d)(v)) = s_L`

**Consequence.**

```
R(d, e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))
R(d, e)|_{s_L} = M(d)⁻¹(coverage(e) ∩ dom(L))
```

The biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` holds for `v ∈ dom(M(d))`:
- Forward (`subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)`): direct from S3★ (GeneralizedReferentialIntegrity, ASN-0047).
- Reverse (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`): by S3★-aux + L14 (StoreDisjointness, ASN-0047): `dom(C) ∩ dom(L) = ∅`.

**Frame.** State-pure.

---

## F-canon-form — CanonicalForm (DEF)

The canonical form of `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})` is the per-subspace family in which:

(i) Each component span in each `Σ_V^S` has start `s` with `#s = m_S(d)`, `subspace(s) = S`, and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (so `s` is an admissible V-position by S8a), and width of the form `δ(c, m_S(d)) = [0, ..., 0, c]` — an *ordinal displacement* of depth `m_S(d)`.

(ii) Each component `Σ_V^S` is in the unique normalised form guaranteed by S9 (NormalizationUniqueness, ASN-0053) — sorted by V-start under T1, with no overlapping or adjacent spans.

(iii) The two components are presented in a fixed external order: `s_C`-component first, `s_L`-component second.

When `m_S(d)` is undefined (either subspace `S ∈ {s_C, s_L}` with `V_S(d) = ∅`), the canonical form is `Σ_V^S = ⟨⟩`.

---

## F-canonical — CanonicalUniqueness (THM)

**Statement.** Given `R(d, e)`, there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form.

**Step 1 — Level-uniformity and ordinal-displacement widths.** Component widths are restricted to ordinal displacements `δ(c, m_S(d))`. The restriction is forced by finiteness and subspace-confinement of `⟦σ⟧_V` for each component `σ = (s, ℓ)` with `#s = #ℓ = m_S(d)`, `subspace(s) = S`, and `s` positive, by case analysis on `k = actionPoint(ℓ)`:

- Case `1 ≤ k < m_S(d)`: `⟦σ⟧_V` is infinite (unbounded last component), excluded by finiteness.
- Case `k = m_S(d)`: `ℓ = δ(ℓ_m, m_S(d))`, and `⟦σ⟧_V = {[s_1, ..., s_{m-1}, s_m + j] : 0 ≤ j < ℓ_m}` — finite, cardinality `ℓ_m`.

**Step 2 — Uniqueness via V-restricted ↔ full bridge.** For a component span `σ = (s, δ(c, m_S(d)))` with positive-component start, `s = min(⟦σ⟧_V)` (by T12(b)) and `|⟦σ⟧_V| = c`, so `(s, c)` is recoverable from `⟦σ⟧_V`. Hence same `⟦·⟧_V` implies same `⟦·⟧`, and S9 (NormalizationUniqueness, ASN-0053) lifts to V-restricted equivalence. The normalised span-set per subspace is unique.

**Step 2a — Existence.** Partition `R(d, e)|_S` into maximal runs of consecutive tumblers. Each run `{[w_1, ..., w_{m-1}, b + i] : 0 ≤ i < c}` maps to span `σ := (t_0, δ(c, m))` with `t_0 = min(run)`. The resulting `Σ_0` is normalised (N1 by construction; N2 by maximality of runs and run-disjointness). Hence a canonical form exists.

**Step 3 — Family-level ordering.** The fixed external convention (`s_C`-component first, then `s_L`-component) removes remaining ambiguity at the family level.

**Conclusion.** Given `R(d, e)`, the canonical form is uniquely determined.

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

**Depends.** The postcondition of `follow` (F1); the definition of `R(d, e)` (F0).

**Frame.** No state modification.

---

## F-complete — Completeness (LEMMA)

**Preconditions.** As `follow`.

**Postcondition.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies:

```
v ∈ ⟦Σ_V^S⟧_V    for S = subspace(v)
```

**Depends.** The postcondition of `follow` (F1); the definition of `R(d, e)` (F0).

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

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1). For the representational conclusion under canonical form: F-canonical and S9 (NormalizationUniqueness, ASN-0053).

**Frame.** No state modification.

---

## F-multi — MultiplicityPreservation (LEMMA)

**Preconditions.** As `follow`; additionally `v₁, v₂ ∈ dom(M(d))` with `v₁ ≠ v₂` and `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`.

**Postcondition.** By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)` and `subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a)`, so:

```
subspace(v₁) = subspace(v₂) = subspace_I(a) =: S
```

Writing `S := subspace_I(a)`:

```
v₁ ∈ ⟦Σ_V^S⟧_V  ∧  v₂ ∈ ⟦Σ_V^S⟧_V
```

**Depends.** Definition of `R(d, e)` (F0); postcondition of `follow` (F1); F-subspace; S3★-aux (SubspaceExhaustiveness, ASN-0047); K.μ⁺ (ArrangementExtension, ASN-0047) — content-side non-injectivity underwrites reachability of the hypothesis; S5 (UnrestrictedSharing, ASN-0036) — abstract-cardinality point only.

**Frame.** No state modification.

---

## F-frame — Frame (INV)

**Preconditions.** As `follow`.

**Postcondition.**

```
Σ' = Σ
```

Specifically: `C' = C`, `M' = M`, `L' = L`, `E' = E`, `R' = R`.

**Depends.** Definition of `follow` as a query (no effect clause).

---

## F-slot — SlotUniformity (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d ∈ E_doc`; `i, i' ∈ {1, ..., |L(ℓ)|}`.

**Postcondition.** For any two slot indices `i, i'`, `follow(ℓ, d, i)` and `follow(ℓ, d, i')` are computed by the same definition:

```
⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S
⟦Σ_V'^S⟧_V = R(d, L(ℓ).eᵢ')|_S
```

The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing.

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

**Frame.** No state modification by `follow` itself; the persistence is a property of `Σ.L` across transitions.

---

## F-state — StateDependenceCorollary (COROLLARY)

**Preconditions.** `Σ → Σ'` reachable.

**Postcondition.** `R_Σ(d, L(ℓ).eᵢ)` and `R_{Σ'}(d, L(ℓ).eᵢ)` may differ even though:

```
L_Σ(ℓ) = L_{Σ'}(ℓ)    (by L12)
```

The difference, when present, originates entirely in:

```
M_Σ(d) ≠ M_{Σ'}(d)
```

**Depends.** L12 (link state-invariance); the transition semantics of ASN-0047 that admit `M(d)` to vary across transitions.

**Frame.** No state modification.

---

## F-multidoc — NoPreferredDocument (LEMMA)

**Preconditions.** `ℓ ∈ dom(Σ.L)`; `d, d' ∈ E_doc`; `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i)` and `follow(ℓ, d', i)` are well-defined and computed by the same mechanism. The home document `home(ℓ)` (Definition Home, ASN-0043) plays no privileged role. No precondition of `follow` references `home(ℓ)`.

**Frame.** No state modification.

---

## F-contig — Contiguity (LEMMA)

**Preconditions.** A mapping block `β = (v, a, n)` of `M(d)` (ASN-0058) and an endset I-span `σ = (s, ℓ_σ)` satisfying T12 (SpanWellDefinedness, ASN-0034).

**Postcondition.** `I(β) ∩ ⟦σ⟧` is either empty or a contiguous sub-progression:

```
{a + j + k : 0 ≤ k < c}
```

of `I(β)`, for some offset `j` and width `c`; the corresponding V-positions `v + j, ..., v + j + c − 1` form a single contiguous V-run within `β`.

**Depends.** M1 (OrderPreservation, ASN-0058) — strict monotonicity of the I-extent map `k ↦ a + k`; T12 (SpanWellDefinedness, ASN-0034) — order-convexity of `⟦σ⟧` under T1 (postcondition (c)).

**Frame.** No state modification.
