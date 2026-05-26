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
image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R}
```

The two preconditions are load-bearing: `d ∈ dom(Σ.M)` so that `Σ.M(d)` is defined as a partial function, and `R ⊆ dom(Σ.M(d))` so that every `Σ.M(d)(v)` is defined for `v ∈ R`. Without both, the comprehension is ill-formed. The reader's V-selection presupposes them — they query a position they can see, in a document that exists — but we state them explicitly because the operation has no value to take at positions outside the arrangement's domain. A query that nominates `v ∉ dom(Σ.M(d))` is either rejected at a higher protocol layer or treated as if `v` were absent from `R`; the abstract specification supports both treatments by leaving `image` undefined on such inputs rather than extending it with a sentinel. The image is a set of I-addresses, every member of which lies in `dom(Σ.C) ∪ dom(Σ.L)` by S3★ (ASN-0047). The phase reduces V-coordinates to address-of-content.

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, produce the set of links whose endsets intersect `I`:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

The two phases compose into the reader-facing operation:

```
findlinks_V(R, d, Σ) = findlinks(image(R, d, Σ), Σ)
```

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
matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)
```

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

A *slot constraint* is a pair `(i, J)` where `i` is a slot index and `J ⊆ T` is an I-set. A link satisfies the constraint iff `coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅`. The reader may supply any conjunction of slot constraints:

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

where `C` is a finite set of slot constraints. The from-to query "links from `I_from` to `I_to`" is the constraint set `{(1, I_from), (2, I_to)}`. The three-endset query adds `(3, I_type)`. A query that restricts only by type is `{(3, I_type)}` — the from and to slots are unconstrained, so the link matches regardless of where its from and to endsets land.

The filtered form is *not* a strict generalization of the unfiltered form: the unfiltered match is an existential over slots (a link matches if *any* slot's coverage meets `I`), while the filtered match is a universal over constraints (a link matches if *every* `(i, J)` is satisfied at slot `i`). The two are structurally distinct — disjunction versus conjunction — and no single conjunctive constraint set over the present `C`-vocabulary recovers the disjunction. The unfiltered form is instead recovered as a *union* over single-slot filters: `findlinks(I, Σ) = ⋃ᵢ findlinks_filtered({(i, I)}, Σ)`, where the union ranges over the slot indices of each link. Extending the constraint vocabulary to admit per-slot disjunctions would close the gap structurally, but the present spec keeps the two operations side by side, with the explicit conversion above.

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

The operation's defining obligation is *completeness*: every link in `dom(Σ.L)` satisfying the match predicate must appear in the result. The promise is to the reader, who is told that the link mechanism ties together the corpus and that the system will return all connections to the queried content. A link that exists in the link store and that touches the queried I-set, but that fails to appear in the result, is a violation of the reader's promise.

We state completeness as a property of the result set rather than of any search procedure. Define `result(I, Σ)` to be the output of the unfiltered FINDLINKS on query `I` and state `Σ`. Completeness is then:

```
F2 (Completeness):
   For every a ∈ dom(Σ.L): matches(a, I, Σ) ⟹ a ∈ result(I, Σ).
```

For the filtered form, completeness reads against the filtered predicate: every link satisfying every constraint in `C` appears in `result(C, Σ)`.

The dual obligation is *soundness*:

```
F3 (Soundness):
   For every a ∈ result(I, Σ): a ∈ dom(Σ.L) ∧ matches(a, I, Σ).
```

A link that appears in the result but does not match is also a violation. Completeness and soundness together pin the result to a single set; there is exactly one correct answer.

**F2 and F3 as tautologies of the definition.** Both follow immediately from the abstract specification `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}`. Completeness: a comprehension by construction contains every element of its source set satisfying the predicate, so every `a ∈ dom(Σ.L)` with `matches(a, I, Σ)` is included. Soundness: the source restriction places every result in `dom(Σ.L)` and the predicate guard ensures the match. At the level of the abstract definition the two are trivial; they acquire force only as implementation obligations that constrain *how* the comprehension is computed.

Completeness must hold *unconditionally* with respect to the population of `dom(Σ.L)`. The number of non-matching links is irrelevant — performance is an implementation property, completeness is a correctness property. The operation cannot terminate early after collecting "enough" links, cannot omit links by random sampling, cannot drop links because they are stored on a remote server that is slow to answer, and cannot exclude links because their endsets are large. If the link is in the store and the match holds, the link is in the result. Soundness's force is dual: a conforming implementation cannot return links that fail the match — no false positives from a stale index, no extras from an over-approximating filter — and so the implementation's index, if any, must remain in lockstep with the link store rather than offering a superset.

## Determinism

The result depends only on the link store and the query specification. It does not depend on any history, any cached state, any concurrent activity, or any implementation choice not visible to the abstract specification:

```
F8 (Determinism):
   result(I, Σ) = result(I, Σ')  whenever Σ.L = Σ'.L.
```

Determinism is structurally guaranteed by the form of `matches`. The derivation chain unfolds step by step. From `Σ.L = Σ'.L`, equality of partial functions gives `dom(Σ.L) = dom(Σ'.L)` and `(A a ∈ dom(Σ.L) :: Σ.L(a) = Σ'.L(a))`. Per-link, component-wise tuple equality on `Link` values (L6, ASN-0043) gives per-slot agreement `Σ.L(a).eᵢ = Σ'.L(a).eᵢ` for every `i ∈ {1, …, |Σ.L(a)|}`. The `coverage(·)` operator is a deterministic function of its argument endset (it takes the union of T1-half-open intervals over the endset's spans), so per-slot endset equality yields per-slot coverage equality `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`. The predicate `matches(a, I, Σ) ≡ (E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is then point-wise equal at the two states for every `a ∈ dom(Σ.L)`. Set extensionality applied to the comprehensions `{a ∈ dom(Σ.L) : matches(a, I, Σ)}` and `{a ∈ dom(Σ'.L) : matches(a, I, Σ')}` (with equal source sets and equal predicates) closes the chain: the result sets are equal.

A direct consequence: the two phases compose unambiguously. Once `I = image(R, d, Σ)` is computed, the I-Link search is determined by `Σ.L`. Two different ways of arriving at the same `I` produce the same result. If a reader at state `Σ` and another reader at state `Σ'` both produce the I-set `I` (perhaps because their respective documents transclude overlapping content), they receive the same result if `Σ.L = Σ'.L`.

## Arrangement Independence

The I→Link phase consults `Σ.L` and `I` alone. It does not consult any arrangement. We can therefore strengthen determinism:

```
F9 (ArrangementIndependence):
   For any Σ, Σ' with Σ.L = Σ'.L: findlinks(I, Σ) = findlinks(I, Σ').
```

This invariance is the structural foundation of link survivability. Editing operations — INSERT, DELETE, REARRANGE, all of the K.μ family — alter arrangements but cannot alter `Σ.L` (L12, ASN-0093). Therefore none of them alter which links match a given I-set. The link's endsets, fixed at creation time, continue to reference the same I-addresses; the match predicate continues to identify the same links.

The V→I phase is sensitive to arrangement, of course. If the reader queries the same V-region before and after an edit, the I-image may change because the arrangement has changed. But the link result for any *fixed* I-set is invariant. The two-phase factoring keeps these concerns separate: V-volatility lives in phase 1; phase 2 is arrangement-blind.

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
   For I-addresses α ≠ β, the result sets findlinks({α}, Σ) and findlinks({β}, Σ)
   are independent: a link belongs to one or the other (or both, or neither) based
   entirely on whether its endset coverage includes α or β, with no consultation of
   Σ.C(α) or Σ.C(β).
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

The empty query is the additive identity in F13: `findlinks(∅ ∪ I₂, Σ) = findlinks(I₂, Σ) = ∅ ∪ findlinks(I₂, Σ) = findlinks(∅, Σ) ∪ findlinks(I₂, Σ)`. F2 holds vacuously (no link satisfies the predicate); F3 holds vacuously (the result is empty); F8 and F9 are trivial since both sides of every equality are empty. The reader who selects no V-positions receives no links, in agreement with the natural reading.

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

The presentation order recovers a creation-order property within each home document. By SubAllocatorAxiom.ChainDiscipline (ASN-0093), each document `d`'s link sub-allocator chain `A_L(d)` is generated by repeated `inc(·, 0)` from the first emission `[d.0.s_L.1]`. ChainEnumerationInjectivity (ASN-0093) shows that this chain is strictly T1-increasing (per-step `inc(tₙ, 0) > tₙ` by TA5(a), lifted across arbitrary gaps by T1 transitivity). So sorting link addresses within a single home document by T1 yields exactly the order in which they were allocated. Across home documents, T1 sorts by document prefix — addresses with the same `home(·)` group together, and home documents themselves order lexicographically. The reader sees results in a canonical, repeatable order: links within a document in allocation order, documents in tumbler order.

## Persistent Discoverability

The link store is monotonic. Once a link is allocated, it persists with its endsets immutable. The match predicate consults only the endsets. Therefore:

```
F11 (PersistentDiscoverability):
   For any state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with matches(a, I, Σ):
       a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

This follows from L12 (ASN-0093): `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`, so the coverage of every endset of `a` is unchanged across the transition. The match predicate against the same `I` therefore yields the same Boolean.

A link is permanently discoverable for any query I-set that overlaps any of its endset coverages. This is the discovery counterpart of link immutability: the link is not only structurally fixed, it is *findability-fixed*. Editing the documents around it, deleting the V-positions that arrange its referenced content, transcluding the content into new documents — none of these alter the link's match status against a fixed I-set.

The converse direction is also worth noting. Across a transition, new links may *enter* the result set (via K.λ adding a link whose endsets overlap `I`), but existing matching links cannot leave it. The result is monotonic in the link store. Phrased differently: if we hold `I` fixed and let `Σ` evolve, `findlinks(I, ·)` is monotone non-decreasing in `Σ.L`.

## A Worked Example

The abstract specification is short enough that it can read as content-free without an instance to anchor it. We fix a small one.

Consider a state `Σ` with two documents, both inhabiting `dom(Σ.M)`.

- `d_a` is a content-bearing document. Its content sub-allocator `A_C(d_a)` (ASN-0093) has produced three I-addresses: `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each placed into `dom(Σ.C)` by successive K.α steps with values `v₁, v₂, v₃ ∈ Val`. Its arrangement, by D-SEQ★ (ASN-0036), is `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}`, where `v_a^k = [s_C, 1, ..., 1, k]` is the canonical depth-`m_C` text-subspace V-position.

- `d_b` transcludes the latter two positions from `d_a`. Its arrangement is `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}`, sharing the I-addresses `α₂` and `α₃` with `d_a`. (No new content addresses were allocated for `d_b`; transclusion shares by reference. By P4★ (ASN-0047), `(α₂, d_b), (α₃, d_b) ∈ Σ.R`.)

- One link `ℓ ∈ dom(Σ.L)` with arity 3, allocated by some `K.λ` step under its home document:
  - Slot 1 (from-endset): one canonical span `(α₂, δ(1, #α₂))`, so `coverage(Σ.L(ℓ).e₁) = {α₂}` by PrefixSpanCoverage (ASN-0043).
  - Slot 2 (to-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ).e₂) = {α₃}`.
  - Slot 3 (type-endset): some non-empty type endset whose coverage we leave abstract; assume it does not meet the content I-addresses we query.

**Query 1: `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: the preconditions `d_a ∈ dom(Σ.M)` and `{v_a^2} ⊆ dom(Σ.M(d_a))` hold, so `image({v_a^2}, d_a, Σ) = {Σ.M(d_a)(v_a^2)} = {α₂}`. Phase 2: test each link in `dom(Σ.L)` against `I = {α₂}`. The only link is `ℓ`. At slot 1, `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {α₂} ∩ {α₂} = {α₂} ≠ ∅`, so the slot-existential fires and `matches(ℓ, {α₂}, Σ) = true`. The result is `{ℓ}`.

**Query 2: `findlinks_V({v_b^1}, d_b, Σ)`.** Phase 1: `image({v_b^1}, d_b, Σ) = {Σ.M(d_b)(v_b^1)} = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address as `d_a`'s native arrangement of `α₂`. Phase 2 is therefore identical to Query 1's Phase 2: result `{ℓ}`. This is F6 (TransclusionTransparency) in operation — the reader querying `d_b`'s view of `α₂` discovers the same link they would have discovered via `d_a`'s native arrangement, because identity travels with the I-address.

**Query 3: `findlinks_V({v_a^2, v_a^3}, d_a, Σ)`.** Phase 1: `image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}`. Phase 2: at `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂, α₃} = {α₂} ∩ {α₂, α₃} = {α₂} ≠ ∅`. The existential is satisfied by slot 1 alone; we need not consult slot 2 (although it also fires, with `{α₃}` as witness). Result: `{ℓ}`. The link appears once, not twice — the result is a set.

**Verifying F13 (SetAdditive).** Compute each side separately. `findlinks({α₂}, Σ) = {ℓ}` (via slot 1) and `findlinks({α₃}, Σ) = {ℓ}` (via slot 2); their union is `{ℓ}`. Independently, `findlinks({α₂, α₃}, Σ) = {ℓ}` (via slot 1's intersection with `{α₂}`, or via slot 2's with `{α₃}`). The two computations agree: `findlinks({α₂} ∪ {α₃}, Σ) = findlinks({α₂}, Σ) ∪ findlinks({α₃}, Σ) = {ℓ}`.

**Verifying F2 (Completeness) against the instance.** The set `dom(Σ.L) = {ℓ}` is the universe of candidates. For the query `{α₂}`, the match predicate fires at `ℓ`; F2 demands `ℓ ∈ result({α₂}, Σ)`. The comprehension `{a ∈ dom(Σ.L) : matches(a, {α₂}, Σ)}` evaluates to `{ℓ}`. Completeness holds.

**Verifying F3 (Soundness) against the instance.** The result `{ℓ}` is a subset of `dom(Σ.L)` (which contains only `ℓ`), and `matches(ℓ, {α₂}, Σ) = true` was verified above. No spurious link appears.

**Verifying F6 against the instance.** Queries 1 and 2 produce the same I-image `{α₂}` and hence the same result `{ℓ}`, despite the V-positions `v_a^2` and `v_b^1` belonging to different documents. The match predicate consulted only the I-image and the link store; the document of origin of the V-position vanished from the computation after Phase 1.

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
| F9 | Arrangement independence: same `Σ.L` and same `I` give same result, irrespective of `Σ.M` | introduced |
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
