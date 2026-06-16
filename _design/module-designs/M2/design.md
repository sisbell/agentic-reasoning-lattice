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
    /// commit and replay. Folds authoritative deltas AND maintains every derived hint
    /// incrementally; a hint NOT folded here is stale after every live write and after
    /// replay (rebuild_derived runs only at load — see below). Deterministic so replay
    /// reproduces committed state exactly; NOT required to be idempotent — recovery
    /// applies each committed record exactly once (the checkpoint embodies Seq ≤ s,
    /// replay covers Seq > s; §6/§7).
    fn apply(&self, record: &Self::Record) -> Self;
    /// Seed derived hints from authoritative state. Runs ONCE at load, BEFORE replay,
    /// and NEVER on a live commit — so it cannot keep any hint current by itself.
    /// Incremental hint maintenance MUST live in `apply` (which runs on every live
    /// commit AND every replay step); `rebuild_derived` exists solely to reconstruct
    /// hints a checkpoint skip-serialized (`#[serde(skip)]`). Default identity (hints
    /// folded by `apply` and serialized in the checkpoint); override iff hints are skipped.
    fn rebuild_derived(self) -> Self { self }
}

/// Opaque serialization key. M2 only Eq/Hash/Ord-s the bytes (Ord is bytewise, for
/// deadlock-free acquisition — NOT tumbler order). Callers prefix a 1-byte space tag
/// so distinct key spaces (e.g. (home,subspace) vs coverage-class) never collide.
pub struct LockKey(pub Vec<u8>);

pub struct Seq(pub u64);  // M2's per-record linearization coordinate; monotone, gap-free.
                          // A REFINEMENT of ASN-0134's 𝔼, not an identity: every →_sh step
                          // (K.σ/K.α/K.λ_sh) gets a Seq, but so do the non-→_sh records a
                          // composite stages (K.μ⁺/K.μ⁻/K.ρ). The subsequence of Seqs carrying
                          // →_sh records is order-isomorphic to 𝔼, so a →_sh record's Seq IS its
                          // idx(σ); M2's full Seq order is a finer total order (§2).
```

**Config & errors** — the knobs the Open-build-decisions section selects; carried on `KernelCfg`.

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (Durability::None ignores it)
    pub concurrency: Concurrency,     // SingleApplier (default) | PerKeyMerge | OptimisticCas — API-invariant (§8)
    pub durability: Durability,       // Fsync | FsyncBatch{window} | None
    pub visibility: Visibility,       // DurableBeforeVisible (canonical) | VisibleBeforeDurable (§1)
    pub burned_seq: BurnedSeqPolicy,  // Rollback (gap-free, default) | TolerateGap (monotone-only) (§1)
    pub checkpoint: CheckpointPolicy, // EveryN(u64) | Interval(Duration) | JournalBytes(u64) | Manual (§6)
    pub locks: LockLayout,            // Striped{stripes} | PerKey — unused under SingleApplier (§4)
}
pub enum Concurrency { SingleApplier, PerKeyMerge, OptimisticCas }
pub enum Durability  { Fsync, FsyncBatch { window: usize }, None }
pub enum Visibility  { DurableBeforeVisible, VisibleBeforeDurable }
pub enum BurnedSeqPolicy { Rollback, TolerateGap }
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }
pub enum LockLayout  { Striped { stripes: usize }, PerKey }

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // checkpoint file unreadable / failed its checksum → fall back to an earlier one or genesis
    Corruption { at: Seq },  // CRC failure INSIDE a marked (acked) composite — durable acked data is corrupt; halt, never drop (§7)
}
pub enum CheckpointError { Io(io::Error), Serialize }
```

**Lifecycle**

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover (latest checkpoint @s → rebuild_derived → replay committed records with
    /// `Seq > s`) or init from `genesis` (= Σ₀, with s = 0).
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint embodying all records with `Seq ≤ s` and truncate exactly
    /// those frames; recovery then replays exactly `Seq > s`. Non-blocking to writers.
    /// Cadence is the caller's policy. Returns the checkpointed seq `s`.
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
    /// under one commit marker before returning (A7). Returns `(T, Seq)`: the closure's
    /// value and the committed `last_seq` — a write's V1 retrospective coordinate, exact
    /// even under per-key concurrency (unlike a post-hoc `current_seq()`). `f` returning
    /// Err → clean typed rejection, nothing committed, no dangling state. `f` returning
    /// Ok with zero records → zero-step op (A1: read-only / idem-hit / nullify-hit), no
    /// commit; the returned Seq is then `base.seq()` — the committed index the op
    /// evaluated against (V1).
    pub fn transact<T, E>(
        &self,
        keys: &[LockKey],
        f: impl FnOnce(&mut Staging<W>) -> Result<T, E>,
    ) -> Result<(T, Seq), TxnError<E>>;
}

pub struct Staging<W: WorldState> { /* base, working, records */ }
impl<W: WorldState> Staging<W> {
    pub fn base(&self) -> &W;            // Σ — the read snapshot at txn start (the applier's working tip; §3)
    pub fn working(&self) -> &W;         // Σᵢ — base folded with records so far (intra-composite checks)
    pub fn push(&mut self, r: W::Record); // fold into working, append to the txn's records
}

pub enum TxnError<E> {
    Rejected(E),            // f's typed precondition failure — surfaced verbatim to M10
    Durability(io::Error),  // canonical durable-before-visible only: a barrier failed BEFORE
                            // install, so the txn's frames were truncated and nothing was
                            // installed → a TRUE no-op; caller may safely re-invoke. Under the
                            // optional visible-before-durable variant a barrier failure instead
                            // POISONS the kernel (§1) — the txn is already installed and cannot
                            // be unwound.
    Conflict,               // optimistic-CAS impl only; caller re-invokes. Never under single-applier/merge-install.
}
```

**Serialization (held-across-commits variant)** — the explicit clause-5 path when a run must be *separately* committed rather than one transaction (rarely needed; `transact`'s `keys` covers the atomic case).

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` until the guard drops, issuing inner `transact(&[], f)` calls between
    /// which readers may land (clause 5, reader-visible mid-run). Available ONLY under the
    /// per-key-concurrent and CAS realizations, where the lock table is live and `transact`
    /// honors keys. Under the single applier the table is unused and the applier lock is
    /// released between the inner commits, so a foreign same-key `transact` could commit
    /// between them and fragment the run — the guard provides NO run-exclusion there;
    /// single-applier runs MUST instead be one `transact([keys], f)` (atomic, over-satisfying
    /// clause 5). Prefer the one-`transact` form regardless.
    pub fn critical_section(&self, keys: &[LockKey]) -> CriticalGuard<'_>;
}

/// RAII guard: holds the acquired `LockKey` locks; releases all on drop. No methods —
/// its lifetime IS the critical section. (Live only under PerKeyMerge / OptimisticCas — §4.)
pub struct CriticalGuard<'a> { /* held lock guards + 'a borrow of the kernel's lock table */ }
```

## Core data model

The **only durable, authoritative state M2 owns is the journal.** Everything in memory is a recoverable fold of it (Lampson: the log is the truth; in-memory structures are hints). Within the recovered `World`, the *store-level* distinction between authoritative slices (C, L, E, M, R) and derived hints (spanfilade, reverse indexes) belongs to M4/M5/M7 — to M2 the whole `World` is one fold.

| Structure | Shape | Authority | Why this shape |
|---|---|---|---|
| **Journal** | append-only file(s) of CRC-framed records + per-txn commit markers | **authoritative, durable** | record-of-record; replay reconstructs everything; append-only makes immutability of committed steps free (ASN-0047 P0/P1/P2 at the log level) |
| **Root** | `arc_swap::ArcSwap<Committed<W>>`, `Committed { seq: Seq, world: W }` | recoverable materialization | lock-free reads; **atomic install = atomic, indivisible step (A0/A4)**; persistent `W` (im) ⇒ snapshot & install are O(1) and snapshots never tear |
| **Working tip** | `Committed<W>` held by the applier across a group-commit batch | volatile (internal to the applier; never externally visible; rebuilt fresh on recovery) | lets a batched txn read its predecessors' not-yet-published records (correct dependent reads); published to **Root** *once*, post-barrier (§1) |
| **Checkpoint** | serialized `W` @ `Seq` on disk (temp→fsync→rename) | recoverable cache (a prefix-fold) | bounds replay time; optional; safe to delete |
| **Lock table** | striped `Vec<parking_lot::Mutex<()>>` *or* `DashMap<LockKey, …>` | volatile (locks don't outlive a crash; recovery is single-threaded) | the keyed critical section (clauses 2/5/7) |
| **Sequencer** | `Seq` high-water + the install serialization point (a `Mutex` or actor mailbox) | volatile, recovered as `max committed Seq` | assigns the total order; serializes journal-append + install |

`W` is the engine's composition of all store slices, each an `im` persistent collection (`OrdMap` for address-keyed stores — gives prefix-range scans free — `HashMap`/`Vector` elsewhere). `W: Clone` is O(1) (Arc bumps); `W::apply` returns a structurally-shared successor touching only changed paths. This is the ASN-0134-recommended persistent-immutable representation: the root's identity *is* the version coordinate, making clauses 1/4/6 nearly free.

`Snapshot<W>` is `Arc<Committed<W>>` — a cheap, pinned, consistent view carrying its own `seq` (so verdicts can be reported as retrospective statements about `Σ_r`, V1).

## Internal design

### 1. The journal & WAL discipline

**Frames.** `[u32 len][u32 crc][payload]`; payload is `Record{ seq, txn, bytes }` or `Marker{ txn, last_seq, frame_checksum }`. A transaction appends its record frames in `Seq` order, then **one marker as its terminal frame**. **The marker is the recovery contract** (ASN-0047): a txn is committed iff its marker is *durable* and its `frame_checksum` validates over the txn's records; record frames past the last valid marker are a torn tail — discarded and truncated.

**Canonical commit ordering: durable-before-visible.** A txn commits in this order — *append records → append marker (terminal frame) → durability barrier → install the root → return `(v, last_seq)`*. Two properties this buys, both load-bearing for sound failure handling:

- **The marker is made durable only as the last step of its *own* commit.** A txn is committed exactly when *its own* marker reaches disk; nothing else may promote it. This closes the **phantom-commit hole**: were the marker merely *appended* before the barrier and left in the file, a later txn's fsync could flush a failed txn's marker, and recovery would replay an operation reported as failed — and, for a same-`(d,S)` allocation, the retried successor (computed against a root without the failed txn) would double-deposit a *colliding* address. The fix is to **truncate the un-acked tail on barrier failure** (below), so a failed marker is physically gone before any later fsync runs.
- **Barrier failure is a true no-op.** If the durability barrier fails, the txn's record+marker frames are truncated (durably) from the journal tail and the root is *not* installed — so no durable marker survives (recovery omits it) and no in-memory state reflects it. `transact` returns `TxnError::Durability` and the caller may safely re-invoke. The Seqs the txn had been assigned are **burned**; the serializer rolls the `Seq` high-water back to the last committed marker's `last_seq` before releasing, preserving the gap-free invariant. (The alternative — *tolerate* the gap, relaxing the invariant to monotone-only — is an open knob.)

**Group commit (the throughput realization of the canonical order).** `FsyncBatch{window}` amortizes the barrier across a batch. Because install must stay *after* durability, no `ArcSwap` root update happens until the batch's barrier — yet a batched txn must still read the state its predecessor left: a COPY pipelined after an INSERT into the same document must see the inserted content, and an allocation must read the frontier its predecessor advanced (H0). The applier therefore threads an **in-memory working tip** — a `Committed<W>` it advances with each batched txn's staged records — and draws each batched txn's `base` from that tip rather than from `root.load()`. So: under the serializer, for each batched txn append its record+marker frames and advance the tip; then *one* durability barrier; then publish the batch's **final tip** to the root in a single atomic install; each `transact` returns only after *its* batch's barrier. A barrier failure aborts the batch's un-acked tail (truncate + Seq rollback) and resets the tip to the last durable state, so no partial marker survives and the root never reflected the aborted work. Install stays *after* durability — external readers never see pre-durable state; the working tip is internal to the applier and never externally visible. (This bug — a batched dependent txn reading a stale pre-batch root yet landing at a higher `Seq` — is specific to *this* canonical default combined with group commit, and the working tip is its fix.)

**Only authoritative deltas are journaled.** Derived hints are *never* journaled — they are reconstructed by `apply` during replay (mandatory incremental maintenance — §6/§7), and seeded once at load by `rebuild_derived` if the checkpoint skip-serialized them. This is the structural answer to ASN-0134's divergence hazard (OQ10): one logical step is exactly one journal record driving one `apply`, so there is nothing to diverge.

`Durability::{ Fsync, FsyncBatch{window}, None }`. `None` is the fully in-memory realization — **MIC-faithful** (ASN-0134 is silent on durability), no journal, no recovery, atomicity/isolation intact.

**Optional variant: visible-before-durable (install-then-fsync).** Install the root *before* the batched barrier, returning only once durable. This is a throughput choice (install latency off the fsync's critical path), justified for *internal* causal dependence by prefix-closure: anything causally dependent on txn T is journaled after T, so "R durable ⟹ T durable," and a reader/writer that acts on a not-yet-durable T either commits (making T durable by prefix) or leaves no persistent effect. **But the install is already visible when the barrier runs, so its failure cannot be a no-op** — readers/writers may already have built on it; the only sound response is to **poison the kernel** (halt; subsequent calls fail), not return `TxnError::Durability`. And prefix-closure does *not* cover an **external read acked by M10**: a client can be told a read result reflecting a committed-but-not-yet-durable state that a crash then rolls back (the resolved ASN-0047/0134 conflict — see *Conflicts resolved*). Choose this variant only when that external-read window is acceptable. (Because it installs the root *before* the barrier, each txn's `base ← root.load()` already reflects its predecessors even under group commit — so this variant needs **no working tip**; the working-tip mechanism above is specific to the canonical durable-before-visible default.)

### 2. Sequencer & the linearization point

Each committed record receives the next `Seq` from a monotone counter, assigned inside the serialization point so the order is gap-free and a composite's records are **Seq-contiguous** (no foreign record interleaves a composite). **`Seq` refines ASN-0134's `idx(σ)`, it is not identical to it:** every `→_sh` step (`K.σ`/`K.α`/`K.λ_sh`) receives a `Seq`, but so do the non-`→_sh` records a composite stages (`K.μ⁺`/`K.μ⁻`/`K.ρ`); the subsequence of `Seq`s carrying `→_sh` records is order-isomorphic to `𝔼`, so a `→_sh` record's `Seq` *is* its `idx(σ)`, while M2's full `Seq` order is a finer total order. A `→_sh` record's `Seq` assignment is its linearization point (A2); one `transact` = one operation = one linearization point (single-step op) or one contiguous composite boundary. M2 fixes it; M10 merely chooses to call `transact` once per operation. Seq-contiguity is a property of M2's *internal* order; it is *not* what delivers W2 chain contiguity — that comes from holding `key(d,s_C)` across the run (§4).

### 3. The transaction / composite boundary

`transact(keys, f)` — recommended single-applier flow, canonical durable-before-visible:

```
acquire keys (bytewise-sorted, dedup'd)        // clauses 2/5/7; no-op under global applier
lock the applier (single global serializer)
base ← tip.load()                              // the working tip: == root for per-commit fsync or a
                                               //   batch's FIRST member; == predecessors' fold within
                                               //   a batch (§1) — so a batched COPY reads its INSERT
stg  ← Staging::new(base)
match f(&mut stg) {                            // store logic: reads stg.base()/working(), pushes records
    Err(e)              → return Rejected(e)            // clean rejection; nothing journaled/installed
    Ok(v) if stg empty  → return Ok((v, base.seq()))   // zero-step (A1); V1 referent = base.seq()
    Ok(v) ⇒
        seqs ← alloc_seqs(stg.records.len())            // linearization (burned & rolled back on failure)
        journal.append_records(txn, seqs, stg.records)
        journal.append_marker(txn, last_seq, checksum)  // the commit marker — terminal frame
        tip.advance(Committed{ last_seq, stg.working }) // advance the in-memory working tip
        durability.barrier()                            // per-commit: here; group commit: once at batch close
            on Err → journal.truncate(seqs); rollback_seq_hi; tip.reset_to_last_durable; return Durability
        root.store(tip.load())                          // atomic install — AFTER durability; group commit
                                                        //   publishes the batch's final tip once
        return Ok((v, last_seq))                         // commit-before-acknowledge
}
```

`base` is the applier's **working tip** (§1): under per-commit fsync it equals the current root and for a group-commit batch's *first* member likewise, but within a batch it is the fold of the batch's earlier txns, so a batched txn reads its predecessors' staged records (a batched COPY sees the INSERT it follows; a batched allocation reads the frontier H0 its predecessor advanced). The root — external readers' view — advances only at batch close, after durability.

`Staging.working` (= `base` folded with staged records, cheap over persistent `W`) is what lets the store check **intra-composite preconditions** at intermediate states (ASN-0047's "observable intermediate states," e.g. S3★ referential integrity after K.α but before K.μ⁺). Those intermediates are visible only to the executing closure — **never to external readers**, who see only the single atomic install. The J-couplings the closure may check at the boundary (`base`→`working`) are M5's to assert; M2 never does.

The barrier shown is the canonical per-txn durable-before-visible commit; group commit (§1) amortizes it across a batch and publishes the batch's final working tip after its barrier. Either way **install follows durability**, so `TxnError::Durability` is a sound true no-op (truncate + Seq rollback). The optional visible-before-durable variant (§1) moves the install above the barrier and converts a barrier failure into a kernel poison.

### 4. Keyed critical sections

One mechanism serves clauses 2, 5, 7; the key is always caller-supplied bytes. `transact` acquires `keys` before taking its snapshot and holds them through commit, so **read-decide-deposit is atomic for those keys** — exactly what clause 7's idem dedup needs (the dedup-read of the global active set and the deposit are one action under the coverage-class key; cf. G2) and what clause 2 needs (frontier-read-and-deposit under the `(home,subspace)` key — M3 does the `inc(max,·)` math; M2 only locks). Acquisition is bytewise-sorted and deduplicated → deadlock-free.

**Run contiguity (W2) is delivered by the held key, not by Seq order.** Staging a multi-atom content run inside one `transact([key(d,s_C)], …)` holds `key(d,s_C)` across every atom, so no foreign `s_C`-allocation to `d` interleaves between the run's first and last atom — *that* is W2 (chain/address contiguity). The single atomic install then *additionally* makes the run atomic-to-readers, over-satisfying clause 5 (no reader lands mid-run at all). Seq-contiguity (§2) is a distinct, internal property and is not the source of W2.

`critical_section` is the rarer guard that holds `keys` across *separate* inner commits — the modeled clause-5 path where readers *may* land mid-run. **It is available only under the per-key-concurrent and CAS realizations**, where the lock table is live and `transact` honors keys. Under the single applier the lock table is **unused** (the global applier lock subsumes every key, and is released between the section's inner commits), so a foreign `transact([key(d,s_C)], …)` — whose key is a no-op there — could commit between the inner commits and fragment the run; the guard therefore provides **no run-exclusion under the single applier**. A single-applier run must instead be **one `transact([keys], …)`** (atomic, satisfying clause 5 by over-satisfaction); the reader-visible-mid-run flavor of clause 5 is simply unavailable under the single applier, whose runs are atomic.

Lock table: striped `Vec<Mutex>` (bounded memory, possible false contention) or per-key map (no false contention, needs entry GC) — an open decision. Under the single-applier impl the table is unused; under per-key concurrency it is live and also backs `critical_section`. The `transact`/`snapshot` API is identical across realizations, so moving single-applier → per-key concurrency changes no caller's *call shape* — though it does newly *bind* the footprint-confinement contract on `f` (§8 / Dependencies & seams).

### 5. Snapshot reads

`snapshot()` is one lock-free `ArcSwap::load` → a pinned `Committed<W>`. Per-call single-state (clause 4 / A3 / V0) is by construction. A multi-read verdict reads all `p` constituents off **one** `Snapshot` → clause 6 / V2 for free (persistent state dissolves the "global" cost ASN-0134 flags). This is the seam contract on M6/M8/M9: thread one `Snapshot` through every constituent of a verdict; do not issue them as separate `snapshot()` calls (the §8 pathology).

### 6. Checkpoint & truncation

Non-blocking: grab a `Snapshot` `Committed{ seq: S, world }` (lock-free) — `world` is the fold of **exactly the records with `Seq ≤ S`**, and `S` is always a committed marker boundary (installs are atomic at commit). Serialize `world()` (authoritative; hints may `#[serde(skip)]`) to `checkpoint.tmp`, fsync, atomic-rename to `checkpoint.<S>`, fsync dir, then **truncate every journal frame with `Seq ≤ S`** (all fully embodied in the checkpoint). The checkpoint @S thus *embodies* `Seq ≤ S`, and recovery (§7) replays *exactly the complement*, `Seq > S` — no overlap, no gap. This complementarity is essential because `apply` is **not** idempotent (a `Vector`-append record double-applies wrongly): every committed record must be folded into the recovered state exactly once. Writers run throughout — the snapshot's Arc keeps the checkpointed version alive while live installs advance the root. Crash mid-checkpoint leaves an ignored `.tmp` and an untruncated journal: always safe (the next recovery just replays more). Cadence (every-N / time / size) and representation (full-World vs per-store/incremental) are open knobs.

### 7. Recovery

`open`: load the latest valid checkpoint `checkpoint.<S>` (else `genesis`, with `S = 0`), call **`rebuild_derived`** (seeds hints the checkpoint skip-serialized from authoritative state — `apply` then keeps them current across replay), then replay the committed records with **`Seq > S`** via `apply` in `Seq` order — exactly the complement of what the checkpoint embodies (§6), no record applied twice or skipped. A txn is committed iff its marker is durable and validates (§1); record frames past the last valid marker, or a CRC-failed frame, are a torn tail → discard + truncate (it was never acked, so loss is correct, and a failed-barrier txn's frames were already truncated at failure time, so no failed marker survives to replay). CRC failure *inside a marked (acked) composite* is corruption of durable acked data → **halt and report** (`OpenError::Corruption`); never silently drop it. `apply` determinism guarantees replay reproduces the exact committed state (A6: every journal prefix up to a marker is a canonical reachable state). Recovery is single-threaded — the volatile lock table and `Seq` high-water are rebuilt fresh (the high-water as the last committed marker's `last_seq`).

### 8. Concurrency realizations — the fault line

The `transact`/`snapshot` API is invariant across these; only internal locking changes.

- **Single applier (recommended first; ASN-0047's choice).** `f` runs under the global applier lock. With per-commit fsync (or for a group-commit batch's *first* member) `base == current root`; under group commit `base` is the applier's **working tip** (§1/§3), so a later batch member reads its predecessors' staged records. The lock table is unused (keys are no-ops). This makes clauses **1, 2, 4, 5, 7 free**, leaving **clause 6** — which still needs the §5 one-`Snapshot` threading, since the §8 read-drift pathology arises even here, with no per-home concurrency — and the **clause-3** commit-gate ordering to be handled explicitly. Group commit (§1) batches the durability barrier across operations for throughput while keeping install after durability. Bounded by one core. *Because `f` always sees the live tip here, a store written against the single applier may freely read state outside its `keys` — which is exactly why the footprint contract below does not bite until migration.*

- **Per-key concurrent with merge-at-install (scaling path; what ASN-0134 G1 blesses).** `f` runs outside the install lock holding only its `keys`; at commit, a short global install section assigns Seqs, re-folds `stg.records` over the *current* root, journals, and swaps. This re-fold is conflict-free **only under a caller obligation** — *footprint confinement*: `f`'s **entire committed-state read set** — every value it consults to decide *what to stage, whether to reject, or which branch to take*, not merely the values it writes into staged records — must lie under state the txn's held `keys` cover, or be append-only-monotone (e.g. `a ∈ dom(C)`, which only grows). The contract is on the *read set* because merge-at-install re-folds the already-decided records over the current root **without re-running `f`**: any read outside the held keys means a stale *decision* (which records, hit vs miss, reject, branch) commits at a non-serializable position. This is ASN-0134 G1's full commutativity hypothesis — neither *reads* nor writes state another txn touches — raised here to a **seam contract** (Dependencies & seams). Under it, the held keys guarantee no concurrent writer touched this txn's read-set (G1 commute) and the re-fold reproduces `f`'s decision. **Persistent state alone gives neither the write-concurrency nor the confinement:** root-install still contends (the held keys, not persistence, give concurrency), and a store that *reads* or writes state *outside* its keys compiles and runs correctly under the single applier but **corrupts silently** under merge-at-install. The example seams honor the contract (M3 holds `key(home,subspace)` across the frontier read; M7 holds `class_key` across the active-in-class read), which is why those migrate cleanly; *new* store ops must be checked against it — and since "build single-applier first" authors stores *before* the discipline would otherwise bite, the contract must be stated up front. fsync stays batched outside the install section.

- **Optimistic frontier-CAS (optional).** No held locks; read fresh, compute, CAS the root, retry on change → may surface `TxnError::Conflict`. Same footprint-confinement obligation (the full read set) as merge-at-install. Viable when same-key contention is rare; retry termination is open (ASN-0134 OQ1/OQ3).

`critical_section` is available only under the latter two realizations (§4); the single applier offers only the one-`transact` run.

## Invariants & contracts

**By construction** (falls out of the data model above):
- **Total order, gap-free monotone `Seq`, refining `𝔼`** — counter under the serializer (ASN-0134 A1/A2, SequentialTransitionAxiom; ASN-0047 same). Every `→_sh` record's `Seq` is its `idx(σ)`; non-`→_sh` records also carry `Seq`s, so M2's order is a *refinement* of `𝔼`, not an identity (§2). Gap-freeness holds under Seq-rollback on durability failure (§1).
- **No torn read / per-call single-state** — immutable `Committed<W>` + atomic `ArcSwap` install + lock-free load (A0/A3/A4/V0, MIC-4). Under group commit, external readers see only the post-barrier root, never the applier's working tip (§1).
- **Multi-read verdict single-state** — one `Snapshot` threaded through all reads (V2, MIC-6; caller contract, made trivial by persistent root).
- **Composite Seq-contiguity** — a composite's Seqs assigned as a unit; an *internal-order* property only — W2 chain contiguity comes from the held `key(d,s_C)`, not from this (§2/§4).
- **Append-only journal; a committed frame (one whose marker is durable) is immutable; every prefix-to-a-marker is a replayable canonical state** — append-only file + terminal per-txn marker + `apply` determinism (ASN-0047 journaling; ASN-0134 A6).

**By active enforcement** (M2 must guard, named where):
- **Same-key serialization** — keyed critical section §4 / single applier §8 (ASN-0134 H2, MIC-2; M3 builds frontier H0 atop it).
- **Commit-before-acknowledge** — `transact` returns only post-durable+install §3 (A7, MIC-3).
- **Composite atomicity (none-or-all to readers)** — single atomic install §3 + commit-marker recovery discard §7 (ASN-0047).
- **Durability before ack, with a sound failure path** — canonical durable-before-visible: append records+marker → barrier → install (group commit: publish the batch's final tip) → return; a barrier failure truncates the txn's un-acked frames and rolls the `Seq` high-water back, so `TxnError::Durability` is a **true no-op** and no failed marker can be promoted by a later fsync §1/§3 (ASN-0047). The optional visible-before-durable variant instead **poisons** on barrier failure and exposes a not-yet-durable state to an external M10-acked read (resolved conflict — see *Conflicts resolved*).
- **Recovery faithfulness** — replay committed (`Seq > S`) records in order; discard the torn tail (a failed-barrier txn already left no marker); halt on corruption of a marked composite §6/§7 (A6; ASN-0047).
- **Deadlock-free multi-key acquire** — bytewise-sorted, deduplicated §4.
- **idem=⊤ dedup atomicity** — read-decide-deposit under the coverage-class key = one `transact` §4 (I1a/I4/G2, MIC-7).
- **Run contiguity** — a run as one `transact([key(d,s_C)], …)`: the held key delivers W2 chain contiguity, the single atomic install over-satisfies clause 5; or — *concurrent impls only* — `critical_section` held across separate deposits §4 (W2, MIC-5).
- **Live derived-hint correctness** — incremental hint maintenance is folded by `apply` on every commit and every replay step; `rebuild_derived` only seeds skip-serialized hints at load (§1/§7). A store that maintains a hint via `rebuild_derived` alone leaves it stale after every live write — so hint folding in `apply` is mandatory.

**Explicitly *not* M2's** (passes through M2, enforced by neighbors):
- store permanence P0–P3/L12 and the J-couplings J0/J1★ (stores' `apply`+API; M5's composite boundary — ASN-0047);
- frontier/address and coverage-class computation (M3, M1/M7);
- register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected` if unmet);
- the request lifecycle and ack-to-client (M10);
- multi-*transaction* batch atomicity (above the substrate, A5);
- durability *as a requirement* (not a MIC clause — `Durability::None` is faithful);
- **footprint confinement of `f`** — a *caller* obligation under merge-at-install/CAS: `f`'s entire committed-state **read set** — every value consulted to decide what to stage, whether to reject, or which branch to take, not just the staged records' values — must lie under its held `keys` or be append-only-monotone (§8). M2 *relies* on it for the conflict-free re-fold but **cannot itself check it**; violated, it corrupts silently under concurrency. Enforced by the stores, by contract, not by M2's mechanism.

## Dependencies & seams

**Upstream: none.** M2 is a foundation (it carries no edge to M1 — keys and payloads are opaque, ordering of keys is plain bytewise, not tumbler order). Its only dependencies are crates: `im`, `arc_swap`, `serde`, `parking_lot`/`dashmap`, a CRC32C lib.

**Composition seam (dependency-inverted).** The engine crate defines `World` (composing all store slices) and `Record` (the enum union of every store's record-types), implements `WorldState` for `World` by dispatching `apply` to the owning store's logic, and instantiates `Kernel<World>`. "Stores register record-types" = contribute `Record` variants + `apply` arms; "index-rebuilders" = **mandatory** incremental hint maintenance inside `apply` (it runs on every live commit and every replay step — a hint not folded here is stale after every write), plus, optionally, `World::rebuild_derived` to seed hints the checkpoint skip-serialized (it runs once at load, before replay, never on a live commit, so it cannot keep a hint current on its own). Two hard contracts on store code: **(1)** stage only authoritative deltas, maintain hints in `apply`; **never journal a hint**. **(2)** under the per-key-concurrent/CAS realizations, **footprint confinement** — `f`'s entire committed-state **read set** (every value consulted to decide what to stage, whether to reject, or which branch to take — not only the staged records' values) must lie under the state the txn's `keys` cover, or be append-only-monotone. Because merge-at-install re-folds the decided records without re-running `f`, a read outside the held keys commits a stale decision at a non-serializable position. A store honoring (2) migrates single-applier → concurrent transparently; one that reads or writes outside its keys is correct under the single applier but corrupts silently under merge-at-install. M2 cannot check (2); it is the store's contract.

**Downstream seams (what neighbors code against):**
- **M3 allocation** (frontier under H0): `let (addr, _seq) = kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.base(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })?`. M3 supplies the key bytes (1-byte space tag + tumbler bytes) and does all address math; M2 only locks + commits. The frontier read is confined to `key(home,subspace)`, satisfying footprint confinement (it is the only committed-state read `f`'s decision depends on).
- **M5 placement composite** (INSERT/COPY/VERSION): one `transact([key(d, s_C)], …)` staging K.α + K.μ⁺ + K.ρ, returning `(_, last_seq)`; M5 checks S3★ on `stg.working()` and the J-couplings at the boundary; M2 commits atomically. CREATENEWDOCUMENT (M3) is one `transact` registering the entity (returning its `Seq`) — it does *not* materialize an arrangement (M5 keeps that lazy).
- **M7 idem=⊤ emit**: `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })` → `(outcome, seq)`. The class_key serializes same-class emits (clause 7); the alloc key serializes same-home allocation (clause 2); the active-in-class read on which the hit/miss decision turns is confined to the held `class_key` (footprint-confined). Nullify hit-branch = a `transact` that stages nothing (zero-step), returning `(Hit, base.seq())`. The spanfilade is M7's hint, maintained incrementally in `apply` (mandatory — never journaled) and seeded by `rebuild_derived` only if the checkpoint skip-serialized it.
- **M6/M8/M9 readers & verdicts**: `let s = kernel.snapshot();` then read every constituent off `s` (clause 6). M9 reports quiescence as "as of `s.seq()`" (V1 retrospective). For its *writes* (rule fires), M9 takes the fire's index from the `Seq` that `transact` returns — exact even under per-key concurrency, unlike a post-hoc `current_seq()`.
- **M10**: opens/commits each operation's transaction via `transact`, receiving `(result, last_seq)`; acknowledges to the external client only after it returns (commit-before-ack), may report `last_seq`, and surfaces `TxnError::Rejected(E)` as a typed rejection (never a silent skip).

## Conflicts resolved

**1. Composite atomicity (ASN-0047) vs "batches are not atomic" (ASN-0134 A5).** The two speak of different units. M2's atomic unit is the **transaction** (one `transact`) — externally none-or-all. ASN-0047's "observable intermediate states" of a composite are precisely `Staging.working`, visible *only to the executing closure* for intra-composite precondition checks, never to external readers. ASN-0134's "batches not atomic" refers to a sequence of *separate* operations (`retract_stale`, a rule firing) whose partial visibility is intended; M2 deliberately does **not** bundle those into one transaction. The **content run** (one `K.α` per atom) is the boundary case ASN-0134 A5 explicitly classes as a non-atomic batch — and M2 may commit it *either* way, the builder's call (ASN-0134 decision #7): as **one atomic `transact([key(d,s_C)], …)`** (the held key delivers W2, the single install over-satisfies clause 5 — no reader lands mid-run), or, when reader-visible mid-run partial visibility is wanted, as **`critical_section` + separate per-atom commits** (clause-5-faithful, available only under the concurrent realizations, §4). So: M2 delivers transaction (composite) atomicity; multi-transaction batch atomicity is the caller's, "above the substrate"; and the content run sits on the seam, committable either as one atomic unit (over-satisfaction) or as a held-key sequence of commits (faithful clause 5).

**2. Single global writer (ASN-0047) vs per-home serialization suffices (ASN-0134 G1).** The **contract** is the weaker one — per-key serialization (clause 2). The recommended **first implementation** is a single applier (ASN-0047), which over-satisfies it. Because `transact(keys, …)` is identical for both, the migration single-applier → per-key-concurrent (merge-at-install) changes no caller's *call shape* — but it is transparent **iff every store confines its entire committed-state read set — every value `f` consults to decide what to stage, whether to reject, or which branch to take, not just its staged records' values — to its held keys** (modulo append-only-monotone reads), ASN-0134 G1's full commutativity hypothesis (neither reads nor writes shared state) raised to a seam contract (§8 / Dependencies & seams). A store written against the single applier that reads or writes state *outside* its keys compiles and runs correctly there but corrupts silently under merge-at-install; and because "build single-applier first" authors stores *before* this discipline would otherwise bite, the contract must be stated up front. ASN-0047's single-writer is one conservative realization of ASN-0134's contract, not a competing requirement.

**3. Visible-after-durable (ASN-0047) vs durability-orthogonal (ASN-0134).** ASN-0047 says make a composite visible only after its batch is durably committed — natural in its single-threaded model, where *visible* == *acked*. ASN-0134 treats durability as orthogonal (not a MIC clause; `Durability::None` is faithful) and takes *visible* == *committed*. M2 resolves this by making **durable-before-visible the canonical ordering** (§1/§3): install follows the marker barrier, so an external M10-acked read never reflects a state a crash can roll back, and `TxnError::Durability` is a sound true no-op. The **visible-before-durable** variant (install-then-fsync) is offered as a throughput option taking ASN-0134's weaker stance: prefix-closure keeps it safe for *internal* causal dependence, but an external read acked during the not-yet-durable window can be rolled back by a crash, and a barrier failure must poison the kernel rather than no-op (the install is already visible). The conflict is thus resolved by canon (ASN-0047), with the ASN-0134 reading available as a documented, caveated knob — not left merely open.

**Boundary clarifications (territory that *looks* like M2's but is a neighbor's, resolved by the decomposition's dependency inversion):** the frontier discipline ASN-0134 reasons about (H0) is M3's *allocator*; M2 owns only its *serialization*. The request/response path and pipelining-vs-sequential client model (G0) are re-homed to M10; M2 keeps only the commit-gate mechanism. Neither is a conflict — both are M2 honoring its seam by *not* doing the neighbor's job.

## Open build decisions

- **Concurrency mechanism** — single applier (recommended first) → per-key concurrent with merge-at-install (scaling path; binds the footprint-confinement read-set contract) → optimistic-CAS (only under measured low same-key contention; retry termination unresolved, OQ1/OQ3). Pick by throughput need; the API doesn't change.
- **Durability/visibility ordering** — **durable-before-visible (canonical: append records+marker → barrier → install; under group commit `base` is drawn from the applier's working tip and the batch's final tip is published once, post-barrier; a `Durability` failure is a sound no-op via truncate + Seq rollback)** vs the visible-before-durable throughput variant (install-then-batched-fsync; needs no working tip; prefix-closure keeps internal dependence safe, but an external M10-acked read can reflect a rolled-back state, and a barrier failure must poison rather than no-op — §1, Conflicts #3). Group commit amortizes the barrier under either.
- **Burned-Seq policy on durability failure** — roll the `Seq` high-water back to the last committed marker (keeps the order gap-free; recommended) vs tolerate the gap (relaxes the invariant to monotone-only) (§1).
- **Durability mode** — `Fsync` per commit vs `FsyncBatch{window}` (group commit) vs `None` (in-memory, MIC-faithful, for tests/embedding).
- **Checkpoint cadence & representation** — every-N-commits / time / journal-size; full-`World` serialize vs per-store/incremental; serialize hints vs `#[serde(skip)]` + `rebuild_derived` (checkpoint size vs recovery recompute). The recovery-time-vs-overhead knob ASN-0047/0134 leave open. (The `≤ S` / `> S` checkpoint-vs-replay boundary itself is *fixed*, not a knob — §6/§7.)
- **Lock-table layout** — striped `Vec<Mutex>` (bounded, false contention) vs per-key `DashMap` (no false contention, entry GC).
- **Journal framing** — CRC algorithm, segment rotation, max frame size, fsync-of-dir on rotate.
- **Whether to build `critical_section` at all** — default to issuing every run as one `transact` (atomic, delivers W2 via the held key, over-satisfies clause 5); build the held-across-commits guard only if a run is genuinely too large to commit atomically or needs intended mid-run reader visibility — and only under the per-key-concurrent/CAS realizations, since under the single applier it provides no run-exclusion (§3/§4).
- **Record/key encoding** — `Record` as one serde enum (recommended for a single binary, compile-time dispatch) vs a runtime type-id registry of boxed appliers; `LockKey` as `Vec<u8>` vs `SmallVec`/`Box<[u8]>` vs a fixed-width digest.
