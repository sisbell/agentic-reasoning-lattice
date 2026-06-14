## What this is

CREATENEWVERSION (the `VERSION` operation) is the **fork primitive** of the document subsystem: it mints one fresh document identity whose initial arrangement *transcribes* an existing document's content arrangement by reference, sharing the underlying content without copying it and leaving the source provably untouched. It is the single operation by which "make a new version of this document" enters the system.

## Design commitments

These are locked in for everything downstream. I mark **[forced]** (the spec/foundations leave no choice) versus **[conventional]** (this note's choice, defensible to revisit).

- **A version is a third thing — neither a copy nor an alias.** [forced] Exactly one entity is minted: the identity. Content is shared by reference; the arrangement is an independently mutable snapshot. This forecloses both copy-based and alias-based version implementations everywhere.
- **Forking may not allocate content — sharing is a prohibition, not an economy.** [forced] Because content identity is identity of *origin*, not of value (S4/GlobalUniqueness), a value-copy yields different addresses, which severs link carry-through, correspondence, and attribution. The operation shares existing addresses; it must not mint new ones for the same bytes.
- **Identity allocation is registry-pure.** [forced] The new address is a function of the registry and one base address alone — no content, no arrangement, no clock, no global counter, and *no bookkeeping held by the source*. The allocator is stateless against the content store.
- **Allocation is the gap-free, monotone frontier.** [forced] Versions occupy a contiguous prefix of the namespace stream; the next version is the first absentee. Skipping is disallowed — it would void the high-water mark and make version enumeration unable to terminate.
- **For owned forks, ancestry is encoded in the identity.** [forced, given the address format] The version ID is a single-component extension of the source ID, differing in the document field alone (node/user/account fields preserved). Allocation lineage is read by truncation, the final component is the allocation ordinal — but decoding these as *derivation* and *fork* rank is sound only under the discipline noted next.
- **Address-decoded derivation and fork-rank hold only under VD (version-namespace discipline).** [forced conditional] The address always encodes *allocation lineage*; reading it as *derivation* (or the final component as a *fork* rank) requires that nothing but forks allocate into a version namespace. ASN-0047's J4 is a live counter-client — it allocates into the very same version sub-allocator — and any discipline-conforming allocation may take the frontier, so one interleaved non-fork allocation gives the k-th fork a rank > k and silently corrupts the decoding. This is OQ1.
- **Cross-owner forks are severed from address-encoded ancestry — by theorem.** [forced] When the forker is not the owner, the version lands in the forker's own account namespace and provably cannot prefix-encode the source. The only surviving tie is shared-content provenance.
- **The source is strictly untouched; the fork writes no forward pointer.** [forced by the frame] Whatever records the fork lives only in the version's identity and the version's provenance rows — never in the source. The fork is strictly additive.
- **The arrangement snapshot is function-level (representation-free).** [forced by M3] The spec constrains the V→I mapping, not its block decomposition; an implementation may re-derive and re-block freely.
- **Fork depth must be unbounded.** [forced] A fixed depth cap creates the renumber-or-refuse dilemma at the cap. The identity format must admit unbounded length.
- **A completed fork carries its full effect; indivisibility is an implementation obligation, not a foundation guarantee.** [forced] The terminal boundary carries v together with its snapshot and provenance (couplings evaluated initial-to-final), so no *completed* VERSION returns a torn version — that boundary invariant is what's forced. The foundations do *not* make the composite indivisible: the interior state (v allocated, `M(v)=∅`) is reachable, and nothing forbids another composite beginning there. Non-observability of interior states is an *implementation* property (single-threaded run-to-completion, as the udanax-green evidence shows), and serializing concurrent forks of one source is OQ4.
- **Content anchoring is the *only* cross-fork connectivity channel.** [forced by V2b] Links carry through via shared content addresses; the link subspace (links about links) cannot be transcribed.

## What must be built

- **An identity allocator** that returns the next gap-free frontier address given the registry and a base (the source, for owned forks; the forker's account, for cross-owner) — registry-pure, monotone.
- **A registry/index** over allocated identities supporting membership (freshness), the allocator's max-child query, and ordered range scans for downward navigation (a document's versions; its descendants).
- **An ownership resolver** that derives a document's effective owner positionally from its address and the set of principals, to branch the operation and to settle the version's owner. Per P-tier (`ω(d_src)=π ∨ zeros(pfx(π))=1`), the cross-owner branch is in-domain *only for an account-tier forker*; a node-tier principal forking a document it does not own is outside VERSION's single-identity domain (it would have to mint both an account and a document under it) and must be rejected or routed elsewhere.
- **An arrangement snapshotter** that captures the source's *content-subspace* arrangement at fork time and installs it as the version's initial arrangement — respecting the subspace boundary (content only; link subspace empty).
- **A provenance recorder** that adds exactly the version-side rows `{(a, v) : a ∈ A}`, deduplicated to the shared address set; together with the pre-existing source rows `{(a, d_src)}` (P4★ at the boundary) these form the dual witness (V9w).
- **A composite/transaction boundary** that makes allocate → snapshot → record atomic to any external observer, with a recovery rule that rejects torn forks.
- **A source-read path requiring no authority** and writing nothing back to the source.

## Implementation approaches

### Identity allocation (the frontier)

The frontier rule is "next sibling of the max existing child, or the first child if none." Two ways to answer the max-child query:

- **A — derive on demand from an ordered registry.** Keep identities in an ordered map keyed by tumbler; the frontier is a range query (max key under the source's subtree, incremented). This is exactly udanax-green's allocator: `findisatoinsertnonmolecule`/`findpreviousisagr` query the *live* granfilade for the maximum key under the source and increment — there is no cached "next available" pointer, so allocation is stateless against the store and yields `.1` then `.2` with no deletions. **Pick this by default:** the registry is the single source of truth, recovery is trivial, and it honors registry-purity directly. Cost is O(log n) per fork.
- **B — cache a per-namespace high-water mark as a *hint*.** O(1) allocation, but only worth it under allocation pressure. Per Lampson, keep it recomputable-on-miss, never authoritative: the spec's registry-purity (V5b) guarantees the frontier is a pure function of the registry, so a lost or stale hint is always rebuildable by range scan. Don't make it durable truth.

Both must avoid a global counter and any per-source durable counter — the note forbids source-side bookkeeping, and udanax-green confirms the live-query design.

### Registry / index

Make this **one ordered structure keyed by tumbler address**, not several. *The structural-sharing recommendations here and in the snapshot section below assume a persistent-immutable-structure engine (a Rust/`im`-style target with persistent ordered maps); nothing in the note or evidence fixes that target, and on a mutable B-tree the cheap-snapshot and copy-on-write properties they rely on do not hold — there, fall back to explicit indices and copies.* On such an engine, a persistent ordered map (`OrdMap`) buys cheap whole-registry snapshots (matching the transition-model-as-immutable-value design) and turns every navigation query into a range scan: a document's owned versions are the children range; all descendants are one contiguous range (T5). Navigation thus falls out of an ordered registry rather than needing a separate maintained index — "do one thing well." Durability follows the familiar append-only pattern: the in-memory map is a materialized view of an **append-only journal recovered by replay** (a `links.jsonl`/`paths.json`-style shape; udanax-green's granfilade likewise never shrinks). Add periodic snapshots to bound replay.

One regime split to accept: **owned-version discovery is an address range scan (cheap); cross-owner-version discovery is impossible by address** (severance) and must go through the provenance/content index. Build both paths, or explicitly give up enumerating cross-owner versions by address.

### Arrangement snapshot

The interesting choice, and the spec licenses the cheapest:

- **A — copy the source's block decomposition verbatim.** Exact structural mirror; simple.
- **B — re-derive the denotation and re-block.** udanax-green does this: it does not copy the source's tree nodes but resolves the source's V-span to I-spans and inserts them into a fresh POOM, where adjacent same-origin runs may coalesce. Because V2 is function-level and representation-invariant (M3), this is conformant and naturally *cleans* fragmentation from the source's edit history. Cost O(spans).
- **C — share the immutable arrangement sub-structure (copy-on-write).** [recommended for `im`] Since the version's initial content arrangement *equals* the source's content-subspace arrangement, and arrangements are persistent immutable maps, install the version's arrangement as the very same sub-structure by reference at fork time — O(1)/O(log n) — and let later edits on either side copy-on-write. This gives snapshot semantics (the shared node is frozen) and independence (divergence allocates only on write) for free. It is the persistent-data-structure analog of transclusion.

Pick **C** as default; offer **B** when the source is heavily fragmented and the version is read-heavy. To make C clean, **structure the arrangement as per-subspace maps** so the snapshot is "share the content sub-map, start an empty link sub-map" — which also enforces the V2/V2b boundary structurally.

Heed Green deviation 2: the extraction must honor the subspace boundary. udanax-green's `doretrievedocvspanfoo` is self-described as "a kluge not yet kluged" — it returns the source's *total* V-extent, so a links-only source is mis-transcribed as content. Build the real content-subspace filter; don't ship the kluge.

### Provenance recording

Provenance is a relation `address → document`; the fork appends `{(a, v)}`. Realize it as an **append-only index, one entry per contiguous shared span**, keyed by document — exactly udanax-green's spanfilade DOCISPAN family, which is append-only and whose version entries *coexist with* the source's for the same I-addresses (never replace, never reference). Append-only is the right shape because provenance never shrinks (P2): no deletion path is needed. Deduplicate to the address set so a shared address used at two V-positions yields one row (`|R'∖R| = |A|`, not `n`). Index R **by address too** (the reverse direction) — that symmetric lookup is what later makes *version correspondence* and *cross-owner version discovery* (V9w, V7's downward limit) computable, though the fork itself only writes rows. It is *not* what carries links through: per V10, carry-through to a version is computed from `ran(M(v))=A` against the unchanged link store via LP12 — R never enters, zero per-link work.

### Ownership resolution

Ownership is positional — the effective owner is the most-specific principal whose prefix covers the address. There is **no ownership ledger**; resolve by **longest-prefix match** against the principal set (the same mechanism as a routing table; a trie or ordered prefix map). The owned-vs-cross-owner branch and the version's owner both come from this one query, and nothing is written for ownership on fork (V8 inheritance is structural).

Heed Green deviation 4, which is a **security boundary, not a nicety**: udanax-green left the principal structure cooperative — the account validator is a stub returning TRUE, the account handler installs the client-supplied tumbler unconditionally, and one FEBE path even seats a cross-owner fork inside the *foreign* document's namespace, breaking the confinement the severance theorem assumes — correct cross-owner placement honors P-tier (the account-tier branch), seating the fork in the *forker's own account* namespace, which is exactly what that path violates. A conforming build must make `Π` real: a principal registry, coverage of the identity space, and allocation **confined to the allocator's own domain**, enforced server-side. Treat the front-end's claimed account as untrusted input.

### Atomicity of the composite, and the source read

- **A — single-threaded run-to-completion.** udanax-green's event loop dispatches one request at a time, so allocate→retrieve→populate all run in one invocation before any other request is dispatched; the interior state (orgl allocated, POOM empty) exists only inside the call. Atomicity is architectural and free — the simplest thing for a single-node engine, and it matches the target's single in-memory binary.
- **B — journal the whole fork as one transaction / publish a new immutable state value.** Needed the moment you process forks concurrently. With persistent structures the "commit" is just publishing the new state value; an aborted fork never publishes and the old value is untouched — which **structurally closes the orphan gap** udanax-green leaves (a failure between allocation and population there returns early and leaves an empty document in the granfilade). Recovery replays committed composites only and discards a torn one.

Pick **A** for the engine's concurrency model *and* run **B's journal underneath for durability regardless** — you need the journal for crash recovery anyway, so making the fork one journal transaction costs little and removes the orphan case. The **source read is trivial and needs no authority**: udanax-green reads the source with no permission check of any kind and writes nothing back (no forward pointer, no child list, no flag); just don't write to the source. Authority is required only to *place* the version in the forker's own domain, not to read the source.

One Lampson note on the snapshot-vs-tracking tension (V11): the stored fact is the snapshot; "what has this passage become in the source?" is realizable as a **read-time query** against the evolving source via shared identity — a recomputable hint, *not* a stored propagation channel into the version. Do not build a propagation mechanism; both of Nelson's window modes coexist with arrangement isolation precisely because tracking is a query.

## Guarantees to uphold

**Hold by construction:**
- **Permanence / no-renumber** — if the registry is append-only and identities are keys (never stored values), nothing in the vocabulary can remove or rewrite one. Don't build a deletion path for identities.
- **Global uniqueness** — from the allocator discipline (same-namespace monotone increment + prefix-disjoint namespaces). *Across* distinct namespaces this needs no coordination; but two concurrent forks of *one* source compute the same frontier `c_{hwm+1}` and collide unless the allocation step is serialized — the abstract model assumes this (SequentialTransitionAxiom), and udanax-green supplies it by single-threading. So uniqueness holds by construction *given* serialized allocation; the serialization itself is the concurrency-policy decision below, not a free guarantee.
- **Gap-free ordering / rank stability** — monotone frontier over an append-only registry; ranks are allocation order and never reused.
- **Content immutability and sharing** — append-only, origin-addressed store with no address reuse.
- **Snapshot independence** — free under copy-on-write persistent structures.
- **Ancestry readability (owned)** — from the address format (truncation).
- **Ownership inheritance** — positional, provided resolution is a pure function of address + principal set.

**Require active enforcement:**
- **Source non-destruction (frame)** — a discipline on the write path: write nothing to the source (or, with persistent state, produce a new value that shares the source's old arrangement node unchanged).
- **Provenance completeness** — record exactly `{(a, v) : a ∈ A}`, pinned from below (J1★) and capped from above (J1'★).
- **Composite atomicity** — serialization or transactional commit; reject torn forks on replay.
- **Unbounded depth** — a format-level obligation: variable-length identities, never a fixed mantissa (Green deviation 1 is the cautionary case — `NPLACES=16` caps depth and was already once bumped from 11 in practice).
- **Principal confinement** — enforce coverage and domain confinement server-side; do not trust the client's claimed account.

## How it fits

- **Leans on** the content store (immutable, origin-addressed, append-only — ASN-0047/P0) for the shared addresses; never allocates into it. *Caution:* this store is **origin-addressed, not content-addressed** — value-hashing/dedup (git-blob style) would merge separately-authored equal content and destroy attribution; the fork's sharing is reference-sharing of existing addresses, orthogonal to value dedup.
- **Leans on** the arrangement model (subspaces, order/width preservation — ASN-0058) for the snapshot and the subspace boundary.
- **Leans on** the baptism/allocation discipline (sibling streams, frontier — ASN-0040), global uniqueness (ASN-0034), and origin-based identity (ASN-0036).
- **Leans on** the ownership/prefix model (ASN-0042) for positional ownership, the owned/cross-owner branch, and the severance theorem.
- **Leans on** the transition-model foundation (ASN-0047) for the composite vocabulary, the provenance couplings J1★/J1'★, and composite boundaries.
- **Hands to** link operations (the link store, projection LP12): the fork supplies the shared anchors that make carry-through total, but does *zero per-link work* — carry-through is a consequence of the shared addresses, not a migration.
- **Hands to** (downstream, out of scope): version comparison (computes correspondence from shared content/provenance), the editing operations (diverge the arrangements), content delivery, and royalty apportionment (consumes the provenance partition by origin).

## Decisions for the builder

Genuinely open implementation choices (distinct from the note's spec-level open questions):

- **Derive the frontier vs. cache a high-water hint.** Derive by default; cache only under allocation pressure, and only as a recoverable hint.
- **VD enforcement (version-namespace discipline):** enforce that nothing but forks allocates into a version namespace — so the address decodes correctly as *derivation* and the final component as *fork* rank — or accept that the final component is *allocation* order, not necessarily fork order, and recover derivation by other means (OQ1).
- **Snapshot representation:** verbatim copy, re-derive-and-reblock, or persistent structural sharing with copy-on-write. On a persistent-immutable (`im`-style) target, structural sharing wins; structure arrangements as per-subspace maps to make it clean.
- **Atomicity mechanism:** single-threaded run-to-completion, journaled transaction, or publish-new-immutable-state — and the concurrency policy for concurrent forks of one source (single-thread, per-namespace lock, or optimistic retry on the frontier).
- **Provenance index form and granularity:** per-span append-only index (spanfilade-style) plus an address→documents reverse index for downstream queries.
- **Principal/ownership store and enforcement posture:** the note's evidence shows udanax-green left it cooperative; a conforming build must enforce. **Pick enforced** — this is a security decision.
- **Crash-recovery rule for partial composites:** define the commit boundary so a torn fork is rejected on replay; decide whether to GC orphaned identities or rely on never-publishing partial state (persistent state makes the latter free).
- **Derivation orientation across owner boundaries:** symmetric provenance is the honest state-level limit. If you need orientation, persist a `derives` event log *outside* the state — extra state for a capability the substrate deliberately doesn't carry.
- **Variable-length identity encoding:** choose a tumbler representation with no fixed depth ceiling.
