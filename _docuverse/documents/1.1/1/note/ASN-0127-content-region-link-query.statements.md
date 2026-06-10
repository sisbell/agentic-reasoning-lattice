# ASN-0127 Claim Statements

*Source: ASN-0127-content-region-link-query.md (revised unknown) — Extracted: 2026-06-10*

## Definition — Image

**F-IMG (ImageDefinition).** *For `d ∈ dom(Σ.M)` and `W ⊆ T`:*

> `image(W, d, Σ) ≡ {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`

*For `d ∉ dom(Σ.M)`, `image(W, d, Σ)` is undefined.*

Degenerate cases: `image(∅, d, Σ) = ∅`; and `image(W, d, Σ) = ∅` whenever `W ∩ dom(Σ.M(d)) = ∅`.

## Definition — MatchPredicate

**F-MATCH (MatchPredicate).** *For `a ∈ dom(Σ.L)` and `I ⊆ T`:*

> `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`

## Definition — FindLinks

**F-FIND (FindPrimitive).** *The bare comprehension:*

> `findlinks(I, Σ) ≡ {a ∈ dom(Σ.L) : matches(a, I, Σ)}`

Degenerate case: `findlinks(∅, Σ) = ∅`.

## Definition — FindLinksV

**F-V (TwoPhaseFactoring).** *For `d ∈ dom(Σ.M)`, `W ⊆ T`:*

> `findlinks_V(W, d, Σ) ≡ findlinks(image(W, d, Σ), Σ)`

*Undefined when `d ∉ dom(Σ.M)`.* Degenerate case: `findlinks_V(W, d, Σ) = ∅` whenever `image(W, d, Σ) = ∅`.

## Definition — FindLinksDisc

**Discovery-anchored combinator.** *Given `d_q ∈ dom(Σ.M)` and query V-region `W ⊆ T`:*

> `findlinks_disc(W, d_q, Σ) ≡ findlinks(image(W, d_q, Σ), Σ)` = `findlinks_V(W, d_q, Σ)`

---

## F-IMG — ImageDefinition (DEF, definition)

*For `d ∈ dom(Σ.M)` and `W ⊆ T`:*

> `image(W, d, Σ) ≡ {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`

*For `d ∉ dom(Σ.M)`, `image(W, d, Σ)` is undefined.*

---

## F-IMG-MONO — ImageMonotonicityUnderArrangementExtension (LEMMA, lemma)

*If `Σ → Σ'` extends `Σ.M(d)` (a K.μ⁺ or K.μ⁺_L step that adds positions to `d`'s arrangement while agreeing on prior positions), then for every `W ⊆ T`:*

> `image(W, d, Σ) ⊆ image(W, d, Σ')`

*Precondition: `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))`.*

---

## F-IMG-CONTR — ImageContractionUnderArrangementContraction (LEMMA, lemma)

*If `Σ → Σ'` contracts `Σ.M(d)` (a K.μ⁻ step), then:*

> `image(W, d, Σ') ⊆ image(W, d, Σ)`

*Precondition: `dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ'.M(d))` (retained-domain agreement).*

---

## F-IMG-SWING — ImageSwingUnderReorder (LEMMA, lemma)

*If `Σ → Σ'` is a K.μ~ reorder of `d`'s arrangement with witnessing bijection `π`, then:*

> `image(W, d, Σ') = {Σ.M(d)(u) : u ∈ π⁻¹(W) ∩ dom(Σ.M(d))}`

*The total range is preserved (`ran(Σ'.M(d)) = ran(Σ.M(d))`) but the forward image of a fixed sub-region `W` may change membership; and when `Σ.M(d)` is non-injective — content sharing (M13/M14, ASN-0058) — the image may additionally gain or lose members (change cardinality). Under injective `Σ.M(d)` only membership change is realizable.*

*Precondition (bijection equation): `Σ'.M(d)(π(u)) = Σ.M(d)(u)` for every `u ∈ dom(Σ.M(d))`; `dom(Σ'.M(d)) = dom(Σ.M(d))` (K.μ~-FIX).*

---

## F-MATCH — MatchPredicate (DEF, definition)

*For `a ∈ dom(Σ.L)` and `I ⊆ T`:*

> `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`

---

## F-FIND — FindPrimitive (DEF, definition)

*The bare comprehension:*

> `findlinks(I, Σ) ≡ {a ∈ dom(Σ.L) : matches(a, I, Σ)}`

*Degenerate case: `findlinks(∅, Σ) = ∅`.*

---

## F-UDIST — UnionDistributivity (LEMMA, lemma)

*For all I-address sets `I₁, I₂ ⊆ T` — no disjointness required:*

> `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`

---

## F-IMONO — FindMonotonicityInI (LEMMA, lemma)

*Corollary of F-UDIST. For all I-address sets `I' ⊆ I ⊆ T`:*

> `findlinks(I', Σ) ⊆ findlinks(I, Σ)`

---

## F-V — TwoPhaseFactoring (DEF, definition)

*For `d ∈ dom(Σ.M)`, `W ⊆ T`:*

> `findlinks_V(W, d, Σ) ≡ findlinks(image(W, d, Σ), Σ)`

*Undefined when `d ∉ dom(Σ.M)`. Degenerate case: `findlinks_V(W, d, Σ) = ∅` whenever `image(W, d, Σ) = ∅` — in particular for `W = ∅`, for any `W` with `W ∩ dom(Σ.M(d)) = ∅`, and for a freshly registered `d` with empty arrangement.*

---

## F-VDIST — RegionUnionDistributivity (LEMMA, lemma)

*For `d ∈ dom(Σ.M)` and any V-regions `W₁, W₂ ⊆ T` — no disjointness required:*

> `findlinks_V(W₁ ∪ W₂, d, Σ) = findlinks_V(W₁, d, Σ) ∪ findlinks_V(W₂, d, Σ)`

---

## F-CIL — ComprehensionInvariantUnderΣL (META-LEMMA, lemma)

*If `Σ.L = Σ'.L` as partial functions, then for every comprehension*

> `{a ∈ dom(Σ.L) : P(a, Σ)}`

*whose membership predicate `P` consults only `Σ.L` and query-data (never `Σ.M`, `Σ.C`, `Σ.E`, `Σ.R`):*

> `{a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}`

*Precondition: `Σ.L = Σ'.L` as partial functions (entails `dom(Σ.L) = dom(Σ'.L)` and `Σ.L(a) = Σ'.L(a)` for all `a ∈ dom(Σ.L)`).*

---

## F-CIL-perlink — PerLinkInvarianceUnderValuePreservation (SUB-LEMMA, lemma)

*For any `a` with `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`:*

- `matches(a, I, Σ) ⟺ matches(a, I, Σ')` for every `I ⊆ T`;
- for every slot constraint `(i, J)`, the per-link conjunct `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` evaluates identically at `Σ` and `Σ'`.

---

## F-PRES — PublishedFramePreservation (LEMMA, lemma)

*Every transition in `V_atomic ∖ {K.λ} = {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` and the composite `K.μ~` preserves the link store:*

> `dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))`

---

## F-INERT — LinkStoreInertPreservation (LEMMA, lemma)

*For every transition in `V_atomic ∪ {K.μ~} ∖ {K.λ}` and every `I ⊆ T`:*

> `findlinks(I, Σ) = findlinks(I, Σ')`

*The transitive closure over `→*` whose every atomic step is in `V_atomic ∖ {K.λ}` is handled by chaining.*

---

## F-LAMBDA — KλInducedIncrement (LEMMA, lemma)

*For a single-step transition `Σ → Σ'` produced by `K.λ` allocating a fresh link `ℓ_new` with endsets `(e₁, …, e_N)`, and any `I ⊆ T`:*

> `findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅)`

*The two parts are disjoint: K.λ's freshness precondition (ASN-0093) gives `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)`, hence `ℓ_new ∉ findlinks(I, Σ)`.*

---

## E-INV — CoveragePermanence (LEMMA, lemma)

*For fixed `I` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies:*

> `a ∈ dom(Σ'.L)` and `matches(a, I, Σ') ⟺ matches(a, I, Σ)`

*Keystone: LP13 (UnconditionalLinkPersistence, ASN-0098) gives `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` across `Σ →* Σ'`, hence arity equality `|Σ'.L(a)| = |Σ.L(a)|` and per-slot coverage equality `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`.*

---

## E-MONO — ExistenceMonotonicity (LEMMA, lemma)

*For fixed `I`:*

> `Σ →* Σ' ⟹ findlinks(I, Σ) ⊆ findlinks(I, Σ')`

---

## E-CONS — CreationConservation (LEMMA, lemma)

*For fixed `I`, the set difference `findlinks(I, Σ') ∖ findlinks(I, Σ)` over `Σ →* Σ'` consists of exactly those links created on that path whose stored value matches `I`.*

*Formally: for any `a ∈ findlinks(I, Σ') ∖ findlinks(I, Σ)`, it follows that `a ∉ dom(Σ.L)` (created after `Σ`); and conversely, any link created on the path with `matches(a, I, Σ')` lies in the difference. Creation is the sole source of change.*

---

## D-PRES — PresentTenseResolution (OBS, predicate)

*`image(W, d_q, Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `findlinks_disc` — can change while `dom(Σ.L)` is fixed.*

---

## D-NONMONO — DiscoveryNonMonotonicity (LEMMA, lemma)

*`findlinks_disc` is not monotone across `Σ →* Σ'`. By case analysis on the K-transition:*

- *K.μ⁺ or K.μ⁺_L on `d_q`*: `image(W, d_q, Σ) ⊆ image(W, d_q, Σ')` (F-IMG-MONO); K.μ⁺/K.μ⁺_L preserves `Σ.L` (F-PRES/F-INERT); hence:

  > `findlinks_disc(W, d_q, Σ) ⊆ findlinks_disc(W, d_q, Σ')`

- *K.μ⁻ on `d_q`*: `image(W, d_q, Σ') ⊆ image(W, d_q, Σ)` (F-IMG-CONTR); K.μ⁻ preserves `Σ.L` (F-PRES/F-INERT); hence:

  > `findlinks_disc(W, d_q, Σ') ⊆ findlinks_disc(W, d_q, Σ)`

- *K.μ~ on `d_q`*: K.μ~ preserves `Σ.L` (F-PRES/F-INERT); every motion of the discovery set comes through the image (F-IMG-SWING). When `π⁻¹(W) ∩ dom(Σ.M(d_q)) = W ∩ dom(Σ.M(d_q))`, image and discovery set are both invariant. When the image moves with `⊆`-comparable motion: F-IMONO applies and `findlinks_disc` moves monotonically. When the image moves with `⊆`-incomparable (lateral) motion: F-IMONO is unavailable and `findlinks_disc` is non-monotone.

- *Transitions not on `d_q`*: `image(W, d_q, Σ) = image(W, d_q, Σ')`; the result changes only if `K.λ` adds a matching link (F-LAMBDA).

---

## D-CWP — ContractionStabilityWP (LEMMA, lemma)

*Fix a K.μ⁻ contraction `Σ → Σ'` on the query document `d_q` with retention set `R = ⋃ {[S, 1, …, 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}` (ASN-0047), so that `enabled(K.μ⁻[d_q, R])` holds and `Σ'.M(d_q) = Σ.M(d_q) ↾ R`. Define:*

> `I_R ≡ {Σ.M(d_q)(v) : v ∈ W ∩ R}` *(the post-state image, expressed in pre-state terms)*
>
> `Δ ≡ image(W, d_q, Σ) ∖ I_R` *(the I-addresses dropped from the queried region)*

*The bridge: `image(W, d_q, Σ') = I_R` (since `dom(Σ'.M(d_q)) = R` and `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` on `v ∈ R`). Then:*

> `findlinks_disc(W, d_q, Σ') = findlinks_disc(W, d_q, Σ)`  *iff*  `findlinks(Δ, Σ) ⊆ findlinks(I_R, Σ)`

*Boundary case `R = ∅`: stability condition collapses to `findlinks_disc(W, d_q, Σ) = ∅`.*

*Both `I_R` and `Δ` are functions of the pre-state `Σ` and `R` alone; the biconditional is a precondition on `(Σ, R)` evaluable before the step.*

---

## D-ZERO — PresentNotHistorical (OBS, predicate)

*A discovery zero `findlinks_disc(W, d_q, Σ) = ∅` asserts that no link in `dom(Σ.L)` is presently reachable from `d_q`'s arrangement at `Σ`. It does not assert historical absence.*

*By contrast, an existence zero against fixed `I` certifies historical absence: by E-INV satisfaction against fixed `I` is per-link time-invariant, and by E-MONO the set is monotone, so `findlinks(I, Σ) = ∅` implies `findlinks(I, Σ₀) ⊆ findlinks(I, Σ) = ∅` along every path `Σ₀ →* Σ` — no link satisfying `I` was ever created.*
