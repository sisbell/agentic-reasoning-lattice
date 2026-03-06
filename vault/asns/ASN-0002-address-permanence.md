# ASN-0002: Address Permanence

*2026-02-23*

We wish to understand what the system must guarantee about the stability of addresses. The question is sharp: once content is assigned an address, what may change? The answer, we shall discover, is equally sharp — nothing may change. But the sharpness of the answer conceals a rich internal structure. There are two address spaces with opposite stability contracts, a write-once content store, a write-only historical index, and a collection of editing operations that must be shown to preserve permanence individually. We develop each piece.


## The system state

We need a minimal vocabulary. Let the system state at any moment be Σ, containing at least:

- **ispace**: a partial function from addresses to content, recording what has been stored. `ispace : Addr ⇀ Content`, where `Content = TextContent | LinkStructure`. A `TextContent` value is an atomic unit of text (a character, a byte — the granularity is not material here). A `LinkStructure` value contains endsets, each being a set of **span descriptors** — `(origin, width)` pairs defining contiguous ranges on the tumbler line. Structural metadata — POOM orgls, allocation tree nodes, document identity entries — are not values of type `Content`; they are maintained outside `ispace` in the system's structural index. The domain of `ispace` is partitioned by subspace: addresses in `text_subspace` carry `TextContent` values; addresses in `link_subspace` carry `LinkStructure` values. Each span designates a region `[origin, origin + width)`; it does not enumerate individual addresses. The range a span covers may include addresses not in `dom.ispace` (ghost addresses, unallocated positions). What content a span currently covers is resolved at query time, not stored at creation time.
- **vspace(d)**: for each document d, a partial function from virtual positions to addresses, recording the current arrangement. `vspace(d) : Pos ⇀ Addr`. The domain of `vspace(d)` is finite and changes with operations. Positions are structured: `Pos = Subspace × Nat`, where `Subspace` distinguishes the text subspace (holding content addresses) from the link subspace (holding link addresses). We write `text_subspace` and `link_subspace` for the two values of `Subspace`, and say that position `p` is "in subspace `s`" when `p.subspace = s`.
- **spanindex**: a relation recording which documents have ever contained which address ranges. `spanindex ⊆ Addr × DocId`.

We write `dom.ispace` for the set of addresses at which content is stored, `ispace.a` for the content at address `a`, `dom.vspace(d)` for the set of positions currently mapped in document d, and `#vspace(d)` for the number of entries in document d's virtual stream (i.e., `|dom.vspace(d)|`). We use primed names (Σ', ispace', etc.) for the state after an operation.

We define two derived sets. The set of **links** is the subset of `dom.ispace` in the link subspace:

  `links = {ℓ ∈ dom.ispace : ℓ ∈ link_subspace}`

For each link `ℓ ∈ links`, the function `endsets(ℓ)` extracts the endset span descriptors from `ispace.ℓ` — the link's stored content. Each endset is a set of spans `{(origin₁, width₁), ..., (originₖ, widthₖ)}`. These are derived from `ispace`, not independently maintained. We write `covers(e)` for the set of tumbler-line positions covered by an endset's spans: `covers(e) = (∪ i : 1 ≤ i ≤ k : {a : originᵢ ≤ a < originᵢ + widthᵢ})`. The set `covers(e) ∩ dom.ispace` gives the content addresses currently reachable through the endset — this intersection may change as `dom.ispace` grows, even though the endset itself is immutable (AP1).


## The permanence axiom

We state the central property. It has two parts — one about the set of addresses, one about the content at those addresses:

**AP0 (Address irrevocability).** Once an address enters the domain of ispace, it remains there forever:

  `(A a : a ∈ dom.ispace : a ∈ dom.ispace')`

for every operation that transforms Σ to Σ'. No operation may shrink `dom.ispace`. The set of allocated addresses grows monotonically.

**AP1 (Content immutability).** Once content is stored at an address, it never changes:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

for every operation. The content function is write-once: each address is written exactly once (at allocation) and read forever after.

Nelson states the guarantee directly: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The word "permanent" is not casual. It means the assignment survives all future operations — not for the lifetime of a session or a version, but for the lifetime of the system.

AP0 and AP1 together give us the combined invariant:

**AP (Address permanence).** `(A a : a ∈ dom.ispace : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`.

AP is the conjunction AP0 ∧ AP1. We keep the parts separate because different operations threaten them differently: a deallocation would violate AP0 while leaving AP1 intact for surviving addresses; a mutation would violate AP1 while leaving AP0 intact.

We must be precise about the quantification. AP holds for *every* operation the system may perform. It is not a statistical property or a best-effort guarantee — it is an invariant in the Dijkstra sense: true before every operation, true after every operation, true in every reachable state.


## The freshness obligation

AP tells us what happens to *existing* addresses. We now ask: what constraint governs *new* addresses? If an operation stores new content, it must use an address that has never been used:

**AP2 (Freshness).** Every allocation produces an address not previously in the domain of ispace:

  `(A a : a is allocated by operation op : a ∉ dom.ispace)`

where `dom.ispace` is the domain *before* the operation.

Freshness is the dual of irrevocability. AP0 says old addresses cannot leave; AP2 says new addresses cannot collide with old ones. Together they establish a strict partition of history: at every moment, the domain of ispace is exactly the set of addresses that have *ever* been allocated, and each address maps to the content that was stored at the unique moment of its allocation.

Nelson's storage model makes this inevitable: "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." In an append-only store, new content goes at the end. There is no mechanism for overwriting.

The freshness guarantee has a structural basis. Nelson's forking allocation — "successive new digits to the right; we call these 'under' the previous digit: 2.1, 2.2, 2.3, 2.4 are successive items" — produces addresses by monotonic increment within a partition. The allocation counter only advances; it never retreats. Gregory confirms: the allocation function queries the content store for the highest existing address below a computed upper bound, then increments by one. The function has no concept of "freed" addresses, no free-list, no gap tracking. It sees what exists and goes forward.

A consequence deserves explicit statement:

**AP3 (No reuse).** If address `a` was once in `dom.ispace`, then for all future states, `a` remains in `dom.ispace` with its original content. In particular, the sequence: allocate `a` with content `c₁`; "free" `a` by some means; allocate `a` again with content `c₂ ≠ c₁` — is impossible. No operation performs the first "free," so the second allocation at `a` cannot occur.

AP3 follows from AP0 (a is never removed) and AP2 (new allocations avoid existing addresses). We state it separately because address reuse is the failure mode that would be most catastrophic. Nelson enumerates the consequences: reuse would corrupt links (which would silently point to the wrong content), destroy attribution (the address encodes the creator), falsify correspondence (version comparison relies on shared addresses), sever transclusion (documents sharing content via shared addresses would diverge), and misdirect royalties (payment flows to the address owner).

Gregory provides empirical confirmation. After creating content at addresses `α₁, α₂, α₃`, deleting the content at `α₂` from a document's virtual space, and then inserting new content, the new content receives addresses `α₄, α₅, α₆` — not `α₂`. The address `α₂` remains in the content store, occupying its position in the allocation sequence, affecting the computation of the next address. The deletion removed a *reference* to `α₂`, not the address itself.


## Ghost addresses

Not every address in the system has content stored at it. Nelson describes "ghost elements" — positions on the address line that are logically occupied but have no stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

Ghost addresses matter for AP because links can point to them: "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." A ghost address is not available for reuse. It is a permanent commitment to a position in the address space, even without associated content.

This works precisely because endsets are span descriptors, not sets of individual content addresses. A span `(origin, width)` designates a region on the tumbler line — it does not assert that content exists at every position in the range. Nelson: "A span that contains nothing today may at a later time contain a million documents." A link whose endset span covers a ghost account address embraces the entire subtree rooted there, including every document that exists or will exist under that account. The span is a zone, not an enumeration; ghost addresses fall naturally within zones.

Ghost addresses require their own permanence guarantee, distinct from AP0–AP3. AP0 protects addresses in `dom.ispace`; ghost addresses are explicitly *not* in `dom.ispace`. The question is: what prevents a ghost address — an address range assigned to a server, account, or document — from being reassigned to a different entity?

Nelson's answer is unequivocal. The tumbler line is "an abstract representation of a particular tree" — the actual historical tree of what was created. Reassigning a range would change the tree's structure retroactively. The word "permanent" in "permanent tumbler address" is unconditional — it does not say "permanent as long as content exists." Ghost elements are "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." If a range assigned to account `1.3.0.7` were reassigned to a different entity, any link pointing to that ghost element would now resolve to the wrong entity. The baptism of an address range — "successive new digits to the right" — is a one-way act of creation; Nelson describes no mechanism for un-creation or re-baptism.

The structural necessity is severe. Links point to I-space addresses; reassignment would silently redirect them. Origin traceability is structural — the I-address encodes the creator; reassignment would make it lie. For vendor failure, Nelson specifies orderly transition of content to other Xanadu locations, not reassignment of the address range. The content migrates; the addresses do not change.

We state this as a design requirement:

**AP4a (Range commitment permanence).** The assignment of an address-space range to an entity (server, account, or document) is permanent and irrevocable. Once a range is committed to an entity, that range cannot be reassigned to a different entity, even if the entity contains no stored content.

AP4a is not a formal invariant over Σ — the state model defined in this ASN does not include the range-to-entity mapping (the "allocation tree" that serves as the document registry). We state it as a design-level requirement derived from Nelson's architecture. The allocation tree is structural metadata maintained outside `ispace`: CREATENEWVERSION allocates a position in this tree without creating an `ispace` entry. A formal treatment would extend Σ with an `alloc : Range → Entity` mapping and require `alloc' ⊇ alloc` (monotonic extension, no reassignment). We defer that extension, but the requirement is binding: AP4a protects the structural commitments of the address hierarchy itself, and any operation that modifies the allocation tree must preserve it.

What we also need is a strengthening of AP2:

**AP4 (Monotonic frontier).** The allocation counter within each partition never retreats. If the highest allocated address in partition `p` is `a`, then the next allocation in `p` produces some `a' > a`. Gaps below `a` are permanent.

We must state a structural prerequisite before deriving freshness from AP4. The allocation frontier is maintained *per partition*, but AP2 requires freshness across *all* of `dom.ispace`. The implication holds only because partitions have structurally disjoint address ranges:

**AP4b (Partition disjointness).** The address ranges of distinct subspace partitions are disjoint:

  `text_subspace ∩ link_subspace = ∅`

where `text_subspace` and `link_subspace` denote the sets of addresses structurally assigned to each partition — addresses whose subspace identifier places them in one partition cannot fall in the other's range.

Gregory confirms: text addresses begin with subspace identifier 1, link addresses with identifier 2. The allocation function computes a different upper bound for each subspace and searches below that bound, ensuring that text allocation never finds a link address and vice versa.

With AP4b in hand, AP4 implies AP2: a fresh address produced by partition `p` is above `p`'s frontier, hence disjoint from all existing addresses in `p`; and by AP4b, it is disjoint from all addresses in every other partition. Therefore the fresh address is not in `dom.ispace`. AP4 is strictly stronger than AP2: it also forbids filling gaps. If addresses `α₃` and `α₅` exist in a partition but `α₄` does not, AP4 guarantees that `α₄` will never be filled by a later allocation — the counter has moved past it.

Gregory provides further evidence: when a link operation allocates in one subspace and a subsequent text operation allocates in the text subspace, each subspace maintains its own frontier independently. The link address does not consume text addresses, and text allocation does not fill the gap left by the link's position in the unified address ordering.


## The two-space architecture

We now address the apparent paradox: if addresses are permanent and content is immutable, how does editing work? The answer is that the system maintains two address spaces with opposite stability contracts.

**I-space** (identity space) is the permanent content store, governed by AP0–AP4. An I-space address is the *identity* of a piece of content — it says "which byte this is, forever."

**V-space** (virtual space) is the mutable arrangement layer. A document's V-space is a partial mapping from positions to I-space addresses: `vspace(d) : Pos ⇀ Addr`. V-space positions are ephemeral — they shift with every edit. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing."

The fundamental separation:

**AP5 (Dual-space contract).** The permanence axioms (AP0–AP4) govern I-space. V-space has no permanence guarantee. We restate AP in the dual-space context to make the architectural separation explicit: editing operations do not modify or remove existing entries in I-space; they may only extend `dom.ispace` with fresh addresses:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a) ∧ dom.ispace ⊆ dom.ispace'`

for every editing operation. This is AP (i.e., AP0 ∧ AP1) restated in the vocabulary of the two-space architecture. The formula adds no new content — it is the same invariant, read through the lens of the I-space / V-space separation. Its purpose is notational: when reasoning about editing operations, we cite AP5 to invoke AP in the dual-space context.

We must be precise about what "modify I-space" means. INSERT extends `dom.ispace` with fresh addresses carrying new content. CREATELINK extends `dom.ispace` with a fresh link address. Both operations *add* to I-space — they perform monotonic extension. Neither operation modifies or removes any existing entry. The distinction is between mutation of existing state (forbidden) and growth of the domain (permitted). DELETE, REARRANGE, and COPY do not touch I-space at all. CREATENEWVERSION allocates a document identity outside I-space (see below).

We can now state what "editing" means precisely. An editing operation changes the mapping `vspace(d)` for some document `d`, and may monotonically extend `dom.ispace` with fresh addresses. The mapping may grow (INSERT adds new I-space addresses and maps V-positions to them), shrink (DELETE removes V-positions), or be permuted (REARRANGE changes which V-positions map to which I-addresses). Through all of this, no existing I-space entry is modified or removed.

The library analogy is apt. I-space is the permanent stacks — books on shelves, each at a fixed location, never moved, never removed. V-space is a reading list — an ordered sequence of references to shelf locations. You can reorder your reading list, add references, remove references. The books on the shelves are indifferent to what your reading list says.


## Operation-by-operation analysis

We must verify AP for each operation. The strategy is: for each operation, we state its effect on ispace and show that AP is preserved. We also state its frame conditions — what it does NOT change.

### INSERT

INSERT creates new content and places it in a document.

*Effect on ispace.* INSERT extends `dom.ispace` with fresh addresses carrying new content. Let `a₁, ..., aₙ` be the addresses allocated for the inserted text. Then:

  `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom.ispace ∧ aᵢ ∈ dom.ispace')`

by AP2 (freshness). The fresh addresses `{a₁, ..., aₙ}` are disjoint from `dom.ispace`. INSERT writes content only at these fresh addresses; it contains no instruction that reads or writes any entry of ispace at an address in `dom.ispace`. Therefore no pre-existing entry is modified:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Furthermore, `dom.ispace ⊆ dom.ispace'` because INSERT extends ispace (adding entries at fresh addresses) and contains no removal instruction — no entry of ispace is deleted by the operation.

*Effect on vspace.* INSERT modifies `vspace(d)` for the target document. New V-positions are created mapping to the fresh I-addresses. Existing V-positions at or beyond the insertion point shift forward by the width of the inserted text. Nelson: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

Crucially, the shift is confined to a single subspace within the document. V-positions in the link subspace are not affected by a text insertion:

**AP6 (Subspace isolation under INSERT).** INSERT at a V-position in subspace `s` of document `d` shifts only V-positions in subspace `s` of document `d`. All V-positions in other subspaces of `d`, and all V-positions in all other documents, are unchanged.

Gregory confirms the mechanism: the shift classifies each entry in the document's mapping into three regions using a two-blade boundary. All entries in the insertion subspace at or beyond the insertion point receive an identical shift equal to the insertion width. Entries before the insertion point and entries in other subspaces receive no shift. No entry receives a different shift magnitude — the operation is uniform within its region.

*Boundary case.* INSERT of zero characters (n = 0) allocates no addresses and is a no-op on both I-space and V-space. AP0, AP1, and AP2 are satisfied vacuously — the universal quantifier over the empty set of allocated addresses is trivially true.

*Frame conditions.* INSERT does not affect `ispace` at existing addresses. INSERT does not affect `vspace(d')` for any document `d' ≠ d`. INSERT does not affect the link subspace of document `d`. These are critical: INSERT's blast radius is exactly one subspace of one document's V-space, plus the monotonic extension of I-space.

### DELETE

DELETE removes content from a document's current arrangement.

*Effect on ispace.* **None.** DELETE does not modify ispace in any way. The content remains at its I-space addresses:

  `dom.ispace' = dom.ispace`
  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Nelson is explicit: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

The phrase "not currently addressable" is precise — not addressable through this document's current V-space mapping. The I-space address remains as valid as ever.

*Effect on vspace.* DELETE modifies `vspace(d)` by removing entries and shifting surviving entries leftward. V-positions after the deleted region decrease by the width of the deletion.

*Boundary case.* DELETE of zero characters is a no-op on both I-space and V-space — no V-positions are removed and no shifts occur.

*Frame conditions.* DELETE does not affect ispace. DELETE does not affect `vspace(d')` for `d' ≠ d`. DELETE's subspace isolation mirrors INSERT's: the leftward shift is confined to the subspace of the deletion. Gregory confirms that the shift arithmetic contains an exponent guard that makes cross-subspace subtraction a no-op — a different mechanism from INSERT's two-blade boundary, but the same abstract guarantee.

**AP7 (Deletion is rearrangement, not destruction).** The precondition and postcondition of DELETE satisfy:

  `dom.ispace' = dom.ispace ∧ (A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

DELETE does not even attempt to modify I-space. It operates entirely within the V-space mapping. The "deleted" content is not gone; it is merely not referenced by this document's current arrangement.

### REARRANGE

REARRANGE transposes regions within a document's virtual stream.

*Precondition.* REARRANGE takes a target document and a sequence of **exactly 3 or 4 cut points** — V-space addresses that partition the document into contiguous sections. Any other count is rejected. The cut points are automatically sorted into ascending order; the caller need not provide them in order. The document must be open for writing.

For 3 cuts `[c₀, c₁, c₂]`, the operation defines two adjacent regions `[c₀, c₁)` and `[c₁, c₂)` and swaps them: entries in `[c₀, c₁)` shift by `+(c₂ − c₁)`, entries in `[c₁, c₂)` shift by `−(c₁ − c₀)`. Entries outside `[c₀, c₂)` are unchanged. For 4 cuts `[c₀, c₁, c₂, c₃]`, regions `[c₀, c₁)` and `[c₂, c₃)` exchange positions; the middle region `[c₁, c₂)` shifts by the difference in widths.

The implementation enforces no further constraints: cuts need not be distinct (degenerate cuts yield no-ops), need not fall within the document's V-extent (out-of-bounds cuts produce silent no-ops), and — critically — need not respect subspace boundaries. A rearrangement whose cuts span the text/link boundary can displace text V-positions into link V-space, violating the subspace content discipline. This is a missing guard in the implementation, not an intended feature. We adopt the following as a formal precondition:

**AP8a (Subspace preservation under rearrangement).** REARRANGE must preserve each affected entry's subspace membership:

  `(A p : p ∈ dom.vspace(d) ∧ p is affected by REARRANGE : subspace(p') = subspace(p))`

A REARRANGE whose cut points span the text/link boundary violates AP8a and is rejected. The implementation does not enforce this guard; the abstract specification requires it. Without AP8a, text content could be displaced into link V-positions (or vice versa), corrupting the subspace content discipline that AP4b and AP6 depend on.

*Boundary case.* When cut points are not distinct (e.g., `c₀ = c₁`), the affected regions have zero width and REARRANGE is a no-op — no V-positions shift and AP8 holds trivially.

*Effect on ispace.* **None.** REARRANGE is a pure V-space operation. Nelson: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

*Effect on vspace.* V-positions are permuted. The set of I-addresses referenced by the document is unchanged — only the mapping from V-positions to those I-addresses changes.

Gregory provides the implementation evidence in detail: the operation modifies exactly one field of each affected entry — the V-displacement — leaving the I-displacement, V-width, and I-width untouched. The modification adds a computed offset to the V-displacement, and this addition is uniform across all affected entries (same magnitude for all entries in the same region). The I-address components are never read, never written, never passed as arguments to any arithmetic operation.

We state this precisely. REARRANGE permutes V-positions without altering the codomain — every old I-address survives and no new I-address appears:

**AP8 (I-address invariance under rearrangement).** The set of I-addresses referenced by document `d` is identical before and after REARRANGE:

  `{a : (E p : p ∈ dom.vspace(d) ∧ vspace(d).p = a)} = {a : (E p' : p' ∈ dom.vspace'(d) ∧ vspace'(d).p' = a)}`

Both directions are required. The left-to-right inclusion — `(A a : (E p : vspace(d).p = a) : (E p' : vspace'(d).p' = a))` — says no I-address reference is lost. The right-to-left inclusion — `(A a : (E p' : vspace'(d).p' = a) : (E p : vspace(d).p = a))` — says no I-address reference is introduced. Together they establish that REARRANGE is a pure permutation of V-positions over a fixed set of I-addresses. Gregory's evidence confirms this: the operation modifies only V-displacements, leaving I-displacements untouched, so no I-address can be created or destroyed.

*Frame conditions.* REARRANGE does not affect ispace. REARRANGE does not affect `vspace(d')` for `d' ≠ d`. REARRANGE does not change which I-addresses the document references — it only changes their V-positions.

### COPY (transclusion)

COPY creates a virtual reference from one document to content that already exists in I-space.

*Effect on ispace.* **None.** COPY does not allocate new I-addresses. It creates a V-space mapping in the target document to *existing* I-addresses from the source document.

This is the architectural foundation of transclusion. Nelson: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." The term "virtual copies" is exact — no actual content duplication occurs. The target document's V-space maps new positions to the same I-addresses that the source document's V-space maps to.

Gregory confirms the data flow: COPY converts the source document's V-span to I-addresses through its mapping, then inserts those I-addresses (unchanged, via direct memory copy) into the target document's mapping at new V-positions. No allocation function for content is called. The I-addresses extracted from the source are the I-addresses deposited in the target — identical values, not copies with new addresses.

*Boundary case.* COPY of zero characters creates no V-positions in the target document and is a no-op on both I-space and V-space.

**AP9 (Identity preservation under transclusion).** If content at I-address `a` appears in document `d₁` and is transcluded to document `d₂`, then both documents' V-space mappings reference the same `a`:

  `(E p₁ : vspace(d₁).p₁ = a) ∧ (E p₂ : vspace'(d₂).p₂ = a)`

The content has one identity — its I-address — regardless of how many documents reference it.

*Frame conditions.* COPY does not modify ispace. For `d₁ ≠ d₂`, COPY modifies `vspace(d₂)` (the target) but not `vspace(d₁)` (the source) — the source document is a read-only participant. When `d₁ = d₂` (copy within the same document), both the read of source positions and the write of target positions operate on the same document's V-space; the source I-addresses are extracted before the target positions are modified.

### CREATENEWVERSION

Version creation produces a new document whose V-space maps to the same I-addresses as the source.

*Effect on ispace.* CREATENEWVERSION allocates one fresh address — the new document's identity. This address does *not* enter `dom.ispace`. It is a ghost address: it occupies a position in the address space (links may reference it, and its range is protected by AP4a), but no content is stored at it.

We must be precise about the distinction. A **content address** is a member of `dom.ispace` — it has stored content. A **document identity address** is a structural position in the address hierarchy, identifying a document (or server, or account) without storing content. CREATENEWVERSION produces a document identity address, not a content address. The document identity is recorded in the system's structural index — the same tree structure that allocates addresses and manages document orgls — rather than as a content mapping in `ispace`.

Gregory's evidence is definitive. The implementation allocates the new document's identity by computing the next available child address under the source document's position in the address hierarchy. The resulting entry is a POOM orgl node (a mapping structure) in the global allocation tree — not a content atom. There is no separate document registry; the allocation tree's structure *is* the document registry. But the POOM orgl is not an `ispace` content entry: it is the document's arrangement layer (its V-space), not content stored at an address. No content allocation function is invoked during version creation.

CREATENEWVERSION does NOT allocate new content addresses. Nelson: "This creates a new document with the contents of document \<doc id\>." The new document's V-space references the same I-addresses as the source. No content duplication occurs.

Gregory provides empirical confirmation: after creating content "ABC" (allocating addresses `α₁, α₂, α₃`), creating a version, then inserting "XYZ", the new content receives addresses `α₄, α₅, α₆` — contiguous with the original allocation. If version creation had consumed content addresses, there would be a gap.

**AP10 (Version identity sharing).** After CREATENEWVERSION creates document `d'` from document `d`, the text content referenced by `d'` is exactly the text content referenced by `d`:

  `{a : (E p : vspace(d).p = a ∧ p ∈ text_subspace)} = {a : (E p' : vspace'(d').p' = a ∧ p' ∈ text_subspace)}`

The I-address sets are equal. This is what makes version comparison possible — the system identifies shared content by shared I-addresses.

**AP10a (New version has empty link subspace).** The new version's V-space contains no link-subspace entries:

  `{p ∈ dom.vspace'(d') : p.subspace = link_subspace} = ∅`

The link subspace of the source is not copied — the new version begins with text content only. Links are not structural properties of content; they are independent artifacts owned by a document. A new version inherits the content arrangement but not the link collection.

*Frame conditions.* CREATENEWVERSION does not modify content in ispace. It does not modify `vspace(d)` (the source document).

### CREATELINK

Link creation allocates a fresh I-address for the link structure, records the link's endsets, and places the link in a document's V-space.

CREATELINK takes a **home document** — the document that will own the link — along with the endset specifications (from, to, type). The home document is an explicit parameter of the operation; it is distinct from the documents whose content the endsets reference.

*Effect on ispace.* CREATELINK extends `dom.ispace` with a fresh address `ℓ` in the link subspace. The endsets are stored as span descriptors — I-address ranges derived by V→I lookup in the endpoint documents at creation time. At creation, each span covers a contiguous range of allocated I-addresses (the V→I lookup traverses the source document's mapping, which references only allocated content). The stored span is thereafter immutable (AP1); the set `covers(e) ∩ dom.ispace` may grow as new content is allocated within the span's range but can never shrink (AP0). The link's own address occupies a separate subspace from text content.

*Boundary case.* CREATELINK with an empty endset (zero span descriptors in one or more endset positions) is a valid operation — it allocates a link address `ℓ` and stores a link structure with empty endsets. The link exists but references no content. AP is preserved: the link address is fresh (AP2) and no existing ispace entry is modified. Whether such a link is useful is a semantic question; the permanence properties do not distinguish it from a link with non-empty endsets.

*Effect on vspace.* CREATELINK inserts a V-position in the **home document's link subspace** mapping the next available link V-position to `ℓ`. This is structurally identical to how INSERT places text: the home document gains a new V-position in its link subspace, and that position maps to the link's I-address. Gregory's evidence is definitive: `docopy` inserts a POOM entry in the home document's enfilade, mapping a link-subspace V-address (at or beyond `2.1` in the internal numbering) to the link's I-space span.

The source and target endpoint documents are **read-only participants** — their V-spaces are consulted to resolve endset V-specifications into I-addresses, but nothing is written into them. Link discoverability from those documents is entirely I-address-based: the span index maps endpoint I-addresses to the link's I-address, so any document containing that content can discover the link without modification to its own V-space.

**AP16 (CREATELINK subspace isolation).** CREATELINK modifies only the link subspace of the home document's V-space. The text subspace of the home document, and all subspaces of all other documents, are unchanged:

  `(A d : d ≠ home(op) : vspace'(d) = vspace(d))`
  `(A p : p ∈ dom.vspace(home(op)) ∧ p.subspace = text_subspace : vspace'(home(op)).p = vspace(home(op)).p)`

*Frame conditions.* CREATELINK does not modify any existing ispace entry. It does not modify any document's text subspace mapping. It does not modify the V-space of any endpoint document. The endset I-addresses it references are not affected.


## The historical index

Beyond ispace and vspace, the system maintains a third data structure: the span index, which records which documents have contained which I-address ranges. This index has its own permanence property.

**AP11 (Index monotonicity).** The span index is append-only. When an operation records that document `d` contains I-address range `R`, that record persists forever:

  `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')`

Gregory provides definitive evidence. The span index has insertion functions but no deletion functions — no `deletespan`, no `removespan`, no cleanup mechanism of any kind exists. When DELETE removes content from a document's V-space mapping, the span index entry recording that the document once contained that content is not touched. The index records historical fact: "document `d` once contained I-addresses `R`." This assertion is true at the moment of recording and remains true forever — it is a statement about the past, and the past does not change.

A consequence is that the span index may contain *stale* entries — records asserting that document `d` contains addresses that `d`'s V-space no longer maps to. The reverse direction of a natural correspondence does not hold: `(a, d) ∈ spanindex` does not imply `(E p : vspace(d).p = a)`. The index is an *over-approximation* of the current state. Queries that consult the span index (such as "find all documents containing these I-addresses") may return documents that no longer reference the content. A second check against the document's V-space mapping is needed to filter stale results.

The forward direction — that every live V-space reference is indexed — is the intended design property:

  `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)`

We do not verify this invariant here. Verification requires specifying, for each operation that creates V-space entries (INSERT, COPY, CREATENEWVERSION), that it also adds corresponding spanindex records. This ASN establishes only that spanindex records, once written, are never removed (AP11). The maintenance obligation — which operations must write spanindex entries and when — is deferred.

This is not a defect — it is the price of AP11. A mutable index could be kept exact, but would violate monotonicity. An append-only index is monotone but over-approximate. The system chooses monotonicity, which is consistent with the broader design principle: the permanent layer never retracts a claim.


## Link survivability as consequence

We are now in a position to derive, rather than merely assert, the survivability of links through editing. Nelson states the guarantee: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

The derivation has three premises:

1. Links reference I-space address ranges (they are stored as span descriptors in the link structure).
2. I-space addresses are permanent (AP0) and content at those addresses is immutable (AP1).
3. Editing operations do not modify or remove existing I-space entries (AP5). They may extend I-space monotonically, but monotonic extension adds fresh addresses — it cannot alter the content at addresses that a link already references.

From (1) and (2): the address ranges that a link's endsets cover never lose existing content — addresses already in `dom.ispace` remain with unchanged content. From (3): editing cannot alter the I-space entries within a link's endset ranges, because AP5 guarantees that existing entries are immutable. The fact that INSERT or CREATELINK may *extend* I-space with fresh addresses is irrelevant to existing link references — a link whose endset covers address `a` is unaffected by the creation of a new address `a' ≠ a`.

Therefore: a link continues to reference valid I-space content after any sequence of editing operations. What *may* change is whether the linked content is *reachable* through some document's V-space — if content is deleted from every document's arrangement, the link's endsets have no V-space presence. The link is not broken (its span descriptors are still valid and the I-addresses they cover still exist); it is merely *unresolvable through V-space* in the current state.

We can now derive the link permanence property from AP1. A link `ℓ ∈ links` has content `ispace.ℓ`, which includes its endset span descriptors. By AP1, `ispace'.ℓ = ispace.ℓ` for every operation. Since the span descriptors are part of `ispace.ℓ`, they are immutable whenever `ispace.ℓ` is immutable — which is always:

**AP12 (Link permanence).** A link's endset span descriptors are not affected by any editing operation:

  `(A ℓ ∈ links, e ∈ endsets(ℓ) : e.spans' = e.spans)`

for every operation that transforms Σ to Σ'. This is a corollary of AP1: `ℓ ∈ dom.ispace` (by definition of `links`), so `ispace'.ℓ = ispace.ℓ`, so `endsets(ℓ)` — being derived from `ispace.ℓ` — is unchanged. Because span descriptors are immutable, the *range* a link covers is permanent. What may change is the *content* within that range: `covers(e) ∩ dom.ispace` can only grow (by AP0 and monotonic extension), never shrink.

And the reconstitution property:

**AP13 (Link endset validity under re-transclusion).** If a link's endset references I-address `a`, and content at `a` is re-introduced into some document's V-space (by COPY from any source that still references `a`), then the link's endset reference to `a` remains valid — the I-address still maps to the same content (by AP1), and the target document now has a V-space mapping to it.

What AP13 does *not* establish is the *discoverability* of the link through the target document. Discoverability requires a mechanism that, given an I-address `a` present in a document's V-space, can find all links whose endsets reference `a`. The span index (`spanindex ⊆ Addr × DocId`) records which documents have contained which addresses, but not which links reference which addresses. A link-discovery mechanism (such as an index from content I-addresses to links) is needed but is not defined in this ASN.

Gregory confirms the re-transclusion cycle: create a link to content; delete the content from all documents; re-transclude the same I-addresses. The link's endset references remain valid throughout — the I-addresses persist (AP0) with unchanged content (AP1). Critically, this works only for COPY (which shares existing I-addresses) — not for re-typing the same text (which produces *new* I-addresses that the link does not reference). Identity is structural, not textual.


## Permanence of the address-content pair

We can now state the strongest form of the permanence guarantee, combining all the individual properties:

**Theorem (Address-content invariance).** For every reachable state Σ and every operation *defined in this ASN* transforming Σ to Σ':

  `(A a ∈ dom.ispace : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`

This ASN defines six operations that modify Σ: INSERT, DELETE, REARRANGE, COPY, CREATENEWVERSION, and CREATELINK. Other operations may exist in the broader system (document creation as distinct from version creation, account creation, node creation, administrative operations). Any such operation must be shown to preserve AP as a condition of its introduction.

*Proof.* By case analysis on each of the six operations:

- **INSERT**: Creates fresh addresses (AP2) with new content. The fresh addresses are disjoint from `dom.ispace`, and INSERT writes only at those addresses, so no pre-existing ispace entry is read or written — hence `ispace'.a = ispace.a` for all `a ∈ dom.ispace`. INSERT extends ispace and contains no removal instruction, so `dom.ispace ⊆ dom.ispace'`.

- **DELETE**: Does not modify ispace at all (AP7). Both AP0 and AP1 hold trivially.

- **REARRANGE**: Does not modify ispace at all. Pure V-space operation (AP8). Both AP0 and AP1 hold trivially.

- **COPY**: Does not modify ispace. Creates V-space mappings to existing I-addresses (AP9). Both AP0 and AP1 hold trivially.

- **CREATENEWVERSION**: The document identity address is not a content address and does not enter `dom.ispace`. A POOM orgl is structural metadata, not a value of type `Content` (= `TextContent | LinkStructure`), so it has no representation in `ispace`. No content addresses are allocated. The operation creates V-space mappings to existing I-addresses but contains no instruction that modifies or removes any ispace entry — hence `dom.ispace' = dom.ispace` and `ispace'.a = ispace.a` for all `a ∈ dom.ispace`.

- **CREATELINK**: Allocates one fresh address in the link subspace (disjoint from existing addresses by AP2). Writes the link structure at that fresh address only. Contains no instruction that reads or writes any pre-existing ispace entry — hence `ispace'.a = ispace.a` for all `a ∈ dom.ispace`, and `dom.ispace ⊆ dom.ispace'`. The V-space effect (inserting a link-subspace position in the home document) does not modify ispace.

Since every operation preserves AP0 and AP1, and the initial state (empty ispace) satisfies AP trivially, AP holds in every reachable state. ∎


## Worked example

We trace a scenario through four operations, verifying the key postconditions at each step. Begin with an empty system: `dom.ispace = ∅`, no documents.

**Step 1: INSERT "AB" into document `d`.** The system allocates fresh addresses `α₁, α₂` (AP2: both `∉ dom.ispace = ∅`). After:

  `dom.ispace = {α₁, α₂}`,  `ispace.α₁ = 'A'`,  `ispace.α₂ = 'B'`
  `dom.vspace(d) = {(text, 0), (text, 1)}`,  `vspace(d).(text, 0) = α₁`,  `vspace(d).(text, 1) = α₂`

Check: AP0 holds (dom.ispace grew from ∅). AP1 holds vacuously (no prior entries). AP2 holds (α₁, α₂ were not in ∅).

**Step 2: DELETE the first character from `d`.** DELETE removes the V-position mapping to `α₁`.

  `dom.ispace = {α₁, α₂}` — unchanged (AP7)
  `ispace.α₁ = 'A'`,  `ispace.α₂ = 'B'` — unchanged (AP1)
  `dom.vspace(d) = {(text, 0)}`,  `vspace(d).(text, 0) = α₂`

Check: AP0 holds (`{α₁, α₂} ⊆ {α₁, α₂}`). AP1 holds (both entries unchanged). The address `α₁` remains in `dom.ispace` — the content 'A' persists — though no V-position maps to it. The "deletion" was a V-space rearrangement, not content destruction.

**Step 3: COPY the surviving character to a new document `d₂`.** COPY reads `vspace(d).(text, 0) = α₂` and creates a V-mapping in `d₂`.

  `dom.ispace = {α₁, α₂}` — unchanged (COPY allocates no content)
  `dom.vspace(d₂) = {(text, 0)}`,  `vspace(d₂).(text, 0) = α₂`

Check: AP0, AP1 hold (ispace untouched). AP9 holds: both `d` and `d₂` reference the same `α₂`. AP14 holds: `vspace(d)` is unchanged (COPY's target is `d₂`, and `d` is read-only).

**Step 4: CREATELINK with home document `d`, referencing `α₁`.** The system allocates fresh link address `ℓ₁` (AP2: `ℓ₁ ∉ {α₁, α₂}`). The link has one endset containing a span covering `α₁`. The home document `d` gains a V-position in its link subspace.

  `dom.ispace = {α₁, α₂, ℓ₁}`,  `ispace.ℓ₁` = link structure with endset span covering `α₁`
  `links = {ℓ₁}`,  `endsets(ℓ₁) = {span(α₁, 1)}`
  `dom.vspace(d) = {(text, 0), (link, 0)}`,  `vspace(d).(link, 0) = ℓ₁`

Check: AP0 holds (`{α₁, α₂} ⊆ {α₁, α₂, ℓ₁}`). AP1 holds (α₁ and α₂ unchanged; ℓ₁ is fresh). AP16 holds (only `d`'s link subspace gained a position; text subspace and `d₂` unchanged). AP12 holds: the link references `α₁`, which is in `dom.ispace` with content 'A'. Even though `α₁` was "deleted" from `d`'s V-space in step 2, the link's endset reference is valid — `α₁` persists in I-space (AP0) with unchanged content (AP1). If `α₁` is later re-transcluded into some document via COPY, the link will be resolvable through V-space again.

The scenario confirms: `dom.ispace` only grows (∅ → {α₁, α₂} → {α₁, α₂} → {α₁, α₂} → {α₁, α₂, ℓ₁}); content is immutable throughout; "deletion" is a V-space operation only; links survive editing because they anchor to I-space.


## Cross-document isolation

A property implicit in the per-operation analysis but worth stating explicitly. We first need a definition: each operation has a **target document** — the document whose V-space it modifies. For INSERT, DELETE, REARRANGE, and CREATELINK, the target is the single document named by the operation. For COPY, the target is `d₂` (the destination); the source `d₁` is a read-only participant. For CREATENEWVERSION, the target is the newly created document `d'`; the source `d` is read-only.

**AP14 (Cross-document independence).** Only the target document's V-space is modified:

  `(A d₂ : d₂ ≠ target(op) : vspace'(d₂) = vspace(d₂))`

We verify for each operation. INSERT, DELETE, REARRANGE: target is `d`, and the operation's V-space effects are confined to `d` (AP6 for INSERT; analogous confinement for DELETE and REARRANGE). COPY from `d₁` to `d₂`: target is `d₂`; the source `d₁`'s V-space is only read, never written — `vspace'(d₁) = vspace(d₁)`. CREATENEWVERSION from `d` producing `d'`: target is `d'`; the source `d`'s V-space is only read — `vspace'(d) = vspace(d)`. CREATELINK: target is the home document; endpoint documents are read-only participants (AP16).

And more specifically for transclusion integrity:

**AP15 (Transclusion survivability).** If document `d₂` transcludes content at I-address `a`, and the owner of document `d₁` (where `a` was created) deletes `a` from `d₁`'s V-space, then `d₂`'s mapping to `a` is unaffected:

  `(E p : vspace(d₂).p = a) ⟹ (E p : vspace'(d₂).p = a)`

This follows from AP14 (the delete operates on `d₁`, not `d₂`) and AP0 (the I-address `a` remains in ispace, so `d₂`'s reference to it remains valid).

Nelson states this guarantee directly: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." Transclusion is not a fragile sharing mechanism that breaks when the source changes — it is a permanent reference to permanent content.


## The permanence hierarchy

Let us step back and observe the layered structure. The system maintains three layers with decreasing mutability:

1. **I-space** (fully immutable): governed by AP0, AP1, AP2, AP3, AP4. Content and addresses are permanent. The only allowed modification is monotonic extension.

2. **Span index** (append-only): governed by AP11. Records are permanent once written. The index grows but never shrinks. Over-approximation is the price of monotonicity.

3. **V-space** (fully mutable): governed by no permanence constraint. V-space mappings are freely modified by INSERT, DELETE, REARRANGE, COPY, and CREATENEWVERSION.

The design principle is: permanence descends toward the foundation. The mutable layer (V-space) sits atop two immutable layers (span index, I-space). Links, attribution, correspondence, and discovery all anchor into the immutable layers. Editing operates in the mutable layer. The two concerns — stability and flexibility — are architecturally separated rather than traded off against each other.


## What permanence costs

Permanence is not free. The append-only I-space grows without bound. Content that has been "deleted" from every document's V-space still occupies I-space. The span index accumulates stale entries. There is no garbage collection — the system is not designed for it, and AP0 would forbid it.

Nelson is aware of this: the storage model is explicitly non-destructive ("Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version"). The design rejects space reclamation in favor of referential stability. This is a conscious trade: in a system where any content may be linked to, transcluded, or cited by any other document, it is impossible to determine that content is "truly unreferenced" without global knowledge. The cost of maintaining permanence is storage growth. The cost of violating it is the corruption of every reference in the system.

Gregory's implementation takes this further: even the allocation counter for I-addresses is not a stored value but is recomputed from the content store on each allocation — the system queries for the highest existing address and increments. This means the allocation frontier is *derived* from the permanent data, not maintained as separate mutable state. There is no counter to lose and no counter that can drift out of sync.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| AP0 | Once an address enters dom.ispace, it remains forever: dom.ispace ⊆ dom.ispace' for every operation | introduced |
| AP1 | Content at an allocated address never changes: ispace'.a = ispace.a for all a ∈ dom.ispace | introduced |
| AP | Address permanence: AP0 ∧ AP1 — irrevocability and immutability combined | introduced |
| AP2 | Every allocation uses an address not previously in dom.ispace (freshness) | introduced |
| AP3 | No address may be freed and re-allocated (no reuse); follows from AP0 ∧ AP2 | derived |
| AP4 | The allocation frontier within each partition is strictly monotonic; gaps below the frontier are permanent | introduced |
| AP4a | The assignment of an address-space range to an entity (server, account, document) is permanent and irrevocable | introduced |
| AP4b | The address ranges of distinct subspace partitions are disjoint: text_subspace ∩ link_subspace = ∅ | introduced |
| AP5 | Restatement of AP (= AP0 ∧ AP1) in the dual-space vocabulary; editing operations preserve I-space and may only extend it | restatement of AP |
| AP6 | INSERT shifts only V-positions in the same subspace of the same document | introduced |
| AP7 | DELETE does not modify ispace; deletion is rearrangement, not destruction | derived |
| AP8 | REARRANGE preserves the set of I-addresses referenced by a document as a set equality; only V-positions change | introduced |
| AP8a | REARRANGE must preserve each affected entry's subspace membership; cross-subspace displacement is rejected | introduced |
| AP9 | COPY (transclusion) shares existing I-addresses; target document references the same addresses as source | introduced |
| AP10 | CREATENEWVERSION shares text I-addresses between source and new version; no content allocation occurs | introduced |
| AP10a | The new version's V-space contains no link-subspace entries | introduced |
| AP11 | The span index is append-only; records of content placement persist forever | introduced |
| AP12 | A link's endset span descriptors are invariant under all editing operations; corollary of AP1 | derived |
| AP13 | A link's endset references remain valid when its I-addresses are re-introduced to V-space via COPY; discoverability requires a link-discovery mechanism not defined here | derived |
| AP14 | Only the target document's V-space is modified; target(op) defined per operation | introduced |
| AP15 | Deletion of content from its home document does not affect transclusions in other documents | derived |
| AP16 | CREATELINK modifies only the link subspace of the home document; text subspace and all other documents unchanged | introduced |
| Σ.ispace | ispace : Addr ⇀ Content — the permanent content store, partitioned into text and link subspaces | introduced |
| Σ.vspace | vspace(d) : Pos ⇀ Addr — per-document mutable arrangement (partial, finite domain) | introduced |
| Σ.spanindex | spanindex ⊆ Addr × DocId — the append-only historical index of content placement | introduced |
| Σ.links | links = {ℓ ∈ dom.ispace : ℓ ∈ link_subspace} — derived from ispace | introduced |


## Open Questions

Must the system provide a mechanism to determine, for a given I-address, which documents currently reference it (as opposed to which documents have ever referenced it)?

What must the system guarantee about the retrievability of content at an I-address that is not referenced by any document's current V-space — is direct I-address lookup a required operation?

Which operations must write spanindex entries, and what is the precise maintenance obligation that preserves the forward correspondence `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)`?

What mechanism must the system provide for link discovery — given a content I-address, how does the system find all links whose endsets reference that address?

Under what conditions may a system declare content at a valid I-address to be *inaccessible* (e.g., due to hardware failure), and what properties survive such a declaration?

Must the allocation frontier be recoverable after a crash without loss of monotonicity, and what minimum persistent state is needed to guarantee this?

What permanence obligations, if any, apply to the document identity address allocated by CREATENEWVERSION — must the version graph itself be append-only?

What must the system guarantee about the ordering of allocations across different subspaces within the same document — must text and link allocations be totally ordered, or only ordered within their respective subspaces?

What operations beyond the six analyzed here (INSERT, DELETE, REARRANGE, COPY, CREATENEWVERSION, CREATELINK) modify system state, and do they preserve AP?
