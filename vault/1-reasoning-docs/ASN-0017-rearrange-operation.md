# ASN-0017: Rearrange Operation

*2026-02-24*

We wish to understand REARRANGE — the operation that reorders content within a document without introducing new content or removing existing content. INSERT creates; DELETE removes (from view); but REARRANGE does neither. It changes only the *order* in which existing content appears. This makes it a unique operation in the system: the only edit primitive that relocates content while preserving every relationship anchored to it. The claim is strong. We develop it formally, derive the consequences for links, transclusions, provenance, and version comparison, characterize the precise sense in which REARRANGE differs from DELETE-then-INSERT, and identify the boundary conditions where the specification is incomplete.


## The state we need

We require the same minimal vocabulary as prior operations. Let the system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. The permanent store. Once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a function from virtual positions to addresses, `poom(d) : Pos → Addr`. Document d's current arrangement — which content appears at which virtual position.
- **spanindex**: a relation recording which documents have contained which address ranges, `spanindex ⊆ Addr × DocId`. Append-only: entries are added but never removed.
- **links**: a set of link structures, each with three endsets (from, to, type), where endsets reference I-space address ranges.
- **provenance(a)**: a function from addresses to their creation context — which user, which document, which moment. Determined at allocation time, encoded in the address structure itself.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address `a`, `poom(d).p` for the I-address that document d maps virtual position p to, and `img(poom(d))` for the image — the set of I-addresses that d currently references. We use primed names for the state after an operation.


## The permanence context

REARRANGE operates under the same permanence commitments as every other operation:

**P0 (Address irrevocability).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace')` — no operation shrinks the set of allocated addresses.

**P1 (Content immutability).** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (Index monotonicity).** `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')` — the span index never loses an entry.

These properties constrain every operation. We state them here because REARRANGE has a special relationship to them: where INSERT must satisfy P0 and P1 while *extending* I-space, and DELETE must satisfy them while *narrowing* V-space, REARRANGE will satisfy them trivially — by touching neither I-space nor the span index. The constraints that bind the other operations are vacuously satisfied for REARRANGE.


## What REARRANGE is

Nelson specifies REARRANGE as one of the 17 FEBE protocol commands — a first-class primitive, not a convenience derived from DELETE and INSERT. The operation "transposes two regions of text." Nelson provides two forms:

- **3-cut (pivot):** Given cut points a, b, c in document d's V-space with a < b < c, the operation swaps the content in [a, b) with the content in [b, c). We write PIVOT(d, a, b, c).
- **4-cut (swap):** Given cut points a, b, c, d with a < b ≤ c < d, the operation swaps the content in [a, b) with the content in [c, d). The content in [b, c) may shift but is not itself swapped. We write SWAP(d, a, b, c, d).

The pivot is the fundamental case. A SWAP with b = c degenerates to a pivot. A pivot with equal-width regions is a clean swap where the middle region stays fixed. We develop the specification primarily for the pivot, then extend to the swap.

Nelson is explicit about where REARRANGE sits in his taxonomy of editorial operations. "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." Rearrangement stands alongside addition and subtraction — not derived from them. Its presence as a separate primitive signals that it does something the others cannot.


## The core property: I-space invariance

We begin with the property that defines REARRANGE and distinguishes it from every other edit operation.

**R0 (I-space frame).** REARRANGE does not modify ispace:

  `dom.ispace' = dom.ispace` and `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Furthermore, REARRANGE allocates no fresh addresses: `dom.ispace' \ dom.ispace = ∅`.

R0 is stronger than what P0 and P1 require. P0 says the domain does not shrink. P1 says values do not change. R0 says, in addition, that the domain does not *grow*. INSERT satisfies P0 and P1 while extending the domain — it adds fresh addresses. REARRANGE satisfies P0 and P1 by leaving the domain utterly unchanged. No address is created, no address is removed, no content is modified.

Nelson justifies this from the architecture of REARRANGE as a "pure V-space operation." The operation transposes regions of text — that is, regions of the document's virtual byte stream. "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." The order changes; the bytes do not. The permanent store — which is where I-space content lives — is not a participant in this operation. It has nothing to contribute and nothing to receive.

Gregory confirms from the implementation that the rearrange code path contains no calls to the content storage insertion functions, no allocation of fresh permascroll addresses, and no modification of any content storage entry. The implementation modifies exactly one field of each affected mapping entry: the V-displacement. The I-displacement, the I-width, and all associated metadata are untouched.


## Content identity preservation

R0 tells us I-space does not change globally. We now state a sharper property about the specific document being rearranged.

**R1 (Content multiset invariance).** The multiset of I-addresses referenced by document d's V-space is unchanged:

  `img(poom'(d)) = img(poom(d))`

No I-address enters the document's reference set. No I-address leaves it. The same bytes are present in the same quantities — only their positions differ.

This property is not merely a consequence of R0. It makes a claim about `poom(d)` specifically: REARRANGE is a *bijective* V-space transformation. Let us make this precise.

**R2 (Bijective rearrangement).** There exists a position permutation π on `dom.poom(d)` such that:

  `(A p : p ∈ dom.poom(d) : poom'(d).(π(p)) = poom(d).p)`

Every I-address that was at position p is now at position π(p). The function π is a bijection — no two old positions map to the same new position, and every new position receives exactly one old position's content.

For the 3-cut case PIVOT(d, a, b, c), the permutation π is:

  `π(p) = p + (c - b)`, for `a ≤ p < b` (region 1 shifts right by width of region 2)
  `π(p) = p - (b - a)`, for `b ≤ p < c` (region 2 shifts left by width of region 1)
  `π(p) = p`, otherwise (exterior positions are fixed)

We verify this is well-defined. Letting w₁ = b - a and w₂ = c - b:

- Region 1 positions [a, b) map to [a + w₂, b + w₂) = [a + w₂, a + w₁ + w₂) = [a + w₂, c).
- Region 2 positions [b, c) map to [b - w₁, c - w₁) = [a, a + w₂).
- These two target ranges are disjoint: [a, a + w₂) and [a + w₂, c) partition [a, c).
- Fixed positions outside [a, c) are unaffected.

The total range [a, c) is covered exactly, with no overlaps and no gaps. π is a bijection on `dom.poom(d)`. ∎

For the 4-cut case SWAP(d, a, b, c, e) with a < b ≤ c < e, the permutation is:

  `π(p) = p + (c - a)`, for `a ≤ p < b` (region 1 shifts right)
  `π(p) = p + (e - c) - (b - a)`, for `b ≤ p < c` (middle shifts by difference of region widths)
  `π(p) = p - (c - a)`, for `c ≤ p < e` (region 3 shifts left)
  `π(p) = p`, otherwise

Letting w₁ = b - a, w_m = c - b, w₃ = e - c, the targets are:

- Region 1 → [a + c - a, b + c - a) = [c, c + w₁).
- Middle → [b + w₃ - w₁, c + w₃ - w₁).
- Region 3 → [c - c + a, e - c + a) = [a, a + w₃).

The full span [a, e) partitions into [a, a + w₃) ∪ [a + w₃, a + w₃ + w_m) ∪ [a + w₃ + w_m, e). We need:

  a + w₃ + w_m = c + w₃ - w₁ (middle end should meet region 1 start)
    = a + w₁ + w_m + w₃ - w₁ = a + w_m + w₃. ✓

And: a + w₃ + w_m + w₁ = e = a + w₁ + w_m + w₃. ✓

The partition is exact. π is a bijection. ∎

**An important observation about the middle region.** When w₁ = w₃ (the two swapped regions have equal width), the middle shift is w₃ - w₁ = 0. The middle region does not move. When w₁ ≠ w₃, the middle region shifts by the difference in widths. This is forced by the partition arithmetic — the middle must absorb the size difference to keep the total extent unchanged.

Gregory confirms this precisely. The implementation computes per-region offsets as pure arithmetic on the cut positions, then applies each offset by adding it to the V-displacement field of every mapping entry classified into that region. For the 3-cut case: `diff[1] = c - b` (region 1 moves right), `diff[2] = -(b - a)` (region 2 moves left). For the 4-cut case: `diff[1] = c - a`, `diff[2] = w₃ - w₁`, `diff[3] = -(c - a)`. These match the permutation π derived above.


## Frame conditions

An operation is not specified until we state what it does not change. REARRANGE has the strongest frame conditions of any edit operation.

**R3 (Span index frame).** REARRANGE does not modify the span index:

  `spanindex' = spanindex`

Not merely monotonicity (P2), but strict equality. REARRANGE creates no new content, so there is nothing to index. REARRANGE does not remove content from V-space, so there is no orphaning to record. The span index is completely undisturbed.

Gregory's evidence is structural: the rearrange code path contains no calls to any span index insertion function. No such call could be correct — an insertion into the span index would duplicate existing entries with new V-positions, corrupting the mapping, since the same I-addresses are already indexed under their original V-positions and the index does not track V-positions at all.

**R4 (Cross-document isolation).** REARRANGE on document d does not affect any other document's arrangement:

  `(A d' : d' ≠ d : poom'(d') = poom(d'))`

This is the same isolation property satisfied by INSERT and DELETE. Each document's arrangement is sovereign. Nelson is explicit: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." The principle is stronger for REARRANGE: where DELETE at least removes content from one document's V-space (potentially affecting queries through that document), REARRANGE doesn't even do that. It merely reorders within d. Other documents have no channel through which to observe the change.

**R5 (Link structure frame).** REARRANGE does not modify any link structure:

  `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))`

Link endsets reference I-space addresses. REARRANGE modifies V-space. The operation literally cannot reach the link structures. No link is created, deleted, or modified.

**R6 (Subspace frame — within the affected document).** REARRANGE with cut points in subspace s does not affect positions in other subspaces of the same document:

  `(A q ∈ dom.poom(d) : sub(q) ≠ s ⟹ poom'(d).q = poom(d).q)`

A text rearrangement does not disturb link positions. This follows from the same subspace separation that governs INSERT and DELETE.

However, we must note a precondition gap. If cut points span the boundary between subspaces — for instance, a pivot with one cut in the text subspace (1.x) and another in the link subspace (2.x) — the implementation applies V-displacement offsets that can relocate text mapping entries into the link address range and vice versa. Gregory's evidence shows that no subspace boundary guard exists in the rearrange path. The offset arithmetic is pure tumbler addition with no domain check.

We state this as a precondition:

**PRE-R1 (Subspace confinement).** All cut points of a REARRANGE operation must lie within the same V-subspace:

  `(A i, j : 0 ≤ i, j < #cuts : sub(cut.i) = sub(cut.j))`

A conforming implementation must enforce PRE-R1 or guarantee that cross-subspace displacement preserves subspace semantics. Gregory's implementation does neither — cross-subspace rearrangement silently relocates mapping entries into the wrong subspace, breaking the classification predicates that downstream operations rely on. We record this as a missing guard, not a feature of the specification.


## Combining the frame conditions

We can now state what is perhaps the most striking fact about REARRANGE. Collecting R0, R3, R4, R5:

**Theorem (REARRANGE modifies exactly one structure).** REARRANGE(d, ...) modifies only `poom(d)`. Specifically:

  `ispace' = ispace`
  `spanindex' = spanindex`
  `links' = links`
  `(A d' ≠ d : poom'(d') = poom(d'))`
  `(A a : provenance'(a) = provenance(a))`

The only thing that changes is the mapping from positions to addresses *within the single document being rearranged*. And by R1, even that mapping is not arbitrary — it is a permutation, preserving the multiset of referenced addresses.

The operation is a pure permutation of one document's arrangement. Nothing else in the universe changes.


## The fundamental distinction: REARRANGE versus DELETE+INSERT

We are now equipped to state precisely why REARRANGE exists as a primitive — why it cannot be derived from DELETE followed by INSERT.

Consider the task: move content from positions [a, b) in document d to position c. Two approaches:

**Approach A — DELETE+INSERT:**
1. Let A = {poom(d).p : a ≤ p < b} — the I-addresses currently at those positions.
2. Let text = (ispace(poom(d).p) : a ≤ p < b) — the text content at those positions.
3. DELETE(d, a, b-a) — removes positions [a, b) from d's V-space.
4. INSERT(d, c', text) — inserts text with the same character values at the adjusted position c'.

After step 4, by the properties of INSERT, the re-inserted text receives *fresh* I-addresses B where `A ∩ B = ∅`. Content identity in this system is based on creation, not on value — two sequences of bytes with identical character values but different creation events have different I-addresses. Nelson is explicit: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." Addresses are allocated, not computed from content. Two independent allocations produce two independent addresses.

The result: positions [a, b) in d now reference addresses in B instead of A. The text *looks* the same — `(A i : 0 ≤ i < b-a : ispace(B.i) = ispace(A.i))` — but the identity is severed.

**Approach B — REARRANGE:**
1. PIVOT(d, a, b, c) or equivalent.
2. By R0: no new I-addresses are allocated. By R2: the permutation maps old positions to new positions, preserving the V→I mapping.

After step 2, the positions that were at [a, b) now sit at their new locations but still reference the same addresses A. The identity is preserved.

**S0 (Identity severance under DELETE+INSERT).** A DELETE followed by INSERT of the same character values produces `img(poom'(d)) ≠ img(poom(d))` — the I-address multiset changes:

  The old addresses A exit the multiset (removed by DELETE).
  The new addresses B enter the multiset (created by INSERT).
  `A ∩ B = ∅`.

**S1 (Identity preservation under REARRANGE).** REARRANGE preserves `img(poom'(d)) = img(poom(d))` exactly — by R1.

The consequences of this distinction cascade through every system guarantee.


## Link survivability

Nelson states the guarantee explicitly, labeling it with the word "SURVIVABILITY": "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." We can derive this from the properties already established.

**Theorem (Links survive rearrangement).** If link L has an endset referencing I-address a, and document d is rearranged, then L's endset still references a, the address is still valid, and a is still reachable through d's V-space.

*Proof.* By R5, L's endsets are unchanged: a is still referenced. By R0, `a ∈ dom.ispace'`: the address is still valid. By R1, `a ∈ img(poom'(d))` since `a ∈ img(poom(d))`: the address is still reachable through d. ∎

The third clause is what distinguishes rearrangement from deletion. After DELETE, the link still exists and the address is still valid, but the address may no longer be reachable through the deleting document. After REARRANGE, every address remains reachable through the rearranged document. No content exits d's reference set, so no endset loses any resolvable address.

**L0 (Link resolution after rearrangement).** For any link L and endset E, the set of I-addresses resolvable through document d is unchanged:

  `{a ∈ E(L) : a ∈ img(poom'(d))} = {a ∈ E(L) : a ∈ img(poom(d))}`

What changes is the *position* at which each address appears. After a PIVOT that moves content from [a, b) to a new range, a query asking "where does the link endpoint appear?" will return the new V-positions. But a query asking "does the link endpoint exist in this document?" returns the same answer as before.

Gregory confirms a subtle consequence. When a pivot splits a contiguous V-span into two non-contiguous spans — for instance, when a link's endset covers [1.3, 1.5) and a pivot places 1.3 and 1.4 at different locations — the link's stored I-span remains a single contiguous range (the span index is unchanged by R3), but the dynamic V-resolution produces two disjoint V-spans. The system returns one V-specification whose internal span list contains multiple entries. This is not fragmentation of the link — the link's I-space definition is untouched — but fragmentation of the link's *appearance* through this document's current arrangement.

**L1 (Endset fragmentation under rearrangement).** After REARRANGE, a single contiguous I-span in a link's endset may resolve through the rearranged document as multiple disjoint V-spans. The number of V-spans may increase (when the rearrangement splits what was contiguous in V-space). The number never exceeds the number of distinct I-addresses in the endset:

  `#(V_spans(resolve(L, E, d'))) ≤ #(I_addresses(E(L)))`

The I-space is the stable reference frame; V-space is the mutable projection.


## Provenance immutability

REARRANGE cannot alter the provenance of any content. The argument is structural, not normative.

**R7 (Provenance frame).** `(A a : provenance'(a) = provenance(a))`.

Provenance is encoded in the I-address itself. Each I-address has the form `Node.User.Document.Element`, where each field was determined at allocation time: which server, which user, which document, which element position. Nelson is explicit: "You always know where you are, and can at once ascertain the home document of any specific word or character."

REARRANGE allocates no new addresses (R0), so it creates no new provenance records. It modifies no I-addresses, so it alters no existing provenance records. The provenance of every byte in the system is the same after REARRANGE as before.

This holds regardless of who performs the rearrangement. If user X rearranges content in document d that includes material authored by user Y (through transclusion), user Y's I-addresses still encode Y as the author. The rearrangement changes the *arrangement* (V-space), not the *authorship* (I-space). Nelson confirms: "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." The "who wrote what" determination depends on I-addresses, which REARRANGE leaves untouched.


## Transclusion isolation

We now derive a stronger isolation result than the cross-document frame R4.

**Theorem (Transclusion survives rearrangement).** If document B transcludes content at I-addresses A from document D, and D is rearranged, then B's transclusion is completely unaffected — the same I-addresses appear at the same V-positions in B.

*Proof.* By R4, `poom'(B) = poom(B)`. Therefore every V→I mapping in B is unchanged. B still maps the same V-positions to the same I-addresses in A. By R0, those I-addresses still resolve to the same content. The transclusion is intact — not merely surviving but entirely unaware that D was rearranged. ∎

The key distinction from DELETE: when D deletes transcluded content, B's transclusion survives (the I-addresses persist and B's POOM is unchanged), but the semantic relationship between D and B changes — D no longer references the shared content, while B still does. After REARRANGE, D still references every shared address. The full sharing relationship is preserved.

Nelson describes two transclusion modes: "floating" (location-fixed, tracking content identity through changes) and "frozen" (time-fixed, capturing a snapshot). Neither mode is affected by REARRANGE in the source document. A floating window tracks I-space identity, which is invariant under rearrangement. A frozen window references a specific historical state, which is also invariant — REARRANGE changes the current arrangement, not the historical record.


## Version comparison and correspondence

The version comparison operation (SHOWRELATIONOF2VERSIONS) finds "corresponding" content between two document states — content that shares I-space origin.

**R8 (Correspondence completeness).** Comparing a document's pre-rearrangement state with its post-rearrangement state yields complete correspondence — every span in the old version corresponds to a span in the new version, and vice versa:

  `(A a ∈ img(poom(d)) : a ∈ img(poom'(d)))` — nothing is "lost"
  `(A a ∈ img(poom'(d)) : a ∈ img(poom(d)))` — nothing is "new"

This follows directly from R1: the I-address multisets are identical.

The comparison mechanism works by converting each version's V-space to I-space, intersecting the I-address sets, and mapping back to V-positions in each version. Since the I-address sets are identical, the intersection equals both sets — full overlap. The returned pairs will show *different V-positions* in each version, reflecting where content moved, but the *set of shared content* is the entire document.

Contrast with DELETE+INSERT. After a DELETE at [a, b) followed by INSERT of the same text:

- Old version contains I-addresses A at [a, b).
- New version contains I-addresses B at the new position, where `A ∩ B = ∅`.
- Comparison: A appears only in the old version (apparent deletion). B appears only in the new version (apparent insertion). Zero correspondence at the affected positions.

The version comparison cannot distinguish "the same text was re-typed" from "completely different text was entered" — because in I-space, they are the same thing. New allocation means new identity means new content.

**R9 (Rearrangement is transparent to correspondence).** REARRANGE is the unique edit operation for which the version comparison between before and after shows *zero loss of shared content*:

  For INSERT: correspondence at all pre-existing positions, plus new unmatched content.
  For DELETE: correspondence at surviving positions, minus the deleted range.
  For REARRANGE: `shared_content = entire_document`.

This property is not merely useful — it is the formal criterion that separates "moving content" from "removing and re-creating content."


## Atomicity

The question of atomicity asks: during a swap of two regions, does there exist any observable intermediate state in which either region is absent from the document?

**R10 (Atomicity).** REARRANGE transitions poom(d) from one well-formed arrangement to another with no intermediate state in which any content is absent from the V-space:

  If `a ∈ img(poom(d))` before REARRANGE, then at every observable state during execution, `a ∈ img(poom_current(d))`.

The argument proceeds on two levels. At the protocol level, REARRANGE is a single FEBE command — it is not decomposed into a sequence of DELETE and INSERT messages. The front-end sends one command; the back-end executes it atomically and returns one response. There is no protocol-level intermediate state.

At the semantic level, REARRANGE is a permutation. A permutation maps the old arrangement to the new arrangement; it does not pass through "partial" arrangements where some elements have been removed but not yet placed. The mathematical object — a bijection on positions — has no intermediate states by construction.

Nelson confirms from the implementation architecture: "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." The "canonical order" mandate means the data structure is always well-formed. There is no moment of inconsistency. This is not eventual consistency — it is the invariant that every mutation leaves the structure valid.


## V-space address instability

We now address what REARRANGE does *not* guarantee about V-addresses.

**R11 (V-address instability of unmoved content).** V-space addresses of content that was not moved are not guaranteed to remain stable after REARRANGE. In the 4-cut case with unequal region widths, content between the two swapped regions shifts by the width difference:

For SWAP(d, a, b, c, e) with w₁ = b - a ≠ w₃ = e - c, the middle region [b, c) shifts by w₃ - w₁. Only content outside the entire affected range [a, e) retains its V-addresses.

In the 3-cut case, the situation is more favorable: since both swapped regions and the "middle" (which does not exist in a 3-cut) are contiguous, content outside [a, c) retains its V-addresses. But within [a, c), every position changes.

| Case | Content outside affected range | Content inside affected range |
|------|-------------------------------|-------------------------------|
| 3-cut, outside [a, c) | V-address stable | — |
| 3-cut, inside [a, c) | — | V-address changes |
| 4-cut, outside [a, e) | V-address stable | — |
| 4-cut, inside [a, e) | — | V-address changes (including middle if w₁ ≠ w₃) |

This is by design. Nelson built two address spaces precisely so that one could be mutable while the other is permanent. "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." V-space is the mutable face presented to the reader. I-space is the permanent substrate. The instability of V-addresses is the *point* of the separation, not a defect.


## The cutting mechanism

We must address what happens when a cut point falls in the interior of a contiguous span in the arrangement.

A document's arrangement is stored as a set of mapping entries, each covering a contiguous range of positions. A cut point may fall exactly on the boundary between two entries, or it may fall strictly inside one entry's range.

**R12 (Cut-point splitting).** When a REARRANGE cut point falls strictly inside the range of a single mapping entry, that entry must be split into two entries: one covering positions before the cut, the other covering positions from the cut onward. Both entries reference the same underlying I-addresses as the original:

Let entry E cover V-range [v₁, v₂) mapping to I-range [i₁, i₂). If cut point k falls at v₁ < k < v₂, then after splitting:

  - E₁ covers [v₁, k) mapping to [i₁, i₁ + (k - v₁))
  - E₂ covers [k, v₂) mapping to [i₁ + (k - v₁), i₂)

The I-addresses are partitioned between the two halves. No I-addresses are created or destroyed. The provenance metadata (home document, origin context) is copied identically to both halves.

When the cut point falls exactly on an existing entry boundary, no split is needed — the entries already align with the cut.

Gregory confirms both cases from the implementation. The cut machinery tests whether each cut point falls strictly inside, on the left boundary, on the right boundary, to the left, or to the right of each entry. The split function fires only for the strictly-inside case. It creates a new entry, divides the V-width at the cut point, copies all metadata including the home-document association, and inserts the new entry as a sibling. The machinery is shared with DELETE — both operations need the same cut-at-a-point capability.

**A consequence of splitting.** After REARRANGE, the number of mapping entries may be greater than before, because cuts that split entries are never retroactively fused. The fragments created at cut boundaries persist as separate entries. The system has no merge step that detects adjacent entries with contiguous I-addresses and fuses them.

This means that repeated rearrangements accumulate entry fragments. Each rearrangement can split entries at its cut points, and no operation reverses the fragmentation. The abstract specification does not require fusion — the fragmentation has no semantic effect (the same I-addresses are referenced, the same V-positions are covered) — but it does have a structural cost that accumulates over time.

**R13 (Fragment accumulation).** Let n₀ be the number of mapping entries in poom(d) before REARRANGE, and let k be the number of cut points that fall strictly inside existing entries. Then:

  `n' ≤ n₀ + k`

Each interior cut adds at most one entry (by splitting one into two). No entries are removed. The bound is tight — every interior cut produces a split.


## REARRANGE as the unique identity-preserving relocation

We can now state the theorem that justifies REARRANGE's existence as a primitive.

**Theorem (Unique identity-preserving relocation).** REARRANGE is the only edit operation that relocates content in V-space while preserving the I-address of every relocated byte.

*Proof by elimination.* Consider the edit operations:

- **INSERT**: Creates fresh I-addresses (by INS1: `S ∩ dom.ispace = ∅`). Cannot preserve existing I-addresses at new positions because it does not move existing content — it adds new content.
- **DELETE**: Removes V→I mappings. Does not relocate; the surviving content that shifts leftward retains its I-addresses, but the deleted content exits the document's V-space entirely.
- **COPY (transclusion)**: Adds a new V→I mapping to a *different* document. Does not relocate within a single document — it duplicates a reference. Combined with DELETE of the source, the destination retains the I-addresses but the source loses them.
- **REARRANGE**: By R2, applies a bijective permutation to V-positions while preserving V→I mappings (each position's I-address is unchanged). Content moves in V-space; I-addresses are invariant. ∎

This is the formal basis for Nelson's architectural decision to include REARRANGE as a primitive. Without it, there is no way to reorder content within a document while maintaining the network of links, transclusions, and version correspondences anchored to that content's I-space identity.


## Preconditions

We collect the preconditions that must hold for REARRANGE to be well-defined.

**PRE-R0 (Document existence and ownership).** The document must exist and the requesting user must be its owner.

**PRE-R1 (Subspace confinement).** All cut points must lie within the same V-subspace. (Stated above, with justification from implementation evidence.)

**PRE-R2 (Cut point ordering).** Cut points must be in strictly ascending V-order within the document's occupied range:

  For 3-cut: `a < b < c`, all in `dom.poom(d)`.
  For 4-cut: `a < b ≤ c < d`, all in `dom.poom(d)`.

The implementation sorts cut points before processing, so the input order is irrelevant — but the values must be distinct (except b = c in the 4-cut degenerate case) and must reference positions within the document.

**PRE-R3 (Non-degenerate regions).** At least one swapped region must be non-empty. If both regions are empty (a = b and c = d in the 4-cut case, or a = b = c in the 3-cut), the operation is the identity and we do not consider it.


## The 4-cut unequal-width boundary condition

Gregory's evidence reveals a boundary condition that the specification must acknowledge.

In the 4-cut case, when the two swapped regions have unequal widths (w₁ ≠ w₃), the middle region [b, c) shifts by w₃ - w₁. We showed above that the permutation is well-defined and the total extent is preserved. But the implementation applies this offset by pure tumbler arithmetic with no validation of the resulting address space.

For the specification, we observe that the permutation π maps `dom.poom(d)` to itself bijectively, regardless of whether w₁ = w₃. The abstract behavior is correct: every V-position receives content, every I-address is placed, and the multiset is preserved. The boundary condition manifests only at the implementation level — the issue is whether the implementation's arithmetic (which adds signed offsets to stored displacements) produces the correct abstract result in all cases.

We state the abstract requirement without implementation qualification:

**R14 (Total extent preservation).** The occupied range of document d's V-space has the same total width before and after REARRANGE:

  `|dom.poom'(d)| = |dom.poom(d)|`

This follows from R2 (bijective permutation) but is worth stating independently: REARRANGE cannot create gaps in V-space or extend its boundaries. The same positions are occupied, in a different order.


## Summary of the specification

We have established that REARRANGE is characterized by five core properties:

1. **R0 (I-space frame):** I-space is completely unchanged — no allocations, no modifications.
2. **R1 (Content multiset invariance):** The same I-addresses are referenced, in the same quantities.
3. **R2 (Bijective permutation):** The V-space transformation is a bijection preserving V→I mappings.
4. **R3–R6 (Frame conditions):** Span index, other documents, links, other subspaces — all unchanged.
5. **R10 (Atomicity):** No intermediate state with absent content.

From these, every consequence follows by calculation: link survivability (from R1 + R5), provenance immutability (from R0 + R7), transclusion isolation (from R4 + R0), correspondence completeness (from R1), and the fundamental distinction from DELETE+INSERT (from R0, specifically the no-allocation clause).

REARRANGE is the purest expression of the I-space/V-space separation. It is the operation that changes *only* the arrangement — the virtual — while leaving *everything* permanent untouched. In Nelson's image, it is reordering the reading list without moving the books on the shelves.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| R0 | `dom.ispace' = dom.ispace ∧ (A a : a ∈ dom.ispace : ispace'.a = ispace.a)` — REARRANGE does not modify I-space and allocates no fresh addresses | introduced |
| R1 | `img(poom'(d)) = img(poom(d))` — the multiset of I-addresses referenced by the rearranged document is unchanged | introduced |
| R2 | There exists a bijection π on `dom.poom(d)` such that `poom'(d).(π(p)) = poom(d).p` — rearrangement is a position permutation preserving V→I mappings | introduced |
| R3 | `spanindex' = spanindex` — the span index is strictly unchanged (not merely monotone) | introduced |
| R4 | `(A d' ≠ d : poom'(d') = poom(d'))` — cross-document isolation | introduced |
| R5 | `(A L ∈ links : L ∈ links' ∧ endsets'(L) = endsets(L))` — link structures are unchanged | introduced |
| R6 | Positions in subspaces other than the one containing the cut points are unchanged | introduced |
| R7 | `(A a : provenance'(a) = provenance(a))` — provenance is invariant under rearrangement | introduced |
| R8 | Version comparison between pre- and post-rearrangement states yields complete correspondence | introduced |
| R9 | REARRANGE is the unique edit operation with zero loss of shared content under version comparison | introduced |
| R10 | REARRANGE transitions between well-formed arrangements with no intermediate state where content is absent | introduced |
| R11 | V-addresses of content outside the affected range are stable; within the range, they may change | introduced |
| R12 | Cut points falling inside a mapping entry split it into two entries preserving all I-address and metadata | introduced |
| R13 | `n' ≤ n₀ + k` — mapping entry count may increase by the number of interior cuts, with no subsequent fusion | introduced |
| R14 | `\|dom.poom'(d)\| = \|dom.poom(d)\|` — total extent of V-space is preserved | introduced |
| S0 | DELETE+INSERT of same character values produces `img(poom'(d)) ≠ img(poom(d))` — I-address multiset changes | introduced |
| S1 | REARRANGE preserves `img(poom'(d)) = img(poom(d))` — I-address multiset is invariant | introduced |
| L0 | The set of I-addresses resolvable through a link endset in the rearranged document is unchanged | introduced |
| L1 | A single contiguous I-span in a link endset may resolve as multiple disjoint V-spans after rearrangement; count bounded by number of I-addresses | introduced |
| PRE-R1 | All cut points must lie within the same V-subspace | introduced |
| PRE-R2 | Cut points must be in strictly ascending V-order within the document's occupied range | introduced |
| PRE-R3 | At least one swapped region must be non-empty | introduced |


## Open Questions

- Must a conforming system provide REARRANGE as a primitive, or may it offer only DELETE and COPY-back as an identity-preserving relocation mechanism?
- What must a system guarantee about the maximum entry fragmentation after a sequence of rearrangements — is there a bound on structural cost?
- What invariants must hold when a link endset straddles a rearrangement cut point and the resulting V-spans become non-contiguous?
- Must version history record REARRANGE as semantically distinct from other operations, or is the distinction recoverable from I-address analysis alone?
- What must REARRANGE guarantee about the ordering of content within each swapped region — must internal order be preserved, or is arbitrary permutation within a region permitted?
- When two documents transclude overlapping I-address ranges and both perform independent rearrangements, what must the system guarantee about their combined version comparison?
- What must the system provide for reversing a rearrangement — is REARRANGE its own inverse in the sense that REARRANGE(π) followed by REARRANGE(π⁻¹) restores the original V-space exactly?
- Under what conditions may the accumulated entry fragments from repeated rearrangements affect the correctness (not merely the cost) of subsequent operations?
