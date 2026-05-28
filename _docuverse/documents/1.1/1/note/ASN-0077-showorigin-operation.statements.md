# ASN-0077 Claim Statements

*Source: ASN-0077-showorigin-operation.md (revised 2026-05-25) — Extracted: 2026-05-28*

## Definition — OriginsI

`origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }` — I-span lift of origin

## Definition — OriginsV (F1)

`origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` — V-span lift via arrangement

## Definition — OriginsVF2

*(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`

## Definition — OriginsVF3

*(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`

## O0 — OriginExtendedToLinks (CLAIM, lemma)

**Claim O0 (Origin extended to dom(L)).** *Define `origin : dom(C) ∪ dom(L) → E_doc` by uniformly applying S7's structural projection:*

> *`origin(x) = N(x).0.U(x).0.D(x)` for all `x ∈ dom(C) ∪ dom(L)`.*

*This extension satisfies:*

> *(a) Structural well-definedness — for every `x ∈ dom(C) ∪ dom(L)`, T4b's projections `N(x), U(x), D(x)` are defined, and `origin(x)` is a document-level tumbler with `zeros(origin(x)) = 2`.*
>
> *(b) Semantic correspondence — for every `x ∈ dom(C) ∪ dom(L)`, `origin(x)` is the tumbler of the document that allocated `x`.*
>
> *(c) Totality and single-valuedness — `origin` is total on `dom(C) ∪ dom(L)` and single-valued.*

## O1 — OriginPartitionsContent (CLAIM, lemma)

**Claim O1 (Origin partitions allocated content).** *Define the relation `~_o` on `⟦σ⟧ ∩ dom(C)` by `a₁ ~_o a₂ ⟺ origin(a₁) = origin(a₂)`. Then:*

> *(a) `~_o` is an equivalence relation on `⟦σ⟧ ∩ dom(C)`;*
> *(b) the quotient map `[a]_{~_o} ↦ origin(a)` is a bijection from `(⟦σ⟧ ∩ dom(C)) / ~_o` to `origins_I(Σ, σ)`;*
> *(c) each equivalence class consists exactly of those I-addresses in `⟦σ⟧ ∩ dom(C)` allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one document tumbler; by SubAllocatorAxiom (a) and (e) (ASN-0047), the outputs of that document's unique content sub-allocator `A_C(d)`.*

## O1.1 — SingleOriginSufficiency (COROLLARY, lemma)

**Corollary O1.1 (Single-origin sufficiency).** *If every `a ∈ ⟦σ⟧ ∩ dom(C)` satisfies `origin(a) = d` for a fixed `d`, then `|origins_I(Σ, σ)| ≤ 1`* — direct from the singleton image of the bijection in O1(b). The bound is `≤ 1` rather than `= 1` because `⟦σ⟧ ∩ dom(C)` may be empty.

## O1.2 — MultiOriginDiagnostic (COROLLARY, lemma)

**Corollary O1.2 (Multi-origin diagnostic).** *If `|origins_I(Σ, σ)| > 1`, then `σ` contains I-addresses allocated by at least two distinct documents* — direct from the bijection in O1(b) combined with S7d.

## O2 — BlockUniformity (CLAIM, lemma)

**Claim O2 (Block uniformity).** *For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `f = M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.*

## O3 — StructuralDerivation (CLAIM, lemma)

**Claim O3 (Structural derivation).** *`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.*

## O4 — ParallelWitnesses (CLAIM, lemma)

**Claim O4 (Parallel witnesses to a single origin).** *Suppose `a ∈ dom(Σ.C)` with `origin(a) = d₁`, and suppose `d₂, d₃, ..., dₙ` are distinct documents each holding a V-position `vᵢ ∈ dom(M(dᵢ))` with `M(dᵢ)(vᵢ) = a` (for `2 ≤ i ≤ n`). Then for every `i ∈ {2, ..., n}`:*

> *`origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`.*

*The right-hand side does not depend on `i`. Each `dᵢ` for `i ≥ 2` is an independent witness to the same fact.*

## O5 — OriginPermanence (CLAIM, lemma)

**Claim O5 (Origin permanence).** *For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`: `origin'(a) = origin(a)`.*

## O5★ — OriginPermanenceMultiStep (CLAIM, lemma)

**Claim O5★ (Multi-step origin permanence).** *For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable state sequence `Σ →* Σ'`: `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)` and `origin'(a) = origin(a)`.*

## O6 — MonotonicGrowthUnderState (CLAIM, lemma)

**Claim O6 (Monotonic growth under state).** *For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

## O6★ — MonotonicGrowthMultiStep (CLAIM, lemma)

**Claim O6★ (Multi-step monotonic growth).** *For any reachable state sequence `Σ →* Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

## O7 — VSpanStabilityUnderFixedArrangement (CLAIM, lemma)

**Claim O7 (V-span stability under fixed arrangement).** *For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.*

## O8 — ISpanContainmentMonotonicity (CLAIM, lemma)

**Claim O8 (I-span containment monotonicity).** *For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.*

## O9 — OriginTracksCreation (CLAIM, lemma)

**Claim O9 (Origin tracks creation, not content).** *Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by allocation events under distinct documents `d₁` and `d₂` (with `d₁ ≠ d₂`), then `origin(a₁) ≠ origin(a₂)`.*

## O10 — ReadOnlyFrameIdempotence (CLAIM, lemma)

**Claim O10 (Read-only frame; idempotence).** *Let `op` be either SHOWORIGIN_I or SHOWORIGIN_V. Then for any Σ in which the precondition holds: (a) `op(Σ) = (Σ', result)` with `Σ' = Σ`; (b) two consecutive applications at the same state yield identical results.*

## O11 — VSpanPreservationUnderKMuPlus (CLAIM, lemma)

**Claim O11 (V-span preservation under K.μ⁺).** *For any reachable K.μ⁺ transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ — in particular precondition (vi), `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

## O11' — VSpanPreservationUnderKMuPlusL (CLAIM, lemma)

**Claim O11' (V-span preservation under K.μ⁺_L).** *For any reachable K.μ⁺_L transition `Σ → Σ'` extending `M(d)` and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

## O11.1 — WellFormednessPreservationUnderArrangementExtension (COROLLARY, lemma)

**Corollary O11.1 (Well-formedness preservation under arrangement extension).** *Let σ be a V-span over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ. For any reachable arrangement-extension transition `Σ → Σ'` — K.μ⁺ on `d` or K.μ⁺_L on `d` — σ also satisfies the SHOWORIGIN_V well-formedness preconditions at Σ'.*

## O11★ — VSpanPreservationUnderKMuPlusChain (CLAIM, lemma)

**Claim O11★ (Multi-step V-span preservation under K.μ⁺ chain).** *For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is K.μ⁺ on `d` (i.e., no K.μ⁻ on `d`, no K.μ~ on `d`, no K.μ⁺_L on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

## O11'★ — VSpanPreservationUnderKMuPlusLChain (CLAIM, lemma)

**Claim O11'★ (Multi-step V-span preservation under K.μ⁺_L chain).** *For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is K.μ⁺_L on `d` (i.e., no K.μ⁻ on `d`, no K.μ~ on `d`, no K.μ⁺ on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

## O11★★ — VSpanPreservationUnderMixedChain (CLAIM, lemma)

**Claim O11★★ (Multi-step V-span preservation under mixed K.μ⁺/K.μ⁺_L chain).** *For any reachable state sequence `Σ →* Σ'` in which every `M(d)`-modifying step is either K.μ⁺ on `d` or K.μ⁺_L on `d` (i.e., no K.μ⁻ on `d` and no K.μ~ on `d` along the chain), and any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ: `origins_V(Σ, d, σ) = origins_V(Σ', d, σ)`.*

## O12 — VSpanContainmentMonotonicity (CLAIM, lemma)

**Claim O12 (V-span containment monotonicity).** *For V-spans `σ₁, σ₂` over the same document `d` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_V(Σ, d, σ₁) ⊆ origins_V(Σ, d, σ₂)`.*

## O13 — KMuMinusAdmissibilityLoss (CLAIM, lemma)

**Claim O13 (K.μ⁻ admissibility loss).** *There exist Σ, a V-span σ over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ, and a reachable K.μ⁻ transition `Σ → Σ'` on `d` such that σ fails precondition (vi) at Σ' — equivalently, `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊄ dom(M'(d))`. Consequently, no K.μ⁻ analogue of O11 / O11' / O11★★ holds — the V-span operation is no longer admissible at the post-state on the original input, so preservation of `origins_V` is not even formulable.*

*Failure condition.* Precondition (vi) — `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` — ceases to hold whenever the K.μ⁻ retention parameters drop V-positions strictly inside `⟦σ⟧` from `dom(M(d))`. By K.μ⁻'s constructive retention `R = ⋃_{S ∈ {s_C, s_L}} {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}`, this happens precisely when some position in `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))` carries a sequential index `k` greater than `n'_S` in its subspace `S`. K.μ⁻'s strict-contraction precondition `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` guarantees at least one subspace shrinks strictly, and any contraction whose strict shrinkage falls inside `⟦σ⟧` witnesses admissibility loss.

## O14 — KMuTildeNonPreservation (CLAIM, lemma)

**Claim O14 (K.μ~ non-preservation).** *There exist Σ, a reachable K.μ~ transition `Σ → Σ'` on `d`, and a V-span `σ` over `d` such that σ is well-formed at both Σ and Σ', yet:*

> *(i) `origins_V(Σ, d, σ) ⊄ origins_V(Σ', d, σ)`, and*
> *(ii) `origins_V(Σ', d, σ) ⊄ origins_V(Σ, d, σ)`.*

*That is, neither set is a subset of the other; no monotonicity claim parallel to O11 / O11' / O11★★ holds for K.μ~.*

## F1≡F2≡F3 — OriginsVEquivalenceChain (CLAIM, lemma)

Equivalence chain for `origins_V`: reader-form `{origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d))}` ≡ decomposition-form `⋃_j {origin(aⱼ + i) : 0 ≤ i < nⱼ}` ≡ block-collapsed-form `{origin(aⱼ) : 1 ≤ j ≤ k}`

*(F1) = (F3):* Inside the inner set for each `j`, O2 (Block uniformity) collapses `{ origin(aⱼ + i) : 0 ≤ i < nⱼ }` to `{ origin(aⱼ) }`. Taking the union over `j` yields `{ origin(aⱼ) : 1 ≤ j ≤ k }`.

*(F1) ⊆ (F3):* Fix `v ∈ ⟦σ⟧ ∩ dom(M(d))`. B1 gives a unique `j` with `v ∈ V(βⱼ)`, so `v = vⱼ + i` for some `0 ≤ i < nⱼ`. By B3, `M(d)(v) = aⱼ + i`. By O2, `origin(M(d)(v)) = origin(aⱼ + i) = origin(aⱼ)`, an element of (F3).

*(F3) ⊆ (F1):* Fix `j ∈ {1, ..., k}`. Since `nⱼ ≥ 1`: `vⱼ ∈ V(βⱼ) ⊆ dom(f) ⊆ dom(M(d))`, and `vⱼ ∈ ⟦σ⟧`. B3 gives `M(d)(vⱼ) = aⱼ`, so `origin(aⱼ) = origin(M(d)(vⱼ))`, an element of (F1).

## wp(SHOWORIGIN_I, |result|=1) — WpShoworiginISingleOrigin (WP, predicate)

> `wp(SHOWORIGIN_I(σ), |result| = 1) = (⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`.

## wp(SHOWORIGIN_V, d_q ∈ result) — WpShoworiginVDocPresent (WP, predicate)

> `wp(SHOWORIGIN_V(d, σ), d_q ∈ result) = (E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`.

## SHOWORIGIN (I-span) — ShoworiginISpan (OPERATION)

**SHOWORIGIN over an I-span.**
- *Preconditions*: `σ = (s, ℓ)` is a well-formed I-span — explicitly, the conjuncts of T12 (SpanWellDefinedness, ASN-0034): (i) `s ∈ T`; (ii) `ℓ ∈ T`; (iii) `Pos(ℓ)` (TA-Pos, ASN-0034); (iv) `actionPoint(ℓ) ≤ #s` (ActionPoint, ASN-0034).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

## SHOWORIGIN (V-span) — ShoworiginVSpan (OPERATION)

**SHOWORIGIN over a content reference.**
- *Preconditions*: `(d, σ)` is a well-formed content reference — explicitly, the conjuncts from the ContentReference definition of ASN-0058: (i) `d ∈ Σ.E_doc`; (ii) `σ = (u, ℓ)` is a level-uniform V-span, i.e. `#u = #ℓ` (S6 of ASN-0053); (iii) `V_{u₁}(d) ≠ ∅`; (iv) T12 holds for `(u, ℓ)` — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`; (v) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth, ASN-0036); (vi) the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`. The subspace identifier `u₁` may be either `s_C` (content) or `s_L` (link); `origin` is total on `dom(C) ∪ dom(L)`, so the postcondition is well-formed in either case (with the link case trivializing to `{d}` by CL-OWN).
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` (form (F1); equal to (F2) and (F3) by the equivalence chain derived above).
- *Frame*: `Σ' = Σ`.
