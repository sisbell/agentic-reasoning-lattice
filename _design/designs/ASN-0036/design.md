## What this is

The Strand Model defines the substrate's core state architecture: the split between a **permanent, append-only content store** (Nelson's Istream) and a **family of mutable per-document arrangements** (the Vstream) that reference it, together with the invariants binding the two. It is the floor every editing, linking, versioning, and transclusion capability stands on.

## Design commitments

These are locked in for the whole system. I separate what the note *forces* from what it constrains but defers to the operations layer.

**Forced — downstream design cannot violate these:**

- **State is exactly two components.** Content identity and document position are separate address spaces: one content store `C` plus a family of arrangements `M(d)`. A conventional "the file is the content is the arrangement" merge is ruled out at the architectural root.
- **Content is write-once and append-only (S0, S1).** Once a value is stored at an address, neither the address nor the value ever changes or disappears; the store only grows. There is no update/replace/delete-of-content operation, anywhere, ever.
- **Identity is by origin, not by value (S4).** Two independent writes of the same bytes get *distinct* addresses; transclusion is address *sharing*; a detached copy is a *new* address. The "are these the same content?" test is address equality — decidable without ever comparing values.
- **Arrangements are functions; content is shared without bound (S2, S5).** Each V-position resolves to exactly one I-address, but a single I-address may be referenced unboundedly many times, across documents and within one. No injectivity, no sharing cap.
- **References resolve, and stay resolved (S3 + S1).** An arrangement may only point at content that exists; once a reference is valid it can never dangle, because the target can never be removed.
- **Attribution is structural, not stored (S7).** The originating document is *computed from the address itself* (truncate the element field). It is permanent and unseverable because the address is. "Where I am reading" (Vstream) and "where this came from" (Istream) are deliberately different.
- **Content persists regardless of reference (S0 frame).** Unreferenced ("orphaned") content is never reclaimed. Persistence is unconditional, not refcount-gated — history depends on this.
- **An arrangement is structurally a finite set of correspondence runs (S8, S8-fin).** The V→I map decomposes into maximal blocks where V and I advance in lockstep, and that maximal decomposition is *unique as a mathematical object*. This is the formal license for run/enfilade-style storage.

**Constrained but deferred — locked for the text subspace, but the *operations* layer enforces them, not storage:**

- **Text V-positions are a gapless `1..n` block starting at `[1,1,…,1]` (D-CTG, D-MIN, D-SEQ).** Well-formed text arrangements have no holes and a fixed minimum. These are invariants on states, but they hold only if every edit preserves them.
- **V-position depth ≥ 2 is forced (S8a); the exact depth `m` is a one-time allocation convention,** not a strand-level commitment.
- **V/I subspace alignment (a V-position's subspace matching its I-address's structure) is an operations-layer obligation, *not* a state invariant.** The strand does not assert it, and — per the udanax-green evidence — nothing in storage will enforce it.

## What must be built

Described functionally:

- **A content store** that, given a fresh address, records a value; answers lookup and domain-membership; and *offers no way to mutate or remove* an existing entry.
- **An arrangement store, per document,** that maps V-positions to I-addresses; supports add / remove / reorder; enumerates active V-positions; and answers positional lookup.
- **An address allocator** (leaning on the tumbler foundation) producing fresh, globally-unique, document-scoped, element-level I-addresses.
- **A referential-integrity gate** ensuring every arrangement write targets content already in (or created in the same step as) the store.
- **An origin function** that recovers the allocating document from any I-address by pure structural projection.
- **A run-decomposition capability** that recognizes/produces the maximal correspondence-run partition of an arrangement (for compact storage, transmission, and queries).
- **Subspace discrimination** (read the first component) and, at the operations layer, **contiguity maintenance** for the text subspace and **subspace-alignment** as a precondition storage won't check.
- *(Optional, workload-driven)* a **reverse-reference capability**: given an I-address, who references it.

## Implementation approaches

### The content store

The note *derives* "append-only log" from S0 + S1, so the structure chooses itself: **an append-only journal of content writes, recovered by replay on load.** Atomicity and crash recovery come from the journal for free (write the record, then it's durable; a torn tail is discarded on replay). This is precisely this repo's working substrate (`links.jsonl` + replay) and precisely Green's permascroll. Take it.

- **Index as a recomputable hint, not authoritative state.** Keep an in-memory map `I-address → value` (or `→ journal offset`) to make membership tests (the hot S3 check) and lookups fast. The journal is the truth; the index is rebuilt by replay on startup and after a miss. In Rust this index can be an `im` persistent map so checkpoints share structure; the durable backing is still the flat journal.
- **Immutability by construction, not by check.** Don't guard mutation at runtime — *don't provide the operation.* Green's protocol has no MODIFY command and the absence is structural; mirror that. A store that only ever appends cannot violate S0.
- **Resist content-addressed storage as the *identity* model.** It is tempting (content is immutable, so hash it), but S4 forbids it outright: identical values must get distinct addresses. CAS is legitimate only as an *internal dedup/compression layer beneath* the address→value map (many I-addresses → one stored byte-run), and that dedup must never surface as identity. Flag this clearly: the address→value map is authoritative; a value-hash table underneath is an optimization hint.
- **The big simplification you've bought:** because content is write-once, the store needs *no* reader locks, *no* value versioning, *no* write-write conflict handling (each address is written once), and — because of S0 — *no garbage collection ever.* Don't build refcounts, compaction, or relocation for content. You give up space reclamation; you gain a dead-simple store and history for free.

### The arrangement — run representation and canonicity

S8 proves the arrangement *is* a finite set of maximal runs `(v_start, i_start, length)` advancing in lockstep — which is exactly a POOM/enfilade entry. The worked example shows runs break exactly at transclusion boundaries (d₂'s "llo" run ends and the native "ws" run begins where the I-side jumps `…1.5 → …2.1`). So:

- **Store arrangements as run-lists, not per-character maps.** Storage cost then scales with the number of *distinct contiguous transclusions*, not with character count: pasting a long quote is one run. Concretely, an ordered map keyed by V-start whose entries carry `(I-start, length)` gives log-time positional lookup plus compact runs. A plain per-position persistent map is simpler and makes S2 trivially true, but it is wasteful at scale — pick it only for a prototype.
- **Use persistent (structurally-shared) structures for the arrangement.** This is where mutation lives, so this is where the `im` crate earns its keep: each edit yields a new arrangement version sharing almost all structure with the old one. That directly delivers cheap historical versions and Nelson's "historical backtrack" without copying.
- **Do not maintain a canonical merged form.** The Green evidence is decisive here and Lampson-aligned: `levelpull` (the height-reducing consolidation) is fully disabled, `recombineseq`/`recombinend` carry height floors and merge at most one pair per pass, and the system relies on *confluence at the query interface* (different representations, identical query answers) rather than a canonical shape. Follow suit: **coalesce opportunistically at write time** (Green's `isanextensionnd` extends a run in place when new content is I-contiguous and same-origin — cheap, and it keeps sequential typing as a single run) but run **no global re-merge pass.** Your contract is that *queries are representation-independent*, not that storage is minimal. You give up minimal footprint; you avoid expensive rebalancing and the bookkeeping to keep canonical form.
- **When you *do* need canonical form, recompute it — don't store it.** S8 guarantees the maximal decomposition is unique, so a canonical form exists and is well-defined for the rare cases that want it (arrangement equality, a wire format). Compute it on demand; keep it out of the authoritative state.

### Allocation and structural attribution

- **Allocation is the owner's job, partitioned by prefix.** Each document owner baptizes element addresses under its own document prefix (S7a, S7b); a per-document ordinal gives within-document freshness, and document-prefix uniqueness (S7d, from the foundation's GlobalUniqueness) gives global uniqueness with *no cross-document coordination.* This is the right place for the function and it makes allocation contention-free.
- **Origin is a computation, not a table.** `origin(a)` truncates the element field — a pure function on the address's components, correct by construction (S7), invariant across all states. Build no attribution index, store no "author/source" metadata that could drift or be stripped. This is the cheapest mechanism that meets the contract, and it is exactly why attribution is unseverable.

### The sharing inverse (reverse references)

The forward map gives `ran(M(d)) ⊆ dom(C)`; the inverse — *given `a`, which `(d,v)` reference it?* — is the note's own open cost question. Engineering stance:

- **If backlinks / "where is this transcluded?" are rare:** compute on demand by scanning arrangements. Correct, no extra state, `O(total arrangement size)`.
- **If they are hot:** maintain an inverted index `I-address → {(d, v)}` — this is the spanfilade's role in Green. Treat it as **derived, rebuildable state** (a cache/hint), reconstructable by scanning arrangements at startup or on a miss; never let it become a second source of truth that can diverge.
- Pick by workload. The model permits either; nothing forces you to carry the index.

### Recovery, snapshots, and history

- **Journal arrangement edits too,** alongside the content journal — the repo's `links.jsonl` (edit journal) + `paths.json` (registry) pattern generalizes directly. Recover everything by replay.
- **Bound replay with periodic snapshots.** Because content is immutable and arrangements are persistent structures, snapshotting is cheap structural sharing: checkpoint the in-memory index/POOMs and replay only the journal tail. Snapshot cadence trades recovery time against space.
- History/time-travel is then a property you *already have*, not a feature to add: keep the arrangement journal and any prior arrangement version is reconstructable, while content permanence guarantees the bytes it referenced still exist.

### Contiguity and subspace alignment

- **Make text contiguity hold by construction.** Represent the text subspace as an *ordered sequence with implicit position* (index = ordinal) rather than explicit tumbler keys; then D-MIN (`min = [1,…,1]`) and D-SEQ (`1..n`) are structural, and insert/delete is a splice that shifts following positions — `O(log n)` with a persistent vector, versus `O(n)` if you store absolute tumbler keys and must renumber. Green's two-blade knife (second blade at `(N+1).1`) confines an insert's shift region to within one subspace; reproduce that boundary so text edits never disturb the link subspace.
- **Subspace alignment: enforce by blessed path plus a boundary check — storage won't do it for you.** The evidence is explicit: Green's `acceptablevsa` is a stub returning TRUE, no V/I subspace validation exists, and misalignment causes silent corruption downstream. The cheap, correct mechanism is to make the *only* way to obtain a V-position one that picks the right subspace (text ops append below the link floor, link ops append at `2.x` from `2.1` like Green's `findnextlinkvsa`), and to validate subspace membership *once, at the system boundary* where untrusted callers supply positions — not as a per-write runtime guard in the trusted core. Be explicit about what you give up if you skip even the boundary check: a caller can map a text V-position to a link I-address and you will not notice until a reader breaks.

## Guarantees to uphold

- **Permanence (S0) and monotonic growth (S1)** — *by construction*, if the store only appends and exposes no mutation.
- **Functionality (S2)** — *by construction*, if the arrangement is a map.
- **Origin-uniqueness (S4)** — *enforced at allocation* (inherited from the foundation's GlobalUniqueness); the strand relies on it rather than re-establishing it.
- **Referential integrity (S3)** — *requires active enforcement*: every arrangement write must ensure its target exists (write content before referencing it, or check on write). The note leaves open whether this may lapse between operations — pick whether your invariant is "every observable state" or "every quiescent state."
- **Unbounded sharing (S5)** — *by construction by omission*: simply never impose a cap. Watch for accidental caps (e.g., a fixed-width refcount that could overflow).
- **Structural attribution (S7)** — *by construction*, as a pure function on permanent addresses.
- **Finiteness (S8-fin) and the run partition (S8)** — *by construction* of any valid arrangement; **canonicity is explicitly NOT guaranteed** and not required.
- **Text contiguity (D-CTG, D-MIN, D-SEQ) and subspace alignment** — *require active enforcement by the operations layer*; they do not hold automatically and are the main proof obligations passed downstream.

## How it fits

- **Leans on the tumbler foundation (ASN-0034):** addresses and their ordering, GlobalUniqueness and allocator discipline (for S4/S7d), hierarchical field parsing (for `origin`'s projection), and ordinal shift (for the lockstep run structure). The allocator and origin function are built directly on these.
- **Hands to the operations layer:** DELETE / INSERT / COPY / REARRANGE (and the displacement mechanism behind insertion) mutate `M(d)` and carry the obligation to preserve S2, S3, and the contiguity/alignment constraints — exactly the note's closing open questions.
- **Hands to the link and query layers:** the link subspace (`2.x`, appended from `2.1`) lives in the same arrangement machinery; a spanfilade-style inverted index, if built, sits atop the arrangement to answer reverse queries; version comparison and history reconstruction consume content permanence plus the arrangement journal.
- The strand is the substrate floor: operations mutate it, link/query layers index it, history reads through it.

## Decisions for the builder

- **Arrangement representation:** per-position map (prototype) vs. ordered run-list/POOM (recommended) vs. hybrid. The note proves the run structure is sound; choose run-list unless you have a reason not to.
- **Canonicity policy:** opportunistic write-time coalescing + canonicalize-on-demand (recommended, and what Green does) vs. eager canonical merging (more bookkeeping, rarely worth it). Your query layer must be representation-independent either way.
- **Content dedup:** whether to add an internal value-dedup layer beneath the address→value map — pure optimization, must not touch identity.
- **Index materialization and snapshot cadence:** what to keep in memory, what to checkpoint, how often — recovery time vs. space.
- **Sharing inverse:** build a rebuildable inverted index (spanfilade analog) vs. scan on demand — decide by how hot backlinks are.
- **Subspace-alignment enforcement:** boundary check + blessed insertion paths (recommended) vs. per-operation precondition vs. trust-the-path-only (Green's choice; silent corruption if abused).
- **Default V-position depth `m` for a new subspace:** `m = 2` for basic insert/delete is the obvious default; deeper only if you commit early to nested subdivision.
- **S3 timing:** enforce referential integrity at every observable state, or only at quiescent points between operations.
- **Reachability queries:** S0 means you build *no* content GC; decide separately whether you expose a derived, recomputable "is this still referenced anywhere?" query — and keep it a hint, never authoritative.
