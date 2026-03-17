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

Recall from ASN-0034 (T4, FieldParsing) that every element-level tumbler has the form `N.0.U.0.D.0.E`, where `E` is the element field, and the first component `E₁` is the subspace identifier. By T7 (SubspaceDisjoint), tumblers with different subspace identifiers are permanently distinct — no address in subspace `s₁` can equal or be confused with an address in subspace `s₂ ≠ s₁`.

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


## Home and Ownership

Because link addresses are element-level tumblers (L1), the `origin` function from ASN-0036 applies directly.

**Definition — LinkHome.** For a link at address `a ∈ dom(Σ.L)`, its *home document* is:

`home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

The home document determines the link's owner. This is not metadata attached to the link — it IS the link's address, read through the field structure. A link at address `a` lives under the document prefix `home(a)`, which identifies who created it and where it resides, by the same structural attribution that governs content (S7, ASN-0036).

The critical property — the one that distinguishes this design from systems where annotations are embedded in the annotated content:

**L2 — OwnershipEndsetIndependence.** The home document of a link is determined entirely by the link's address and is independent of the link's endsets:

`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`

Nelson makes this a first principle: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." This separation of residence from reference is what permits annotation without modification. Your link lives in your document, under your authority, even though its endsets reach into someone else's content. The annotated document is untouched — no byte added, no structure modified, no permission required.


## The Three-Endset Structure

What internal structure must a link have? We seek the minimal structure sufficient for typed, directional connections between arbitrary spans.

A connection has at least two sides — a *source* and a *target*. Without two sides there is no connection. Gregory confirms this minimum in the code: the internal function `domakelink` takes only two endsets (`fromspecset` and `tospecset`), and the insertion functions (`insertendsetsinspanf`, `insertendsetsinorgl`) treat the from and to endsets as mandatory while the third is conditional. Two endsets are the structural floor.

But two sides alone do not suffice. We need to distinguish a citation from a comment from a refutation. If all links are structurally uniform two-endset connections, one cannot ask "find all citations" without also retrieving every comment and footnote. Classification is required.

Nelson's design resolves this not by adding a metadata field — a type tag bolted onto a binary link — but by adding a *third endset*, structurally identical to the first two, pointing into the address space. This achieves three things simultaneously:

1. **Extensibility.** Any user can define new types by choosing new addresses, without schema changes. Nelson: "The set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose."

2. **Uniformity.** All three endsets have the same representation — a set of spans in the tumbler space. The link is a homogeneous triple, not a pair-plus-metadata.

3. **Hierarchical classification.** Because tumbler containment is decidable (T6, ASN-0034), type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering. A query matching `p` matches both (by T5, ContiguousSubtrees).

We now define the components.

**Definition — Endset.** An *endset* is a finite set of well-formed spans:

`Endset = 𝒫_fin(Span)`

where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined, ASN-0034): `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s`. The empty set `∅` is a valid endset — a link may have an endset that references nothing.

**Definition — Link.** A *link value* is a triple of endsets:

`Link = (from : Endset, to : Endset, type : Endset)`

The three components are called the *from-endset*, the *to-endset*, and the *type-endset* respectively.

**L3 — TripleEndsetStructure.** Every link in the link store has exactly three endsets:

`(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

Nelson's MAKELINK operation takes four parameters — home document, from-set, to-set, and three-set — and nothing else. Gregory's code confirms that three is not a soft convention but a hard structural constraint. The V-subspace assignment function `setlinkvsas` hardcodes three V-addresses (1.1, 2.1, 3.1). The spanfilade index uses three integer constants (`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). The query function `intersectlinksets` takes exactly three input lists. The wire protocol (`FINDLINKSFROMTOTHREE`) encodes three endset parameters. And the integer namespace for a fourth endset type is already consumed — `DOCISPAN = 4` — blocking extension without renumbering the entire storage layer. Three is the design commitment.


## Endset Properties

Each endset is a set of spans — potentially multiple, potentially discontiguous, potentially spanning multiple documents. Nelson:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse."

We now state the properties that endsets must satisfy.

**L4 — EndsetGenerality.** The spans within an endset may reference any addresses in the tumbler space. There is no constraint confining spans to a single document, to content addresses only, or to addresses at which content currently exists:

`(A a ∈ dom(Σ.L), e ∈ {from, to, type}, (s, ℓ) ∈ Σ.L(a).e :: s ∈ T ∧ (s, ℓ) satisfies T12)`

The only structural constraint on an endset span is span well-formedness (T12). In particular:

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

Although the three endsets are structurally identical (all are elements of `Endset`), they are not interchangeable. The from-endset and to-endset are distinguished positions — the system records which is "first" and which is "second," and search can constrain on each independently.

**L6 — SlotDistinction.** The three endsets occupy structurally distinguished positions within the link. A link `(F, G, Θ)` is a different value from `(G, F, Θ)` when `F ≠ G`:

`(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`

Gregory's implementation encodes this distinction at two independent levels: in the link's own permutation matrix (V-addresses 1.1, 2.1, 3.1 for from, to, and type) and in the spanfilade index (ORGL-range prefixes `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`). A query for "links from span A" and a query for "links to span A" search different index columns and may return different results.

But the slot distinction is *structural*, not *semantic*. Whether "from" means "source" and "to" means "destination" is determined by the link's type, not by the link structure:

**L7 — DirectionalFlexibility.** The semantic interpretation of from-endset versus to-endset is a function of the link type, not a fixed property of the link structure.

Nelson: "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" The word "typically" is deliberate. A citation link is directional — it goes *from* citing text *to* cited source. A counterpart link marking equivalence has no meaningful direction. A heading link populates only one content endset — Nelson calls it "inane" to label that one endset "from." The structure provides two slots; the type defines whether the distinction carries directional weight.

The consequence: any system that determines a link's directionality from slot position alone — treating "from" as inherently "source" and "to" as inherently "target" without consulting the type — is misinterpreting the design. The slots provide structural asymmetry sufficient for indexing and query; the type provides semantic interpretation.

Despite the slot distinction, access is symmetric. The system must support retrieving any endset of any link with equal facility. Gregory confirms: the `followlink` operation takes a `whichend` parameter (1, 2, or 3) and calls `link2sporglset` with a V-range query parameterized by that integer. The retrieval path is identical for all three slots — no endset is privileged or hidden.


## The Type Endset

The type endset deserves extended treatment. It is structurally an endset — a finite set of spans — but its role is semantic classification, and it has distinctive properties that follow from that role.

**L8 — TypeByAddress.** Type matching is by *address identity*, not by content at the address. Whether two links share the same type is determined by whether their type endsets reference the same addresses, not by what is stored at those addresses:

`same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`

where endset equality is set equality of spans.

Nelson: "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

This is a profound design choice. It decouples classification from content retrieval entirely. A search for "all links of type X" never fetches the bytes at address X — it only matches the address. This means:

**L9 — TypeGhostPermission.** The type endset may reference addresses at which no content exists:

`¬ [(A a ∈ dom(Σ.L), (s, ℓ) ∈ Σ.L(a).type :: coverage({(s, ℓ)}) ⊆ dom(Σ.C))]`

Nelson: "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." The type address is a pure name — a position chosen by convention, not a pointer to content that must be dereferenced.

A consequence of L8 and L9 together: new link types can be defined by choosing a fresh tumbler address and using it as a type endset. No content needs to be created at that address. No registry needs to be updated. No schema needs to change. The type exists as soon as someone uses it. This is what makes the type system "open-ended" — any user can extend it without coordination or system modification.

**L10 — TypeHierarchyByContainment.** For type addresses `p, c ∈ T` where `p ≼ c` (p is a prefix of c), define `subtypes(p) = {c ∈ T : p ≼ c}`. By T5 (ContiguousSubtrees, ASN-0034), `subtypes(p)` is a contiguous interval under T1. Therefore there exists a span `(p, ℓ)` such that:

`(A c : p ≼ c : c ∈ coverage({(p, ℓ)}))`

That is, a single span query rooted at `p` with appropriately chosen width matches every subtype of `p`. Hierarchical type relationships follow from the tumbler ordering without any additional mechanism.

Gregory documents this in the bootstrap document's type registry: `MARGIN` at address `1.0.2.6.2` is hierarchically nested under `FOOTNOTE` at `1.0.2.6`. A query for all footnote-family links, expressed as a span query rooted at `1.0.2.6`, matches both types because `1.0.2.6.2` lies within `[1.0.2.6, 1.0.2.7)`. The subtyping mechanism is the tumbler ordering itself — no separate hierarchy data structure is needed.

We observe that L10 characterizes the structural affordance that the address space provides for type hierarchies. Whether a conforming system must implement subtype-aware query operations, or whether subtype matching is the caller's responsibility, is a question about the query interface — outside this ASN's scope.


## Link Distinctness and Permanence

We now establish the identity semantics of links. The three requirements we began with — distinguishability, ownership, referenceability — crystallize into two properties.

**L11 — IdentityByAddress.** The identity of a link is its tumbler address. Two links at different addresses are distinct objects regardless of whether their endsets are identical:

`(A a₁, a₂ ∈ dom(Σ.L) :: a₁ ≠ a₂ ⟹ Σ.L(a₁) and Σ.L(a₂) are distinct links)`

The converse does *not* hold as an identity principle: `Σ.L(a₁).from = Σ.L(a₂).from ∧ Σ.L(a₁).to = Σ.L(a₂).to ∧ Σ.L(a₁).type = Σ.L(a₂).type` does not imply `a₁ = a₂`. Two links with identical endsets — same from, same to, same type — but different addresses are separate objects, independently owned, independently removable, independently targetable by other links.

This follows from the allocation mechanism: each link creation event produces a new address by forward allocation (T9, ASN-0034). By GlobalUniqueness (ASN-0034), no two allocation events anywhere in the system, at any time, produce the same address. Therefore every link has a globally unique, permanent identity, and the question "are these the same link?" reduces to tumbler comparison (T2, IntrinsicComparison).

**L12 — LinkImmutability.** Once created, a link's address persists and its value is permanently fixed:

`(A Σ, Σ' : Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

for every state transition `Σ → Σ'`. This parallels S0 (ContentImmutability, ASN-0036) in both halves: the address endures, and the value at that address — the triple of endsets — never changes.

The evidence is unambiguous. Nelson's FEBE protocol defines exactly five link operations: MAKELINK (create), FINDLINKSFROMTOTHREE (search), FINDNUMOFLINKSFROMTOTHREE (count), FINDNEXTNLINKSFROMTOTHREE (paginate), and RETRIEVEENDSETS (read). There is no MODIFYLINK, UPDATELINK, or EDITENDSETS. The only write operation is creation; the rest are queries. Gregory confirms at the implementation level: `insertendsetsinorgl` and `insertendsetsinspanf` are called exclusively from `docreatelink`; no other code path writes to the link's orgl or spanfilade entries. The link orgl is written once by `createorglingranf` and never touched again.

Link immutability follows from the same principle that makes content immutable: others may have linked to it. Since links are first-class objects with tumbler addresses, other links can point to them (L13). Modifying a link's endsets after creation would silently change the meaning of every meta-link pointing to it — violating the permanence guarantee. To effectively change a connection, the owner deletes the old link (V-space removal only) and creates a new one via MAKELINK with the desired endsets. The old link persists in I-space and historical versions; the new link gets a fresh address in creation order.

Note what L12 does not address. Whether a link remains *discoverable* through indexing, whether its endsets remain *resolvable* to visible content, and what it means for a link to be "removed" while its address and value persist — these are questions about operations and their effects, outside this ASN's scope.

**L12a — LinkStoreMonotonicity.** The domain of the link store is monotonically non-decreasing:

`[dom(Σ.L) ⊆ dom(Σ'.L)]`

for every state transition `Σ → Σ'`. This is the direct corollary of L12, paralleling S1 (StoreMonotonicity) for the content store.


## Reflexive Addressing

Because links have tumbler addresses (L0, L1), and endsets can reference any tumbler address (L4), endsets can reference link addresses. This enables *link-to-link* connections — a link whose endset points at another link's address.

**L13 — ReflexiveAddressing.** Link addresses are valid targets for endset spans. For any link at address `b ∈ dom(Σ.L)`:

`(b, [1]) is a well-formed span referencing exactly the link at address b`

where `[1]` is the unit displacement — a single-component tumbler with value 1. The well-formedness of this span follows from T12: the action point of `[1]` is position 1, and since `b` is an element-level tumbler with `#b ≥ 4`, the precondition `k ≤ #b` is satisfied.

Nelson: "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several). The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only."

Gregory confirms at the implementation level that this is not merely theoretically possible but architecturally unavoidable. The type `typeisa` is `typedef tumbler typeisa` — a bare tumbler with no type discriminant. The endset conversion functions (`specset2sporglset`, `vspanset2sporglset`) accept any tumbler address without checking whether it refers to content or to a link. The insertion functions (`insertspanf`, `insertpm`) store whatever `sporgladdress` they receive, with no type validation. The retrieval function (`findorgl`) resolves any address that maps to a valid granfilade entry, regardless of its atom type. There is no code, at any layer, that draws a boundary between "addressable objects" and "non-addressable objects."

From L13, arbitrary relational structures can be composed:

> "Complex relational structures, such as the faceted link, may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links."

The three-endset link plays the same role for structured connections that the cons cell plays for structured data: a universal building block from which compound forms of arbitrary complexity are assembled. A faceted link — one that relates multiple distinct groups of spans in more than three roles — is built from a chain of links, each contributing its three endset slots, with link-to-link references providing the composition glue.


## The Dual-Primitive Architecture

We can now state the architectural consequence that unifies the preceding properties. The docuverse is built from exactly two kinds of stored entity:

**L14 — DualPrimitive.** The set of addresses at which entity values reside is `dom(Σ.C) ∪ dom(Σ.L)`. No state component maps an address outside this union to an entity value. Arrangements `Σ.M(d)` are mappings *between* addresses — they relate V-positions to I-addresses — but V-positions are not entities in their own right. The two domains are disjoint:

`dom(Σ.C) ∩ dom(Σ.L) = ∅`

Nelson: "In the present implementation, the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." Documents, accounts, servers, and nodes are organizational concepts — positions in the tumbler hierarchy that structure the address space — but they have no stored representation. Only content and links occupy storage.

Gregory confirms with emphasis: the granfilade's union type has exactly two variants (`GRANTEXT` and `GRANORGL`), the hint mechanism accepts exactly two atom types (`TEXTATOM = 1` and `LINKATOM = 2`), and the V-space within each document is partitioned into exactly two regions (text at `1.x`, links at `2.x`). No third category exists.

The two primitives are peers. Both have permanent tumbler addresses. Both are stored in the same master index (the granfilade). Both support the same addressing and containment mechanisms. But they are categorically different:

| | Content | Links |
|---|---|---|
| State component | `Σ.C : T ⇀ Val` | `Σ.L : T ⇀ Link` |
| Subspace | `s_C` | `s_L` |
| Payload | Opaque values (bytes) | Structured triples (three endsets) |
| Identity semantics | Shareable via transclusion (S5) | Unique per address (L11) |
| Address determines | Content origin (S7) | Link home and owner (L2) |

Content identity is *shareable*: the same I-address can appear in the arrangements of multiple documents via transclusion, and this sharing is the mechanism for content reuse (S5, ASN-0036). Link identity is *unique*: each link has exactly one address, and there is no mechanism to make two documents "share" the same link. We can derive this from two properties already established. First, S3 (ReferentialIntegrity, ASN-0036) requires that every V-mapping points to a content address: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`. Second, L0 establishes `dom(Σ.L) ∩ dom(Σ.C) = ∅`. Together these entail that no arrangement can map a V-position to a link address — the transclusion mechanism (multiple arrangements referencing the same I-address) cannot apply to links. A link at address `a` is homed in `home(a)` and owned by the principal of `home(a)` — period. It cannot be transcluded into another owner's authority.

This asymmetry is deliberate. Content wants to be shared — that is the point of transclusion. But a connection is an assertion by a specific principal about specific content, and assertions are not transferable by reference.


## Summary of the Link Model

A link is an addressed, owned, typed, bidirectional connection between arbitrary spans of content in the tumbler space. More precisely:

A link at address `a ∈ dom(Σ.L)` is characterized by:

- **Address** `a` — a permanent, globally unique element-level tumbler in the link subspace (L0, L1, L11, L12). The address IS the link's identity.
- **Home** `home(a) = origin(a)` — the document under whose prefix `a` falls, determining the link's owner, independent of what the link connects (L2).
- **Three endsets** `Σ.L(a) = (F, G, Θ)` — the from-endset `F`, to-endset `G`, and type-endset `Θ`, each a finite set of well-formed spans pointing anywhere in the tumbler space (L3, L4, L5).
- **Slot structure** — the three endsets are structurally distinguished positions, enabling independent query on each, with directional semantics determined by the type rather than by the slot itself (L6, L7).
- **Type semantics** — the type endset is matched by address, not by content; it may reference ghost addresses; and hierarchical type relationships follow from tumbler containment (L8, L9, L10).


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.L | `Σ.L : T ⇀ Link` — the link store, mapping addresses to link values | introduced |
| L0 | SubspacePartition — link addresses occupy subspace `s_L`, content addresses occupy `s_C`, and `dom(Σ.L) ∩ dom(Σ.C) = ∅` | introduced |
| L1 | LinkElementLevel — every link address is an element-level tumbler: `(A a ∈ dom(Σ.L) :: zeros(a) = 3)` | introduced |
| L2 | OwnershipEndsetIndependence — `home(a)` depends only on `a`, not on the link's endsets | introduced |
| L3 | TripleEndsetStructure — every link has exactly three endsets: `Σ.L(a) = (F, G, Θ)` | introduced |
| L4 | EndsetGenerality — endset spans may reference any address in `T`; no single-document, content-only, or existence constraint | introduced |
| L5 | EndsetSetSemantics — an endset is an unordered set; only span membership matters | introduced |
| L6 | SlotDistinction — the three endsets are structurally distinguished positions: `F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ)` | introduced |
| L7 | DirectionalFlexibility — the semantic interpretation of from vs. to is a function of the link type | introduced |
| L8 | TypeByAddress — type matching is by address identity, not by content at the address | introduced |
| L9 | TypeGhostPermission — type endsets may reference addresses at which no content exists | introduced |
| L10 | TypeHierarchyByContainment — tumbler prefix containment provides hierarchical type relationships | introduced |
| L11 | IdentityByAddress — link identity is its tumbler address; identical endsets do not imply identical links | introduced |
| L12 | LinkImmutability — `(A Σ, Σ' : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` for every state transition | introduced |
| L12a | LinkStoreMonotonicity — `dom(Σ.L) ⊆ dom(Σ'.L)` for every state transition | introduced |
| L13 | ReflexiveAddressing — link addresses are valid endset span targets, enabling link-to-link connections | introduced |
| L14 | DualPrimitive — stored entities partition into content (`dom(Σ.C)`) and links (`dom(Σ.L)`) with no third category | introduced |
| coverage(e) | the union of address sets denoted by the spans in endset e | introduced |
| home(a) | `origin(a)` applied to link addresses — the document under whose prefix the link resides | introduced |
| Endset | `𝒫_fin(Span)` — a finite set of well-formed spans | introduced |
| Link | `(from : Endset, to : Endset, type : Endset)` — a triple of endsets | introduced |


## Open Questions

- What invariants must hold between the link store and the content store when the same I-address appears in multiple arrangements via transclusion?
- What well-formedness constraints, if any, govern compound link structures where links reference other links through endsets?
- Under what conditions should two endsets with different span decompositions but identical coverage be treated as equivalent for query purposes?
- What constraints govern the allocation ordering of link addresses relative to content addresses within the same document?
- What must a conforming type address hierarchy satisfy beyond tumbler prefix containment?
- Must the link store maintain consistency with the arrangements `Σ.M`, or are the two components independently mutable?
