# Design Digest — ASN-0036: Strand Model

## What this is
The strand model defines the substrate's **foundational state architecture**: the separation of permanent content storage (the Istream *content store*, `Σ.C`) from per-document mutable *arrangement* (the Vstream position→address maps, `Σ.M(d)`), and the invariants that bind them. This is the state that every editing, linking, transclusion, and versioning operation reads and writes — the layer everything else stands on.

## Design commitments
These are *forced* — no downstream design may violate them:

- **Two address spaces, never merged.** Content identity (I-addresses) and document position (V-positions) are distinct roles. The same content reached from two documents has *one* I-address but *different* V-positions. A conventional "the file is the content is the layout" model is ruled out at the foundation.
- **The content store is append-only and immutable (S0/S1).** Once `C(a)=w`, the address and its value are fixed forever. There is no overwrite, no update, no delete operation — and crucially, **no garbage collection**: content unreferenced by any current arrangement still persists (S0's antecedent is membership in `dom(C)` alone). Reference-count-and-reclaim is *forbidden*, not merely unimplemented.
- **Identity is by origin, not by value (S4).** Two independent writings of identical bytes get distinct I-addresses; transclusion is *address sharing*. You may not use value/content equality as identity. (You may still dedup *payloads* underneath — see traps below.)
- **All mutation lives in arrangements; `C` is invariant under every edit.** Editing rewrites `M(d)`; the store is untouched (the S0 "frame"). This is the load-bearing premise of permanence, transclusion, and attribution.
- **No dangling references (S3).** Every active V-position resolves to stored content. Combined with S1, a valid reference can never *become* dangling.
- **Sharing is unbounded (S5).** An I-address may be referenced any finite number of times, across documents and within one document. No data structure may assume a fan-out cap; multiplicity may also be zero (orphaned).
- **Attribution is structural and permanent (S7).** `origin(a)` — the allocating document — is computable from the address alone by truncating the element field. Provenance is *encoded in the address*, not stored in a sidecar table, and is unseverable because the address is immutable.
- **The text subspace is a dense, 1-based, gapless sequence (D-CTG/D-MIN/D-SEQ).** Well-formed text arrangements occupy exactly `[1,1..1,k]` for `1 ≤ k ≤ n`. The Vstream has no empty positions.

*Conventional / not forced here* (deferred to operations or the builder): the specific V-position depth `m` (only `m≥2` is forced); **subspace alignment** between a V-position's subspace and its I-address's element field (the note explicitly makes this an operations-layer obligation, *not* a state invariant); and whether the stored run decomposition is canonical (S8 proves the partition is mathematically unique, but says nothing about representation).

## What must be built
- **A content store** — maps I-addresses to opaque content values; supports *write-at-fresh-address* and *lookup*; never mutates or removes an entry; survives restart.
- **An address allocator honoring baptism** — produces globally unique I-addresses under the originating document's prefix, so `origin` is recoverable. (Consumes ASN-0034 machinery; does not re-implement it.)
- **An origin projection** — given an I-address, return its document-level prefix. A pure function of the address.
- **A per-document arrangement** — maps V-positions to I-addresses; supports add/remove/reorder of mappings; preserves referential integrity and text-subspace contiguity across every edit.
- **A correspondence-run decomposition** — given an arrangement, produce its maximal lockstep runs `(v,a,n)`, for compact storage, positional retrieval, and the displacement semantics insertion needs.
- **An insertion-position validator** — decide `ValidInsertionPosition` / `ValidFirstInsertionPosition` from current arrangement state.
- **(Implied) a sharing inverse** — given an I-address, find the `(d,v)` that reference it. The model needs it for link-following/back-reference; the note leaves its cost open.

## Implementation approaches

**Content store.** Make it an **append-only journal recovered by replay** — Nelson's own "filed chronologically," this repo's working `links.jsonl` substrate, and udanax-green's granfilade/permascroll all converge here. S0/S1 make the log not just *an* implementation but the *natural* one: the store **is** the log; permanence and crash recovery come for free; the only derived artifact is an address→value **index**, which is a Lampson *hint* — recomputable by replay, so a torn or lost index is never authoritative loss. Build it as a persistent (structurally-shared) map (the `im` crate): because entries never mutate, every committed state shares structure with its predecessor, giving near-free historical snapshots for version reconstruction. Bound replay time with periodic **checkpoints** of the index.

> **Trap — content-addressing.** Immutability tempts you to use a content hash *as* the address. S4 forbids it: independent writes of equal bytes must be distinct addresses. CAS is fine only as a *payload-dedup layer beneath* distinct addresses, invisible to the model. Given that sharing is already by-reference (transclusion shares the address, so identical-bytes-from-independent-writes is rare), payload dedup buys little — **skip it initially.**

**Allocator & origin.** `origin(a)` needs *no stored state* — it is a structural truncation of the tumbler (Lampson: don't duplicate authoritative state; derive it). The allocator's only job is to honor baptism: a per-document monotonic counter under the document prefix, leaning entirely on ASN-0034's GlobalUniqueness. Attribution is then correct *by construction*.

**Arrangement.** Two representations, and the choice is the main lever:
- *(a) Flat position→address map per document* (this repo's `paths.json` registry, udanax POOM in spirit). Simplest; every edit is a set of point updates; runs computed on demand. Right for a first cut and small documents.
- *(b) Run/enfilade representation* — store the arrangement **as** its correspondence runs `(v,a,n)`. A transcluded 10,000-character span is *one* run, not 10,000 entries; positional retrieval is `O(log n)`. This is udanax-green's enfilade/POOM. Pick it once transclusion spans get large.

For Rust, a **persistent ordered map keyed by V-position, valued by run descriptors** gives both ordered traversal and structural sharing (cheap per-edit document versions).

> **Canonicality — settled by evidence (Q3).** Do **not** maintain maximally-merged runs as an invariant. Udanax-green deliberately tolerated non-canonical forms: `levelpull` is stubbed out (height never shrinks), `recombine*` has height floors and merges at most one pair per pass, and coalescing (`isanextensionnd`) is opportunistic write-time only. The design target was *confluence at the query interface* — equal query results from different physical shapes — **not** a canonical store. So: pick a representation cheap to update and correct to query; treat run-merging as **optional background compaction** (a hint-maintenance task), never a correctness requirement. This is "make the common case fast, the rare case correct."

**Displacement (maintaining D-SEQ).** Contiguity means inserting `k` at position `p` renumbers everything `≥ p` upward. Two strategies:
- *Eager renumber* — physically shift the tail. `O(tail)` in a flat map, `O(runs after p)` in a run map. Simple; keeps V-positions literal.
- *Lazy indirection* — a balanced/order-statistics tree (rope-like) over runs where the logical V-position is *computed* from tree position; insert/delete is `O(log n)` and renumbering is implicit. The right call at scale.

Either way, **replicate udanax-green's two-blade knife (Q2/Q5): bound the shift at `(subspace+1).1`** so a text insert at `1.x` never perturbs link positions at `2.x`. Partition the arrangement by subspace and shift only within the affected band. Note Q5's finding that the link subspace is itself contiguous-append from `2.1` — so per-subspace contiguity machinery is reusable, not text-only.

**Run decomposition.** Compute by a single linear pass over sorted V-positions, testing lockstep (`shift(v,1)↦shift(a,1)`). Because S8 proves the maximal partition is *unique*, a cached decomposition is a safe hint: regenerate on a miss and it will always agree. Don't store it as authoritative duplicate state.

**Insertion validator.** A pure predicate over the current arrangement (min position plus `N+1` shift slots from D-SEQ's `n`). No stored state.

**Sharing inverse.** The model doesn't require you to store it, but link-following does. This is exactly udanax-green's **spanfilade** (inverse enfilade: I-spans → documents). Options: recompute by scanning all arrangements (`O(total V-positions)`, fine if rare) vs. maintain a reverse index as a *hint* updated on each edit and rebuildable by full scan. For a hypertext system, back-reference queries are hot — **maintain the reverse index**, but treat it as a derived cache, not ground truth.

## Guarantees to uphold
- **Permanence (S0/S1)** — *by construction* if the store is an append-only journal that never rewrites entries; the mechanism is the *absence* of a mutate/delete path (Nelson's FEBE has no MODIFY). Active enforcement is only at the API boundary: reject any write that would overwrite an existing address, and never reclaim unreferenced content.
- **Address uniqueness (S4)** — *by construction* via the allocator/GlobalUniqueness; enforce by never reusing a counter and always allocating under the correct prefix.
- **Attribution permanence (S7)** — *by construction*; nothing to enforce beyond honoring baptism at allocation time.
- **Single image per V-position (S2)** — *by construction* if the arrangement is a map.
- **Referential integrity (S3)** — **requires active enforcement**: every operation adding a V-mapping must ensure the target is already in the store (allocate-then-reference ordering). Not free.
- **Text contiguity / 1-based / gapless (D-CTG/D-MIN/D-SEQ)** — **requires active enforcement** by every editing operation; these are well-formedness obligations the operations must re-establish, not properties of the medium.
- **Subspace alignment (V-subspace ↔ I-address element field)** — **requires active enforcement that the reference implementation never provided.** Q2 confirms udanax-green's `acceptablevsa` returned `TRUE` unconditionally, and several readers (`ispanset2vstuffset`, version comparison) *assume* alignment and silently corrupt or crash when it's violated. **Build the guard Green lacked**, or inherit the same fragility.

## How it fits
- **Leans entirely on ASN-0034 (tumbler algebra)** for the address space, lexicographic order, ordinal shift/displacement, GlobalUniqueness, hierarchical parsing/projections (`N/U/D/E`), and allocator discipline (baptism). The strand model is a *client* of all of it and re-derives none of it.
- **Hands to the operation layer** (DELETE/INSERT/COPY/REARRANGE), which mutates arrangements while preserving S2/S3/D-CTG/D-MIN/D-SEQ — the note flags these operation obligations as its own open work.
- **Underpins the link/transclusion subsystem** (links occupy subspace 2; transclusion *is* S5 address sharing), **version reconstruction** (depends on S0 permanence plus retained orphaned content), and **attribution/ownership** (S7 with the ASN-0040/0042 baptism-ownership chain).
- It is the **missing foundation beneath the operation stack**: operations assume the strand invariants hold and must preserve them; the consistency/isolation model sits adjacent (when S3 must hold — see below).

## Decisions for the builder
- **Content-store physical form** — single append-only journal + in-memory index (recommended) vs. paged store; whether to add a payload-dedup CAS layer underneath (recommend not, initially).
- **Arrangement representation** — flat position→address map vs. run/enfilade tree. Driven by expected document size and transclusion-span size.
- **Run-merge policy** — never-merge, write-time-opportunistic, or background compaction. Evidence favors **non-canonical + optional compaction**.
- **Displacement strategy** — eager renumber vs. lazy order-statistics indirection. Driven by edit-vs-read ratio and document size; adopt the per-subspace shift bound regardless.
- **Reverse (sharing) index** — maintain a spanfilade-style inverse as a hint vs. recompute on demand. Driven by how hot back-reference queries are (recommend maintain).
- **Snapshot/checkpoint cadence** for both journals, trading replay time against write amplification.
- **Subspace-alignment enforcement** — build a runtime placement guard (recommended, given Q2) vs. trust caller discipline as Green did.
- **Forced-by-an-open-question picks:** you must commit to a V-position **depth `m`** for new subspaces (`m=2` is the natural default for INSERT/DELETE; deeper `m` reserves room for nested subdivision); and you must choose **when S3 holds** — at every observable state vs. only at quiescence between operations — which is really a visibility/isolation-model decision to settle alongside the adjacent consistency model.
