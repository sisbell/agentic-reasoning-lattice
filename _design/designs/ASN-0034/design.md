## What this is

The addressing and naming subsystem — the bottom of the stack. It defines the **tumbler** (the permanent, globally unique address carried by every server, account, document, and element) and the minimal algebra over tumblers — a total order, hierarchical containment parsing, position arithmetic, and an allocation increment — that every higher layer uses to compare, contain, reference, and allocate. Nothing else in the system can name a thing without this.

## Design commitments

These are the locks downstream design cannot violate.

- **An address *is* a finite sequence of unbounded naturals — nothing more.** Identity is sequence identity (T3): no mantissa/exponent, no normalization map, no quotient, no external interpretation. *Forced.* Any representation that admits two encodings of one tumbler breaks equality, breaks transitivity of the order, and breaks uniqueness. The note records this happening concretely in the reference implementation, where an un-normalized leading zero made a positive address compare equal to zero.
- **The space is unbounded in two independent dimensions** — unlimited siblings at a level (T0a) and unlimited depth (T0b). *Forced.* A fixed-width representation is a spec violation unless you separately *prove* the reachable state never reaches the bound. The note documents the reference design crashing on this and widening its bound after the fact.
- **Comparison and containment are intrinsic** — decidable from the two addresses alone, no index, no shared state (T2, T6). *Forced.* This is the whole basis of decentralization; the first containment test that needs a lookup collapses the coordination-free property.
- **Hierarchy is convention projected onto a flat line — not enforced by the algebra** (T4). Comparison and arithmetic treat every component identically; the four-field structure and zeros-as-separators live in the *allocator* and the *parser*. *Forced separation of concerns:* keep the arithmetic flat and uniform, put hierarchy one layer up.
- **Tree containment equals line contiguity** (T5). Every subtree is a contiguous interval; a span between two endpoints under a prefix captures exactly that subtree. *Forced* — spans, link endsets, and content reference all rest on it.
- **Allocation is permanent and monotone; there is no deallocation** (T8, T9). The allocated set only grows; gaps are permanent. *Forced as an axiom* — the absence of free/reclaim is deliberate, because links, transclusion, and attribution all assume addresses are never reused or revoked.
- **Uniqueness comes from the shape of names, not from consensus** (T10). Partition by prefix; non-nesting prefixes can never collide, so independent owners allocate concurrently with zero coordination. *Forced* — but it rests entirely on the **allocator discipline** (T10a): siblings by shallow increment only, children by a single deep increment (depth 1 or 2). Break the discipline and uniqueness can break.
- **The subspace identifier is part of the address, not metadata** (T7). Text and link addresses are disjoint by construction.
- **This is an addressing calculus, not a counting calculus.** ⊕ advances a position, ⊖ recovers a displacement; a difference is a *boundary*, not a *count*. *Forced/scoping:* no multiplication, no division, no additive identity or inverse. The minimal structure — an ordered set with an order-preserving shift and an allocation increment — is the *whole* contract; anything more is unused machinery and unverified obligation.

## What must be built

- **A tumbler value** — an immutable, ordered sequence of unbounded-magnitude components, with equality as sequence equality.
- **An intrinsic comparator** — orders two tumblers by left-to-right component scan with "prefix is smaller," consulting nothing external.
- **A field parser and admission validator** — locates zero separators, extracts node/user/document/element fields and the level (zero-count) from the address alone; admits only well-formed addresses (≤3 zeros, no adjacent/leading/trailing zero, never all-zero).
- **Three position operations** — advance-by-displacement (⊕), displacement-between (⊖), and allocation-increment (`inc`, in sibling and child-spawn modes) — as pure functions on immutable tumblers.
- **Per-domain allocators** — one logical frontier per active prefix, advancing the sibling counter and spawning children under the discipline that guarantees uniqueness.
- **A durable, monotone allocation frontier** — the per-allocator high-water mark, which must survive crashes and never regress. This is the *only* mutable persistent state the note implies.
- **A span** — a (start, length) pair with an intrinsic membership test and the subtree-capture (1-position) convention.
- **The ordinal-only shift apparatus** — element-local advancement that carries the subspace identifier as context, never as an arithmetic operand.

## Implementation approaches

**Representing the tumbler.** Store the *literal sequence* and make canonical identity (T3) free. This is the single highest-leverage decision. The reference design's mantissa+exponent form required a normalization routine after every operation, a validation guard, and still admitted the leading-zero alias that broke transitivity. Storing the bare sequence deletes that entire bug class — no normalization, no canonicalization, identity by construction. That is the Lampson move: pick the representation where the invariant holds for free.

- *Component magnitude:* arbitrary precision (bignum) honors T0a exactly. This is cheap in the common case because ⊕ has **no carry propagation** — addition touches exactly one component, so bignum cost is paid at one position, not across the address. Bignum also makes the abstract associativity of ⊕ actually hold (finite-width arithmetic can break it via overflow).
- *Sequence storage:* default to an inline small-sequence (most addresses are short). Reach for a persistent, structurally-shared vector (`im`) only if profiling shows deep tumblers dominate — then siblings and parent/child addresses share their common prefix in memory, and increment is copy-with-change. The tradeoff is persistent vectors' higher constant factor against short flat arrays; for the common short address, inline wins.
- *Encoding at rest:* a variable-length integer encoding (Nelson's "humber") — compact for small components, expanding for large — decouples the journal/wire format from the in-memory form.
- *Fixed-width fast path:* acceptable only as an optional cache with bignum fallback on overflow, never as the system of record. The note is explicit that fixed-width without a proven bound *is* the violation.

**Comparison, parsing, containment.** A direct lexicographic scan is O(min(#a, #b)), intrinsic, and already the simplest correct thing — leave it alone; don't cache what's this cheap. The field parse (fields/zeros/level) is a single scan; if it turns out hot on a containment-query path, attach it to the tumbler as a *hint* — recomputable on a miss, never authoritative — but measure first, because #t is small. Run T4 validation **at admission only**: internal arithmetic operates on flat sequences and must not re-validate or normalize, matching the note's "flat and uniform" arithmetic layer.

**The arithmetic.** Implement ⊕/⊖/`inc` straight from the constructive definitions (action point, tail-replacement, divergence-zeroing). They are short, pure, total within their preconditions, and free of I/O and shared state — they belong in the value layer. Do *not* port the reference mantissa arithmetic; the note documents its add routine carrying an operand-order asymmetry that discarded an argument and lost information. A clean from-spec implementation avoids inheriting that. One caution worth wiring into the API contract: ⊕ is **many-to-one** (it discards the start's structure below the action point), so a start position cannot in general be recovered from result-plus-displacement. The displacement round-trip recovers endpoints only under specific length/divergence conditions (D0–D2); outside them, **store endpoints rather than recompute them.**

**Allocation — partition first.** Give each ownership domain (server, account, document, element-stream) its own allocator. Because non-nesting prefixes can never collide (T10), allocators in different domains are fully independent: allocate concurrently, no cross-prefix locks, no coordination. Serialize only *within* a single allocator — it is a counter. The state per allocator is tiny: the current sibling high-water mark, with a new sibling = `inc(frontier, 0)` and a child = one `inc(frontier, k>0)` plus a fresh sub-allocator.

**Durability and recovery of the frontier — the part that needs real care.** T8 plus the note's own open question on counter durability force a choice, and the invariant that decides it is sharp: **never hand out an address twice.** Over-shooting (leaving gaps) is harmless — T9 makes gaps permanent and legitimate. Under-shooting (reusing) is fatal once any consumer has persisted a reference. So the cheap, safe designs all lean on *skip-ahead, never reuse*:

- *Durable write per allocation* — synchronous persist of the frontier on every `inc`. Simplest correctness story, but a synchronous write on the hot path. Fine only if allocation is genuinely rare.
- *Batch reservation (hi-lo)* — durably reserve a block of sibling slots, hand them out from memory, persist only when a block is exhausted. On recovery, resume from the last durably-reserved high-water mark; the unused tail of the in-flight block is *skipped*, which is safe. This makes the common case fast (in-memory increment, one durable write per block) and the crash case correct by construction.
- *Journal + replay, with periodic snapshot* — append allocation events to an append-only log; recover frontiers by replaying and taking the per-prefix max; snapshot the frontier registry periodically to bound replay. The log carries atomicity and recovery; the registry is a *hint*, recomputable from the log if lost or corrupt.

These compose, and the composition is what I'd build: **a journal of record for what was allocated, a recomputable per-prefix frontier registry as a fast-start snapshot, and in-memory batch reservation to keep the hot path off synchronous writes.** This is exactly the repo's proven substrate — an append-only `links.jsonl` journal with a `paths.json` registry recovered by replay — and the allocation frontier should ride that same log so the system has one recovery story, not two. Note the corollary the note insists on: allocation and content are **decoupled**. An address can be permanently claimed (in the journal/frontier) with nothing in the content map — Nelson's "ghost elements." "Is this allocated?" and "does this hold content?" are two queries against two structures; keep them so.

**Spans.** Represent (start, length); membership is two intrinsic comparisons, and subtree capture is the 1-position convention (a length whose action point sits at the prefix's level). No index needed for membership. The *inverse* query — "which spans cover address *t*?", i.e. link-endset lookup — is an indexing problem you hand off; Green's **spanfilade** is the proven structure for it. Out of scope here, but the seam is at this boundary.

**Ordinal-only shift (TA7a).** Carry the subspace identifier as structural context and do the arithmetic on the bare ordinal. The note shows why this isn't optional: feeding a full `[subspace, ordinal]` position into ⊖ finds the divergence at the subspace identifier and no-ops. Bake the strip/shift/reattach into the element-stream API so a caller cannot accidentally shift a full position and silently get nothing.

## Guarantees to uphold

**Hold by construction** (free, given the representation choices above):
- Canonical identity (T3) — free *iff* you store the literal sequence, not a mantissa/exponent.
- Total order and intrinsic comparison (T1, T2) — free from the lexicographic scan.
- Contiguous subtrees, decidable containment, subspace disjointness (T5, T6, T7) — emergent from T1+T4, free *provided* T4 validation holds at admission.
- Global uniqueness (T10) — free *given* the allocator discipline holds.

**Require active enforcement** (the runtime must guard these):
- Unbounded space (T0) — use arbitrary precision, or discharge the proof that the bound is unreachable. The default fixed-width choice silently violates this.
- Well-formedness (T4) — validate at every admission boundary; reject adjacent/leading/trailing zeros, more than three zeros, and any all-zero sequence used as an address.
- Allocator discipline (T10a) — siblings by `inc(·,0)`, children by one `inc(·,k∈{1,2})`. This is what *produces* uniqueness, so it must be enforced inside the allocator, not assumed of callers.
- Permanence and monotonicity (T8, T9) — no deallocation in the API, and a durable frontier that never regresses across crashes. This is the most important runtime invariant in the note and its only persistent mutable state.

## How it fits

This is the foundation; it leans on nothing below it but ℕ arithmetic. It hands tumblers *upward* as: the ordering key for content mapping (the **granfilade** and the enfilade family key on tumblers), the endpoint type for links and spans (endsets are spans; the **spanfilade** indexes them), and the position type for the element stream / **permascroll** (ordinal shift drives element allocation and traversal). It deliberately does **not** provide version-derivation history: the document field records who allocated under whom, not what was copied from what (T6(d)); derivation needs a separate version graph — a handoff, not a responsibility of this layer. The prefix-as-ownership-domain model here is the substrate the ownership/baptism notes build on, and the span definition here is what span algebra and arrangement operations extend.

## Decisions for the builder

These are genuine engineering picks the note leaves open — distinct from its spec-level open questions.

- **Component representation:** bignum (recommended default) vs. varint-only vs. fixed-width-with-fallback. Fixed-width only with a discharged finite-model obligation.
- **Sequence storage:** inline small-sequence vs. persistent shared vector — decided by whether deep tumblers actually dominate your workload.
- **Frontier durability strategy:** per-allocation durable write vs. batch reservation vs. journal+snapshot. Default to journal-of-record + recomputable frontier registry + in-memory batch reservation, reusing the existing append-only journal.
- **Recovery cadence and granularity** (the builder's read of the note's durability open question): how often to persist the high-water mark — every allocation, every block, every checkpoint — and how aggressively to over-allocate on clean shutdown vs. crash. Over-allocation is always safe; reuse is never.
- **Where validation lives:** validate-at-admission and trust internal producers (recommended) vs. validate-everywhere. The former keeps the arithmetic flat and uniform.
- **Within-prefix concurrency model:** actor-per-prefix vs. lock-per-prefix vs. lock-free counter. Cross-prefix is coordination-free regardless; this choice is only about the single counter.
- **Subspace-context plumbing:** carry the subspace id alongside ordinals everywhere vs. an element-stream API that strips and reattaches it (recommended — it makes TA7a un-violable by callers).
- **Fixed-width hot cache:** whether to keep one for comparison/arithmetic with bignum fallback — a pure optimization, off until measured pressure justifies it.
- **At-rest encoding:** the humber varint vs. a simpler length-prefixed bignum sequence — a journal-format choice you can defer.
