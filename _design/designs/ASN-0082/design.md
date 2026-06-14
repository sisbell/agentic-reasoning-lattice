## What this is
The arrangement-transformation layer beneath INSERT and DELETE: how a document's V→I arrangement map is rigidly repositioned — pushed forward to open room (insertion) or pulled back to close a gap (deletion) — while the content it references is left completely untouched. It is the "make room / close the gap" mechanics, not the content-allocation half.

## Design commitments
- **Editing repositions references, never content.** INSERT and DELETE modify only the per-document arrangement map M(d); the content store is invariant (I3-C: `dom(C')=dom(C)`, values unchanged; D-I is stronger still: `Σ'.C = Σ.C`). *Forced.*
- **I-addresses ride along; V-positions move.** The mapping carries its value: `M'(shift(v,n)) = M(v)`. The content reference (value) is permanent; the virtual coordinate (key) is what relocates. *Forced* — this is the entire content of I3/D-SHIFT.
- **Shifts are uniform rigid translations of a contiguous suffix.** Every position at/beyond the edit point in the affected subspace moves by exactly the same displacement δ — a bulk relocation, not a per-element rewrite. *Forced.*
- **Edits are isolated to one subspace of one document.** A text edit leaves links and other documents unchanged (I3-X/I3-D, D-CS/D-CD). The displacement acts only at the ordinal (deepest) component and never alters the subspace identifier — which is *why* depth ≥ 2 is a precondition (m=1 would corrupt the subspace id). *Forced.*
- **Text is dense, links are sparse — and that asymmetry is inherited, not chosen.** ASN-0036 imposes contiguity (D-CTG/D-SEQ/D-MIN) on text (S=1) and exempts links (S=2). So insertion's transient gap is a *violation to be repaired* in text but a *permitted tombstone* in links; contraction exists precisely to re-establish text contiguity. *Forced by the cited foundation.*
- **DELETE is non-destructive at the content layer.** Contraction removes V→I entries and slides the suffix back; the de-referenced content stays in the store. With append-only content this *is* the permanence guarantee and yields historical versions for free. *Forced* (no claim removes content) and load-bearing.
- **Spans move rigidly; width is invariant** (I3-S, D-S). A stored selection survives an edit by moving its start alone. *Forced.*
- **Contraction is proven only for depth-2 text spans; insertion for general depth ≥ 2.** A *proof boundary*, not a hard design limit — but it coincides with what udanax-green actually implemented, so it is a sound build target. (Forced floor = depth ≥ 2; current ceiling for delete = depth 2.)

## What must be built
- **A per-document arrangement map V→I** — partial, totally ordered by V-position, supporting point lookup, ordered/range traversal, and subspace-scoped queries (subspace = first component).
- **"Open a gap" (the INSERT sub-op)** — relocate the suffix at/beyond p in subspace S forward by n, leaving the n vacated slots unmapped for the caller to fill.
- **"Contract" (DELETE)** — drop a contiguous range and slide the suffix back by the range width, re-establishing text contiguity and minimum-position.
- **Tumbler arithmetic** — lexicographic compare (to locate p and range-scan), ⊕/⊖, ordinal extraction/reconstruction. Needed in full only for I-addresses; trivial at depth-2 V-positions.
- **Subspace partitioning of the domain**, with the dense/sparse discipline enforced per subspace.
- **The immutable, append-only content store (Istream/permascroll) it maps into** — defined elsewhere, but this note pins its invariance and is why referential integrity is cheap.
- *(Derived)* **span-endpoint maintenance** under shift, for any selection/link layer above.

## Implementation approaches

**The arrangement map.** Three realistic shapes, best-fit first:

1. **Sequence for text, sparse ordered map for links (recommended first build).** Represent text as a *persistent ordered sequence* with O(log n) split/concat (a rope / RRB-vector — `im`'s persistent vector is exactly this). The V-position [1,k] is then *implicit in the index* — never stored, recomputed on demand (a hint, in Lampson's sense). INSERT = split, splice, concat; DELETE = split out the range, concat the remainder. Crucially, **the shift is never computed** — splicing relocates the suffix for free, and the entire I3-V "vacating"/overlap/gap apparatus the spec must reason about for a *map* simply never arises for a *sequence*. Contiguity, single-valuedness, minimum-position, and finiteness all become true *by construction*. Represent links as a *sparse ordered map* keyed by ordinal, tombstones = absent keys; a shifted image landing in a former tombstone is just an overwrite of an empty key.
   - *Tradeoff:* two representations, but each matched to its subspace's invariant, and the hardest parts of the proof evaporate. The simplest thing that honors the spec.

2. **One displacement-carrying ordered tree for both subspaces (the enfilade / Green's POOM).** Interior nodes carry cumulative displacements so a whole subtree shifts by adjusting one node; a leaf's V-position is the sum of displacements on its root path (materialized lazily). Shift = split at p + bump the right subtree's displacement, O(log n), uniform across dense and sparse subspaces. This is the proven Xanadu approach and the literal embodiment of δ as a single relative offset.
   - *Tradeoff:* more machinery than the sequence, and single-valuedness must be re-established from the shift's injectivity (TS2) rather than gotten free. Pick this when you want *one* mechanism, lazy V-materialization, O(log n) shift on the sparse (link) side, or a path toward depth > 2.

3. **Absolute-keyed ordered map for everything.** Keys are full V-position tumblers; INSERT/DELETE re-key every shifted entry, O(k).
   - *Tradeoff:* trivial to write, wrong cost model — a one-character edit re-keys the whole tail on every keystroke. Fine as a prototype or a correctness oracle; not for production.

   **Pick:** Option 1 for the first real implementation — it makes the common case (small text edits) both simplest and fastest, and converts the note's invariant lemmas into free facts. Move to Option 2 (displacement enfilade) only if link edits get hot, you need lazy V-materialization, or you commit to deep ordinals. Keep Option 3 as a dead-simple reference oracle to differential-test the fast path against.

   *Unify-or-split note:* if links are *dense-ish with occasional tombstones*, fold them into the sequence as explicit tombstone elements (one mechanism; splice handles both; tombstone-overwrite is natural). If links are *genuinely sparse* (endpoints far apart), the sparse map wins — a sequence would store thousands of tombstones. Decide by link density.

**The content store (Istream).** An **append-only journal** is essentially forced by content immutability + permanence: content is identified by *origin* (append position / I-address), never by value, and is never rewritten. This is Green's permascroll and this repo's own `links.jsonl`/`paths.json`-recovered-by-replay pattern. I-addresses are genuine multi-story tumblers (account/document/version — the Green evidence raised the mantissa width specifically for these version chains), so the *full* tumbler arithmetic lives **here**, on the I side, not on the depth-2 V side.

**Shift/contraction at depth 2.** A depth-2 V-position is just (subspace S, ordinal k): shift = (S, k+n), contraction σ = (S, k−c) — ordinary integer arithmetic on k. The spec's tumbler ⊕/⊖ and the ord/vpos round-trip are *not exercised on V-positions* at depth 2; reserve them for I-addresses. Put the V-side arithmetic behind a narrow seam so depth > 2 can slot in later — but don't pay for it now (the proof and Green both stop at depth 2, and Green's author even flagged the depth-shift computation as suspect).

**Atomicity and recovery.** Log **operations** (INSERT p,n / DELETE p,w), not states: they are small, deterministic, and replay rebuilds the arrangement exactly — the journal is the source of truth, the in-memory persistent structures a fast cache. Bound replay with periodic **snapshots**; because the arrangement is structurally shared, a snapshot is just a retained root and old versions stay live — so version history and the permanence guarantee fall out of the *same* mechanism, no extra bookkeeping.

**External references / staleness (the note's open question, given a design answer).** Anchor durable references to **I-addresses**, which never move — not to V-positions, which do. A reverse index from I-address to referrers (the **spanfilade** role) then stays valid across every shift, and a V-position handed outside is treated as a recomputable view coordinate, re-resolved through its I-address after an edit. If live V-position handles are unavoidable, you need an indirection table updated on each shift — but prefer I-address anchoring and avoid the problem.

## Guarantees to uphold
- **Permanence / content immutability** — by construction (append-only store; edits never write content).
- **Referential integrity (`ran M' ⊆ dom C`)** — by construction: shifts introduce no new I-addresses, so if the API only ever maps to already-appended content, it holds without checks.
- **Functionality (M' single-valued)** — *by construction* under the sequence (index→one value); under a displacement tree it rests on shift injectivity (TS2) and must be respected by the split/bump logic.
- **Order preservation (monotone shift)** — by construction in a sequence/ordered tree; the uniform, positive displacement is what guarantees no reordering.
- **Text contiguity & minimum position (D-CTG/D-SEQ/D-MIN)** — *free* with the sequence; with a sparse-map-for-text it becomes active renumbering on every delete (a strong reason not to use a sparse map for text).
- **Link sparsity** — tolerated by construction (absent keys / tombstones).
- **Width preservation** — by construction if a span is stored as (start, width) and only its start is shifted.
- **Subspace / document isolation** — by construction if the arrangement is partitioned per (document, subspace) so an edit cannot address foreign entries.

The pattern: choosing the sequence representation for text turns nearly every invariant-preservation lemma in this note into a by-construction fact; choosing a map/tree turns them into obligations the shift logic must actively maintain.

## How it fits
- **Builds on ASN-0036** (arrangement map, V-positions, the S-invariants, the text-contiguity invariants) — this note is a pair of transformations *on* that structure.
- **Built from ASN-0034** (tumbler ⊕/⊖, ordinal shift, lexicographic order, partial-inverse laws) — every displacement reduces to these.
- **Hands up to ASN-0053** (span algebra): the width-preservation corollaries (I3-S, D-S) are what let a span/selection layer maintain endpoints cheaply under edits.
- **Sits beneath the INSERT/DELETE operations.** This note is the arrangement-transform sub-operation; the *full* INSERT composes it with a content append to the Istream and a fill of the opened gap, while the *full* DELETE is essentially this contraction alone (no content change).
- **Leans on the content store / permascroll** as the immutable target whose invariance makes referential integrity and permanence nearly free.

## Decisions for the builder
- **Arrangement representation:** sequence-for-text + sparse-map-for-links vs. unified displacement enfilade vs. absolute-keyed map — chosen by edit frequency, link density, and whether you'll pursue deep ordinals.
- **V-position storage:** implicit/recomputed (recommended for text) vs. materialized.
- **Link encoding:** in-sequence tombstone elements (dense-ish links) vs. sparse ordered map with absent keys (truly sparse links); and whether tombstones are explicit markers (distinguishing "deleted" from "never existed") or just gaps.
- **Insertion shape:** model the spec's two steps (open empty gap, then fill) literally, or collapse to a single splice-in-of-new-content — the decomposition permits either, and for text the one-step splice is simpler.
- **Depth:** build depth-2 (matches both the contraction proof and the reference implementation) behind a seam, or invest now in general depth (note the supporting inverse-law math is still open).
- **Journal granularity & snapshot cadence:** operation log vs. content-append log vs. both; how often to snapshot to bound replay.
- **Span maintenance:** eager (shift endpoints on every edit) vs. lazy (re-resolve through I-addresses); spans stored relative to a moving base or absolute.
- **Reference-anchoring policy:** I-address anchoring + reverse index (recommended) vs. a V-position indirection table updated on shift.
