# ASN-0077 Claim Statements

*Source: ASN-0077-showorigin-operation.md (revised 2026-05-25) — Extracted: 2026-06-03*

## Definition — OriginsI

`origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`

Where σ is an I-span with start `s` and width `ℓ`, denoting the half-open interval `⟦σ⟧ = { t ∈ T : s ≤ t < s ⊕ ℓ }`.

---

## Definition — OriginsV

Three equivalent forms; (F1) is the definition:

> *(F1)* `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`

> *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`

> *(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`

Where `{β₁, ..., βₖ} = {(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}` is the unique maximally merged block decomposition of `f = M(d) ↾ ⟦σ⟧` via C1a (ASN-0058).

---

## O0 — OriginExtendedToLinkDomain (CLAIM, lemma)

*Define `origin : dom(C) ∪ dom(L) → E_doc` by uniformly applying S7's structural projection:*

> *`origin(x) = N(x).0.U(x).0.D(x)` for all `x ∈ dom(C) ∪ dom(L)`.*

*This extension satisfies:*

> *(a) Structural well-definedness — for every `x ∈ dom(C) ∪ dom(L)`, T4b's projections `N(x), U(x), D(x)` are defined, and `origin(x)` is a document-level tumbler with `zeros(origin(x)) = 2`.*
>
> *(b) Semantic correspondence — for every `x ∈ dom(C) ∪ dom(L)`, `origin(x)` is the tumbler of the document that allocated `x`.*
>
> *(c) Totality and single-valuedness — `origin` is total on `dom(C) ∪ dom(L)` and single-valued.*

---

## O1 — OriginPartitionsAllocatedContent (CLAIM, lemma)

*Define the relation `~_o` on `⟦σ⟧ ∩ dom(C)` by `a₁ ~_o a₂ ⟺ origin(a₁) = origin(a₂)`. Then:*

> *(a) `~_o` is an equivalence relation on `⟦σ⟧ ∩ dom(C)`;*
> *(b) the quotient map `[a]_{~_o} ↦ origin(a)` is a bijection from `(⟦σ⟧ ∩ dom(C)) / ~_o` to `origins_I(Σ, σ)`;*
> *(c) each equivalence class consists exactly of those I-addresses in `⟦σ⟧ ∩ dom(C)` allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one document tumbler; by the Allocator hierarchy definition and SubAllocatorBundle (ASN-0047), the outputs of that document's unique content sub-allocator `A_C(d)`.*

---

## O1.1 — SingleOriginSufficiency (COROLLARY, lemma)

*If every `a ∈ ⟦σ⟧ ∩ dom(C)` satisfies `origin(a) = d` for a fixed `d`, then `|origins_I(Σ, σ)| ≤ 1`* — direct from the singleton image of the bijection in O1(b). The bound is `≤ 1` rather than `= 1` because `⟦σ⟧ ∩ dom(C)` may be empty.

---

## O1.2 — MultiOriginDiagnostic (COROLLARY, lemma)

*If `|origins_I(Σ, σ)| > 1`, then `σ` contains I-addresses allocated by at least two distinct documents* — direct from the bijection in O1(b) combined with S7d.

---

## O2 — BlockUniformity (CLAIM, lemma)

*For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `f = M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.*

---

## O3 — StructuralDerivation (CLAIM, lemma)

*`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.*

---

## O4 — ParallelWitnesses (CLAIM, lemma)

*Suppose `a ∈ dom(Σ.C)` with `origin(a) = d₁`, and suppose `d₂, d₃, ..., dₙ` are distinct documents each holding a V-position `vᵢ ∈ dom(M(dᵢ))` with `M(dᵢ)(vᵢ) = a` (for `2 ≤ i ≤ n`). Then for every `i ∈ {2, ..., n}`:*

> *`origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`.*

*The right-hand side does not depend on `i`. Each `dᵢ` for `i ≥ 2` is an independent witness to the same fact.*

---

## O5 — OriginPermanence (CLAIM, lemma)

*For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`: `origin'(a) = origin(a)`.*

---

## O5★ — OriginPermanenceMultiStep (CLAIM, lemma)

*For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable state sequence `Σ →* Σ'`: `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)` and `origin'(a) = origin(a)`.*

---

## O6 — MonotonicGrowthUnderState (CLAIM, lemma)

*For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

---

## O6★ — MonotonicGrowthMultiStep (CLAIM, lemma)

*For any reachable state sequence `Σ →* Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

---

## O7 — VSpanStabilityFixedArrangement (CLAIM, lemma)

*For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.*

---

## O8 — ISpanContainmentMonotonicity (CLAIM, lemma)

*For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.*

---

## O9 — OriginTracksCreationNotContent (CLAIM, lemma)

*Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by allocation events under distinct documents `d₁` and `d₂` (with `d₁ ≠ d₂`), then `origin(a₁) ≠ origin(a₂)`.*

---

## O10 — ReadOnlyFrameIdempotence (CLAIM, lemma)

*Let `op` be either SHOWORIGIN_I or SHOWORIGIN_V. Then for any Σ in which the precondition holds:*

> *(a) `op(Σ) = (Σ', result)` with `Σ' = Σ`;*
> *(b) two consecutive applications at the same state yield identical results.*

---

## O11 — VSpanPreservationKMuPlus (CLAIM, lemma)

*For any reachable K.μ⁺ transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ — in particular precondition (vi), `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

---

## O11' — VSpanPreservationKMuPlusL (CLAIM, lemma)

*For any reachable K.μ⁺_L transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

---

## O11.1 — WellFormednessPreservationArrangementExtension (COROLLARY, lemma)

*Let σ be a V-span over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ. For any reachable arrangement-extension transition `Σ → Σ'` — K.μ⁺ on `d` or K.μ⁺_L on `d` — σ also satisfies the SHOWORIGIN_V well-formedness preconditions at Σ'.*

---

## O11★ — VSpanPreservationKMuPlusChain (CLAIM, lemma)

*For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is K.μ⁺ on `d` (i.e., no K.μ⁻ on `d`, no K.μ~ on `d`, no K.μ⁺_L on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

---

## O11'★ — VSpanPreservationKMuPlusLChain (CLAIM, lemma)

*For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is K.μ⁺_L on `d` (i.e., no K.μ⁻ on `d`, no K.μ~ on `d`, no K.μ⁺ on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

---

## O11★★ — VSpanPreservationMixedChain (CLAIM, lemma)

*For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is either K.μ⁺ on `d` or K.μ⁺_L on `d` (i.e., no K.μ⁻ on `d` and no K.μ~ on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

---

## O12 — VSpanContainmentMonotonicity (CLAIM, lemma)

*For V-spans `σ₁, σ₂` over the same document `d` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_V(Σ, d, σ₁) ⊆ origins_V(Σ, d, σ₂)`.*

---

## O13 — KMuMinusAdmissibilityLoss (CLAIM, lemma)

*There exist Σ, a V-span σ over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ, and a reachable K.μ⁻ transition `Σ → Σ'` on `d` such that σ fails precondition (vi) at Σ' — equivalently, `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊄ dom(M'(d))`. Consequently, no K.μ⁻ analogue of O11 / O11' / O11★★ holds — the V-span operation is no longer admissible at the post-state on the original input, so preservation of `origins_V` is not even formulable.*

Failure condition: Precondition (vi) — `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` — ceases to hold whenever the K.μ⁻ retention parameters drop V-positions strictly inside `⟦σ⟧` from `dom(M(d))`. By K.μ⁻'s constructive retention `R = ⋃_{S ∈ {s_C, s_L}} {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`, this happens precisely when some position in `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` carries a sequential index `k` greater than `n'_S` in its subspace `S`.

---

## O14 — KMuTildeNonPreservation (CLAIM, lemma)

*There exist Σ, a reachable K.μ~ transition `Σ → Σ'` on `d`, and a V-span `σ` over `d` such that σ is well-formed at both Σ and Σ', yet:*

> *(i) `origins_V(Σ, d, σ) ⊄ origins_V(Σ', d, σ)`, and*
> *(ii) `origins_V(Σ', d, σ) ⊄ origins_V(Σ, d, σ)`.*

*That is, neither set is a subset of the other; no monotonicity claim parallel to O11 / O11' / O11★★ holds for K.μ~.*

---

## F1 ≡ F2 ≡ F3 — OriginsVEquivalenceChain (LEMMA, lemma)

The three forms of `origins_V` are equal. (F1) is the definition; (F2) and (F3) are derived equivalent forms.

> *(F1)* `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`
>
> *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`
>
> *(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`

Where `{(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}` is the C1a block decomposition of `f = M(d) ↾ ⟦σ⟧`.

Equivalence:
- *(F2) = (F3):* O2 (Block uniformity) collapses `{ origin(aⱼ + i) : 0 ≤ i < nⱼ }` to `{ origin(aⱼ) }` for each `j`.
- *(F1) ⊆ (F3):* Fix `v ∈ ⟦σ⟧ ∩ dom(M(d))`; B1 gives unique `j` with `v = vⱼ + i`; by O2, `origin(M(d)(v)) = origin(aⱼ) ∈` (F3).
- *(F3) ⊆ (F1):* Fix `j`; since `nⱼ ≥ 1`, `vⱼ ∈ dom(f)` and B3 gives `M(d)(vⱼ) = aⱼ`, so `origin(aⱼ) ∈` (F1).

---

## wp(SHOWORIGIN_I, |result| = 1) — WpShoworiginISingleOrigin (PREDICATE, predicate)

`wp(SHOWORIGIN_I(σ), |result| = 1) = (⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`

---

## wp(SHOWORIGIN_V, d_q ∈ result) — WpShoworiginVDocumentPresent (PREDICATE, predicate)

`wp(SHOWORIGIN_V(d, σ), d_q ∈ result) = (E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`

---

## SHOWORIGIN (I-span) — ShoworiginISpan (SPEC, method)

- *Preconditions*: `σ = (s, ℓ)` is a well-formed I-span — explicitly, the conjuncts of T12 (SpanWellDefinedness, ASN-0034): (i) `s ∈ T`; (ii) `ℓ ∈ T`; (iii) `Pos(ℓ)` (TA-Pos, ASN-0034); (iv) `actionPoint(ℓ) ≤ #s` (ActionPoint, ASN-0034).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

---

## SHOWORIGIN (V-span) — ShoworiginVSpan (SPEC, method)

- *Preconditions*: `(d, σ)` is a well-formed content reference — explicitly: (i) `d ∈ Σ.E_doc`; (ii) `σ = (u, ℓ)` is a level-uniform V-span, i.e. `#u = #ℓ` (S6 of ASN-0053); (iii) `V_{u₁}(d) ≠ ∅`; (iv) T12 holds for `(u, ℓ)` — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`; (v) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth, ASN-0036); (vi) the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`. The subspace identifier `u₁` may be either `s_C` (content) or `s_L` (link).
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` (form (F1); equal to (F2) and (F3) by the equivalence chain).
- *Frame*: `Σ' = Σ`.
