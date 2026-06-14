## What this is

This note defines the **read-side link-resolution layer**: how a stored link's reach into any document is computed against that document's *current* arrangement, and exactly how that reach moves — grows, shrinks, or rebinds — as documents are edited. It is the semantics underneath "follow this link" and "what links reach here," and it draws the system's sharpest line between *permanent stored state* (the link, its coverage) and a *live, recomputed query result* (the projection).

## Design commitments

These are locked in; downstream design cannot violate them.

- **Projection is computed, never stored (the central commitment).** `project(e, d, Σ)` is a pure function of exactly two inputs — `coverage(e)` (static) and the document's current arrangement `M(d)` (live) — and consults nothing else (LP4). *Forced.* No projection cache can ever be authoritative; any stored projection is a hint, correct only insofar as it can be recomputed.
- **The stored link is immutable and permanent.** Address, endset sequence, and the spans within each endset never change and the link is never deleted — regardless of whether anything currently reaches it (LP2, LP13, LP17). *Forced* by L12 (ASN-0043).
- **Coverage is a stateless combinatorial function of the endset's spans.** It does not consult `C`, `L`, `M`, or anything else (LP3), and endsets with equal coverage are interchangeable for every projection (LP21). *Forced.* This licenses re-representing, splitting, merging, or normalizing endset spans freely as long as coverage is preserved.
- **Discoverability is derived, per-document, and arrangement-conditional — not a property of the link.** A link reaches document `d` iff some endset's coverage still intersects `d`'s arrangement range (LP12); this can be lost and regained (orphan/resurrect, LP17/LP18) without the link object changing. *Forced.*
- **Projection is per-document.** Editing document `d'` cannot affect the projection through any `d ≠ d'` (LP5). *Forced* by the single-document frame of every edit operation. This is the locality guarantee that licenses per-document indexing and per-document recomputation.
- **Each edit class moves projection in exactly one way.** Extension only grows it (LP9); contraction only shrinks it (LP10); reordering rigidly rebinds it through a bijection that preserves both the I-addresses reached and the cardinality (LP11); allocation, link-allocation, document-registration, and provenance-recording never move it (LP6–LP8, LP14). *Forced.* This is the complete catalog of displacement.
- **Survival of *reach* is conditional; survival of the *object* is not.** "A link survives if anything is left at each end" is precisely `coverage ∩ ran(M(d)) ≠ ∅` (LP12); the link's mere existence requires nothing (LP13). *Forced.*
- **Identity is by I-address, and content I-addresses are permanent.** Deletion removes arrangement entries, not content; orphaned coverage addresses persist and remain re-arrangeable (LP10, LP17, LP18). *Forced* by S0 / store monotonicity.
- **Tightness is a construction discipline, not an enforced invariant.** Build endsets canonically against currently-allocated addresses and fresh allocations provably fall outside coverage (LP19/LP19a) — but the substrate does *not* check this. *Conventional / builder-owned.*
- **The content/link subspace partition of the arrangement range is load-bearing for projection.** Content-subspace V-positions resolve into the content store, link-subspace into the link store, and the two are disjoint (LP20, LP12b). The partition is what makes per-subspace contraction reasoning sound — but it rests on a *convention* the arrangement layer must uphold (see green below).

## What must be built

- A **projection capability**: given an endset (or a link slot) and a document, return the V-positions in that document's current arrangement whose I-addresses lie in the endset's coverage; undefined when the document doesn't exist.
- A **coverage capability**: from an endset's spans, produce the denoted I-address set as a union of half-open tumbler intervals — pure, stateless, memoizable.
- A **discoverability test**: does any slot's projection through a document hit — equivalently, does coverage intersect the document's arrangement range.
- A **pre-edit survival check**: given a proposed contraction, decide which links it will orphan (LP12a's weakest precondition: a link survives iff some slot's projection meets the retained set). This is the practical payoff for offering "this delete will break N links" before committing.
- A **link store** that is append-only and value-preserving (no mutate, no delete path).
- An **arrangement family** (per-document V→I maps) supporting extend / contract / reorder with their frame and monotonicity behaviors, and never naming an unallocated I-address.
- A **reverse-discovery index** ("which links reach this content/V-position") — the substrate needs this even though the note leaves its invariants open.
- Optionally, a **tight-endset constructor** at link-creation time, if the builder adopts the no-future-capture discipline.

## Implementation approaches

**Projection.** The proven approach (udanax-green) is a *single dimension-parametric routine* (`permute`) that walks a 2-D-indexed arrangement (the POOM enfilade) and returns entries whose (I, V) rectangle intersects the query — one algorithm serving V→I and I→V, with endset/span/address distinctions living only in thin wrappers above it. This is exactly LP21 made structural: the engine sees only `(start, width)` spans, never the endset's decomposition, so equal-coverage endsets are automatically interchangeable. For a Rust/`im` build, model `M(d)` as a persistent ordered map V→I and realize projection two ways:
- *Forward filter* — scan `dom(M(d))`, test each I-address for coverage membership. Simplest, always correct, honors the spec literally. Pick this first; it is the right default for small/medium documents or cold projection.
- *Coverage-range query via an inverse-arrangement index* — keep an I→V index (the arrangement's range side) so projection becomes "intersect coverage's half-open intervals with the document's I-range." LP-Fin guarantees only finitely many *allocated* addresses fall in any canonical span's reach, so you never enumerate the (dense) coverage — you filter the (finite) arrangement. This is the enfilade's rectangle walk generalized. Faster for large documents, but the inverse index is a **hint**: derive it from `M(d)`, never treat it as authoritative, and rebuild on suspected staleness. Add it only when profiling says projection is hot.

**Coverage.** Represent an endset's coverage as a union of half-open tumbler intervals `[s, s⊕ℓ)`; membership is interval containment. Because LP21 says only coverage matters, you may *normalize* to a canonical interval-union at link-creation time — buying fast equality/dedup at the cost of discarding the user's original span decomposition. Normalize if you index or compare coverages; keep raw spans if you must display them. Coverage is pure, so cache it freely (Lampson: cache answers that are cheap to recompute on a miss).

**Link store.** This maps directly onto the repo's own working substrate: an **append-only journal of link-creation records, recovered by replay on load**, with a registry for address→offset lookup. It fits because links never mutate or vanish — there is no overwrite or delete path to reconcile, so replay is unconditional and LP13 (unconditional persistence) holds *by construction*. In memory, a persistent map (`im`) from link address to value gives O(1) per-state snapshots via structural sharing, which is what makes "project at Σ vs Σ′" cheap across the branch points the note traces. Snapshots on top of the journal are a cold-start optimization, not a correctness requirement.

**Arrangement + edits.** Per-document persistent ordered map V→I, snapshotted per state. The note's operations partition cleanly: contraction = remove a D-SEQ prefix's complement; reordering = re-key by a permutation (I-addresses reached are invariant, so it is pure rebinding); extension = add new V-positions with existing mappings fixed (LP9's E2). **Decision point with green:** green's INSERT *shifts* all downstream V-positions (the two-blade knife / `makegappm`), so a mid-document insert both adds and moves entries in one primitive — which is neither a clean LP9 grow nor a clean LP11 permute. The note instead treats insertion as a *composite* (allocate + arrange) and keeps reordering separate. I'd follow the note: expose extend and reorder as distinct operations and build mid-document insertion as extend-at-frontier + reorder. You keep the per-operation displacement laws (and thus the pre-edit survival check) exact; green's primitive shift is simpler to implement but forfeits that clean reasoning.

**Discoverability + reverse index.** Discoverability is `coverage ∩ ran(M(d)) ≠ ∅` — cheap if you keep `ran(M(d))` or the inverse index. For reverse discovery the proven approach is the **spanfilade: a reverse index from content I-address to link addresses.** The decisive design choice is *what you key it on*:
- Key on **coverage** (permanent, LP3) and **filter on read** through live projection. The index can then never go stale — it over-approximates (false positives only), and the authoritative answer is always the recomputed projection. This is a textbook hint: benign over-approximation, corrected by recomputation. It also makes orphan→resurrect cycles free, because the coverage-keyed entry was never wrong — only the current reach changed. Green's spanfilade is exactly this shape: write-only, returning a stale *superset* after deletion that callers post-filter.
- Key on **current reach** (precise, maintained) — then every contraction must update the index, you duplicate information already in `M`+`L`, and you fight LP17/LP18 (you'd delete entries you'll want back on resurrection).

I'd key on coverage and filter live, every time. (Green also shows the contrast cleanly: link discovery there admits only *content* addresses as queries; link addresses are outputs, not query keys — so a link-to-link reverse capability, flagged open by the note, is genuinely new work, not a reuse of this index.)

**Tight-endset construction.** Build canonical spans (`ℓ = δ(n, #s)`) whose reach contains only currently-allocated addresses, and rely on strictly-monotone allocation so future allocations land above the captured range (LP19a). Green achieves this *emergently* — endsets are captured exactly from arrangement-resident content, and the append-only allocator places new addresses strictly higher — with no invariant asserting it. The single-component difference between `δ(3,m)` (tight) and `δ(4,m)` (reaches one slot past the frontier) is the whole difference between "future content cannot enter this link" and "the next allocation resurrects into it." Choose per link semantics.

## Guarantees to uphold

*Hold by construction* if you follow the approaches above:
- **Link permanence** (LP13) — from an append-only/journaled store with no delete path.
- **Coverage invariance** (LP3) — from deriving coverage purely from immutable spans.
- **Projection = coverage ∩ live range** (LP20) — from always recomputing, never serving an unvalidated cache.
- **Per-document independence** (LP5) — from per-document arrangement storage with single-document edits.
- **Monotone/rigid displacement** (LP9/LP10/LP11) — from not implementing any primitive that adds *and* removes in one step (decompose insert-with-shift).
- **Orphan persistence + resurrection** (LP17/LP18) — from link permanence + live recomputation; requires that you never GC orphaned links or their coverage addresses.
- **Passive discoverability through transclusion** (LP16) — falls out free: a document that transcludes covered content becomes a discovery site with no notification path to build.

*Require active enforcement:*
- **No spurious future capture** (LP19) — the tightness discipline at construction; the substrate won't do it for you.
- **Subspace integrity** (LP12b, LP20 partition) — content-subspace V-positions must resolve to content, link-subspace to links. Green's placement guard is a stub that always accepts, so nothing structural prevents cross-subspace corruption; for a fresh build a cheap write-time check is worthwhile insurance, because LP12b shows projection is sensitive to the subspace *partition* of a deletion, not just its size.
- **Referential integrity of the arrangement** (LP20 corollary) — every arranged I-address must be allocated. Green gets this for free because its V→arrangement→I path can only name already-resolved addresses; if you let arrangements name raw I-addresses, you must re-impose it.

## How it fits

- **ASN-0047** provides the extended state `Σ = (C, L, E, M, R)`, the edit operations and their single-document frames, document registration, and generalized referential integrity (S3★) — this note is a pure consumer of those transitions.
- **ASN-0043** provides the stored link/endset structure, the coverage definition, and link immutability (L12) — the permanent half of the permanent/live split.
- **ASN-0093** provides substrate addressing: sub-allocator chains, contiguous emission, the subspace convention, and store disjointness/monotonicity — the ground for LP-Sub/LP-Fin and the tightness argument.
- **ASN-0034** provides the tumbler algebra (spans, `⊕`, half-open intervals, ordinal displacement `δ`) that coverage is built from.
- This layer **hands to** the user-facing link-following / endset-retrieval / link-finding operations, and to transclusion and version-comparison features, which are all expressed in terms of `project` and `discoverable_from`.

## Decisions for the builder

1. **Recompute-always vs cached hint.** Default to recompute; add the per-document inverse-arrangement index as a recoverable hint only when projection is hot. Never let it be authoritative.
2. **Coverage representation.** Normalized interval-union (fast equality/dedup, LP21-licensed) vs raw spans (preserves the user's decomposition for display). Pick by whether you index/compare coverages.
3. **Reverse-index keying.** Coverage-keyed + live filter (never stale, free resurrection — recommended) vs reach-keyed + maintained (precise but fights LP17/LP18 and duplicates state).
4. **Insertion model.** Decompose into extend + reorder (keeps LP9/LP11 and the pre-edit survival check exact) vs a green-style shift primitive (simpler, muddier reasoning).
5. **V-position identity.** Stable structured addresses (LP9's prior-domain agreement holds literally) vs positional offsets that shift (you must re-derive it). Tied to #4.
6. **Tightness.** Enforce canonical, frontier-bounded endsets at construction, or allow loose spans that admit future capture. Substrate won't decide for you.
7. **Subspace-convention enforcement.** Structural write-time check vs trust callers (green's choice). For a new build, check.
8. **Durability.** Journal-and-replay (natural for an immutable store) vs periodic snapshot vs both.
9. **Recomputation timing.** Per-document independence (LP5) lets you recompute only the edited document — eagerly on edit or lazily on next query. Lazy is simpler and the live-recomputation model fully supports it.
