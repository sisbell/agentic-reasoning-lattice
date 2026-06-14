## What this is

ASN-0036 defines the **storage substrate's core state model**: the split between a permanent content store (Istream) and the mutable per-document arrangements (Vstream) that reference it. It is the foundation on which permanence, transclusion, and attribution all rest — the note from which every editing operation, link, and version mechanism inherits its invariants.

## Design commitments

These are locked in; nothing downstream may violate them.

- **Two address spaces, never merged.** Content identity (I-addresses) and document position (V-positions) are distinct. "The file" is never the content *and* the arrangement at once. Editing touches arrangements only; content is untouched. This is the premise, not a convenience.
- **Content is write-once and never reclaimed.** Once an I-address is bound to a value, both the address and value are fixed for all future states (S0), and the domain only grows (S1). There is no MODIFY/UPDATE/DELETE on the store. Garbage collection of content is *forbidden*, not merely unimplemented — orphaned content (referenced by no arrangement) must persist, because version history depends on it.
- **Identity is by origin, not by value.** Two independent writings of "hello" get distinct I-addresses; a transclusion shares the original address (S4). The structural test for "is this the same content?" is address equality, decided from addresses alone without ever comparing values. This is what lets the system *know* quotation is quotation.
- **References must always resolve.** Every active V-position maps to an I-address actually present in the store (S3). No dangling references in any observable state. Because the store only grows, a once-valid reference can never go bad.
- **Attribution is structural and unseverable.** The allocating document is computable from the I-address itself — `origin(a)` truncates the element field to recover `N.U.D` (S7). No provenance sidecar table; the address *is* the provenance. "Where I read it" (Vstream context) and "where it came from" (Istream structure) are deliberately different.
- **Sharing is unbounded.** An I-address may appear in any number of arrangements and at any number of positions within one (S5). Transclusion is recursive and uncapped by construction.
- **Arrangements are finite, fixed-depth-per-subspace, contiguous from ordinal 1.** Each document's arrangement is finite (S8-fin); within a subspace all V-positions share a depth (S8-depth); the text subspace occupies an unbroken ordinal block `1..n` starting at `[1,1]` (D-SEQ, D-MIN, D-CTG).

Merely conventional (not forced by this note): the specific V-position depth `m` (only `m ≥ 2` is locked); the choice of which subspace number means "text" vs "link"; whether V-positions and the I-addresses they map to share a subspace identifier (explicitly left to the operations layer).

## What must be built

- **A content store** — an append-only association from I-addresses to opaque values, supporting insert-at-fresh-address and lookup, never overwrite or delete.
- **An I-address allocator** — issues globally unique, document-scoped, element-level addresses (`zeros=3`) under the owning document's prefix, honoring the baptism discipline of ASN-0034.
- **A per-document arrangement** — a finite map from V-positions to I-addresses, supporting insert/remove/reorder of V-mappings, that preserves contiguity and referential integrity.
- **A reference-resolution check** — every arrangement write must verify (or structurally guarantee) the target I-address exists in the store at commit.
- **An origin/attribution projection** — pure computation of the allocating document from any I-address; no stored state.
- **A correspondence-run view** — the ability to decompose an arrangement into maximal lockstep runs `(v, a, n)` where V and I advance in step. This is the natural compressed representation of an arrangement and the basis for efficient storage and retrieval.
- **An insertion-position oracle** — given a document, enumerate the valid V-positions for the next insert (the `N+1` positions of ValidInsertionPosition, or the single first position for an empty subspace).

## Implementation approaches

**Content store.** This is textbook append-only journaling, and the note's S0/S1 *are* the journal contract. The cheapest realization that honors the spec is exactly this repo's working substrate: an **append-only journal** (`links.jsonl`-style) of content writes, each record `address → value`, recovered by **replay on load**, with an in-memory index (the `paths.json`-style registry as a recomputable *hint*, not authoritative state — rebuildable from the journal on a miss). The udanax-green analogue is the **granfilade**; note the verified evidence that Green's granfilade uses `MAXBCINLOAF=1` (one entry per bottom crum) — i.e. it did *not* try to compress the store itself, treating it as a flat singleton list. That validates keeping the store dumb and flat. For the Rust target, the durable form is the journal; the in-memory form is a **persistent map** (`im::HashMap`) so that snapshots are cheap and structural sharing across versions is free. Pick the journal as the source of truth always; pick periodic **snapshotting** of the in-memory index only if replay-on-load gets too slow — the snapshot is a hint, the journal is the ground.

Because S0 makes entries immutable, you get a major simplification Lampson would insist on exploiting: **no cache invalidation, ever.** Any cached lookup, any memoized `origin(a)`, any derived index is valid for the life of the system. Caches here are pure performance with no coherence burden.

**I-address allocator.** Allocation is document-scoped baptism (S7a/S7d). The simplest correct mechanism is a **per-document monotonic counter** under the document's `N.U.D` prefix, persisted in the same journal (so allocation survives restart by replay). Uniqueness is then by-construction from ASN-0034's GlobalUniqueness, not something you re-check at runtime. Don't build a global allocation table; the address structure already encodes enough to avoid collisions.

**Arrangement.** Here is the real design choice, and the evidence section is decisive. Two representations:

1. *Position-keyed map* — `V-position → I-address`, e.g. a persistent ordered map (`im::OrdMap`). Simple, directly matches S2/S3, trivial point lookup. But it stores every position explicitly, and an insert in the middle requires renumbering the tail (D-CTG/D-SEQ force contiguity, so positions *do* shift) — O(n) churn per edit.
2. *Run-list (correspondence runs)* — store the arrangement as the S8 maximal-run decomposition `(v, a, n)`. This is the **enfilade/POOM** approach from udanax-green and the one S8 is clearly written to license. A transcluded span of 1000 characters is one run, not 1000 entries. Inserts split a run (+2 runs), deletes trim or split, contiguous typing extends a run in place.

I would pick the **run-list as the durable/in-memory arrangement representation**, with an optional position-index hint over it for fast point lookup. It matches the structure the spec proves exists (S8), and it makes the common cases (transclusion, append, contiguous edits) cheap.

But heed the verified Green evidence on **canonicality**: Green's enfilade *tolerates non-canonical decompositions* — `levelpull` is stubbed out, `recombine` has height floors and merges at most one pair per pass, and same-content arrangements can have different cardinality depending on edit history. The lesson for the builder: **do not make minimal/canonical run-count an invariant.** S8 guarantees the maximal decomposition is *unique as a mathematical object*, but an implementation may carry a coarser (more fragmented) physical decomposition and still be correct, because — per Green's `INV-ENFILADE-CONFLUENCE` — different physical shapes yield identical query results. Treat consolidation (merging adjacent mergeable runs) as an **optional background compaction** (Green even had it probabilistic at 30%), not a correctness obligation on the write path. This is the cheaper mechanism that meets the contract: do opportunistic write-time coalescing (Green's `isanextensionnd`: extend the last run when the new content is suffix-contiguous and same-origin), skip the expensive global re-merge.

Where Green used a 2D enfilade keyed on both V and I to answer V→I *and* I→V (the spanfilade for the reverse direction), decide per the open question on the sharing inverse below.

**Origin projection.** Pure function over the tumbler — no storage, no index. Memoize freely (immutability makes the cache permanent) if profiling shows it hot. This belongs in the address/tumbler module (ASN-0034 territory), not the store.

**Insertion-position oracle.** Derivable from the arrangement's current `V_1(d)` extent — just `min` and `max+1` of the text-subspace ordinal block. O(1) if you track the run-list's first and last run. No separate structure.

## Guarantees to uphold

- **Permanence of content (S0/S1)** — *by construction* if the store is append-only with no delete path. The strongest guarantee, and the cheapest: you uphold it by *not building* the operations that would violate it. Audit the store's API surface for the absence of overwrite/remove, exactly as Nelson's FEBE protocol has no MODIFY.
- **Address & origin uniqueness (S4/S7)** — *by construction* from the allocator's baptism discipline; inherited from ASN-0034, not re-enforced here.
- **Referential integrity (S3)** — *requires active enforcement* at every arrangement write: the target I-address must exist before (or atomically with) the V-mapping that names it. The natural mechanism is **ordering within the journal** — write the content record before the arrangement record in the same atomic commit, so replay never reconstructs a dangling reference. This is the one contract the store's immutability does *not* hand you for free.
- **Arrangement functionality (S2)** — *by construction* if the arrangement is a map (one image per key) rather than a relation.
- **Contiguity, minimum-at-1, sequential block (D-CTG/D-MIN/D-SEQ)** — *requires active enforcement* by the editing operations (out of scope for this note, but this note sets the obligation): insert and delete must renumber to keep the text subspace a gap-free block from `[1,1]`. The run-list representation makes this a local splice rather than a global renumber, but the obligation is real.
- **Sharing multiplicity (S5)** — *by construction*; nothing caps it, so nothing must be built to allow it — only avoid accidentally introducing a cap (e.g. don't key the store by value, which would collapse distinct allocations).

## How it fits

- **Leans on ASN-0034 (tumbler algebra)** for everything addressing: global uniqueness, hierarchical field parsing (the `N.U.D.E` decomposition behind `origin`), ordinal shift and its composition/injectivity laws (the engine of S8's correspondence runs), and the allocator/baptism discipline. This note adds *no* new addressing machinery — it consumes ASN-0034's.
- **Hands to the operations layer** (DELETE/INSERT/COPY/REARRANGE ASNs) the obligation to preserve S2, S3, and the D-CTG/D-MIN/D-SEQ contiguity invariants, plus the insertion-position contract and the subspace-alignment obligation it explicitly defers.
- **Hands to the link/version subsystems** the two-stream separation they depend on: links reference I-addresses (permanent endpoints survive edits); version reconstruction relies on orphaned content persisting (S0's unconditional frame).
- **Sits directly above the durable journal** and directly below every document-mutating and content-addressing capability — it is the waist of the stack.

## Decisions for the builder

- **Run-list vs. position-map for the arrangement** — pick the run-list (POOM/enfilade) if transclusion and large spans dominate; accept that you must then implement split/trim/extend on runs. Use a position-map only for a small-document or prototype path.
- **How canonical to keep run decompositions** — decide up front that minimal run-count is *not* an invariant (following Green). Then choose your compaction policy: write-time coalescing only (cheapest, recommended), periodic background merge, or none. Don't build a fixpoint re-merge loop on the edit path.
- **Reverse index (I→V / the sharing inverse)** — the note leaves the cost bound for "which documents reference this I-address?" open. Decide whether to maintain a **spanfilade-style reverse index** (Green did, as authoritative-looking but really a derived structure) or to treat it as a recomputable hint rebuilt by scanning arrangements. Maintain it incrementally only if reverse queries are common; otherwise leave it out and recompute.
- **Snapshot cadence** — replay-on-load vs. periodic in-memory snapshots of indices. Start with pure replay; add snapshots only when load time demands. Snapshots are hints, never the source of truth.
- **V-position depth `m`** — the note fixes only `m ≥ 2`. Pick the allocation convention (almost certainly `m = 2` for basic text INSERT/DELETE) and document what deeper `m` would buy (nested subdivision, link sub-positions) before foreclosing it.
- **Subspace/I-subspace alignment** — the Green evidence is blunt: nothing enforces that a text V-position maps to a text I-address; `acceptablevsa` is a stub returning `TRUE`. Decide deliberately whether *your* implementation makes subspace alignment a checked precondition on every arrangement-accepting operation, or trusts the insertion paths as Green did. Given a Rust rebuild with no legacy callers, I'd make it a checked precondition — the cost is one comparison, the payoff is eliminating a whole class of silent corruption Green tolerated.
- **`Val` typing** — the note leaves open whether content values are uniform or heterogeneous (text/link/media). Decide whether the store is byte-opaque (simplest; type lives in the address subspace) or carries a typed value domain. Lean opaque: keep the store dumb, let subspace and address structure carry type.
