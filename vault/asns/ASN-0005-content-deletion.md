# ASN-0005: Content Deletion

*2026-02-23*

We wish to understand what deletion means in a system where content is permanent. The word "delete" appears throughout Nelson's design, yet the system's foundational commitment — that every allocated address persists forever and content at that address never changes — seems to forbid the very thing the word denotes. The tension is real, and its resolution is one of the most revealing features of the architecture: deletion is an act of rearrangement, not an act of destruction. We develop this claim formally, derive its consequences for links and transclusions, characterize the sense in which deletion is reversible, and identify the residual effects that make the span index diverge from the live state.


## The state we need

We require a minimal vocabulary. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. This is the permanent store. Once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a function from virtual positions to addresses, `poom(d) : Pos → Addr`. This is document d's current arrangement — which content appears at which virtual position.
- **spanindex**: a relation recording which documents have contained which address ranges, `spanindex ⊆ Addr × DocId`. This index is append-only — entries are added but never removed.
- **links**: a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, `poom(d).p` for the I-address that document d maps virtual position p to, and `img(poom(d))` for the image of the mapping — the set of I-addresses that d currently references. We use primed names for the state after an operation.

A document's virtual stream has two subspaces: text (positions prefixed by subspace identifier 1) and links (positions prefixed by subspace identifier 2). DELETE operates on positions in one subspace and, as we shall establish, affects nothing outside that subspace.


## The permanence context

Before stating what DELETE does, we must be precise about what it cannot do. The system makes three permanence commitments that constrain every operation:

**P0 (Address irrevocability).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation shrinks the set of allocated addresses.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (Index monotonicity).** `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')` — the span index never loses an entry.

These three properties hold for every operation, including DELETE. We do not prove them here — we take them as the context within which DELETE must be defined. The question is: what can DELETE mean if it must satisfy P0, P1, and P2?


## DELETE as V-space surgery

The answer is that DELETE operates exclusively on V-space. It modifies a single document's arrangement, removing a contiguous span of virtual positions and compacting the remaining positions to close the gap. It does nothing to I-space.

Let DELETE(d, p, w) denote the deletion of w positions starting at position p in document d. We require:

**DEL0 (I-space frame).** DELETE does not modify ispace:

  `dom.ispace' = dom.ispace` and `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Nelson is direct: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And the diagram on Literary Machines 4/9 labels the result: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The phrase "not currently addressable" is precise — the bytes are no longer reachable through this document's virtual stream, but they remain at their permanent I-space addresses.

DEL0 is not a safety net or an optimization opportunity. It is forced by P0 and P1. Any operation that attempted to remove content from I-space would violate address irrevocability; any operation that attempted to overwrite it would violate content immutability. DELETE can modify only the mutable layer — V-space.

**DEL1 (V-space effect).** After DELETE(d, p, w), the V-space mapping of document d loses the positions in [p, p ⊕ w) and surviving positions beyond the deletion shift leftward by w:

  `(A q : q < p : poom'(d).q = poom(d).q)`
  `(A q : q ≥ p ⊕ w : poom'(d).(q ⊖ w) = poom(d).q)`
  `(A q : p ≤ q < p ⊕ w : q ∉ dom.poom'(d))`

where `⊕` and `⊖` denote position arithmetic (tumbler addition and subtraction within a subspace). The first clause says content before the deletion is untouched. The second says content after the deletion shifts left, preserving its I-address mapping. The third says the deleted positions disappear from the mapping.

Nelson describes this compaction as the inverse of INSERT's expansion: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" — DELETE decreases them by the length of the deleted text.


## The frame conditions

An operation is not specified until we state what it does NOT change. DELETE's frame conditions are as important as its effects.

**DEL2 (Cross-document isolation).** DELETE on document d does not affect any other document's POOM:

  `(A d' : d' ≠ d : poom'(d') = poom(d'))`

No operation on document d₁ may modify the V-space mapping of d₂ ≠ d₁. Gregory's implementation evidence confirms this with structural finality: the delete function takes a document handle and operates on that document's enfilade tree alone. No other document's tree is opened, read, or modified. The isolation is not a check — it is a consequence of the operation receiving exactly one document's data structure as input.

**DEL3 (Subspace confinement).** DELETE at a position in subspace s of document d shifts only V-positions in subspace s:

  `(A q ∈ other_subspace(d, s) : poom'(d).q = poom(d).q)`

A text deletion does not shift link positions. A link deletion does not shift text positions. Gregory confirms the mechanism: an exponent guard in the shift arithmetic makes cross-subspace subtraction a no-op. The abstract guarantee is that the document's two subspaces are independently arranged.

**DEL4 (Span index frame).** DELETE does not remove entries from the span index:

  `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')`

This follows from P2, but we state it explicitly because it has a non-obvious consequence: after DELETE removes I-addresses from document d's POOM, the span index still claims that d "contains" those addresses. The forward direction of the correspondence breaks — the index over-approximates the current state. We return to this point below.

**DEL5 (Link structure frame).** DELETE does not modify any link structure:

  `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

Links are stored by I-space addresses in their endsets. DELETE operates on V-space. No operation that modifies only V-space can reach into the link structures, which live in I-space. The endset addresses of every link are unchanged after any DELETE.


## I-dimension invariance in surviving entries

The V-space compaction merits closer inspection. When DELETE shifts surviving entries leftward, what exactly changes? The question matters because each entry in the POOM maps a V-position to an I-address, and we need to confirm that the shift is a pure V-translation.

**DEL6 (I-dimension invariance under compaction).** For every surviving POOM entry, the I-address fields (I-displacement and I-width) remain exactly unchanged. Only the V-displacement field is modified:

  `(A entry ∈ surviving(poom(d)) : entry'.iaddr = entry.iaddr ∧ entry'.iwidth = entry.iwidth)`

Gregory provides definitive evidence. The shift operation modifies `cdsp.dsas[V]` (V-displacement) and touches no other field. The three untouched fields are: I-displacement (the starting I-address), V-width (the virtual extent), and I-width (the I-address extent). The modification is a single subtraction — the deletion width is subtracted from the V-displacement of every entry beyond the deletion point. The I-address components are never read, never written, never passed as arguments to any arithmetic. DELETE's compaction is a pure V-translation that leaves all I-space information intact in surviving entries.

This is the formal expression of Nelson's dictum that deletion is rearrangement. The "arrangement" lives in the V-dimension of the POOM entries. The "content identity" lives in the I-dimension. DELETE modifies the former and leaves the latter untouched.


## Transclusion independence

We are now in a position to derive a property that the consultation answers confirmed empirically: deletion in one document cannot affect content visible in another.

**Theorem (Transclusion survives deletion).** If document B transcludes content at I-addresses A from document D, and D deletes that content, then B still references A and can resolve every address in A.

*Proof.* D's DELETE modifies only `poom(D)` (by DEL2, no other document's POOM is affected). The I-addresses in A remain in `dom.ispace` (by DEL0, DELETE does not modify ispace). Therefore `poom(B)` still maps V-positions to addresses in A, and `ispace.a` is well-defined for every `a ∈ A`. The transclusion is intact. ∎

The independence is structural, not temporal. It does not depend on the order of operations, the timing of access, or whether B "noticed" the deletion. B's POOM is a separate data structure from D's POOM. D's operation cannot reach B's state. This is the force of DEL2 — cross-document isolation is not a feature to be maintained but an architectural consequence of the operation's scope.

Nelson states it without qualification: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And more broadly: "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals."


## Link survival

Links in the system attach to I-space addresses — to the bytes themselves, not to their virtual positions. Nelson calls this the "strap between bytes" design: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing."

We can now derive link survival after deletion:

**Theorem (Links survive deletion).** If link L has an endset referencing I-address a, and a is deleted from document d, then L's endset still references a and a remains a valid I-space address.

*Proof.* By DEL5, DELETE does not modify L's endsets. By DEL0, `a ∈ dom.ispace'`. Therefore `a` is still referenced by L and `ispace.a` is still defined. ∎

The derivation has exactly two premises: DELETE doesn't touch links (DEL5), and DELETE doesn't touch I-space (DEL0). No special-case link protection is needed.

What changes after deletion is not the link's validity but its *discoverability* through the document that performed the delete. Link discovery works by converting a document's V-spans to I-addresses and querying for links whose endsets overlap. After DELETE removes the V→I mapping for address a from document d, a query through d will not find L — there are no V-positions in d that map to a, so the query never generates a as a search term. But the link is still discoverable through any other document whose POOM maps to a.

This leads us to a taxonomy of link discoverability states.


## Ghost links

We define the discoverability state of a link endset relative to the set of documents that reference its I-addresses:

**DEL7 (Link discoverability classification).** Let L be a link with endset referencing I-addresses A. The link's discoverability state for a given endset is determined by how many documents' POOMs currently reference addresses in A:

- **Live**: `(E d, p : poom(d).p ∈ A)` — at least one document maps to addresses in A. The link is discoverable through that document.
- **Ghost**: `¬(E d, p : poom(d).p ∈ A)` — no document's current POOM maps to any address in A. The link exists (its I-space structure is permanent) but is not discoverable through any document's V-space query.

A link can transition from live to ghost as documents delete content. It can transition from ghost to live when content is re-introduced to a document's POOM via COPY (as we shall establish below). The transition is not a property of the link — which is immutable — but of the surrounding documents' arrangements.

**DEL8 (Ghost link resolution).** When a query resolves a ghost link's endset — attempting to convert the endset's I-addresses to V-positions in a specified document — the result is empty. The operation succeeds (no error is raised) but returns no V-positions:

  `(A a ∈ endset(L) : ¬(E p : poom(d).p = a)) ⟹ resolve(L, endset, d) = ∅`

Gregory confirms this behavior. The I-to-V conversion function searches the document's POOM for the endset's I-addresses. When no POOM entry maps to those addresses, the search returns NULL, and the calling function returns an empty result without error. The ghost link is not "broken" — it is silently empty. The distinction matters: a broken link would indicate corruption; an empty resolution indicates that the referenced content is not currently arranged in the queried document.

Nelson acknowledges the intermediate case: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." The words "if anything is left at each end" describe exactly the ghost boundary — the link persists structurally regardless, but it becomes navigable only when at least some bytes at each endset are arranged in some document's V-space.


## The span index divergence

We now address a consequence of P2 (span index monotonicity) combined with DELETE's asymmetry. When content is placed in a document — by INSERT or COPY — the span index records the association between the I-addresses and the document:

  `(A a ∈ newly_placed : (a, d) ∈ spanindex')`

When content is later deleted from that document's POOM, the span index entry persists (by P2). This creates a divergence:

**DEL9 (Span index over-approximation).** After DELETE, the span index may contain entries `(a, d)` for which `a ∉ img(poom(d))`:

  `(E a, d : (a, d) ∈ spanindex ∧ ¬(E p : poom(d).p = a))`

The forward inclusion holds — every live reference is indexed:

  `(A d, a : (E p : poom(d).p = a) ⟹ (a, d) ∈ spanindex)`

But the reverse does not:

  `(a, d) ∈ spanindex ⇏ (E p : poom(d).p = a)`

Gregory provides the structural explanation. The span index has insertion functions but no deletion functions. No `deletespanf` exists. When DELETE removes content from a document's POOM, no corresponding removal from the span index occurs. The index is write-only.

This means any query that consults the span index — such as FINDDOCSCONTAINING, which returns all documents associated with a set of I-addresses — returns a **superset** of the documents that currently contain those addresses:

**DEL10 (FINDDOCSCONTAINING is approximate).** The result of FINDDOCSCONTAINING(A) satisfies:

  `{d : (E a ∈ A, p : poom(d).p = a)} ⊆ FINDDOCSCONTAINING(A)`

but not necessarily equality. Documents that previously contained the I-addresses but have since deleted them appear as stale results.

The caller cannot distinguish stale from current results at query time. The distinction emerges only when attempting to resolve the I-addresses through each candidate document's POOM: a stale result yields an empty V-span set; a current result yields actual positions. This filtering — querying the span index for candidates, then validating each candidate against its POOM — is the specified access pattern. The span index provides breadth (which documents might be relevant); the POOM provides precision (which documents actually reference the content now).

We observe that this is not a defect. It is the price of P2. An index that could retract entries would be exact but would violate monotonicity. An append-only index is monotone but over-approximate. The architecture chooses monotonicity, consistent with the broader principle: the permanent layer never retracts a claim. The span index is a historical record — it answers "which documents have ever contained these addresses?" rather than "which documents currently contain them?"


## Reversibility

We now address the central question: in what sense is deletion reversible? The answer has two parts, and the distinction between them is the deepest consequence of the I-space/V-space separation.

**DEL11 (Content persistence after deletion).** The content that was "deleted" still exists in I-space. Let A be the set of I-addresses removed from document d's POOM by DELETE. Then:

  `(A a ∈ A : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`

This follows from DEL0 (DELETE does not modify ispace). The "deleted" content is not gone — it is merely unreferenced by one document's current arrangement. The content is available for re-inclusion at any time.

But re-inclusion comes in two forms, and only one of them constitutes genuine reversal.

**DEL12 (INSERT does not reverse DELETE).** If content at I-addresses A is deleted from document d, and the user subsequently INSERTs text with the same character values, the new content receives fresh I-addresses B where `A ∩ B = ∅`:

  `(A a ∈ B : a ∉ dom.ispace)` (freshness of INSERT)

The document now displays text that looks the same. But every cross-document relationship is severed:

- Links whose endsets reference addresses in A do not discover the content at addresses B.
- Version comparison between d and any document sharing addresses in A finds no correspondence — A and B are disjoint address sets.
- Attribution at addresses in B identifies the current document as creator, not the original creator of content at A.
- The span index for addresses in A still points to d (a stale entry), while the span index for B is new.

INSERT after DELETE is not reversal. It is the creation of textually identical but structurally distinct content. The identity — as encoded in I-space addresses — is different.

**DEL13 (COPY reverses DELETE identity-preservingly).** If content at I-addresses A is deleted from document d, and document d' still references some or all of A (because d' transcluded the content before or after the deletion, or because d' is a previous version of d), then COPY from d' to d restores the original I-addresses in d's POOM:

  `(A a ∈ A : (E p : poom(d').p = a)) ⟹ after COPY: (E q : poom'(d).q = a)`

After this COPY, d's POOM again maps positions to the original I-addresses in A. The consequences are immediate:

- Links whose endsets reference A become discoverable through d again.
- Version comparison between d and other documents sharing A finds correspondence.
- Attribution at A identifies the original creator (encoded in the I-address).
- The content's identity is fully restored — as if the deletion had never occurred, from the perspective of address-based queries.

Gregory confirms this cycle end-to-end. Create content at I-addresses α₁...αₙ. Create a link referencing those addresses. Delete the content from the document. COPY the same content back from a version or transclusion that still references it. The link is discoverable again. The reason is that COPY shares existing I-addresses (extracting them from the source POOM and depositing them unchanged in the target), while INSERT allocates fresh ones. The COPY operation is the identity-preserving restoration mechanism.

Nelson's architecture makes this possible because version history is built into the system: "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." Every previous version of every document is reconstructible. The previous version contains the I-addresses that the deletion removed. COPY from that version restores them.


## What the system must remember

Given that DELETE is reversible via COPY, we ask: what must the system retain so that reversal is possible? The answer is: almost nothing beyond what it already retains by its permanence guarantees.

**DEL14 (Reversal prerequisites).** For DELETE(d, p, w) to be reversible, the system must retain:

(a) The I-space content at the deleted addresses — guaranteed by P0 and P1. The content was never destroyed.

(b) Some document whose POOM still maps to the deleted I-addresses — this is the source for the restorative COPY. In the common case, previous versions of d serve this role. If the system maintains version history (and Nelson's design requires it), then the version of d that existed before the DELETE still references the deleted I-addresses.

(c) The DELETE operation record itself — which identifies the position and width of the deletion. The system's journal records every operation, so the DELETE is already captured. From this record plus the version history, the POOM at any previous state is reconstructible.

(d) Nothing about links. Links remember themselves — their endset I-addresses are unchanged (DEL5). The moment the I-addresses re-enter a document's POOM, links are discoverable again through that document. No "link re-attachment" step is needed.

(e) Nothing about transclusion structure. The V→I mapping restored by COPY carries the transclusion structure implicitly — the I-addresses encode which document created the content (home document is readable from the address). Restoring the mapping restores the provenance.

The architecture does not need a special undo mechanism. The entire design is, in Nelson's phrase, built on an "append-only storage system" where "the file management system automatically keeps track of the changes and the pieces." Deletion is a change of view; the reality underneath is permanent. Reversal is a request for a previous view.


## The asymmetry of effects

We can now characterize DELETE's complete impact by collecting the asymmetries:

| Component | Effect of DELETE | Reversible via COPY? |
|-----------|-----------------|---------------------|
| Target document's POOM | V-positions removed, survivors compacted | Yes — COPY restores I-addresses at new V-positions |
| I-space content | Unchanged (DEL0) | N/A — nothing to reverse |
| Span index | Unchanged (DEL4); stale entries persist | N/A — entries were never removed |
| Link structures | Unchanged (DEL5) | N/A — nothing to reverse |
| Other documents' POOMs | Unchanged (DEL2) | N/A — nothing to reverse |
| Link discoverability through d | Reduced — ghost transitions possible | Yes — re-introducing I-addresses restores discoverability |

The asymmetry is stark. DELETE touches exactly one thing: the target document's V→I mapping. Everything else — the permanent store, the span index, the links, all other documents — is unchanged. The "blast radius" is a single document's arrangement, and even within that document, the I-dimension of surviving entries is untouched (DEL6).


## DELETE preserves the invariants

We verify that DELETE preserves the system's key structural guarantees.

*P0 (address irrevocability)*: DELETE does not modify `dom.ispace` (DEL0). Preserved trivially.

*P1 (content immutability)*: DELETE does not modify any `ispace.a` (DEL0). Preserved trivially.

*P2 (span index monotonicity)*: DELETE does not remove span index entries (DEL4). Preserved trivially.

*Subspace independence*: DELETE's V-compaction is confined to the subspace of the deletion (DEL3). The other subspace is untouched.

*Cross-document isolation*: DELETE operates on a single document's POOM (DEL2). All other documents' states are preserved.

*Link permanence*: DELETE does not modify link structures (DEL5). All link endsets are preserved.

The pattern is striking: DELETE preserves every system invariant because it modifies only one component of the state — one document's V-space mapping — and the invariants are defined in terms of components that DELETE does not touch. This is what Nelson means when he distinguishes "the document's current arrangement" from "the content itself." The invariants protect content. DELETE rearranges the arrangement.


## Deletion of links

The preceding analysis focused on text deletion — removing content from the text subspace of a document's V-space. We must also consider link deletion.

Nelson's design treats deleted links symmetrically with deleted bytes. The Literary Machines 4/9 diagram labels both: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" and, in parallel, "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)."

**DEL15 (Link deletion is also V-space surgery).** Deleting a link from a document's link subspace removes the V→I mapping for the link's position within that document. The link's I-space structure (its endsets, type, content) is unaffected:

  `(A L : L.iaddr ∈ deleted_addrs : L ∈ links' ∧ endsets'(L) = endsets(L))`

A "deleted" link is not destroyed — it is removed from one document's link arrangement. The link's I-space structure persists permanently. Previous versions of the document (which include the link in their link subspace) can still resolve it. Other documents that reference the link are unaffected.

The parallel between text deletion and link deletion is exact: both remove a V→I mapping from a single document's POOM; both leave I-space untouched; both are reversible via COPY from a source that still references the original I-addresses. The two subspaces are structurally independent (DEL3), so a text deletion cannot accidentally remove links, and a link deletion cannot shift text positions.


## Formal summary

We collect the specification of DELETE. The operation `δ(Σ, DELETE(d, p, w)) = Σ'` is defined by:

*Precondition:* Position p is valid in document d's virtual stream, and the span [p, p ⊕ w) lies within the existing content: `(A q : p ≤ q < p ⊕ w : q ∈ dom.poom(d))`. The width w is nonzero.

*Effect:* Document d's POOM is modified. The entries mapping positions in [p, p ⊕ w) to I-addresses are removed. Entries at positions beyond p ⊕ w are shifted leftward by w, with their I-address fields unchanged (DEL1, DEL6). The virtual stream contracts by w positions.

*Frame:* I-space is unchanged (DEL0). All other documents' POOMs are unchanged (DEL2). The link subspace of d is unchanged if the deletion targets the text subspace, and vice versa (DEL3). The span index is unchanged (DEL4). All link structures are unchanged (DEL5).

*Invariants preserved:* P0, P1, P2, subspace independence, cross-document isolation, link permanence — all trivially, because DELETE modifies only one document's V-space mapping.

*Residual effects:* The span index retains entries for the deleted I-addresses associated with document d (DEL9). Queries consulting the span index may return d as a stale result (DEL10). Link discoverability through d is reduced; links whose endsets reference only deleted addresses become ghosts relative to d (DEL7, DEL8).

*Reversibility:* Content persists in I-space (DEL11). Identity-preserving restoration is possible via COPY from any document whose POOM still maps to the deleted I-addresses (DEL13). Re-typing the same text via INSERT does not restore identity — it creates new addresses (DEL12). The version history provides the canonical source for restoration.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| DEL0 | DELETE does not modify ispace: `dom.ispace' = dom.ispace` and `ispace'.a = ispace.a` for all `a ∈ dom.ispace` | introduced |
| DEL1 | DELETE removes V-positions in [p, p⊕w), shifts surviving positions beyond the deletion leftward by w, preserving their I-address mappings | introduced |
| DEL2 | DELETE on document d does not modify any other document's POOM: `poom'(d') = poom(d')` for all `d' ≠ d` | introduced |
| DEL3 | DELETE's V-compaction is confined to the subspace of the deletion; the other subspace is unaffected | introduced |
| DEL4 | DELETE does not remove entries from the span index; follows from P2 | introduced |
| DEL5 | DELETE does not modify any link structure: all endsets are unchanged | introduced |
| DEL6 | DELETE's V-compaction modifies only V-displacement of surviving entries; I-displacement, I-width, and V-width are invariant | introduced |
| DEL7 | A link endset is live (discoverable through some document) or ghost (no document's POOM maps to its I-addresses); DELETE can transition endsets from live to ghost | introduced |
| DEL8 | Resolving a ghost link's endset through a document returns empty (not error); the operation succeeds with no V-positions | introduced |
| DEL9 | After DELETE, the span index may contain stale entries `(a, d)` where `a ∉ img(poom(d))` | introduced |
| DEL10 | FINDDOCSCONTAINING returns a superset of documents currently referencing the queried I-addresses; stale results require POOM validation | introduced |
| DEL11 | "Deleted" content persists in I-space; `a ∈ dom.ispace'` for all deleted addresses a | introduced |
| DEL12 | INSERT after DELETE creates fresh I-addresses, not the original ones; textual identity ≠ structural identity | introduced |
| DEL13 | COPY from a document still referencing the original I-addresses restores those addresses in the target's POOM (identity-preserving reversal) | introduced |
| DEL14 | Reversal requires: persistent I-space (P0/P1), a POOM still referencing the addresses (version history), and the operation record (journal); no additional state is needed | introduced |
| DEL15 | Link deletion is V-space surgery on the link subspace, symmetric with text deletion; the link's I-space structure is unaffected | introduced |
| P0 | (context) Address irrevocability: `dom.ispace ⊆ dom.ispace'` for every operation | context |
| P1 | (context) Content immutability: `ispace'.a = ispace.a` for all `a ∈ dom.ispace`, for every operation | context |
| P2 | (context) Span index monotonicity: `spanindex ⊆ spanindex'` for every operation | context |


## Open Questions

Must the system provide a mechanism to query the span index for "current" containment (excluding stale entries), or is the two-step pattern (span index query followed by POOM validation) the only specified access method?

What must the system guarantee about the atomicity of DELETE when the deletion spans multiple POOM entries — must all entries be removed in a single observable step, or may intermediate states be visible?

Under what conditions, if any, may a system reclaim span index entries for I-addresses that are provably unreferenced by every document's POOM — and would such reclamation violate the specification or merely an implementation choice?

What must the system guarantee about the behavior of FINDDOCSCONTAINING when called during a DELETE operation — must the result reflect the pre-DELETE or post-DELETE state, or is either acceptable?

If the version history that would serve as the COPY source for reversal is itself subject to deletion (the user deletes content from all versions), what is the last-resort source for identity-preserving restoration — and must the system guarantee that such a source always exists?

What invariants must the system maintain to ensure that the two-step filtering pattern (DEL10) is sound — specifically, must the span index be a superset at every observable state, or only at quiescent states?

Must the span index accumulation be bounded, or may it grow without limit as documents repeatedly INSERT and DELETE the same I-addresses via COPY cycles?
