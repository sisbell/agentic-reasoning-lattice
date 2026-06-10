# ASN-0127: Content-Region Link Query

*The foundation algebra for "which links does this content region reach, and what stays stable as state evolves?"*

A reader looks at a stretch of arranged content and asks: *what connects to this from elsewhere?* The substrate question underneath this — independent of any reader-facing operation — is: given a region of V-positions in a document, what set of I-addresses does that region currently cover, and what comprehension over the link store does it induce? This note answers that — and only that.

The algebra factors cleanly through arrangement. The reader names a region in V-coordinates; the document's arrangement resolves that region to a set of I-addresses; the link store is then queried against those I-addresses. The two phases are independent — Phase 1 consults `Σ.M`, Phase 2 consults `Σ.L` — and the stability properties of the composite are determined by which state component each operation moves. The foundation supplies the named primitives, the keystone invariance meta-lemma, and the anchoring taxonomy that distinguishes count-and-set behavior depending on whether the reader's request is *fixed* in the permanent address space or *resolved* through a live arrangement.

## State and notation

Addresses are tumblers from `T` (ASN-0034), totally ordered under T1. We operate over the extended state `Σ = (C, L, E, M, R)` of ASN-0047: content store `C : T ⇀ Val` (append-only with immutable values, S0, ASN-0036), link store `L : T ⇀ Link` (append-only with immutable values, L12, finite at every reachable state, L-fin), entity set `E`, arrangement family `M(d) : T ⇀ T` for each `d ∈ dom(M)`, and provenance relation `R`. Links carry endset tuples `Σ.L(a) = (e₁, …, eₙ)` with `n ≥ 3` (L3); `coverage(e) ⊆ T` is the address set an endset denotes, a deterministic function of its spans (ASN-0043).

The K-transition vocabulary is ASN-0047's. The *atomic* vocabulary is `V_atomic = {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` — `K.α` (content allocation), `K.δ` (entity/document registration), `K.λ` (link creation), `K.μ⁺` and `K.μ⁺_L` (content/link-subspace arrangement extension), `K.μ⁻` (arrangement contraction), `K.ρ` (provenance) — with `K.μ~` (reordering) the named composite of K.μ⁻ + K.μ⁺ (ASN-0047), not itself atomic. `K.λ` is the unique transition that modifies `Σ.L`.

## Phase 1: Region projection through arrangement

Given a document `d ∈ dom(Σ.M)` and a query region `W ⊆ T`, the document's current arrangement resolves the region to a set of I-addresses:

**F-IMG (ImageDefinition).** *For `d ∈ dom(Σ.M)` and `W ⊆ T`:*

> `image(W, d, Σ) ≡ {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`

*For `d ∉ dom(Σ.M)`, `image(W, d, Σ)` is undefined.*

*Degenerate cases.* `image(∅, d, Σ) = ∅` (empty region); and `image(W, d, Σ) = ∅` whenever `W ∩ dom(Σ.M(d)) = ∅` — in particular for a freshly registered document whose arrangement is empty (`dom(Σ.M(d)) = ∅`, the K.δ `Document` post-state, ASN-0047), where the image is `∅` for every `W`. This matches the boundary behavior ASN-0098 pins down for the analogous primitive `project`: `project(∅, d, Σ) = ∅`, and `project(e, d, Σ) = ∅` whenever `dom(Σ.M(d)) = ∅`.

The intersection `W ∩ dom(Σ.M(d))` is load-bearing: V-positions named by `W` but absent from `d`'s arrangement contribute nothing, so the image fabricates no I-address absent from the arrangement. The image is a forward image of a partial function on its defined domain — a basic projection.

When `W` is a contiguous V-span in some subspace `S`, the image is a union of I-runs delivered by ASN-0058's *restriction* decomposition. The restriction `f = Σ.M(d)|W` has induced domain `W ∩ dom(Σ.M(d))` confined to the single subspace `S`, so C1a (RestrictionDecomposition, ASN-0058) supplies a unique maximally merged decomposition of `f` into *W-confined* blocks `βⱼ = (vⱼ, aⱼ, nⱼ)`: their V-extents partition `W ∩ dom(Σ.M(d))` and the per-block consistency `f(vⱼ + k) = aⱼ + k` makes each I-extent the contiguous run `{aⱼ + k : 0 ≤ k < nⱼ}`, so `image(W, d, Σ)` is exactly the union of these I-extents. The restriction is load-bearing: blocks of the *full* arrangement `Σ.M(d)` (B1–B3, ASN-0058, quantified over all of `dom(Σ.M(d))`) may straddle `W`'s boundary, and their full I-extents `I(βⱼ)` would overstate the image, which is the union of the W-restricted sub-runs `{Σ.M(d)(v) : v ∈ V(βⱼ) ∩ W}` — exactly what C1a's W-confined blocks compute. When `v ∈ W` has `subspace(v) = s_L`, S3★ (ASN-0047) routes `Σ.M(d)(v) ∈ dom(Σ.L)` and the image picks up a link address; endsets may reference any address in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target.

**F-IMG-MONO (ImageMonotonicityUnderArrangementExtension).** *If `Σ → Σ'` extends `Σ.M(d)` (a K.μ⁺ or K.μ⁺_L step that adds positions to `d`'s arrangement while agreeing on prior positions), then for every `W ⊆ T`:*

> `image(W, d, Σ) ⊆ image(W, d, Σ')`.

*Derivation. The extension frame (K.μ⁺/K.μ⁺_L, ASN-0047) gives `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))`. Take any `b ∈ image(W, d, Σ)`; by F-IMG, `b = Σ.M(d)(v)` for some `v ∈ W ∩ dom(Σ.M(d))`. Then `v ∈ W ∩ dom(Σ'.M(d))` (prior domain is included) and `Σ'.M(d)(v) = Σ.M(d)(v) = b` (agreement on the prior domain), so `b ∈ image(W, d, Σ')`.*

**F-IMG-CONTR (ImageContractionUnderArrangementContraction).** *If `Σ → Σ'` contracts `Σ.M(d)` (a K.μ⁻ step), then:*

> `image(W, d, Σ') ⊆ image(W, d, Σ)`.

*Derivation. Symmetric to F-IMG-MONO. The contraction frame (K.μ⁻, ASN-0047) gives `dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ'.M(d))` (retained-domain agreement). Take any `b ∈ image(W, d, Σ')`; then `b = Σ'.M(d)(v)` for some `v ∈ W ∩ dom(Σ'.M(d))`, whence `v ∈ W ∩ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) = b`, so `b ∈ image(W, d, Σ)`.*

**F-IMG-SWING (ImageSwingUnderReorder).** *If `Σ → Σ'` is a K.μ~ reorder of `d`'s arrangement with witnessing bijection `π`, then `image(W, d, Σ') = {Σ.M(d)(u) : u ∈ π⁻¹(W) ∩ dom(Σ.M(d))}`. The total range is preserved (LP11, ASN-0098: `ran(Σ'.M(d)) = ran(Σ.M(d))`) but the forward image of a fixed sub-region `W` may change membership; and when `Σ.M(d)` is non-injective — content sharing (M13/M14, ASN-0058) — the image may additionally gain or lose members (change cardinality). Under injective `Σ.M(d)` only membership change is realizable.*

*Derivation. K.μ~-FIX (ASN-0047) gives `dom(Σ'.M(d)) = dom(Σ.M(d))`, so the witness `π : dom(Σ.M(d)) → dom(Σ'.M(d))` is a bijection of `dom(Σ.M(d))` onto itself, satisfying the bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)` for every `u ∈ dom(Σ.M(d))`. Unfolding F-IMG at `Σ'` and reindexing each `v = π(u)`: since `π` ranges over all of `dom(Σ'.M(d))`, `v ∈ W ⟺ u ∈ π⁻¹(W)`, and `Σ'.M(d)(v) = Σ'.M(d)(π(u)) = Σ.M(d)(u)`, whence `image(W, d, Σ') = {Σ'.M(d)(v) : v ∈ W ∩ dom(Σ'.M(d))} = {Σ.M(d)(u) : u ∈ π⁻¹(W) ∩ dom(Σ.M(d))}`. That `π` need not fix `W` setwise is why the image membership can change. The cardinality, however, is not free to move under an arbitrary reorder: `π` is a bijection on `dom(Σ.M(d))`, so `|π⁻¹(W) ∩ dom(Σ.M(d))| = |W ∩ dom(Σ.M(d))|` always. When `Σ.M(d)` is injective, these equal-size index sets carry to equal-size images — the image can only change membership, never gain or lose. *Injective witness:* with `Σ.M(d) : v₁ ↦ a, v₂ ↦ b` (injective, `a ≠ b`) and `W = {v₁}`, `image(W, d, Σ) = {a}`; the transposition reorder `π = (v₁ v₂)` yields `Σ'.M(d) : v₁ ↦ b, v₂ ↦ a` and `π⁻¹(W) = {v₂}`, so `image(W, d, Σ') = {b}` — the same cardinality, membership moved. A genuine cardinality change therefore requires `Σ.M(d)` non-injective, i.e. content sharing (M13/M14, ASN-0058). *Non-injective witness:* with `Σ.M(d) : v₁ ↦ a, v₂ ↦ a, v₃ ↦ b` (so `a` is shared) and `W = {v₁, v₂}`, `image(W, d, Σ) = {a}`; the reorder `π` given by `π(v₁) = v₁, π(v₂) = v₃, π(v₃) = v₂` yields `Σ'.M(d) : v₁ ↦ a, v₂ ↦ b, v₃ ↦ a`, and `π⁻¹(W) = {v₁, v₃}` gives `image(W, d, Σ') = {a, b}` — a gain from one member to two, with `ran(Σ'.M(d)) = ran(Σ.M(d)) = {a, b}` preserved throughout.*

## Phase 2: Per-link matching

Given an I-address set `I ⊆ T`, the per-link relevance test names which links the set reaches:

**F-MATCH (MatchPredicate).** *For `a ∈ dom(Σ.L)` and `I ⊆ T`:*

> `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`.

A link matches the I-address set when *some* slot's coverage meets it. The existential over slots is essential: a link with a multi-slot endset that meets `I` in any one slot is matched.

**F-FIND (FindPrimitive).** *The bare comprehension:*

> `findlinks(I, Σ) ≡ {a ∈ dom(Σ.L) : matches(a, I, Σ)}`.

*Degenerate case.* `findlinks(∅, Σ) = ∅`: for every `a ∈ dom(Σ.L)` and every slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ∅ = ∅`, so F-MATCH's slot existential has no non-empty intersection to witness and `matches(a, ∅, Σ)` is false; the comprehension therefore collects no link. The empty I-argument is exactly the Phase-2 input produced by an empty Phase-1 image (see F-V).

**F-UDIST (UnionDistributivity).** *For all I-address sets `I₁, I₂ ⊆ T` — no disjointness required:*

> `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`.

*Derivation. Fix `a ∈ dom(Σ.L)` and unfold the match predicate at `I₁ ∪ I₂`: `matches(a, I₁ ∪ I₂, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ (I₁ ∪ I₂) ≠ ∅)`. Intersection distributes over union — `coverage(Σ.L(a).eᵢ) ∩ (I₁ ∪ I₂) = (coverage(Σ.L(a).eᵢ) ∩ I₁) ∪ (coverage(Σ.L(a).eᵢ) ∩ I₂)` — and a union is non-empty iff one of its parts is, so the slot test becomes `coverage(Σ.L(a).eᵢ) ∩ I₁ ≠ ∅ ∨ coverage(Σ.L(a).eᵢ) ∩ I₂ ≠ ∅`. The existential distributes over this disjunction, giving `matches(a, I₁, Σ) ∨ matches(a, I₂, Σ)`. None of these steps consults `I₁ ∩ I₂`, so the law holds for arbitrary `I₁, I₂` — this is union-distribution of a set-valued operation, not a measure-style additive law over disjoint pieces. Set-builder over the disjunction splits the comprehension into `findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)`. The unrestricted form is what Phase 1 needs: images of two disjoint V-regions need not be disjoint I-sets, since distinct V-positions may resolve to a shared I-address under content sharing (M13/M14, ASN-0058).*

**F-IMONO (FindMonotonicityInI — corollary of F-UDIST).** *For all I-address sets `I' ⊆ I ⊆ T`:*

> `findlinks(I', Σ) ⊆ findlinks(I, Σ)`.

*Derivation. Write `I = I' ∪ (I ∖ I')` and apply F-UDIST: `findlinks(I, Σ) = findlinks(I', Σ) ∪ findlinks(I ∖ I', Σ) ⊇ findlinks(I', Σ)`. Monotonicity in the I-argument is thus immediate from union-distributivity; it is the fact a shrinking resolved request needs in the discovery analysis (D-NONMONO).*

## The two-phase composite

**F-V (TwoPhaseFactoring).** *The two-phase combinator composes the projection with the per-link comprehension. For `d ∈ dom(Σ.M)`, `W ⊆ T`:*

> `findlinks_V(W, d, Σ) ≡ findlinks(image(W, d, Σ), Σ)`,

*undefined when `d ∉ dom(Σ.M)`. Degenerate case: `findlinks_V(W, d, Σ) = ∅` whenever `image(W, d, Σ) = ∅` — in particular for `W = ∅`, for any `W` with `W ∩ dom(Σ.M(d)) = ∅`, and for a freshly registered `d` with empty arrangement — since `findlinks(∅, Σ) = ∅` (F-FIND). This is the composite reading of the ASN-0098 `project` boundary precedent: an empty resolved region induces the empty comprehension.*

This is a *definition*, not a derived theorem. The factoring is what makes the stability analysis tractable: each phase consults only one of `Σ.M(d)` and `Σ.L`, so the composite's stability decomposes accordingly.

**F-VDIST (RegionUnionDistributivity).** *For `d ∈ dom(Σ.M)` and any V-regions `W₁, W₂ ⊆ T` — no disjointness required:*

> `findlinks_V(W₁ ∪ W₂, d, Σ) = findlinks_V(W₁, d, Σ) ∪ findlinks_V(W₂, d, Σ)`.

*Derivation. The image is a forward image of the partial function `Σ.M(d)`, and forward image distributes over union of its argument. Unfolding F-IMG, `image(W₁ ∪ W₂, d, Σ) = {Σ.M(d)(v) : v ∈ (W₁ ∪ W₂) ∩ dom(Σ.M(d))}`; since `(W₁ ∪ W₂) ∩ dom(Σ.M(d)) = (W₁ ∩ dom(Σ.M(d))) ∪ (W₂ ∩ dom(Σ.M(d)))`, the image splits as `image(W₁, d, Σ) ∪ image(W₂, d, Σ)`. Then `findlinks_V(W₁ ∪ W₂, d, Σ) = findlinks(image(W₁ ∪ W₂, d, Σ), Σ) = findlinks(image(W₁, d, Σ) ∪ image(W₂, d, Σ), Σ) = {F-UDIST} findlinks(image(W₁, d, Σ), Σ) ∪ findlinks(image(W₂, d, Σ), Σ) = findlinks_V(W₁, d, Σ) ∪ findlinks_V(W₂, d, Σ)`. The middle step is exactly where F-UDIST must be unrestricted: even when `W₁ ∩ W₂ = ∅`, the two images may overlap — distinct V-positions can resolve to a shared I-address under content sharing (M13/M14, ASN-0058) — so a disjointness-restricted union law would not close this composition. F-VDIST is the Phase-1 payoff F-UDIST exists to enable: image distributes over V-region union, and union-distributivity over the resulting (possibly overlapping) I-sets carries the comprehension through.*

## The stability keystone

This note runs on *two* keystones, one per anchoring regime; they must not be collapsed into one. The first governs the *store-fixed* lane — transitions that hold `Σ.L` literally fixed — and is the meta-lemma below. It propagates to F-INERT and, through its per-link weakening F-CIL-perlink, to F-LAMBDA, and thence to everything D-NONMONO and D-CWP draw from F-INERT. It does *not* reach the existence-anchoring lane (E-INV → E-MONO → E-CONS): there the I-request is fixed in the permanent store, but the *path* `Σ →* Σ'` admits K.λ, so `Σ.L` may *grow* and F-CIL's store-equality hypothesis `Σ.L = Σ'.L` fails outright. That lane rests on a distinct foundation — LP13's per-link value persistence (UnconditionalLinkPersistence, ASN-0098), which pins each *surviving* link's value across a growing store — named as the second keystone in the existence-anchoring section below.

**F-CIL (ComprehensionInvariantUnderΣL — meta-lemma).** *If `Σ.L = Σ'.L` as partial functions, then for every comprehension*

> `{a ∈ dom(Σ.L) : P(a, Σ)}`

*whose membership predicate `P` consults only `Σ.L` and query-data (never `Σ.M`, `Σ.C`, `Σ.E`, `Σ.R`):*

> `{a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}`.

*Derivation chain. `Σ.L = Σ'.L` gives `dom(Σ.L) = dom(Σ'.L)` and per-link value equality `Σ.L(a) = Σ'.L(a)`. Component-wise tuple equality on link values (L6) gives `|Σ.L(a)| = |Σ'.L(a)|` and per-slot endset equality `Σ.L(a).eᵢ = Σ'.L(a).eᵢ`. Coverage is a deterministic function of its endset argument, so per-slot coverage agrees. Any membership predicate built from these evaluates identically at the two states; set extensionality closes the equality.*

A weaker per-link form supports the inductive step for K.λ:

**F-CIL-perlink (PerLinkInvarianceUnderValuePreservation — sub-lemma).** *For any `a` with `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`:*

- *`matches(a, I, Σ) ⟺ matches(a, I, Σ')` for every `I ⊆ T`;*
- *for every slot constraint `(i, J)`, the per-link conjunct `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` evaluates identically at `Σ` and `Σ'`.*

*Derivation. From the per-link value equality `Σ'.L(a) = Σ.L(a)`, component-wise tuple equality on link values (L6) gives arity equality `|Σ'.L(a)| = |Σ.L(a)|` and per-slot endset equality `Σ'.L(a).eᵢ = Σ.L(a).eᵢ`; coverage is a deterministic function of its endset argument, so per-slot coverage agrees, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Both the `matches` existential `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` and the per-slot conjunct `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` are built from exactly the arity bound and the per-slot coverage, so each evaluates identically at `Σ` and `Σ'`. This is the per-link tail of F-CIL's chain, begun from per-link value equality rather than the global store equality `Σ.L = Σ'.L`; the weakening is load-bearing under K.λ, where `dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new} ≠ dom(Σ.L)` makes F-CIL's global hypothesis fail while per-link preservation still holds at each prior key `a ∈ dom(Σ.L)`. F-CIL-perlink is therefore not an instance of F-CIL but the residual per-link reasoning that survives the weaker hypothesis.*

## Operational consequences

The store-fixed keystone F-CIL turns the question "which transitions preserve the result?" into the question "which transitions preserve `Σ.L`?" — for the store-fixed lane. (The existence lane is governed instead by LP13; see below.)

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

The request is given directly as a fixed I-address set `I ⊆ T` in the permanent address space. The match predicate then turns only on `coverage(Σ.L(a).eᵢ) ∩ I`; link values are permanent (LP13, ASN-0098), so both a link's arity and its per-slot coverage are fixed across every transition. LP13 is *this* lane's keystone, standing where F-CIL stood for the store-fixed lane: because the path `Σ →* Σ'` admits link creation, `Σ.L` is not fixed and F-CIL does not apply, yet LP13 still pins every surviving link's value under the growing store. The three claims below all descend from it.

**E-INV (CoveragePermanence).** *For fixed `I` and any `Σ →* Σ'`, every `a ∈ dom(Σ.L)` satisfies `a ∈ dom(Σ'.L)` and `matches(a, I, Σ') ⟺ matches(a, I, Σ)`.*

*Derivation. LP13 (UnconditionalLinkPersistence, ASN-0098) gives `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` across `Σ →* Σ'` — full link-value persistence, hence both arity equality `|Σ'.L(a)| = |Σ.L(a)|` and per-slot coverage equality `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`. Then `matches(a, I, Σ') = (E i : 1 ≤ i ≤ |Σ'.L(a)| : coverage(Σ'.L(a).eᵢ) ∩ I ≠ ∅) = (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅) = matches(a, I, Σ)`, the middle equality discharged by LP13 (arity and per-slot coverage together). LP3★ alone fixes per-slot coverage but not the arity bound `|Σ.L(a)|` over which the existential ranges; LP13 supplies both.*

**E-MONO (ExistenceMonotonicity).** *For fixed `I`, `Σ →* Σ' ⟹ findlinks(I, Σ) ⊆ findlinks(I, Σ')`.*

*The store grows across the transitive closure (Store Monotonicity, ASN-0098), coverage is invariant (E-INV), so the matching set only gains members.*

**E-CONS (CreationConservation).** *For fixed `I`, the set difference `findlinks(I, Σ') ∖ findlinks(I, Σ)` over `Σ →* Σ'` consists of exactly those links created on that path whose stored value matches `I`.*

*The "exactly" is a two-direction claim, and the exclusion direction is the one that needs E-INV. Take any `a ∈ findlinks(I, Σ') ∖ findlinks(I, Σ)`. Either `a ∉ dom(Σ.L)` or `a ∈ dom(Σ.L)`. Suppose `a ∈ dom(Σ.L)`: then E-INV gives `matches(a, I, Σ) ⟺ matches(a, I, Σ')`; from `a ∈ findlinks(I, Σ')` we have `matches(a, I, Σ')`, hence `matches(a, I, Σ)`, and together with `a ∈ dom(Σ.L)` this places `a ∈ findlinks(I, Σ)` — contradicting `a ∉ findlinks(I, Σ)`. So the second case is impossible: only `a ∉ dom(Σ.L)` survives, and such an `a` is a link created somewhere on the path `Σ →* Σ'` (it entered `dom(Σ'.L)` after `Σ`), matching at `Σ'` by its membership in `findlinks(I, Σ')`. Conversely, any link created on the path whose value matches `I` at `Σ'` lies in `findlinks(I, Σ')` and not in `findlinks(I, Σ)` (it was not yet a key at `Σ`), so it sits in the difference. Creation is therefore the sole source of change.*

### Discovery anchoring

The request is resolved through a querying document's current arrangement. Given `d_q ∈ dom(Σ.M)` and a query V-region `W ⊆ T`, the I-address argument is the state-resolved image:

> `findlinks_disc(W, d_q, Σ) ≡ findlinks(image(W, d_q, Σ), Σ)` = `findlinks_V(W, d_q, Σ)`.

**D-PRES (PresentTenseResolution).** *`image(W, d_q, Σ)` is a live reading of `d_q`'s arrangement. Editing `d_q` moves content into or out of the queried V-region without any link being created or retracted, so the resolved request — and hence `findlinks_disc` — can change while `dom(Σ.L)` is fixed.*

**D-NONMONO (DiscoveryNonMonotonicity).** *`findlinks_disc` is not monotone across `Σ →* Σ'`. By case analysis on the K-transition:*

- *K.μ⁺ or K.μ⁺_L on `d_q`*: the arrangement extends, so `image(W, d_q, Σ) ⊆ image(W, d_q, Σ')` (F-IMG-MONO). These transitions preserve `Σ.L` (F-PRES), so `findlinks(·, Σ) = findlinks(·, Σ')` for any fixed I-argument (F-INERT); this bridges the comprehension's evaluation state, letting it be held fixed at `Σ'` while only the image moves. Hence `findlinks_disc(W, d_q, Σ) = findlinks(image(W, d_q, Σ), Σ) = findlinks(image(W, d_q, Σ), Σ') ⊆ findlinks(image(W, d_q, Σ'), Σ') = findlinks_disc(W, d_q, Σ')` — the middle equality by F-INERT, the inclusion by F-IMG-MONO then F-IMONO evaluated at `Σ'`. The discovery set can only grow; the new I-addresses falling in `W`'s positions are what add the new link matches, evaluated against the unchanged store.
- *K.μ⁻ on `d_q`*: the arrangement contracts, so `image(W, d_q, Σ') ⊆ image(W, d_q, Σ)` (F-IMG-CONTR). K.μ⁻ preserves `Σ.L` (F-PRES), so `findlinks(·, Σ') = findlinks(·, Σ)` for any fixed I-argument (F-INERT); this bridges the comprehension's evaluation state, letting it be held fixed at `Σ` while only the image moves. Hence `findlinks_disc(W, d_q, Σ') = findlinks(image(W, d_q, Σ'), Σ') = findlinks(image(W, d_q, Σ'), Σ) ⊆ findlinks(image(W, d_q, Σ), Σ) = findlinks_disc(W, d_q, Σ)` — the middle equality by F-INERT, the inclusion by F-IMONO evaluated at `Σ`. The discovery set can only shrink.
- *K.μ~ on `d_q`*: the reorder holds `Σ.L` fixed (F-PRES/F-INERT), so every motion of the discovery set comes through the image, and F-IMG-SWING moves the image only when `W` is *not* fixed setwise by `π` — when `π⁻¹(W) ∩ dom(Σ.M(d_q)) = W ∩ dom(Σ.M(d_q))`, image and discovery set are both invariant. When the image does move, whether that motion is a containment — and hence whether the F-IMONO step the extension and contraction clauses turn on is available — depends on the injectivity of `Σ.M(d_q)`, and the two regimes must be kept separate. *Non-injective `d_q` (content sharing, M13/M14, ASN-0058):* the image may gain or lose members, and the motion can be a containment in either direction — F-IMG-SWING's own non-injective witness exhibits `image(W, d_q, Σ) = {a} ⊊ {a, b} = image(W, d_q, Σ')` (image growing), and the companion arrangement `Σ.M(d_q) : v₁ ↦ a, v₂ ↦ b, v₃ ↦ b` with `W = {v₁, v₂}` under the reorder `π(v₁) = v₃, π(v₂) = v₁, π(v₃) = v₂` gives `image(W, d_q, Σ') = {b} ⊊ {a, b} = image(W, d_q, Σ)` (image shrinking). Whenever the image motion is a containment, F-IMONO applies verbatim — bridged through F-INERT, since K.μ~ preserves `Σ.L` — and `findlinks_disc` moves monotonically in that single step, growing with a growing image and shrinking with a shrinking one, exactly as in the K.μ⁺ and K.μ⁻ clauses. *Injective `d_q`:* F-IMG-SWING pins the image cardinality (the witness bijection carries the equal-size index sets `π⁻¹(W) ∩ dom(Σ.M(d_q))` and `W ∩ dom(Σ.M(d_q))` to equal-size images), so when the image moves its two values are *distinct sets of equal size* — necessarily incomparable, since distinct finite sets of equal size cannot nest under `⊆` — and the F-IMONO step is genuinely unavailable here: image incomparability supplies no containment to lift, so the discovery set's behavior must be read off directly rather than inherited from the image. Image-motion is moreover *necessary but not sufficient* for the discovery set to move: because F-MATCH is a per-link existential over slots, a displaced in-region I-address alters the link set only when it was the *sole* in-region witness for some matched link — a member still reached through another slot of the same link, or through another retained in-region address, leaves that link's membership intact. Even sole-witness displacement is not sufficient: if the swapped-in I-address re-witnesses exactly the links the swapped-out one did, the discovery set holds fixed despite a sole witness moving. And — the point on which this regime must not be overstated — the image's incomparability does *not* transfer to the discovery set: `findlinks` is not order-reflecting, so the two incomparable equal-size image values may map to *nested* discovery sets, in either direction. If the swapped-in address witnesses no link, the discovery set drops `{L_1} ↦ ∅` — a strict shrink, the displaced member having been `L_1`'s sole in-region witness, yet the discovery change *being* a containment, not the incomparable move the image's incomparability might suggest; dually, when a *matched link's* endset covers the swapped-in address as well as the swapped-out one (so that link survives), and the swapped-in address additionally matches a further link, the set grows `{L_1} ↦ {L_1, L_2}`. The invalid step is therefore "incomparable image change ⟹ incomparable discovery change"; what the injective regime does establish, and all the lemma needs, is the existence claim that *some* injective reorder swings the discovery set across an incomparable pair, neither `⊆` nor `⊇`. The worked illustration's reorder clause exhibits two such moves, each lifting F-IMG-SWING through Phase 2 with no link created or retracted: a lateral same-cardinality swing `{L_1} ↦ {L_2}` (incomparable precisely because its from-endsets are disjoint singletons), and — with one auxiliary link reaching the swung-in address — a cardinality-changing swing `{L_1} ↦ {L_2, L_2'}`. The latter, image cardinality pinned at 1 throughout (F-IMG-SWING) yet the discovery set moving `1 ↦ 2`, shows discovery-set cardinality is not pinned even when image cardinality is: distinct I-addresses may match distinct link-counts. Taking the two regimes together, `findlinks_disc` is non-monotone under K.μ~: the injective lateral swing alone refutes monotonicity, exhibiting a change that respects no containment in either direction.
- *Transitions not on `d_q`*: `image(W, d_q, Σ) = image(W, d_q, Σ')`; the result changes only if `K.λ` adds a matching link (F-LAMBDA).

**D-CWP (ContractionStabilityWP).** *Fix a K.μ⁻ contraction `Σ → Σ'` on the query document `d_q` with retention set `R = ⋃ {[S, 1, …, 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}` (ASN-0047), so that `enabled(K.μ⁻[d_q, R])` holds — the retention counts `n'_S ∈ {0, …, n_S}` are admissible and at least one subspace strictly contracts — and `Σ'.M(d_q) = Σ.M(d_q) ↾ R`. The post-state image reduces to a pre-state quantity (the **bridge**, the discovery analog of LP12a's `project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R`):*

> `image(W, d_q, Σ') = {Σ.M(d_q)(v) : v ∈ W ∩ R} ≡ I_R`,

*since `dom(Σ'.M(d_q)) = R` (D-SEQ★ gives `R ⊆ dom(Σ.M(d_q))`, so `Σ.M(d_q) ↾ R` has domain exactly `R`) and `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` on `v ∈ R` (retained-domain agreement). Write `Δ ≡ image(W, d_q, Σ) ∖ I_R` for the I-addresses the contraction drops from the queried region (well-defined, with `image(W, d_q, Σ) = I_R ∪ Δ`, by F-IMG-CONTR). The contraction leaves the discovery set fixed*

> `findlinks_disc(W, d_q, Σ') = findlinks_disc(W, d_q, Σ)`  *iff*  `findlinks(Δ, Σ) ⊆ findlinks(I_R, Σ)`

*— i.e. iff every link reaching a dropped I-address also reaches a retained one. Both `I_R = {Σ.M(d_q)(v) : v ∈ W ∩ R}` and `Δ = image(W, d_q, Σ) ∖ {Σ.M(d_q)(v) : v ∈ W ∩ R}` are functions of the pre-state `Σ` and the retention set `R` alone — the bridge eliminates every post-state quantity — so the biconditional is a genuine precondition on `(Σ, R)`, evaluable before the step, exactly as LP12a expresses its wp over `Σ` and `R` and records its own post/pre bridge separately.*

*Derivation. K.μ⁻ preserves `Σ.L` (F-PRES), so `findlinks(I, Σ') = findlinks(I, Σ)` for every fixed `I` (F-INERT); in particular `findlinks_disc(W, d_q, Σ') = findlinks(image(W, d_q, Σ'), Σ) = findlinks(I_R, Σ)` by the bridge — the comprehension may be evaluated at `Σ`. Expanding the pre-state set through `image(W, d_q, Σ) = I_R ∪ Δ` and applying F-UDIST (no disjointness required): `findlinks_disc(W, d_q, Σ) = findlinks(I_R ∪ Δ, Σ) = findlinks(I_R, Σ) ∪ findlinks(Δ, Σ) = findlinks_disc(W, d_q, Σ') ∪ findlinks(Δ, Σ)`. Writing `A = findlinks_disc(W, d_q, Σ') = findlinks(I_R, Σ)` and `B = findlinks(Δ, Σ)`, this reads `findlinks_disc(W, d_q, Σ) = A ∪ B`, so the stability equation `A = findlinks_disc(W, d_q, Σ)` becomes `A = A ∪ B`, which holds iff `B ⊆ A` — exactly `findlinks(Δ, Σ) ⊆ findlinks(I_R, Σ)`. This is the weakest precondition for discovery-anchored stability under this single K.μ⁻ step — the discovery analog, on the contraction side, of ASN-0098's LP12a (ContractionDiscoverabilityWP), and like LP12a it is stated purely over the pre-state `Σ` and the retention set `R`.*

*Boundary case `R = ∅`. Full clearance of a non-empty `d_q` is a valid K.μ⁻ (every retention count `n'_S = 0`; strict contraction holds because `d_q` is non-empty, some `n_S ≥ 1`). Here `I_R = {Σ.M(d_q)(v) : v ∈ W ∩ ∅} = ∅`, so `Δ = image(W, d_q, Σ)` and the stability condition collapses to `findlinks(image(W, d_q, Σ), Σ) ⊆ findlinks(∅, Σ) = ∅` (F-FIND), i.e. `findlinks_disc(W, d_q, Σ) = ∅`: full clearance preserves the discovery set exactly when it was already empty. This is the whole-set reading of LP12a's own `R = ∅` specialisation `wp ≡ false` — no single link survives as discoverable, so `findlinks_disc(W, d_q, Σ') = ∅`, and stability against that post-state zero forces the pre-state set to have been `∅`. The difference is one of grain: LP12a asks a single-link question (and gets the flat `false`), D-CWP a whole-set one (and gets the pre-state emptiness condition). The uniform characterization over arbitrary transitions and regions remains open (Q3).*

**D-ZERO (PresentNotHistorical).** *A discovery zero `findlinks_disc(W, d_q, Σ) = ∅` asserts that no link in `dom(Σ.L)` is presently reachable from `d_q`'s arrangement at `Σ`. It does not assert historical absence. A link whose endpoints have left `d_q`'s consulted arrangement merely ceases to be reachable through it (its image drops by D-NONMONO), so it leaves the discovery set while remaining a permanent member of the store (L12).*

*By contrast, an existence zero against fixed `I` certifies historical absence: by E-INV satisfaction against fixed `I` is per-link time-invariant, and by E-MONO the set is monotone, so `findlinks(I, Σ) = ∅` implies `findlinks(I, Σ₀) ⊆ findlinks(I, Σ) = ∅` along every path `Σ₀ →* Σ` — no link satisfying `I` was ever created.*

## Worked illustration

Take a single document `d` with three text positions `v_1, v_2, v_3` mapping to content addresses `a_1, a_2, a_3` respectively, and two stored links, each a conforming triple (L3) with a non-empty type endset at slot 3: `L_1 = ({a_1}, {a_3}, Θ)` and `L_2 = ({a_2}, {a_3}, Θ)`, with type endset `Θ = {a_θ}`.

*Coverage of the endset shorthand.* Each singleton `{x}` here abbreviates the canonical unit-depth endset `{(x, δ(1, #x))}`, whose coverage is the entire subtree `coverage({x}) = {t ∈ T : x ≼ t} = subtree(x)` (PrefixSpanCoverage) — never the bare singleton `{x}`, which no endset can denote. The slot reductions below rest on one structural premise: the generating addresses are pairwise prefix-incomparable. This holds because `a_1, a_2, a_3` are distinct content addresses of the same document `d`, hence siblings on `d`'s content chain `A_C(d)` (ChainMembershipForOrigin, ASN-0093) and pairwise prefix-incomparable (T10a.2, ASN-0034); and `a_θ` is a type address in a distinct subspace (`s_L`), so it diverges from every content address at or before the subspace component and is prefix-incomparable with each — a fortiori `a_θ ∉ {a_1, a_2, a_3}`. Under this premise each subtree meets the query I-set only at its own generating address: for any `I ⊆ {a_1, a_2, a_3}`, `coverage({a_i}) ∩ I = subtree(a_i) ∩ I = {a_i} ∩ I` (no other listed address lies under `a_i`), and `subtree(a_θ) ∩ {a_1, a_2, a_3} = ∅`.

*Phase 1.* `W = {v_1, v_2}` yields `image(W, d, Σ) = {a_1, a_2}`.

*Phase 2.* `findlinks({a_1, a_2}, Σ)` — both links match via slot 1, every slot intersected against the full query I-set `{a_1, a_2}`. For `L_1`, `coverage(e₁) ∩ {a_1, a_2} = subtree(a_1) ∩ {a_1, a_2} = {a_1} ≠ ∅` (since `a_1 ⋠ a_2`); for `L_2`, `coverage(e₁) ∩ {a_1, a_2} = subtree(a_2) ∩ {a_1, a_2} = {a_2} ≠ ∅` (since `a_2 ⋠ a_1`). The other slots do not fire: both links' slot 2 is `{a_3}`, so `coverage(e₂) ∩ {a_1, a_2} = subtree(a_3) ∩ {a_1, a_2} = ∅` (`a_3 ⋠ a_1`, `a_3 ⋠ a_2`), and the type slot gives `coverage(e₃) ∩ {a_1, a_2} = subtree(a_θ) ∩ {a_1, a_2} = ∅` (`a_θ` prefix-incomparable with each). The match is carried entirely by slot 1, and the result is `{L_1, L_2}`.

*Stability under K.α* — allocating fresh content `a_4` adds nothing to `image(W, d, Σ)` (V-positions in `W` are unchanged); F-INERT carries the result. ✓

*Stability under K.μ⁻* — with `v_1 = [1,1], v_2 = [1,2], v_3 = [1,3]`, K.μ⁻ retains an initial segment `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ n'_{s_C}}` of the sequential positions (D-SEQ★), never a mid-sequence position. Retaining `n'_{s_C} = 1` keeps only the prefix `{v_1}`, removing both `v_2` and `v_3`. Then `W ∩ dom(Σ'.M(d)) = {v_1, v_2} ∩ {v_1} = {v_1}`, so `image(W, d, Σ')` shrinks to `{a_1}` and `findlinks_disc(W, d, Σ')` shrinks to `{L_1}`. ✓ D-NONMONO contraction clause.

*Rise under K.μ⁺ (store-fixed)* — Continue from the contracted state of the previous bullet, naming it `Σ₁`: `dom(Σ₁.M(d)) = {v_1}`, so `image(W, d, Σ₁) = {a_1}` and `findlinks_disc(W, d, Σ₁) = {L_1}`. The pre-existing link `L_2 = ({a_2}, {a_3}, Θ)` still resides in `dom(Σ₁.L)` (K.μ⁻ preserved the store) and its from-endpoint `a_2` still resides in `dom(Σ₁.C)` (content is permanent, P0) — but `a_2 ∉ image(W, d, Σ₁)`, so `L_2 ∉ findlinks_disc(W, d, Σ₁)`: the link and its target both persist, yet `L_2` is presently undiscoverable through `d`. Now apply K.μ⁺ adding `v_2 ↦ a_2`, a valid content-subspace extension restoring the contiguous segment `{v_1, v_2}` (D-SEQ★) whose image `a_2 ∈ dom(Σ₁.C)` discharges referential integrity (S3★); call the result `Σ₂`. The link store is untouched — `Σ₂.L = Σ₁.L` (F-PRES) — so no link is created. Yet `image(W, d, Σ₂) = {a_1, a_2}`, and `L_2` re-enters via slot 1 (`coverage(e₁) ∩ {a_1, a_2} = subtree(a_2) ∩ {a_1, a_2} = {a_2} ≠ ∅`): `findlinks_disc(W, d, Σ₂) = {L_1, L_2}`. Thus `L_2 ∉ findlinks_disc(W, d, Σ₁)` while `L_2 ∈ findlinks_disc(W, d, Σ₂)` — the discovery set rises under a pure arrangement extension, with no link created or modified. ✓ D-NONMONO extension clause. This store-fixed rise is precisely the motion existence anchoring cannot exhibit: against fixed `I`, only K.λ ever changes `findlinks(I, ·)` (F-LAMBDA, E-CONS), so the existence-anchored set never rises without a creation — here discovery rises on arrangement alone.

*Swing under K.μ~ (store-fixed)* — Return to the initial state `Σ` (all three positions live: `v_1 ↦ a_1, v_2 ↦ a_2, v_3 ↦ a_3`) and narrow the query to the single position `W₀ = {v_1}`. Then `image(W₀, d, Σ) = {a_1}` and `findlinks_disc(W₀, d, Σ) = {L_1}`: only `L_1` matches, via slot 1 (`coverage(e₁) ∩ {a_1} = subtree(a_1) ∩ {a_1} = {a_1} ≠ ∅`), while `L_2`'s slot 1 misses (`subtree(a_2) ∩ {a_1} = ∅`, since `a_2 ⋠ a_1`) and `L_2`'s slot-2/slot-3 coverages `subtree(a_3)`, `subtree(a_θ)` miss `{a_1}` as well. Now apply the transposition reorder `π = (v_1 v_2)` — a valid K.μ~ on `d`: it fixes the V-position set `{v_1, v_2, v_3}` (K.μ~-FIX, ASN-0047), preserves length and subspace, has non-trivial net effect (`v_1`'s image changes), and the arrangement-shape invariants (D-CTG★, D-MIN★, S8a, S8-depth) hold in the post-state because the V-position domain is unchanged. The bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)` gives `Σ'.M(d) : v_1 ↦ a_2, v_2 ↦ a_1, v_3 ↦ a_3`. The link store is untouched — `Σ'.L = Σ.L` (F-PRES) — so no link is created or retracted. But `W₀ = {v_1}` is not fixed setwise by `π` (`π⁻¹({v_1}) = {v_2}`), so the image swings: `image(W₀, d, Σ') = {a_2}`, and now only `L_2` matches (slot 1: `subtree(a_2) ∩ {a_2} = {a_2} ≠ ∅`); `L_1` no longer matches, since its slots — anchored at `a_1`, `a_3`, `a_θ` — all miss `{a_2}`. Hence `findlinks_disc(W₀, d, Σ') = {L_2}`. The discovery set moves `{L_1} ↦ {L_2}`: a lateral swing — neither `{L_1} ⊆ {L_2}` nor the reverse — at the same cardinality (the arrangement is injective, so F-IMG-SWING permits only membership change), with no link created or retracted. Each displaced image member is here the *sole* in-region witness for its link, which is why the swing reaches the link set rather than being absorbed by the multi-slot existential. Had the query stayed at `W = {v_1, v_2}` — fixed setwise by `π` (`π⁻¹({v_1, v_2}) = {v_1, v_2}`) — both image and discovery set would be invariant; the swing requires a region the reorder does not preserve. *Cardinality-changing variant.* The lateral swing above moved the discovery set at fixed cardinality, but the cardinality is not forced. Admit one further link `L_2' = ({a_2}, ∅, Θ)` (a conforming triple — empty to-endset admissible, `Θ = {a_θ}` mandatory) so that `a_2` is reached by two links where `a_1` is reached by one. `L_2'` leaves the pre-state result untouched — its only non-empty coverage slot misses `{a_1}` (`coverage(e_1) ∩ {a_1} = subtree(a_2) ∩ {a_1} = ∅`, since `a_2 ⋠ a_1`), so `findlinks_disc(W₀, d, Σ) = {L_1}` still — while at the post-state both links reaching `a_2` fire (`subtree(a_2) ∩ {a_2} = {a_2} ≠ ∅` for each): `findlinks_disc(W₀, d, Σ') = {L_2, L_2'}`. The same transposition reorder now swings `{L_1} ↦ {L_2, L_2'}` — cardinality `1 ↦ 2`, with no link created or retracted by the reorder (`L_2'` was already stored and `Σ'.L = Σ.L`). This needs no content sharing: the arrangement stays injective, so the *image* cardinality remains pinned at 1 (F-IMG-SWING); only the *discovery-set* cardinality moves, and it moves purely because distinct I-addresses match distinct link-counts. ✓ D-NONMONO reorder clause.

*K.λ adding L_3* `= ({a_1}, ∅, Θ)` (a conforming triple; the empty to-endset is admissible, the type slot `Θ = {a_θ} ≠ ∅` is mandatory): F-LAMBDA gives `findlinks({a_1, a_2}, Σ') = {L_1, L_2, L_3}` — the prior result plus the new link's match, which fires via slot 1 (`coverage(e₁) ∩ {a_1, a_2} = subtree(a_1) ∩ {a_1, a_2} = {a_1} ≠ ∅`).

*Existence vs discovery zero.* Suppose K.μ⁻ removes all of `v_1, v_2, v_3` — the `R = ∅` full-clearance contraction of D-CWP's boundary case. Then `image(W, d, Σ') = ∅`, `findlinks_disc(W, d, Σ') = ∅` (discovery zero — present absence); and since the pre-state discovery set `findlinks_disc(W, d, Σ) = {L_1, L_2}` is non-empty, D-CWP's `R = ∅` stability condition `findlinks_disc(W, d, Σ) = ∅` fails — the discovery set is correctly *not* stable, dropping `{L_1, L_2} ↦ ∅`. But `findlinks({a_1, a_2}, Σ') = {L_1, L_2}` (existence non-zero — K.μ⁻ preserves `Σ.L`, so the fixed-`I` comprehension `findlinks({a_1, a_2}, ·)` is unchanged by F-INERT, with per-link coverage permanence by E-INV).

## Properties established

| Claim | Statement | Role |
|-------|-----------|------|
| F-IMG | `image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}` | Phase 1 primitive |
| F-IMG-MONO | image grows under K.μ⁺/K.μ⁺_L | image stability |
| F-IMG-CONTR | image shrinks under K.μ⁻ | image stability |
| F-IMG-SWING | image may move under K.μ~ | image instability |
| F-MATCH | match predicate (existential over slots) | Phase 2 primitive |
| F-FIND | comprehension primitive `findlinks(I, Σ)` | Phase 2 primitive |
| F-UDIST | `findlinks(I₁ ∪ I₂) = findlinks(I₁) ∪ findlinks(I₂)` for all `I₁, I₂` | Phase 2 algebra |
| F-IMONO | `I' ⊆ I ⟹ findlinks(I') ⊆ findlinks(I)` | Phase 2 algebra (corollary of F-UDIST) |
| F-V | `findlinks_V(W, d, Σ) = findlinks(image(W, d, Σ), Σ)` | two-phase combinator (definition) |
| F-VDIST | `findlinks_V(W₁ ∪ W₂, d, Σ) = findlinks_V(W₁, d, Σ) ∪ findlinks_V(W₂, d, Σ)` | composite algebra (Phase-1 payoff of F-UDIST) |
| F-CIL | comprehension over `dom(Σ.L)` with `Σ.L`-only predicate is `Σ.L`-stable | store-fixed-lane keystone |
| F-CIL-perlink | per-link version under per-link value preservation | sub-lemma |
| F-PRES | `V_atomic ∖ {K.λ}` and `K.μ~` preserve `Σ.L` | transition vocabulary |
| F-INERT | preservation ⟹ result invariance | operational consequence |
| F-LAMBDA | `K.λ` increments result by the newly matching singleton (or nothing) | unique store-modifying op |
| E-INV | coverage permanence (per-link, against fixed `I`) | existence anchoring |
| E-MONO | existence-anchored result is `→*`-monotone | existence anchoring |
| E-CONS | path-level set difference is exactly matching creations | existence anchoring |
| D-PRES | image is a live reading of `Σ.M(d_q)` | discovery anchoring |
| D-NONMONO | discovery-anchored result is non-monotone (K-case analysis) | discovery anchoring |
| D-CWP | K.μ⁻ stability iff every dropped-region link also reaches a retained I-address | discovery anchoring (wp) |
| D-ZERO | discovery zero ≠ historical absence | discovery anchoring |

## Open questions

What is the relationship between `findlinks_V` and a content-keyed query that names addresses through `Σ.C` rather than `Σ.M`? Both are content-region queries in a broad sense; this note treats only the arrangement-mediated case.

Under what filter-set constraints over `findlinks` does union-distributivity (F-UDIST) preserve into the filtered form, and where does the per-slot universal vs the per-link existential distinction matter for compositional reasoning?

D-CWP computes the weakest precondition for discovery-anchored stability under a K.μ⁻ contraction on the query document. What is the corresponding weakest precondition for an arbitrary transition `Σ → Σ'` and region `W` — a uniform characterization across the whole K-vocabulary (extension, reorder, and off-document transitions alongside contraction) of when `findlinks_V(W, d, Σ) = findlinks_V(W, d, Σ')`, of which D-CWP is the contraction instance?

How does this foundation compose with ASN-0098's link projection displacement? `image()` and the LP** results both consult `Σ.M`; the natural composition is "project a link through arrangement, then ask if the projection meets a content region" — but the operational composition is not addressed here.
