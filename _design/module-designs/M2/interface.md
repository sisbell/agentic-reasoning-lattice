# M2 — Interface (for dependents)

M2 owns the generic transactional substrate: it turns every state change into one atomic, totally-ordered, durable, recoverable step (or a composite committed as one), serves consistent snapshots of committed state, and serializes writers — knowing nothing about what any change means.

The main type is `Kernel<W>` for an engine-supplied `W: WorldState`. Keys are opaque bytes; payloads are the engine's `Record` enum (`W::Record`). The v1 concurrency realization is the single applier; the `transact`/`snapshot` signatures and the `LockKey` seam are invariant across concurrency/durability realizations.

## Public interface

```rust
// ---- The engine's contract to M2 (dependency-inverted): the engine implements this ----
pub trait WorldState: Clone + Serialize + DeserializeOwned + Send + Sync + 'static {
    type Record: Serialize + DeserializeOwned + Clone + Send + Sync + 'static;
    /// The ONE deterministic, total, side-effect-free fold step — drives both live commit and
    /// replay; folds authoritative deltas AND maintains every derived hint incrementally;
    /// NOT required to be idempotent (recovery applies each committed record exactly once).
    fn apply(&self, record: &Self::Record) -> Self;
    /// Seed derived hints from authoritative state. Runs ONCE at load, BEFORE replay, NEVER on a
    /// live commit. Default identity; override iff hints are `#[serde(skip)]`. An override MUST
    /// seed exactly the `apply`-fold of every record with Seq ≤ S (S = loaded checkpoint's seq).
    fn rebuild_derived(self) -> Self { self }
}
```

```rust
/// Opaque serialization key — the documented serialization seam M3/M7 code against. M2 only
/// Eq/Hash/Ord-s the bytes (Ord is bytewise, NOT tumbler order). Callers prefix a 1-byte space
/// tag (from M2's central enum) so distinct key spaces never collide.
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct LockKey(pub Vec<u8>);

/// M2's per-record linearization coordinate; monotone, gap-free (under Rollback). Copy.
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct Seq(pub u64);
```

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (in-memory mode ignores it)
    pub durability: Durability,       // per-commit Fsync (durable-before-visible) | InMemory (no journal/recovery)
    pub checkpoint: CheckpointPolicy, // auto-checkpoint trigger, evaluated on-commit inside transact; no timer thread
    pub retain_checkpoints: usize,    // N ≥ 1 most-recent checkpoints kept; journal reclaimed only below the oldest
}

pub enum Durability {
    Fsync { burned_seq: BurnedSeqPolicy }, // the one ordering: append records → marker → barrier (one fsync) → install
    InMemory,                              // no journal/barrier/recovery (MIC-faithful); checkpoint()/flush() are no-ops
}
pub enum BurnedSeqPolicy { Rollback, TolerateGap }  // gap-free (default) | monotone-only
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }  // on-commit; no timer

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // no retained checkpoint loads and genesis is unreachable (whole fallback chain exhausted)
    Corruption { at: Seq },  // durable committed data in the replayed range (S_load, W] is corrupt; halt, never drop.
                             // `at` is the next intact frame's seq (the run's own seqs are unreadable)
}
pub enum CheckpointError { Io(io::Error), Serialize, Poisoned }  // Poisoned: a prior barrier failure halted the kernel
```

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover (load latest valid retained checkpoint @S_load, falling back to an older retained
    /// one then genesis; replay committed records S_load < Seq ≤ W) or init from `genesis` (= Σ₀).
    /// CALLER CONTRACT: `genesis` MUST be byte-identical on every open() of a given journal.
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint embodying all records with Seq ≤ s, keep `retain_checkpoints`, reclaim
    /// journal below the oldest retained one. Non-blocking to writers; serialized against itself.
    /// Returns the checkpointed seq, or Poisoned. Under InMemory it is a no-op returning current_seq().
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Shutdown/checkpoint hook. Under per-commit Fsync and InMemory it is a no-op returning Ok
    /// (every commit already fsyncs its barrier). No-op on a poisoned kernel.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

```rust
/// A pinned, consistent view of one committed state. Newtype over the loaded root Arc; field
/// private (Committed is M2-internal). Carries its own seq() (V1 retrospective) and world().
pub struct Snapshot<W: WorldState>(Arc<Committed<W>>);

impl<W: WorldState> Kernel<W> {
    /// One committed state, pinned. Read EVERY constituent of a multi-read verdict off ONE
    /// Snapshot (discharges clause 6). INFALLIBLE; keeps serving the last root even when poisoned.
    pub fn snapshot(&self) -> Snapshot<W>;
    /// The currently installed root's seq — equal AT THE INSTANT OF CALL to a snapshot() taken then,
    /// but NOT a substitute for it across calls, and NOT the stamp for a snapshot-computed verdict.
    /// Never regresses; infallible, including when poisoned.
    pub fn current_seq(&self) -> Seq;
}
impl<W: WorldState> Snapshot<W> {
    pub fn seq(&self) -> Seq;     // the committed index this view is OF (V1 retrospective); by value (Seq: Copy)
    pub fn world(&self) -> &W;    // read your store's slice off this
}
```

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` for the txn's duration, run `f` against a consistent base, and — iff `f` returns
    /// Ok with ≥1 staged record — commit them atomically & durably under one marker, install the
    /// root, then return (A7). Returns (T, Seq): the closure's value and the committed last_seq.
    /// f → Err: clean typed rejection, nothing committed. f → Ok with zero records: zero-step op,
    /// no commit, returned Seq is the base Committed's seq. NON-REENTRANT: `f` MUST NOT call any
    /// kernel write path (the applier lock is held — a nested write DEADLOCKS).
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
    Durability(io::Error),  // barrier failed before install AND the un-acked tail was durably truncated → a TRUE
                            // no-op; caller may safely re-invoke
    Poisoned,               // kernel halted by a prior unrecoverable failure; returned by the poisoning call and by
                            // every later transact. Do not re-invoke. Reads keep serving the last consistent root.
}
```

## Caller contracts & obligations

**`WorldState` (the engine implements; M2 only calls down through it)**
- `apply` MUST be deterministic, total, side-effect-free — replay must reproduce committed state exactly.
- `apply` MUST maintain every derived hint incrementally; a hint not folded in `apply` is stale after every live write and after replay.
- `apply` is NOT required to be idempotent — M2 folds each committed record exactly once; do not write `apply` to tolerate double-application, and do not rely on it being applied twice.
- `rebuild_derived` runs once at load, before replay, never on a live commit — it cannot keep a hint current by itself.
- If you override `rebuild_derived`, it MUST seed exactly the hint state that folding every record with Seq ≤ S (S = loaded checkpoint's seq) through `apply` would produce; otherwise the recovered hint diverges from the live-maintained one and reads go wrong. M2 cannot check this.

**`open`**
- The caller MUST pass a byte-identical `genesis` (= Σ₀) on every `open()` of a given journal; recovery folds journaled deltas onto it, never onto a journaled root. A drifting `genesis` silently mis-recovers. M2 cannot check this.
- Handle `OpenError::Io`, `OpenError::BadCheckpoint`, and `OpenError::Corruption { at }` — the latter two are operator-intervention conditions, not auto-retried.
- Under `Durability::InMemory`, `open()` ignores `journal_path`, runs no recovery, and inits from `genesis` (S_load = 0).

**`checkpoint`**
- Returns the checkpointed `Seq`, or `CheckpointError::Poisoned` if a prior barrier failure halted the kernel.
- Non-blocking to writers and serialized against itself; safe to call concurrently with the on-commit auto-trigger.
- A caller-invoked `checkpoint()` does not reset the auto-trigger's cadence counters (benign cadence imprecision).
- Under `Durability::InMemory` it is a no-op returning `current_seq()`.

**`flush`** — no-op returning `Ok` under per-commit `Fsync`, `InMemory`, and on a poisoned kernel; retained as the slot-in point for the deferred group-commit mode.

**`snapshot`**
- INFALLIBLE; continues to serve the last committed root even on a poisoned kernel.
- Read EVERY constituent of a multi-read verdict off ONE `Snapshot` — that discharges clause 6 by construction. Do NOT issue separate `snapshot()` calls per constituent.

**`current_seq`**
- Returns the currently installed root's seq; never regresses (install is serialized); infallible, including when poisoned.
- NOT a substitute for `snapshot()` across calls, and NOT the stamp for a snapshot-computed verdict — a write may land between a `snapshot()` and a later `current_seq()`. Stamp a verdict with the `seq()` of the one `Snapshot` its constituents were read off; reserve `current_seq()` for a bare "where is the log now?" query.

**`Snapshot::seq` / `world`** — `seq()` is the committed index this view is OF (V1 retrospective, by value); `world()` returns the pinned `&W` to read your store's slice off.

**`transact`**
- The caller MUST NOT call `transact` (or any kernel write path) from inside `f` — the applier lock is held, so a nested write deadlocks. Compose a composite as ONE closure over neighbors' PURE math, never a transaction-within-a-transaction.
- `push` takes `W::Record`; stage your store's OWN record type lifted via `.into()` (never construct the central `Record`).
- For frontier/allocation math read `stg.working().x()` (reflects records already pushed this closure — required for multi-atom runs to mint at consecutive slots); read `stg.base().x()` for the txn-start state.
- Guarantee on `Ok(_, ≥1 record)`: committed atomically and (under `Fsync`) durably under one marker, root installed before return; returned `Seq` is the committed `last_seq` — a write's exact V1 coordinate (use this, never a post-hoc `current_seq()`).
- `f` returning `Ok` with zero records → zero-step op, no commit; returned `Seq` is the base `Committed`'s seq (the committed index the op evaluated against). Under `Fsync` it never waits.
- `f` returning `Err(e)` → `TxnError::Rejected(e)`, nothing committed, no dangling state (surface verbatim to M10).
- `TxnError::Durability(_)` → a TRUE no-op (tail truncated, nothing installed); the caller may safely re-invoke.
- `TxnError::Poisoned` → the kernel is halted; do not re-invoke (reads still work).
- Commit-before-acknowledge: a successful `transact` returns only after its commit is installed and (durable mode) durable. External readers never see `Staging::working()` intermediate states — only the single atomic install.

**Invariants a caller may rely on**
- Total order, monotone `Seq`; gap-free under `BurnedSeqPolicy::Rollback`, monotone-only under `TolerateGap` (the replayed range may then contain gaps — do not add a Seq-contiguity check).
- No torn read / per-call single state; `Snapshot` is a stable pinned view; `current_seq()` never regresses.
- Composite atomicity: none-or-all to external readers.
- Under `Fsync`, file order == `Seq` order and every installed root is durable (durable-before-visible).

## Seams exposed downstream

- **→ everyone (store code), three hard contracts:** (1) stage only authoritative deltas, maintain hints incrementally in `apply`, and never journal a hint; (2) any `rebuild_derived` override must seed exactly the `apply`-fold of the `Seq ≤ S_load` prefix; (3) **Pure composable step surface** — any store primitive that appears as a step inside another store's composite MUST be exposed in two forms: its standalone `transact`-wrapped form AND a pure function over its own slice `&XState` (reached as `stg.base().x()`/`stg.working().x()` through the `HasX` accessor, never the bare `&W`), returning its OWN `XRec` (never the central `Record`), which the composite lifts with `.into()` and `stg.push`es. M3/M5 must publish this pure surface and their `XRec` variants up front.
- **→ M3 (allocation):** `let (addr, _seq) = kernel.transact(&[key(home, subspace)], |stg| { let max = recompute_max(stg.working().ns(), home, subspace); let addr = inc(max, 0); stg.push(NsRec::Alloc{ addr, … }.into()); Ok(addr) })?`. M3 supplies the key bytes and does the address math; pushes its own `NsRec`. When the same discipline is a step of a composite, reuse the pure `recompute_max`/`inc` body — never a nested `transact`.
- **→ M5 (placement composite, INSERT/COPY/VERSION):** one `transact([key(d, s_C)], …)` staging m × K.α with their K.μ⁺ and K.ρ, returning `(_, last_seq)`. Each K.α mints from `stg.working().content()` + M1's pure `inc` (NOT `base().content()`). M5 checks S3★ on `stg.working()` and the J-couplings at the boundary; M2 commits atomically. Each record is the owning store's `XRec` via `.into()`. CREATENEWDOCUMENT is one `transact` registering the entity (returns its `Seq`); it does not materialize an arrangement.
- **→ M7 (idem=⊤ emit + link-seating):** `transact([class_key, key(home, s_L)], …)`; dedup-read off `stg.working().links()`; hit branch stages nothing (zero-step, returns `(Hit, base.seq())`); emit branch stages `LinkRec::Emit` (K.λ) and M5's `ArrRec::SeatLink` (K.μ⁺_L) by folding M5's pure `m5_next_link_vpos` — the M7 → M5 edge with no return. No K.ρ push for link seating (J-LV). `class_key` serializes same-class emits; the alloc key serializes same-home allocation.
- **→ M6/M8/M9 (readers & verdicts):** `let s = kernel.snapshot();` then read every constituent off `s` (clause 6). M9 reports quiescence as "as of `s.seq()`" (V1). M9's reactive rule fires do NOT call `transact` directly — they go through M7's gated write path (and predicate-def content rides M5's placement composite); a single-step (m = 1) fire is one atomic `transact` inside M7's emit, and M9 takes the fire's index from the `Seq` M7 returns.
- **→ M10:** opens/commits each operation's transaction via `transact`, receives `(result, last_seq)`, acknowledges to the external client only after it returns (commit-before-ack), may report `last_seq`, surfaces `TxnError::Rejected(E)` as a typed rejection (never a silent skip), and treats `TxnError::Poisoned` as a halt (do not re-invoke). On startup, `OpenError::Corruption`/`BadCheckpoint` are operator-intervention conditions, not auto-retried.
- **Crate placement of the seam:** the central `LockKey` space-tag enum lives in M2's own crate (`skep-kernel`), below every store — every store draws its 1-byte prefix from it (cross-store tag uniqueness). The shared `key(home, …) -> LockKey` constructor (which names both `Address` and `LockKey`) lives in the shared base crate over `skep-address` + `skep-kernel`, not in `skep-kernel`; every store building a namespace lock key calls that one constructor.

## Boundary — NOT provided here

- Address, frontier, or coverage-class computation — M2 has no address algebra (M1/M3/M7 supply keys and do the math).
- Store permanence P0–P3/L12 and the J-couplings J0/J1★ — the stores enforce these at their composite boundaries *through* M2, never by it.
- Interpretation of record semantics — payloads are opaque `W::Record`.
- Register-before-allocate ordering — a store precondition checked against the snapshot, then a clean `Rejected` if unmet.
- The request lifecycle, parse/dispatch table, and acknowledgment-to-client — M10's; M2 keeps only the commit-gate *mechanism*.
- Ownership of derived hints — the stores own them; M2 journals only authoritative deltas.
- Multi-*step* (m ≥ 2) batch atomicity — M2 offers only the per-`transact` atomic unit; a store issues an m ≥ 2 batch as *separate* `transact`s (collapsing a *witnessed* batch into one suppresses intended partial visibility). A single-step (m = 1) fire IS one atomic `transact`. M2 neither forces nor forbids the granularity.
- Durability *as a requirement* — not a MIC clause; the `Durability::InMemory` mode is faithful.
- `LockKey` ordering carries no meaning beyond bytewise `Ord` (never tumbler order). M2 has no upstream module dependency.
