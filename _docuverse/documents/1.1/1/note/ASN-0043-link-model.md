# ASN-0043: Link Model

*2026-03-16 (revised 2026-04-09, revision 44)*

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

*Notation from ASN-0036.* ASN-0036 introduces `Σ.M(d) : T ⇀ T` as the arrangement of document `d`. We treat `Σ.M` itself as a partial function over the tumbler space — `Σ.M : T ⇀ (T ⇀ T)` — and write `dom(Σ.M) = {d ∈ T : Σ.M(d) is defined}` for *the set of allocated documents* in state `Σ`. This is the set that S7d (DocumentAllocationDiscipline, ASN-0036) presupposes when asserting that every `d ∈ dom(Σ.M)` is a T10a-allocated node in the system's allocator tree 𝒯.

**Definition — StateExtension.** A state `Σ'` *extends* `Σ`, written `Σ' ⊒ Σ`, iff all three stores grow monotonically and agree on the shared domain: `dom(Σ.C) ⊆ dom(Σ'.C)` with `Σ'.C(a) = Σ.C(a)` for every `a ∈ dom(Σ.C)`; `dom(Σ.M) ⊆ dom(Σ'.M)` with `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`; and `dom(Σ.L) ⊆ dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)` for every `a ∈ dom(Σ.L)`. Extension permits each store to acquire new entries but forbids any change to or removal of an existing one.

**L-fin — LinkStoreFiniteness.** For each reachable system state, `dom(Σ.L)` is finite:

`|dom(Σ.L)| < ∞`

This parallels S8-fin (FiniteArrangement, ASN-0036) for arrangements. The set of valid link addresses — element-level tumblers with `subspace_I(a) = s_L` and `#E(a) ≥ 2` — is countably infinite, but only finitely many are occupied in any reachable state.


## Subspace Residence

Links share the tumbler space `T` with content, but they must be categorically distinguishable from content. A link is not a piece of text. It is a relational assertion *about* text — what Nelson calls a "meta-virtual structure connecting parts of documents (which are themselves virtual structures)." The address space provides a natural mechanism for this categorical distinction: subspace separation.

Recall from ASN-0034 (T4, HierarchicalParsing) that every element-level tumbler has the form `N.0.U.0.D.0.E`, where `E` is the element field, and the first component `E₁` is the subspace identifier. By T7 (FirstElementFieldDistinction, ASN-0034), tumblers with different first element-field components are pairwise distinct: `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

*Notational convention.* We extend `subspace_I(a) = E(a)₁` (ASN-0036's projection name) uniformly across every tumbler on which T4b's `E` projection is well-defined — i.e., every T4-valid tumbler `a` with `zeros(a) = 3` and `#E(a) ≥ 1`. T4-validity discharges T4b's domain condition (UniqueParse, ASN-0034); `zeros(a) = 3` together with `#E(a) ≥ 1` ensures the projected element field is non-empty so its first component `E(a)₁` exists. Each invocation site discharges these preconditions where it occurs.

The system designates at least two subspaces within each document's element field: one for content, one for links. Let `s_C` and `s_L` be the subspace identifiers for content and links respectively, with `s_C ≠ s_L`.

**L0 — SubspacePartition.** Every link address has subspace identifier `s_L`:

`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`

`s_L` is the link subspace identifier introduced by this ASN, and L0 pins every link address to it.

**L0a — ContentSubspaceScope.** This ASN scopes its content-side disjointness guarantee to the `s_C`-resident portion of the content store. Define:

`dom(Σ.C)|_{s_C} = {a ∈ dom(Σ.C) : subspace_I(a) = s_C}`

— the slice of `dom(Σ.C)` whose addresses occupy subspace `s_C`. The projection `subspace_I(·)` is well-defined on every `a ∈ dom(Σ.C)`: ASN-0036's S7b discharges T4-validity (by giving well-definedness of T4b's projections, whose definitional domain is the T4-valid subset of `T`) and `zeros(a) = 3`, and T4's field-segment constraint gives `#E(a) ≥ 1`, so `E(a)₁` exists. The disjointness this ASN derives is:

`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`

— no link address shares an address with any `s_C`-resident content.

By L1 (below), `zeros(a) = 3` for all `a ∈ dom(Σ.L)`; by S7b (ElementLevelIAddresses, ASN-0036), `zeros(b) = 3` for all `b ∈ dom(Σ.C)` (and a fortiori for `b ∈ dom(Σ.C)|_{s_C}`). T7's precondition requires both T4-validity and equal zero counts. T4-validity is discharged on each side: for `a ∈ dom(Σ.L)`, by L1c's T4-validity postcondition; for `b ∈ dom(Σ.C)`, by S7b's postcondition that T4b's projections `N(b)`, `U(b)`, `D(b)`, `E(b)` are well-defined, combined with T4b's definitional domain (UniqueParse, ASN-0034) being precisely the T4-valid subset of `T` — so any `b ∈ dom(Σ.C)` lies in `dom(N) ∩ dom(U) ∩ dom(D) ∩ dom(E)`, hence is T4-valid. With T4-validity discharged and `zeros(a) = zeros(b) = 3` on each side, T7 applies pairwise: for every `a ∈ dom(Σ.L)` and every `b ∈ dom(Σ.C)|_{s_C}`, L0 gives `subspace_I(a) = s_L` and the `s_C`-residence restriction gives `subspace_I(b) = s_C`; together with `s_L ≠ s_C` this yields `subspace_I(a) ≠ subspace_I(b)`, so T7's postcondition gives `a ≠ b`. Universally instantiating over the product `dom(Σ.L) × dom(Σ.C)|_{s_C}` lifts this pairwise distinctness to the scoped set disjointness:

`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`

Links and `s_C`-resident content cannot share an address. They are peers in the tumbler space — both first-class, both permanent, both addressable — but they are different kinds of entity occupying different regions. Gregory confirms this at the implementation level: the granfilade has exactly two leaf types (`GRANTEXT = 1` and `GRANORGL = 2`), distinguished by an `infotype` discriminator in the bottom crum. Content stores byte sequences; links store pointers to nested enfilades encoding the endset structure. Runtime predicates (`istextcrum`, `islinkcrum`) explicitly test for and separate these two categories.

**L1 — LinkElementLevel.** Every link address is an element-level tumbler:

`(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

This parallels S7b for content (ASN-0036). A link address carries all four tumbler fields (node, user, document, element), enabling the same structural attribution that content addresses enjoy. Gregory confirms: link addresses are allocated by `findisatoinsertmolecule` with the `LINKATOM` hint, producing full element-level tumblers.

**Definition — home.** For any T4-valid element-level tumbler `a` (so `zeros(a) = 3`), the *home document* is the document-level prefix obtained by field projection:

`home(a) = N(a).0.U(a).0.D(a)`

extracted via T4b's projections `N`, `U`, `D` (UniqueParse, ASN-0034), well-defined precisely because `a` is T4-valid and element-level. This is the same field-extraction formula ASN-0036 uses to define `origin` on content addresses, applied here to link addresses. Every link address meets the precondition: `zeros(a) = 3` by L1, and T4-validity by L1c (LinkAllocatorConformance).

**L1a — LinkScopedAllocation.** Every link address is allocated under the tumbler prefix of the document whose owner created it. By the home definition above, `home(a)` is well-defined on every `a ∈ dom(Σ.L)`, and we state the invariant in terms of it directly:

`(A a ∈ dom(Σ.L) :: home(a) ∈ dom(Σ.M))`

The membership clause requires that `home(a)` be an allocated, owned document in the current state. Nelson is explicit on this point — a link's home document is "the document under which the link is filed," presupposing an actual document with an owner; ghost addresses are admitted only for endset targets (notably the type endset, L9), not for the home prefix. This parallels S7a (DocumentScopedAllocation, ASN-0036) for content. Gregory confirms: `docreatelink` allocates the link address within the creating document's address space via `findisatoinsertmolecule`, which extends the document's I-stream. The allocation prefix is determined by the document parameter — a document that must already exist for `docreatelink` to be called — not by the endsets; a link whose endsets reference entirely foreign content is still allocated under the creating document's prefix.

**L1b — LinkElementFieldDepth.** Every link address has element field depth at least 2:

`(A a ∈ dom(Σ.L) :: #E(a) ≥ 2)`

**L1c — LinkAllocatorConformance.** Link allocation operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034): link addresses are produced by allocators that use `inc(·, 0)` for sibling allocation and `inc(·, k')` with `k' ∈ {1, 2}` (within the TA5a bounds) for child-spawning.

*Chain.* There exists a T4-valid document-level seed `s` and a T10a-conforming step sequence terminating at `a`:

`(A a ∈ dom(Σ.L) :: (E s ∈ T, n ≥ 1, t₀, t₁, ..., tₙ, k₁, ..., kₙ :: T4-valid(s) ∧ zeros(s) = 2 ∧ t₀ = s ∧ tₙ = a ∧ (A i : 1 ≤ i ≤ n : tᵢ = inc(tᵢ₋₁, kᵢ) ∧ kᵢ ∈ {0, 1, 2} ∧ (kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2)) ∧ k₁ = 2 ∧ (A i : 1 ≤ i ≤ n : #tᵢ > #s)))`

Each step is locally T10a-admissible: `kᵢ ∈ {0, 1, 2}` (the allowed T10a step types — `0` for sibling advance, `1` or `2` for child-spawn), and TA5a's side condition (ASN-0034) is discharged whenever `kᵢ = 2` by the explicit `zeros(tᵢ₋₁) ≤ 2` clause; for `kᵢ ∈ {0, 1}` TA5a is unconditional. The first step seats the field-separating zero at position `#s + 1`, between the document prefix and the element field.

**CPP — ChainPrefixPreservation (local lemma).** Let `t₀, t₁, ..., tₙ` be a T10a-conforming chain of T4-valid tumblers (T4-validity propagated along the chain by T10a.4), and let `p` be a fixed length with `p ≤ #t₀`. Suppose every step modifies only positions strictly beyond `p`: each child-spawn `inc(·, k')` (`k' ≥ 1`) agrees with its input on positions `1..#tᵢ₋₁` (TA5(b)), and each sibling advance `inc(·, 0)` modifies only the `sig` position (TA5(c)), which for the T4-valid input is the terminal position `#tᵢ₋₁` (TA5-SigValid) — so whenever `#tᵢ₋₁ > p` the advance leaves positions `1..p` fixed. Then by induction on chain length every `tᵢ`, and in particular the terminus `tₙ`, agrees with `t₀` on positions `1..p`. Applied to the L1c chain with `t₀ = s` and `p = #s`: the opening child-spawn agrees on positions `1..#s`, and every later step operates at length `> #s`, so CPP yields that `a` agrees with `s` on positions `1..#s`.

*Postcondition: T4-validity of `a`.* By T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every output of a T10a-conforming allocator step is T4-valid given a T4-valid input. The chain begins at the T4-valid seed `s` and proceeds entirely by T10a steps, so by induction on chain length, `tₙ = a` is T4-valid. With T4-validity of `a` established and L1's `zeros(a) = 3` placing `a` at element level, T4b's projections `N(a)`, `U(a)`, `D(a)`, `E(a)` are well-defined; in particular, the document-level prefix `home(a)` (Definition — home) is well-defined.

*Postcondition: `s = home(a)`.* By CPP, `a` agrees with `s` on positions `1..#s`. The third zero of `a` first appears at position `#s + 1` — the one seated by `k₁ = 2` — and `s` ends at position `#s` with a positive component (T4-validity of `s`). The prefix of `a` ending just before the third zero is therefore exactly the length-`#s` prefix `s`, which by definition is `home(a)`. Hence `s = home(a)`.


## Home and Ownership

A link's *home document* is `home(a)` (Definition — home), well-defined on every link address by L1 (`zeros(a) = 3`) and L1c (T4-validity). We now develop its ownership semantics.

By GlobalUniqueness (ASN-0034), no two allocation events produce the same address. Link addresses are produced by allocation events conforming to T10a (L1c). Therefore each link receives a globally unique address.

The home document determines the link's owner. This is not metadata attached to the link — it IS the link's address, read through the field structure. For the creating document `d`, L1c's `s = home(a)` postcondition gives `home(a) = s = d` directly. L1a (the membership invariant `home(a) ∈ dom(Σ.M)`) and that postcondition together deliver the link analog of S7 (StructuralAttribution, ASN-0036): `home(a)` is computed by field projection on the address alone (L1, T4), uniquely identifies the creating document across the system, and is structurally guaranteed to *be* that document — not merely *some* allocated document in `dom(Σ.M)`. For links `a₁, a₂` allocated under distinct documents `d₁ ≠ d₂`, the same postcondition gives `home(a₁) = d₁` and `home(a₂) = d₂`; since `d₁ ≠ d₂` as document-level tumblers (by T3, CanonicalRepresentation — tumbler equality is sequence equality), `home(a₁) ≠ home(a₂)` — directly, without routing through element-level address uniqueness. This identification is structural, embedded in the address, not attached as metadata.

The critical property — the one that distinguishes this design from systems where annotations are embedded in the annotated content:

**L2 — OwnershipEndsetIndependence.** The home document of a link is determined entirely by the link's address and is independent of the link's endsets. This is an immediate consequence of the `home` definition: `home(a) = N(a).0.U(a).0.D(a)` is computed by T4 field extraction from the address `a` alone. The endset content `Σ.L(a)` never appears as an argument to this computation — `home` is a function of the address, not of the link value. Whatever endsets a link carries, its home document is fixed by its address.

Nelson makes this a first principle: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." This separation of residence from reference is what permits annotation without modification. Your link lives in your document, under your authority, even though its endsets reach into someone else's content. The annotated document is untouched — no byte added, no structure modified, no permission required.


## The Endset Structure

What internal structure must a link have? We seek the minimal structure sufficient for typed, directional connections between arbitrary spans.

A connection has at least two sides — a *source* and a *target*. Without two sides there is no connection. But two sides alone do not suffice: we cannot distinguish a citation from a comment from a refutation by structure alone. If all links are structurally uniform two-endset connections, one cannot ask "find all citations" without also retrieving every comment and footnote. Classification is required.

Nelson's design resolves this not by adding a metadata field — a type tag bolted onto a binary link — but by adding a *third endset*, structurally identical to the first two, pointing into the address space. The type endset is part of every link's identity: Nelson treats it as symmetrical with from and to ["A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." LM 4/44]. The standard triple — from, to, type — is the design floor.

Gregory's implementation admits a relaxation that Nelson's design does not: `docreatelink` short-circuits the third-endset insertion when the client passes an empty type specset (`insertendsetsinorgl` and `insertendsetsinspanf` both guard on `threesporglset` being non-NULL, silently skipping the storage step when it is NULL). The legacy internal entry point `domakelink` also exposes a two-endset path. Per Nelson, every link carries a *non-empty* type endset — the type is the link's classifying address and must reference at least one tumbler (possibly a ghost, by L9 below). L3 formalizes this requirement and fixes the resulting conformance verdict below.

Adding the third endset achieves three things simultaneously:

1. **Extensibility.** Any user can define new types by choosing new addresses, without schema changes. Nelson: "The set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose."

2. **Uniformity.** All endsets have the same representation — a set of spans in the tumbler space. The link is a homogeneous sequence, not a pair-plus-metadata.

3. **Hierarchical classification.** Because tumbler prefix containment is decidable — `p ≼ t` requires only finite component-wise equality (PrefixRelation, ASN-0034), computable from the tumblers alone (T2, IntrinsicComparison) — type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering. A query matching `p` matches both (by T5, ContiguousSubtrees).

But Nelson's design does not stop at three. The three-endset case — from, to, type — is the standard convention, not a structural ceiling; higher-arity links are admitted directly. A faceted link relating content across more than three roles need not be decomposed into chains of ternary links; it can be expressed directly as a single link with the required number of endsets.

We now define the components.

**Definition — Endset.** An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefinedness, ASN-0034): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset — a link may have an endset that references nothing.

**Definition — Link.** A *link value* is a finite sequence of N ≥ 3 endsets, with the third slot designated as the type endset by the StandardTriple convention (below):

`Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`

We write `|L|` for the *arity* of a link — the number of endsets in the sequence.

**Convention — StandardTriple.** The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*. We write `(F, G, Θ)` for a link following this convention. Nelson's MAKELINK operation takes these three endsets plus a home document, and Gregory's implementation hardcodes three V-addresses (1.1, 2.1, 3.1) and three spanfilade index constants (`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). The standard triple is the dominant case — but it is a convention, not a structural limit.

*Named accessor.* Conditional on `|Σ.L(a)| ≥ 3`, we introduce the abbreviation `Σ.L(a).type ≡ Σ.L(a).e₃` as a synonym for the indexed accessor of slot 3. The side condition `|Σ.L(a)| ≥ 3` that makes the abbreviation well-defined is discharged for every conforming link by L3. The two forms are interchangeable in all formal statements.

**L3 — NEndsetStructure.** Every link in the link store is a sequence of at least three endsets, each in `Endset`, with slot 3 a non-empty type endset:

`(A a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |Σ.L(a)| : Σ.L(a).eᵢ ∈ Endset) ∧ Σ.L(a).e₃ ≠ ∅)`

Nelson [LM 4/79] explicitly calls for N-endset support beyond three: "4-sets, 5-sets ... n-sets supported in link storage and search." Gregory's implementation fixes N = 3 — the V-subspace assignment function `setlinkvsas` hardcodes three V-addresses, the query function `intersectlinksets` takes exactly three input lists, and the wire protocol (`FINDLINKSFROMTOTHREE`) encodes three endset parameters. The integer namespace for a fourth endset type is already consumed (`DOCISPAN = 4`), blocking extension without renumbering. The design commitment: every link carries the standard triple (from, to, type) as its floor, with higher arity admitted for relational roles that need more slots. Arity-2 "untyped" links are not part of the design — where Gregory's implementation can store such links via empty-type-specset short-circuit, the resulting state lies outside this ASN's conforming link store.

The non-emptiness conjunct `Σ.L(a).e₃ ≠ ∅` excludes arity-3 links `(F, G, ∅)` whose type slot is structurally present but vacuously inhabited: such a link carries no classifying address.


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

**L5 — EndsetSetSemantics.** An endset is an *unordered* set; the ordering of spans within an endset carries no semantic meaning. Two endsets are equal iff they have the same span members, and the model exposes no positional accessor within an endset:

`(A a, a' ∈ dom(Σ.L), i ∈ {1, ..., |Σ.L(a)|}, j ∈ {1, ..., |Σ.L(a')|} :: Σ.L(a).eᵢ = Σ.L(a').eⱼ ⟺ (A (s, ℓ) :: (s, ℓ) ∈ Σ.L(a).eᵢ ⟺ (s, ℓ) ∈ Σ.L(a').eⱼ))`

The substantive content is two-fold: (i) endset equality reduces to extensional set equality over `Span`, and (ii) no operator in the model selects a span by position within an endset — span access is by membership only. By contrast, slot access *across* endsets is positional (L6, SlotDistinction).

Gregory confirms exhaustively. During storage, spans receive sequential V-addresses within the link's own permutation matrix (an artifact of linked-list traversal order). Upon retrieval, spans come back ordered by I-address value, not by insertion sequence — the original ordering is not preserved or recoverable. No code path in the implementation treats any span as "primary" or consults positional index within an endset. All link-finding (`sporglset2linksetinrange`) and intersection (`intersectlinksets`) operations iterate uniformly, comparing addresses by value without regard to position. A planned `consolidatespanset` function — which might have imposed normalization — was never implemented.

**Definition — Coverage.** For an endset `e`, define the *coverage* as the union of the sets denoted by its spans:

`coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`

This is the set of all tumbler addresses referenced by the endset. Note that coverage is a lossy projection: two endsets with different span decompositions may have identical coverage. For instance, `{(1, [3])}` and `{(1, [1]), (2, [2])}` cover the same addresses but are distinct endsets — they contain different spans, and by L5 (which collapses only reorderings of the same span collection, not distinct collections) they are not equal. Coverage tells us *which addresses* an endset references, abstracting away the particular decomposition into spans, but it does not determine endset identity.


## Slot Distinction and Directionality

Although all endsets within a link are structurally identical (all are elements of `Endset`), they are not interchangeable. Each endset occupies a distinguished position — its slot index — and search can constrain on each slot independently.

**L6 — SlotDistinction.** The endsets within a link are addressable by slot position. The link model provides a positional accessor `Σ.L(a).eᵢ` returning the i-th endset, defined for every `a ∈ dom(Σ.L)` and every `i ∈ {1, ..., |Σ.L(a)|}`; slot index is a primitive of the model, not a derived label over an unordered collection. Link equality is component-wise tuple equality, by the `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` definition.

L6 is the structural dual of L5. L5 forbids any positional accessor *within* an endset — span access reduces to membership, with no `e.spanⱼ` operator in the model. L6 provides one *across* endsets within a link — slot 1 and slot 2 are different positions, retrievable independently, and a query constraint on slot 1 is structurally distinct from a query constraint on slot 2. The two together carve out the structural primitive: at the link level, position matters; within an endset, it does not. Standard-triple consequence: when `F ≠ G`, `(F, G, Θ) ≠ (G, F, Θ)`; more generally, any slot-permutation that swaps differing entries produces a distinct link value by component-wise tuple inequality.

Gregory's implementation encodes this distinction at two independent levels: in the link's own permutation matrix (V-addresses 1.1, 2.1, 3.1 for from, to, and type) and in the spanfilade index (ORGL-range prefixes `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). A query for "links from span A" and a query for "links to span A" search different index columns and may return different results.

But the slot distinction is *structural*, not *semantic*. Whether "from" means "source" and "to" means "destination" is not determined by any invariant of the link structure:

**L7 — DirectionalFlexibility.** The invariants L0–L14 and L-fin impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure.

*By inspection.* No invariant in L0–L14 or L-fin references slot directionality or the source/target roles: none uses the words "from," "to," "source," "target," "origin," or "destination" in any structural role. L6 establishes that slots are positionally addressable, but that is sequence-position, not direction — it asserts only that slot 1 and slot 2 are different positions, not that one is "from" and the other "to." The F/G labels in the standard triple `(F, G, Θ)` are nominal conveniences for prose, not constraints carried by the invariants.

Nelson: "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" The word "typically" is deliberate. A citation link is directional — it goes *from* citing text *to* cited source. A counterpart link marking equivalence has no meaningful direction. A heading link populates only one content endset — Nelson calls it "inane" to label that one endset "from." The structure provides two slots; the type defines whether the distinction carries directional weight.

The consequence: any system that determines a link's directionality from slot position alone — treating "from" as inherently "source" and "to" as inherently "target" without consulting the type — is misinterpreting the design. The slots provide structural asymmetry sufficient for indexing and query; the type provides semantic interpretation.

Despite the slot distinction, access is symmetric. The system must support retrieving any endset of any link with equal facility. Gregory confirms: the `followlink` operation takes a `whichend` parameter (1, 2, or 3) and calls `link2sporglset` with a V-range query parameterized by that integer. The retrieval path is identical for all slots — no endset is privileged or hidden.


## The Type Endset

The type endset deserves extended treatment. It is structurally an endset — a finite set of spans — but its role is semantic classification, and it has distinctive properties that follow from that role.

**L8 — TypeByAddress.** Type matching is by *address identity*, not by content at the address. Whether two links share the same type is determined by whether their type endsets reference the same addresses, not by what is stored at those addresses:

`same_type(a₁, a₂) ⟺ coverage(Σ.L(a₁).type) = coverage(Σ.L(a₂).type)`

where `Σ.L(a).type` denotes slot 3 — well-defined for every `a ∈ dom(Σ.L)` by L3's `|Σ.L(a)| ≥ 3` — and `coverage(·)` is the address-set projection defined above. The relation is on coverage (the address set referenced by the endset), not on span-set identity: two type endsets with different span decompositions but identical address coverage denote the same type.

*Consequences.* The defining biconditional is set-equality on coverage, so `same_type` inherits the three closure properties of `=` on sets immediately:

- *Reflexive.* `(A a ∈ dom(Σ.L) :: same_type(a, a))` — `coverage(Σ.L(a).type) = coverage(Σ.L(a).type)` by reflexivity of set equality.
- *Symmetric.* `(A a₁, a₂ ∈ dom(Σ.L) :: same_type(a₁, a₂) ⟹ same_type(a₂, a₁))` — by symmetry of set equality.
- *Transitive.* `(A a₁, a₂, a₃ ∈ dom(Σ.L) :: same_type(a₁, a₂) ∧ same_type(a₂, a₃) ⟹ same_type(a₁, a₃))` — by transitivity of set equality.

`same_type` is therefore an equivalence relation on `dom(Σ.L)`, partitioning the link store into type-equivalence classes; under search semantics, every member of a class is indistinguishable from every other by type matching.

Nelson: "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

The design choice — coverage rather than span-set identity — falls out of Nelson's search semantics. He frames matching at the request-against-link level: "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58] The criterion is *address overlap* between request and stored endset, not equality of span decompositions; since type-equivalence is what makes two links indistinguishable to any search request, two type endsets with the same coverage are interchangeable under search and therefore the same type. Gregory confirms at the implementation level: `sporglset2linksetinrange` performs range-overlap matching via `crumqualifies2d` (a half-open interval intersection test), and `intersectlinksets` compares only link ISAs across the three endset queries — there is no span-equality test at any stage of retrieval. The query architecture is built on I-address coverage intersection, not on span-set comparison.

This is a profound design choice. It decouples classification from content retrieval entirely. A search for "all links of type X" never fetches the bytes at address X — it only matches the address. This means:

**L9 — TypeGhostPermission.** Ghost types are permitted. For any state `Σ` satisfying the state-local invariants of this ASN (L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin) together with ASN-0036's state-local invariants (S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ), with `dom(Σ.M) ≠ ∅`, and with `s_C`-resident content (`(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`), there exists for every arity `N ≥ 3` a conforming state `Σ'` extending `Σ` (`Σ' ⊒ Σ`, StateExtension) with a link of arity `N` whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`:

`(A Σ : Σ satisfies the state-local L- and S-invariants ∧ dom(Σ.M) ≠ ∅ ∧ (A b ∈ dom(Σ.C) :: subspace_I(b) = s_C) : (A N ≥ 3 :: (E Σ' extending Σ, a ∈ dom(Σ'.L), (s, ℓ) ∈ Σ'.L(a).type :: |Σ'.L(a)| = N ∧ s ∉ dom(Σ'.C) ∪ dom(Σ'.L))))`

*Witness.* Take any conforming `Σ`. By T4's positive-component constraint on present fields, both `s_C ≥ 1` and `s_L ≥ 1` (each is the first component of some element field, hence non-separator and strictly positive). Choose a subspace identifier `s_X ∈ ℕ` with `s_X ≥ 1`, `s_X ≠ s_C`, and `s_X ≠ s_L` (such `s_X` exists by T0(a)'s unbounded positive component values: infinitely many naturals differ from any two given values).

*Selection of `d'` (a T10a-allocated document under 𝒯).* L1a requires `home(a) ∈ dom(Σ'.M)`, and S7d requires every entry of `dom(Σ'.M)` to be a node in the system's allocator tree 𝒯 produced by a T10a allocation event. By the L9 precondition `dom(Σ.M) ≠ ∅`, pick any `d ∈ dom(Σ.M)` and set `d' = d`. By S7d on `Σ`, `d` is the terminus of a T10a-conforming allocator chain from 𝒯's root: the root is T4-valid by T10a's root-of-allocator-tree axiom, and T10a.4 (T4PreservationUnderDiscipline) propagates T4-validity along each chain step, so `d` is T4-valid. Reusing the existing arrangement keeps `Σ'.M = Σ.M`, so no new document allocation event is introduced. `d'` is therefore a T4-valid document-level tumbler (`zeros(d') = 2`, by S7d) with `d' ∈ dom(Σ.M) = dom(Σ'.M)`.

*Construction of `g` (T4-valid ghost address in subspace `s_X`).* Build `g = d'.0.s_X.1` — concatenate `[0, s_X, 1]` to `d'`. T4-validity: `d'` is T4-valid with `zeros(d') = 2`; appending `0` introduces one new zero (so `zeros(g) = 3`); the last component of `d'` is strictly positive by T4-validity of `d'`, so the new `0` does not create adjacent zeros, and `s_X ≥ 1` separates the new `0` from the trailing `1`; the first component of `g` (inherited from `d'`) and the last (`1`) are strictly positive; every non-separator component is strictly positive (inherited components by T4-validity of `d'`; `s_X ≥ 1` by construction; `1 > 0` at the tail). T4b's projections therefore apply: `E(g) = [s_X, 1]`, giving `subspace_I(g) = s_X` and `#E(g) = 2`. By L0 applied to `Σ`, `dom(Σ.L) ⊆ {t : subspace_I(t) = s_L}`; by the L9 precondition (`s_C`-residence of content), `dom(Σ.C) ⊆ {t : subspace_I(t) = s_C}`. By the L0a discharge (with `zeros = 3` per side — `g` by construction, content by S7b, links by L1 — and `s_X` distinct from both `s_C` and `s_L`), `g ∉ dom(Σ.C) ∪ dom(Σ.L)`, regardless of the size of these domains.

*Choice of `a` (fresh link address under `d'`).* By L-fin, `dom(Σ.L)` is finite. By T0(a), element-field component values are unbounded, so infinitely many element-level tumblers with `subspace_I(·) = s_L` and `#E(·) ≥ 2` exist within `d'`'s link subspace. We construct `a` explicitly by case analysis on `d'`'s prior link-allocation state; the same construction yields the freshness `a ∉ dom(Σ.L)` (for L11a) and the producibility chain (for L1c).

*Case A — `d'` has no prior link allocations under `Σ` (`{b ∈ dom(Σ.L) : home(b) = d'} = ∅`).* Set `a = d'.0.s_L.1`. The producer chain from `d'` to `a`: (i) `inc(d', 2)` → `d'.0.1` — element field depth 1, subspace 1 (`k' = 2`, requiring `zeros(d') ≤ 2` by TA5a; satisfied since `zeros(d') = 2`); (ii) sibling sweep `inc(·, 0)` from subspace 1 across to subspace `s_L` at element field depth 1, applied `s_L − 1` times — each step a `k = 0` sibling advance, unconditionally T4-preserving (each intermediate `d'.0.j` for `j ∈ [2, s_L]` is T4-valid: `zeros = 3`, every non-separator component positive since `j ≥ 1`, no adjacent zeros); (iii) `inc(d'.0.s_L, 1)` → `d'.0.s_L.1` = `a` — child-spawn to element field depth 2 (`k' = 1`; TA5a is unconditional for `k ∈ {0, 1}`; the output has `zeros(a) = 3`). Each step conforms to T10a. *Freshness:* every step from `t₁ = d'.0.1` onward operates at length `> #d'`, so CPP (with `t₀ = d'`, `p = #d'`) gives that `a` agrees with `d'` on positions `1..#d'`; the third zero of `a` first appears at position `#d' + 1`, so `home(a) = d'`. The case hypothesis then directly yields `a ∉ dom(Σ.L)`: any `b ∈ dom(Σ.L)` with `b = a` would have `home(b) = home(a) = d'`, contradicting the empty-set hypothesis. No appeal to GlobalUniqueness is needed.

*Case B — `d'` has prior link allocations under `Σ` (`{b ∈ dom(Σ.L) : home(b) = d'} ≠ ∅`).* Pick any existing link `b ∈ dom(Σ.L)` with `home(b) = d'`. By L-fin (`dom(Σ.L)` finite) and T10a.7 (the sibling chain `b, inc(b, 0), inc²(b, 0), …` is injective and hence infinite), the least `i ≥ 1` with `incⁱ(b, 0) ∉ dom(Σ.L)` exists; set `a = incⁱ(b, 0)`. *Freshness:* `a ∉ dom(Σ.L)` is immediate. Each `inc(·, 0)` step modifies only the `sig` position (TA5(c)), which for the T4-valid `b` (and its T4-valid outputs, by T10a.4) is the terminal position `#·` (TA5-SigValid), incrementing a nonzero component — no separator zero added or removed — so `zeros(a) = zeros(b) = 3`; by CPP (with `t₀ = b`, `p = #h(b)`) `home(a) = home(b) = d'`; producibility follows by extending `b`'s L1c chain with `i` sibling advances, each unconditionally T4-preserving.

Define `Σ'` as `Σ` extended with `Σ'.L(a) = (∅, ∅, {(g, δ(1, #g))}, ∅, ..., ∅)` (`N − 3` empty endsets at slots `4..N`, vacuous when `N = 3`), `Σ'.C = Σ.C`, and `Σ'.M = Σ.M` (the arrangement store is unchanged, since `d' ∈ dom(Σ.M)` is reused). The arity-3 case `(∅, ∅, {(g, δ(1, #g))})` is the canonical witness; for arbitrary `N ≥ 3`, padding with empty endsets at slots `4..N` is sound: each `∅ ∈ Endset` (since `Endset = 𝒫_fin(Span)` and the empty set is finite), L3's slot-3 non-emptiness clause constrains slot 3 alone (slots `4..N` may be empty by the per-slot `eᵢ ∈ Endset` conjunct's admission of `∅`), and the conformance verification below operates uniformly on the type endset (slot 3) and the address `a`, so adding empty endsets at slots `4..N` preserves every state-local invariant established for the arity-3 witness.

We verify that `Σ'` is conforming. Both this construction and the one for L11b (NonInjectivity, below) append a single fresh sibling link to the store while leaving content and arrangements untouched; the conformance argument is identical in both cases except for the payload. We isolate the shared argument as a lemma and then supply only the L9-specific delta.

**FSP — FreshSiblingConformance (local lemma).** Let `Σ` satisfy the state-local L- and S-invariants (L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin, and ASN-0036's S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) with `s_C`-resident content. Suppose a tumbler `a` satisfies:

- (h1) *Freshness:* `a ∉ dom(Σ.L)`;
- (h2) *Producibility:* `a` is the terminus of a T10a-conforming chain seeded at a T4-valid document-level tumbler `home(a) ∈ dom(Σ.M)`;
- (h3) *Shape:* `subspace_I(a) = s_L`, `zeros(a) = 3`, `#E(a) ≥ 2`, and `a` is T4-valid.

Let `ℓ = (e₁, ..., e_N)` with `N ≥ 3`, each `eᵢ ∈ Endset` (a finite set of T12-well-formed spans), and `e₃ ≠ ∅`. Define `Σ'` by `Σ'.L = Σ.L ∪ {a ↦ ℓ}`, `Σ'.C = Σ.C`, `Σ'.M = Σ.M`. Then `Σ'` satisfies every state-local L-invariant (L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin) and every state-local ASN-0036 invariant (S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ); and the `Σ → Σ'` transition satisfies the transition invariants L12 (LinkImmutability) and L12a (LinkStoreMonotonicity). FSP places no constraint on the endset *targets* of `ℓ`; in particular `coverage(ℓ.type)` is unconstrained. (L11a is the one cross-event claim in this list, not a per-state predicate; FSP "preserves" it by extending its conclusion to the new event — the address `a` added by `Σ → Σ'` is distinct from every link address allocated in `Σ`, as the L11a bullet below discharges.) FSP places no constraint on the endset *targets* of `ℓ`; in particular `coverage(ℓ.type)` is unconstrained.

*Proof.* The construction adds one link-store entry at `a`; `Σ'.C = Σ.C` and `Σ'.M = Σ.M`. We treat the new entry and the carry-over of existing entries.

- *L0.* By the L0a discharge (with `zeros = 3` per side and `s_L ≠ s_C`): `subspace_I(a) = s_L` (h3) and `dom(Σ'.C) = dom(Σ.C)` is `s_C`-resident, so `a ∉ dom(Σ'.C)`, preserving `dom(Σ'.L) ∩ dom(Σ'.C)|_{s_C} = ∅`. Existing addresses unchanged.
- *L1.* `zeros(a) = 3` (h3); existing entries by L1 on `Σ`.
- *L1a.* `home(a) ∈ dom(Σ.M) = dom(Σ'.M)` (h2). For existing `b`, `home(b)` depends only on `b`'s fields (unchanged) and `home(b) ∈ dom(Σ.M)` by L1a on `Σ`.
- *L1b.* `#E(a) ≥ 2` (h3); existing entries by L1b on `Σ`.
- *L1c.* `a` is the terminus of a T10a-conforming chain (h2); existing entries by L1c on `Σ`.
- *L3.* `|ℓ| = N ≥ 3`, each `eᵢ ∈ Endset`, `e₃ ≠ ∅` by the payload hypothesis (the non-emptiness conjunct constrains slot 3 alone, so empty slots `4..N` are admissible). Existing entries by L3 on `Σ`.
- *L5.* Each endset of `ℓ` is a set under extensional membership; existing entries unchanged.
- *L6.* `ℓ` is an `N`-tuple of endsets with well-defined positional accessors, conforming to the `Link` definition; existing entries unchanged.
- *L11a.* `a ∉ dom(Σ.L)` (h1), so the new allocation event produces an address distinct from every previously-allocated link address; existing pairwise distinctness carries over.
- *L12 / L12a (transition).* For every `b ∈ dom(Σ.L)`: `b ∈ dom(Σ'.L)` and `Σ'.L(b) = Σ.L(b)`, since only the entry at `a` is added — this discharges L12 across `Σ → Σ'`, and `dom(Σ.L) ⊆ dom(Σ'.L)` discharges its corollary L12a.
- *L14.* `dom(Σ'.C) ∪ dom(Σ'.L) = dom(Σ.C) ∪ (dom(Σ.L) ∪ {a})`; disjointness over the `s_C`-slice holds since `a` is in `s_L` and `Σ'.C = Σ.C`.
- *L14a.* For every `(d, v)` with `v ∈ dom(Σ'.M(d)) = dom(Σ.M(d))`: `Σ'.M(d)(v) ∈ dom(Σ.C)` by S3 on `Σ`; since `dom(Σ.C) ∩ dom(Σ'.L) = ∅` by L0 (above), `Σ'.M(d)(v) ∉ dom(Σ'.L)`.
- *L-fin.* `dom(Σ'.L) = dom(Σ.L) ∪ {a}` is finite, since `dom(Σ.L)` is finite.
- *ASN-0036 invariants.* `Σ'.C = Σ.C` discharges S0, S1, S7a, S7b verbatim; `Σ'.M = Σ.M` discharges S2, S3, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ verbatim — every constraint on the content store and arrangement family is reproduced from `Σ`. ∎

*Application to L9.* We discharge FSP's hypotheses for the address `a` constructed above and payload `ℓ = (∅, ∅, {(g, δ(1, #g))}, ∅, ..., ∅)`.

- (h3) *Shape:* in both cases `a` has `subspace_I(a) = s_L`, `zeros(a) = 3`, `#E(a) ≥ 2` (at minimum `E(a) = [s_L, 1]`), and is T4-valid (T10a.4 along the producer chain given above).
- (h1)/(h2) *Freshness and producibility:* established by the Case A / Case B construction above — `a ∉ dom(Σ.L)`, and `a` is the terminus of a T10a-conforming chain seeded at `home(a) = d' ∈ dom(Σ.M)`.

- *Payload:* each `∅ ∈ Endset` (the empty set is finite); `{(g, δ(1, #g))}` is a finite set whose single span is T12-well-formed — by the construction of `g`, `#g = #d' + 3 ≥ 1`, so `δ(1, #g) > 0` has action point `k = #g ≤ #g`; slot 3 `= {(g, δ(1, #g))} ≠ ∅`. So `ℓ` satisfies FSP's payload hypothesis at every arity `N ≥ 3`.

By FSP, `Σ'` satisfies every state-local L- and S-invariant. It remains to establish the L9-specific conclusion that FSP leaves open: the ghost-type disjointness `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`. The disjointness `g ∉ dom(Σ.C) ∪ dom(Σ.L)` established above transfers to `Σ'` unchanged: `Σ'.C = Σ.C`, and the sole new link address `a ≠ g` lies in subspace `s_L ≠ s_X`, so `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`. ∎

No property of L0–L14 or L-fin constrains type endset targets to content addresses. Nelson: "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." The type address is a pure name — a position chosen by convention, not a pointer to content that must be dereferenced.

A consequence of L8 and L9 together: new link types can be defined by choosing a fresh tumbler address and using it as a type endset. No content needs to be created at that address. No registry needs to be updated. No schema needs to change. The type exists as soon as someone uses it. This is what makes the type system "open-ended" — any user can extend it without coordination or system modification.

**PrefixSpanCoverage (local lemma, span/tumbler algebra).** For any tumbler `x` with `#x ≥ 1`, the unit-depth displacement `δ(1, #x)` (OrdinalDisplacement, ASN-0034) is `[0, ..., 0, 1]` of length `m = #x`, with action point `k = m`; the span `(x, δ(1, m))` is well-formed by T12; and:

`coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`

*Derivation.* By OrdinalShift (ASN-0034), `shift(x, 1) = x ⊕ δ(1, #x) = x ⊕ δ(1, m)` — the tumbler of length `m` agreeing with `x` on positions `1..m−1` and with last component `x_m + 1`. By T12 (SpanWellDefinedness, ASN-0034), with `δ(1, m) > 0` and action point `m ≤ #x`, the span is well-formed and `coverage({(x, δ(1, m))}) = {t ∈ T : x ≤ t < x ⊕ δ(1, m)} = {t ∈ T : x ≤ t < shift(x, 1)}`. We show this half-open interval equals `subtree(x) = {t : x ≼ t}` by mutual inclusion.

(⊇) Suppose `x ≼ t`. Then `t` agrees with `x` on positions `1..m`. If `#t = m` then `t = x` (T3, CanonicalRepresentation), so `x ≤ t`; if `#t > m` then `x` is a proper prefix of `t` and T1 case (ii) gives `x < t` — either way `x ≤ t`. For the upper bound, `t` and `shift(x, 1)` agree on positions `1..m−1` (both equal `x` there) and at position `m` satisfy `t_m = x_m < x_m + 1 = shift(x, 1)_m`; T1 case (i) at the divergence position `m` gives `t < shift(x, 1)`. Hence `t ∈ {t : x ≤ t < shift(x, 1)}`.

(⊆) Suppose `x ≤ t < shift(x, 1)`; we show `x ≼ t`. If `x = t`, done. Otherwise `x < t`, so by T1 either (ii) `x` is a proper prefix of `t` — giving `x ≼ t` directly — or (i) `x` and `t` first diverge at some `k ≤ m` with `x_k < t_k`. In case (i) we derive a contradiction with `t < shift(x, 1)`. Since `shift(x, 1)` agrees with `x` on positions `1..m−1`, and `t` agrees with `x` on positions `1..k−1`, `t` and `shift(x, 1)` agree on positions `1..k−1`. If `k < m`: at position `k`, `t_k > x_k = shift(x, 1)_k`, so T1 case (i) gives `shift(x, 1) < t`, contradicting `t < shift(x, 1)`. If `k = m`: `t_m > x_m` forces `t_m ≥ x_m + 1 = shift(x, 1)_m`; if `t_m > shift(x, 1)_m`, T1 case (i) gives `shift(x, 1) < t` (contradiction); if `t_m = shift(x, 1)_m`, then `t` agrees with `shift(x, 1)` on positions `1..m`, so either `t = shift(x, 1)` (when `#t = m`) or `shift(x, 1)` is a proper prefix of `t` (T1 case (ii), `shift(x, 1) < t`) — both contradict `t < shift(x, 1)`. Thus case (i) is impossible, and `x ≼ t`.

By T5 (ContiguousSubtrees, ASN-0034), `subtree(x)` is order-convex, confirming that the matched set is exactly the contiguous prefix interval and contains no extraneous tumblers. ∎

**L10 — TypeHierarchyByContainment.** For type addresses `p, c ∈ T` where `p ≼ c` (p is a prefix of c), define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. By PrefixSpanCoverage:

`coverage({(p, δ(1, #p))}) = {t ∈ T : p ≼ t} = subtypes(p)`

A single span query rooted at `p` matches all and only subtypes of `p`. The exclusion direction is essential: without it, a span query at `p` that also matched non-subtypes would not give a clean type hierarchy.

*Hierarchy inclusion.* The map `p ↦ subtypes(p)` reverses prefix order:

`(A p₁, p₂ ∈ T :: p₁ ≼ p₂ ⟹ subtypes(p₂) ⊆ subtypes(p₁))`

Let `c ∈ subtypes(p₂)`, so `p₂ ≼ c`. We derive `p₁ ≼ c` inline from PrefixRelation's definition (ASN-0034): `p₁ ≼ p₂` means `#p₁ ≤ #p₂` and `(A j : 1 ≤ j ≤ #p₁ : p₂_j = p₁_j)`; `p₂ ≼ c` means `#p₂ ≤ #c` and `(A j : 1 ≤ j ≤ #p₂ : c_j = p₂_j)`. By transitivity of `≤` on naturals (NAT-order, ASN-0034), `#p₁ ≤ #c`. For positions `1 ≤ j ≤ #p₁`: since `#p₁ ≤ #p₂`, the range `1..#p₁` is contained in `1..#p₂`, so `c_j = p₂_j` (from the second agreement), and `p₂_j = p₁_j` (from the first), giving `c_j = p₁_j`. By PrefixRelation, `p₁ ≼ c`, i.e., `c ∈ subtypes(p₁)`. A query rooted at a shallower type address therefore subsumes the matches of any query rooted at one of its descendants — the subtype intervals nest in the same direction as the prefix order they encode.

Gregory documents this in the bootstrap document's type registry: `MARGIN` at address `1.0.2.6.2` is hierarchically nested under `FOOTNOTE` at `1.0.2.6`. A query for all footnote-family links, expressed as a span query rooted at `1.0.2.6`, matches both types because `1.0.2.6.2` lies within `[1.0.2.6, 1.0.2.7)`. The subtyping mechanism is the tumbler ordering itself — no separate hierarchy data structure is needed.


## Link Distinctness and Permanence

We now establish the identity semantics of links. The three requirements we began with — distinguishability, ownership, referenceability — crystallize into two derived properties.

**L11a — LinkUniqueness.** Distinct T10a-conforming allocation events produce distinct link addresses. Formally, for any pair of allocation events producing link addresses `a₁` and `a₂` in the system, if the events are distinct then `a₁ ≠ a₂` as tumblers. This is GlobalUniqueness (ASN-0034) instantiated at link addresses: its sole precondition is T10a-conformance of the events, and L1c (LinkAllocatorConformance) discharges precisely that — every `a ∈ dom(Σ.L)` is the terminus of a T10a-conforming chain.

Within-state single-valuedness (an address names at most one link) is immediate from the partial-function typing `Σ.L : T ⇀ Link`; L11a is the cross-event strengthening.

**L11b — NonInjectivity.** The link store imposes no injectivity constraint — multiple addresses may store the same endset sequence:

`(A Σ satisfying the state-local L- and S-invariants, a ∈ dom(Σ.L) :: (E Σ' extending Σ, a' ∈ dom(Σ'.L) :: a' ≠ a ∧ Σ'.L(a') = Σ.L(a) ∧ Σ' satisfies the state-local L- and S-invariants))`

— where "the state-local L- and S-invariants" denotes the per-state predicates L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, L14, L14a, L-fin, and ASN-0036's S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ — the same set FSP (FreshSiblingConformance) preserves. The derived L-lemmas (L2, L9, L10, L11b, L12a, L12b, L13) are consequences, not preconditions, so a state is not "checked against" them.

That is, for any conforming state `Σ` with a link at `a ∈ dom(Σ.L)` where `Σ.L(a) = (F, G, Θ)`, there exists a conforming extension `Σ'` (`Σ' ⊒ Σ`, StateExtension) with a fresh address `a' ∈ dom(Σ'.L)`, `a' ≠ a`, and `Σ'.L(a') = (F, G, Θ)`. The invariants *permit* non-injectivity — every state with a link can be extended to a non-injective state — but they do not *require* it.

*Construction of fresh `a'`.* By L1c on `Σ`, the existing link `a` is structurally producible from `home(a)`'s document-level prefix by a T10a-conforming chain. From `a`, enumerate the sibling stream `a⁽⁰⁾ = a, a⁽¹⁾ = inc(a⁽⁰⁾, 0), a⁽²⁾ = inc(a⁽¹⁾, 0), …` in `home(a)`'s link subspace at element field depth `#E(a) ≥ 2`. Each `inc(·, 0)` step is unconditionally T4-preserving (TA5a is unconditional for `k = 0`), so every `a⁽ⁱ⁾` is T4-valid. By L1b, the rightmost component is the ordinal (not the subspace identifier), so successive `inc(·, 0)` steps advance the ordinal while keeping `subspace_I(a⁽ⁱ⁾) = s_L`. By T0(a), the ordinal stream is unbounded.

By L-fin, `dom(Σ.L)` is finite, while the sibling stream `a⁽⁰⁾, a⁽¹⁾, a⁽²⁾, …` is infinite (T10a.7: the `inc(·, 0)` enumeration is injective). Hence some `a⁽ⁱ⁾` with `i ≥ 1` satisfies `a⁽ⁱ⁾ ∉ dom(Σ.L)`; take it. Set `a' = a⁽ⁱ⁾` and define `Σ'` by:

`Σ'.L = Σ.L ∪ {a' ↦ (F, G, Θ)}`, `Σ'.C = Σ.C`, `Σ'.M = Σ.M`.

`a' ≠ a` since `i ≥ 1`, and `a' ∉ dom(Σ.L)` by choice, discharging the freshness requirement directly.

*Conformance of `Σ'`.* This is another fresh-sibling extension, so we appeal to FSP (FreshSiblingConformance, stated under L9) for the shared invariant set, discharging its hypotheses for `a'` and payload `ℓ = (F, G, Θ) = Σ.L(a)`:

- (h1) `a' ∉ dom(Σ.L)` by the choice of `a'` above;
- (h2) `a'` is producible by the L1c chain for `a` extended by `i` sibling advances (each `k = 0`, unconditionally T4-preserving), with `home(a') = home(a) ∈ dom(Σ.M)` — sibling advance via `inc(·, 0)` preserves the document-level prefix (CPP with `t₀ = a`, `p = #home(a)`), and `home(a) ∈ dom(Σ.M)` by L1a on `Σ`;
- (h3) `subspace_I(a') = s_L` (L1b: the ordinal, not the subspace identifier, is the rightmost component, so `inc(·, 0)` fixes the subspace); `zeros(a') = zeros(a) = 3` (each `inc(·, 0)` modifies only the terminal `sig` position by TA5(c)/TA5-SigValid, adding no separator zero); `#E(a') = #E(a) ≥ 2` (by `#a' = #a` from T10a.1 UniformSiblingLength, `#home(a') = #home(a)` from CPP, and L1b on `Σ`); T4-valid by T10a.4.

The payload `ℓ = (F, G, Θ) = Σ.L(a)` has T12-well-formed spans (inherited from the conforming link `a` by L4 on `Σ`) and satisfies L3 (arity ≥ 3, slot 3 the non-empty type endset, by L3 on `Σ`). By FSP, `Σ'` satisfies every state-local L- and S-invariant, and the `Σ → Σ'` transition satisfies L12 and L12a. The L11b-specific delta is the *endset equality* `Σ'.L(a') = (F, G, Θ) = Σ.L(a)`, which holds by construction — this is the non-injectivity witness, not an invariant.

Two links with identical endsets — same from, same to, same type — but different addresses are separate objects, independently owned, independently removable, independently targetable by other links.

**L12 — LinkImmutability.** Once created, a link's address persists and its value is permanently fixed:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`. This parallels S0 (ContentImmutability, ASN-0036) in both halves: the address endures, and the value at that address — the triple of endsets — never changes.

The evidence is unambiguous. Nelson's FEBE protocol defines exactly five link operations: MAKELINK (create), FINDLINKSFROMTOTHREE (search), FINDNUMOFLINKSFROMTOTHREE (count), FINDNEXTNLINKSFROMTOTHREE (paginate), and RETRIEVEENDSETS (read). There is no MODIFYLINK, UPDATELINK, or EDITENDSETS. The only write operation is creation; the rest are queries. Gregory confirms at the implementation level: `insertendsetsinorgl` and `insertendsetsinspanf` are called exclusively from `docreatelink`; no other code path writes to the link's orgl or spanfilade entries. The link orgl is written once by `createorglingranf` and never touched again.

Link immutability follows from the same principle that makes content immutable: others may have linked to it. Since links are first-class objects with tumbler addresses, other links can point to them (L13). Modifying a link's endsets after creation would silently change the meaning of every meta-link pointing to it — violating the permanence guarantee. To effectively change a connection, the owner creates a new link via MAKELINK with the desired endsets. The old link persists in `Σ.L` by L12; the new link gets a fresh address in creation order. Immutability is not removal: how an old link ceases to be discoverable or resolvable is a question about operations, deferred to Open Questions.

**L12a — LinkStoreMonotonicity.** The domain of the link store is monotonically non-decreasing:

`[dom(Σ.L) ⊆ dom(Σ'.L)]`

for every state transition `Σ → Σ'`. This is the direct corollary of L12, paralleling S1 (StoreMonotonicity) for the content store.

**L12b — HomeDocumentPersistence.** The home documents of all existing links remain allocated across every state transition:

`(A Σ, Σ' : Σ → Σ' :: {home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M))`

*Derivation.* Let `a ∈ dom(Σ.L)`. By L12a, `a ∈ dom(Σ'.L)`. Applying L1a (LinkScopedAllocation) to `Σ'`: `home(a) ∈ dom(Σ'.M)`. The inclusion `{home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M)` follows by set-builder closure over `dom(Σ.L) ⊆ dom(Σ'.L)`.

This is the link-side dual of S7a's persistence guarantee for content-bearing documents.


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

**L14 — DualPrimitive.** The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses — they relate V-positions to I-addresses — but V-positions are not entities in their own right. The two domains are disjoint over the `s_C`-resident slice of content (L0a):

`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`

— no address holds both a link and `s_C`-resident content (L0a).

Nelson: "In the present implementation, the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." Documents, accounts, servers, and nodes are organizational concepts — positions in the tumbler hierarchy that structure the address space — but they have no stored representation. Only content and links occupy storage.

Gregory confirms with emphasis: the granfilade's union type has exactly two variants (`GRANTEXT` and `GRANORGL`), the hint mechanism accepts exactly two atom types (`TEXTATOM = 1` and `LINKATOM = 2`), and the Vstream within each document is partitioned into exactly two regions (text at `1.x`, links at `2.x`). No third category exists.

The two primitives are peers. Both have permanent tumbler addresses. Both are stored in the same master index (the granfilade). Both support the same addressing and containment mechanisms. But they are categorically different:

| | Content | Links |
|---|---|---|
| State component | `Σ.C : T ⇀ Val` | `Σ.L : T ⇀ Link` |
| Subspace | `s_C` | `s_L` |
| Payload | Opaque values (bytes) | Structured endset sequences (N ≥ 3; standard triple by convention, slot 3 the type) |
| Sharing | Transcludable — same I-address in multiple arrangements (S5) | Non-transcludable — arrangements cannot map to link addresses (L14a) |
| Address determines | Content origin (S7) | Link home and owner (L2) |

Content identity is *shareable*: the same I-address can appear in the arrangements of multiple documents via transclusion, and this sharing is the mechanism for content reuse (S5, ASN-0036). Link identity is *non-transcludable*: no arrangement may map a V-position to a link address. We state this as an explicit invariant:

**L14a — NonTranscludability.** In any system whose content is `s_C`-resident (`(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`):

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`

A connection is an assertion by a specific principal about specific content, and assertions are not transferable by reference. A link at address `a` is homed in `home(a)` and owned by the principal of `home(a)` — period. It cannot be transcluded into another owner's authority.

This is discharged by S3 together with L0+L0a: S3 (ReferentialIntegrity, ASN-0036) requires `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`; the `s_C`-residence hypothesis places `Σ.M(d)(v)` in `dom(Σ.C)|_{s_C}`; and L0+L0a establish `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`, so no V-position image can be a link address.


## Summary of the Link Model

A link is an addressed, owned, typed, bidirectional connection between arbitrary spans of content in the tumbler space. More precisely:

A link at address `a ∈ dom(Σ.L)` is characterized by:

- **Address** `a` — a permanent, globally unique element-level tumbler in the link subspace (L0, L1, L11a, L12). The address IS the link's identity.
- **Home** `home(a)` — the document-level prefix extracted from `a` via T4 field parsing, determining the link's owner, independent of what the link connects (L2).
- **N ≥ 3 endsets** — each link carries at least three endsets, with slot 3 the type endset (L3). The standard triple `Σ.L(a) = (F, G, Θ)` — from-endset `F`, to-endset `G`, and type-endset `Θ` — is the floor; each endset is a finite set of well-formed spans pointing anywhere in the tumbler space (L4, L5).
- **Slot structure** — endsets occupy structurally distinguished positions, enabling independent query on each, with directional semantics determined by the type rather than by the slot itself (L6, L7).
- **Type semantics** — the type endset is matched by address, not by content; it may reference ghost addresses; and hierarchical type relationships follow from tumbler containment (L8, L9, L10).


## Worked Example

We construct a minimal conforming state to verify that L0–L14 hold simultaneously.

**Setup.** Node 1, user 1, document 1. The content subspace identifier is `s_C = 1`, the link subspace identifier is `s_L = 2`, and the ghost-type subspace identifier is `s_X = 3` — a fresh subspace disjoint from both `s_C` and `s_L`, used only by the type endset of the link below.

Content addresses have element field starting with 1; link addresses have element field starting with 2. The document prefix is `1.0.1.0.1`.

**Content store.** Two content characters at addresses:

- `c₁ = 1.0.1.0.1.0.1.1` — first character, element field `1.1`
- `c₂ = 1.0.1.0.1.0.1.2` — second character, element field `1.2`

So `Σ.C = {c₁ ↦ v₁, c₂ ↦ v₂}` for some values `v₁, v₂ ∈ Val`.

**Arrangement.** One document `d = 1.0.1.0.1` with `Σ.M(d) = {[1.1] ↦ c₁, [1.2] ↦ c₂}` (V-positions are element-field tumblers within the document).

**Link store.** One link — a citation from `c₁` to `c₂` with a ghost type — at address:

- `a = 1.0.1.0.1.0.2.1` — element field `2.1` (subspace 2, ordinal 1)

Choose a ghost type address `g = 1.0.1.0.1.0.3.1` — an element-level tumbler in the same document `d` as the link, with element field `[s_X, 1] = [3, 1]`, so `subspace_I(g) = 3 = s_X`. We verify `g ∉ dom(Σ.C) ∪ dom(Σ.L)` by direct enumeration in the L9 step below — `Σ`'s content store and link store are each enumerable as small finite sets in this state, so the verification proceeds by T7 against each entry. Define:

All addresses here have depth 8, so the unit-depth displacement is `δ(1, 8) = [0, 0, 0, 0, 0, 0, 0, 1]`.

- From-endset: `F = {(c₁, δ(1, 8))}` (action point `k = 8 = #c₁`, unit width)
- To-endset: `G = {(c₂, δ(1, 8))}`
- Type-endset: `Θ = {(g, δ(1, 8))}`

So `Σ.L = {a ↦ (F, G, Θ)}`.

**Verification.**

*L0 (SubspacePartition).* `subspace_I(a) = 2 = s_L`, `subspace_I(c₁) = subspace_I(c₂) = 1 = s_C`; by the L0a discharge (with `zeros = 3` per side and distinct subspaces), `a ≠ c₁` and `a ≠ c₂`, so `dom(Σ.L) ∩ dom(Σ.C) = ∅`. ✓

*L1 (LinkElementLevel).* `zeros(a) = zeros(1.0.1.0.1.0.2.1) = 3`. ✓

*L1a (LinkScopedAllocation).* `home(a) = 1.0.1.0.1 = d`, the creating document; `d ∈ dom(Σ.M)` since `Σ.M(d) = {[1.1] ↦ c₁, [1.2] ↦ c₂}` is defined above — `d` is an allocated, owned document. ✓

*L1b (LinkElementFieldDepth).* `E(a) = [2, 1]`, so `#E(a) = 2 ≥ 2`. ✓

*L1c (LinkAllocatorConformance).* The link address `a = 1.0.1.0.1.0.2.1` is producible by a T10a-conforming allocator from the document prefix `d = 1.0.1.0.1` (taken as the L1c seed `s = d`; T4-valid with `zeros(s) = 2`): (i) `inc(s, 2)` → `1.0.1.0.1.0.1` — element depth 1, subspace 1 (`k₁ = 2` with `zeros(s) = 2`, satisfying TA5a: `k = 2` requires `zeros ≤ 2`); (ii) `inc(1.0.1.0.1.0.1, 0)` → `1.0.1.0.1.0.2` — sibling advance to subspace 2 (`k₂ = 0`, unconditionally T4-preserving, zero count preserved at 3); (iii) `inc(1.0.1.0.1.0.2, 1)` → `1.0.1.0.1.0.2.1` = `a` — child at depth 2 (`k₃ = 1`; TA5a is unconditional for `k ∈ {0, 1}`; the output has `zeros(a) = 3`). Each step conforms to T10a; only the first step is `kᵢ = 2` (TA5a's `zeros ≤ 2` precondition fires once at `k₁ = 2` and cannot fire again, since `zeros(t₁) = 3` thereafter). Chain shape: `t₀ = s = d` (the T4-valid document-level seed); `k₁ = 2`; intermediate lengths are `#t₁ = #t₂ = 7 > 5 = #s` and `#t₃ = #a = 8 > 5` — every step after the seed operates above `#s`. Postconditions: T4-validity of `a` follows from T10a.4 along the chain; `s = home(a) = 1.0.1.0.1` follows from CPP (the third zero of `a` first appears at position `#s + 1 = 6`, the one seated by `k₁ = 2`). ✓

*L-fin (LinkStoreFiniteness) at `Σ` (state-local).* `|dom(Σ.L)| = 1`, which is finite. ✓

*L2 (OwnershipEndsetIndependence).* `home(a) = 1.0.1.0.1`, computed from the field structure of `a` alone. The endsets `(F, G, Θ)` are not consulted. ✓

*L3 (NEndsetStructure).* `|Σ.L(a)| = 3 ≥ 3`, slot 3 is the type endset `Θ = {(g, δ(1, 8))} ≠ ∅`, and each endset is in `𝒫_fin(Span)`. ✓

*L4 (EndsetGenerality).* Each span is well-formed by T12: for `(c₁, δ(1, 8))`, `δ(1, 8) > 0` and the action point `k = 8 ≤ #c₁ = 8`. Similarly for the other spans. Start addresses are in `T`. ✓

*L5 (EndsetSetSemantics).* Each endset is a singleton set — set semantics hold trivially. ✓

*L6 (SlotDistinction).* `Σ.L(a) = (F, G, Θ)` is a 3-tuple of endsets, with positional accessors `Σ.L(a).e₁ = F`, `Σ.L(a).e₂ = G`, `Σ.L(a).e₃ = Θ` well-defined. Standard-triple consequence: since `F ≠ G`, `(F, G, Θ) ≠ (G, F, Θ)` by component-wise tuple inequality at slot 1. ✓

*L7 (DirectionalFlexibility) — illustration.* L6 distinguishes the link `(F, G, Θ)` from its slot-swap `(G, F, Θ)` as structurally distinct values, but no L-invariant determines whether `F` carries the "source" role and `G` the "target" role. The labels `F`, `G` in the standard triple are nominal — chosen above for prose convenience because the link was introduced as "a citation from `c₁` to `c₂`," but the structural part of that introduction is only that slot 1 holds `{(c₁, δ(1, 8))}` and slot 2 holds `{(c₂, δ(1, 8))}`. Whether reading slot 1 as "source" matches Nelson's directional convention depends entirely on the type at `g`; under a counterpart or equivalence type, the same `(F, G, Θ)` carries no directional weight at all (per L7). ✓

*L11a (LinkUniqueness).* `a` was produced by forward allocation. With `|dom(Σ.L)| = 1`, no collision is possible. ✓

*L11b (NonInjectivity).* The clause applies: `a ∈ dom(Σ.L)` satisfies the universal quantifier's precondition. The extension `Σ'` witnessing the existential is constructed in Step 1 below, where `a'` is allocated with `Σ_1.L(a') = Σ.L(a)`. ✓

*L12 (LinkImmutability).* L12 constrains state transitions, not individual states. In this single-state example, no transition is under consideration, so L12 is vacuously satisfied. Verified non-vacuously below across two transitions. ✓ (vacuous)

*L12a (LinkStoreMonotonicity).* Similarly a transition invariant, vacuously satisfied here. Verified non-vacuously below. ✓ (vacuous)

*L14 (DualPrimitive).* `dom(Σ.C) ∪ dom(Σ.L) = {c₁, c₂, a}`. All stored entities. `dom(Σ.C) ∩ dom(Σ.L) = ∅`. ✓

*L14a (NonTranscludability).* `ran(Σ.M(d)) = {c₁, c₂}`. For each `v ∈ dom(Σ.M(d))`: `Σ.M(d)(v) ∈ {c₁, c₂} ⊆ dom(Σ.C)`, and `dom(Σ.L) = {a}` with `a ∉ {c₁, c₂}` (by L0). So `Σ.M(d)(v) ∉ dom(Σ.L)`. ✓

*L10 (TypeHierarchyByContainment).* For the ghost type at `g = 1.0.1.0.1.0.3.1`, define a parent type `p = 1.0.1.0.1.0.3` with displacement `δ(1, 7) = [0, 0, 0, 0, 0, 0, 1]` (action point `k = 7 = #p`). The coverage of `(p, δ(1, #p))` is `{t : p ≤ t < shift(p, 1)} = {t : 1.0.1.0.1.0.3 ≤ t < 1.0.1.0.1.0.4}`. Since `g = 1.0.1.0.1.0.3.1` and `p ≼ g`, by T1(ii) `g ≥ p`, and `g < 1.0.1.0.1.0.4` because `g` agrees with `p` at position 7 (both have value 3) while `inc(p, 0)` has value 4 there. So `g ∈ coverage({(p, δ(1, #p))})` — a single span query at `p` matches the subtype at `g`. ✓

*L9 (TypeGhostPermission).* The type endset references `g = 1.0.1.0.1.0.3.1` with `subspace_I(g) = 3 = s_X`. *Direct enumeration.* `dom(Σ.C) = {c₁, c₂}` with `subspace_I(c₁) = subspace_I(c₂) = 1 = s_C`; since `s_X = 3 ≠ 1 = s_C`, T7 applied to each pair gives `g ≠ c₁` and `g ≠ c₂`, so `g ∉ dom(Σ.C)`. `dom(Σ.L) = {a}` with `subspace_I(a) = 2 = s_L`; since `s_X = 3 ≠ 2 = s_L`, T7 gives `g ≠ a`, so `g ∉ dom(Σ.L)`. Therefore `g ∉ dom(Σ.C) ∪ dom(Σ.L)` — verified by enumeration over the (finite) content and link stores of this state, with T7's hypotheses (T4-validity and equal zero counts) discharged for each pair via S7b on content addresses and L1 + L1c's T4-validity postcondition on the link address. The L9 lemma applies to this state because its `s_C`-residence precondition is satisfied (`subspace_I(c₁) = subspace_I(c₂) = s_C`), so this state lies within L9's scope; the direct enumeration shown here can also be read as discharging L9's conclusion in this state without routing through the lemma. ✓

*L8 (TypeByAddress) at `Σ` — reflexivity.* The single-link state admits a non-vacuous reflexivity check: `same_type(a, a) ⟺ coverage(Σ.L(a).type) = coverage(Σ.L(a).type)`. The right-hand side is a set-equality of identical sets, true by reflexivity. To exhibit the actual coverage concretely, `Σ.L(a).type = Θ = {(g, δ(1, 8))}`; since `#g = 8`, PrefixSpanCoverage applies, giving `coverage({(g, δ(1, 8))}) = {t ∈ T : g ≼ t}` — the set of all tumblers extending `g`. This is the address set against which any other link's type would be compared under L8's coverage-equality criterion. ✓

*S3 (ReferentialIntegrity, ASN-0036).* `ran(Σ.M(d)) = {c₁, c₂} ⊆ dom(Σ.C)`. ✓

*S7a (DocumentScopedAllocation, ASN-0036).* For each content address: `N(c₁).0.U(c₁).0.D(c₁) = 1.0.1.0.1 = d ∈ dom(Σ.M)`, and identically for `c₂`. Both content addresses sit under their allocated home document. ✓

*S7b (ElementLevelIAddresses, ASN-0036).* `zeros(c₁) = zeros(1.0.1.0.1.0.1.1) = 3` and `zeros(c₂) = zeros(1.0.1.0.1.0.1.2) = 3`; both T4-valid (no adjacent zeros, every non-separator component positive). T4b's projections `N, U, D, E` are therefore well-defined on each. ✓

*S7d (DocumentAllocationDiscipline, ASN-0036).* `dom(Σ.M) = {d}` with `d = 1.0.1.0.1`; `zeros(d) = 2`, T4-valid; `d` is producible by a single `inc(r, 2)` allocation event from a user-level root `r = 1.0.1` (`zeros(r) = 1 ≤ 2`, satisfying TA5a's side condition for `k' = 2`): `inc(1.0.1, 2)` appends one separator zero and a final `1`, yielding `1.0.1.0.1 = d` (or `d` is reached along a T10a-conforming chain from 𝒯's `zeros = 0` node root), so `d` is a T10a-allocated node in 𝒯. ✓

*S8a (VPositionWellFormedness, ASN-0036).* The V-positions of `Σ.M(d)` are `{[1.1], [1.2]}`; each V-position is an element-field tumbler whose subspace component is `1 = s_C`, restricting `Σ.M(d)` to the content subspace's V-position slice. ✓

*S8-depth (FixedDepthVPositions, ASN-0036).* Each V-position of `Σ.M(d)` has element-field depth `2`: `#[1.1] = #[1.2] = 2 ≥ 2`. ✓

*D-CTG (VContiguity, ASN-0036).* The V-position set `V_1(d) = dom(Σ.M(d)) = {[1, 1], [1, 2]}` is contiguous along its second component at fixed subspace `1`: positions `[1, 1]` and `[1, 2]` cover `{[1, k] : 1 ≤ k ≤ 2}` with no gaps. ✓

*D-MIN (VMinimumPosition, ASN-0036).* `min(V_1(d)) = [1, 1]` — the lexicographically least V-position in `V_1(d)` is the canonical start position `[1, 1]`. ✓

*D-SEQ (SequentialPositions, ASN-0036).* `V_1(d) = {[1, k] : 1 ≤ k ≤ 2}` is a contiguous arithmetic sequence of element-field tumblers at depth 2, starting at the D-MIN witness `[1, 1]` and advancing by `inc(·, 0)` to `[1, 2]`. ✓

**Extension: L11b non-injectivity, L13, and transition verification.**

We extend the state in four steps, naming each intermediate state, to verify L11b, L12, L13, and the higher-arity/discrimination behavior of L3/L6/L8 non-vacuously.

*Each added link is a fresh sibling.* Each of `a'`, `a₂`, `a₃`, `a₄` is the next `inc(·, 0)` sibling of the previous link; FSP applies, so only the new check per step is shown below.

*Step 1: adding `a'`.* Define `a' = 1.0.1.0.1.0.2.2` with `Σ_1.L(a') = (F, G, Θ)` — same endsets as `a`. The intermediate state is `Σ_1` with `Σ_1.L = {a ↦ (F, G, Θ),\; a' ↦ (F, G, Θ)}`, `Σ_1.C = Σ.C`, `Σ_1.M = Σ.M`. The state-local invariants hold by the fresh-sibling argument above.

*L11b non-injectivity in `Σ_1`.* `|dom(Σ_1.L)| = 2`, `a ≠ a'`, and `Σ_1.L(a) = Σ_1.L(a') = (F, G, Θ)`. The link store is non-injective — two distinct addresses map to the same triple. This is the witness for L11b applied to `Σ` with `a`. ✓

*L12 across `Σ → Σ_1` (transition).* `dom(Σ.L) = {a}`. We verify: `a ∈ dom(Σ_1.L)` and `Σ_1.L(a) = (F, G, Θ) = Σ.L(a)`. The sole pre-existing link is preserved. ✓

*L12a across `Σ → Σ_1` (transition).* `dom(Σ.L) = {a} ⊆ {a, a'} = dom(Σ_1.L)`. ✓

*Step 2: adding the meta-link `a₂`.* Define `a₂ = 1.0.1.0.1.0.2.3` — a meta-link whose from-endset references the first link `a`.

Define the span targeting `a`: `δ(1, 8) = [0, 0, 0, 0, 0, 0, 0, 1]` has action point `k = 8 = #a`, and `k ≤ #a` holds, so `(a, δ(1, 8))` is well-formed by T12. ✓

Define the meta-link:

- From-endset: `F₂ = {(a, δ(1, 8))}` — pointing at the first link
- To-endset: `G₂ = {(c₂, δ(1, 8))}` — pointing at content
- Type-endset: `Θ₂ = {(g, δ(1, 8))}` — same ghost type

The final state is `Σ_2` with `Σ_2.L = {a ↦ (F, G, Θ),\; a' ↦ (F, G, Θ),\; a₂ ↦ (F₂, G₂, Θ₂)}`, `Σ_2.C = Σ_1.C`, `Σ_2.M = Σ_1.M`.

*L13 (ReflexiveAddressing).* The from-endset of `a₂` contains the span `(a, δ(1, 8))` where `a ∈ dom(Σ_2.L)`. This is a concrete link-to-link reference — `a₂`'s from-endset targets the link entity at `a`. ✓

*L0 for `a₂`.* `subspace_I(a₂) = 2 = s_L`. The from-endset span `(a, δ(1, 8))` references `a` with `subspace_I(a) = 2 = s_L` — a same-subspace reference from `s_L` to `s_L`, permitted by L4. ✓

*L4 for `a₂`.* The span `(a, δ(1, 8))` has `a ∈ T` and satisfies T12 (verified above). No constraint prevents the span from referencing a link-subspace address. ✓

The remaining state-local invariants at `Σ_2` (L0, L1, L1a–c, L3, L5, L6, L11a, L14, L14a, L-fin) hold for the new entry `a₂` by the fresh-sibling argument above (`a₂ = 1.0.1.0.1.0.2.3` is the next sibling after `a'`), and for the pre-existing entries `a, a'` by L12.

*L12 across `Σ_1 → Σ_2` (transition).* `dom(Σ_1.L) = {a, a'}`. For `a`: `a ∈ dom(Σ_2.L)` and `Σ_2.L(a) = (F, G, Θ) = Σ_1.L(a)`. For `a'`: `a' ∈ dom(Σ_2.L)` and `Σ_2.L(a') = (F, G, Θ) = Σ_1.L(a')`. Both pre-existing links are preserved. ✓

*L12a across `Σ_1 → Σ_2` (transition).* `dom(Σ_1.L) = {a, a'} ⊆ {a, a', a₂} = dom(Σ_2.L)`. ✓

*Step 3: adding the arity-4 faceted link `a₃`.* The standard triple (from, to, type) suffices for binary relational connections, but L3 admits `N ≥ 3` to support Nelson's 4-sets, 5-sets, and n-sets [LM 4/79]. We construct an arity-4 link to exercise L3, L6, and L8 in the higher-arity regime. Define `a₃ = 1.0.1.0.1.0.2.4` — the next sibling in the link subspace after `a₂` (sibling advance from `a₂ = 1.0.1.0.1.0.2.3` via `inc(·, 0)` to `1.0.1.0.1.0.2.4`, unconditionally T4-preserving).

Suppose `a₃` connects an annotated passage (`c₁`) to a discussion (`c₂`), under a ghost type (`g`), with a fourth endset recording a supporting reference back to the original meta-link (`a₂`). Define the four endsets:

- Slot 1 (from): `F₃ = {(c₁, δ(1, 8))}` — the annotated content
- Slot 2 (to): `G₃ = {(c₂, δ(1, 8))}` — the discussion content
- Slot 3 (type): `Θ₃ = {(g, δ(1, 8))}` — the ghost type, by L3's slot-3 convention
- Slot 4 (supporting reference): `R₃ = {(a₂, δ(1, 8))}` — a fourth endset whose semantic role is determined by the type at `g`, outside this ASN's scope

The final state is `Σ_3` with `Σ_3.L = Σ_2.L ∪ {a₃ ↦ (F₃, G₃, Θ₃, R₃)}`, `Σ_3.C = Σ_2.C`, `Σ_3.M = Σ_2.M`.

*L3 (NEndsetStructure) at arity 4.* `|Σ_3.L(a₃)| = 4 ≥ 3`, and each `eᵢ ∈ Endset` since each is a singleton set of T12-well-formed spans. Slot 3 is the type endset (Θ₃ = `{(g, δ(1, 8))}` ≠ ∅) by L3's slot-3 convention, which fixes the role of position 3 uniformly for every arity `N ≥ 3` and requires non-emptiness there. ✓

*L6 (SlotDistinction) at arity 4.* `Σ_3.L(a₃) = (F₃, G₃, Θ₃, R₃)` is a 4-tuple of endsets with positional accessors `Σ_3.L(a₃).eᵢ` well-defined for `i ∈ {1, 2, 3, 4}`. The four entries have pairwise-distinct start addresses across slots (`c₁`, `c₂`, `g`, `a₂` are four distinct tumblers), so the transposition `π = (1 2)` yields `(G₃, F₃, Θ₃, R₃) ≠ (F₃, G₃, Θ₃, R₃)` (slot 1 differs) and `π = (1 4)` yields `(R₃, G₃, Θ₃, F₃) ≠ (F₃, G₃, Θ₃, R₃)` (slot 1 differs) — slot positions are addressable distinctly at arity 4. ✓

*L8 (TypeByAddress) at arity 4.* `Σ_3.L(a₃).type = Σ_3.L(a₃).e₃ = Θ₃ = {(g, δ(1, 8))}` — the `.type` accessor resolves to slot 3 unambiguously under the StandardTriple convention extended to arity 4 by L3. For the existing arity-3 link `a` with `Σ_3.L(a).type = Σ_3.L(a).e₃ = Θ = {(g, δ(1, 8))}`, coverage-based matching gives `same_type(a, a₃) ⟺ coverage(Σ_3.L(a).e₃) = coverage(Σ_3.L(a₃).e₃)`. Both endsets are `{(g, δ(1, 8))}` (a unit-depth span at `g`), so by PrefixSpanCoverage each has coverage `{t ∈ T : g ≼ t}` — the two coverage sets are identical. The arity-3 and arity-4 links share a type without any need to inspect content at `g`. ✓

The remaining state-local invariants at `Σ_3` (L0, L1, L1a–c, L5, L11a, L14, L14a, L-fin; L3 and L6 verified above at arity 4) hold for the new entry `a₃` by the fresh-sibling argument above (`a₃ = 1.0.1.0.1.0.2.4` is the next sibling after `a₂`, payload arity 4 with non-empty slot 3), and for the pre-existing entries by L12.

*L12 across `Σ_2 → Σ_3` (transition).* All three prior entries `Σ_2.L(a), Σ_2.L(a'), Σ_2.L(a₂)` are unchanged in `Σ_3`; only the new entry at `a₃` is added. ✓

*L12a across `Σ_2 → Σ_3` (transition).* `dom(Σ_2.L) = {a, a', a₂} ⊆ {a, a', a₂, a₃} = dom(Σ_3.L)`. ✓

*Step 4: adding `a₄` with a distinct ghost type — exercising L8 discrimination.* Steps 1-3 share a single ghost type at `g`, so the only L8 check available across that history is the reflexive one (`same_type(a, a)` and the `coverage(Θ) = coverage(Θ')` illustration at Σ — both equality cases). L8's substantive content is *discrimination*: distinguishing same-type from different-type links by address coverage. We add a fifth link `a₄` whose type endset targets a *different* ghost type `g'`, and verify `same_type(a, a₄) = false`.

Define `g' = 1.0.1.0.1.0.3.2` — a sibling of `g = 1.0.1.0.1.0.3.1` in subspace `s_X`. By construction: `subspace_I(g') = 3 = s_X` (so `g' ∉ dom(Σ_3.C) ∪ dom(Σ_3.L)` by L0, since `s_X ∉ {s_C, s_L}` — the ghost is structurally outside the stored entities, by the same subspace-separation argument that placed `g` outside `Σ`'s stores); T4-validity holds (`zeros(g') = 3`, no adjacent zeros at the appended `[0, 3, 2]` tail since the inherited last component of `d = 1.0.1.0.1` is `1 > 0`, and the trailing component `2 > 0`); `#g' = 8`. The sibling step `g → g'` is `inc(g, 0)` (`k = 0`, unconditionally T4-preserving by TA5a), so `g'` is a structurally well-formed ghost address in `s_X`.

Define `a₄ = 1.0.1.0.1.0.2.5` — the next sibling in the link subspace after `a₃`, by `inc(a₃, 0)`. Define the endsets:

- From-endset: `F₄ = {(c₁, δ(1, 8))}`
- To-endset: `G₄ = {(c₂, δ(1, 8))}`
- Type-endset: `Θ₄ = {(g', δ(1, 8))}` — targeting `g'`, *not* `g`

The final state is `Σ_4` with `Σ_4.L = Σ_3.L ∪ {a₄ ↦ (F₄, G₄, Θ₄)}`, `Σ_4.C = Σ_3.C`, `Σ_4.M = Σ_3.M`.

*L8 (TypeByAddress) at `Σ_4` — discrimination.* `Σ_4.L(a).type = Θ = {(g, δ(1, 8))}` and `Σ_4.L(a₄).type = Θ₄ = {(g', δ(1, 8))}`. By PrefixSpanCoverage applied to each (using `#g = #g' = 8`, so `δ(1, 8)` is the unit-depth displacement at the action point at the tail):

- `coverage({(g, δ(1, 8))}) = {t ∈ T : g ≼ t}`
- `coverage({(g', δ(1, 8))}) = {t ∈ T : g' ≼ t}`

These two prefix sets are disjoint. Suppose `t` extends both: `g ≼ t` and `g' ≼ t`. Then `t` agrees with `g` and with `g'` at all positions `1..8`, so `t_8 = g_8 = 1` and simultaneously `t_8 = g'_8 = 2` — contradiction. Hence `coverage(Θ) ∩ coverage(Θ₄) = ∅`, and a fortiori `coverage(Θ) ≠ coverage(Θ₄)`. By L8's defining biconditional, `same_type(a, a₄) ⟺ coverage(Σ_4.L(a).type) = coverage(Σ_4.L(a₄).type)`, and the right-hand side is false; therefore `same_type(a, a₄) = false`. ✓

The discrimination is structural: `g` and `g'` differ only at the tail (position 8), but that single divergence forces their prefix-cone coverages to be disjoint — sibling ghost addresses generate sibling type cones, neither containing the other. This is the structural counterpart to the earlier reflexivity check: same-coverage links match (e.g., `a ↦ Θ` and `a' ↦ Θ` with identical `Θ` give `same_type(a, a') = true`); disjoint-coverage links discriminate (e.g., `a ↦ Θ` and `a₄ ↦ Θ₄` give `same_type(a, a₄) = false`).

The remaining state-local invariants at `Σ_4` (L0, L1, L1a–c, L3, L5, L6, L11a, L14, L14a, L-fin) hold for the new entry `a₄` by the fresh-sibling argument above (`a₄ = 1.0.1.0.1.0.2.5` is the next sibling after `a₃`), and for the pre-existing entries by L12.

*L12 across `Σ_3 → Σ_4` (transition).* All four prior entries `Σ_3.L(a), Σ_3.L(a'), Σ_3.L(a₂), Σ_3.L(a₃)` are unchanged in `Σ_4`; only the new entry at `a₄` is added. ✓

*L12a across `Σ_3 → Σ_4` (transition).* `dom(Σ_3.L) = {a, a', a₂, a₃} ⊆ {a, a', a₂, a₃, a₄} = dom(Σ_4.L)`. ✓


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| Σ.L | DEF | `Σ.L : T ⇀ Link` — the link store, mapping addresses to link values | introduced |
| L-fin | INV | LinkStoreFiniteness — `|dom(Σ.L)| < ∞` for each reachable state; parallels S8-fin (ASN-0036) | introduced |
| L0 | INV | SubspacePartition — link addresses occupy subspace `s_L`: `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)`; together with L0a yields the scoped disjointness `dom(Σ.L) ∩ dom(Σ.C)\|_{s_C} = ∅` via T7 | introduced |
| L0a | DEF | ContentSubspaceScope — `dom(Σ.C)\|_{s_C} = {a ∈ dom(Σ.C) : subspace_I(a) = s_C}` is the `s_C`-resident slice of content; the disjointness `dom(Σ.L) ∩ dom(Σ.C)\|_{s_C} = ∅` is derived in-place via L0 + T7 (the L0a discharge) | introduced |
| L1 | INV | LinkElementLevel — every link address is an element-level tumbler: `(A a ∈ dom(Σ.L) :: zeros(a) = 3)` | introduced |
| L1a | INV | LinkScopedAllocation — every link address is allocated under the creating document's tumbler prefix | introduced |
| L1b | INV | LinkElementFieldDepth — every link address has element field depth ≥ 2: `(A a ∈ dom(Σ.L) :: #E(a) ≥ 2)` | introduced |
| L1c | AXIOM | LinkAllocatorConformance — link allocation conforms to T10a (AllocatorDiscipline, ASN-0034); every link address is the T4-valid terminus of a T10a-conforming chain seeded at its document-level prefix (full statement and postconditions in body) | introduced |
| CPP | LEMMA | ChainPrefixPreservation (local) — along a T10a-conforming chain of T4-valid tumblers whose every step modifies only positions beyond a fixed length `p ≤ #t₀`, the terminus agrees with `t₀` on positions `1..p` | introduced |
| FSP | LEMMA | FreshSiblingConformance (local) — appending one fresh sibling link `a` (h1 freshness, h2 producibility, h3 shape) carrying any L3-conforming payload, with `Σ'.C = Σ.C` and `Σ'.M = Σ.M`, preserves every state-local L- and S-invariant and satisfies the `Σ → Σ'` transition invariants L12/L12a; leaves `coverage(ℓ.type)` unconstrained | introduced |
| L2 | LEMMA | OwnershipEndsetIndependence — `home(a)` depends only on `a`, not on the link's endsets | introduced |
| L3 | INV | NEndsetStructure — every link has at least three endsets, with slot 3 a non-empty type endset: `\|Σ.L(a)\| ≥ 3 ∧ Σ.L(a).e₃ ≠ ∅`; arity 3 `(F, G, Θ)` is the standard triple, higher arity admitted | introduced |
| L4 | META | EndsetGenerality — the model imposes no constraint on endset spans beyond T12 well-formedness (definitional from L3): no single-document, content-only, or existence restriction | introduced |
| L5 | INV | EndsetSetSemantics — an endset is an unordered set; only span membership matters | introduced |
| L6 | INV | SlotDistinction — endsets within a link are addressable by positional accessor `Σ.L(a).eᵢ`; dual to L5 (no positional accessor within an endset); link equality is component-wise tuple equality; standard-triple consequence: `F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ)` | introduced |
| L7 | META | DirectionalFlexibility — L0–L14 and L-fin impose no constraint on directional significance of from/to slots | introduced |
| L8 | DEF | TypeByAddress — type matching is by address coverage: `same_type(a₁, a₂) ⟺ coverage(Σ.L(a₁).type) = coverage(Σ.L(a₂).type)`; `.type` is slot 3, well-defined by L3 | introduced |
| L9 | LEMMA | TypeGhostPermission — any conforming state with `dom(Σ.M) ≠ ∅` and `s_C`-resident content (`(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`) can be extended, for every arity `N ≥ 3`, with a link of arity `N` whose type endset references addresses outside `dom(Σ.C) ∪ dom(Σ.L)`; arity-3 witness `(∅, ∅, {(g, δ(1, #g))})` extends to higher arities by padding empty endsets at slots `4..N` (admissible by L3's slot-3-only non-emptiness conjunct) | introduced |
| PrefixSpanCoverage | LEMMA | For any tumbler `x` with `#x ≥ 1`, the unit-depth span has `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`; derived from OrdinalShift (`x ⊕ δ(1, #x) = shift(x, 1)`), T12, T1 cases (i)/(ii), and T5 (ASN-0034) | introduced |
| L10 | LEMMA | TypeHierarchyByContainment — `coverage({(p, δ(1, #p))}) = subtypes(p)` by PrefixSpanCoverage | introduced |
| L11a | LEMMA | LinkUniqueness — distinct T10a-conforming allocation events produce distinct link addresses (corollary of L1c + GlobalUniqueness; derivation in body) | introduced |
| L11b | LEMMA | NonInjectivity — every conforming state with a link can be extended to a non-injective conforming state | introduced |
| L12 | INV | LinkImmutability — `(A Σ, Σ' : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` for every state transition | introduced |
| L12a | LEMMA | LinkStoreMonotonicity — `dom(Σ.L) ⊆ dom(Σ'.L)` for every state transition | introduced |
| L12b | LEMMA | HomeDocumentPersistence — `{home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M)` for every state transition; joint consequence of L1a (at `Σ'`) and L12a | introduced |
| L13 | LEMMA | ReflexiveAddressing — link addresses are valid endset span targets; canonical span coverage by PrefixSpanCoverage | introduced |
| L14 | INV | DualPrimitive — stored entities partition into content (`dom(Σ.C)`) and links (`dom(Σ.L)`) with no third category | introduced |
| L14a | INV | NonTranscludability (under `s_C`-resident content) — `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))` | introduced |
| coverage(e) | DEF | the union of address sets denoted by the spans in endset e | introduced |
| home(a) | DEF | document-level prefix extracted from a link address via T4 field parsing — the document under whose prefix the link resides | introduced |
| Endset | DEF | `𝒫_fin(Span)` — a finite set of well-formed spans | introduced |
| Link | DEF | `{(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`; standard triple `(F, G, Θ)` by convention, slot 3 is the type endset | introduced |


## Open Questions

- *Scope of content-side disjointness.* L0a (ContentSubspaceScope) scopes content-side disjointness to the `s_C`-resident slice because no ASN-0036 S-invariant fixes a global content-subspace constant; conforming systems may, in principle, place content in subspaces other than `s_C`, and any such residue lies outside this ASN's disjointness scope. Conforming systems whose content is entirely `s_C`-resident — Gregory's implementation among them, by the granfilade discriminator's exhaustive assignment of `TEXTATOM = 1` (i.e., `s_C`) to all stored content — enjoy the global disjointness `dom(Σ.L) ∩ dom(Σ.C) = ∅` as a corollary. A future ASN-0036 revision that absorbs a global content-subspace constant would lift L0a's scope from "`s_C`-resident slice" to "all of `dom(Σ.C)`".
- What invariants must hold between the link store and the content store when the same I-address appears in multiple arrangements via transclusion?
- What well-formedness constraints, if any, govern compound link structures where links reference other links through endsets?
- Under what conditions should two endsets with different span decompositions but identical coverage be treated as equivalent for query purposes?
- What constraints govern the allocation ordering of link addresses relative to content addresses within the same document?
- What must a conforming type address hierarchy satisfy beyond tumbler prefix containment?
- Must the link store maintain consistency with the arrangements `Σ.M`, or are the two components independently mutable?
- If links are permitted V-positions in the arrangement layer, what must S3 (ReferentialIntegrity) guarantee so that non-transcludability (L14a) is preserved?
