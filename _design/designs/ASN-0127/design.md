# Design Digest — ASN-0127: Content-Region Link Query

## What this is
The read-side query algebra for **link discovery**: given a region of a document in reader (V) coordinates, which stored links reach it — and what stays stable as the substrate evolves. It defines a pure lookup capability (no mutation) plus its invariance taxonomy; it sits beneath any reader-facing "show me the links here" operation, not as one itself.

## Design commitments

**Forced — downstream cannot violate these:**

- **V→I resolution runs only through the document's live arrangement, and invents nothing.** The path from a reader's region to addresses is `image(W, d)` over `Σ.M(d)`; the `W ∩ dom(M(d))` intersection is load-bearing — positions a document doesn't currently arrange contribute no I-address. No query may manufacture reachability for unarranged positions.
- **The single-filter match is per-link *disjunctive across slots*.** A link reaches an I-set if *any one* endset slot's coverage meets it (F-MATCH). This is a different operation from the multi-slot *conjunctive* query (from ∩ to ∩ type) that Green's `find-links-from-to-three` implements — that is Q2, left open. Build the primitive so the conjunctive form composes *from* it, not the reverse.
- **Coverage is a deterministic, total function of an endset's spans.** Same endset ⟹ same coverage, always (ASN-0043). This is the hinge F-CIL turns on, and it means coverage is *derivable* — never authoritative stored state.
- **`K.λ` (link creation) is the sole mutator of the link store; every other transition preserves `Σ.L` exactly** (F-PRES, from ASN-0047). The entire change-tracking story for link queries therefore reduces to "observe link creations."
- **Two query regimes with different contracts, decided solely by how the I-argument is obtained.** A *fixed* I in the permanent address space (existence anchoring) rides only on `Σ.L`: stable, monotone, changes only under `K.λ`. An I read off a live arrangement (discovery anchoring) rides on `Σ.M` too: non-monotone, moves under arrangement edits with the store frozen. These are distinct cacheability/consistency regimes and must be treated as such.
- **Permanence and address identity.** Links, content, and their tumbler addresses are permanent (L12/S0/P0); what changes is *reachability through an arrangement*, never existence. A query result dropping a link asserts present unreachability, never deletion.
- **Endsets may target any address, including link addresses** (L4; S3★ routes link-subspace positions into `dom(Σ.L)`). The index that answers "what covers this I-address" must accept links-about-links, not just content targets.

**Conventional — this note's framing, not forced:** the explicit two-phase combinator (`findlinks ∘ image`) and the "existence/discovery" naming. An engine may fuse the stages internally — but the *two distinct state-dependencies* (M for resolution, L for matching) and their separate stability properties are forced, so the phases must stay distinguishable even if fused.

## What must be built

- **A region resolver (image):** given `(document d, V-region W)`, return the I-addresses the region currently covers via `M(d)`, restricted to the arranged domain. Must handle empty region, unarranged positions (drop silently), and contiguous V-spans resolving to a union of contiguous I-runs.
- **A coverage evaluator:** from an endset's spans, decide `coverage(e) ∩ I ≠ ∅` *without materializing the covered set* (subtrees are large/unbounded). Coverage of a unit-depth span is `subtree(x)` — a prefix-closed, order-contiguous set — so this is a prefix/interval test.
- **A link matcher (findlinks):** given an I-set, return all links with some slot meeting it — backed by an index so it is not a full store scan.
- **The composite query** chaining resolver into matcher, with the empty-image short-circuit.
- **Derived indexes maintained across evolution:** a global coverage index over the link store (the spanfilade's job); optionally a per-document I-footprint (`ran M(d)`) for whole-document queries (the F-FULL case).
- **Result-caching machinery honoring the two regimes:** monotone incremental maintenance for existence queries; recompute-or-invalidate discipline for discovery queries.
- **Recovery:** rebuild every index and cache from the append-only stores; none of the derived state is itself a source of truth.

## Implementation approaches

**Coverage evaluation — intensional, never materialized.** Represent an endset by its spans and test intersection by prefix/interval comparison against I. Because tumblers are totally ordered (T1) and a unit-depth coverage is the contiguous interval `subtree(x)` in that order, `coverage ∩ I ≠ ∅` is an *interval-overlap (stabbing) test*; a multi-span endset is a union of such intervals. This is a pure function (Lampson: cache the cheap thing — here, don't cache at all; recompute). Materialize coverage only for a hot link as a transient optimization.

**The link matcher — index, don't scan.**
- *Full scan of `dom(Σ.L)`* is correct and simple; keep it as the cold-start / recovery / verification path. It is also the honest fallback when an index is suspected stale.
- *The spanfilade* is the proven structure: an enfilade keyed on the I-address space that endsets cover, returning the links touching a queried span — and crucially **keyed per slot** (Green tags storage `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`). Build it slot-aware even though this note's primitive is slot-disjunctive, because the per-slot result sets are exactly what the conjunctive Q2 query (and Green's `intersectlinksets`) needs to AND together later. Realize it as either:
  - a **range/interval index** over the tumbler order (coverage = union of intervals; match = overlap query) — my default, because it mirrors the subtree-is-an-interval structure and handles multi-span endsets cleanly; or
  - a **radix/prefix trie** over tumbler digits — attractive if you lean on the prefix-subtree structure directly (an I-address matches an endset iff the endset's generating address is an ancestor on the trie path).
  Either way, maintenance is *append-only*: `K.λ` is the only writer and links are never retracted, so the index only grows — no deletion, no rebalancing for removal. **The index is a hint** (Lampson): fully rebuildable by replaying the link journal, so it is never journaled itself and a suspected miss is recoverable by recomputation.

**The region resolver — a run map, versioned.** Model `M(d)` as a run/interval map V→I (POOM-style), so a contiguous `W` resolves by walking its run decomposition and unioning I-extents — `O(runs in W)`, not `O(|W|)`. Arrangements are per-document, numerous, and frequently edited (μ⁺/μ⁻/μ~), so favor a **persistent ordered map with structural sharing** (`im`): an edit is `O(log n)`, the prior version survives for free (needed to evaluate `image` at a past state, and for MVCC), and reorder/contract/extend become cheap structural operations. Contrast the asymmetry with the link side: many small versioned per-document maps vs. one large append-only global link index.

**Caching across evolution — exploit F-CIL/F-LAMBDA and the regime split.**
- *Existence-anchored (fixed I):* cache freely and **maintain monotonically**. The result only grows (E-MONO) and changes only under `K.λ` (F-LAMBDA), so maintenance is: on each new link, test it against the fixed I and union the singleton if it matches. Never invalidate — only append. This is the ideal incremental-view situation.
- *Discovery-anchored (live arrangement):* **recompute by default; if cached, invalidate conservatively.** The result is non-monotone (D-NONMONO), so a stale cache is a correctness bug, not a staleness annoyance. Safe invalidation triggers: (a) any arrangement edit to `d_q` that could move `image(W, d_q)`, and (b) any `K.λ`. D-ABSORB says image-motion is *necessary but not sufficient* for the result to move — so keying invalidation on image-motion *over-invalidates but never under-invalidates*, which is the correct safe direction. As a refinement, **D-CWP gives a pre-step weakest precondition** for contraction stability computable from `(Σ, R)` alone — use it to *skip* invalidation when a contraction provably preserves the result; weigh its per-`(W,d_q)` cost against just recomputing.
- *Whole-document queries* (`W ⊇ dom M(d)`, F-FULL) equal ASN-0098's discovery set; maintain a per-document I-footprint (`ran M(d)`) as a hint to answer them without re-resolving the whole arrangement.

**Query planning from the algebra.** F-UDIST / F-VDIST (union distributivity, no disjointness needed) license decomposing a region into runs, querying the spanfilade per run, and unioning — a natural pipeline and parallelization plan. The empty-image short-circuit (F-V/F-FIND) returns ∅ without touching the link index; Green likewise short-circuits its conjunctive intersection on the first empty per-slot result, so short-circuiting is a proven pattern (here on the empty-I case).

**Recovery and durability.** This maps directly onto the repo's working substrate: an **append-only link journal** (`links.jsonl`-style) is the source of truth — the analog of Green's permascroll/granfilade — and the spanfilade, per-document POOMs, and both caches are **derived state rebuilt by replay** (the `paths.json`-registry pattern). For large stores, **checkpoint the derived indexes and replay only the journal tail** (standard WAL + checkpoint). For concurrent queries against an evolving state, serve each query a **consistent (L, M) snapshot** — MVCC falls out for free from the persistent structures, which matters here because the two phases read two stores and a query straddling independent L/M updates would otherwise violate phase independence.

**Divergences from Green to *not* replicate.** The evidence shows Green's type (THREE) slot filter is non-functional and its `homedocids` scoping is disabled by a `TRUE||` guard. F-MATCH's existential ranges over *all* slots, so a faithful build indexes the type slot too; and home-document scoping should actually filter. Treat these as Green limitations, not the contract.

## Guarantees to uphold

**Hold by construction** (given faithful implementation + append-only stores):
- Permanence of links/content/addresses, and "result drop = present unreachability, not deletion."
- Coverage determinism; result determinism given a fixed state.
- Union distributivity and I-monotonicity (algebraic; free if `findlinks` is a faithful comprehension) — and result-as-set, so order/idempotence are non-issues.
- Existence-anchored monotonicity and "existence zero ⟹ historical absence" — because the append-only store *is* the complete history.

**Require active enforcement:**
- **Index/cache consistency with the journal.** Indexes are hints; on `K.λ` they must be updated (or marked rebuildable) or the matcher silently under-reports.
- **Discovery present-tense semantics.** Never serve a stale discovery result across an arrangement edit; the invalidation discipline above is the enforcement.
- **Monotone maintenance of existence caches.** If you cache, never drop a member — the only-grows promise is now yours to keep.
- **Snapshot consistency** so a query sees one coherent (L, M) pair.

## How it fits

Leans on: **ASN-0034** (tumblers: total order, prefix/subtree); **ASN-0036** (content store: immutable, finite domain); **ASN-0043** (link store: endsets, coverage as deterministic span function, append-only permanence); **ASN-0047** (state Σ, the K-transition vocabulary, effect frames, and `K.λ` uniqueness); **ASN-0058** (arrangement, restriction/run decomposition, content sharing M13/M14); **ASN-0093** (allocation freshness/injectivity that the worked witnesses rest on); **ASN-0098** (the discovery predicate F-FULL bridges to, plus link persistence and store monotonicity that the existence lemmas inherit).

Hands to: reader-facing link-following operations; the conjunctive multi-slot retrieval (Q2 / Green's `find-links-from-to-three`); a content-keyed variant via `Σ.C` (Q1); and composition with ASN-0098 link-projection displacement (Q4). It sits as **read-side foundation algebra** — above the stores and arrangement, below reader operations.

## Decisions for the builder

- **Link-index structure:** range/interval index over the tumbler order vs. radix/prefix trie vs. a sorted base + small mutable overlay merged on read (LSM-style). Default to the interval form; pick the trie if your tumbler representation makes prefix-walks natural.
- **Index granularity:** one global spanfilade vs. per-home-document partitioning (which would make `homedocids` scoping real, unlike Green).
- **Discovery-cache policy:** recompute-always vs. image-keyed conservative invalidation vs. D-CWP precondition checks — and at what invalidation granularity (per-region, per-document, or global on `K.λ`).
- **Arrangement representation:** persistent ordered run-map (versioned, MVCC-friendly) vs. flat mutable map (cheaper per-op, no free history). Decide whether you need to evaluate `image` at past states; if yes, persistence is effectively forced.
- **Coverage strategy:** purely intensional vs. transient materialization for hot links.
- **Recovery cadence:** pure replay vs. checkpoint + tail replay, and snapshot frequency.
- **Concurrency model:** whether queries run against MVCC snapshots concurrent with `K.λ`/arrangement edits, or under a simpler serialized regime. (The repo's history of multi-worker torn-read races argues for snapshot isolation if concurrency is real.)
