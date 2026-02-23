# ASN-0006: Transclusion (COPY)

*2026-02-23*

We wish to understand what transclusion must guarantee. The word "transclusion" appears throughout Nelson's design as the mechanism by which content is shared across documents without duplication. The system provides two ways to place text in a document: INSERT, which creates fresh content with new addresses, and COPY, which references content that already exists. These two operations look identical to a reader — both produce visible text — yet the system treats their products as fundamentally different. We seek the precise formal distinction, and the properties that follow from it.

The approach is: define what identity means for content, show how COPY preserves identity while INSERT creates it, then derive the consequences — for link discovery, attribution, version comparison, and economic compensation. We shall find that the entire web of cross-document relationships rests on a single architectural choice: transclusion shares addresses rather than values.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store — once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a function from virtual positions to addresses, `poom(d) : Pos → Addr`. This is the document's current arrangement — which content appears where.
- **spanindex**: a relation recording which documents contain which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only.
- **links**: a set of link structures, each having three endsets (from, to, type), where endsets reference I-space address ranges.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, and `poom(d).p` for the I-address that document d maps position p to. We use primed names for the state after an operation.

An I-space address encodes provenance structurally. Every address has the form `Node.0.User.0.Document.0.Element`, where each field is readable from the address alone. The Document field identifies which document created the content; the Element field's first component identifies its subspace (1 for text, 2 for links). This encoding is intrinsic — no external index is needed to answer "who created this byte?"


## Content identity

We are looking for the right definition of "same content." In conventional systems, content identity is value-based: two strings are the same if they have the same characters. In Xanadu, content identity is address-based: two bytes are the same if and only if they have the same I-space address.

This is not a design whim. It is forced by the requirement that the system distinguish between independent creation and deliberate sharing. Nelson poses the scenario directly: if I type "Hello" into my document and you type "Hello" into yours, we have created content that is value-identical but identity-distinct. We did not share anything — we independently produced the same character sequence. No link, attribution, or economic relationship should connect our two instances. But if you transclude my "Hello" into your document, the system must recognize that your copy IS my content — that links to my text reach your display of it, that I receive attribution and compensation when your document is read.

We state this formally:

**TC0 (Identity is address).** Two content references in the system denote the same content if and only if they resolve to the same I-space address:

  `same(r₁, r₂) ≡ iaddr(r₁) = iaddr(r₂)`

where `iaddr(r)` extracts the I-space address that reference `r` points to. Value equality is neither necessary nor sufficient for identity. Two bytes at different I-addresses are distinct even if their content is the same character. Two references to the same I-address are identical even if they appear in different documents at different V-positions.

TC0 is what makes the system's cross-document relationships computable. Without it, every operation that asks "does this content appear elsewhere?" would require a full-text comparison of the entire docuverse — an operation that is both computationally infeasible and semantically wrong (it would falsely connect independently created identical text). With TC0, the question reduces to set intersection on I-addresses, which is both efficient and correct.


## The COPY operation

We now define what COPY does. The operation takes a source specification (a set of V-spans in one or more documents) and a target (a document and position), and makes the source content appear at the target position. The critical question is: how does the target document's mapping relate to the source's?

**TC1 (I-address preservation).** COPY creates V→I mappings in the target document that reference the same I-addresses as the source:

  `(A a : a ∈ iaddrs(source_span) : (E p : poom'(target).p = a))`

where `iaddrs(source_span)` is the set of I-addresses that the source document's POOM maps the source V-span to. No fresh I-addresses are allocated. The set `dom.ispace` is unchanged:

  `dom.ispace' = dom.ispace`

Nelson states this with precision: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." The term "virtual copies" is exact — no content is duplicated. The target document gains V-space positions that map to I-addresses belonging to the source.

Gregory confirms the data flow definitively. The implementation converts source V-spans to I-spans by reading the source document's POOM, obtaining the existing I-addresses. These I-addresses are then inserted (as-is, with no transformation) into the target document's POOM at the specified V-position. The allocation function for content — the function that assigns fresh I-addresses — is never called during COPY. The I-addresses extracted from the source POOM are exactly the I-addresses deposited in the target POOM.

We must state the contrast with INSERT to make the distinction sharp:

**TC2 (INSERT creates identity; COPY preserves it).** INSERT at position p in document d allocates fresh addresses `a₁, ..., aₙ` such that:

  `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom.ispace)` and `(A i : 1 ≤ i ≤ n : aᵢ ∈ dom.ispace')`

COPY from source to target at position p creates no new addresses:

  `dom.ispace' = dom.ispace`

and the addresses in the target are drawn from the source:

  `{a : (E p : poom'(target).p = a) ∧ p is new} = iaddrs(source_span)`

This is the sole architectural distinction between duplication and transclusion. Every observable behavioral difference — in link discovery, version comparison, attribution, compensation — flows from this single fact: INSERT allocates new I-addresses; COPY shares existing ones.


## The frame

We are not done until we have stated what COPY does NOT change. The frame conditions are as important as the effects.

**TC3 (Source invariance).** COPY does not modify the source document's POOM:

  `poom'(source_doc) = poom(source_doc)`

The source is a read-only participant. Its V→I mappings are consulted but not altered.

**TC4 (Cross-document isolation).** COPY does not modify the POOM of any document other than the target:

  `(A d : d ≠ target : poom'(d) = poom(d))`

**TC5 (I-space invariance).** COPY does not modify ispace:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` and `dom.ispace' = dom.ispace`

No content is created, modified, or removed from the permanent store.

**TC6 (Target text preservation).** COPY at position p in the target document preserves all existing content of the target. V-positions before p are unchanged; V-positions at or beyond p shift forward by the width of the copied content. The I-addresses at those shifted positions are unchanged:

  `(A q : q < p : poom'(target).q = poom(target).q)`
  `(A q : q ≥ p : poom'(target).(q ⊕ w) = poom(target).q)`

where `w` is the total width of the copied content. This is the same shift behavior as INSERT — both operations expand the V-space at the insertion point and displace subsequent content rightward.

**TC7 (Subspace confinement).** The V-position shift caused by COPY is confined to the text subspace. Link positions within the target document are not affected:

  `(A q ∈ link_subspace(target) : poom'(target).q = poom(target).q)`


## Span index registration

When COPY places content in the target document, the span index must record this fact:

**TC8 (Index registration).** After COPY, the span index contains entries associating the target document with the copied I-address ranges:

  `(A a ∈ iaddrs(source_span) : (a, target) ∈ spanindex')`

The granularity of registration is per contiguous I-span, not per byte. If the source content maps to three non-contiguous I-address ranges, three index entries are created. Each entry records the I-address range and the target document's identity. The I-address ranges in these entries are identical to those in the source document's existing index entries — only the document identifier differs.

Gregory confirms: the index insertion function iterates over the converted I-span list, creating one entry per list element. Each entry carries the target document's address as the associated document, while the I-address range is the unchanged range from the conversion. There is no allocation of I-addresses, no transformation of the range, no merging of entries.


## Independence of transclusions

We now derive the property that makes transclusion a robust sharing mechanism: independence from the source document's future mutations.

**Theorem (Transclusion independence).** If document B transcludes content at I-addresses `A` from document D, and subsequently D deletes that content from its POOM, then B's mapping to `A` is unaffected.

*Proof.* D's DELETE operates on D's POOM alone (by TC4, operations on D do not modify B's POOM). The I-addresses in `A` remain in `dom.ispace` (by I-space permanence — no operation removes addresses from the permanent store). Therefore `poom(B)` still maps V-positions to addresses in `A`, and `ispace.a` is well-defined for every `a ∈ A`. ∎

This is stronger than it first appears. B's transclusion is not merely "safe for now" — it is unconditionally immune to anything D does. D can delete the content, rearrange it, transclude over it, create new versions. None of these operations touches B's POOM. The independence is not temporal ("D has not yet deleted it") but structural ("D's operations cannot reach B's state").

Nelson states the guarantee directly: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." The formal derivation confirms that this follows from cross-document isolation plus I-space permanence, not from any special-case protection of transclusions.

A consequence for link discovery deserves explicit statement. If links exist whose endsets reference I-addresses in `A`, those links are discoverable through B even after D deletes the content:

**TC9 (Transclusion preserves link discoverability).** If document B transcludes I-addresses `A` and a link `L` has an endset referencing some `a ∈ A`, then `L` is discoverable through B regardless of the state of any other document's POOM:

  `(E p : poom(B).p = a) ∧ a ∈ endsets(L) ⟹ L ∈ discoverable_links(B)`

This holds because link search operates by converting B's V-spans to I-addresses (using B's intact POOM), then querying the span index for links whose endsets intersect those I-addresses. B's POOM is intact (by TC4). The span index entry associating `L` with addresses in `A` persists (by index monotonicity). The intersection is non-empty. The link is found.

Gregory confirms this end-to-end: the link search function converts V-spans to I-spans by reading the searching document's POOM, then queries the span index for intersecting link endsets. The searching document's POOM is the only document-specific state consulted. If the searching document still references the I-addresses, the search succeeds — regardless of what has happened to the document that originally created the content.


## Links follow content, not containers

We can now state the fundamental link-following property of transclusion. Links in Xanadu attach to I-space addresses — to the bytes themselves, not to their position in any document. Nelson captures this with the "strap between bytes" metaphor: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes."

Because links attach to I-addresses, and transclusion preserves I-addresses, links are automatically discoverable through transclusion:

**TC10 (Links follow transclusion).** If link L has an endset referencing I-address `a`, and document B transcludes content at address `a`, then L is discoverable through B:

  `a ∈ endsets(L) ∧ (E p : poom(B).p = a) ⟹ L ∈ discoverable_links(B)`

This is not a feature that needs to be implemented on top of transclusion. It is a structural consequence of three design choices: (i) links reference I-addresses; (ii) transclusion preserves I-addresses; (iii) link search operates on I-addresses. No special-case logic is needed to "carry links across" a transclusion. The links were never attached to the source document — they were attached to the content, and the content is now visible in B.

Nelson confirms: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." And more broadly: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay."

An important clarification: link visibility through transclusion is guaranteed at the discovery level but subject to filtering at the display level. Nelson describes front-end "sieving" — user-controlled filters that select which links to show based on criteria such as origin, recency, or author. The guarantee is that links are *findable*, not that they are *automatically displayed*. A reader viewing transcluded content can always ask for all links and receive a complete answer; what the front end chooses to present is a separate concern.


## Attribution is structural

We now turn to a property that Nelson considers among Xanadu's most important: the guarantee that content origin is always traceable. In conventional systems, attribution is metadata — an author tag, a copyright notice, a citation — that can be stripped, falsified, or simply omitted. In Xanadu, attribution is encoded in the address.

**TC11 (Structural attribution).** For every I-address `a ∈ dom.ispace`, the creating document is determinable from `a` alone:

  `home(a) = fields(a).document`

where `fields` extracts the four-level hierarchy (node, user, document, element) from the address. This function requires no index lookup, no metadata query, no external data. The address IS the attribution.

Nelson is explicit: "You always know where you are, and can at once ascertain the home document of any specific word or character." And: "only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted."

Because transclusion preserves I-addresses (TC1), the attribution of transcluded content is automatic and unseverable. When document B transcludes content from document A, the I-addresses in B's POOM still carry A's document identifier. No operation within the system can alter this — I-addresses are permanent, and the document field is part of the address. To sever the attribution, one would need to change the I-address itself, which violates the most basic permanence guarantee.

This gives us a reverse traceability guarantee:

**TC12 (Reverse traceability).** The system provides an operation (FINDDOCSCONTAINING) that, given a set of I-addresses, returns all documents whose POOMs currently map to any of those addresses:

  `finddocscontaining(A) = {d : (E a ∈ A, p : poom(d).p = a)}`

This operation is sound because of TC0 (identity is address). Two documents contain "the same content" if and only if their POOMs map to the same I-addresses. The query is a set intersection on addresses, not a text comparison. Nelson: "This returns a list of all documents containing any portion of the material included by ⟨vspec set⟩."

A subtlety: the span index is an over-approximation (it records historical containment, not current containment). A query against the span index may return documents that no longer reference the content. A second check against each candidate document's current POOM is needed to filter stale results. The forward direction is exact: every document that currently references the I-addresses is in the span index. The reverse direction requires filtering.


## Version comparison as corollary

Transclusion's identity preservation also enables version comparison. When CREATENEWVERSION creates a new version of a document, the new version's POOM maps to the same I-addresses as the source (for text content — no fresh content addresses are allocated). Subsequent edits to one version create new I-addresses (via INSERT) or remove references (via DELETE), but do not affect the shared I-addresses.

The SHOWRELATIONOF2VERSIONS operation exploits this: it converts both versions' V-spans to I-addresses and computes the intersection.

**TC13 (Correspondence by shared identity).** Two documents (or versions) share content if and only if they share I-addresses:

  `correspondence(d₁, d₂) = {a : (E p₁ : poom(d₁).p₁ = a) ∧ (E p₂ : poom(d₂).p₂ = a)}`

Nelson motivates this: "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."

The key insight: the system does not compare text values to find matches. It compares I-addresses. Two versions created by CREATENEWVERSION share most of their I-addresses (those for unchanged text). Passages that were independently typed have different I-addresses even if the text is identical. This means correspondence is provenance-based, not value-based — it tracks "what came from the same creative act" rather than "what happens to look the same."


## Depth irrelevance

Transclusion may be nested to arbitrary depth: document C may transclude from B, which transcludes from A. We must show that the properties hold regardless of depth.

**TC14 (Depth collapse).** If document B transcludes content from A, and document C transcludes that same content from B, then C's POOM maps to A's I-addresses directly — not to B's "copy" of them (there is no such copy):

  `poom(C).p = a ∧ home(a) = A`

regardless of the number of intermediate transclusion steps. The depth collapses to zero because every step preserves the original I-addresses. B's POOM maps to A's addresses; C's POOM maps to the same addresses (extracted from B's POOM, which holds A's addresses). There is no chain of intermediate addresses — the I-address is the same at every level.

Nelson makes this explicit with the glass-pane metaphor: "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." And: "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character."

Depth irrelevance is a consequence, not an axiom. It follows from TC1 (COPY preserves I-addresses) applied inductively: each COPY step extracts addresses from the source POOM and deposits them unchanged in the target. If the source's addresses are already A's addresses (by the induction hypothesis), the target's addresses are A's addresses too.

This gives us depth-independent attribution: `home(a)` returns A's document identity regardless of whether the reader is viewing A, B, or C. And depth-independent link discovery: links to A's I-addresses are found through C by the same mechanism as through A — TC10 cares only that the POOM maps to the link's endset addresses, not how many transclusion steps produced that mapping.


## Economic consequence

Nelson designs an economic model where content creators receive compensation automatically when their content is viewed. The mechanism is a "cash register" per published document that increments whenever its bytes are delivered:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery."

Transclusion interacts with this model through identity preservation. When a reader views a compound document containing transcluded content, the system delivers bytes from their home locations. The royalty accrues at the home document — the one identified by `home(a)` for each byte `a`:

**TC15 (Compensation follows identity).** When content at I-address `a` is delivered to a reader from any document, compensation accrues to the owner of `home(a)`:

  `compensate(delivery(a)) → owner(home(a))`

This holds regardless of which document the reader is viewing, because `home(a)` is determined by the I-address, not by the viewing context. Nelson: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."

For a compound document containing both native content (created by INSERT, with I-addresses whose document field identifies this document) and transcluded content (referenced by COPY, with I-addresses whose document field identifies the source), the compensation splits naturally: native bytes compensate this document's owner; transcluded bytes compensate the respective source documents' owners. The split is computed from the I-addresses, which encode provenance directly.

Depth irrelevance (TC14) ensures this works across arbitrary transclusion chains. The 50th re-transclusion of a passage still carries the original creator's I-addresses, so compensation flows to the original creator.


## Transclusion permanence and the publication boundary

The preceding properties establish what transclusion guarantees at the I-space and V-space level. But a distinct question concerns the *accessibility* of transcluded content. A document's ability to display transcluded content depends on the content being retrievable from the system:

**TC16 (Transclusion as reference, not cache).** Transcluded content is retrieved from its home location on each access. The transcluding document stores V→I mappings, not content:

  `display(d, p) = ispace.(poom(d).p)`

If `poom(d).p` is defined but `ispace.(poom(d).p)` is not retrievable (due to the home location being unavailable), the transcluding document has a gap at position p. There is no local fallback, no cached copy, no degradation to a previous value.

This is by design. Nelson: "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about."

The permanence of a transclusion therefore depends on the permanence of its source. The publication status of the source determines the strength of this dependency:

- **Published content**: The publication contract forbids casual withdrawal. Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." Transclusions of published content are protected by this contract — not by the transclusion mechanism itself, but by the social and economic obligation attached to publication.

- **Private or retractable content**: Content that has not been published (or has been "privashed" — made universally accessible but explicitly retractable) may be withdrawn at any time. Nelson: "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing." Transclusions of such content inherit the retractability.

Note that TC16 describes the abstract access model. The I-space permanence guarantee ensures that I-addresses remain valid forever and content at those addresses is immutable. What TC16 captures is the additional dependency: even if the content *exists* in ispace, its *retrievability* may depend on factors outside the formal model — network availability, storage funding, access permissions. The formal model guarantees that the V→I mapping is intact and the content is unchanged; the operational model adds the constraint that the content must be reachable.


## POOM coalescing is semantically transparent

One final property deserves mention, because it guards the boundary between abstract specification and implementation freedom. An implementation may choose to represent POOM entries in various ways — one entry per byte, one entry per contiguous I-span, or some intermediate representation. When COPY inserts I-addresses that are contiguous with existing entries in the target POOM, an implementation may silently coalesce them into a single entry (extending an existing mapping rather than creating a new one).

**TC17 (Representation transparency).** The internal structure of the POOM — how many entries it uses, whether adjacent entries are coalesced — has no effect on the observable semantics of link discovery, version comparison, attribution, or content retrieval:

  `observable(poom₁) = observable(poom₂)` whenever `(A p : poom₁(p) = poom₂(p))`

Two POOMs that define the same function from V-positions to I-addresses are observationally equivalent, regardless of their internal structure. The coalescing of entries is an optimization that an implementation may perform freely, because all queries operate on the V→I mapping (the abstract function), not on the entry structure (the representation).

Gregory confirms this with analysis of the coalescing mechanism. When contiguous I-addresses from the same home document are detected, the existing entry is silently extended rather than a new one created. The condition for coalescing — same home document and I-address contiguity — precisely characterizes the cases where the mathematical I-address range is unchanged. Link discovery, which operates by converting V-spans to I-spans and querying for intersection, produces identical results because the I-span coverage is identical whether the POOM uses one entry or two.


## What transclusion is NOT

We have stated what COPY guarantees. We must equally state what it does NOT guarantee, to prevent over-specification.

Transclusion is not a cache. TC16 establishes that transcluded content is retrieved from its home location; there is no stored copy in the target document. The target holds mappings, not content.

Transclusion is not a subscription. COPY captures the I-addresses of the source at the moment of the operation. If the source document subsequently has new content inserted, the transcluding document does not automatically see the new content. The I-addresses captured by COPY were the ones present at copy time; the new content has new I-addresses that the target does not reference.

Transclusion is not versioned linkage. The target does not track "the current state of the source document." It references specific I-addresses. If the source evolves, the target retains its original references — it becomes a record of what the source contained at the time of transclusion.

Transclusion does not create bidirectional awareness. The source document has no record that its content was transcluded. The span index records that the target contains those I-addresses, but the source document's POOM is unchanged (TC3). Discovering that content has been transcluded elsewhere requires the FINDDOCSCONTAINING query — it is not implicit in the source document's state.


## Formal summary

We collect the structure. The COPY operation is a transformation `δ(Σ, COPY(source, target, p)) = Σ'` where:

*Effect:* The target document's POOM gains new V→I mappings at position `p`, referencing the I-addresses extracted from the source's POOM. No fresh I-addresses are allocated. The span index is extended with entries associating the target document with the copied I-address ranges.

*Frame:* I-space is unchanged. The source document's POOM is unchanged. All other documents' POOMs are unchanged. The link subspace of the target document is unchanged.

*Identity:* The I-addresses in the target after COPY are identical to those in the source — not copies, not translations, not re-allocations. TC0 defines content identity as address identity, and COPY preserves addresses.

*Consequences:* From identity preservation alone (TC1), all of the following are derived rather than axiomatized:

| Consequence | Derivation |
|-------------|------------|
| Links follow transclusion (TC10) | Links reference I-addresses; COPY preserves I-addresses; link search operates on I-addresses |
| Attribution is unseverable (TC11) | The I-address encodes the home document; COPY preserves I-addresses |
| Version comparison works (TC13) | Shared I-addresses = shared content; COPY shares I-addresses |
| Compensation flows to origin (TC15) | Compensation keys on home(a); home is determined by I-address; COPY preserves I-addresses |
| Depth is irrelevant (TC14) | Each COPY step preserves I-addresses; induction over depth |
| Source mutations are harmless (TC9) | Cross-document isolation + I-space permanence |

The power of the design is that all six consequences flow from a single architectural choice — COPY shares I-addresses rather than allocating new ones — combined with the permanence guarantee. No special-case mechanisms are needed for any of these properties. They are structural consequences of identity preservation.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| TC0 | Content identity is I-address identity: same(r₁, r₂) ≡ iaddr(r₁) = iaddr(r₂) | introduced |
| TC1 | COPY creates V→I mappings in the target referencing the same I-addresses as the source; dom.ispace is unchanged | introduced |
| TC2 | INSERT allocates fresh I-addresses; COPY shares existing ones — the sole structural distinction between duplication and transclusion | introduced |
| TC3 | COPY does not modify the source document's POOM | introduced |
| TC4 | COPY does not modify the POOM of any document other than the target | introduced |
| TC5 | COPY does not modify ispace — no content is created, modified, or removed | introduced |
| TC6 | COPY at position p preserves all existing target content; subsequent V-positions shift by the copied width | introduced |
| TC7 | COPY's V-position shift is confined to the text subspace; link positions are unaffected | introduced |
| TC8 | COPY registers the target document in the span index for the copied I-address ranges, one entry per contiguous I-span | introduced |
| TC9 | Transclusion preserves link discoverability: links to transcluded I-addresses are findable through the transcluding document regardless of the source's state | introduced |
| TC10 | Links follow transclusion: a link referencing I-address a is discoverable through any document whose POOM maps to a | introduced |
| TC11 | Attribution is structural: home(a) = fields(a).document is computable from the I-address alone, requiring no index | introduced |
| TC12 | FINDDOCSCONTAINING returns all documents whose POOMs currently map to a given set of I-addresses | introduced |
| TC13 | Two documents share content iff they share I-addresses; correspondence is address intersection, not value comparison | introduced |
| TC14 | Transclusion depth collapses: after N transclusion steps, the I-addresses are still the original creator's; all properties hold depth-independently | introduced |
| TC15 | Compensation accrues to owner(home(a)) for each delivered byte a, regardless of which document delivers it | introduced |
| TC16 | Transclusion is reference, not cache: transcluded content is retrieved from the home location, with no local fallback | introduced |
| TC17 | POOM internal structure (entry count, coalescing) is transparent to all observable queries | introduced |
| Σ.poom | poom(d) : Pos → Addr — per-document V→I arrangement mapping | introduced |
| home | home(a) = fields(a).document — the document that created content at address a | introduced |


## Open Questions

Must the system guarantee any mechanism by which a transcluding document is notified that its source content has become unretrievable, or is silent failure (a gap in the display) the specified behavior?

What invariant must the system maintain to ensure that FINDDOCSCONTAINING filters stale span index entries — and must this filtering be exact, or may it over-approximate?

When content is transcluded from a document the reader lacks permission to access directly, what must the system guarantee about the visibility of that content and its associated links?

Must the system provide an operation that distinguishes native content (created by INSERT) from transcluded content (placed by COPY) within a document, or is this distinction invisible to the reader?

What must the system guarantee about the atomicity of COPY when the source specifies multiple non-contiguous spans — must all spans be copied or none, or may a partial copy be observable?

Under what conditions, if any, may the system defer the span index registration (TC8) relative to the POOM insertion — and what queries might return incomplete results during the window between them?

What must the system guarantee about COPY when the source document is concurrently being modified — must the extracted I-addresses reflect a consistent snapshot of the source's POOM?

Must the royalty split (TC15) be computed per-byte, per-span, or per-delivery — and what granularity of accounting is sufficient to satisfy the economic model?
