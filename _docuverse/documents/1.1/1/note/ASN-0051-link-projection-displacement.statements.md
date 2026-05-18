# ASN-0051 Claim Statements

*Source: ASN-0051-link-projection-displacement.md (revised 2026-03-23) — Extracted: 2026-05-17*

## Definition — EndsetProjection

For an endset e ∈ Endset and a document d ∈ E_doc, the *projection* of e onto d is:

`π(e, d) = coverage(e) ∩ ran(M(d))`

Two boundary cases: when d's arrangement shares no I-addresses with the endset, π(e, d) = ∅; when d's arrangement contains every I-address the endset references, π(e, d) = coverage(e).

## Definition — EndsetLocation

For an endset e and document d, the *location* of e in d is:

`locate(e, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

## Definition — Resolution

The *resolution* of endset e in document d is the function `locate(e, d)` — the set of V-positions in d whose content is part of e.

The two are related by M(d)'s function property (S2, ArrangementFunctionality): for all v ∈ dom(M(d)), v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d).

Since M(d) need not be injective — within-document sharing is permitted (S5, UnrestrictedSharing) — we may have |locate(e, d)| ≥ |π(e, d)|.

## Definition — TextSubspaceProjection

`π_text(e, d) = coverage(e) ∩ ran_text(M(d))`

where `ran_text(M(d)) = {M(d)(v) : v ∈ dom(M(d)) ∧ subspace(v) = s_C}` is the content-subspace portion of M(d)'s range.

`π_text(e, d) ⊆ π(e, d)` since `ran_text(M(d)) ⊆ ran(M(d))` by definition.

The block decomposition `ran_text(M(d)) = ⋃_k I(β_k)` used in the Partial Survival section is established there once B is in scope.

## Definition — EndsetVitality

An endset e is *vital in document d* when π(e, d) ≠ ∅ — at least one I-address that the endset references appears in d's current arrangement. Equivalently, locate(e, d) ≠ ∅.

## Definition — SlotwiseVitality

A link at address a with Σ.L(a) = (F, G, Θ) is *slotwise vital in d* when each non-empty content endset is vital in d:

`F = ∅ ∨ π(F, d) ≠ ∅`   and   `G = ∅ ∨ π(G, d) ≠ ∅`

## Definition — BilateralVitality

A link at address a with Σ.L(a) = (F, G, Θ) is *bilaterally vital in d* when both content endsets are non-empty *and* each projects non-emptily:

`F ≠ ∅ ∧ π(F, d) ≠ ∅`   and   `G ≠ ∅ ∧ π(G, d) ≠ ∅`

*Equivalent compact form.* The conjuncts `F ≠ ∅` and `G ≠ ∅` are mathematically redundant given the projection conjuncts: when `F = ∅`, `coverage(F) = ⋃_{(s, ℓ) ∈ ∅} ⟦(s, ℓ)⟧ = ∅` (vacuous union), so `π(F, d) = ∅ ∩ ran(M(d)) = ∅`, forcing `π(F, d) ≠ ∅ ⟹ F ≠ ∅`. The predicate is therefore equivalent to its two-conjunct compact form `π(F, d) ≠ ∅ ∧ π(G, d) ≠ ∅`.

## Definition — LinkDiscovery

For any state Σ, set of I-addresses A ⊆ T, and endset slot s ∈ {from, to, type}, define:

`discover_s(A) in Σ = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}`

## Definition — DiscoveryThroughDocument

`discover_through_s(d) in Σ = discover_s(ran(Σ.M(d))) in Σ`

— the set of links whose slot-s endset shares at least one I-address with d's current arrangement.

## Definition — DecompositionTerm

For each pair (j, k) with 1 ≤ j ≤ m and 1 ≤ k ≤ p, the *(j, k)-decomposition term* is the set `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)`. The number of decomposition terms is exactly m · p (possibly with empty terms).

## Definition — MaximalEndsetFragment

For an endset e and document d, let B = {β₁, ..., β_p} be the maximally merged block decomposition (C1a, ASN-0058) of the restriction M(d)|_{V_{s_C}(d)}. A *maximal fragment* of e in d is a maximal contiguous subsequence of I-addresses within a single mapping block's ordinal sequence taken within the *text-subspace projection* π_text(e, d). Formally, F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π_text(e, d) ∩ I(β_k) for some block β_k = (v_k, a_k, n_k), where F is maximal with respect to extending j₁ downward or j₂ upward within π_text(e, d) ∩ I(β_k). That is, either j₁ = 0 or a_k + (j₁ - 1) ∉ π_text(e, d), and either j₂ = n_k - 1 or a_k + (j₂ + 1) ∉ π_text(e, d).

---

## NoStaleResolutionState — NoStaleResolutionState (ARCH, remark)

*Schema closure.* (i) *Link-store signature [L3, ASN-0043; K.λ, ASN-0047].* The link value Σ.L(a) = (F, G, Θ) stores I-space content only — endsets are sets of spans (s, ℓ) over T (L3, NEndsetStructure); no V-address, no per-document arrangement, no creation-time snapshot is recorded in the link value at allocation (K.λ). (ii) *State-schema (present-state property) [Σ = (C, L, E, M, R), ASN-0047].* In the current ASN-0047 state schema, M(d) is the *current* arrangement; no component carries a historical M_k. R holds per-mapping provenance over I-addresses only (J0/J1/J1★, ASN-0047), not over V-addresses. No field of the current schema caches V-positions. (iii) *Operational closure [K = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}, ASN-0047].* No elementary transition writes a V-address into Σ.L, into a link value, or into any historical-M slot.

*Structural conclusion:* There is no field in which a stale V-position could persist, and no transition that could populate one. No state component external to (coverage(e), current M(d)) participates in resolution.

*Functional consequence.* `Σ₁.M(d) = Σ₂.M(d) ⇒ locate_{Σ₁}(e, d) = locate_{Σ₂}(e, d)` is immediate from the definition; no L-equality precondition is required.

---

## ArrangementLinkFrame — ArrangementLinkFrame (COR, corollary)

For every state transition Σ → Σ':

`(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

*Consequence for coverage:*

`(A Σ → Σ', a ∈ dom(Σ.L), s ∈ {from, to, type} :: coverage(Σ'.L(a).s) = coverage(Σ.L(a).s))`

---

## TransclusionCouplingAbsence — TransclusionCouplingAbsence (COR, corollary)

When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no *link-store* coupling step beyond K.μ⁺ itself.

*Fixed-A invariance (SV7).* For every fixed I-address set A, discover_s(A) evaluated in Σ' equals discover_s(A) evaluated in Σ. In particular, discover_s({a}) in Σ' = discover_s({a}) in Σ — call this set L_a.

*Document-derived set change.* A_{Σ}(d₂) = ran(Σ.M(d₂)) in Σ and A_{Σ'}(d₂) = ran(Σ'.M(d₂)) = A_{Σ}(d₂) ∪ {a} in Σ'. Discovery through d₂ in Σ' is:

`discover_s(A_{Σ'}(d₂)) = discover_s(A_{Σ}(d₂)) ∪ discover_s({a}) = discover_s(A_{Σ}(d₂)) ∪ L_a`

---

## SV2 — ExtensionMonotonicity (SV, lemma)

`(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', e, d :: π_Σ(e, d) ⊆ π_{Σ'}(e, d) ∧ locate_Σ(e, d) ⊆ locate_{Σ'}(e, d))`

*Projection.* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Coverage(e) is determined by e alone and is independent of state; when e is the slot value of a link in dom(L), L12 (LinkImmutability, ASN-0043) fixes that value across the transition. Combining state-independence of coverage with ran(M'(d)) ⊇ ran(M(d)) (both K.μ⁺ and K.μ⁺_L extend dom(M(d)) while preserving existing V↦I mappings), we have coverage(e) ∩ ran(M'(d)) ⊇ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*Resolution.* Let v ∈ locate_Σ(e, d). Then v ∈ dom(M(d)) and M(d)(v) ∈ coverage(e). Both K.μ⁺ and K.μ⁺_L preserve existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d))). So v ∈ dom(M'(d)) and M'(d)(v) = M(d)(v) ∈ coverage(e), giving v ∈ locate_{Σ'}(e, d). ∎

---

## SV3 — ContractionReduction (SV, lemma)

`(A Σ →_{K.μ⁻} Σ', e, d :: π_{Σ'}(e, d) ⊆ π_Σ(e, d) ∧ locate_{Σ'}(e, d) ⊆ locate_Σ(e, d))`

*Projection.* π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)). Coverage(e) is independent of state; when e is the slot value of a link in dom(L), L12 (LinkImmutability, ASN-0043) fixes that value. Combining state-independence of coverage with ran(M'(d)) ⊆ ran(M(d)) (K.μ⁻ restricts the domain while preserving values), we have coverage(e) ∩ ran(M'(d)) ⊆ coverage(e) ∩ ran(M(d)) = π_Σ(e, d). ∎

*Vitality loss condition:*

`π_Σ(e, d) ≠ ∅ ∧ π_{Σ'}(e, d) = ∅`

which requires: `(A a : a ∈ coverage(e) ∩ ran(M(d)) : a ∉ ran(M'(d)))` — every I-address that the endset shared with d's arrangement must be removed by the contraction.

*Resolution.* Let v ∈ locate_{Σ'}(e, d). Then v ∈ dom(M'(d)) and M'(d)(v) ∈ coverage(e). Since K.μ⁻ restricts the domain (dom(M'(d)) ⊂ dom(M(d))) while preserving values (M'(d)(v) = M(d)(v) for all v ∈ dom(M'(d))), we have v ∈ dom(M(d)) and M(d)(v) = M'(d)(v) ∈ coverage(e), giving v ∈ locate_Σ(e, d). ∎

---

## SV4 — ArrangementIsolation (SV, lemma)

`(A Σ →_{K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~} Σ', e, d, d' : d ≠ d' :: π_{Σ'}(e, d') = π_Σ(e, d'))`

Arrangement operations on document d do not alter any other document's arrangement (frame conditions of K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~: `(A d' : d' ≠ d : M'(d') = M(d'))`). Therefore π_{Σ'}(e, d') = coverage(e) ∩ ran(M'(d')) = coverage(e) ∩ ran(M(d')) = π_Σ(e, d').

*For resolution:* `locate_{Σ'}(e, d') = locate_Σ(e, d')`. Since M'(d') = M(d') (frame), locate_{Σ'}(e, d') = {v ∈ dom(M'(d')) : M'(d')(v) ∈ coverage(e)} = {v ∈ dom(M(d')) : M(d')(v) ∈ coverage(e)} = locate_Σ(e, d'). ∎

---

## SV5 — ReorderingProjectionInvariance (SV, lemma)

`(A Σ →_{K.μ~} Σ', e, d :: π_{Σ'}(e, d) = π_Σ(e, d))`

*Proof at composite endpoints.*

`π_{Σ'}(e, d) = coverage(e) ∩ ran(Σ'.M(d)) = coverage(e) ∩ ran(Σ.M(d)) = π_Σ(e, d)`

The middle equality is range invariance at composite endpoints: K.μ~'s ran-preservation corollary (ASN-0047) records that ran(M'(d)) = ran(M(d)) when read at the composite endpoints Σ and Σ' bracketing the full K.μ~ composite — because K.μ~ is a bijection on V-positions that holds the V↦I assignment's image fixed. ∎

*Composite-level scope.* SV5 is the *composite-endpoint* equality. Per-step ran is not invariant: it shrinks at the internal K.μ⁻ stage and recovers at the internal K.μ⁺ stage.

---

## SV5b — ReorderingLocateTransformation (SV, lemma)

Under the same K.μ~ hypothesis as SV5, with ψ the K.μ~ reordering bijection on dom(M(d)):

`(A Σ →_{K.μ~} Σ', e, d :: locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)})`

*Proof.* v' ∈ locate_{Σ'}(e, d) iff v' ∈ dom(M'(d)) and M'(d)(v') ∈ coverage(e). By K.μ~-FIX, dom(M'(d)) = dom(M(d)) and ψ is a bijection on this common domain (subspace-respecting), so every v' ∈ dom(M'(d)) equals ψ(v) for a unique v ∈ dom(M(d)), and M'(d)(ψ(v)) = M(d)(v). So M'(d)(v') ∈ coverage(e) iff M(d)(v) ∈ coverage(e) iff v ∈ locate_Σ(e, d). ∎

---

## SV6 — CrossOriginExclusion (SV, lemma)

For a span (s, ℓ) where s is element-level (zeros(s) = 3), the span's action point lies strictly within the element field (k > p₃, where k = actionPoint(ℓ) and p₃ is the position of the third zero component in s), and an address b with zeros(b) = 3 and origin(b) ≠ origin(s):

`b ∉ ⟦(s, ℓ)⟧`

*Preconditions:*
- `s, b ∈ T`
- `(s, ℓ)` is T12-well-formed (T12, SpanWellDefinedness, ASN-0034: `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`)
- `zeros(s) = 3 ∧ zeros(b) = 3`
- `s, b` are T4-valid
- `origin(b) ≠ origin(s)`
- `k > p₃`, where `k = actionPoint(ℓ)` and `p₃` is the position of the third zero component in s

*Equivalently*, the last condition `k > p₃` says the leading k − 1 components of s contain all three field separators: `|{i : 1 ≤ i ≤ k−1 ∧ sᵢ = 0}| = 3`.

---

## SV7 — DiscoveryInvarianceUnderLFrame (SV, lemma)

For every transition Σ → Σ' that holds L in frame — every L-frame elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ) and the distinguished composite K.μ~ — and for every fixed set of I-addresses A:

`discover_s(A) in Σ' = discover_s(A) in Σ`

*Proof.* Each L-frame transition holds dom(L') = dom(L) and L'(a) = L(a) for all a ∈ dom(L). Therefore coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) for every a ∈ dom(Σ.L), and dom(Σ'.L) = dom(Σ.L). Both inputs to discover_s — coverage and dom(L) — are identical in Σ and Σ', so the discovery sets are equal. ∎

The only elementary transition that can change discover_s is K.λ, which adds a new link to dom(L).

---

## SV8 — DiscoveryPermanence (SV, lemma)

For any fixed set of I-addresses A:

`(A Σ → Σ', a ∈ discover_s(A) in Σ :: a ∈ discover_s(A) in Σ')`

*Proof.* a ∈ discover_s(A) means coverage(Σ.L(a).s) ∩ A ≠ ∅. By L12, a ∈ dom(Σ'.L) and Σ'.L(a) = Σ.L(a). So coverage(Σ'.L(a).s) = coverage(Σ.L(a).s), and the intersection with A is unchanged. ∎

*Caveat.* SV8 quantifies over a fixed I-address set A; the document-derived specialisation discover_through_s(d) = discover_s(ran(M(d))) is not preserved across arrangement edits, because its argument ran(M(d)) is not fixed.

---

## SV9 — DiscoveryMonotonicity (SV, lemma)

`(A Σ → Σ' :: discover_s(A) in Σ ⊆ discover_s(A) in Σ')`

for any fixed A.

*Proof.* Take any a ∈ discover_s(A) in Σ: a ∈ dom(Σ.L) and coverage(Σ.L(a).s) ∩ A ≠ ∅. Two L-invariants from ASN-0043:

- *Entry preservation [L12].* L12 gives Σ'.L(a) = Σ.L(a) entry-by-entry for every a ∈ dom(Σ.L) ∩ dom(Σ'.L), so coverage(Σ'.L(a).s) = coverage(Σ.L(a).s) and its intersection with A is unchanged.
- *Domain non-shrinking [L12a].* L12a (LinkStoreMonotonicity, ASN-0043) gives dom(Σ'.L) ⊇ dom(Σ.L), so a ∈ dom(Σ.L) carries over to a ∈ dom(Σ'.L).

Both clauses of `a ∈ discover_s(A) in Σ'` membership are therefore met. ∎

---

## SV10 — DiscoveryProjectionIndependence (SV, lemma)

A link may be discoverable through a set of I-addresses A yet have only partial projection in a particular document:

`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

*Note.* Discovery through d entails non-empty projection in d: if a ∈ discover_s({M(d)(v) : v ∈ V}), then coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅, and since {M(d)(v) : v ∈ V} ⊆ ran(M(d)), we have π(Σ.L(a).s, d) ⊇ coverage(Σ.L(a).s) ∩ {M(d)(v) : v ∈ V} ≠ ∅.

---

## SV11 — PartialSurvivalDecomposition (SV, lemma)

Let e = {(s₁, ℓ₁), ..., (s_m, ℓ_m)} be an endset, and let B = {β₁, ..., β_p} be the maximally merged block decomposition of the restriction M(d)|_{V_{s_C}(d)}. The block-indexed expansion `ran_text(M(d)) = ⋃_k I(β_k)` holds under B. Two count claims:

**(a)** *Decomposition-term cover — exactly m · p terms.*

`π_text(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

The union is over *exactly* m · p decomposition terms (one per (span, block) pair), some possibly empty.

**(b)** *Maximal-fragment count — at most m · p fragments.* The same set π_text(e, d) is the disjoint union (within each block) of its maximal ordinal-contiguous fragments, totalling *at most* m · p of them across all blocks. The inequality is strict whenever (a) some decomposition term `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` is empty, or (b) two non-empty decomposition terms within a single block are ordinally adjacent or overlap, coalescing into a single maximal fragment. The bound m · p is attained iff every (j, k) pair yields a non-empty decomposition term *and* these terms are pairwise non-adjacent and non-overlapping within each block.

*Empty-arrangement boundary case (p = 0).* When M(d)|_{V_{s_C}(d)} = ∅, B is empty, so p = 0. The cover (a) becomes a vacuous union equal to ∅, matching π_text(e, d) = ∅; the fragment count (b) is 0.

*Derivation.* `coverage(e) = ⋃_{j=1}^{m} ⟦(sⱼ, ℓⱼ)⟧` and `ran_text(M(d)) = ⋃_{k=1}^{p} I(β_k)`, so:

`π_text(e, d) = (⋃_j ⟦(sⱼ, ℓⱼ)⟧) ∩ (⋃_k I(β_k)) = ⋃_j ⋃_k (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)) = ⋃_{j,k} (⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`

Each decomposition term ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k) is contiguous within its block's ordinal sequence (by S0 convexity and M1 OrderPreservation).

---

## SV14 — DocumentDerivedDiscoverySurvivability (SV, lemma)

**(a)** *Monotonicity under extension.*

`(A Σ →_{K.μ⁺/K.μ⁺_L} Σ', d, s :: discover_through_s(d) in Σ ⊆ discover_through_s(d) in Σ')`

*Proof.* K.μ⁺/K.μ⁺_L satisfy `ran(Σ.M(d)) ⊆ ran(Σ'.M(d))`. For every a ∈ discover_through_s(d) in Σ, coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ≠ ∅, so by L12 coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ⊇ coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ≠ ∅, giving a ∈ discover_through_s(d) in Σ'. ∎

**(b)** *Reduction under contraction.*

`(A Σ →_{K.μ⁻} Σ', d, s :: discover_through_s(d) in Σ' ⊆ discover_through_s(d) in Σ)`

*Proof.* K.μ⁻ satisfies `ran(Σ'.M(d)) ⊆ ran(Σ.M(d))`. For every a ∈ discover_through_s(d) in Σ', coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ≠ ∅, so by L12 coverage(Σ.L(a).s) ∩ ran(Σ.M(d)) ⊇ coverage(Σ'.L(a).s) ∩ ran(Σ'.M(d)) ≠ ∅, giving a ∈ discover_through_s(d) in Σ. ∎

**(c)** *Cross-document isolation.*

`(A Σ →_{K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~} Σ', d, d', s : d ≠ d' :: discover_through_s(d') in Σ' = discover_through_s(d') in Σ)`

*Proof.* All four transitions hold M(d') in frame for d' ≠ d; together with L12 the two inputs to discover_s — coverage and ran(M(d')) — are unchanged, so the discovery set is identical in both states. ∎

**(d)** *Non-permanence witness — strict shrinkage under contraction.*

`(E Σ →_{K.μ⁻} Σ', d, s, a ∈ dom(Σ.L) :: a ∈ discover_through_s(d) in Σ ∧ a ∉ discover_through_s(d) in Σ')`

**(e)** *Monotonicity under link allocation.*

`(A Σ →_{K.λ} Σ', d, s :: discover_through_s(d) in Σ ⊆ discover_through_s(d) in Σ')`

*Proof.* K.λ holds M in frame, so ran(Σ'.M(d)) = ran(Σ.M(d)). Therefore discover_through_s(d) in Σ' = discover_s(ran(Σ'.M(d))) in Σ' = discover_s(ran(Σ.M(d))) in Σ', and applying SV9 to the fixed I-address set A = ran(Σ.M(d)) gives discover_s(A) in Σ ⊆ discover_s(A) in Σ', i.e., discover_through_s(d) in Σ ⊆ discover_through_s(d) in Σ'. ∎

---

## ContentFidelity — ContentFidelity (COR, corollary)

For every a ∈ dom(Σ.C) and every state transition Σ → Σ', a ∈ dom(Σ'.C) and Σ'.C(a) = Σ.C(a).

Applied to endset I-addresses: for any link a ∈ dom(Σ.L) created at state Σ_k, and any later state Σ_j with j ≥ k:

`(A i : i ∈ coverage(Σ.L(a).s) ∩ dom(Σ_k.C) : Σ_j.C(i) = Σ_k.C(i))` for every endset slot s.

---

## CrossDocumentDecoupling — CrossDocumentDecoupling (COR, corollary)

Discovery in one document and empty resolution in another are simultaneously realisable:

`(E Σ, a, d₁, d₂, s, A :: d₁ ≠ d₂ ∧ a ∈ discover_s(A) ∧ A ⊆ ran(Σ.M(d₁)) ∧ π(Σ.L(a).s, d₂) = ∅)`

---

## SV13 — SurvivabilityTheorem (SV, theorem)

For a link a ∈ dom(Σ.L) with Σ.L(a) = (F, G, Θ), and for any state transition Σ → Σ':

**(a)** *The link persists:* a ∈ dom(Σ'.L) and Σ'.L(a) = (F, G, Θ). [L12]

**(b)** *Endset coverage is invariant:* coverage(F), coverage(G), coverage(Θ) are the same in Σ' as in Σ. [L12, ASN-0043]

**(c)** *Content at endset addresses is unchanged:* for every I-address i in any endset's coverage, Σ'.C(i) = Σ.C(i) when i ∈ dom(Σ.C). [S0, ASN-0036]

**(d)** *Discovery is permanent:* if a ∈ discover_s(A) in Σ for some fixed A, then a ∈ discover_s(A) in Σ'. [SV8]

**(e)** *Projection and resolution are arrangement-dependent:*

- Extension of M(d) — whether K.μ⁺ (content subspace) or K.μ⁺_L (link subspace) — can only enlarge π(e, d) and locate(e, d). [SV2]
- Contraction of M(d) can only shrink π(e, d) and locate(e, d). [SV3]
- Reordering of M(d) via the distinguished composite K.μ~:
  - *Composite-endpoint π-invariance:* K.μ~ preserves π(e, d) exactly at the composite endpoints Σ and Σ'. Per-step π is not invariant — it shrinks at the K.μ⁻ internal stage and recovers at the K.μ⁺ internal stage. [SV5]
  - *Locate-set transformation:* `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` where ψ is the K.μ~ reordering bijection. By K.μ~-FIX, ψ acts on a fixed domain — dom(M'(d)) = dom(M(d)). [SV5b]
- Changes to M(d) cannot affect locate(e, d') for d' ≠ d. [SV4]
- K.α, K.δ, K.ρ, and K.λ preserve M-values in their frame, so locate(e, d) is unchanged for every endset e and every pre-existing document d ∈ dom(Σ.M). K.δ additionally introduces a new document d_new with Σ'.M(d_new) = ∅, so `locate_{Σ'}(e, d_new) = ∅` for every endset e.

**(f)** *Cross-origin coverage exclusion:* new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the span's action point k satisfies k > p₃ (strictly beyond the third field separator). Scoped to element-level allocations (zeros(b) = 3) and element-level spans (k > p₃). Broader-level spans (k ≤ p₃) are not closed by this clause. [SV6]

**(g)** *Partial survival is well-structured:* the surviving text-subspace projection in any document is the union of *exactly* m · p decomposition terms `⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k)` (at the post-transition state's block count p; some possibly empty), equal as a set to the union of *at most* m · p maximal ordinal-contiguous fragments. The count inequality is strict whenever (a) some decomposition term is empty or (b) two non-empty terms within a single block are ordinally adjacent or overlap. The collection is a cover — not necessarily a partition — due to non-injective arrangements. [SV11]

**(h)** *Bilateral vitality survives extension and reordering; only contraction can falsify it.* For a link with `F ≠ ∅`, `G ≠ ∅`, `π_Σ(F, d) ≠ ∅`, `π_Σ(G, d) ≠ ∅` at Σ:

- *K.μ⁺ / K.μ⁺_L extension:* both `π(F, d) ≠ ∅` and `π(G, d) ≠ ∅` are preserved by SV2 applied slot-by-slot. Bilateral vitality survives.
- *K.μ~ reordering:* `π(F, d) ≠ ∅ ∧ π(G, d) ≠ ∅` preserved at composite endpoints by SV5 applied slot-by-slot. Bilateral vitality survives.
- *K.μ⁻ contraction:* the wp form is the conjunction of two K.μ⁻-vitality conditions read per side: `(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(F))` *and* the symmetric clause for coverage(G). Bilateral vitality is lost exactly when at least one side's conjunct fails.
- *M-frame transitions K.α, K.δ, K.ρ, K.λ:* bilateral vitality of every pre-existing link is preserved.

[SV2, SV3, SV4, SV5 read per slot; BilateralVitality predicate]

**(i)** *System-level discovery structure:*

- (i₁) *Invariance under L-frame transitions:* `discover_s(A) in Σ' = discover_s(A) in Σ` for every L-frame elementary transition and K.μ~. [SV7]
- (i₂) *Monotonic growth under K.λ:* `discover_s(A) in Σ ⊆ discover_s(A) in Σ'` for any transition; strict growth occurs exactly when a freshly allocated link's slot-s endset shares an I-address with A. [SV9]
- (i₃) *Discovery does not entail full projection:* `(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`. [SV10, CrossDocumentDecoupling]
- (i₄) *Document-derived discovery non-permanence:* `discover_through_s(d)` is not permanent; it is monotonic under K.μ⁺/K.μ⁺_L, reduced under K.μ⁻, isolated across d ≠ d', and monotonic under K.λ. [SV14]

---

## NewLinkEvaluationDefinedness — NewLinkEvaluationDefinedness (COR, corollary)

For a link a_new allocated by K.λ at Σ → Σ' with Σ'.L(a_new) = (F_new, G_new, Θ_new), every slot s ∈ {from, to, type} and every document d ∈ dom(Σ'.M) yield well-defined values `locate(Σ'.L(a_new).s, d)` and `discover_s(A)` (with a_new admissible to enter) immediately at Σ' without any additional state-priming step.

*Four definedness obligations:*

1. `Σ'.L(a_new)` is defined at Σ': K.λ's effect is exactly `Σ'.L = Σ.L ⊕ {a_new ↦ (F_new, G_new, Θ_new)}`, so a_new ∈ dom(Σ'.L) immediately.
2. `.s` is well-defined for s ∈ {from, to, type}: L3 (NEndsetStructure, ASN-0043) requires `|Σ'.L(a_new)| ≥ 3`, the K.λ-amendment records the value as a standard triple.
3. `coverage(Σ'.L(a_new).s)` is a well-defined subset of T: L4 (EndsetGenerality, ASN-0043) makes each slot value a set of spans over T; coverage is well-defined under T12.
4. `Σ'.M(d)` is well-defined for d ∈ dom(Σ'.M): K.λ holds M in frame, so `Σ'.M(d) = Σ.M(d)` for every d ∈ dom(Σ.M) = dom(Σ'.M).

---

## wp — WeakestPrecondition (WP, analysis)

For postcondition R = `π_{Σ'}(e, d) ≠ ∅` (*endset e remains vital in d after the transition*):

**wp(K.μ⁻ removing V_rm ⊆ dom(Σ.M(d)), π(e, d) ≠ ∅)** =

`(E v : v ∈ dom(Σ.M(d)) \ V_rm : Σ.M(d)(v) ∈ coverage(e))`

under the domain-of-applicability precondition that V_rm is D-SEQ-admissible (for every subspace S, V_rm ∩ V_S(d) is an upward tail of V_S(d) or empty).

*Vitality-loss condition:* `(A v : v ∈ dom(Σ.M(d)) \ V_rm :: Σ.M(d)(v) ∉ coverage(e))` together with `(E v : v ∈ V_rm : Σ.M(d)(v) ∈ coverage(e))`.

**wp(K.μ⁺ adding extension Δ with I_new = ran(Δ) ⊆ dom(Σ.C), π(e, d) ≠ ∅)** =

`π(e, d) ≠ ∅ ∨ coverage(e) ∩ I_new ≠ ∅`

Single-mapping specialisation Δ = {(v_new, i_new)}: `π(e, d) ≠ ∅ ∨ i_new ∈ coverage(e)`.

**wp(K.μ⁺_L adding v_ℓ ↦ ℓ, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅ ∨ ℓ ∈ coverage(e)`

**wp(K.μ~ under bijection ψ, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅`

**wp(K.α, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅`

**wp(K.δ, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅`

**wp(K.ρ, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅`

**wp(K.λ, π(e, d) ≠ ∅)** = `π(e, d) ≠ ∅` for every pre-existing endset e.

For postcondition `a ∈ discover_s(A)`:

**wp(K, a ∈ discover_s(A))** = `a ∈ discover_s(A)` for every L-frame elementary K ∈ {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ} and for the distinguished composite K.μ~, for every fixed A.

**wp(K.λ allocating a_new with L_new(a_new) = (F_new, G_new, Θ_new), a ∈ discover_s(A))** =

`a ∈ discover_s(A) ∨ (a = a_new ∧ coverage(L_new.s) ∩ A ≠ ∅)`
