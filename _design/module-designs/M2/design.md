# M2 — Transaction, Journal & Concurrency Kernel — Detailed Design

## Purpose & boundary

M2 is the engine's **generic transactional substrate**: it turns every state change into one atomic, totally-ordered, durable, recoverable step (or a composite committed as one), serves consistent snapshots of committed state, and serializes same-key writers — *knowing nothing about what any change means*. It is a WAL + atomic-install + keyed-serialization + snapshot engine that the stores plug into, dependency-inverted: M2 defines the fold (`WorldState::apply`), the engine implements it, and M2 only calls down through that trait. **One thing well: make the spec's single sequential, atomic-step order real and durable for a plural, concurrent world — over an opaque payload and opaque keys.**

It does **not**: compute addresses, frontiers, or coverage-classes (M1/M3/M7 supply keys and do the math — M2 has no address algebra); enforce store permanence P0–P3 or the J-couplings (the stores enforce those at their composite boundaries *through* M2, never by it — see ASN-0047); interpret record semantics; own the request lifecycle, the parse/dispatch table, or the acknowledgment-to-client (M10 — M2 keeps only the commit-gate *mechanism*); own derived hints (the stores do; M2 journals only authoritative deltas); or provide atomicity for *multi-transaction batches* such as `retract_stale` or a rule firing (deliberately partial-visible per ASN-0134 A5 — "above the substrate").

## Public interface

The kernel is `Kernel<W>` for an engine-supplied `W: WorldState`. Keys are opaque bytes; payloads are the engine's `Record` enum (`W::Record`). All write paths return only after their commit is durable (commit-before-acknowledge).

```rust
// ---- The engine's contract to M2 (dependency-inverted) ----
pub trait WorldState: Clone + Serialize + DeserializeOwned + Send + Sync + 'static {
    type Record: Serialize + DeserializeOwned + Clone + Send + Sync + 'static;
    /// The ONE deterministic, total, side-effect-free fold step — drives both live
    /// commit and replay. A record that committed once must re-apply cleanly forever.
    fn apply(&self, record: &Self::Record) -> Self;
    /// Reconstruct derived hints from authoritative state. Called once after a
    /// checkpoint/genesis load and BEFORE replay. Default identity (hints folded
    /// by `apply` & serialized in the checkpoint); override iff hints are skip-serialized.
    fn rebuild_derived(self) -> Self { self }
}

/// Opaque serialization key. M2 only Eq/Hash/Ord-s the bytes (Ord is bytewise, for
/// deadlock-free acquisition — NOT tumbler order). Callers prefix a 1-byte space tag
/// so distinct key spaces (e.g. (home,subspace) vs coverage-class) never collide.
pub struct LockKey(pub Vec<u8>);

pub struct Seq(pub u64);      // linearization coordinate (ASN-0134 idx(σ)); monotone, gap-free
```

**Lifecycle**

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover (latest checkpoint → rebuild_derived → replay committed records) or
    /// init from `genesis` (= Σ₀, supplied by the engine).
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint @seq and truncate the journal before it. Non-blocking
    /// to writers. Cadence is the caller's policy. Returns the checkpointed seq.
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Drain pending (group-commit) durability barriers; used at shutdown/checkpoint.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

**Reads (snapshots)** — discharge MIC clauses 4 & 6.

```rust
impl<W: WorldState> Kernel<W> {
    /// One committed state, pinned. Read EVERY constituent of a multi-read verdict
    /// off ONE Snapshot — that discharges clause 6 by construction.
    pub fn snapshot(&self) -> Snapshot<W>;
    pub fn current_seq(&self) -> Seq;
}
impl<W: WorldState> Snapshot<W> {
    pub fn seq(&self) -> Seq;     // the committed index this view is OF (V1 retrospective)
    pub fn world(&self) -> &W;    // read your store's slice off this
}
```

**Writes (transactions / composites)** — discharge clauses 1, 2, 3, 5, 7.

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` for the txn's duration, run `f` against a consistent state, and —
    /// iff `f` returns Ok with ≥1 staged record — commit them atomically & durably
    /// under one commit marker before returning (A7). `f` returning Err → clean
    /// typed rejection, nothing committed, no dangling state. `f` returning Ok with
    /// zero records → zero-step op (A1: read-only / idem-hit / nullify-hit), no commit.
    pub fn transact<T, E>(
        &self,
        keys: &[LockKey],
        f: impl FnOnce(&mut Staging<W>) -> Result<T, E>,
    ) -> Result<T, TxnError<E>>;
}

pub struct Staging<W: WorldState> { /* base, working, records */ }
impl<W: WorldState> Staging<W> {
    pub fn base(&self) -> &W;            // Σ — the read snapshot at txn start
    pub fn working(&self) -> &W;         // Σᵢ — base folded with records so far (intra-composite checks)
    pub fn push(&mut self, r: W::Record); // fold into working, append to the txn's records
}

pub enum TxnError<E> {
    Rejected(E),            // f's typed precondition failure — surfaced verbatim to M10
    Durability(io::Error),  // the durability barrier failed → NOT committed; treat as no-op
    Conflict,               // optimistic-CAS impl only; caller re-invokes. Never under single-applier/merge-install.
}
```

**Serialization (held-across-commits variant)** — the explicit clause-5/7 path when a run must be *separately* committed rather than one transaction (rarely needed; `transact`'s `keys` covers the atomic case).

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` until the guard drops. Issue inner `transact(&[], f)` calls (the
    /// section already serializes). Readers may land between the inner commits (clause 5,
    /// reader-visible mid-run). Prefer one `transact([keys], f)` staging the whole run.
    pub fn critical_section(&self, keys: &[LockKey]) -> CriticalGuard<'_>;
}
```

## Core data model

The **only durable, authoritative state M2 owns is the journal.** Everything in memory is a recoverable fold of it (Lampson: the log is the truth; in-memory structures are hints). Within the recovered `World`, the *store-level* distinction between authoritative slices (C, L, E, M, R) and derived hints (spanfilade, reverse indexes) belongs to M4/M5/M7 — to M2 the whole `World` is one fold.

| Structure | Shape | Authority | Why this shape |
|---|---|---|---|
| **Journal** | append-only file(s) of CRC-framed records + per-txn commit markers | **authoritative, durable** | record-of-record; replay reconstructs everything; append-only makes immutability of committed steps free (ASN-0047 P0/P1/P2 at the log level) |
| **Root** | `arc_swap::ArcSwap<Committed<W>>`, `Committed { seq: Seq, world: W }` | recoverable materialization | lock-free reads; **atomic install = atomic, indivisible step (A0/A4)**; persistent `W` (im) ⇒ snapshot & install are O(1) and snapshots never tear |
| **Checkpoint** | serialized `W` @ `Seq` on disk (temp→fsync→rename) | recoverable cache (a prefix-fold) | bounds replay time; optional; safe to delete |
| **Lock table** | striped `Vec<parking_lot::Mutex<()>>` *or* `DashMap<LockKey, …>` | volatile (locks don't outlive a crash; recovery is single-threaded) | the keyed critical section (clauses 2/5/7) |
| **Sequencer** | `Seq` high-water + the install serialization point (a `Mutex` or actor mailbox) | volatile, recovered as `max committed Seq` | assigns the total order; serializes journal-append + install |

`W` is the engine's composition of all store slices, each an `im` persistent collection (`OrdMap` for address-keyed stores — gives prefix-range scans free — `HashMap`/`Vector` elsewhere). `W: Clone` is O(1) (Arc bumps); `W::apply` returns a structurally-shared successor touching only changed paths. This is the ASN-0134-recommended persistent-immutable representation: the root's identity *is* the version coordinate, making clauses 1/4/6 nearly free.

`Snapshot<W>` is `Arc<Committed<W>>` — a cheap, pinned, consistent view carrying its own `seq` (so verdicts can be reported as retrospective statements about `Σ_r`, V1).

## Internal design

### 1. The journal & WAL discipline

Frames: `[u32 len][u32 crc][payload]`. Payload is either `Record{ seq, txn, bytes }` or `Marker{ txn, last_seq, frame_checksum }`. A transaction appends its record frames in `Seq` order, then one marker. **The marker is the recovery contract** (ASN-0047): a txn is committed iff its marker is present and its `frame_checksum` validates over the txn's records; records past the last valid marker are a torn tail — discarded and truncated.

**Only authoritative deltas are journaled.** Derived hints are *never* journaled — they are reconstructed (by `apply` during replay, or by `rebuild_derived`). This is the structural answer to ASN-0134's divergence hazard (OQ10): there is nothing to diverge because one logical step is exactly one journal record driving one `apply`.

Durability is `Durability::{ Fsync, FsyncBatch{window}, None }`. `None` is the fully in-memory realization — **MIC-faithful** (ASN-0134 is silent on durability), no journal, no recovery, atomicity/isolation intact. Production uses group commit (`FsyncBatch`): the serial section assigns Seqs, appends to the journal buffer, and installs the root (fast); a batched fsync follows; `transact` returns only after *its* batch is durable. Installing visible-before-durable is safe because journal durability is **prefix-closed** — anything causally dependent on txn T is journaled after T, so "R durable ⟹ T durable," and a reader that acts on a not-yet-durable T either commits (making T durable by prefix) or has no persistent effect.

### 2. Sequencer & the linearization point

Each committed record receives the next `Seq` from a monotone counter, assigned inside the serialization point so the order has no gaps and a composite's records are **contiguous** (no foreign record interleaves a composite — a bonus that over-satisfies W2 when a run is one transaction). `Seq` assignment is the linearization point of A2; one `transact` = one operation = one linearization point (for a single-step op) or one contiguous composite boundary. M2 fixes it; M10 merely chooses to call `transact` once per operation.

### 3. The transaction / composite boundary

`transact(keys, f)` — recommended single-applier flow:

```
acquire keys (bytewise-sorted, dedup'd)        // clauses 2/5/7; no-op under global applier
lock the applier (single global serializer)
base ← root.load()                              // stable under the applier lock
stg  ← Staging::new(base)
match f(&mut stg) {                             // store logic: reads stg.base()/working(), pushes records
    Err(e)               → return Rejected(e)   // clean rejection, nothing journaled/installed
    Ok(_) if stg empty   → return Ok(_)         // zero-step (A1): read-only / idem-hit / nullify-hit
    Ok(v) ⇒
        seqs ← alloc_seqs(stg.records.len())    // linearization
        journal.append(txn, seqs, stg.records)  // record frames + commit marker → buffer+file
        durability.commit(txn)?                 // fsync / group; on err → Durability, NOT committed
        root.store(Committed{ last_seq, stg.working })   // atomic install (working == base+records)
        return Ok(v)                            // commit-before-acknowledge
}
```

`Staging.working` (= `base` folded with staged records, cheap over persistent `W`) is what lets the store check **intra-composite preconditions** at intermediate states (ASN-0047's "observable intermediate states," e.g. S3★ referential integrity after K.α but before K.μ⁺). Those intermediates are visible only to the executing closure — **never to external readers**, who see only the single atomic install. The J-couplings the closure may check at the boundary (`base`→`working`) are M5's to assert; M2 never does.

A composite (INSERT = K.α+K.μ⁺+K.ρ; Fork) is exactly one `transact` staging several records → atomic, contiguous, durable as a unit. A multi-step *batch* with intended partial visibility (`retract_stale`, a rule firing) is *several* `transact` calls the caller sequences — M2 does not bundle them (A5).

### 4. Keyed critical sections

One mechanism serves clauses 2, 5, 7; the key is always caller-supplied bytes. `transact` acquires `keys` before taking its snapshot and holds them through commit, so **read-decide-deposit is atomic for those keys** — exactly what clause 7's idem dedup needs (the dedup-read of the global active set and the deposit are one action under the coverage-class key; cf. G2) and what clause 2 needs (frontier-read-and-deposit under the (home,subspace) key — M3 does the `inc(max,·)` math; M2 only locks). Acquisition is bytewise-sorted and deduplicated → deadlock-free. `critical_section` is the rarer guard held across *separate* commits (the modeled clause-5 path where readers may land mid-run); the common run is one `transact`, which over-satisfies clause 5.

Lock table: striped (bounded memory, possible false contention) or per-key map (no false contention, needs entry GC) — an open decision. Under the single-applier impl the table is unused (the global lock subsumes every key); the API is identical, so moving to per-key concurrency changes no caller.

### 5. Snapshot reads

`snapshot()` is one lock-free `ArcSwap::load` → a pinned `Committed<W>`. Per-call single-state (clause 4 / A3 / V0) is by construction. A multi-read verdict reads all `p` constituents off **one** `Snapshot` → clause 6 / V2 for free (persistent state dissolves the "global" cost ASN-0134 flags). This is the seam contract on M6/M8/M9: thread one `Snapshot` through every constituent of a verdict; do not issue them as separate `snapshot()` calls (the §8 pathology).

### 6. Checkpoint & truncation

Non-blocking: grab a `Snapshot` (lock-free), serialize `world()` (authoritative; hints may `#[serde(skip)]`) to `checkpoint.tmp`, fsync, atomic-rename to `checkpoint.<seq>`, fsync dir, then truncate journal frames `< seq`. Writers run throughout — the snapshot's Arc keeps the checkpointed version alive while live installs advance the root. Crash mid-checkpoint leaves an ignored `.tmp` and an untruncated journal: always safe. Cadence (every-N / time / size) and representation (full-World vs per-store/incremental) are open knobs.

### 7. Recovery

`open`: load latest valid checkpoint (else `genesis`), call **`rebuild_derived`** (seeds hints from authoritative state — makes both hint strategies work), then replay post-checkpoint **committed** records via `apply` in `Seq` order. Torn tail (records past the last valid marker, or a CRC-failed frame) → discard + truncate; it was never acked, so loss is correct. CRC failure *inside a marked (acked) composite* is corruption of durable acked data → **halt and report** (`OpenError::Corruption`); never silently drop it. `apply` determinism guarantees replay reproduces the exact committed state (A6: every journal prefix up to a marker is a canonical reachable state).

### 8. Concurrency realizations — the fault line

The `transact`/`snapshot` API is invariant across these; only internal locking changes.

- **Single applier (recommended first; ASN-0047's choice).** `f` runs under the global applier lock → `base == current root`, keys are no-ops, all seven clauses free. Group commit moves fsync out of the serial section for throughput. Bounded by one core.
- **Per-key concurrent with merge-at-install (scaling path; what ASN-0134 G1 blesses).** `f` runs outside the install lock, holding only its `keys`; at commit, a short global install section re-folds `stg.records` over the *current* root and swaps. The held keys guarantee no concurrent writer touched this txn's read-set (G1 commute), so the re-fold is conflict-free — persistent state alone does **not** give this (root-install contention), the held keys do. fsync stays batched outside the install section.
- **Optimistic frontier-CAS (optional).** No held locks; read fresh, compute, CAS the root, retry on change → may surface `TxnError::Conflict`. Viable when same-key contention is rare; retry termination is open (ASN-0134 OQ1/OQ3).

## Invariants & contracts

**By construction** (falls out of the data model above):
- **Total order, unique monotone `Seq`** — counter under the serializer (ASN-0134 A1/A2, SequentialTransitionAxiom; ASN-0047 same).
- **No torn read / per-call single-state** — immutable `Committed<W>` + atomic `ArcSwap` install + lock-free load (A0/A3/A4/V0, MIC-4).
- **Multi-read verdict single-state** — one `Snapshot` threaded through all reads (V2, MIC-6; caller contract, made trivial by persistent root).
- **Composite contiguity in the order** — a composite's Seqs assigned as a unit (supports W2 when run = one txn).
- **Append-only journal; committed frames immutable; every prefix-to-a-marker is a replayable canonical state** — append-only file + per-txn marker + `apply` determinism (ASN-0047 journaling; ASN-0134 A6).

**By active enforcement** (M2 must guard, named where):
- **Same-key serialization** — keyed critical section §4 / single applier §8 (ASN-0134 H2, MIC-2; M3 builds frontier H0 atop it).
- **Commit-before-acknowledge** — `transact` returns only post-durable+install §3 (A7, MIC-3).
- **Composite atomicity (none-or-all to readers)** — single atomic install §3 + commit-marker recovery discard §7 (ASN-0047).
- **Durability before ack** — fsync/group barrier before return §1 (ASN-0047).
- **Recovery faithfulness** — replay committed records in order; discard torn tail; halt on corruption of a marked composite §7 (A6; ASN-0047).
- **Deadlock-free multi-key acquire** — bytewise-sorted, deduplicated §4.
- **idem=⊤ dedup atomicity** — read-decide-deposit under the coverage-class key = one `transact` §4 (I1a/I4/G2, MIC-7).
- **Run contiguity** — run as one `transact` (over-satisfies) or `critical_section` across deposits §4 (W2, MIC-5).

**Explicitly *not* M2's** (passes through M2, enforced by neighbors): store permanence P0–P3/L12 and the J-couplings J0/J1★ (stores' `apply`+API; M5's composite boundary — ASN-0047); frontier/address and coverage-class computation (M3, M1/M7); register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected` if unmet); the request lifecycle and ack-to-client (M10); multi-*transaction* batch atomicity (above the substrate, A5); durability *as a requirement* (not a MIC clause — `Durability::None` is faithful).

## Dependencies & seams

**Upstream: none.** M2 is a foundation (it carries no edge to M1 — keys and payloads are opaque, ordering of keys is plain bytewise, not tumbler order). Its only dependencies are crates: `im`, `arc_swap`, `serde`, `parking_lot`/`dashmap`, a CRC32C lib.

**Composition seam (dependency-inverted).** The engine crate defines `World` (composing all store slices) and `Record` (the enum union of every store's record-types), implements `WorldState` for `World` by dispatching `apply` to the owning store's logic, and instantiates `Kernel<World>`. "Stores register record-types" = contribute `Record` variants + `apply` arms; "index-rebuilders" = `World::rebuild_derived` (and/or hint maintenance inside `apply`). Hard contract: **stages only authoritative deltas; never journal a hint.**

**Downstream seams (what neighbors code against):**
- **M3 allocation** (frontier under H0): `kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.base(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })`. M3 supplies the key bytes (1-byte space tag + tumbler bytes) and does all address math; M2 only locks + commits.
- **M5 placement composite** (INSERT/COPY/VERSION): one `transact([key(d, s_C)], …)` staging K.α + K.μ⁺ + K.ρ; M5 checks S3★ on `stg.working()` and the J-couplings at the boundary; M2 commits atomically. CREATENEWDOCUMENT (M3) is one `transact` registering the entity — it does *not* materialize an arrangement (M5 keeps that lazy).
- **M7 idem=⊤ emit**: `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })`. The class_key serializes same-class emits (clause 7); the alloc key serializes same-home allocation (clause 2). Nullify hit-branch = a `transact` that stages nothing (zero-step). The spanfilade is M7's hint, maintained in `apply`/`rebuild_derived`, **not journaled**.
- **M6/M8/M9 readers & verdicts**: `let s = kernel.snapshot();` then read every constituent off `s` (clause 6). M9 reports quiescence as "as of `s.seq()`" (V1 retrospective).
- **M10**: opens/commits each operation's transaction via `transact`, acknowledges to the external client only after it returns (commit-before-ack), and surfaces `TxnError::Rejected(E)` as a typed rejection (never a silent skip).

## Conflicts resolved

**1. Composite atomicity (ASN-0047) vs "batches are not atomic" (ASN-0134 A5).** The two speak of different units. M2's atomic unit is the **transaction** (one `transact`) — externally none-or-all. ASN-0047's "observable intermediate states" of a composite are precisely `Staging.working`, visible *only to the executing closure* for intra-composite precondition checks, never to external readers. ASN-0134's "batches not atomic" refers to a sequence of *separate* operations (`retract_stale`, a rule firing) whose partial visibility is intended; M2 deliberately does **not** bundle those into one transaction. So: M2 delivers transaction (composite) atomicity; multi-transaction batch atomicity is the caller's, "above the substrate."

**2. Single global writer (ASN-0047) vs per-home serialization suffices (ASN-0134 G1).** The **contract** is the weaker one — per-key serialization (clause 2). The recommended **first implementation** is a single applier (ASN-0047), which over-satisfies it. Because `transact(keys, …)` is identical for both, the implementation can move single-applier → per-key-concurrent (merge-at-install) without touching any store. ASN-0047's single-writer is one conservative realization of ASN-0134's contract, not a competing requirement.

**Boundary clarifications (territory that *looks* like M2's but is a neighbor's, resolved by the decomposition's dependency inversion):** the frontier discipline ASN-0134 reasons about (H0) is M3's *allocator*; M2 owns only its *serialization*. The request/response path and pipelining-vs-sequential client model (G0) are re-homed to M10; M2 keeps only the commit-gate mechanism. Neither is a conflict — both are M2 honoring its seam by *not* doing the neighbor's job.

## Open build decisions

- **Concurrency mechanism** — single applier (recommended first) → per-key concurrent with merge-at-install (scaling path) → optimistic-CAS (only under measured low same-key contention; retry termination unresolved, OQ1/OQ3). Pick by throughput need; the API doesn't change.
- **Durability/visibility ordering** — install-then-batched-fsync (recommended; higher throughput; prefix-closure makes visible-before-durable safe) vs fsync-then-install (stricter: no reader ever sees pre-durable state).
- **Durability mode** — `Fsync` per commit vs `FsyncBatch{window}` (group commit) vs `None` (in-memory, MIC-faithful, for tests/embedding).
- **Checkpoint cadence & representation** — every-N-commits / time / journal-size; full-`World` serialize vs per-store/incremental; serialize hints vs `#[serde(skip)]` + `rebuild_derived` (checkpoint size vs recovery recompute). The recovery-time-vs-overhead knob ASN-0047/0134 leave open.
- **Lock-table layout** — striped `Vec<Mutex>` (bounded, false contention) vs per-key `DashMap` (no false contention, entry GC).
- **Journal framing** — CRC algorithm, segment rotation, max frame size, fsync-of-dir on rotate.
- **Whether to build `critical_section` at all** — default to issuing every run as one `transact` (atomic, over-satisfies clause 5); build the held-across-commits guard only if a run is genuinely too large to commit atomically or needs intended mid-run reader visibility.
- **Record/key encoding** — `Record` as one serde enum (recommended for a single binary, compile-time dispatch) vs a runtime type-id registry of boxed appliers; `LockKey` as `Vec<u8>` vs `SmallVec`/`Box<[u8]>` vs a fixed-width digest.
