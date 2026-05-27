# ASN-0099: FINDLINKS Operation

*2026-05-26*

## The Reader's Question

The reader looks at a stretch of content in their document and asks: *what connects here from elsewhere?* This is one half of the central reader-side promise of a Xanadu-style system — that the literature is bidirectionally navigable, that the links from the rest of the docuverse to the content in front of me must be findable on demand and (per Nelson's design intent at Literary Machines 2/46, "without appreciable delay") at interactive responsiveness rather than batch latency. We adopt this as our starting obligation, treating the Nelson phrase here as design framing for the operation's reader-experience role — binding on interactive responsiveness for backlink discovery, but silent on stronger commit-visibility models. The user supplies a region of arranged content; the system must return every link whose endsets touch that content.

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

The two phases compose into the reader-facing operation, defined as their composite. We name the definitional unfolding so downstream derivations can cite it as a discrete step rather than re-unfolding `findlinks_V` from first principles each time:

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V (not a derived identity):
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

F12 is a definition: it introduces no claim over and above the abstract definition of `findlinks_V`, and the equivalence holds by stipulation. The "F12" label exists only as a citation handle so downstream derivations (F6, V-side additivity, the worked example) can name the definitional move when unfolding `findlinks_V` to its two-phase form. To keep this status visible at the citation site, downstream derivations write "by F12 (def)" or "by F12's definition" when the step is definitional unfolding. Readers auditing a chain of derivations should treat any such citation as "by definition" — equivalent in epistemic force to a substitution lemma rather than a derived implication. The single precondition is inherited from `image`'s `defined when` clause — `findlinks_V` is well-formed precisely when `image(R, d, Σ)` is. We restate it at the composite to keep the document-existence requirement visible at the call site. The treatment of the two failure modes is asymmetric and worth stating explicitly. (i) Document non-existence: for `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is *undefined* — `image(R, d, Σ)` has no value at such `d`, and the composite inherits the undefinedness. The caller is responsible for establishing `d ∈ dom(Σ.M)` before invoking the V-side operation; no silent fallback (empty set, error sentinel) is supplied at the abstract specification level. (ii) Position non-existence: for `d ∈ dom(Σ.M)` and V-positions in `R` that lie outside `dom(Σ.M(d))`, those positions are silently projected away by `image` and do not impose a pre-validation obligation on the caller; this is the only treatment that gives a total operation over `R ⊆ T` for a fixed allocated document.

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
F4 (MatchFormulaMinimality):
   F1's slot-existential / singleton-overlap form is the unique
   match predicate that, when wired into F2 ∧ F3, produces
   conformance with the reader's promise — the architectural
   commitment that "every link touching the queried region must
   appear". The substantive content of F4 is *realizability*: any
   alternative predicate's gap against F1 manifests as an observable
   behavioral disagreement at some K.λ-reachable state. The
   uniqueness is therefore operational, not predicate-theoretic —
   F4 does not establish that F1 is the only conceivable match
   predicate in some absolute sense; it establishes that any
   predicate disagreeing with F1 on a realizable (a, I) pair defines
   a different operation. Throughout the two derivation directions
   below, F1 is fixed as the meta-level reference: strengthenings
   are read as "fails to admit at least one F1-admitted pair";
   weakenings as "admits at least one F1-non-admitted pair"; and
   "conforming to F2 ∧ F3" means satisfying F2 ∧ F3 with F1 as the
   embedded match predicate.

   We discharge the two directions separately:

   (Strengthening direction.) No strengthening of F1 —
   `coverage(Σ.L(a).eᵢ) ⊆ I`, `I ⊆ coverage(Σ.L(a).eᵢ)`,
   `|coverage(Σ.L(a).eᵢ) ∩ I| ≥ k` for any fixed `k > 1`, or any
   other refinement that excludes at least one singleton-overlap
   pair `(eᵢ, I)` — defines a predicate `P_s` strictly narrower
   than F1. An implementation that computes `result(I, Σ)` using
   `P_s` omits the F1-admitted-but-`P_s`-rejected witness pair at
   any state where that pair is realized — and the realizability
   argument below shows that some such state exists for every
   strengthening considered. The conformance test (F2 ∧ F3 evaluated
   against F1) then fails: a link belongs to F1's `findlinks(I, Σ)`
   but is missing from the alternative `result(I, Σ)`.

   (Weakening direction.) Any predicate `P_w` admitting strictly
   more `(a, I)` pairs than F1 has some witness pair admitted by
   `P_w` but not by F1. K.λ (LinkAllocation, ASN-0093) and L4
   (ASN-0043) impose no constraint on endset configurations or on
   the addresses spans may reference, so the witness link is
   realizable by direct K.λ allocation in any conforming state with
   `dom(Σ.M) ≠ ∅`. An implementation using `P_w` returns the
   witness `a` in `result(I, Σ)` at that state; F1's
   `findlinks(I, Σ)` excludes `a` by F1-non-admission. The
   conformance test fails: the alternative `result(I, Σ)` contains
   a link absent from F1's `findlinks(I, Σ)`.

   Together: F2 forbids strengthenings (which would miss F1-admitted
   matches), F3 forbids weakenings (which would return non-F1 links).
   F1 is the unique match predicate that satisfies both halves of the
   conformance contract.
```

The derivation is immediate from F1 under existential introduction: any singleton overlap at any slot satisfies F1's predicate, so any predicate that fails to recognize at least one such overlap excludes a link that F1 includes. We discharge each enumerated strengthening with a concrete `(eᵢ, I)` witness pair that F1 admits but the strengthening rejects. Each witness is realizable through canonical spans of the form `(α, δ(1, #α))`. By L4 (ASN-0043), endset spans may reference any addresses in T, so the base address `α ∈ T` is unconstrained; by PrefixSpanCoverage (ASN-0043), the resulting coverage is the prefix subtree `{t ∈ T : α ≼ t}` — the canonical realizable shape of endset coverage from a single span, generated by T12's half-open interval over the tumbler line (ASN-0034). The query I-set `I ⊆ T` is independently unconstrained. The witness link configurations are themselves realizable as conforming states extending any base `Σ`: K.λ (LinkAllocation, ASN-0093) admits, at any state with a non-empty `dom(Σ.M)`, the allocation of a link with arity `N ≥ 3` whose endsets are freely chosen subject only to K.λ's well-formedness precondition `(A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` — and L4 (ASN-0043) places no constraint on the addresses spans may reference. The arity-3 standard-triple shape of every witness below satisfies K.λ's `N ≥ 3` directly, and each witness's slot endsets (one canonical span at slot 1, a non-empty type endset at slot 3, and any chosen content at slot 2) satisfy the well-formedness conjunct. Each witness below constructs coverage as such a prefix subtree and chooses `I` to defeat the candidate strengthening; we do not appeal to unrealizable singleton or finite coverage shapes.

*Containment from coverage to query (`coverage(Σ.L(a).eᵢ) ⊆ I`).* Witness: a slot `i` at link `a` with a single canonical span `(α, δ(1, #α))` (so `coverage(Σ.L(a).eᵢ) = {t ∈ T : α ≼ t}` by PrefixSpanCoverage (ASN-0043)) and `I = {α}`. Then `coverage(Σ.L(a).eᵢ) ∩ I = {α} ≠ ∅` — the only element of `I` extending `α` is `α` itself, by reflexivity of `≼` — so F1 includes `a`; but `coverage(Σ.L(a).eᵢ) ⊄ I` because `α.0 ∈ coverage(Σ.L(a).eᵢ)` (since `α ≼ α.0` by the definition of `≼` extending `α` with one further component) while `α.0 ∉ I` (the singleton `I = {α}` does not contain `α.0`, as `α ≠ α.0` by T3 (CanonicalRepresentation, ASN-0034) on differing lengths). One subtlety to surface explicitly: `α.0` is a tumbler in `T` (per T0 (CarrierSetDefinition, ASN-0034), any finite sequence of naturals with length ≥ 1) but is not itself a T4-valid address (it ends in a zero, violating T4's last-component condition). PrefixSpanCoverage (ASN-0043) defines coverage as `{t ∈ T : α ≼ t}` — ranging over the full carrier set `T`, not the restricted subset of T4-valid addresses — so `α.0` is legitimately in `coverage(Σ.L(a).eᵢ)` even though it could not itself serve as an element-level address. The strengthening excludes `a`; F1's matching pair is excluded by the strengthening.

*Containment from query to coverage (`I ⊆ coverage(Σ.L(a).eᵢ)`).* Witness: a slot `i` at link `a` with the same canonical span `(α, δ(1, #α))` (so `coverage(Σ.L(a).eᵢ) = {t : α ≼ t}`) and `I = {α, γ}` for any `γ ∈ T` with `α ⋠ γ` — for example, a same-length sibling of `α` that agrees with `α` on positions `1..#α − 1` but disagrees at position `#α`; the prefix-extension condition fails at position `#α`, so `α ⋠ γ`. Then `coverage(Σ.L(a).eᵢ) ∩ I = {t : α ≼ t} ∩ {α, γ} = {α} ≠ ∅` (since `α ≼ α` puts `α` in the intersection while `α ⋠ γ` keeps `γ` out), so F1 includes `a`; but `I ⊄ coverage(Σ.L(a).eᵢ)` because `γ ∈ I` and `γ ∉ {t : α ≼ t}` (by `α ⋠ γ`), so the strengthening excludes `a`.

*Cardinality threshold (`|coverage(Σ.L(a).eᵢ) ∩ I| ≥ k` for any fixed `k > 1`).* Witness: the same canonical span `(α, δ(1, #α))` (so `coverage(Σ.L(a).eᵢ) = {t : α ≼ t}`) and `I = {α}`. Then `coverage(Σ.L(a).eᵢ) ∩ I = {α}` (as computed in the first witness above), so F1 includes `a` via the singleton intersection; but `|{α}| = 1 < k`, so the strengthening excludes `a`. The argument is parametric in `k > 1`: a singleton intersection witnesses F1's existential and lies below every threshold strictly greater than one.

*Any other refinement (reachable exclusions).* We strengthen the universal claim: any predicate `P` that excludes a *reachable* F1-admitted pair `(a, I)` — meaning `(a, I)` is realizable as a link configuration and query I-set in some conforming state — defines a different match predicate, and the implementation gap is operationally observable as an excluded link in that state. The qualification on reachability matters: an unreachable exclusion would produce a `P` and an F1 that agree on all conforming behavior, making the distinction predicate-definitional rather than operational. We close this gap by showing that the entire space of F1-admitted pairs is reachable, regardless of which shapes the three enumerated strengthenings cover or fail to cover.

The realizability discharge is *universal in endset configuration*. The three enumerated witnesses use single canonical spans because they suffice for the three enumerated strengthenings: each of containment from coverage to query, containment from query to coverage, and cardinality threshold is defeated by a single-canonical-span witness. But strengthenings outside the enumeration may admit single-canonical-span pairs while rejecting other F1-admitted shapes. For example, "F1 ∧ #spans(eᵢ) ≥ 2" (every witnessing slot must carry at least two spans) rejects single-span witnesses while admitting multi-span ones; "F1 ∧ |Σ.L(a)| ≥ 4" (the witnessing link must have arity at least 4) rejects standard-triple links while admitting higher-arity ones; "F1 ∧ home(a) = d_0" (the witnessing link must be allocated under a fixed document) rejects links allocated under other documents. For any such strengthening `P`, the witness shape that defeats `P` is whatever F1-admitted (endset configuration, I-set) pair `P` rejects. The realizability of every such shape follows from the same K.λ + L4 argument as for the three enumerated cases, applied to the relevant shape — we do not need to re-derive realizability per shape, because K.λ's free endset choice and L4's address freedom cover the entire space of F1-admitted endset configurations uniformly.

The realizability discharge is global. For any candidate F1-admitted pair `(a, I)` — a link with arbitrary endset configuration and an arbitrary query I-set — we exhibit a conforming state in which `(a, I)` realizes. The construction extends any base state Σ with `dom(Σ.M) ≠ ∅` as follows. Such a base state is itself reachable from the initial state Σ₀ (ASN-0047, with `dom(M₀) = ∅`) by the standard K.δ entity-creation chain — a K.δ at `k = 2` from the bootstrap node `n₀` placing an account into `E_account`, followed by a K.δ at `k = 2` from that account placing a document into `E_doc`, which by K.δ's effect in the IsDocument case simultaneously initializes `M(d_new) = ∅` and registers `d_new` into `dom(M)`. After two K.δ steps `dom(M)` is non-empty, so the realizability discharge applies to a state genuinely reachable from Σ₀, not merely a hypothetical extension. K.λ (LinkAllocation, ASN-0093) admits, at any such state, the allocation of a link with arity `N ≥ 3` whose endset sequence `(e₁, ..., e_N)` is freely chosen subject only to K.λ's well-formedness preconditions: each `eᵢ ∈ Endset` (well-formed span-set, where Endset is `𝒫_fin(Span)` — any finite set of well-formed spans, of any cardinality including 0 at non-type slots and any positive integer otherwise) and `e₃ ≠ ∅` (non-empty type slot). L4 (ASN-0043) places no constraint on which addresses the spans in any endset may reference. The query I-set is independent of state — it is a parameter of the query, not a state component — so any `I ⊆ T` is admissible. Therefore *every* F1-admitted (endset configuration, I-set) pair — including those with multi-span endsets, higher arities, cross-document address references, or any other shape `P` might privilege — is realizable by a K.λ allocation with that endset configuration, regardless of how many spans the endsets carry, how many slots the link occupies, or which addresses the spans reference. The three enumerated witnesses are illustrative concrete instances; the universal closure rests on K.λ's free endset choice covering every F1-admitted endset shape.

*Parametric factoring of the realization.* The phrasing "any pair `(a, I)` is realizable" can mislead, so we surface the factoring explicitly. The witness link's address `a` is *not* an independently chosen parameter — it is determined by K.λ's chain discipline: the first-emission predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅` fires at chain index 1, fixing `a = [d.0.s_L.1]`, and the subsequent-emission formula `a = inc(ℓ_prev, 0)` (with `ℓ_prev` the max of the prior emissions under `d`, by SubAllocatorAxiom.ChainDiscipline, ASN-0093) fixes `a` at every chain index `k ≥ 2`. What K.λ admits as a free choice at its commitment step is the *endset tuple* `(e₁, …, e_N)`, subject only to the well-formedness preconditions above; the query I-set is independently free. The match predicate `matches(a, I, Σ)` factors through the endset tuple — two links with identical endset configurations have identical match status against any fixed `I` — so what F4's realizability requires is realization of every (endset configuration, I-set) shape admitted by F1, and K.λ's free endset choice supplies exactly that. L1c (LinkAllocatorConformance, ASN-0043) closes the inclusion in the other direction: every `a ∈ dom(Σ.L)`, and hence every F1-admitted link address arising in any conforming state, inhabits some `A_L(d)` chain, so the realization space (the set of K.λ-reachable addresses) covers the F1-admission space (the set of addresses that may appear in F1's existential at any reachable state).

*Base construction at higher chain indices.* The "single K.λ step" reading is exact when the witness sits at chain index 1 of `A_L(d)`: the first-emission predicate fires at the initially-empty `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`, and the K.λ step that follows the two-step K.δ prelude is the witness step. For witness chain indices `k ≥ 2`, the base must additionally have received `k − 1` prior K.λ allocations under `d` — each K.λ step under `d` advances `A_L(d)` by exactly one (SubAllocatorAxiom.ChainDiscipline, ASN-0093), and the chain element at index `k` is reached only after `k − 1` prior advancements. The prior K.λ steps may carry arbitrary well-formed endsets; their endsets are immaterial to the witness's match status, since `matches` consults only the witness link's endsets. The realization is therefore "extending an *appropriately-set-up* base via a *final* K.λ step that produces the witness link with the chosen endsets": the prelude consists of two K.δ steps (to reach `dom(M) ≠ ∅`) followed by `k − 1` K.λ steps under `d` (to advance the chain to index `k − 1`), and the final K.λ at chain index `k` is the realization step that commits the witness link with the chosen endsets. The three enumerated cases above are concrete instances of this construction at canonical-span coverage shapes; the general result covers every F1-admitted (endset configuration, I-set) shape regardless of coverage shape and regardless of which chain index the witness's address occupies.

Combined with the strengthened universal claim, the realizability discharge gives operational minimality: any strengthening that excludes any F1-admitted pair excludes a witness that some conforming state realizes, and the implementation gap is observable as an excluded link in that state. The abstract uniqueness conclusion is therefore not merely predicate-theoretic but operationally binding — F1 is the unique match predicate satisfying both halves of the conformance contract over all reachable F1-admissions.

The reader's promise rests on this singleton-overlap reading, as argued above for the "Why intersection" choice: a link is about every byte its endset names (L13, ASN-0043), and one shared byte is one shared byte. F4 records that this minimality is not optional: alternative match formulas are alternative operations, not alternative implementations of FINDLINKS. Conforming implementations are bound to F1 as the unique match predicate against which F2 ∧ F3 are evaluated.

**Empty endsets at non-type slots.** L3 (ASN-0043) requires only the type-endset (slot 3) to be non-empty; any other slot may carry the empty endset. An empty endset has `coverage(∅) = ∅` (the empty union), so the intersection `coverage(Σ.L(a).eᵢ) ∩ I = ∅` for every `I` whenever `Σ.L(a).eᵢ = ∅`. The slot-existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` is therefore never witnessed by an empty slot — but other non-empty slots of the same link may still witness it. The match predicate accommodates empty endsets mechanically: a link with `Σ.L(a).e₁ = ∅` and a non-empty `Σ.L(a).e₂` whose coverage meets `I` still matches `I`, via slot 2. The filtered form behaves differently: a filter constraint `(i, J)` is satisfied at slot `i` iff `i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅`, and when `Σ.L(a).eᵢ = ∅` the right conjunct is false for every `J`, so any constraint naming slot `i` is unsatisfiable at that link. A filtered query that explicitly nominates an empty slot therefore excludes the link from its result, even when other slots' coverages would have admitted it under the unfiltered match.

Note two distinct short-circuits for an unsatisfied per-constraint conjunct of the filtered match: when `i > |Σ.L(a)|`, the *left* conjunct `i ≤ |Σ.L(a)|` is false and short-circuits the conjunction — the slot does not exist on this link (a structural mismatch between the constraint's positional reference and the link's arity); when `i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅`, the left conjunct passes but the *right* conjunct `coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` is false for every `J` — the slot exists but its coverage is empty (a structurally present slot whose endset carries no spans). Both paths produce the same outcome (the constraint is unsatisfiable at `a`, so the link is excluded from the filtered result) via distinct argumentative routes. Implementation-side, the distinction is useful for diagnostics — "wrong link kind" (slot index out of range, e.g. asking a 3-endset link to satisfy a constraint at slot 4) vs. "incomplete link" (slot is present but its endset has not been populated) — but abstract conformance is indifferent to which short-circuit fires first.

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

The abstract specification `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` is one set — uniquely determined by `(Σ.L, I)`. A conforming implementation must produce *exactly* this set in response to the query. We let `result : 𝒫(T) × 𝒮 → 𝒫(T)` denote a conforming implementation's actual output function, where `𝒮` is the Xanadu system state space — states of the form `Σ = (C, L, M, E, R, …)` carrying the substrate's content store, link store, arrangements, entity set, provenance relation, and any further components introduced downstream by ASN-0036, ASN-0043, ASN-0047, and ASN-0093. We use `𝒮` locally for this full-system state space; it is distinct from ASN-0034's AllocatedSet, which scopes its own state space to allocator-tree configurations alone. The codomain is the powerset of `T`, matching `findlinks`'s codomain. The signature commits the implementation to *functionality* — `result(I, Σ)` is uniquely determined by `(I, Σ)`, with no non-deterministic dependence on any other variable, and any two evaluations on equal arguments yield equal outputs. We state completeness and soundness as the two halves of the conformance obligation pinning `result` to `findlinks`:

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

Together F2 and F3 force `result(I, Σ) = findlinks(I, Σ)` — there is exactly one conforming output set. The same conformance obligation transfers to the filtered, scoped, and V-side forms, and we state each formally so the claims table pins each abstract operation to a named implementation contract. We let `result_filtered : 𝒫(ℕ⁺ × 𝒫(T)) × 𝒮 → 𝒫(T)`, `result_scoped : 𝒫(T) × 𝒫(T) × 𝒮 → 𝒫(T)`, and `result_V : 𝒫(T) × T × 𝒮 → 𝒫(T)` denote conforming implementations' actual output functions for the filtered, scoped, and V-side operations — `𝒮` here is the same full-system state space defined above — each functional in its arguments by the same hypothesis applied to `result` above. `result_V` inherits its defined-when condition from `findlinks_V`: defined precisely when `d ∈ dom(Σ.M)`, with the conformance contract below quantifying only over such `(R, d, Σ)`.

```
F2-filt (FilteredCompleteness):
   For every a ∈ dom(Σ.L):
       (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)
         ⟹ a ∈ result_filtered(C, Σ).
   Equivalently: findlinks_filtered(C, Σ) ⊆ result_filtered(C, Σ).
```

```
F3-filt (FilteredSoundness):
   For every a ∈ result_filtered(C, Σ):
       a ∈ dom(Σ.L) ∧ (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅).
   Equivalently: result_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ).
```

```
F2-sco (ScopedCompleteness):
   For every a ∈ dom(Σ.L) ∩ S:
       matches(a, I, Σ) ⟹ a ∈ result_scoped(I, S, Σ).
   Equivalently: findlinks_scoped(I, S, Σ) ⊆ result_scoped(I, S, Σ).
```

```
F3-sco (ScopedSoundness):
   For every a ∈ result_scoped(I, S, Σ):
       a ∈ dom(Σ.L) ∩ S ∧ matches(a, I, Σ).
   Equivalently: result_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ).
```

```
F2-V (VSideCompleteness):
   For every R ⊆ T, d ∈ dom(Σ.M), and a ∈ dom(Σ.L):
       matches(a, image(R, d, Σ), Σ) ⟹ a ∈ result_V(R, d, Σ).
   Equivalently: findlinks_V(R, d, Σ) ⊆ result_V(R, d, Σ).
```

```
F3-V (VSideSoundness):
   For every R ⊆ T, d ∈ dom(Σ.M), and a ∈ result_V(R, d, Σ):
       a ∈ dom(Σ.L) ∧ matches(a, image(R, d, Σ), Σ).
   Equivalently: result_V(R, d, Σ) ⊆ findlinks_V(R, d, Σ).
```

F2-filt ∧ F3-filt forces `result_filtered(C, Σ) = findlinks_filtered(C, Σ)`; F2-sco ∧ F3-sco forces `result_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ)`; F2-V ∧ F3-V forces `result_V(R, d, Σ) = findlinks_V(R, d, Σ)` for every `R ⊆ T` and every `d ∈ dom(Σ.M)`. The six claims share the same conformance structure as F2 ∧ F3 — each pair pins the implementation's actual output to the abstract specification of the corresponding operation. Completeness for the filtered form requires every link satisfying *every* constraint in `C` to appear in the filtered output, and soundness rejects any spurious link. Completeness for the scoped form is restated *within the scope*: every link in `S ∩ dom(Σ.L)` satisfying the match predicate must appear, while soundness rejects links that fail the match or fall outside `S`. Completeness for the V-side form binds the reader-facing operation directly: every link whose endset coverage meets the I-image of the V-region must appear in `result_V(R, d, Σ)`, and soundness rejects any link absent from `dom(Σ.L)` or failing the match against the I-image.

F2-V ∧ F3-V pins `result_V(R, d, Σ)` to `findlinks_V(R, d, Σ)` exactly at every `(R, d, Σ)` with `d ∈ dom(Σ.M)`. Implementations may compute the V-side output by routing through an internal `result` function — `result_V(R, d, Σ) := result(image(R, d, Σ), Σ)`, in which case F2-V ∧ F3-V is a derived consequence of F2 ∧ F3 via the factoring equation and F12's definitional unfolding — or by any direct procedure that produces `findlinks_V(R, d, Σ)` exactly, in which case F2-V ∧ F3-V is a parallel conformance obligation. The choice is purely one of code organization within the implementation; the abstract spec produces the same `findlinks_V(R, d, Σ)` value in either case, so the *outputs* are identical at every `(R, d, Σ)`. An implementation exposing both surfaces must satisfy F2 ∧ F3 and F2-V ∧ F3-V coherently — either by asserting the factoring equation and discharging F2-V ∧ F3-V through F2 ∧ F3, or by satisfying both independently — but cannot disagree across the two surfaces, since both are pinned to the same abstract value.

A note on predicate domain. The match predicate `matches(a, I, Σ)` is defined only for `a ∈ dom(Σ.L)` — its definition consults `|Σ.L(a)|` (which requires `a ∈ dom(Σ.L)` so that `Σ.L(a)` is defined) and `Σ.L(a).eᵢ` (likewise). For `a ∉ dom(Σ.L)`, the predicate is undefined; we make no claim about its value, and no claim of this ASN takes such an `a` as an argument. The scope-filter intersection `dom(Σ.L) ∩ S` in F2-sco's universal and in F3-sco's conjunct keeps every quantification within the predicate's domain: F2-sco quantifies only over `a ∈ dom(Σ.L) ∩ S ⊆ dom(Σ.L)`, and F3-sco asserts `a ∈ dom(Σ.L) ∩ S` as part of the soundness conclusion, so the predicate is invoked only on `a ∈ dom(Σ.L)`. The boundary case `a ∈ S ∖ dom(Σ.L)` — addresses in the user-supplied scope that are not link addresses — is operationally excluded from the result by F3-sco's `a ∈ dom(Σ.L) ∩ S` clause, so the predicate is never invoked outside its domain at the implementation surface. This well-definedness convention applies uniformly to F2, F3, F2-filt, F3-filt, F2-sco, F3-sco, F2-V, and F3-V; we surface it here at the scoped pair because the scope set `S` is the only place where a user-supplied `S` could in principle drag a non-link address into the quantifier's range. F2-V and F3-V respect the convention by quantifying over `a ∈ dom(Σ.L)` (in F2-V's universal) and asserting `a ∈ dom(Σ.L)` (in F3-V's soundness conjunct).

F2 and F3 (and their variants F2-filt, F3-filt, F2-sco, F3-sco, F2-V, F3-V) are not tautologies of the abstract definitions — they are constraints on the separate symbols `result`, `result_filtered`, `result_scoped`, and `result_V`. At the level of the abstract operations alone the corresponding inclusions are trivial (a comprehension contains exactly those source elements satisfying its predicate, and only those); each abstract specification is one set. The named conformance claims acquire force precisely as the requirements that the implementations' actual outputs must coincide with their respective abstract sets.

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

The I→Link phase consults `Σ.L` and `I` alone. It does not consult any arrangement. F8 already encodes this in its hypothesis `Σ.L = Σ'.L`: `Σ.M` is unmentioned, so two states agreeing on the link store give equal results regardless of how their arrangements differ. Before stating the operationally salient specialisation as the frame condition exercised by editing operations, we surface one structural lemma of the substrate on which the derivation of survivability rests.

ASN-0093's operation specifications list every preserved component explicitly — K.σ, K.α, and K.λ each end with `L' = L`. ASN-0047's K.δ, K.μ~, and K.μ⁺_L likewise list `L' = L` in their published frames. Three operations in ASN-0047 omit `L` from their published frames: K.μ⁺ (its frame names only `C`, `E`, `R`, and per-document arrangement), K.μ⁻ (likewise), and K.ρ (whose frame names only `C`, `E`, and per-document arrangement). At each of these three transitions, L12 (LinkImmutability, ASN-0093) supplies per-link value preservation conditional on `a ∈ dom(L)`, and L12a (LinkStoreMonotonicity, ASN-0043) supplies `dom(L) ⊆ dom(L')`, but neither pins down equality `Σ'.L = Σ.L` directly — they permit but do not require `dom(L)` to remain fixed. We derive the missing equality as a pair of structural lemmas of this ASN — A1a below for the five operations whose published frames name `L' = L`, and A1b below for the three whose frames are silent on `L` — with A1b deriving the equality from the substrate's effect-clause convention together with the architectural separation between content and link state components. A1 packages the two sub-lemmas into a single composite claim covering all of V ∖ {K.λ}. The A1b derivation is supported by two convergent sources — design intent and implementation evidence — that ground the closed-world reading of the substrate effect-clause convention applied there; A1a requires no such grounding because the equality is published verbatim in the substrate frames.

```
A1a (PublishedFramePreservation) — derived structural lemma from
substrate-published frames:
   For every transition Σ → Σ' produced by an operation in the subset
   {K.σ, K.α, K.δ, K.μ~, K.μ⁺_L} of V ∖ {K.λ} — the operations whose
   published frames in ASN-0047 and ASN-0093 list `L' = L` directly —
   the link store is preserved:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   The conclusion is immediate from the published frame at any
   transition of these operations and requires no further argument
   beyond reading the substrate spec.
```

```
A1b (ClosedWorldPreservation) — convention-grounded structural lemma:
   For every transition Σ → Σ' produced by an operation in the subset
   {K.μ⁺, K.μ⁻, K.ρ} of V ∖ {K.λ} — the operations whose published
   frames in ASN-0047 omit `L` from the frame clause — the link store
   is preserved:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   This ASN reads ASN-0047's effect-clause convention as closed-world:
   components absent from both effect and frame are preserved across
   the transition. We adopt this reading as the methodological default
   for this specification's evaluation of silent frames. The
   substrate-published lemmas L12 (LinkImmutability) and L12a
   (LinkStoreMonotonicity) supply only the directionally-correct
   halves of the equality — value preservation conditional on `a ∈
   dom(L)`, and `dom(L) ⊆ dom(L')` — and so leave room for `dom(Σ.L)
   ⊊ dom(Σ'.L)` (link allocation) at any operation whose frame is
   silent on L. The equality refinement `dom(Σ'.L) = dom(Σ.L)` at
   K.μ⁺, K.μ⁻, K.ρ is supplied by the closed-world reading, not by
   the substrate lemmas alone.

   Convergent grounding (non-constitutive). Two outside-the-foundation
   sources converge with — but do not constitute — the closed-world
   reading. (i) Nelson's design intent in Literary Machines requires
   that operations preserve state they do not explicitly modify: the
   Istream is append-only ("user makes changes, the changes difflessly
   into the storage system, filed, as it were, chronologically" at
   2/14), edits are non-destructive ("users may create new published
   documents out of old ones indefinitely, making whatever changes
   seem appropriate—without damaging the originals" at 2/45), and
   modification is restricted to the owner ("Only the owner has a
   right to withdraw a document or change it" at 2/29). The closed-
   world reading is one faithful way to discharge these principles
   for the substrate effect-clause convention; an open-world reading
   that derived preservation from the principles by an explicit
   side-condition on each operation would be equally faithful. (ii)
   Gregory's udanax-green implementation leaves the link store
   unmodified across the operations corresponding to K.μ⁺ (INSERT),
   K.μ⁻ (DELETE / `dodeletevspan`), and K.ρ (DOCISPAN insertion via
   `docopy`) — confirming that closed-world behavior at these three
   operations is the established implementation pattern, not merely
   an interpretive choice of the present ASN. Both sources are
   *convergent*: they support the same conclusion that A1b reaches
   via the closed-world reading, but the methodological commitment
   remains primary because the substrate spec does not formally
   axiomatise the convention.

   Why not a substrate revision. A foundation revision — publishing
   `L' = L` explicitly in the three silent frames of ASN-0047, or
   axiomatising the closed-world convention as a substrate-level
   meta-axiom — would discharge A1b directly and remove the
   convention-grounded interpretive commitment from every downstream
   invocation. We prefer the local methodological commitment in
   ASN-0099 for two reasons. First, scope: revising ASN-0047 is a
   substrate-level amendment whose impact extends to every consumer
   of the operation vocabulary (not just discovery-side ASNs), and
   ASN-0099 should not unilaterally commit the substrate to a
   convention that other downstream ASNs may not need or may
   articulate differently. Second, separability: tagging A1b with
   convention status keeps the interpretive commitment surfaced at
   the citation site of every claim that depends on it, so a future
   substrate revision can replace A1b's convention-grounded reading
   with an axiomatised one cleanly — removing the tag without
   restructuring the dependent claims. Readers who reject the
   closed-world reading must restate A1b against an alternative
   interpretation or weaken its conclusion at these three operations.
```

```
A1 (LinkStoreInertOfNonAllocatingOperations) — composite structural
lemma:
   For every transition Σ → Σ' produced by an operation in V ∖ {K.λ},
   the link store is preserved:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   Equivalently, K.λ is the unique operation of the substrate
   vocabulary V that modifies the link store.

   A1 is the union of A1a (PublishedFramePreservation, covering
   K.σ, K.α, K.δ, K.μ~, K.μ⁺_L from their published `L' = L` frames)
   and A1b (ClosedWorldPreservation, covering K.μ⁺, K.μ⁻, K.ρ from
   the closed-world reading of the substrate's effect-clause
   convention). Because the operational reach of A1's contribution
   is *entirely* through A1b — the five operations covered by A1a
   discharge preservation directly from their published frames and
   never need A1 as an intermediate citation — downstream invocations
   of A1 at K.μ⁺, K.μ⁻, or K.ρ should be read as A1b citations and
   inherit A1b's convention-grounded status. Invocations at the
   remaining five operations are A1a citations and rest entirely on
   substrate-published frames.

   Vocabulary scope: V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~,
   K.μ⁺_L, K.ρ} as published in ASN-0047 and ASN-0093 at the time
   this ASN was written. Downstream ASNs consuming A1 against an
   evolved vocabulary must restate the claim — including its A1a /
   A1b partition — against the then-current operation set.
```

The split of A1 into A1a and A1b makes the methodological status of each derivation step visible at the citation surface. A1a is a routine derivation from substrate-published text — citing A1a at K.σ, K.α, K.δ, K.μ~, or K.μ⁺_L invokes only the relevant published frame clause, with no further interpretive commitment. A1b, by contrast, is convention-grounded — citing A1b at K.μ⁺, K.μ⁻, or K.ρ commits to the closed-world reading of the substrate's effect-clause convention, and downstream readers should understand the citation as inheriting that interpretive commitment.

The closed-world reading underlying A1b deserves expanded statement here, since A1b is the load-bearing premise behind every downstream invocation that this ASN cites against the three silent-frame operations.

*The closed-world reading.* The substrate's effect-clause convention is that an operation's effect clause is a complete enumeration of every state-component modification the operation makes, with components absent from both the effect and the frame held unchanged. K.μ⁺'s effect (ASN-0047) names only extensions to `dom(M(d))`; K.μ⁻'s effect names only contractions of `dom(M(d))`; K.ρ's effect names only an addition to `R`. None of these effect clauses names `L`, `dom(L)`, or any sub-component of the link store. Under the closed-world reading, the absence of `L` from an effect clause is equivalent to `Σ'.L = Σ.L`. The substrate ASNs (ASN-0047, ASN-0093) do not explicitly axiomatise this reading; A1b adopts it as the methodological default for this ASN's evaluation of silent frames. As A1b's statement records, two convergent grounding sources support the choice (Nelson's design-intent principles of append-only, non-destruction, and owner-only modification; Gregory's udanax-green implementation showing link-store invariance at INSERT, DELETE, and `docopy`), though neither is constitutive — the methodological commitment remains primary. The alternative interpretation — that silent frames leave the component's evolution unconstrained — would deny A1b its conclusion and require the substrate to either publish `L' = L` explicitly in the three frames or axiomatise the closed-world convention; for the reasons stated in A1b's "Why not a substrate revision" paragraph, the present ASN does not attempt that revision and instead adopts the methodological reading locally.

A1's load-bearing role in this ASN is bounded to exactly three operations of V — K.μ⁺, K.μ⁻, and K.ρ — and these are precisely the operations covered by A1b. The five remaining non-allocating operations (K.σ, K.α, K.δ, K.μ~, K.μ⁺_L) are covered by A1a and inherit preservation from their own published frame clauses, so A1 is the bridge across which this ASN's derivations transport the unmentioned `L' = L` conjunct from ASN-0047's frames *only at the three silent-frame operations* — and the A1b sub-lemma is the precise load-bearing component. Readers auditing the chain of derivations should treat each A1 invocation at K.μ⁺, K.μ⁻, or K.ρ as an A1b invocation that inherits the convention-grounded interpretive commitment; A1 invocations at the other five operations are A1a invocations that inherit nothing beyond the published frames.

We now state the specialisation:

```
F9 (LinkSurvivabilityUnderEdits):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d — K.μ⁺ (content extension), K.μ⁻ (contraction),
   K.μ~ (reordering), or K.μ⁺_L (link extension) — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   Premise: A1b (ClosedWorldPreservation), invoked at the K.μ⁺ and K.μ⁻
   sub-cases of the derivation below. A1b is the convention-grounded
   sub-lemma of A1 — F9 inherits A1b's interpretive commitment to the
   closed-world reading at these two sub-cases. The K.μ~ and K.μ⁺_L
   sub-cases of F9 are discharged from their own published `L' = L`
   frames (an A1a invocation in the partition of A1) and carry no
   convention-grounded commitment.
```

F9 follows from F8 once we observe that `Σ'.L = Σ.L` at every K.μ-family transition. The derivation splits into two cases.

*K.μ~ and K.μ⁺_L.* These operations state `L' = L` explicitly in their frame clauses (ASN-0047), so the F8 hypothesis is satisfied directly from the published frame.

*K.μ⁺ and K.μ⁻.* These operations do not list `L` in their published frames in ASN-0047 — their frames cover `C`, `E`, `R`, and the per-document arrangement clause `(A d' : d' ≠ d : M'(d') = M(d'))`, but say nothing about `L`. A1b (ClosedWorldPreservation) supplies the preservation as a convention-grounded structural lemma of this ASN, with the derivation discharged from the substrate's effect-clause convention under the closed-world reading adopted methodologically in A1b's statement. A1b's conclusion `dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))` at every K.μ⁺ and K.μ⁻ transition is `Σ.L = Σ'.L` as partial functions. This is consistent with — and in the value-preservation conjunct, exactly the restriction to existing entries of — L12 (LinkImmutability, ASN-0093). The F8 hypothesis is satisfied at K.μ⁺ and K.μ⁻ transitions, with the interpretive commitment to the closed-world reading discharged by A1b.

For completeness, the substrate-level view of which operations modify `L`: the full operation vocabulary is exactly {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ}. Among these, K.λ is the unique operation whose effect clause names `L`: K.λ's effect is `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}` (ASN-0093 K.λ). Every other operation's effect clause modifies only non-L state components — K.σ modifies `dom(M)` and `M(d_new)`; K.α modifies `C`; K.δ modifies `E` (and `M(d_new)` in the IsDocument case); K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L modify a specific `M(d)`; K.ρ modifies `R`. The composite A1 packages this enumeration together with its A1a / A1b partition into the single structural lemma that K.λ is the unique L-modifying operation in V — with A1a covering the five operations whose published frames name `L' = L` and A1b covering the three whose frames are silent on `L`.

We state F9 separately because it names the operation classes by which arrangements actually change, and so reads as a direct survivability promise: editing does not invalidate discovery. K.α, K.λ, K.δ, K.ρ, and K.σ touch one of the non-arrangement components and so fall outside F9's scope; the K.μ family is exactly the editing surface against which links must remain findable.

```
F9-cor (NonAllocatingPreservation):
   For every single-step transition Σ → Σ' produced by an operation in
   V ∖ {K.λ} — that is, every substrate operation other than the unique
   link-allocating operation K.λ — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').
```

By F8, it suffices to verify `Σ.L = Σ'.L` at every such transition. Splitting V ∖ {K.λ} by the source of the preservation: K.σ, K.α, K.δ, K.μ~, and K.μ⁺_L each name `L' = L` directly in the published frame (an A1a invocation in the A1 partition); K.μ⁺, K.μ⁻, and K.ρ omit `L` from the published frame and inherit `Σ.L = Σ'.L` from A1b (ClosedWorldPreservation), which covers all three operations uniformly as the convention-grounded half of A1. K.ρ enters A1b's scope on the same structural footing as K.μ⁺ and K.μ⁻: its effect modifies only `R`, naming no sub-component of `L`, so the closed-world reading adopted in A1b's statement applies uniformly and yields `Σ.L = Σ'.L` at K.ρ transitions. F9-cor therefore inherits A1b's closed-world interpretive commitment at the K.μ⁺, K.μ⁻, and K.ρ sub-cases, while the remaining five sub-cases rest entirely on substrate-published frames.

K.δ has three sub-cases (IsNode, IsAccount, IsDocument), and the IsDocument sub-case modifies `M(d_new)` (setting it to `∅`) in addition to extending `E`. F9-cor's conclusion `findlinks(I, Σ) = findlinks(I, Σ')` is unaffected by this M-modification: the comprehension `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` consults only `dom(Σ.L)`, the link values `Σ.L(a)`, and the query I-set, never `Σ.M`. K.δ's published frame includes `L' = L` uniformly across its three sub-cases, so F8's hypothesis `Σ.L = Σ'.L` is satisfied for K.δ as a whole regardless of which sub-case fires. (The V-side companion claim — that `findlinks_V(R, d, Σ) = findlinks_V(R, d, Σ')` across a K.δ-IsDocument step that introduces a fresh document — is the subject of ASN-0098's LP8 and is not what F9-cor asserts; F9-cor scopes to the I-level operation.)

F9-cor surfaces the full dependency surface of A1b in one place: only K.μ⁺, K.μ⁻, and K.ρ require A1b to discharge the F8 hypothesis, and these are precisely the three operations for which A1b is the load-bearing premise. The other five operations of V ∖ {K.λ} discharge the F8 hypothesis from A1a's coverage of their published `L' = L` frames, with no convention-grounded interpretive commitment. K.λ is the only operation of V that can change `findlinks(I, ·)` across a single step, and F19 below confirms that the change is monotone — additions only, never removals.

F9 lifts to multi-step sequences only under restrictive conditions. Operationally relevant sequences interleave K.λ with K.μ-family steps, and a K.λ step that allocates a new matching link adds to the result without removing anything — so findlinks-equality fails along the direction of strict growth. The multi-step claim that holds across every reachable sequence is the weaker inclusion `findlinks(I, Σ) ⊆ findlinks(I, Σ')`, which is F11 (PersistentDiscoverability) below; F11's derivation uses LP13 (UnconditionalLinkPersistence, ASN-0098) and does not invoke F9. The edit-only specialization, however, lifts to equality and is worth stating explicitly:

```
F9★ (EditOnlySurvivability):
   For any reachable transition sequence Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' in which every
   step Σᵢ → Σᵢ₊₁ is a K.μ-family operation (K.μ⁺, K.μ⁻, K.μ~, or K.μ⁺_L) and any
   I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   Premise: A1b (ClosedWorldPreservation), invoked once per K.μ⁺ and K.μ⁻
   step in the sequence. K.μ~ and K.μ⁺_L steps discharge from their own
   published frames (A1a). F9★ inherits A1b's closed-world interpretive
   commitment at every K.μ⁺ and K.μ⁻ step in the sequence.
```

The derivation is the per-step F9 chained by transitivity. Each step satisfies `Σᵢ.L = Σᵢ₊₁.L` by F9's derivation (drawing on A1b for the K.μ⁺ and K.μ⁻ sub-cases). Transitivity of equality across the finite chain yields `Σ.L = Σ₀.L = Σ₁.L = ... = Σₙ.L = Σ'.L`. F8 then forces `findlinks(I, Σ) = findlinks(I, Σ')`. F9★ is the multi-step closure of F9 within the edit-only fragment of the operation vocabulary; the moment a K.λ enters the sequence, the claim collapses to the strict inclusion of F11/F19.

F9★ naturally generalizes from the K.μ-family to the full non-allocating fragment V ∖ {K.λ}: editing operations are not the only ones that preserve `findlinks(I, ·)`, since by F9-cor every operation in V ∖ {K.λ} does. The multi-step closure across this broader fragment is the natural lift of F9-cor:

```
F9★-cor (NonAllocatingMultiStepPreservation):
   For any reachable transition sequence Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' in which
   every step Σᵢ → Σᵢ₊₁ is an operation in V ∖ {K.λ} — that is, any of K.σ,
   K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, or K.ρ — and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   Premise: A1b (ClosedWorldPreservation), invoked once per K.μ⁺, K.μ⁻,
   and K.ρ step in the sequence. K.σ, K.α, K.δ, K.μ~, K.μ⁺_L steps
   discharge from their own published frames (A1a). F9★-cor inherits
   A1b's closed-world interpretive commitment at every K.μ⁺, K.μ⁻, and
   K.ρ step in the sequence.
```

The derivation is the per-step F9-cor chained by transitivity. Each step satisfies `Σᵢ.L = Σᵢ₊₁.L` by F9-cor's derivation: K.σ, K.α, K.δ, K.μ~, and K.μ⁺_L from their own published `L' = L` frames (A1a), and K.μ⁺, K.μ⁻, K.ρ from A1b. Transitivity of equality across the finite chain yields `Σ.L = Σ₀.L = ... = Σₙ.L = Σ'.L`, and F8 forces `findlinks(I, Σ) = findlinks(I, Σ')`. F9★ is the specialization of F9★-cor to the K.μ-family fragment alone, kept as a separate named claim because the operationally salient sequence in the editing surface is exactly K.μ-only and reads as a direct survivability promise; F9★-cor covers the broader case of sequences that interleave editing with content allocation, document registration, or provenance recording — common in practice once the substrate accumulates non-trivial state. Both claims collapse to the strict inclusion of F11/F19 the moment a K.λ enters the sequence.

The V→I phase is sensitive to arrangement, of course — querying the same V-region before and after an edit may yield different I-images. But the link result for any *fixed* I-set is invariant under every K.μ-family step and monotone non-decreasing across every reachable sequence. The two-phase factoring keeps these concerns separate: V-volatility lives in phase 1; phase 2 is arrangement-blind in the K.μ-only setting and monotone in the general setting.

## Transclusion Transparency

When content at I-address `α` is transcluded into multiple documents, every V-position in every document that maps to `α` contributes `α` to its I-image when queried. Therefore the query result is the same regardless of which V-occurrence the reader queries:

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

The derivation chain unfolds in three steps. Direct evaluation of `image` on each singleton gives `image({v₁}, d₁, Σ) = {Σ.M(d₁)(v₁)} = {α}` (since the precondition `v₁ ∈ dom(Σ.M(d₁))` survives the projection `{v₁} ∩ dom(Σ.M(d₁)) = {v₁}`), and symmetrically `image({v₂}, d₂, Σ) = {α}`. By F12's definition of `findlinks_V`, each V-side query unfolds to its I-side comprehension: `findlinks_V({v₁}, d₁, Σ) = findlinks(image({v₁}, d₁, Σ), Σ) = findlinks({α}, Σ)`, and symmetrically `findlinks_V({v₂}, d₂, Σ) = findlinks({α}, Σ)`. Functional determinism of `findlinks` (one set per `(I, Σ)`) supplies `findlinks({α}, Σ) = findlinks({α}, Σ)` reflexively, closing the equality. The match predicate consulted only the I-image and the link store; how `α` came to be in `I` — through `d₁`'s native arrangement or `d₂`'s transclusion — is invisible to phase 2.

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
  = findlinks(image(R₁ ∪ R₂, d, Σ), Σ)              by F12 (def)
  = findlinks(image(R₁, d, Σ) ∪ image(R₂, d, Σ), Σ)  by F20
  = findlinks(image(R₁, d, Σ), Σ) ∪ findlinks(image(R₂, d, Σ), Σ)  by F13
  = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)   by F12 (def).
```

(The two F12 citations above mark definitional unfolding rather than derivation steps — F12 introduces `findlinks_V` as the named composite, so "by F12 (def)" reads "by definition". We mark them explicitly to distinguish from genuine implication steps elsewhere in the chain.)

A reader who selects two V-regions and asks for the links touching either receives the same answer as one who asks for each region separately and unions the results. The two-phase factoring distributes over set union at every stage.

## The Empty Query

The empty query is a meaningful boundary, and the abstract specification handles it without ceremony. For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential `(E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` has no witness, and `matches(a, ∅, Σ) = false` for every `a ∈ dom(Σ.L)`. The comprehension gives `findlinks(∅, Σ) = ∅`. Symmetrically, `image(∅, d, Σ) = {Σ.M(d)(v) : v ∈ ∅ ∩ dom(Σ.M(d))} = {Σ.M(d)(v) : v ∈ ∅} = ∅`, so `findlinks_V(∅, d, Σ) = findlinks(∅, Σ) = ∅`. A V-region `R` entirely disjoint from `dom(Σ.M(d))` is also a boundary handled uniformly: `R ∩ dom(Σ.M(d)) = ∅` projects to the empty image, and the V-side query returns `∅` without any error path.

The dual boundary is the empty link store. When `dom(Σ.L) = ∅`, the comprehension's source set is empty and `findlinks(I, Σ) = ∅` for every `I ⊆ T`. This is the bootstrap behaviour at the initial state Σ₀, where `L₀ = ∅` (ASN-0047): every query produces the empty result until the first K.λ allocates a link. F2 holds vacuously (the source set has no member to test); F3 holds vacuously (the result is empty); F10, F10-filt, F10-sco, and F11 hold vacuously for the same reason (the empty set admits the empty enumeration as its unique strictly increasing presentation). The reader querying an empty docuverse receives an empty answer, consistent with the natural reading and with the absence of any structure for the query to discover.

The empty query is the additive identity in F13: `findlinks(∅ ∪ I₂, Σ) = findlinks(I₂, Σ) = ∅ ∪ findlinks(I₂, Σ) = findlinks(∅, Σ) ∪ findlinks(I₂, Σ)`. F2 holds vacuously (no link satisfies the predicate); F3 holds vacuously (the result is empty); F8 and F9 are trivial since both sides of every equality are empty. The reader who selects no V-positions receives no links, in agreement with the natural reading.

A third boundary belongs to the filtered form: the *empty constraint set*. When `C = ∅`, the universal `(A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` is vacuously true at every `a ∈ dom(Σ.L)`, so `findlinks_filtered(∅, Σ) = dom(Σ.L)`. A query with no constraints returns every link in the store, in agreement with the natural reading — restricting by nothing is the same as not restricting at all. This is the conjunctive dual of the empty I-set case for `findlinks`: the empty universal returns everything, the empty existential returns nothing.

A fourth boundary specific to the filtered form is the *empty constraint target*: a constraint `(i, J) ∈ C` with `J = ∅`. The per-constraint conjunct `coverage(Σ.L(a).eᵢ) ∩ ∅ ≠ ∅` is `∅ ≠ ∅`, which is false at every link regardless of slot. The universal over `C` therefore fails uniformly, and `findlinks_filtered(C, Σ) = ∅` whenever any single constraint in `C` has empty target. This is distinct from the empty-slot case discussed earlier under F1 (where the link's own endset `Σ.L(a).eᵢ = ∅` defeats the slot only at the affected link); the empty-target case is a *query-side* boundary that defeats the filtered match uniformly, independently of which links are in the store and what their endsets look like. The natural reading agrees: asking for links whose slot `i` coverage meets the empty I-set is asking for an impossible condition, and the answer is nothing.

A fifth boundary belongs to the scoped form: the *empty scope*. When `S = ∅`, F14's intersection form gives `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅` for any I and any Σ, so a scoped query with empty scope produces the empty result by direct intersection. The natural reading agrees — restricting the candidate set to no links can yield only no links — and F19-sco's monotonicity holds vacuously (the empty inclusion is preserved across every reachable sequence).

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

The filtered comprehension's predicate `(A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)` consults only `(Σ.L, C)`: coverage is a function of the endset alone, `|Σ.L(a)|` is determined by `Σ.L(a)`, and `C` is the supplied query. Equality of `Σ.L` forces both `|Σ.L(a)| = |Σ'.L(a)|` and per-slot coverage equality `coverage(Σ.L(a).eᵢ) = coverage(Σ'.L(a).eᵢ)` at every `a ∈ dom(Σ.L)` — the former by L6 (ASN-0043)'s component-wise tuple equality on `Link` values (so the slot-index guard `i ≤ |Σ.L(a)|` evaluates identically at the two states for every constraint `(i, J) ∈ C`), the latter by the deterministic action of `coverage(·)` on equal endsets (the same fact F8 used). The universal `(A (i, J) ∈ C : ...)` therefore ranges over the same finite constraint set `C` at both states (`C` is query-data, not state-data, so its slot-index range is fixed by the query itself), and each per-constraint conjunct evaluates identically — every conjunct is true at one state iff true at the other, so the universal as a whole is true at one state iff true at the other. Set extensionality on the comprehensions closes the chain.

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

Every K.μ-family step preserves `Σ.L` (per F9's derivation, invoking A1b at the K.μ⁺ and K.μ⁻ cases and A1a at the K.μ~ and K.μ⁺_L cases). F15 then forces equality of the filtered result at the two states, via the same universal-quantifier carry-through argument given in F15: `Σ.L = Σ'.L` gives `|Σ.L(a)| = |Σ'.L(a)|` (by L6's component-wise tuple equality) and per-slot coverage equality (by `coverage(·)` determinism on equal endsets), so the universal `(A (i, J) ∈ C : ...)` ranges over the same `C` at both states and every per-constraint conjunct evaluates identically. F17 inherits A1b's closed-world interpretive commitment at K.μ⁺ and K.μ⁻ steps.

```
F18 (ScopedSurvivability):
   For any single-step transition Σ → Σ' produced by a K.μ-family operation
   on a document d, any I ⊆ T, and any S ⊆ T:
       findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ').
```

By F9, `findlinks(I, Σ) = findlinks(I, Σ')` across any K.μ-family step. Intersecting both sides with the same query-supplied `S` preserves the equality, yielding F18 directly. F18 inherits A1b's closed-world interpretive commitment transitively through F9 at the K.μ⁺ and K.μ⁻ sub-cases; the K.μ~ and K.μ⁺_L sub-cases discharge from F9's A1a coverage of their published `L' = L` frames.

The four claims share the same structural backbone as F8 and F9: the abstract-side comprehensions consult only `(Σ.L, query-data)`, and the K.μ family preserves `Σ.L`. We state them explicitly because filtered and scoped queries are the operationally common forms — the unfiltered, full-store `findlinks` is rarely what a reader-facing UI calls — and the determinism/survivability obligations propagate to them with the same force.

## Result Ordering

The result is a set, and a set carries no ordering. But the reader is shown an ordered list, and pagination demands that the order be stable across requests. We adopt the natural ordering: T1's lexicographic order on tumbler addresses. The result is presentable as a sequence:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence ⟨a₁, a₂, ..., aₙ⟩
   with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ), and a₁ < a₂ < ... < aₙ under T1.
```

Presentability as a finite sequence rests on finiteness, which we discharge explicitly. By F3, `result(I, Σ) ⊆ dom(Σ.L)`; by L-fin (ASN-0093), `|dom(Σ.L)| < ∞`; so `result(I, Σ)` is finite as a subset of a finite set. T1 (LexicographicOrder, ASN-0034) is a strict total order on `T`, and by trichotomy it restricts to a strict total order on any subset of `T`. Any non-empty finite totally-ordered set admits a unique enumeration in increasing order: by trichotomy of T1's restriction, the finitely many pairwise comparisons among its elements terminate and identify a unique minimum; the second-least is the least of the remainder, and so on by finite induction over the finite carrier. Finiteness — not well-ordering of T1's restriction (which is the stronger property that any non-empty *subset* of the carrier admits a least element, and which T1's restriction to a general subset of T need not satisfy) — is what makes the construction terminate. The ordering is therefore total, deterministic, and uniquely realized. Pagination is then well-defined: "the next N links past `aⱼ`" means the next N elements in the sorted sequence with addresses greater than `aⱼ` under T1.

The same canonical-presentation argument extends to the filtered and scoped result sets without modification. Filtered queries from a UI are at least as common as unfiltered ones, and pagination across filtered or scoped results imposes the same stability demand as for the unfiltered form. We state the two derivative claims explicitly so the filtered and scoped forms are not relegated to silent corollary status (matching the explicit treatment of F15–F18 for determinism and survivability, and F19-filt / F19-sco for monotonicity):

```
F10-filt (FilteredOrderedResult):
   The filtered result set findlinks_filtered(C, Σ) admits a unique
   presentation as a sequence ⟨a₁, a₂, ..., aₘ⟩ with each aⱼ ∈ dom(Σ.L)
   satisfying every constraint in C — `(A (i, J) ∈ C : i ≤ |Σ.L(aⱼ)|
   ∧ coverage(Σ.L(aⱼ).eᵢ) ∩ J ≠ ∅)` — and a₁ < a₂ < ... < aₘ under T1.
```

```
F10-sco (ScopedOrderedResult):
   The scoped result set findlinks_scoped(I, S, Σ) admits a unique
   presentation as a sequence ⟨a₁, a₂, ..., aₖ⟩ with each aⱼ ∈ dom(Σ.L) ∩ S
   satisfying matches(aⱼ, I, Σ), and a₁ < a₂ < ... < aₖ under T1.
```

Each derivation is a one-line lift of F10's argument, citing the comprehension structure directly rather than routing through the implementation-side conformance contracts F3-filt / F3-sco. For F10-filt: `findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : ...} ⊆ dom(Σ.L)` by the comprehension's source set; L-fin gives `|dom(Σ.L)| < ∞`; so `findlinks_filtered(C, Σ)` is finite as a subset of a finite set. T1's restriction to any subset of T is a strict total order, so the finite-strict-total-order-has-unique-enumeration argument used for F10 applies verbatim, yielding the unique strictly increasing sequence ⟨a₁, …, aₘ⟩. For F10-sco: `findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S ⊆ dom(Σ.L) ∩ S ⊆ dom(Σ.L)` by F14 and the comprehension's source set; L-fin gives finiteness; T1's restriction yields the unique strictly increasing sequence ⟨a₁, …, aₖ⟩. The structural argument is identical to F10's — finiteness of the result set under L-fin combined with T1's strict total order on any subset — and the same pagination-stability conclusions follow: "the next N filtered links past `aⱼ`" and "the next N scoped links past `aⱼ`" are well-defined in exactly the same way.

The presentation order recovers a creation-order property within each home document. By SubAllocatorAxiom.ChainDiscipline (ASN-0093), each document `d`'s link sub-allocator chain `A_L(d)` is generated by repeated `inc(·, 0)` from the first emission `[d.0.s_L.1]`. K.λ's *subsequent emission* precondition (ASN-0093) pins each new link allocation under `d` to the chain successor of the previously-most-recently-allocated link: `ℓ = inc(ℓ_prev, 0)` where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}` (with `max` taken under T1, equivalently the latest-allocated element by ChainEnumerationInjectivity below). The identification chain-index = K.λ-event-count for `d` rests on connecting K.λ's subsequent-emission precondition to the chain enumeration: ChainMembershipForOrigin (ASN-0093) places `dom(L) ∩ {ℓ' : origin(ℓ') = d}` as a contiguous prefix `{t_1, …, t_{m_d}}` of `A_L(d)`'s enumeration (where `t_i = inc^{i-1}(t_1, 0)` and `m_d` is the count of links allocated under `d` so far); ChainEnumerationInjectivity (ASN-0093) gives strict T1-ordering `t_1 < t_2 < ... < t_{m_d}` on this prefix (per-step `inc(t_n, 0) > t_n` by TA5(a), lifted across arbitrary gaps by T1 transitivity); so `max{t_1, …, t_{m_d}} = t_{m_d}` is the chain element at index `m_d` — equivalently, the most recently allocated link under `d`. K.λ's subsequent-emission precondition therefore pins the new allocation to `ℓ = inc(t_{m_d}, 0) = t_{m_d + 1}`, advancing the chain index by exactly one per K.λ event. The chain index of a link within `A_L(d)` equals the K.λ event count for `d` at the moment of that allocation, and the chain remains strictly T1-increasing across the entire allocation history. The three facts compose: chain index = K.λ event count = T1 rank within `A_L(d)`. So sorting link addresses within a single home document by T1 yields exactly the order in which they were allocated.

For the cross-document part of the ordering claim, we derive that addresses with the same `home(·)` group together and that home documents themselves order lexicographically. The cross-document derivation rests on a recurring lifting pattern — from document-level T1 ordering to anchor-level T1 ordering — which we name as a labeled lemma so subsequent invocations of the pattern can cite a discrete handle rather than re-deriving the lifting inline:

```
F10a (AnchorLiftingOfDocumentOrdering):
   For documents d₁, d₂ ∈ dom(Σ.M) with `zeros(d₁) = zeros(d₂) = 2`
   (M0, ASN-0093) and `d₁ < d₂` under T1, the link sub-allocator
   anchors satisfy `b_L(d₁) < b_L(d₂)` under T1, and they are
   non-nesting under `≼`. By PrefixOrderingExtension (ASN-0034),
   every `ℓ₁` extending `b_L(d₁)` is strictly less than every `ℓ₂`
   extending `b_L(d₂)`. The lifting splits by T1 case on `d₁ < d₂`:

   *Case (i) (component divergence on documents).* The divergence
   position `k ≤ min(#d₁, #d₂)` with `d₁_k < d₂_k` carries over to
   `b_L(d₁) vs b_L(d₂)` at the same position, since each anchor
   agrees with its document on positions `1..#d`. T1 case (i) at
   position `k` yields `b_L(d₁) < b_L(d₂)`. The anchors are
   non-nesting because they share positions `1..k − 1` but disagree
   at position `k`, and this disagreement is strict (T1 case (i)
   gives strict inequality of components).

   *Case (ii) (proper prefix on documents).* `d₁ ≺ d₂` (so
   `#d₁ < #d₂`) forces `d₂_{#d₁+1} ≥ 1` — both documents satisfy
   `zeros(·) = 2` by M0 (ASN-0093), so the proper extension cannot
   introduce a zero — and at position `#d₁+1`, `b_L(d₁)` has the
   appended `0` separator (from `b_L(·) = [·.0.s_L]`) while `b_L(d₂)`
   has `d₂_{#d₁+1} ≥ 1`. The anchors have lengths `#b_L(d₁) = #d₁ + 2`
   and `#b_L(d₂) = #d₂ + 2 ≥ #d₁ + 3`, so the divergence position
   `#d₁ + 1` satisfies `#d₁ + 1 ≤ #d₁ + 2 = min(#b_L(d₁), #b_L(d₂))`.
   T1 case (i) at position `#d₁ + 1` (note: case (ii) on documents
   becomes case (i) on anchors because the appended `.0.s_L`
   introduces a divergence position before either anchor terminates)
   yields `b_L(d₁) < b_L(d₂)`. The anchors are non-nesting because
   they disagree at position `#d₁ + 1`, which is internal to both
   anchors.
```

F10a does not require independent invocation of CrossDocDisjointness (ASN-0093) for non-nesting: the case-by-case derivation establishes non-nesting locally as a consequence of the strict component disagreement at the divergence position. (CrossDocDisjointness remains the substrate-level statement of cross-document anchor non-nesting; F10a's derivation produces the same non-nesting fact at the anchor level as a structural consequence of the T1 lifting, with the divergence position made explicit.)

Returning to the cross-document ordering of links: ChainMembershipForOrigin (ASN-0093) places every link address `ℓ` with `home(ℓ) = d` in `A_L(d)`, and ChainPrefixExtension (ASN-0093) gives `b_L(d) ≼ ℓ` for every such `ℓ`. For documents `d₁ < d₂`, F10a lifts to `b_L(d₁) < b_L(d₂)` with the anchors non-nesting, and PrefixOrderingExtension (ASN-0034) lifts to every extension: every `ℓ₁` extending `b_L(d₁)` is strictly less than every `ℓ₂` extending `b_L(d₂)`. So under T1, link addresses with the same `home(·)` group together as a contiguous T1-block (all extending the common anchor `b_L(d)`), and the blocks for distinct documents sort by their documents' tumblers.

The reader sees results in a canonical, repeatable order: links within a document in allocation order, documents in tumbler order. The lift from these pairwise orderings to an n-document presentation is *not* an inductive iteration of case analysis. F10a's case (i)/(ii) lifting applies once per document pair, supplying a strict inequality `b_L(d_i) < b_L(d_j)` for every pair `(d_i, d_j)` with `d_i < d_j` — case (i) at non-nesting document pairs, case (ii) at version-extension pairs. PrefixOrderingExtension (ASN-0034) lifts each pairwise inequality to every link-address extension. T1's postconditions (a) irreflexivity, (b) trichotomy, and (c) transitivity (ASN-0034) quantify universally over T, so each specializes by instantiation to any S ⊆ T — restricting the quantified variables to S preserves the postcondition — yielding a strict total order on S. Applied at S = the finite set of link addresses across the n documents, the restriction of T1 is itself a strict total order on this set, and the pairwise strict inequalities supplied by the per-pair F10a + PrefixOrderingExtension applications are exactly the constituents of that strict total order. The order ranks the n link blocks uniquely. The case analysis settles pairs; T1's restriction-to-subset chains them. No inductive case analysis beyond the pairwise machinery is needed because the chaining mechanism is T1 itself.

For the version-extension specialization (a three-document instance the worked example exercises directly): case (ii) at the parent–version pair gives `b_L(d_parent) < b_L(d_version)`, case (i) at the parent–sibling pair gives `b_L(d_parent) < b_L(d_sibling)` (with the sibling allocated after the parent under the same account), and a separate case (i) at the version–sibling pair places the version's anchor below the sibling's. PrefixOrderingExtension yields `ℓ_parent < ℓ_version < ℓ_sibling` across the three blocks — a version's link block sits between its parent's block and the parent's siblings' blocks. The specific instance `ℓ < ℓ_v < ℓ'` is the one exhibited in the worked example's "Verifying F10 across a version extension" paragraph below.

The chronological reading of T1 order is local to a single home document. Across documents, T1 reflects the lexicographic order of home tumblers, NOT the operation-history order of K.λ events: two documents may interleave their K.λ commitments across the operation history in any order admitted by SequentialTransitionAxiom (ASN-0093), and the result presentation will still group every document's links together by `home(·)`. Within a home document, T1 = K.λ order; across home documents, T1 is canonical and deterministic but does not track the K.λ event sequence of the underlying operation history.

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

Monotonicity propagates to the filtered and scoped forms with the same force. We state both explicitly so that the operationally common forms are not relegated to silent corollary status (matching the explicit treatment of F15–F18 for determinism and survivability):

```
F19-filt (FilteredMonotonicity):
   For any reachable state sequence Σ →* Σ' and any finite set of slot constraints C:
       findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ').
```

```
F19-sco (ScopedMonotonicity):
   For any reachable state sequence Σ →* Σ', any I ⊆ T, and any S ⊆ T:
       findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ').
```

F19-filt tracks F11 directly, with the universal-quantifier structure of the filtered predicate carrying through LP13's per-link value preservation just as the existential in `matches` does in F11's lift. For any `a ∈ findlinks_filtered(C, Σ)`, every constraint `(i, J) ∈ C` is satisfied at `a` in `Σ` — `i ≤ |Σ.L(a)|` and `coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅`. LP13 (UnconditionalLinkPersistence, ASN-0098) gives `a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)` across any reachable sequence; by L6 (ASN-0043)'s component-wise tuple equality on `Link` values, this forces `|Σ'.L(a)| = |Σ.L(a)|` and per-slot endset equality `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` for every `i` in the common slot range; per-slot coverages are then identical at the two states by the deterministic action of `coverage(·)` on equal endsets (the same fact F8, F15, and F11's derivation used). The universal `(A (i, J) ∈ C : ...)` therefore ranges over the same finite constraint set `C` at both states, and every per-constraint conjunct continues to hold at `Σ'` — both the slot-index guard `i ≤ |Σ'.L(a)|` and the coverage-overlap condition `coverage(Σ'.L(a).eᵢ) ∩ J ≠ ∅` evaluate identically to their `Σ`-side counterparts. So `a ∈ findlinks_filtered(C, Σ')`. F19-sco follows from F19 by intersection-preservation: `findlinks(I, Σ) ⊆ findlinks(I, Σ')` (F19) implies `findlinks(I, Σ) ∩ S ⊆ findlinks(I, Σ') ∩ S` for the query-supplied `S`, which by F14 is `findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ')`.

F19 (together with F19-filt and F19-sco) is the load-bearing consequence behind any indexed implementation's promise: an index that mirrors `findlinks` — or its filtered or scoped variant — is *never required to remove entries* as the state evolves, only to add them. The discovery operation is monotone non-decreasing in the link store at the set level across all three abstract forms, so indexes can be append-only just like the link store itself.

## A Worked Example

The abstract specification is short enough that it can read as content-free without an instance to anchor it. We fix a small one.

Consider a state `Σ` with two documents, both inhabiting `dom(Σ.M)`.

- `d_a` is a content-bearing document. Its content sub-allocator `A_C(d_a)` (ASN-0093) has produced three I-addresses: `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each placed into `dom(Σ.C)` by successive K.α steps with values `v₁, v₂, v₃ ∈ Val`. Its arrangement, by D-SEQ★ (ASN-0047), is `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}`. We fix the content-subspace depth at `m_C = 2` so that each text-subspace V-position takes the canonical form `v_a^k = [s_C, k]`. The choice makes the depth structure visible at every V-position and aligns the content subspace with the link subspace's fixed depth `m_L = 2` exercised by Query 9 below; per-subspace depth independence (S8-depth, ASN-0036) permits `m_C` and `m_L` to be chosen separately within each document, and we use the same value here only for the worked example's uniformity.

- `d_b` transcludes the latter two positions from `d_a`. Its arrangement is `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}` with `v_b^k = [s_C, k]` of depth 2 (we fix `m_C = 2` for `d_b`'s text subspace as well), sharing the I-addresses `α₂` and `α₃` with `d_a`. (No new content addresses were allocated for `d_b`; transclusion shares by reference. By P4★ (ASN-0047), `(α₂, d_b), (α₃, d_b) ∈ Σ.R`.) We assume `d_a` was allocated immediately before `d_b` under the same account, with no intervening document allocations — that is, `d_b = inc(d_a, 0)` is the next chain emission of that account's document sub-allocator after `d_a`. By T10a.7 (EnumerationInjectivity, ASN-0034) applied to their common account's document sub-allocator — every T10a-conforming `inc(·, 0)` chain is strictly T1-increasing, uniformly across A_C, A_L, A_doc, A_account, and A_v — `d_a < d_b` under T1. With this immediate-successor assumption, `d_b` sits at the document-chain frontier of its account at `Σ`, so `inc(d_b, 0) ∉ E` is available for a fresh K.δ at `k = 0` from `d_b` — a point exercised by Query 10 below.

- Three type-tumbler addresses `τ_comment`, `τ_reply`, `τ_meta`, allocated as the first three emissions of `A_C(d_τ)` (ASN-0093) under a separate type-registry document `d_τ ∈ dom(Σ.M)` chosen non-nesting with both `d_a` and `d_b`: `d_τ ⋠ d_a`, `d_a ⋠ d_τ`, `d_τ ⋠ d_b`, `d_b ⋠ d_τ` (concretely, `d_τ` is allocated under a different account or node from `d_a` and `d_b`'s shared account). So `τ_comment = [d_τ.0.s_C.1]`, `τ_reply = [d_τ.0.s_C.2]`, `τ_meta = [d_τ.0.s_C.3]`, pairwise distinct by ChainEnumerationInjectivity (ASN-0093) and uniform-length by ChainUniformLength (ASN-0093). The non-nesting of `d_τ` with `d_a` and `d_b` lifts to all τ-disjointness obligations the downstream queries will invoke. Every τ-address extends `d_τ`; every content address `αᵢ` extends `d_a` (via `b_C(d_a)`); the link address `ℓ` extends `d_a` (via `b_L(d_a)`); the link addresses `ℓ'` and `ℓ_meta` extend `d_b` (via `b_L(d_b)`). Since the document-level prefixes `d_τ`, `d_a`, `d_b` are pairwise non-nesting (`d_a ⋠ d_b` and `d_b ⋠ d_a` follow from `d_a` and `d_b` being siblings — equal length, disagreeing final component, hence neither extends the other), T10 (PartitionIndependence, ASN-0034) together with PrefixOrderingExtension (ASN-0034) — extensions of non-nesting prefixes remain pairwise prefix-incomparable, since a putative `x ≼ y` would force the underlying prefixes into a nesting they cannot achieve — gives: for any τ-address `τ` and any `x ∈ {α₁, α₂, α₃, ℓ, ℓ', ℓ_meta}`, `τ ⋠ x` and `x ⋠ τ`. The pairwise non-extension among the τ-addresses themselves follows from ChainUniformLength (equal length) and final-component disagreement (1, 2, 3) under T1.

- Three links `ℓ, ℓ', ℓ_meta ∈ dom(Σ.L)`, all with arity 3. `ℓ` is allocated under `d_a` (so `home(ℓ) = d_a` and `ℓ = [d_a.0.s_L.1]`); `ℓ'` is allocated under `d_b` (so `home(ℓ') = d_b` and `ℓ' = [d_b.0.s_L.1]`); `ℓ_meta` is allocated under `d_b` after `ℓ'`, so by K.λ's subsequent-emission precondition (ASN-0093) `ℓ_meta = inc(ℓ', 0) = [d_b.0.s_L.2]`. The slot assignments:
  - `ℓ`'s slot 1 (from-endset): one canonical span `(α₂, δ(1, #α₂))`, so `coverage(Σ.L(ℓ).e₁) = {t ∈ T : α₂ ≼ t}` by PrefixSpanCoverage (ASN-0043). The coverage is *not* the singleton `{α₂}` — it is the prefix-closure of `α₂`, containing `α₂` itself together with every tumbler extending `α₂` (e.g. `α₂.0`, `α₂.1`, `α₂.0.0`, …). Coverage of a canonical span is always a prefix-subtree, never a singleton; the singleton arises only when we intersect with a singleton query.
  - `ℓ`'s slot 2 (to-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ).e₂) = {t ∈ T : α₃ ≼ t}` by the same reasoning.
  - `ℓ`'s slot 3 (type-endset): one canonical span `(τ_comment, δ(1, #τ_comment))`, so `coverage(Σ.L(ℓ).e₃) = {t ∈ T : τ_comment ≼ t}`. By the τ-disjointness assumption, this coverage is disjoint from `{α₁, α₂, α₃}` and from the other type-coverages below.
  - `ℓ'`'s slot 1 (from-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ').e₁) = {t ∈ T : α₃ ≼ t}` — the same prefix-closure as `ℓ`'s slot 2.
  - `ℓ'`'s slot 2 (to-endset): one canonical span `(α₁, δ(1, #α₁))`, so `coverage(Σ.L(ℓ').e₂) = {t ∈ T : α₁ ≼ t}`.
  - `ℓ'`'s slot 3 (type-endset): one canonical span `(τ_reply, δ(1, #τ_reply))`, so `coverage(Σ.L(ℓ').e₃) = {t ∈ T : τ_reply ≼ t}`.
  - `ℓ_meta`'s slot 1: one canonical span `(ℓ, δ(1, #ℓ))`, so `coverage(Σ.L(ℓ_meta).e₁) = {t ∈ T : ℓ ≼ t}` — the prefix-closure of the link address `ℓ` itself. This is the address-of-address shape: an endset whose target is another link's address, admissible by L4 (ASN-0043).
  - `ℓ_meta`'s slot 2: the empty endset `∅`, with `coverage(∅) = ∅`. L3 (ASN-0043) requires only slot 3 to be non-empty.
  - `ℓ_meta`'s slot 3 (type-endset): one canonical span `(τ_meta, δ(1, #τ_meta))`, so `coverage(Σ.L(ℓ_meta).e₃) = {t ∈ T : τ_meta ≼ t}`.

The three prefix-subtrees over `α₁, α₂, α₃` are pairwise disjoint: each `αᵢ` is an element-level tumbler of equal length with disagreeing final components (1, 2, 3 respectively), so no pair extends the other (`αᵢ ⋠ αⱼ` for `i ≠ j`), and a tumbler cannot extend two of them simultaneously. The coverages `{t : ℓ ≼ t}` and `{t : αᵢ ≼ t}` are also disjoint: `ℓ = [d_a.0.s_L.1]` has subspace identifier `s_L` at position `#d_a + 2`, while each `αᵢ` has `s_C` at that position, so no tumbler can extend both. By ChainEnumerationInjectivity and CrossDocDisjointness (ASN-0093) together with PrefixOrderingExtension (ASN-0034), the link addresses satisfy `ℓ < ℓ' < ℓ_meta` under T1: across home documents `d_a < d_b` lifts to `ℓ < ℓ'` by the cross-document argument used in F10, and within `A_L(d_b)` the per-step strict increase `inc(ℓ', 0) > ℓ'` gives `ℓ' < ℓ_meta`.

**Query 1: `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: the precondition `d_a ∈ dom(Σ.M)` holds, and `{v_a^2} ∩ dom(Σ.M(d_a)) = {v_a^2}` (the queried position survives the projection), so `image({v_a^2}, d_a, Σ) = {Σ.M(d_a)(v_a^2)} = {α₂}`. Phase 2: test each link in `dom(Σ.L)` against `I = {α₂}`. At `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅` (the only element of `{α₂}` that extends `α₂` is `α₂` itself, by reflexivity of `≼`), so the slot-existential fires and `matches(ℓ, {α₂}, Σ) = true`. At `ℓ'`, slot 1 covers `{t : α₃ ≼ t}`, slot 2 covers `{t : α₁ ≼ t}`, slot 3 covers `{t : τ_reply ≼ t}` (disjoint from content addresses by the τ-disjointness assumption); none meet `{α₂}` (since `α₃ ⋠ α₂` and `α₁ ⋠ α₂` — final components disagree — and `τ_reply ⋠ α₂` by τ-disjointness). At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (disjoint from `{α₂}` by subspace separation — `ℓ` has subspace `s_L` at position `#d_a + 2` and `α₂` has `s_C` at that position, so `ℓ ⋠ α₂`), slot 2 is empty (`coverage(∅) = ∅`), slot 3 covers `{t : τ_meta ≼ t}` (disjoint from `{α₂}` by τ-disjointness); no slot meets `{α₂}`. The result is `{ℓ}`.

**Query 2: `findlinks_V({v_b^1}, d_b, Σ)`.** Phase 1: `image({v_b^1}, d_b, Σ) = {Σ.M(d_b)(v_b^1)} = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address as `d_a`'s native arrangement of `α₂`. Phase 2 is therefore identical to Query 1's Phase 2 (ℓ matches; ℓ' and ℓ_meta do not, by the same structural reasoning): result `{ℓ}`. This is F6 (TransclusionTransparency) in operation — the reader querying `d_b`'s view of `α₂` discovers the same link they would have discovered via `d_a`'s native arrangement, because identity travels with the I-address.

**Query 3: `findlinks_V({v_a^2, v_a^3}, d_a, Σ)`.** Phase 1: `image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}`. Phase 2: at `ℓ`, slot 1 gives `coverage(Σ.L(ℓ).e₁) ∩ {α₂, α₃} = {α₂} ≠ ∅` (matches); slot 2 also fires (`{t : α₃ ≼ t} ∩ {α₂, α₃} = {α₃}`), although either witness alone suffices. At `ℓ'`, slot 1 gives `coverage(Σ.L(ℓ').e₁) ∩ {α₂, α₃} = {t : α₃ ≼ t} ∩ {α₂, α₃} = {α₃} ≠ ∅` (matches via slot 1); slot 2 (covering `{t : α₁ ≼ t}`) does not fire. At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (subspace-disjoint from `{α₂, α₃}`, both s_C-resident), slot 2 is empty, slot 3 covers `{t : τ_meta ≼ t}` (τ-disjoint from content addresses); no slot meets `{α₂, α₃}`, so ℓ_meta does not match. Result: `{ℓ, ℓ'}`. Both matching links appear once each — the result is a set.

**Verifying F10 (OrderedResult) on Query 3.** The set `{ℓ, ℓ'}` admits a unique strictly T1-increasing presentation. We have `home(ℓ) = d_a` and `home(ℓ') = d_b` with `d_a < d_b` (by the allocation-order assumption). Both links lie in their respective `A_L` chains: `ℓ = [d_a.0.s_L.1] ∈ A_L(d_a)` and `ℓ' = [d_b.0.s_L.1] ∈ A_L(d_b)`. Since `d_a` and `d_b` are siblings under the same account (allocation-order assumption), they share a prefix and have equal length (T10a.1), so `d_a < d_b` falls under T1 case (i) — the divergence position is `#d_a = #d_b` itself (sibling document tumblers agree on positions before their distinguishing component). F10a's case (i) instantiated at `(d₁, d₂) := (d_a, d_b)` lifts the document-level T1 case (i) to anchor-level T1 case (i): `b_L(d_a) < b_L(d_b)` with the anchors non-nesting. PrefixOrderingExtension (ASN-0034), through F10a's conclusion, lifts to every extension: `ℓ < ℓ'`. The canonical presentation is `⟨ℓ, ℓ'⟩`. The result delivered to the reader is therefore ordered by home document under T1, with links within a document in allocation order — here each document has only one link, but the cross-document ordering machinery is fully exercised in F10a's case (i).

**Verifying F10 across a version extension (T1 case (ii)).** Case (i) handles sibling documents; the routine version-of relationship — K.δ at `k = 1` (ASN-0047) producing `d_new = inc(d_src, 1)` — falls under T1 case (ii) because the resulting `d_src ≺ d_new` is the prefix-extension shape rather than the divergence shape. We exercise the case explicitly with a hypothetical version document `d_v = inc(d_a, 1)`, a version of `d_a` produced by K.δ at `k = 1` in some other state (the broader Worked Example operates at `Σ`, which need not contain `d_v`; this paragraph is local, with `d_v` and its link `ℓ_v` both local to this hypothetical and distinct from the globally introduced `ℓ_meta` — and distinct in particular from Query 10's later sibling document `d_c = inc(d_b, 0)`, which is a sibling under `d_b`'s account rather than a version of `d_a`). Suppose `d_v ∈ dom(Σ.M)` and an additional link `ℓ_v = [d_v.0.s_L.1] ∈ dom(Σ.L)` is allocated under `d_v`. We verify the placement of `ℓ_v` under T1 against `ℓ` and `ℓ'`. By TA5(d) (ASN-0034), `#d_v = #d_a + 1` and `d_v` agrees with `d_a` on positions `1..#d_a`, so `d_a ≺ d_v` and `(d_v)_{#d_a + 1} = 1`. The lifting from `d_a ≺ d_v` to `b_L(d_a) < b_L(d_v)` is exactly F10a's case (ii) instantiated at `(d₁, d₂) := (d_a, d_v)`: the proper prefix on documents lifts to component divergence at position `#d_a + 1` on anchors, with `b_L(d_a)[#d_a + 1] = 0` and `b_L(d_v)[#d_a + 1] = (d_v)_{#d_a + 1} = 1`. PrefixOrderingExtension (via F10a's conclusion) lifts to every extension: `ℓ < ℓ_v`. For the `ℓ_v vs ℓ'` comparison, the first divergence is at position `#d_a` itself — the last position of both `d_a` and `d_b`. `d_v = inc(d_a, 1)` preserves every component of `d_a` on positions `1..#d_a` (TA5(d) at `k = 1` modifies only positions beyond `#d_a`), so `(d_v)_{#d_a} = (d_a)_{#d_a}`. `d_b = inc(d_a, 0)` increments only `d_a`'s significant position (TA5(c) at `sig(d_a) = #d_a` by TA5-SigValid for the T4-valid `d_a`), so `(d_b)_{#d_a} = (d_a)_{#d_a} + 1` and `(d_b)_j = (d_a)_j` for `1 ≤ j < #d_a`. Both anchors inherit their documents' components on the document positions: `b_L(d_v)[1..#d_v] = d_v` and `b_L(d_b)[1..#d_b] = d_b`. The first emissions append a single `.1` past each anchor, so `ℓ_v[1..#d_v] = d_v` and `ℓ'[1..#d_b] = d_b`. At position `#d_a` — which lies inside both `ℓ_v` (length `#d_a + 4`) and `ℓ'` (length `#d_a + 3`) — we have `ℓ_v[#d_a] = (d_v)_{#d_a} = (d_a)_{#d_a}` and `ℓ'[#d_a] = (d_b)_{#d_a} = (d_a)_{#d_a} + 1`. Earlier positions `1..#d_a - 1` agree because `d_a`, `d_b`, and `d_v` share that prefix. T1 case (i) at position `#d_a` gives `ℓ_v < ℓ'`; the divergence is internal to both tumblers, so they are non-nesting. The canonical presentation of the augmented hypothetical result set `{ℓ, ℓ', ℓ_v}` is `⟨ℓ, ℓ_v, ℓ'⟩` — the version-extension link sits between the original link and its sibling-document counterpart. F10 holds across both T1 cases: case (i) for siblings, case (ii) for versions.

**Verifying F13 (SetAdditive).** Compute each side separately. `findlinks({α₂}, Σ) = {ℓ}` (`ℓ` via slot 1; neither `ℓ'` nor `ℓ_meta` matches `{α₂}`) and `findlinks({α₃}, Σ) = {ℓ, ℓ'}` (`ℓ` via slot 2 and `ℓ'` via slot 1, both intersecting `{α₃}` in `{α₃}`; `ℓ_meta`'s endsets remain subspace/τ-disjoint from `{α₃}`); their union is `{ℓ, ℓ'}`. Independently, `findlinks({α₂, α₃}, Σ) = {ℓ, ℓ'}` by direct evaluation as in Query 3. The two computations agree: `findlinks({α₂} ∪ {α₃}, Σ) = findlinks({α₂}, Σ) ∪ findlinks({α₃}, Σ) = {ℓ, ℓ'}`.

**F2 (Completeness): conformance obligation at the instance.** F2 and F3 are conformance contracts on a separate implementation function `result(I, Σ)`; the worked example does not "verify" the abstract specification against itself but exhibits what F2 ∧ F3 *obligate* any conforming implementation to produce at this specific `(I, Σ)`. The set `dom(Σ.L) = {ℓ, ℓ', ℓ_meta}` is the universe of candidates. For the query `{α₂}`, the match predicate fires at `ℓ` only. F2 obligates any conforming implementation to satisfy `result({α₂}, Σ) ⊇ {ℓ}` — the matching link must appear in the implementation's output. The abstract comprehension `{a ∈ dom(Σ.L) : matches(a, {α₂}, Σ)}` evaluates to `{ℓ}` for this instance, pinning the completeness obligation: an implementation conforms to F2 here iff its actual `result({α₂}, Σ)` contains at least `{ℓ}`. (The dual no-spurious obligation belongs to F3 and is addressed in the next paragraph.)

**F3 (Soundness): conformance obligation at the instance.** F3 obligates any conforming implementation to satisfy `result({α₂}, Σ) ⊆ {ℓ}` — only links in `dom(Σ.L)` that match `{α₂}` may appear in the output. We verified above that `matches(ℓ', {α₂}, Σ) = false` and `matches(ℓ_meta, {α₂}, Σ) = false`, so a conforming implementation cannot return `ℓ'` or `ℓ_meta`. Jointly F2 ∧ F3 force `result({α₂}, Σ) = {ℓ}`; the abstract specification produces `{ℓ}` for this instance, and every conforming implementation must produce exactly this set.

**Verifying F6 against the instance.** Queries 1 and 2 produce the same I-image `{α₂}` and hence the same result `{ℓ}`, despite the V-positions `v_a^2` and `v_b^1` belonging to different documents. The match predicate consulted only the I-image and the link store; the document of origin of the V-position vanished from the computation after Phase 1.

**Verifying F5 (IdentityNotValue) against the instance.** Slot 1's coverage at `ℓ` is `{t : α₂ ≼ t}`, so `matches(ℓ, {α₂}, Σ) = true` (via slot 1: `α₂ ≼ α₂` puts `α₂` in the intersection with `{α₂}`) while `matches(ℓ, {α₃}, Σ) = true` only via slot 2 — the slot 1 test against `{α₃}` evaluates `{t : α₂ ≼ t} ∩ {α₃} = ∅` (since `α₂ ⋠ α₃`) and so does not fire. The slot 1 decision turns entirely on which I-addresses extend `α₂` as tumblers. The content values `v₂, v₃ ∈ Val` at `α₂, α₃` are never consulted: even if the writer of `d_a` had stored `v₂ = v₃` (the same value at distinct addresses), the slot 1 test would still discriminate `{α₂}` from `{α₃}` — the address-level intersection `{t : α₂ ≼ t} ∩ {α₃} = ∅` is decided by `α₂ ⋠ α₃` (their last components disagree, 2 vs 3), itself a consequence of GlobalUniqueness (ASN-0034) which forced these addresses to be distinct in the first place. F5 says the match predicate factors through the address space, not through the value space; this instance exhibits the factoring directly.

**Query 4: Survivability under arrangement edit (F11, F9).** Apply a K.μ⁻ transition to `d_a` retaining only the first content position: the post-state Σ' has `Σ'.M(d_a) = {v_a^1 ↦ α₁}`, with `v_a^2` and `v_a^3` removed from `dom(Σ'.M(d_a))` (so `α₂` and `α₃` are no longer in `ran(Σ'.M(d_a))`). The link store is untouched by K.μ⁻: K.μ⁻ falls in V ∖ {K.λ} with a published frame silent on `L`, so by A1b (ClosedWorldPreservation) the structural invariant `dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))` holds across the step — `dom(Σ'.L) = {ℓ, ℓ', ℓ_meta}` and each link's value is preserved (`Σ'.L(·) = Σ.L(·)`), consistent with L12. Re-evaluate `findlinks({α₂}, Σ')`: the match predicate at `ℓ` tests slot 1, `coverage(Σ'.L(ℓ).e₁) ∩ {α₂} = {α₂} ≠ ∅`, so `matches(ℓ, {α₂}, Σ') = true`. `ℓ'`'s endsets still do not meet `{α₂}`, and ℓ_meta's endsets remain subspace/τ-disjoint from `{α₂}` (Query 1's reasoning carries over since per-link endset values are preserved). The result is `{ℓ}`, the same as Query 1's pre-edit result.

This exercises F11 directly: the link survives the arrangement edit because its endset references `α₂`'s I-address (not `v_a^2`'s V-position), and `α₂`'s identity is preserved by content immutability (C0, ASN-0093). It also exercises F9 — the K.μ⁻ transition is a K.μ-family step satisfying F9's frame condition, so `findlinks({α₂}, Σ) = findlinks({α₂}, Σ')` is guaranteed before we re-evaluate the comprehension. The V-side query `findlinks_V({v_a^2}, d_a, Σ')` remains well-formed under the projection semantics of `image`: `{v_a^2} ∩ dom(Σ'.M(d_a)) = ∅` (since `v_a^2` was contracted out), so `image({v_a^2}, d_a, Σ') = ∅` and `findlinks_V({v_a^2}, d_a, Σ') = findlinks(∅, Σ') = ∅`. The reader who previously queried `α₂` via `v_a^2` now receives an empty V-side answer through that route and must reach `α₂` via a surviving V-position — `d_b`'s transclusion suffices: `findlinks_V({v_b^1}, d_b, Σ')` images to `{α₂}` and recovers `ℓ`. The link's I-side identity persists; the V-side query surface has shrunk while the link-side survivability has not.

**Query 5: Filtered query exercising F7 (filter conjunction).** Evaluate `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ)` — the conjunctive "links from `α₂` to `α₃`" query. At `ℓ`: slot 1 satisfies `coverage(Σ.L(ℓ).e₁) ∩ {α₂} = {α₂} ≠ ∅`, slot 2 satisfies `coverage(Σ.L(ℓ).e₂) ∩ {α₃} = {α₃} ≠ ∅`. Both constraints hold; `ℓ` is in the result. At `ℓ'`: slot 1 covers `{t : α₃ ≼ t}`, intersected with `{α₂}` is `∅` (since `α₃ ⋠ α₂`); the slot-1 constraint already fails, the universal is false, and `ℓ'` is excluded — even though `ℓ'`'s slot 1 *does* meet `{α₃}`, which would have satisfied a slot-1 constraint had we named the to-set under slot 1. At `ℓ_meta`: slot 1 covers `{t : ℓ ≼ t}`, intersected with `{α₂}` is `∅` (subspace mismatch); the slot-1 constraint fails, so `ℓ_meta` is excluded. The conjunctive force of the filter is essential: the *from* slot must meet `{α₂}` and the *to* slot must meet `{α₃}`, both holding simultaneously. Result: `{ℓ}`. Contrast with the union-form unfiltered query `findlinks({α₂} ∪ {α₃}, Σ) = {ℓ, ℓ'}` — the filtered form is strictly stricter, as F7(b) and the section on filtered semantics anticipate.

**Query 6: Scoped query exercising F14.** Evaluate `findlinks_scoped({α₂, α₃}, {a ∈ T : home(a) = d_a}, Σ)`. The unscoped result `findlinks({α₂, α₃}, Σ) = {ℓ, ℓ'}` (Query 3; ℓ_meta does not match the unscoped I-set). The scope `S = {a : home(a) = d_a}` contains every link allocated under `d_a`; in this instance only `ℓ`, since `home(ℓ) = d_a` while `home(ℓ') = home(ℓ_meta) = d_b`. The intersection `findlinks({α₂, α₃}, Σ) ∩ S = {ℓ, ℓ'} ∩ {ℓ} = {ℓ}`. The reader who restricts to `d_a`-owned links receives `{ℓ}`, even though `ℓ'` also touches the queried content. The match predicate is unweakened — `ℓ'` still matches the I-set — but the scope narrows the candidate set before reporting. F14's definition `findlinks_scoped = findlinks(I, Σ) ∩ S` is exercised by direct intersection.

**Query 7: Determinism under arrangement variation (F8).** Apply a K.μ~ reordering transition to `d_a` realising the cyclic permutation `π(v_a^k) = v_a^{(k mod 3) + 1}`: the post-state Σ'' has `Σ''.M(d_a) = {v_a^1 ↦ α₃, v_a^2 ↦ α₁, v_a^3 ↦ α₂}` (the same three I-addresses arranged at the same three V-positions, rotated). K.μ~'s published frame names `L' = L` directly — an A1a invocation in the partition of A1, carrying no convention-grounded commitment — so `Σ''.L = Σ.L` exactly. F8's hypothesis is satisfied, and F8 forces `findlinks({α₂}, Σ) = findlinks({α₂}, Σ'')` directly from the I-side: the match predicate consults only `(Σ.L, I)`, both unchanged, so the comprehension produces the same set. Direct evaluation at Σ'' confirms — the slot-1 test at `ℓ` evaluates `coverage(Σ''.L(ℓ).e₁) ∩ {α₂} = {t : α₂ ≼ t} ∩ {α₂} = {α₂} ≠ ∅` exactly as in Query 1; `ℓ'`'s and `ℓ_meta`'s endset coverages do not meet `{α₂}` for the same address-level reasons as Query 1 (preserved values across K.μ~); the result is `{ℓ}`. Crucially, no V-position appeared anywhere in the I-side derivation. The V-image *of any V-position in `d_a`* changed under the reordering (`v_a^2` now maps to `α₁` rather than `α₂`), but the link-side answer for the fixed I-set `{α₂}` is invariant. This is the operational content of F8: link discovery is a property of `(Σ.L, I)`, with arrangement permutations preserving the link store leaving the answer untouched.

**Query 8: Type-endset filter exercising F7(a) (slot-3 first-class searchability).** Evaluate `findlinks_filtered({(3, {τ_comment})}, Σ)` — "links whose type endset covers the comment type". At `ℓ`: slot 3 covers `{t : τ_comment ≼ t}`, intersected with `{τ_comment}` is `{τ_comment}` (reflexivity of `≼`), so the slot-3 constraint is satisfied. The only constraint in `C` is `(3, {τ_comment})`, so the universal `(A (i, J) ∈ C : ...)` holds vacuously beyond slot 3; `ℓ` is in the result. At `ℓ'`: slot 3 covers `{t : τ_reply ≼ t}`, intersected with `{τ_comment}` is `∅` (since `τ_reply ⋠ τ_comment` by τ-disjointness). The slot-3 constraint fails; `ℓ'` is excluded. At `ℓ_meta`: slot 3 covers `{t : τ_meta ≼ t}`, intersected with `{τ_comment}` is `∅` by τ-disjointness; the slot-3 constraint fails. Result: `{ℓ}`. The filter operates on the type endset on equal footing with the from/to endsets exercised in Query 5 — F7(a)'s slot symmetry says slots are equally searchable, and slot 3 here is the discriminating slot, not slot 1 or slot 2. The unfiltered query `findlinks({τ_comment}, Σ)` would have produced the same `{ℓ}` here (by F1's existential, the slot-3 witness at `ℓ` suffices), so the filter does not change the answer in this single-constraint case — but `findlinks_filtered({(1, {τ_comment})}, Σ) = ∅` (no link's slot 1 covers `τ_comment`), illustrating that the filter's slot-naming is load-bearing when the constraint is positional.

**Query 9: Link-subspace V-position via K.μ⁺_L (cross-subspace findlinks_V).** We exercise cross-subspace handling: a V-position in the link subspace `s_L` mapping to a link in `dom(Σ.L)`, exposing an "annotation on an annotation" via the standard discovery operation. First, perform a K.μ⁺_L transition on `d_a` extending its arrangement to include the V-position `v_a^L := [s_L, 1]` (the depth-2 minimum position in the link subspace per LinkVPositionDepthAxiom, satisfying D-MIN★ for the freshly-non-empty subspace) mapping to `ℓ`. The K.μ⁺_L precondition is satisfied: `ℓ ∈ dom(Σ.L)` (from setup), `origin(ℓ) = d_a` (so the home-document constraint holds), `ℓ ∉ ran(Σ.M(d_a))` (the pre-state arranged only content addresses in `d_a`'s content subspace), and the V-position is the canonical depth-2 minimum. Call the post-state Σ_L: `Σ_L.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃, v_a^L ↦ ℓ}`. The link store is preserved by K.μ⁺_L (`Σ_L.L = Σ.L`), so the three links and their endsets are unchanged.

Now evaluate `findlinks_V({v_a^L}, d_a, Σ_L)`. Phase 1: `v_a^L ∈ dom(Σ_L.M(d_a))` and `Σ_L.M(d_a)(v_a^L) = ℓ`, so `image({v_a^L}, d_a, Σ_L) = {ℓ}` — the image is the *link address* `ℓ`, a member of `dom(Σ_L.L)`, not a member of `dom(Σ_L.C)`. Phase 2: test each link in `dom(Σ_L.L) = {ℓ, ℓ', ℓ_meta}` against `I = {ℓ}`. At `ℓ`: slot 1 covers `{t : α₂ ≼ t}`, intersected with `{ℓ}` is `∅` (since `α₂ ⋠ ℓ` — `α₂` has subspace `s_C` at position `#d_a + 2` while `ℓ` has `s_L` at that position); slots 2 and 3 cover `{t : α₃ ≼ t}` and `{t : τ_comment ≼ t}`, neither extending `ℓ`. No match. At `ℓ'`: slots 1, 2, 3 cover `{t : α₃ ≼ t}`, `{t : α₁ ≼ t}`, `{t : τ_reply ≼ t}`; none extends `ℓ` (subspace separation handles slots 1 and 2; τ-disjointness handles slot 3 against `τ_comment` and against link addresses generally). No match. At `ℓ_meta`: slot 1 covers `{t : ℓ ≼ t}`, intersected with `{ℓ}` is `{ℓ}` (reflexivity of `≼`); the slot-existential fires and `matches(ℓ_meta, {ℓ}, Σ_L) = true`. Result: `{ℓ_meta}`.

The reader who selects the V-position `v_a^L` in `d_a` — a position arranged in the link subspace whose image is the link `ℓ` — discovers `ℓ_meta`, the meta-link annotating `ℓ`. The operation works uniformly across subspaces: the image is a link address rather than a content address, but `findlinks` consults only the I-image and the link store and is indifferent to whether the image's elements inhabit `dom(C)` or `dom(L)`. S3★'s cross-subspace routing of V-positions to `dom(L)` (ASN-0047) feeds naturally into the address-agnostic match predicate of F1. This is the formal realization of the "annotation on an annotation, a comment about a typed connection" case mentioned in the I-image discussion.

**Query 10: Multi-step survivability under V ∖ {K.λ} (F9★-cor).** We exercise the multi-step closure F9★-cor with a five-step sequence interleaving non-allocating operations across multiple state components. The sequence touches `M`, `C`, `R`, and a contraction of an arrangement — every state component the substrate non-allocating fragment can modify — while leaving `Σ.L` invariant throughout. From the worked-example base state `Σ`:

Throughout this sequence we operate against the extended state of ASN-0047 (`Σ = (C, L, E, M, R)`), since step (iv) invokes K.ρ — whose precondition `d ∈ E_doc` and effect `R' = R ∪ {(a, d)}` are stated against the extended vocabulary. Steps (i) and (ii) therefore cite K.δ and K.α as published in ASN-0047, not the corresponding substrate-only operations of ASN-0093.

(i) K.δ (EntityCreation, ASN-0047) case (ii) at `k = 0` from `d_b` creates a fresh document `d_c = inc(d_b, 0)` with `d_c ∉ E`. The K.δ preconditions are satisfied: `d_b ∈ E` (since `d_b ∈ E_doc` from the worked-example setup), `¬IsNode(d_b)` (d_b is a document), `inc(d_b, 0) ∉ E` (the freshness condition for d_c — d_b is itself the chain successor of d_a under the same account, so the next chain element is unused at Σ), and `parent(d_c) = parent(d_b) ∈ E` (by K.δ-ID.parent-0/1 (ASN-0047) and P8 (EntityHierarchy, ASN-0047) — d_b's owning account is in E since d_b descends from it). By K.δ-ID.zeros-0/1 (ASN-0047), `zeros(d_c) = zeros(d_b) = 2`, so `IsDocument(d_c)` holds. K.δ's published effect places `d_c` into `E'_doc` (so `d_c ∈ Σ_1.E_doc`) and simultaneously initializes `Σ_1.M(d_c) = ∅`, with `Σ_1.M(d') = Σ.M(d')` for every `d' ≠ d_c`. The transition modifies `E` and `M`; K.δ's published frame names `L' = L` directly, so `Σ_1.L = Σ.L`.

(ii) K.α (ContentAllocation, ASN-0047) allocates a fresh content address `α_c = [d_c.0.s_C.1]` — the first emission of `A_C(d_c)` — and places it into `dom(C)` with some value `v_c ∈ Val`. The precondition `d_c ∈ E_doc` is discharged by step (i), which placed `d_c ∈ Σ_1.E_doc`. The transition modifies `C`; K.α's published frame names `L' = L` directly, so `Σ_2.L = Σ_1.L = Σ.L`.

(iii) K.μ⁺ (ArrangementExtension, ASN-0047) extends `Σ_2.M(d_c)` to map a fresh V-position `v_c^1 = [s_C, 1]` of depth 2 to `α_c`, satisfying K.μ⁺'s precondition `α_c ∈ dom(Σ_2.C)` (just established by step ii) along with S8a, S8-depth, and D-MIN★ at the freshly-non-empty subspace. The transition modifies `M(d_c)`; K.μ⁺'s published frame in ASN-0047 omits `L`, but A1b supplies `Σ_3.L = Σ_2.L = Σ.L`.

(iv) K.ρ (ProvenanceRecording, ASN-0047) records `(α_c, d_c) ∈ R`, satisfying K.ρ's precondition `α_c ∈ dom(Σ_3.C)` (established by step ii, with `α_c ∈ dom(Σ_2.C) ⊆ dom(Σ_3.C)` carried through step iii by C0, ASN-0093) and `d_c ∈ Σ_3.E_doc` (established by step i, with `d_c ∈ E_doc` carried through steps ii–iii by P1 (EntityPermanence, ASN-0047), under which `E ⊆ E'` and the `IsDocument` clause specialises to `e ∈ E_doc ⟹ e ∈ E'_doc`). The transition modifies `R`; K.ρ's published frame omits `L`, but A1b supplies `Σ_4.L = Σ_3.L = Σ.L`.

(v) K.μ⁻ (ArrangementContraction, ASN-0047) contracts `Σ_4.M(d_a)` to `{v_a^1 ↦ α₁}` (the contraction of Query 4 applied to the running sequence's state). The transition modifies `M(d_a)`; K.μ⁻'s published frame omits `L`, but A1b supplies `Σ_5.L = Σ_4.L = Σ.L`.

Across the whole chain `Σ → Σ_1 → Σ_2 → Σ_3 → Σ_4 → Σ_5`, transitivity of equality through the per-step `Σᵢ.L = Σᵢ₋₁.L` chain yields `Σ.L = Σ_5.L`. F8 then forces `findlinks(I, Σ) = findlinks(I, Σ_5)` for every I ⊆ T — the I-side answer at every step of the sequence is exactly the I-side answer at `Σ`. Concretely, at `I = {α₂}`: `findlinks({α₂}, Σ) = {ℓ}` (Query 1) and `findlinks({α₂}, Σ_5) = {ℓ}` by direct evaluation (`Σ_5.L = Σ.L = {ℓ, ℓ', ℓ_meta}` with values preserved by L12 across the whole chain; the slot-1 test at `ℓ` still produces `coverage(Σ_5.L(ℓ).e₁) ∩ {α₂} = {α₂} ≠ ∅`, and `ℓ'`, `ℓ_meta` remain non-matching by their endset-coverage reasoning of Query 1, unchanged). The chain exercises A1b three times — once each at the K.μ⁺, K.μ⁻, and K.ρ steps — and exercises A1a's coverage of the published `L' = L` frame twice (at K.δ in step i and K.α in step ii); K.σ, K.μ~, and K.μ⁺_L are not invoked here since the sequence does not use them, but their published `L' = L` frames (also A1a) would extend the chain identically. F9★-cor's claim that any reachable sequence in V ∖ {K.λ} preserves `findlinks(I, ·)` is operationally exercised here against a sequence that touches every other state component, with the discovery answer invariant across the chain. The V-side answer at `v_a^2` in `d_a` does change across the chain (the K.μ⁻ step contracts `v_a^2` out of `dom(M(d_a))`, so `findlinks_V({v_a^2}, d_a, Σ_5) = findlinks(∅, Σ_5) = ∅`), but the I-side answer at the fixed I-set `{α₂}` does not.

**Query 11: F9★ verification via a K.μ-only two-step chain (cross-step precondition transfer).** Query 10 exhibits the broader F9★-cor closure across a mixed sequence; F9★'s K.μ-only specialization deserves its own direct exhibition, since the operationally salient editing surface is exactly K.μ-only. The chain we construct also illustrates a feature absent from Query 9's single K.μ⁺_L: a K.μ⁺_L step whose precondition was originally evaluated against the base state Σ must be re-evaluated against the intermediate state at which it actually fires. Compose Query 4's K.μ⁻ transition `Σ → Σ'` (contracting `Σ.M(d_a)` to `{v_a^1 ↦ α₁}`) with Query 9's K.μ⁺_L transition extended now off `Σ'` (extending `Σ'.M(d_a)` with `v_a^L ↦ ℓ`, yielding state `Σ_edit_link`). The local name `Σ_edit_link` is chosen to disambiguate from Query 7's `Σ''` — that state arose from a single K.μ~ reordering and is structurally different from this two-step composite (K.μ⁻ then K.μ⁺_L), so a distinct name keeps the worked-example state names unambiguous.

The cross-step precondition transfer is load-bearing: K.μ⁺_L's precondition `ℓ ∈ dom(L)`, `origin(ℓ) = d_a`, `ℓ ∉ ran(M(d_a))`, and the D-MIN★ admissibility of `v_a^L` were all stated against the base state Σ in Query 9; here we must check them against Σ' (the K.μ⁻ post-state). All four transfer cleanly: `ℓ ∈ dom(Σ'.L) = dom(Σ.L)` (preserved by A1b across the K.μ⁻ step, since K.μ⁻'s published frame is silent on L), `origin(ℓ) = d_a` (a property of `ℓ`'s allocation history, invariant across non-allocating transitions), `ℓ ∉ ran(Σ'.M(d_a)) = {α₁}` (K.μ⁻ contracted everything but `α₁` from the content subspace, and `ℓ ∉ {α₁}` by subspace separation), and `v_a^L = [s_L, 1]` is the canonical depth-2 minimum in `d_a`'s link subspace (which remains empty at Σ' since it was empty at Σ and K.μ⁻ touched only the content subspace, so D-MIN★ admits `v_a^L` at Σ'). Both steps are K.μ-family operations: K.μ⁻ ∈ {K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L} and K.μ⁺_L ∈ that set. Per-step `Σᵢ.L = Σᵢ₋₁.L` discharges: K.μ⁻ via A1b (silent frame), K.μ⁺_L via A1a's coverage of its published `L' = L` frame. Transitivity yields `Σ.L = Σ'.L = Σ_edit_link.L`. F8 then forces `findlinks(I, Σ) = findlinks(I, Σ_edit_link)` for every I ⊆ T — the K.μ-only multi-step closure asserted by F9★. Concretely at `I = {α₂}`: `findlinks({α₂}, Σ) = {ℓ}` (Query 1) and `findlinks({α₂}, Σ_edit_link) = {ℓ}` by direct evaluation (the link store is identical to Σ.L across both steps, so the slot-1 test at `ℓ` still meets `{α₂}`; `ℓ'`, `ℓ_meta` remain non-matching). F9★ holds across the chain — every step is K.μ-family, and the result is invariant — matching F9★'s claim against a sequence drawn entirely from the editing surface.

**Implicit verifications in Queries 1–3 (F1, F7(a)).** Queries 1–3 each rely on the singleton-overlap reading of F1's slot-existential: in Query 1, slot 1's coverage at `ℓ` meets `{α₂}` in the singleton `{α₂}`, and that singleton overlap suffices to fire the existential and put `ℓ` in the result without examining slot 2 or slot 3. The design constraint that no strengthening of the intersection condition is permitted (full overlap, majority overlap, etc.) is exercised silently throughout — any strengthening would have excluded `ℓ` from Query 1's result, since slot 1's coverage is the entire prefix-closure of `α₂` and the query is a singleton. Queries 1–3 also exercise F7(a)'s slot symmetry: the match predicate's existential ranges over every slot of every link uniformly, so when Query 3 finds `ℓ'` via its slot 1 (whose coverage extends `α₃`), no slot is privileged over any other — the same uniformity that lets Query 1 find `ℓ` via slot 1 alone. Both observations are intrinsic to the existential structure of `matches` and require no separate verification step.

**Verifying F20 (ImageSetAdditive) by splitting Query 3.** Decompose the V-region `R = {v_a^2, v_a^3}` of Query 3 into the disjoint sub-regions `R₁ = {v_a^2}` and `R₂ = {v_a^3}`. Compute each image separately: `image(R₁, d_a, Σ) = {α₂}` (Query 1's image); `image(R₂, d_a, Σ) = {Σ.M(d_a)(v_a^3)} = {α₃}` by the same projection. Their union `{α₂} ∪ {α₃} = {α₂, α₃}` agrees with the direct computation `image(R₁ ∪ R₂, d_a, Σ) = image({v_a^2, v_a^3}, d_a, Σ) = {α₂, α₃}` (Query 3's image). Composing with `findlinks` via F12's definition yields V-side additivity: `findlinks_V(R₁ ∪ R₂, d_a, Σ) = findlinks_V(R₁, d_a, Σ) ∪ findlinks_V(R₂, d_a, Σ) = {ℓ} ∪ {ℓ, ℓ'} = {ℓ, ℓ'}`, matching Query 3's result.

**Verifying F19 (ResultSetMonotonicity) under a K.λ extension.** From the original state Σ, apply a single K.λ allocating a fresh link `ℓ_n` under `d_a` whose slot 1 has the canonical span `(α₂, δ(1, #α₂))` (so its coverage is the same prefix-closure as `ℓ`'s slot 1) and whose slot 2 and slot 3 have coverages disjoint from `{α₂}`. K.λ's subsequent-emission precondition pins `ℓ_n` to the chain successor of the most-recently-allocated link under `d_a`: `ℓ_n = inc(ℓ, 0) = [d_a.0.s_L.2]`. By the K.λ effect, `Σ'''.L = Σ.L ∪ {ℓ_n ↦ ...}` with all prior entries unchanged (L12). Then `findlinks({α₂}, Σ) = {ℓ}` (Query 1) while `findlinks({α₂}, Σ''') = {ℓ, ℓ_n}` (both `ℓ` and `ℓ_n` now satisfy the slot-1 test against `{α₂}`; ℓ' and ℓ_meta still do not, per Query 1's reasoning carried forward). The inclusion `findlinks({α₂}, Σ) ⊆ findlinks({α₂}, Σ''')` holds with strict containment: `ℓ_n` enters the result, and no prior member leaves it. K.λ is the only operation of V that can grow the result; the growth is monotone, never destructive.

**Verifying F15 (FilteredDeterminism) at Σ vs. Σ''.** The K.μ~ transition of Query 7 preserves `Σ.L` exactly (by K.μ~'s published `L' = L` frame), so `Σ''.L = Σ.L`. F15's hypothesis is satisfied, and F15 predicts `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ) = findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ'')`. Direct evaluation at Σ'' confirms: at `ℓ`, slot 1 covers `{t : α₂ ≼ t}` (unchanged from Σ by L12) and meets `{α₂}` in `{α₂}`; slot 2 covers `{t : α₃ ≼ t}` and meets `{α₃}` in `{α₃}`; both constraints hold. At `ℓ'`, slot 1's intersection with `{α₂}` is empty, the universal fails. At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (subspace-disjoint from `{α₂}`); the slot-1 constraint fails. Result: `{ℓ}`, matching Query 5's pre-K.μ~ evaluation. The arrangement permutation did not perturb the filtered answer because the filtered predicate consults only `(Σ.L, C)` and `Σ.L` is invariant under K.μ~.

**Verifying F17 (FilteredSurvivability) across Query 4's K.μ⁻.** Query 4's K.μ⁻ transition Σ → Σ' contracts `d_a` to `{v_a^1 ↦ α₁}`, but by A1b (ClosedWorldPreservation, invoked at the K.μ⁻ step), `Σ'.L = Σ.L`. F17 then predicts `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ) = findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ')`. Direct evaluation at Σ' confirms: at `ℓ`, slot 1 coverage and slot 2 coverage are both unchanged from Σ (L12), so both constraints continue to hold and `ℓ` is in the filtered result. At `ℓ'`, slot 1 still fails the `{α₂}` test, so `ℓ'` is excluded. At `ℓ_meta`, slot 1's subspace mismatch persists, so the slot-1 constraint still fails. Result: `{ℓ}`, matching Query 5's pre-edit evaluation. The reader's "from `α₂` to `α₃`" query survives the contraction in the I-side answer; the V-side query surface has shrunk (no V-position in `d_a` now maps to `α₂` or `α₃`), but the filtered link-side answer at the fixed `(I_from, I_to)` is invariant.

The example is small enough to inspect by eye, and the abstract definitions reduce to elementary set operations. Larger instances scale the same way: each link tests independently, slot existentials collect witnesses, and the comprehension assembles the answer.

## What Completeness Demands of Implementations

We have specified the result as a set. An implementation must produce exactly this set — no more, no fewer. The abstract specification is silent on *how* the set is computed.

The spec's demand on any conforming implementation is exactly F2 ∧ F3: `result(I, Σ) = findlinks(I, Σ)`. We do not specify the mechanism. We specify the result. Any implementation whose `result(I, Σ)` differs from the set comprehension is non-conforming, regardless of cause.

## Local Atomicity and the Single-State Setting

The abstract specification is stated against a single state `Σ`. By the sequential-transition axiom (ASN-0093), every state transition is atomic and uninterruptible. The state `Σ` is well-defined at every point at which a query is evaluated.

A K.λ transition commits a link to `dom(Σ.L)` atomically. By the time the K.λ committing `a` returns, `a` is in `dom(Σ.L)`. The next query — at any state succeeding the K.λ — must include `a` in its result if `a` matches. There is no intermediate state in which `a` exists in `dom(Σ.L)` but is undiscoverable through the abstract operation.

This atomicity is the abstract-specification-level mechanism by which any conforming implementation makes the *next-query* coherence concrete: the query result reflects the current state's link store, fully and exactly. Implementations that defer index maintenance to a background process create a window in which the index lags the link store; during that window, results computed from the index would violate F2. The abstract specification permits no such window. (Nelson's design intent at Literary Machines 2/46 — that backlinks be returnable "without appreciable delay" — is a commitment on interactive responsiveness for the reader experience, binding the implementation to interactive rather than batch latency for backlink discovery, but silent on stronger commit-visibility models beyond the "next query after K.λ commitment reflects the link" reading. The next-query coherence above is the abstract-specification-level reading of this latency commitment; no foundation invariant of this ASN formalises a timing bound.)

## Implementation Notes (Non-Normative)

Conformance is exhausted by F2 ∧ F3 — any procedure (with or without an auxiliary index) that produces `result(I, Σ) = findlinks(I, Σ)` conforms; the abstract specification is index-agnostic.

## What We Have Not Specified

We have not specified the procedure by which the operation is computed. We have not specified how the operation behaves across multiple physical instances of the link store, where partition tolerance and consistency models become relevant. We have not specified caching. We have not specified access control beyond noting it as an orthogonal scope filter.

We have not specified the inverse direction — the resolution of the result's endsets back to V-positions in the reader's document or in some target document. Once links are found, the reader typically wants to see where the other ends lead, which requires consulting `Σ.M(·)` to find V-positions whose I-image lies in the relevant endset coverage. That is the I→V resolution belonging to FOLLOWLINK/RETRIEVEENDSETS, and it has its own specification with its own subtleties (notably, the handling of I-addresses that no current arrangement maps).

We have not specified what FINDLINKS returns when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The match predicate still works mechanically — `coverage(e) ∩ I` is well-defined for any `I ⊆ T` — but the operational meaning of querying with phantom addresses is left unsettled.

We have not introduced a separate operation for the combined filtered-and-scoped form `findlinks_filtered_scoped(C, S, Σ)` — the operationally common shape combining slot constraints with an address-set scope. The intended composition is naive intersection: `findlinks_filtered(C, Σ) ∩ S`, equivalently `{a ∈ dom(Σ.L) ∩ S : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}`. Determinism, survivability, and monotonicity propagate to this composition pointwise: determinism by F15 ∧ F16 composed under intersection (intersecting two equal sets with a query-supplied `S` preserves equality), survivability by F17 ∧ F18 under the same intersection lemma, and monotonicity by F19-filt under intersection-preservation (`findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ')` lifts to the intersected form with `S` held fixed). The combined operation adds no new structural content over the two separate operations and so is left implicit here; downstream specs that need the composed form should restate the conformance contract `result_filtered_scoped(C, S, Σ) = findlinks_filtered(C, Σ) ∩ S` against their own implementation surface, inheriting determinism, survivability, and monotonicity from the per-component claims above.

## Reflection

The discovery operation reduces to a single set comprehension: take the I-set the user named (directly, or by V-projection through phase 1), test each link's endset coverage for overlap (the match predicate of phase 2), and return the matching links. The complexity of real systems lies entirely in the *implementation* — in maintaining indexes that make the comprehension fast, in propagating updates across servers, in handling access control, in managing the storage of large endsets. The abstract specification is just the comprehension.

That the specification is so spare is a consequence of design choices that began long before this operation. Because links attach to bytes (ASN-0043 L13), discovery can be by address overlap. Because bytes carry permanent identity (ASN-0036 S0, ASN-0093 C0), the overlap is well-defined and stable. Because arrangement is a separate concern from identity (ASN-0036 S9), discovery is arrangement-independent. Because the address space is globally unique (ASN-0034 T10), identity-based queries cannot collide across owners. Because the link store is monotonic (ASN-0093 L12), discovery is monotone in the link store. None of these properties were established for the sake of discovery; they were established for other reasons, and discovery falls out of them.

The reverse claim is equally true. None of these design choices could have been weakened without compromising discovery. If links attached to V-positions rather than I-addresses, editing would invalidate them. If content identity were not permanent, the match predicate would have no stable referent. If arrangement and identity were not separated, discovery would have to consult the arrangement and lose its key invariance property. The discovery operation is short because the architecture earned its shortness.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `image(R, d, Σ)` | I-image of a V-region with silent projection: `{Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}` | definition |
| `findlinks(I, Σ)` | Discovery operation: `{a ∈ dom(Σ.L) : matches(a, I, Σ)}` | definition |
| `findlinks_V(R, d, Σ)` | Two-phase composite: `findlinks(image(R, d, Σ), Σ)` (see F12) | definition |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints `C` | definition |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | definition |
| A1a | PublishedFramePreservation: for operations in {K.σ, K.α, K.δ, K.μ~, K.μ⁺_L} (the subset of V ∖ {K.λ} whose published frames list `L' = L` directly), every transition preserves `Σ.L` immediately from the published frame. Derived structural lemma carrying no interpretive commitment beyond the substrate spec | introduced (derived structural lemma) |
| A1b | ClosedWorldPreservation: for operations in {K.μ⁺, K.μ⁻, K.ρ} (the subset of V ∖ {K.λ} whose published frames omit `L`), every transition preserves `Σ.L` under the closed-world reading of the substrate's effect-clause convention (components absent from both effect and frame are unchanged). Convention-grounded structural lemma adopted methodologically by this ASN; downstream citations at K.μ⁺, K.μ⁻, K.ρ inherit the convention-grounded interpretive commitment. Convergent (non-constitutive) grounding from Nelson's design-intent principles (LM 2/14, 2/45, 2/29) and Gregory's udanax-green implementation evidence at INSERT, DELETE, and `docopy` supports the closed-world reading; the methodological commitment remains primary because the substrate spec does not formally axiomatise the convention. Substrate revision (publishing `L' = L` in the three silent frames or axiomatising the convention) is not pursued here for scope and separability reasons recorded in A1b's body | introduced (convention-grounded structural lemma) |
| A1 | LinkStoreInertOfNonAllocatingOperations: K.λ is the unique operation in V that modifies the link store; every operation in V ∖ {K.λ} preserves `Σ.L`. Composite structural lemma: union of A1a (covering K.σ, K.α, K.δ, K.μ~, K.μ⁺_L from published frames — A1a invocations carry no convention-grounded commitment) and A1b (covering K.μ⁺, K.μ⁻, K.ρ from the closed-world reading — A1b invocations inherit the convention-grounded interpretive commitment). Operational reach of A1's contribution is entirely through A1b at the three silent-frame operations; A1a invocations at the other five operations rest on substrate-published frames alone | introduced (composite structural lemma) |
| F1 | MatchPredicate: defining equation `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` introducing the named match predicate (uniqueness as a match formula is the substantive content of F4) | definition |
| F2 | Completeness: every matching link in `dom(Σ.L)` appears in the result | introduced |
| F3 | Soundness: every link in the result is in `dom(Σ.L)` and matches | introduced |
| F2-filt | Filtered completeness: every link satisfying every constraint in `C` appears in `result_filtered(C, Σ)` | introduced |
| F3-filt | Filtered soundness: every link in `result_filtered(C, Σ)` is in `dom(Σ.L)` and satisfies every constraint in `C` | introduced |
| F2-sco | Scoped completeness: every link in `dom(Σ.L) ∩ S` matching `I` appears in `result_scoped(I, S, Σ)` | introduced |
| F3-sco | Scoped soundness: every link in `result_scoped(I, S, Σ)` is in `dom(Σ.L) ∩ S` and matches `I` | introduced |
| F2-V | V-side completeness: every link in `dom(Σ.L)` matching `image(R, d, Σ)` appears in `result_V(R, d, Σ)` | introduced |
| F3-V | V-side soundness: every link in `result_V(R, d, Σ)` is in `dom(Σ.L)` and matches `image(R, d, Σ)` | introduced |
| F4 | MatchFormulaMinimality: F1's form is the unique match predicate up to operational distinguishability via F2 ∧ F3 conformance, with the operational gap realizable at K.λ-reachable states (uniqueness stated relative to the reader's promise, not absolute predicate-theoretic uniqueness); F2 forbids strengthenings (incompleteness), F3 forbids weakenings (unsoundness); realizability discharge covers the full space of F1-admitted pairs via K.λ allocation | introduced |
| F5 | Identity, not value: the match consults coverage, not content values | introduced |
| F6 | Transclusion transparency: same I-address, same matches regardless of V-path | introduced |
| F7 | Endset symmetry: slots are equally searchable; filters conjoin | introduced |
| F8 | Determinism: `result(I, Σ)` is a function of `(Σ.L, I)` | introduced |
| F9 | Link survivability under edits: K.μ-family transitions preserve `findlinks(I, ·)` | introduced |
| F9★ | Edit-only survivability: across any reachable sequence in which every step is a K.μ-family operation, `findlinks(I, ·)` is invariant — multi-step closure of F9 within the edit-only fragment | introduced |
| F9★-cor | Non-allocating multi-step preservation: across any reachable sequence in which every step is in V ∖ {K.λ}, `findlinks(I, ·)` is invariant — multi-step closure of F9-cor across the full non-allocating fragment | introduced |
| F9-cor | Non-allocating preservation: every operation in V ∖ {K.λ} preserves `findlinks(I, ·)`; A1b is the load-bearing premise at K.μ⁺, K.μ⁻, and K.ρ (the three silent-frame operations); the other five operations discharge from A1a's coverage of their published `L' = L` frames | introduced |
| F10 | Ordered result: canonical T1-sorted presentation | introduced |
| F10-filt | Filtered ordered result: `findlinks_filtered(C, Σ)` admits a unique canonical T1-sorted presentation | introduced |
| F10-sco | Scoped ordered result: `findlinks_scoped(I, S, Σ)` admits a unique canonical T1-sorted presentation | introduced |
| F10a | AnchorLiftingOfDocumentOrdering: for documents `d₁ < d₂` with `zeros(d₁) = zeros(d₂) = 2`, the link sub-allocator anchors satisfy `b_L(d₁) < b_L(d₂)` under T1 and are non-nesting under `≼`; PrefixOrderingExtension lifts to every link address extension | introduced |
| F11 | Persistent discoverability: matching at `Σ` implies matching at every `Σ'` reached from `Σ` | introduced |
| F12 | TwoPhaseFactoring: `findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)` — names the V→I→Link composite for citation in downstream derivations | definition |
| F13 | Set-additive in the I-input: `findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ)` | introduced |
| F14 | Scope filter is intersection: `findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S` | introduced |
| F15 | Filtered determinism: `findlinks_filtered(C, ·)` is a function of `(Σ.L, C)` | introduced |
| F16 | Scoped determinism: `findlinks_scoped(I, S, ·)` is a function of `(Σ.L, I, S)` | introduced |
| F17 | Filtered survivability: K.μ-family transitions preserve `findlinks_filtered(C, ·)` | introduced |
| F18 | Scoped survivability: K.μ-family transitions preserve `findlinks_scoped(I, S, ·)` | introduced |
| F19 | Result-set monotonicity: `findlinks(I, Σ) ⊆ findlinks(I, Σ')` for every reachable sequence `Σ →* Σ'` | introduced |
| F19-filt | Filtered monotonicity: `findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ')` for every reachable sequence | introduced |
| F19-sco | Scoped monotonicity: `findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ')` for every reachable sequence | introduced |
| F20 | Image set-additive: `image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ)` | introduced |

## Open Questions

What semantics should the operation have when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`?

What completeness guarantees must hold when the link store is logically partitioned across multiple physical instances that may be temporarily disconnected?

What consistency model must FINDLINKS observe with respect to K.λ operations that may be concurrent with or interleaved with the query at a higher protocol layer?

How does access-control filtering compose with the completeness obligation — is completeness restated relative to the authorized scope, and what invariants must the access-control layer preserve to make the composition coherent?

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?

What is the relationship between FINDLINKS and the inverse direction (resolving the result's endsets back to V-positions in some target document), and what additional guarantees does the inverse direction require that FINDLINKS does not?

What is the minimum structural commitment any conforming substrate must make to the non-allocating fragment of its operation vocabulary in order to support link-discovery invariance under those operations?
