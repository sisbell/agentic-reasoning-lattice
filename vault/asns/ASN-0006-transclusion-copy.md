# ASN-0006: Transclusion (COPY)

*2026-02-23*

We wish to understand what transclusion must guarantee. The word "transclusion" appears throughout Nelson's design as the mechanism by which content is shared across documents without duplication. The system provides two ways to place text in a document: INSERT, which creates fresh content with new addresses, and COPY, which references content that already exists. These two operations look identical to a reader — both produce visible text — yet the system treats their products as fundamentally different. We seek the precise formal distinction, and the properties that follow from it.

The approach is: define what identity means for content, show how COPY preserves identity while INSERT creates it, then derive the consequences — for link discovery, attribution, version comparison, and economic compensation. We shall find that the entire web of cross-document relationships rests on a single architectural choice: transclusion shares addresses rather than values.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store — once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a partial function from virtual positions to addresses, `poom(d) : Pos ⇀ Addr`. This is the document's current arrangement — which content appears where.
- **spanindex**: a relation recording which documents contain which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only.
- **links**: a set of link structures, each having three endsets (from, to, type), where endsets reference I-space address ranges.

Positions are subspace-qualified. A position `q = (s, k)` pairs a subspace `s` with an offset `k`, where `s = 0` for links and `s = 1` for text. The total ordering is lexicographic: all link positions `(0, _)` precede all text positions `(1, _)`, and within a subspace, offsets are ordered naturally. We define `link_subspace(d) = {q ∈ dom(poom(d)) : q.s = 0}`, `text_subspace(d) = {q ∈ dom(poom(d)) : q.s = 1}`, `size(poom(d)) = |text_subspace(d)|`, and the within-subspace shift `(s, k) ⊕ w = (s, k + w)`. This separation is the structural basis for TC8: text insertions shift text offsets without disturbing link positions. When the subspace is unambiguous, we write positions as bare offsets.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, and `poom(d).p` for the I-address that document d maps position p to. We use primed names for the state after an operation.

An I-space address encodes provenance structurally. Every address has the form `Node.0.User.0.Document.0.Element`, where each field is readable from the address alone. We write `a↓doc` for the document-level prefix of address `a` — the first five components `Node.0.User.0.Document` — which uniquely identifies the creating document. The Element field's first component identifies its subspace (1 for text, 2 for links). This encoding is intrinsic — no external index is needed to answer "who created this byte?"


## Content identity

We are looking for the right definition of "same content." In conventional systems, content identity is value-based: two strings are the same if they have the same characters. In Xanadu, content identity is address-based: two bytes are the same if and only if they have the same I-space address.

This is not a design whim. It is forced by the requirement that the system distinguish between independent creation and deliberate sharing. Nelson poses the scenario directly: if I type "Hello" into my document and you type "Hello" into yours, we have created content that is value-identical but identity-distinct. We did not share anything — we independently produced the same character sequence. No link, attribution, or economic relationship should connect our two instances. But if you transclude my "Hello" into your document, the system must recognize that your copy IS my content — that links to my text reach your display of it, that I receive attribution and compensation when your document is read.

We state this formally:

**TC0 (Identity is address).** Two content references in the system denote the same content if and only if they resolve to the same I-space address:

  `same(r₁, r₂) ≡ iaddr(r₁) = iaddr(r₂)`

where `iaddr(r)` extracts the I-space address that reference `r` points to. Value equality is neither necessary nor sufficient for identity. Two bytes at different I-addresses are distinct even if their content is the same character. Two references to the same I-address are identical even if they appear in different documents at different V-positions.

TC0 is what makes the system's cross-document relationships computable. Without it, every operation that asks "does this content appear elsewhere?" would require a full-text comparison of the entire docuverse — an operation that is both computationally infeasible and semantically wrong (it would falsely connect independently created identical text). With TC0, the question reduces to set intersection on I-addresses, which is both efficient and correct.

Nelson states this with precision. Five guarantees depend on shared identity: attribution ("You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]), correspondence ("unless it can show you, word for word, what parts of two versions are the same" [LM 2/20]), royalties ("there is a royalty on every byte transmitted... paid automatically by the user to the owner" [LM 2/43]), the distributed update solution ("we solve the problems of update... simply by windowing to a changing document" [LM 2/36]), and link survivability (links attach to I-addresses and follow content through transclusion). If two occurrences were independent copies with separate I-addresses, all five would collapse.


## The COPY operation

We now define what COPY does. The operation takes a source specification (a set of V-spans in one or more documents) and a target (a document and position), and makes the source content appear at the target position. The critical question is: how does the target document's mapping relate to the source's?

We begin with the precondition. COPY requires that its arguments be well-formed: the source and target documents must exist, the source V-span must be fully covered by the source's current POOM, and the insertion position must be valid in the target:

  `source_doc ∈ dom.documents ∧ target ∈ dom.documents`
  `source_span ⊆ dom(poom(source_doc))` — every position in the source V-span maps to an I-address
  `0 ≤ p ≤ size(poom(target))` — insertion at any position from the start to one past the end

Without these conditions, the postconditions would be vacuously satisfiable. An operation with precondition `false` satisfies any postcondition — which tells us nothing.

**TC2 (INSERT creates identity; COPY preserves it).** INSERT at position p in document d allocates fresh addresses `a₁, ..., aₙ` such that:

  `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom.ispace)` and `(A i : 1 ≤ i ≤ n : aᵢ ∈ dom.ispace')`

COPY from `source_span = [source_start, source_start + w)` in `source_doc` to `target` at position p creates no new addresses:

  `dom.ispace' = dom.ispace`

and deposits the source's I-addresses at the target positions in order:

  `(A i : 0 ≤ i < w : poom'(target).(p ⊕ i) = poom(source_doc).(source_start ⊕ i))`

where `w = |source_span|`. The mapping is pointwise — the i-th source position maps to the i-th target position. This is the sole architectural distinction between duplication and transclusion. Every observable behavioral difference — in link discovery, version comparison, attribution, compensation — flows from this single fact: INSERT allocates new I-addresses; COPY shares existing ones.

**TC1 (I-address preservation).** Every I-address in the source span appears in the target after COPY:

  `(A a : a ∈ iaddrs(source_span) : (E q : poom'(target).q = a))`

where `iaddrs(source_span) = {poom(source_doc).q : q ∈ source_span}`. TC1 is a corollary of TC2: the pointwise mapping guarantees that each source I-address is deposited at a specific target position, and existential weakening gives the weaker "appears somewhere" claim. No fresh I-addresses are allocated; `dom.ispace' = dom.ispace`.

Nelson states this with precision: "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations" [LM 4/11]. The term "virtual copies" is exact — no content is duplicated. The target document gains V-space positions that map to I-addresses belonging to the source.

Gregory confirms the data flow definitively. The implementation converts source V-spans to I-spans by reading the source document's POOM, obtaining the existing I-addresses. These I-addresses are then inserted (as-is, with no transformation) into the target document's POOM at the specified V-position. The POOM insertion function iterates over the source spans sequentially, advancing the target V-position after each span — preserving source order. The allocation function for content — the function that assigns fresh I-addresses — is never called during COPY. The I-addresses extracted from the source POOM are exactly the I-addresses deposited in the target POOM.


## COPY is specset-driven

A crucial property of COPY deserves immediate attention: COPY transfers whatever the source specset specifies. It performs no filtering, no validation of content type, no subspace-aware exclusion.

**TC3 (No content-type filtering).** COPY operates on the I-addresses obtained by converting the source span through the source document's POOM. The content type, subspace, or semantic classification of those I-addresses is not examined:

  `copied_addresses = iaddrs(source_span)`

regardless of whether those addresses fall in the text subspace (V ≥ 1.0), the link subspace (V < 1.0), or any other region.

Gregory confirms this emphatically. The COPY function receives a specset, converts it to I-spans, and passes those I-spans to the POOM insertion function. No filter is applied. If the specset covers link subspace V-spans (0.2.x), the link POOM entries are transferred — their I-addresses (which are link ISAs, not text content) are placed into the target's text subspace, producing semantically invalid content.

*(The implementation natively accepts a multi-document, multi-span specset as the source argument, resolving each component through its own document's POOM in a single atomic operation. The formal properties in this ASN are stated for the single-span, single-document case; the multi-document generalization is deferred.)*

This means the convention that COPY transfers only text content is enforced by the **caller**, not by the back end. The front end must construct specsets that cover only the text subspace (V ≥ 1.0) unless link transfer is specifically intended.

The contrast with CREATENEWVERSION is instructive. VERSION is the one operation that explicitly filters to text-only, regardless of source content. It retrieves only text subspace V-spans from the source, even when the source contains links. COPY has no such filter — it is the raw mechanism on which higher-level operations build conventions.

This is an instance of the broader pattern: the back end provides powerful primitives; the front end is responsible for using them correctly. The system does not enforce the subspace convention at the COPY level.


## The frame

We are not done until we have stated what COPY does NOT change. The frame conditions are as important as the effects.

**TC4 (Read-before-write).** COPY extracts I-addresses from the source document's pre-state POOM. The addresses to be copied are determined before any modification to the target:

  `copied = {poom(source_doc).q : q ∈ source_span}`

where `poom` (unprimed) denotes the pre-state. When `source_doc = target` (self-transclusion — a document transcludes content from itself), the target POOM is modified per TC7, but the addresses extracted are those from before the modification. When `source_doc ≠ target`, TC5 implies `poom'(source_doc) = poom(source_doc)` — the source POOM is unchanged as a consequence, not as an axiom.

**TC5 (Cross-document isolation).** COPY does not modify the POOM of any document other than the target:

  `(A d : d ≠ target : poom'(d) = poom(d))`

**TC6 (I-space invariance).** COPY does not modify ispace:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` and `dom.ispace' = dom.ispace`

No content is created, modified, or removed from the permanent store.

**TC7 (Target content preservation).** COPY at text position p in the target document preserves all existing content at positions before p — in any subspace — and shifts text positions at or beyond p forward by the copied width:

  `(A q : q ∈ dom(poom(target)) ∧ q < p : poom'(target).q = poom(target).q)`
  `(A q : q ∈ text_subspace(target) ∧ q ≥ p : poom'(target).(q ⊕ w) = poom(target).q)`

where `w = |source_span|` is the width of the copied content and `⊕` is the within-subspace shift defined earlier. The first clause quantifies over all of `dom(poom(target))`, not just `text_subspace` — any position in any subspace that precedes p is preserved. The second clause is restricted to `text_subspace` because the shift applies only within the insertion point's subspace. This is the same shift behavior as INSERT — both operations expand the text subspace at the insertion point and displace subsequent content rightward.

**TC8 (Subspace confinement of shifts).** The V-position shift caused by COPY is confined to the insertion point's subspace. Link positions within the target document are not affected by text-subspace insertions, and vice versa:

  `(A q ∈ link_subspace(target) : poom'(target).q = poom(target).q)`

TC8 is a corollary of TC7's first clause. Since all link positions `(0, _)` precede all text positions `(1, _)` in the lexicographic order, and the insertion point `p` is a text position, every link position `q` satisfies `q ∈ dom(poom(target)) ∧ q < p`. TC7's first clause — which quantifies over `dom(poom(target))`, not just `text_subspace` — directly gives `poom'(target).q = poom(target).q` for all such `q`. TC8 constrains the *shift*, not the *scope* — the question of *what content* is copied is governed by TC3.

**TC12 (Links invariance).** COPY does not create, modify, or remove links:

  `links' = links`

COPY modifies only the target document's POOM and the span index. The links set — the collection of link structures with their endsets — is unaffected. Link *discoverability* through a document changes when its POOM changes (TC11), but the links themselves are invariant under COPY.


## Non-contiguous spans

When the source V-span maps to non-contiguous I-address ranges — as happens when the source document has been edited since the content was first inserted — COPY must handle each contiguous region separately.

**TC9 (Automatic splitting).** If the source V-span maps to k non-contiguous I-address ranges `R₁, R₂, ..., Rₖ`, COPY creates k separate V→I mapping groups in the target, one per range, with contiguous V-positions:

  `(A i : 1 ≤ i ≤ k : target maps [pᵢ, pᵢ + |Rᵢ|) → Rᵢ)`

where `p₁ = p` (the insertion point), `pᵢ₊₁ = pᵢ + |Rᵢ|`, and each `Rᵢ` is a contiguous I-address range. The V-space in the target is contiguous even when the I-space is not.

Gregory confirms this is an emergent behavior of the retrieval mechanism, not a special case. The conversion of V-spans to I-spans walks the source POOM's tree, producing one output span per contiguous I-address region. The POOM insertion function iterates over this list, inserting each region separately. No special-case logic handles non-contiguity — the data structure naturally decomposes.


## Span index registration

When COPY places content in the target document, the span index must record this fact:

**TC10 (Index registration).** After COPY, the span index contains entries associating the target document with the copied I-address ranges:

  `(A a ∈ iaddrs(source_span) : (a, target) ∈ spanindex')`

The granularity of registration is per contiguous I-span, not per byte. If the source content maps to three non-contiguous I-address ranges, three index entries are created. Each entry records the I-address range and the target document's identity. The I-address ranges in these entries are identical to those in the source document's existing index entries — only the document identifier differs.

A consequence: the target document becomes independently discoverable via span index queries immediately after COPY. This independence is structural — the target's span index entries are its own, not references to the source's entries. If the source document subsequently empties itself (deleting all its content), the target's span index entries persist. The span index is append-only; no operation on the source can remove the target's entries.


## A concrete trace

*(The addresses below use a simplified single-component Element field for readability. In the full address form, Element is multi-component with the first component indicating subspace: e.g., the five text bytes would be `1.0.1.0.1.0.1.1` through `1.0.1.0.1.0.1.5`, where Element = 1.1..1.5 and the leading 1 marks the text subspace. The simplified form elides this nesting.)*

We verify the postconditions against a specific scenario. Document A (identifier `1.0.1.0.1`) contains "HELLO" at I-addresses `[1.0.1.0.1.0.1 .. 1.0.1.0.1.0.5]` — five bytes, contiguous in I-space. Document B (identifier `1.0.1.0.2`) contains "XY" at I-addresses `[1.0.1.0.2.0.1, 1.0.1.0.2.0.2]`, so `poom(B) = {0 → 1.0.1.0.2.0.1, 1 → 1.0.1.0.2.0.2}` and `size(poom(B)) = 2`. We execute COPY of A's V-span `[0,5)` into B at position `p = 1`.

**Precondition check.** A and B exist. A's V-span `[0,5)` is fully covered by `poom(A)` — five positions, each mapped. Insertion position `p = 1` satisfies `0 ≤ 1 ≤ 2 = size(poom(B))`. The precondition holds.

**TC4 (Read-before-write).** The source addresses are extracted from A's pre-state POOM: `copied = {1.0.1.0.1.0.1, ..., 1.0.1.0.1.0.5}`.

**TC1 (I-address preservation).** B's new mappings reference A's I-addresses. No fresh addresses are allocated; `dom.ispace' = dom.ispace`.

**TC7 (Target text preservation).** Position 0 in B is unchanged: `poom'(B).0 = poom(B).0 = 1.0.1.0.2.0.1` ("X"). The five copied bytes occupy positions 1 through 5. The old position 1 ("Y" at `1.0.1.0.2.0.2`) shifts to position 6: `poom'(B).6 = poom(B).1 = 1.0.1.0.2.0.2`. The resulting B has 7 positions:

  | pos | I-address | content | origin |
  |-----|-----------|---------|--------|
  | 0 | 1.0.1.0.2.0.1 | X | B (native) |
  | 1 | 1.0.1.0.1.0.1 | H | A (transcluded) |
  | 2 | 1.0.1.0.1.0.2 | E | A (transcluded) |
  | 3 | 1.0.1.0.1.0.3 | L | A (transcluded) |
  | 4 | 1.0.1.0.1.0.4 | L | A (transcluded) |
  | 5 | 1.0.1.0.1.0.5 | O | A (transcluded) |
  | 6 | 1.0.1.0.2.0.2 | Y | B (native) |

**TC9 (Automatic splitting).** The source maps to one contiguous I-address range (k=1), so a single mapping group is created at positions `[1, 6)`.

**TC10 (Index registration).** The span index gains an entry `([1.0.1.0.1.0.1 .. 1.0.1.0.1.0.5], B)`. B is now independently discoverable for A's content.

**TC13 (Structural attribution).** `home(1.0.1.0.1.0.3) = (1.0.1.0.1.0.3)↓doc = 1.0.1.0.1`, which is A's identifier. The "L" at position 3 in B is attributed to A — determinable from the address alone.

The trace confirms internal consistency: TC7 shifts exactly the positions at or beyond p=1; TC1 deposits exactly A's addresses; TC10 registers exactly those addresses under B. No property contradicts another.


## Independence of transclusions

We now derive the property that makes transclusion a robust sharing mechanism: independence from the source document's future mutations. The proof requires two general axioms about the system — properties that hold for all operations, not just COPY. We state them here because the independence theorem is their first application.

**AX1 (POOM isolation).** Every operation modifies the POOM of at most one document:

  `#{d : poom'(d) ≠ poom(d)} ≤ 1`

This is confirmed for each mutating operation individually: INSERT modifies the target document's POOM only; DELETE modifies the deleting document's POOM only; COPY modifies the target's POOM only (TC5); CREATENEWVERSION creates a new document's POOM without modifying the source's; MAKELINK modifies exactly one document's POOM — the home document — registering the link ISA in its link subspace, while documents whose content appears in the link's endsets are accessed read-only for V→I address conversion. Gregory confirms the mechanism: `docreatelink` calls `docopy` on the home document's POOM to place the link ISA, and `specset2sporglset` on each endset document's POOM to resolve V-addresses to I-addresses — the latter is a read-only traversal that never calls `insertpm` or any write operation on those documents' POOMs. Read-only operations (RETRIEVE, FINDDOCSCONTAINING, RETRIEVEENDSETS, find_links) modify no POOM. No operation reaches across document boundaries to modify another document's arrangement.

**AX2 (I-space permanence).** No operation removes addresses from `dom.ispace` or modifies existing content:

  `dom.ispace ⊆ dom.ispace'`
  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

The state definition already asserts this in prose ("once an address enters `dom.ispace`, it remains forever and its content never changes"). We now give it a label because the proofs that follow must cite it precisely. TC6 is the COPY-specific instance; AX2 is the general principle.

**Theorem (Transclusion independence).** If document B transcludes content at I-addresses `A` from document D, and subsequently D deletes that content from its POOM, then B's mapping to `A` is unaffected.

*Proof.* D's DELETE modifies at most D's POOM (by AX1). Since B ≠ D, `poom'(B) = poom(B)`. The I-addresses in `A` remain in `dom.ispace'` (by AX2) and `ispace'.a = ispace.a` for every `a ∈ A`. Therefore B's mapping is intact and the content is unchanged. ∎

This is stronger than it first appears. B's transclusion is not merely "safe for now" — it is unconditionally immune to anything D does. D can delete the content, rearrange it, transclude over it, create new versions. None of these operations touches B's POOM. The independence is not temporal ("D has not yet deleted it") but structural ("D's operations cannot reach B's state").

We observe that this guarantee is overdetermined — it follows from multiple independent principles, any one of which would suffice. The proof above uses POOM isolation (AX1) and I-space permanence (AX2). But the same conclusion follows from: (i) transclusion is reference, not copy — no bytes are moved, so there is nothing to "take back"; (ii) DELETE operates on V-space only and cannot touch I-space; (iii) ownership isolation — only a document's owner may modify it; (iv) I-space immutability — content at an I-address never changes. This defense-in-depth means that breaking the independence guarantee would require simultaneous violations of multiple foundational properties.

Nelson states the guarantee directly: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11]. The formal derivation confirms that this follows from cross-document isolation plus I-space permanence, not from any special-case protection of transclusions.

Similarly, INSERT in the source document is harmless to the target:

**Corollary (INSERT isolation).** If document B transcludes content from document A, and subsequently A inserts new content (shifting A's V-positions), B's POOM is completely unchanged.

INSERT in A modifies at most A's POOM (by AX1). Since B ≠ A, `poom'(B) = poom(B)`. The I-addresses that B references persist unchanged in ispace (by AX2). Gregory confirms that each document's POOM is a separate data structure with no shared nodes; operations on A's POOM physically cannot modify B's POOM.


## Links follow content, not containers

We can now state the fundamental link-following property of transclusion. Links in Xanadu attach to I-space addresses — to the bytes themselves, not to their position in any document. Nelson captures this with the strap-between-bytes metaphor: "A Xanadu link is not between points, but between spans of data" [LM 4/42].

Because links attach to I-addresses, and transclusion preserves I-addresses, links are automatically discoverable through transclusion. We must first define the terms precisely.

A link L has three endsets: `from(L)`, `to(L)`, and `type(L)`, each a set of I-addresses. We write:

  `endsets(L) = from(L) ∪ to(L)`

for the *discoverable* endsets — from and to only. Gregory's implementation confirms that link discovery operates on these two endsets: the `find_links` function queries the span index for from-endset and to-endset intersections, then takes their intersection when both are specified. The type endset is stored in the same span index (under a separate prefix tag) and is retrievable via `RETRIEVEENDSETS`, but does not participate in `find_links` discovery — the type filter is accepted syntactically but produces no results in the implementation. Link discovery is effectively a two-dimensional operation: from-address and to-address intersection.

For a document B, the set of I-addresses currently referenced is:

  `iaddrs_of(B) = {a : (E p : poom(B).p = a)}`

Link discoverability through B is then:

  `discoverable_links(B) = {L ∈ links : endsets(L) ∩ iaddrs_of(B) ≠ ∅}`

A link is discoverable through B if any I-address in its from or to endsets is currently mapped by B's POOM. This definition depends only on B's current POOM and the link's endset addresses — no other document's state is consulted.

**TC11 (Links follow transclusion).** After COPY of `source_span` into `target` at position p, every link whose endsets intersect the copied I-addresses becomes discoverable through the target:

  `discoverable_links'(target) ⊇ {L ∈ links : endsets(L) ∩ iaddrs(source_span) ≠ ∅}`

*Derivation.* TC1 guarantees `iaddrs(source_span) ⊆ iaddrs_of'(target)`. TC12 guarantees `links' = links`. Therefore any link L with `endsets(L) ∩ iaddrs(source_span) ≠ ∅` also satisfies `endsets(L) ∩ iaddrs_of'(target) ≠ ∅`, placing it in `discoverable_links'(target)` by definition.

This is not a feature that needs to be implemented on top of transclusion. It is a structural consequence of three design choices: (i) links reference I-addresses; (ii) transclusion preserves I-addresses (TC1); (iii) link search operates on I-addresses. No special-case logic is needed to "carry links across" a transclusion. The links were never attached to the source document — they were attached to the content, and the content is now visible in the target.

Gregory confirms the mechanism end-to-end. The link search function converts V-spans to I-spans by reading the searching document's POOM, then queries the span index for intersecting link endsets. The searching document's POOM is the only document-specific state consulted. If the searching document still references the I-addresses, the search succeeds — regardless of what has happened to the document that originally created the content.

A crucial observation: TC11's definition of `discoverable_links(B)` depends only on B's POOM and the link's endsets. It does not mention any other document. Therefore, if document D originally created the content and later deletes it from D's POOM, link discovery through B is unaffected — by AX1, D's deletion modifies only D's POOM, leaving B's POOM (and hence `iaddrs_of(B)`) unchanged. The independence is structural, not temporal: it does not matter *when* D deletes, because D's operations cannot reach B's state.

An important clarification: link visibility through transclusion is guaranteed at the discovery level but subject to filtering at the display level. Nelson describes "sieving" — user-controlled filters that select which links to show based on criteria such as origin, recency, or author. The guarantee is that links are *findable*, not that they are *automatically displayed*. A reader viewing transcluded content can always ask for all links and receive a complete answer; what the front end chooses to present is a separate concern.

Nelson: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay" [LM 2/46]. This applies regardless of whether the reader is viewing the content in its home document or in a transcluding document.


## Attribution is structural

We now turn to a property that Nelson considers among Xanadu's most important: the guarantee that content origin is always traceable. In conventional systems, attribution is metadata — an author tag, a copyright notice, a citation — that can be stripped, falsified, or simply omitted. In Xanadu, attribution is encoded in the address.

**TC13 (Structural attribution).** For every I-address `a ∈ dom.ispace`, the creating document is determinable from `a` alone:

  `home(a) = a↓doc`

where `a↓doc` is the document-level prefix (the first five components `Node.0.User.0.Document`), as defined in "The state we need." This function requires no index lookup, no metadata query, no external data. The address IS the attribution.

Nelson is explicit: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. And: "only when you step through the window — turning one glass page and going on in the next — do you reach the original that you wanted" [LM 2/34].

Because transclusion preserves I-addresses (TC1), the attribution of transcluded content is automatic and unseverable. When document B transcludes content from document A, the I-addresses in B's POOM still carry A's document identifier. No operation within the system can alter this — I-addresses are permanent, and the document field is part of the address. To sever the attribution, one would need to change the I-address itself, which violates the most basic permanence guarantee.

A subtlety: the I-address always reveals the **account** that created the content. Whether the real-world person behind that account is identifiable depends on publication choices — anonymous publication ("John Doe publication" [LM 2/60]) hides the real-world identity but not the account and document of origin. The structural guarantee is: you always know *which document* the content came from, even if you don't know *who* is behind that document.

This gives us a reverse traceability guarantee:

**TC14 (Reverse traceability).** The system provides an operation (FINDDOCSCONTAINING) that, given a set of I-addresses, returns all documents whose POOMs currently map to any of those addresses:

  `finddocscontaining(A) = {d : (E a ∈ A, p : poom(d).p = a)}`

This operation is sound because of TC0 (identity is address). Two documents contain "the same content" if and only if their POOMs map to the same I-addresses. The query is a set intersection on addresses, not a text comparison. Nelson: "This returns a list of all documents containing any portion of the material included by ⟨vspec set⟩" [LM 4/63].

A subtlety: the span index is an over-approximation (it records historical containment, not current containment). A query against the span index may return documents that no longer reference the content. A second check against each candidate document's current POOM is needed to filter stale results. The forward direction is exact: every document that currently references the I-addresses is in the span index. The reverse direction requires filtering.


## Correspondence as corollary

Transclusion's identity preservation enables content comparison between any two documents that share I-addresses — not only between versions of the same document. When CREATENEWVERSION creates a new version, it shares I-addresses with the source (for text content). Subsequent edits to one version create new I-addresses (via INSERT) or remove references (via DELETE), but do not affect the shared I-addresses. But the same sharing occurs through COPY between unrelated documents. Any two documents that share I-addresses (by whatever mechanism) exhibit correspondence.

The SHOWRELATIONOF2VERSIONS operation exploits this:

**TC15 (Correspondence by shared identity).** Two documents share content if and only if they share I-addresses:

  `correspondence(d₁, d₂) = {a : (E p₁ : poom(d₁).p₁ = a) ∧ (E p₂ : poom(d₂).p₂ = a)}`

This definition applies regardless of whether d₁ and d₂ are related by versioning, by transclusion, or by any chain involving both. Gregory confirms that the operation is purely I-address intersection — there is no check for version relationship. The operation's name ("SHOWRELATIONOF2VERSIONS") is misleading by modern standards; it detects I-address overlap between any two documents.

Nelson motivates this: "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same" [LM 2/20].

The key insight: the system does not compare text values to find matches. It compares I-addresses. Two passages that were independently typed have different I-addresses even if the text is identical. This means correspondence is provenance-based, not value-based — it tracks "what came from the same creative act" rather than "what happens to look the same."


## Depth irrelevance

Transclusion may be nested to arbitrary depth: document C may transclude from B, which transcludes from A. We must show that the properties hold regardless of depth.

**TC16 (Depth collapse).** If document B transcludes content from A, and document C transcludes that same content from B, then C's POOM maps to A's I-addresses directly — not to B's "copy" of them (there is no such copy):

  `poom(C).p = a ∧ home(a) = A`

regardless of the number of intermediate transclusion steps. The depth collapses to zero because every step preserves the original I-addresses. B's POOM maps to A's addresses; C's POOM maps to the same addresses (extracted from B's POOM, which holds A's addresses). There is no chain of intermediate addresses — the I-address is the same at every level.

Nelson makes this explicit with the glass-pane metaphor: "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely" [LM 2/34]. And more directly: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely: each having links to what was already in place" [LM 2/36].

Depth irrelevance is a consequence, not an axiom. It follows from TC1 (COPY preserves I-addresses) applied inductively: each COPY step extracts addresses from the source POOM and deposits them unchanged in the target. If the source's addresses are already A's addresses (by the induction hypothesis), the target's addresses are A's addresses too.

This gives us depth-independent attribution: `home(a)` returns A's document identity regardless of whether the reader is viewing A, B, or C. Depth-independent link discovery: links to A's I-addresses are found through C by the same mechanism as through A — TC11 cares only that the POOM maps to the link's endset addresses, not how many transclusion steps produced that mapping. And depth-independent compensation: every byte still traces to its original I-address regardless of the transclusion chain length.

Gregory confirms with a concrete trace: when C transcludes from B, the implementation reads B's POOM to extract I-addresses. Those are A's original I-addresses (deposited by B's earlier transclusion from A). The implementation writes those same addresses into C's POOM. The transitivity holds by the composition of identity-preserving operations.


## Derivative documents

Transcluded content cannot be modified through the transclusion. The target document holds V→I mappings to the source's I-addresses; those I-addresses are permanent and their content is immutable. You cannot change bytes you do not own — "Every document has an owner... Only the owner has a right to withdraw a document or change it" [LM 2/29]. And even the owner cannot change I-space content; only V-space arrangements are mutable.

But Nelson provides a powerful mechanism for creating what *appears* to be a modified version: the **derivative document**.

**TC17 (Derivative composition).** A derivative document is a document whose V-stream interleaves transcluded content (via COPY) with native content (via INSERT). The system distinguishes native from transcluded content structurally — by examining `home(a)` for each I-address in the POOM:

  `native(d, a) ≡ home(a) = d`
  `transcluded(d, a) ≡ home(a) ≠ d`

For every I-address `a` in a document d's POOM, `native(d, a)` and `transcluded(d, a)` are decidable from the address alone.

Nelson's example makes this concrete: to create an annotated version of someone else's document, you transclude the first part up to the passage you wish to comment on, INSERT your own commentary, then transclude the remainder. The reader sees a unified text; the system sees a composition of transclusions and native inserts. Nelson: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links" [LM 2/45]. And: "The old viewpoint is still present too — you can always say, 'Show me what this originally was'" [LM 2/45].

This is architecturally clean: the derivative author never touches the original bytes. The result is a new V-space arrangement that interleaves references to existing content with fresh content. Attribution is preserved structurally (different I-addresses have different home documents), and the royalty split follows automatically — transcluded bytes compensate the source author; native bytes compensate the derivative author. Nelson: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45].


## Economic consequence

Nelson designs an economic model where content creators receive compensation automatically when their content is viewed. The mechanism is a "cash register" per published document that increments whenever its bytes are delivered:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

Transclusion interacts with this model through identity preservation. When a reader views a compound document containing transcluded content, the system delivers bytes from their home locations. The royalty accrues at the home document — the one identified by `home(a)` for each byte `a`:

**TC18 (Compensation follows identity).** When content at I-address `a` is delivered to a reader from any document, compensation accrues to the owner of `home(a)`:

  `compensate(delivery(a)) → owner(home(a))`

This holds regardless of which document the reader is viewing, because `home(a)` is determined by the I-address, not by the viewing context.

Note that the royalty is triggered by *delivery*, not by *transclusion*. Creating a transclusion has no immediate economic effect — the V→I mapping is created, but no bytes are delivered. The economic event occurs when a reader retrieves content. This distinction matters: within the system, there is no mechanism to incorporate existing content that evades royalty. The COPY operation *is* transclusion — it shares I-addresses with the source rather than creating new content. There is no FEBE command that creates a true byte-for-byte duplicate with fresh I-addresses. To create genuinely new content at new I-addresses, you would have to INSERT — physically retyping the text.

Nelson is explicit about the boundary of enforcement: "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate" [LM 2/47]. Content copied *out of* the system (to paper, to disk) evades royalty. But such a copy is "frozen and dead, lacking access to the new linkage" [LM 2/48] — it loses all cross-document relationships.

Depth irrelevance (TC16) ensures this works across arbitrary transclusion chains. The 50th re-transclusion of a passage still carries the original creator's I-addresses, so compensation flows to the original creator.


## The publication contract

The economic model connects to a normative guarantee about content availability. Nelson's design specifies that publishing is an irrevocable grant of transclusion permission:

**TC19 (Publication grants transclusion).** All published content is available for transclusion by any participant. An author who publishes relinquishes the right to prevent transclusion:

  `published(d) ⟹ (A d' : any_participant(d') : may_transclude(d', d))`

Nelson is unambiguous: "since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document'" [LM 2/45]. And: "each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract" [LM 2/43].

The tradeoff is explicit: the author surrenders control but never loses compensation. Traditional copyright conflates two goals — compensating creators and controlling use. Nelson separates them. The economic right (TC18) is preserved; the control right is surrendered (TC19).

This gives rise to a three-tier accessibility model:

| Status | Transclusion permitted? | Compensation? | Withdrawal? |
|--------|------------------------|---------------|-------------|
| Private | Only by owner/designees | N/A | Free |
| Privashed | Universal access | No | At will |
| Published | Universal, irrevocable | Yes, per-byte | Only by lengthy due process |

Nelson: "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process" [LM 2/43]. The reason is precisely because others will have linked to and transcluded the content. Their links and transclusions — which are *their* property at *their* addresses — depend on continued access.


## Two window modes

We have described the COPY operation as capturing a snapshot: the I-addresses present in the source POOM at the moment of the operation. This is the time-fixed mode. Nelson specifies a second mode — location-fixed — that creates the appearance of a live connection:

**TC20 (Two reference modes).** A transclusion may be:

(a) *Time-fixed*: the target document's POOM maps to the I-addresses that were in the source POOM at the time of COPY. If the source is later revised, the target does not change.

(b) *Location-fixed*: the target tracks the current state of a source location, automatically reflecting revisions.

Nelson: "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically" [LM 2/37].

The FEBE COPY operation is the time-fixed primitive. It captures I-addresses at invocation time and deposits them in the target's POOM. The target has no structural dependency on the source's future state (by TC5, the target's POOM and the source's POOM are independent).

The location-fixed mode requires a higher-level mechanism — the front end re-resolves through the source document's current POOM on each access. When the source is edited, its POOM changes (new content gets new I-addresses, rearrangements change V→I mappings), and the front end follows. This mode is built on top of the time-fixed primitive, not beside it; it is the front end repeatedly executing the equivalent of "read the source's current POOM at this V-span and use those I-addresses."

Nelson frames the location-fixed mode as solving the distributed update problem: "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document" [LM 2/36].

For the abstract specification, we note that the back-end COPY operation provides the time-fixed semantics. Location-fixed windowing is a front-end concern — a usage pattern, not a distinct back-end operation. The back end need not distinguish between the two; it needs only to support the primitives that make both possible: COPY (for time-fixed capture) and V-to-I resolution of another document's current POOM (for location-fixed re-resolution).


## Transclusion permanence

The preceding properties establish what transclusion guarantees at the I-space and V-space level. But a distinct question concerns the *accessibility* of transcluded content:

**TC21 (Transclusion as reference, not cache).** Transcluded content is retrieved from its home location on each access. The transcluding document stores V→I mappings, not content:

  `display(d, p) = ispace.(poom(d).p)`

If `poom(d).p` is defined but `ispace.(poom(d).p)` is not retrievable (due to the home location being unavailable), the transcluding document has a gap at position p. There is no local fallback, no cached copy, no degradation to a previous value.

This is by design. Nelson: "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about" [LM 2/47].

The permanence of a transclusion therefore depends on the permanence of its source. The I-space permanence guarantee ensures that I-addresses remain valid forever and content at those addresses is immutable. What TC21 captures is the additional dependency: even if the content *exists* in ispace, its *retrievability* may depend on factors outside the formal model — network availability, storage funding, access permissions. The formal model guarantees that the V→I mapping is intact and the content is unchanged; the operational model adds the constraint that the content must be reachable.

The publication contract (TC19) provides the strongest retrievability guarantee: published content is contractually protected from casual withdrawal. Transclusions of published content inherit this protection.


## POOM representation transparency

One final property guards the boundary between abstract specification and implementation freedom. An implementation may choose to represent POOM entries in various ways — one entry per byte, one entry per contiguous I-span, or some intermediate representation. When COPY inserts I-addresses that are contiguous with existing entries in the target POOM, an implementation may silently coalesce them into a single entry (extending an existing mapping rather than creating a new one).

**TC22 (Semantic transparency of representation).** Two POOMs that define the same function from V-positions to I-addresses are semantically equivalent — they produce the same results for all operations that depend on the V→I mapping:

  `(A p : poom₁(p) = poom₂(p)) ⟹`
  `  link_discovery(poom₁) = link_discovery(poom₂) ∧`
  `  correspondence(poom₁, d₂) = correspondence(poom₂, d₂) ∧`
  `  attribution(poom₁) = attribution(poom₂)`

The condition for coalescing — same home document and I-address contiguity — precisely characterizes the cases where the mathematical I-address mapping is unchanged.

We must note a tension at the implementation level. Gregory's analysis reveals that the retrieval operation produces one output span per internal POOM entry (bottom crum). This means that two functionally equivalent POOMs — one with a single coalesced entry, one with two separate entries — may produce different numbers of output spans from a RETRIEVE operation. The mapping is identical; the representation of the answer differs.

For the abstract specification, we assert TC22: the V→I mapping is the abstraction, not the entry structure. Operations defined over the abstract mapping (link discovery, correspondence, attribution, content retrieval) are invariant under representation changes. The number of spans returned by a low-level retrieval is an implementation artifact. An alternative implementation that uses a different representation (hash table, sorted array, etc.) would produce different span counts but identical semantic results. Any client that depends on span count rather than span coverage is depending on the representation, not the abstraction.


## What transclusion is NOT

We have stated what COPY guarantees. We must equally state what it does NOT guarantee, to prevent over-specification.

Transclusion is not a cache. TC21 establishes that transcluded content is retrieved from its home location; there is no stored copy in the target document. The target holds mappings, not content.

Transclusion is not a subscription. The FEBE COPY operation captures the I-addresses of the source at the moment of the operation. If the source document subsequently has new content inserted, the transcluding document does not automatically see the new content. The I-addresses captured by COPY were the ones present at copy time; the new content has new I-addresses that the target does not reference. (The location-fixed window mode described in TC20 provides subscription-like behavior through front-end re-resolution, but this is not a back-end COPY property.)

Transclusion does not create bidirectional awareness. The source document has no record that its content was transcluded. The span index records that the target contains those I-addresses, but the source document's POOM is unchanged (by TC5, when source ≠ target). Discovering that content has been transcluded elsewhere requires the FINDDOCSCONTAINING query — it is not implicit in the source document's state.

Transclusion does not transfer links. COPY of text content (V ≥ 1.0) does not transfer link POOM entries (V < 1.0) from the source to the target. Links are *discovered* through transclusion (TC11) because link search operates on I-addresses and the target shares I-addresses with the source. But the target's POOM does not contain link entries from the source. The distinction is: link discoverability is automatic (via I-address sharing); link ownership is not transferred.


## Formal summary

We collect the structure. The COPY operation is a transformation `δ(Σ, COPY(source, target, p)) = Σ'` where:

*Precondition:* Source and target documents exist. The source V-span is fully covered by the source's POOM. The insertion position `p` satisfies `0 ≤ p ≤ size(poom(target))`.

*Effect:* The target document's POOM gains new V→I mappings at position `p`, referencing the I-addresses extracted from the source's pre-state POOM (TC4). No fresh I-addresses are allocated. The span index is extended with entries associating the target document with the copied I-address ranges.

*Frame:* I-space is unchanged (TC6). No document's POOM other than the target is modified (TC5). The link subspace of the target document is unchanged (when copying text content, TC8). The links set is unchanged (TC12). When `source ≠ target`, this implies the source POOM is unchanged; when `source = target`, the source POOM is the target POOM and reflects the modification.

*Scope:* COPY is specset-driven — it transfers whatever the specset specifies. Subspace filtering is a caller convention, not a back-end enforcement.

*Identity:* The I-addresses in the target after COPY are identical to those in the source — not copies, not translations, not re-allocations. TC0 defines content identity as address identity, and COPY preserves addresses.

*Consequences:* From identity preservation alone (TC1), combined with the general axioms (AX1, AX2), all of the following are derived rather than axiomatized:

| Consequence | Derivation |
|-------------|------------|
| Links follow transclusion (TC11) | Links reference I-addresses; COPY preserves I-addresses; link search operates on I-addresses |
| Attribution is unseverable (TC13) | The I-address encodes the home document; COPY preserves I-addresses |
| Correspondence detection works (TC15) | Shared I-addresses = shared content; COPY shares I-addresses |
| Compensation flows to origin (TC18) | Compensation keys on home(a); home is determined by I-address; COPY preserves I-addresses |
| Depth is irrelevant (TC16) | Each COPY step preserves I-addresses; induction over depth |
| Source mutations are harmless (TC11 + AX1) | POOM isolation + I-space permanence; link discoverability depends only on the searching document's POOM |
| Derivative documents are transparent (TC17) | Different home documents = different I-addresses; native vs. transcluded is decidable from address |

The power of the design is that all seven consequences flow from a single architectural choice — COPY shares I-addresses rather than allocating new ones — combined with the permanence guarantee. No special-case mechanisms are needed for any of these properties. They are structural consequences of identity preservation.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| TC0 | Content identity is I-address identity: same(r₁, r₂) ≡ iaddr(r₁) = iaddr(r₂) | introduced |
| TC1 | COPY preserves I-addresses: every source I-address appears in the target (corollary of TC2 by existential weakening); dom.ispace is unchanged | introduced |
| TC2 | INSERT allocates fresh I-addresses; COPY deposits source I-addresses at target positions pointwise in order: (A i : 0 ≤ i < w : poom'(target).(p ⊕ i) = poom(source_doc).(source_start ⊕ i)) | introduced |
| TC3 | COPY transfers whatever the source span specifies with no content-type filtering; multi-document specset support is deferred | introduced |
| TC4 | COPY extracts I-addresses from the source's pre-state POOM (read-before-write); source POOM unchanged when source ≠ target (by TC5) | introduced |
| TC5 | COPY does not modify the POOM of any document other than the target | introduced |
| TC6 | COPY does not modify ispace — no content is created, modified, or removed | introduced |
| TC7 | COPY at position p preserves all existing content at positions before p (any subspace); text positions at or beyond p shift by the copied width | introduced |
| TC8 | COPY's V-position shift is confined to the subspace of the insertion point; other subspaces are unaffected (corollary of TC7) | introduced |
| TC9 | Non-contiguous I-address ranges in the source are automatically split into separate mapping groups with contiguous V-positions in the target | introduced |
| TC10 | COPY registers the target document in the span index for the copied I-address ranges; the target becomes independently discoverable | introduced |
| TC11 | Links follow transclusion: after COPY, discoverable_links'(target) ⊇ {L ∈ links : endsets(L) ∩ iaddrs(source_span) ≠ ∅} (derived from TC1 + TC12) | introduced |
| TC12 | COPY does not create, modify, or remove links: links' = links | introduced |
| TC13 | Attribution is structural: home(a) = a↓doc is computable from the I-address alone, requiring no index | introduced |
| TC14 | FINDDOCSCONTAINING returns all documents whose POOMs currently map to a given set of I-addresses (with possible stale over-approximation from span index) | introduced |
| TC15 | Two documents share content iff they share I-addresses; correspondence is address intersection, not value comparison; works across COPY and VERSION alike | introduced |
| TC16 | Transclusion depth collapses: after N transclusion steps, the I-addresses are still the original creator's; all properties hold depth-independently | introduced |
| TC17 | Derivative documents interleave COPY and INSERT; native vs. transcluded content is decidable from home(a) ≟ d | introduced |
| TC18 | Compensation accrues to owner(home(a)) for each delivered byte a, regardless of which document delivers it | introduced |
| TC19 | Publication is an irrevocable grant of universal transclusion permission; published content cannot be withheld from transclusion | introduced |
| TC20 | Two reference modes: time-fixed (COPY captures I-addresses at invocation) and location-fixed (front-end re-resolves through source's current POOM) | introduced |
| TC21 | Transclusion is reference, not cache: transcluded content is retrieved from the home location, with no local fallback | introduced |
| TC22 | POOM representation (entry count, coalescing) is semantically transparent: operations over the V→I mapping are invariant under representation changes | introduced |
| AX1 | Every operation modifies the POOM of at most one document (verified for INSERT, DELETE, COPY, CREATENEWVERSION, MAKELINK; read-only ops modify none) | introduced |
| AX2 | No operation removes addresses from dom.ispace or modifies existing ispace content | introduced |
| Σ.poom | poom(d) : Pos ⇀ Addr — per-document V→I arrangement mapping | introduced |
| Σ.spanindex | spanindex ⊆ Addr × DocId — append-only reverse index from I-addresses to documents | introduced |
| endsets | endsets(L) = from(L) ∪ to(L) — the discoverable endsets of a link (from and to only; type endset does not participate in discovery) | introduced |
| iaddrs_of | iaddrs_of(B) = {a : (E p : poom(B).p = a)} — I-addresses currently referenced by document B | introduced |
| discoverable_links | discoverable_links(B) = {L ∈ links : endsets(L) ∩ iaddrs_of(B) ≠ ∅} | introduced |
| home | home(a) = a↓doc — document-level prefix (Node.0.User.0.Document) identifying the creating document | introduced |
| native | native(d, a) ≡ home(a) = d — content was created by document d | introduced |
| transcluded | transcluded(d, a) ≡ home(a) ≠ d — content was created by another document | introduced |


## Open Questions

Must the system guarantee any mechanism by which a transcluding document is notified that its source content has become unretrievable, or is silent failure (a gap in the display) the specified behavior?

What invariant must the system maintain to ensure that FINDDOCSCONTAINING filters stale span index entries — and must this filtering be exact, or may it over-approximate?

When content is transcluded from a document the reader lacks permission to access directly, what must the system guarantee about the visibility of that content and its associated links?

Must the system provide an operation that distinguishes native content (created by INSERT) from transcluded content (placed by COPY) within a document, or is this distinction visible only through address inspection?

What must the system guarantee about the atomicity of COPY when the source specifies multiple non-contiguous spans — must all spans be copied or none, or may a partial copy be observable?

Under what conditions, if any, may the system defer the span index registration (TC10) relative to the POOM insertion — and what queries might return incomplete results during the window between them?

What must the system guarantee about COPY when the source document is concurrently being modified — must the extracted I-addresses reflect a consistent snapshot of the source's POOM?

Must the royalty split (TC18) be computed per-byte, per-span, or per-delivery — and what granularity of accounting is sufficient to satisfy the economic model?

What must location-fixed windowing (TC20) guarantee about the "sameness" of the tracked location when the source document's V-space is rearranged — must it follow content (via I-address correspondence) or position (via V-offset)?

What convention must the front end enforce to prevent COPY from placing link ISAs into the text subspace — and must the back end provide any validation, or is this purely a caller obligation?
