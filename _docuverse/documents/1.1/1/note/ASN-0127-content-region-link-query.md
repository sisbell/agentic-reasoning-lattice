# ASN-0127: Content-Region Link Query

*The foundation algebra for "which links does this content region reach, and what stays stable as state evolves?"*

A reader looks at a stretch of arranged content and asks: *what connects to this from elsewhere?* The substrate question underneath this — independent of any reader-facing operation — is: given a region of V-positions in a document, what set of I-addresses does that region currently cover, and what comprehension over the link store does it induce? This note answers that — and only that.

The algebra factors cleanly through arrangement. The reader names a region in V-coordinates; the document's arrangement resolves that region to a set of I-addresses; the link store is then queried against those I-addresses. The two phases are independent — Phase 1 consults `Σ.M`, Phase 2 consults `Σ.L` — and the stability properties of the composite are determined by which state component each operation moves. The foundation supplies the named primitives, the keystone invariance meta-lemma, and the anchoring taxonomy that distinguishes count-and-set behavior depending on whether the reader's request is *fixed* in the permanent address space or *resolved* through a live arrangement.

## State and notation

Addresses are tumblers from `T` (ASN-0034), totally ordered under T1. We operate over the extended state `Σ = (C, L, E, M, R)` of ASN-0047: content store `C : T ⇀ Val` (append-only with immutable values, S0, ASN-0036), link store `L : T ⇀ Link` (append-only with immutable values, L12, finite at every reachable state, L-fin), entity set `E`, arrangement family `M(d) : T ⇀ T` for each `d ∈ dom(M)`, and provenance relation `R`. Links carry endset tuples `Σ.L(a) = (e₁, …, eₙ)` with `n ≥ 3` (L3); `coverage(e) ⊆ T` is the address set an endset denotes, a deterministic function of its spans (ASN-0043).

The K-transition vocabulary is ASN-0047's: `K.α` (content allocation), `K.δ` (entity/document registration), `K.λ` (link creation), `K.μ⁺` and `K.μ⁺_L` (content/link-subspace arrangement extension), `K.μ⁻` (arrangement contraction), `K.μ~` (reordering, a composite of K.μ⁻ + K.μ⁺), `K.ρ` (provenance). `K.λ` is the unique transition that modifies `Σ.L`.

## Phase 1: Region projection through arrangement

Given a document `d ∈ dom(Σ.M)` and a query region `R ⊆ T`, the document's current arrangement resolves the region to a set of I-addresses:

**F-IMG (ImageDefinition).** *For `d ∈ dom(Σ.M)` and `R ⊆ T`:*

> `image(R, d, Σ) ≡ {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}`

*For `d ∉ dom(Σ.M)`, `image(R, d, Σ)` is undefined.*

The intersection `R ∩ dom(Σ.M(d))` is load-bearing: V-positions named by `R` but absent from `d`'s arrangement contribute nothing, so the image fabricates no I-address absent from the arrangement. The image is a forward image of a partial function on its defined domain — a basic projection.

When `R` is a contiguous V-span in some subspace `S`, ASN-0058's mapping-block decomposition gives the image as a union of I-runs (B1+B2, ASN-0058). When `v ∈ R` has `subspace(v) = s_L`, S3★ (ASN-0047) routes `Σ.M(d)(v) ∈ dom(Σ.L)` and the image picks up a link address; endsets may reference any address in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target.

**F-IMG-MONO (ImageMonotonicityUnderArrangementExtension).** *If `Σ → Σ'` extends `Σ.M(d)` (a K.μ⁺ or K.μ⁺_L step that adds positions to `d`'s arrangement while agreeing on prior positions), then for every `R ⊆ T`:*

> `image(R, d, Σ) ⊆ image(R, d, Σ')`.

*Derivation. The extension frame (K.μ⁺/K.μ⁺_L, ASN-0047) gives `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))`. Take any `b ∈ image(R, d, Σ)`; by F-IMG, `b = Σ.M(d)(v)` for some `v ∈ R ∩ dom(Σ.M(d))`. Then `v ∈ R ∩ dom(Σ'.M(d))` (prior domain is included) and `Σ'.M(d)(v) = Σ.M(d)(v) = b` (agreement on the prior domain), so `b ∈ image(R, d, Σ')`.*

**F-IMG-CONTR (ImageContractionUnderArrangementContraction).** *If `Σ → Σ'` contracts `Σ.M(d)` (a K.μ⁻ step), then:*

> `image(R, d, Σ') ⊆ image(R, d, Σ)`.

*Derivation. Symmetric to F-IMG-MONO. The contraction frame (K.μ⁻, ASN-0047) gives `dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ'.M(d))` (retained-domain agreement). Take any `b ∈ image(R, d, Σ')`; then `b = Σ'.M(d)(v)` for some `v ∈ R ∩ dom(Σ'.M(d))`, whence `v ∈ R ∩ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) = b`, so `b ∈ image(R, d, Σ)`.*

**F-IMG-SWING (ImageSwingUnderReorder).** *If `Σ → Σ'` is a K.μ~ reorder of `d`'s arrangement with witnessing bijection `π`, then `image(R, d, Σ') = {Σ.M(d)(u) : u ∈ π⁻¹(R) ∩ dom(Σ.M(d))}`. The total range is preserved (LP11, ASN-0098: `ran(Σ'.M(d)) = ran(Σ.M(d))`) but the forward image of a fixed sub-region `R` may change membership; and when `Σ.M(d)` is non-injective — content sharing (M13/M14, ASN-0058) — the image may additionally gain or lose members (change cardinality). Under injective `Σ.M(d)` only membership change is realizable.*

*Derivation. K.μ~-FIX (ASN-0047) gives `dom(Σ'.M(d)) = dom(Σ.M(d))`, so the witness `π : dom(Σ.M(d)) → dom(Σ'.M(d))` is a bijection of `dom(Σ.M(d))` onto itself, satisfying the bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)` for every `u ∈ dom(Σ.M(d))`. Unfolding F-IMG at `Σ'` and reindexing each `v = π(u)`: since `π` ranges over all of `dom(Σ'.M(d))`, `v ∈ R ⟺ u ∈ π⁻¹(R)`, and `Σ'.M(d)(v) = Σ'.M(d)(π(u)) = Σ.M(d)(u)`, whence `image(R, d, Σ') = {Σ'.M(d)(v) : v ∈ R ∩ dom(Σ'.M(d))} = {Σ.M(d)(u) : u ∈ π⁻¹(R) ∩ dom(Σ.M(d))}`. That `π` need not fix `R` setwise is why the image membership can change. The cardinality, however, is not free to move under an arbitrary reorder: `π` is a bijection on `dom(Σ.M(d))`, so `|π⁻¹(R) ∩ dom(Σ.M(d))| = |R ∩ dom(Σ.M(d))|` always. When `Σ.M(d)` is injective, these equal-size index sets carry to equal-size images — the image can only change membership, never gain or lose. A genuine cardinality change therefore requires `Σ.M(d)` non-injective, i.e. content sharing (M13/M14, ASN-0058). Witness: with `Σ.M(d) : v₁ ↦ a, v₂ ↦ a, v₃ ↦ b` (so `a` is shared) and `R = {v₁, v₂}`, `image(R, d, Σ) = {a}`; the reorder `π` given by `π(v₁) = v₁, π(v₂) = v₃, π(v₃) = v₂` yields `Σ'.M(d) : v₁ ↦ a, v₂ ↦ b, v₃ ↦ a`, and `π⁻¹(R) = {v₁, v₃}` gives `image(R, d, Σ') = {a, b}` — a gain from one member to two, with `ran(Σ'.M(d)) = ran(Σ.M(d)) = {a, b}` preserved throughout.*

## Phase 2: Per-link matching

Given an I-address set `I ⊆ T`, the per-link relevance test names which links the set reaches:

**F-MATCH (MatchPredicate).** *For `a ∈ dom(Σ.L)` and `I ⊆ T`:*

> `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`.

A link matches the I-address set when *some* slot's coverage meets it. The existential over slots is essential: a link with a multi-slot endset that meets `I` in any one slot is matched.

**F-FIND (FindPrimitive).** *The bare comprehension:*

> `findlinks(I, Σ) ≡ {a ∈ dom(Σ.L) : matches(a, I, Σ)}`.

**F-UDIST (UnionDistributivity).** *For all I-address sets `I₁, I₂ ⊆ T` — no disjointness required:*

> `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`.

*Derivation. Fix `a ∈ dom(Σ.L)` and unfold the match predicate at `I₁ ∪ I₂`: `matches(a, I₁ ∪ I₂, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅)`. Intersection distributes over union — `coverage(Σ.L(a).eᵢ) ∩ (I₁ ∪ I₂) = (coverage(Σ.L(a).eᵢ) ∩ I₁) ∪ (coverage(Σ.L(a).eᵢ) ∩ I₂)` — and a union is non-empty iff one of its parts is, so the slot test becomes `coverage(Σ.L(a).eᵢ) ∩ I₁ ≠ ∅ ∨ coverage(Σ.L(a).eᵢ) ∩ I₂ ≠ ∅`. The existential distributes over this disjunction, giving `matches(a, I₁, Σ) ∨ matches(a, I₂, Σ)`. None of these steps consults `I₁ ∩ I₂`, so the law holds for arbitrary `I₁, I₂` — this is union-distribution of a set-valued operation, not a measure-style additive law over disjoint pieces. Set-builder over the disjunction splits the comprehension into `findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`. The unrestricted form is what Phase 1 needs: images of two disjoint V-regions need not be disjoint I-sets, since distinct V-positions may resolve to a shared I-address under content sharing (M13/M14, ASN-0058).*

**F-IMONO (FindMonotonicityInI — corollary of F-UDIST).** *For all I-address sets `I' ⊆ I ⊆ T`:*

> `findlinks(I', Σ) ⊆ findlinks(I, Σ)`.

*Derivation. Write `I = I' ∪ (I ∖ I')` and apply F-UDIST: `findlinks(I, Σ) = findlinks(I', Σ) ∪ findlinks(I ∖ I', Σ) ⊇ findlinks(I', Σ)`. Monotonicity in the I-argument is thus immediate from union-distributivity; it is the fact a shrinking resolved request needs in the discovery analysis (D-NONMONO).*

## The two-phase composite

**F-V (TwoPhaseFactoring).** *The two-phase combinator composes the projection with the per-link comprehension. For `d ∈ dom(Σ.M)`, `R ⊆ T`:*

> `findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)`,

*undefined when `d ∉ dom(Σ.M)`.*

This is a *definition*, not a derived theorem. The factoring is what makes the stability analysis tractable: each phase consults only one of `Σ.M(d)` and `Σ.L`, so the composite's stability decomposes accordingly.

**F-VDIST (RegionUnionDistributivity).** *For `d ∈ dom(Σ.M)` and any V-regions `R₁, R₂ ⊆ T` — no disjointness required:*

> `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)`.

*Derivation. The image is a forward image of the partial function `Σ.M(d)`, and forward image distributes over union of its argument. Unfolding F-IMG, `image(R₁ ∪ R₂, d, Σ) = {Σ.M(d)(v) : v ∈ (R₁ ∪ R₂) ∩ dom(Σ.M(d))}`; since `(R₁ ∪ R₂) ∩ dom(Σ.M(d)) = (R₁ ∩ dom(Σ.M(d))) ∪ (R₂ ∩ dom(Σ.M(d)))`, the image splits as `image(R₁, d, Σ) ∪ image(R₂, d, Σ)`. Then `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks(image(R₁ ∪ R₂, d, Σ), Σ) = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ) = {F-UDIST} findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)`. The middle step is exactly where F-UDIST must be unrestricted: even when `R₁ ∩ R₂ = ∅`, the two images may overlap — distinct V-positions can resolve to a shared I-address under content sharing (M13/M14, ASN-0058) — so a disjointness-restricted union law would not close this composition. F-VDIST is the Phase-1 payoff F-UDIST exists to enable: image distributes over V-region union, and union-distributivity over the resulting (possibly overlapping) I-sets carries the comprehension through.*

## The stability keystone

The single result that propagates to every preservation claim in the rest of the note:

**F-CIL (ComprehensionInvariantUnderΣL — meta-lemma).** *If `Σ.L = Σ'.L` as partial functions, then for every comprehension*

> `{a ∈ dom(Σ.L) : P(a, Σ)}`

*whose membership predicate `P` consults only `Σ.L` and query-data (never `Σ.M`, `Σ.C`, `Σ.E`, `Σ.R`):*

> `{a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}`.

*Derivation chain. `Σ.L = Σ'.L` gives `dom(Σ.L) = dom(Σ'.L)` and per-link value equality `Σ.L(a) = Σ'.L(a)`. Component-wise tuple equality on link values (L6) gives `|Σ.L(a)| = |Σ'.L(a)|` and per-slot endset equality `Σ.L(a).eᵢ = Σ'.L(a).eᵢ`. Coverage is a deterministic function of its endset argument, so per-slot coverage agrees. Any membership predicate built from these evaluates identically at the two states; set extensionality closes the equality.*

A weaker per-link form supports the inductive step for K.λ:

**F-CIL-perlink (PerLinkInvarianceUnderValuePreservation — sub-lemma).** *For any `a` with `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`:*

- *`matches(a, I, Σ) ⟺ matches(a, I, Σ')` for every `I ⊆ T`;*
- *for every slot constraint `(i, J)`, the per-link conjunct `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` evaluates identically at `Σ` and `Σ'`.*

## Operational consequences

The keystone meta-lemma turns the question "which transitions preserve the result?" into the question "which transitions preserve `Σ.L`?"

**F-PRES (PublishedFramePreservation).** *Every transition in `V_atomic ∖ {K.λ} = {K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` and the composite `K.μ~` preserves the link store: `dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))`. The atomic operations publish `L' = L` in their effect frame (ASN-0047). The composite `K.μ~` is K.μ⁻ + K.μ⁺ and preserves `Σ.L` by composition.*

**F-INERT (LinkStoreInertPreservation).** *For every transition in `V_atomic ∪ {K.μ~} ∖ {K.λ}` and every `I ⊆ T`:*

> `findlinks(I, Σ) = findlinks(I, Σ')`.

*F-PRES gives `Σ.L = Σ'.L`; F-CIL forces the equality. The transitive closure over `→*` whose every atomic step is in `V_atomic ∖ {K.λ}` is handled by chaining.*

**F-LAMBDA (KλInducedIncrement).** *For a single-step transition `Σ → Σ'` produced by `K.λ` allocating a fresh link `ℓ_new` with endsets `(e₁, …, e_N)`, and any `I ⊆ T`:*

> `findlinks(I, Σ') = findlinks(I, Σ) ⊎ ({ℓ_new} if matches(ℓ_new, I, Σ') else ∅)`.

*The two parts are disjoint: K.λ's freshness precondition (ASN-0093) gives `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)`, hence `ℓ_new ∉ findlinks(I, Σ)`. The prior-key contribution is preserved by F-CIL-perlink applied at each `a ∈ dom(Σ.L)`; the fresh-key contribution is the singleton `{ℓ_new}` exactly when the match holds at the new state.*

`K.λ` is therefore the unique single-step source of change in `findlinks(I, Σ)` for *fixed* `I` — the existence-anchored result — and its effect there is fully characterized. The scope is essential: this is a statement about the fixed-`I` comprehension that F-INERT and F-LAMBDA range over, not about the discovery-anchored `findlinks_V`/`findlinks_disc` over a live arrangement. For the latter, K.μ⁺, K.μ⁻, and K.μ~ on the query document all move the result with no link created or retracted, because they move the resolved I-argument rather than `Σ.L` (D-NONMONO).

## Anchoring: existence vs discovery

The crux of how a caller experiences `findlinks_V`'s behavior is *how the I-address argument is obtained*, because that choice fixes whether the answer is a stable property of the permanent store or a live reading of the current arrangement.

### Existence anchoring

The request is given directly as a fixed I-address set `I ⊆ T` in the permanent address space. The match predicate then turns only on `coverage(Σ.L(a).eᵢ) ∩ I`, and coverage is invariant across all transitions (LP3★, ASN-0098).

**E-INV (CoveragePermanence).** *For fixed `I` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies `matches(a, I, Σ') ⟺ matches(a, I, Σ)`.*

**E-MONO (ExistenceMonotonicity).** *For fixed `I`, `Σ →* Σ' ⟹ findlinks(I, Σ) ⊆ findlinks(I, Σ')`.*

*The store grows across the transitive closure (Store Monotonicity, ASN-0098), coverage is invariant (E-INV), so the matching set only gains members.*

**E-CONS (CreationConservation).** *For fixed `I`, the set difference `findlinks(I, Σ') ∖ findlinks(I, Σ)` over `Σ →* Σ'` consists of exactly those links created on that path whose stored value matches `I`.*

*The "exactly" is a two-direction claim, and the exclusion direction is the one that needs E-INV. Take any `a ∈ findlinks(I, Σ') ∖ findlinks(I, Σ)`. Either `a ∉ dom(Σ.L)` or `a ∈ dom(Σ.L)`. Suppose `a ∈ dom(Σ.L)`: then E-INV gives `matches(a, I, Σ) ⟺ matches(a, I, Σ')`; from `a ∈ findlinks(I, Σ')` we have `matches(a, I, Σ')`, hence `matches(a, I, Σ)`, and together with `a ∈ dom(Σ.L)` this places `a ∈ findlinks(I, Σ)` — contradicting `a ∉ findlinks(I, Σ)`. So the second case is impossible: only `a ∉ dom(Σ.L)` survives, and such an `a` is a link created somewhere on the path `Σ →* Σ'` (it entered `dom(Σ'.L)` after `Σ`), matching at `Σ'` by its membership in `findlinks(I, Σ')`. Conversely, any link created on the path whose value matches `I` at `Σ'` lies in `findlinks(I, Σ')` and not in `findlinks(I, Σ)` (it was not yet a key at `Σ`), so it sits in the difference. Creation is therefore the sole source of change.*

### Discovery anchoring

The request is resolved through a querying document's current arrangement. Given `d_q ∈ dom(Σ.M)` and a query V-region `W ⊆ T`, the I-address argument is the state-resolved image:

> `findlinks_disc(W, d_q, Σ) ≡ findlinks(image(W, d_q, Σ), Σ)` = `findlinks_V(W, d_q, Σ)`.

**D-PRES (PresentTenseResolution).** *`image(W, d_q, Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `findlinks_disc` — can change while `dom(Σ.L)` is fixed.*

**D-NONMONO (DiscoveryNonMonotonicity).** *`findlinks_disc` is not monotone across `Σ →* Σ'`. By case analysis on the K-transition:*

- *K.μ⁺ or K.μ⁺_L on `d_q`*: the arrangement extends, so `image(W, d_q, Σ) ⊆ image(W, d_q, Σ')` (F-IMG-MONO); new I-addresses falling in `W`'s positions can add new link matches.
- *K.μ⁻ on `d_q`*: the arrangement contracts, so `image(W, d_q, Σ') ⊆ image(W, d_q, Σ)` (F-IMG-CONTR); the resolved request can only shrink, and since `findlinks` is monotone in its I-argument (F-IMONO), the discovery set can only shrink with it: `findlinks_disc(W, d_q, Σ') ⊆ findlinks_disc(W, d_q, Σ)`.
- *K.μ~ on `d_q`*: the witnessing bijection can carry a position with otherwise-unshared image across the `W` boundary, so `findlinks_disc` may rise or fall (F-IMG-SWING), with no link created or retracted.
- *Transitions not on `d_q`*: `image(W, d_q, Σ) = image(W, d_q, Σ')`; the result changes only if `K.λ` adds a matching link (F-LAMBDA).

**D-ZERO (PresentNotHistorical).** *A discovery zero `findlinks_disc(W, d_q, Σ) = ∅` asserts that no link in `dom(Σ.L)` is presently reachable from `d_q`'s arrangement at `Σ`. It does not assert historical absence. A link whose endpoints have left `d_q`'s consulted arrangement merely ceases to be reachable through it (its image drops by D-NONMONO), so it leaves the discovery set while remaining a permanent member of the store (L12).*

*By contrast, an existence zero against fixed `I` certifies historical absence: by E-INV satisfaction against fixed `I` is per-link time-invariant, and by E-MONO the set is monotone, so `findlinks(I, Σ) = ∅` implies `findlinks(I, Σ₀) ⊆ findlinks(I, Σ) = ∅` along every path `Σ₀ →* Σ` — no link satisfying `I` was ever created.*

## Worked illustration

Take a single document `d` with three text positions `v_1, v_2, v_3` mapping to `a_1, a_2, a_3` respectively, and two stored links, each a conforming triple (L3) with a non-empty type endset at slot 3: `L_1 = ({a_1}, {a_3}, Θ)` and `L_2 = ({a_2}, {a_3}, Θ)`, where the type endset `Θ = {a_θ}` references a type address `a_θ ∉ {a_1, a_2, a_3}`.

*Phase 1.* `R = {v_1, v_2}` yields `image(R, d, Σ) = {a_1, a_2}`.

*Phase 2.* `findlinks({a_1, a_2}, Σ)` — both links match via slot 1 (`L_1` via `e₁ ∩ {a_1} = {a_1}`; `L_2` via `e₁ ∩ {a_2} = {a_2}`). The other slots do not fire on this query: `e₂ ∩ {a_1, a_2} = {a_3} ∩ {a_1, a_2} = ∅`, and the type slot `e₃ ∩ {a_1, a_2} = {a_θ} ∩ {a_1, a_2} = ∅` since `a_θ ∉ {a_1, a_2, a_3}`. The match is carried entirely by slot 1, and the result is `{L_1, L_2}`.

*Stability under K.α* — allocating fresh content `a_4` adds nothing to `image(R, d, Σ)` (V-positions in `R` are unchanged); F-INERT carries the result. ✓

*Stability under K.μ⁻* — with `v_1 = [1,1], v_2 = [1,2], v_3 = [1,3]`, K.μ⁻ retains an initial segment `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ n'_{s_C}}` of the sequential positions (D-SEQ★), never a mid-sequence position. Retaining `n'_{s_C} = 1` keeps only the prefix `{v_1}`, removing both `v_2` and `v_3`. Then `R ∩ dom(Σ'.M(d)) = {v_1, v_2} ∩ {v_1} = {v_1}`, so `image(R, d, Σ')` shrinks to `{a_1}` and `findlinks_disc(R, d, Σ')` shrinks to `{L_1}`. ✓ D-NONMONO contraction clause.

*K.λ adding L_3* `= ({a_1}, ∅, Θ)` (a conforming triple; the empty to-endset is admissible, the type slot `Θ = {a_θ} ≠ ∅` is mandatory): F-LAMBDA gives `findlinks({a_1, a_2}, Σ') = {L_1, L_2, L_3}` — the prior result plus the new link's match, which fires via slot 1 (`e₁ ∩ {a_1} = {a_1}`).

*Existence vs discovery zero.* Suppose K.μ⁻ removes all of `v_1, v_2, v_3`. Then `image(R, d, Σ') = ∅`, `findlinks_disc(R, d, Σ') = ∅` (discovery zero — present absence). But `findlinks({a_1, a_2}, Σ') = {L_1, L_2}` (existence non-zero — the links persist in the store, their coverage unchanged by D-NONMONO and F-PRES).

## Properties established

| Claim | Statement | Role |
|-------|-----------|------|
| F-IMG | `image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}` | Phase 1 primitive |
| F-IMG-MONO | image grows under K.μ⁺/K.μ⁺_L | image stability |
| F-IMG-CONTR | image shrinks under K.μ⁻ | image stability |
| F-IMG-SWING | image may move under K.μ~ | image instability |
| F-MATCH | match predicate (existential over slots) | Phase 2 primitive |
| F-FIND | comprehension primitive `findlinks(I, Σ)` | Phase 2 primitive |
| F-UDIST | `findlinks(I₁ ∪ I₂) = findlinks(I₁) ∪ findlinks(I₂)` for all `I₁, I₂` | Phase 2 algebra |
| F-IMONO | `I' ⊆ I ⟹ findlinks(I') ⊆ findlinks(I)` | Phase 2 algebra (corollary of F-UDIST) |
| F-V | `findlinks_V(R, d, Σ) = findlinks(image(R, d, Σ), Σ)` | two-phase combinator (definition) |
| F-VDIST | `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)` | composite algebra (Phase-1 payoff of F-UDIST) |
| F-CIL | comprehension over `dom(Σ.L)` with `Σ.L`-only predicate is `Σ.L`-stable | keystone meta-lemma |
| F-CIL-perlink | per-link version under per-link value preservation | sub-lemma |
| F-PRES | `V_atomic ∖ {K.λ}` and `K.μ~` preserve `Σ.L` | transition vocabulary |
| F-INERT | preservation ⟹ result invariance | operational consequence |
| F-LAMBDA | `K.λ` increments result by the newly matching singleton (or nothing) | unique store-modifying op |
| E-INV | coverage permanence (per-link, against fixed `I`) | existence anchoring |
| E-MONO | existence-anchored result is `→*`-monotone | existence anchoring |
| E-CONS | path-level set difference is exactly matching creations | existence anchoring |
| D-PRES | image is a live reading of `Σ.M(d_q)` | discovery anchoring |
| D-NONMONO | discovery-anchored result is non-monotone (K-case analysis) | discovery anchoring |
| D-ZERO | discovery zero ≠ historical absence | discovery anchoring |

## Open questions

What is the relationship between `findlinks_V` and a content-keyed query that names addresses through `Σ.C` rather than `Σ.M`? Both are content-region queries in a broad sense; this note treats only the arrangement-mediated case.

Under what filter-set constraints over `findlinks` does union-distributivity (F-UDIST) preserve into the filtered form, and where does the per-slot universal vs the per-link existential distinction matter for compositional reasoning?

What conditions on `R` and on a transition `Σ → Σ'` are jointly sufficient to preserve `findlinks_V(R, d, Σ) = findlinks_V(R, d, Σ')` — i.e., the weakest precondition for discovery-anchored stability under a specific transition?

How does this foundation compose with ASN-0098's link projection displacement? `image()` and the LP** results both consult `Σ.M`; the natural composition is "project a link through arrangement, then ask if the projection meets a content region" — but the operational composition is not addressed here.
