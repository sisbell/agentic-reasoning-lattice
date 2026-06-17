# M2 — Interface (for dependents)

M2 owns the generic transactional substrate: it turns every state change into one atomic, totally-ordered, durable, recoverable step (or a composite committed as one), serves consistent snapshots of committed state, and serializes writers — over an opaque payload and opaque keys, knowing nothing about what any change means.

## Public interface

```rust
// ---- The engine's contract to M2 (dependency-inverted) ----
pub trait WorldState: Clone + Serialize + DeserializeOwned + Send + Sync + 'static {
    type Record: Serialize + DeserializeOwned + Clone + Send + Sync + 'static;
    /// The ONE deterministic, total, side-effect-free fold step — drives both live
    /// commit and replay. Folds authoritative deltas AND maintains every derived hint
    /// incrementally. Deterministic so replay reproduces committed state exactly; NOT
    /// required to be idempotent — recovery applies each committed record exactly once.
    fn apply(&self, record: &Self::Record) -> Self;
    /// Seed derived hints from authoritative state. Runs ONCE at load, BEFORE replay,
    /// and NEVER on a live commit. Default identity; override iff hints are skip-serialized.
    /// CONSISTENCY OBLIGATION: an override MUST seed exactly the hint state that folding
    /// every record with Seq ≤ S through `apply` would produce (S = loaded checkpoint's seq).
    fn rebuild_derived(self) -> Self { self }
}

/// Opaque serialization key — the documented serialization seam M3/M7 code against.
/// M2 only Eq/Hash/Ord-s the bytes (Ord is bytewise, NOT tumbler order). Callers prefix
/// a 1-byte space tag drawn from a SINGLE CENTRAL ENUM in the engine crate (never chosen
/// per-store) so distinct key spaces never collide.
pub struct LockKey(pub Vec<u8>);

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct Seq(pub u64);  // M2's per-record linearization coordinate; monotone, gap-free.
```

**Config & errors**

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (in-memory mode ignores it)
    pub durability: Durability,       // per-commit Fsync (durable-before-visible) | InMemory (MIC-faithful)
    pub checkpoint: CheckpointPolicy, // EveryN(u64) | Interval(Duration) | JournalBytes(u64) | Manual
    pub retain_checkpoints: usize,    // N ≥ 1 most-recent checkpoints kept; journal reclaimed only BELOW the oldest
}

pub enum Durability {
    Fsync { burned_seq: BurnedSeqPolicy }, // durable-before-visible; burned_seq governs durability-failure rollback
    InMemory,                              // no journal/barrier/recovery; checkpoint()/flush() are no-ops
}
pub enum BurnedSeqPolicy { Rollback, TolerateGap }  // gap-free (default) | monotone-only
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // no retained checkpoint loads and genesis is unreachable — whole fallback chain exhausted
    Corruption { at: Seq },  // CRC failure in the genuinely-replayed range (S_load, W] — durable committed data is corrupt;
                             // halt. `at` carries the corrupt run's inferred upper bound.
}
pub enum CheckpointError { Io(io::Error), Serialize, Poisoned }  // Poisoned: a prior barrier/truncation failure halted the kernel
```

**Lifecycle**

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover (load latest valid retained checkpoint @S_load, falling back to older retained
    /// checkpoint then genesis; rebuild_derived → replay committed records S_load < Seq ≤ W) or
    /// init from `genesis` (= Σ₀, S_load = 0). Records beyond W are an un-acked/torn tail, discarded.
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint embodying all records with Seq ≤ s, keep retain_checkpoints, reclaim
    /// journal segments wholly below the oldest retained checkpoint. Non-blocking to writers.
    /// Returns the checkpointed seq `s`, or Poisoned if a prior barrier failure halted the kernel.
    /// Under InMemory it is a NO-OP returning current_seq().
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Shutdown/checkpoint hook. No-op under per-commit Fsync and InMemory (returns Ok(())).
    /// Slot-in point for the deferred group-commit mode. No-op on a poisoned kernel.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

**Reads (snapshots)**

```rust
/// A pinned, consistent view of one committed state. Newtype over the loaded root Arc.
pub struct Snapshot<W: WorldState>(Arc<Committed<W>>);

impl<W: WorldState> Kernel<W> {
    /// One committed state, pinned. Read EVERY constituent of a multi-read verdict off ONE
    /// Snapshot — discharges clause 6 by construction. INFALLIBLE; serves the last in-memory
    /// root even on a POISONED kernel.
    pub fn snapshot(&self) -> Snapshot<W>;
    /// The currently installed root's seq — equal AT THE INSTANT OF CALL to a snapshot() taken
    /// then, but NOT a substitute for it across calls. Never regresses. Infallible, including poisoned.
    pub fn current_seq(&self) -> Seq;
}
impl<W: WorldState> Snapshot<W> {
    pub fn seq(&self) -> Seq;     // the committed index this view is OF (V1 retrospective)
    pub fn world(&self) -> &W;    // read your store's slice off this
}
```

**Writes (transactions / composites)**

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` for the txn's duration, run `f` against a consistent base state, and — iff
    /// `f` returns Ok with ≥1 staged record — commit them atomically & durably under one commit
    /// marker, INSTALL the root, then return (A7). Returns (T, Seq): the closure's value and the
    /// committed last_seq. `f` Err → clean typed rejection, nothing committed. `f` Ok with zero
    /// records → zero-step op (A1), no commit; returned Seq is base.seq().
    /// NON-REENTRANT: `f` MUST NOT call transact (or any kernel write path) — DEADLOCKS.
    pub fn transact<T, E>(
        &self,
        keys: &[LockKey],
        f: impl FnOnce(&mut Staging<W>) -> Result<T, E>,
    ) -> Result<(T, Seq), TxnError<E>>;
}

pub struct Staging<W: WorldState> { /* base, working, records */ }
impl<W: WorldState> Staging<W> {
    pub fn base(&self) -> &W;            // Σ — the installed root at txn start
    pub fn working(&self) -> &W;         // Σᵢ — base folded with records so far (intra-composite checks)
    pub fn push(&mut self, r: W::Record); // fold into working, append to the txn's records
}

pub enum TxnError<E> {
    Rejected(E),            // f's typed precondition failure — surfaced verbatim to M10
    Durability(io::Error),  // per-commit barrier failed BEFORE install AND the un-acked tail was durably
                            // truncated → a TRUE no-op; caller may safely re-invoke
    Poisoned,               // kernel halted by a prior UNRECOVERABLE failure; do not re-invoke
}
```

## Caller contracts & obligations

- **`open(cfg, genesis)`** — pass `genesis` = Σ₀; returns `Err(OpenError::Corruption{at})` (durable committed data corrupt — halt, operator intervention) or `Err(BadCheckpoint)` (no recovery base — operator intervention). Neither is auto-retryable.
- **`checkpoint()`** — cadence is the caller's policy; non-blocking to writers. Returns the checkpointed `Seq`, or `Err(CheckpointError::Poisoned)` if the kernel is halted. No-op under `InMemory`.
- **`flush()`** — call at shutdown; no-op under v1 durability modes; never fails in v1.
- **`snapshot()`** — infallible, always available (even poisoned). To satisfy clause 6, read **every** constituent of a multi-read verdict off **one** `Snapshot`; never re-issue separate `snapshot()` calls for constituents of one verdict.
- **`Snapshot::seq()`** — the V1 coordinate to stamp a snapshot-computed verdict with; this is the retrospective committed index the view was read from.
- **`current_seq()`** — infallible, never regresses; use only as a bare "latest committed index" progress query. **Not** a substitute for `Snapshot::seq()` — a write may land between calls, so never stamp a snapshot-computed verdict with it.
- **`transact(keys, f)`** — caller supplies `keys` (1-byte central-enum space tag + key bytes); `f` runs against a consistent base and must do all domain math itself.
  - **NON-REENTRANT**: `f` MUST NOT call `transact` or any kernel write path — the applier lock is held, a nested call **deadlocks**.
  - `f` returning `Err(e)` → `TxnError::Rejected(e)`, nothing committed, no dangling state.
  - `f` returning `Ok` with zero staged records → zero-step op, no commit; returned `Seq` is `base.seq()`.
  - `f` returning `Ok` with ≥1 record → atomic+durable commit; returns `(T, last_seq)`, the exact V1 coordinate of the write.
  - On commit, the write reports its own coordinate from the returned `last_seq` — never from a post-hoc `current_seq()`.
  - `TxnError::Durability` → a TRUE no-op; the caller may safely re-invoke.
  - `TxnError::Poisoned` → the kernel is halted; treat as a halt condition, do **not** re-invoke.
- **`Staging::working()` vs `base()`** — for frontier/allocation math use `working()` (reflects records already pushed in this closure); use `base()` only for the txn-start root. In a multi-atom run, reading `base()` per atom collides addresses and the freshness precondition rejects atom 2.

**Trait obligations on the engine implementing `WorldState`:**
- `apply` must be deterministic, total, side-effect-free, and maintain **every** derived hint incrementally (a hint not folded in `apply` is stale after every live write and after replay). Not required to be idempotent.
- If `rebuild_derived` is overridden, it MUST seed exactly the hint state that folding every record with `Seq ≤ S` through `apply` would produce — otherwise recovered hints diverge from live ones and reads go wrong. M2 cannot check this.
- Stage only authoritative deltas; **never journal a hint**.

## Seams exposed downstream

- **→ M3 allocation** (frontier under H0): `kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.working(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })?`. M3 supplies key bytes and all address math; reads `stg.working()`. When allocation is one step of a larger composite, the caller folds M3's **pure** `recompute_max`/`inc` body — never a nested `transact`.
- **→ M5 placement composite** (INSERT/COPY/VERSION): one `transact([key(d, s_C)], …)` staging m × K.α + K.μ⁺ + K.ρ, returning `(_, last_seq)`. Each content K.α mints against `stg.working()` (reuses M3's pure math). M5 checks S3★ and the J-couplings on `stg.working()`/at the boundary; M2 commits atomically. Composes neighbors' pure bodies in one closure — never a transaction-within-a-transaction.
- **→ M7 idem=⊤ emit**: `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })`. Read-decide-deposit is atomic under the global lock. Nullify hit-branch stages nothing (zero-step), returning `(Hit, base.seq())`. M7's MAKELINK seats home links by folding **M5's** pure seating body (edge M7 → M5, no return edge).
- **→ M6/M8/M9 readers & verdicts**: `let s = kernel.snapshot();` then read every constituent off `s`. M9 reports quiescence "as of `s.seq()`". M9's reactive fires do **not** call `transact` directly — single-step (`m=1`) fires go through M7's gated emit (obtaining the index from the `Seq` M7 returns); predicate-def creation rides M5's placement composite.
- **→ M10**: opens/commits each operation via `transact`, receiving `(result, last_seq)`; acknowledges to the client only after it returns (commit-before-ack); may report `last_seq`; surfaces `TxnError::Rejected(E)` as a typed rejection; treats `TxnError::Poisoned` as a halt (do not re-invoke); treats `OpenError::Corruption`/`BadCheckpoint` on startup as operator-intervention conditions.
- **→ everyone (contract 3, Pure composable step surface)**: any store primitive that appears as a step inside another store's composite MUST be exposed in two forms — its standalone `transact`-wrapped form **and** a pure function over a supplied `&W` (read off `base()`/`working()`) plus its `Record` variant(s). M3/M5 must publish the pure surface up front; M2 cannot enforce this.

## Boundary — NOT provided here

- Address, frontier, and coverage-class computation (M3, M1/M7) — M2 has no address algebra; keys/payloads are opaque, key Ord is plain bytewise (not tumbler order).
- Store permanence P0–P3/L12 and the J-couplings J0/J1★ — stores enforce these through M2, never by it.
- Record-semantic interpretation; derived hints (the stores own them — M2 journals only authoritative deltas).
- The request lifecycle, parse/dispatch table, and ack-to-client (M10) — M2 keeps only the commit-gate mechanism.
- Multi-**step** (`m ≥ 2`) batch atomicity — M2 offers only the per-`transact` atomic unit; a store issues an `m ≥ 2` batch as separate `transact`s (and may over-satisfy by committing as one). A single-step (`m = 1`) fire **is** one atomic `transact`.
- Register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected` if unmet).
- Durability *as a requirement* — the in-memory mode is MIC-faithful.
- Per-key-concurrent and optimistic-CAS write realizations, and group-commit (`FsyncBatch`) — deferred; the `transact`/`snapshot` signatures and `LockKey` seam are invariant across these realizations.
