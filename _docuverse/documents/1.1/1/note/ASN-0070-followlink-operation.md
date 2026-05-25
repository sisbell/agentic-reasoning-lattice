# ASN-0070: FOLLOWLINK Operation

*2026-05-25*

We are looking for the operation that, given a link and a document, identifies where in the document the link's endsets reach — what V-positions in that document's arrangement currently hold the bytes the link points to. The operation is a pure query; it modifies no state. What it must compute, what regularity it must exhibit, and what shape its result must take are the questions of this note.

The argument begins with a single mathematical relation: an inverse image. Every property of the operation — determinism, multiplicity, partial reach, empty admissibility, slot uniformity, origin symmetry — follows from that relation combined with the foundations. We shall develop it once and then read off consequences.

## The Setting

The link store `Σ.L` carries link values `L(ℓ) = (e₁, ..., eₙ)` where each `eᵢ` is a finite set of well-formed I-spans (L3, ASN-0043). Every endset has an associated set of I-addresses — its *coverage*:

```
coverage(e) = ⋃_{σ ∈ e} ⟦σ⟧
```

where `⟦σ⟧` is the I-coverage of span `σ` (T12, ASN-0034). The coverage is a subset of `T`, fixed at link creation and immutable thereafter (L12, ASN-0043). An endset records *which bytes* a link reaches; the specific span decomposition is a representational choice, not a semantic one.

Documents arrange I-addresses into V-positions. The arrangement of document `d` is the partial function `M(d) : T ⇀ T` from V-positions to I-addresses (ASN-0036). For any `v ∈ dom(M(d))`, `M(d)(v)` is the I-address that `d` currently places at V-position `v`. The set of I-addresses `d` references right now is `ran(M(d))`.

What lies in `dom(Σ.C)` but not in `ran(M(d))` is content stored in the system but not arranged in `d` — perhaps arranged in some other document, perhaps unarranged anywhere. By content immutability (S0, ASN-0036), the content remains; only the arrangement varies. The arrangement is the variable; the content is the constant.

Resolution is the inverse problem: given I-addresses (from an endset), find the V-positions in `d` that currently hold them.

## The Inverse-Image Relation

The mathematical content of resolution is the inverse image. For a document `d` and an endset `e`, define:

```
R(d, e) = { v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e) }
```

Equivalently, `R(d, e) = M(d)⁻¹(coverage(e))`.

This is well-defined. By S2 (ArrangementFunctionality, ASN-0036), `M(d)` is a partial function — every V-position in its domain has exactly one image. The inverse image of `coverage(e)` is the set of pre-images, and it is a uniquely determined subset of `dom(M(d))`.

The definition is *abstract*. It does not depend on how `M(d)` is stored, decomposed, or accessed. It does not depend on the order or structure of spans within `e`. Two endsets with the same coverage produce the same `R(d, e)`. Resolution is a function of coverage and arrangement — nothing more.

From this single relation, the entire specification of FOLLOWLINK follows.

## Reachability

Whether a given I-address `a ∈ coverage(e)` contributes V-positions to `R(d, e)` is determined entirely by whether `a ∈ ran(M(d))`. We observe three regimes:

**Total reach.** `coverage(e) ⊆ ran(M(d))`. Every I-address in the endset's coverage is mapped somewhere in `d`. `R(d, e)` is the full pre-image, possibly with multiplicity if S5 (UnrestrictedSharing, ASN-0036) is realised — that is, if some `a` is arranged at multiple V-positions of `d`.

**Partial reach.** `coverage(e) ∩ ran(M(d)) ≠ ∅` but `coverage(e) ⊄ ran(M(d))`. Some I-addresses are reached; others are not. `R(d, e)` is non-empty but contains only the V-positions for the reached subset.

**No reach.** `coverage(e) ∩ ran(M(d)) = ∅`. None of the endset's I-addresses appears in `d`'s arrangement. `R(d, e) = ∅`.

The system must accept all three regimes uniformly. There is no error condition for an unreached I-address; the empty set is a regular outcome. Whether the unreached portion can be observed elsewhere — in another document, in a past or future state, in any arrangement at all — is irrelevant to the resolution against `d` in the current state.

In particular, the link `ℓ` itself remains in `dom(Σ.L)` regardless of any reach condition. By L12, `L(ℓ)` and its endsets are state-invariant. A "broken" link, in the sense of one that resolves to `∅` everywhere, is not destroyed: it is simply a link whose referenced content is not currently arranged. The link is preserved; what varies is whether any arrangement reflects it.

## Result Form and the Operation

`R(d, e)` is a set of V-positions — a set, not a structured object. For transmission, storage, and presentation we require a finite representation. The natural representation is a span-set in V-space (ASN-0053).

We argue the choice is essentially forced. By the per-subspace decomposition of `M(d)` (S8★, ASN-0047) and the existence of finite mapping-block decompositions (M2, ASN-0058), the inverse image `M(d)⁻¹(X)` of any finite union of I-spans `X` corresponds to a finite collection of contiguous V-runs. Each V-run is described by a single V-span. A finite collection of V-spans is, by definition, a span-set.

Concretely, the operation FOLLOWLINK has the following form:

```
follow : (ℓ, d, i) → (d, Σ_V)
```

**Preconditions.** `ℓ ∈ dom(Σ.L)`, `d ∈ E_doc`, `1 ≤ i ≤ |L(ℓ)|`.

**Postcondition.** `follow(ℓ, d, i) = (d, Σ_V)` where `Σ_V` is a finite V-span-set with `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`.

**Frame.** `Σ' = Σ`. No component of state is modified.

The preconditions are weak: only that the link exists, the document is allocated, and the endset index is in range. There is no requirement that `d` be `ℓ`'s home document. There is no requirement that any I-address in the endset's coverage be arranged in `d`. There is no requirement that the link have been resolved before, nor that the arrangement be in any particular state.

The result is a *pair* `(d, Σ_V)`. The document `d` accompanies the span-set because V-positions only have meaning relative to a document's arrangement: the span `[1,1,3]` in `d`'s V-space and `[1,1,3]` in `d'`'s V-space denote unrelated V-positions in unrelated arrangements. Pairing the span-set with `d` preserves the resolution's context.

The span-set `Σ_V` admits canonicalisation. By S8 (NormalizationExistence) and S9 (NormalizationUniqueness) of ASN-0053, every span-set whose components are mutually level-compatible has a unique normalised form sorted by V-start with neither overlap nor adjacency. Within a single V-subspace of `d`, all V-positions share a common depth (S8-depth, ASN-0036), so the level-uniformity required for normalisation is structurally available. When `R(d, e)` spans multiple V-subspaces, the result decomposes naturally into per-subspace components, each canonicalised independently. The canonical form is the preferred representation; any equivalent representation satisfies the postcondition.

## Derived Properties

Each of the following is a consequence of the inverse-image definition combined with the foundations. We catalogue them as F1, F2, ... to support reference.

**(F-det) Determinism.** For fixed `Σ`, `ℓ`, `d`, `i`: the canonical form of `Σ_V` is uniquely determined.

`R(d, L(ℓ).eᵢ)` is the inverse image of a fixed set under a partial function (S2). Its canonical span-set representation is unique (S9). Two queries against the same state produce identical canonical results. Nelson's commitment — "a given part of a given version at a given time" yields the same answer — is the structural consequence of working with functions and a canonical normal form. Without it, citation would be impossible.

**(F-sound) Soundness.** Every `v ∈ ⟦Σ_V⟧` satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)`.

By the definition `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`. The result contains nothing extraneous.

**(F-complete) Completeness.** Every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` satisfies `v ∈ ⟦Σ_V⟧`.

Also by the definition. The result omits no qualifying V-position.

**(F-empty) Empty admissibility.** `⟦Σ_V⟧ = ∅` is a valid outcome, represented by `Σ_V = ⟨⟩`.

When `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅`, the inverse image is empty. The operation succeeds and returns `(d, ⟨⟩)`. There is no exception, no error, no fallback.

**(F-multi) Multiplicity preservation.** If `v₁ ≠ v₂` are both in `dom(M(d))` with `M(d)(v₁) = M(d)(v₂) = a ∈ coverage(L(ℓ).eᵢ)`, both are in `⟦Σ_V⟧`.

The inverse image of a set is the union of pre-images. Every pre-image of `a` is in the result. Where the arrangement places the same I-address at multiple V-positions (the within-document transclusion case of S5), the resolution returns all of them.

**(F-frame) Frame.** `Σ' = Σ`. The operation is read-only: `C' = C`, `M' = M`, `L' = L`, `E' = E`, `R' = R`.

The operation requires no write-locking and no exclusive access. Concurrent queries are admissible insofar as the underlying arrangement is accessible.

These properties are not independent axioms requiring separate verification. They are five readings of the same definition: `R(d, e) = M(d)⁻¹(coverage(e))` with a canonical span-set representation.

## Computation via Decomposition

The mapping-block decomposition view of `M(d)` makes the computation of `follow` concrete.

Each block `β = (v, a, n)` describes a contiguous mapping run: V-positions `v, v+1, ..., v+n−1` map to I-addresses `a, a+1, ..., a+n−1` (ASN-0058). The I-extent `I(β) = {a + k : 0 ≤ k < n}` is the contribution of this block to `ran(M(d))`.

For each endset I-span `σ = (s, ℓ_σ)` with coverage `⟦σ⟧`:

- If `I(β) ∩ ⟦σ⟧ = ∅`, the block `β` contributes nothing.
- If `I(β) ∩ ⟦σ⟧` is non-empty, it is a contiguous sub-range `{a + j + k : 0 ≤ k < c}` for some offset `j` and width `c`. The corresponding V-positions are `v + j, ..., v + j + c − 1` — a single contiguous V-run within `β`. This is recorded as the V-span `(v + j, δ(c, #(v + j)))`.

Aggregating across all blocks and all endset spans, then normalising via S8, yields `Σ_V` in canonical form.

This is *one* admissible computation. The abstract specification does not mandate the decomposition strategy. Any procedure that produces a span-set with denotation `R(d, e)` satisfies the postcondition. The decomposition view simply confirms that the computation is finite and well-structured: linear in the number of (block, endset-span) pairs whose I-extents intersect.

The decomposition also clarifies why fragmentation appears naturally. If a single endset I-span `σ` intersects two non-adjacent mapping blocks of `d`, it produces two non-adjacent V-runs in the result — exactly because the blocks themselves are non-adjacent in V-space. No special logic handles fragmentation; the decomposition delivers it automatically. The same observation explains multiplicity: if multiple blocks each have the same `a` as their I-start with the same width, each block independently contributes a V-run, and the result contains all of them.

## Sub-cases as One Phenomenon

The three results commonly distinguished — *multiple occurrences*, *fragmentation*, and *empty resolution* — are not three separate cases requiring distinct handling. They are the same definition observed under different arrangement configurations.

**Multiple occurrences.** When `d` arranges a single I-address at multiple V-positions (a within-document transclusion), every such V-position resolves. The inverse image of a singleton may have any cardinality consistent with S5.

**Fragmentation.** When an endset's I-coverage is contiguous but the corresponding V-positions are non-contiguous (because the arrangement has placed the content non-contiguously, or has been rearranged), the result has multiple disjoint V-spans. The single endset becomes multiple V-spans in the result — not because the link changed but because the arrangement did.

**Empty result.** When no I-address in `coverage(e)` appears in `ran(M(d))`, the inverse image of `coverage(e)` is empty. The result is `(d, ⟨⟩)`.

All three arise without special logic from the inverse-image definition. They are observable distinctions in the result, not architectural distinctions in the operation.

## Slot Uniformity

A link `L(ℓ) = (e₁, ..., eₙ)` has multiple endset slots, including the designated type endset `e₃` (StandardTriple convention, ASN-0043). The operation `follow` treats every slot identically. For any `i ∈ {1, ..., |L(ℓ)|}`:

```
follow(ℓ, d, i) = (d, Σ_V) with ⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)
```

The from-endset, the to-endset, and the type endset resolve by the same mechanism. There is no special routing for the type slot, no privileged path for the source, no different handling for any role. Whatever semantics slots carry — directionality, type-as-classifier, additional roles in extended links — they are imposed by interpretation, not by resolution.

This uniformity is what makes the operation composable. Resolving all endsets is exactly resolving each endset:

```
followAll(ℓ, d) = ( follow(ℓ, d, 1), follow(ℓ, d, 2), ..., follow(ℓ, d, |L(ℓ)|) )
```

The all-endsets variant is a tuple of single-endset resolutions, positionally aligned with the link's slots. Each component is independent; the type endset's resolution is a span-set in `d`'s V-space, just like any other endset's.

The type endset's *contents* refer to type tumblers (typically allocated in a bootstrap type namespace). Whether `d`'s arrangement includes those tumblers determines whether `R(d, e₃)` is non-empty. If `d` does not arrange any type addresses, `R(d, e₃) = ∅` — the type endset resolves to nothing in `d`, exactly as any unreached endset would. The link's *type identity* is preserved in `L(ℓ).e₃` regardless of whether it resolves in any particular document.

## Origin Symmetry

By L4 (ASN-0043), endset spans may reference any addresses in tumbler space — including addresses with `origin(a) ≠ d`. The resolution mechanism is symmetric with respect to origin:

```
v ∈ R(d, e) ⟺ v ∈ dom(M(d)) ∧ M(d)(v) ∈ coverage(e)
```

The condition tests `M(d)(v) ∈ coverage(e)`. It does not test `origin(M(d)(v))`. A V-position that holds native content (with `origin(M(d)(v)) = d`) and a V-position that holds transcluded content (with `origin(M(d)(v)) ≠ d`) qualify for inclusion in `R(d, e)` on the same basis: whether the I-address falls in the endset's coverage.

This is the structural form of Nelson's claim that non-native bytes are as much a logical part of a document as native bytes. From the resolution function's perspective, they are indistinguishable.

The origin distinction does become observable downstream. For any `v ∈ ⟦Σ_V⟧`, the address `M(d)(v)` is recoverable by consulting the state, and from that address `origin(M(d)(v))` is computable by the structural projection of S7 (ASN-0036). A reader examining the result can ascertain the home of any V-position they look at. But the resolution itself does not filter by origin, and the operation makes no architectural distinction between native and transcluded V-positions.

## State-Dependence

The link `L(ℓ)` is state-invariant (L12). The coverage `coverage(L(ℓ).eᵢ)` is fixed at creation. But the arrangement `M(d)` varies with state.

Consequently, `follow(ℓ, d, i)` evaluated at state `Σ` and at state `Σ'` (with `Σ'` reachable from `Σ`) may produce different results. This is not a violation of determinism. Determinism is "same state, same result." Across different states, the result reflects the different arrangements.

Two observations follow.

First, the link is not a function of its result. A link's identity is determined by its address and its endsets (L11b, NonInjectivity), not by what its endsets currently resolve to. Two links with identical endsets are distinct links. A single link resolves differently in different documents, and differently in the same document at different states.

Second, brokenness is a state-relative notion. A link whose resolution is empty in `d` at state `Σ` may resolve non-emptily in `d'` at `Σ`, or in `d` at `Σ'`. The link itself is unbroken; its resolution against a specific arrangement may yield the empty span-set. The link persists; what varies is whether arrangements happen to reflect it.

## Multi-Document Reach

For a fixed link `ℓ`, the family `{ follow(ℓ, d, i) : d ∈ E_doc, 1 ≤ i ≤ |L(ℓ)| }` characterises `ℓ`'s reach across the docuverse. The link is one object; its resolutions are many — one per (document, endset) pair.

No document holds special status for resolution. The link's home document `home(ℓ)` — the document under whose tumbler prefix `ℓ` was allocated (L1a, L2 of ASN-0043) — is the allocator of `ℓ`'s address. It need not be the document where the endset's content lives; it need not be the document where readers will encounter the link; it need not be the document being viewed. Resolution against `home(ℓ)` is no different from resolution against any other document. The same link reaches whatever bytes it points to, wherever those bytes are currently arranged.

This is the structural reading of Nelson's "a link to one version is a link to all versions." The link's reach is determined by where its endsets' content is arranged. The universe of arrangements is the universe of documents. The link extends into each on the same terms.

A particular consequence: when a document `d'` is derived from `d` by some derivation that preserves content references (i.e., when `ran(M(d'))` intersects `ran(M(d))` significantly), then links that resolved against `d` will resolve, possibly with different V-position structure, against `d'`. The resolution follows the content, not the document.

## Result Stability

For fixed `Σ`, repeated queries return identical canonical results — by F-det above. This is what makes `follow` suitable as the basis for downstream operations whose correctness depends on result identity: citation, archival reference, comparison across queries, and the entire programme of stable referential integrity.

The stability is a property of three things together:

1. The state `Σ` is fixed.
2. The inverse image `R(d, e)` is uniquely determined by `M(d)` and `coverage(e)`.
3. The canonical span-set form is unique by S9.

Were any of these relaxed, repeatability would fail. With all three in place, `follow` is the bedrock query: ask the same question of the same state, receive the same answer. Nelson's "the part you want comes when you ask for it" is the foundational guarantee, and `follow` is the operation that delivers it for the link-resolution case.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F0 | `R(d, e) := M(d)⁻¹(coverage(e))` is the V-position set of endset `e` in document `d` | introduced |
| F1 | `follow : (ℓ, d, i) → (d, Σ_V)` with `⟦Σ_V⟧ = R(d, L(ℓ).eᵢ)`; `Σ' = Σ` (signature, postcondition, frame) | introduced |
| F2 | Soundness — every `v ∈ ⟦Σ_V⟧` satisfies `v ∈ dom(M(d))` and `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` | introduced |
| F3 | Completeness — every `v ∈ dom(M(d))` with `M(d)(v) ∈ coverage(L(ℓ).eᵢ)` is in `⟦Σ_V⟧` | introduced |
| F4 | Determinism — same `Σ` produces the same canonical `Σ_V` | introduced |
| F5 | Empty admissibility — `⟦Σ_V⟧ = ∅` is a regular outcome, not an error condition | introduced |
| F6 | Multiplicity preservation — all `v` mapping to a given `a ∈ coverage` are in `⟦Σ_V⟧` | introduced |
| F7 | Frame — `follow` reads `Σ` and does not modify any of `C, M, L, E, R` | introduced |
| F8 | Slot uniformity — every `i ∈ {1, ..., |L(ℓ)|}` resolves by the same `R` mechanism | introduced |
| F9 | Origin symmetry — `R` does not filter by `origin(M(d)(v))`; native and transcluded V-positions are treated identically | introduced |
| F10 | Link persistence — `ℓ ∈ dom(Σ.L)` is preserved regardless of any reach condition | introduced |
| F11 | State-dependence — `follow` varies with `Σ.M` but `L(ℓ).eᵢ` is state-invariant | introduced |
| F12 | No preferred document — `follow` accepts any `d ∈ E_doc`; `home(ℓ)` holds no special status | introduced |

## Open Questions

What must the system guarantee about how partial reach is reported to the reader — must the result form preserve information about which I-addresses in the coverage failed to resolve, or only what did resolve?

When an endset's coverage spans I-addresses with multiple distinct origins, what relationship — if any — must hold between resolutions against documents that transclude from different subsets of those origins?

What concurrency semantics, if any, must `follow` guarantee when the document being queried is being modified by another transition concurrently?

Under what conditions, if any, must the result of `follow(ℓ, d, i)` and `follow(ℓ, d', i)` be related when `d` and `d'` share transclusion lineage — that is, when significant portions of their arrangements reference the same I-addresses?

Must the system distinguish the case where `L(ℓ).eᵢ = ∅` (the endset itself is empty) from the case where `L(ℓ).eᵢ ≠ ∅` but `R(d, L(ℓ).eᵢ) = ∅` (the endset has content but none is arranged in `d`)?

When an endset's coverage includes link-subspace addresses, what must the system guarantee about the result's V-positions — are link V-positions distinguished from content V-positions in the result form, or is the result a uniform span-set?

What must the system promise about ordering of the returned span-set — is the canonical V-tumbler order under T1 required, or is any equivalent denotation admissible?

When `coverage(L(ℓ).eᵢ)` is unbounded in cardinality (an endset spanning a very long region of I-space), what must the system guarantee about the result's representational compactness — must the span-set be in canonical form, or is any finite representation admissible regardless of redundancy?

What must the system guarantee about the relationship between resolution and content retrieval — must `R(d, e)` always yield V-positions whose subsequent content lookup via `M(d)` and `C` succeeds, or may resolution succeed where content access would fail?
