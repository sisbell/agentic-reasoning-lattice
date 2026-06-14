## What this is

RETRIEVEENDSETS (`RE(W, d, Σ)`) is the read-only query that, given a content region of a document, returns the `(role, endset)` anchoring pairs of every *live* link that touches that region — reporting **that** and **how** content is bound without revealing **which** links bind it. It is the "anchoring without names" sibling of the link-discovery query (`findlinks`): same region, same selection, deliberately poorer answer.

## Design commitments

These are locked in for everything downstream; I mark what is *forced* versus *conventional*.

- **Identity is withheld; the answer is a deduplicated set of `(role, endset)` pairs.** *(Forced — this is the operation's whole reason for being.)* Two distinct links bearing the same endset value in the same slot collapse to one pair. A consequence the builder cannot escape: multiplicity is not recoverable, and a surfaced from-endset cannot be paired with its link's to-endset. The query is non-followable by construction.
- **The key is content identity (I-addresses), never position or document.** *(Forced.)* Both the anchoring (endsets cover I-addresses) and the region (its image is I-addresses) live in content-identity space. Transclusion-blindness and coverage-permanence fall out of this for free — they are not separate features to build.
- **Overlap, not containment; single shared address suffices; existential within an endset; tested per-endset.** *(Forced.)* A straddling endset is surfaced on one shared address and is *not* clipped to the region.
- **No clipping — every span is reported at full recorded extent.** *(Forced, load-bearing.)* Clipping would lie about the link's grip. This holds under either extent reading.
- **Discovery-anchored / present-tense.** *(Forced by resolving through `Σ.M(d)`.)* A zero answer means "nothing is reachable through this region as it now stands," never "nothing was ever anchored." The answer is non-monotone under editing.
- **Pure read over the *addressable* (live, non-nullified) population.** *(Forced.)* `Σ' = Σ`; reads only `Σ.M(d)` and `Σ.L`; never `Σ.C` values, `Σ.E`, or `Σ.R`.
- **Whole-endset surfacing — all spans, including those pointing outside the region.** *(CONVENTIONAL — provisional, Open Question 1.)* A touching-spans-only implementation still honors no-clipping. This is the one place the note explicitly leaves the payload shape open.

## What must be built

Functionally, an implementation must provide:

- **A region resolver** — turn `(W, d)` into the content-image `I` by reading the *current* arrangement `Σ.M(d)`. Shared verbatim with `findlinks` and content retrieval.
- **A coverage/touch oracle** — decide `coverage(e) ∩ I ≠ ∅` exactly, over the totally-ordered address space, returning the endset *unclipped*.
- **A live-link endset enumerator** — given `I`, produce every `(slot, endset)` of an addressable link whose coverage meets `I`.
- **An addressability determination** — distinguish live links from nullified ones (`addressable = dom(Σ.L) ∖ nullified`).
- **A deduplicating, identity-stripping collector** — assemble `(role, endset)` pairs into a set, discarding link addresses and collapsing duplicates.
- **(Optional) a renderer** — project surfaced endset I-spans into the querying document's V-order, for consumers that want a positioned answer rather than a content-identity one.

## Implementation approaches

This is the heart. The note's deepest engineering gift is that `RE` is *thin*: it is a join over three mechanisms that belong to other subsystems, plus a dedup. Build it that way.

### Resolving the region (V→I)
The image is `{Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}`. Two realizations:
- **Ordered map from V-position to I-address** (an `im::OrdMap`-style persistent map). Image = collect over `W`. This is the simplest thing that honors the spec; start here.
- **Run-compressed / interval representation** (the udanax-green POOM/enfilade approach). Because the arrangement is a canonical *contiguous* prefix of the content subspace (D-CTG/D-SEQ), the common case is a handful of contiguous runs, and an interval map stores one entry per run, not per position, and answers V-ranges directly.

I'd ship the ordered map first and move to interval/run-compression only when arrangement size demands it — but note the contiguity invariant makes the interval form natural, so this migration is a known, bounded one, not a rewrite.

### The anchoring index — and "one index, two readers"
The query must, given `I`, find every `(link, slot, endset)` whose coverage meets `I`. Options:

- **Option A — scan the live links.** For each addressable link, for each endset, run the touch test. This is *literally* RE-DEF, and the note proves it decidable and finite. No index to build, maintain, or recover; nothing can go stale. For a small corpus or a cold path, this is the correct, cheapest thing — pick it first.
- **Option B — a content-keyed coverage index (the spanfilade).** Index every endset span by its I-address range, carrying `(link, slot)` as payload; the query intersects `I` against it. This is udanax-green's spanfilade, proven at scale: a two-dimensional range structure with the I-address on one axis (`SPANRANGE`) and link-identity-plus-role on the other (`ORGLRANGE`), role as a prefix so you can query one slot or all. Since `RE` tests every slot of every link (no per-slot request differentiation), you query all role-bands.

  The verified green pipeline shows `findlinks` and RETRIEVEENDSETS run the *same* V→I→spanfilade search and diverge only in **which axis of the hit they read**: `findlinks` reads the link-identity axis; RETRIEVEENDSETS reads the endset-span axis and strips identity. So **build one link-endset index and give it two readers** — do not build a separate endset index. This is the cleanest "put the function where it belongs" move available here.

The decisive simplification: links are permanent and immutable (L12) and emission is append-only, so the coverage index is a **pure monotone function of the link journal** — append-only, never updated, never deleted. That makes it a *hint* in Lampson's sense: recomputable by replay on a miss or after a crash, never authoritative, never transactionally coupled to anything. For the Rust target, realize it as a persistent ordered interval map keyed by I-address; each emission yields a structurally-shared new version cheaply.

When to pick which: scan for small/cold; the shared index for the hot path at scale. They are not exclusive — the scan is also your recovery-time oracle and your correctness reference for the index.

### Coverage and the touch test
Represent coverage as ranges over the ordered address space and answer touch by range-overlap. A wide span is a half-open interval `[start, start⊕width)`; a unit-depth span is the prefix-closed set `{t : start ≼ t}`, which is just the range `[start, next-sibling)`. One mechanism — interval overlap on an ordered structure — serves both, and it is exactly what makes the note's disjointness arguments (type endsets vs content, retraction to-sets vs content) computable as prefix/field comparisons.

### Addressability as a separate live-set filter
Green's spanfilade is write-only and monotone — it never removes an endset entry, even after the content is gone. The note's `addressable = dom(Σ.L) ∖ nullified` is an *additional* live-set filter that green did not need (green has no retraction; links are permanent). Keep this decomposition clean:
- **Filter nullified at query time.** The index returns candidate `(link, slot, endset)`; drop those whose link is nullified. This keeps the index append-only (a pure hint) and puts the retraction logic where it belongs — a separate, cheap set-membership test.
- *Reject* maintaining a live-only index (removing on nullify): it breaks append-only and couples the index to retraction for no benefit.

`nullified` itself is a hint: derived by replaying retraction links (each `Nullify` appends a retraction-typed link whose unit-depth to-set names its target). Materialize it as a persistent set updated incrementally on each retraction emission, recoverable by replay.

### Recovery: journal + replay, indices as hints
This subsystem reads only `Σ.M` and `Σ.L`, and `Σ.L` is naturally an **append-only journal** — exactly this repo's working substrate (`links.jsonl` with a `paths.json` registry, recovered by replay), and exactly green's permascroll discipline. So: one authoritative append-only log; the coverage index, the `nullified` set, and the `addressable` set are all hints rebuilt by replay. No duplicate authoritative state, no recovery protocol beyond "replay the journal."

### Assembling the answer — and a real subtlety
Collect into a persistent set keyed by `(slot, endset-value)`; endset equality is set-equality on spans; duplicates collapse. For *stateless recompute*, that is all.

But if you want to **incrementally maintain** a cached `RE` answer (attractive, because RE-EDIT/RE-RET tell you exactly how the answer moves), retraction forces a wrinkle: RE-RET says a pair drops *iff the retracted link was its sole addressable bearer*. To maintain the deduplicated set incrementally under retraction you must keep an **internal per-pair bearer refcount** — even though the answer deliberately hides that very multiplicity (RE-UNIT). The answer hides counts; incremental maintenance needs them privately. Decide up front: stateless recompute (simple, no refcounts) versus incremental-with-refcounts (cheap updates, internal bookkeeping). I'd default to stateless recompute and add refcounts only if query latency on a churning store demands it.

### Content-identity vs rendered answer
The note's primitive is a **content-identity** answer: endsets as spans over I-addresses, arrangement-independent and permanent (RE-IDENT). Green actually returns a **rendered** answer: it converts endset I-spans back to the *querying* document's V-positions and **silently drops** any I-address that document does not currently arrange — so an endset can come back empty or partial, and a reorder/pivot can fragment one contiguous endset into several V-spans. That rendered behavior is Open Question 3, not the note's answer.

Build the content-identity answer as the stable primitive and offer rendering as an *optional projection on top*. Put the permanent, arrangement-independent thing underneath; put the lossy, present-tense view where its losses are visible and expected.

### Caching by region cover
Union-distributivity (RE-UDIST) is a gift: cache atomic-unit answers (per V-position, per line) and compose larger regions by **union**. Do **not** compose by intersection — RE-UDIST-∩ fails in general, and the note proves *no arrangement restriction recovers it* (the split-witness obstruction defeats `⊇` even under a perfectly injective arrangement). So a cache that answers `W₁ ∩ W₂` by intersecting cached `RE(W₁)`, `RE(W₂)` is unsound. Compose only upward, by union.

## Guarantees to uphold

- **Soundness** *(by construction — never fabricate; the index payload must witness a real link/slot)*. **Completeness** *(active enforcement — every emitted endset span must be indexed; a missed insert silently violates RE-CMP)*.
- **No clipping** *(active — always use the full-extent extraction path; never the intersect-and-truncate path used for content retrieval; green proves these are two different routines and only the full-extent one is correct here)*.
- **Anchoring without names** *(active — the link address is an internal lookup key only; ensure it never reaches the answer; dedup on `(slot, endset)`)*.
- **Content-identity invariance / coverage permanence** *(by construction, given link immutability and content-keying — holds as long as endsets are never rewritten and the key is the I-address)*.
- **Determinism** *(by construction — pure read of current state)*.
- **Present-tense correctness** *(active — resolve through the *current* arrangement; even atop a monotone index, gate the answer on what `Σ.M(d)` arranges now, exactly as green's POOM gates input and output)*.
- **Union-distributivity** *(by construction)* — with the standing caution that intersection-distributivity does not hold.

## How it fits

`RE` sits at the query layer and leans on four subsystems, re-deriving none:

- **Arrangement** (`Σ.M`, ASN-0036/0047) for the image — the same `F-IMG` primitive `findlinks` and content retrieval use.
- **Link store** (`Σ.L`, ASN-0043) for endsets — append-only, immutable, non-injective.
- **Span/coverage algebra** (ASN-0098, ASN-0043, ASN-0034) for `coverage(e)` and the half-open/prefix touch test.
- **Retraction discipline** (ASN-0086) for `nullified` / addressability — a standing assumption (every retraction is a `Nullify` with empty from-set and unit-depth to-set).

It is the **sibling of `findlinks`** (ASN-0127): identical selection (`sel = findlinks_V ∩ addressable`), different deliverable — share the index, project differently. It is **distinct from FINDLINKSFROMTOTHREE** (per-slot-differentiated, identity-returning) and **FOLLOWLINK** (identity-in, endsets-out). It **hands its answer to anchoring-aware consumers** — UI that shades bound regions, "is this linked?" indicators, link-density displays — anything that needs to know content is gripped without needing to follow the grip. It touches neither content values, entities, nor provenance.

## Decisions for the builder

Genuinely open implementation choices (distinct from the note's spec-level Open Questions):

- **Scan vs index.** Brute-force scan over live links for small/cold corpora (proven correct, zero maintenance); the shared content-keyed index for the hot path at scale. Keep the scan as your recovery oracle and correctness reference regardless.
- **Index representation.** Persistent ordered interval map keyed by I-address with role as a dimension and `(link, slot)` as payload, versus the run-compressed enfilade. Choose on corpus size and how contiguous endset coverage tends to be.
- **Addressability placement.** Filter nullified at query time (recommended — keeps the index a pure append-only hint) versus a live-only index (rejected).
- **`nullified` materialization.** Incrementally-updated persistent set versus replay-on-demand; both are valid hints, recoverable from the journal.
- **Content-identity vs rendered answer at the API.** Return I-address spans (stable primitive), V-rendered spans (green's lossy, present-tense view), or both. If you render, decide how to surface the silent-drop of unarranged I-addresses and the pivot-induced fragmentation (Open Question 3 territory). Recommended: content-identity underneath, rendering as an opt-in projection.
- **Whole-endset vs touching-spans payload.** The note adopts whole-endset provisionally (Open Question 1); green returns the whole stored extent, matching it. Touching-spans-only is a legitimate economy that still honors no-clipping. Decide and document — it is a wire-payload-size tradeoff.
- **Stateless recompute vs incremental maintenance.** If you cache `RE` and want incremental updates, retraction forces internal per-pair bearer refcounts (even though the answer hides multiplicity). Default to stateless recompute; add refcounts only under measured query pressure.
- **Cache composition.** Exploit union-distributivity to compose region answers from atomic units; never compose by intersection.
- **Index scope: global vs per-document.** A global, content-keyed index makes transclusion-blindness (RE-TRANS) and cross-store completeness (RE-CMP, Open Question 5) fall out, as green's global spanfilade demonstrates. If you partition the link store per document, you must union across all co-transcluders at query time to avoid silently dropping anchoring reached through borrowed content.
