# ASN-0077 Claim Statements

*Source: ASN-0077-showorigin-operation.md (revised 2026-05-25) — Extracted: 2026-05-25*

## Definition — OriginsI

`origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`

Where `⟦σ⟧ = { t ∈ T : s ≤ t < s ⊕ ℓ }` for span σ with start `s` and width `ℓ`.

---

## Definition — OriginsV

`origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` — form (F1), defined as the primary form; equal to (F2) and (F3) by the equivalence chain.

---

## Definition — OriginsVEquivalenceChain (DEF, function)

Three equivalent expressions for `origins_V(Σ, d, σ)`, given block decomposition `{β₁, ..., βₖ} = {(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}` from C1a (ASN-0058):

> *(F1)* `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.

> *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`.

> *(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`.

(F1) is the definition; (F2) and (F3) are derived equivalent forms.

---

## O0 — OriginExtendedToLinks (CLAIM, lemma)

Define `origin : dom(C) ∪ dom(L) → E_doc` by uniformly applying S7's structural projection:

> `origin(x) = N(x).0.U(x).0.D(x)` for all `x ∈ dom(C) ∪ dom(L)`.

This extension satisfies:

> (a) Structural well-definedness — for every `x ∈ dom(C) ∪ dom(L)`, T4b's projections `N(x), U(x), D(x)` are defined, and `origin(x)` is a document-level tumbler with `zeros(origin(x)) = 2`.
>
> (b) Semantic correspondence — for every `x ∈ dom(C) ∪ dom(L)`, `origin(x)` is the tumbler of the document that allocated `x`.
>
> (c) Totality and single-valuedness — `origin` is total on `dom(C) ∪ dom(L)` and single-valued.

---

## O1 — OriginPartitionsContent (CLAIM, lemma)

Define the relation `~_o` on `⟦σ⟧ ∩ dom(C)` by `a₁ ~_o a₂ ⟺ origin(a₁) = origin(a₂)`. Then:

> (a) `~_o` is an equivalence relation on `⟦σ⟧ ∩ dom(C)`;
> (b) the quotient map `[a]_{~_o} ↦ origin(a)` is a bijection from `(⟦σ⟧ ∩ dom(C)) / ~_o` to `origins_I(Σ, σ)`;
> (c) each equivalence class consists exactly of those I-addresses in `⟦σ⟧ ∩ dom(C)` allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one document tumbler; by SubAllocatorAxiom (a) and (e) (ASN-0047), the outputs of that document's unique content sub-allocator `A_C(d)`.

---

## O1.1 — SingleOriginSufficiency (CLAIM, lemma)

If every `a ∈ ⟦σ⟧ ∩ dom(C)` satisfies `origin(a) = d` for a fixed `d`, then `|origins_I(Σ, σ)| ≤ 1` — direct from the singleton image of the bijection in O1(b). The bound is `≤ 1` rather than `= 1` because `⟦σ⟧ ∩ dom(C)` may be empty.

---

## O1.2 — MultiOriginDiagnostic (CLAIM, lemma)

If `|origins_I(Σ, σ)| > 1`, then `σ` contains I-addresses allocated by at least two distinct documents — direct from the bijection in O1(b) combined with S7d.

---

## O2 — BlockUniformity (CLAIM, lemma)

For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `f = M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.

---

## O3 — StructuralDerivation (CLAIM, lemma)

`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.

---

## O4 — ParallelWitnesses (CLAIM, lemma)

Suppose `a ∈ dom(Σ.C)` with `origin(a) = d₁`, and suppose `d₂, d₃, ..., dₙ` are distinct documents each holding a V-position `vᵢ ∈ dom(M(dᵢ))` with `M(dᵢ)(vᵢ) = a` (for `2 ≤ i ≤ n`). Then for every `i ∈ {2, ..., n}`:

> `origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`.

The right-hand side does not depend on `i`. Each `dᵢ` for `i ≥ 2` is an independent witness to the same fact.

---

## O5 — OriginPermanence (CLAIM, lemma)

For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`: `origin'(a) = origin(a)`.

---

## O6 — MonotonicGrowthUnderState (CLAIM, lemma)

For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.

---

## O7 — VSpanStabilityFixedArrangement (CLAIM, lemma)

For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.

---

## O8 — ISpanContainmentMonotonicity (CLAIM, lemma)

For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.

---

## O9 — OriginTracksCreation (CLAIM, lemma)

Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by allocation events under distinct documents `d₁` and `d₂` (with `d₁ ≠ d₂`), then `origin(a₁) ≠ origin(a₂)`.

---

## O10 — ReadOnlyFrameIdempotence (CLAIM, lemma)

Let `op` be either SHOWORIGIN_I or SHOWORIGIN_V. Then for any Σ in which the precondition holds:

> (a) `op(Σ) = (Σ', result)` with `Σ' = Σ`;
> (b) two consecutive applications at the same state yield identical results.

---

## O11 — VSpanMonotonicGrowthKMuPlus (CLAIM, lemma)

For any reachable K.μ⁺ transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d`: `origins_V(Σ, d, σ) ⊆ origins_V(Σ', d, σ)`.

---

## O11' — VSpanMonotonicGrowthKMuPlusL (CLAIM, lemma)

For any reachable K.μ⁺_L transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d`: `origins_V(Σ, d, σ) ⊆ origins_V(Σ', d, σ)`.

---

## O12 — VSpanContainmentMonotonicity (CLAIM, lemma)

For V-spans `σ₁, σ₂` over the same document `d` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_V(Σ, d, σ₁) ⊆ origins_V(Σ, d, σ₂)`.

---

## wp(SHOWORIGIN_I, |result| = 1) — WpShoworiginISingleOrigin (WP, predicate)

`wp(SHOWORIGIN_I(σ), |result| = 1) = (⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`

---

## wp(SHOWORIGIN_V, d_q ∈ result) — WpShoworiginVDocPresent (WP, predicate)

`wp(SHOWORIGIN_V(d, σ), d_q ∈ result) = (E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`

---

## SHOWORIGIN (I-span) — ShoworiginI (OP, method)

- *Preconditions*: `σ = (s, ℓ)` is a well-formed I-span — explicitly, the conjuncts of T12 (SpanWellDefinedness, ASN-0034): (i) `s ∈ T`; (ii) `ℓ ∈ T`; (iii) `Pos(ℓ)` (TA-Pos, ASN-0034); (iv) `actionPoint(ℓ) ≤ #s` (ActionPoint, ASN-0034).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

---

## SHOWORIGIN (V-span) — ShoworiginV (OP, method)

- *Preconditions*: `(d, σ)` is a well-formed content reference — explicitly, the conjuncts from the ContentReference definition of ASN-0058: (i) `d ∈ Σ.E_doc`; (ii) `σ = (u, ℓ)` is a level-uniform V-span, i.e. `#u = #ℓ` (S6 of ASN-0053); (iii) `V_{u₁}(d) ≠ ∅`; (iv) T12 holds for `(u, ℓ)` — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`; (v) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth, ASN-0036); (vi) the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`. The subspace identifier `u₁` may be either `s_C` (content) or `s_L` (link).
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` (form (F1); equal to (F2) and (F3) by the equivalence chain derived above).
- *Frame*: `Σ' = Σ`.
