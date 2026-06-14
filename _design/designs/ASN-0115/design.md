## What this is

RETRIEVEV is the content-delivery subsystem: the single operation in the whole protocol that turns a *name* for content (a spec-set — an ordered series of spans over one or more documents) into the *material* itself, delivering text values and link references rather than the addresses, extents, or document identities that every other span-taking operation returns. Abstractly it is one thing: **resolution followed by faithful dereference, in order**, executed as a pure query that changes no state.

## Design commitments

These are locked in for everything downstream. I separate what is *forced* from what the note *deliberately chose*.

**Forced — downstream cannot violate:**

- **A spec-set is an ordered sequence, not a set or bag.** Order carries meaning; delivery concatenates per-spec results *in spec-set index order* with no global re-sort by V-magnitude. A later spec naming smaller positions is not floated ahead of an earlier spec. Any layer that globally sorts a multi-spec request delivers a *different object*.
- **Delivery is a pure read.** It is a function of state, mutates nothing, and appears in no transition. This permits caching, snapshotting, replay, and concurrent reads without coordination.
- **Two payload kinds, fixed by position subspace.** A content position delivers its *value*; a link position delivers a *reference* (the address). This kind-asymmetry is load-bearing: link provenance survives into the output, content origin does not.
- **Resolution is against the *current* named arrangement, and only that one.** The document tumbler *is* the version selector; there is no privileged "basic" version to substitute, and naming a document does not freeze it. The only mutable input to delivery is the arrangement.
- **Stored content is permanent and delivered by value, faithfully.** Content and link stores are append-only and immutable; "deletion" is contraction of an arrangement, never removal of content. A value that ever entered the store stays deliverable forever, through any arrangement that still binds it.
- **A named-but-unbound position is a legal gap, not an error.** Partial delivery is the norm; the operation never fails the whole for a missing part. The gap is signaled *structurally* (by absence — the caller diffs what it asked against what arrived), never by an error code.
- **No deduplication.** Two positions resolving to one address deliver the content twice — once per position. Merging them would silently omit a named, bound position and break exactness.

**Deliberately chosen (the note could have decided otherwise):**

- **Spans are confined to one subspace by an *ordinal-level* well-formedness rule.** Designating both the text and link subspaces is done by *composing* per-subspace specs into the spec-set, never by one straddling span. The note forbids the straddle at the request boundary rather than splitting it downstream.
- **The depth-compatibility override force-empties a stale spec** rather than taking the geometric intersection. A spec whose start depth no longer matches a re-pinned subspace delivers *nothing*, instead of risking a shallow start that vacuums the whole re-pinned subspace. This is a correctness-over-cleverness choice against a discontinuity, not a forced consequence.
- **The subspace identifiers** (`s_C = 1`, `s_L = 2`) are conventional axioms, not semantic necessities.

## What must be built

Described functionally — what each capability must *do*:

- **A request gate** that accepts a spec-set and checks each V-spec is well-formed: a span that acts at its deepest level (ordinal), is level-uniform, has a positive zero-free start of depth ≥ 2, and names an allocated document. This gate is where the single-subspace discipline is enforced.
- **A per-spec resolver** that, against the named document's arrangement, produces the *active positions*: the bound positions falling in the span's half-open interval, in ascending order — subject to a depth-compatibility short-circuit that yields the empty set on a stale-depth mismatch.
- **A dereference / item-former** that, per active position, looks up the resolved address and emits either the *content value* (content subspace) or the *address as a reference* (link subspace), tagged by kind.
- **An assembler** that concatenates per-spec deliveries in spec-set order, with no merge and no cross-spec re-sort.
- **Read access to a single global, immutable content pool by address**, and to the link store by address.
- **Read access to the per-document arrangements** (the one mutable map family).
- **Exact half-open boundary realization** — delivering precisely the interval `[start, reach)` when a requested boundary falls between stored positions.

## Implementation approaches

**The central factoring: one global immutable content pool + many per-document mutable arrangements.** This is the load-bearing architectural split, and it is forced by transclusion and versioning — both require a shared, address-indexed content pool with thin V→I maps layered over it. The verified udanax-green shape is exactly this (the global *granfilade* of content, per-document *POOM* arrangements), and the delivery path it runs is the right one to copy: **two-phase resolve-then-fetch** — first walk each document's arrangement to turn V-spans into addresses, then fetch values from the content pool by address. Keep these phases separate. Notably, content delivery in Green does *not* route through the provenance-annotation path that link operations use; delivery needs no origin tag in the output, since it delivers the value itself. Don't pay for provenance you don't deliver.

**Arrangement representation — persistent ordered map vs. enfilade.** The arrangement `Σ.M(d)` is a sorted V-position → address map needing one operation for delivery: a **range scan over the span's interval**. Two options:
- *Persistent ordered map per document* (an `im::OrdMap` keyed by tumbler). Range query is a sub-range scan; a version fork that shares most of its parent's arrangement is a structurally-shared clone — O(1) to create, sharing interior nodes. This is the simplest thing that honors the spec, and I'd pick it for delivery. It also makes repeatability *free* (below).
- *Full enfilade* (the Green structure). Earns its complexity where you need 2-D range queries and *reverse* lookups (which content lives where, version comparison, link endpoint indexing). For RETRIEVEV **alone**, that power is unused. Reserve the enfilade for the operations that exercit it; don't impose it on content delivery.

Decisive point for the scan: **iterate the sparse bound positions inside the interval, never enumerate the interval and filter.** The half-open interval is the *scan bound*; `act = dom(M(d)) ∩ ⟦σ⟧` is realized as a bounded scan of an ordered structure, not a set intersection against a dense (effectively infinite) point set. This is where the common case stays fast.

**The depth-compatibility gate as a cheap short-circuit.** Before scanning, compare the span's start depth to the subspace's common depth `m_S(d)`; on a non-empty subspace with a depth mismatch, return empty without scanning. `m_S(d)` is a **hint** in Lampson's sense — fully recomputable from the arrangement (the common depth of any bound position in that subspace, since allocations are level-uniform). Cache it as a per-(document, subspace) scalar updated on insert, or recompute by peeking one bound position on each call; recompute-on-miss is fine. Don't promote it to authoritative duplicate state.

**Content store — append-only journal recovered by replay.** This maps directly onto this repo's working substrate: an **append-only journal of content writes** (the `links.jsonl` pattern) plus an **in-memory address→offset index** rebuilt by replay on load (the `paths.json` registry pattern). The journal is ground truth; the index is a hint. Crucially: **the store has no delete path at all.** That gives permanence (R11) *by construction* — Green confirms the address lookup carries no liveness check; whatever was committed is returned whenever an arrangement resolves to it. One caution carried from this repo's experience: rebuild-on-load and any persisted index must use atomic writes — torn reads of a registry under concurrent writers have bitten this substrate before.

**Identity is by origin, not by value — so do *not* hash-address content.** Content identity is by *creation*: two independently created identical strings get distinct addresses; transcluded content shares one. A naïve hash-content-addressed store would merge coincidentally-equal content and destroy origin attribution (S4). Addresses are allocated at creation and encode origin; the store is origin-addressed, append-only, opaque bytes.

**Byte-opacity and boundary clipping.** Values are opaque byte runs; delivery never interprets encoding — a boundary mid-character delivers split bytes, by design (Green does exactly this). For efficiency, **coalesce contiguous (V, address) runs** in storage and **clip at the half-open boundary** when a requested edge falls inside a run — the common case is a contiguous run, the rare case is a boundary cut, and clipping keeps the rare case correct without changing any delivered content. Note the modeling gap to bridge: the spec is *position-granular* (each position → one item); a real store coalesces runs and clips. Both honor `[start, reach)`; coalescing is a representation choice invisible to the contract. Expect, and preserve, **non-contiguous spans delivered as multiple segments** (an address gap, e.g. from an interleaved link allocation, yields separate runs, not one fused byte stream).

**Assembly is concatenation — and that is also the correct thing.** Concatenate per-spec results in sequence order; sort *within* a spec by ascending V; never global-sort; never merge co-referent items. Green's evidence is instructive precisely because the consolidation step is absent — and the note proves merging would *violate* exactness. The simplest assembler is the conformant one.

**Where to enforce single-subspace — at the gate, not in the resolver.** The Green read path has *no* subspace guard, and a straddling span there silently returns garbage for its link positions. The note's defense is structural: an ordinal-level span *cannot* straddle (Confinement). I'd realize that defense by **checking ordinal-level well-formedness at request acceptance** — a cheap test (the width acts at its deepest component) that closes the footgun by construction. This is a place to be *stricter than the reference*: validate at the boundary rather than trust the caller.

**Repeatability — free against an immutable snapshot.** Because the arrangement is the sole mutable input and the stores never change what they hold, persistent maps make repeatability a non-theorem: a "version's arrangement" is an immutable map *value*, and re-running delivery against the same value is bit-identical by construction. Against *live* state, repeatability holds only while the consulted slice is unedited — so offer callers a way to **pin an arrangement snapshot** (a cheap handle to a persistent value) when they need stable re-delivery, while the default reads current state per the spec.

## Guarantees to uphold

- **Permanence (R11)** — *by construction*, if the content store has no delete path. The single most important by-construction property; everything else leans on it.
- **Faithfulness (R2)** — *by construction*, if delivery literally reads the stored value at the resolved address with no transform interposed. Active discipline: never insert transcoding/normalization. Frame limit: this governs the *denotation* only — it asserts nothing about a transmission channel.
- **Exactness (R3)** — *by construction* from bounded-scan-plus-ordered-concatenation. Active discipline: no dedup, no dropping a bound position on a neighbouring gap.
- **Order fidelity (R5)** — *by construction* if you concatenate per spec in index order and sort within by V. Active discipline: resist the global-sort "optimization," which silently breaks the contract.
- **No-dedup / multiplicity (R8)** — *by construction* (plain concatenation); a position delivered twice is correct.
- **Partial-delivery, never-fail (R6)** — *active enforcement*: unbound positions are empty contributions, not faults. Lean on the contiguity invariant — within a subspace at its common depth, bound positions form a contiguous prefix, so a short scan means you reached the frontier; there are no interior holes to special-case in the bindable slice.
- **Repeatability (R7)** — *by construction* against an immutable snapshot; *conditional* on an unedited slice against live state.
- **Origin attribution (R9)** — *by construction* through the resolution mapping, kind-asymmetrically: a link's home travels in the output (the address is delivered); a content fragment's origin is recoverable only through the internal V→address mapping, never from the bytes.
- **Subspace confinement / crossing-observability (R10)** — *active enforcement* at the gate (reject straddling spans); given that, the heterogeneous content/reference tagging makes the crossing observable for free.
- **The one legitimate failure** is a precondition, not a delivery fault: the named document must be *allocated/open*. Everything past that gate degrades to partial delivery, never to failure.

## How it fits

RETRIEVEV sits at the top of the read stack and leans downward on:

- the **immutable content store** and **link store** (ASN-0036, ASN-0043/0093) for values and link entities by address;
- the **per-document arrangement family** (ASN-0036, ASN-0047) — the one mutable input — for V→address resolution;
- **span denotation and tumbler arithmetic** (ASN-0053, ASN-0034) for the half-open interval `⟦σ⟧`;
- **generalized referential integrity and the subspace convention** (ASN-0047 S3★, subspace axioms; ASN-0082 ordinal-level) to know that a content position resolves into the content store and a link position into the link store, and that a well-formed span stays in one subspace;
- **sequential-transition reachability** (ASN-0047) for the state space it queries.

It hands *up* a tagged sequence of content values and link references to whatever transport/protocol layer frames the stream — and, being a pure query, imposes nothing on that layer beyond delivering items in the order given. It deliberately does **not** lean on the provenance-annotation path that link-creation and version-comparison operations use. It shares the *resolution* machinery (the arrangement walk) with sibling span-taking operations that return descriptions instead of material — they differ only in what they emit at the leaves, so the resolver is the natural shared component to factor out.

## Decisions for the builder

These are genuinely open — you must pick when you build, distinct from the note's own spec-level open questions:

- **Arrangement structure:** persistent ordered map per document (recommended for delivery) vs. a full enfilade shared with link/version operations. Pick by whether you're building delivery in isolation or atop machinery those other operations already need.
- **Content index strategy:** in-memory address→offset *hint* over the journal vs. an address→value map vs. a persistent ordered map; all recovered by replay. Choose by working-set size and whether values are large enough to want offset indirection over the journal.
- **Run granularity:** store one entry per position vs. coalesce contiguous (V, address) runs and clip at boundaries. Coalesce for the common case; the contract is indifferent.
- **`m_S(d)` as cached scalar vs. recomputed peek.** A hint either way — pick by edit frequency.
- **Live vs. snapshot delivery:** read current arrangement (spec default) vs. expose pinned immutable snapshots for stable re-delivery. Persistent maps make snapshots nearly free; decide whether to surface them in the API.
- **Straddle handling:** enforce ordinal-level at the gate (recommended) vs. trust the caller (the reference's footgun). If you must accept legacy straddling requests, decide whether to reject or split-per-subspace.
- **Streaming vs. materializing:** the pure-query nature permits lazy, streamed delivery for large spec-sets; decide how back-pressure interacts with partial-delivery semantics (a stream still "succeeds" while emitting nothing for gaps).
- **Wire segmentation:** one item per position, per coalesced run, or per spec — and how non-contiguous segments are framed for the caller.
- **Placement of the access/open check** — the one sanctioned failure point — and whether it is per-spec or per-request.
