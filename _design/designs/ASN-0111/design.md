## What this is

READLINK is the link store's primitive read: given a link's *own* permanent address, it returns the complete relationship the link records — its positional sequence of endsets (from / to / type, and any further slots) — or a distinguished "no link here" value. It sits *below* all resolution and search: it discloses the **recorded** structure of one stored object, never its current positions in any document and never anything reachable through it.

## Design commitments

**Forced (downstream cannot violate these):**

- **Links are first-class, independently addressable objects.** A link is read by its own address alone — no containing document, no arrangement, no open-handle or lock context. (Green confirms: the link orgl is reachable by ISA with `NOBERTREQUIRED`, on the same I-address path as span queries, with no document-open precondition.) No part of the system may make reading a link's structure depend on document state.
- **The read is pure, total, and reports absence in-contract.** It changes nothing (frame `Σ'=Σ`), is defined on *every* address, and answers an unallocated address with a distinguished value `⊥`, not an exception or protocol violation. Totality is *forced*, not stylistic: no address-only predicate is sufficient for membership in the store (at the initial state the store is empty), so the read cannot be correctly gated by a precondition — only the outcome settles membership. (Green concurs: an unallocated link address returns the in-contract failure byte `'?'`.)
- **Disclosure is verbatim and unconditional.** The read returns the full recorded structure — the address-spans exactly as stored — with no conversion to current positions, no filtering against any arrangement, and **no dereferencing of nested-link targets**. The link value type does *not* enforce this (a fragment of a stored link is itself a valid link), so completeness and non-flattening are behavioral obligations the implementation must actively honor.
- **Identity is by address, not by value.** Two structurally identical links are distinct objects; the store key is the tumbler address. Never deduplicate or content-address link *values*.
- **Slot position is semantic.** Arity is preserved (≥ 3) and each endset is returned under its own index; the read copies per-slot and must never pool or reorder. Type identity is by `coverage` (an address-set relation), independent of whatever is stored at those addresses — so **ghost-typed links read completely**.
- **A successful read is permanent.** Link values are immutable and append-only; once read, a value is valid for all future states.

**Conventional (chosen, not forced):**

- The *naming* from = slot 1, to = slot 2, type = slot 3 is convention; the *positional* discipline is what is forced.
- The structural screen (`T4-valid ∧ zeros=3 ∧ subspace=s_L ∧ #E≥2`) is an optimization, not part of correctness — the store probe is authoritative.
- Whether to allow arity > 3: the model *permits* it; Green caps at 3. Capping is a legitimate simplification but a real narrowing of the note.

## What must be built

- **A link store** — an address → link-value mapping with membership test and lookup, holding immutable values that are never overwritten.
- **The read primitive** — return the stored value or `⊥`, touching nothing else.
- **An address-analysis module** — pure field projections over a tumbler (zeros, subspace field, element-field length, node-lineage head, user-field width) that powers both the structural screen and the permanence classifier below.
- **A permanence classifier for absence** — decide, from the address alone, whether `⊥` is *permanent* (screen failure, or one of the depth / lineage / user-field families) or merely *current* (the residual class).
- **Recovery** — reconstruct the store on load from the durable record.
- **(Optional) a read cache / hint layer** governed by the classifier.

Home-document identity is *not* a component to build into the value: it is derivable from the link's own address by field projection (Green stores it nowhere in the orgl and recovers it by truncation).

## Implementation approaches

**Organizing decision — factor the raw read as its own layer.** The single most useful engineering takeaway from this note is that READLINK is exactly the *raw* structural read that the udanax-green reference computed internally (`link2sporglset`: pull the I-address spans out of the link orgl with no POOM check) **but never exposed as an operation**. Green's `FOLLOWLINK` immediately fused that raw read with V-resolution against a chosen document's POOM (`linksporglset2specset`, silently dropping unmapped addresses), and that fusion is what produced Green's unexplained "type endset comes back empty when both endpoints are deleted" anomaly. Build the raw read as the bottom layer; let FOLLOWLINK be *readlink ∘ resolve* and search be a separate index path. Put resolution where resolution belongs and nowhere else.

**The link store.** Back it with an append-only journal recovered by replay — the proven pattern both in Green (the permascroll/granfilade) and in this repo's own substrate (`links.jsonl` + `paths.json`, replayed on load). The in-memory index is a persistent (structurally-shared) map (the `im` crate). Choose:
- *Ordered map keyed by tumbler* — preferred. It gives O(log n) point lookup *and* the ordered/range traversal that allocation (frontier = chain maximum), the "links homed at d form a contiguous initial segment" structure, and search all want. One structure serves readlink and its neighbors.
- *Hashed map* — marginally faster point lookup, but it throws away the order the rest of the link subsystem needs. Pick this only if readlink were the sole consumer, which it isn't.

Because values are immutable and append-only, recovery is *pure replay* — no undo log, no compaction needed for correctness. Add periodic snapshotting only to bound load time; the persistent map makes a snapshot a retained root pointer, nearly free.

**Link value and endset representation.** Model the value as a short *positional* sequence of slots (arity small, ≥ 3) — positional indexing is the primitive, so do not key slots by role-name. Each endset is semantically a *set* of spans (membership, not sequence — there is no "j-th span" operator). Represent it as a set, but you may *back* it with a canonical ordering (by span start): Green in fact returns multi-span endsets in ascending I-address order from the enfilade. A canonical order costs a little at construction and buys cheap structural equality, deterministic serialization, and easier cache keying — without promising order as a contract. Spans are stored verbatim; normalize only to well-formedness (positive, well-anchored), never collapsing the "broken, scattered" collections the model permits.

**The read primitive and `⊥`.** The operation itself is a membership test plus a copy out of the persistent map — trivial. The only design content is the codomain: surface absence as an ordinary distinguished result (the in-contract `⊥` / the protocol's failure reply), never as a thrown error. The whole point is that "nothing here" is a valid answer to an all-that-is-there question.

**The structural screen (fast negative path).** A left-to-right, short-circuiting address predicate. Use it as a pre-probe guard *when reads of bogus or untrusted addresses are common* (external queries, speculative walkers) — it rejects impossible addresses without a store probe. Skip it when callers hold known-good addresses, since legitimate addresses always pass it and it only ever saves work on the failing path. Note Green does *not* screen on read (it just probes and returns FALSE on miss, and its read-side address validator is a stub) — screening is your optional optimization, not a fidelity requirement.

**Permanence classification and caching (the hints discipline).** This is the rich part, and it is a textbook "use hints, recompute on a miss" situation:
- **Positive results: cache forever.** Immutability (L12 / LP13) means a cached value is *never* stale; there is no invalidation path. This is the ideal hint. Often the in-memory persistent map already *is* this cache — you may need nothing more.
- **Negative results: do not cache — recompute.** Permanence of absence is *address-computable*: `⊥` is permanent exactly when the address fails the screen or falls in the **depth** family (`#E > 2`), the **lineage** family (node head ≠ the root lineage), or the **user-field** family (`#U ≥ 2`). The classifier is the same field-projection machinery as the screen plus three more tests. Recomputing the verdict (a handful of projections) is cheaper than a store probe, so the fast path is: classifier says *permanently absent* → return `⊥` with no probe; classifier says *residual class* (screen-passing, `#E=2`, lineage-head = root, `#U=1`) → probe the store, and on a hit, positive-cache the value.
- **The one correctness landmine:** never cache `⊥` for a residual-class address. Every such address is allocatable in some future history; a cached `⊥` there becomes a lie that breaks read stability for a later reader. This is the only place caching is unsound, and the classifier exists precisely to fence it off.

**Concurrency.** readlink over an immutable, append-only, persistently-shared store is lock-free: a reader holds an immutable root (a snapshot) and is untouched by concurrent appends — MVCC for free. This matches Green treating link reads as global, lockless lookups even while it gated *content* reads.

## Guarantees to uphold

- **Permanence / immutability of a successful read** — *by construction* from append-only, frozen values; uphold simply by never mutating or overwriting.
- **Totality (always an answer)** — *by construction* via the distinguished `⊥`; uphold by making absence a normal return.
- **Completeness, verbatim** — *actively enforced*. The type permits fragments, so "return the whole thing" is a behavioral obligation, not a type guarantee; make it a test target.
- **Nesting locality (never dereference a covered link)** — *actively enforced* as a layering rule: the read consults the single entry and nothing the endsets cover. This is easy to violate by "helpfully" resolving nested targets. The note's branched-history witness (two states agreeing on the read address, differing at a covered address, must read equal) is a ready-made property test.
- **Independence from arrangement (recorded, not resolved)** — *by construction* if the read never calls into the resolution layer; this is exactly the boundary Green blurred, so enforce it as a hard layering rule.
- **Role / slot preservation and arity** — *by construction* if you keep positional structure and copy per index; never pool or reorder.
- **Determinacy / stability over time** — *by construction* for the success branch (immutability); for the failure branch it holds only for provably-permanent `⊥`, which is *why* the caching discipline above is itself a guarantee.
- **Identity by address** — *by construction* from keying the store by address; uphold by never deduplicating by value.

## How it fits

- **Leans on** the link store and its invariants (ASN-0043: the address→value map, link/endset shape, immutability L12, type-by-coverage L8, ghost types L9, reflexive span L13, span generality L4); the tumbler/span algebra (ASN-0034: T4 validity and field projections for the screen and home-derivation, span well-formedness, coverage); and the reachable-state / allocation / persistence frame (ASN-0047, ASN-0093, ASN-0098: the state shape, link allocation, unconditional persistence LP13, the substrate-emittable-address structure behind the depth family, and the frontier/chain structure behind residual-class allocatability).
- **Hands to / is leaned on by** FOLLOWLINK — which is readlink's raw structure *plus* resolution against a chosen arrangement (Green's `link2sporglset` → `linksporglset2specset` split, done right by keeping the two as separate layers); FINDLINKS / COUNT — a *sibling*, not a consumer: it reaches links through the content-region index (the spanfilade), not through readlink; and any consumer of compound / faceted / nested structure — which reads a to-set as *addresses* via readlink and then chooses whether to recurse, recursion being the consumer's decision, never readlink's.

Position in the stack: readlink is the floor of the link-read tower — the primitive that follow, search, and count are defined against.

## Decisions for the builder

- **Whether and where to run the structural screen** — as a pre-probe fast path, as a boundary guard for untrusted addresses, or not at all. Driven by your read mix (trusted handles vs. external queries).
- **Endset backing: pure set vs. canonically-ordered set** — semantics is membership either way; canonical order buys cheap equality, stable serialization, and easier caching at a small construction cost. Recommended: canonical order under set semantics.
- **Store flavor: ordered vs. hashed map** — a system-wide call (allocation and search want order); readlink itself is happy with either. Recommended: ordered, keyed by tumbler.
- **Cache footprint** — whether to keep a positive read cache beyond the in-memory map (often unnecessary), and its eviction policy (purely a memory decision — eviction is never a correctness issue since values are immutable). Recommended default: rely on the persistent map, add the address-computable permanence classifier as the pre-probe fast path, and keep **no** negative cache.
- **How to surface `⊥`** — a distinguished result value vs. an optional/absence type vs. a non-error status. The note requires only that it be in-contract; the shape is yours.
- **Whether to support arity > 3** — variable-arity (≥ 3) is faithful to the model and barely harder; fixed-triple is simpler and matches Green. Recommended: variable-arity.
- **Whether to validate address shape defensively on the boundary** — Green trusts its allocator and leaves the read-side validator a stub (shapes are emergent, not enforced). If you accept addresses from outside the allocator, validate via the same screen module; if every address comes from your own allocator, trusting it is defensible.
