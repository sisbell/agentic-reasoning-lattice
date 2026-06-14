## What this is

ASN-0116 defines **INSERT** — the substrate's primary write path: the operation that brings new content into existence inside a document. It mints permanent identity for the new material, splices it into one document's sequence at a chosen point, displaces the following material to make room, and records who created it — without disturbing the content's existing identities, the links that point at them, or any other document that shares them.

## Design commitments

These are locked in for everything downstream; violating them breaks the model, not just this operation.

- **Two-layer state, kept uncontaminated.** Content lives in a global, append-only store keyed by permanent *I-address*; arrangement is a *per-document* map from ordinal *V-positions* to I-addresses. Almost every invariant INSERT upholds is a statement that a change in one layer must not leak into the other. This split is the single most load-bearing decision.
- **Identity is by origin, never by value.** Allocation consults *position*, never *content*. Inserting identical bytes twice yields two distinct addresses. There is no content-addressing, no hashing, no deduplication anywhere on the write path — and any "optimization" that collapses equal-valued content to one identity is forbidden, because a link to one occurrence would silently bind the other.
- **Content is permanent and write-once.** The store only grows; an existing address never changes value and is never reused or freed. INSERT is *purely additive* on content, links, and the entity set.
- **V-positions are slots, not containers.** A position binds no permanent content. After an insert, the slot that "held X" now resolves to new content and X has moved to a higher slot. Permanence attaches to the I-address; the arrangement re-coordinates *around* fixed identity. This is forced, and it is the whole reason links survive edits.
- **Allocation is monotonic and document-scoped; a span is contiguous.** New addresses for one document advance past every address that document already owns, and an *n*-unit insert occupies *n* consecutive addresses on that document's content chain. The contiguity and origin-stamping are forced; the *mechanism* that achieves them is not (see Decisions).
- **The displacement is uniform, confined, and gap-free.** Following positions in *the same subspace of the same document* all shift by exactly *n*, preserving their relative order; nothing before the cut moves, nothing in another subspace moves, and no other document moves. Density (a contiguous, gap-free ordinal run) is preserved — no gap opens, no two positions collide.
- **Provenance is coupled to allocation, not deferred.** Each new address is bound to its inserting document within the *same atomic unit* that allocates and places it. The record set only grows.
- **Origin is recoverable from the address itself.** The inserting document is encoded in the address's prefix (foundation addressing). The provenance relation is therefore *derivable*, not primary — a fact that turns one whole subsystem into a cache (see below).

*Merely conventional* (not forced): the `shift(t,0)=t` boundary convention; the proof's decomposition of INSERT into a contraction-then-extension pair. That sequencing is how the spec earns its invariants — **the implementation may fuse the steps into one displacement** as long as the net effect and atomicity hold. The note itself says the arrangement rewrite "is not itself one of these atomics."

## What must be built

- **A content store** that maps addresses to values, accepts only writes to addresses that do not yet exist, and never mutates or removes an entry.
- **An allocator** that, given a document, yields the next fresh address on that document's content chain, and for a span yields *n* contiguous fresh addresses — derived from current state, origin-stamped, monotonic.
- **A per-document arrangement** that resolves the document's ordered V-positions to I-addresses, and supports an in-the-middle insert: place *n* new units at a valid point and displace the following units uniformly.
- **A displacement mechanism** that shifts the suffix by *n*, leaves the prefix and all other subspaces/documents untouched, and stops at the subspace boundary.
- **A provenance/reverse-lookup facility** that answers "which document originated this address" and "which documents/links touch this content" — the second of which is *not* recoverable from the address and must be indexed or scanned.
- **A precondition checker** for the insertion point: correct subspace (content), matching depth, and seated at or one-past an existing slot so no gap can open; plus the document's current length *N*.
- **An atomic-commit-and-recovery binding** that makes the whole composite (allocate + displace + record provenance) all-or-nothing and survivable across a crash.

## Implementation approaches

**The unifying move (do this first).** Make an **append-only journal of edit operations** the single ground truth, and treat the content store, the arrangements, the provenance relation, and every reverse index as *derived projections rebuilt by replay on load*. This is exactly this repo's working substrate (`links.jsonl` replayed, `paths.json` as registry) and exactly the spirit of the udanax permascroll: log the operation, recompute the views. One INSERT becomes **one journal record** — `(document, position, content, allocated-start)` — which makes the multi-step composite atomic for free (the record either lands or it doesn't) and makes recovery a replay, not a repair. Everything below is then a *cache* over this journal.

*Tradeoff — log the operation vs. log the state mutation.* Logging the operation is compact and naturally atomic per INSERT; the allocated addresses can even be recomputed (query-and-increment is deterministic given replay order). I would nonetheless **store the allocated start in the record** so replay is a verification rather than a re-derivation, decoupling the on-disk format from allocator internals — a Lampson hint that costs a few bytes and removes a long-term coupling.

**1. Content store.** The proven structure is the **granfilade** — an ordered tree keyed by I-address. In Rust over `im`, an **immutable persistent ordered map** keyed by tumbler address is the direct analog; immutability is the commitment, so a persistent structure gives it by construction and gives you near-free *versioned snapshots* (structural sharing) — valuable for a versioning hypertext system. Because content is write-once, you may also keep the in-memory map purely as a replay cache over the journal and never persist it separately. Do **not** reach for content-addressed storage here: it is precisely the deduplication the origin-identity commitment forbids. (You *could* dedup *physical bytes* under distinct addresses as a storage trick, but it buys little and complicates the simple thing — skip it.)

**2. Allocator.** udanax-green's verified mechanism is **stateless query-and-increment**: find the greatest existing address under the document's content scope and return its successor — *no global counter anywhere*. Three options:

- *Query-and-increment (proven).* Each allocation is a bounded max-query on the store. Robust, derives from ground truth, identical across sessions/replays. Cost: a tree query per insert.
- *Per-document hint cache (recommended).* Cache "next address for document *d*" as a **Lampson hint** — authoritative-free, recomputable on a miss by querying the max. Makes the common case (sequential typing/append) O(1) and the rare case (cold cache, crash) correct by recomputation. This is the right blend: the spec forbids only *authoritative* duplicate counter state, not a recomputable hint.
- *Persisted per-document counter.* Simplest mental model but introduces authoritative duplicate state you must persist and recover in lockstep with the store — exactly the kind of duplicate truth to avoid. Reject unless profiling somehow demands it.

Note the contiguity caveat from the evidence: interleaving a link-creation (which also draws from the allocator) between two text inserts breaks text contiguity. INSERT alone never does; a builder batching a span should allocate the whole run in one step.

**3. Arrangement + displacement.** The spec models the arrangement as a *dense per-unit* map V→I. **Do not implement it literally per unit** — that makes a front-insert an O(length) rekey. Treat the per-position map as a *denotation* and represent it as a **piece sequence** over the immutable content store (this is what a piece table / rope is, and it is what the POOM enfilade is at heart):

- *Flat piece table (recommended start).* A sequence of pieces, each naming a contiguous I-address run; V-position is the running offset, *computed, never stored*. Insert = split at most one piece and add one. **The "shift of all following V-positions" becomes free** — later pieces simply have higher running offsets. Cost: O(pieces) to splice the array; pieces stay few because contiguous same-origin runs **coalesce** (udanax-green does exactly this — sequential typing costs +2 structural nodes for the first character and +0 thereafter). Simple, correct, great for moderate documents.
- *Persistent displacement-tree / rope (graduate to this at scale).* A balanced tree of pieces carrying *relative* offsets in each subtree — the modern restatement of the POOM enfilade. Insert is O(log n) with no suffix rekey, and over `im`-style persistence you get versioned arrangements with structural sharing. More complex; pick it when large documents and front-inserts show up in profiles.
- *Explicit V-keyed persistent map (avoid except as a reference oracle).* Mirrors the spec one-to-one and is trivially correct, but the displacement is an O(suffix) rekey. Useful as a test oracle to differentially check the piece representation; not the production choice.

The udanax displacement trick worth importing wholesale is the **two-blade cut**: bound the shift between the insertion point and the *next subspace boundary*, so a content insert provably never perturbs link positions. In the abstract positional model this confinement is automatic (the ordinal shift fixes the address prefix); in a tree/displacement representation it is a **deliberate guard you must implement** — the evidence is explicit that INSERT's subspace isolation there is an intentional second-blade boundary, not an accident.

**4. Provenance and discoverability — two different things, built differently.**

- *Origin provenance ("who created this address").* Recoverable from the address prefix. So the relation *R* is a **derivable view, not primary state** — decode it from the address, or materialize a small reverse index as a hint. Don't persist it as authoritative duplicate state.
- *Discoverability ("which documents/links touch this content").* **Not** recoverable from the address (transclusion can place a foreign address into another document), so this genuinely needs a **reverse index from content to arrangements/links** — the **spanfilade / DOCISPAN** structure, maintained append-style on insert, or recomputed by scanning arrangements on load. Maintain-incrementally for query speed; keep recompute-by-scan as the recovery path, since the journal makes it rebuildable.

On *resolving links across the shift*: follow udanax-green's **pull model** — links store I-addresses and are resolved to current V-positions on demand by walking the arrangement. INSERT then needs to do *nothing* to links; their resolved positions reflect the new layout automatically, and they survive because no I-address was removed. The one subtlety the note surfaces (IP4/IP6): a freshly allocated address can fall inside a pre-existing link's coverage (a "ghost" reference), so an insert can *add* witnesses and even resurrect an orphaned link. Because resolution is pull-based, this is handled correctly for free at query time — but a builder who *caches* discoverability must invalidate/extend it for any link whose coverage meets the new run.

**5. Atomicity and recovery.** Bind 1–4 with the journal from the unifying move. The composite (n allocations + displacement + n provenance records) must be **one commit**; a crash between allocation and provenance would orphan an address, which the spec forbids. Two viable shapes: *(a)* one operation record per INSERT, with the derived stores rebuilt by replay (recommended — simplest, atomic by construction, matches the repo); *(b)* a write-ahead log of finer mutations with a commit marker (more machinery, warranted only if other operations need sub-operation durability). Either way, **the derived structures are caches** — lost ones are rebuilt, never repaired.

## Guarantees to uphold

*Hold by construction* given an append-only store, monotonic positional allocation, and a positional shift:
- **Permanence / immutability** — content never overwritten or removed (append-only store).
- **Origin identity & freshness** — distinct addresses per allocation event regardless of value (monotonic allocation, single writer).
- **Ordering & density** — suffix keeps relative order; the run stays contiguous and gap-free (uniform shift).
- **Document isolation** — other documents' arrangements and resolved content are untouched (you write exactly one arrangement and append to shared immutable content).
- **Link survival** — every prior link designates exactly the same content afterward (links name I-addresses; INSERT removes none).
- **Subspace confinement** — automatic in the abstract address model.

*Require active enforcement:*
- **Freshness under concurrency** — two writers querying the same max collide; needs serialization (the note flags this as open).
- **Provenance coupling** — the origin record must commit in the *same atomic unit* as allocation; enforced by the single-commit design.
- **Atomicity of the composite** — a partial INSERT must not leave a gap or an unprovenanced address; enforced by journaling/commit.
- **Subspace confinement in a tree representation** — the second-blade boundary is an explicit guard you must code (only the abstract model gets it for free).

## How it fits

INSERT sits in the **operations layer**, composing foundation primitives and handing a maintained arrangement to everything above:

- **Leans on:** content allocation (K.α / ASN-0093) for fresh origin-stamped addresses; the arrangement contraction/extension and the post-insertion shift family (K.μ / ASN-0082's I3) for the displacement spec; provenance recording (K.ρ / ASN-0047); the tumbler address algebra and ordinal shift (ASN-0036/0058/0034); the reachable-state invariant bundle (ASN-0047) that delivers well-formedness of the post-state in one appeal; and link persistence/discoverability (ASN-0098) for the link-survival and weakest-precondition results.
- **Hands to:** the sibling editing operations (DELETE, REARRANGE, transclusion/COPY) that share the same K-vocabulary and the same two-layer discipline; link operations that resolve against the arrangement INSERT maintains; and content/link discovery queries that consume the reverse index.

## Decisions for the builder

- **Allocation mechanism:** query-and-increment vs. a recomputable per-document hint cache vs. a persisted counter. *Pick the hint-cached query* — fast common case, correct by recomputation, no authoritative duplicate state.
- **Arrangement representation:** flat piece table vs. persistent displacement-tree/rope vs. explicit per-unit V-map. *Start with the coalescing piece table* (V-positions computed, shift implicit); *graduate to the rope* when large-document front-inserts appear; keep the per-unit map only as a differential test oracle.
- **Do you coalesce contiguous same-origin runs?** Yes — it keeps piece/node count near the number of edit *sessions*, not characters.
- **Is provenance materialized or decoded?** Decode origin from the address (or keep a hint index); reserve real indexing for the *discoverability* direction, which is not address-recoverable.
- **Discoverability maintenance:** incremental reverse index vs. recompute-by-scan on load. *Maintain incrementally for queries, keep scan as the rebuild path.* If you cache discoverability, decide how to extend it for links whose coverage meets the new run (or stay pull-based and skip the problem).
- **Atomicity unit:** one operation record per INSERT (recommended) vs. a finer write-ahead log with commit markers.
- **Do you store the allocated start in the journal record, or recompute it on replay?** *Store it* (replay becomes verification, format decouples from allocator internals).
- **Concurrency / serialization (genuinely open in the note):** single-writer-per-document vs. per-document lock vs. optimistic-with-retry. *The simple thing is per-document serialization* — it makes freshness hold without a global authority; revisit only if multi-writer throughput on one document becomes a real requirement.
- **Content granularity:** what a single content unit *is* (byte, code point, grapheme, opaque blob) — fixes addressing density and the meaning of "length *n*."
- **Subspace-boundary guard:** in a tree representation, where the second blade lives and how the next-subspace ceiling is computed.
