## What this is

ASN-0119 defines **REARRANGE**, the editorial operation that transposes two regions of one document's text — a pivot (three cuts) or a swap (four cuts). It is the subsystem that lets a document be re-ordered while every link, attribution, and transclusion to its content survives automatically, because it rewrites *only* the document's position→content mapping and never the content itself.

## Design commitments

These are the constraints downstream design cannot violate.

- **REARRANGE writes only the arrangement map `M(d)` of one document.** Content store, link store, entity set, provenance, and every *other* document's arrangement are verbatim frames. *Forced* — every other guarantee in the note (link survival, isolation, permanence) is a corollary of this single fact.
- **Identity is by I-address, not V-position.** The operation permutes the *keys* (V-positions) and carries the *values* (I-addresses) across intact. No I-address is created, destroyed, or rebound. *Forced* — this is the deepest commitment and the reason links endure a reordering.
- **The post-state is specified by its target arrangement — the specific tiling the postconditions name — not by offsets read off raw cut spans.** The destinations of the moved regions must tile the affected interval exactly: disjoint and exhausting, hence a bijection. Per-region displacements *derived from that tiling* realize it fine (the postconditions are themselves displacement equations). *Forced* — and the point where udanax-green is provably wrong, but narrowly. Green's offsets are per-region and mostly correct (Q11, Q19): the 3-cut pivot is entirely right, and the swap's middle (`w_β−w_α`) and back (`−(w_α+w_μ)`) offsets are the tiling values. The lone defect is the swap's **α** offset, `c₂−c₀ = w_α+w_μ` where the tiling needs `w_β+w_μ = c₃−c₁` — correct only when the swapped regions are equal-width, else the middle collides with the relocated α (Q14). The symptom is global (no valid tiling); the cause is that one offset. A *separate* hazard: no offset is guarded against crossing the `s_C`/`s_L` subspace boundary (Q17).
- **The transition is atomic: one canonical order directly to the next, with no observable intermediate.** A move-then-move realization manufactures a real, addressable intermediate order (the note exhibits `A C D B E`); the single operation has none. *Forced* for the ordering invariants — all cuts resolve against one unshifted coordinate frame.
- **Extent is conserved by construction, not by repair.** Because the operation is a permutation of a fixed key set, cardinality and endpoints are invariant; there is no recompute-and-fix step in the correctness path. *Forced/structural* — Green's own width recomputation after a rearrange "should do nothing" (Q13).
- **REARRANGE is partial.** Defined only where its preconditions hold (cuts strictly ascending within the active text run, affected interval within active text, regions non-empty); outside that domain it names no post-state. *Forced.*
- **Sharing is by reference, never by copy.** A transcluding document holds its *own* V→I mapping over the same immutable I-addresses; one document's rearrange is structurally unable to reach another's order. *Forced* (follows from the first two commitments).

*Merely conventional / scope-bounded:* confinement to the text subspace at working depth 2, and the 3-/4-cut framing, are the precise scope at which the imported primitive (ASN-0084) is established. Load-bearing for *this* note's claims, but not a fundamental limit of the substrate.

## What must be built

Described functionally — what each capability must do.

- **A per-document arrangement store** mapping V-positions to I-addresses, able to reorder a contiguous interval *in place over identity* — moving the (position→content) association without touching the content it points at.
- **A cut/region resolver** that validates the preconditions, splits the *representation* at each cut point — a cut falls on a *position* boundary of the active run (the final cut may sit one position past the last active position), and the split is a representation split, not a run-decomposition boundary: that decomposition is a property of the map's values, recomputed afterward — and partitions the affected interval into regions with known widths. It must distinguish a degenerate *branch* from a degenerate *input*: reject only genuine R-PRE failures — an affected interval reaching outside the active run, non-strict cut ascent, or an active run shorter than the minimum interval (two positions for a pivot, three for a swap) — while *accepting* valid empty-exterior cases — `c₀` at the first active position, or an interval covering the whole active run — where π stays a bijection and extent is still conserved. A guard against empty exteriors would wrongly reject whole-document and leading-edge rearranges.
- **A transposition engine** that produces the new order as a tiling — laying β, then μ, then α (or β then α) so the result is collision-free and gap-free by construction.
- **A frame discipline** that makes the content store, link store, provenance, and other documents' arrangements *unwritable* by this operation — ideally unreachable from the call, not merely left alone.
- **An atomic commit** so a reader sees either the old order or the new, never a partial reordering.
- **Query-time link-footprint resolution**: links are not rewritten; a link's V-footprint is recomputed by projecting its unchanged I-address coverage through the current arrangement, yielding a possibly-fragmented span-set in the new order.
- **Identity-keyed discoverability**: link discovery and navigation resolve *through* the arrangement to I-address, so moved content is found under its new position with everything attached.
- **Durable recovery** of the new order across restart — a reasonable inference from `M` being authoritative state in `Σ`, though not itself note-mandated; recovering a *prior* arrangement is the note's OQ5 and stays spec-open.

## Implementation approaches

### The arrangement store — represent it as the run decomposition

The note's own `S8★` says the arrangement *admits* a unique maximal correspondence-run decomposition: maximal stretches where consecutive V-positions map to consecutive I-addresses. The cheapest representation that honors that property is a **piece/span list** (a piece-table over content-runs). Build the in-memory arrangement as an **ordered, structurally-shared (persistent) sequence of content-runs** (a persistent vector or ordered map):

- *Piece/span list (recommended default).* A transposition is a splice of a handful of runs; the unit of work matches the spec's unit of structure; and because it is persistent, an old version coexists with the new at near-zero copy cost. Retaining prior roots cheaply serves version coexistence and the note's "recover a prior arrangement" open question (OQ5). The no-observable-intermediate property is a separate matter — it comes from the atomic root *swap* below (the imported operation is atomic), not from retention.
- *Enfilade / POOM (the proven heavyweight).* Green's POOM stores each run as a crum with relative V- and I-displacements and reorders by adjusting V-displacements (Q12, Q18); it is proven and gives logarithmic locality at scale. Reach for it only when a document's run count is large enough that the span list's splice cost or linear scans bite. Its relative-addressing rebalancing is subtle, and — see below — its offset arithmetic carries a real bug.

**I'd pick the persistent span list** as the default and reserve the enfilade for very large documents. The simplest thing that honors `S8★` is to *be* `S8★`.

### The transposition engine — tile by placement, do not offset

This is the load-bearing technique and the place the reference is wrong — though the defect is narrow. Green's per-region offsets are mostly tiling-correct (Q11, Q19): the 3-cut pivot is entirely right, and the swap's middle and back offsets are exact. The one wrong offset is the swap's **α** destination — `diff[1] = cut2 − cut0 = w_α+w_μ` where the tiling needs `w_β+w_μ = cut3 − cut1`, equal only when the swapped regions are equal-width; when β is wider than α the middle collides with the relocated α, breaking the bijection (Q14). Separately, none of the offsets is guarded against crossing the `s_C`/`s_L` subspace boundary, so an unchecked addition can push a position into the link subspace (Q17) — a missing precondition, not a wrong offset.

Avoid both hazards structurally: **construct the new interval by concatenation.** Place β at the interval's start, then μ at start + w_β, then α at start + w_β + w_μ, letting ordinals fall out of cumulative widths. A list splice cannot overlap or leave a gap, so the bijection and single-valuedness hold *by construction*; subspace confinement holds for a separate reason — you splice *only within the text (`s_C`) interval*. (A gap-free splice that relocated a span past the `s_C`/`s_L` boundary would still be gap-free yet cross it, so confinement rides on within-interval placement, not on gap-freeness.) With both in place, there is nothing to guard.

The permutation is **cut-determined, not content-inferred**: read π off the cut geometry, and gate the operation on R-PRE alone — never on whether content "actually moved." The note is pointed about why: with shared content (S5) an interval can map every position to a single I-address, and then a legal `π ≠ id` leaves `M'(d) = M(d)` — a real rearrange whose net effect is the identity. Deriving π from the content *values* — rather than from the cuts — would compute the wrong map (the identity) for exactly that case, since duplicate I-addresses make the values ambiguous; tile-by-placement, reading π from the cuts, gets it right.

If you do want offset arithmetic (e.g., inside an enfilade for locality), derive offsets from the *cumulative tiling* the note gives (β: `−(w_α+w_μ)`, μ: `w_β−w_α`, α: `w_β+w_μ`), **not** from raw cut spans, and add the explicit checks the note's open questions call for: assert destinations are disjoint-and-exhausting, and assert no permuted position changes subspace. That guard is the price of the cheaper per-crum update. The placement approach pays nothing for the same contract — pick it unless profiling forces the other.

### Frame discipline — guarantee by unreachability, not by assertion

The cheapest way to honor "touches only `M(d)`" is to make everything else unreachable from the operation: pass only the one document's arrangement as mutable; do not pass the content store or link store mutably at all. Then RA0, RA6, and RA9 hold because you *cannot* violate a frame you cannot reach. Green achieves exactly this — a second document's tree is "structurally unreachable from a single-document REARRANGE call" (Q20) — which is a stronger and cheaper guarantee than checking frames after the fact.

One distinction to keep crisp if a document's text positions and its own link-anchor positions share one arrangement `M(d)`: freezing the link *store* `L` (RA6) is a different freeze from leaving that document's link-anchor positions — the `s_L` slice of `M(d)` — untouched (R-NS). Operate only on the text (`s_C`) interval and leave every `s_L` entry of `M(d)` fixed; with the span list this is automatic, since you splice only within the text interval.

The note's OQ1 — what boundary-hood must hold when a cut in `d` resolves to an I-address interior to another document `d′`'s independent arrangement of the same transcluded content — stays genuinely open at the spec level, but is outside this operation's build scope: `d′` is wholly unaffected (RA9, Q20), so REARRANGE has nothing to discharge for it.

### Atomic commit and durable recovery — version swap over a journal of intent

Two coupled mechanisms:

- *Atomicity* comes free from the persistent representation: publish the new arrangement as a single atomic root swap. Readers on the old root see the old order; readers after the swap see the new; no intermediate is ever addressable — that is the atomicity of the imported primitive, and RA8a guarantees the published arrangement is the same final state any realization of the permutation reaches (RA8a establishes this for a two-move composite; the generalization to any realization is sound). A move-then-move realization is exactly what this avoids: it would manufacture the observable intermediate RA8b exhibits. (Green gets the same no-intermediate property a different way — single-threaded run-to-completion scheduling around an in-place crum loop. Versioning is more robust under concurrency.)
- *Durability* is an **append-only journal recovered by replay**. The open choice is *what* to journal, and it is a genuine design choice: in this model the arrangement `M(d)` is *authoritative mutable state* (the note's `Σ = (C, L, E, M, R)` records "how content is currently ordered"), not a view derived from a content store — the Istream is *content* (`C`), and order is recorded state. *Journaling the operation* (the cut sequence) keeps entries tiny and self-validating and event-sources `M(d)` by replaying cuts against a base arrangement plus the immutable content store — at the cost of needing that base plus periodic checkpoints, and making the operation log authoritative state the spec does not itself keep. *Journaling the effect* (the resulting V→I map) gives larger entries that restore trivially, and — being append-only — *retains* every prior arrangement directly, recovering a prior order by reading an earlier record rather than replaying a prefix. I lean toward intent for the small, self-validating entries, but the edge is entry size, not history (both retain it); and since the spec records only the new map (OQ5), neither journal is mandated and the spec-level "recover a prior arrangement" guarantee stays open whichever you choose.

### Link-footprint resolution — content-addressed index, footprints as recomputable hints

Do not maintain V-position indexes for links; those would need invalidation on every rearrange — a cache that is expensive to keep coherent. Instead keep the **link index keyed on I-address coverage** (the spanfilade approach: Green keys endsets on I-addresses and converts to V at query time through the live POOM — Q15, Q16), and compute a link's footprint on demand by projecting its coverage through the current arrangement. The note hands you the cheap discoverability test directly: a link is discoverable from a document iff its coverage intersects the document's I-range (`LP12`), and that intersection is invariant under REARRANGE — so discoverability is answerable *without touching V at all*. Treat V-footprints as hints recomputed from the authoritative I-keyed index; cache them only if projection proves hot.

Footprint **fragmentation is correct, not a fault**: a footprint that straddled a cut returns as multiple non-contiguous spans because the bytes it holds now sit at separated positions (Q16). Tolerate multi-span footprints everywhere; optionally re-merge adjacent spans into canonical runs at query time (RA7c: within a region run-structure is preserved; across relocated seams runs may heal or break).

This design retires two of the note's open questions for the builder. OQ3 asks what invariant must relate a content-based discovery index to the arrangement after a rearrange; the answer is *none* — an I-address-keyed index is not arrangement-keyed, and discoverability (`coverage ∩ ran`, invariant by RA1/LP12) needs no arrangement-relative invariant at all. OQ4 asks what run-structure guarantee REARRANGE must provide for a footprint spanning three or more regions; tolerating arbitrary fragmentation makes that guarantee unnecessary to wait on. Both are dissolved by the I-keyed, fragmentation-tolerant design rather than answered within it.

### Run-decomposition canonicalization (S8★)

`S8★` holds for *any* arrangement — it is a theorem the note proves (R-BLK carries the run partition across the permutation, R-CANON canonicalizes it), not something the representation must earn. What a canonical merge-normal form buys is *footprint minimality*, not S8★-compliance: if the span list keeps adjacent runs over contiguous I-addresses coalesced, the note's `R-CANON` step is just "merge adjacent spans after the splice," it is cheap to maintain, and it keeps footprints minimally fragmented. Crucially, runs coalesce *only* on I-address contiguity, never on content-value equality: identity is per-allocation, not per-value (S4, OriginBasedIdentity), so two distinct I-addresses holding equal bytes are distinct content and must never be merged. The permutation itself is cut-determined and value-blind (R-PRE imposes no value condition), so canonicalization must be too — this forecloses the content-dedup trap by rationale, not by a rule a future optimizer might relax.

## Guarantees to uphold

*Hold by construction* (given the structural choices above):

- **Content permanence** — no I-address created/destroyed/rebound: holds if the content store is not a mutable input.
- **Extent conservation** — cardinality and endpoints invariant: holds for any permutation of a fixed key set.
- **Identity correspondence** — `π(v)` denotes what `v` denoted: holds if you move the (position, content) pair and never recompute identity.
- **Referential integrity (S3★)** — every rearranged content position still maps into `dom(C)`, and each link position into `dom(L)`: holds because π carries values unchanged and both stores are frozen.
- **Document isolation** — every other document, including transcluders, unchanged: holds if their arrangements are unreachable from the call.
- **Link survival** — endsets endure: holds if the link store is unwritten and footprints derive from I-addresses.

*Require active enforcement:*

- **Bijection / no collision** and **subspace confinement** — the two properties Green can violate (the first via its one wrong swap offset, the second for want of a boundary guard). Enforce *structurally* by tiling-by-placement (cannot collide, cannot cross), or by explicit disjoint-and-exhausting + boundary guards if you compute offsets.
- **Atomicity** — requires the commit to be a single atomic publish (root swap) or a journaled transaction; a crum-by-crum in-place reorder exposes intermediates unless serialized.
- **Cut boundary-hood** — requires the resolver to split the representation at the cut points; a cut always falls on a position boundary, so there is no "non-boundary cut" to reject. The split is a representation split, not a run-decomposition boundary — the canonical decomposition is recomputed from the new map's values (R-BLK/R-CANON) and the split may merge away.

## How it fits

- Sits on **the extended arrangement state and its invariants (ASN-0047)** — REARRANGE is one transition in that `(C, L, E, M, R)` state machine, and it joins that note's atomic-operation vocabulary as a new primitive, extending the existing invariant-preservation induction.
- Imports its operation from **the atomic rearrangement primitive (ASN-0084)** — cut sequences, pivot/swap postconditions, the cut-point-induced bijection, and the run-decomposition transformation. This note adds system guarantees; it does not redefine the permutation.
- Leans on **the immutable content/strand model (ASN-0036)** for the append-only Istream and origin-based identity, and on **the tumbler/address foundation (ASN-0034)** for V-positions and I-addresses as ordered identifiers with global uniqueness and no deallocation.
- Leans on **the link model (ASN-0043)** for endsets that reference content by address, and on **the projection model (ASN-0098)** for `coverage`, `project`, and the discoverability characterization that makes footprints recomputable.
- Hands to: any **content-addressed discovery index** (the spanfilade analog), any **RETRIEVE/read** path that renders the current order, and **transclusion** that shares I-addresses across documents. It is a sibling to INSERT/DELETE/COPY in the same operation vocabulary.

## Decisions for the builder

Genuinely open *how*-choices (distinct from the note's spec-level open questions):

1. **Arrangement representation** — persistent span list (recommended), enfilade/POOM for very large documents, or a persistent ordered map.
2. **Journal intent vs. effect** — persist the cut sequence and replay (recommended for small, self-validating entries; event-sources `M(d)` from a base arrangement plus the content store, and needs checkpoints), or persist the resulting V→I map (larger entries, restores trivially; an append-only effect log retains every prior arrangement directly). Both can recover prior arrangements — by prefix-replay or by reading an earlier record — so the difference is entry size and whether the operation log becomes authoritative state, not history. *Note:* the spec records only the new map, so the spec-level "recover a prior arrangement" guarantee (OQ5) stays open whichever you pick.
3. **Atomicity mechanism** — persistent-structure root swap (simplest, gives no-intermediate for free), transactional journal with a commit record, or copy-on-write of just the affected interval.
4. **Collision/subspace safety** — structural tile-by-placement (recommended; nothing to guard) vs. offset arithmetic plus an explicit bijection-and-boundary guard.
5. **Footprint canonicalization** — return raw fragmented span-sets vs. merge adjacent spans into canonical runs at query time.
6. **Footprint materialization** — pure query-time projection (recommended default; V-footprints are hints) vs. a cached V-index invalidated on rearrange (only if projection is measured hot).
7. **Concurrency control** — single-writer-per-document vs. optimistic concurrency with conflict detection on overlapping cut intervals. Whether two *independent* rearranges on the same content leave the final arrangement order-independent is the note's Open Question 2, and it is unresolved — RA8a settles only that a *single* fixed permutation reaches the same final state however it is realized, not that two distinct rearranges commute. Pick a serialization story rather than assume commutativity.
8. **Cut granularity** — split runs eagerly at cut points (simpler, risks over-fragmentation) vs. lazily, and whether to re-merge over-fragmented runs afterward.
