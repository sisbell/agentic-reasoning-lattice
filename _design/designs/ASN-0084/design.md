# Design Digest — ASN-0084: Cut-Point Rearrangements

## What this is
This note defines **REARRANGE** — the operation that reorders existing text inside a document by transposing blocks delimited by cut points — as a *pure permutation of the document's V→I arrangement map*, with content left entirely untouched. It is one editing primitive of the mutable arrangement layer (the POOM), alongside insert/delete/copy, and it comes in exactly two shapes: a 3‑cut **pivot** (swap two adjacent blocks) and a 4‑cut **swap** (exchange two outer blocks across a held-fixed middle).

## Design commitments

**Forced — downstream design cannot violate these:**
- **Rearrange mutates only the arrangement, never content.** `C' = C` by definition. The content store is not even read-modify-written; only the per-document map `M(d): V → I` changes. Keep arrangement physically separate from content and this holds for free.
- **Rearrange is a *relabeling*, not an edit.** The V-position set is fixed (`dom` unchanged), the referenced I-address set is fixed (`ran` unchanged), and π is a bijection. No I-address is created, dropped, or duplicated. This single fact is load-bearing: it makes referential integrity and content permanence *unbreakable by this operation, by construction*.
- **The permutation is a piecewise-uniform block translation, never an arbitrary shuffle.** Each region (α, μ, β, the exteriors) moves by one constant offset determined by region *widths alone*. This is what lets you move blocks instead of characters.
- **Exactly two shapes (CS1).** Pivot = adjacent transpose; swap = transpose across a fixed middle. The middle is forced non-empty (`w_μ ≥ 1`), so a swap is genuinely distinct from a pivot, not a degenerate one.
- **Confined to one subspace at depth 2.** All cuts in the text subspace `S = 1`, ordinal depth 1; non-S positions pass through untouched. Cross-subspace transposition is out of scope — and, per the Green evidence, is precisely where an unguarded implementation silently corrupts the store.
- **The operation is partial and precondition-gated.** `REARRANGE_K` is defined *only* where R-PRE holds (3–4 strictly-ordered same-subspace depth-2 cuts, affected range fully covered). Outside that domain it has no result — the implementation must refuse, not improvise.
- **Origin/ownership is carried verbatim.** I-addresses (which encode origin) are never rewritten; only which V-position points at which I-address changes.

**Conventional — natural framing, not forced:**
- Representing `M(d)` as the **correspondence-run (span) partition**. The foundation (S8) guarantees this partition exists and has a *unique maximal form*, but does not mandate it as the storage representation — it is merely the obvious, proven one.
- Fixing `m_1 = 2`. The foundation permits deeper text subspaces; this ASN scopes them out. A builder may honor only depth 2 and still be complete for 0084.

## What must be built
- **A per-document, per-subspace arrangement map** `V → I` supporting point lookup, split-at-a-position, block reorder, and concatenation.
- **A cut-sequence validator** enforcing R-PRE: count ∈ {3,4}, strict order, all in subspace S, depth 2, positive ordinals, and *gap-free coverage* of `[c₀, c_last)`. On any violation, reject the whole operation with **no state change**.
- **The rearrange transform**: from a valid cut sequence, split the arrangement at the cuts, classify each resulting block into a region, and re-lay the blocks in pivot/swap order — realizing the bijection π.
- **A run canonicalizer (merge)**: fuse adjacent spans that are *both* V-adjacent and I-adjacent, restoring the unique maximal-run form.
- **Durability and recovery**: a way to record each rearrange so document state survives restart and is rebuildable.
- **Structural subspace confinement**: a guarantee that a rearrange on S cannot read or write any other subspace's positions.

## Implementation approaches

### The arrangement map (the central choice)
Three representations, in increasing sophistication:

- **Per-position ordered map `V → I`** (e.g., a persistent ordered map). Trivial to reason about and to check against the spec's explicit π. But a rearrange touches *every position* in the affected range — O(affected · log n). Fine for a reference/oracle model; wasteful in production when a large range is only a few spans.
- **Sorted span/run list** — `(v_start, i_start, length)` triples, exactly the udanax-green **POOM**'s content. Lookup is a binary search on V-start; rearrange is O(spans touched), not O(characters). This is the natural unit because the foundation already hands you the run partition. Pick this for the model and as the conceptual representation everywhere.
- **Enfilade / rope / order-statistics tree of spans** — a balanced tree carrying cumulative V-widths, which is Green's actual structure and the rope/finger-tree family. Gives O(log n) positional lookup, split, *and* concatenation simultaneously. Pick this for production at scale.

For a Rust target with `im`, the cleanest mapping is an **RRB-vector of spans** (`im::Vector`): its split and concatenate are O(log n) — which is *exactly* the rearrange shape (split at cuts, reorder, concat) — and its structural sharing gives you cheap historical versions for free (see persistence below).

**The decisive sub-choice: absolute vs. implicit V-positions.** This is where to apply "pick the cheapest mechanism that meets the contract."
- *Absolute V-starts* (Green's `tumbleradd` approach): each moved span's V-start must be rewritten by its displacement. The note's entire Displacement Analysis (forward by `w_β`, backward by `w_α + w_μ`, the μ sub-cases) is exactly this arithmetic.
- *Implicit positions* (sequence/rope, V-position = prefix sum of preceding widths): reordering the blocks *re-positions everything automatically* — the displacement arithmetic vanishes, and gap-freeness (D-CTG/D-SEQ) is preserved by construction. Positional lookup costs a prefix-sum (O(log n) in a rope).

**Recommendation:** realize rearrange as a **structural splice on an implicit-position sequence** — split, reorder blocks, concat — and treat the note's explicit π and per-region displacements as the **verification oracle**, not the algorithm. The spec says *what* the V→V map is; the cheapest *how* never computes a displacement at all. (This is the same split → classify → displace pipeline Green runs via `makeoffsetsfor3or4cuts` / `rearrangecutsectionnd` / `tumbleradd`; the implicit-position form simply absorbs the displace step into the concat.)

### Realizing the rearrange
Cuts cleave the span sequence into `[ext-left][α][(μ)][β][ext-right]`; you reassemble as `[ext-left][β][α][ext-right]` (pivot) or `[ext-left][β][μ][α][ext-right]` (swap). A cut interior to a span splits it (≤ one split per cut, so ≤ 4 new boundaries); a cut on a span boundary splits nothing. This is O(cuts + spans-in-range). The bijection is then *implicit* in block order. Assert that the moved block widths tile `[c₀, c_last)` exactly — that assertion is the cheap, complete check that your splice is a true permutation (no loss/dup).

### Cut validation and atomicity
Validate fully *before* mutating, so a rejected op leaves state untouched — the WAL/transaction discipline. Given D-SEQ (V-positions are exactly `[S,1..N]`), coverage reduces to: cut ordinals within range and the exclusive last cut ≤ N+1 (the EXT-VAC boundary case, where the rightmost cut legitimately sits one past the end). You may accept unsorted cuts and sort them (Green's `sortknives`) or require sorted input — a UX choice; CS2 only cares that the *validated* sequence is strictly ordered. **Do not** replicate Green here: its handler sends success *before* doing the work, never enforces bounds, and `abort()`s when a cut straddles a span — the canonical example of an unguarded partial operation. R-PRE exists precisely to convert those crashes/corruptions into a clean refusal.

### Canonicalization (merge)
The note proves merging is terminating and confluent, and that a no-mergeable-pair partition *is* the unique canonical decomposition. Two strategies:
- **Eager, at the seams.** Only the boundaries a rearrange *creates* can newly become mergeable, so you check O(cuts) seam pairs (≤ ~8), not the whole list. Cheap, bounded, and keeps the representation in canonical normal form — valuable for any downstream that compares arrangements (version comparison) or dedups runs.
- **Lazy.** Let runs fragment; merge on read or periodically. Saves work under bursty rearrange-heavy / read-light loads, at the cost of degraded lookup and storage.

**Recommendation: eager seam-merge.** It is cheap and bounded, and it makes the canonical (recomputable, unique) form the resident form. Frame merge as a *normalization hint*: it never changes the meaning of `M'(d)` — only the span representation — so on a miss you can always recompute it; you keep it canonical because it's nearly free, not because correctness demands it.

### Durability and recovery
Mirror this repo's proven substrate — an **append-only journal recovered by replay**, with a registry/checkpoint to bound replay cost (the `links.jsonl` + `paths.json` pattern).
- **Log the intent** (document + cut sequence): minimal (≤ 5 numbers), faithful to what the user asked; replay re-executes `REARRANGE_K`. Requires deterministic replay from genesis or a snapshot — so checkpoint periodically.
- **Log the effect** (the resulting span edits): larger but self-contained, independent of operation semantics drifting across versions.

**Recommendation: log intent, snapshot periodically.** Rearrange is a deterministic total function on R-PRE-valid states, so replay is deterministic. Because C is untouched, the rearrange record is cleanly independent of content-write records — a single logical, atomically-applied journal entry.

### Subspace confinement
Green's flat POOM protected the link subspace only by accident of tumbler ordering, with *no* guard — and cuts reaching into `2.x` corrupt it. Put the function where it belongs: **store/index the arrangement keyed by subspace**, so a rearrange on S structurally *cannot* address another subspace. That converts confinement from a runtime check you might forget (as Green did) into a property that holds by construction; the non-S "pass-through" runs of R-BLK are then simply spans you never touch.

## Guarantees to uphold
- **Content permanence (`C' = C`)** — *by construction* if arrangement and content are separate stores. Free.
- **Referential integrity (no dangling refs, `ran(M') ⊆ dom(C)`)** — *by construction*: rearrange permutes the existing range, introducing no new I-address (R-RI). A rearrange can *never* create a dangling reference.
- **No content loss or duplication (π bijective)** — *by construction* if the splice is a true permutation; enforce cheaply by asserting the moved block widths tile the affected range exactly.
- **Domain & contiguity preserved (D-CTG/D-SEQ)** — *by construction* with implicit positions; with absolute V-starts it follows from the displacements tiling exactly (proven, but assert it).
- **Origin/ownership invariance** — *by construction*: I-addresses carried verbatim.
- **Unique canonical run form** — the *meaning* is unique regardless; keeping the *representation* canonical requires *active enforcement* (you must merge).
- **Subspace confinement** — *by construction* with per-subspace storage; otherwise *active enforcement* (validate CS3 + filter). Green proves it is **not** automatic in a flat store.
- **Atomicity / clean partiality** — *active enforcement*: validate R-PRE before any mutation; reject with no state change.

## How it fits
- **Leans on ASN-0036 (Strand Model)** for the content store `C` (immutable, S0), the arrangement function `M(d)`, V-positions and subspaces, structural attribution (element-level I-addresses), referential integrity (S3), the contiguity invariants (D-CTG/D-SEQ), and above all the **S8 correspondence-run partition** — the span machinery this note transforms rather than re-derives.
- **Leans on ASN-0034 (tumbler algebra)** for ordering (T1), ordinal shift and its composition/monotonicity (OrdinalShift, TS3–TS5), and disjoint-subtree separation (T10) that keeps non-S runs cleanly apart. The displacement and merge-adjacency arithmetic *is* last-component tumbler shift.
- **Sits in the mutable arrangement layer (POOM)**, above the immutable content layer (granfilade/permascroll), as a sibling of insert/delete/copy.
- **Hands to** version-comparison and arrangement-diff work (the canonical run decomposition is the comparable normal form) and to any future composition-of-edits operation (the note's own open question). One concrete lever for the reverse-index/`find-documents` subsystem: because `ran(M') = ran(M)`, a *membership* reverse index ("which documents reference this content") is **invariant under rearrange** and needs no update — which retroactively justifies Green's commented-out index update on rearrange; only a reverse index that records *V-positions* must be touched, and that can be updated incrementally via π.

## Decisions for the builder
Genuine choices this note leaves open (distinct from its spec-level open questions about k>4 cuts, edit composition, run-count bounds, and weakest preconditions):
- **Arrangement representation**: per-position map vs. span list vs. enfilade/rope — and the consequential **absolute vs. implicit V-positions** sub-choice that decides whether you compute displacements at all.
- **Canonicalization timing**: eager seam-merge vs. lazy/periodic.
- **Journal granularity**: log intent (cut sequence) vs. log effect (span edits); and snapshot cadence.
- **Subspace storage**: unified-and-filter vs. partitioned-by-subspace (the latter makes Green's bug impossible).
- **Persistence vs. ephemerality**: with `im`'s structural sharing you can retain the prior arrangement as a cheap immutable version (undo, history) — or overwrite in place. Decide whether arrangement history is a feature.
- **Cut input contract**: accept and sort arbitrary order vs. require strictly-ordered cuts; and whether to accept the exclusive last cut sitting one past `max(V_S(d))`.
- **Failure channel**: the note mandates *that* you reject precondition violations (partiality) but not *how* you report them — pick the error/refusal surface deliberately, and unlike Green, make it observable to the caller.
