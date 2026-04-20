# ASN-0007: Links and Endsets

*2026-02-23*

We wish to understand what bidirectional links must guarantee. Xanadu's most distinctive claim is that its links are not the fragile, unidirectional pointers of conventional hypertext — they are permanent, bidirectional, typed associations between arbitrary spans of content. When content is edited, deleted, or rearranged, the links survive. When content is shared across documents through transclusion, the links follow. We seek the formal properties that make these guarantees possible, and discover that they all flow from a single architectural choice: endsets reference content identity, not content position.

The approach is: define what a link is in the abstract state, establish endset semantics, derive survivability as a theorem from permanence, then work outward to discovery, resolution, and the cross-context visibility guarantees. We begin with the state we need.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store — once an address enters `dom.ispace`, it remains forever (permanence) and its content never changes (immutability).
- **poom(d)**: for each document d, a function from virtual positions to addresses, `poom(d) : Pos → Addr`. This is the document's current arrangement — which content appears where.
- **links**: the set of all link structures in the system. Each link has a home document, three endsets, and a permanent address in I-space.

An I-space address encodes provenance structurally. Every address has the form `Node.0.User.0.Document.0.Element`, where each field is readable from the address alone. The Element field's first component identifies the *subspace*: 1 for text, 2 for links. We write `sub(a)` for this first element-field component.

We assume the following properties hold (they are established elsewhere but we state them here for self-containment):

**P0 (Address permanence).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation removes an address from the store.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (V-space mutability).** Editing operations (INSERT, DELETE, REARRANGE) modify `poom(d)` for a single document d while leaving `ispace` unchanged. I-space is the permanent substrate; V-space is the ephemeral arrangement.


## What a link is

A link is a permanent I-space object. It is not metadata, not an annotation, not an overlay — it occupies addresses in the link subspace (sub = 2) of its home document's I-space. Nelson: "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms" [LM 4/41].

We define a link as a quadruple:

**LK0 (Link structure).** A link L is a tuple `(home, from, to, type)` where:
- `home ∈ DocId` — the document that owns the link, determining ownership and access control.
- `from : ISpanSeq` — the source endset, an ordered sequence of I-space spans.
- `to : ISpanSeq` — the target endset, an ordered sequence of I-space spans.
- `type : ISpanSeq` — the type endset, an ordered sequence of I-space spans.

Each endset is a sequence of spans, where a span is a pair `(start, width)` of I-space addresses. Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" [LM 4/42]. The strap metaphor is precise — a link binds to specific bytes identified by their permanent I-space addresses.

The three endsets are structurally identical. Nelson confirms the symmetry: "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets" [LM 4/44]. From-set, to-set, and type are distinguished by role, not by structure. Each is an arbitrary collection of spans pointing anywhere in the docuverse.

The home document is independent of the endsets. Nelson: "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document" [LM 4/12]. This separation is fundamental — it means your commentary link about someone else's work lives at your address, under your control.


## Endsets reference identity, not position

We now state the central property from which nearly everything else follows:

**LK1 (Endsets are I-space references).** Each span in a link's endsets references content by permanent I-space address, not by V-space position:

  `(A L ∈ links, e ∈ {from, to, type}, s ∈ L.e : s.start ∈ Addr_I)`

where `Addr_I` is the I-space address domain. The endset does not contain V-space positions, document identifiers for specific views, or any other ephemeral reference.

Nelson states this directly: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. And: "since the links are to the bytes themselves" — the emphasis on "the bytes themselves" is the I-space identity claim.

LK1 is what separates Xanadu links from conventional hyperlinks. A URL points to a *location* — a server, a path, a position. When the content at that location changes, the URL may point to something different, or to nothing. An I-space address points to a *byte* — a specific piece of content with a permanent identity. When the byte moves in V-space, the address does not change.

Nelson explains why V-space references would fail: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this" [LM 4/11]. V-space is "constantly changing." Building survivable links on something that constantly changes is impossible.


## Endsets reach anywhere

An endset is not confined to the home document, to a single document, or even to content that currently exists:

**LK2 (Unrestricted endset scope).** Each endset may reference I-space addresses in any document, across any number of documents:

  `(A L ∈ links, e ∈ {from, to, type} : (A s ∈ L.e : s.start ∈ dom.ispace ∨ s.start ∈ ghost_addresses))`

Nelson: "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse" [LM 4/43]. And more remarkably: "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements" [LM 4/45]. Endsets may point to addresses where no content has been stored — ghost addresses used as type identifiers.

The ghost address provision is essential. Link types in Xanadu are not drawn from a fixed vocabulary of labels — they are themselves endsets pointing to I-space spans. A type endset may point to content that describes the link type (a "footnote" label, an "annotation" marker), or it may point to ghost addresses that serve purely as type identifiers without associated content. The system places no restriction on what addresses an endset may reference.


## Link permanence and immutability

Links, being I-space objects, inherit the permanence guarantees of I-space:

**LK3 (Link permanence).** Once a link `L` enters the system, it cannot be removed from I-space:

  `L ∈ links ⟹ L ∈ links'`

This follows from P0. A link occupies I-space addresses in the link subspace (sub = 2) of its home document. P0 guarantees those addresses persist. The link's existence is a permanent fact in the docuverse.

**LK4 (Endset immutability).** A link's endsets cannot be modified after creation:

  `(A L ∈ links : L.from' = L.from ∧ L.to' = L.to ∧ L.type' = L.type)`

This follows from P1. The endsets are I-space content — they are the data stored at the link's I-space addresses. P1 guarantees that content at an I-space address never changes.

The FEBE protocol confirms this structurally. The protocol defines exactly one link-creation command (MAKELINK) and zero link-modification commands. The editing operations (INSERT, DELETEVSPAN, REARRANGE, COPY, APPEND) apply to document text content, not to links. What the system IS defined to do with links: create them, find them, retrieve their endsets, count them, and remove them from a document's current view. What it cannot do: change an endset.

Nelson: "The links designated by a tumbler address are in their permanent order of arrival" [LM 4/31]. Even the arrival order is permanent.

The only way to "change" a link is to delete it from the current version (removing it from V-space, where "deleted links" become "not currently addressable, awaiting historical backtrack functions" [LM 4/9]) and create a new link with different endsets. Even deletion does not destroy — the old link remains in I-space, recoverable through historical mechanisms.


## Link storage structure

We now describe how a link's endsets are stored within the link's I-space object. This detail is abstract — it concerns the semantic structure of the link, not its physical representation.

**LK5 (Endset separation).** The three endsets occupy distinct, non-overlapping regions within the link object. Each endset is retrievable independently of the others:

  `retrieve(L, FROM) yields L.from`
  `retrieve(L, TO) yields L.to`
  `retrieve(L, TYPE) yields L.type`

The retrieval of one endset does not depend on the resolvability or content of the other two.

Gregory confirms the mechanism: the three endsets are stored at distinct V-positions within the link orgl — from-set at position range 1.x, to-set at 2.x, type at 3.x. The constants LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 define these boundaries. The FOLLOWLINK operation takes a `whichend` parameter (1, 2, or 3) that selects exactly one endset for extraction.

**LK6 (Endset order preservation).** When a link is created with a multi-span endset (multiple disjoint I-ranges in a single endset), the spans are stored in the order provided by the creator, and retrieval returns them in the same order:

  `create(L, from=[s₁, s₂, ..., sₙ]) ⟹ retrieve(L, FROM) = [s₁, s₂, ..., sₙ]`

This holds because spans are stored at sequentially increasing V-positions within the link orgl, and retrieval sorts by V-position, which reconstructs the original order. Whether an alternative implementation preserves span ordering by V-position sorting or by some other mechanism is irrelevant; the abstract guarantee is that the sequence is preserved.


## Survivability

We are now ready to derive the central guarantee. Link survivability is not an axiom — it is a theorem that follows from LK1 (endsets reference I-space) combined with P2 (editing operations modify V-space only).

**LK-SURV (Survivability theorem).** For any editing operation `op ∈ {INSERT, DELETE, REARRANGE, COPY}` applied to any document d:

  `(A L ∈ links : L.from' = L.from ∧ L.to' = L.to ∧ L.type' = L.type)`

*Proof.* By LK4 (endset immutability), which follows from P1. But we must verify that each operation's effects are consistent with this claim — that no operation has a side effect on link endsets.

**Case INSERT(d, p, c).** INSERT allocates fresh I-addresses for the new content and modifies `poom(d)`. It does not modify any link's endsets (links are in I-space; INSERT modifies V-space). The fresh I-addresses are disjoint from all existing addresses, so they cannot collide with any address referenced by any endset. ∎

**Case DELETE(d, vspan).** DELETE removes V-space mappings from `poom(d)`. It does not modify I-space — the content at the deleted I-addresses persists (by P0), and the link endsets (which are themselves I-space content) persist unchanged (by P1). ∎

**Case REARRANGE(d, vspan₁, vspan₂).** REARRANGE moves V-space positions — it changes which I-addresses appear at which V-positions. I-space is untouched. Link endsets reference I-space. Therefore link endsets are unaffected. ∎

**Case COPY(source, target, p).** COPY creates new V-space mappings in the target document using existing I-addresses from the source. No I-space content is created or modified. Link endsets are unchanged. ∎

Nelson states the guarantee compactly: "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43].

The "if anything is left at each end" condition deserves attention. In Xanadu, content is never truly destroyed — DELETE removes V-space references but I-space content persists (P0). So the condition "anything is left" is trivially satisfied at the I-space level: the bytes are always there. The condition becomes non-trivial only at the V-space level — whether any of the link's referenced bytes are currently *visible* in some document's arrangement. This distinction matters for link resolution (below) but not for link existence.


## V-space consequences of editing

While link endsets do not change, editing operations change the *V-space appearance* of linked content. We must characterize these effects.

**LK7 (INSERT may fragment V-space contiguity).** If a link endset references a contiguous I-address range that maps to a contiguous V-span in some document, and INSERT places new content in the middle of that V-span, the endset's V-space appearance becomes discontiguous:

Before INSERT:
  `L.from = {(i₁, w)}` (one I-span)
  `poom(d)` maps `[v₁, v₁+w)` → `[i₁, i₁+w)` (contiguous)

After INSERT of width k at V-position v₁+j (where 0 < j < w):
  `L.from = {(i₁, w)}` (unchanged — same I-span)
  `poom'(d)` maps:
    `[v₁, v₁+j)` → `[i₁, i₁+j)` and
    `[v₁+j+k, v₁+w+k)` → `[i₁+j, i₁+w)` (two V-regions, one I-span)

Nelson anticipated this directly: "We see from above that one end of a link may be on a broken, discontiguous set of bytes" [LM 4/42]. The endset is a "strap between bytes" — inserting new bytes between the strapped bytes stretches the visual display but does not stretch the strap. The strap still binds to exactly the original bytes.

The new content receives fresh I-addresses (by INSERT's allocation guarantee). These addresses are not in any link's endset. The link's endset covers exactly what it covered before — no more, no less.

**LK8 (DELETE removes V-space visibility, not I-space existence).** If content referenced by a link endset is deleted from a document, the endset's I-space references remain valid but may not resolve to any V-position in that document:

  `(A s ∈ L.from : s.start ∈ dom.ispace' ∧ ispace'.(s.start) = ispace.(s.start))`

The content still exists at its permanent address. It has merely been removed from the current V-space view. Nelson: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. And: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11].

A link to deleted content is not broken. It is a link to content that is currently invisible in one version but permanent in I-space. The content may still be visible in other versions of the same document, in other documents that transclude it, or in the version history.

**LK9 (REARRANGE preserves all V-space visibility).** REARRANGE moves content to new V-positions but does not remove any content from V-space:

  `(A a ∈ range(poom(d)) : a ∈ range(poom'(d)))`

Therefore every I-address that was V-resolvable before REARRANGE remains V-resolvable after. The link endset resolves to the same I-addresses at (possibly different) V-positions. This is the strongest case of survivability — not only does the link survive, but its entire endset remains fully resolvable.


## Link discovery

We now turn to how links are found. The central guarantee is symmetry: links are discoverable from any direction.

**LK10 (Discovery by I-address intersection).** The operation `findlinks(constraint)` returns the set of all links whose endsets satisfy the constraint. The constraint specifies, for each of the three endset roles (from, to, type), a set of I-addresses that must have non-empty intersection with the corresponding endset. The satisfaction condition is:

  `satisfies(L, C) ≡ (A e ∈ constrained(C) : iaddrs(L.e) ∩ C.e ≠ ∅)`

where `iaddrs(L.e)` is the set of all I-addresses covered by endset e's spans, and `constrained(C)` is the set of endset roles that C specifies (unconstrained roles impose no restriction).

Nelson specifies this as the single operation FINDLINKSFROMTOTHREE, which accepts constraints on all four dimensions simultaneously — home-set, from-set, to-set, and type. "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" [LM 4/58].

**LK11 (Discovery symmetry).** The satisfaction condition LK10 treats all three endset roles identically. No endset is privileged:

  `findlinks(from=A, to=*, type=*) discovers all links whose from-set touches A`
  `findlinks(from=*, to=A, type=*) discovers all links whose to-set touches A`
  `findlinks(from=*, to=*, type=A) discovers all links whose type touches A`

Nelson: "it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time" [LM 2/37–2/40]. The reader can ask "What links here?" (constrain the to-set) as easily as "What links from here?" (constrain the from-set).

This symmetry is Nelson's answer to the backlinks problem. Traditional hyperlinks are one-directional — you can follow a link forward but cannot discover what points at you. Nelson: "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work" [LM 2/43]. Free linking and discoverable in-links are inseparable aspects of the same design.

**LK12 (Partial overlap suffices).** Discovery requires only that the constraint's I-addresses *intersect* the endset's I-addresses — not that they cover the endset completely:

  `iaddrs(L.from) ∩ C.from ≠ ∅ ⟹ L satisfies from-constraint C.from`

If a link's from-set spans I-addresses `{i₁, i₂, i₃, i₄, i₅}` and the query covers only `{i₃}`, the link is discovered. This is essential for links whose V-space appearance has been fragmented by editing: a query covering any single fragment discovers the link.

Gregory confirms the mechanism: link discovery operates on I-address intersection within the span index. The query's V-addresses are first converted to I-addresses through the querying document's POOM. These I-addresses are intersected with the link endsets stored in the span index. Partial overlap suffices — a search specset that shares even one I-address with a link endset will discover that link.

**LK13 (Per-endset independence in discovery).** When the query constrains multiple endset roles, each role is searched independently and the results are intersected:

  `findlinks(from=A, to=B) = findlinks(from=A) ∩ findlinks(to=B)`

The discovery of links whose from-set touches A does not depend on the resolvability of their to-sets, and vice versa. If a link's from-set is fully reachable but its type endset has become a ghost (all referenced content deleted from V-space), the link is still discoverable through its from-set.

Gregory confirms this directly: when `find_links` is called with a source constraint but no type constraint, the type endset is not consulted at all. The operation searches only the specified endset dimensions in the span index, then intersects the per-dimension results. An unresolvable type endset has no effect on discovery through source or target.

**LK14 (Scale-independent discovery).** The system must guarantee that the number of non-matching links does not impede search:

  `performance(findlinks(C)) is independent of |{L ∈ links : ¬satisfies(L, C)}|`

Nelson is explicit: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60]. This is not a complexity guarantee — it is a design requirement. The indexing mechanism must be structured so that irrelevant links are eliminated without examination.


## Link resolution

Finding a link is not the same as following it. Discovery (LK10) returns a set of link identifiers. *Resolution* converts a link's endset into V-space positions within a specific document.

**LK15 (Resolution is document-relative).** Following a link's endset produces V-addresses relative to a specific document's POOM:

  `follow(L, e, d) = {(d, v) : (E i ∈ iaddrs(L.e) : poom(d).v = i)}`

The operation takes a document parameter and resolves I-addresses through that document's POOM. If the same I-addresses appear in multiple documents (through transclusion or versioning), the resolution depends on which document is specified.

Gregory reveals a subtlety: the FOLLOWLINK implementation resolves through the *creation-time* document stored in the link's sporgl structures, not through the document used in the discovery query. When a link is created with the target endset specified as V-spans in document A, the link permanently stores A's document identifier along with the I-addresses. A subsequent FOLLOWLINK resolves through A's POOM, even if the link was *discovered* through document B (which shares I-addresses with A through transclusion). The creation-time document binding is immutable — it is part of the link's I-space content.

This means discovery and resolution may produce different documents. You can discover a link by querying from document B (because B shares I-addresses with the link's endset), but following that link takes you to V-positions in document A (the creation-time context). The front end may then translate from A to B using correspondence (shared I-addresses between versions), but this is a front-end decision, not a back-end guarantee.

**LK16 (Partial resolution).** When only some I-addresses in an endset are currently mapped by a document's POOM, resolution returns a partial result — the V-addresses of the mapped I-addresses — without error:

  `follow(L, FROM, d) = {(d, v) : (E i ∈ iaddrs(L.from) : poom(d).v = i)}`

Three cases arise:

(a) All I-addresses mapped → full result.

(b) Some I-addresses mapped, some not → partial result, containing only the mapped addresses.

(c) No I-addresses mapped → empty result. The operation succeeds with an empty answer.

Gregory confirms this at the code level: the I-to-V conversion function iterates through each I-address in the endset. For each address, it queries the specified document's POOM. If the POOM returns no mapping (the I-address is not in any V-position of that document), the address is silently dropped from the result. There is no error, no indication to the caller that the result is partial.

This silent partial resolution is the operational meaning of Nelson's survivability condition "if anything is left at each end" — the link survives in the sense that it returns whatever it can find. Partial survival is the norm, not an error condition.

**LK17 (Endset resolution independence).** The resolution of each endset is independent. If a link's from-set resolves fully but its to-set resolves empty, the from-set resolution succeeds:

  `follow(L, FROM, d) is defined independently of follow(L, TO, d')`

Gregory confirms that the three endsets are extracted and resolved separately. The RETRIEVEENDSETS operation retrieves all three, but each endset's resolution depends only on whether its specific I-addresses have POOM mappings. The success or failure of one endset has no effect on the others.


## V-space fragmentation upon resolution

When an endset whose I-addresses are contiguous is resolved through a document whose POOM maps those addresses to non-contiguous V-positions (due to intervening INSERTs or REARRANGE operations), the result contains multiple V-spans:

**LK18 (Resolution produces V-span sets).** The resolution of a single I-span in an endset may produce multiple V-spans:

  `follow_span((istart, iwidth), d) = {(vstart₁, vwidth₁), ..., (vstartₖ, vwidthₖ)}`

where each `(vstartⱼ, vwidthⱼ)` is a maximal contiguous V-range whose I-addresses fall within `[istart, istart+iwidth)`. The V-spans are grouped within a single document result (one VSpec with multiple VSpans), not returned as separate document results.

Gregory confirms the mechanism: the I-to-V conversion walks through the document's POOM, finding all V-regions that map to the queried I-range. Each contiguous V-region produces one V-span. If INSERT or REARRANGE has fragmented the original contiguity, multiple V-spans result within the same document. The result structure contains one document entry with an arbitrary number of V-spans within it.


## Cross-version visibility

Versions share I-space content. When CREATENEWVERSION creates a new version of a document, the new version's POOM maps to the same I-addresses as the original (for text content). Since link endsets reference I-addresses, and since discovery operates by I-address intersection, a link to the original is simultaneously a link to all versions sharing those I-addresses.

**LK19 (Version-spanning discovery).** If document d₁ and d₂ share I-addresses (by versioning, transclusion, or any other mechanism), and link L's endset references some of those shared I-addresses, then L is discoverable from both d₁ and d₂:

  `iaddrs(L.e) ∩ iaddrs(poom(d₁)) ≠ ∅ ∧`
  `iaddrs(poom(d₁)) ∩ iaddrs(poom(d₂)) ⊇ iaddrs(L.e) ∩ iaddrs(poom(d₁))`
  `⟹ iaddrs(L.e) ∩ iaddrs(poom(d₂)) ≠ ∅`

Nelson: "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions" [LM 2/26].

The mechanism is not magical — it is structural. Versions share I-addresses. Links reference I-addresses. Discovery intersects I-addresses. The three facts compose to give cross-version visibility without any version-aware logic in the link subsystem.

**LK20 (Temporal ordering does not affect discovery).** A link created *after* a version branch is discoverable from the version, and a link created on the version is discoverable from the original, provided they share the relevant I-addresses:

  `(A L ∈ links, d₁, d₂ : iaddrs(L.e) ∩ iaddrs(poom(d₁)) ≠ ∅ ∧`
  `  iaddrs(L.e) ∩ iaddrs(poom(d₂)) ≠ ∅ :`
  `  L ∈ findlinks_from(d₁) ∧ L ∈ findlinks_from(d₂))`

The link index stores I-address ranges without timestamps or causal ordering. A query from any document that shares I-addresses with the link's endset discovers the link, regardless of whether the link was created before or after the document's version branch.

Gregory confirms: the link index (span index) stores I-address-to-link mappings without document filtering. When querying from a version, the system converts V-addresses to I-addresses through the version's POOM, then searches the span index for matching links. No check is made on whether the link was created before or after the version was branched. The query is purely I-address intersection.

Nelson explains why old versions must persist: "the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version" [LM 2/43]. Links "reach through" across versions because all versions sharing the same I-addresses are connected by content identity.


## Transclusion and link discovery

Transclusion creates the same I-address sharing as versioning. When document B transcludes content from document A, B's POOM maps V-positions to A's I-addresses. Since link discovery operates on I-address intersection, a link whose endset touches those I-addresses is discoverable from both A and B:

**LK21 (Transclusion-spanning discovery).** If `poom(B).v = a` and `a ∈ iaddrs(L.from)`, then L is discoverable from document B at position v, regardless of whether B is the link's home document, the content's home document, or neither:

  `a ∈ iaddrs(poom(B)) ∧ a ∈ iaddrs(L.from) ⟹ L ∈ findlinks(from=a, context=B)`

At the I-space level, there is no distinction between "original" and "transcluded appearance." The content at address `a` is the same content regardless of which document's POOM maps to it. Nelson: "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it" [LM 4/45]. Endsets map to the universal tumbler line, not to document-local positions. Since transclusion shares tumbler-line positions (I-addresses), link discovery is automatically transclusion-aware.

The depth of transclusion is irrelevant. If C transcludes from B which transcludes from A, C's POOM maps to A's original I-addresses (transclusion preserves I-addresses at every step). A link to A's I-addresses is discoverable from C by the same mechanism as from A or B.


## Link creation and ownership

**LK22 (Freedom to link).** Any participant may create a link to any published content, regardless of ownership:

  `published(d) ⟹ (A user : may_create_link(user, endsets_touching(d)))`

Nelson: "each user is free to link to anything privately or publicly" [LM 2/43]. No permission is required. No approval workflow. If the content is published, you can link to it.

**LK23 (Target author cannot suppress links).** The author of published content cannot prevent incoming links or suppress their discoverability:

  `published(d) ⟹ ¬(E op : op removes discoverability of links touching d)`

Nelson: "each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract" [LM 2/43]. The relinquishment is contractual — it is the price of publishing. You surrender control over incoming links; in exchange, you receive automatic royalty compensation when your content is delivered.

**LK24 (Ownership by home document).** A link's owner is determined by its home document, not by its endsets:

  `owner(L) = owner(L.home)`

This means a link connecting two documents you don't own is still *your* link, housed in *your* document. The endsets can point anywhere in the docuverse; the home document determines who owns the link and who may delete it from the current version.


## Completeness of discovery

**LK25 (Completeness within access domain).** Within the domain of content the querying user is authorized to access, the system must return ALL links satisfying the query constraint:

  `findlinks(C, user) = {L ∈ links : satisfies(L, C) ∧ accessible(L, user)}`

Nelson: "If the home-set is the whole docuverse, all links between these two elements are returned" [LM 4/63]. The word "all" is deliberate. The system returns every matching link, not a sample, not a ranked subset.

**LK26 (Privacy as the sole visibility boundary).** A link housed in a private document is legitimately invisible to non-authorized users. This is the only permitted reason for a link to be excluded from discovery results:

  `¬accessible(L, user) ≡ private(L.home) ∧ ¬authorized(user, L.home)`

Nelson: "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone" [LM 2/42]. A private link to published content is a valid state — the link creator chose privacy. A published link to published content is always discoverable.

The system must not filter results editorially. Nelson: "Some advocates of Artificial Intelligence would have computers decide what the reader shall see. As a filtering service this may be just what you want — but the danger is its evolving into a circumscription of your rights, where the choice is no longer yours" [LM 3/21]. The user controls filtering (through sieving by attributes such as location, author, time); the system provides completeness within the access domain.

**LK27 (User-controlled sieving).** The system provides a filtering mechanism for managing the abundance of discovered links, but sieving narrows what the user *chooses to see*, not what the system *can return*:

  `sieve(findlinks(C, user), criteria) ⊆ findlinks(C, user)`

Nelson: "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]. Remove all sieving criteria, and you get the complete result set.


## Span index structure

The link discovery guarantees above require an indexing structure that supports efficient I-address intersection queries. We note the structure abstractly:

**LK28 (Per-I-span indexing).** Each I-span within each endset of a link is independently indexed. If a link's from-set contains two non-contiguous I-ranges, two index entries are created — one per I-span, not one per endset:

  `(A L ∈ links, e ∈ {from, to, type}, s ∈ L.e : (s, L, e) ∈ spanindex)`

This granularity is necessary for LK12 (partial overlap suffices): a query that touches any one I-span of a multi-span endset must discover the link. If the index stored only whole-endset references, the system would need to load and intersect entire endsets during search, violating the LK14 scale-independence requirement.

Gregory confirms: `insertendsetsinspanf` iterates through each I-span in each endset, calling `insertnd` once per I-span. A link with a two-span from-set, a one-span to-set, and a one-span type produces four span index entries (tagged with LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN respectively). Each entry maps an I-address range to a link identifier.


## Formal summary

We collect the structure. A link is a permanent I-space object LK0 whose endsets reference content identity LK1, not position. Endsets are immutable LK4 and their I-space references persist through all editing operations (LK-SURV), with the V-space appearance potentially fragmented LK7 but the I-space content unchanged LK8.

Discovery operates by I-address intersection LK10, is symmetric across all three endset roles LK11, requires only partial overlap LK12, and is independent per endset role LK13. Discovery is complete within the user's access domain LK25, with privacy as the sole visibility boundary LK26.

Resolution is document-relative LK15 and produces partial results when not all endset I-addresses are mapped LK16. The three endsets resolve independently LK17.

Cross-context visibility arises structurally: because versions and transclusions share I-addresses, and because discovery operates on I-address intersection, links are automatically visible across all documents that share the relevant content (LK19, LK20, LK21).

The power of the design is that every guarantee beyond LK0 and LK1 is *derived*. Survivability is a theorem from endset immutability and I-space permanence. Cross-version visibility is a theorem from I-address sharing and intersection-based discovery. Link completeness is a stated requirement, but the mechanism that achieves it — the span index with per-I-span granularity — follows naturally from the decision to index by content identity rather than position. The entire architecture of bidirectional, survivable, transclusion-aware links rests on the single foundation: endsets reference I-space addresses, and I-space is permanent.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LK0 | A link is a tuple (home, from, to, type) where each endset is an ordered sequence of I-space spans | introduced |
| LK1 | Endsets reference content by permanent I-space address, not by V-space position | introduced |
| LK2 | Endsets may reference I-addresses in any document, including ghost addresses where no content is stored | introduced |
| LK3 | Once a link enters the system, it cannot be removed from I-space (follows from P0) | introduced |
| LK4 | A link's endsets cannot be modified after creation (follows from P1) | introduced |
| LK5 | The three endsets occupy distinct regions and are independently retrievable | introduced |
| LK6 | Multi-span endsets preserve span ordering from creation through retrieval | introduced |
| LK-SURV | INSERT, DELETE, REARRANGE, and COPY do not modify any link's endsets (theorem from LK4, P1, P2) | introduced |
| LK7 | INSERT may fragment a contiguous endset's V-space appearance into multiple V-spans without altering the I-space references | introduced |
| LK8 | DELETE removes V-space visibility of linked content but does not affect I-space existence or endset validity | introduced |
| LK9 | REARRANGE preserves all V-space visibility of linked content — the strongest survivability case | introduced |
| LK10 | Link discovery operates by I-address intersection: a link satisfies a query when each constrained endset shares at least one I-address with the corresponding constraint | introduced |
| LK11 | Discovery is symmetric across from-set, to-set, and type — no endset role is privileged | introduced |
| LK12 | Partial I-address overlap suffices for discovery — a query touching any fragment of an endset discovers the link | introduced |
| LK13 | Per-endset independence in discovery: each constrained role is searched independently, results intersected | introduced |
| LK14 | Scale-independent discovery: the count of non-matching links does not impede search | introduced |
| LK15 | Resolution is document-relative: following a link produces V-addresses through a specific document's POOM | introduced |
| LK16 | Partial resolution: when only some endset I-addresses are POOM-mapped, the mapped portion is returned without error | introduced |
| LK17 | Endset resolution independence: success/failure of one endset does not affect the others | introduced |
| LK18 | A single I-span may resolve to multiple V-spans when editing has fragmented V-space contiguity | introduced |
| LK19 | Links are discoverable from any document sharing the relevant I-addresses (version-spanning visibility) | introduced |
| LK20 | Temporal ordering of link creation relative to version branching does not affect discoverability | introduced |
| LK21 | Links are discoverable through transclusion: same I-addresses in any document's POOM suffice | introduced |
| LK22 | Any participant may create a link to any published content, regardless of ownership | introduced |
| LK23 | The author of published content cannot suppress incoming links or their discoverability | introduced |
| LK24 | Link ownership is determined by home document, independent of endset targets | introduced |
| LK25 | Discovery is complete within the user's access domain — all matching accessible links are returned | introduced |
| LK26 | Privacy (link's home document is private and user is unauthorized) is the sole visibility boundary | introduced |
| LK27 | User-controlled sieving narrows display, not system capability | introduced |
| LK28 | Each I-span in each endset is independently indexed in the span index | introduced |
| P0 | No operation removes an address from I-space (assumed) | introduced |
| P1 | Content at an I-space address never changes (assumed) | introduced |
| P2 | Editing operations modify V-space (poom) while leaving I-space unchanged (assumed) | introduced |


## Open Questions

Must the system guarantee that FOLLOWLINK resolves through the creation-time document's POOM, or may an implementation resolve through the querying document's POOM — and what semantic differences would each choice produce?

When a link's endset references I-addresses that span a document boundary (bytes from two different home documents within a single endset span), must the system guarantee contiguous treatment or may it split at document boundaries?

What must the system guarantee about the atomicity of MAKELINK — must the link's three endsets and their span index entries all be committed atomically, or may a partially indexed link be observable?

Must the span index guarantee exact correspondence with current link state, or may it over-approximate (containing entries for deleted links) as the POOM span index does for document content?

What invariants must the system maintain about ghost addresses in type endsets — may a ghost address later become a real address through content allocation, and if so, does the type endset retroactively gain content?

When a link's creation-time document is itself deleted (removed from V-space), what must the system guarantee about the link's continued resolvability through other documents sharing the same I-addresses?

Must multi-endset discovery (constraining from AND to simultaneously) guarantee that returned links satisfy BOTH constraints, or may the intersection be approximate?

What must the system guarantee about link ordering in discovery results — must links be returned in creation order, in I-address order, or is the order unspecified?

Under what conditions may the system defer span index updates relative to link creation — and what queries might return incomplete results during the window between link storage and index update?

What convention must the front end enforce when presenting a link discovered through transclusion — must it indicate the creation-time document context, or may it present V-addresses relative to the discovery document?
