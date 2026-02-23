# ASN-0004: Content Insertion

*2026-02-23*

We wish to specify INSERT — the operation that introduces new content into a document. INSERT is the primary way the system acquires content: every byte that enters the permanent store does so through some insertion. The word suggests a simple act — place new text at a position — but the consequences are far-reaching. The system must allocate fresh permanent addresses, splice new content into a mutable arrangement, shift existing positions to make room, record the new content in the domain index, and do all this while preserving the identity of every piece of content that existed before. We develop the preconditions, postconditions, and frame conditions that govern this operation, reasoning backward from the guarantees the system must maintain.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store. Once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a partial function from active virtual positions to addresses, `poom(d) : Pos ⇀ Addr`. This is document d's current arrangement — which content appears at which virtual position. The domain of this function is exactly the set of currently occupied positions.
- **spanindex**: a relation recording which documents contain which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only.
- **links**: a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.
- **owner(d)**: a function from documents to users, recording the creator and authority over each document.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, `poom(d).p` for the I-address that document d maps virtual position p to, and `img(poom(d))` for the image of the mapping — the set of I-addresses currently referenced by d. We write `|poom(d)|` for the number of active positions in document d's text subspace, and we write `vextent(d)` for the highest occupied position in d's text subspace (when it is non-empty). We use primed names for the state after an operation.

A document's virtual stream has two subspaces: text (positions whose first component is 1 — that is, addresses of the form 1.x) and links (positions whose first component is 2 — that is, addresses of the form 2.x). We write `sub(p)` for the subspace identifier of position p. Similarly, a document's I-space content occupies separate allocation ranges for text atoms and link atoms, distinguished by a subspace prefix within the document's I-address tree. INSERT of text operates in the text subspace of both V-space and I-space.


## The permanence context

Before we state what INSERT does, we must establish what it cannot undo. The system makes three commitments that hold across every operation:

**P0 (Address irrevocability).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation shrinks the set of allocated addresses.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (Index monotonicity).** `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')` — the span index never loses an entry.

These are not properties we prove here; they are the context within which INSERT must operate. Any specification of INSERT that violates any of these three is wrong, regardless of what else it achieves. Nelson is explicit: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." I-space only grows; content never changes; the index never forgets.


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

**INS1 (Address freshness).** INSERT allocates `#c` new addresses, one per byte of content, from a range never previously used:

  `(E S : S ⊆ Addr ∧ #S = #c ∧ S ∩ dom.ispace = ∅ : S ⊆ dom.ispace')`

The freshly allocated addresses form a contiguous range in I-space: if a₀ is the starting address, the allocation produces `{a₀, a₀+1, ..., a₀+#c-1}`, where the successor operation respects the tumbler allocation order within the document's text subspace.

Nelson justifies this from multiple directions. "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." The freshness follows from the append-only storage model: content is "filed, as it were, chronologically" — each new piece receives the next address in sequence. If addresses could be reused, the permanence guarantee ("a permanent tumbler address") would be vacuous: a reference made today might resolve to different content tomorrow. The allocation counter for each document's text subspace advances monotonically and never retreats.

Gregory provides the structural confirmation. Text I-addresses are allocated in a document-specific subspace (the `.0.0.1.x` range under the document's I-address prefix). The allocation function finds the highest existing address within this subspace and returns its successor. Crucially, text and link atoms occupy separate allocation subspaces — a CREATELINK operation that allocated a link atom does not advance the text allocation counter, and a subsequent INSERT of text continues from the previous text high-water mark. The allocation is subspace-local, not global within the document.

This subspace separation matters for the formal model. We can state a sharper property:

**INS1a (Allocation subspace isolation).** The addresses allocated by INSERT of text fall within the document's text allocation subspace and continue from the previous allocation maximum within that subspace, regardless of intervening operations that allocated in other subspaces (such as CREATELINK):

  `(A i : 0 ≤ i < #c : sub_i(allocated.i) = TEXT)`

where `sub_i` is the I-space subspace classifier. An alternative implementation may structure its allocation differently, but must preserve the abstract guarantee: text insertion allocates text-subspace addresses, and the allocation counter within that subspace is independent of allocations in other subspaces.

**INS2 (Content establishment).** The newly allocated addresses receive the inserted content:

  `(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)`

where `c.i` is the i-th byte of the content being inserted. This is the moment content enters the permanent store. Nelson's guarantee is that once this happens, the content is "there" — addressable, retrievable, linkable, transcludable: "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." There is no staging area, no pending state. Content that has been inserted IS content in the system.

Combined with P1, INS2 has a permanent corollary: `(A i : 0 ≤ i < #c : (A future Σ'' : ispace''.(a₀ + i) = c.i))`. No future operation can alter what these addresses resolve to. This is the meaning of the append-only model: I-space grows monotonically, and once bytes enter, they never leave and never change.

### V-space arrangement

The new content must appear at the requested position. This requires two coordinated updates to the document's arrangement.

**INS3 (Content placement).** The new content occupies virtual positions [p, p + #c) in document d's V-space:

  `(A i : 0 ≤ i < #c : poom'(d).(p + i) = a₀ + i)`

The mapping from the new virtual positions to the freshly allocated I-addresses preserves order: position p maps to a₀, position p+1 maps to a₀+1, and so on.

**INS4 (Position shift).** Existing content at or beyond the insertion point shifts rightward by the insertion width. Existing content before the insertion point does not move:

  `(A q : q < p ∧ q ∈ dom.poom(d) : poom'(d).q = poom(d).q)`
  `(A q : q ≥ p ∧ q ∈ dom.poom(d) : poom'(d).(q + #c) = poom(d).q)`

Nelson describes this directly: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." The first clause says content before the insertion point is undisturbed. The second says content at or after the insertion point acquires a new virtual position — its old position plus the insertion width — while retaining its I-address mapping.

We must be precise about the scope of INS4. The shift applies only within the subspace of the insertion point. When INSERT targets the text subspace (positions 1.x), only text entries shift; link entries (positions 2.x) are unaffected. We formalize this confinement below as INS-F5.

The combination of INS3 and INS4 specifies a complete V-space transition for the text subspace: the new V-stream is the concatenation of the pre-insertion prefix [1, p), the new content [p, p + #c), and the shifted suffix [p + #c, |poom(d)| + #c + 1). Every position in the new stream maps to exactly one I-address, and no I-address is mapped by two positions within the same document. The document's text length increases by exactly #c.

### Domain index update

**INS5 (Span index extension).** The newly allocated address range is recorded in the span index under document d:

  `(A i : 0 ≤ i < #c : (a₀ + i, d) ∈ spanindex')`

Gregory's evidence is specific: the INSERT operation writes exactly one domain index entry (DOCISPAN) covering the contiguous I-address range allocated for this insertion. This entry is constructed from the allocation result before any arrangement manipulation occurs, and is passed unchanged to the index-writing function. The domain index entry records precisely the range that was allocated — never a wider or narrower span. Arrangement-level optimizations (such as coalescing adjacent entries into a single tree node) do not affect the domain index, because the index operates on I-addresses directly, independent of V-space structure.

A critical observation follows. INSERT writes exactly one new domain index entry. It does NOT update or duplicate existing entries for content whose V-positions shifted. Since the domain index maps I-addresses to documents (not V-positions to documents), and existing content's I-addresses do not change when V-positions shift, the existing domain index entries remain valid without modification. The index is stable under V-rearrangement because it is anchored to the permanent layer.


## The frame: what INSERT preserves

The postcondition tells us what changes. The frame conditions tell us what does not. For INSERT, the frame is as important as the effect — most of the system state must remain untouched.

### I-space preservation

**INS-F1 (Existing content frame).** All content that existed in I-space before the insertion is unchanged:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

This is P1 restated for INSERT specifically, but it deserves emphasis. INSERT creates new I-space entries (INS2); it never modifies existing ones. Nelson designs the entire system around this separation: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." Xanadu rejects this. I-space is the immutable substrate.

Gregory's implementation reveals an interesting nuance at the concrete level. Pre-existing storage entries may be physically modified during INSERT — a text buffer adjacent to the new content may be extended in place to absorb additional bytes, and tree metadata (widths, sibling pointers) may be updated during rebalancing. But these modifications concern the physical representation of the abstract mapping `ispace : Addr ⇀ Content`, not the mapping itself. The abstract guarantee is: `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. The content retrievable at any previously allocated address is unchanged. An alternative implementation might use immutable storage blocks and achieve the same guarantee through different means.

### Cross-document isolation

**INS-F2 (Document isolation).** INSERT on document d does not modify any other document's V-space arrangement:

  `(A d' : d' ≠ d : poom'(d') = poom(d'))`

Nelson is explicit about this for the case of transclusion. When Document B transcludes content from Document A (B's V-space maps some positions to I-addresses owned by A), an INSERT into A does not modify B's V-space. B's mapping remains untouched — it still references the same I-addresses as before. The new I-addresses created by A's insertion exist only in A's V-space. "The owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." If even deletion cannot affect other documents' inclusions, insertion certainly cannot.

This extends to versions. Each version is a separate document with its own V→I mapping. "CREATENEWVERSION creates a new document with the contents of document `<doc id>`." From that point forward the two documents are structurally independent. INSERT into version A shifts V-positions in A alone; version B's V-space is unaffected.

### Correspondence preservation

**INS-F3 (V→I correspondence).** For every position that existed before the insertion, the content at the (possibly shifted) position is the same byte that was at the original position:

  `(A q : q ∈ dom.poom(d) ∧ q < p : ispace'.(poom'(d).q) = ispace.(poom(d).q))`
  `(A q : q ∈ dom.poom(d) ∧ q ≥ p : ispace'.(poom'(d).(q + #c)) = ispace.(poom(d).q))`

This is the central architectural invariant. V-addresses shift; I-addresses do not. The bijection between content identity and content value is preserved through the shift. Nelson designed the two-space architecture precisely for this: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Proof. For content before the insertion point: `poom'(d).q = poom(d).q` (by INS4, first clause), so the I-address is unchanged. By P1, the content at that I-address is unchanged. For content at or after the insertion point: `poom'(d).(q + #c) = poom(d).q` (by INS4, second clause), so the I-address is again unchanged. By P1, the content at that I-address is unchanged. In both cases, the content retrievable through the V-space mapping after INSERT is identical to the content retrievable before INSERT, for every pre-existing position. ∎

This is not a derived convenience. It is the property on which link survivability, attribution, version comparison, transclusion integrity, and royalty accounting all depend. If INSERT corrupted the V→I mapping — swapping which I-address a V-position refers to — links would silently attach to wrong content, attribution would identify wrong authors, version comparison would report false correspondences, and royalty payments would go to wrong parties.

### Link survival

**INS-F4 (Link endpoint invariance).** INSERT does not modify any link structure. All link endsets resolve to the same content after the insertion as before:

  `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

Links reference I-space addresses in their endsets, not V-space positions. INSERT creates new I-space entries but does not modify existing ones (INS-F1), and does not modify any link structure. Therefore every endset that referenced content before the insertion still references the same content. Nelson states this as a design property: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." For INSERT specifically, the "if anything is left" condition is trivially satisfied — INSERT adds content but removes nothing. Every link endpoint that resolved before continues to resolve afterward.

The proof is almost too short to write. Let L be any link, and let E be any endset of L. E is a set of I-space address ranges. By INS-F1, no pre-existing I-space content changes. By INS1, the fresh addresses are disjoint from `dom.ispace`. Therefore E references exactly the same addresses, and those addresses contain exactly the same content. Link resolution is invariant under INSERT. ∎

### Subspace confinement

**INS-F5 (Subspace isolation).** INSERT at a position in the text subspace does not modify arrangement entries in the link subspace, and vice versa:

  `(A q ∈ other_subspace(d, sub(p)) : poom'(d).q = poom(d).q)`

When INSERT places text at position 1.x, link entries at positions 2.x are completely unaffected — their V-positions do not shift, their I-address mappings do not change. The position shift (INS4) operates only within the subspace of the insertion point.

Gregory's evidence reveals the mechanism by which the existing implementation achieves this — a two-boundary construction that limits the shift region to positions between the insertion point and the start of the next subspace. For an insertion at position N.x, the shift region is bounded above by (N+1).1. Entries at or beyond this boundary are classified into a "no shift" category and left untouched. A concrete example: with text at V:1.1-1.5 and a link at V:2.1, an insertion at V:1.3 shifts text entries in [1.3, 2.1) rightward by the insertion width, while the link entry at V:2.1 remains at V:2.1 with every field — V-displacement, I-displacement, V-width, I-width — byte-identical to its pre-insertion state.

The abstract property is that the two subspaces of a document (text and links) are independently arranged. No operation on one subspace can disturb the other. The bounded-shift mechanism is one way to achieve this; the guarantee itself is what any implementation must provide.

### Span index stability

**INS-F6 (Existing index frame).** INSERT does not modify or remove any pre-existing span index entry:

  `(A (a, d') : (a, d') ∈ spanindex : (a, d') ∈ spanindex')`

This follows from P2. But we state it explicitly for INSERT because it has a useful corollary: the only change to the span index is the addition of the new entries specified by INS5. The index grows by exactly the entries for the newly allocated addresses, and all previous entries are preserved.


## The correspondence theorem

The individual properties above can be assembled into a single characterization of what INSERT means. We state it as a theorem and verify it against the component properties.

**INS-CORR (INSERT Correctness).** Let Σ' = INSERT(d, p, c) applied to state Σ satisfying PRE1–PRE4. Then:

(i) `dom.ispace' = dom.ispace ∪ {a₀, ..., a₀ + #c - 1}` where `{a₀, ..., a₀ + #c - 1} ∩ dom.ispace = ∅` — exactly #c fresh addresses are added.

(ii) `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — all pre-existing content is preserved.

(iii) `(A i : 0 ≤ i < #c : ispace'.(a₀ + i) = c.i)` — new addresses receive the inserted content.

(iv) `poom'(d) = shift(poom(d), p, #c) ∪ {(p+i, a₀+i) : 0 ≤ i < #c}` where `shift` displaces all text-subspace positions ≥ p rightward by #c and leaves all other positions unchanged.

(v) `(A d' : d' ≠ d : poom'(d') = poom(d'))` — all other documents are untouched.

(vi) `spanindex' = spanindex ∪ {(a₀+i, d) : 0 ≤ i < #c}` — exactly the new addresses are indexed.

(vii) `links' = links` — no link is created, modified, or destroyed.

(viii) `(A q ∈ link_subspace(d) : poom'(d).q = poom(d).q)` — link positions are unaffected (when the insertion targets the text subspace).

Clause (i) follows from INS1 and P0. Clause (ii) from INS-F1 (= P1). Clause (iii) from INS2. Clause (iv) from INS3, INS4, and INS-F5. Clause (v) from INS-F2. Clause (vi) from INS5 and INS-F6. Clause (vii) from INS-F4. Clause (viii) from INS-F5.


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

**INSERT does not create links.** INSERT creates content in I-space and arranges it in V-space. It does not create, modify, or destroy any link structure (INS-F4). Link creation is a separate operation (CREATELINK) with its own preconditions and effects.

**INSERT does not modify the allocation state of other subspaces.** If the document previously had link atoms allocated in the link I-subspace (via CREATELINK), those allocations are invisible to INSERT's text allocation. The text allocation counter operates within its own subspace and continues from the previous text high-water mark, regardless of intervening link allocations (INS1a). An implementation that used a single global allocation counter per document — causing link creation to advance the text counter — would violate INS1a. The specification mandates that each atom type's allocation is subspace-local.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| P0 | `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation removes an address | introduced |
| P1 | `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes | introduced |
| P2 | `(A (a,d) : (a,d) ∈ spanindex : (a,d) ∈ spanindex')` — span index never loses an entry | introduced |
| PRE1 | `d ∈ dom.owner` — target document must exist | introduced |
| PRE2 | `user = owner(d)` — requesting user must be document owner | introduced |
| PRE3 | `1 ≤ p ≤ |poom(d)| + 1` — position within [1, m+1] | introduced |
| PRE4 | `#c > 0` — content to insert is non-empty | introduced |
| INS1 | INSERT allocates #c fresh addresses disjoint from dom.ispace | introduced |
| INS1a | Text allocation is subspace-local, independent of link allocations | introduced |
| INS2 | `(A i : 0 ≤ i < #c : ispace'.(a₀+i) = c.i)` — new addresses receive inserted content | introduced |
| INS3 | `(A i : 0 ≤ i < #c : poom'(d).(p+i) = a₀+i)` — content placed at insertion position | introduced |
| INS4 | Positions < p unchanged; positions ≥ p shift rightward by #c (within same subspace) | introduced |
| INS5 | `(A i : 0 ≤ i < #c : (a₀+i, d) ∈ spanindex')` — new range indexed under d | introduced |
| INS-F1 | `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — existing I-space content unchanged | introduced |
| INS-F2 | `(A d' : d' ≠ d : poom'(d') = poom(d'))` — other documents' V-space unchanged | introduced |
| INS-F3 | V→I correspondence preserved: same content at shifted positions | introduced |
| INS-F4 | `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))` — all links unchanged | introduced |
| INS-F5 | `(A q ∈ other_subspace(d, sub(p)) : poom'(d).q = poom(d).q)` — subspace isolation | introduced |
| INS-F6 | `(A (a,d') : (a,d') ∈ spanindex : (a,d') ∈ spanindex')` — existing index preserved | introduced |
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
