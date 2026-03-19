# ASN-0004: Content Insertion

*2026-02-23 (revised 2026-03-06)*

We wish to specify INSERT — the operation that introduces new content into a document. INSERT is the primary way the system acquires content: every byte that enters the permanent store does so through some insertion. The word suggests a simple act — place new text at a position — but the consequences are far-reaching. The system must allocate fresh permanent addresses, splice new content into a mutable arrangement, shift existing positions to make room, record the new content in the domain index, and do all this while preserving the identity of every piece of content that existed before. We develop the preconditions, postconditions, and frame conditions that govern this operation, reasoning backward from the guarantees the system must maintain.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store. Once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a partial function from active virtual positions to addresses, `poom(d) : Pos ⇀ Addr`. This is document d's current arrangement — which content appears at which virtual position. The domain of this function is exactly the set of currently occupied positions.
- **spanindex**: a relation recording which documents contain which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only.
- **links**: a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.
- **owner(d)**: a function from documents to users, recording the creator and authority over each document.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, `poom(d).p` for the I-address that document d maps virtual position p to, and `img(poom(d))` for the image of the mapping — the set of I-addresses currently referenced by d. We write `|poom(d)|` for the number of active positions in document d's text subspace, and we write `vextent(d)` for the highest occupied position in d's text subspace (when it is non-empty). We use primed names for the state after an operation.

A document's virtual stream has two subspaces: text (positions whose first component is 1 — that is, addresses of the form 1.x) and links (positions whose first component is 2 — that is, addresses of the form 2.x). We write `sub(p)` for the subspace identifier of position p. Similarly, a document's I-space content occupies separate allocation ranges for text atoms and link atoms, distinguished by a subspace prefix within the document's I-address tree. We write `sub_i(a)` for the I-space subspace classifier of address a. INSERT of text operates in the text subspace of both V-space and I-space.

**S-DISJ (I-space subspace disjointness).** Text I-addresses and link I-addresses are drawn from disjoint ranges within a document's allocation tree:

  `(A d : (A a₁, a₂ : a₁ ∈ img_text(d) ∧ a₂ ∈ img_link(d) : a₁ ≠ a₂))`

where `img_text(d)` is the set of I-addresses allocated in d's text subspace and `img_link(d)` is the set allocated in d's link subspace. Gregory's evidence grounds this: text I-addresses are allocated in the `.0.0.1.x` range under a document's I-address prefix, while link atoms occupy a separate range (`.0.0.2.x`). These ranges are structurally disjoint — no allocation in one range can produce an address in the other. S-DISJ is an axiom of the allocation scheme, not a state invariant requiring per-operation verification: the disjointness is guaranteed by the structure of address assignment itself. Any allocation that produces a text I-address produces one in the text range; any allocation that produces a link I-address produces one in the link range. No sequence of operations can violate S-DISJ because no operation can cause an allocation to land in the wrong range. An alternative implementation may use different ranges, but must preserve the abstract guarantee: text and link I-addresses never collide.


## The permanence context

Before we state what INSERT does, we must establish what it cannot undo. The fundamental invariants S0–S5 govern every operation. We state S2 and S3 formally, then derive three consequences directly relevant to INSERT.

**S0 (V→I Grounding).** `(A d, q : q ∈ dom.poom(d) : poom(d).q ∈ dom.ispace)` — every virtual position maps to an allocated I-address.

**S1 (I-space Immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**S2 (Link Grounding).** `(A L ∈ links, a ∈ addrs(endsets(L)) : a ∈ dom.ispace)` — every address referenced by any link endset is allocated in I-space.

**S3 (Span Index Consistency).** `(A (a, d) ∈ spanindex : a ∈ dom.ispace)` — every entry in the span index references an allocated I-address.

**S4 (Intra-document Injectivity).** `(A d, q₁, q₂ : q₁ ∈ dom.poom(d) ∧ q₂ ∈ dom.poom(d) ∧ q₁ ≠ q₂ : poom(d).q₁ ≠ poom(d).q₂)` — within a single document, no two positions map to the same I-address.

**S5 (Position Density).** For every document d, the occupied text positions form a contiguous range `[1, |poom(d)|]` (or the empty set when `|poom(d)| = 0`).

Three consequences are directly relevant to INSERT:

**P0 (Address irrevocability).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation shrinks the set of allocated addresses.

P0 follows from S1 (I-space immutability) together with the append-only property of I-space: addresses can be added to `dom.ispace` but never removed.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

P1 restates S1 directly. We give it a local label for convenient reference within this ASN.

**P2 (Index monotonicity).** `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')` — the span index never loses an entry.

P2 is a system-level axiom, on the same footing as S0–S5. It cannot be derived from S3. S3 says every span index entry references an allocated address — a grounding invariant on a single state. P2 says entries are never removed between states — a transition invariant across states. No single-state property implies a cross-state monotonicity. We elevate P2 to axiomatic status: the span index is append-only by design, just as I-space is append-only by design (S1). Nelson's append-only storage model ("user makes changes, the changes difflessly into the storage system, filed, as it were, chronologically") applies to the index as well as to content. Once the system records that address a belongs to document d, that fact is permanent.

Any specification of INSERT that violates any of these three is wrong, regardless of what else it achieves. Nelson is explicit: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." I-space only grows; content never changes; the index never forgets.


## Preconditions

We reason backward. INSERT(d, p, c) shall denote the insertion of content c (a non-empty sequence of bytes) at virtual position p in document d. For the postcondition to be achievable, certain conditions must hold before execution begins.

**PRE1 (Document existence).** `d ∈ dom.owner` — document d must already exist. INSERT takes a document identifier as a parameter; Nelson specifies this as `<doc id>` at Literary Machines 4/66. Documents are created by a separate operation (CREATENEWDOCUMENT), which returns the identifier. INSERT cannot conjure a document into being — it operates on one that already has an identity in the system.

**PRE2 (Ownership).** `user = owner(d)` — the requesting user must be the document's owner. Nelson is unambiguous: "Only the owner has a right to withdraw a document or change it." INSERT is a modification. Only the owner may perform it. The corollary is important: a non-owner's recourse is not an error message but a fork — create a new version and insert there. Writing always succeeds; it may simply succeed in a different document.

**PRE3 (Position validity).** `1 ≤ p ≤ |poom(d)| + 1` — the insertion position must lie within the range from the first position through one past the last occupied position (interpreting virtual positions as a 1-based dense sequence within the text subspace).

This range is forced. Consider the lower bound: virtual positions begin at 1. Nelson states that the digit after the document identifier "indicates the byte position in the current ordering of bytes. This is its virtual stream address." Position 0 has no meaning.

The upper bound requires the stronger argument. When d is empty (`|poom(d)| = 0`), the only valid position is 1 (= 0 + 1). If we restricted INSERT to positions within [1, |poom(d)|], the valid range for an empty document would be empty — the first byte could never be inserted. Therefore position |poom(d)| + 1 must be valid for every document, including non-empty ones. There is no principled distinction between "append to an empty document" and "append to a non-empty one." The shift clause in Nelson's specification — "the v-stream addresses of any following characters in the document are increased by the length of the inserted text" — is vacuously satisfied at position |poom(d)| + 1: there are no following characters, so no shift occurs.

Gregory's implementation confirms the bounds from a different angle. For a non-empty document, the insertion mechanism performs an early-exit check: if the insertion position is at or beyond the current extent, the shift phase is skipped entirely and the operation has no effect. For an empty document, a separate code path handles the first insertion at any specified position. The abstract consequence: positions strictly beyond the extent do not silently produce gaps — the system either accepts the position (empty case or within bounds) or produces no arrangement change (non-empty and beyond extent). We therefore state PRE3 as the condition that must hold for the operation to have its intended effect.

**PRE4 (Non-empty content).** `#c > 0` — the content to insert must be non-empty. An insertion of zero bytes is the identity operation on all state components, and we do not consider it separately.


## The effect: what INSERT establishes

With the preconditions satisfied, INSERT(d, p, c) transitions state Σ to Σ'. We develop the postcondition in stages, beginning with what the operation adds and then characterizing how it rearranges.

### Fresh address allocation

**INS1 (Address freshness and contiguity).** INSERT allocates `#c` new addresses, one per byte of content, forming a contiguous range from a fresh starting address a₀:

  `(E a₀ : a₀ ∈ Addr ∧ {a₀, ..., a₀+#c-1} ∩ dom.ispace = ∅ : {a₀, ..., a₀+#c-1} ⊆ dom.ispace')`

The successor operation `a₀ + i` respects the tumbler allocation order within the document's text subspace. The set of allocated addresses is S = {a₀ + i : 0 ≤ i < #c} — contiguous by construction, with a₀ as its minimum. All subsequent properties that reference `a₀ + i` (INS2, INS3, INS1a, INS-F1, INS5, INS-F6, INS-CORR) are well-defined through this binding.

Nelson justifies this from multiple directions. "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." The freshness follows from the append-only storage model: content is "filed, as it were, chronologically" — each new piece receives the next address in sequence. If addresses could be reused, the permanence guarantee ("a permanent tumbler address") would be vacuous: a reference made today might resolve to different content tomorrow. The allocation counter for each document's text subspace advances monotonically and never retreats.

Gregory provides the structural confirmation. Text I-addresses are allocated in a document-specific subspace (the `.0.0.1.x` range under the document's I-address prefix). The allocation function finds the highest existing address within this subspace and returns its successor. Crucially, text and link atoms occupy separate allocation subspaces — a CREATELINK operation that allocated a link atom does not advance the text allocation counter, and a subsequent INSERT of text continues from the previous text high-water mark. The allocation is subspace-local, not global within the document.

This subspace separation matters for the formal model. We can state a sharper property:

**INS1a (Allocation subspace isolation).** The addresses allocated by INSERT of text fall within the document's text allocation subspace and continue from the previous allocation maximum within that subspace, regardless of intervening operations that allocated in other subspaces (such as CREATELINK):

  `(A i : 0 ≤ i < #c : sub_i(a₀ + i) = TEXT)`

An alternative implementation may structure its allocation differently, but must preserve the abstract guarantee: text insertion allocates text-subspace addresses, and the allocation counter within that subspace is independent of allocations in other subspaces.

**INS2 (Content establishment).** The newly allocated addresses receive the inserted content:

  `(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)`

where `c.i` is the i-th byte of the content being inserted. This is the moment content enters the permanent store. Nelson's guarantee is that once this happens, the content is "there" — addressable, retrievable, linkable, transcludable: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." There is no staging area, no pending state. Content that has been inserted IS content in the system.

Combined with P1, INS2 has a permanent corollary: `(A i : 0 ≤ i < #c : (A future Σ'' : ispace''.(a₀ + i) = c.i))`. No future operation can alter what these addresses resolve to. This is the meaning of the append-only model: I-space grows monotonically, and once bytes enter, they never leave and never change.

### V-space arrangement

The new content must appear at the requested position. This requires two coordinated updates to the document's arrangement.

**INS3 (Content placement).** The new content occupies virtual positions [p, p + #c) in document d's V-space:

  `(A i : 0 ≤ i < #c : poom'(d).(p + i) = a₀ + i)`

The mapping from the new virtual positions to the freshly allocated I-addresses preserves order: position p maps to a₀, position p+1 maps to a₀+1, and so on.

**INS4 (Position shift).** Existing content at or beyond the insertion point shifts rightward by the insertion width, within the same subspace. Existing content before the insertion point does not move:

  `(A q : q < p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).q = poom(d).q)`
  `(A q : q ≥ p ∧ q ∈ dom.poom(d) ∧ sub(q) = sub(p) : poom'(d).(q + #c) = poom(d).q)`

Nelson describes this directly: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." The first clause says content before the insertion point is undisturbed. The second says content at or after the insertion point acquires a new virtual position — its old position plus the insertion width — while retaining its I-address mapping. Both clauses are restricted to positions in the same subspace as the insertion point; positions in other subspaces are governed by the independent frame condition INS-F5.

The combination of INS3 and INS4 specifies a complete V-space transition for the text subspace: the new V-stream is the concatenation of the pre-insertion prefix [1, p), the new content [p, p + #c), and the shifted suffix [p + #c, |poom(d)| + #c + 1). Every position in the new stream maps to exactly one I-address, and no I-address is mapped by two positions within the same document.

**INS-D1 (Domain size).** The document's text length increases by exactly #c:

  `|poom'(d)| = |poom(d)| + #c`

This follows from INS3 and INS4 together. INS3 introduces #c new positions [p, p + #c). INS4 preserves all pre-existing positions (shifting those at or beyond p). No position is lost — the first clause of INS4 retains all positions below p, and the second clause retains all positions at or above p by mapping them to new (higher) positions. The domain of `poom'(d)` restricted to the text subspace is therefore `{1, ..., |poom(d)| + #c}`.

### Domain index update

**INS5 (Span index extension).** The newly allocated address range is recorded in the span index under document d:

  `(A i : 0 ≤ i < #c : (a₀ + i, d) ∈ spanindex')`

Gregory's evidence is specific: the INSERT operation writes exactly one domain index entry (DOCISPAN) covering the contiguous I-address range allocated for this insertion. This entry is constructed from the allocation result before any arrangement manipulation occurs, and is passed unchanged to the index-writing function. The domain index entry records precisely the range that was allocated — never a wider or narrower span. Arrangement-level optimizations (such as coalescing adjacent entries into a single tree node) do not affect the domain index, because the index operates on I-addresses directly, independent of V-space structure.

A critical observation follows. INSERT writes exactly one new domain index entry. It does NOT update or duplicate existing entries for content whose V-positions shifted. Since the domain index maps I-addresses to documents (not V-positions to documents), and existing content's I-addresses do not change when V-positions shift, the existing domain index entries remain valid without modification. The index is stable under V-rearrangement because it is anchored to the permanent layer.


## The frame: what INSERT preserves

The postcondition tells us what changes. The frame conditions tell us what does not. For INSERT, the frame is as important as the effect — most of the system state must remain untouched.

### I-space frame

INSERT creates new I-space entries (INS2); it never modifies existing ones. P1 (= S1) guarantees this directly: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. Nelson designs the entire system around this separation: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." Xanadu rejects this. I-space is the immutable substrate.

**INS-F1 (I-space upper bound).** INSERT adds to `dom.ispace` only at the #c allocated addresses — no other addresses are introduced:

  `dom.ispace' ⊆ dom.ispace ∪ {a₀, ..., a₀ + #c - 1}`

This is a frame condition on I-space: INSERT does not silently allocate additional addresses beyond the content being inserted. Combined with P0 (which gives the ⊇ direction: `dom.ispace ⊆ dom.ispace'`) and INS1 (which gives `{a₀, ..., a₀ + #c - 1} ⊆ dom.ispace'`), INS-F1 yields the exact equality `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}`.

Gregory's implementation reveals an interesting nuance at the concrete level. Pre-existing storage entries may be physically modified during INSERT — a text buffer adjacent to the new content may be extended in place to absorb additional bytes, and tree metadata (widths, sibling pointers) may be updated during rebalancing. But these modifications concern the physical representation of the abstract mapping `ispace : Addr ⇀ Content`, not the mapping itself. The abstract guarantee is: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. The content retrievable at any previously allocated address is unchanged. An alternative implementation might use immutable storage blocks and achieve the same guarantee through different means.

### Cross-document isolation

**INS-F2 (Document isolation).** INSERT on document d does not modify any other document's V-space arrangement:

  `(A d' : d' ≠ d : poom'(d') = poom(d'))`

Nelson is explicit about this for the case of transclusion. When Document B transcludes content from Document A (B's V-space maps some positions to I-addresses owned by A), an INSERT into A does not modify B's V-space. B's mapping remains untouched — it still references the same I-addresses as before. The new I-addresses created by A's insertion exist only in A's V-space. "The owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." If even deletion cannot affect other documents' inclusions, insertion certainly cannot.

This extends to versions. Each version is a separate document with its own V→I mapping. "CREATENEWVERSION creates a new document with the contents of document `<doc id>`." From that point forward the two documents are structurally independent. INSERT into version A shifts V-positions in A alone; version B's V-space is unaffected.

### Link survival

**INS-F4 (Link endpoint invariance).** INSERT does not modify any link structure. All link endsets resolve to the same content after the insertion as before:

  `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

**INS-F4a (Link upper bound).** INSERT creates no new links:

  `links' ⊆ links`

Together, INS-F4 and INS-F4a yield `links' = links`: INS-F4 gives `links ⊆ links'` (every old link survives unchanged) and INS-F4a gives `links' ⊆ links` (no new link appears).

Links reference I-space addresses in their endsets, not V-space positions. INSERT creates new I-space entries but does not modify existing ones (P1), and does not modify any link structure. Therefore every endset that referenced content before the insertion still references the same content. Nelson states this as a design property: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." For INSERT specifically, the "if anything is left" condition is trivially satisfied — INSERT adds content but removes nothing. Every link endpoint that resolved before continues to resolve afterward.

The proof is almost too short to write. Let L be any link, and let E be any endset of L. E is a set of I-space address ranges. By P1, no pre-existing I-space content changes. By INS1, the fresh addresses are disjoint from `dom.ispace`. Therefore E references exactly the same addresses, and those addresses contain exactly the same content. Link resolution is invariant under INSERT. ∎

### Subspace confinement

**INS-F5 (Subspace isolation).** INSERT at a position in the text subspace does not modify arrangement entries in the link subspace, and vice versa:

  `(A q : q ∈ dom.poom(d) ∧ sub(q) ≠ sub(p) : poom'(d).q = poom(d).q)`

INS-F5 is an independent frame condition, not a corollary of INS4. INS4 specifies the behavior of positions within the insertion's subspace; it is silent about positions in other subspaces. But silence is not a frame condition — this is the classical frame problem. An operation that says nothing about a state component does not thereby guarantee that component is unchanged. INS-F5 closes the gap: it is the assertion that INSERT's effect on V-space is confined to positions with `sub(q) = sub(p)`. This is a design property of the system — INSERT operates within a single subspace — and must be stated independently.

When INSERT places text at position 1.x, link entries at positions 2.x are completely unaffected — their V-positions do not shift, their I-address mappings do not change. INS4 and INS-F5 together cover all positions in `dom.poom(d)`: INS4 handles the same-subspace positions, INS-F5 handles the rest.

Gregory's evidence reveals the mechanism by which the existing implementation achieves this — a two-boundary construction that limits the shift region to positions between the insertion point and the start of the next subspace. For an insertion at position N.x, the shift region is bounded above by (N+1).1. Entries at or beyond this boundary are classified into a "no shift" category and left untouched. A concrete example: with text at V:1.1-1.5 and a link at V:2.1, an insertion at V:1.3 shifts text entries in [1.3, 2.1) rightward by the insertion width, while the link entry at V:2.1 remains at V:2.1 with every field — V-displacement, I-displacement, V-width, I-width — byte-identical to its pre-insertion state.

The abstract property is that the two subspaces of a document (text and links) are independently arranged. No operation on one subspace can disturb the other. The bounded-shift mechanism is one way to achieve this; the guarantee itself is what any implementation must provide.

### Span index stability

**INS-F6 (Span index upper bound).** INSERT adds to the span index only the #c entries for the newly allocated addresses — no other entries are introduced:

  `spanindex' ⊆ spanindex ∪ {(a₀ + i, d) : 0 ≤ i < #c}`

This is the upper-bound companion to INS5 (which gives the ⊇ direction for the new entries) and P2 (which gives the ⊇ direction for pre-existing entries). Together, INS5, P2, and INS-F6 yield the exact equality `spanindex' = spanindex ∪ {(a₀ + i, d) : 0 ≤ i < #c}`. INSERT does not modify or remove any pre-existing span index entry (P2), and does not introduce entries beyond those specified by INS5. The index grows by exactly the entries for the newly allocated addresses, and all previous entries are preserved.

### Ownership stability

**INS-F7 (Owner preservation).** INSERT does not modify document ownership:

  `(A d' : owner'(d') = owner(d'))`

PRE2 requires that the requesting user be the document's owner, but INSERT does not alter the ownership relation — neither for the target document d nor for any other document. Ownership is a metadata property established at document creation and modified only by an explicit ownership-transfer operation (if one exists). INSERT's effect is confined to content and arrangement.


## Derived consequences

Two important properties follow from the postconditions and frame conditions above. They are not frame conditions (they do not state what is unchanged) but rather consequences of how the change and the preserved state interact.

### V→I correspondence

**INS-D2 (V→I correspondence preservation).** For every position that existed before the insertion, the content at the (possibly shifted) position is the same byte that was at the original position:

  `(A q : q ∈ dom.poom(d) ∧ sub(q) = sub(p) ∧ q < p : ispace'.(poom'(d).q) = ispace.(poom(d).q))`
  `(A q : q ∈ dom.poom(d) ∧ sub(q) = sub(p) ∧ q ≥ p : ispace'.(poom'(d).(q + #c)) = ispace.(poom(d).q))`

This is the central architectural consequence. V-addresses shift; I-addresses do not. The bijection between content identity and content value is preserved through the shift. Nelson designed the two-space architecture precisely for this: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Proof. For content before the insertion point: `poom'(d).q = poom(d).q` (by INS4, first clause), so the I-address is unchanged. By P1, the content at that I-address is unchanged. For content at or after the insertion point: `poom'(d).(q + #c) = poom(d).q` (by INS4, second clause), so the I-address is again unchanged. By P1, the content at that I-address is unchanged. In both cases, the content retrievable through the V-space mapping after INSERT is identical to the content retrievable before INSERT, for every pre-existing position. ∎

This is not a derived convenience. It is the property on which link survivability, attribution, version comparison, transclusion integrity, and royalty accounting all depend. If INSERT corrupted the V→I mapping — swapping which I-address a V-position refers to — links would silently attach to wrong content, attribution would identify wrong authors, version comparison would report false correspondences, and royalty payments would go to wrong parties.


## Invariant preservation

INSERT must preserve the fundamental invariants S0–S5. We verify each.

**S0 (V→I Grounding).** We must show `(A d', q : q ∈ dom.poom'(d') : poom'(d').q ∈ dom.ispace')`.

For documents d' ≠ d: `poom'(d') = poom(d')` by INS-F2, and `dom.ispace ⊆ dom.ispace'` by P0, so S0 for d' follows from S0 pre-INSERT.

For document d, we consider four kinds of positions in `dom.poom'(d)`:
- Positions q with `sub(q) = sub(p)` and `q < p`: `poom'(d).q = poom(d).q` by INS4 (first clause). This address is in `dom.ispace` by S0 pre-INSERT, hence in `dom.ispace'` by P0. ✓
- New positions q with `p ≤ q < p + #c`: `poom'(d).q = a₀ + (q - p)` by INS3. This address is in `dom.ispace'` by INS1. ✓
- Shifted positions q with `q ≥ p + #c` (originally at `q - #c`): `poom'(d).q = poom(d).(q - #c)` by INS4 (second clause). This address is in `dom.ispace` by S0 pre-INSERT, hence in `dom.ispace'` by P0. ✓
- Positions q with `sub(q) ≠ sub(p)`: `poom'(d).q = poom(d).q` by INS-F5. In `dom.ispace` by S0 pre-INSERT, hence in `dom.ispace'` by P0. ✓

**S1 (I-space Immutability).** P1 guarantees `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. INSERT writes only to fresh addresses (INS1: `{a₀, ..., a₀+#c-1} ∩ dom.ispace = ∅`). No pre-existing content is modified. ✓

**S2 (Link Grounding).** We must show `(A L ∈ links', a ∈ addrs(endsets'(L)) : a ∈ dom.ispace')`. By INS-F4a, `links' ⊆ links`, and by INS-F4, `endsets'(L) = endsets(L)` for all L ∈ links. So every address in every endset of links' was in `addrs(endsets(L))` for some L ∈ links. By S2 pre-INSERT, `a ∈ dom.ispace`. By P0, `a ∈ dom.ispace'`. ✓

**S3 (Span Index Consistency).** We must show `(A (a, d') ∈ spanindex' : a ∈ dom.ispace')`. By INS-F6, `spanindex' ⊆ spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}`. For pre-existing entries: `(a, d') ∈ spanindex` implies `a ∈ dom.ispace` by S3 pre-INSERT, hence `a ∈ dom.ispace'` by P0. For new entries: `a₀+i ∈ dom.ispace'` by INS1. ✓

**S4 (Intra-document Injectivity).** We must show `poom'(d)` is injective. Consider two distinct positions q₁, q₂ ∈ dom.poom'(d) with q₁ ≠ q₂. We need `poom'(d).q₁ ≠ poom'(d).q₂`. Four cases arise:

- *Both same-subspace pre-existing (before or shifted)*: their I-addresses are the same as their original I-addresses under `poom(d)`, which were distinct by S4 pre-INSERT. ✓
- *Both new (in [p, p + #c))*: `poom'(d).q₁ = a₀ + (q₁ - p) ≠ a₀ + (q₂ - p) = poom'(d).q₂` since q₁ ≠ q₂. ✓
- *One pre-existing same-subspace, one new*: the pre-existing position maps to some address in `dom.ispace`; the new position maps to some address in `{a₀, ..., a₀+#c-1}`. By INS1, the fresh addresses are disjoint from `dom.ispace`, so the two I-addresses are necessarily distinct. ✓
- *Cross-subspace (one text, one link)*: one position has `sub(q₁) = sub(p)` (text), the other has `sub(q₂) ≠ sub(p)` (link). The text position's I-address is either a pre-existing text I-address or a freshly allocated text I-address (INS1a: `sub_i(a₀ + i) = TEXT`). The link position's I-address is unchanged by INS-F5 and was a link I-address before INSERT. By S-DISJ — which holds as an axiom of the allocation scheme, not as an invariant requiring per-operation verification — text and link I-addresses are drawn from disjoint ranges, so the two I-addresses are necessarily distinct. ✓

In all cases, `poom'(d).q₁ ≠ poom'(d).q₂`. For d' ≠ d, poom'(d') = poom(d') which was injective by S4 pre-INSERT. ✓

**S5 (Position Density).** We must show that the occupied text positions of d after INSERT form the contiguous range `[1, |poom(d)| + #c]`. Before INSERT, the occupied range is `[1, |poom(d)|]` by S5 pre-INSERT. After INSERT:
- Positions [1, p) are unchanged (INS4, first clause) — contiguous. ✓
- Positions [p, p + #c) are newly created (INS3) — contiguous. ✓
- Positions [p + #c, |poom(d)| + #c] are the shifted versions of [p, |poom(d)|] (INS4, second clause). Shifting by the constant #c preserves contiguity. ✓
- The three ranges are adjacent: [1, p) ends where [p, p + #c) begins; [p, p + #c) ends where [p + #c, |poom(d)| + #c] begins.

The union is `[1, |poom(d)| + #c]` — contiguous. ✓


## The correspondence theorem

The individual properties above can be assembled into a single characterization of what INSERT means. We first define the shift function used in clause (iv), then state the theorem.

**Definition.** Let `m : Pos ⇀ Addr` be a partial mapping, `p` a position, and `w > 0` a width. The shift of m at p by w is:

  `shift(m, p, w) = {(q, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q < p}`
  `              ∪ {(q + w, m.q) : q ∈ dom.m ∧ sub(q) = sub(p) ∧ q ≥ p}`
  `              ∪ {(q, m.q) : q ∈ dom.m ∧ sub(q) ≠ sub(p)}`

The first component preserves same-subspace positions below p. The second displaces same-subspace positions at or above p rightward by w. The third passes all other-subspace positions through unchanged.

**INS-CORR (INSERT Correctness).** Let Σ' = INSERT(d, p, c) applied to state Σ satisfying PRE1–PRE4. Then:

(i) `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}` where `{a₀, ..., a₀ + #c - 1} ∩ dom.ispace = ∅` — exactly #c fresh addresses are added.

(ii) `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — all pre-existing content is preserved.

(iii) `(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)` — new addresses receive the inserted content.

(iv) `poom'(d) = shift(poom(d), p, #c) ∪ {(p+i, a₀+i) : 0 ≤ i < #c}` — the V-space mapping is the shifted original plus the new content.

(v) `(A d' : d' ≠ d : poom'(d') = poom(d'))` — all other documents are untouched.

(vi) `spanindex' = spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}` — exactly the new addresses are indexed.

(vii) `links' = links` — no link is created, modified, or destroyed.

(viii) `(A d' : owner'(d') = owner(d'))` — document ownership is unchanged.

Clause (i) follows from P0, INS1, and INS-F1 — P0 gives `dom.ispace ⊆ dom.ispace'`, INS1 gives `{a₀, ..., a₀+#c-1} ⊆ dom.ispace'`, and INS-F1 gives `dom.ispace' ⊆ dom.ispace ∪ {a₀, ..., a₀+#c-1}`. The three together yield the exact equality. Clause (ii) from P1. Clause (iii) from INS2. Clause (iv) from INS3, INS4, and INS-F5 — the shift definition encodes all three. Clause (v) from INS-F2. Clause (vi) from P2, INS5, and INS-F6 — P2 gives `spanindex ⊆ spanindex'`, INS5 gives `{(a₀+i, d)} ⊆ spanindex'`, and INS-F6 gives `spanindex' ⊆ spanindex ∪ {(a₀+i, d)}`. Clause (vii) from INS-F4 and INS-F4a — INS-F4 gives `links ⊆ links'`, INS-F4a gives `links' ⊆ links`. Clause (viii) from INS-F7.


## Concrete examples

### Interior insertion

Let document d have three bytes of content, with `poom(d) = {(1, a), (2, b), (3, c)}` where `ispace.a = 'H'`, `ispace.b = 'i'`, `ispace.c = '!'`. The document reads "Hi!" and `|poom(d)| = 3`.

We apply INSERT(d, 2, "EY"), inserting two bytes at position 2. The preconditions hold: PRE1 (d exists), PRE2 (user owns d), PRE3 (1 ≤ 2 ≤ 4), PRE4 (#"EY" = 2 > 0).

The allocation produces fresh addresses x, y with `{x, y} ∩ dom.ispace = ∅`. After INSERT:

- INS1: `{x, y} ⊆ dom.ispace'` and `{x, y} ∩ dom.ispace = ∅`. ✓
- INS2: `ispace'.x = 'E'`, `ispace'.y = 'Y'`. ✓
- INS3: `poom'(d).2 = x`, `poom'(d).3 = y`. The new content occupies positions [2, 4). ✓
- INS4 (first clause, q < 2): `poom'(d).1 = poom(d).1 = a`. Position 1 unchanged. ✓
- INS4 (second clause, q ≥ 2): `poom'(d).(2 + 2) = poom(d).2 = b`, so `poom'(d).4 = b`. And `poom'(d).(3 + 2) = poom(d).3 = c`, so `poom'(d).5 = c`. ✓
- INS5: `(x, d) ∈ spanindex'` and `(y, d) ∈ spanindex'`. ✓
- INS-D1: `|poom'(d)| = 3 + 2 = 5`. ✓

The resulting mapping is `poom'(d) = {(1, a), (2, x), (3, y), (4, b), (5, c)}`. The document reads "HEYY!" — wait. Let us check: position 1 → a → 'H', position 2 → x → 'E', position 3 → y → 'Y', position 4 → b → 'i', position 5 → c → '!'. The document reads "HEYi!" — the original "Hi!" with "EY" spliced in at position 2.

Invariant verification against this example:
- S0: every position maps to an address in `dom.ispace'`. Addresses a, b, c were in `dom.ispace` (hence in `dom.ispace'` by P0). Addresses x, y are in `dom.ispace'` by INS1. ✓
- S4: all five I-addresses (a, x, y, b, c) are distinct — a, b, c were distinct by S4 pre-INSERT; x, y are fresh and mutually distinct. ✓
- S5: occupied positions are {1, 2, 3, 4, 5} = [1, 5]. ✓
- INS-D2: content at shifted positions — `ispace'.(poom'(d).4) = ispace'.b = ispace.b = 'i'` = `ispace.(poom(d).2)`. ✓

### Insertion into an empty document

Let document e be empty: `poom(e) = ∅` and `|poom(e)| = 0`. We apply INSERT(e, 1, "OK"), inserting two bytes.

Preconditions: PRE1 (e exists), PRE2 (user owns e), PRE3 (`1 ≤ 1 ≤ 0 + 1 = 1` ✓), PRE4 (#"OK" = 2 > 0). The precondition PRE3 holds with equality at both bounds — position 1 is the only valid insertion position for an empty document.

The allocation produces fresh addresses r, s. After INSERT:

- INS1: `{r, s} ⊆ dom.ispace'` and `{r, s} ∩ dom.ispace = ∅`. ✓
- INS2: `ispace'.r = 'O'`, `ispace'.s = 'K'`. ✓
- INS3: `poom'(e).1 = r`, `poom'(e).2 = s`. ✓
- INS4 (first clause, q < 1): no positions satisfy this — the pre-insertion domain is empty. Vacuously satisfied. ✓
- INS4 (second clause, q ≥ 1): no positions satisfy this either — `dom.poom(e) = ∅`. The shift clause is vacuously satisfied. This is the critical boundary case: INS3 alone determines the entire V-space of the new state. ✓
- INS5: `(r, e) ∈ spanindex'` and `(s, e) ∈ spanindex'`. ✓
- INS-D1: `|poom'(e)| = 0 + 2 = 2`. ✓

The resulting mapping is `poom'(e) = {(1, r), (2, s)}`. The document reads "OK".

Invariant verification:
- S0: positions 1 and 2 map to r and s, both in `dom.ispace'` by INS1. ✓
- S4: r ≠ s since both are freshly allocated contiguous addresses (and #c = 2 > 1, so a₀ ≠ a₀ + 1). ✓
- S5: occupied positions are {1, 2} = [1, 2], and `|poom'(e)| = 2`. Contiguous. ✓

This is the case that motivates the upper bound in PRE3. Without allowing position `|poom(d)| + 1`, the first byte could never enter an empty document. The shift clause contributes nothing here; the entire post-state V-space is determined by INS3.

### Append (insertion at the end)

Using the document from the interior example after INSERT: `poom'(d) = {(1, a), (2, x), (3, y), (4, b), (5, c)}` reading "HEYi!", with `|poom'(d)| = 5`. We now apply INSERT(d, 6, "?"), inserting one byte at the append position.

Preconditions: PRE1 (d exists), PRE2 (user owns d), PRE3 (`1 ≤ 6 ≤ 5 + 1 = 6` ✓), PRE4 (#"?" = 1 > 0).

The allocation produces fresh address z. After INSERT:

- INS1: `{z} ⊆ dom.ispace''` and `{z} ∩ dom.ispace' = ∅`. ✓
- INS2: `ispace''.z = '?'`. ✓
- INS3: `poom''(d).6 = z`. The new content occupies position [6, 7). ✓
- INS4 (first clause, q < 6): `poom''(d).q = poom'(d).q` for q ∈ {1, 2, 3, 4, 5}. All five pre-existing positions unchanged. ✓
- INS4 (second clause, q ≥ 6): no positions satisfy this — `dom.poom'(d)` has no position ≥ 6. The shift clause is vacuously satisfied. This is the boundary case Nelson describes: "the v-stream addresses of any following characters in the document are increased" — but there are no following characters, so no shift occurs. ✓
- INS5: `(z, d) ∈ spanindex''`. ✓
- INS-D1: `|poom''(d)| = 5 + 1 = 6`. ✓

The resulting mapping is `poom''(d) = {(1, a), (2, x), (3, y), (4, b), (5, c), (6, z)}`. The document reads "HEYi!?".

Invariant verification:
- S0: all six positions map to addresses in `dom.ispace''`. ✓
- S4: z is fresh, hence distinct from a, x, y, b, c. ✓
- S5: occupied positions are {1, 2, 3, 4, 5, 6} = [1, 6]. ✓

The append case confirms that APPEND(d, c) = INSERT(d, |poom(d)| + 1, c) satisfies all postconditions. The shift clause is vacuous, and INS3 alone places the content.


## Atomicity

Nelson does not use the word "atomic." Literary Machines is silent on whether INSERT must be all-or-nothing. But his specification is only consistent with all-or-nothing semantics, and we state this as a derived requirement.

**INS-ATOM (All-or-nothing execution).** Either INSERT(d, p, c) transitions Σ to a state Σ' satisfying all of INS-CORR(i)–(viii), or the state is unchanged: Σ' = Σ.

Three converging requirements force this conclusion.

First, Nelson's operational descriptions are state-to-state. INSERT is specified as a single coherent outcome — content appears at a position and subsequent addresses shift by the full width. No intermediate state is described or acknowledged.

Second, the "canonical order mandate." Nelson records that "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." A partially applied INSERT — one that allocated I-space but did not update V-space, or that shifted some positions but not all — would leave the structure in a non-canonical state. The mandate requires that every change leave the structure valid, which for INSERT means either fully applied or not applied at all.

Third, the coherent version model. If every historical state is reconstructible and comparable, then every state must be a complete, consistent snapshot. A half-applied insertion is neither the pre-insertion state nor the post-insertion state — it is an incoherent intermediate with no place in the version history.

Gregory reveals that the existing implementation does not enforce atomicity through any transactional mechanism — there is no write-ahead log, no undo log, no two-phase commit. Operations proceed through their phases sequentially, and a crash partway through would leave the state partially modified. Furthermore, the implementation dispatches the success response to the client before executing the mutation; if the mutation fails (for instance, due to a permission check), the client receives a success response for an operation that never occurred. Both are implementation deficiencies, not design intent. The abstract specification requires atomicity; any correct implementation must provide it.

The gap between the abstract requirement and the implementation's behavior is a refinement obligation. The implementation must ensure, through whatever mechanism (logging, write-ahead, undo, or otherwise), that no observable state violates INS-ATOM.


## Same-position insertion

A special case merits attention. What happens when two successive INSERTs target the same virtual position? Let INSERT(d, p, "A") produce state Σ₁, then INSERT(d, p, "B") be applied to Σ₁. We ask: where does "B" appear relative to "A"?

By INS3, the first insertion places "A" at position p. By INS4, everything at or beyond p in the original state has shifted right by 1. In state Σ₁, "A" occupies position p. The second insertion, INSERT(d, p, "B"), places "B" at position p in Σ₁. By INS4, "A" (which is now at position p in Σ₁) shifts to position p+1. The result: "B" is at position p, "A" is at position p+1.

This is LIFO ordering: the last-inserted content occupies the specified position, and previously inserted content shifts rightward. The pattern generalizes: n successive insertions at the same position produce the content in reverse order at that position. The specification does not require any special treatment — it falls out naturally from INS3 and INS4 applied in sequence.

Gregory confirms that the implementation produces separate internal entries for each such insertion — it does not coalesce them, even though their permanent addresses may be contiguous. Coalescing is an optimization available only when a new insertion extends the right boundary of an existing entry (advancing cursor typing). When the insertion point is at or before the left boundary, the shift phase moves the existing entry out of the way before the new entry is placed, and the internal merge criterion (which checks adjacency in both the virtual and permanent dimensions) cannot be satisfied because the virtual dimension has become non-adjacent.

The abstract implication is that LIFO ordering is a theorem of the specification (INS3 + INS4), not a design choice or implementation artifact.


## Append as special case

Nelson specifies APPEND as a separate operation: "This appends `<text set>` onto the end of the text space of the document `<doc id>`." We observe that APPEND(d, c) is semantically equivalent to INSERT(d, |poom(d)| + 1, c). The position is one past the last occupied position; by INS4, the shift clause is vacuously satisfied (no following characters exist); by INS3, the content is placed at the end. APPEND is a convenience name for a common case of INSERT, not a distinct operation with separate semantics.

The equivalence means every property we have established for INSERT applies to APPEND without modification. In particular, APPEND satisfies INS-CORR(i)–(viii) with `p = |poom(d)| + 1`.


## What INSERT does not do

Several things that might seem plausible are expressly excluded by the specification.

**INSERT does not propagate through transclusion.** If Document B transcludes a passage from Document A, and we INSERT into A at a position within that passage, B is unaffected (INS-F2). B's V-space still maps to the same I-addresses as before. The new bytes created by the insertion exist only in A's V-space arrangement. Nelson is direct: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." The converse is also true — content added to one document is not automatically added to others that transclude from it. Each document's arrangement is sovereign.

A front-end may provide a "location-fixed window" that re-resolves the source document's current arrangement and displays updates. Nelson describes this: "a quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time... Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." But this is a display behavior, not a state modification. The including document's V-space mapping is unchanged. The reader sees the update through a live view; the document structure is not altered.

**INSERT does not create links.** INSERT creates content in I-space and arranges it in V-space. It does not create, modify, or destroy any link structure (INS-F4, INS-F4a). Link creation is a separate operation (CREATELINK) with its own preconditions and effects.

**INSERT does not modify the allocation state of other subspaces.** If the document previously had link atoms allocated in the link I-subspace (via CREATELINK), those allocations are invisible to INSERT's text allocation. The text allocation counter operates within its own subspace and continues from the previous text high-water mark, regardless of intervening link allocations (INS1a). An implementation that used a single global allocation counter per document — causing link creation to advance the text counter — would violate INS1a. The specification mandates that each atom type's allocation is subspace-local.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| S-DISJ | `(A d, a₁ ∈ img_text(d), a₂ ∈ img_link(d) : a₁ ≠ a₂)` — text and link I-addresses disjoint | axiom |
| P0 | `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — address irrevocability (derived from S1) | derived |
| P1 | `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content immutability (restates S1) | derived |
| P2 | `(A (a,d) : (a,d) ∈ spanindex : (a,d) ∈ spanindex')` — index monotonicity (axiom) | axiom |
| PRE1 | `d ∈ dom.owner` — target document must exist | introduced |
| PRE2 | `user = owner(d)` — requesting user must be document owner | introduced |
| PRE3 | `1 ≤ p ≤ \|poom(d)\| + 1` — position within [1, m+1] | introduced |
| PRE4 | `#c > 0` — content to insert is non-empty | introduced |
| INS1 | `(E a₀ : {a₀,...,a₀+#c-1} ∩ dom.ispace = ∅ : {a₀,...,a₀+#c-1} ⊆ dom.ispace')` — #c fresh contiguous addresses | introduced |
| INS1a | `(A i : 0 ≤ i < #c : sub_i(a₀+i) = TEXT)` — text allocation is subspace-local | introduced |
| INS2 | `(A i : 0 ≤ i < #c : ispace'.(a₀+i) = c.i)` — new addresses receive inserted content | introduced |
| INS3 | `(A i : 0 ≤ i < #c : poom'(d).(p+i) = a₀+i)` — content placed at insertion position | introduced |
| INS4 | Positions < p unchanged, positions ≥ p shift by #c (same subspace only) | introduced |
| INS-D1 | `\|poom'(d)\| = \|poom(d)\| + #c` — text length increases by insertion width | introduced |
| INS5 | `(A i : 0 ≤ i < #c : (a₀+i, d) ∈ spanindex')` — new range indexed under d | introduced |
| INS-F1 | `dom.ispace' ⊆ dom.ispace ∪ {a₀, ..., a₀+#c-1}` — I-space upper bound | introduced |
| INS-F2 | `(A d' : d' ≠ d : poom'(d') = poom(d'))` — other documents' V-space unchanged | introduced |
| INS-D2 | V→I correspondence preserved: same content at shifted positions | introduced |
| INS-F4 | `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))` — all pre-existing links unchanged | introduced |
| INS-F4a | `links' ⊆ links` — INSERT creates no new links | introduced |
| INS-F5 | `(A q : q ∈ dom.poom(d) ∧ sub(q) ≠ sub(p) : poom'(d).q = poom(d).q)` — subspace isolation | introduced |
| INS-F6 | `spanindex' ⊆ spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}` — span index upper bound | introduced |
| INS-F7 | `(A d' : owner'(d') = owner(d'))` — document ownership unchanged | introduced |
| INS-CORR | Complete correctness: clauses (i)–(viii) characterize the full state transition | introduced |
| INS-ATOM | All-or-nothing: either INS-CORR holds or Σ' = Σ | introduced |


## Open Questions

Must INSERT at a position between two entries that are contiguous in both V-space and I-space preserve any observable property about the resulting fragmentation of the arrangement?

When the owner of a document performs INSERT, does the system record the insertion event in a way that permits replay — and if so, what journal entry must the insertion produce?

What must an implementation guarantee about crash recovery to satisfy INS-ATOM, given that the operation modifies both the permanent store and the document arrangement?

If two front-ends hold the same document open and one performs INSERT, must the other observe the insertion before performing its own operation — or may concurrent insertions produce a merge?

Does the span index entry written by INSERT carry sufficient information to reconstruct which document version the allocation was part of, or does it record only the document-level association?

Must INS-F5 (subspace isolation) hold by construction in any correct implementation, or is it permissible for an implementation to enforce it via a runtime check that rejects cross-subspace shifts?

What must the system guarantee about the relationship between INSERT's allocation order and the observable order of content in the V-stream — must content allocated later always appear after content allocated earlier within the same document?

When INSERT is dispatched through a request-response protocol, must the success response be contingent on the mutation having completed — and what must the system do if the mutation fails after the response is sent?
