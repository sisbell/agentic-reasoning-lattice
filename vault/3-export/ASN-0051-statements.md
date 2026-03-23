# ASN-0051 Formal Statements

*Source: ASN-0051-link-survivability.md (revised 2026-03-20) — Extracted: 2026-03-23*

## Definition — EndsetProjection

For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

---

## Definition — EndsetResolution

For an endset e and document d, the *resolution* of e in d is:

`resolve(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

Relationship to projection: v ∈ resolve(e, d) iff M(d)(v) ∈ π(e, d). Since M(d) need not be injective, |resolve(e, d)| ≥ |π(e, d)|.

---

## Definition — EndsetVitality

An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, resolve(e, d) ≠ ∅.

---

## Definition — BilateralVitality

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(Type endset Θ excluded: type endsets may reference addresses outside dom(Σ.C), per L9.)

When both F = ∅ and G = ∅, both disjunctions are satisfied by the left branch — the link is bilaterally vital in every document vacuously.

---

## Definition — LinkDiscovery

For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

Partial overlap suffices — a single shared I-address is enough to discover the link.

---

## Definition — EndsetFragment

For an endset e and document d with block decomposition B = {β₁, ..., β_p} of M(d), a *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence.

Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π(e, d).

---

## Definition — TextSubspaceProjection

For an endset e and document d with block decomposition B = {β₁, ..., β_p}:

`π_text(e, d) = coverage(e) ∩ ran_text(M(d))`

where `ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ v₁ ≥ 1} = ⋃_k I(β_k)`.

---

## SV0 — ResolutionCurrentness (LEMMA, lemma)

For any endset e and document d:

`resolve(e, d) is determined entirely by coverage(e) and the current M(d)`

There is no mechanism by which stale arrangement information could participate, because the link stores only I-addresses (via its endset spans), and V-addresses are derived from them through the current arrangement.

---

## SV1 — ArrangementLinkFrame (LEMMA, lemma)

For every state transition Σ → Σ':

`(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

*Consequence for coverage:*

`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

*Consequence for directionality:* The from/to/type slot assignment is a structural property of the link value. Since L12 preserves the entire link value, the directional assignment is permanent.

---

## SV2 — ExtensionMonotonicity (LEMMA, lemma)

`(A Σ →_{K.μ⁺} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d))`

*Resolution corollary:* `resolve_Σ(e, d) ⊆ resolve_{Σ'}(e, d)`.

For all v ∈ resolve_Σ(e, d): v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Since K.μ⁺ preserves existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))), v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ resolve_{Σ'}(e, d). New V-positions in dom(M'(d)) \ dom(M(d)) may additionally enter the resolve set when their I-addresses lie in coverage(e).

---

## SV3 — ContractionReduction (LEMMA, lemma)

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d))`

*Vitality loss condition:*

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

*Resolution corollary:* `resolve_{Σ'}(e, d) ⊆ resolve_Σ(e, d)`.

For all v ∈ resolve_{Σ'}(e, d): v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ resolve_Σ(e, d).

---

## SV4 — ArrangementIsolation (LEMMA, lemma)

`(A Σ →_{K.μ⁺/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

Frame condition used: `(A d' : d' ≠ d : M'(d') = M(d'))`.

*Resolution corollary:* `resolve_{Σ'}(e, d') = resolve_Σ(e, d')`.

Since M'(d') = M(d'), resolve_{Σ'}(e, d') = {v ∈ dom(M'(d')) : M'(d')(v) ∈ coverage(e)} = {v ∈ dom(M(d')) : M(d')(v) ∈ coverage(e)} = resolve_Σ(e, d').

---

## SV5 — ReorderingProjectionInvariance (LEMMA, lemma)

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). The resolution relationship is:

`resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)}`

In general, resolve_{Σ'}(e, d) ≠ resolve_Σ(e, d) as sets.

*Witness:* let dom(M(d)) = {v₁, v₂} with M(d) = {v₁ ↦ a₁, v₂ ↦ a₂}, and let coverage(e) = {a₁} (so resolve_Σ(e, d) = {v₁}). The swap ψ(v₁) = v₂, ψ(v₂) = v₁ gives M'(d) = {v₁ ↦ a₂, v₂ ↦ a₁}, so resolve_{Σ'}(e, d) = {v₂} ≠ {v₁}.

---

## SV6 — CrossOriginExclusion (LEMMA, lemma)

For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Precondition:* s and b are element-level tumblers (zeros(s) = 3, zeros(b) = 3), so origin(s) and origin(b) are well-defined. Let p₃ denote the position of the third zero component in s; the precondition is k > p₃ where k is the action point of ℓ. Equivalently: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`.

*Same-origin sequential overshoot:* if a span's reach extends beyond the current allocation maximum, future sibling allocations will enter the span as they advance through the ordinal sequence.

*Same-origin child-depth entry:* a child-depth address c produced by inc(t, 1) satisfies t < c < t+1. If an endset span contains t and has reach ≥ t+1, c falls within the span.

---

## SV7 — TransclusionCouplingAbsence (LEMMA, lemma)

When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)):

`discover_s({a}) in Σ ⊆ discover_s({a}) in Σ'`

No K.ρ (provenance recording), no link-store operation, and no additional elementary transition is required for d₂ to inherit all of a's link associations. K.μ⁺ alone suffices, because discovery operates on I-addresses (which K.μ⁺ shares) and L12 preserves the link store across the transition.

*Basis:* Direct corollary of SV8 instantiated with A = {a}.

---

## SV8 — DiscoveryPermanence (LEMMA, lemma)

For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

*Proof basis:* a ∈ discover_s(A) means coverage(Σ.L(a).s) ∩ A ≠ ∅. By L12, a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a). So coverage(Σ'.L(a).s) = coverage(Σ.L(a).s), and the intersection with A is unchanged.

---

## SV9 — DiscoveryMonotonicity (LEMMA, lemma)

For any fixed A:

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow.

---

## SV10 — DiscoveryResolutionIndependence (LEMMA, lemma)

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

*Corollary within the discovering document:* if a ∈ discover_s({M(d)(v) : v ∈ V}), then:

`coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅`

and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)):

`π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅`

So within the discovering document, resolution is guaranteed non-empty.

---

## SV11 — PartialSurvivalDecomposition (LEMMA, lemma)

Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be a block decomposition of M(d). Define the *text-subspace projection* π_text(e, d) = coverage(e) ∩ ran_text(M(d)), where ran_text(M(d)) = ⋃_k I(β_k). Then:

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

*Contiguity basis:* For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, since a_k + j₁ < a_k + j₂ < a_k + j₃ (by TA-strict), by convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence each intersection ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is a contiguous ordinal subsequence, compactly described by (a_k + j₁, j₂ − j₁ + 1).

Total fragment count is bounded by m · p.

*Note:* In the current foundation model (no defined operation creates non-text V-positions), π_text(e, d) = π(e, d) for all reachable states.

---

## SV12 — ContentFidelity (LEMMA, lemma)

For every a ∈ dom(Σ.C) and every state transition Σ → Σ':

`a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`

Applied to endset I-addresses: for any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k:

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))`

for every endset slot s.

---

## SV13 — SurvivabilityTheorem (THEOREM, lemma)

For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

**(a)** *The link persists:*

`a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, Θ)`

**(b)** *Endset coverage is invariant:*

`coverage(F), coverage(G), coverage(Θ) are the same in Σ' as in Σ`

**(c)** *Content at endset addresses is unchanged:*

`(A i ∈ coverage(F) ∪ coverage(G) ∪ coverage(Θ) : i ∈ dom(Σ.C) ⟹ Σ'.C(i) = Σ.C(i))`

**(d)** *Discovery is permanent:*

`a ∈ discover_s(A) in Σ ⟹ a ∈ discover_s(A) in Σ'`

**(e)** *Resolution is arrangement-dependent:*

- `Σ →_{K.μ⁺} Σ' ⟹ resolve_Σ(e, d) ⊆ resolve_{Σ'}(e, d)`
- `Σ →_{K.μ⁻} Σ' ⟹ resolve_{Σ'}(e, d) ⊆ resolve_Σ(e, d)`
- `Σ →_{K.μ~} Σ' ⟹ π_{Σ'}(e, d) = π_Σ(e, d) ∧ resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)}` where ψ is the reordering bijection from K.μ~
- `d ≠ d' ⟹ π_{Σ'}(e, d') = π_Σ(e, d') ∧ resolve_{Σ'}(e, d') = resolve_Σ(e, d')`
- All other elementary transitions (K.α, K.δ, K.ρ) preserve M in their frame, so resolve(e, d) is unchanged.

**(f)** *Coverage stability is level-dependent:*

- Element-level endset spans (zeros(s) = 3, action point within element field): `b ∉ ⟦(s, ℓ)⟧` for any newly allocated b with origin(b) ≠ origin(s) [SV6]
- Same-origin coverage growth at byte level: closed by sequential sibling allocation discipline
- Same-origin coverage growth at broader levels: open by design

**(g)** *Partial survival is well-structured:*

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

decomposing into finitely many ordinal-contiguous fragments, each compactly described by start address and count. [SV11]
