# ASN-0020: Allocation Order Invariants

*2026-02-25*

## The Question

What must the system guarantee about the relationship between the temporal order in which content is allocated and its spatial position in V-space? Must allocation order correspond to document order?

We are looking for the invariants that separate *when content came into being* from *where a reader encounters it*. The question sounds simple — surely content appears in the order it was created? — but the answer turns out to be architecturally decisive. The two orderings are not merely "allowed" to differ; their independence is the central structural commitment from which permanence, link survivability, version comparison, and non-destructive editing all flow. We must state precisely what IS guaranteed about allocation order, what is NOT, and why the negative answer is as important as the positive one.


## The State

We need two address spaces and a mapping between them. Let system state Σ contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr ⇀ Content`. The permanent store. Append-only: once an address enters `dom.ispace`, it remains forever and its content never changes.
- **poom(d)**: for each document d, a total function from virtual positions to addresses, `poom(d) : Pos → Addr`. The document's current arrangement — which content appears at which virtual position.
- **frontier(d)**: for each document d, the allocation frontier — the next available I-address for fresh content in d. Monotonically advancing.

We write `dom.ispace` for the set of allocated addresses, `ispace.a` for the content at address a, `poom(d).p` for the I-address that document d maps virtual position p to, and `#poom(d)` for the width of d's V-space. Primed names denote the state after an operation.

Two orderings arise from this state:

- **I-order within a document d**: the total order on I-addresses allocated by d, given by the tumbler ordering on `{a : a was allocated by d}`. Because allocation is append-only, this ordering coincides with temporal sequence.
- **V-order of document d**: the total order on V-positions `1 ≤ p ≤ #poom(d)`, which is the order in which a reader encounters content.

The question of this ASN is: must V-order agree with I-order? We shall show that it must not — and that the system's deepest guarantees depend on this freedom.


## The Independence Theorem

We state the central property first, then derive it from the design.

**A0 (Allocation-Arrangement Independence).** There exists no invariant of the system relating the V-order of a document's content to the I-order of that content's allocation. Formally, for any document d and any bijection σ on `{1, ..., #poom(d)}`, there exists a reachable state in which the V→I mapping satisfies:

  `(A p : 1 ≤ p ≤ #poom(d) : poom(d).p = poom(d₀).(σ(p)))`

where d₀ is some reference arrangement of the same content. Every permutation of content within V-space is reachable.

This is not a mere absence-of-constraint. It is a *design principle*. Nelson states it at multiple levels of the architecture:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

If no arrangement is a priori better, then chronological order has no privileged status among arrangements. A0 is the formal expression of this philosophical commitment.


## Why Independence Must Hold: The Operations

We establish A0 constructively by exhibiting the operations that produce arbitrary V→I arrangements. Three distinct mechanisms break any supposed correspondence between allocation order and document order.

### Mechanism 1: INSERT at Arbitrary Position

INSERT places new content at any V-position the user chooses. Nelson's specification:

> "This inserts ⟨text set⟩ in document ⟨doc id⟩ at ⟨doc vsa⟩. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The parameter `⟨doc vsa⟩` is the user's chosen insertion point — determined by editorial intent, not by allocation time. Content created at noon can be inserted before content created at 9am, simply by choosing a V-position that precedes the earlier content.

More precisely: consider two insertions at the same V-position. INSERT "A" at V:1, then INSERT "B" at V:1. The second insertion shifts "A" to V:2. Now "B" (allocated later, higher I-address) precedes "A" (allocated earlier, lower I-address) in V-space. This is the LIFO inversion — every insertion at a non-final position produces it.

Gregory confirms the mechanism: `makegappm` in the insertion path classifies every existing entry and shifts those at or after the insertion point rightward by adding the inserted width to their V-displacement. The newly allocated I-address (always at the frontier, always higher than all prior allocations) is placed at the caller-specified V-position. The implementation imposes no constraint requiring the new I-address to appear at a V-position consistent with its allocation order.

### Mechanism 2: REARRANGE

REARRANGE is a pure V-space permutation. Nelson:

> "Rearrange transposes two regions of text." [LM 4/67]

The operation modifies only V-displacements. I-addresses are untouched. If content was in I-order before REARRANGE, it may be in any permutation of I-order after. Gregory confirms at the implementation level: the rearrange code path modifies only `cdsp.dsas[V]` (the V-dimension displacement) and never touches `cdsp.dsas[I]` (the I-dimension displacement). The multiset of I-addresses is invariant across REARRANGE.

REARRANGE is the most general inversion mechanism: starting from any arrangement, PIVOT can produce any adjacent transposition, and a sequence of adjacent transpositions generates the full symmetric group. Every permutation of I-addresses within V-space is reachable by REARRANGE alone.

### Mechanism 3: COPY (Transclusion)

COPY places content from any document at any V-position in the target document:

> "The material determined by ⟨spec set⟩ is copied to the document determined by ⟨doc id⟩ at the address determined by ⟨doc vsa⟩." [LM 4/67]

COPY reuses existing I-addresses — it does not allocate fresh ones. Content originally allocated in document A at time t₁ can appear at any V-position in document B, regardless of when the COPY occurs or what I-addresses B has already allocated. The user specifies the V-position; the system supplies the I-addresses from the source.

Gregory reveals an additional subtlety: COPY propagates existing inversions. When `specset2ispanset` traverses source content, it returns I-spans in source-V-order. If the source already has inversions (from prior LIFO INSERT or REARRANGE), the retrieved I-spans will be in the inverted order, and COPY deposits them in that same order at the destination. Inversions are transitive through COPY.

These three mechanisms — INSERT at position, REARRANGE, and COPY — each independently break any correspondence between allocation order and document order. Together, they make A0 trivially reachable.


## What IS Guaranteed About Allocation Order

Independence does not mean allocation order is meaningless. Several properties of allocation order are invariant and critical to the system's guarantees.

### I-Space Monotonicity

**A1 (I-Monotonicity).** Within a single document d, content allocated later receives a strictly higher I-address:

  `(A a, b : allocated_by(d, a) ∧ allocated_by(d, b) ∧ time(a) < time(b) : a < b)`

where `<` is the tumbler ordering on I-addresses within d's element subspace.

Nelson grounds this in the append-only storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The word "chronologically" is the key. I-space is ordered by time of creation. Each INSERT allocates the next address beyond the current frontier. The frontier advances monotonically; no mechanism exists to allocate below it.

Gregory confirms that `findpreviousisagr` locates the current maximum I-address in the document, and the next allocation increments beyond it. Deleted I-addresses (addresses whose V-mapping has been removed) are never reused — the frontier only advances.

**A2 (Frontier Monotonicity).** The allocation frontier for document d only advances:

  `frontier'(d) ≥ frontier(d)`

with equality only when no content is allocated. INSERT increases the frontier by the width of the inserted content. DELETE, REARRANGE, and COPY leave it unchanged (DELETE removes V-mappings without affecting I-space; REARRANGE permutes V-space; COPY reuses existing I-addresses).

### I-Space Immutability

**A3 (I-Address Immutability).** Once content is allocated at an I-address, neither the address nor its content ever changes:

  `(A a : a ∈ dom.ispace : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`

This is stronger than merely "append-only." It means no operation — INSERT, DELETE, REARRANGE, COPY, or any combination — can alter the content at an existing I-address or remove an I-address from the space. The I-addresses allocated by a document are permanent witnesses to what was created and when.

Gregory confirms this at the deepest level: REARRANGE never touches I-displacements in POOM entries. INSERT allocates fresh I-addresses without modifying any existing ones. DELETE removes V-mappings but leaves I-space entirely untouched. COPY creates new V→I mappings to existing I-addresses without modifying those addresses.

### No I-Address Reuse

**A4 (No Reuse).** An I-address, once allocated, is never reassigned to different content, even after the V-mapping referencing it is deleted:

  `(A a, t₁, t₂ : allocated(a, t₁) ∧ allocated(a, t₂) : t₁ = t₂)`

Each I-address is allocated exactly once. DELETE removes the V→I mapping, not the I-space content. A subsequent INSERT at the same V-position allocates a fresh I-address beyond the frontier, never the address of the deleted content. Gregory confirms this: after DELETE at V:1.2, the granfilade retains the original I-address; the next INSERT calls `findpreviousisagr`, finds the highest existing I-address, and increments past it.

This property interacts with A0 in a critical way. Because the V→I mapping is free to place any I-address at any V-position, and because deleted I-addresses are never recycled, the system accumulates a growing collection of permanent content from which any arrangement can be assembled. The freedom of V-space and the permanence of I-space are complementary.


## The Two Spaces Are Architecturally Separate

We now make explicit what the independence property and the allocation guarantees together entail. The system maintains two fundamentally distinct orderings, and the document IS the mapping between them.

**A5 (Dual Ordering).** The system state for a document d consists of:

  (i) An I-ordering: the total order on I-addresses allocated by d, which coincides with temporal allocation order (by A1).
  (ii) A V-ordering: the total order on V-positions `1, ..., #poom(d)`, which is the document's current reading order.
  (iii) A mapping `poom(d)` from (ii) to (i) that may be any injection (or, in the presence of transclusion, any function — the same I-address may appear at multiple V-positions).

Nelson states this separation as the architectural foundation:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

Users work entirely in V-space. I-space is invisible to the front end. The mapping is the document.

**A6 (V-Space Contiguity).** After every operation, V-space is dense — there are no gaps:

  `poom(d) is a total function on {1, ..., #poom(d)}`

INSERT at position p shifts all positions ≥ p rightward by the inserted width. DELETE at position p shifts all positions > p leftward by the deleted width. REARRANGE permutes positions without changing the domain. The V-space is always a contiguous sequence of positions, regardless of how fragmented the corresponding I-addresses may be.

This means a contiguous V-span may map to arbitrarily many non-contiguous I-spans. Gregory confirms that `vspanset2sporglset` splits at every I-address discontinuity: a V-span covering content from N distinct temporal insertions produces N separate I-spans (sporgls). The result is ordered by V-position, not by I-address — the V-ordering is the document ordering, and it bears no necessary relationship to the I-ordering.


## Temporal Sequence Must Remain Recoverable

A0 tells us that V-order need not reflect I-order. But the converse question is equally important: must the system preserve enough information to *reconstruct* the temporal allocation sequence, even when the document presents content in a completely different reading order?

The answer is yes, and it follows from the architecture itself rather than from any additional mechanism.

**A7 (Temporal Recoverability).** The temporal sequence of allocations within a document d is recoverable from the I-space address ordering:

  `(A a, b : allocated_by(d, a) ∧ allocated_by(d, b) : time(a) < time(b) ≡ a < b)`

By A1, I-addresses are assigned in temporal order. By A3, I-addresses are immutable. Therefore the I-address ordering IS the temporal record. There is nothing to "preserve" as a separate datum — the information is structurally present in the I-space itself.

Nelson makes this explicit:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

This statement is subtle. Absolute wall-clock time is metadata tracked alongside the structure. But *relative* temporal sequence — what was allocated before what, within a single document — is encoded in the I-space address ordering itself. The append-only model guarantees this: if byte a has a lower I-address than byte b in the same document, a was allocated first. This is not metadata; it is structural.

### Why Recoverability Matters

Five guarantees depend on A7 — on the ability to distinguish temporal allocation order from current arrangement:

**Historical backtrack.** "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15] Reconstructing a prior version requires knowing which allocations existed at that time. By A7, the I-address ordering answers this: all addresses below a given frontier value existed at the time that frontier was current.

**Link survivability.** Links point to I-addresses, not V-positions. "A Xanadu link is not between points, but between spans of data... it means that links can survive editing." [LM 4/42] When a document is rearranged, V-positions shift but I-addresses do not. The link's reference remains valid regardless of V-ordering — precisely because it was never tied to V-ordering in the first place.

**Version correspondence.** SHOWRELATIONOF2VERSIONS identifies matching parts across versions by shared I-space origin. "A facility that holds multiple versions is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20] The algorithm intersects I-spans from both versions. V-ordering is irrelevant — the I-address identity is the stable reference frame.

Gregory confirms this concretely: `compare_versions` converts both documents' V-spans to I-spans, then intersects them pairwise. The intersection is purely I-address range overlap — V-address proximity plays no role. A sequence INSERT "ABC", DELETE "B", INSERT "XY" at the gap produces "A" and "C" at non-contiguous I-addresses with "XY" at higher I-addresses between them in the V-stream. The comparison correctly identifies the shared "A" and "C" spans because the I-address ranges overlap with the original, regardless of the gap.

**Origin traceability.** "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40] The I-address encodes provenance — which server, which account, which document. This encoding is permanent by A3 and independent of arrangement by A0.

**Link discovery across rearrangement.** When content is rearranged in V-space, links to that content must remain discoverable. Gregory traces the full chain: `find_links` converts the V-span query to I-addresses via the current POOM, then searches the link index (spanfilade) by I-address. The spanfilade contains no V-coordinates whatsoever. After any number of rearrangements, the POOM correctly maps the new V-locations back to their stable I-addresses, and the link lookup proceeds entirely in I-space.


## Cross-Document Independence

Within a single document, allocation is monotonic (A1). But across documents, the situation is entirely different.

**A8 (Cross-Document Allocation Independence).** Allocations in different documents impose no ordering constraints on each other:

  `(A d₁, d₂, a, b : d₁ ≠ d₂ ∧ allocated_by(d₁, a) ∧ allocated_by(d₂, b) : a < b ∨ a > b ∨ a ∥ b)`

where `a ∥ b` denotes that a and b are incomparable in the tumbler ordering (they lie in different subtrees of the address tree).

Nelson grounds this in the "owned numbers" allocation model:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

Alice allocates I-space addresses under her subtree. Bob allocates under his. Neither needs to know the other exists. There is no global clock, no global sequence number, no coordination.

The tumbler line does impose a total order on all tumblers, but this ordering reflects tree structure, not temporal sequence. Nelson:

> "In a sense the tumbler line is like the real line... But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

Account 1 comes "before" account 2 on the tumbler line because `1 < 2` in the tree — not because account 1 was created first. Moreover, forking breaks even this structural monotonicity: creating a sub-digit under `2.4` at time T₃ produces an address that sits between `2.4` and `2.5` on the tumbler line, even if `2.5` was created at T₂ < T₃.

**A9 (No Global Monotonicity).** The permanent address space does NOT grow monotonically with time at the global level:

  `¬(A a, b : time(a) < time(b) : a < b)`

This is a direct consequence of the forking mechanism. Within a single sibling sequence under the same parent, allocations are monotonic. But children appear between their parent and the parent's next sibling, so a later allocation can occupy a lower position on the tumbler line than an earlier allocation in a different branch.

This negative property is as important as the positive ones. A system that required global monotonicity would need a global allocation coordinator — violating the distributed, owner-sovereign allocation model that Nelson designed.


## The Compound Document Model

The independence of allocation order from document order is most vivid in Nelson's vision of compound documents — documents assembled from content originating at different times, in different documents, by different authors.

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

A compound document may present Shakespeare's 1600 text followed by a 2024 annotation followed by a 1985 commentary. The V-ordering reflects *literary intent*, not the temporal sequence 1600 → 1985 → 2024 in which the content was created. The I-addresses faithfully record who created what and when; the V-space presents it in whatever order serves the reader.

Nelson's glass pane metaphor reinforces the point:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The author paints and windows wherever they choose. The arrangement reflects the author's compositional decisions, not the temporal sequence of the referenced content. V-space is the author's canvas; I-space is the library of permanent materials from which the canvas is assembled.


## Frame Conditions for Each Operation

We now catalog how each editing operation interacts with allocation order. For each operation, we state what it does to I-order, what it does to V-order, and what it does to the relationship between them.

### INSERT(d, p, content)

Allocates fresh I-addresses starting at `frontier(d)`, places them at V-position p.

**Effect on I-order:** Extends it. New addresses are strictly above all existing addresses of d (by A1). `frontier'(d) = frontier(d) + |content|`.

**Effect on V-order:** Shifts positions ≥ p rightward by |content|. Inserts the new content at positions p through p + |content| - 1.

**Effect on allocation-arrangement relationship:** Creates a new inversion whenever p < #poom(d) + 1. The fresh I-addresses (highest in I-order) appear at V-position p (not necessarily highest in V-order). The LIFO pattern — insert at the same position twice — guarantees that the later allocation precedes the earlier one in V-space.

**Frame:** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. All existing I-addresses and their content are unchanged. All existing V→I mappings are preserved — only their V-positions are shifted: `(A q : q ≥ p : poom'(d).(q + |content|) = poom(d).q)`.

### DELETE(d, p, w)

Removes V-positions p through p + w - 1 from d's arrangement.

**Effect on I-order:** None. I-space is entirely unchanged. `dom.ispace' = dom.ispace`, `frontier'(d) = frontier(d)`.

**Effect on V-order:** Shifts positions > p + w - 1 leftward by w. The V-space shrinks by w positions.

**Effect on allocation-arrangement relationship:** The deleted I-addresses persist in I-space (by A3) but are no longer mapped by any V-position in d. If those addresses had lower I-values than surrounding content, the gap in I-order within the remaining V-space may become wider. But no new inversions are created — the relative I-order of the remaining V-mapped content is unchanged.

**Frame:** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. No I-address is removed from the global space. The deleted addresses are recoverable — they persist at their original I-addresses.

### REARRANGE(d, cuts)

Permutes V-positions within d according to the cut specification.

**Effect on I-order:** None. No I-address is created, modified, or removed. `dom.ispace' = dom.ispace`, `frontier'(d) = frontier(d)`.

**Effect on V-order:** The content at each V-position is permuted. The domain of `poom(d)` is unchanged (same positions exist); only the values change.

**Effect on allocation-arrangement relationship:** REARRANGE is the most powerful inversion mechanism. By permuting V-space arbitrarily while leaving I-space fixed, it can produce any degree of disagreement between V-order and I-order. After REARRANGE, the multiset of I-addresses in the V-space is identical to what it was before — `img(poom'(d)) = img(poom(d))` as multisets — but the order may be completely reversed.

**Frame:** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)` and `img(poom'(d)) = img(poom(d))`. The span index and link index are untouched.

### COPY(d_src, v_range, d_tgt, p)

Creates V→I mappings in d_tgt pointing to I-addresses from d_src.

**Effect on I-order:** None for d_tgt's own I-space allocations. No fresh I-addresses are allocated. `frontier'(d_tgt) = frontier(d_tgt)`.

**Effect on V-order:** Inserts the transcluded content at V-position p in d_tgt, shifting existing positions rightward.

**Effect on allocation-arrangement relationship:** COPY creates the most dramatic inversions. Content allocated in d_src (possibly decades ago, with very low I-addresses) can appear at any V-position in d_tgt, interleaved with locally-allocated content (high I-addresses). The resulting V→I mapping may juxtapose wildly different I-address ranges.

Gregory traces the mechanism: `insertpm` pairs source I-addresses with caller-specified V-positions unconditionally. There is no constraint forcing I-addresses to be monotonically aligned with V-addresses. Self-transclusion (COPY from a document to itself) is also valid, producing the same I-address at multiple V-positions simultaneously.

**Frame:** `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`. Source document's POOM is unchanged: `poom'(d_src) = poom(d_src)`.


## The POOM as a Non-Identity Permutation

We can now characterize the POOM precisely. Each document's POOM is a 2D structure mapping V-positions to I-addresses. After an arbitrary sequence of operations, the V→I mapping is, in general, a non-identity permutation: V-order may be any rearrangement of I-order. In the presence of COPY, it is not even a permutation — it is a general function, since the same I-address may appear at multiple V-positions.

**A10 (POOM Generality).** The V→I mapping `poom(d)` for a document d may be any function from `{1, ..., #poom(d)}` to `dom.ispace`:

  (i) The function need not be injective (COPY can map multiple V-positions to the same I-address).
  (ii) The function need not be order-preserving (INSERT, REARRANGE, and COPY all create inversions).
  (iii) The function need not map to contiguous I-addresses (the image may have arbitrarily many gaps).

The only constraint is that `img(poom(d)) ⊆ dom.ispace` — the I-addresses must actually exist.

### The Retrieval Consequence

This generality imposes a requirement on retrieval: content must be returned in V-order, not I-order. Gregory confirms that the retrieval path uses explicit insertion-sort by V-address (`incontextlistnd` sorts by `totaloffset.dsas[V]`). The sort is unconditional — it does not assume or exploit any relationship between V-order and I-order. Even when the tree traversal encounters entries in an order that reflects neither V nor I (due to the diagonal-sum rebalancing heuristic in the tree structure), the insertion-sort re-establishes V-order in the result.

**A11 (V-Ordered Retrieval).** Retrieval of document content returns spans in V-position order:

  `(A j, k : 0 ≤ j < k < |result| : result.j.vstart ≤ result.k.vstart)`

This ordering is independent of the I-addresses of the spans, independent of the internal tree structure, and independent of the order in which spans were allocated. The retrieval mechanism must actively impose V-ordering; it cannot rely on any correlation with I-ordering.


## The Coalescing Invariant

One implementation concern surfaces that has abstract significance: when should two adjacent entries in the V→I mapping be merged into a single entry?

**A12 (Coalescing Condition).** Two V→I mapping entries may be coalesced into one if and only if they are contiguous in BOTH V-space AND I-space AND share the same provenance:

  Let entry₁ map V-range [v₁, v₁ + w) to I-range [i₁, i₁ + w), and entry₂ map V-range [v₁ + w, v₁ + 2w') to I-range [i₂, i₂ + w'). Coalescing is valid iff:
  (i) V-contiguity: `v₁ + w = v₂` (the V-ranges are adjacent)
  (ii) I-contiguity: `i₁ + w = i₂` (the I-ranges are adjacent)
  (iii) Same provenance: the two entries originate from the same source document

Failure of any condition requires separate entries.

Gregory confirms that the coalescing check in the implementation compares both dimensions simultaneously. For a POOM with `dspsize = 2`, the check iterates over all dimensions and requires equality in each. Placing I-address-contiguous content at a non-adjacent V-position (condition i fails) does not coalesce. Placing V-adjacent content from non-contiguous I-addresses (condition ii fails) does not coalesce. Merging entries from different source documents (condition iii fails) does not coalesce.

This property is abstract because any implementation that coalesces based on only one dimension would corrupt the V→I mapping — a single merged entry would falsely claim that a contiguous V-range maps to a contiguous I-range when it does not.


## The Cross-Space Lookup Guarantee

The independence of V-order from I-order means that operations which need to cross between the two orderings must work without any ordering assumption. We state the abstract requirement.

**A13 (Cross-Space Query Correctness).** For any document d:

  (i) **V→I mapping:** Given a V-span [v₁, v₂), the system returns the (possibly non-contiguous) set of I-spans to which those V-positions map, in V-order.
  (ii) **I→V mapping:** Given an I-span [i₁, i₂), the system returns the set of V-spans at which that I-range currently appears in d, regardless of how many V-positions map to those I-addresses or in what V-order they appear.

Both lookups are correct after any sequence of INSERT, DELETE, REARRANGE, and COPY operations. Neither assumes monotonic alignment between V and I.

Gregory's evidence is emphatic on this point: the V→I and I→V lookups in the implementation use independent dimension parameters. The sort dimension for the result list is specified by the caller. For V→I queries, the result is V-sorted; for I→V queries, the result is I-sorted. Neither sort depends on the other dimension's ordering. The lookup functions operate correctly even when V-order and I-order are completely reversed.


## Summary of the Two Orderings

We collect the properties into a table.

| Aspect | I-Order | V-Order | Relationship |
|--------|---------|---------|-------------|
| Determined by | Allocation time (A1) | Editorial choice (A0) | Independent (A0) |
| Mutability | Immutable (A3) | Freely mutable | I-order is permanent reference frame |
| Monotonicity | Within-document: yes (A1) | N/A — positions are dense by A6 | No monotonic correspondence |
| Cross-document | No ordering (A8) | Each document independent | Doubly independent |
| Recoverability | Self-recovering from addresses (A7) | From snapshot/version | I-order recoverable at any time |
| Gaps | None within a document's allocations | None (A6 — dense) | V-contiguous spans may have I-gaps |
| Retrieval order | By I-address for I-queries | By V-position for V-queries (A11) | Each ordering independent of the other |


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| A0 | Allocation-Arrangement Independence: no invariant constrains V-order relative to I-order; every permutation of content within V-space is reachable | introduced |
| A1 | I-Monotonicity: within a single document, later allocations receive strictly higher I-addresses | introduced |
| A2 | Frontier Monotonicity: the allocation frontier for each document only advances | introduced |
| A3 | I-Address Immutability: once content is allocated at an I-address, neither address nor content ever changes | introduced |
| A4 | No Reuse: each I-address is allocated exactly once; deleted addresses are never recycled | introduced |
| A5 | Dual Ordering: the system maintains I-ordering (temporal) and V-ordering (editorial) as architecturally separate structures | introduced |
| A6 | V-Space Contiguity: after every operation, V-space is dense with no gaps | introduced |
| A7 | Temporal Recoverability: the temporal allocation sequence within a document is recoverable from I-address ordering | introduced |
| A8 | Cross-Document Allocation Independence: allocations in different documents impose no ordering constraints on each other | introduced |
| A9 | No Global Monotonicity: the global address space does not grow monotonically with time due to the forking mechanism | introduced |
| A10 | POOM Generality: the V→I mapping may be any function — not necessarily injective, not order-preserving, with arbitrarily non-contiguous image | introduced |
| A11 | V-Ordered Retrieval: retrieval of document content returns spans in V-position order, independent of I-address ordering | introduced |
| A12 | Coalescing Condition: V→I mapping entries may be merged only when contiguous in both V and I and sharing provenance | introduced |
| A13 | Cross-Space Query Correctness: V→I and I→V lookups are correct after any operation sequence, assuming no monotonic alignment | introduced |
| Σ.frontier(d) | The monotonically advancing allocation frontier for document d | introduced |


## Open Questions

- What must the system guarantee about allocation order when multiple concurrent users insert into the same document simultaneously?
- Must the frontier for a document be a single value, or can concurrent allocations produce a set of frontier points that must later be reconciled?
- What properties must the version snapshot mechanism satisfy to ensure that A7 (temporal recoverability) composes correctly with version forking?
- When content is transcluded from a document that is later deleted, what must the system guarantee about the persistence of the transcluded content's I-addresses?
- Must the coalescing condition (A12) be an exact conjunction, or can alternative equivalence relations on provenance yield valid coalescings?
- What must the system guarantee about the ordering of link endsets when the content they reference has been rearranged across multiple documents?
- Under what conditions can the cross-space query guarantee (A13) be weakened without losing link survivability or version correspondence?
- What must the relationship between I-order and version derivation order be when a version fork allocates content in the child before the parent has committed?
