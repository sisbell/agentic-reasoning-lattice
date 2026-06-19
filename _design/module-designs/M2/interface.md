# M2 — Interface (for dependents)

M2 owns the generic transactional substrate: it turns every state change into one atomic, totally-ordered, durable, recoverable step (or a composite committed as one), serves consistent committed snapshots, and serializes writers — over an opaque payload and opaque keys.

## Public interface

```rust
// ---- The engine's contract to M2 (dependency-inverted) ----
pub trait WorldState: Clone + Serialize + DeserializeOwned + Send + Sync + 'static {
    type Record: Serialize + DeserializeOwned + Clone + Send + Sync + 'static;
    /// The ONE deterministic, total, side-effect-free fold step — drives both live
    /// commit and replay. NOT required to be idempotent. Maintains every derived hint
    /// incrementally (a hint not folded here is stale after every write and after replay).
    fn apply(&self, record: &Self::Record) -> Self;
    /// Seed derived hints from authoritative state. Runs ONCE at load, BEFORE replay,
    /// NEVER on a live commit. Default identity; override iff hints are `#[serde(skip)]`.
    fn rebuild_derived(self) -> Self { self }
}

/// Opaque serialization key — the documented serialization seam M3/M7 code against.
/// M2 only Eq/Hash/Ord-s the bytes (Ord is bytewise, NOT tumbler order). Callers prefix
/// a 1-byte space tag drawn from the engine crate's SINGLE CENTRAL ENUM.
pub struct LockKey(pub Vec<u8>);

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct Seq(pub u64);  // M2's per-record linearization coordinate; monotone, gap-free (under Rollback). Copy.
```

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (in-memory mode ignores it)
    pub durability: Durability,       // per-commit Fsync (durable-before-visible) | InMemory (MIC-faithful)
    pub checkpoint: CheckpointPolicy, // EveryN(u64) | Interval(Duration) | JournalBytes(u64) | Manual
    pub retain_checkpoints: usize,    // N ≥ 1 most-recent checkpoints kept; reclamation floor = oldest retained
}

pub enum Durability {
    Fsync { burned_seq: BurnedSeqPolicy }, // the ONE ordering — durable-before-visible
    InMemory,                              // no journal, no barrier, no recovery (MIC-faithful)
}
pub enum BurnedSeqPolicy { Rollback, TolerateGap }  // gap-free (default) | monotone-only
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // no retained checkpoint loads and genesis is unreachable (whole fallback chain exhausted)
    Corruption { at: Seq },  // CRC failure in the genuinely-replayed range (S_load, W]; `at` = the corrupt run's
                             // inferred upper bound (next intact frame's seq). Halt, never drop.
}
pub enum CheckpointError { Io(io::Error), Serialize, Poisoned }  // Poisoned: a prior barrier failure halted the kernel
```

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover from cfg.journal_path (load latest valid retained checkpoint → rebuild_derived →
    /// replay committed records S_load < Seq ≤ W) or init from `genesis` (= Σ₀). Returns Self or OpenError.
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint embodying all records with Seq ≤ s; non-blocking to writers; cadence is
    /// the caller's policy. Returns the checkpointed seq `s`, or CheckpointError::Poisoned. In-memory
    /// mode: a NO-OP returning current_seq().
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Shutdown/checkpoint hook. Under per-commit Fsync and in-memory mode it is a no-op returning Ok(());
    /// on a poisoned kernel likewise a no-op returning Ok.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

```rust
/// A pinned, consistent view of one committed state. A newtype over the loaded root Arc
/// (`Committed` is M2-internal; the field is private).
pub struct Snapshot<W: WorldState>(Arc<Committed<W>>);

impl<W: WorldState> Kernel<W> {
    /// One committed state, pinned. Read EVERY constituent of a multi-read verdict off ONE
    /// Snapshot (discharges clause 6 by construction). INFALLIBLE, including on a poisoned kernel.
    pub fn snapshot(&self) -> Snapshot<W>;
    /// The currently installed root's seq — equal AT THE INSTANT OF CALL to a snapshot() taken then,
    /// but NOT a substitute for it across calls. Never regresses. Infallible, including when poisoned.
    pub fn current_seq(&self) -> Seq;
}
impl<W: WorldState> Snapshot<W> {
    pub fn seq(&self) -> Seq;     // the committed index this view is OF (V1 retrospective); by value
    pub fn world(&self) -> &W;    // read your store's slice off this
}
```

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` for the txn's duration, run `f` against a consistent base state, and — iff `f`
    /// returns Ok with ≥1 staged record — commit them atomically & durably under one marker, INSTALL,
    /// then return (A7). Returns (T, Seq): the closure's value and the committed last_seq.
    /// `f` returning Err → clean typed rejection, nothing committed. Ok with zero records → zero-step
    /// op, no commit, returned Seq = base.seq(). NON-REENTRANT: `f` MUST NOT call any kernel write path.
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
    Durability(io::Error),  // per-commit barrier failed, un-acked tail durably truncated → TRUE no-op; caller may re-invoke
    Poisoned,               // kernel halted by a prior UNRECOVERABLE failure; returned by poisoning call and every later transact
}
```

## Caller contracts & obligations

- **`open(cfg, genesis)`** — caller supplies `genesis` = Σ₀ (used only when no journal/checkpoint exists). Handle `OpenError::Corruption{at}` and `BadCheckpoint` as operator-intervention halts (do **not** auto-retry); `Io` as I/O failure.
- **`checkpoint()`** — non-blocking to writers; cadence is the caller's policy. Returns the checkpointed `Seq`, or `CheckpointError::Poisoned` (kernel halted — no further checkpoint). In-memory mode returns `current_seq()` as a no-op.
- **`flush()`** — currently always a no-op `Ok(())` (per-commit Fsync, in-memory, and poisoned kernel); call it as the shutdown hook regardless.
- **`snapshot()`** — INFALLIBLE, stays available even on a poisoned kernel. Read **every** constituent of a multi-read verdict off **one** `Snapshot`; do not issue separate `snapshot()` calls per constituent.
- **`current_seq()`** — infallible, never regresses; a sound "latest committed index" progress indicator only. **NOT** the stamp for a snapshot-computed verdict — stamp a verdict with the `seq()` of the single `Snapshot` its constituents were read off (a write may land between a `snapshot()` and a later `current_seq()`).
- **`Snapshot::seq()`** — the committed index `world()` is of; a verdict's V1 retrospective coordinate.
- **`Snapshot::world()`** — read your store's slice off this `&W`.
- **`transact(keys, f)` preconditions** — `f` MUST NOT call `transact` (or any kernel write path): the applier lock is held, so a nested write **deadlocks**. Compose a neighbor's *pure* body inside the one closure, never a transaction-within-a-transaction. Caller supplies `keys` as opaque bytes, each prefixed with a 1-byte space tag from the engine's central enum.
- **`transact` outcomes** — `f` Ok with ≥1 record → returns `(T, Seq)` where `Seq` is the committed `last_seq` (the write's exact V1 coordinate). Returns only after the commit is installed and (under Fsync) durable (commit-before-acknowledge). `f` Ok with zero records → zero-step op, no commit, returned `Seq = base.seq()`.
- **`transact` errors caller must handle** — `TxnError::Rejected(E)` (f's typed precondition failure, verbatim); `TxnError::Durability(io::Error)` (a **true no-op** — nothing committed, caller may safely re-invoke); `TxnError::Poisoned` (kernel halted — treat as a halt condition, do **not** re-invoke).
- **`Staging`** — read `base()` for the txn-start root; read `working()` (base folded with records pushed so far) for any frontier/allocation math, so each atom of a multi-atom run sees prior atoms' deposits (reading `base()` for every atom collides). `push(r)` folds `r` into `working` and appends it to the txn's records. Intra-composite intermediate states are visible only to the executing closure, never to external readers.
- **`LockKey`** — the 1-byte space tag MUST be drawn from the engine crate's single central enum (never chosen per-store); that is what guarantees cross-store key uniqueness. M2 orders keys bytewise, **not** in tumbler order.
- **`WorldState` implementer obligations** — `apply` must be deterministic/total/side-effect-free and maintain every derived hint incrementally (a hint not folded in `apply` is stale after every live write and after replay); it is **not** required idempotent. `rebuild_derived` defaults to identity; override it iff hints are skip-serialized, and an override MUST seed exactly the hint state that folding every record with `Seq ≤ S_load` through `apply` would produce, else the recovered hint diverges from the live one (M2 cannot check this). Stage only authoritative deltas; **never journal a hint**.

**Invariants a caller may rely on:**
- Total order, monotone `Seq` refining 𝔼; gap-free under `BurnedSeqPolicy::Rollback`, monotone-only under `TolerateGap`. No caller derives `idx(σ)` from `Seq`.
- No torn reads / per-call single-state: external readers see only the atomically-installed committed root; `current_seq()` never regresses.
- Composite atomicity: a `transact` is externally none-or-all.
- Multi-read single-state: all constituents read off one `Snapshot` give a consistent verdict.
- Reads stay available and sound on a poisoned kernel; only `transact`/`checkpoint` fail with `Poisoned`.

## Seams exposed downstream

- **→ everyone (composition seam):** the engine crate defines `World` (composing all store slices) and `Record` (the union enum of all stores' record-types), implements `WorldState` for `World` by dispatching `apply` to the owning store, owns the single central `LockKey` space-tag enum, and instantiates `Kernel<World>`. Stores contribute `Record` variants + `apply` arms; mandatory incremental hint maintenance lives in `apply`, with optional `rebuild_derived` to seed skip-serialized hints.
- **→ M3 allocation:** `kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.working(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })?`. M3 supplies key bytes and all address math; M2 serializes + commits. Standalone form is for a bare allocation; per contract (3), when allocation is a step of a larger composite, the caller reuses the **pure** `recompute_max_under`/`inc` body against `stg.working()` rather than nesting this `transact`.
- **→ M5 placement composite (INSERT/COPY/VERSION):** one `transact([key(d, s_C)], …)` staging, for a span of m content atoms, m × K.α + their K.μ⁺ + K.ρ, returning `(_, last_seq)`. Each `K.α` mints against `stg.working()` (not `stg.base()`). M5 checks S3★ on `stg.working()` and the J-couplings at the boundary; M2 commits atomically. CREATENEWDOCUMENT is one `transact` registering the entity (returns its `Seq`), not an arrangement.
- **→ M7 idem=⊤ emit:** `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })` → `(outcome, seq)`. Nullify hit-branch stages nothing (zero-step), returning `(Hit, base.seq())`. M7's MAKELINK seats home links by folding **M5's** pure seating body (edge M7 → M5, no return edge), never a nested `transact`.
- **→ M6/M8/M9 readers & verdicts:** `let s = kernel.snapshot();` then read every constituent off `s`; report a verdict "as of `s.seq()`" (V1). M9 calls M2 directly only for snapshot verdicts; its rule *fires* go through M7's gated write path and its predicate-def content rides M5's placement composite. A single-step (`m = 1`) fire is one atomic `transact` inside M7's emit; M9 takes the fire's index from the `Seq` M7 returns.
- **→ M10:** opens/commits each operation's transaction via `transact`, receiving `(result, last_seq)`; acknowledges the external client only after it returns (commit-before-ack), may report `last_seq`, surfaces `TxnError::Rejected(E)` as a typed rejection, treats `TxnError::Poisoned` as a halt (do not re-invoke). On startup, `OpenError::Corruption`/`BadCheckpoint` are operator-intervention conditions, not auto-retried.
- **Pure composable step surface (contract 3), among M3/M5:** because `transact` is non-reentrant, any store primitive that appears as a step inside another store's composite MUST be published in **two** forms — its standalone `transact`-wrapped form **and** a **pure** function over a supplied `&W` (read off `stg.base()`/`stg.working()`) plus its `Record` variant(s) — so the enclosing composite folds the pure body and stages the records, never nesting transactions. M2 cannot enforce this; M3/M5 must publish the pure surface up front.

## Boundary — NOT provided here

- Address, frontier, and coverage-class computation (M1/M3/M7) — M2 has no address algebra; keys and payloads are opaque.
- Store permanence P0–P3/L12 and the J-couplings J0/J1★ (stores enforce these *through* M2, never by it).
- Interpretation of record semantics (M2 acts on no record's meaning or →_sh classification).
- The request lifecycle, parse/dispatch table, and acknowledgment-to-client (M10) — M2 keeps only the commit-gate mechanism.
- Derived-hint *ownership* (the stores own hints; M2 journals only authoritative deltas).
- Register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected`).
- Multi-*step* (`m ≥ 2`) batch atomicity — M2 offers only the per-`transact` atomic unit; the store issues an A5 batch as separate `transact`s (or may over-satisfy by committing as one). A single-step (`m = 1`) fire **is** one atomic `transact`.
- Durability *as a requirement* — not a MIC clause; the `Durability::InMemory` mode (no journal/barrier/recovery) is faithful.
