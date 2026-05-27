# ASN-0099: FINDLINKS Operation

*2026-05-26*

## The Reader's Question

The reader looks at a stretch of content in their document and asks: *what connects here from elsewhere?* This is one half of the central reader-side promise of a Xanadu-style system — that the literature is bidirectionally navigable, that the links from the rest of the docuverse to the content in front of me must be findable on demand and without appreciable delay. We adopt this as our starting obligation. The user supplies a region of arranged content; the system must return every link whose endsets touch that content.

The reader knows only what they see. They see arranged content — a stretch of V-positions in some document `d`. They do not see I-addresses directly, do not see the content store, do not see other documents' arrangements, and they certainly do not see the link store. The query is in V-coordinates of `d`.

The links the reader wants live in `dom(Σ.L)`. By L1 (ASN-0043), each is at an element-level tumbler address, and by L3 carries a sequence of endsets whose spans reference content I-addresses, not V-positions. The first problem is therefore one of identity reconciliation: the reader's V-coordinates and the link store's I-coordinates speak different languages. The arrangement `Σ.M(d)` is the bridge between them.

## A Two-Phase Factoring

Before any formalism, let us recognize that the question splits cleanly into two phases with qualitatively different concerns. We separate them deliberately so each can be analyzed without the other underfoot.

**Phase 1 (V→I).** Given a document `d ∈ dom(Σ.M)` and a query region `R ⊆ dom(Σ.M(d))`, produce the *I-image* of the region:

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))
  ≡             {Σ.M(d)(v) : v ∈ R}
```

The two preconditions in the `defined when` clause are load-bearing: `d ∈ dom(Σ.M)` so that `Σ.M(d)` is defined as a partial function, and `R ⊆ dom(Σ.M(d))` so that every `Σ.M(d)(v)` is defined for `v ∈ R`. Without both, the comprehension is ill-formed. The reader's V-selection presupposes them — they query a position they can see, in a document that exists — but we state them explicitly because the operation has no value to take at positions outside the arrangement's domain. A query that nominates `v ∉ dom(Σ.M(d))` is either rejected at a higher protocol layer or treated as if `v` were absent from `R`; the abstract specification supports both treatments by leaving `image` undefined on such inputs rather than extending it with a sentinel. The image is a set of I-addresses, every member of which lies in `dom(Σ.C) ∪ dom(Σ.L)` by S3★ (ASN-0047). The phase reduces V-coordinates to address-of-content.

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, produce the set of links whose endsets intersect `I`:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

The two phases compose into the reader-facing operation:

```
F12 (TwoPhaseFactoring):
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))
     ≡             findlinks(image(R, d, Σ), Σ).
```

The preconditions are inherited from `image`'s `defined when` clause — `findlinks_V` is well-formed precisely when `image(R, d, Σ)` is. We restate them at the composite to keep the partiality visible at the call site: a query that nominates a non-existent document or a V-position outside the arrangement's domain has no well-defined V-side answer, and the abstract specification declines to invent one.

The factoring matters because the two phases have entirely different stability properties. The arrangement `Σ.M` is mutable: K.μ⁺, K.μ⁻, K.μ~, and K.μ⁺_L all modify it. The link store `Σ.L` is monotonic: K.λ adds to it, and L12 (ASN-0093) forbids any modification of existing entries. Phase 1 consults the mutable component; phase 2 consults the monotonic component. This separation will let us conclude later that link discovery is fundamentally a property of `(Σ.L, I)`, with the arrangement entering only to translate V-input into I-input.

We will spend most of our effort on phase 2. Phase 1 is a finite lookup once the arrangement is fixed; it has no degrees of freedom to analyze.

## The Image Set

The V-region `R` need not be contiguous. The reader may select a single position, a contiguous V-span, or any subset of `dom(Σ.M(d))`. We do not constrain `R` beyond its inclusion in the arrangement's domain.

When `R` is a contiguous V-span in subspace `s_C`, the image decomposes naturally by ASN-0058's mapping block decomposition: each maximal correspondence run whose V-extent overlaps `R` contributes a contiguous I-run to `image(R, d, Σ)`. If the content of `d` was natively allocated in `d`, the image is a single contiguous I-run lying in `A_C(d)`'s chain. If `d` contains transclusions from multiple sources, the image is a union of disjoint I-runs, each rooted in a different sub-allocator chain.

The query may also touch the link subspace. When `v ∈ R` has `subspace(v) = s_L`, then by S3★ (ASN-0047), `Σ.M(d)(v) ∈ dom(Σ.L)` — the image picks up a link address, not a content address. The match predicate accepts this without modification: endsets may reference any addresses in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target. A query for the links attached to an arranged link — an annotation on an annotation, a comment about a typed connection — is the natural use case. The operation works uniformly across subspaces because the match predicate is address-set agnostic: it consults coverage of the endset and overlap with the image, not what kind of entity inhabits the image's addresses.

We let these facts emerge naturally rather than encode them in the operation's signature. The match predicate in phase 2 treats `I` as an opaque set of I-addresses; it does not consult `origin(·)` and does not care that `I` decomposes into multiple sub-chains, nor whether each address inhabits `dom(Σ.C)` or `dom(Σ.L)`. Whatever the V-region's history and whatever the subspace of its positions, the image is the I-address set we hand to phase 2.

## The Match Predicate

Fix a query I-set `I ⊆ T` and a state `Σ`. A link `a ∈ dom(Σ.L)` *matches* iff one of its endsets has coverage that meets `I`:

```
F1 (MatchPredicate):
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

This generalizes ASN-0098's `discoverable_from(a, d, Σ)`, which is `matches(a, ran(Σ.M(d)), Σ)`. The two predicates coincide when the query I-set is the I-image of an entire document; FINDLINKS admits arbitrary `I ⊆ T` and so spans the full design space that LP12 (DiscoverabilityCharacterisation, ASN-0098) specialises along one axis.

We must justify the existential over slots and the choice of intersection rather than containment.

**Why the existential.** A link's endsets are independent positional slots, and L7 (ASN-0043) explicitly leaves directional significance to the link type — slot 1 is "from" and slot 2 is "to" only by convention, with the convention's force determined elsewhere. The reader's question — *what connects here?* — does not privilege from over to. If the type-endset covers `I`, the link is about content of that type residing in `I`; that is no less a connection than if the from-endset covered `I`. We existentially quantify over all slots, including the type-endset and any further slots permitted by the N-endset structure of L3 (ASN-0043).

**Why intersection rather than containment.** A link's endset is a span-set, and its coverage is the set of addresses that any of its spans names. A link *is about* the bytes its endsets cover. If the query touches even one of those bytes, the query has touched a byte that the link is about, and the link is structurally implicated by the query. To require containment in either direction would impose a circular precondition: the reader would have to know each link's exact extent to know whether to include the link in the query, but the purpose of the query is precisely to discover links whose existence the reader does not yet know. The match must be symmetric in `coverage(eᵢ)` and `I`, and a singleton overlap must suffice.

Stated formally:

```
F4 (PartialOverlapSuffices):
   For any e and any I, if there exists α ∈ T with α ∈ coverage(e) ∧ α ∈ I,
   then a link with endset e at slot i has matches(a, I, Σ) = true.
```

This is immediate from the definition of `matches`. We name it as a separate claim because the consequence — that the implementation cannot require full overlap, near-overlap, majority overlap, or any other strengthened condition — is a load-bearing design choice that propagates through the rest of the operation's semantics.

## Endset Filtering

The reader may not want every link that touches `I`. They may want only links *from* the queried region, or only links *of type θ*, or "from `I_from` to `I_to`". We generalize the match predicate to admit per-slot constraints.

A *slot constraint* is a pair `(i, J)` where `i ∈ ℕ⁺` is a slot index and `J ⊆ T` is an I-set. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. The positional accessor `Σ.L(a).eᵢ` is undefined for `i > |Σ.L(a)|` (L6, ASN-0043), so we fold the out-of-range case into the per-constraint conjunct as an explicit guard — a link with too few slots fails any constraint that references a slot it does not have. The reader may supply any conjunction of slot constraints:

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C :
                       i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

where `C` is a finite set of slot constraints. The conjunct `i ≤ |Σ.L(a)| ∧ ...` keeps the comprehension well-formed at every `a ∈ dom(Σ.L)`: when `i > |Σ.L(a)|`, the left conjunct is false and short-circuits the undefined accessor, so the per-constraint clause evaluates to false without consulting `Σ.L(a).eᵢ`. The from-to query "links from `I_from` to `I_to`" is the constraint set `{(1, I_from), (2, I_to)}`. The three-endset query adds `(3, I_type)`. A query that restricts only by type is `{(3, I_type)}` — the from and to slots are unconstrained, so the link matches regardless of where its from and to endsets land.

The filtered form is *not* a strict generalization of the unfiltered form: the unfiltered match is an existential over slots (a link matches if *any* slot's coverage meets `I`), while the filtered match is a universal over constraints (a link matches if *every* `(i, J)` is satisfied at slot `i`). The two are structurally distinct — disjunction versus conjunction — and no single conjunctive constraint set over the present `C`-vocabulary recovers the disjunction. The unfiltered form is instead recovered as a *union* over single-slot filters:

```
findlinks(I, Σ) = ⋃_{i ∈ ℕ⁺} findlinks_filtered({(i, I)}, Σ)
```

The index `i` ranges over all positive integers, but each link contributes only over its own slot range: a link `a` with `|Σ.L(a)| = n` participates in `findlinks_filtered({(i, I)}, Σ)` for `i ∈ {1, …, n}` only. For `i > n`, the constraint `(i, I)` references a slot absent from `a` and is unsatisfiable, so `a` is excluded from `findlinks_filtered({(i, I)}, Σ)` at that `i`. The right-hand side is therefore well-defined as a union over ℕ⁺: each link enters finitely many terms (bounded by its own arity), and L3 (ASN-0043) supplies the lower bound `|Σ.L(a)| ≥ 3` so every link enters at least three terms. Moreover, only finitely many terms of the union are non-empty in total: by L-fin (ASN-0093), `dom(Σ.L)` is finite, so `max{|Σ.L(a)| : a ∈ dom(Σ.L)}` is a finite bound when `dom(Σ.L) ≠ ∅`, and `findlinks_filtered({(i, I)}, Σ) = ∅` for every `i` exceeding this maximum. The infinite union therefore has a finite effective range — the apparent unboundedness is a notational artefact of indexing over ℕ⁺, not a computational obligation. Extending the constraint vocabulary to admit per-slot disjunctions would close the gap structurally, but the present spec keeps the two operations side by side, with the explicit conversion above.

The conjunction is intersection in the link-set lattice. The implementation may compute each per-slot result independently and intersect, or may apply constraints sequentially with pruning, or may employ any other strategy that produces the same set. The abstract specification only requires that the *result* be the conjunctive set.

These structural properties travel together:

```
F7 (EndsetSymmetry):
   (a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly via the
       existential (E i : 1 ≤ i ≤ |Σ.L(a)|), so no slot is privileged a priori.
       Type-endsets and any further slots in the N-endset structure (L3) are
       searchable on the same footing as the conventional from/to.
   (b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot
       constraints via the universal (A (i, J) ∈ C), so the force of a filter
       set is conjunctive — a link must satisfy every constraint to appear in
       the result.
```

Both halves follow directly from the quantifier structure of the definitions: the existential in `matches` makes slots equally searchable (the reader's question does not privilege which endset connects); the universal in `findlinks_filtered` makes filters conjoin (each constraint narrows the candidate set). The symmetry is intrinsic to the formal shape — no auxiliary axiom is needed.

## Completeness

The operation's defining obligation is *completeness*: every link in `dom(Σ.L)` satisfying the match predicate must appear in an implementation's output. The promise is to the reader, who is told that the link mechanism ties together the corpus and that the system will return all connections to the queried content. A link that exists in the link store and touches the queried I-set, but fails to appear in the result, is a violation of the reader's promise.

The abstract specification `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` is one set — uniquely determined by `(Σ.L, I)`. A conforming implementation must produce *exactly* this set in response to the query. We let `result(I, Σ)` denote the implementation's actual output and state completeness and soundness as the two halves of the conformance obligation pinning `result` to `findlinks`:

```
F2 (Completeness):
   For every a ∈ dom(Σ.L): matches(a, I, Σ) ⟹ a ∈ result(I, Σ).
   Equivalently: findlinks(I, Σ) ⊆ result(I, Σ).
```

```
F3 (Soundness):
   For every a ∈ result(I, Σ): a ∈ dom(Σ.L) ∧ matches(a, I, Σ).
   Equivalently: result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 and F3 force `result(I, Σ) = findlinks(I, Σ)` — there is exactly one conforming output set. For the filtered form, the same obligation holds against `findlinks_filtered(C, Σ)`: completeness requires every link satisfying every constraint in `C` to appear in the filtered output, and soundness requires no spurious link.

F2 and F3 are not tautologies of the abstract definition `findlinks` — they are constraints on the separate symbol `result`. At the level of `findlinks` alone the corresponding inclusions are trivial (a comprehension contains exactly those source elements satisfying its predicate, and only those); the abstract specification is one set. F2 and F3 acquire force precisely as the conformance requirements that an implementation's actual output must coincide with this set.

Completeness must hold *unconditionally* with respect to the population of `dom(Σ.L)`. The number of non-matching links is irrelevant — performance is an implementation property, completeness is a correctness property. The operation cannot terminate early after collecting "enough" links, cannot omit links by random sampling, cannot drop links because they are stored on a remote server that is slow to answer, and cannot exclude links because their endsets are large. If the link is in the store and the match holds, the link is in the result. Soundness's force is dual: a conforming implementation cannot return links that fail the match — no false positives from a stale index, no extras from an over-approximating filter — and so the implementation's index, if any, must remain in lockstep with the link store rather than offering a superset.

## Determinism

The result depends only on the link store and the query specification. It does not depend on any history, any cached state, any concurrent activity, or any implementation choice not visible to the abstract specification:

```
F8 (Determinism):
   findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

F8 is a property of the *abstract* operation — the comprehension is a function of `(Σ.L, I)` alone, so two states agreeing on the link store yield equal abstract results regardless of any other state component. The implementation-side consequence `result(I, Σ) = result(I, Σ')` is *not* additional content; it follows from F8 by F2 and F3: each `result(·, ·)` coincides with its `findlinks(·, ·)` by F2 ∧ F3, and equality of the two `findlinks` values transfers through. We separate the two levels because the abstract determinism is a structural fact of the definition, while the conformance equality is the implementation's obligation to track that structural fact.

Determinism is structurally guaranteed by the form of `matches`. The derivation chain unfolds step by step. From `Σ.L = Σ'.L`, equality of partial functions gives `dom(Σ.L) = dom(Σ'.L)` and `(A a ∈ dom(Σ.L) :: Σ.L(a) = Σ'.L(a))`. Per-link, component-wise tuple equality on `Link` values (L6, ASN-0043) gives per-slot agreement `Σ.L(a).eᵢ = Σ'.L(a).eᵢ` for every `i ∈ {1, …, |Σ.L(a)|}`. The `coverage(·)` operator is a deterministic function of its argument endset (it takes the union of T1-half-open intervals over the endset's spans), so per-slot endset equality yields per-slot coverage equality `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`. The predicate `matches(a, I, Σ) ≡ (E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is then point-wise equal at the two states for every `a ∈ dom(Σ.L)`. Set extensionality applied to the comprehensions `{a ∈ dom(Σ.L) : matches(a, I, Σ)}` and `{a ∈ dom(Σ'.L) : matches(a, I, Σ')}` (with equal source sets and equal predicates) closes the chain: the `findlinks` sets are equal.

A direct consequence: the two phases compose unambiguously. Once `I = image(R, d, Σ)` is computed, the I-Link search is determined by `Σ.L`. Two different ways of arriving at the same `I` produce the same result. If a reader at state `Σ` and another reader at state `Σ'` both produce the I-set `I` (perhaps because their respective documents transclude overlapping content), they receive the same result if `Σ.L = Σ'.L`.

## Arrangement Independence

The I→Link phase consults `Σ.L` and `I` alone. It does not consult any arrangement. F8 already encodes this in its hypothesis `Σ.L = Σ'.L`: `Σ.M` is unmentioned, so two states agreeing on the link store give equal results regardless of how their arrangements differ. We name the operationally salient specialisation separately, as the frame condition exercised by editing operations:

```
F9 (LinkSurvivabilityUnderEdits):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d — K.μ⁺ (content extension), K.μ⁻ (contraction),
   K.μ~ (reordering), or K.μ⁺_L (link extension) — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').
```

F9 follows from F8 once we observe that `Σ'.L = Σ.L` at every K.μ-family transition. The derivation splits into two cases.

*K.μ~ and K.μ⁺_L.* These operations state `L' = L` explicitly in their frame clauses (ASN-0047), so the F8 hypothesis is satisfied directly from the published frame.

*K.μ⁺ and K.μ⁻.* These operations do not list `L` in their published frames in ASN-0047 — their frames cover `C`, `E`, `R`, and the per-document arrangement clause `(A d' : d' ≠ d : M'(d') = M(d'))`, but say nothing about `L`. We derive `Σ.L = Σ'.L` for these operations in two steps, by combining L12 (LinkImmutability, ASN-0093) with an explicit enumeration of the link-modifying operations.

First, L12 gives `(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` at every transition. This yields the inclusion `Σ.L ⊆ Σ'.L` as partial functions: every existing entry persists in `dom(Σ'.L)` with its value unchanged. The remaining question is whether `dom(Σ'.L) ∖ dom(Σ.L)` can be non-empty at a K.μ⁺ or K.μ⁻ step — that is, whether either operation can add new links.

Second, we enumerate the link-modifying operations. The full operation vocabulary established by ASN-0093 and ASN-0047 is exactly {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ} — no other operations modify the system state. Among these, K.λ is the unique operation whose effect clause names `L`: K.λ's effect is `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}` (ASN-0093 K.λ). Every other operation's effect clause modifies only non-L state components — K.σ modifies `dom(M)` and `M(d_new)`; K.α modifies `C`; K.δ modifies `E` (and `M(d_new)` in the IsDocument case); K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L modify a specific `M(d)`; K.ρ modifies `R`. To close the argument we adopt *effect-clause exhaustivity*: an operation's stated effect clause names every state-component modification the operation makes, so any state component not named in the effect clause is unchanged across the transition. Under this convention, the absence of `L` from the effect clauses of K.μ⁺ and K.μ⁻ forces `dom(Σ'.L) = dom(Σ.L)` at K.μ⁺ and K.μ⁻ steps. Combined with L12, this gives `Σ.L = Σ'.L`.

We surface effect-clause exhaustivity explicitly because it is load-bearing for F9 in the absence of explicit `L' = L` clauses in ASN-0047's K.μ⁺ and K.μ⁻ frames. It is the standard reading of operation effect/frame pairs across this specification family — ASN-0093's K.σ, for instance, includes `L' = L` directly in its frame, demonstrating that frame clauses do list `L` when authors track the dependency — and ASN-0047's omission for K.μ⁺ and K.μ⁻ reads as a documentation gap that a revision adding `L' = L` to both frames would close cleanly. The convention is invoked once more in the Worked Example below, when re-evaluating the link store after a K.μ⁻ transition; outside these uses it does not propagate into the rest of the derivation.

We state F9 separately because it names the operation classes by which arrangements actually change, and so reads as a direct survivability promise: editing does not invalidate discovery. K.α, K.λ, K.δ, K.ρ, and K.σ touch one of the non-arrangement components and so fall outside F9's scope; the K.μ family is exactly the editing surface against which links must remain findable.

Across multi-step reachable sequences, link survivability is obtained by composing F9 over the K.μ-family steps and applying LP13 (UnconditionalLinkPersistence, ASN-0098) for the link-store-preserving guarantee across mixed step sequences. The V→I phase is sensitive to arrangement, of course — querying the same V-region before and after an edit may yield different I-images. But the link result for any *fixed* I-set is invariant under every K.μ-family step, and by composition under every reachable sequence whose link-store-modifying steps are accounted for separately. The two-phase factoring keeps these concerns separate: V-volatility lives in phase 1; phase 2 is arrangement-blind.

## Transclusion Transparency

When content at I-address `α` is transcluded into multiple documents, every V-position in every document that maps to `α` contributes `α` to its I-image when queried. Therefore the query result is the same regardless of which V-occurrence the reader queries:

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks({α}, Σ) is the same set regardless of whether α is queried via v₁ or v₂.
```

This is not an additional axiom — it follows from F1 (the match predicate consults coverage and `I`) together with the definition of `image`. How `α` came to be in `I` is invisible to phase 2. The match fires for every link whose endset covers `α`, regardless of which document supplied `α` to the query.

The corollary is the cross-document discoverability of links via shared content. A link created against `α`'s native location in `d_a` is found when querying `d_b`'s transclusion of `α`. The link does not "belong" to `d_a` in any sense visible to the discovery operation — it belongs to its home document by L1a (ASN-0043), but its *findability* is at the I-address, not at the document. The two-phase factoring makes this fall out without effort.

## Identity, Not Value

Two pieces of content with the same value but distinct I-addresses produce different query results. The match is on I-address identity, supplied by GlobalUniqueness (ASN-0034) and propagated through ContentImmutability (S0, ASN-0036):

```
F5 (IdentityNotValue):
   The match predicate matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·),
   never Σ.C(·). For distinct I-addresses α ≠ β, the tests matches(a, {α}, Σ)
   and matches(a, {β}, Σ) are therefore computed independently: each is decided
   by whether α (respectively β) lies in coverage(Σ.L(a).eᵢ) for some slot i,
   with no reference to the content values Σ.C(α) or Σ.C(β). Membership of a
   in findlinks({α}, Σ) and in findlinks({β}, Σ) is decided by these two
   independent address-level tests.
```

If two users at different addresses write the same string, the two strings have distinct I-addresses. Links to one are not links to the other. The discovery operation respects this distinction strictly: the match predicate examines coverage of address sets, not values of content. The content store `Σ.C` does not enter the match predicate at all.

This is the structural basis of attribution. Identity comes from origin, and origin is preserved through every operation that touches the content store (P0, ASN-0047). Discovery builds on this foundation; it does not erase it.

## Composite Queries

A query I-set may decompose into disjoint subsets, particularly when the V-region spans transclusions from multiple source documents. Suppose the reader's V-selection in `d` images to `I₁ ∪ I₂` with `I₁ ⊆ chain of A_C(d_a)` and `I₂ ⊆ chain of A_C(d_b)`. The match predicate handles this naturally:

```
F13 (SetAdditive):
   findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).
```

The derivation is immediate. By distributivity of intersection over union:

```
coverage(e) ∩ (I₁ ∪ I₂) = (coverage(e) ∩ I₁) ∪ (coverage(e) ∩ I₂)
```

The right-hand side is non-empty iff at least one disjunct is non-empty. So a link matches `I₁ ∪ I₂` iff it matches `I₁` or matches `I₂`, and the result is set-theoretic union.

The operation is therefore additive in its I-input. Multi-source content imposes no special machinery beyond the underlying span-set generalization. The same property propagates to V-region inputs: the I-image of a V-region union is the union of I-images (since `image` is the image-of-set under the function `Σ.M(d)`), so V-region union induces I-set union, and the result is union.

## The Empty Query

The empty query is a meaningful boundary, and the abstract specification handles it without ceremony. For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` has no witness, and `matches(a, ∅, Σ) = false` for every `a ∈ dom(Σ.L)`. The comprehension gives `findlinks(∅, Σ) = ∅`. Symmetrically, `image(∅, d, Σ) = {Σ.M(d)(v) : v ∈ ∅} = ∅`, so `findlinks_V(∅, d, Σ) = findlinks(∅, Σ) = ∅`.

The dual boundary is the empty link store. When `dom(Σ.L) = ∅`, the comprehension's source set is empty and `findlinks(I, Σ) = ∅` for every `I ⊆ T`. This is the bootstrap behaviour at the initial state Σ₀, where `L₀ = ∅` (ASN-0047): every query produces the empty result until the first K.λ allocates a link. F2 holds vacuously (the source set has no member to test); F3 holds vacuously (the result is empty); F10 and F11 hold vacuously for the same reason. The reader querying an empty docuverse receives an empty answer, consistent with the natural reading and with the absence of any structure for the query to discover.

The empty query is the additive identity in F13: `findlinks(∅ ∪ I₂, Σ) = findlinks(I₂, Σ) = ∅ ∪ findlinks(I₂, Σ) = findlinks(∅, Σ) ∪ findlinks(I₂, Σ)`. F2 holds vacuously (no link satisfies the predicate); F3 holds vacuously (the result is empty); F8 and F9 are trivial since both sides of every equality are empty. The reader who selects no V-positions receives no links, in agreement with the natural reading.

A third boundary belongs to the filtered form: the *empty constraint set*. When `C = ∅`, the universal `(A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` is vacuously true at every `a ∈ dom(Σ.L)`, so `findlinks_filtered(∅, Σ) = dom(Σ.L)`. A query with no constraints returns every link in the store, in agreement with the natural reading — restricting by nothing is the same as not restricting at all. This is the conjunctive dual of the empty I-set case for `findlinks`: the empty universal returns everything, the empty existential returns nothing.

## Scope

The operation may be restricted by a *scope* — a constraint on which links are considered. The default scope is `dom(Σ.L)` (the whole link store). The reader, or a higher-level system, may narrow it to a subset:

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

where `S ⊆ T` is any address set. Natural choices include "all links in document `d`" (`S = {a : home(a) = d}`), "all links by user `u`" (`S = {a : N(a) = n ∧ U(a) = u}`), or "all links allocated by some specified set of accounts".

Scope does not weaken the match predicate. A scoped query still requires full overlap-based matching; it merely restricts the candidate set. Completeness becomes completeness *within the scope*: every link in `S ∩ dom(Σ.L)` satisfying the match predicate must appear.

Scope is also where access control may live. A link in a private document, inaccessible to the querying user, may be excluded from the candidate set before the match predicate is applied. The match is unchanged; the candidate set is narrowed by the access-control predicate. We mention this but do not formalize access control here — it is a separate concern that composes with discovery rather than altering its semantics.

## Result Ordering

The result is a set, and a set carries no ordering. But the reader is shown an ordered list, and pagination demands that the order be stable across requests. We adopt the natural ordering: T1's lexicographic order on tumbler addresses. The result is presentable as a sequence:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence ⟨a₁, a₂, ..., aₙ⟩
   with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ), and a₁ < a₂ < ... < aₙ under T1.
```

Presentability as a finite sequence rests on finiteness, which we discharge explicitly. By F3, `result(I, Σ) ⊆ dom(Σ.L)`; by L-fin (ASN-0093), `|dom(Σ.L)| < ∞`; so `result(I, Σ)` is finite as a subset of a finite set. T1 (LexicographicOrder, ASN-0034) is a strict total order on `T`, and by trichotomy it restricts to a strict total order on any subset of `T`. A finite strictly totally ordered set has a unique enumeration in increasing order (the least element exists by well-orderedness of `T1`'s restriction, the second-least is the least of the remainder, and so on by finite induction). The ordering is therefore total, deterministic, and uniquely realized. Pagination is then well-defined: "the next N links past `aⱼ`" means the next N elements in the sorted sequence with addresses greater than `aⱼ` under T1.

The presentation order recovers a creation-order property within each home document. By SubAllocatorAxiom.ChainDiscipline (ASN-0093), each document `d`'s link sub-allocator chain `A_L(d)` is generated by repeated `inc(·, 0)` from the first emission `[d.0.s_L.1]`. ChainEnumerationInjectivity (ASN-0093) shows that this chain is strictly T1-increasing (per-step `inc(tₙ, 0) > tₙ` by TA5(a), lifted across arbitrary gaps by T1 transitivity). So sorting link addresses within a single home document by T1 yields exactly the order in which they were allocated.

For the cross-document part of the ordering claim, we derive that addresses with the same `home(·)` group together and that home documents themselves order lexicographically. ChainMembershipForOrigin (ASN-0093) places every link address `ℓ` with `home(ℓ) = d` in `A_L(d)`, and ChainPrefixExtension (ASN-0093) gives `b_L(d) ≼ ℓ` for every such `ℓ`. For two distinct documents `d₁ ≠ d₂`, CrossDocDisjointness (ASN-0093) supplies that `b_L(d₁)` and `b_L(d₂)` are non-nesting under `≼`. We must also lift the T1 order from documents to anchors: if `d₁ < d₂` under T1, then `b_L(d₁) < b_L(d₂)` under T1. In T1 case (i) on `d₁ < d₂`, the divergence position `k ≤ min(#d₁, #d₂)` with `d₁_k < d₂_k` carries over to `b_L(d₁) vs b_L(d₂)` at the same position, since each anchor agrees with its document on positions `1..#d`. In T1 case (ii), `d₁ ≺ d₂` (so `#d₁ < #d₂`) forces `d₂_{#d₁+1} ≥ 1` — both documents satisfy `zeros(·) = 2` by M0 (ASN-0093), so the proper extension cannot introduce a zero — and at position `#d₁+1`, `b_L(d₁)` has the appended `0` separator while `b_L(d₂)` has `d₂_{#d₁+1} ≥ 1`, yielding `b_L(d₁) < b_L(d₂)` by T1 case (i). With `b_L(d₁) < b_L(d₂)` and the anchors non-nesting, PrefixOrderingExtension (ASN-0034) lifts to every extension: every `ℓ₁` extending `b_L(d₁)` is strictly less than every `ℓ₂` extending `b_L(d₂)`. So under T1, link addresses with the same `home(·)` group together as a contiguous T1-block (all extending the common anchor `b_L(d)`), and the blocks for distinct documents sort by their documents' tumblers. The reader sees results in a canonical, repeatable order: links within a document in allocation order, documents in tumbler order.

## Persistent Discoverability

The link store is monotonic. Once a link is allocated, it persists with its endsets immutable. The match predicate consults only the endsets. Therefore:

```
F11 (PersistentDiscoverability):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with matches(a, I, Σ):
       a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

The conclusion is the multi-step lift of single-step link permanence. ASN-0098's LP13 (UnconditionalLinkPersistence) gives the dom-and-value part directly: for every reachable sequence `Σ →* Σ'` and every `a ∈ dom(Σ.L)`, `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. From per-link value equality, per-slot endset equality follows by component-wise tuple equality on `Link` values (L6, ASN-0043). LP3★ (multi-step coverage invariance, ASN-0098) then lifts per-slot endset equality to per-slot coverage equality across the sequence: `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` for every slot `i`. The match predicate's existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is therefore evaluated against identical per-slot coverages at Σ and Σ', and so yields the same Boolean against any fixed `I` — the witness slot found at Σ remains a witness at Σ'.

A link is permanently discoverable for any query I-set that overlaps any of its endset coverages. This is the discovery counterpart of link immutability: the link is not only structurally fixed, it is *findability-fixed*. Editing the documents around it, deleting the V-positions that arrange its referenced content, transcluding the content into new documents — none of these alter the link's match status against a fixed I-set.

The converse direction is also worth noting. Across a transition, new links may *enter* the result set (via K.λ adding a link whose endsets overlap `I`), but existing matching links cannot leave it. The result is monotonic in the link store. Phrased differently: if we hold `I` fixed and let `Σ` evolve, `findlinks(I, ·)` is monotone non-decreasing in `Σ.L`.

## A Worked Example

The abstract specification is short enough that it can read as content-free without an instance to anchor it. We fix a small one.

Consider a state `Σ` with two documents, both inhabiting `dom(Σ.M)`.

- `d_a` is a content-bearing document. Its content sub-allocator `A_C(d_a)` (ASN-0093) has produced three I-addresses: `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each placed into `dom(Σ.C)` by successive K.α steps with values `v₁, v₂, v₃ ∈ Val`. Its arrangement, by D-SEQ★ (ASN-0036), is `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}`, where `v_a^k = [s_C, 1, ..., 1, k]` is the canonical depth-`m_C` text-subspace V-position.

- `d_b` transcludes the latter two positions from `d_a`. Its arrangement is `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}`, sharing the I-addresses `α₂` and `α₃` with `d_a`. (No new content addresses were allocated for `d_b`; transclusion shares by reference. By P4★ (ASN-0047), `(α₂, d_b), (α₃, d_b) ∈ Σ.R`.)

- One link `ℓ ∈ dom(Σ.L)` with arity 3, allocated by some `K.λ` step under its home document:
  - Slot 1 (from-endset): one canonical span `(α₂, δ(1, #α₂))`, so `coverage(Σ.L(ℓ).e₁) = {t ∈ T : α₂ ≼ t}` by PrefixSpanCoverage (ASN-0043). The coverage is *not* the singleton `{α₂}` — it is the prefix-closure of `α₂`, containing `α₂` itself together with every tumbler extending `α₂` (e.g. `α₂.0`, `α₂.1`, `α₂.0.0`, …). Coverage of a canonical span is always a prefix-subtree, never a singleton; the singleton arises only when we intersect with a singleton query.
  - Slot 2 (to-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ).e₂) = {t ∈ T : α₃ ≼ t}` by the same reasoning.
  - Slot 3 (type-endset): some non-empty type endset whose coverage we leave abstract; assume it does not meet the content I-addresses we query.

The two prefix-subtrees are disjoint: `α₂` and `α₃` are both element-level tumblers of equal length with disagreeing final components (2 vs 3), so neither extends the other (`α₂ ⋠ α₃` and `α₃ ⋠ α₂`), and a tumbler cannot extend both simultaneously.

**Query 1: `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: the preconditions `d_a ∈ dom(Σ.M)` and `{v_a^2} ⊆ dom(Σ.M(d_a))` hold, so `image({v_a^2}, d_a, Σ) = {Σ.M(d_a)(v_a^2)} = {α₂}`. Phase 2: test each link in `dom(Σ.L)` against `I = {α₂}`. The only link is `ℓ`. At slot 1, `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅` (the only element of `{α₂}` that extends `α₂` is `α₂` itself, by reflexivity of `≼`), so the slot-existential fires and `matches(ℓ, {α₂}, Σ) = true`. The result is `{ℓ}`.

**Query 2: `findlinks_V({v_b^1}, d_b, Σ)`.** Phase 1: `image({v_b^1}, d_b, Σ) = {Σ.M(d_b)(v_b^1)} = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address as `d_a`'s native arrangement of `α₂`. Phase 2 is therefore identical to Query 1's Phase 2: result `{ℓ}`. This is F6 (TransclusionTransparency) in operation — the reader querying `d_b`'s view of `α₂` discovers the same link they would have discovered via `d_a`'s native arrangement, because identity travels with the I-address.

**Query 3: `findlinks_V({v_a^2, v_a^3}, d_a, Σ)`.** Phase 1: `image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}`. Phase 2: at `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂, α₃} = {t : α₂ ≼ t} ∩ {α₂, α₃} = {α₂} ≠ ∅` — `α₂ ≼ α₂` puts `α₂` in the intersection, while `α₂ ⋠ α₃` (last components disagree) excludes `α₃`. The existential is satisfied by slot 1 alone; we need not consult slot 2 (although it also fires: `{t : α₃ ≼ t} ∩ {α₂, α₃} = {α₃}` by the same reasoning). Result: `{ℓ}`. The link appears once, not twice — the result is a set.

**Verifying F13 (SetAdditive).** Compute each side separately. `findlinks({α₂}, Σ) = {ℓ}` (via slot 1: `{t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅`) and `findlinks({α₃}, Σ) = {ℓ}` (via slot 2: `{t : α₃ ≼ t} ∩ {α₃} = {α₃} ≠ ∅`); their union is `{ℓ}`. Independently, `findlinks({α₂, α₃}, Σ) = {ℓ}` — slot 1's coverage meets `{α₂, α₃}` in `{α₂}` and slot 2's meets it in `{α₃}`, either witness alone satisfying the existential. The two computations agree: `findlinks({α₂} ∪ {α₃}, Σ) = findlinks({α₂}, Σ) ∪ findlinks({α₃}, Σ) = {ℓ}`.

**Verifying F2 (Completeness) against the instance.** The set `dom(Σ.L) = {ℓ}` is the universe of candidates. For the query `{α₂}`, the match predicate fires at `ℓ`; F2 demands `ℓ ∈ result({α₂}, Σ)`. The comprehension `{a ∈ dom(Σ.L) : matches(a, {α₂}, Σ)}` evaluates to `{ℓ}`. Completeness holds.

**Verifying F3 (Soundness) against the instance.** The result `{ℓ}` is a subset of `dom(Σ.L)` (which contains only `ℓ`), and `matches(ℓ, {α₂}, Σ) = true` was verified above. No spurious link appears.

**Verifying F6 against the instance.** Queries 1 and 2 produce the same I-image `{α₂}` and hence the same result `{ℓ}`, despite the V-positions `v_a^2` and `v_b^1` belonging to different documents. The match predicate consulted only the I-image and the link store; the document of origin of the V-position vanished from the computation after Phase 1.

**Verifying F5 (IdentityNotValue) against the instance.** Slot 1's coverage is `{t : α₂ ≼ t}`, so `matches(ℓ, {α₂}, Σ) = true` (via slot 1: `α₂ ≼ α₂` puts `α₂` in the intersection with `{α₂}`) while `matches(ℓ, {α₃}, Σ) = true` only via slot 2 — the slot 1 test against `{α₃}` evaluates `{t : α₂ ≼ t} ∩ {α₃} = ∅` (since `α₂ ⋠ α₃`) and so does not fire. The slot 1 decision turns entirely on which I-addresses extend `α₂` as tumblers. The content values `v₂, v₃ ∈ Val` at `α₂, α₃` are never consulted: even if the writer of `d_a` had stored `v₂ = v₃` (the same value at distinct addresses), the slot 1 test would still discriminate `{α₂}` from `{α₃}` — the address-level intersection `{t : α₂ ≼ t} ∩ {α₃} = ∅` is decided by `α₂ ⋠ α₃` (their last components disagree, 2 vs 3), itself a consequence of GlobalUniqueness (ASN-0034) which forced these addresses to be distinct in the first place. F5 says the match predicate factors through the address space, not through the value space; this instance exhibits the factoring directly.

**Query 4: Survivability under arrangement edit (F11, F9).** Apply a K.μ⁻ transition to `d_a` retaining only the first content position: the post-state Σ' has `Σ'.M(d_a) = {v_a^1 ↦ α₁}`, with `v_a^2` and `v_a^3` removed from `dom(Σ'.M(d_a))` (so `α₂` and `α₃` are no longer in `ran(Σ'.M(d_a))`). The link store is untouched by K.μ⁻ — its effect clause names only `M(d_a)`, so by effect-clause exhaustivity (the convention surfaced in F9's derivation), `L' = L` — so `dom(Σ'.L) = {ℓ}` and `Σ'.L(ℓ) = Σ.L(ℓ)`. Re-evaluate `findlinks({α₂}, Σ')`: the match predicate at `ℓ` tests slot 1, `coverage(Σ'.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅`, so `matches(ℓ, {α₂}, Σ') = true`. The result is `{ℓ}`, the same as Query 1's pre-edit result.

This exercises F11 directly: the link survives the arrangement edit because its endset references `α₂`'s I-address (not `v_a^2`'s V-position), and `α₂`'s identity is preserved by content immutability (C0, ASN-0093). It also exercises F9 — the K.μ⁻ transition is a K.μ-family step satisfying F9's frame condition, so `findlinks({α₂}, Σ) = findlinks({α₂}, Σ')` is guaranteed before we re-evaluate the comprehension. The V-side query `findlinks_V({v_a^2}, d_a, Σ')` is now ill-formed in Phase 1 because `v_a^2 ∉ dom(Σ'.M(d_a))`; the reader who previously queried via `v_a^2` must now route through `d_b`'s transclusion (`findlinks_V({v_b^1}, d_b, Σ')` still images to `{α₂}` and recovers `ℓ`). The link's I-side identity persists; the V-side query surface has shrunk while the link-side survivability has not.

The example is small enough to inspect by eye, and the abstract definitions reduce to elementary set operations. Larger instances scale the same way: each link tests independently, slot existentials collect witnesses, and the comprehension assembles the answer.

## What Completeness Demands of Implementations

We have specified the result as a set. An implementation must produce exactly this set — no more, no fewer. The abstract specification is silent on *how* the set is computed.

Implementations commonly maintain indexes — auxiliary structures that map I-addresses to the links whose endsets cover them. An index makes the I→Link search fast at the cost of an obligation: the index must agree with the link store on every reachable state. This obligation is not an addition to the abstract spec; it is what the abstract spec demands of any index-based implementation. The spec's set comprehension is the answer; an index is just a means.

The implementation obligation has a concrete form. Each K.λ transition that adds a link `a` to `dom(Σ.L)` must arrange for `a` to be findable via every I-address in `coverage(Σ.L(a).eᵢ)` for every slot `i`. If the implementation maintains an index, every I-address in every endset's coverage must, by the end of the transition, point to `a` in the index. If multiple I-runs participate in a single endset's coverage (because the endset has multiple disjoint spans), each I-run requires its own index entry.

The obligation extends to durability: the index must survive any system event short of a fault that loses the link itself. If a crash leaves the link present and the index absent, the link is permanently undiscoverable through the index path. That state violates F2 if the implementation relies on the index for completeness. A conforming implementation must either guarantee atomic index-with-link write, or maintain a fallback path that reads the link store directly to recover from index incoherence.

We do not specify the mechanism. We specify the result. Any implementation whose `result(I, Σ)` differs from the set comprehension is non-conforming, regardless of cause.

## Local Atomicity and the Single-State Setting

The abstract specification is stated against a single state `Σ`. By the sequential-transition axiom (ASN-0093), every state transition is atomic and uninterruptible. The state `Σ` is well-defined at every point at which a query is evaluated.

A K.λ transition commits a link to `dom(Σ.L)` atomically. By the time the K.λ committing `a` returns, `a` is in `dom(Σ.L)`. The next query — at any state succeeding the K.λ — must include `a` in its result if `a` matches. There is no intermediate state in which `a` exists in `dom(Σ.L)` but is undiscoverable through the abstract operation.

This atomicity is what underwrites the *immediate* component of Nelson's "without appreciable delay" promise within a single instance. The query result reflects the current state's link store, fully and exactly. Implementations that defer index maintenance to a background process create a window in which the index lags the link store; during that window, results computed from the index would violate F2. The abstract specification permits no such window.

## What We Have Not Specified

We have not specified the procedure by which the operation is computed. We have not specified how the operation behaves across multiple physical instances of the link store, where partition tolerance and consistency models become relevant. We have not specified caching. We have not specified access control beyond noting it as an orthogonal scope filter.

We have not specified the inverse direction — the resolution of the result's endsets back to V-positions in the reader's document or in some target document. Once links are found, the reader typically wants to see where the other ends lead, which requires consulting `Σ.M(·)` to find V-positions whose I-image lies in the relevant endset coverage. That is the I→V resolution belonging to FOLLOWLINK/RETRIEVEENDSETS, and it has its own specification with its own subtleties (notably, the handling of I-addresses that no current arrangement maps).

We have not specified what FINDLINKS returns when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The match predicate still works mechanically — `coverage(e) ∩ I` is well-defined for any `I ⊆ T` — but the operational meaning of querying with phantom addresses is left unsettled.

## Reflection

The discovery operation reduces to a single set comprehension: take the I-set the user named (directly, or by V-projection through phase 1), test each link's endset coverage for overlap (the match predicate of phase 2), and return the matching links. The complexity of real systems lies entirely in the *implementation* — in maintaining indexes that make the comprehension fast, in propagating updates across servers, in handling access control, in managing the storage of large endsets. The abstract specification is just the comprehension.

That the specification is so spare is a consequence of design choices that began long before this operation. Because links attach to bytes (ASN-0043 L13), discovery can be by address overlap. Because bytes carry permanent identity (ASN-0036 S0, ASN-0093 C0), the overlap is well-defined and stable. Because arrangement is a separate concern from identity (ASN-0036 S9), discovery is arrangement-independent. Because the address space is globally unique (ASN-0034 T10), identity-based queries cannot collide across owners. Because the link store is monotonic (ASN-0093 L12), discovery is monotone in the link store. None of these properties were established for the sake of discovery; they were established for other reasons, and discovery falls out of them.

The reverse claim is equally true. None of these design choices could have been weakened without compromising discovery. If links attached to V-positions rather than I-addresses, editing would invalidate them. If content identity were not permanent, the match predicate would have no stable referent. If arrangement and identity were not separated, discovery would have to consult the arrangement and lose its key invariance property. The discovery operation is short because the architecture earned its shortness.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `image(R, d, Σ)` | I-image of a V-region: `{Σ.M(d)(v) : v ∈ R}` | introduced |
| `matches(a, I, Σ)` | Match predicate: `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` | introduced |
| `findlinks(I, Σ)` | Discovery operation: `{a ∈ dom(Σ.L) : matches(a, I, Σ)}` | introduced |
| `findlinks_V(R, d, Σ)` | Two-phase composite: `findlinks(image(R, d, Σ), Σ)` | introduced |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints `C` | introduced |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | introduced |
| F1 | Match predicate as set-theoretic overlap, existential over slots | introduced |
| F2 | Completeness: every matching link in `dom(Σ.L)` appears in the result | introduced |
| F3 | Soundness: every link in the result is in `dom(Σ.L)` and matches | introduced |
| F4 | Partial overlap suffices: any non-empty intersection forces a match | introduced |
| F5 | Identity, not value: the match consults coverage, not content values | introduced |
| F6 | Transclusion transparency: same I-address, same matches regardless of V-path | introduced |
| F7 | Endset symmetry: slots are equally searchable; filters conjoin | introduced |
| F8 | Determinism: `result(I, Σ)` is a function of `(Σ.L, I)` | introduced |
| F9 | Link survivability under edits: K.μ-family transitions preserve `findlinks(I, ·)` | introduced |
| F10 | Ordered result: canonical T1-sorted presentation | introduced |
| F11 | Persistent discoverability: matching at `Σ` implies matching at every `Σ'` reached from `Σ` | introduced |
| F12 | Two-phase factoring: `findlinks_V` composes `image` (V→I) and `findlinks` (I→Link) | introduced |
| F13 | Set-additive in the I-input: `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)` | introduced |
| F14 | Scope filter is intersection: `findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S` | introduced |

## Open Questions

What semantics should the operation have when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`?

What completeness guarantees must hold when the link store is logically partitioned across multiple physical instances that may be temporarily disconnected?

What consistency model must FINDLINKS observe with respect to K.λ operations that may be concurrent with or interleaved with the query at a higher protocol layer?

How does access-control filtering compose with the completeness obligation — is completeness restated relative to the authorized scope, and what invariants must the access-control layer preserve to make the composition coherent?

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?

What is the relationship between FINDLINKS and the inverse direction (resolving the result's endsets back to V-positions in some target document), and what additional guarantees does the inverse direction require that FINDLINKS does not?
