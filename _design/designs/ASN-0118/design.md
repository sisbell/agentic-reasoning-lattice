## What this is

The COPY operation — the system's **transclusion** primitive. It places content that already lives in the docuverse into a destination document by *reference*: it binds the destination's virtual positions to the source's existing content addresses, growing the arrangement and the provenance record but never the content store.

## Design commitments

**Forced — downstream design cannot violate these:**

- **Inclusion is by reference; the content store does not grow on COPY (CP1).** This single frame condition *is* the operation — every other property follows from it together with the permanence of the address space and the destination owning its arrangement but not the content it arranges. An operation that mints fresh content for the included material is REPLICATE — a different operation that breaks the architecture.
- **Identity is by address, not value (CP2).** The destination binds the *same* I-addresses the sources bind. There is one identity referenced from many places, never many equal copies. Two positions binding one address are permanently independent occurrences (CP4/M14) and may never be merged or identified.
- **Attribution is structural — read off the address, not stored as detachable metadata (CP5).** `origin(a)` is the allocating document, recovered by field projection and invariant while the address is stored. COPY can neither strip nor transfer it.
- **Reused content is immutable and byte-identical (CP10, inherited S0)** — same bytes because the same address.
- **The destination owns only its arrangement and its provenance entries** — never the content's identity, value, or home (CP5/CP6).
- **Provenance is monotone and permanent (P2).** A reference recorded once survives even deletion of the positions that caused it; the historical "ever referenced" relation only grows and is *not* recomputable from the current arrangement.
- **Resolution is a pure read of source state; the source is otherwise untouched (CP0b, CP6).**
- **Cross-origin material never merges (CP11/M16).** Assembling from *k* sources preserves the origin multiset verbatim — ≤ *k* distinct homes, counted with multiplicity — keeping each seam intact.

**Conventional — chosen here, deliberately, but a stricter system could differ:**

- **Accept-and-intersect admissibility.** Spans are designated by boundaries; positions the source doesn't bind are silently skipped; span depth/shape is neither normalized nor validated (the note drops ASN-0058's condition iii). This matches udanax-green's unconditional acceptance; resolution restricts to whatever is bound.
- **Forward displacement implemented by reusing INSERT's existing placement primitive (CP3).** The shift *mechanism* is the genuinely conventional kernel. (That the displacement is *per-subspace* — only `s_C` shifts, the destination's link positions fixed — is **not** a choice but CP6, a frame condition the operation cannot violate; the note's composite proof works hard to discharge it.)
- **W ≥ 1; empty placement is a no-op.**
- **Provenance redundancy is free.** Re-recording an existing pair is a set no-op, so skip-vs-re-emit is an implementation choice, not a semantic one.

## What must be built

- **A spec-set resolver** — read the source arrangements over the named spans and return content addresses as ordered runs in spec-set order. Pure read; tolerant of unbound positions (restrict, never reject); preserves source-run boundaries so distinct origins stay distinct. **Enforce content-residence** as a precondition — every *bound* (active) position must lie in the text subspace `s_C`. This is load-bearing, not cosmetic: without it resolution can read an address out of the link store `dom(L)`, and the placement would then bind a link address into a content position, violating referential integrity (S3★). COPY as specified is therefore **content-only**; transcluding a *link* by reference is unspecified — the note's open question 5 — so do not assume the operation generalizes to the link subspace `s_L`.
- **An arrangement placement (splice) primitive** — bind the resolved sequence at a *valid insertion position* `p` (inside the existing run or at its boundary, `p ∈ [min, max+1]`; on an empty subspace, the canonical first position) and displace trailing same-subspace content forward by `W`, preserving order and prior bindings, **vacating the old keys** (so no position is double-bound), leaving other subspaces and other documents untouched. The result is hole-free *because* `p` is valid and the `W`-block is contiguous with the retained prefix — vacating keys alone does not prevent gaps; an out-of-range `p` would leave one. This is INSERT's primitive.
- **A provenance recorder + reverse index** — record `(address, document)` references and answer "which documents reference this address/span?"; monotone/append-only; run-granular; dedup somewhere.
- **Atomic commit + recovery** — present the composite as one logical, atomic change; survive crash by journal + replay; snapshot to bound replay.
- **A consistent source snapshot for resolution** — resolve against a coherent view of the source arrangement without locking the source.

**Free — no build, all consequences of content-addressed sharing:** link inheritance, origin attribution, immutability preservation, source-state isolation.

## Implementation approaches

### Arrangement representation (this choice fixes both resolver and placement cost)

Three viable representations, in increasing power and complexity:

1. **Persistent ordered map** V-position → I-address, absolute keys. Range query for resolution is O(log n + k). The splice inserts `W` bindings and then *re-keys* the trailing region (shift by `W`) — O(trailing), but structural sharing bounds allocation. Simplest; the pre-edit root is a free snapshot.
2. **Run-compressed persistent structure** — store maximal lockstep runs (V-start, I-start, width) in a persistent ordered/finger structure. Resolution returns runs directly; placement splices runs and can coalesce. Storage and cost are **O(span count), not O(byte count)** — the same property udanax-green's POOM (the *arrangement*) exhibits, where each contiguous run is one bottom crum regardless of byte volume (`isanextensionnd` widens an existing crum only when the incoming run shares its `homedoc` *and* abuts its right edge in both I and V, `reach == origin`; otherwise a new crum).
3. **Displacement-offset enfilade (the POOM), mutable or persistent** — nodes carry offsets relative to parent, so a mid-document insert "makes a gap" by adjusting one cut path: O(log n) shift independent of trailing size, and 2-D so it also answers I→V queries. The proven-at-scale udanax structure; most bookkeeping. udanax's own enfilade is *mutable*, hence gives no snapshots — but that is a property of its mutability, **not** of relative-offset addressing. A **persistent** displacement-offset enfilade (on a splice, path-copy the cut path and share the rest; relative offsets leave untouched descendants shared verbatim) keeps the O(log n) shift, adds free pre-state snapshots, and stays O(span count) in storage.

**Pick:** for a content substrate the **persistent displacement-offset enfilade** (3) is the strongest default. It is the only representation with O(log n) shift *independent of trailing size*, and that matters because mid-document insertion is *first-class* for COPY, not exotic — the note's entire displacing-case analysis and udanax's shared `makegappm` shift path are exactly about inserting into the middle of an existing run. Its persistent form also supplies the free pre-state snapshots the concurrency and self-transclusion strategies below depend on, plus the 2-D I→V query. The earlier instinct to pit run-compressed (2) [free snapshots] against the enfilade (3) [O(log n) shift, *but no snapshots*] is a false tradeoff: the "no snapshots" was udanax's *mutable* enfilade, not the offset structure, and persistence dissolves it — so no displacing-case benchmark is needed to justify reaching for (3). Choose **(2)** instead only to avoid the enfilade's bookkeeping, accepting that its splice is **O(trailing runs), not O(log n)** — fine when documents are modest, but for COPY's first-class mid-document inserts, price that in. Choose **(1)** only when you want the least machinery and documents are small enough that an O(trailing) re-key never bites.

**Correctness invariant for any representation:** the splice must *vacate* pre-shift keys, not merely add shifted copies (CP3c closes the domain so each position carries exactly one binding — S2 functionality). Re-keying does this automatically; the enfilade cut does it; a naive "insert shifted, leave old" double-binds and breaks functionality. And the displacement is **per-subspace** — shift only `s_C` positions, leaving the destination's link positions fixed (CP6). Udanax's proven two-blade gap (cut at `p`, bounded at the next subspace boundary) is exactly this.

### Resolution

**Pick:** resolve by range-restricting each source arrangement to the span's denotation, decomposing into maximal runs, and concatenating in spec-set order — i.e. reuse ASN-0058's `resolve`; do not reinvent it. **Derive each resolved address by reading the arrangement at the bound position (`M(d_s)(v)`), never by offset arithmetic from the span's start tumbler** — this read-the-image discipline is the note's central immunity result. It is precisely what makes the abstract resolution immune to udanax-green's cross-depth bug, where boundary differences are clipped to integer offsets (`context2span`/`tumblerintdiff` discards sub-depth structure), so a cross-depth boundary is silently mis-read as a content offset and the wrong I-spans returned; the residual question of assembling differing-depth spans into one region is the note's open question 2. **Keep the result run-compressed; never materialize the flat W-length list** (the note's `expand` is a reasoning device, not an object to build).

- **Partial binding:** intersect with bound positions, with no validation of span shape or depth — pure order intersection. Unbound positions vanish silently. This matches the note's boundary semantics and udanax-green's no-normalize, intersection-only behavior. If you want a stricter contract, add a boundary check *at the API edge*, but keep the resolver core intersection-only.
- **Source consistency without a lock:** capture the source arrangement's persistent root once and resolve against it. Content immutability plus a captured root means **no source write-lock is needed** — realizing udanax-green's "source unlocked" discipline *safely* (udanax leaves the source safe only by convention; the captured persistent root makes the cheap option correct). This also makes **self-transclusion (CP9) trivial**: resolve against the pre-edit root, then build the new root — the pre-state read is free.

### Placement

COPY *is* INSERT's placement fed resolved existing addresses instead of freshly allocated ones — udanax-green confirms the two operations share one insert-and-gap path, differing only in address provenance. **Build the splice once and share it.** The operation: splice resolved runs at a valid `p`, displace trailing `s_C` content by `W`. On an empty destination subspace (`V_{s_C}(d) = ∅`) the placement instead establishes the document's first content at the canonical first position, and the builder must choose the new subspace's tumbler depth `m ≥ 2` (ValidFirstInsertionPosition) — surface that choice wherever positions are tumbler-keyed.

**Run-coalescing on placement (optional compaction):** merge a placed run into an adjacent existing run iff **I-contiguous AND V-contiguous**. **Never coalesce across a discontiguity** — CP11/M16 forbids merging across origins, merging would erase the seam and corrupt the origin multiset, and I-contiguity is exactly the guard that prevents it (contiguous I-addresses already share one origin, M16a). This is storage-level compaction only: it folds a contiguous lockstep run into one entry and does **not** "merge or identify occurrences" in the M14 sense — the logical V→I multimap is unchanged, so CP4/M14's permanent independence of distinct occurrences is untouched. So, gated on I-contiguity, it carries **no risk to any guarantee the note states**. But it is an optimization, not a free win, and it *diverges* from the only proven implementation: udanax-green coalesces only under a stricter guard — equal `homedoc` *and* right-edge I/V contiguity (`reach == origin`) — and `homedoc` tracks the *immediate* source, which under chained transclusion can differ from the structural `origin`. Bare I-contiguity coalesces strictly more, erasing that immediate-source distinction; whether anything needs the distinction is exactly the note's open question 4 (the correspondence relation). **Default to udanax's `homedoc`-guarded behavior**; relax to bare I-contiguity only if run-count is a *measured* problem.

### Provenance recorder + reverse index

Be explicit that there are **two distinct objects**:

- **Live containment** ("which documents *currently* reference `a`") is recomputable from arrangements (`a ∈ ran_C(M(d))`) — a pure hint, rebuilt by replay, needing no durable storage of its own.
- **Historical provenance** ("which documents *ever* referenced `a`", CP8/Σ.R) is **not** recomputable — P2 keeps the pair after the positions are deleted. This is a log; it must be durable, and in practice it lives in the journal (every COPY's provenance pairs are journal payload).

**Pick:** maintain a reverse index keyed by I-address/I-span → documents — a **query structure over the durable provenance records (Σ.R)**, recorded at **run granularity** (O(span count)), with **blind append and dedup at query time**. This is exactly udanax-green's DOCISPAN behavior — append-only, no delete path, redundant entries tolerated, `find_documents` returning a superset deduped on read. It is the Lampson-cheapest mechanism (no read-before-write, no delete) that satisfies a set-membership contract. But be precise about what is *recoverable* and what is *authoritative*: the historical provenance Σ.R the index ranges over is **not** recomputable from current arrangements — P2 keeps the pair after the positions are deleted, so arrangements yield only *live* containment, a strict subset. The Σ.R *records* are therefore authoritative durable state: snapshot the accumulated relation (it is append-only, so snapshot + journal tail is complete), and rebuild the query *index* over those records on load. Do **not** rebuild the historical index from arrangements, nor from a journal truncated past a snapshot — either loses every pair whose positions were deleted before the snapshot, exactly the pairs P2 makes permanent. Only a *live-containment* index would be a hint safe to omit-and-rebuild from arrangements. Because re-recording is idempotent on the set, the recorder needs no read-before-write.

If a use case genuinely needs *live* containment (prune on delete) rather than "ever referenced ⊇", that is a different, stronger index with a delete path — build it only then. The note commits to the historical reading (P2), so the append-only index is the right default.

**Links need nothing here.** COPY does not touch the link→content index; link inheritance (CP7) is free, because links cover I-addresses and placing those addresses into the destination's range makes coverage ∩ range nonempty for the existing discoverability query. COPY updates only the content→document index — the isolation udanax-green's spanfilade design already enforces.

### Atomicity, journaling, recovery

**Pick:** journal each COPY as one logical record — *(destination, insertion position, resolved runs, provenance pairs)* — append durably, then apply in memory; replay on load. This is the repo's `links.jsonl` + replay pattern. Journaling the **resolved runs** (not the raw spec-set) makes replay a self-contained blind apply: no re-resolution, robust to resolver changes, with the displacement re-derived from `p` and `W`. Size is O(span count) — already cheap. The compact alternative — journal the spec-set request and re-resolve on replay — is correct (immutability + ordered replay make re-resolution deterministic) but couples replay to resolver determinism; choose it only if journal size bites.

- **Atomic visibility:** with persistent structures, "apply" is a single root-pointer swap per affected structure (the destination's arrangement, the reverse index). Stage the new roots, then publish — the displacing case's internal contract-then-extend is never observable because consumers see only committed roots, honoring the composite boundary (P4★). Append the journal record with an **atomic write/rename** (this repo has been bitten by torn reads of shared registry state — atomicity here is not optional), then swap.
- **Snapshot/recovery:** snapshot arrangements *and the accumulated historical provenance Σ.R* (both authoritative), plus the journal tail. The reverse *index* (the query structure) is recoverable — **omit it from snapshots and rebuild it from the snapshotted Σ.R records + journal-tail provenance on load**. What you must **not** do is omit Σ.R *itself* and try to rebuild it from arrangements: arrangements give only live containment, so every pair whose positions were deleted before the snapshot — exactly the pairs P2 makes permanent — would be lost. Only a *live-containment* index (recomputable from arrangements) is a hint safe to omit-and-rebuild; the historical relation is durable state.

### Concurrency

**Pick:** take the **destination** under a write exclusion; resolve the **source against a captured snapshot**, no source lock. Content immutability keeps resolved addresses stable under concurrent source edits; the captured root gives resolution a coherent source arrangement. This is udanax-green's target-WRITE / source-unlocked discipline, made correct by the snapshot. Document-granular locking is the simplest correct choice; go finer only if hot-document contention shows up.

## Guarantees to uphold

**Hold by construction** (fall out of content-addressed sharing + an immutable store):
- Permanence/immutability of reused content (CP10) — store untouched.
- Origin invariance and origin-multiset preservation (CP5, CP11) — addresses carry origin structurally; reuse rides the homes along, provided cross-origin runs never merge.
- Link survival/inheritance (CP7) — shared identity + the existing link index; nothing COPY-specific.
- Source-state isolation (CP6) — only the destination's arrangement and the provenance index are written.
- Shared identity / multiplicity (CP4) — many references to one address is the native model.

**Require active enforcement** (the splice and recorder must get these right):
- Content-residence precondition (`enabled(COPY)`) — reject any spec-set whose bound positions leave `s_C`; otherwise resolution reads `dom(L)` and placement binds a link address into a content position, breaking S3★. COPY is content-only (link-transclusion is note OQ5, out of scope).
- Domain closure / functionality (CP3c, S2) — vacate old keys (⇒ no double-binding); displace per-subspace (shift only `s_C`).
- No holes / contiguity (CP3 — D-MIN/D-SEQ/D-CTG) — *not* a consequence of vacating keys but of placing at a valid insertion position `p ∈ [min, max+1]`, laying a contiguous `W`-block that abuts the retained prefix. Enforce valid-`p` (or accept gaps as a deliberate choice).
- Order preservation and injectivity (CP3) — never reorder neighbors.
- Exact multiplicity (CP4) — displacement *re-keys* (replaces) references rather than duplicating them: `+W` total, no spurious refs.
- Provenance closure ⊆ (CP8) — only placed pairs enter; the recorder writes nothing else.
- No content/entity allocation (CP1, CP12) — the operation runs no allocate/mint step; this is a contract to *not* do something, easy to break by inadvertently allocating.
- Atomic composite boundary — partial application must never be observable.

## How it fits

- **Leans on the content store** (immutable, append-only I-address→value; ASN-0036) — reads address existence, never writes it.
- **Reuses the arrangement-resolution subsystem** (ASN-0058) for run decomposition — do not duplicate it.
- **Shares the insertion/placement primitive** (ASN-0082) — COPY is that primitive with resolved addresses.
- **Hands to link discoverability** (ASN-0098, coverage ∩ range) — placement *enables* discoverability; COPY does not compute it.
- **Records into the provenance/reference index** (the spanfilade analogue) consumed by "which documents contain this?" queries.
- **Operates under the transition discipline** (ASN-0047) — a composite of K.μ⁻/K.μ⁺/K.ρ with no K.δ and no K.α; the journal/atomicity layer realizes its composite boundary.

## Decisions for the builder

Distinct from the note's spec-level open questions, these are choices you must make to ship:

- **Arrangement representation:** absolute-key ordered map (simplest, O(trailing) shift — only when documents are small) vs run-compressed persistent structure (O(span count) storage + free snapshots, but O(trailing-runs) splice) vs **persistent displacement-offset enfilade** (O(log n) shift independent of trailing size, free snapshots, O(span count), 2-D I→V — the strongest default for a content substrate; most bookkeeping). The mutable enfilade's "no snapshots" is a property of its mutability, not of relative-offset addressing — persist it and the (2)-vs-(3) tradeoff dissolves.
- **Resolved sequence:** keep run-compressed end-to-end (recommended) vs materialize flat.
- **Journal granularity:** physical resolved runs (self-contained replay, recommended) vs logical spec-set request (compact, needs deterministic re-resolution).
- **Reverse-index policy:** append-only historical index over durable Σ.R records — snapshot Σ.R as authoritative state, rebuild only the query structure on load — read-dedup (matches P2, recommended) vs live-containment index with a delete path, recomputable from arrangements (only if "currently contains" exactly is needed); write-dedup vs read-dedup.
- **Run-coalescing on placement:** off / `homedoc`-guarded like udanax (recommended default) vs bare I-contiguity (coalesces more, drops the immediate-source distinction; only if run-count is a measured problem) — never coalesce across a discontiguity, either way.
- **API-edge admissibility:** accept-and-intersect like the note/udanax vs reject malformed or unbound spans; and whether to **surface the partial-binding shortfall** (placed `W` vs nominal extent) to the caller or keep it silent.
- **Insertion-position validity:** enforce the note's valid-`p` (`p ∈ [min, max+1]`, contiguous result, no holes) vs accept-any like udanax (`acceptablevsa` is an unconditional stub — tolerate gaps); plus, on an empty destination, the new subspace depth `m ≥ 2`.
- **Locking granularity and source-snapshot mechanism:** captured persistent root (recommended) vs read lock vs copy.
- **Snapshot cadence; whether to persist the reverse *index* or rebuild it from records** (recommended: rebuild the index, but snapshot Σ.R itself as authoritative state — never omit-and-rebuild it from arrangements).
