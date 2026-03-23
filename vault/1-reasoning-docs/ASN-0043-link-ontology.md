# ASN-0043: Link Ontology

*2026-03-16*

The two-space model (ASN-0036) established two state components: the content store `Σ.C` — an immutable, append-only mapping from I-addresses to values — and the arrangements `Σ.M(d)` — mutable mappings from V-positions to I-addresses, one per document. Together these give us content: its existence, its identity, and its presentation.

But the docuverse is not merely a store of content. Nelson:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

We are looking for the second primitive. Content is substance; what is the nature of connection? We seek the minimum structure that a connection between arbitrary spans of tumbler addresses must have, and the properties that such connections must satisfy.


## Why Connections Need Identity

We begin with a guarantee: the system must support connections between arbitrary spans of content. What must such a connection be?

First, connections must be *distinguishable*. If Alice asserts that paragraph P is a commentary on paragraph Q, and Bob independently makes the same assertion, these are two assertions, not one. Two connections between identical content must coexist as separate objects. Nelson confirms this forcefully: MAKELINK "always creates and always returns a fresh ID" — there is no find-or-create. Gregory's implementation confirms: each call to `docreatelink` allocates a new sequential address; there is no deduplication, no uniqueness constraint, no identity-by-endset.

Second, connections must be *owned*. Alice's annotation is hers; Bob's is his. The system must record who made each connection, independently of what it connects. Nelson: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to."

Third, connections should be *referenceable*. One connection should be able to point to another, enabling compound relational structures. Nelson: links to links "use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links."

These three requirements — distinguishability, ownership, referenceability — force connections to be first-class addressed objects in the tumbler space. A connection that lacked its own address could not be distinguished from another connection with the same endpoints, could not be independently owned, and could not be pointed to by other connections. We are compelled to give connections their own permanent tumbler addresses.

We call these addressed connections *links*.


## The Link Store

We introduce the third component of the system state:

**Definition — LinkStore.** `Σ.L : T ⇀ Link` is the *link store*, a partial function mapping tumbler addresses to link values. The domain `dom(Σ.L)` is the set of addresses at which links have been created. We specify the type `Link` below.

The full system state is now:

`Σ = (Σ.C, Σ.M, Σ.L)`

where `Σ.C` is the content store (ASN-0036), `Σ.M` is the family of arrangements (ASN-0036), and `Σ.L` is the link store (this ASN).


## Subspace Residence

Links share the tumbler space `T` with content, but they must be categorically distinguishable from content. A link is not a piece of text. It is a relational assertion *about* text — what Nelson calls a "meta-virtual structure connecting parts of documents (which are themselves virtual structures)." The address space provides a natural mechanism for this categorical distinction: subspace separation.

Recall from ASN-0034 (T4, HierarchicalParsing) that every element-level tumbler has the form `N.0.U.0.D.0.E`, where `E` is the element field, and the first component `E₁` is the subspace identifier. By T7 (SubspaceDisjointness), tumblers with different subspace identifiers are permanently distinct — no address in subspace `s₁` can equal or be confused with an address in subspace `s₂ ≠ s₁`.

The system designates at least two subspaces within each document's element field: one for content, one for links. Let `s_C` and `s_L` be the subspace identifiers for content and links respectively, with `s_C ≠ s_L`.

**L0 — SubspacePartition.** Every link address has subspace identifier `s_L`, and every content address has subspace identifier `s_C`:

`(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

`(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

By T7, this yields the fundamental disjointness:

`dom(Σ.L) ∩ dom(Σ.C) = ∅`

Links and content cannot share an address. They are peers in the tumbler space — both first-class, both permanent, both addressable — but they are different kinds of entity occupying different regions. Gregory confirms this at the implementation level: the granfilade has exactly two leaf types (`GRANTEXT = 1` and `GRANORGL = 2`), distinguished by an `infotype` discriminator in the bottom crum. Content stores byte sequences; links store pointers to nested enfilades encoding the endset structure. Runtime predicates (`istextcrum`, `islinkcrum`) explicitly test for and separate these two categories.

**L1 — LinkElementLevel.** Every link address is an element-level tumbler:

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

This parallels S7b for content (ASN-0036). A link address carries all four tumbler fields (node, user, document, element), enabling the same structural attribution that content addresses enjoy. Gregory confirms: link addresses are allocated by `findisatoinsertmolecule` with the `LINKATOM` hint, producing full element-level tumblers.

**L1a — LinkScopedAllocation.** Every link address is allocated under the tumbler prefix of the document whose owner created it:

`(A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)`

This parallels S7a (DocumentScopedAllocation, ASN-0036) for content. Gregory confirms: `docreatelink` allocates the link address within the creating document's address space via `findisatoinsertmolecule`, which extends the document's I-stream. The allocation prefix is determined by the document parameter, not by the endsets — a link whose endsets reference entirely foreign content is still allocated under the creating document's prefix.


## Home and Ownership

Because link addresses are element-level tumblers (L1) allocated under their creating document's prefix (L1a), the `origin` function from ASN-0036 applies directly.

**Definition — LinkHome.** For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

**GlobalUniqueness.** No two allocation events anywhere in the system produce the same address. S4 (OriginBasedIdentity, ASN-0036) establishes this for I-addresses (content store addresses). The underlying derivation — from T9 (ForwardAllocation), T10 (PartitionIndependence), and T10a + TA5(d) + T3 (ASN-0034) — depends only on tumbler algebra, not on any property specific to the content store. The same three cases (same-allocator distinctness via T9, non-nesting cross-allocator distinctness via T10, nesting-prefix cross-allocator distinctness via T10a + TA5(d) + T3) apply to any element-level tumbler produced by the allocation discipline, including link-subspace allocations.

The home document determines the link's owner. This is not metadata attached to the link — it IS the link's address, read through the field structure. By L1a, the document-level prefix of `a` identifies the document whose owner created the link; by L1 and T4 (HierarchicalParsing, ASN-0034), the prefix is recoverable from the address alone. Together these yield the link analog of S7 (StructuralAttribution, ASN-0036): `home(a)` uniquely identifies the creating document across the system (by the same three cases as S7's derivation — T9, T10, and T10a + TA5(d) + T3, ASN-0034 — with L1a replacing S7a and L1 replacing S7b), and this identification is structural — embedded in the address, not attached as metadata.

The critical property — the one that distinguishes this design from systems where annotations are embedded in the annotated content:

**L2 — OwnershipEndsetIndependence.** The home document of a link is determined entirely by the link's address and is independent of the link's endsets:

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

Nelson makes this a first principle: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." This separation of residence from reference is what permits annotation without modification. Your link lives in your document, under your authority, even though its endsets reach into someone else's content. The annotated document is untouched — no byte added, no structure modified, no permission required.


## The Endset Structure

What internal structure must a link have? We seek the minimal structure sufficient for typed, directional connections between arbitrary spans.

A connection has at least two sides — a *source* and a *target*. Without two sides there is no connection. Gregory confirms this minimum in the code: the internal function `domakelink` takes only two endsets (`fromspecset` and `tospecset`), and the insertion functions (`insertendsetsinspanf`, `insertendsetsinorgl`) treat the from and to endsets as mandatory while the third is conditional. Two endsets are the structural floor.

But two sides alone do not suffice. We need to distinguish a citation from a comment from a refutation. If all links are structurally uniform two-endset connections, one cannot ask "find all citations" without also retrieving every comment and footnote. Classification is required.

Nelson's design resolves this not by adding a metadata field — a type tag bolted onto a binary link — but by adding a *third endset*, structurally identical to the first two, pointing into the address space. This achieves three things simultaneously:

1. **Extensibility.** Any user can define new types by choosing new addresses, without schema changes. Nelson: "The set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose."

2. **Uniformity.** All endsets have the same representation — a set of spans in the tumbler space. The link is a homogeneous sequence, not a pair-plus-metadata.

3. **Hierarchical classification.** Because tumbler containment is decidable (T6, ASN-0034), type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering. A query matching `p` matches both (by T5, ContiguousSubtrees).

But Nelson's design does not stop at three. He explicitly lists support for higher-arity links as a desired feature: "4-sets, 5-sets ... n-sets supported in link storage and search" [LM 4/79]. The three-endset case — from, to, type — is the standard convention, not a structural ceiling. A faceted link relating content across more than three roles need not be decomposed into chains of ternary links; it can be expressed directly as a single link with the required number of endsets.

We now define the components.

**Definition — Endset.** An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefinedness, ASN-0034): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset — a link may have an endset that references nothing.

**Definition — Link.** A *link value* is a finite sequence of N ≥ 2 endsets:

`Link = {(e₁, e₂, ..., eₙ) : N ≥ 2, each eᵢ ∈ Endset}`

We write `|L|` for the *arity* of a link — the number of endsets in the sequence.

**Convention — StandardTriple.** The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. We write `(F, G, Θ)` for a link following this convention. Nelson's MAKELINK operation takes these three endsets plus a home document, and Gregory's implementation hardcodes three V-addresses (1.1, 2.1, 3.1) and three spanfilade index constants (`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). The standard triple is the dominant case — but it is a convention, not a structural limit.

**L3 — NEndsetStructure.** Every link in the link store is a sequence of at least two endsets:

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 2 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset))`

Nelson [LM 4/79] explicitly calls for N-endset support: "4-sets, 5-sets ... n-sets supported in link storage and search." Gregory's implementation fixes N = 3 — the V-subspace assignment function `setlinkvsas` hardcodes three V-addresses, the query function `intersectlinksets` takes exactly three input lists, and the wire protocol (`FINDLINKSFROMTOTHREE`) encodes three endset parameters. The integer namespace for a fourth endset type is already consumed (`DOCISPAN = 4`), blocking extension without renumbering. This reflects the implementation convention (StandardTriple), not a principled design boundary. The design commitment is to the sequence structure itself — a link carries as many endsets as its relational role requires, with three as the standard convention.


## Endset Properties

Each endset is a set of spans — potentially multiple, potentially discontiguous, potentially spanning multiple documents. Nelson:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse."

We now state the properties that endsets must satisfy.

**L4 — EndsetGenerality.** The spans within an endset may reference any addresses in the tumbler space. There is no constraint confining spans to a single document, to content addresses only, or to addresses at which content currently exists.

The formal content follows from definitions: by L3, every link value is a sequence of endsets of type `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed pairs satisfying T12. Therefore:

`(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)|, (s, ℓ) ∈ Σ.L(a).eᵢ :: s ∈ T ∧ (s, ℓ) satisfies T12)`

The substantive content of L4 is not what the types require, but what they *omit* — the design-significant absence of additional constraints beyond T12. The following sub-items make explicit what the model does NOT restrict:

(a) *Cross-document endsets.* A single endset may contain spans whose start addresses fall under different document-level prefixes. Gregory confirms: the sporglset data structure stores one `sporgladdress` per span entry, and the conversion function `specset2sporglset` iterates over specset elements with different `docisa` values without rejection. A link whose from-endset touches passages in three different documents is a single link with a single multi-span endset, not three separate links.

(b) *Intra-document links.* Nothing prevents a link's endsets from referencing content within the link's own home document. Nelson: "links connecting parts of a document need not reside in that document" — the converse, that they *may* reside in the document they connect, is equally valid. Heading links, paragraph markers, and footnote links are standard examples of intra-document connections.

(c) *Cross-subspace endsets.* Endset spans may reference addresses in the link subspace — that is, addresses of other links. This is L4's most consequential implication; we develop it fully under Reflexive Addressing below.

**L5 — EndsetSetSemantics.** An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning. Only membership matters:

`(A a ∈ dom(Σ.L), e :: Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e})`

Gregory confirms exhaustively. During storage, spans receive sequential V-addresses within the link's own permutation matrix (an artifact of linked-list traversal order). Upon retrieval, spans come back ordered by I-address value, not by insertion sequence — the original ordering is not preserved or recoverable. No code path in the implementation treats any span as "primary" or consults positional index within an endset. All link-finding (`sporglset2linksetinrange`) and intersection (`intersectlinksets`) operations iterate uniformly, comparing addresses by value without regard to position. A planned `consolidatespanset` function — which might have imposed normalization — was never implemented.

**Definition — Coverage.** For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

This is the set of all tumbler addresses referenced by the endset. Note that coverage is a lossy projection: two endsets with different span decompositions may have identical coverage. For instance, `{(1, [3])}` and `{(1, [1]), (2, [2])}` cover the same addresses but are distinct endsets — they contain different spans, and by L5 (which collapses only reorderings of the same span collection, not distinct collections) they are not equal. Coverage tells us *which addresses* an endset references, abstracting away the particular decomposition into spans, but it does not determine endset identity.


## Slot Distinction and Directionality

Although all endsets within a link are structurally identical (all are elements of `Endset`), they are not interchangeable. Each endset occupies a distinguished position — its slot index — and search can constrain on each slot independently.

**L6 — SlotDistinction.** The endsets within a link occupy structurally distinguished positions. A link is a sequence — permuting endset slots produces a different link value when the permuted entries differ. For the standard triple:

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

Gregory's implementation encodes this distinction at two independent levels: in the link's own permutation matrix (V-addresses 1.1, 2.1, 3.1 for from, to, and type) and in the spanfilade index (ORGL-range prefixes `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). A query for "links from span A" and a query for "links to span A" search different index columns and may return different results.

But the slot distinction is *structural*, not *semantic*. Whether "from" means "source" and "to" means "destination" is not determined by any invariant of the link structure:

**L7 — DirectionalFlexibility.** The invariants L0–L14 impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

Nelson: "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" The word "typically" is deliberate. A citation link is directional — it goes *from* citing text *to* cited source. A counterpart link marking equivalence has no meaningful direction. A heading link populates only one content endset — Nelson calls it "inane" to label that one endset "from." The structure provides two slots; the type defines whether the distinction carries directional weight.

The consequence: any system that determines a link's directionality from slot position alone — treating "from" as inherently "source" and "to" as inherently "target" without consulting the type — is misinterpreting the design. The slots provide structural asymmetry sufficient for indexing and query; the type provides semantic interpretation.

Despite the slot distinction, access is symmetric. The system must support retrieving any endset of any link with equal facility. Gregory confirms: the `followlink` operation takes a `whichend` parameter (1, 2, or 3) and calls `link2sporglset` with a V-range query parameterized by that integer. The retrieval path is identical for all slots — no endset is privileged or hidden.


## The Type Endset

The type endset deserves extended treatment. It is structurally an endset — a finite set of spans — but its role is semantic classification, and it has distinctive properties that follow from that role.

**L8 — TypeByAddress.** For links following the standard triple convention (`|Σ.L(a)| ≥ 3`), type matching is by *address identity*, not by content at the address. Whether two links share the same type is determined by whether their type endsets reference the same addresses, not by what is stored at those addresses:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

Nelson: "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

This is a profound design choice. It decouples classification from content retrieval entirely. A search for "all links of type X" never fetches the bytes at address X — it only matches the address. This means:

**L9 — TypeGhostPermission.** For links following the standard triple convention: ghost types are permitted. For any conforming state `Σ` satisfying L0–L14 and S0–S3, there exists a conforming state `Σ'` extending `Σ` with a standard-triple link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)))`

*Witness.* Take any conforming `Σ`. Let `d` be a document with an allocator for subspace `s_L`. Choose a fresh ghost address `g ∈ T` with `fields(g).E₁ = s_C` and `g ∉ dom(Σ.C)` (such an address exists: by S7a, every address in `dom(Σ.C)` is allocated under some document's prefix; by T9, allocation within each document's content subspace is strictly increasing; by T0(a), components are unbounded — so a content-subspace address beyond the allocation frontier of every document is always available). Allocate a new link address `a` via forward allocation (T9) within `d`'s link subspace. Define `Σ'` as `Σ` extended with `Σ'.L(a) = (∅, ∅, {(g, δ(1, #g))})`, and `Σ'.C = Σ.C`, `Σ'.M = Σ.M`.

We verify that `Σ'` is conforming:

- *L0 (SubspacePartition).* The address `a` is allocated in `d`'s link subspace, so `fields(a).E₁ = s_L`. Since `s_L ≠ s_C`, `a ∉ dom(Σ'.C) = dom(Σ.C)`, preserving disjointness.
- *L1 (LinkElementLevel).* The address `a` is an element-level tumbler by construction: allocated under a document prefix with all four fields, giving `zeros(a) = 3`.
- *L1a (LinkScopedAllocation).* The address `a` is allocated under `d`'s prefix by construction: `origin(a) = d`.
- *L3–L5.* The type span `(g, δ(1, #g))` is well-formed by T12; the endset sequence `(∅, ∅, {(g, δ(1, #g))})` has arity 3 ≥ 2, satisfying L3. Empty endsets are valid by the definition of Endset. L5 holds trivially.
- *L11a (LinkUniqueness).* By GlobalUniqueness, the freshly allocated `a` is distinct from every address in `dom(Σ.L)`.
- *L12 (LinkImmutability).* For every `b ∈ dom(Σ.L)`: `b ∈ dom(Σ'.L)` and `Σ'.L(b) = Σ.L(b)`, since `Σ'` only adds the new entry at `a`.
- *L14 (DualPrimitive).* `dom(Σ'.C) ∪ dom(Σ'.L) = dom(Σ.C) ∪ (dom(Σ.L) ∪ {a})`. Disjointness holds since `a` is in subspace `s_L` and `dom(Σ'.C) ⊆ s_C`.
- *S0–S3.* Content store and arrangements are unchanged (`Σ'.C = Σ.C`, `Σ'.M = Σ.M`), so all ASN-0036 invariants carry over from `Σ`.
- *Remaining properties.* L2 holds structurally (home is field extraction from the address); L6 vacuously (F = G = ∅ makes the antecedent false); L8, L10, L13 are lemmas that do not constrain states; L12a follows from L12.

No property of L0–L14 or S0–S3 constrains `coverage(Σ'.L(a).type) ⊆ dom(Σ'.C)`. Now, `Σ'.C = Σ.C`, so `g ∉ dom(Σ.C) = dom(Σ'.C)`. And `fields(g).E₁ = s_C` while every address in `dom(Σ'.L)` has subspace `s_L` by L0; since `s_C ≠ s_L`, T7 gives `g ∉ dom(Σ'.L)`. Therefore `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`. ∎

No property of L0–L14 constrains type endset targets to content addresses. Nelson: "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." The type address is a pure name — a position chosen by convention, not a pointer to content that must be dereferenced.

A consequence of L8 and L9 together: new link types can be defined by choosing a fresh tumbler address and using it as a type endset. No content needs to be created at that address. No registry needs to be updated. No schema needs to change. The type exists as soon as someone uses it. This is what makes the type system "open-ended" — any user can extend it without coordination or system modification.

**Lemma — PrefixSpanCoverage.** For any tumbler `x` with `#x ≥ 1`, `δ(1, #x)` (OrdinalDisplacement, ASN-0034) is the displacement `[0, ..., 0, 1]` of length `#x`, with action point `k = #x`. The span `(x, δ(1, #x))` is well-formed by T12: `δ(1, #x) > 0` and `k ≤ #x`. By OrdinalShift (ASN-0034), `x ⊕ δ(1, #x) = shift(x, 1) = [x₁, ..., x_{#x-1}, x_{#x} + 1]`. Then:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

*Inclusion* (`{t : x ≼ t} ⊆ coverage`): let `c` extend `x`, so `x ≼ c`. By T1(ii), `c ≥ x`. Since `c` agrees with `x` at all positions `1` through `#x`, we have `c_{#x} = x_{#x} < x_{#x} + 1 = shift(x, 1)_{#x}`, giving `c < shift(x, 1)` by T1(i). Therefore `c ∈ [x, shift(x, 1))`.

*Exclusion* (`coverage ⊆ {t : x ≼ t}`): we show that every `t ∈ [x, shift(x, 1))` with `t ≠ x` must extend `x`, by case analysis on depth.

- *Same depth* (`#t = #x`): since `t ≠ x`, let `j` be the least position `≤ #x` with `t_j ≠ x_j` — that is, `j = divergence(t, x)`. As `t > x`, T1(i) gives `t_j > x_j`. Since `shift(x, 1)` agrees with `x` at all positions before `#x`, if `j < #x` then `t_j > x_j = shift(x, 1)_j`, giving `t > shift(x, 1)` — outside the interval. If `j = #x`, then `t_{#x} ≥ x_{#x} + 1 = shift(x, 1)_{#x}`, giving `t ≥ shift(x, 1)` — outside the interval. Only `x` itself survives at this depth, and `x ≼ x` holds trivially.
- *Greater depth* (`#t > #x`): if `t` does not extend `x`, let `j` be the least position `≤ #x` with `t_j ≠ x_j` — that is, `j = divergence(t, x)`. As `t > x`, T1(i) gives `t_j > x_j`. If `j < #x`: `t_j > x_j = shift(x, 1)_j`, giving `t > shift(x, 1)` by T1(i). If `j = #x`: `t_{#x} ≥ x_{#x} + 1 = shift(x, 1)_{#x}`. When strict: `t > shift(x, 1)` by T1(i). When equal: `t` agrees with `shift(x, 1)` at all `#x` positions and `#t > #x = #shift(x, 1)`, so `shift(x, 1)` is a proper prefix of `t`, giving `shift(x, 1) < t` by T1(ii). Either way `t ≥ shift(x, 1)` — outside the interval. Only extensions of `x` remain.
- *Shorter depth* (`#t < #x`): if `t` agrees with `x` at all positions `1..#t`, then `x` extends `t`, so `t < x` by T1(ii) — contradicting `t ≥ x`. If `t` diverges from `x`, let `j` be the least position `≤ #t` with `t_j ≠ x_j` — that is, `j = divergence(t, x)`. Since `t > x`, T1(i) gives `t_j > x_j = shift(x, 1)_j` (as `j < #x`), giving `t > shift(x, 1)` — outside the interval.

The unit-depth span at `x` covers all and only extensions of `x`, with no extraneous tumblers. ∎

**L10 — TypeHierarchyByContainment.** For type addresses `p, c ∈ T` where `p ≼ c` (p is a prefix of c), define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

A single span query rooted at `p` matches all and only subtypes of `p`. The exclusion direction is essential: without it, a span query at `p` that also matched non-subtypes would not give a clean type hierarchy.

Gregory documents this in the bootstrap document's type registry: `MARGIN` at address `1.0.2.6.2` is hierarchically nested under `FOOTNOTE` at `1.0.2.6`. A query for all footnote-family links, expressed as a span query rooted at `1.0.2.6`, matches both types because `1.0.2.6.2` lies within `[1.0.2.6, 1.0.2.7)`. The subtyping mechanism is the tumbler ordering itself — no separate hierarchy data structure is needed.

We observe that L10 characterizes the structural affordance that the address space provides for type hierarchies. Whether a conforming system must implement subtype-aware query operations, or whether subtype matching is the caller's responsibility, is a question about the query interface — outside this ASN's scope.


## Link Distinctness and Permanence

We now establish the identity semantics of links. The three requirements we began with — distinguishability, ownership, referenceability — crystallize into two derived properties.

**L11a — LinkUniqueness.** Link addresses are produced by forward allocation (T9, ASN-0034) within the link subspace. By GlobalUniqueness, no two allocation events anywhere in the system produce the same address. Therefore every link has a globally unique, permanent identity, and the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

**L11b — NonInjectivity.** The link store imposes no injectivity constraint — multiple addresses may store the same endset sequence:

`(A Σ satisfying L0–L14, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies L0–L14))`

That is, for any conforming state `Σ` with a link at `a ∈ dom(Σ.L)` where `Σ.L(a) = (F, G, Θ)`, there exists a conforming extension `Σ'` with a fresh address `a' ∈ dom(Σ'.L)`, `a' ≠ a`, and `Σ'.L(a') = (F, G, Θ)`. The invariants *permit* non-injectivity — every state with a link can be extended to a non-injective state — but they do not *require* it. The witness is immediate: allocate `a'` by forward allocation within the same document's link subspace, and set `Σ'.L(a') = (F, G, Θ)` with `Σ'.C = Σ.C` and `Σ'.M = Σ.M`. All invariants L0–L14 are preserved: L0 by subspace (`a'` is in `s_L`); L1/L1a by allocation; L2 structurally (home is field extraction from the address); L3–L5 by construction (same endset sequence as the existing link); L6 because the new entry copies the same sequence, preserving slot distinction; L11a uniqueness for `a'` by GlobalUniqueness; L12 because existing entries are unchanged; L12a follows from L12; L14 because `a'` is in subspace `s_L`, preserving disjointness with `dom(Σ'.C)`; L8, L10, L13 are lemmas that do not constrain states; S0–S3 hold trivially since `Σ'.C = Σ.C` and `Σ'.M = Σ.M`.

Two links with identical endsets — same from, same to, same type — but different addresses are separate objects, independently owned, independently removable, independently targetable by other links.

**L12 — LinkImmutability.** Once created, a link's address persists and its value is permanently fixed:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`. This parallels S0 (ContentImmutability, ASN-0036) in both halves: the address endures, and the value at that address — the triple of endsets — never changes.

The evidence is unambiguous. Nelson's FEBE protocol defines exactly five link operations: MAKELINK (create), FINDLINKSFROMTOTHREE (search), FINDNUMOFLINKSFROMTOTHREE (count), FINDNEXTNLINKSFROMTOTHREE (paginate), and RETRIEVEENDSETS (read). There is no MODIFYLINK, UPDATELINK, or EDITENDSETS. The only write operation is creation; the rest are queries. Gregory confirms at the implementation level: `insertendsetsinorgl` and `insertendsetsinspanf` are called exclusively from `docreatelink`; no other code path writes to the link's orgl or spanfilade entries. The link orgl is written once by `createorglingranf` and never touched again.

Link immutability follows from the same principle that makes content immutable: others may have linked to it. Since links are first-class objects with tumbler addresses, other links can point to them (L13). Modifying a link's endsets after creation would silently change the meaning of every meta-link pointing to it — violating the permanence guarantee. To effectively change a connection, the owner creates a new link via MAKELINK with the desired endsets. The old link persists in `Σ.L` by L12; the new link gets a fresh address in creation order. The mechanism by which the old link ceases to be discoverable — whether through an arrangement-layer operation analogous to content deletion, or through some other visibility mechanism — is outside this ASN's scope. (Gregory's implementation reveals that links do occupy V-positions in a dedicated subspace of the document's permutation matrix, and that `deletevspan` removes only the POOM entry while leaving the link's own orgl and spanfilade entries intact — the link remains permanently discoverable through index traversal even after removal from the document's arrangement. Accommodating this in the abstract model would require extending the arrangement semantics beyond S3, which restricts `Σ.M(d)` to content addresses.)

Note what L12 does not address. Whether a link remains *discoverable* through indexing, whether its endsets remain *resolvable* to visible content, and what it means for a link to be "removed" while its address and value persist — these are questions about operations and their effects, outside this ASN's scope.

**L12a — LinkStoreMonotonicity.** The domain of the link store is monotonically non-decreasing:

`[dom(Σ.L) ⊆ dom(Σ'.L)]`

for every state transition `Σ → Σ'`. This is the direct corollary of L12, paralleling S1 (StoreMonotonicity) for the content store.


## Reflexive Addressing

Because links have tumbler addresses (L0, L1), and endsets can reference any tumbler address (L4), endsets can reference link addresses. This enables *link-to-link* connections — a link whose endset points at another link's address.

**L13 — ReflexiveAddressing.** Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`, `b` is an element-level tumbler by L1, so `#b ≥ 1` and PrefixSpanCoverage applies. The unit-depth span `(b, δ(1, #b))` is well-formed, and:

`coverage({(b, δ(1, #b))}) = {t ∈ T : b ≼ t}`

The canonical span contains exactly the target entity and its extensions, with no extraneous tumblers. More generally, an endset *references* an entity at address `a` when `a ∈ coverage(e)`, and `(b, δ(1, #b))` is the canonical span for referencing the entity at `b`.

Nelson: "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several). The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only."

Nelson's "span of 1" is the informal rendering of `δ(1, #b)`: advance by 1 at the depth of the target address.

Gregory confirms at the implementation level that this is not merely theoretically possible but architecturally unavoidable. The type `typeisa` is `typedef tumbler typeisa` — a bare tumbler with no type discriminant. The endset conversion functions (`specset2sporglset`, `vspanset2sporglset`) accept any tumbler address without checking whether it refers to content or to a link. The insertion functions (`insertspanf`, `insertpm`) store whatever `sporgladdress` they receive, with no type validation. The retrieval function (`findorgl`) resolves any address that maps to a valid granfilade entry, regardless of its atom type. There is no code, at any layer, that draws a boundary between "addressable objects" and "non-addressable objects."

From L13, arbitrary relational structures can be composed:

> "Complex relational structures, such as the faceted link, may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links."

The three-endset link plays the same role for structured connections that the cons cell plays for structured data: a universal building block from which compound forms of arbitrary complexity are assembled. A faceted link — one that relates multiple distinct groups of spans in more than three roles — is built from a chain of links, each contributing its three endset slots, with link-to-link references providing the composition glue.


## The Dual-Primitive Architecture

We can now state the architectural consequence that unifies the preceding properties. The docuverse is built from exactly two kinds of stored entity:

**L14 — DualPrimitive.** The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses — they relate V-positions to I-addresses — but V-positions are not entities in their own right. The two domains are disjoint:

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Nelson: "In the present implementation, the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." Documents, accounts, servers, and nodes are organizational concepts — positions in the tumbler hierarchy that structure the address space — but they have no stored representation. Only content and links occupy storage.

Gregory confirms with emphasis: the granfilade's union type has exactly two variants (`GRANTEXT` and `GRANORGL`), the hint mechanism accepts exactly two atom types (`TEXTATOM = 1` and `LINKATOM = 2`), and the Vstream within each document is partitioned into exactly two regions (text at `1.x`, links at `2.x`). No third category exists.

The two primitives are peers. Both have permanent tumbler addresses. Both are stored in the same master index (the granfilade). Both support the same addressing and containment mechanisms. But they are categorically different:

| | Content | Links |
|---|---|---|
| State component | `Σ.C : T ⇀ Val` | `Σ.L : T ⇀ Link` |
| Subspace | `s_C` | `s_L` |
| Payload | Opaque values (bytes) | Structured endset sequences (N ≥ 2; standard triple by convention) |
| Sharing | Transcludable — same I-address in multiple arrangements (S5) | Non-transcludable — S3 requires `M(d)(v) ∈ dom(Σ.C)`, and L0 gives `dom(Σ.L) ∩ dom(Σ.C) = ∅` |
| Address determines | Content origin (S7) | Link home and owner (L2) |

Content identity is *shareable*: the same I-address can appear in the arrangements of multiple documents via transclusion, and this sharing is the mechanism for content reuse (S5, ASN-0036). Link identity is *unique*: each link has exactly one address, and there is no mechanism to make two documents "share" the same link. We can derive this from two properties already established. First, S3 (ReferentialIntegrity, ASN-0036) requires that every V-mapping points to a content address: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`. Second, L0 establishes `dom(Σ.L) ∩ dom(Σ.C) = ∅`. Together these entail that no arrangement can map a V-position to a link address — the transclusion mechanism (multiple arrangements referencing the same I-address) cannot apply to links. A link at address `a` is homed in `home(a)` and owned by the principal of `home(a)` — period. It cannot be transcluded into another owner's authority.

This asymmetry is deliberate. Content wants to be shared — that is the point of transclusion. But a connection is an assertion by a specific principal about specific content, and assertions are not transferable by reference.


## Summary of the Link Model

A link is an addressed, owned, typed, bidirectional connection between arbitrary spans of content in the tumbler space. More precisely:

A link at address `a ∈ dom(Σ.L)` is characterized by:

- **Address** `a` — a permanent, globally unique element-level tumbler in the link subspace (L0, L1, L11a, L12). The address IS the link's identity.
- **Home** `home(a) = origin(a)` — the document under whose prefix `a` falls, determining the link's owner, independent of what the link connects (L2).
- **N ≥ 2 endsets** — each link carries at least two endsets (L3). The standard triple convention `Σ.L(a) = (F, G, Θ)` — from-endset `F`, to-endset `G`, and type-endset `Θ` — is the dominant form; each endset is a finite set of well-formed spans pointing anywhere in the tumbler space (L4, L5).
- **Slot structure** — endsets occupy structurally distinguished positions, enabling independent query on each, with directional semantics determined by the type rather than by the slot itself (L6, L7).
- **Type semantics** — the type endset is matched by address, not by content; it may reference ghost addresses; and hierarchical type relationships follow from tumbler containment (L8, L9, L10).


## Worked Example

We construct a minimal conforming state to verify that L0–L14 hold simultaneously.

**Setup.** Node 1, user 1, document 1. The content subspace identifier is `s_C = 1` and the link subspace identifier is `s_L = 2`.

Content addresses have element field starting with 1; link addresses have element field starting with 2. The document prefix is `1.0.1.0.1`.

**Content store.** Two content characters at addresses:

- `c₁ = 1.0.1.0.1.0.1.1` — first character, element field `1.1`
- `c₂ = 1.0.1.0.1.0.1.2` — second character, element field `1.2`

So `Σ.C = {c₁ ↦ v₁, c₂ ↦ v₂}` for some values `v₁, v₂ ∈ Val`.

**Arrangement.** One document `d = 1.0.1.0.1` with `Σ.M(d) = {[1.1] ↦ c₁, [1.2] ↦ c₂}` (V-positions are element-field tumblers within the document).

**Link store.** One link — a citation from `c₁` to `c₂` with a ghost type — at address:

- `a = 1.0.1.0.1.0.2.1` — element field `2.1` (subspace 2, ordinal 1)

Choose a ghost type address `g = 1.0.2.0.1.0.1.1` (a content address in a different document — one at which nothing is stored). Define:

All addresses here have depth 8, so the unit-depth displacement is `δ(1, 8) = [0, 0, 0, 0, 0, 0, 0, 1]`.

- From-endset: `F = {(c₁, δ(1, 8))}` (action point `k = 8 = #c₁`, unit width)
- To-endset: `G = {(c₂, δ(1, 8))}`
- Type-endset: `Θ = {(g, δ(1, 8))}`

So `Σ.L = {a ↦ (F, G, Θ)}`.

**Verification.**

*L0 (SubspacePartition).* `fields(a).E₁ = 2 = s_L`. `fields(c₁).E₁ = fields(c₂).E₁ = 1 = s_C`. Since `s_L ≠ s_C`, we have `dom(Σ.L) ∩ dom(Σ.C) = {a} ∩ {c₁, c₂} = ∅`. ✓

*L1 (LinkElementLevel).* `zeros(a) = zeros(1.0.1.0.1.0.2.1) = 3`. ✓

*L1a (LinkScopedAllocation).* `origin(a) = 1.0.1.0.1 = d`, the creating document. ✓

*L2 (OwnershipEndsetIndependence).* `home(a) = origin(a) = 1.0.1.0.1`, computed from the field structure of `a` alone. The endsets `(F, G, Θ)` are not consulted. ✓

*L3 (NEndsetStructure).* `|Σ.L(a)| = 3 ≥ 2`, and each endset is in `𝒫_fin(Span)`. ✓

*L4 (EndsetGenerality).* Each span is well-formed by T12: for `(c₁, δ(1, 8))`, `δ(1, 8) > 0` and the action point `k = 8 ≤ #c₁ = 8`. Similarly for the other spans. Start addresses are in `T`. ✓

*L5 (EndsetSetSemantics).* Each endset is a singleton set — set semantics hold trivially. ✓

*L6 (SlotDistinction).* `F ≠ G` (different start addresses in their spans), so `(F, G, Θ) ≠ (G, F, Θ)`. ✓

*L11a (LinkUniqueness).* `a` was produced by forward allocation. With `|dom(Σ.L)| = 1`, no collision is possible. ✓

*L11b (NonInjectivity).* The clause applies: `a ∈ dom(Σ.L)` satisfies the universal quantifier's precondition. The extension `Σ'` witnessing the existential is constructed in Step 1 below, where `a'` is allocated with `Σ_1.L(a') = Σ.L(a)`. ✓

*L12 (LinkImmutability).* L12 constrains state transitions, not individual states. In this single-state example, no transition is under consideration, so L12 is vacuously satisfied. Verified non-vacuously below across two transitions. ✓ (vacuous)

*L12a (LinkStoreMonotonicity).* Similarly a transition invariant, vacuously satisfied here. Verified non-vacuously below. ✓ (vacuous)

*L14 (DualPrimitive).* `dom(Σ.C) ∪ dom(Σ.L) = {c₁, c₂, a}`. All stored entities. `dom(Σ.C) ∩ dom(Σ.L) = ∅`. ✓

*L10 (TypeHierarchyByContainment).* For the ghost type at `g = 1.0.2.0.1.0.1.1`, define a parent type `p = 1.0.2.0.1.0.1` with displacement `δ(1, 7) = [0, 0, 0, 0, 0, 0, 1]` (action point `k = 7 = #p`). The coverage of `(p, δ(1, #p))` is `{t : p ≤ t < shift(p, 1)} = {t : 1.0.2.0.1.0.1 ≤ t < 1.0.2.0.1.0.2}`. Since `g = 1.0.2.0.1.0.1.1` and `p ≼ g`, by T1(ii) `g ≥ p`, and `g < 1.0.2.0.1.0.2` because `g` agrees with `p` at position 7 (both have value 1) while `inc(p, 0)` has value 2 there. So `g ∈ coverage({(p, δ(1, #p))})` — a single span query at `p` matches the subtype at `g`. ✓

*L9 (TypeGhostPermission).* The type endset references `g = 1.0.2.0.1.0.1.1`, which is not in `dom(Σ.C) ∪ dom(Σ.L) = {c₁, c₂, a}`. This state is conforming — the ghost type is permitted. ✓

*S3 (ReferentialIntegrity, ASN-0036).* `ran(Σ.M(d)) = {c₁, c₂} ⊆ dom(Σ.C)`. ✓

**Extension: L11b non-injectivity, L13, and transition verification.**

We extend the state in two steps, naming each intermediate state, to verify L11b, L12, and L13 non-vacuously.

*Step 1: adding `a'`.* Define `a' = 1.0.1.0.1.0.2.2` with `Σ_1.L(a') = (F, G, Θ)` — same endsets as `a`. The intermediate state is `Σ_1` with `Σ_1.L = {a ↦ (F, G, Θ),\; a' ↦ (F, G, Θ)}`, `Σ_1.C = Σ.C`, `Σ_1.M = Σ.M`.

*L11b non-injectivity in `Σ_1`.* `|dom(Σ_1.L)| = 2`, `a ≠ a'`, and `Σ_1.L(a) = Σ_1.L(a') = (F, G, Θ)`. The link store is non-injective — two distinct addresses map to the same triple. This is the witness for L11b applied to `Σ` with `a`. ✓

*L12 across `Σ → Σ_1`.* `dom(Σ.L) = {a}`. We verify: `a ∈ dom(Σ_1.L)` and `Σ_1.L(a) = (F, G, Θ) = Σ.L(a)`. The sole pre-existing link is preserved. ✓

*L12a across `Σ → Σ_1`.* `dom(Σ.L) = {a} ⊆ {a, a'} = dom(Σ_1.L)`. ✓

*Step 2: adding the meta-link `a₂`.* Define `a₂ = 1.0.1.0.1.0.2.3` — a meta-link whose from-endset references the first link `a`.

Define the span targeting `a`: `δ(1, 8) = [0, 0, 0, 0, 0, 0, 0, 1]` has action point `k = 8 = #a`, and `k ≤ #a` holds, so `(a, δ(1, 8))` is well-formed by T12. ✓

Define the meta-link:

- From-endset: `F₂ = {(a, δ(1, 8))}` — pointing at the first link
- To-endset: `G₂ = {(c₂, δ(1, 8))}` — pointing at content
- Type-endset: `Θ₂ = {(g, δ(1, 8))}` — same ghost type

The final state is `Σ_2` with `Σ_2.L = {a ↦ (F, G, Θ),\; a' ↦ (F, G, Θ),\; a₂ ↦ (F₂, G₂, Θ₂)}`, `Σ_2.C = Σ_1.C`, `Σ_2.M = Σ_1.M`.

*L13 (ReflexiveAddressing).* The from-endset of `a₂` contains the span `(a, δ(1, 8))` where `a ∈ dom(Σ_2.L)`. This is a concrete link-to-link reference — `a₂`'s from-endset targets the link entity at `a`. ✓

*L0 for `a₂`.* `fields(a₂).E₁ = 2 = s_L`. The from-endset span `(a, δ(1, 8))` references `a` with `fields(a).E₁ = 2 = s_L` — a cross-subspace reference from `s_L` to `s_L`, permitted by L4. ✓

*L4 for `a₂`.* The span `(a, δ(1, 8))` has `a ∈ T` and satisfies T12 (verified above). No constraint prevents the span from referencing a link-subspace address. ✓

*L12 across `Σ_1 → Σ_2`.* `dom(Σ_1.L) = {a, a'}`. For `a`: `a ∈ dom(Σ_2.L)` and `Σ_2.L(a) = (F, G, Θ) = Σ_1.L(a)`. For `a'`: `a' ∈ dom(Σ_2.L)` and `Σ_2.L(a') = (F, G, Θ) = Σ_1.L(a')`. Both pre-existing links are preserved. ✓

*L12a across `Σ_1 → Σ_2`.* `dom(Σ_1.L) = {a, a'} ⊆ {a, a', a₂} = dom(Σ_2.L)`. ✓


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| Σ.L | DEF | `Σ.L : T ⇀ Link` — the link store, mapping addresses to link values | introduced |
| L0 | INV | SubspacePartition — link addresses occupy subspace `s_L`, content addresses occupy `s_C`, and `dom(Σ.L) ∩ dom(Σ.C) = ∅` | introduced |
| L1 | INV | LinkElementLevel — every link address is an element-level tumbler: `(A a ∈ dom(Σ.L) :: zeros(a) = 3)` | introduced |
| L1a | INV | LinkScopedAllocation — every link address is allocated under the creating document's tumbler prefix | introduced |
| L2 | LEMMA | OwnershipEndsetIndependence — `home(a)` depends only on `a`, not on the link's endsets | introduced |
| L3 | INV | NEndsetStructure — every link has at least two endsets: `\|Σ.L(a)\| ≥ 2`; arity 3 `(F, G, Θ)` by StandardTriple convention | introduced |
| L4 | LEMMA | EndsetGenerality — endset spans satisfy T12 (definitional from L3); the substantive content is the absence of additional constraints: no single-document, content-only, or existence restriction | introduced |
| L5 | INV | EndsetSetSemantics — an endset is an unordered set; only span membership matters | introduced |
| L6 | INV | SlotDistinction — endsets occupy structurally distinguished positions; for the standard triple: `F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ)` | introduced |
| L7 | META | DirectionalFlexibility — L0–L14 impose no constraint on directional significance of from/to slots | introduced |
| L8 | DEF | TypeByAddress — for standard-triple links, type matching is by address identity: `same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type` | introduced |
| L9 | LEMMA | TypeGhostPermission — for standard-triple links, any conforming state can be extended with a link whose type endset references addresses outside `dom(Σ.C) ∪ dom(Σ.L)` | introduced |
| PrefixSpanCoverage | LEMMA | For any tumbler `x` with `#x ≥ 1`, the unit-depth span has `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`; equivalently `x ⊕ δ(1, #x) = shift(x, 1)` | introduced |
| L10 | LEMMA | TypeHierarchyByContainment — `coverage({(p, δ(1, #p))}) = subtypes(p)` by PrefixSpanCoverage | introduced |
| GlobalUniqueness | LEMMA | No two allocation events produce the same address — extends S4 (OriginBasedIdentity, ASN-0036) beyond I-addresses via T9, T10, T10a, TA5, T3 (ASN-0034) | introduced |
| L11a | LEMMA | LinkUniqueness — link addresses inherit GlobalUniqueness; each link has a globally unique, permanent identity | introduced |
| L11b | LEMMA | NonInjectivity — every conforming state with a link can be extended to a non-injective conforming state | introduced |
| L12 | INV | LinkImmutability — `(A Σ, Σ' : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` for every state transition | introduced |
| L12a | LEMMA | LinkStoreMonotonicity — `dom(Σ.L) ⊆ dom(Σ'.L)` for every state transition | introduced |
| L13 | LEMMA | ReflexiveAddressing — link addresses are valid endset span targets; canonical span coverage by PrefixSpanCoverage | introduced |
| L14 | INV | DualPrimitive — stored entities partition into content (`dom(Σ.C)`) and links (`dom(Σ.L)`) with no third category | introduced |
| coverage(e) | DEF | the union of address sets denoted by the spans in endset e | introduced |
| home(a) | DEF | `origin(a)` applied to link addresses — the document under whose prefix the link resides | introduced |
| Endset | DEF | `𝒫_fin(Span)` — a finite set of well-formed spans | introduced |
| Link | DEF | `{(e₁, ..., eₙ) : N ≥ 2, each eᵢ ∈ Endset}`; standard triple `(F, G, Θ)` by convention | introduced |


## Open Questions

- What invariants must hold between the link store and the content store when the same I-address appears in multiple arrangements via transclusion?
- What well-formedness constraints, if any, govern compound link structures where links reference other links through endsets?
- Under what conditions should two endsets with different span decompositions but identical coverage be treated as equivalent for query purposes?
- What constraints govern the allocation ordering of link addresses relative to content addresses within the same document?
- What must a conforming type address hierarchy satisfy beyond tumbler prefix containment?
- Must the link store maintain consistency with the arrangements `Σ.M`, or are the two components independently mutable?
