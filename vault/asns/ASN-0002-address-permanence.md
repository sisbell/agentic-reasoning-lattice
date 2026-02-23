# ASN-0002: Address Permanence

*2026-02-23*

We wish to understand what the system must guarantee about the stability of addresses. The question is sharp: once content is assigned an address, what may change? The answer, we shall discover, is equally sharp — nothing may change. But the sharpness of the answer conceals a rich internal structure. There are two address spaces with opposite stability contracts, a write-once content store, a write-only historical index, and a collection of editing operations that must be shown to preserve permanence individually. We develop each piece.


## The system state

We need a minimal vocabulary. Let the system state at any moment be Σ, containing at least:

- **ispace**: a partial function from addresses to content, recording what has been stored. `ispace : Addr ⇀ Content`.
- **vspace(d)**: for each document d, a function from virtual positions to addresses, recording the current arrangement. `vspace(d) : Pos → Addr`.
- **spanindex**: a relation recording which documents have ever contained which address ranges. `spanindex ⊆ Addr × DocId`.

We write `dom.ispace` for the set of addresses at which content is stored, `ispace.a` for the content at address `a`, and `#vspace(d)` for the length of document d's virtual stream. We use primed names (Σ', ispace', etc.) for the state after an operation.


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

We need not formalize ghost elements as a separate type. They are simply addresses in the range of the address space's total order that are not (yet) in `dom.ispace`. AP0–AP3 already handle them correctly: AP0 does not require that every address in the ordering be in `dom.ispace`, only that addresses which *enter* `dom.ispace` never leave. Ghost addresses are below the allocation frontier — they may eventually receive content (becoming members of `dom.ispace`), or they may remain forever empty. In neither case can they be repurposed.

What we do need is a strengthening of AP2:

**AP4 (Monotonic frontier).** The allocation counter within each partition never retreats. If the highest allocated address in partition `p` is `a`, then the next allocation in `p` produces some `a' > a`. Gaps below `a` are permanent.

AP4 implies AP2 (fresh addresses are above all existing ones, hence disjoint from them) but is strictly stronger: it also forbids filling gaps. If addresses `α₃` and `α₅` exist in a partition but `α₄` does not, AP4 guarantees that `α₄` will never be filled by a later allocation — the counter has moved past it.

Gregory confirms: when a link operation allocates in one subspace and a subsequent text operation allocates in the text subspace, each subspace maintains its own frontier independently. The link address does not consume text addresses, and text allocation does not fill the gap left by the link's position in the unified address ordering. The two subspaces have disjoint address ranges by structural design: text addresses begin with subspace identifier 1, link addresses with identifier 2. The allocation function computes a different upper bound for each subspace and searches below that bound, ensuring that text allocation never finds a link address and vice versa.


## The two-space architecture

We now address the apparent paradox: if addresses are permanent and content is immutable, how does editing work? The answer is that the system maintains two address spaces with opposite stability contracts.

**I-space** (identity space) is the permanent content store, governed by AP0–AP4. An I-space address is the *identity* of a piece of content — it says "which byte this is, forever."

**V-space** (virtual space) is the mutable arrangement layer. A document's V-space is a mapping from positions to I-space addresses: `vspace(d) : Pos → Addr`. V-space positions are ephemeral — they shift with every edit. Nelson: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing."

The fundamental separation:

**AP5 (Dual-space contract).** Editing operations modify V-space; they do not modify I-space. The permanence axioms (AP0–AP4) govern I-space. V-space has no permanence guarantee.

We can now state what "editing" means precisely. An editing operation changes the mapping `vspace(d)` for some document `d`. It does not change `ispace`. The mapping may grow (INSERT adds new I-space addresses and maps V-positions to them), shrink (DELETE removes V-positions), or be permuted (REARRANGE changes which V-positions map to which I-addresses). But through all of this, the I-space side is untouched.

The library analogy is apt. I-space is the permanent stacks — books on shelves, each at a fixed location, never moved, never removed. V-space is a reading list — an ordered sequence of references to shelf locations. You can reorder your reading list, add references, remove references. The books on the shelves are indifferent to what your reading list says.


## Operation-by-operation analysis

We must verify AP for each operation. The strategy is: for each operation, we state its effect on ispace and show that AP is preserved. We also state its frame conditions — what it does NOT change.

### INSERT

INSERT creates new content and places it in a document.

*Effect on ispace.* INSERT extends `dom.ispace` with fresh addresses carrying new content. Let `a₁, ..., aₙ` be the addresses allocated for the inserted text. Then:

  `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom.ispace ∧ aᵢ ∈ dom.ispace')`

by AP2 (freshness). And for all pre-existing addresses:

  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

by AP1 (content immutability).

*Effect on vspace.* INSERT modifies `vspace(d)` for the target document. New V-positions are created mapping to the fresh I-addresses. Existing V-positions at or beyond the insertion point shift forward by the width of the inserted text. Nelson: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

Crucially, the shift is confined to a single subspace within the document. V-positions in the link subspace are not affected by a text insertion:

**AP6 (Subspace isolation under INSERT).** INSERT at a V-position in subspace `s` of document `d` shifts only V-positions in subspace `s` of document `d`. All V-positions in other subspaces of `d`, and all V-positions in all other documents, are unchanged.

Gregory confirms the mechanism: the shift classifies each entry in the document's mapping into three regions using a two-blade boundary. All entries in the insertion subspace at or beyond the insertion point receive an identical shift equal to the insertion width. Entries before the insertion point and entries in other subspaces receive no shift. No entry receives a different shift magnitude — the operation is uniform within its region.

*Frame conditions.* INSERT does not affect `ispace` at existing addresses. INSERT does not affect `vspace(d')` for any document `d' ≠ d`. INSERT does not affect the link subspace of document `d`. These are critical: INSERT's blast radius is exactly one subspace of one document's V-space, plus the monotonic extension of I-space.

### DELETE

DELETE removes content from a document's current arrangement.

*Effect on ispace.* **None.** DELETE does not modify ispace in any way. The content remains at its I-space addresses:

  `dom.ispace' = dom.ispace`
  `(A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

Nelson is explicit: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." And: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

The phrase "not currently addressable" is precise — not addressable through this document's current V-space mapping. The I-space address remains as valid as ever.

*Effect on vspace.* DELETE modifies `vspace(d)` by removing entries and shifting surviving entries leftward. V-positions after the deleted region decrease by the width of the deletion.

*Frame conditions.* DELETE does not affect ispace. DELETE does not affect `vspace(d')` for `d' ≠ d`. DELETE's subspace isolation mirrors INSERT's: the leftward shift is confined to the subspace of the deletion. Gregory confirms that the shift arithmetic contains an exponent guard that makes cross-subspace subtraction a no-op — a different mechanism from INSERT's two-blade boundary, but the same abstract guarantee.

**AP7 (Deletion is rearrangement, not destruction).** The precondition and postcondition of DELETE satisfy:

  `dom.ispace' = dom.ispace ∧ (A a : a ∈ dom.ispace : ispace'.a = ispace.a)`

DELETE does not even attempt to modify I-space. It operates entirely within the V-space mapping. The "deleted" content is not gone; it is merely not referenced by this document's current arrangement.

### REARRANGE

REARRANGE transposes regions within a document's virtual stream.

*Effect on ispace.* **None.** REARRANGE is a pure V-space operation. Nelson: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

*Effect on vspace.* V-positions are permuted. The set of I-addresses referenced by the document is unchanged — only the mapping from V-positions to those I-addresses changes.

Gregory provides the implementation evidence in detail: the operation modifies exactly one field of each affected entry — the V-displacement — leaving the I-displacement, V-width, and I-width untouched. The modification adds a computed offset to the V-displacement, and this addition is uniform across all affected entries (same magnitude for all entries in the same region). The I-address components are never read, never written, never passed as arguments to any arithmetic operation.

We state this precisely:

**AP8 (I-address invariance under rearrangement).** For every address `a` referenced by document `d` before REARRANGE:

  `(A a : (E p : vspace(d).p = a) : (E p' : vspace'(d).p' = a))`

The set of I-addresses in the document's mapping is invariant under REARRANGE. What changes is only which V-position maps to each I-address.

*Frame conditions.* REARRANGE does not affect ispace. REARRANGE does not affect `vspace(d')` for `d' ≠ d`. REARRANGE does not change which I-addresses the document references — it only changes their V-positions.

### COPY (transclusion)

COPY creates a virtual reference from one document to content that already exists in I-space.

*Effect on ispace.* **None.** COPY does not allocate new I-addresses. It creates a V-space mapping in the target document to *existing* I-addresses from the source document.

This is the architectural foundation of transclusion. Nelson: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." The term "virtual copies" is exact — no actual content duplication occurs. The target document's V-space maps new positions to the same I-addresses that the source document's V-space maps to.

Gregory confirms the data flow: COPY converts the source document's V-span to I-addresses through its mapping, then inserts those I-addresses (unchanged, via direct memory copy) into the target document's mapping at new V-positions. No allocation function for content is called. The I-addresses extracted from the source are the I-addresses deposited in the target — identical values, not copies with new addresses.

**AP9 (Identity preservation under transclusion).** If content at I-address `a` appears in document `d₁` and is transcluded to document `d₂`, then both documents' V-space mappings reference the same `a`:

  `(E p₁ : vspace(d₁).p₁ = a) ∧ (E p₂ : vspace'(d₂).p₂ = a)`

The content has one identity — its I-address — regardless of how many documents reference it.

*Frame conditions.* COPY does not modify ispace. COPY modifies `vspace(d₂)` (the target) but not `vspace(d₁)` (the source). The source document is a read-only participant.

### CREATENEWVERSION

Version creation produces a new document whose V-space maps to the same I-addresses as the source.

*Effect on ispace.* CREATENEWVERSION allocates one fresh address — the new document's identity. It does NOT allocate new content addresses. Nelson: "This creates a new document with the contents of document \<doc id\>." The new document's V-space references the same I-addresses as the source. No content duplication occurs.

Gregory confirms this emphatically. The implementation converts the source document's V-span to I-addresses, then inserts those I-addresses into the new document's mapping. No content allocation function is invoked. The evidence is empirical: after creating content "ABC" (allocating addresses `α₁, α₂, α₃`), creating a version, then inserting "XYZ", the new content receives addresses `α₄, α₅, α₆` — contiguous with the original allocation. If version creation had consumed content addresses, there would be a gap.

**AP10 (Version identity sharing).** After CREATENEWVERSION creates document `d'` from document `d`, the text content referenced by `d'` is exactly the text content referenced by `d`:

  `{a : (E p : vspace(d).p = a ∧ p ∈ text_subspace)} = {a : (E p' : vspace'(d').p' = a ∧ p' ∈ text_subspace)}`

The I-address sets are equal. This is what makes version comparison possible — the system identifies shared content by shared I-addresses.

*Frame conditions.* CREATENEWVERSION does not modify content in ispace. It does not modify `vspace(d)` (the source document). The link subspace of the source is not copied — the new version begins with text content only.

### CREATELINK

Link creation allocates a fresh I-address for the link structure and records the link's endsets.

*Effect on ispace.* CREATELINK extends `dom.ispace` with a fresh address in the link subspace. The endsets are stored as I-address references — they point to existing content addresses. The link's own address occupies a separate subspace from text content.

*Frame conditions.* CREATELINK does not modify any existing ispace entry. It does not modify any document's text subspace mapping. The endset I-addresses it references are not affected.


## The historical index

Beyond ispace and vspace, the system maintains a third data structure: the span index, which records which documents have contained which I-address ranges. This index has its own permanence property.

**AP11 (Index monotonicity).** The span index is append-only. When an operation records that document `d` contains I-address range `R`, that record persists forever:

  `(A (a, d) : (a, d) ∈ spanindex : (a, d) ∈ spanindex')`

Gregory provides definitive evidence. The span index has insertion functions but no deletion functions — no `deletespan`, no `removespan`, no cleanup mechanism of any kind exists. When DELETE removes content from a document's V-space mapping, the span index entry recording that the document once contained that content is not touched. The index records historical fact: "document `d` once contained I-addresses `R`." This assertion is true at the moment of recording and remains true forever — it is a statement about the past, and the past does not change.

A consequence is that the span index may contain *stale* entries — records asserting that document `d` contains addresses that `d`'s V-space no longer maps to. The forward direction of the correspondence is maintained:

  `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)`

Every live reference is indexed. But the reverse does not hold: `(a, d) ∈ spanindex` does not imply `(E p : vspace(d).p = a)`. The index is an *over-approximation* of the current state. Queries that consult the span index (such as "find all documents containing these I-addresses") may return documents that no longer reference the content. A second check against the document's V-space mapping is needed to filter stale results.

This is not a defect — it is the price of AP11. A mutable index could be kept exact, but would violate monotonicity. An append-only index is monotone but over-approximate. The system chooses monotonicity, which is consistent with the broader design principle: the permanent layer never retracts a claim.


## Link survivability as consequence

We are now in a position to derive, rather than merely assert, the survivability of links through editing. Nelson states the guarantee: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."

The derivation has three premises:

1. Links reference I-space addresses (they are stored as I-address spans in the link structure).
2. I-space addresses are permanent (AP0) and content at those addresses is immutable (AP1).
3. Editing operations modify only V-space (AP5, AP7, AP8).

From (1) and (2): the addresses that a link points to never become invalid and never change their content. From (3): editing cannot alter the addresses a link references, because those addresses live in I-space and editing operates in V-space.

Therefore: a link continues to reference valid I-space content after any sequence of editing operations. What *may* change is whether the linked content is *reachable* through some document's V-space — if content is deleted from every document's arrangement, the link's endsets have no V-space presence. The link is not broken (its I-address references are still valid); it is merely *unresolvable through V-space* in the current state.

**AP12 (Link permanence).** A link's endset I-addresses are not affected by any editing operation:

  `(A link ∈ links, e ∈ endsets(link) : e.iaddrs' = e.iaddrs)`

for every operation that transforms Σ to Σ'.

And the reconstitution property:

**AP13 (Link reconstitution).** If a link's endset references I-address `a`, and content at `a` is re-introduced into some document's V-space (by COPY from any source that still references `a`), then the link becomes discoverable again through that document.

Gregory confirms this cycle: create a link to content; delete the content from all documents; re-transclude the same I-addresses. The link is discoverable after re-transclusion because the span index still records the link's association with those I-addresses, and the re-transclusion restores a V-space mapping to them. Critically, this works only for COPY (which shares existing I-addresses) — not for re-typing the same text (which produces *new* I-addresses that the link does not reference). Identity is structural, not textual.


## Permanence of the address-content pair

We can now state the strongest form of the permanence guarantee, combining all the individual properties:

**Theorem (Address-content invariance).** For every reachable state Σ and every operation transforming Σ to Σ':

  `(A a ∈ dom.ispace : a ∈ dom.ispace' ∧ ispace'.a = ispace.a)`

*Proof.* By case analysis on each operation:

- **INSERT**: Creates fresh addresses (AP2) with new content. Existing addresses are not in the allocated set (AP2), so they are untouched. AP0 and AP1 hold.

- **DELETE**: Does not modify ispace at all (AP7). Both AP0 and AP1 hold trivially.

- **REARRANGE**: Does not modify ispace at all. Pure V-space operation (AP8). Both AP0 and AP1 hold trivially.

- **COPY**: Does not modify ispace. Creates V-space mappings to existing I-addresses (AP9). Both AP0 and AP1 hold trivially.

- **CREATENEWVERSION**: Allocates one fresh document address. Does not allocate content addresses. Does not modify existing ispace entries (AP10). Both AP0 and AP1 hold.

- **CREATELINK**: Allocates fresh link address. Does not modify existing ispace entries. Both AP0 and AP1 hold.

Since every operation preserves AP0 and AP1, and the initial state (empty ispace) satisfies AP trivially, AP holds in every reachable state. ∎


## Cross-document isolation

A property implicit in the per-operation analysis but worth stating explicitly:

**AP14 (Cross-document independence).** No operation on document `d₁` modifies the V-space mapping of document `d₂ ≠ d₁`:

  `(A d₂ : d₂ ≠ d₁ : vspace'(d₂) = vspace(d₂))`

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
| AP3 | No address may be freed and re-allocated (no reuse); follows from AP0 ∧ AP2 | introduced |
| AP4 | The allocation frontier within each partition is strictly monotonic; gaps below the frontier are permanent | introduced |
| AP5 | Editing operations modify V-space; they do not modify I-space (dual-space contract) | introduced |
| AP6 | INSERT shifts only V-positions in the same subspace of the same document | introduced |
| AP7 | DELETE does not modify ispace; deletion is rearrangement, not destruction | introduced |
| AP8 | REARRANGE preserves the set of I-addresses referenced by a document; only V-positions change | introduced |
| AP9 | COPY (transclusion) shares existing I-addresses; target document references the same addresses as source | introduced |
| AP10 | CREATENEWVERSION shares text I-addresses between source and new version; no content allocation occurs | introduced |
| AP11 | The span index is append-only; records of content placement persist forever | introduced |
| AP12 | A link's endset I-addresses are invariant under all editing operations | introduced |
| AP13 | A link becomes discoverable again when its endset I-addresses are re-introduced to V-space via COPY | introduced |
| AP14 | No operation on document d₁ modifies the V-space mapping of d₂ ≠ d₁ | introduced |
| AP15 | Deletion of content from its home document does not affect transclusions in other documents | introduced |
| Σ.ispace | ispace : Addr ⇀ Content — the permanent content store | introduced |
| Σ.vspace | vspace(d) : Pos → Addr — per-document mutable arrangement | introduced |
| Σ.spanindex | spanindex ⊆ Addr × DocId — the append-only historical index of content placement | introduced |


## Open Questions

Must the system provide a mechanism to determine, for a given I-address, which documents currently reference it (as opposed to which documents have ever referenced it)?

What must the system guarantee about the retrievability of content at an I-address that is not referenced by any document's current V-space — is direct I-address lookup a required operation?

What invariants connect the span index to V-space mappings, and what filtering obligation falls on queries that use the span index to answer questions about current state?

Under what conditions may a system declare content at a valid I-address to be *inaccessible* (e.g., due to hardware failure), and what properties survive such a declaration?

Must the allocation frontier be recoverable after a crash without loss of monotonicity, and what minimum persistent state is needed to guarantee this?

What permanence obligations, if any, apply to the document identity address allocated by CREATENEWVERSION — must the version graph itself be append-only?

What must the system guarantee about the ordering of allocations across different subspaces within the same document — must text and link allocations be totally ordered, or only ordered within their respective subspaces?
