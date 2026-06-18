# M4 — Content Store (Istream) — Detailed Design

## Purpose & boundary

M4 is the **write-once `address → value` map** — Nelson's permascroll, the immutable half of the two-layer state. It does exactly one thing: given a pre-minted, T4-valid element address, it records a value there permanently, and thereafter answers *membership* (`a ∈ dom(C)?`) and *value-at* (`C(a)`). The store only grows; nothing it holds is ever mutated, deleted, garbage-collected, or refcount-reclaimed. It is *value-oblivious* (ASN-0036 S4): it never inspects, types, compares, or hashes a value for identity.

It deliberately does **not**: mint or sequence addresses (that is M3's frontier allocator — M4 calls no allocator); orchestrate placement, enforce referential integrity, or own the arrangement (that is M5 — M4 is only the *target* and the *oracle* of S3); store link values (those live in M7's `L` — M4 is *never read for bytes by the link layer*); compute origin/attribution (a pure projection in M1, surfaced as the SHOWORIGIN *operation* in M6); or maintain any reverse/sharing index (the I→V inverse lives in M5, link discovery in M8). It depends only on **M1** (address types/projections) and **M2** (journal, atomicity, snapshots, recovery).

## Public interface

M4 owns one slice of the engine `World` (M2's `WorldState`), one arm of the engine's central `Record` enum, and one fold arm. Indices are 1-based (M1 convention).

```rust
// ---- Owned types (contributed to the engine's WorldState / Record) ----

/// One immutable content atom. Value-oblivious by contract (ASN-0036 S4): M4 never
/// inspects, compares, types, or hashes a `Val` for identity. Deliberately NOT `Hash`/`Eq`
/// for identity use. Inline shared bytes shown; representation is the builder's (§Open 1).
#[derive(Clone, Serialize, Deserialize)]
pub struct Val(Arc<[u8]>);          // cheap clone; granularity (codepoint/byte/token) fixed by M5

/// M4's slice of `World`. Authoritative folded state: dom(C)=map.keys(), C(a)=map[a].
/// Checkpointed by M2, replay-rebuilt by M2. Keyed by flat `Tumbler` (M2's storage key).
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct ContentStore { map: im::HashMap<Tumbler, Val> }

/// M4's arm of the engine's central Record enum (M2's W::Record). The K.α value-write
/// half — the ONLY authoritative delta M4 owns:
///     Record::ContentWrite { addr: Tumbler, val: Val }

pub enum ContentError {
    AlreadyStored,      // addr ∈ dom(C): would overwrite — violates S0/C0. The spine guard.
    NotContentAddress,  // ¬(level==Element ∧ #E≥2 ∧ subspace==s_C): C1/C1b/L0 shape gate.
}
```

```rust
impl ContentStore {
    pub fn empty() -> ContentStore;                          // genesis seed: dom(C)=∅
    pub fn len(&self) -> usize;                              // |dom(C)|

    // --- Reads (run off a Snapshot<World>: `snap.world().content.…`) ---
    /// Membership in dom(C). The S3 referential-integrity oracle (ASN-0036 S3). O(1).
    pub fn contains(&self, addr: &Tumbler) -> bool;
    /// C(addr). None ⇔ addr ∉ dom(C). RETRIEVEV (M6), predicate-def read-back (M9). O(1).
    pub fn value_at(&self, addr: &Tumbler) -> Option<&Val>;

    // --- Write, pure step (M2 contract 3): folded into M5's placement composite ---
    /// Pure precondition gate + record production; COMMITS NOTHING. `self` is the working
    /// content slice (`&stg.working().content`). Upholds C0 (write-once) and the content
    /// shape gate (C1/C1b/L0). Returns the record to `stg.push`, or a typed reject.
    pub fn stage_write(&self, addr: &Address, val: Val) -> Result<Record, ContentError>;

    // --- Write, standalone wrapper (M2 contract 3): tests/genesis/tools, NOT hot path ---
    /// transact keyed by (document_of(addr), s_C); stages one write; commits.
    pub fn store(kernel: &Kernel<World>, addr: &Address, val: Val)
        -> Result<(Address, Seq), TxnError<ContentError>>;

    // --- Fold arm (called ONLY by World::apply; trusts committed/replayed records) ---
    pub fn apply_write(&self, addr: &Tumbler, val: &Val) -> ContentStore;
}
```

That is the entire surface. `contains` → M5; `value_at` → M6/M9; `stage_write` → M5's composite; `store` → tests/genesis. Nothing is exposed to M7/M8.

## Core data model

**Authoritative truth is the journal, not the map.** The sequence of `Record::ContentWrite` entries in M2's journal *is* the permascroll — append-only, M2-owned, durable. M4's `ContentStore.map` is the **folded materialization** of those records: M2 checkpoints it (to bound replay) and rebuilds it by replay on `open`. It is therefore "a recomputable hint over an append-only journal" in ASN-0036's sense, *and* "authoritative folded state" in M2's checkpoint sense — these are not in tension (see Conflicts). It is **not** a `rebuild_derived` hint: it is the primary fold of M4's *own* authoritative deltas, not something derived from other folded state, so M4 lets M2 checkpoint it normally and does **not** override `rebuild_derived`.

**Structure: `im::HashMap<Tumbler, Val>`.** The invariant it makes free is O(1) membership — the hot S3 oracle (`contains`) that M5 hits on every content-subspace arrangement write — and O(1) `value_at`. The common-case cost is a single hash probe. **No M4 consumer needs key order**: the only ordered/predecessor query in the corpus ("max same-origin address under a subspace") belongs to the *allocator*, which lives in M3 with its own frontier — never in M4 (no M3→M4 edge; see Seams). So `HashMap` beats `OrdMap` here; `im`'s structural sharing makes each post-commit `World` a cheap immutable value and each checkpoint share structure with its predecessor.

**Keys are flat `Tumbler`** (M2's storage-key convention); writes arrive as validated `Address` (so M4 can shape-check and project), and store `addr.tumbler().clone()`. A `Val` is **one content atom**; the atom convention (codepoint/byte/token) is fixed by M5, which splits content into `m` `ContentWrite` writes. A multi-atom object (a text run, a predicate-def body) is `m` consecutive addresses → `m` records → `m` map entries, kept *flat* here; M5's arrangement and the provenance relation R re-aggregate them into runs. M4 never re-aggregates and never groups.

**Distinguish authoritative from recomputable:** `map` keys+values = authoritative content (folded journal). M4 holds **no** derived hint of its own — no secondary index, no reverse index, no refcount, no value-hash table (unless a builder adds an *internal* dedup layer strictly beneath identity, §Open 3).

## Internal design

#### Content write — `stage_write` (gate) + `apply_write` (fold)

Production writes are a **pure step inside M5's placement composite**. M5 runs one `transact([key(d, s_C)], f)` staging `m × K.α + K.μ⁺ + K.ρ`; for each content atom `i`, M5 mints `addr_i` via M3's pure allocator (reading `stg.working()`), then calls `stg.working().content.stage_write(&addr_i, val_i)?` and `stg.push(rec)`. `stage_write`:

1. **Shape gate** (defends C1/C1b/L0): require `addr.level() == Element` (zeros=3, S7b/C1), `addr.element_field().len() ≥ 2` (#E≥2, C1b), `addr.subspace() == Some(s_C)` (=1, L0). Else `NotContentAddress`.
2. **Freshness gate** (defends S0/C0, the spine): require `!self.contains(addr.tumbler())`. Else `AlreadyStored`.
3. Return `Record::ContentWrite { addr: addr.tumbler().clone(), val }`.

Because it reads `stg.working()` (which reflects records already pushed in this composite), the freshness gate catches intra-composite collisions too. If any gate rejects, M5's closure returns `Err` → `TxnError::Rejected` → the *entire* composite aborts atomically (nothing commits) — so a content write and its placement never split.

`apply_write` is the fold M2 invokes via `World::apply`: `ContentStore { map: self.map.update(addr.clone(), val.clone()) }`. It runs on both live commit and replay, against **committed** (trusted) records, so it inserts unconditionally — the gates already ran pre-commit. In dev builds add `debug_assert!(!self.map.contains_key(addr))` to catch a corrupt journal; production trusts the record.

**Common-case path:** one hash insert with path-copy structural sharing — O(log₃₂ n) amortized, effectively O(1). **Tradeoff:** the two gates cost one shape-check + one probe; cheap insurance that makes a misrouted or double-minted write the *rare-but-correct* case rather than a silent S0 violation.

**Concurrency is M2's, not M4's.** M4 holds no locks. M2 serializes writers (M5's `(d, s_C)` key); reads run lock-free off pinned snapshots. Write-once means there is no *logical* write-write conflict — each address is written exactly once — and the per-document partition lets distinct documents proceed in parallel; M4 inherits all of this and adds nothing.

#### Membership & value-at

`contains` / `value_at` are O(1) probes on the snapshot's `content` slice. `contains` is the S3 oracle M5 calls (against `working()` mid-composite, or a snapshot standalone) to verify a target exists before an arrangement write — including the COPY/transclusion case where M5 arranges an *existing* address without any new write. `value_at` serves M6's RETRIEVEV (after M5 resolves V→I) and M9's predicate-def read-back. Both return `None`/`false` for any absent or malformed key — a definitive "not stored," never a rebuild trigger, because the map is complete after replay.

#### No-mutate / no-delete / no-GC

Enforced **by omission**: M4 exposes no update, delete, compaction, relocation, or GC operation, and keeps no refcount. `dom(C)` only grows; unreferenced ("orphaned") content is never reclaimed (S0 frame — persistence is unconditional, not refcount-gated). The optional "is `a` still referenced anywhere?" query is *not* M4's — reachability is over M5's arrangements and M8's links; if ever built it is a hint and never gates M4's permanence.

#### Origin-identity discipline (no value-dedup as identity)

M4 keys solely on the minted `Tumbler`. Two identical values at two addresses are two map entries — `S4` by construction. M4 never derives a value-hash key and `Val` is not used for identity comparison anywhere. A builder may add an *internal* `value-hash → blob` dedup/compression layer **beneath** the `address → value` map (many addresses → one stored blob), but it must never surface as identity (§Open 3).

#### Recovery

M4 carries **no recovery code**. Its slice is `Serialize`; `apply_write` is the deterministic fold. M2's `open` loads the latest checkpoint (content map up to `S_load`) and replays `ContentWrite` records `(S_load, W]` through `apply_write`; an un-acked torn tail (> W) is discarded — safe, since commit-before-ack means no consumer ever observed it. Checkpoint cadence is M2's `KernelCfg`, not M4's.

## Invariants & contracts

**By construction** (falls out of the data model / API shape):

- **S1 / C0-monotone** — `dom(C)` non-decreasing (ASN-0036 S1; ASN-0093 C0): no delete/GC API exists.
- **S0(a) domain persistence** — once present, an address stays (ASN-0036 S0(a); ASN-0093 C0): no removal path.
- **S4 origin-based identity** — distinct allocations → distinct entries (ASN-0036 S4): keyed on address, never value-deduped as identity. (Address distinctness itself is M3's GlobalUniqueness, relied on.)
- **S5 unbounded sharing** — no cap (ASN-0036 S5): M4 keeps no refcount; multiplicity lives entirely in M5's arrangements. No fixed-width counter exists to overflow.
- **S7 structural attribution** — origin computed, not stored (ASN-0036 S7): M4 stores no author/source metadata; `document_of` (M1) recovers it.
- **K.α frame** — content write touches neither `L` nor `M` (ASN-0093 K.α frame): `apply_write` mutates only the `content` slice.

**By active enforcement** (M4 must guard; where):

- **S0(b) value preservation / write-once** — `stage_write` freshness gate (`!contains`) → `AlreadyStored` (ASN-0036 S0(b); ASN-0093 C0). The last-line guard for the spine: even if M3's frontier and M4's `dom(C)` diverged, M4 refuses to overwrite at the point of truth.
- **C1 / C1b / L0 content shape** — `stage_write` shape gate → `NotContentAddress` (ASN-0093 C1, C1b, L0). Defensive: by construction M3 mints and M5 routes correctly, but M4 owns `dom(C)` so it gates at the seam.

**Relied upon, enforced upstream** (NOT M4's to establish):

- **S3 referential integrity** (ASN-0036 S3) — M4 is the *target* and supplies the *oracle* (`contains`); M5 performs the check. Because M5 co-commits content+placement atomically and pushes the `ContentWrite` before the arrangement reference within one closure, S3 holds at *every committed snapshot* — M2's atomic composite resolves ASN-0036's open "S3 timing" question in favor of "every observable state," for free.
- **S4 freshness / global uniqueness** (ASN-0036 S4) — M3 mints fresh; M4's gate is the backstop.
- **C2 content-scoped allocation** (`origin ∈ dom(M)`, ASN-0093 C2) — ensured by M5 (registered-document precondition, M5→M3) before M4's write; M4 cannot check it (no registry edge).

## Dependencies & seams

**Upstream — M1 (call as given):** `Address::level` / `element_field` / `subspace` / `tumbler` for the shape gate and to derive the flat key; `document_of` to key the standalone `store`; the `Tumbler`/`Address` types throughout. M4 uses **no** `inc` (no allocation), **no** span/span-set algebra.

**Upstream — M2 (call as given):** M4 implements its slice's `apply_write` (invoked by `World::apply`); contributes the `ContentWrite` variant; reads via `snapshot().world().content`; the standalone `store` wraps `transact`. M4 owns no `Kernel` — there is one engine `Kernel<World>`. M4 publishes both composable forms (M2 contract 3): pure `stage_write(&ContentStore,…) -> Record` and standalone `store`.

**Relationship to M3 (no edge — important).** M4 is **not** M3's frontier source. M3 maintains its own per-(home, s_C) content frontier and emits its own allocation record; M4's `ContentWrite` carries only the value. The two co-advance inside *one* M5 composite, so `dom(C)` and M3's minted-set never diverge across a commit — except by design for **ghost elements** (addresses M3 mints with no value), where M3's set strictly contains `dom(C)`. This is exactly why M3 must *not* recompute its frontier from `dom(C)`: a minted ghost is absent here, and M5's S3 check (`contains`) correctly refuses to reference it.

**Downstream seams (build neighbors against these):**

- **→ M5:** `fn stage_write(&self, &Address, Val) -> Result<Record, ContentError>` — the K.α step M5 folds `m` times into its placement composite (M5 supplies the M3-minted address + the value). `fn contains(&self, &Tumbler) -> bool` — the S3 oracle M5 calls before/at every content-subspace arrangement write. The J0/J1★ couplings are M5's composite-boundary obligation; M4's `ContentWrite` is J0's content-allocation half but M4 does not enforce the coupling (it cannot see placements).
- **→ M6:** `fn value_at(&self, &Tumbler) -> Option<&Val>` — RETRIEVEV fetches bytes after M5 resolves V→I. (SHOWORIGIN/SHOWDELETIONS/COMPARE/FINDDOCSCONTAINING read M1/M5/R, not M4.)
- **→ M9:** `value_at` — predicate-def read-back by the def's content start-address.
- **→ M7/M8:** nothing. The link layer never reads M4 for bytes.

## Conflicts resolved

1. **ASN-0093's cursor reads `dom(C)`, but the DAG forbids M3→M4.** ASN-0093 derives the next address from `max{a' ∈ dom(C) : origin(a')=d}`, implying the allocator scans the content store — which would require an *ordered* map + predecessor query *in M4* and an M3→M4 edge. **Resolution:** the cursor and its frontier live entirely in **M3**, reading M3's own state, never M4's map. Consequently M4 needs no ordered map (no consumer of M4 needs key order) and uses `HashMap`. This is a deliberate relocation forced by the module split (ASN-0093 assumed C/L/M in one module); the "recompute-from-store" alternative is out of scope for M4 and would change M3.

2. **"Index as hint" (ASN-0036) vs "checkpointed folded state" (M2).** ASN-0036 calls the in-memory map a hint over the journal; M2 checkpoints the `WorldState` slice. **Resolution:** both hold. The `ContentWrite` records are the authoritative truth; the `ContentStore.map` is their fold, which M2 checkpoints (to bound replay) and replay-rebuilds — recomputable-from-journal *and* materialized. It is **not** a `rebuild_derived` skip-serialized hint (it is the primary fold of M4's own deltas, not derived from other folded state), so M4 checkpoints it normally. (The decomposition's "replay-recovered index (a hint)" names exactly this.)

3. **ASN-0036 puts "link objects" in the content store; ASN-0093/decomposition separate `C` and `L`.** **Resolution:** M4 stores **content only**; link values live in M7's `L`. M4 is "never read for bytes by the link layer." ASN-0036's single-store phrasing reflects its pre-split framing.

4. **Split of K.α.** ASN-0093's K.α fuses mint + value-write + scoping under one substrate. **Resolution:** M4 implements only the value-write effect `C' = C ∪ {a ↦ v}` over a pre-minted address; minting → M3, scoping (`origin ∈ dom(M)`) → M5/M3, freshness-vs-content → M4 (the defensive backstop above).

## Open build decisions

1. **Inline vs out-of-line `Val`.** Default **inline** (`Address → Val`, values in the checkpoint; in-memory `value_at`). For large content, store `Address → Handle` with values in a blob store / journal-by-offset — smaller checkpoints, but `value_at` may touch disk, and the handle-map then *does* become a `rebuild_derived` hint (skip-serialized, rebuilt by journal scan). Pick by content size and `value_at` hotness.
2. **`HashMap` vs `OrdMap`.** Default **`HashMap`** (O(1), no consumer needs order). Choose `OrdMap` (O(log n)) only to gain prefix-range scans for an out-of-band "dump all content under document `d`" export/debug path — never required by the live contract.
3. **Internal value-dedup/compression.** Optional CAS layer (`value-hash → blob`) *beneath* the identity map for highly repetitive content. Default **none**; add only under measured duplication, and never let it surface as identity (S4).
4. **Shape-gate strictness.** Default **defensive** (`stage_write` checks C1/C1b/L0). May be relaxed to trust-the-path (M3 mints, M5 routes) if the seam is fully trusted — mirroring ASN-0036's subspace-alignment enforcement choice. The **freshness gate is not optional**: it guards S0.
