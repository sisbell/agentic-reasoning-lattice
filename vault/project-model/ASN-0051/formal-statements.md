# ASN-0051 Formal Statements

*Source: ASN-0051-link-survivability.md (revised 2026-03-23) — Extracted: 2026-03-23*

## Definition — EndsetProjection

For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

## Definition — EndsetLocation

For an endset e and document d, the *location* of e in d is:

`locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

Relation to projection: v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d). Since M(d) need not be injective (S5, UnrestrictedSharing), |locate(e, d)| ≥ |π(e, d)|.

## Definition — EndsetVitality

An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, locate(e, d) ≠ ∅.

## Definition — BilateralVitality

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(Type endset Θ is excluded from the vitality condition per L9, TypeGhostPermission.)

## Definition — LinkDiscovery

For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

## Definition — EndsetFragment

For an endset e and document d, let B = {β₁, ..., β_p} be the maximally merged block decomposition of the restriction M(d)|_{V_{s_C}(d)}. A *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence:

F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π_text(e, d) ∩ I(β_k)

for some block β_k = (v_k, a_k, n_k), where F is maximal: either j₁ = 0 or a_k + (j₁ - 1) ∉ π_text(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π_text(e, d).

---

## SV0 — ResolutionCurrentness (LEMMA, lemma)

For any endset e and document d:

`locate(e, d) is determined entirely by coverage(e) and the current M(d)`

There is no mechanism by which stale arrangement information could participate, because the link stores only I-addresses (via its endset spans), and V-addresses are derived from them through the current arrangement.

## SV1 — ArrangementLinkFrame (INV, lemma)

For every state transition Σ → Σ':

`(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

(= L12, ASN-0043)

*Consequence for coverage:*
`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

*Consequence for directionality:* the from/to/type slot assignment is permanent; no operation can swap, reassign, or modify the endset ordering.

## SV2 — ExtensionMonotonicity (LEMMA, lemma)

`(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d))`

*For resolution:* `locate_Σ(e, d) ⊆ locate_{Σ'}(e, d)`.

Let v ∈ locate_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Both K.μ⁺ and K.μ⁺_L preserve existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))). So v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ locate_{Σ'}(e, d).

## SV3 — ContractionReduction (LEMMA, lemma)

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d))`

*For resolution:* `locate_{Σ'}(e, d) ⊆ locate_Σ(e, d)`.

The vitality loss condition is:
`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))`.

## SV4 — ArrangementIsolation (LEMMA, lemma)

`(A Σ →_{K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

*For resolution:* `locate_{Σ'}(e, d') = locate_Σ(e, d')`.

From the frame conditions of K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`.

## SV5 — ReorderingProjectionInvariance (LEMMA, lemma)

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). The formal relationship for resolution is:

`locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`

In general, `locate_{Σ'}(e, d) ≠ locate_Σ(e, d)` as sets.

## SV6 — CrossOriginExclusion (LEMMA, lemma)

*Precondition:* s and b are element-level tumblers (zeros(s) = 3, zeros(b) = 3), so origin(s) and origin(b) are well-defined. The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently, the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`.

For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

## SV7 — TransclusionCouplingAbsence (LEMMA, lemma)

For any transition Σ → Σ' that holds L in frame and any set of I-addresses A:

`discover_s(A) in Σ' = discover_s(A) in Σ`

K.μ⁺ and K.μ⁺_L both hold L in their frame: dom(L') = dom(L) and L'(a) = L(a) for all a ∈ dom(L). The same equality holds for every elementary transition that holds L in frame — K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ. The only transition where the inclusion of SV9 can be strict is K.λ.

## SV8 — DiscoveryPermanence (LEMMA, lemma)

For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

## SV9 — DiscoveryMonotonicity (LEMMA, lemma)

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

for any fixed A. New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow.

## SV10 — DiscoveryResolutionIndependence (LEMMA, lemma)

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

Note that discovery through d entails non-empty projection in d: if a ∈ discover_s({M(d)(v) : v ∈ V}), then coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅, and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)), we have π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅.

## SV11 — PartialSurvivalDecomposition (LEMMA, lemma)

Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be the maximally merged block decomposition of the restriction M(d)|_{V_{s_C}(d)}. Define the *text-subspace projection*:

`π_text(e, d) = coverage(e) ∩ ran_text(M(d))`

where `ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C} = ⋃_k I(β_k)`. Then:

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

Each term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is contiguous within the ordinal sequence of I(β_k). The fragment collection is a *cover* of π_text(e, d), not necessarily a partition (due to non-injective arrangements). The number of fragment objects is bounded by m · p.

## SV12 — ContentFidelity (INV, lemma)

For every a ∈ dom(Σ.C) and every state transition Σ → Σ', `a ∈ dom(Σ'.C) and Σ'.C(a) = Σ.C(a)` (= S0, ASN-0036).

Applied to endset I-addresses: for any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k:

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))`

for every endset slot s.

## SV13 — SurvivabilityTheorem (THM, lemma)

For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

(a) *The link persists:* `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, Θ)` [L12]

(b) *Endset coverage is invariant:* `coverage(F), coverage(G), coverage(Θ)` are the same in Σ' as in Σ. [L12, ASN-0043]

(c) *Content at endset addresses is unchanged:* for every I-address i in any endset's coverage, `Σ'.C(i) = Σ.C(i)` when `i ∈ dom(Σ.C)`. [S0, ASN-0036]

(d) *Discovery is permanent:* if `a ∈ discover_s(A)` in Σ for some fixed A, then `a ∈ discover_s(A)` in Σ'. [SV8]

(e) *Resolution is arrangement-dependent:*
- Extension of M(d) (K.μ⁺ or K.μ⁺_L) can only enlarge locate(e, d). [SV2]
- Contraction of M(d) can only shrink locate(e, d). [SV3]
- Reordering of M(d) preserves π(e, d); `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` where ψ is the reordering bijection from K.μ~. The locate *set* may change. [SV5]
- Changes to M(d) cannot affect `locate(e, d')` for `d' ≠ d`. [SV4]
- All other elementary transitions (K.α, K.δ, K.λ, K.ρ) preserve M in their frame, so `locate(e, d)` is unchanged.

(f) *Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field. [SV6]

(g) *Partial survival is well-structured:* the surviving text-subspace projection in any document is covered by finitely many ordinal-contiguous fragments within mapping blocks (a cover, not necessarily a partition, due to non-injective arrangements). [SV11]
