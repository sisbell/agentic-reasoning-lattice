# ASN-0068: COMPAREVERSIONS Operation

*2026-05-24*

We are looking for the abstract structure of an operation that, given two documents, surfaces the content they share. The starting fact is the storage model. Every byte in the docuverse occupies exactly one I-address; a document `d`'s *arrangement* `Σ.M(d) : T ⇀ T` is a partial map from V-positions to I-addresses. The same I-address may be referenced by many V-positions across many documents — that is what transclusion produces, and what attribution preserves. *Two documents share content* when their arrangements reference one or more of the same I-addresses.

Before deriving the operation, we must rule out one natural-sounding alternative. Consider two documents `d_a` and `d_b` whose owners independently typed the string `"the cat sat on the mat"`. The bytes were allocated by `d_a`'s and `d_b`'s respective content sub-allocators, producing distinct I-addresses by GlobalUniqueness (ASN-0034). The two documents hold textually identical content at structurally different identities. *They share nothing*. Inversely, two documents holding distinct value sequences at a common transcluded I-address *do* share, though no value-level comparison would detect the relationship. The operation we are constructing exposes I-address overlap, not textual equivalence. The test for correspondence is exact and it is structural; it inherits from the addressing scheme the same atomic, identity-grounded discipline that underwrites attribution, royalty flow, and link survival.

## The Input

The operation takes two `(document, restricting span-set)` pairs:

> `compareversions : (E_doc × SpanSet) × (E_doc × SpanSet) → Result`

written `compareversions(d_a, R_a, d_b, R_b)`. The restricting span-sets `R_a, R_b` select which portions of each arrangement participate. Without them, comparison would implicitly span the entire arrangement of each side; with them, the caller confines the operation to a passage of `d_a` against a passage of `d_b`. Restriction is therefore not a separate filtering stage — it is part of what defines the operation, the lens through which it is asked to look.

For the operation to be well-defined we require:

> **CV-IN**: `d_a, d_b ∈ E_doc`. `R_a, R_b` are normalized V-span-sets (ASN-0053). Every span in `R_a` and every span in `R_b` lies within a single common subspace `S ∈ {s_C, s_L}`, the same `S` for both. Every span `σ ∈ R_a` satisfies `start(σ) ∈ V_S(d_a)` and is level-uniform at depth `m_a := m_{d_a, S}`; symmetrically `σ ∈ R_b` is level-uniform at depth `m_b := m_{d_b, S}` (S8-depth, ASN-0036).

The common-subspace restriction is not optional. Were `R_a` to range over content positions (subspace `s_C`) while `R_b` ranged over link positions (subspace `s_L`), the I-addresses on the two sides would inhabit disjoint storage subspaces — `dom(C)` and `dom(L)` respectively, by L14 (ASN-0047) — and no I-address could coincide. The relation would be empty, but more importantly, its very meaning would be confused: comparison is a per-subspace operation. We require this invariant up front.

The typical setting is `S = s_C`. Comparing arrangements in `s_L` is meaningful (one can ask "which link arrangements do two documents share?") but is a separate semantic concern, and the development here applies uniformly to either single subspace.

We do *not* require `m_a = m_b`. Two documents may carry V-positions at different depths in the same subspace, and the comparison must accommodate this. The depths affect only how V-positions are represented within each document; the I-addresses they point to are sub-allocator outputs whose comparison is depth-independent.

## The Correspondence Relation

Given an admissible input, define the *correspondence relation*:

> `corr_{a,b}(R_a, R_b) = { (v_a, v_b) : v_a ∈ ⟦R_a⟧ ∩ dom(M(d_a)) ∧ v_b ∈ ⟦R_b⟧ ∩ dom(M(d_b)) ∧ M(d_a)(v_a) = M(d_b)(v_b) }`

A pair `(v_a, v_b)` lies in the relation when each V-position is inside its respective restriction, each is mapped, and the two map to the same I-address. The condition is a single tumbler equation in `T` — exact identity, no slack. We note three structural features.

*The relation is symmetric*: `(v_a, v_b) ∈ corr_{a,b}(R_a, R_b) ⟺ (v_b, v_a) ∈ corr_{b,a}(R_b, R_a)`. This is immediate from the symmetry of equality.

*The relation is not in general injective on either side*. A document `d_a` may self-transclude: the same I-address `a` may appear at multiple V-positions `v¹_a, v²_a ∈ dom(M(d_a))`. If `a ∈ ran(M(d_b))` at position `u_b`, then both `(v¹_a, u_b)` and `(v²_a, u_b)` lie in the relation. The relation is many-to-many in the general case, and the operation must report this faithfully.

*The relation is determined entirely by current state*. The expression depends only on `M(d_a)`, `M(d_b)`, and the restrictions; no history is consulted, no derivation lineage is traversed. We name two consequences.

> **CV-IDENT** (*identity test*): Membership of `(v_a, v_b)` in `corr_{a,b}` depends only on the tumbler equation `M(d_a)(v_a) = M(d_b)(v_b)`. The stored values `C(M(d_a)(v_a))` and `C(M(d_b)(v_b))` play no role. Two V-positions whose stored values coincide but whose I-addresses differ do not correspond. Two V-positions whose I-addresses coincide do correspond, regardless of any property of the stored bytes.

> **CV-PROV-FORGOTTEN** (*provenance forgotten*): When `(v_a, v_b) ∈ corr_{a,b}` with shared I-address `a := M(d_a)(v_a) = M(d_b)(v_b)`, the relation provides no information about how `a` came to be referenced by both documents. By S7 (ASN-0036), `a` was allocated by exactly one document `origin(a)`. This may be `d_a` (in which case `d_b` transcluded `a`); it may be `d_b` (the converse); it may be neither (both transcluded from a third source). The relation reports correspondence without explaining lineage.

CV-PROV-FORGOTTEN is necessary for the operation to be definable on any pair of documents regardless of their derivation history. The pair `(d_a, d_b)` may be unrelated to each other — siblings forked from a common ancestor, ancestor and descendant, or wholly independent documents that happen to transclude common material. The operation reports the present-state overlap; it does not reconstruct the history.

## Why I-Address Identity Suffices

A reasonable question: why is I-address identity the right criterion for "shared content," when one might want to ask about value equivalence, derivation, or counterpart correspondence?

Identity captures *what the storage model says is shared*. By design, transclusion shares I-addresses, copying does not. Two documents that genuinely share a fragment do so by transclusion, which preserves the I-address. Two documents that coincidentally contain identical text have different I-addresses, because the bytes were allocated by different sub-allocators. The system uses I-address identity for the same reason it uses identity for attribution: it tracks *which bytes* were referenced, not what they happened to spell.

Counterpart correspondence — the relation between translations, paraphrases, or independently-typed renderings of the same idea — is a *user-asserted* relation. Nelson's mechanism for it is the counterpart link, an explicit declaration in `dom(L)`. The comparison operation cannot derive counterpart correspondence, because counterparts are not byte-shared, and the system does not run heuristic textual analysis. The two notions — shared by inclusion vs. asserted equivalent — are kept rigorously separate.

## The Result

A *correspondence run* between `(d_a, R_a)` and `(d_b, R_b)` is a triple `(v_a, v_b, n)` with `v_a, v_b ∈ T` and `n ≥ 1` such that:

> (i)   `v_a + k ∈ ⟦R_a⟧ ∩ dom(M(d_a))` for `0 ≤ k < n`
> (ii)  `v_b + k ∈ ⟦R_b⟧ ∩ dom(M(d_b))` for `0 ≤ k < n`
> (iii) `M(d_a)(v_a + k) = M(d_b)(v_b + k)` for `0 ≤ k < n`

The notation `v + k` denotes shift in the V-position depth of each document (ASN-0034). A run records that `n` consecutive V-offsets, starting at `v_a` in `d_a` and at `v_b` in `d_b`, share their I-addresses pointwise.

A run is *maximal* when it cannot be extended on either side without leaving a restriction, leaving a domain, or breaking pointwise correspondence:

> *Left-maximal*: either `v_a − 1` is not a valid V-predecessor at depth `m_a` within `⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b − 1` is not a valid V-predecessor at depth `m_b` within `⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a − 1) ≠ M(d_b)(v_b − 1)`.
> *Right-maximal*: either `v_a + n ∉ ⟦R_a⟧ ∩ dom(M(d_a))`, or `v_b + n ∉ ⟦R_b⟧ ∩ dom(M(d_b))`, or `M(d_a)(v_a + n) ≠ M(d_b)(v_b + n)`.

(Here "valid V-predecessor at depth `m`" means the unique tumbler `v'` of depth `m` with `v' + 1 = v`, if such exists at depth `m` within the relevant subspace. By S8a and D-MIN★ (ASN-0047), the V-position `[S, 1, ..., 1]` is the minimum at any given depth and has no predecessor; in that case left-maximality is automatic.)

We define the result of the operation as the set of all maximal correspondence runs over the given input.

> **CV-MAX** (*maximal decomposition*): For admissible input `(d_a, R_a, d_b, R_b)`, there exists a unique set
>
>     `MaxRuns(d_a, R_a, d_b, R_b)`
>
> of maximal correspondence runs such that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one run in the set — i.e., there exists exactly one triple `(v'_a, v'_b, n) ∈ MaxRuns` and exactly one offset `k` with `0 ≤ k < n` such that `v_a = v'_a + k` and `v_b = v'_b + k`. The result of the operation is this set:
>
>     `compareversions(d_a, R_a, d_b, R_b) = MaxRuns(d_a, R_a, d_b, R_b)`

The uniqueness of the maximal decomposition follows the same line of reasoning that underwrites the canonical mapping-block decomposition of an arrangement (M12, ASN-0058). Walking left from any pair `(v_a, v_b) ∈ corr_{a,b}` while pointwise correspondence and restriction membership both hold reaches a unique left-maximal extension; walking right reaches a unique right-maximal extension; the combined extension is the unique maximal run containing the pair.

A correspondence run `(v_a, v_b, n)` projects naturally to a pair of V-spans `(σ_a, σ_b)`:

> `σ_a = (v_a, δ(n, m_a))` and `σ_b = (v_b, δ(n, m_b))`

The widths `δ(n, m_a)` and `δ(n, m_b)` (OrdinalDisplacement, ASN-0034) denote the same ordinal count `n`, expressed at each document's V-position depth. Both spans are level-uniform, and the span-pair view is the natural form for a user-facing rendering: a client can highlight `σ_a` in `d_a` and `σ_b` in `d_b` synchronously, knowing that the underlying I-addresses correspond pointwise.

The set of maximal correspondence runs equivalently presents as a set of span-pairs `{(σ¹_a, σ¹_b), ..., (σᵏ_a, σᵏ_b)}`. The triple form and the span-pair form carry the same information; the choice of representation is presentational, not semantic.

## Atomicity and Granularity

The smallest unit at which sharing is recognized is a single I-address. There is no minimum quotation length, no merge threshold, no lower bound on a meaningful correspondence.

> **CV-ATOM** (*byte granularity*): For each I-address `a ∈ dom(C)` (resp. `dom(L)`) that appears in both restrictions — i.e., `a ∈ ran(M(d_a)|_{⟦R_a⟧})` and `a ∈ ran(M(d_b)|_{⟦R_b⟧})` — every V-position pair `(v_a, v_b)` with `M(d_a)(v_a) = M(d_b)(v_b) = a` is witnessed by a maximal correspondence run of width at least 1 containing it.

This atomicity flows from the addressing scheme. Every byte has its own I-address; correspondence is decided per-address; the result's granularity is therefore one byte. Aggregation into wider runs is a *consequence* of consecutive matches at consecutive offsets — not an editorial choice imposed at the result-construction layer. The maximality condition ensures that contiguous matches do aggregate (a width-`n` run with `n > 1` is not represented as `n` separate width-1 runs); conversely, an isolated single-byte match is not absorbed into a neighboring run if it does not lie in the relation at the adjacent offset.

A subtle consequence: in the presence of self-transclusion, the same I-address `a` may produce multiple width-1 runs that cannot be merged. If `a` appears at V-positions `v¹_a, v²_a` in `d_a` and at `u_b` in `d_b`, the result contains two runs `(v¹_a, u_b, 1)` and `(v²_a, u_b, 1)`. Each is its own maximal extension; the relation `corr_{a,b}` contains two distinct pairs that must both be witnessed (M14, ASN-0058, supplies the structural analogue: multiple V-positions sharing one I-address are independent mapping-block entries).

## Symmetry

The operation is *symmetric in content* and *order-preserving in presentation*. These are two distinct claims about two distinct things.

> **CV-SYM** (*operand symmetry*): There exists a bijection between `compareversions(d_a, R_a, d_b, R_b)` and `compareversions(d_b, R_b, d_a, R_a)` that pairs each run `(v_a, v_b, n)` of the first result with the run `(v_b, v_a, n)` of the second.

This is immediate from the symmetry of the underlying relation: `(v_a, v_b) ∈ corr_{a,b} ⟺ (v_b, v_a) ∈ corr_{b,a}`. The maximal decomposition extends this pointwise symmetry to run-level symmetry: a maximal run in one ordering corresponds to a maximal run in the other, related by the swap of operand positions within the triple.

The relation is symmetric; the *presentation* preserves operand order. Calling `d_a` the "reference" and `d_b` the "comparator" is a convention of the caller, not a distinction the system honors structurally. The operation computes a join, not a unilateral examination.

## Non-Destruction

The operation is *read-only*. Neither `M(d_a)` nor `M(d_b)` is modified; the content store `C`, the link store `L`, the entity registry `E`, and the provenance relation `R` are unchanged. The comparison reads state to produce a value; it commits no transition.

> **CV-RO** (*read-only*): For any state `Σ` and any admissible input, the invocation `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` produces a value of type `Result` without producing a state transition. In particular, `compareversions` is *not* an element of the transition vocabulary Σ-of-ASN-0034 (NoDeallocation) nor of the elementary transition kinds K.α, K.δ, K.μ, K.λ, K.ρ (ASN-0047).

This is structurally guaranteed by the operation's signature: it produces a `Result` value and has no side-effecting clauses in its specification. The arrangement `M(d_a)` is consulted, not modified. The same holds for `M(d_b)`. The content store `C` is consulted only via the implicit S3★ guarantee (ASN-0047) that every arrangement target lies in storage. Nothing is added, nothing is removed.

If a user wishes to record observations from a comparison — say, to annotate that two corresponding passages have a particular relationship — they must do so by creating new content or new links in *their own* document. That is a separate operation, governed by separate transition kinds (K.α, K.μ⁺, or K.λ + K.μ⁺_L), not part of the comparison itself.

## Determinism

The result depends only on the present state.

> **CV-DETERM** (*deterministic*): For any state `Σ` and admissible input `(d_a, R_a, d_b, R_b)`, the value `compareversions(d_a, R_a, d_b, R_b)` evaluated at `Σ` is uniquely determined. Two invocations against the same state with the same input yield the same result.

This follows from the uniqueness of the maximal decomposition (CV-MAX). The arrangements `M(d_a)` and `M(d_b)` are determined by the state; the relation `corr_{a,b}` is determined by the arrangements and the restrictions; the maximal decomposition is unique; the result is therefore unique.

By contrast, the result *does* depend on state. If `Σ → Σ'` is an arrangement transition affecting either `M(d_a)` or `M(d_b)` — for instance, a K.μ⁻ contraction removing some V-positions, a K.μ⁺ extension adding new ones, or a K.μ~ reordering — the relation `corr_{a,b}` may change, and `compareversions` evaluated at `Σ'` may yield different maximal runs. The operation is a snapshot, not a continuous binding. Caller-side caching is safe only as long as the relevant arrangements remain stable.

## Pairwise Scope

The operation compares two specified arrangements. It does not traverse version history.

If `d_a` and `d_b` are two versions of the same document — i.e., one was forked from the other by K.δ at `k = 1` (ASN-0047), or both descend from a common ancestor in the version graph — the comparison operates on `M(d_a)` and `M(d_b)` directly. Whether intermediate versions exist in the fork graph between them is irrelevant: only the present arrangements of `d_a` and `d_b` participate.

This is a separation of concerns. The version-graph structure makes any historical state of any document a valid version entity in `E_doc`. The user who wishes to traverse a history asks for individual pairwise comparisons; the system does not aggregate them into a multi-version operation. The full history remains *accessible* (every version is in `E_doc`); it is not *implicit* in any single invocation.

## What the Result Cannot Express

By construction, the operation cannot:

(i) *Witness historical sharing that no longer holds*. If content was once in `M(d_a)` and was later deleted (K.μ⁻), the I-address is no longer in `dom(M(d_a))` and contributes no correspondence. The provenance relation `R` (ASN-0047) retains the historical fact `(a, d_a) ∈ R` (P4a), but `compareversions` consults `M`, not `R`. Stale references in `R` cannot generate phantom correspondences.

(ii) *Witness counterpart correspondence*. Independent textual matches without I-address identity are invisible. The user-asserted counterpart link is Nelson's mechanism for declaring such correspondences; it lives in `dom(L)` and is a distinct structural artifact.

(iii) *Witness derivation lineage*. Whether `d_a` transcluded from `d_b`, or the converse, or both from a third document, is not visible in the result. The operation reports correspondence; it does not explain it.

These omissions are not deficiencies of the operation; they are consequences of grounding correspondence in I-address identity. The same grounding is what makes attribution, royalty flow, and link survival work uniformly across the docuverse. Every operation that consumes I-addresses inherits exactness from the addressing scheme. The comparison operation is no exception — and the things it cannot express are precisely the things that would require a different grounding.

## Closure Properties

The operation composes cleanly with the state-transition system of ASN-0047. Because it is read-only (CV-RO), it satisfies the frame conditions of every transition kind trivially — it modifies nothing. It can be invoked freely without interfering with concurrent or subsequent transitions; it neither adds to `dom(C)` (so does not interact with allocation invariants), nor modifies any arrangement (so does not interact with arrangement invariants), nor records provenance (so does not affect coupling constraints).

Because it is deterministic (CV-DETERM), the result is robust under stable state: the same comparison invoked at multiple points in time yields the same answer, provided neither `M(d_a)` nor `M(d_b)` (nor the restrictions) change. The result is therefore a pure derived value — extractable from state, but not a part of state.

These two properties together — read-only and deterministic — make `compareversions` a *pure observation* of state. It extracts a derived value (the set of maximal correspondence runs) without affecting the state from which it is derived. This pure-observation status is what allows the operation to be safely invoked under any conditions, at any time, with no risk of corrupting the documents being examined.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CV-IN | Admissibility: `d_a, d_b ∈ E_doc`; `R_a, R_b` normalized V-span-sets lying within a single common subspace `S`; each span level-uniform at the document's V-position depth in `S` | introduced |
| `corr_{a,b}` | Correspondence relation: `{(v_a, v_b) ∈ ⟦R_a⟧ ∩ dom(M(d_a)) × ⟦R_b⟧ ∩ dom(M(d_b)) : M(d_a)(v_a) = M(d_b)(v_b)}` | introduced |
| CV-IDENT | Correspondence is determined by I-address equality, not by value equality of stored content | introduced |
| CV-PROV-FORGOTTEN | The relation does not distinguish how shared I-addresses came to be referenced — direct or transitive transclusion produces indistinguishable correspondences | introduced |
| Correspondence run | A triple `(v_a, v_b, n)` with `n ≥ 1` and pointwise correspondence at all offsets `0 ≤ k < n`, both endpoints lying in their restrictions | introduced |
| Maximal correspondence run | A correspondence run that cannot be extended left or right without leaving a restriction or breaking pointwise correspondence | introduced |
| CV-MAX | `MaxRuns(d_a, R_a, d_b, R_b)` is uniquely determined; every pair in `corr_{a,b}` is witnessed by exactly one maximal run | introduced |
| CV-ATOM | Sharing is recognized at single-I-address granularity; the minimum-width run is 1; no quotation-length threshold | introduced |
| CV-SYM | Operand-swap symmetry: there is a bijection swapping each run `(v_a, v_b, n)` with `(v_b, v_a, n)` between the two orderings of the operation | introduced |
| CV-RO | The operation is read-only — no component of `Σ` is modified by its invocation; it is not an element of the transition vocabulary | introduced |
| CV-DETERM | The result is uniquely determined by the inputs and the state; two invocations against identical state with identical inputs yield identical results | introduced |

## Open Questions

What invariants must the correspondence relation preserve when one or both documents undergo concurrent arrangement modification mid-comparison?

Under what conditions must `compareversions` return identical results across replicated copies of the docuverse holding the same documents at logically equivalent states?

What must remain true about a maximal correspondence run when its underlying I-addresses span a sub-allocator boundary — i.e., when consecutive V-offsets are mapped to I-addresses with different `origin`?

What must the system guarantee about the result's representation when V-position depths differ between the two compared documents?

Under what conditions can shared content between two documents be bounded in size — relative to either input's restriction — without exhaustive enumeration?

What invariants must hold over a sequence of comparisons that walk a version history pairwise, given that each invocation is independent and pairwise?

What guarantees must the operation make when restrictions overlap V-positions that have been contracted from the arrangement but are still referenced in the provenance relation `R`?

Under what conditions can multiple `compareversions` results be composed into a coherent multi-document correspondence — and what abstract structure must such a composition preserve?

What must remain true about a correspondence run when one or both of its V-positions hold content that is itself transcluded from a third document?

Under what conditions can the result be presented as a set of span-pairs whose total V-width is bounded by the smaller of the two input restrictions?
