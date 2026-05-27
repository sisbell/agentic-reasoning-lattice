# ASN-0099: FINDLINKS Operation

*2026-05-26*

## The Reader's Question

The reader looks at a stretch of content in their document and asks: *what connects here from elsewhere?* This is one half of the central reader-side promise of a Xanadu-style system — that the literature is bidirectionally navigable, that the links from the rest of the docuverse to the content in front of me must be findable on demand and without appreciable delay. We adopt this as our starting obligation. The user supplies a region of arranged content; the system must return every link whose endsets touch that content.

The reader knows only what they see. They see arranged content — a stretch of V-positions in some document `d`. They do not see I-addresses directly, do not see the content store, do not see other documents' arrangements, and they certainly do not see the link store. The query is in V-coordinates of `d`.

The links the reader wants live in `dom(Σ.L)`. By L1 (ASN-0043), each is at an element-level tumbler address, and by L3 carries a sequence of endsets whose spans reference content I-addresses, not V-positions. The first problem is therefore one of identity reconciliation: the reader's V-coordinates and the link store's I-coordinates speak different languages. The arrangement `Σ.M(d)` is the bridge between them.

## A Two-Phase Factoring

Before any formalism, let us recognize that the question splits cleanly into two phases with qualitatively different concerns. We separate them deliberately so each can be analyzed without the other underfoot.

**Phase 1 (V→I).** Given a document `d ∈ dom(Σ.M)` and a query region `R ⊆ T`, produce the *I-image* of the region:

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

The single precondition `d ∈ dom(Σ.M)` is load-bearing so that `Σ.M(d)` is defined as a partial function. The comprehension silently projects `R` onto `dom(Σ.M(d))`: V-positions in `R` that are absent from the arrangement contribute nothing to the image. We choose silent projection deliberately. A V-position outside the arrangement's domain has no I-address to map to, and no I-address can encode "this V-position", so omitting such positions from the image is the only treatment that leaves the operation total over `R ⊆ T` without introducing a sentinel value. The treatment matches the system's natural reading at both extremes: an empty `R` produces an empty image, and an `R` that intersects the arrangement in a non-empty subset produces the image of that subset. The image is a set of I-addresses, every member of which lies in `dom(Σ.C) ∪ dom(Σ.L)` by S3★ (ASN-0047). The phase reduces V-coordinates to address-of-content.

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, produce the set of links whose endsets intersect `I`:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

The two phases compose into the reader-facing operation:

```
F12 (TwoPhaseFactoring):
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

The single precondition is inherited from `image`'s `defined when` clause — `findlinks_V` is well-formed precisely when `image(R, d, Σ)` is. We restate it at the composite to keep the document-existence requirement visible at the call site. V-positions in `R` that lie outside `dom(Σ.M(d))` are silently projected away by `image` and do not impose a pre-validation obligation on the caller; this is the only treatment that gives a total operation over `R ⊆ T` for a fixed allocated document.

The factoring matters because the two phases have entirely different stability properties. The arrangement `Σ.M` is mutable: K.μ⁺, K.μ⁻, K.μ~, and K.μ⁺_L all modify it. The link store `Σ.L` is monotonic: K.λ adds to it, and L12 (ASN-0093) forbids any modification of existing entries. Phase 1 consults the mutable component; phase 2 consults the monotonic component. This separation will let us conclude later that link discovery is fundamentally a property of `(Σ.L, I)`, with the arrangement entering only to translate V-input into I-input.

We will spend most of our effort on phase 2. Phase 1 is a finite lookup once the arrangement is fixed; it has no degrees of freedom to analyze.

## The Image Set

The V-region `R` need not be contiguous, nor confined to the arrangement's current domain. The reader may select a single position, a contiguous V-span, or any subset of `T`; `image` projects `R` onto `dom(Σ.M(d))` and consults only the surviving intersection. We do not constrain `R` beyond `R ⊆ T`.

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

F1's slot-existential together with its intersection (rather than containment) form is exactly the minimal sufficient match condition: any non-empty intersection `coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅` at any slot `i` already witnesses the existential and forces `matches(a, I, Σ)` to hold. We surface this as a labeled claim:

```
F4 (MatchFormulaUniqueness):
   The match predicate of F1 is uniquely fixed by the reader's promise. No
   strengthened condition — `coverage(Σ.L(a).eᵢ) ⊆ I`, `I ⊆ coverage(Σ.L(a).eᵢ)`,
   `|coverage(Σ.L(a).eᵢ) ∩ I| ≥ k` for any fixed `k > 1`, or any other
   refinement that excludes at least one singleton-overlap pair `(eᵢ, I)` — is
   a refinement of F1. Any such alternative defines a different match
   predicate and therefore (via F2 ∧ F3) a different — and, with respect to
   F1, incomplete — conforming result set.
```

The derivation is immediate from F1 under existential introduction: any singleton overlap at any slot satisfies F1's predicate, so any predicate that fails to recognize at least one such overlap excludes a link that F1 includes. The reader's promise rests on this singleton-overlap reading, as argued above for the "Why intersection" choice: a link is about every byte its endset names (L13, ASN-0043), and one shared byte is one shared byte. F4 records that this minimality is not optional: alternative match formulas are alternative operations, not alternative implementations of FINDLINKS. Conforming implementations are bound to F1 as the unique match predicate against which F2 ∧ F3 are evaluated.

**Empty endsets at non-type slots.** L3 (ASN-0043) requires only the type-endset (slot 3) to be non-empty; any other slot may carry the empty endset. An empty endset has `coverage(∅) = ∅` (the empty union), so the intersection `coverage(Σ.L(a).eᵢ) ∩ I = ∅` for every `I` whenever `Σ.L(a).eᵢ = ∅`. The slot-existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is therefore never witnessed by an empty slot — but other non-empty slots of the same link may still witness it. The match predicate accommodates empty endsets mechanically: a link with `Σ.L(a).e₁ = ∅` and a non-empty `Σ.L(a).e₂` whose coverage meets `I` still matches `I`, via slot 2. The filtered form behaves differently: a filter constraint `(i, J)` is satisfied at slot `i` iff `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅`, and when `Σ.L(a).eᵢ = ∅` the right conjunct is false for every `J`, so any constraint naming slot `i` is unsatisfiable at that link. A filtered query that explicitly nominates an empty slot therefore excludes the link from its result, even when other slots' coverages would have admitted it under the unfiltered match.

## Endset Filtering

The reader may not want every link that touches `I`. They may want only links *from* the queried region, or only links *of type θ*, or "from `I_from` to `I_to`". We generalize the match predicate to admit per-slot constraints.

A *slot constraint* is a pair `(i, J)` where `i ∈ ℕ⁺` is a slot index and `J ⊆ T` is an I-set. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. The positional accessor `Σ.L(a).eᵢ` is undefined for `i > |Σ.L(a)|` (L6, ASN-0043), so we fold the out-of-range case into the per-constraint conjunct as an explicit guard — a link with too few slots fails any constraint that references a slot it does not have. The reader may supply any conjunction of slot constraints:

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C :
                       i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

where `C` is a finite set of slot constraints. The conjunct `i ≤ |Σ.L(a)| ∧ ...` keeps the comprehension well-formed at every `a ∈ dom(Σ.L)`: when `i > |Σ.L(a)|`, the left conjunct is false and short-circuits the undefined accessor, so the per-constraint clause evaluates to false without consulting `Σ.L(a).eᵢ`. The from-to query "links from `I_from` to `I_to`" is the constraint set `{(1, I_from), (2, I_to)}`. The three-endset query adds `(3, I_type)`. A query that restricts only by type is `{(3, I_type)}` — the from and to slots are unconstrained, so the link matches regardless of where its from and to endsets land.

The filtered form is *not* a strict generalization of the unfiltered form: the unfiltered match is an existential over slots (a link matches if *any* slot's coverage meets `I`), while the filtered match is a universal over constraints (a link matches if *every* `(i, J)` is satisfied at slot `i`). The two are structurally distinct — disjunction versus conjunction — and no single conjunctive constraint set over the present `C`-vocabulary recovers the disjunction. The unfiltered form is instead recovered as a *finite* union over single-slot filters:

```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

L-fin (ASN-0093) gives finiteness of `dom(Σ.L)`, so the maximum is well-defined whenever the link store is non-empty; L3 (ASN-0043) gives `N ≥ 3` in that case. A link `a` with `|Σ.L(a)| = n` participates in `findlinks_filtered({(i, I)}, Σ)` for `i ∈ {1, …, n}` only — for `i > n`, the constraint references a slot absent from `a` and is unsatisfiable. The union is therefore finite by construction with at most `N` terms. Extending the constraint vocabulary to admit per-slot disjunctions would close the gap structurally, but the present spec keeps the two operations side by side, with the explicit conversion above.

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

The I→Link phase consults `Σ.L` and `I` alone. It does not consult any arrangement. F8 already encodes this in its hypothesis `Σ.L = Σ'.L`: `Σ.M` is unmentioned, so two states agreeing on the link store give equal results regardless of how their arrangements differ. Before stating the operationally salient specialisation as the frame condition exercised by editing operations, we surface one structural premise on which the derivation of survivability rests.

Operation effects/frames in this specification family are stated by ASN-0093 and ASN-0047 in side-by-side fashion: an *effect* clause names what changes, and a *frame* clause names what does not. ASN-0093's operation specifications list every preserved component explicitly — K.σ, for instance, ends its frame with `L' = L`. Several operations in ASN-0047 omit `L` from their published frames: K.μ⁺ (its frame names only `C`, `E`, `R`, and per-document arrangement), K.μ⁻ (likewise), and K.ρ (whose frame names only `C`, `E`, and per-document arrangement). To bridge this gap we make explicit the interface contract that every operation specification in V must satisfy:

```
A1 (EffectClauseExhaustivity):
   Vocabulary scope (scope of the contract): The operation vocabulary V
   of the substrate is whatever set of operations is currently published
   across ASN-0047 and ASN-0093. At the time this ASN was written, that
   set is V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ}; this
   enumeration is illustrative, not constraining. A1 binds the current
   vocabulary whatever it may be — the listed set is not frozen against
   substrate evolution. No operation outside the current V exists in the
   substrate.

   Contract (obligation on every operation specification in V): The
   operation's stated effect clause must name every state-component
   modification the operation makes. Equivalently: any state component
   not appearing in either the effect clause or the frame clause is
   required to be unchanged across the transition. An operation
   specification whose published effect clause omits a modification it
   actually performs is non-conforming.

   Propagation (binding force across revisions): The exhaustivity
   obligation applies to every operation in the substrate's current
   vocabulary at every state of substrate evolution. If V is extended by
   future revision — a new operation added, an existing operation
   replaced — every operation in the revised V inherits the same
   exhaustivity obligation. The propagation clause overrides any
   reading of the vocabulary-scope clause that would freeze A1's reach
   to the operations enumerated above.
```

A1 is not a passive observation about current text — it is an explicit interface contract that every operation specification in V must satisfy, and that this ASN treats as part of the published interface against which it specifies FINDLINKS. Three consequences follow.

*First, A1 is the obligation discharged differently by ASN-0093 and ASN-0047.* ASN-0093's K.σ honours the contract directly by listing `L' = L` in its frame; the K.σ specification is conforming on the contract's own terms with no further argument required. ASN-0047's K.μ⁺, K.μ⁻, and K.ρ leave `L` unmentioned in their published frames; under A1 this silence is constrained to mean *no modification*, and any implementation of these operations that modifies `L` violates the contract and is non-conforming. The contract is therefore the bridge across which this ASN's derivations transport the unmentioned `L' = L` conjunct from ASN-0047's frames into F9's `Σ.L = Σ'.L` hypothesis.

*Second, A1's propagation clause makes the contract binding on future revisions.* If the substrate vocabulary is later extended — a new operation `K.foo` added to V — that operation's specification must publish its `L`-behaviour (and the behaviour of every other state component) explicitly to satisfy A1. The contract does not weaken or expand with vocabulary growth; new operations inherit the same exhaustivity obligation, and the propagation clause is explicit that this binding overrides any reading of the vocabulary-scope clause that would freeze A1's reach to the operations currently enumerated. Likewise, if any existing operation in V is revised to modify a previously-unmentioned component, the revision is non-conforming until the published effect clause is updated.

*Third, A1's load-bearing role is bounded and can be discharged by ASN-0047 revision.* A1 is load-bearing in this ASN for exactly three operations of V: K.μ⁺, K.μ⁻, and K.ρ. F9's derivation invokes A1 at the K.μ⁺ and K.μ⁻ cases; the K.ρ case enters via the unified corollary to F9 (below) and is reused for K.ρ in any composite that records provenance. Query 4 of the Worked Example exercises K.μ⁻. The natural path to eliminate A1 from this ASN's derivations is the ASN-0047 revision proposed in the Open Questions: adding `L' = L` to K.μ⁺'s, K.μ⁻'s, and K.ρ's published frames discharges F9's hypothesis from each operation's own text rather than through A1, after which A1 reverts to a recorded contract with no active deductive role. Until that revision lands, A1 stands as the contract this ASN consumes from ASN-0047 (and ASN-0093), and downstream ASNs that consume F9 inherit the same contract.

We now state the specialisation:

```
F9 (LinkSurvivabilityUnderEdits):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d — K.μ⁺ (content extension), K.μ⁻ (contraction),
   K.μ~ (reordering), or K.μ⁺_L (link extension) — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   Premise: A1 (EffectClauseExhaustivity), invoked at the K.μ⁺ and K.μ⁻
   sub-cases of the derivation below.
```

F9 follows from F8 once we observe that `Σ'.L = Σ.L` at every K.μ-family transition. The derivation splits into two cases.

*K.μ~ and K.μ⁺_L.* These operations state `L' = L` explicitly in their frame clauses (ASN-0047), so the F8 hypothesis is satisfied directly from the published frame.

*K.μ⁺ and K.μ⁻.* These operations do not list `L` in their published frames in ASN-0047 — their frames cover `C`, `E`, `R`, and the per-document arrangement clause `(A d' : d' ≠ d : M'(d') = M(d'))`, but say nothing about `L`. We derive `Σ.L = Σ'.L` by combining L12 (LinkImmutability, ASN-0093) with A1.

First, L12 gives `(A a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` at every transition. This yields the inclusion `Σ.L ⊆ Σ'.L` as partial functions: every existing entry persists in `dom(Σ'.L)` with its value unchanged. The remaining question is whether `dom(Σ'.L) ∖ dom(Σ.L)` can be non-empty at a K.μ⁺ or K.μ⁻ step — that is, whether either operation can add new links.

Second, we enumerate the link-modifying operations. The full operation vocabulary is exactly {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ} — no other operations modify the system state. Among these, K.λ is the unique operation whose effect clause names `L`: K.λ's effect is `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}` (ASN-0093 K.λ). Every other operation's effect clause modifies only non-L state components — K.σ modifies `dom(M)` and `M(d_new)`; K.α modifies `C`; K.δ modifies `E` (and `M(d_new)` in the IsDocument case); K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L modify a specific `M(d)`; K.ρ modifies `R`. Invoking A1, the absence of `L` from the effect clauses of K.μ⁺ and K.μ⁻ forces `dom(Σ'.L) = dom(Σ.L)` at K.μ⁺ and K.μ⁻ steps. Combined with L12, this gives `Σ.L = Σ'.L`.

We state F9 separately because it names the operation classes by which arrangements actually change, and so reads as a direct survivability promise: editing does not invalidate discovery. K.α, K.λ, K.δ, K.ρ, and K.σ touch one of the non-arrangement components and so fall outside F9's scope; the K.μ family is exactly the editing surface against which links must remain findable.

```
F9-cor (NonAllocatingPreservation):
   For every single-step transition Σ → Σ' produced by an operation in
   V ∖ {K.λ} — that is, every substrate operation other than the unique
   link-allocating operation K.λ — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').
```

By F8, it suffices to verify `Σ.L = Σ'.L` at every such transition. Splitting V ∖ {K.λ} by the source of the preservation: K.σ, K.α, K.δ, K.μ~, and K.μ⁺_L each name `L' = L` directly in the published frame; K.μ⁺, K.μ⁻, and K.ρ omit `L` from the published frame and inherit `Σ.L = Σ'.L` from the L12 + A1 derivation given for K.μ⁺/K.μ⁻ above, with K.ρ's argument structurally identical (its effect modifies only `R`, so A1 forces `dom(Σ'.L) = dom(Σ.L)`, and L12 fixes the values).

K.δ has three sub-cases (IsNode, IsAccount, IsDocument), and the IsDocument sub-case modifies `M(d_new)` (setting it to `∅`) in addition to extending `E`. F9-cor's conclusion `findlinks(I, Σ) = findlinks(I, Σ')` is unaffected by this M-modification: the comprehension `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` consults only `dom(Σ.L)`, the link values `Σ.L(a)`, and the query I-set, never `Σ.M`. K.δ's published frame includes `L' = L` uniformly across its three sub-cases, so F8's hypothesis `Σ.L = Σ'.L` is satisfied for K.δ as a whole regardless of which sub-case fires. (The V-side companion claim — that `findlinks_V(R, d, Σ) = findlinks_V(R, d, Σ')` across a K.δ-IsDocument step that introduces a fresh document — is the subject of ASN-0098's LP8 and is not what F9-cor asserts; F9-cor scopes to the I-level operation.)

F9-cor surfaces the full dependency surface of A1 in one place: only K.μ⁺, K.μ⁻, and K.ρ require A1 to discharge the F8 hypothesis. K.λ is the only operation of V that can change `findlinks(I, ·)` across a single step, and F19 below confirms that the change is monotone — additions only, never removals.

F9 lifts to multi-step sequences only under restrictive conditions. Operationally relevant sequences interleave K.λ with K.μ-family steps, and a K.λ step that allocates a new matching link adds to the result without removing anything — so findlinks-equality fails along the direction of strict growth. The multi-step claim that holds across every reachable sequence is the weaker inclusion `findlinks(I, Σ) ⊆ findlinks(I, Σ')`, which is F11 (PersistentDiscoverability) below; F11's derivation uses LP13 (UnconditionalLinkPersistence, ASN-0098) and does not invoke F9. The pure-K.μ inductive composition of F9 across edit-only sequences (each step's `Σᵢ.L = Σᵢ₊₁.L` chaining by transitivity into F8 over the endpoints) is a structural completeness observation rather than an operationally needed claim; we note it here but do not develop it further.

The V→I phase is sensitive to arrangement, of course — querying the same V-region before and after an edit may yield different I-images. But the link result for any *fixed* I-set is invariant under every K.μ-family step and monotone non-decreasing across every reachable sequence. The two-phase factoring keeps these concerns separate: V-volatility lives in phase 1; phase 2 is arrangement-blind in the K.μ-only setting and monotone in the general setting.

## Transclusion Transparency

When content at I-address `α` is transcluded into multiple documents, every V-position in every document that maps to `α` contributes `α` to its I-image when queried. Therefore the query result is the same regardless of which V-occurrence the reader queries:

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

The derivation chain unfolds in three steps. Direct evaluation of `image` on each singleton gives `image({v₁}, d₁, Σ) = {Σ.M(d₁)(v₁)} = {α}` (since the precondition `v₁ ∈ dom(Σ.M(d₁))` survives the projection `{v₁} ∩ dom(Σ.M(d₁)) = {v₁}`), and symmetrically `image({v₂}, d₂, Σ) = {α}`. F12 (TwoPhaseFactoring) then unfolds each V-side query to its I-side comprehension: `findlinks_V({v₁}, d₁, Σ) = findlinks(image({v₁}, d₁, Σ), Σ) = findlinks({α}, Σ)`, and symmetrically `findlinks_V({v₂}, d₂, Σ) = findlinks({α}, Σ)`. Functional determinism of `findlinks` (one set per `(I, Σ)`) supplies `findlinks({α}, Σ) = findlinks({α}, Σ)` reflexively, closing the equality. The match predicate consulted only the I-image and the link store; how `α` came to be in `I` — through `d₁`'s native arrangement or `d₂`'s transclusion — is invisible to phase 2.

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

The operation is therefore additive in its I-input. Multi-source content imposes no special machinery beyond the underlying span-set generalization. The same property propagates to V-region inputs through the image function's own additivity:

```
F20 (ImageSetAdditive):
   For any d ∈ dom(Σ.M) and any R₁, R₂ ⊆ T:
       image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).
```

The derivation is the standard image-of-union identity for any function. `image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}`, so
`image(R₁ ∪ R₂, d, Σ) = {Σ.M(d)(v) : v ∈ (R₁ ∪ R₂) ∩ dom(Σ.M(d))} = {Σ.M(d)(v) : v ∈ (R₁ ∩ dom(Σ.M(d))) ∪ (R₂ ∩ dom(Σ.M(d)))}`,
which by distributing the comprehension over the union splits as `{Σ.M(d)(v) : v ∈ R₁ ∩ dom(Σ.M(d))} ∪ {Σ.M(d)(v) : v ∈ R₂ ∩ dom(Σ.M(d))} = image(R₁, d, Σ) ∪ image(R₂, d, Σ)`. The function-image-of-set identity supplies the second equality directly.

V-side additivity for `findlinks_V` is then immediate from F12, F13, and F20:

```
findlinks_V(R₁ ∪ R₂, d, Σ)
  = findlinks(image(R₁ ∪ R₂, d, Σ), Σ)              by F12
  = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ)  by F20
  = findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ)  by F13
  = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)   by F12.
```

A reader who selects two V-regions and asks for the links touching either receives the same answer as one who asks for each region separately and unions the results. The two-phase factoring distributes over set union at every stage.

## The Empty Query

The empty query is a meaningful boundary, and the abstract specification handles it without ceremony. For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` has no witness, and `matches(a, ∅, Σ) = false` for every `a ∈ dom(Σ.L)`. The comprehension gives `findlinks(∅, Σ) = ∅`. Symmetrically, `image(∅, d, Σ) = {Σ.M(d)(v) : v ∈ ∅ ∩ dom(Σ.M(d))} = {Σ.M(d)(v) : v ∈ ∅} = ∅`, so `findlinks_V(∅, d, Σ) = findlinks(∅, Σ) = ∅`. A V-region `R` entirely disjoint from `dom(Σ.M(d))` is also a boundary handled uniformly: `R ∩ dom(Σ.M(d)) = ∅` projects to the empty image, and the V-side query returns `∅` without any error path.

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

The determinism (F8) and survivability (F9) properties extend uniformly to both the filtered and the scoped forms. We state the four corresponding claims explicitly so that the filtered and scoped forms are not relegated to silent corollary status.

```
F15 (FilteredDeterminism):
   findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ')  whenever Σ.L = Σ'.L.
```

The filtered comprehension's predicate `(A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` consults only `(Σ.L, C)`: coverage is a function of the endset alone, `|Σ.L(a)|` is determined by `Σ.L(a)`, and `C` is the supplied query. Equality of `Σ.L` forces equality of every per-constraint conjunct (by the same per-slot coverage equality that drives F8's derivation), and set extensionality on the comprehensions closes the chain.

```
F16 (ScopedDeterminism):
   findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ')  whenever Σ.L = Σ'.L.
```

`findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S` by F14. Equality `Σ.L = Σ'.L` gives `findlinks(I, Σ) = findlinks(I, Σ')` by F8, and intersection with the query-supplied `S` (which is not a state component) preserves equality on both sides.

```
F17 (FilteredSurvivability):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d, and any finite set of slot constraints C:
       findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ').
```

Every K.μ-family step preserves `Σ.L` (per F9's derivation, invoking A1 at the K.μ⁺ and K.μ⁻ cases). F15 then forces equality of the filtered result at the two states.

```
F18 (ScopedSurvivability):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d, any I ⊆ T, and any S ⊆ T:
       findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ').
```

By F9, `findlinks(I, Σ) = findlinks(I, Σ')` across any K.μ-family step. Intersecting both sides with the same query-supplied `S` preserves the equality, yielding F18 directly.

The four claims share the same structural backbone as F8 and F9: the abstract-side comprehensions consult only `(Σ.L, query-data)`, and the K.μ family preserves `Σ.L`. We state them explicitly because filtered and scoped queries are the operationally common forms — the unfiltered, full-store `findlinks` is rarely what a reader-facing UI calls — and the determinism/survivability obligations propagate to them with the same force.

## Result Ordering

The result is a set, and a set carries no ordering. But the reader is shown an ordered list, and pagination demands that the order be stable across requests. We adopt the natural ordering: T1's lexicographic order on tumbler addresses. The result is presentable as a sequence:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence ⟨a₁, a₂, ..., aₙ⟩
   with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ), and a₁ < a₂ < ... < aₙ under T1.
```

Presentability as a finite sequence rests on finiteness, which we discharge explicitly. By F3, `result(I, Σ) ⊆ dom(Σ.L)`; by L-fin (ASN-0093), `|dom(Σ.L)| < ∞`; so `result(I, Σ)` is finite as a subset of a finite set. T1 (LexicographicOrder, ASN-0034) is a strict total order on `T`, and by trichotomy it restricts to a strict total order on any subset of `T`. A finite strictly totally ordered set has a unique enumeration in increasing order (the least element exists by well-orderedness of `T1`'s restriction, the second-least is the least of the remainder, and so on by finite induction). The ordering is therefore total, deterministic, and uniquely realized. Pagination is then well-defined: "the next N links past `aⱼ`" means the next N elements in the sorted sequence with addresses greater than `aⱼ` under T1.

The presentation order recovers a creation-order property within each home document. By SubAllocatorAxiom.ChainDiscipline (ASN-0093), each document `d`'s link sub-allocator chain `A_L(d)` is generated by repeated `inc(·, 0)` from the first emission `[d.0.s_L.1]`. ChainEnumerationInjectivity (ASN-0093) shows that this chain is strictly T1-increasing (per-step `inc(tₙ, 0) > tₙ` by TA5(a), lifted across arbitrary gaps by T1 transitivity). So sorting link addresses within a single home document by T1 yields exactly the order in which they were allocated.

For the cross-document part of the ordering claim, we derive that addresses with the same `home(·)` group together and that home documents themselves order lexicographically. ChainMembershipForOrigin (ASN-0093) places every link address `ℓ` with `home(ℓ) = d` in `A_L(d)`, and ChainPrefixExtension (ASN-0093) gives `b_L(d) ≼ ℓ` for every such `ℓ`. For two distinct documents `d₁ ≠ d₂`, CrossDocDisjointness (ASN-0093) supplies that `b_L(d₁)` and `b_L(d₂)` are non-nesting under `≼`. We must also lift the T1 order from documents to anchors: if `d₁ < d₂` under T1, then `b_L(d₁) < b_L(d₂)` under T1. In T1 case (i) on `d₁ < d₂`, the divergence position `k ≤ min(#d₁, #d₂)` with `d₁_k < d₂_k` carries over to `b_L(d₁) vs b_L(d₂)` at the same position, since each anchor agrees with its document on positions `1..#d`. T1 case (ii) on documents is the routine version-extension case rather than an exotic branch — K.δ at `k=1` (ASN-0047) creates a version via `d₂ = inc(d₁, 1)`, producing `d₁ ≺ d₂` as the version-of relationship under the prefix order — so the derivation here exercises the version-ordering machinery on which any multi-version corpus rests. In that case `d₁ ≺ d₂` (so `#d₁ < #d₂`) forces `d₂_{#d₁+1} ≥ 1` — both documents satisfy `zeros(·) = 2` by M0 (ASN-0093), so the proper extension cannot introduce a zero — and at position `#d₁+1`, `b_L(d₁)` has the appended `0` separator while `b_L(d₂)` has `d₂_{#d₁+1} ≥ 1`, yielding `b_L(d₁) < b_L(d₂)` by T1 case (i). With `b_L(d₁) < b_L(d₂)` and the anchors non-nesting, PrefixOrderingExtension (ASN-0034) lifts to every extension: every `ℓ₁` extending `b_L(d₁)` is strictly less than every `ℓ₂` extending `b_L(d₂)`. So under T1, link addresses with the same `home(·)` group together as a contiguous T1-block (all extending the common anchor `b_L(d)`), and the blocks for distinct documents sort by their documents' tumblers. The reader sees results in a canonical, repeatable order: links within a document in allocation order, documents in tumbler order — with version chains nested under their parents by the version-extension ordering just derived.

The chronological reading of T1 order is local to a single home document. Across documents, T1 reflects the lexicographic order of home tumblers, NOT the chronological order of K.λ events: two documents may interleave their K.λ commitments arbitrarily in time, and the result presentation will still group every document's links together by `home(·)`. Within a home document, T1 = K.λ order; across home documents, T1 is canonical and deterministic but not chronological.

## Persistent Discoverability

The link store is monotonic. Once a link is allocated, it persists with its endsets immutable. The match predicate consults only the endsets. Therefore:

```
F11 (PersistentDiscoverability):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with matches(a, I, Σ):
       a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

The conclusion is the multi-step lift of single-step link permanence. ASN-0098's LP13 (UnconditionalLinkPersistence) supplies the full per-link guarantee: for every reachable sequence `Σ →* Σ'` and every `a ∈ dom(Σ.L)`, `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. The `Link` carrier is, by L3 (ASN-0043), a finite sequence `(e₁, …, eₙ)` of endsets with `N ≥ 3`, and arity `|·|` is determined by the underlying sequence length; the value equality `Σ'.L(a) = Σ.L(a)` is therefore equality of two such finite sequences and forces both `|Σ'.L(a)| = |Σ.L(a)|` and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` for every `i` in the common (equal) range. Component-wise tuple equality on `Link` values (L6, ASN-0043) is the explicit form of this extraction: `|Σ.L(a)| = |Σ'.L(a)|` (so the slot-range of the match predicate's existential is the same at the two states) and `Σ.L(a).eᵢ = Σ'.L(a).eᵢ` for every `i ∈ {1, …, |Σ.L(a)|}`. The `coverage(·)` operator is a deterministic function of its endset argument (as exercised in F8's derivation — a union of T1 half-open intervals over the endset's spans), so per-slot endset equality gives per-slot coverage equality `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)`. The match predicate's existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is therefore evaluated against identical per-slot coverages over identical slot ranges at Σ and Σ', and so yields the same Boolean against any fixed `I` — the witness slot found at Σ remains a witness at Σ'.

A link is permanently discoverable for any query I-set that overlaps any of its endset coverages. This is the discovery counterpart of link immutability: the link is not only structurally fixed, it is *findability-fixed*. Editing the documents around it, deleting the V-positions that arrange its referenced content, transcluding the content into new documents — none of these alter the link's match status against a fixed I-set.

The converse direction is also worth noting. Across a transition, new links may *enter* the result set (via K.λ adding a link whose endsets overlap `I`), but existing matching links cannot leave it. The result is monotonic in the link store. Stated as a set-level claim:

```
F19 (ResultSetMonotonicity):
   For any reachable state sequence Σ →* Σ' and any I ⊆ T:
       findlinks(I, Σ) ⊆ findlinks(I, Σ').
```

The derivation is a one-line lift of F11 to the comprehension level. By the definition of `findlinks`, `a ∈ findlinks(I, Σ)` iff `a ∈ dom(Σ.L) ∧ matches(a, I, Σ)`. F11 gives `a ∈ dom(Σ'.L) ∧ matches(a, I, Σ')` for every such `a` across any reachable sequence `Σ →* Σ'`, which is `a ∈ findlinks(I, Σ')` by the same definition. Set extensionality closes the inclusion.

F19 is the load-bearing consequence behind any indexed implementation's promise: an index that mirrors `findlinks` is *never required to remove entries* as the state evolves, only to add them. The discovery operation is monotone non-decreasing in the link store at the set level, so indexes can be append-only just like the link store itself.

## A Worked Example

The abstract specification is short enough that it can read as content-free without an instance to anchor it. We fix a small one.

Consider a state `Σ` with two documents, both inhabiting `dom(Σ.M)`.

- `d_a` is a content-bearing document. Its content sub-allocator `A_C(d_a)` (ASN-0093) has produced three I-addresses: `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each placed into `dom(Σ.C)` by successive K.α steps with values `v₁, v₂, v₃ ∈ Val`. Its arrangement, by D-SEQ★ (ASN-0036), is `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}`, where `v_a^k = [s_C, 1, ..., 1, k]` is the canonical depth-`m_C` text-subspace V-position.

- `d_b` transcludes the latter two positions from `d_a`. Its arrangement is `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}`, sharing the I-addresses `α₂` and `α₃` with `d_a`. (No new content addresses were allocated for `d_b`; transclusion shares by reference. By P4★ (ASN-0047), `(α₂, d_b), (α₃, d_b) ∈ Σ.R`.) We assume `d_a` was allocated before `d_b` under the same account, so by SubAllocatorAxiom.ChainDiscipline and T10a (ASN-0093, ASN-0034), `d_a < d_b` under T1.

- Two links `ℓ ∈ dom(Σ.L)` (allocated under `d_a`, so `home(ℓ) = d_a` and `ℓ = [d_a.0.s_L.1]`) and `ℓ' ∈ dom(Σ.L)` (allocated under `d_b`, so `home(ℓ') = d_b` and `ℓ' = [d_b.0.s_L.1]`), both with arity 3:
  - `ℓ`'s slot 1 (from-endset): one canonical span `(α₂, δ(1, #α₂))`, so `coverage(Σ.L(ℓ).e₁) = {t ∈ T : α₂ ≼ t}` by PrefixSpanCoverage (ASN-0043). The coverage is *not* the singleton `{α₂}` — it is the prefix-closure of `α₂`, containing `α₂` itself together with every tumbler extending `α₂` (e.g. `α₂.0`, `α₂.1`, `α₂.0.0`, …). Coverage of a canonical span is always a prefix-subtree, never a singleton; the singleton arises only when we intersect with a singleton query.
  - `ℓ`'s slot 2 (to-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ).e₂) = {t ∈ T : α₃ ≼ t}` by the same reasoning.
  - `ℓ`'s slot 3 (type-endset): some non-empty type endset whose coverage we leave abstract; assume it does not meet the content I-addresses we query.
  - `ℓ'`'s slot 1 (from-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ').e₁) = {t ∈ T : α₃ ≼ t}` — the same prefix-closure as `ℓ`'s slot 2.
  - `ℓ'`'s slot 2 (to-endset): one canonical span `(α₁, δ(1, #α₁))`, so `coverage(Σ.L(ℓ').e₂) = {t ∈ T : α₁ ≼ t}`.
  - `ℓ'`'s slot 3 (type-endset): some non-empty type endset assumed disjoint from the queried content addresses.

The three prefix-subtrees over `α₁, α₂, α₃` are pairwise disjoint: each `αᵢ` is an element-level tumbler of equal length with disagreeing final components (1, 2, 3 respectively), so no pair extends the other (`αᵢ ⋠ αⱼ` for `i ≠ j`), and a tumbler cannot extend two of them simultaneously. By ChainEnumerationInjectivity and CrossDocDisjointness (ASN-0093) together with PrefixOrderingExtension (ASN-0034), the link addresses satisfy `ℓ < ℓ'` under T1: at the divergence position between `d_a` and `d_b` (where `d_a` precedes `d_b`), the same divergence carries forward to `b_L(d_a) < b_L(d_b)` and onward to every extension, giving `ℓ < ℓ'`.

**Query 1: `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: the precondition `d_a ∈ dom(Σ.M)` holds, and `{v_a^2} ∩ dom(Σ.M(d_a)) = {v_a^2}` (the queried position survives the projection), so `image({v_a^2}, d_a, Σ) = {Σ.M(d_a)(v_a^2)} = {α₂}`. Phase 2: test each link in `dom(Σ.L)` against `I = {α₂}`. At `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅` (the only element of `{α₂}` that extends `α₂` is `α₂` itself, by reflexivity of `≼`), so the slot-existential fires and `matches(ℓ, {α₂}, Σ) = true`. At `ℓ'`, slot 1 covers `{t : α₃ ≼ t}`, slot 2 covers `{t : α₁ ≼ t}`, and slot 3's coverage is disjoint from the content addresses by assumption; none meet `{α₂}` (since `α₃ ⋠ α₂` and `α₁ ⋠ α₂` — final components disagree). The result is `{ℓ}`.

**Query 2: `findlinks_V({v_b^1}, d_b, Σ)`.** Phase 1: `image({v_b^1}, d_b, Σ) = {Σ.M(d_b)(v_b^1)} = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address as `d_a`'s native arrangement of `α₂`. Phase 2 is therefore identical to Query 1's Phase 2: result `{ℓ}`. This is F6 (TransclusionTransparency) in operation — the reader querying `d_b`'s view of `α₂` discovers the same link they would have discovered via `d_a`'s native arrangement, because identity travels with the I-address.

**Query 3: `findlinks_V({v_a^2, v_a^3}, d_a, Σ)`.** Phase 1: `image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}`. Phase 2: at `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂, α₃} = {α₂} ≠ ∅` (matches); slot 2 also fires (`{t : α₃ ≼ t} ∩ {α₂, α₃} = {α₃}`), although either witness alone suffices. At `ℓ'`, slot 1 gives `coverage(Σ.L(ℓ').e₁) ∩ {α₂, α₃} = {t : α₃ ≼ t} ∩ {α₂, α₃} = {α₃} ≠ ∅` (matches via slot 1); slot 2 (covering `{t : α₁ ≼ t}`) does not fire. Result: `{ℓ, ℓ'}`. Both links appear once each — the result is a set.

**Verifying F10 (OrderedResult) on Query 3.** The set `{ℓ, ℓ'}` admits a unique strictly T1-increasing presentation. We have `home(ℓ) = d_a` and `home(ℓ') = d_b` with `d_a < d_b` (by the allocation-order assumption). Both links lie in their respective `A_L` chains: `ℓ = [d_a.0.s_L.1] ∈ A_L(d_a)` and `ℓ' = [d_b.0.s_L.1] ∈ A_L(d_b)`. CrossDocDisjointness (ASN-0093) gives `b_L(d_a) = [d_a.0.s_L] ⋠ b_L(d_b) = [d_b.0.s_L]` and `b_L(d_b) ⋠ b_L(d_a)` — the anchors are non-nesting. T1 case (i) at the divergence position between `d_a` and `d_b` lifts to `b_L(d_a) < b_L(d_b)`, since each anchor agrees with its document on positions `1..#d_a = 1..#d_b` (documents being siblings under the same account have equal length by T10a.1) and shares the appended `.0.s_L` thereafter. PrefixOrderingExtension (ASN-0034) then lifts to every extension: `ℓ < ℓ'`. The canonical presentation is `⟨ℓ, ℓ'⟩`. The result delivered to the reader is therefore ordered by home document under T1, with links within a document in allocation order — here each document has only one link, but the cross-document ordering machinery is fully exercised in T1 case (i).

**Verifying F10 across a version extension (T1 case (ii)).** Case (i) handles sibling documents; the routine version-of relationship — K.δ at `k = 1` (ASN-0047) producing `d_new = inc(d_src, 1)` — falls under T1 case (ii) because the resulting `d_src ≺ d_new` is the prefix-extension shape rather than the divergence shape. We exercise the case explicitly with a hypothetical version document `d_c = inc(d_a, 1)`, a version of `d_a` produced by K.δ at `k = 1` in some other state (the broader Worked Example operates at `Σ`, which need not contain `d_c`; this paragraph is local). Suppose `d_c ∈ dom(Σ.M)` and a third link `ℓ'' = [d_c.0.s_L.1] ∈ dom(Σ.L)` is allocated under `d_c`. We verify the placement of `ℓ''` under T1 against `ℓ` and `ℓ'`. By TA5(d) (ASN-0034), `#d_c = #d_a + 1` and `d_c` agrees with `d_a` on positions `1..#d_a`, so `d_a ≺ d_c` and `(d_c)_{#d_a + 1} = 1`. The anchors satisfy `b_L(d_a) = [d_a, 0, s_L]` and `b_L(d_c) = [d_a, 1, 0, s_L]` (positions `1..#d_a` shared, position `#d_a + 1` is `0` for `b_L(d_a)` and `1` for `b_L(d_c)`). At position `#d_a + 1` the anchors diverge: `b_L(d_a)[#d_a + 1] = 0 < 1 = b_L(d_c)[#d_a + 1]`, so by T1 case (i) at that position, `b_L(d_a) < b_L(d_c)` — and the divergence is genuine (case (ii) on the underlying documents lifts to case (i) on the anchors once the trailing `.0.s_L` is appended). The anchors are non-nesting because they share positions `1..#d_a` but disagree at position `#d_a + 1`. PrefixOrderingExtension lifts to every extension: `ℓ < ℓ''`. For the `ℓ'' vs ℓ'` comparison, at position `#d_a + 1`: `b_L(d_c)[#d_a + 1] = 1` while `b_L(d_b)[#d_a + 1] = (d_b)_{#d_a + 1}`, and since `d_b = inc(d_a, 0)` produces a sibling that increments only the last component of `d_a` (TA5(c)), `(d_b)_{#d_a + 1}` does not exist — `d_b`'s length equals `d_a`'s length, both being depth-`#d_a` documents under the same account. The comparison `ℓ'' vs ℓ'` is therefore decided at an earlier position. At position `#d_a` (the last position of `d_a` and of `d_b`): `(d_a)_{#d_a}` and `(d_b)_{#d_a}` diverge, with `(d_a)_{#d_a} < (d_b)_{#d_a}` by sibling-increment ordering (TA5(a)); both `ℓ''` and `ℓ` agree with `d_a` on position `#d_a` (since `ℓ'' = [d_a, 1, 0, s_L, 1]` and `ℓ = [d_a, 0, s_L, 1]` both extend `d_a` at this position), while `ℓ' = [d_b, 0, s_L, 1]` agrees with `d_b` there. So at position `#d_a`, `ℓ''[#d_a] = (d_a)_{#d_a} < (d_b)_{#d_a} = ℓ'[#d_a]`, and earlier positions agree because `d_a` and `d_b` share their account prefix. T1 case (i) at position `#d_a` gives `ℓ'' < ℓ'`. The canonical presentation of the augmented result set `{ℓ, ℓ', ℓ''}` is `⟨ℓ, ℓ'', ℓ'⟩` — the version-extension link sits between the original link and its sibling-document counterpart. F10 holds across both T1 cases: case (i) for siblings, case (ii) for versions.

**Verifying F13 (SetAdditive).** Compute each side separately. `findlinks({α₂}, Σ) = {ℓ}` (`ℓ` via slot 1; `ℓ'` matches none of `{α₂}`) and `findlinks({α₃}, Σ) = {ℓ, ℓ'}` (`ℓ` via slot 2 and `ℓ'` via slot 1, both intersecting `{α₃}` in `{α₃}`); their union is `{ℓ, ℓ'}`. Independently, `findlinks({α₂, α₃}, Σ) = {ℓ, ℓ'}` by direct evaluation as in Query 3. The two computations agree: `findlinks({α₂} ∪ {α₃}, Σ) = findlinks({α₂}, Σ) ∪ findlinks({α₃}, Σ) = {ℓ, ℓ'}`.

**Verifying F2 (Completeness) against the instance.** The set `dom(Σ.L) = {ℓ, ℓ'}` is the universe of candidates. For the query `{α₂}`, the match predicate fires at `ℓ` only; F2 demands `ℓ ∈ result({α₂}, Σ)` — the no-spurious obligation belongs to F3 and is addressed in the next paragraph. The comprehension `{a ∈ dom(Σ.L) : matches(a, {α₂}, Σ)}` evaluates to `{ℓ}`. Completeness holds.

**Verifying F3 (Soundness) against the instance.** The result `{ℓ}` is a subset of `dom(Σ.L) = {ℓ, ℓ'}`, and `matches(ℓ, {α₂}, Σ) = true` was verified above. `ℓ'` is correctly absent from the result because `matches(ℓ', {α₂}, Σ) = false`. No spurious link appears.

**Verifying F6 against the instance.** Queries 1 and 2 produce the same I-image `{α₂}` and hence the same result `{ℓ}`, despite the V-positions `v_a^2` and `v_b^1` belonging to different documents. The match predicate consulted only the I-image and the link store; the document of origin of the V-position vanished from the computation after Phase 1.

**Verifying F5 (IdentityNotValue) against the instance.** Slot 1's coverage at `ℓ` is `{t : α₂ ≼ t}`, so `matches(ℓ, {α₂}, Σ) = true` (via slot 1: `α₂ ≼ α₂` puts `α₂` in the intersection with `{α₂}`) while `matches(ℓ, {α₃}, Σ) = true` only via slot 2 — the slot 1 test against `{α₃}` evaluates `{t : α₂ ≼ t} ∩ {α₃} = ∅` (since `α₂ ⋠ α₃`) and so does not fire. The slot 1 decision turns entirely on which I-addresses extend `α₂` as tumblers. The content values `v₂, v₃ ∈ Val` at `α₂, α₃` are never consulted: even if the writer of `d_a` had stored `v₂ = v₃` (the same value at distinct addresses), the slot 1 test would still discriminate `{α₂}` from `{α₃}` — the address-level intersection `{t : α₂ ≼ t} ∩ {α₃} = ∅` is decided by `α₂ ⋠ α₃` (their last components disagree, 2 vs 3), itself a consequence of GlobalUniqueness (ASN-0034) which forced these addresses to be distinct in the first place. F5 says the match predicate factors through the address space, not through the value space; this instance exhibits the factoring directly.

**Query 4: Survivability under arrangement edit (F11, F9).** Apply a K.μ⁻ transition to `d_a` retaining only the first content position: the post-state Σ' has `Σ'.M(d_a) = {v_a^1 ↦ α₁}`, with `v_a^2` and `v_a^3` removed from `dom(Σ'.M(d_a))` (so `α₂` and `α₃` are no longer in `ran(Σ'.M(d_a))`). The link store is untouched by K.μ⁻ — its effect clause names only `M(d_a)`, so by A1 (EffectClauseExhaustivity), `L' = L` — so `dom(Σ'.L) = {ℓ, ℓ'}` and `Σ'.L(ℓ) = Σ.L(ℓ)`, `Σ'.L(ℓ') = Σ.L(ℓ')`. Re-evaluate `findlinks({α₂}, Σ')`: the match predicate at `ℓ` tests slot 1, `coverage(Σ'.L(ℓ).e₁) ∩ {α₂} = {α₂} ≠ ∅`, so `matches(ℓ, {α₂}, Σ') = true`. `ℓ'`'s endsets still do not meet `{α₂}`. The result is `{ℓ}`, the same as Query 1's pre-edit result.

This exercises F11 directly: the link survives the arrangement edit because its endset references `α₂`'s I-address (not `v_a^2`'s V-position), and `α₂`'s identity is preserved by content immutability (C0, ASN-0093). It also exercises F9 — the K.μ⁻ transition is a K.μ-family step satisfying F9's frame condition, so `findlinks({α₂}, Σ) = findlinks({α₂}, Σ')` is guaranteed before we re-evaluate the comprehension. The V-side query `findlinks_V({v_a^2}, d_a, Σ')` remains well-formed under the projection semantics of `image`: `{v_a^2} ∩ dom(Σ'.M(d_a)) = ∅` (since `v_a^2` was contracted out), so `image({v_a^2}, d_a, Σ') = ∅` and `findlinks_V({v_a^2}, d_a, Σ') = findlinks(∅, Σ') = ∅`. The reader who previously queried `α₂` via `v_a^2` now receives an empty V-side answer through that route and must reach `α₂` via a surviving V-position — `d_b`'s transclusion suffices: `findlinks_V({v_b^1}, d_b, Σ')` images to `{α₂}` and recovers `ℓ`. The link's I-side identity persists; the V-side query surface has shrunk while the link-side survivability has not.

**Query 5: Filtered query exercising F7 (filter conjunction).** Evaluate `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ)` — the conjunctive "links from `α₂` to `α₃`" query. At `ℓ`: slot 1 satisfies `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {α₂} ≠ ∅`, slot 2 satisfies `coverage(Σ.L(ℓ).e₂) ∩ {α₃} = {α₃} ≠ ∅`. Both constraints hold; `ℓ` is in the result. At `ℓ'`: slot 1 covers `{t : α₃ ≼ t}`, intersected with `{α₂}` is `∅` (since `α₃ ⋠ α₂`); the slot-1 constraint already fails, the universal is false, and `ℓ'` is excluded — even though `ℓ'`'s slot 1 *does* meet `{α₃}`, which would have satisfied a slot-1 constraint had we named the to-set under slot 1. The conjunctive force of the filter is essential: the *from* slot must meet `{α₂}` and the *to* slot must meet `{α₃}`, both holding simultaneously. Result: `{ℓ}`. Contrast with the union-form unfiltered query `findlinks({α₂} ∪ {α₃}, Σ) = {ℓ, ℓ'}` — the filtered form is strictly stricter, as F7(b) and the section on filtered semantics anticipate.

**Query 6: Scoped query exercising F14.** Evaluate `findlinks_scoped({α₂, α₃}, {a ∈ T : home(a) = d_a}, Σ)`. The unscoped result `findlinks({α₂, α₃}, Σ) = {ℓ, ℓ'}` (Query 3). The scope `S = {a : home(a) = d_a}` contains every link allocated under `d_a`; in this instance only `ℓ`, since `home(ℓ) = d_a` while `home(ℓ') = d_b`. The intersection `findlinks({α₂, α₃}, Σ) ∩ S = {ℓ, ℓ'} ∩ {ℓ} = {ℓ}`. The reader who restricts to `d_a`-owned links receives `{ℓ}`, even though `ℓ'` also touches the queried content. The match predicate is unweakened — `ℓ'` still matches the I-set — but the scope narrows the candidate set before reporting. F14's definition `findlinks_scoped = findlinks(I, Σ) ∩ S` is exercised by direct intersection.

**Query 7: Determinism under arrangement variation (F8).** Apply a K.μ~ reordering transition to `d_a` realising the cyclic permutation `π(v_a^k) = v_a^{(k mod 3) + 1}`: the post-state Σ'' has `Σ''.M(d_a) = {v_a^1 ↦ α₃, v_a^2 ↦ α₁, v_a^3 ↦ α₂}` (the same three I-addresses arranged at the same three V-positions, rotated). K.μ~'s published frame names `L' = L` directly (no appeal to A1 is needed here), so `Σ''.L = Σ.L` exactly. F8's hypothesis is satisfied, and F8 forces `findlinks({α₂}, Σ) = findlinks({α₂}, Σ'')` directly from the I-side: the match predicate consults only `(Σ.L, I)`, both unchanged, so the comprehension produces the same set. Direct evaluation at Σ'' confirms — the slot-1 test at `ℓ` evaluates `coverage(Σ''.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅` exactly as in Query 1; `ℓ'`'s endset coverages do not meet `{α₂}` for the same address-level reasons; the result is `{ℓ}`. Crucially, no V-position appeared anywhere in the I-side derivation. The V-image *of any V-position in `d_a`* changed under the reordering (`v_a^2` now maps to `α₁` rather than `α₂`), but the link-side answer for the fixed I-set `{α₂}` is invariant. This is the operational content of F8: link discovery is a property of `(Σ.L, I)`, with arrangement permutations preserving the link store leaving the answer untouched.

**Implicit verifications in Queries 1–3 (F1, F7(a)).** Queries 1–3 each rely on the singleton-overlap reading of F1's slot-existential: in Query 1, slot 1's coverage at `ℓ` meets `{α₂}` in the singleton `{α₂}`, and that singleton overlap suffices to fire the existential and put `ℓ` in the result without examining slot 2 or slot 3. The design constraint that no strengthening of the intersection condition is permitted (full overlap, majority overlap, etc.) is exercised silently throughout — any strengthening would have excluded `ℓ` from Query 1's result, since slot 1's coverage is the entire prefix-closure of `α₂` and the query is a singleton. Queries 1–3 also exercise F7(a)'s slot symmetry: the match predicate's existential ranges over every slot of every link uniformly, so when Query 3 finds `ℓ'` via its slot 1 (whose coverage extends `α₃`), no slot is privileged over any other — the same uniformity that lets Query 1 find `ℓ` via slot 1 alone. Both observations are intrinsic to the existential structure of `matches` and require no separate verification step.

**Verifying F20 (ImageSetAdditive) by splitting Query 3.** Decompose the V-region `R = {v_a^2, v_a^3}` of Query 3 into the disjoint sub-regions `R₁ = {v_a^2}` and `R₂ = {v_a^3}`. Compute each image separately: `image(R₁, d_a, Σ) = {α₂}` (Query 1's image); `image(R₂, d_a, Σ) = {Σ.M(d_a)(v_a^3)} = {α₃}` by the same projection. Their union `{α₂} ∪ {α₃} = {α₂, α₃}` agrees with the direct computation `image(R₁ ∪ R₂, d_a, Σ) = image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}` (Query 3's image). Composing with `findlinks` via F12 yields V-side additivity: `findlinks_V(R₁ ∪ R₂, d_a, Σ) = findlinks_V(R₁, d_a, Σ) ∪ findlinks_V(R₂, d_a, Σ) = {ℓ} ∪ {ℓ, ℓ'} = {ℓ, ℓ'}`, matching Query 3's result.

**Verifying F19 (ResultSetMonotonicity) under a K.λ extension.** From the original state Σ, apply a single K.λ allocating a fresh link `ℓ''` under `d_a` whose slot 1 has the canonical span `(α₂, δ(1, #α₂))` (so its coverage is the same prefix-closure as `ℓ`'s slot 1) and whose slot 2 and slot 3 have coverages disjoint from `{α₂}`. By the K.λ effect, `Σ'''.L = Σ.L ∪ {ℓ'' ↦ ...}` with all prior entries unchanged (L12). Then `findlinks({α₂}, Σ) = {ℓ}` (Query 1) while `findlinks({α₂}, Σ''') = {ℓ, ℓ''}` (both `ℓ` and `ℓ''` now satisfy the slot-1 test against `{α₂}`). The inclusion `findlinks({α₂}, Σ) ⊆ findlinks({α₂}, Σ''')` holds with strict containment: `ℓ''` enters the result, and no prior member leaves it. K.λ is the only operation of V that can grow the result; the growth is monotone, never destructive.

**Verifying F15 (FilteredDeterminism) at Σ vs. Σ''.** The K.μ~ transition of Query 7 preserves `Σ.L` exactly (by K.μ~'s published `L' = L` frame), so `Σ''.L = Σ.L`. F15's hypothesis is satisfied, and F15 predicts `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ) = findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ'')`. Direct evaluation at Σ'' confirms: at `ℓ`, slot 1 covers `{t : α₂ ≼ t}` (unchanged from Σ by L12) and meets `{α₂}` in `{α₂}`; slot 2 covers `{t : α₃ ≼ t}` and meets `{α₃}` in `{α₃}`; both constraints hold. At `ℓ'`, slot 1's intersection with `{α₂}` is empty, the universal fails. Result: `{ℓ}`, matching Query 5's pre-K.μ~ evaluation. The arrangement permutation did not perturb the filtered answer because the filtered predicate consults only `(Σ.L, C)` and `Σ.L` is invariant under K.μ~.

**Verifying F17 (FilteredSurvivability) across Query 4's K.μ⁻.** Query 4's K.μ⁻ transition Σ → Σ' contracts `d_a` to `{v_a^1 ↦ α₁}`, but by F9-cor (with K.μ⁻ inheriting `Σ.L = Σ'.L` via the L12 + A1 derivation), `Σ'.L = Σ.L`. F17 then predicts `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ) = findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ')`. Direct evaluation at Σ' confirms: at `ℓ`, slot 1 coverage and slot 2 coverage are both unchanged from Σ (L12), so both constraints continue to hold and `ℓ` is in the filtered result. At `ℓ'`, slot 1 still fails the `{α₂}` test, so `ℓ'` is excluded. Result: `{ℓ}`, matching Query 5's pre-edit evaluation. The reader's "from `α₂` to `α₃`" query survives the contraction in the I-side answer; the V-side query surface has shrunk (no V-position in `d_a` now maps to `α₂` or `α₃`), but the filtered link-side answer at the fixed `(I_from, I_to)` is invariant.

The example is small enough to inspect by eye, and the abstract definitions reduce to elementary set operations. Larger instances scale the same way: each link tests independently, slot existentials collect witnesses, and the comprehension assembles the answer.

## What Completeness Demands of Implementations

We have specified the result as a set. An implementation must produce exactly this set — no more, no fewer. The abstract specification is silent on *how* the set is computed.

The spec's demand on any conforming implementation is exactly F2 ∧ F3: `result(I, Σ) = findlinks(I, Σ)`. We do not specify the mechanism. We specify the result. Any implementation whose `result(I, Σ)` differs from the set comprehension is non-conforming, regardless of cause.

## Local Atomicity and the Single-State Setting

The abstract specification is stated against a single state `Σ`. By the sequential-transition axiom (ASN-0093), every state transition is atomic and uninterruptible. The state `Σ` is well-defined at every point at which a query is evaluated.

A K.λ transition commits a link to `dom(Σ.L)` atomically. By the time the K.λ committing `a` returns, `a` is in `dom(Σ.L)`. The next query — at any state succeeding the K.λ — must include `a` in its result if `a` matches. There is no intermediate state in which `a` exists in `dom(Σ.L)` but is undiscoverable through the abstract operation.

This atomicity is what underwrites the *immediate* component of Nelson's "without appreciable delay" promise within a single instance. The query result reflects the current state's link store, fully and exactly. Implementations that defer index maintenance to a background process create a window in which the index lags the link store; during that window, results computed from the index would violate F2. The abstract specification permits no such window.

## Implementation Notes (Non-Normative)

Conformance is exhausted by F2 ∧ F3 — any procedure (with or without an auxiliary index) that produces `result(I, Σ) = findlinks(I, Σ)` conforms; the abstract specification is index-agnostic.

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
| `image(R, d, Σ)` | I-image of a V-region with silent projection: `{Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}` | introduced |
| `matches(a, I, Σ)` | Match predicate: `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` | introduced |
| `findlinks(I, Σ)` | Discovery operation: `{a ∈ dom(Σ.L) : matches(a, I, Σ)}` | introduced |
| `findlinks_V(R, d, Σ)` | Two-phase composite: `findlinks(image(R, d, Σ), Σ)` | introduced |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints `C` | introduced |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | introduced |
| A1 | EffectClauseExhaustivity (interface contract on every operation specification in V): the effect clause must name every modified state component, so silence in the frame is binding preservation; scope fixed by the vocabulary-closure premise | introduced |
| F1 | Match predicate as set-theoretic overlap, existential over slots | introduced |
| F2 | Completeness: every matching link in `dom(Σ.L)` appears in the result | introduced |
| F3 | Soundness: every link in the result is in `dom(Σ.L)` and matches | introduced |
| F4 | MatchFormulaUniqueness: F1's slot-existential / singleton-overlap form is the unique match predicate; no strengthening is a refinement of F1 | introduced |
| F5 | Identity, not value: the match consults coverage, not content values | introduced |
| F6 | Transclusion transparency: same I-address, same matches regardless of V-path | introduced |
| F7 | Endset symmetry: slots are equally searchable; filters conjoin | introduced |
| F8 | Determinism: `result(I, Σ)` is a function of `(Σ.L, I)` | introduced |
| F9 | Link survivability under edits: K.μ-family transitions preserve `findlinks(I, ·)` | introduced |
| F9-cor | Non-allocating preservation: every operation in V ∖ {K.λ} preserves `findlinks(I, ·)`; surfaces the full A1 dependency surface (K.μ⁺, K.μ⁻, K.ρ) | introduced |
| F10 | Ordered result: canonical T1-sorted presentation | introduced |
| F11 | Persistent discoverability: matching at `Σ` implies matching at every `Σ'` reached from `Σ` | introduced |
| F12 | Two-phase factoring: `findlinks_V` composes `image` (V→I) and `findlinks` (I→Link) | introduced |
| F13 | Set-additive in the I-input: `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)` | introduced |
| F14 | Scope filter is intersection: `findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S` | introduced |
| F15 | Filtered determinism: `findlinks_filtered(C, ·)` is a function of `(Σ.L, C)` | introduced |
| F16 | Scoped determinism: `findlinks_scoped(I, S, ·)` is a function of `(Σ.L, I, S)` | introduced |
| F17 | Filtered survivability: K.μ-family transitions preserve `findlinks_filtered(C, ·)` | introduced |
| F18 | Scoped survivability: K.μ-family transitions preserve `findlinks_scoped(I, S, ·)` | introduced |
| F19 | Result-set monotonicity: `findlinks(I, Σ) ⊆ findlinks(I, Σ')` for every reachable sequence `Σ →* Σ'` | introduced |
| F20 | Image set-additive: `image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ)` | introduced |

## Open Questions

What semantics should the operation have when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`?

What completeness guarantees must hold when the link store is logically partitioned across multiple physical instances that may be temporarily disconnected?

What consistency model must FINDLINKS observe with respect to K.λ operations that may be concurrent with or interleaved with the query at a higher protocol layer?

How does access-control filtering compose with the completeness obligation — is completeness restated relative to the authorized scope, and what invariants must the access-control layer preserve to make the composition coherent?

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?

What is the relationship between FINDLINKS and the inverse direction (resolving the result's endsets back to V-positions in some target document), and what additional guarantees does the inverse direction require that FINDLINKS does not?

Should ASN-0047's K.μ⁺ and K.μ⁻ frame clauses be revised to include explicit `L' = L` conjuncts? Doing so would discharge F9's K.μ⁺/K.μ⁻ case from a published frame rather than through A1 (EffectClauseExhaustivity), eliminating the only dependency on A1 in this ASN's derivations.
