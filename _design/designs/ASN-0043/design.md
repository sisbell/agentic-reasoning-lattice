## What this is

ASN-0043 defines the docuverse's **connection primitive** — the link subsystem. It adds the third system-state component, the link store `Σ.L`, and fixes the *dual-primitive* shape of storage: every stored thing is either content or a link, with no third category. Links are first-class, permanently-addressed, owned, immutable connections among arbitrary spans of the tumbler address space.

## Design commitments

**Forced — downstream design cannot violate these:**

- **Identity is by address, never by value.** A link's identity is the address the allocator minted for it. There is no find-or-create, no deduplication, no injectivity constraint: two links with identical from/to/type endsets are distinct objects, independently owned and removable. The payload never participates in identity. (This is the inverse of content-addressing, and it is deliberate.)
- **Links live in a distinct, disjoint address subspace `s_L`.** The address is self-describing — a link is told apart from content by the subspace field of its own tumbler, not by a side flag. Disjointness from content's `s_C` is then automatic (T7) — though only over content the content layer actually keeps in `s_C` (see *Guarantees to uphold*). This *is* the dual-primitive architecture.
- **Ownership is by address, independent of what the link connects.** `home(a)` is field-projected from the address alone; the endsets never enter the computation. Residence ≠ reference — this single decision is what permits annotation without modifying (or seeking permission on) the annotated document.
- **Links are immutable and append-only.** Creation is the only write. The store grows monotonically; no entry is ever changed or removed. The whole-state `StateExtension` relation is the journaling discipline stated as an invariant.
- **A link is a slot-indexed sequence of ≥ 3 endsets; an endset is a *set* of spans.** Slot index (from/to/type) is a primitive of the model; span *order within* an endset is not — access is by membership only. Link equality is component-wise.
- **Type is itself an endset of addresses, matched by coverage, not by content.** Whether two links share a type is decided by the *address set* their type endsets cover, never by dereferencing those addresses. Ghost types are legal — naming the address *is* defining the type. Type hierarchy is tumbler prefix containment, requiring no separate hierarchy structure.
- **Links are non-transcludable.** Content is shareable across arrangements; links are not. No arrangement may ever map a position to a link address.
- **Endset spans are otherwise unrestricted.** Cross-document, intra-document, cross-subspace, and dangling-into-nonexistent-content are all valid; link addresses are themselves valid span targets (link-to-link).

**Conventional — not forced:**

- The standard triple and slot numbering (from=1, to=2, type=3); the model admits arity > 3 (the reference implementation fixes 3).
- "from = source, to = destination" is a *type-level* interpretation (L7), not a structural invariant.
- The concrete integer values chosen for `s_C` and `s_L`.

## What must be built

- A **link store**: create and read, never update or delete; reconstructable after restart.
- An **address allocator**: per home document, minting fresh monotone addresses in `s_L` under the document prefix; globally unique; *requiring the home document to already exist*.
- An **endset representation**: a set of spans exposing membership and coverage, with no positional span accessor.
- A **link value**: a slot-indexed ≥3-endset sequence with positional slot access and component-wise equality.
- **Subspace discrimination**: telling a link address from a content address from the address itself.
- A **type-matching and hierarchy capability**: coverage-equality for same-type, prefix-range matching for subtypes, never dereferencing the type address.
- A **link search index**: given a slot and a query span, find links whose endset in that slot *overlaps* the query; intersect across constrained slots by link identity.
- **Reflexive addressing**: link addresses usable as span targets exactly like content addresses.
- **Recovery**: deterministic rebuild of store and indexes.
- (Handed upstream) a **non-transclusion guard** in the arrangement layer.

## Implementation approaches

**Link store persistence — append-only journal, recovered by replay.** The note's invariants make an append-only journal the right fit rather than a convenience: because links are immutable and the store is append-only (L12/L12a), the journal *never* needs rewriting — no update records, no tombstones, no compaction for correctness. Each record is `(address, endset-sequence)`; load replays them into an in-memory map. The journal is authoritative; the map is a cache over it. Replay cost grows with history — bound it with periodic snapshots (checkpoint the map plus a journal offset; recover = load snapshot + replay tail). Treat the snapshot as a *hint*: recomputable from the journal, so a missing or stale one only costs more replay, never correctness.

The tempting wrong turn is **content-addressing** (key by a hash of the endset value). That is correct for *content*, but forbidden here: identity is by address, and the store must not *enforce* injectivity (non-injectivity is permitted — L11b), so keying by a hash of the endset value would collapse distinct links into one. Links are precisely the case where you must *not* derive the key from the payload — the allocator assigns it.

**Address allocator — stateless query-and-increment, or a cached high-water hint.** Green's proven approach is a *stateless* query-and-increment: the next address is `max existing sibling under home.0.s_L.* + 1` (first link seated at the document's link-subspace child), computed fresh each time, with no counter object. Its virtue is Lampsonian — the store *is* the counter, so there is no duplicate state to drift. Its cost is a "max-under-prefix" query per allocation. The alternative keeps a per-home high-water map in memory; I'd pick this, but as a **hint rebuilt from the journal on load** rather than authoritative state — making the common case (allocate) O(1) while the journal remains the source of truth — an index/registry as a recomputable hint over the authoritative journal. Either way:

- *Document-scoping is the concurrency boundary.* The verified Green behavior bounds each search to the document's own link subtree, so allocations in different documents never contend; allocations in the *same* document serialize through one cursor. That gives a natural sharding/locking granularity: per-home-document serialization, parallel across homes.
- *The home-existence precondition is real and must be enforced here.* Green gates link allocation on an exact-match check that the home document is registered. Honor it: refuse to mint under an unregistered document prefix.
- *Do not reify "allocation events."* The verified implementation has no first-class event or chain object — uniqueness is just monotone increment plus the journal record. L11a's "distinct allocation events" is spec vocabulary; don't build an object for it.

**Endset and coverage — store the spans verbatim, derive coverage for matching.** Immutability forces you to keep the *as-created* span decomposition (the worked example keeps `Θ_split ≠ Θ_single` as values though they are coverage-equal). So do not canonicalize the stored form; compute coverage only as a query-time projection. This means carrying two distinct notions of equality and keeping them separate: **extensional** set equality decides whether two endsets are the same *value*; **coverage** equality decides whether two links share a *type*. Conflating them over-discriminates types.

**Type matching and hierarchy — range matching over tumbler order, not a type graph.** A type query rooted at prefix `p` is a half-open interval `[p, shift(p,1))`, which is exactly `p`'s subtree (T5). Subtyping is therefore *free*: it is the tumbler ordering itself — confirmed at the implementation level, no separate hierarchy structure. Build type queries as interval-overlap tests, the same machinery as any span query (the uniformity the third endset buys you). Ghost types fall out for nothing: since matching is on the address and never fetches what is stored there, the address need not resolve.

**Link search — a spanfilade-style range index, scan when small.** The fundamental query is "which links touch this region of address space, in this slot?" — a stabbing/interval-overlap query. The proven structure is the spanfilade: a per-slot index from address ranges to the link IDs whose endset in that slot covers them. A query overlaps the index to get candidate IDs per constrained slot, then intersects the candidate sets *by link identity* (the verified `intersectlinksets` compares link addresses, not span structures; matching throughout is coverage-overlap, never span equality — building the index on exact spans would over-discriminate). In Rust this is an interval map per slot; a persistent/immutable ordered map gives structurally-shared snapshots and cheap checkpoints. Crucially, **the index is a hint over the journal** — fully rebuildable by replay — so it need not be persisted transactionally with the store; that decouples durability (journal) from query performance (index). For the bootstrap/test/small-corpus case, a brute-force scan over all links is correct and trivial; add the index when scale demands it rather than before.

**Physical layout — one journal or two.** The spec separates content and links *logically* (disjoint subspaces); physically you may share one append-only journal carrying both content-write and link-create records (Green's single granfilade with two leaf types — one allocator domain, one recovery path) or keep a dedicated link journal separate from content. Disjoint subspaces guarantee no address collision either way, so this is a pure operational-simplicity call. Treat the self-describing address as the single source of truth for "content vs link"; a redundant leaf-type tag (as Green carries) is then only a cheap consistency check, not authoritative.

## Guarantees to uphold

| Guarantee | Holds by… |
|---|---|
| **Permanence** (L12) — addresses and values never change or vanish | *Construction* — append-only-immutable journal; provide no update/delete API. |
| **Uniqueness** (L11a) — distinct creations get distinct addresses | *Construction* — monotone per-home allocation; never reissue an ordinal. |
| **Ownership derivability** (L2) — home computable from the address | *Construction* — pure field projection. |
| **Home existence** (L1a) — a link's home document is allocated | *Active enforcement* — the document-existence gate at allocation time. |
| **Subspace disjointness** (L1d, L14) — links and `s_C`-resident content never collide | *Construction (partial)* — if the allocator keeps links in `s_L`, T7 gives disjointness for free over `s_C`-resident content; full content-side disjointness is a cross-layer dependency — see below. |
| **Type-by-address / ghost permission** (L8, L9) — matching never dereferences the type | *Construction* — search matches on address coverage and never fetches type content. |
| **Endset order-independence** (L5), **slot distinction** (L6) | *Construction* — representation choice (no positional span accessor; slot-indexed sequence). |
| **Non-transcludability** (L14a) — no arrangement points at a link | *Active enforcement, **and not here*** — see below. |

The one guarantee this note states but **cannot itself enforce** is non-transcludability. It is discharged by the arrangement layer's referential-integrity check restricting V-position images to the content subspace. The link layer's job is to keep links in `s_L` (so the upstream check has a clean subspace boundary to test); the actual exclusion lives in the arrangement/edit operations. Flag this at the layer seam so it is not silently dropped.

Subspace disjointness is a second cross-layer dependency the table only half-discharges. The note proves it solely over the `s_C`-resident slice of content (L14: `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`). The link layer holds up its end by keeping every link in `s_L`; but full link/content disjointness holds only if the content layer keeps *all* content in `s_C`. Extending disjointness to the whole of `dom(Σ.C)` would require a global content-subspace constant — which the note lists as an **open spec question, not an invariant**. So treat content-side `s_C`-residence as a contract owed by the content layer, and do not over-claim universal disjointness from inside the link layer.

## How it fits

- **Leans on ASN-0036 (two-space model)** — content store `Σ.C` and arrangements `Σ.M`. This note adds the third state component and reuses ASN-0036's field-projection wholesale: `home` is literally the same formula as content's `origin`, applied to a link address.
- **Leans on ASN-0034 (tumbler algebra)** — for essentially all of its machinery: subspace disjointness (T7), the prefix relation and intrinsic comparison, allocator discipline (T10a), span well-formedness (T12), global uniqueness, contiguous subtrees (T5), and displacement/shift. The "hierarchy for free" result is entirely T5 plus prefix ordering. (Its `PrefixSpanCoverage` lemma is really span-algebra machinery borrowed into the link note — a natural home for it is the span/tumbler-algebra layer, not the link ontology.)
- **Hands the non-transclusion contract up** to the arrangement layer.
- **Hands the store and index up** to the link-operations / query layer — MAKELINK plus the find / count / paginate / retrieve-endsets family — and provides, via reflexive addressing (L13), the substrate on which compound and faceted-link structures are later defined.
- It sits **above** the address algebra, **beside** the content store, and **under** link operations and search.

## Decisions for the builder

These are genuinely open *implementation* choices — distinct from the note's own spec-level open questions (global content-subspace constant, transclusion invariants, compound-link well-formedness, etc.), which you should not conflate with these:

1. **One physical journal/index for both primitives, or two** (shared granfilade-style log vs. a dedicated link journal). Disjoint subspaces make both correct; choose on recovery and operational simplicity.
2. **Allocator: recompute-max each time vs. a cached per-home high-water hint** rebuilt from the journal on load. Both correct; the hint trades recomputable duplicate state for O(1) allocation.
3. **Index eagerly (spanfilade range index) vs. brute-force scan**, and whether to snapshot the index or always rebuild it from the journal.
4. **Snapshot/checkpoint cadence** — the knob that bounds replay time on recovery.
5. **Coverage materialization** — merge endset spans into a canonical interval set at index time, vs. keep raw spans and test overlap directly. This affects index size and query cost but must never alter the *stored* (immutable) value.
6. **Arity policy and where the conformance gate lives.** The model admits N ≥ 3; the reference path fixes 3 — *and can silently emit a two-endset / empty-type link* when the client sends an empty type specset (verified). A conforming store excludes these, so decide explicitly to reject *only* a missing or empty **type** endset (slot 3) **at the create boundary** (the right place to put the check) rather than letting non-conforming links into the store. Do *not* generalize the check to from/to: L3 constrains slot 3 alone, and empty from/to endsets are conforming — L9's witness is `(∅, ∅, {(g, …)})` and L7's heading link populates a single content endset. Note the spec/impl gap: Green's `setlinkvsas` always populates from/to, but the model permits them empty — build to the model.
7. **Concurrency granularity** — home-document-level serialization for allocation (free from the single per-home cursor), with full parallelism across distinct home documents.
8. **Discriminator policy** — rely solely on the self-describing address subspace, or also carry a redundant leaf-type tag as a cheap consistency check.
