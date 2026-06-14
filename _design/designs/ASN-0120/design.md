## What this is

ASN-0120 defines **MAKELINK** — the write-side primitive of the connection layer. It is the operation that creates a link: given a home document and three content-region arguments (from, to, type), it records a typed connection and returns the link's permanent identity. Its entire substance is a single coordinate conversion — naming content by mutable *arrangement position* on the way in, recording it by immutable *content identity* on the way out.

## Design commitments

These are locked in for the whole system; downstream design cannot violate them.

- **Links record content by identity, never by position.** The V→I conversion *is* the operation. Endsets store I-addresses (content identities), not the V-positions the caller supplied. This is forced — it is the single thing everything else (survivability, stable discoverability, reference permanence) is bought with. Get this wrong and the rest collapses.
- **Resolution is a one-time snapshot taken at creation, against the current arrangement.** The link captures the V→I mapping as it stands when the link is made, then freezes it. No later edit to any source ever revisits a created link. Forced.
- **A link's identity is a fresh, permanent, never-reused address allocated under its home document, with the home encoded in the address itself.** There is no mutable "home" attribute that could drift; residence is structural. Forced — and it forbids coalescing: two MAKELINK calls with identical arguments produce *distinct* links.
- **Home (where the link lives) and endsets (what it connects) are orthogonal.** The operation imposes no relation between the home document and the resolved content. A link in C may connect A to B and touch nothing in C. Forced — this is precisely what makes third-party annotation of published, un-owned content possible.
- **Discoverability is by content identity and is decoupled from residence — and it is not a separate action.** A link is findable from any region any endset references, regardless of home. Critically, the note is emphatic that discovery is *the standing meaning of having content-identity endsets in the store*, not an indexing step MAKELINK performs. This is the central Lampson move in the whole note: the discovery index is a **hint over the endsets**, not authoritative state MAKELINK must maintain.
- **Three ordered endsets; the third is a mandatory type.** Order is a semantic from/to *label*, not a one-way traversal valve — discovery is symmetric across all three endsets. Two endsets assert a bare connection; the type endset (which must resolve non-empty) makes it a *typed relation*, matched by address, not by content.
- **Coverage is pinned; span decomposition is free.** What the endset *covers* (the resolved I-address set) is fixed extensionally; *how* it is cut into spans is an implementation freedom (representation independence). The decomposition is nonetheless observable through raw value read-back and membership tests.
- **A link, once made, is immutable.** No operation in the vocabulary removes a link or rewrites its value.

Merely *conventional* (not forced): the first-link V-position depth (the note fixes `m=2` but says any `m≥2` serves); the choice of span decomposition; which of the two non-type slots a user *reads* as "from."

## What must be built

Functionally, an implementation honoring this note must provide:

- **An endset resolver.** Given a spec-set (source document + list of V-spans), read each source's *current* arrangement, keep only positions active *and* inside the span interval, and collect the I-addresses they map to. Must tolerate partial spans (some named positions since deleted), depth-mismatched specs, and empty results.
- **A well-formedness gate plus the type precondition.** Reject specs that name an unallocated source, escape the content subspace, sit below depth 2, or lack an ordinal displacement; and reject calls whose *type* slot resolves empty. Validation must be total and up-front.
- **An endset packager.** Turn a resolved I-address set into spans whose coverage exactly traces the substrate-allocatable address set on the resolved set — without claiming any address that was not resolved (notably, never merging across an unallocated chain frontier).
- **A link-identity allocator.** Mint a fresh, never-reused, link-subspace address scoped to the home document.
- **A link writer.** Record `home-address ↦ (from, to, type)` permanently.
- **A home seater.** Bind one fresh link-subspace position in the home document's arrangement to the new link, making it enumerable by the home's owner.
- **A discovery capability.** Make the link findable from any content region any endset references, with home ignored — by index or by scan.

## Implementation approaches

**Endset resolution (the V→I conversion).** The arrangement is a V-position→I-address partial function; resolving a span is a range query over an order-convex interval, collecting the images of active positions. Two proven shapes:
- *Persistent ordered map keyed by V-position* (e.g. an `im` balanced-tree map). A range scan over the span interval yields the active positions and their I-addresses directly; contiguous runs fall out of the scan for free. Cheap, simple, and exactly enough for MAKELINK, which only ever needs the V→I direction at creation.
- *Enfilade (Green's POOM)* — a cumulative-offset 2-D tree carrying both V↔I directions and run-coalescing in one structure. Green walks it with `permute`, emitting one I-region per contiguous run as a *sporgl* (I-origin, I-width, source-doc). This is the proven approach and it buys the *reverse* (I→V) direction that FOLLOWLINK needs.

Pick by where the reverse mapping belongs: **build the simple ordered map for MAKELINK and let the read-side subsystem own the bidirectional index.** Don't pay for an enfilade just to resolve at creation — that puts a read-side mechanism in a write-side operation. The reverse direction is a different function and belongs elsewhere. (Verified Green behavior worth inheriting: resolved I-widths trace *exactly* allocated content and never reach past the allocation frontier — your range scan should clip to active positions, never round up to chain boundaries.)

**Validation ordering.** Because identity allocation must be fresh and never-reused, *resolve and validate all three slots before touching the allocator.* The type-slot precondition forces a resolution anyway; checking the full `enabled` predicate first keeps the rare rejection path from burning (or having to roll back) an address. Common case fast, rare case correct.

**Endset packaging / decomposition.** Coverage is pinned, decomposition free, so choose for simplicity:
- *Reference decomposition* — one unit-depth span per resolved address. Trivially satisfies the recovery equation; no merge logic; no way to over-reach. The Lampson "simplest thing."
- *Merged canonical spans* — fold chain-adjacent resolved addresses into one wider span to save room. Legal **only** when every chain address in the run is resolved; one unresolved or frontier member would make the span cover unresolved content and break the recovery equation.

Recommendation: emit one span per contiguous *resolved* run as it falls out of the range scan — you get most of the merge benefit with no extra adjacency bookkeeping, and you never merge across a gap because the scan only sees active positions. Document that decomposition is observable on raw read-back, so two coverage-equal links are not value-equal. (Green's `vspanset2sporglset` is deterministic given arrangement state but explicitly *non*-canonical — fragmentation reflects insertion history. That is fine here and confirms decomposition is unobservable to the coverage-determined views.)

**Identity allocation.** Green allocates `docISA.0.2.N` with N monotone *per home document* (no global link counter). Two ways to keep "fresh + never-reused" durable:
- *Recompute the high-water mark on recovery* — the next address is `max(existing links homed at d) + 1`, derivable by replaying the link journal. This makes the counter a **hint**, not authoritative state — preferred. Green effectively does this (append-at-extent / scan for the previous link).
- *Persist a per-home counter* in a registry (the `paths.json` analog). Faster, but now it is authoritative state you must keep consistent with the journal across crashes.

Prefer the hint: the link journal is already the source of truth, so derive the counter from it.

**Link write + home seating (atomicity).** The link store never mutates entries, so writing the link is an **append to a journal** — the repo's `links.jsonl` recovered by replay is exactly right. The home seating is the *one* in-place arrangement edit, and it is append-at-the-link-subspace-extent, so it never shifts existing positions (Green confirms this shift is structurally a no-op). The composite has an intermediate state, so make the two effects crash-atomic with **one journal record** capturing both the link value and the home binding; apply to in-memory state, then fsync; recover by replay. This is plain write-ahead logging and needs nothing fancier.

**Discovery.** This is the design-critical choice, and the note hands you the principle: the index is derived, not authoritative.
- *Scan* — to find links from a region, walk the link store and test coverage∩region. Always correct, nothing to maintain, O(#links) per query. Fine at small scale.
- *Materialized index* — Green's **spanfilade**: an I-address-keyed range structure mapping content addresses → links covering them, with the home dimension **explicitly nulled out** so residence plays no role. Fast containment queries; the proven approach for scale.

Either way the index is a **hint recomputable from the link journal** — so it needs no durability of its own, a miss can fall back to a scan, and rebuild-on-load is free. Build it keyed by the *resolved I-addresses* (a range/interval structure if you must answer span-overlap queries; an ordered map on exact addresses if point lookups suffice), and **never key it by home** — that single discipline is what upholds discoverability-decoupled-from-residence. The crucial architectural stance: MAKELINK's contract is discharged by writing the endsets; index maintenance lives in the discovery subsystem, eager or lazy, as a view.

**The direct-I-address path (out of scope here, present in Green).** Green exposes an `ISPANID` argument shape that supplies I-addresses directly, bypassing V-resolution — which can record ghost or foreign endsets outside the content store. MAKELINK-via-V-specs cannot do this (every resolved address is real content). If you offer a direct path, know that it escapes the well-formedness containment and is a distinct operation, not a mode of this one.

## Guarantees to uphold

- **Permanence of the link** — by construction, if you simply never expose a delete or rewrite. The append-only journal gives it for free.
- **Endset immutability and survivability** — by construction, *given* you record I-addresses against an immutable content store. The reference outlives any editing of the content it names because edits touch the arrangement, never the I-addresses. This is the payoff of the V→I conversion; it is the one thing you cannot get wrong.
- **Identity uniqueness / never-reuse** — *active enforcement.* The allocator must be monotone and durable across crashes — recompute the high-water mark on recovery (or journal allocation before use); never reset it.
- **Home-scoping of identity** — by construction; home is the address prefix, fixed at allocation.
- **Residence/application orthogonality** — by construction, upheld by a *non-feature*: never add a precondition relating home to endset content.
- **Discoverability decoupled from residence** — by construction *if* the discovery index ignores home; a home-scoped index would silently break it. Active discipline: null the home dimension.
- **Type-endset non-empty** — *active enforcement.* Reject empty type resolution before allocating. (Note: Green does *not* — it stores links with empty type and even empty from/to slots silently. The spec requires rejection of the type slot; this is the one place implementation and specification deliberately part.)
- **Coverage exactness (recovery equation)** — *active enforcement in the packager.* Never let a span claim an allocatable address that wasn't resolved; the reference decomposition, or merging only fully-resolved runs, discharges this.

## How it fits

MAKELINK sits in the connection/link layer as the write-side counterpart to FOLLOWLINK and content-region discovery on the read side. It leans on:

- the **content store** for immutable, permanent I-addresses (the survivability substrate);
- the **per-document arrangement** (V→I mapping) as the input it resolves against;
- the **link store** and its **link-subspace allocator** for permanent link values and fresh home-scoped addresses;
- the **subspace conventions** and the **composite-transition discipline** (link allocation followed by link-subspace seating) that frame its two elementary steps;
- the **span algebra** for canonical spans and the adjacent-run merge;
- **content-region resolution**, which MAKELINK lifts from a single source to a spec-set (extending it along two axes: it tolerates partial spans and gives depth-mismatched/empty specs a value where single-source resolution is undefined).

It hands its output to the **discovery / FOLLOWLINK** subsystem (which consumes the recorded endsets — the discoverability biconditional is read against coverage), to **type matching**, and to **projection**. Every downstream link operation builds on the link values MAKELINK writes.

## Decisions for the builder

Distinct from the note's own open questions (what an empty non-type endset *means*; how to handle an endset that points into the link subspace):

- **Discovery: index or scan, eager or lazy.** The note guarantees discovery as a view over endsets but leaves the realization to you. Whichever you choose, treat it as a recomputable hint — no separate durability, miss falls back to scan.
- **Span decomposition policy** — reference (one span per address) vs. merged runs. Coverage-equivalent; choose for space vs. simplicity, knowing read-back exposes the choice.
- **Allocation counter: recomputed hint vs. persisted registry entry.** Prefer recompute-on-recovery unless you have measured a reason to cache.
- **Atomicity mechanism for the composite** — a single WAL record covering both the link write and the home seating is the simple, sufficient choice; anything heavier is unjustified.
- **Whether to expose the direct-I-address endset shape** at all, accepting that it bypasses content-containment and can record ghost/foreign endsets.
- **How strictly to follow the spec over Green on empty slots** — you must reject empty *type*; decide whether to also reject (or, like Green, silently store) empty from/to, which the spec *admits* but which yield a link discoverable only through its populated endsets.
