# ASN-0022: Ghost Link Discoverability

*2026-02-26*

We wish to understand what happens to link discoverability when the content a link references ceases to appear in any document's current view. The question is precise: a link's endset names certain I-space addresses; those addresses still hold content (I-space is append-only); but no document's V-space arrangement currently maps to those addresses. The link is structurally intact — it has not been modified or destroyed. Yet the standard mechanism by which users discover links begins with V-space content and works inward. What must the system guarantee about finding such a link? Can it be discovered at all? If the content reappears through transclusion, does the link become discoverable again without intervention? These questions expose a deep asymmetry between a link's *existence* and its *reachability*, and the formal analysis reveals that this asymmetry is not a defect but an architectural consequence of separating identity from arrangement.

Nelson's design intent is unambiguous: links point to permanent content, content is never destroyed, and therefore links never lose their targets. "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43]. Since I-space is append-only, "anything is left at each end" is satisfied by construction — the bytes exist forever at their I-addresses. In Nelson's model, the scenario we describe should be unremarkable. A link to content is a link to that content wherever it appears, and the content always exists somewhere (in I-space, if nowhere else).

Gregory's implementation reveals a subtler picture. The system maintains three independent layers — permanent content storage, a persistent link index, and per-document arrangement mappings (POOMs). Content deletion removes only the arrangement mapping. The link index retains all entries permanently. But the standard discovery path *begins* by translating V-space positions to I-addresses through the arrangement mapping, and *then* consults the link index. When no arrangement mapping exists for the target I-addresses, the translation step produces nothing, and the link index is never reached. The link is present in the index but invisible through the standard query path. We call this state *ghosting*.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function `ispace : Addr → Content`, the permanent store. Once an address enters `dom.ispace`, it remains forever (permanence) and its content never changes (immutability).
- **poom(d)**: for each document d, a partial function `poom(d) : Pos → Addr`, the document's current V-space arrangement. This is mutable — editing operations change it.
- **lindex**: a relation from I-address ranges to link identifiers, tagged by endset role, `lindex ⊆ IRange × LinkId × Role`. This is the persistent link index.
- **links**: the set of all link objects. Each link L has endsets `L.from`, `L.to`, `L.type`, each a set of I-space spans.

We write `iaddrs(L.e)` for the set of all I-addresses covered by the spans in endset e of link L. We write `live(a)` for the predicate "there exists a document d and position v such that `poom(d).v = a`" — content at address a is *live* if some document currently displays it. We write `range(poom(d))` for the set of I-addresses in the range of `poom(d)` — all content currently arranged in document d.

We assume three foundational properties, derived from first principles:

**P0 (I-space permanence).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation removes an address.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'(a) = ispace(a))` — content never changes.

**P2 (V-space mutability).** Editing operations modify `poom(d)` while leaving `ispace` and `lindex` unchanged.


## Link index permanence

We must first establish a property of the link index that is independent of I-space permanence but structurally parallel to it. When a link is created, the system records an entry in `lindex` for each endset, mapping the endset's I-address range to the link's identifier. The critical property is that this entry is *never removed*:

**G0 (Index permanence).** For every link L admitted to the system and every endset role e ∈ {from, to, type}:

  `(A r : r ∈ iaddrs(L.e) : (r, L, e) ∈ lindex) ⇒ (A r : r ∈ iaddrs(L.e) : (r, L, e) ∈ lindex')`

Once an index entry exists, no operation removes it. The link index grows monotonically: `lindex ⊆ lindex'`.

G0 is the index analogue of P0. Together they establish that the permanent layer of the system — content and link associations — only accumulates. Nelson's design makes this inevitable: in a system where content is permanent and links attach to content identity, the link-to-content association cannot be severed without destroying either the link or the content, neither of which the append-only model permits.

Gregory confirms G0 structurally: the link index implementation has insertion operations but no deletion operations. The `DELETE` operation on a document's V-space calls only the arrangement-modification path; no index-removal path exists in the call chain. Gregory's evidence reveals that the DELETE path contains a placeholder where index cleanup was once contemplated but never implemented. Whether G0 reflects deliberate design or fortunate incompletion, the structural fact is the same: no index-removal mechanism exists, and the monotonicity property holds unconditionally.

We note the frame condition: DELETE modifies `poom(d)` and does not modify `lindex`. INSERT modifies `poom(d)` and `ispace` and does not modify `lindex`. COPY modifies `poom(d)` and adds entries to `lindex` (for document-containment indexing) but never removes entries. No operation decreases `lindex`.


## The V→I bridge

Link discovery, as experienced by a user, begins with visible content. The user sees text on screen, selects a region, and asks "what links touch this?" The system must translate the user's V-space selection into I-space addresses before consulting the link index:

**G1 (Discovery through content identity).** The system discovers links by computing the I-address set corresponding to a V-space region and intersecting that set with `lindex`:

  `discover(d, v_region) = { L : (E r : r ∈ iaddrs_of(d, v_region) : (r, L, e) ∈ lindex) }`

where `iaddrs_of(d, v_region) = { poom(d).v : v ∈ v_region ∧ v ∈ dom.poom(d) }`.

The function `iaddrs_of` is the V→I bridge. It produces I-addresses only for V-positions that have current POOM entries. If a V-position has no POOM entry (because content was deleted or rearranged away), it contributes nothing to the I-address set. This is not a failure — it is correct behavior. The V-position is empty; there is no content there to discover links for.

The V→I bridge is the *only* path through which normal discovery operates. There is no mechanism in the standard protocol by which a user provides raw I-addresses for link search. The user works in V-space; the front end translates; the back end searches. Nelson explicitly places this translation in the front end: "None of these commands are to be seen by the user... the complications of the protocol are to be handled invisibly by programs in the user's front-end machine" [LM 4/61].


## Ghosting: the state between existence and reachability

We are now prepared to define the ghost state precisely. Consider a link L with endset e referencing I-addresses A = iaddrs(L.e). The link was created when content at addresses A appeared in some document's V-space. Later, that content was deleted from all documents' V-spaces. What is L's status?

We observe three facts simultaneously:

1. **L exists.** The link object occupies permanent I-space addresses. P0 guarantees it persists.
2. **L is indexed.** G0 guarantees that `(A r : r ∈ A : (r, L, e) ∈ lindex)`. The index entries persist.
3. **L is unreachable through V-space.** For every document d: `A ∩ range(poom(d)) = ∅`. No V-space region maps to addresses in A. Therefore `iaddrs_of(d, any_region)` never produces elements of A. Therefore `discover(d, any_region)` never returns L via endset e.

We define the ghost predicate on a per-endset basis:

**G2 (Ghost endset).** An endset e of link L is *ghost* at state Σ if and only if:

  `ghost(L, e) ≡ iaddrs(L.e) ≠ ∅ ∧ (A d : d ∈ Documents : iaddrs(L.e) ∩ range(poom(d)) = ∅)`

The endset references real I-space content (the first conjunct confirms it is non-vacuous) but no document currently arranges any of that content (the second conjunct).

**G3 (Ghost link).** A link L is *ghost* if all three of its endsets are ghost:

  `ghost(L) ≡ ghost(L, from) ∧ ghost(L, to) ∧ ghost(L, type)`

A fully ghost link is one where no endset can contribute to discovery through any document's V-space. It exists in the permanent layer, is indexed, but is entirely unreachable through standard V-addressed queries.

We note the intermediate state: a link may have *some* ghost endsets and some live ones. We define the partial ghost:

**G4 (Partial ghost).** A link L is *partially ghost* if at least one but not all endsets are ghost:

  `partial_ghost(L) ≡ (E e : e ∈ {from, to, type} : ghost(L, e)) ∧ ¬ghost(L)`

This matters. A link whose *from* endset is live but whose *to* endset is ghost is still discoverable from the source side. The link appears in the result of `discover(d, region)` when the source content is in d's V-space. But when the user follows the link to its target, the target resolution produces nothing — the I-addresses in `L.to` map to no V-positions in any document.


## The discovery/resolution asymmetry

We have uncovered a fundamental asymmetry. Discovery and resolution are two different operations with different dependencies:

**Discovery** asks: "what links touch this content?" It operates through the V→I bridge on the *queried* content, then consults `lindex`. It requires only that the queried endset's content be live in some document.

**Resolution** asks: "where does this link's endset point?" It reads the link's stored endset I-addresses, then attempts I→V conversion in a specific document context. It requires that the *target* endset's content be live in the resolved document.

**G5 (Discovery-resolution independence).** Discovery of a link through endset e₁ is independent of the liveness of endset e₂:

  `¬ghost(L, e₁) ⇒ L ∈ discover(d, region) for some d, region covering iaddrs(L.e₁)`

regardless of whether `ghost(L, e₂)` holds for any other endset e₂.

This follows directly from G1: discovery via endset e₁ requires only that `iaddrs_of(d, region) ∩ iaddrs(L.e₁) ≠ ∅`, which depends solely on e₁'s liveness and the index entry, not on e₂'s state.

Gregory's evidence confirms this precisely. When a link's target content is deleted from all V-spaces while its source content remains live, `find_links` from the source document still discovers the link. The source's I-addresses translate through the source document's POOM, reach the link index, and find the link's source-endset entry. The target's ghosted state is irrelevant to this query. But `follow_link` to the target returns an empty V-span set — the I-addresses in the target endset have no current V-space positions.

The asymmetry is not a defect. It preserves the fundamental guarantee that links survive editing. A user who deletes content from their document cannot thereby make other users' links to *other* content undiscoverable. Each endset's liveness is independent.


## The I→V filter

We must now formalize what happens when the system attempts to resolve an endset whose content is partially or fully ghost. The resolution path is: read the link's stored I-addresses, then convert each to V-positions in a specified document context.

**G6 (Silent I→V filtering).** When converting I-addresses to V-positions in document d, any I-address a for which `a ∉ range(poom(d))` is silently excluded from the result:

  `resolve(L, e, d) = { v : (E a : a ∈ iaddrs(L.e) ∧ poom(d).v = a : true) }`

No error is raised. No placeholder is inserted. The address simply does not appear in the output. The operation succeeds — it returns the (possibly empty) set of V-positions.

This is a precise guarantee: `resolve(L, e, d)` is always well-defined and never fails. It may return the empty set, but it never signals an error based on the absence of I-addresses from d's POOM. Gregory confirms: the implementation returns `works: true` with an empty result set, not an error, when all endset I-addresses are unreferenced.

We derive an immediate consequence. Let A = iaddrs(L.e) and partition A into live and ghost portions relative to document d:

  `A_live(d) = A ∩ range(poom(d))`
  `A_ghost(d) = A \ range(poom(d))`

Then `resolve(L, e, d) = { v : (E a : a ∈ A_live(d) : poom(d).v = a) }`.

**G7 (Partial resolution).** If some I-addresses in an endset are live and others are ghost, resolution returns the live portion only:

  `A_live(d) ⊂ A ∧ A_live(d) ≠ ∅ ⇒ resolve(L, e, d) ≠ ∅ ∧ #resolve(L, e, d) < #A`

The user sees a partial endset — the surviving fragment of the original. This is consistent with Nelson's survivability conditional: "If any of the bytes are left to which a link is attached, that link remains on them" [LM 4/42]. The link does not vanish entirely when part of its endset is deleted; it clings to whatever remains.


## Resolution is document-relative

We pause to note a crucial property that ghosting exposes. Resolution is not absolute — it is relative to a specific document context.

**G8 (Document-relative resolution).** For a given link L, endset e, and two documents d₁ and d₂:

  `resolve(L, e, d₁) ≠ resolve(L, e, d₂)` in general

even when both documents contain some of the endset's I-addresses. The V-positions differ because each document has its own arrangement.

This means that after content is deleted from document d₁ and transcluded into document d₂, the same link's endset *could* resolve to:
- Empty in d₁ (the content was deleted from d₁'s POOM)
- Non-empty in d₂ (d₂'s POOM maps fresh V-positions to the same I-addresses)

We say "could" because this requires the resolution mechanism to accept a document-context parameter. Gregory's implementation reveals a significant gap: the resolution path reads the endset's I-addresses, then always resolves against the *original* document stored at link creation time — not the document through which the link was discovered. The implementation provides no mechanism for the caller to specify an alternative document context. This means that following a link discovered through a transclusion in d₂ may attempt resolution in d₁ — the original document — and produce empty results even though d₂ has the content.

The abstract guarantee must be stated carefully:

**G9 (Resolution well-definedness).** For any link L, endset e, and document d, `resolve(L, e, d)` is well-defined as a mathematical function. The system *should* provide a mechanism by which the front end can specify which document context to resolve against. Without such a mechanism, the full benefit of re-discoverability (G10, below) is limited: a link may be discoverable from a new document but its endset may resolve against the original document, producing empty results.

Nelson's design intent favors document-context flexibility: "the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version — if it's still there" [LM 2/43]. The back end should provide the I→V conversion primitive parameterized by document context; the front end should choose the context. Whether to resolve against the original document, the transcluding document, or a historical version is a front-end design decision. But the back end must support the choice. Gregory's implementation does not yet fulfill this requirement — resolution is hard-coded to the creation-time document context.


## Re-discoverability through transclusion

We arrive at the central theorem of ghost link behavior. When content that was ghost — absent from all V-spaces — is re-introduced into some document through transclusion (COPY), the ghost links to that content become discoverable again. No re-indexing, no re-linking, no administrative intervention is required.

We establish this formally. Suppose link L has endset e with `iaddrs(L.e) = A`, and A is currently ghost: `(A d : d ∈ Documents : A ∩ range(poom(d)) = ∅)`. Now COPY introduces some or all of A into a new document d_new at V-positions V_new:

  `COPY postcondition: (E v ∈ V_new, a ∈ A : poom'(d_new).v = a)`

After COPY:
- `A ∩ range(poom'(d_new)) ≠ ∅` — some of A is now live in d_new
- `ghost'(L, e) = false` — the endset is no longer ghost
- `iaddrs_of(d_new, V_new)` now produces elements of A
- `discover(d_new, V_new)` now returns L

**G10 (Automatic re-discoverability).** If content at I-addresses A becomes live in document d through COPY, then every link L with `iaddrs(L.e) ∩ A ≠ ∅` becomes discoverable from d through endset e, without any modification to L or to `lindex`:

  `(E a : a ∈ iaddrs(L.e) ∩ A : (a, L, e) ∈ lindex) ∧ A ⊆ range(poom'(d))`
  `⇒ L ∈ discover'(d, V_new)`

The proof is immediate. G0 guarantees the index entry `(a, L, e)` persists. COPY establishes `a ∈ range(poom'(d))`. Therefore `a ∈ iaddrs_of(d, V_new)`. Therefore the index lookup returns L.

We note a caveat informed by the resolution gap identified at G9: while the link becomes *discoverable* from d_new, *following* the link may still resolve against the original document and return empty. Full re-discoverability — where the user can both find and follow the link to visible content — requires that the resolution mechanism accept d_new as the document context. Discovery and resolution are independent (G5), and the current implementation provides re-discoverability of the link but not necessarily re-resolvability of its endsets from the new context.

The power of G10 lies in what it does *not* require. It does not require that L's creation predated the deletion. It does not require that d_new is related to the document from which A was deleted. It does not require that d_new's owner knows about L. The re-discoverability is a structural consequence of two permanence properties (P0 for content, G0 for the index) and the identity-based discovery mechanism (G1). Any document that transcludes the content inherits all links to that content — automatically, immediately, unconditionally.

This is Nelson's deepest insight about the relationship between links and transclusion: "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26]. The principle extends beyond versions to any form of content sharing. A link to content is a link to that content wherever it appears — in any document, any version, any context. The mechanism is always the same: shared I-addresses, permanent index entries, discovery through identity.


## The ghost state is reachable but not permanent

We now characterize the ghost state's dynamics. Ghosting is:

1. **Reachable.** Any link can become ghost through sufficient deletion. If every document that contains L.e's content deletes that content from its V-space, L.e becomes ghost.

2. **Reversible.** G10 guarantees that transclusion reverses ghosting. The transition ghost → live is always available (assuming the system can identify the I-addresses to transclude).

3. **Not catastrophic.** A ghost link is not broken, not destroyed, not corrupted. It is *indexed but unreachable through V-addressed queries*. The distance between ghost and live is exactly one COPY operation.

We formalize the lifecycle:

**G11 (Ghost state transitions).** For a link L with endset e:

  `live(L, e) ≡ ¬ghost(L, e)` — content is arranged in some document

  Transition `live → ghost`: occurs when `DELETE` removes the last POOM mapping to any I-address in `iaddrs(L.e)`.

  `wp(DELETE(d, v), ghost(L, e)) = (A d' ≠ d : iaddrs(L.e) ∩ range(poom(d')) = ∅) ∧ poom(d).v ∈ iaddrs(L.e)`

  That is, L.e becomes ghost when the deleted position was the *last* V-space reference to L.e's content. The weakest precondition requires that (a) no other document references the content, and (b) the deleted position held content from the endset. If any other document retains the content, the endset remains live.

  Transition `ghost → live`: occurs when COPY introduces any I-address from `iaddrs(L.e)` into any document's POOM:

  `wp(COPY(d, v, a), ¬ghost(L, e)) = a ∈ iaddrs(L.e)`

  A single COPY of a single address from the endset is sufficient to restore liveness. The endset need not be fully reconstituted — partial liveness suffices for discovery by G5.

Nelson captures this dynamic with his description of deleted bytes as "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The phrase "awaiting historical backtrack functions" is precisely the ghost → live transition: the content exists, the links exist, and the system needs only a mechanism to re-introduce the content into some V-space.


## Transclusion suppresses ghosting

A corollary of G10 and G11 deserves explicit statement, because it captures a fundamental design property:

**G12 (Transclusion as ghost suppression).** If content at I-addresses A is transcluded into n documents, then ghosting of any endset referencing A requires deletion from all n documents:

  `(A L, e : iaddrs(L.e) ∩ A ≠ ∅ : ghost(L, e) ⇒ (A d : d ∈ Documents : A ∩ range(poom(d)) = ∅))`

The more widely content is transcluded, the harder it is to ghost links to that content. Nelson's design intent is explicit: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11]. Deletion is local to a document. Transclusion creates redundancy that protects link discoverability.

For published content, Nelson strengthens this to a social guarantee: "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process" [LM 2/43]. Published content, by policy, cannot be removed — and therefore links to published content can never become ghost. The permanence obligation of publication exists *because* of links: "This is vital because of the links other users may have made to it" [LM 2/43].


## The I-address query path

We have established that ghost links are unreachable through V-addressed queries (the standard discovery path). But the system also supports queries specified directly in I-addresses, bypassing the V→I bridge entirely.

**G13 (I-address discovery).** If a query is specified using I-addresses directly (rather than V-space positions requiring POOM translation), then ghost links are discoverable:

  `(A L, e : (E r : r ∈ iaddrs(L.e) : (r, L, e) ∈ lindex) : L ∈ discover_by_iaddr(r))`

regardless of whether `ghost(L, e)` holds.

Gregory confirms this with a precise structural observation: the link search function accepts query terms in two forms — V-space specifiers (which require POOM translation) and I-space specifiers (which bypass it). When I-space specifiers are used, the query goes directly to the link index. The ghost state is irrelevant because the V→I bridge is never traversed.

This means the ghost state is a property of the *query path*, not of the link itself. The link is always present in the index. Whether it is reachable depends on how the query is expressed. V-addressed queries pass through the POOM bottleneck; I-addressed queries do not.

The implications for the abstract specification are significant. A system satisfying G0–G12 could still choose to expose I-address queries to users (or to front ends), which would eliminate the ghost phenomenon entirely. Nelson's protocol does not specify such an operation in the standard FEBE command set — all 17 operations use V-space specifiers for link search. But the back end's capability to handle I-address queries exists, and a front end that maintained an I-address cache (for example, remembering the I-addresses of recently viewed content) could use this path to discover ghost links.


## What the system must never do

We collect the negative guarantees — properties that assert what the system must *not* do in the ghost state:

**G14 (No false failure).** Following a link whose target endset is ghost must not produce an error. It must produce a successful, possibly empty, result:

  `ghost(L, to) ⇒ resolve(L, to, d) = ∅ ∧ operation_succeeds`

The link is valid. The I-addresses exist. The content exists. There is simply no current V-space arrangement to map them into. Reporting an error would be incorrect — nothing has gone wrong. Reporting "link not found" would be incorrect — the link was found. The only correct response is: the link exists, its target has no current V-space position.

**G15 (No ghost contagion).** The ghost state of one endset must not affect the liveness of other endsets:

  `ghost(L, to) ⇒ ¬ghost(L, from)` is *not* implied; conversely, `ghost(L, to)` does *not* imply `ghost(L, from)` or `ghost(L, type)`.

Each endset ghosts independently based solely on whether its own I-addresses appear in any POOM. Gregory notes one anomalous exception: in the implementation, when both source and target are ghost, the type endset also returns empty even when type content remains live. This appears to be a bug rather than an architectural requirement — the abstract specification asserts endset independence without exception.

**G16 (No index degradation).** Ghost links must not cause the link index to degrade, slow down, or produce incorrect results for non-ghost queries:

  `(A L_live : ¬ghost(L_live, e) : discover(d, region) returns L_live correctly regardless of #ghost_links)`

Nelson states this directly: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60]. Ghost links are simply links that don't satisfy V-addressed queries. They must not impede the discovery of links that do.


## Ghost elements and the deeper principle

Nelson supports an even more radical case than ghost links — ghost *elements*, where a link's endset points to addresses at which no content has ever been stored:

"It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them" [LM 4/23].

This goes beyond G2. A ghost endset (as we defined it) has content at its I-addresses that is merely not arranged in any V-space. A ghost *element* endset has addresses where `a ∉ dom.ispace` — nothing was ever created there. The link still exists and the endset still points to those addresses.

**G17 (Ghost element validity).** A link's endset may reference addresses outside `dom.ispace`. Such a link is valid, exists in the system, and occupies space in the link index:

  `(A L ∈ links, e ∈ {from, to, type} : iaddrs(L.e) ∩ dom.ispace = ∅ does not contradict L ∈ links)`

If ghost element links are valid, then ghost links (where the content exists but is not arranged) are *a fortiori* valid. The ghost state is strictly less extreme than the ghost element state, and if the system handles the more extreme case, it must handle the less extreme one.

This also means that `live(a) ⇒ a ∈ dom.ispace` (live content must exist in I-space), but the converse fails: `a ∈ dom.ispace` does not imply `live(a)`. And for ghost elements, even the first implication does not apply — the endset points to addresses with no content at all.


## The front end's obligations

Nelson explicitly places presentation decisions with the front end. The back end provides primitives (link search, endset retrieval, version reconstruction); the front end composes them into a user experience. For ghost links, we identify obligations that emerge from the architecture:

**G18 (Resolution context selection).** When a user follows a link whose target endset is ghost in one document context but live in another, the front end should attempt resolution in alternative contexts. The back end must provide sufficient primitives:

- `FINDDOCSCONTAINING(iaddrs)` returns all documents whose index entries reference those I-addresses (note: this may include stale entries from documents that no longer actively contain the content — the front end must verify by attempting I→V conversion)
- Version reconstruction retrieves prior states of documents where the content once appeared
- I-address queries (G13) allow direct link discovery when the front end knows the relevant I-addresses

The abstract requirement is that the system must never present a ghost endset as a broken link when alternative resolution contexts exist. This obligation falls primarily on the front end, but the back end must provide the primitives that make it fulfillable. As noted at G9, the current implementation's resolution mechanism does not accept a caller-specified document context — this is a gap between the abstract requirement and the implementation that any correct system must close.

**G19 (Ghost link transparency).** When a user views a document, the system should support (but need not mandate) revealing that links exist to content the document once contained. Nelson frames bidirectional discovery as "the reader should be able to ask... 'What connects here from other documents?'" [LM 2/46]. This is a reader's right, not an automatic notification. But the right extends to ghost content: a reader who asks about links to content that was deleted from the current version must be able to get an answer.

The abstract guarantee is:

  `(A d, A : A ⊆ range(poom_historical(d)) : discover_by_iaddr(A) is well-defined)`

where `poom_historical(d)` includes all content ever arranged in d, across all versions. The system must not prevent the query from being formulated — even if the front end must use historical version data and I-address queries to formulate it.


## The permanence-discoverability theorem

We conclude with the central theorem, which synthesizes the properties above:

**Theorem (Ghost link discoverability).** For any link L with endset e:

  (i) L exists permanently: `L ∈ links ⇒ L ∈ links'` (from P0, since L occupies I-space)

  (ii) L is permanently indexed: `(a, L, e) ∈ lindex ⇒ (a, L, e) ∈ lindex'` (from G0)

  (iii) If ghost, L is unreachable via V-addressed queries: `ghost(L, e) ⇒ (A d, R : L ∉ discover(d, R) via e)` (from G2 and G1)

  (iv) If ghost, L is reachable via I-addressed queries: `(a, L, e) ∈ lindex ⇒ L ∈ discover_by_iaddr(a)` (from G13)

  (v) Ghost state is reversible: `COPY(d, v, a) where a ∈ iaddrs(L.e) ⇒ ¬ghost'(L, e)` (from G10)

  (vi) Re-discovery is automatic: after (v), `L ∈ discover'(d, region covering v)` without modifying L or lindex (from G10)

The proof of each clause is immediate from the referenced properties. The theorem tells us that ghost links occupy a precise intermediate state: they are permanent, indexed, and recoverable, but temporarily unreachable through the standard user-facing query path. The system's obligation is to preserve this intermediate state faithfully — never destroying the link or its index entries — and to provide the primitives that allow the ghost → live transition (COPY) and alternative discovery (I-address queries, historical version access).

Nelson's architecture is designed so that this intermediate state is the *worst case*. No link is ever truly lost. The ghost state is the maximum damage that content deletion can inflict on link discoverability, and it is fully reversible. This is the architectural payoff of separating identity (I-space) from arrangement (V-space): arrangement changes cannot destroy identity-based associations.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| G0 | Link index entries are never removed: `lindex ⊆ lindex'` | introduced |
| G1 | Discovery operates through V→I translation followed by index lookup | introduced |
| G2 | An endset is ghost iff its I-addresses are non-empty and absent from all POOMs | introduced |
| G3 | A link is ghost iff all three endsets are ghost | introduced |
| G4 | A link is partially ghost iff some but not all endsets are ghost | introduced |
| G5 | Discovery via endset e₁ is independent of the liveness of endset e₂ | introduced |
| G6 | I→V conversion silently excludes I-addresses absent from the target document's POOM | introduced |
| G7 | Partial resolution returns only the live portion of an endset | introduced |
| G8 | Resolution is relative to a specific document context | introduced |
| G9 | Resolution is always well-defined; the system should allow choice of document context | introduced |
| G10 | Transclusion automatically restores discoverability without re-indexing | introduced |
| G11 | Ghost state transitions: live → ghost via last-DELETE; ghost → live via COPY | introduced |
| G12 | Transclusion into n documents requires deletion from all n to ghost a link | introduced |
| G13 | I-address queries bypass the V→I bridge and discover ghost links | introduced |
| G14 | Following a ghost-endset link must succeed with empty result, not error | introduced |
| G15 | Ghost state of one endset does not affect other endsets (independence) | introduced |
| G16 | Ghost links must not degrade index performance for non-ghost queries | introduced |
| G17 | Links to ghost elements (no content ever stored) are valid | introduced |
| G18 | Front end should attempt alternative resolution contexts for ghost targets | introduced |
| G19 | The system must support querying links to content a document once contained | introduced |
| Σ.lindex | lindex ⊆ IRange × LinkId × Role — persistent link-to-content-identity index | introduced |


## Open Questions

- Must the system provide a standard protocol operation for I-address-based link discovery, or may it rely entirely on V-addressed queries with front-end workarounds for the ghost case?
- When a ghost endset is partially reconstituted (some but not all I-addresses become live), must the system guarantee that the partial result is contiguous in the new document's V-space?
- Must the system preserve enough historical version information to reconstruct the I-addresses of deleted content, enabling a front end to formulate I-address queries for ghost link discovery?
- What must the system guarantee about the performance of link index queries as the proportion of ghost index entries grows relative to live entries?
- Must the system distinguish between a ghost endset (content exists in I-space, absent from all V-spaces) and a ghost element endset (no content ever stored) in its response to resolution queries?
- When multiple documents transclude the same content and all delete it simultaneously, must the system guarantee that the ghost transition is atomic across documents or may the link flicker between live and ghost?
- What ordering guarantees must hold between a COPY operation that re-introduces ghost content and the subsequent discoverability of links to that content from the copying document?
- Must the front end's resolution context selection (G18) be deterministic, or may different front ends resolve the same ghost endset to different document contexts?
- If a link's type endset is a ghost element (pointing to an address with no content), must the system still return the link when searching by source or target endset alone?
