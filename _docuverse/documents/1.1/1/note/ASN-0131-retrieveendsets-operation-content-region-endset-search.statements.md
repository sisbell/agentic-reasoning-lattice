# ASN-0131 Claim Statements

*Source: ASN-0131-retrieveendsets-operation-content-region-endset-search.md (revised 2026-06-13) — Extracted: 2026-06-13*

## Definition — TouchPredicate

`touch_W(e) ≡ coverage(e) ∩ image(W, d, Σ) ≠ ∅`

where `W` names the region's V-position set, `e` is an endset, `coverage(e) ⊆ T` (ASN-0098), and `image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}` (F-IMG, ASN-0127).

## Definition — Addressable

`addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`

over ASN-0086's `nullified`.

## Definition — ContentImage

`I = image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}` (F-IMG, ASN-0127)

with `d ∈ dom(Σ.M)` and `W ⊆ T` a content-subspace V-position set (`∀ v ∈ W : subspace(v) = s_C`), yielding `I ⊆ dom(Σ.C)` by S3★ (ASN-0047).

## Definition — AvailablePool

`Avail(Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e) }`

a function of `(Σ.L, nullified(Σ))` independent of the region.

## Definition — DiscoverySelection

`sel(W, d, Σ) = { a ∈ addressable(Σ) : (∃ i : touch_W(Σ.L(a).eᵢ)) } = findlinks_V(W, d, Σ) ∩ addressable(Σ)`

because `findlinks_V(W, d, Σ) = {a ∈ dom(Σ.L) : (∃ i : coverage(Σ.L(a).eᵢ) ∩ image(W,d,Σ) ≠ ∅)}` (F-V, F-FIND, F-MATCH, ASN-0127).

---

## RE-DEF — RetrieveEndsetsDef (DEFINITION, def)

`RE(W, d, Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e ∧ touch_W(e)) }`, where the region `(W, d)` has `d ∈ dom(Σ.M)` and `W ⊆ T` a **content-subspace** V-position set (`∀ v ∈ W : subspace(v) = s_C`, a caller obligation, so the image lies in content — `I ⊆ dom(Σ.C)` by S3★, ASN-0047), resolving to `I = image(W, d, Σ)` (F-IMG, ASN-0127); `touch_W(e) ≡ coverage(e) ∩ I ≠ ∅` (ASN-0098, ASN-0043), and `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` (ASN-0086); the answer is a finite, computable set of role-tagged endsets, and the operation has frame `Σ' = Σ` (reads only, writes nothing)

## RE-LOC — Locality (INV, predicate)

Locality — for fixed `(W, d)`, `RE` is a function of `(Σ.M, Σ.L)` alone: it reads `Σ.M(d)` for the image and `Σ.L` for endsets and (via `nullified`) addressability; the content *values* `Σ.C`, the entity set `Σ.E`, and the provenance relation `Σ.R` are never consulted

## RE-UNIT — AnchoringWithoutNames (INV, predicate)

Anchoring without names — the answer's elements are `(role, endset)` pairs (anchoring structure), never link identities; the link address is withheld, distinct links sharing an endset value collapse to one pair, link multiplicity is not recoverable, and a surfaced from-endset cannot be paired with the to-endset of the same link

## RE-OVL — OverlapMatching (INV, predicate)

Overlap matching — an endset is surfaced iff at least one address it covers lies in the region's image (overlap, not containment); partial, single-address overlap suffices; the test is existential *within* an endset and applied *per-endset* against the one region, with no per-slot request differentiation

## RE-CLIP — NoClipping (INV, predicate)

No clipping (load-bearing) — no reported span is ever truncated to the region boundary; every surfaced span is reported at the full extent recorded in the link. This is universal across both the whole-endset (RE-WHOLE) and touching-spans-only readings; clipping would misrepresent the link's grip (a straddling span would be falsely shortened)

## RE-WHOLE — WholeEndsetSurfacing (INV, predicate)

Whole-endset surfacing (adopted convention) — the reading adopted here returns a surfaced endset in full, *all* of its spans (not only those intersecting `W`), so a discontiguous endset retains the spans pointing outside the region. This is a convention, not a forced consequence of RE-CLIP: a touching-spans-only implementation would still satisfy RE-CLIP while violating RE-WHOLE. Held **provisional** pending Open Question 1

## RE-BND — BoundaryCases (LEMMA, lemma)

Boundary cases — `RE(W, d, Σ) = ∅` whenever the image is empty (`W ∩ dom(Σ.M(d)) = ∅`, in particular a freshly registered document with empty arrangement) or `addressable(Σ) = ∅` (no links, or all nullified); and an empty endset slot (`∅`, admitted in non-type slots by ASN-0043, only the type-slot non-empty per L3) has `coverage(∅) = ∅`, so `touch_W(∅)` is false and it is never surfaced

## RE-SND — Soundness (LEMMA, lemma)

Soundness — `(i, e) ∈ RE(W, d, Σ) ⟹ e` is a genuine slot-`i` endset of an addressable link ∧ `touch_W(e)`; no anchoring is fabricated and none is reported that does not genuinely reach the region (no false positives)

## RE-CMP — Completeness (LEMMA, lemma)

Completeness — every addressable link `a` and slot `i` with `touch_W(Σ.L(a).eᵢ)` has `(i, Σ.L(a).eᵢ) ∈ RE(W, d, Σ)`; the answer is *exactly* the touching set, with no silent omission, whether reached by native or transcluded content

## RE-UDIST — UnionDistributivity (LEMMA, lemma)

Union-distributivity — `RE(W₁ ∪ W₂, d, Σ) = RE(W₁, d, Σ) ∪ RE(W₂, d, Σ)`: the forward image distributes over union unconditionally, so `touch_{W₁∪W₂}` is the disjunction `touch_{W₁} ∨ touch_{W₂}`, and the available slot-endset pool `Avail(Σ)` is region-independent; the RE-level analogue of F-UDIST/F-VDIST (ASN-0127). Intersection-distributivity does *not* follow — the forward image fails to distribute over intersection under the non-injective arrangement (M13, M14, ASN-0058) — and is left open

## RE-SEL — DiscoverySideSelection (LEMMA, lemma)

Discovery-side selection — `sel(W, d, Σ) = findlinks_V(W, d, Σ) ∩ addressable(Σ)` (F-V, ASN-0127): the contributing links are the addressable links discoverable through the region, so the operation is discovery-anchored — present-tense, non-monotone, arrangement-mediated (D-NONMONO, D-ZERO, ASN-0127), not existence-anchored (fixed-`I`, historical, monotone)

## RE-EXST — ExistenceOfAnchoringDeliverable (INV, predicate)

Existence-of-anchoring deliverable — by withholding identity the answer certifies the *presence and shape* of anchoring without making it followable; the foundation's existence/discovery axis (query mode: fixed vs arrangement-resolved) and the designer's existence/discovery axis (deliverable: structure vs named-and-followable) are orthogonal — RE is discovery on the first, existence-of-anchoring on the second

## RE-TRANS — TransclusionBlindness (LEMMA, lemma)

Transclusion blindness — surfacing is by content identity, independent of the link's home and of the covered content's origin (LP16, ASN-0098): a link reaching the region only through transcluded content is surfaced identically to one reaching native content, and each returned span describes the content's permanent home identity, not the borrowing V-position

## RE-IDENT — ContentIdentityInvariance (INV, predicate)

Content-identity invariance — each surfaced endset's coverage is permanent (L12, ASN-0043; LP3, ASN-0098), so the content-level answer (which I-addresses each surfaced endset anchors to) is arrangement-independent, even though the *selection* of which endsets are surfaced is arrangement-mediated

## RE-EDIT — PresentTenseStability (LEMMA, lemma)

Present-tense stability under editing — the answer tracks `d`'s current arrangement, the touch test composing on top of the region image: insertion surfaces newly-reachable anchoring (region image grows, F-IMG-MONO, ASN-0127), deletion drops anchoring whose content departs the region (region image shrinks, F-IMG-CONTR, ASN-0127; the contracted image no longer meets the coverage, so the touch test fails — LP10, LP12, ASN-0098 — the link nonetheless persisting, L12, ASN-0043, and re-surfaced on re-arrangement, F-IMG-MONO/LP9, ASN-0098), a region-local loss of reach, *not* the global orphaning/resurrection of LP17/LP18 (ASN-0098), whose premise of reach from no document a single-region deletion does not meet; rearrangement swings the *membership* of surfaced `(i, e)` pairs via the image swing (F-IMG-SWING, ASN-0127) while every surfaced endset's spans remain invariant — footprint fragmentation is a V-order *display* effect (ASN-0082), deferred to the rendered mode of open question 3, not a change to this content-identity answer; content identity is preserved throughout; edits to other documents leave the answer fixed (LP5, ASN-0098), as do content allocation `K.α` (LP6), entity creation `K.δ` (LP8, node/account creation also having frame `M' = M`), and provenance recording `K.ρ` (LP14, writing only `Σ.R`, which RE-LOC excludes) — all ASN-0098; the link-subspace extension `K.μ⁺_L`, though it edits `Σ.M(d)`, likewise leaves a content-region answer fixed (it adds only an `s_L` V-position `v_ℓ ∉ W`, so the image is unchanged — F-IMG-MONO sharpened to equality under `W ⊆ s_C`, ASN-0127 — and frames `Σ.L`), as does a *link-subspace-only* contraction `K.μ⁻` (`n'_{s_C} = n_{s_C}`, `n'_{s_L} < n_{s_L}`, ASN-0047 — the `Δ = ∅` case of RE-CWP); the single transition kind `K.μ⁻` is thus dual-natured — a *content-subspace* deletion `K.μ⁻` moves the answer through the image, a link-subspace-only one leaves it fixed. With insertion `K.μ⁺` and rearrangement `K.μ~` (content-subspace edits to `d`) moving it through the image, and `K.λ` moving it through `Σ.L` (ordinary emission may add a pair; a retraction removes *via the addressable population* — the only channel that shrinks it, since `dom(Σ.L)` grows by L12a/ASN-0043 and `nullified` grows by R6a/ASN-0086, whereas a content-subspace `K.μ⁻` removes through the image instead), this classifies every member of the vocabulary {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ} (ASN-0047)

## RE-RET — RetractionStability (LEMMA, lemma)

Retraction stability — a retraction is a `K.λ` emission, `Nullify(Σ, d_retr, ℓ) ≡ Emit_R(Σ, d_retr, ∅, {(ℓ, δ(1, #ℓ))})` (Nullify/Emit_K, ASN-0086): the same step marks `ℓ` nullified — removing it from `addressable(Σ)` permanently (R6a) — *and* emits a fresh, addressable retraction link `b` with endsets `(∅, {(ℓ, δ(1, #ℓ))}, R)`. For a content region (`W ⊆ s_C`, so `I ⊆ dom(Σ.C)`), the from-set `∅` and the to-set are disjoint from content *unconditionally*: the to-set covers only the link address `ℓ` and its `s_L`-extensions, by field-segment agreement along `≼` (Prefix/T4, ASN-0034: a content `c` with `ℓ ≼ c` would force `E(c)₁ = s_L ≠ s_C`), with `ℓ` genuinely `s_L` element-level (L0, L1, ASN-0093). The type-set `R` is *not* reached by that argument — a type endset may point anywhere, content included (L4, L9, ASN-0043), and ASN-0086's designated retraction type carries no structural disjointness — so `coverage(R) ∩ dom(Σ.C) = ∅` is an **imposed discipline** (seat `R` at a dedicated element-level subspace `s_R ≠ s_C`, after which field-segment agreement transfers), not a derivation. Under that discipline `b` touches nothing and a retraction's net effect on `RE` is removal only; an undisciplined `R` meeting the content image would instead surface `b` as `(3, R)` and *add* anchoring. Because the answer deduplicates `(role, endset)` pairs and discards identity (RE-UNIT), a pair `(i, e)` that `ℓ` bore leaves the answer **iff `ℓ` was its sole addressable bearer in `Σ`** (forward: under the discipline the emitter `b` cannot re-witness it and `ℓ` is gone by R6a; backward: any other live bearer `ℓ'` survives the step — `ℓ ⋠ ℓ'` by R0a/FlatLinkDomain and a single Nullify confines fresh nullification to its target by R-Scope/SingleTupleScope, both ASN-0086, so `ℓ' ∈ addressable(Σ')` with value fixed by L12, ASN-0043); an identical pair value may re-enter only via a separately, distinctly-identified live link (R6c, ASN-0086). Link-level permanence (R6a) is not pair-value-level permanence. (For a link-subspace region, `b`'s to-set can meet the image, so the "iff" would acquire an emitter conjunct — see the content-subspace restriction.)

## RE-CWP — ContractionStabilityWP (LEMMA, lemma)

Contraction-stability weakest precondition — for a `K.μ⁻[d, R]` step, `RE(W, d, ·) = RE(W, d, Σ)` iff `enabled(K.μ⁻[d, R]) ∧ (∀ (i, e) ∈ Avail(Σ) : coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅)`, where `I_R = {Σ.M(d)(v) : v ∈ W ∩ R}` (D-CWP bridge, ASN-0127), `Δ = image(W, d, Σ) ∖ I_R`, and `Avail(Σ)` is the region-independent pool of addressable slot-endsets; `RE` is monotone-decreasing under contraction (`RE(W, d, Σ') ⊆ RE(W, d, Σ)`), the condition is strictly finer than D-CWP's per-link condition, and `R = ∅` collapses it to `RE(W, d, Σ) = ∅`

## RE-DET — Determinism (INV, predicate)

Determinism — `RE(W, d, Σ)` is a function of `(W, d, Σ)`; with no intervening state change the same region query returns the same anchoring, so every change in the answer is the image of a change in `Σ`
