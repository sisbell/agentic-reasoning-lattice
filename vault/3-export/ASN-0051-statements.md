# ASN-0051 Formal Statements

*Source: ASN-0051-link-survivability.md (revised 2026-03-20) — Extracted: 2026-03-20*

## Definition — EndsetProjection

For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

## Definition — EndsetResolution

For an endset e and document d, the *resolution* of e in d is:

`resolve(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

v ∈ resolve(e, d) iff M(d)(v) ∈ π(e, d). Since M(d) need not be injective, we may have |resolve(e, d)| ≥ |π(e, d)|.

## Definition — EndsetVitality

An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, resolve(e, d) ≠ ∅.

## Definition — BilateralVitality

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when each non-empty content endset is vital in d:

`F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`

(The type endset is excluded from the vitality condition per L9, TypeGhostPermission.)

## Definition — LinkDiscovery

For a set of I-addresses A ⊆ dom(Σ.C) and an endset slot s ∈ {from, to, type}:

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

Partial overlap suffices — a single shared I-address is enough to discover the link.

## Definition — EndsetFragment

For an endset e and document d with block decomposition B = {β₁, ..., β_p} of M(d), a *fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence. Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π(e, d).

---

## π(e, d) — EndsetProjection (DEF, function)

`π(e, d) = coverage(e) ∩ ran(M(d))`

## resolve(e, d) — EndsetResolution (DEF, function)

`resolve(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

## Vitality — EndsetVitality (DEF, predicate)

An endset e is vital in document d when:

`π(e, d) ≠ ∅`

## BilateralVitality — BilateralVitality (DEF, predicate)

Link at address a with Σ.L(a) = (F, G, Θ) is bilaterally vital in d when:

`(F = ∅ ∨ π(F, d) ≠ ∅) ∧ (G = ∅ ∨ π(G, d) ≠ ∅)`

## discover_s(A) — LinkDiscovery (DEF, function)

`discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

## SV0 — ResolutionCurrentness (INV, lemma)

For any endset e and document d:

`resolve(e, d) is determined entirely by coverage(e) and the current M(d)`

There is no mechanism by which stale arrangement information could participate, because the link stores only I-addresses (via its endset spans), and V-addresses are derived from them through the current arrangement.

## SV1 — ArrangementLinkFrame (INV, lemma)

For every state transition Σ → Σ':

`(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

*Consequence for coverage:*

`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

## SV2 — ExtensionMonotonicity (INV, lemma)

Writing π_Σ(e, d) when the state at which projection is evaluated matters:

`(A Σ →_{K.μ⁺} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d))`

*Proof:* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (SV1) and ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺ frame), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*For resolution:* resolve_Σ(e, d) ⊆ resolve_{Σ'}(e, d). Let v ∈ resolve_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Since K.μ⁺ preserves existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))), we have v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ resolve_{Σ'}(e, d). ∎

## SV3 — ContractionReduction (INV, lemma)

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d))`

*Proof:* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Since coverage(e) is invariant (SV1) and ran(M'(d)) ⊆ ran(M(d)) (K.μ⁻ restricts the domain while preserving values), we have coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*For resolution:* resolve_{Σ'}(e, d) ⊆ resolve_Σ(e, d). Let v ∈ resolve_{Σ'}(e, d). Then v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), we have v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ resolve_Σ(e, d). ∎

Vitality loss condition:

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))`

## SV4 — ArrangementIsolation (INV, lemma)

`(A Σ →_{K.μ⁺/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

From frame conditions of K.μ⁺, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`. Therefore π_{Σ'}(e, d') = coverage(e) ∩ ran(M'(d')) = coverage(e) ∩ ran(M(d')) = π_Σ(e, d').

*For resolution:* `resolve_{Σ'}(e, d') = resolve_Σ(e, d')`. Since M'(d') = M(d') (frame), resolve_{Σ'}(e, d') = {v ∈ dom(M'(d')) : M'(d')(v) ∈ coverage(e)} = {v ∈ dom(M(d')) : M(d')(v) ∈ coverage(e)} = resolve_Σ(e, d'). ∎

## SV5 — ReorderingProjectionInvariance (INV, lemma)

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

Let ψ be the reordering bijection from K.μ~ (so that M'(d)(ψ(v)) = M(d)(v) for all v ∈ dom(M(d))). The formal relationship is:

`resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)}`

*Proof:* v' ∈ resolve_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e). Since ψ is a bijection from dom(M(d)) to dom(M'(d)), every v' ∈ dom(M'(d)) equals ψ(v) for a unique v ∈ dom(M(d)), and M'(d)(ψ(v)) = M(d)(v). So M'(d)(v') ∈ coverage(e) iff M(d)(v) ∈ coverage(e) iff v ∈ resolve_Σ(e, d). ∎

In general, resolve_{Σ'}(e, d) ≠ resolve_Σ(e, d) as sets.

## SV6 — CrossOriginExclusion (INV, lemma)

For a span (s, ℓ) in an existing endset where s is element-level (zeros(s) = 3), and a newly allocated address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Precondition:* s and b are element-level tumblers (zeros(s) = 3, zeros(b) = 3), so origin(s) and origin(b) are well-defined. The action point k of ℓ must satisfy: for s with zeros(s) = 3, let p₃ denote the position of the third zero component in s; the precondition is k > p₃. Equivalently, the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`.

*Proof:* Let k be the action point of ℓ, with k > p₃ as stated. By TumblerAdd, components before k are copied from s, and (s ⊕ ℓ)ₖ = sₖ + ℓₖ. Consider any t with s ≤ t < s ⊕ ℓ. For any j < k, if t diverges from s at position j then tⱼ > sⱼ (T1 case (i)), but sⱼ = (s ⊕ ℓ)ⱼ, so tⱼ > (s ⊕ ℓ)ⱼ, giving t > s ⊕ ℓ — contradicting t < s ⊕ ℓ. Hence t agrees with s on all positions 1 through k−1. Since k > p₃, these positions include all three field-separator positions, so origin(t) = origin(s). Any element-level b with origin(b) ≠ origin(s) satisfies b ∉ ⟦(s, ℓ)⟧. ∎

## SV7 — TransclusionCouplingAbsence (INV, lemma)

When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself. Formally, the monotonicity result discover_s({a}) in Σ ⊆ discover_s({a}) in Σ' is a direct corollary of SV8 instantiated with A = {a}. No K.ρ (provenance recording), no link-store operation, and no additional elementary transition is required for d₂ to inherit all of a's link associations. K.μ⁺ alone suffices, because discovery operates on I-addresses (which K.μ⁺ shares) and L12 preserves the link store across the transition.

## SV8 — DiscoveryPermanence (INV, lemma)

For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

*Proof:* a ∈ discover_s(A) means coverage(Σ.L(a).s) ∩ A ≠ ∅. By L12, a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a). So coverage(Σ'.L(a).s) = coverage(Σ.L(a).s), and the intersection with A is unchanged. ∎

## SV9 — DiscoveryMonotonicity (INV, lemma)

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

for any fixed A. New links may be created (L12a, LinkStoreMonotonicity: dom(Σ'.L) ⊇ dom(Σ.L)), so the discoverable set can only grow.

## SV10 — DiscoveryResolutionIndependence (INV, lemma)

A link may be discoverable through a set of I-addresses A yet have only partial resolution in a particular document:

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

Note that discovery through d entails non-empty projection in d: if a ∈ discover_s({M(d)(v) : v ∈ V}), then coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅, and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)), we have π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅.

## SV11 — PartialSurvivalDecomposition (INV, lemma)

Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be a block decomposition of M(d). Define the *text-subspace projection*:

`π_text(e, d) = coverage(e) ∩ ran_text(M(d))`

where ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ v₁ ≥ 1} = ⋃_k I(β_k). Then:

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

For ordinal indices j₁ < j₂ < j₃ with a_k + j₁ and a_k + j₃ both in ⟦(sⱼ, ℓⱼ)⟧, we have a_k + j₁ < a_k + j₂ < a_k + j₃ (by TA-strict), so by the convexity of the span (S0), a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧. Hence the intersection is contiguous within the ordinal sequence of I(β_k): if the first and last elements have ordinal offsets j₁ and j₂ respectively, then every intermediate element a_k + j with j₁ ≤ j ≤ j₂ also lies in the intersection. The number of fragments is bounded by m · p.

(The full projection π(e, d) = coverage(e) ∩ ran(M(d)) may additionally include I-addresses reached through non-text-subspace V-positions. In the current foundation model, no defined operation creates non-text V-positions, so π_text(e, d) = π(e, d) for all reachable states.)

## SV12 — ContentFidelity (INV, lemma)

For any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k:

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))`

for every endset slot s.

## SV13 — SurvivabilityTheorem (INV, lemma)

For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

**(a)** *The link persists:*

`a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, Θ)`

[L12]

**(b)** *Endset coverage is invariant:* coverage(F), coverage(G), coverage(Θ) are the same in Σ' as in Σ. [SV1, from L12]

**(c)** *Content at endset addresses is unchanged:*

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ.C) : Σ'.C(i) = Σ.C(i))`

for every endset slot s. [SV12, from S0]

**(d)** *Discovery is permanent:* if a ∈ discover_s(A) in Σ for some fixed A, then a ∈ discover_s(A) in Σ'. [SV8]

**(e)** *Resolution is arrangement-dependent:*
- Extension of M(d) can only enlarge resolve(e, d). [SV2]
- Contraction of M(d) can only shrink resolve(e, d). [SV3]
- Reordering of M(d) preserves π(e, d); resolve_{Σ'}(e, d) = {ψ(v) : v ∈ resolve_Σ(e, d)} where ψ is the reordering bijection from K.μ~. The resolve *set* may change. [SV5]
- Changes to M(d) cannot affect resolve(e, d') for d' ≠ d. [SV4]
- All other elementary transitions (K.α, K.δ, K.ρ) preserve M in their frame, so resolve(e, d) is unchanged.

**(f)** *Coverage stability is level-dependent:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the action point is within the element field (SV6). Same-origin coverage growth depends on the allocation regime — closed at the byte level by sequential sibling allocation, open at broader address levels by design.

**(g)** *Partial survival is well-structured:* the surviving projection in any document decomposes into finitely many ordinal-contiguous fragments within mapping blocks. [SV11]
