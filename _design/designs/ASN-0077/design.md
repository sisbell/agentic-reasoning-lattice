## What this is

SHOWORIGIN is the substrate's read-only **attribution query**: given a span of content — one character or a whole chapter, addressed either in I-space or in some document's V-space — it reports the home document(s) that first allocated (baptised) that content. It is the "where did this come from?" probe, and nothing more: not who-has-it-now, not who-the-author-is, not the transclusion chain.

The single most important thing the note establishes is a *negative*: origin needs **no stored state**. It is a projection of the address itself. Most of the engineering judgement below flows from that.

## Design commitments

**Forced — downstream design cannot violate these:**

- **Origin is a pure projection of the address, not stored state.** `origin(a)` is the document-level truncation of the tumbler. Attribution therefore lives *inside* the address — the very bits used to fetch the bytes. There is no separable "origin metadata" to store, synchronise, or strip; this is why Nelson's attribution is "unstrippable." Every other commitment follows from this one.
- **Identity is by allocation event, not by content value (O9).** Identical bytes allocated under two documents get distinct addresses and distinct origins. SHOWORIGIN reports "quoted from the original," never "happens to match the same words."
- **Transclusion shares the I-address by reference.** Inherited from the substrate (ASN-0047), not chosen here — but SHOWORIGIN rests on it entirely: every document in a chain `d₁→…→dₙ` records the *same* I-address, so origin is invariant down the chain and any link is an equally good witness (O4). **Intermediate transcluders never appear in the result — only the original allocator.**
- **Origin is document-level and permanent (O5).** Distinct documents ⇒ distinct tumblers, so origin-equality *is* same-document; and a reported origin never changes for a fixed address under any reachable transition. Callers may treat it as eternal.
- **The query is read-only and idempotent (O10).** A passive observation: asking never perturbs the answer.
- **Any index or cache is a hint, never authoritative (O3).** The address structure is the source of truth; acceleration structures must remain recomputable from it.
- **I-span origins grow monotonically (O6); an empty answer is legitimate** and may become non-empty later.

**Conventional — chosen, not forced:**

- Returning the *set* of home documents for multi-origin spans (vs. a single "mixed" sentinel).
- The I-span lift reporting *content* origins only, silently dropping link addresses in range — a definitional choice.
- Offering two arities (I-span and V-span); one could be omitted.
- Result ordering — the spec imposes none (note this against Green's incidental ascending-tumbler order).

## What must be built

- **A pointwise origin projector** — from a well-formed content or link address, produce its document-level home tumbler by structural truncation, reading only the address.
- **An I-span resolver** — over a half-open I-interval, find the allocated content addresses present, project each, return the deduplicated set; correctly handle empty (legitimate result), singleton (the common case), and multi-origin.
- **A V-span resolver** — restrict a document's arrangement to the queried V-interval, decompose into maximally-merged blocks, project one origin per block (block uniformity, O2), dedup. Handles content and link subspaces uniformly; the link-subspace case trivially yields `{d}` (the home document itself).
- **A V-span admissibility check** — verify the queried V-positions are present in the *current* arrangement, and reject or narrow when contraction has removed them (O13).
- **Result assembly** — dedup into a set of document tumblers.

## Implementation approaches

**Pointwise origin — direct tumbler-prefix decomposition.** Parse the component sequence, locate the field separators, truncate at the document boundary. This is the spec read literally and is the right primitive: cost ∝ tumbler length, no I/O, no lock, embarrassingly parallel. Green's own evidence confirms the derivation is sound — allocation is document-scoped, so prefix truncation reliably names the allocator — yet Green *never wired it as a query path*, reaching for the spanfilade instead. The note's contribution is to elevate this projection to *the* primitive. **Pick it unconditionally**; it is the cheapest mechanism that meets the contract, and it belongs in the shared tumbler/address algebra, reused by every operation that attributes. One allocation-time guard worth adding (Green Q19): a *version of a non-owned document* gets its document ISA allocated under the user's *account*; ensure the allocator never emits content addresses whose nearest enclosing allocation is an account rather than a document, or the "document-level" (`zeros=2`) invariant the projection depends on is exactly what breaks.

**I-span lift — three options:**
- *Enumerate-and-project*: walk the allocated content in range, project, collect. Simple, correct, cost ∝ addresses. Fine for narrow spans.
- *Boundary-walk*: because allocation is document-scoped, the origins in an interval are just the document prefixes the interval crosses. Walk a 1-D I-address-indexed allocation tree — Green's **granfilade** is exactly this shape — and collect distinct boundaries crossed. Cost ∝ number of distinct origins. **Pick this for wide spans.**
- *2-D index (spanfilade-style)*: a `(I-range → document)` enfilade. Green's **spanfilade/DOCISPAN** is this shape — but it answers historical *containment*, returns a **superset** (every transcluder, plus documents that *deleted* the content — the index is append-only/write-only), keeps no origin flag, and imposes ascending-tumbler order with no origin priority. That is a *different question*. If you build an index for origin, key it on the **allocation** event (one entry per document's content sub-allocation), not on every containment.

Recommendation: enumerate for narrow, boundary-walk for wide; treat any 2-D index as a **hint**, recomputable on a miss, never consulted as authoritative. The single-origin weakest-precondition is the common case, so a fast path — "do the span's endpoints share a document prefix, with known single-document allocation between?" — short-circuits to a singleton without enumeration.

**V-span lift — block-decompose, then project per block.** Represent the arrangement `M(d)` as a **run/block structure** (V-range → I-range) — precisely the **POOM** enfilade shape. Restrict to the V-interval, take maximally-merged blocks, and project origin of each block's I-start *once* (O2 guarantees the whole block shares it). Cost ∝ blocks in range. **Pick this.** Optionally cache origin per block — exactly Green's per-crum **`homedoc`** field. Because origin is *permanent* (O5), this cache **never needs invalidation** (Lampson's best kind), but it is redundant with the block's I-start, trading space to avoid a cheap parse. Default to project-on-demand; add the `homedoc` hint only if the parse profiles hot or blocks are traversed far more than built. Green's `homedoc` is current-state and drops on DELETE — and that is *correct* here, because the V-span answer is defined against the *current* arrangement (O7/O13): when a block is removed, its origin should vanish from the V-answer.

**Permanence / recovery — falls out, isn't built.** Origin permanence is not a feature; it is a consequence of append-only content allocation with no address reuse. If content writes go to an append-only journal — this repo's `links.jsonl` + `paths.json` registry, recovered by replay — and addresses are assigned at write time and never reused, every address is stable and origin (a function of the address) is automatically permanent. The only promise to actively keep is *never reassign or reuse a content address*; the journal already enforces it. No SHOWORIGIN-specific durability machinery is needed.

**Admissibility (V-span).** Check the range condition against the live arrangement before answering. On a contracted arrangement, **reject-and-signal** ("pose a smaller query") rather than silently clamp to the surviving sub-span — so a caller never mistakes a narrowed answer for the full one.

## Guarantees to uphold

- **Permanence** — a reported origin never changes for a fixed address. *By construction*, given append-only allocation.
- **Identity-not-equivalence** — same origin ⇔ same allocating document; identical content from different documents ⇒ different origins. *By construction.*
- **Stateless derivability** — the answer depends only on the address(es), and for V-spans the arrangement restricted to the span. *By construction* — but this is the one guarantee that **requires active enforcement**: it breaks the moment an index is treated as authoritative and allowed to disagree with the projection. Keep every index validatable against the address structure.
- **Monotonic growth (I-span)** — origins only accumulate. *By construction*, given content permanence.
- **Read-only / idempotence** — *by construction*; enforce by giving the operation no write path at all.
- **Unstrippable attribution** — no metadata channel exists to strip; origin rides in the fetch address. *By construction*, provided you never introduce a "detached" content representation that drops the originating address.
- **V-span fidelity to the live arrangement** — transcluded-then-removed content correctly disappears. *Requires* the resolver to read the current arrangement, not an origin cache that outlives its block.

## How it fits

- **Below it:** tumbler/unique-parse algebra (the projection primitives and field-separator parse); the address-origin foundation (origin document-level, permanent, distinct-docs-distinct-tumblers); allocation discipline (document-scoped allocation, disjoint content/link sub-allocators, content permanence, arrangement-mutability-only, the transition kinds); span algebra (state-independent span denotation); arrangement/content-mapping (the `M(d)` map, block decomposition and consistency, link ownership); the closure schema (lifts single-step permanence and monotonicity to multi-step).
- **Beside it:** a *separate* historical-containment operation — Green's `find_documents_containing` over the spanfilade — answering "which documents have ever contained this," a superset including transcluders and even deleted documents. SHOWORIGIN deliberately does **not** do this; the note flags the two as distinct and the spanfilade as the wrong tool for origin.
- **Above it / hands to:** anything needing attribution — provenance UI, ownership/royalty accounting (origin's account ancestor names the owning *account*, though never a human — John Doe publication is allowed), transclusion-integrity checks. It does **not** hand off the transclusion *chain* (not transitive provenance); a chain-walker, if wanted, is a separate operation.

## Decisions for the builder

- **Index, or pure derivation, for I-spans.** Prefix-projection + boundary-walk may be all you need; a 2-D index is justified only if wide multi-origin spans are hot — and then key it on allocation (origins), not containment (transcluders), and keep it a hint.
- **Cache origin per block, or project on demand.** Permanence makes a per-block cache invalidation-free but redundant with the block's I-start. Default on-demand; cache only if the parse profiles hot.
- **Arrangement representation.** Run/block (POOM-style) vs. a flat position map; the block form is what the V-span lift wants for one-origin-per-block.
- **Admissibility policy for V-spans.** Reject inadmissible (contracted) queries vs. clamp to the survivor — I'd reject and signal.
- **Result type and order.** A set of document tumblers; dedup via sorted-by-tumbler or a hash set; ordering is unspecified — pick one and *document that there is no "originating document first" priority*, since a reader might otherwise assume one.
- **Single-origin fast path.** Whether to detect and short-circuit the common single-document span before enumerating.
- **Where the projector lives.** Put it in the shared address algebra, not inside SHOWORIGIN — every attributing operation reuses it.
