# ASN-0077: SHOWORIGIN Operation

*2026-05-25*

Suppose a reader confronts a passage — perhaps a single character, perhaps an entire chapter — and asks: *where did this come from?* In what document was it first set down, by what allocator was it first baptised? The answer must not depend on what the reader is doing or where the passage currently appears. A quote in a tenth-generation derivative document still has one true source. A character copied from one paragraph to another still has one true author. Whatever mechanism we build, it must give one answer, and the same answer in every state of the system.

Nelson states the requirement plainly: *"You always know where you are, and can at once ascertain the home document of any specific word or character."* [LM 2/40] The phrase *any specific word or character* sets the lower bound on scale; the phrase *at once* rules out any procedure that walks chains of indirection. The operation we are searching for is called SHOWORIGIN. Its input is a span of content. Its output is the identity of the home document — or, when the span draws from multiple sources, the set of home documents present. We must show that this operation can be specified abstractly, that its result is determined by the content alone, and that the specification extends uniformly from one address to spans of any size.

## Where origin already lives

The origin of a single I-address is not a new fact we must compute — it is recorded in the address itself. Foundation ASN-0036 establishes this as S7: for every `a ∈ dom(Σ.C)`, the *origin* is the document-level tumbler obtained by truncating the element field,

> `origin(a) = N(a).0.U(a).0.D(a)`,

a projection that is total on `dom(C)`, single-valued, and document-level (`zeros(origin(a)) = 2`). By S7d (DocumentAllocationDiscipline), distinct documents have distinct tumblers, so `origin(a₁) = origin(a₂)` says exactly that `a₁` and `a₂` were allocated by the same document. By S7's clause (d), `origin(a)` is invariant across every state in which `a ∈ dom(C)`. The structural projection reads only components of `a` itself; no registry, no index, no external context is consulted.

What we do not yet have is an operation that takes a *span* — not just one address — and reports the documents present. That is what we now construct.

## Lifting origin to an I-span

Let σ be an I-span (foundation ASN-0053, T12), with start `s` and width `ℓ`, denoting the half-open interval

> `⟦σ⟧ = { t ∈ T : s ≤ t < s ⊕ ℓ }`.

Not every position in `⟦σ⟧` need lie in `dom(C)`; only those that do are content. We define the I-span lift of origin:

> `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.

The result is a finite set of document-level tumblers — finite because `dom(C)` is finite (C-fin, foundation ASN-0047). The set may be empty (no positions in σ are allocated), a singleton (all allocated addresses come from one document), or larger (σ crosses content subspaces of distinct documents).

By S7a (DocumentScopedAllocation, foundation ASN-0036), every I-address allocated by document `d` carries `d`'s prefix. Two addresses share an origin iff they share the prefix `N(a).0.U(a).0.D(a)`. The structural fact this delivers is what we call the origin partition:

**Claim O1 (Origin partitions allocated content).** *Define the relation `~_o` on `⟦σ⟧ ∩ dom(C)` by `a₁ ~_o a₂ ⟺ origin(a₁) = origin(a₂)`. Then:*

> *(a) `~_o` is an equivalence relation on `⟦σ⟧ ∩ dom(C)`;*
> *(b) the quotient map `[a]_{~_o} ↦ origin(a)` is a bijection from `(⟦σ⟧ ∩ dom(C)) / ~_o` to `origins_I(Σ, σ)`;*
> *(c) each equivalence class consists exactly of those I-addresses in `⟦σ⟧ ∩ dom(C)` allocated by one document — by S7d (DocumentAllocationDiscipline, ASN-0036), one allocator.*

*Derivation.* (a) Reflexivity, symmetry, and transitivity are inherited from equality on the codomain of `origin`. (b) The map is well-defined: if `a₁ ~_o a₂` then `origin(a₁) = origin(a₂)` by definition. It is surjective onto `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(C) }` by the definition of `origins_I` (every element is hit by the class of some `a`). It is injective: if `[a₁]_{~_o} ≠ [a₂]_{~_o}` then `origin(a₁) ≠ origin(a₂)`, so the images differ. (c) Fix an equivalence class `[a]_{~_o}`. By S7a, every `b ∈ ⟦σ⟧ ∩ dom(C)` with `origin(b) = origin(a)` was allocated by the document whose tumbler is `origin(a)`. By S7d, distinct documents have distinct tumblers, so a single document tumbler `origin(a)` names a single allocator. Hence the class `[a]_{~_o}` consists exactly of addresses allocated by that one document. ∎

Two corollaries follow without further argument.

**Corollary O1.1 (Single-origin sufficiency).** *If every `a ∈ ⟦σ⟧ ∩ dom(C)` satisfies `origin(a) = d` for a fixed `d`, then `|origins_I(Σ, σ)| ≤ 1`* — direct from the singleton image of the bijection in O1(b). The bound is `≤ 1` rather than `= 1` because `⟦σ⟧ ∩ dom(C)` may be empty.

**Corollary O1.2 (Multi-origin diagnostic).** *If `|origins_I(Σ, σ)| > 1`, then `σ` contains I-addresses allocated by at least two distinct documents* — direct from the bijection in O1(b) combined with S7d. This is what justifies treating multi-origin results as informative: such spans necessarily cross document-allocation boundaries in the I-stream. T12 admits these spans (placing no upper limit on width), but they do not arise from any single document's allocation activity.

## Lifting origin to a V-span

A reader more naturally has access to a V-span — a contiguous region of positions in the document they are reading. The content at those positions may be native (allocated by the reader's document) or transcluded (allocated elsewhere, included by reference). SHOWORIGIN must resolve this question through the document's arrangement.

Foundation ASN-0058 supplies the machinery. A content reference is a pair `(d, σ)` where `d` is a document and `σ = (u, ℓ)` is a level-uniform V-span in `d`'s arrangement. The resolution function returns a sequence of mapping blocks:

> `resolve(d, σ) = ⟨ (a₁, n₁), ..., (aₖ, nₖ) ⟩`,

where each block `(aⱼ, nⱼ)` denotes the I-address run `aⱼ, aⱼ + 1, ..., aⱼ + (nⱼ − 1)`. The V-positions in `⟦σ⟧` map to exactly the I-addresses in these runs (M2, M3 of ASN-0058).

We work with three equivalent expressions for `origins_V(Σ, d, σ)`. The reader-facing form — the form that the operation specification will use — is:

> *(F1)* `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.

The decomposition-expanded form, which reads through `resolve`:

> *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`.

The block-collapsed form, which collects one origin per block:

> *(F3)* `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`.

We adopt (F1) as the definition and derive (F2) and (F3) as equivalent forms; this matches the operation specification below.

**Claim O2 (Block uniformity).** *For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `f = M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.*

*Derivation.* Fix `0 ≤ i < nⱼ`. B3 (Consistency, ASN-0058) gives `f(vⱼ + i) = aⱼ + i`; since `f` is a restriction of `M(d)`, also `M(d)(vⱼ + i) = aⱼ + i`. S3 (ReferentialIntegrity, ASN-0036) gives `M(d)(vⱼ + i) ∈ dom(C)`, hence `aⱼ + i ∈ dom(C)`. This discharges M16a's precondition at `(aⱼ, i)`, and M16a (OriginInvarianceUnderShift, ASN-0058) delivers `origin(aⱼ + i) = origin(aⱼ)`. ∎

**Equivalence chain (F1) ≡ (F2) ≡ (F3).** Apply C1a (RestrictionDecomposition, ASN-0058) to `f = M(d) ↾ ⟦σ⟧`: `f` is a finite partial function with functionality (S2), finite domain (S8-fin), and common depth `m ≥ 2` across its domain (S8-depth combined with S8a, ASN-0036). C1a yields a unique maximally merged decomposition `{β₁, ..., βₖ} = {(v₁, a₁, n₁), ..., (vₖ, aₖ, nₖ)}` of `f`.

*(F2) = (F3):* Inside the inner set for each `j`, M16a applied as in O2 collapses `{ origin(aⱼ + i) : 0 ≤ i < nⱼ }` to `{ origin(aⱼ) }`. Taking the union over `j` yields `{ origin(aⱼ) : 1 ≤ j ≤ k }`.

*(F1) ⊆ (F3):* Fix `v ∈ ⟦σ⟧ ∩ dom(M(d))`. Since `v ∈ ⟦σ⟧ ∩ dom(M(d))` is exactly `v ∈ dom(M(d) ↾ ⟦σ⟧) = dom(f)`, B1 (Coverage, ASN-0058) applied to the decomposition of `f` gives a unique `j` with `v ∈ V(βⱼ)`, so `v = vⱼ + i` for some `0 ≤ i < nⱼ`. By B3, `f(v) = aⱼ + i`, and since `f` is the restriction, `M(d)(v) = aⱼ + i`. By O2, `origin(M(d)(v)) = origin(aⱼ + i) = origin(aⱼ)`, an element of (F3).

*(F3) ⊆ (F1):* Fix `j ∈ {1, ..., k}`. Since `nⱼ ≥ 1`, the block is non-empty: `vⱼ ∈ V(βⱼ) ⊆ dom(f) ⊆ dom(M(d))`, and `vⱼ ∈ ⟦σ⟧` because `dom(f) ⊆ ⟦σ⟧`. B3 gives `M(d)(vⱼ) = aⱼ`, so `origin(aⱼ) = origin(M(d)(vⱼ))`, an element of (F1). ∎

The set `origins_V(Σ, d, σ)` may be smaller than `k` if multiple blocks share an origin — for instance, two separately-transcluded passages drawn from the same source document, or transcluded content interleaved with native content of `d` where the native portions and `d` itself share an origin (`d` itself, for native).

## Structural derivation

The most important claim about SHOWORIGIN is not what it computes but what it does *not* need.

**Claim O3 (Structural derivation).** *`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.*

*Derivation.* For the pointwise claim: (i) S7 of ASN-0036 defines `origin(a) = N(a).0.U(a).0.D(a)`. (ii) T4b (UniqueParse, ASN-0034) defines `N(a), U(a), D(a)` as projections that read only the component sequence of `a` — they require the structural facts `zeros(a) ≥ 2` (here ≥ 3 by S7b of ASN-0036) and the field-separator positions, both determinable by scanning `a`. (iii) Composition of two functions that read only `a` is a function that reads only `a`. Hence `origin(a)` consults no state beyond `a`.

For the I-span lift: `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(C) }` evaluates `origin` pointwise. The set `⟦σ⟧ ∩ dom(C)` is determined by σ (whose denotation is a function of `start(σ)` and `width(σ)` alone, by ASN-0053) and by `dom(C)` (the set of allocated content addresses in Σ). No other component of Σ is consulted.

For the V-span lift, by (F1): `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`. The arrangement `M(d) ↾ ⟦σ⟧` determines `dom(M(d) ↾ ⟦σ⟧) = ⟦σ⟧ ∩ dom(M(d))` and the function values `M(d)(v)` for `v` in that domain. By the pointwise claim, `origin(M(d)(v))` reads only the value `M(d)(v)`, which the restriction supplies. No other state component (no `L`, no `R`, no `E`, no other document's arrangement) is consulted. ∎

The consequence for transclusion is decisive. A document whose server is unreachable still has its tumbler recorded in every transcluded I-address that originated from it; SHOWORIGIN reports this tumbler from the address structure alone. The unreachability of the source bears on whether the bytes can be *fetched*, not on whether the origin can be *named*.

This is what Nelson means when he insists attribution is *unstrippable within the docuverse* [Q1]: there is no metadata to strip. The origin claim is part of the address, and the address is the means by which the bytes are retrieved.

## Direct resolution through transclusion

Suppose content was allocated in document `d₁`. Document `d₂` transcludes it; `d₃` transcludes from `d₂`; this continues to `dₙ`. A reader of `dₙ` asks SHOWORIGIN. What does it return?

Because each transclusion is by reference rather than copy, the I-address recorded in every intermediate document's arrangement is the *same* — it points to the bytes baptised by `d₁`. Each intermediate document `d₂, d₃, ..., d_{n-1}` holds an arrangement entry mapping its own V-positions to this single I-address, but the address does not change as it propagates. The substantive claim is therefore not that origin is computable from `a` alone — that was already O3 — but that *each intermediate document's arrangement independently records the same `a`*, and any of these arrangements can be queried with the same result:

**Claim O4 (Parallel witnesses to a single origin).** *Suppose `a ∈ dom(Σ.C)` with `origin(a) = d₁`, and suppose `d₂, d₃, ..., dₙ` are distinct documents each holding a V-position `vᵢ ∈ dom(M(dᵢ))` with `M(dᵢ)(vᵢ) = a` (for `2 ≤ i ≤ n`). Then for every `i ∈ {2, ..., n}`:*

> *`origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`.*

*The right-hand side does not depend on `i`. Each `dᵢ` for `i ≥ 2` is an independent witness to the same fact.*

*Derivation.* Fix `i ∈ {2, ..., n}`. By hypothesis, `M(dᵢ)(vᵢ) = a`. The pure projection `origin` (defined on `dom(C)`, by S7 of ASN-0036) takes `M(dᵢ)(vᵢ)` to `origin(M(dᵢ)(vᵢ)) = origin(a)`. By hypothesis `origin(a) = d₁`. This argument uses only `dᵢ`'s entry at `vᵢ` and the projection; it never names or reads `dⱼ` for any `j ≠ i`. ∎

This is what Nelson means by *at once* [Q10]: the resolution mechanism walks no chain. Each intermediate `dᵢ` independently registered, via its own K.μ⁺ extension or fork (ASN-0047), an entry mapping one of its V-positions to the I-address `a`. The shared identity of `a` across all intermediate arrangements is what makes the chain depth irrelevant — not a property of the answer, but of the recorded data. By O3, the answer is computable from `a` alone; by O4, every intermediate document holds the same `a` and is interchangeable as a query target. The two claims complement each other.

The same point in calculational form. Let `f_{Mᵢ} = origin ∘ M(dᵢ)`. Then for every `i ∈ {2, ..., n}`:

> `f_{Mᵢ}(vᵢ) = origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`,

with no occurrence of `dⱼ` (for `j ≠ i`) anywhere in the chain of reasoning. The intermediate documents are *parallel witnesses*, not a chain to be traversed.

## Permanence

We turn to the question raised at the start: does the answer change?

**Claim O5 (Origin permanence).** *For any `a ∈ dom(Σ.C)` and any reachable transition `Σ → Σ'`, if `a ∈ dom(Σ'.C)`, then `origin'(a) = origin(a)`.*

*Derivation.* (1) The hypothesis gives `a ∈ dom(Σ.C)` and `a ∈ dom(Σ'.C)`. (2) The address `a` is a fixed tumbler — a sequence of natural-number components. No transition rewrites the components of an existing address; only `dom(C)` (the set of allocated addresses) and `C` (the mapping from addresses to values) can change. The address-as-tumbler is invariant by construction. (3) The projection `origin(·) = N(·).0.U(·).0.D(·)` is a pure function of the component sequence of its argument (O3, sub-claim 1). (4) Both `origin(a)` and `origin'(a)` apply the same projection to the same component sequence, since the projection is independent of state. (5) Therefore `origin'(a) = origin(a)`. P0 (ContentPermanence, ASN-0047) is invoked only to justify that `dom(C) ⊆ dom(C')` is possible at all — that is, that the hypothesis `a ∈ dom(Σ'.C)` is consistent with the hypothesis `a ∈ dom(Σ.C)` under transitions. ∎

For the I-span lift, permanence has a directional character.

**Claim O6 (Monotonic growth under state).** *For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

*Derivation.* Fix any `o ∈ origins_I(Σ, σ)`. By definition, there exists `a ∈ ⟦σ⟧ ∩ dom(Σ.C)` with `origin(a) = o`. (1) By P0 (ContentPermanence, ASN-0047), `dom(Σ.C) ⊆ dom(Σ'.C)`; hence `a ∈ dom(Σ'.C)`. (2) Since `⟦σ⟧` is a state-independent function of σ alone (ASN-0053), the membership `a ∈ ⟦σ⟧` is preserved. (3) Therefore `a ∈ ⟦σ⟧ ∩ dom(Σ'.C)`. (4) By O5, `origin'(a) = origin(a) = o`. (5) Hence `o ∈ origins_I(Σ', σ)`. Since `o` was arbitrary, `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`. ∎

New allocations within σ may introduce new origins, but existing origins cannot be reassigned or removed.

The V-span lift is more nuanced. `origins_V(Σ, d, σ)` depends on the arrangement `M(d)`, which is mutable under editing operations. A passage transcluded today may be removed tomorrow, in which case the corresponding source document is no longer represented at those V-positions. The strongest claim we can make about V-span permanence requires fixing the arrangement:

**Claim O7 (V-span stability under fixed arrangement).** *For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.*

*Derivation.* By (F1), `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`. (1) The frame condition `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧` gives `dom(M'(d) ↾ ⟦σ⟧) = dom(M(d) ↾ ⟦σ⟧)`; that is, `⟦σ⟧ ∩ dom(M'(d)) = ⟦σ⟧ ∩ dom(M(d))`. The two indexing sets are identical. (2) For each `v` in the common indexing set, the function values agree: `M'(d)(v) = M(d)(v)`. (3) Let `a = M(d)(v) = M'(d)(v)`. By S3 (ReferentialIntegrity, ASN-0036), `a ∈ dom(Σ.C)`. (4) S3 applied in Σ' (via S3★ in ASN-0047 when the V-position is in the content subspace, or S3 in ASN-0036 in the foundational case) gives `a ∈ dom(Σ'.C)`. (Alternatively: P0 directly gives `dom(Σ.C) ⊆ dom(Σ'.C)`.) (5) By O5, `origin'(a) = origin(a)`. (6) Hence `origin'(M'(d)(v)) = origin(M(d)(v))` for every `v` in the common indexing set. (7) The two sets `origins_V(Σ', d, σ)` and `origins_V(Σ, d, σ)` are constructed by applying the same operation to the same data, and therefore coincide. ∎

## Span union monotonicity

Nelson is explicit that the system must distinguish no scale below *any specific word or character*: the mechanism that names the home of a million-character chapter must name the home of a single character [Q8]. *Uniformity of mechanism* is captured by O3 (Structural derivation): a single pointwise projection performs the work, with no procedural case distinction on size. What remains to record is the corresponding *set-inclusion* property: enlarging the span never loses an origin.

**Claim O8 (Span union monotonicity).** *For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.*

*Derivation.* Fix `o ∈ origins_I(Σ, σ₁)`. By definition, there exists `a ∈ ⟦σ₁⟧ ∩ dom(Σ.C)` with `origin(a) = o`. By hypothesis `⟦σ₁⟧ ⊆ ⟦σ₂⟧`, so `a ∈ ⟦σ₂⟧`. Since `a ∈ dom(Σ.C)` is unchanged, `a ∈ ⟦σ₂⟧ ∩ dom(Σ.C)`, and `origin(a) = o ∈ origins_I(Σ, σ₂)`. ∎

The smallest case is the singleton: for any `a ∈ dom(C)`, the singleton span (containing only `a`) yields `origins_I = {origin(a)}`. The largest case is unbounded — by T0(b) of ASN-0034, there is no maximum tumbler length, so spans can be arbitrarily wide. The pointwise projection (O3) is what makes attribution at the paragraph level reducible to attribution at the character level; O8 records the elementary set-inclusion consequence.

## Identity, not equivalence

The system distinguishes *wrote the same words* from *quoted from the original* [Q1, Q9]. Two documents that independently produce identical text have distinct I-addresses; transcluded content shares an I-address with its source. SHOWORIGIN tracks the I-address, so it reports identity-of-origin, not equivalence-of-text.

**Claim O9 (Origin tracks creation, not content).** *Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by allocation events under distinct documents `d₁` and `d₂` (with `d₁ ≠ d₂`), then `origin(a₁) ≠ origin(a₂)`.*

*Derivation.* (1) By hypothesis, the allocation event producing `a₁` was performed by document `d₁`; by S7a (DocumentScopedAllocation, ASN-0036), `origin(a₁) = d₁`. (2) Similarly, `origin(a₂) = d₂`. (3) By hypothesis, `d₁ ≠ d₂`. (4) By S7d (DocumentAllocationDiscipline, ASN-0036), distinct documents have distinct document-level tumblers; hence `d₁ ≠ d₂` at the tumbler level. (5) Therefore `origin(a₁) = d₁ ≠ d₂ = origin(a₂)`. The hypothesis `C(a₁) = C(a₂)` does not enter the derivation: the conclusion holds regardless of whether content values agree. ∎

The stronger fact, that the addresses themselves differ (`a₁ ≠ a₂`), is supplied independently by S4 (OriginBasedIdentity, ASN-0036) — distinct allocation events produce distinct addresses, with or without distinct documents. But the relevant point for SHOWORIGIN is the document-level distinction at the projection: reading the same value back from two addresses tells you the bytes match; it does not tell you they came from the same place.

## The operation

We can now specify SHOWORIGIN as a non-state-modifying operation in two arities.

**SHOWORIGIN over an I-span.**
- *Preconditions*: `σ = (s, ℓ)` is a well-formed I-span — explicitly, the conjuncts of T12 (SpanWellDefinedness, ASN-0034): (i) `s ∈ T`; (ii) `ℓ ∈ T`; (iii) `Pos(ℓ)` (TA-Pos, ASN-0034); (iv) `actionPoint(ℓ) ≤ #s` (ActionPoint, ASN-0034).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

**SHOWORIGIN over a content reference.**
- *Preconditions*: `(d, σ)` is a well-formed content reference — explicitly, the conjuncts from the ContentReference definition of ASN-0058: (i) `d ∈ D(Σ)` (the source document has an arrangement defined in the ambient state Σ); (ii) `σ = (u, ℓ)` is a level-uniform V-span, i.e. `#u = #ℓ` (S6 of ASN-0053); (iii) `V_{u₁}(d) ≠ ∅` (the V-subspace identified by `u₁` is non-empty in `d`'s arrangement); (iv) T12 holds for `(u, ℓ)` — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #u`; (v) `#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth, ASN-0036); (vi) the range condition `{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`.
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` (form (F1); equal to (F2) and (F3) by the equivalence chain derived above).
- *Frame*: `Σ' = Σ`.

**Claim O10 (Read-only frame; idempotence).** *Let `op` be either SHOWORIGIN_I or SHOWORIGIN_V. Then for any Σ in which the precondition holds: (a) `op(Σ) = (Σ', result)` with `Σ' = Σ`; (b) two consecutive applications at the same state yield identical results.*

*Derivation.* (a) The frame clause of the operation specification declares `Σ' = Σ` explicitly — every component (`C`, `L`, `E`, `M`, `R`) is unchanged. This is the definition of the operation. (b) Let `op(Σ) = (Σ, r₁)` be the first application. By (a), the post-state is `Σ`. The second application is `op(Σ) = (Σ, r₂)`. The operation's result is a pure function of `Σ`, σ, and (for SHOWORIGIN_V) `d` (because the result is defined by an expression in (F1) or its I-span analogue, which mentions only state-derivable sets and the projection `origin`). Applying the same function to the same arguments yields the same value: `r₁ = r₂`. ∎

Idempotence is essential: SHOWORIGIN must be a passive observation. Without the read-only frame, the act of asking would alter the answer, which would defeat the purpose of having an answer at all.

### Edge cases

Each of the following configurations satisfies the operation precondition; we record what the postcondition delivers in each.

*Empty intersection (I-span).* When `⟦σ⟧ ∩ dom(Σ.C) = ∅` — the well-formed span happens to contain no allocated content addresses — the postcondition expression evaluates to `∅`. The operation succeeds and returns the empty set as a legitimate output. This case is not exceptional: by O6, an empty result at Σ may become non-empty at some `Σ'` if new content is allocated within σ.

*Singleton I-span.* For any `a ∈ dom(Σ.C)`, the span `σ_a = (a, [0, ..., 0, 1])` of length `#a` with all-zero prefix and final component 1 satisfies T12: `Pos(ℓ)` holds, and `actionPoint(ℓ) = #a ≤ #a`. By TA-strict (ASN-0034), `a ⊕ ℓ > a`, so `a ∈ ⟦σ_a⟧`; and the next tumbler exceeding `a` in the same parent is by construction `a ⊕ ℓ`, so `⟦σ_a⟧ ∩ dom(C) = {a}` (assuming no other allocated address sits at that exact position, which is impossible by S4 — distinct allocation events have distinct addresses). The result is `{origin(a)}`, a single document.

*Cross-subspace I-span.* If `⟦σ⟧` spans positions in both the content subspace (`subspace_I = s_C`) and the link subspace (`subspace_I = s_L`) — say, `s` has element field beginning with `s_C` and `reach(σ)` has element field beginning beyond `s_L` — then `⟦σ⟧ ∩ dom(Σ.C)` automatically excludes the link addresses (by L0 of ASN-0047, `dom(L) ⊆ {a : subspace_I(a) = s_L}` and `dom(C) ⊆ {a : subspace_I(a) = s_C}`, and L14 gives `dom(C) ∩ dom(L) = ∅`). The lift's intersection with `dom(C)` therefore silently drops link addresses; no link origins appear in `origins_I`. This is a deliberate choice of the lift's definition: SHOWORIGIN over an I-span reports origins of content, not of links. (Reporting link origins is left as Open Question 1.)

*Empty document arrangement (V-span).* If `M(d) = ∅`, then every subspace projection `V_S(d)` is empty for every `S`. The precondition (iii) of the V-span operation — `V_{u₁}(d) ≠ ∅` — fails, so the operation is *not admissible* on empty documents. There is no V-span over which to query origin because no V-positions exist. (Compare with the I-span case, where empty intersection produces a well-formed empty result; in the V-span case, the precondition itself is unsatisfiable.) The asymmetry reflects that V-span queries are document-relative — there must be at least one V-position to fix a depth `m`, by S8-depth's vacuity on empty subspaces.

*Empty-restriction within a non-empty document (V-span).* If `M(d) ≠ ∅` and `V_{u₁}(d) ≠ ∅` (so precondition (iii) holds), but `⟦σ⟧ ∩ dom(M(d)) = ∅` — the well-formed V-span happens to cover no arranged V-positions — the postcondition expression evaluates to `∅`. This case is permitted: well-formedness requires every depth-`m` position in the span's range to be in `dom(M(d))` (precondition (vi)), so the intersection cannot be empty unless the span's range itself is empty under the depth-`m` constraint. Since `reach(σ) > u` by TA-strict and at least one depth-`m` position lies between them (the position `u` itself), this case does not arise when precondition (vi) is interpreted nontrivially. The intersection therefore inherits the nonemptiness of precondition (vi), and the result has at least one origin.

### Weakest precondition for single-origin output

We compute one wp characterising what SHOWORIGIN reveals about state. For the I-span operation:

> `wp(SHOWORIGIN_I(σ), |result| = 1) = (⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`.

*Derivation.* The postcondition `|result| = 1` says the result set is a singleton. (1) `|origins_I(Σ, σ)| = 1` iff (a) `origins_I(Σ, σ) ≠ ∅` and (b) all elements of `origins_I(Σ, σ)` are equal. (2) Non-emptiness `origins_I(Σ, σ) ≠ ∅` iff `⟦σ⟧ ∩ dom(C) ≠ ∅`: the result is the image of the intersection under `origin`, so the result is empty iff the intersection is empty (the image of the empty set is empty; the image of a non-empty set under a total function is non-empty). (3) All elements equal iff every pair shares a common value: `(A a, b : a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))`. (4) Conjoining: the wp is exactly the precondition that the intersection is non-empty and consists of addresses sharing a single origin. ∎

This wp is the exact characterisation of *single-origin spans*: any I-span whose allocated content lies wholly under one document's allocation prefix. Equivalently (by the partition O1), it is the precondition for `(⟦σ⟧ ∩ dom(C)) / ~_o` to be a one-element quotient.

A second wp characterises when a specific document is reported by SHOWORIGIN_V:

> `wp(SHOWORIGIN_V(d, σ), d_q ∈ result) = (E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)`.

That is, the precondition that some block of the resolution of `(d, σ)` is sourced from `d_q`. This delivers the operational use of SHOWORIGIN as a discovery probe: a reader who suspects that material from `d_q` is present in some region of `d`'s arrangement can confirm or refute by SHOWORIGIN's output.

## What SHOWORIGIN does not promise

The claims above bound what SHOWORIGIN guarantees. Three exclusions deserve explicit statement.

*Not historical containment.* SHOWORIGIN reports origin, not the set of documents that *have ever contained* the queried content. A document that once transcluded the content and then contracted its arrangement (`K.μ⁻`) is no longer represented by `M(d)` and does not appear in `origins_V`. Historical containment is recorded in the provenance relation `Σ.R` (foundation ASN-0047) and is a separate concern. Gregory's investigation of the spanfilade [Q17] confirms that the implementation's `find_documents_containing` mixes these two notions and returns a superset of currently-containing documents — a behaviour distinct from SHOWORIGIN.

*Not human authorship.* As Nelson notes [Q2], the User field of the tumbler identifies an owning *account*, not necessarily a known human. *John Doe publication* is permitted: anonymous and pseudonymous content has well-defined origin without revealing identity. SHOWORIGIN reports what the address structure encodes, and no more.

*Not transitive provenance.* SHOWORIGIN follows no chain. When `dₙ` transcludes from `d_{n-1}` which transcluded from `d_{n-2}`, etc., the result names `d₁` (the original allocator), not the chain `d₁ → d₂ → ... → dₙ`. Users who wish to see the chain of intermediate documents must perform a different operation — for instance, step pane-by-pane through each layer's arrangement [Q10]. SHOWORIGIN gives them the direct answer only.

## A worked example

We exhibit a scenario that exercises each of the claims in turn.

*Initial state Σ₀.* Document `d₁` allocates content at I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` containing the five characters of *Hello*. Document `d₂` arranges these five I-addresses at V-positions `[1,1,1]` through `[1,1,5]` in its own arrangement — a transclusion of the entire word, by reference. Document `d₃` similarly transcludes `d₂`'s arrangement of these positions, recording I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` at its own V-positions — note that `d₃`'s arrangement records the original I-addresses directly, not pointers to `d₂`'s arrangement.

A reader at `d₃` asks SHOWORIGIN over the V-span containing all five positions. The resolution yields one mapping block `(v_start, [d₁.0.1.1], 5)`. By O2, this block contributes one origin: `origin([d₁.0.1.1]) = d₁`. The answer is `{d₁}`. The intermediate document `d₂` does not appear — illustrating O4 (parallel witnesses): `d₂` and `d₃` each independently hold an arrangement entry mapping their own V-positions to the same I-address `[d₁.0.1.1]`, and either document could be queried with identical result.

*Transition Σ₀ → Σ₁ (allocation of native content in `d₃`).* `d₃` natively appends two new characters at V-positions `[1,1,6]` and `[1,1,7]`, allocated at `[d₃.0.1.1]` and `[d₃.0.1.2]` via K.α (ASN-0047) and arranged via K.μ⁺. A SHOWORIGIN over the full seven-position V-span returns two origins:

> `origins_V(Σ₁, d₃, σ_{1..7}) = { origin([d₁.0.1.1]), origin([d₃.0.1.1]) } = { d₁, d₃ }`.

Two mapping blocks, two origins. The block for the first five positions traces to `d₁`; the block for the last two traces to `d₃`. The multi-origin case is not a degenerate case — it is the expected case for any document of mixed authorship.

*Verifying O5 and O6 (permanence and growth).* Consider the I-address `[d₁.0.1.1]` itself, viewed across the transition Σ₀ → Σ₁: at Σ₀, `origin([d₁.0.1.1]) = d₁`; at Σ₁, the same projection on the same address still yields `d₁`. O5 holds pointwise. For the I-span lift, consider an I-span σ_{cover} containing all of `d₁`'s and `d₃`'s allocated content addresses:
- At Σ₀: `origins_I(Σ₀, σ_{cover}) = {d₁}` (only `d₁`'s addresses are allocated; `d₃` has none in this span yet).
- At Σ₁: `origins_I(Σ₁, σ_{cover}) = {d₁, d₃}` (after K.α, `d₃`'s two new addresses lie in σ_{cover}).

The inclusion `origins_I(Σ₀, σ_{cover}) ⊆ origins_I(Σ₁, σ_{cover})` holds (O6 verified): `{d₁} ⊆ {d₁, d₃}`. Allocation can only enlarge the set, never reduce or rewrite it.

*Transition Σ₁ → Σ₂ (arrangement contraction in `d₃`).* `d₃` contracts its arrangement via K.μ⁻ to retain only V-positions `[1,1,1]` through `[1,1,5]` (the transcluded `Hello`). The native suffix is removed from the arrangement; `dom(M(d₃))` shrinks. By P0 (ContentPermanence, ASN-0047), `[d₃.0.1.1]` and `[d₃.0.1.2]` remain in `dom(C)`, but they are no longer in `ran(M(d₃))`.

- For the I-span lift: `origins_I(Σ₂, σ_{cover}) = {d₁, d₃}` — unchanged from Σ₁, because P0 keeps the content store. O6 holds, and indeed the equality is tighter than the inclusion.
- For the V-span lift over `d₃`: at Σ₁, `origins_V(Σ₁, d₃, σ_{1..7}) = {d₁, d₃}`; at Σ₂, the seven-position V-span overshoots `dom(M(d₃))` — `⟦σ_{1..7}⟧ ∩ dom(M(d₃)) = {[1,1,1], ..., [1,1,5]}` (the remaining five) — so `origins_V(Σ₂, d₃, σ_{1..7}) = {d₁}`. The V-span lift is *not* monotonic under state transitions that contract arrangements; `d₃` itself drops out of the V-result although it remains an origin in the I-result. This illustrates the gap between O6 (I-span monotonicity) and the V-span case.

*Verifying O7 (V-span stability under fixed arrangement).* Now consider the smaller V-span σ_{1..5} over just the first five positions, across Σ₁ → Σ₂. The restriction `M(d₃) ↾ ⟦σ_{1..5}⟧` is `{[1,1,1] ↦ [d₁.0.1.1], ..., [1,1,5] ↦ [d₁.0.1.5]}` in both states (the K.μ⁻ removed only positions `[1,1,6]` and `[1,1,7]`, which lie outside `⟦σ_{1..5}⟧`). The frame condition of O7 holds, and accordingly `origins_V(Σ₁, d₃, σ_{1..5}) = origins_V(Σ₂, d₃, σ_{1..5}) = {d₁}`. The same V-positions, restricted to the same arrangement, produce the same origin set.

*Verifying O9 (origin tracks creation, not content).* Suppose a fourth document `d₄` independently allocates the same five characters of *Hello* at I-addresses `[d₄.0.1.1]` through `[d₄.0.1.5]`. By the K.α allocation rule (ASN-0047), `[d₁.0.1.1]` and `[d₄.0.1.1]` are distinct addresses despite `C([d₁.0.1.1]) = C([d₄.0.1.1]) = 'H'`. By S7a, `origin([d₁.0.1.1]) = d₁` and `origin([d₄.0.1.1]) = d₄`; by S7d, `d₁ ≠ d₄` at the tumbler level. SHOWORIGIN distinguishes them — the identical content values do not collapse the origins.

*Verifying O10 (idempotence).* At any of the states Σ₀, Σ₁, or Σ₂, two consecutive applications of SHOWORIGIN at the same input yield the same result, because the post-state equals the pre-state and the postcondition is a pure function of state and input. For instance, `SHOWORIGIN_V(Σ₂, d₃, σ_{1..5})` invoked twice in succession both yield `{d₁}` with no state change. There is no "first-query" effect.

## Summary

The abstract specification of SHOWORIGIN reduces to three primitives:

(1) The pointwise projection `origin : dom(C) → E_doc` (established in S7 of foundation ASN-0036), which is structural, total, and permanent.

(2) The lift to I-spans, `origins_I(Σ, σ) = origin(⟦σ⟧ ∩ dom(C))`, computable from the span and `dom(C)` alone.

(3) The lift to V-spans, `origins_V(Σ, d, σ) = origin(ran(M(d) ↾ ⟦σ⟧))`, computable from the span, the arrangement, and `dom(C)` alone.

Every other property — span union monotonicity, transclusion-depth invariance, permanence under state, immunity to source-document unreachability — follows from these three. The operation derives no new knowledge; it presents existing structural facts about the address space.

Any implementation of Xanadu that claims to support SHOWORIGIN must satisfy O1–O10 (with the O1 corollaries O1.1, O1.2). It may realise the operation through different mechanisms — direct tumbler-prefix decomposition, spanfilade lookup, granfilade traversal, or per-block `homedoc` records [Q12, Q13] — and these mechanisms may have different operational characteristics. But the abstract guarantees they deliver must coincide: every byte names its home, every span reveals its sources, and the answer never changes once given.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `origins_I(Σ, σ)` | `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }` — I-span lift of origin | introduced |
| `origins_V(Σ, d, σ)` | `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` — V-span lift via arrangement | introduced |
| O1 | Origin partitions allocated content: `~_o` is an equivalence on `⟦σ⟧ ∩ dom(C)` whose quotient is in bijection with `origins_I(Σ, σ)`; each class corresponds to one document's allocations | introduced |
| O1.1 | Single-origin sufficiency: confinement to one document's content yields `|origins_I| ≤ 1` (corollary of O1) | introduced |
| O1.2 | Multi-origin diagnostic: `|origins_I| > 1` ⇒ σ crosses ≥ 2 document allocation boundaries (corollary of O1) | introduced |
| O2 | Block uniformity: every I-address within a single mapping block shares one origin | introduced |
| O3 | Structural derivation: `origin(a)` and both lifts consult only the address (and, for V-span, the arrangement restricted to the span) | introduced |
| O4 | Parallel witnesses to a single origin: each intermediate document `d_i` (`2 ≤ i ≤ n`) independently records the same I-address `a`, and any can be queried with identical result `origin(a)` | introduced |
| O5 | Origin permanence: `origin(a)` is identical in every reachable state containing `a` | introduced |
| O6 | Monotonic growth under state: `origins_I` is non-decreasing as content is added | introduced |
| O7 | V-span stability under fixed arrangement: `origins_V` is unchanged when the arrangement restricted to the span is unchanged | introduced |
| O8 | Span union monotonicity: `⟦σ₁⟧ ⊆ ⟦σ₂⟧` ⇒ `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)` | introduced |
| O9 | Origin tracks creation, not content: two addresses allocated under distinct documents have distinct origins, regardless of content values | introduced |
| O10 | Read-only frame; idempotence: SHOWORIGIN preserves the state; consecutive applications at the same state yield identical results | introduced |
| `F1 ≡ F2 ≡ F3` | Equivalence chain for `origins_V`: reader-form `{origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d))}` ≡ decomposition-form `⋃_j {origin(aⱼ + i) : 0 ≤ i < nⱼ}` ≡ block-collapsed-form `{origin(aⱼ) : 1 ≤ j ≤ k}` | introduced |
| wp(SHOWORIGIN_I, \|result\| = 1) | `(⟦σ⟧ ∩ dom(C) ≠ ∅) ∧ (A a, b ∈ ⟦σ⟧ ∩ dom(C) : origin(a) = origin(b))` — characterisation of single-origin I-spans | introduced |
| wp(SHOWORIGIN_V, d_q ∈ result) | `(E v : v ∈ ⟦σ⟧ ∩ dom(M(d)) : origin(M(d)(v)) = d_q)` — characterisation of when a queried document appears in the V-span result | introduced |
| SHOWORIGIN (I-span) | Operation over a well-formed I-span (T12 conjuncts (i)–(iv)) returning `origins_I(Σ, σ)` with `Σ' = Σ` | introduced |
| SHOWORIGIN (V-span) | Operation over a well-formed content reference (ASN-0058 conjuncts (i)–(vi)) returning `origins_V(Σ, d, σ)` with `Σ' = Σ` | introduced |

## Open Questions

What must SHOWORIGIN guarantee when its input span crosses subspace boundaries (content addresses and link addresses both present in the I-stream range)?

When a span's content has been transcluded through several intermediate documents, must any abstract operation be provided that surfaces the intermediate chain, or is the direct origin answer sufficient?

Must SHOWORIGIN distinguish content that was natively allocated in a queried document from content transcluded into it, or is this distinction the responsibility of a separate operation?

What guarantee must hold for SHOWORIGIN when the home document's I-addresses are no longer reachable for byte-fetching, but the address itself remains well-formed?

Does the system require a complementary operation reporting historical containment (from `Σ.R`) distinct from current arrangement origins, and what invariants must couple the two?

When multiple V-positions in a single arrangement map to the same I-address (intra-document sharing per S5 of ASN-0036), what must SHOWORIGIN report at each position?
