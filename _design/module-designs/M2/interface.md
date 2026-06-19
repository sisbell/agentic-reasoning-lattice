# M2 — Interface (for dependents)

M2 owns the engine's **generic transactional substrate**: a WAL + atomic-install + keyed-serialization + snapshot kernel (`Kernel<W>`) that makes every state change one atomic, totally-ordered, durable, recoverable step (or a composite committed as one) over **opaque payloads and opaque keys** — serving consistent snapshots and serializing writers, knowing nothing about what any change means.

## Public interface

The kernel is `Kernel<W>` for an engine-supplied `W: WorldState`. Keys are opaque bytes; payloads are the engine's `W::Record`. All write paths return only after the commit is installed and (under the durable mode) durable.

```rust
// ---- The engine's contract to M2 (dependency-inverted) ----
pub trait WorldState: Clone + Serialize + DeserializeOwned + Send + Sync + 'static {
    type Record: Serialize + DeserializeOwned + Clone + Send + Sync + 'static;
    /// The ONE deterministic, total, side-effect-free fold step — drives both live commit
    /// and replay. Folds authoritative deltas AND maintains every derived hint incrementally.
    /// NOT required to be idempotent (recovery applies each committed record exactly once).
    fn apply(&self, record: &Self::Record) -> Self;
    /// Seed derived hints from authoritative state. Runs ONCE at load, BEFORE replay, NEVER on
    /// a live commit. Default identity; override iff hints are #[serde(skip)]. An override MUST
    /// seed exactly the apply-fold of the Seq ≤ S prefix it stands in for (S = loaded checkpoint seq).
    fn rebuild_derived(self) -> Self { self }
}

/// Opaque serialization key — the documented serialization seam M3/M7 code against. M2 only
/// Eq/Hash/Ord-s the bytes (Ord is bytewise, NOT tumbler order). Callers prefix a 1-byte space
/// tag drawn from a SINGLE CENTRAL ENUM in the engine crate (guarantees cross-store uniqueness).
pub struct LockKey(pub Vec<u8>);

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct Seq(pub u64);  // M2's per-record linearization coordinate; monotone, gap-free. Copy.
                          // A REFINEMENT of ASN-0134's 𝔼, not an identity; no caller derives idx(σ) from Seq.
```

**Config & errors** — carried on `KernelCfg`.

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (ignored by the in-memory mode)
    pub durability: Durability,       // per-commit Fsync (durable-before-visible barrier) | InMemory (MIC-faithful)
    pub checkpoint: CheckpointPolicy, // checkpoint cadence
    pub retain_checkpoints: usize,    // N ≥ 1 most-recent checkpoints kept; N = 1 ⇒ newest is sole base, no fallback
}

pub enum Durability {
    Fsync { burned_seq: BurnedSeqPolicy }, // the one ordering: append records → marker → barrier → install
    InMemory,                              // no journal/barrier/recovery; checkpoint()/flush() are no-ops
}
pub enum BurnedSeqPolicy { Rollback, TolerateGap }  // gap-free (default) | monotone-only — durability-failure rollback
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // the whole retained-checkpoint → genesis fallback chain is exhausted
    Corruption { at: Seq },  // CRC failure in the genuinely-replayed range (S_load, W]; `at` = inferred upper bound.
                             // Halt, never drop. (A CRC failure ≤ S_load or beyond W is NOT fatal.)
}
pub enum CheckpointError { Io(io::Error), Serialize, Poisoned }  // Poisoned: a prior barrier/truncation failure halted the kernel
```

**Lifecycle**

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover from the journal (load latest valid retained checkpoint → rebuild_derived → replay
    /// committed records) or init from `genesis` (= Σ₀). Records present beyond the committed prefix
    /// are an un-acked/torn tail and are discarded.
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint and reclaim journal space. Non-blocking to writers; cadence is the
    /// caller's policy. Returns the checkpointed seq, or Poisoned if a prior barrier failure halted
    /// the kernel. Under Durability::InMemory it is a NO-OP returning current_seq().
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Shutdown/checkpoint hook. Under per-commit Fsync and under InMemory it is a no-op returning
    /// Ok(()) (every commit already fsynced its barrier). No-op on a poisoned kernel.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

**Reads (snapshots)**

```rust
/// A pinned, consistent view of one committed state. (A newtype over the loaded root Arc; the
/// inner field is private — `Committed<W>` is M2-internal and not constructible by callers.)
pub struct Snapshot<W: WorldState>(Arc<Committed<W>>);

impl<W: WorldState> Kernel<W> {
    /// One committed state, pinned. INFALLIBLE; continues serving the last in-memory root even on
    /// a POISONED kernel. Read EVERY constituent of a multi-read verdict off ONE Snapshot.
    pub fn snapshot(&self) -> Snapshot<W>;
    /// The currently installed root's seq. Never regresses; a sound standalone "latest committed
    /// index" indicator. NOT the stamp for a snapshot-computed verdict. Infallible, incl. when poisoned.
    pub fn current_seq(&self) -> Seq;
}
impl<W: WorldState> Snapshot<W> {
    pub fn seq(&self) -> Seq;     // the committed index this view is OF (V1 retrospective); by value (Seq: Copy)
    pub fn world(&self) -> &W;    // read your store's slice off this
}
```

**Writes (transactions / composites)**

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` for the txn's duration, run `f` against a consistent base state, and — iff `f`
    /// returns Ok with ≥1 staged record — commit them atomically & durably under one marker, install
    /// the root, then return. Returns (T, Seq): the closure's value and the committed `last_seq`.
    /// `f` → Err: clean typed Rejected, nothing committed. `f` → Ok with zero records: zero-step op
    /// (A1), no commit, returned Seq = base.seq(). NON-REENTRANT: `f` MUST NOT call any kernel write
    /// path (a nested write DEADLOCKS).
    pub fn transact<T, E>(
        &self,
        keys: &[LockKey],
        f: impl FnOnce(&mut Staging<W>) -> Result<T, E>,
    ) -> Result<(T, Seq), TxnError<E>>;
}

pub struct Staging<W: WorldState> { /* base, working, records */ }
impl<W: WorldState> Staging<W> {
    pub fn base(&self) -> &W;            // Σ — the installed root at txn start
    pub fn working(&self) -> &W;         // Σᵢ — base folded with records so far (intra-composite checks; allocation math)
    pub fn push(&mut self, r: W::Record); // fold into working, append to the txn's records
}

pub enum TxnError<E> {
    Rejected(E),            // f's typed precondition failure — surfaced verbatim
    Durability(io::Error),  // barrier failed, un-acked tail truncated durably → a TRUE no-op; caller may re-invoke
    Poisoned,               // kernel halted by a prior unrecoverable failure → do NOT re-invoke
}
```

## Caller contracts & obligations

**Engine implementing `WorldState`:**
- `apply` MUST be deterministic, total, side-effect-free, and MUST maintain every derived hint incrementally — a hint not folded in `apply` is stale after every live write and after replay.
- `apply` MUST tolerate being non-idempotent only in the sense that M2 guarantees each committed record is folded exactly once; do not rely on M2 to dedup a double-apply.
- `rebuild_derived` runs once at load before replay and never on a live commit, so it cannot keep any hint current by itself — incremental maintenance MUST live in `apply`.
- If `rebuild_derived` is overridden, it MUST seed exactly the hint state that folding the `Seq ≤ S_load` prefix through `apply` would produce; M2 cannot check this, and a divergent seed makes recovered reads wrong.
- Stage only authoritative deltas; never journal a hint.

**`open(cfg, genesis)`:**
- Caller supplies `genesis` = Σ₀, used only when there is no journal to recover.
- Returns `OpenError::Corruption{at}` (durable committed data the recovered state needs is corrupt) — halt; treat as operator intervention, never auto-retry.
- Returns `OpenError::BadCheckpoint` when the retained-checkpoint→genesis fallback chain is exhausted — operator intervention.
- A committed-but-un-acked tail marker (lost ack) is replayed as a committed op — the caller, having received no ack/`Poisoned`, owns the lost-ack/indeterminate case (re-issue is the client's, against the recovered, advanced frontier).

**`transact(keys, f)`:**
- Pass the `keys` you would need under a per-key realization; in v1 the global lock serializes all writes, so `keys` is the documented seam, not a live lock table.
- `f` MUST NOT call `transact` (or `checkpoint`/`flush`) — it is non-reentrant; a nested write deadlocks on the held applier lock.
- Compose a multi-step composite as ONE closure that stages each record and calls neighbors' **pure** math against `stg.working()`/`stg.base()`; never nest a neighbor's `transact`.
- For frontier/allocation math read `stg.working()` (reflects records already pushed this closure), not `stg.base()` — each atom of a multi-atom run must mint against `working()` or addresses collide and the second atom is rejected.
- On `Ok(v)` with ≥1 record the returned `Seq` is the committed `last_seq` — a write's exact V1 coordinate; report from this, never from a post-hoc `current_seq()`.
- On `Ok(v)` with zero records (read-only/idem-hit/nullify-hit) no commit occurs and the returned `Seq` is `base.seq()`.
- `TxnError::Rejected(E)` is your typed precondition failure verbatim — surface it, never silently skip.
- `TxnError::Durability` is a TRUE no-op — nothing committed, no durable marker — safe to re-invoke.
- `TxnError::Poisoned` means the kernel is halted by an unrecoverable failure — do NOT re-invoke; treat as a halt condition.

**`snapshot()` / `Snapshot`:**
- Read every constituent of a multi-read verdict off ONE `Snapshot` — that alone discharges clause 6 (single-state verdict); do NOT issue separate `snapshot()` calls per constituent.
- Stamp a snapshot-computed verdict with that `Snapshot`'s `seq()` (V1 retrospective about Σ_r), never with `current_seq()`.
- Infallible and still served on a poisoned kernel; `world()` gives you your store's slice.

**`current_seq()`:**
- Use only as a bare "where is the log now?" progress indicator; it never regresses but is NOT a substitute for `snapshot()` across calls and NOT a verdict stamp (a write may land between a `snapshot()` and a later `current_seq()`).

**`checkpoint()` / `flush()`:**
- Cadence is the caller's policy; `checkpoint()` is non-blocking to writers and returns the checkpointed seq, or `Poisoned`.
- Under `Durability::InMemory` both are no-ops (`checkpoint()` returns `current_seq()`, `flush()` returns `Ok`).

**Invariants a caller may rely on:**
- Every installed/returned root is durable before the call returns (durable-before-visible); an acked read never reflects a state a crash can roll back.
- Total order with monotone `Seq`; gap-free under `BurnedSeqPolicy::Rollback`, monotone-only under `TolerateGap`.
- No torn reads; per-call single-state; atomic install = one indivisible step.
- A composite is none-or-all to external readers; intra-composite intermediate states (`stg.working()`) are visible only inside the executing closure.
- Reads (`snapshot`/`current_seq`) stay available and sound even when writes/checkpoints fail with `Poisoned`.

## Seams exposed downstream

- **→ engine crate (composition, dependency-inverted):** define `World` (composing all store slices) and `Record` (union of every store's record-types), implement `WorldState` for `World` (dispatch `apply` to the owning store), instantiate `Kernel<World>`, and own the **single central `LockKey` space-tag enum** from which every store's key constructor draws its 1-byte prefix (guarantees cross-store key uniqueness — no store picks a tag locally).
- **→ everyone (three hard contracts on store code):** (1) stage only authoritative deltas, maintain hints incrementally in `apply`, never journal a hint; (2) any `rebuild_derived` override must seed exactly the `apply`-fold of the `Seq ≤ S_load` prefix; (3) **pure composable step surface** — any store primitive that appears as a step inside another store's composite MUST be published in two forms: its standalone `transact`-wrapped form AND a pure function over a supplied `&W` (plus its `Record` variant(s)), so the enclosing composite folds the pure body into its own closure rather than nesting a `transact`.
- **→ M3 (allocation under frontier H0):** `kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.working(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })?` — M3 supplies key bytes and does all address math against `stg.working()`; M2 only serializes + commits. Publish the pure `recompute_max`/`inc` body per contract (3).
- **→ M5 (placement composite, INSERT/COPY/VERSION):** one `transact([key(d, s_C)], …)` staging m × K.α + K.μ⁺ + K.ρ, returning `(_, last_seq)`; M5 checks S3★/J-couplings on `stg.working()`. Each content K.α mints against `stg.working()` by reusing M3's pure math inside the one closure — never a nested allocation `transact`. M5 publishes its pure link-seating body + arrangement `Record` variants per contract (3).
- **→ M7 (idem=⊤ emit):** `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })?` → `(outcome, seq)`. Read-decide-deposit is atomic under the global lock; nullify hit = a zero-step `transact`. M7's MAKELINK seats home links by folding M5's pure seating body (edge M7 → M5, no return edge).
- **→ M6/M8/M9 (readers & verdicts):** `let s = kernel.snapshot();` then read every verdict constituent off `s`; report "as of `s.seq()`" (V1). M9 calls M2 directly only for snapshot verdicts; rule fires reach M2 through M7's gated write path (single-step m = 1 fire = one atomic `transact` inside M7's emit; M9 gets the fire index from the `Seq` M7 returns) and predicate-def content through M5's placement composite.
- **→ M10 (request lifecycle):** open/commit each operation via `transact`, receive `(result, last_seq)`, acknowledge the client only after it returns (commit-before-ack), may report `last_seq`, surface `Rejected(E)` as a typed rejection, treat `Poisoned` as a halt (do not re-invoke), and treat `OpenError::Corruption`/`BadCheckpoint` on startup as operator intervention.

## Boundary — NOT provided here

- Address/frontier/coverage-class computation and any address algebra — keys are opaque bytes, `Ord` is plain bytewise (M1/M3/M7 do all the math).
- Store permanence P0–P3/L12 and the J-couplings J0/J1★ — stores enforce these at their composite boundaries *through* M2.
- Interpretation of record semantics — M2 folds an opaque payload.
- Frontier discipline H0 itself (M3's allocator), register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected`).
- Derived hints — stores own them; M2 journals only authoritative deltas.
- The request lifecycle, parse/dispatch table, pipelining-vs-sequential client model, and ack-to-client (M10) — M2 keeps only the commit-gate mechanism.
- Multi-*step* (`m ≥ 2`) batch atomicity — M2 offers only the per-`transact` atomic unit; a store issues an A5 batch as *separate* `transact`s (and may over-satisfy by committing as one). A single-step `m = 1` fire **is** one atomic `transact`.
- Durability *as a requirement* — not a MIC clause; `Durability::InMemory` is a faithful no-journal/no-recovery mode.
- Per-key/CAS write concurrency and group-commit (`FsyncBatch`) — deferred out of v1; the `transact`/`snapshot` signatures and `LockKey` seam are invariant across these, so do not build against a live per-key lock table or a `Clean{through}` watermark in v1.
