# M2 — Transaction, Journal & Concurrency Kernel — Detailed Design

## Purpose & boundary

M2 is the engine's **generic transactional substrate**: it turns every state change into one atomic, totally-ordered, durable, recoverable step (or a composite committed as one), serves consistent snapshots of committed state, and serializes same-key writers — *knowing nothing about what any change means*. It is a WAL + atomic-install + keyed-serialization + snapshot engine that the stores plug into, dependency-inverted: M2 defines the fold (`WorldState::apply`), the engine implements it, and M2 only calls down through that trait. **One thing well: make the spec's single sequential, atomic-step order real and durable for a plural, concurrent world — over an opaque payload and opaque keys.**

It does **not**: compute addresses, frontiers, or coverage-classes (M1/M3/M7 supply keys and do the math — M2 has no address algebra); enforce store permanence P0–P3 or the J-couplings (the stores enforce those at their composite boundaries *through* M2, never by it — see ASN-0047); interpret record semantics; own the request lifecycle, the parse/dispatch table, or the acknowledgment-to-client (M10 — M2 keeps only the commit-gate *mechanism*); own derived hints (the stores do; M2 journals only authoritative deltas); or provide atomicity for *multi-step* (`m ≥ 2`) batches such as `retract_stale` or a multi-step rule firing (deliberately partial-visible per ASN-0134 A5 — "above the substrate"). A *single-step* (`m = 1`) fire, by contrast, **is** one atomic `transact` — indivisible by A0, exactly the "atomic fires" M9 leans on — so only `m ≥ 2` fires are the A5 batches left above the substrate.

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
    ///
    /// CONSISTENCY OBLIGATION: an override MUST seed exactly the hint state that folding
    /// every record with Seq ≤ S through `apply` would produce (S = the loaded checkpoint's
    /// seq). Recovery runs `rebuild_derived` (to seed hints for Seq ≤ S) THEN replays
    /// Seq > S through `apply`; if this seed disagrees with the `apply`-fold of the ≤ S
    /// prefix it stands in for, the recovered hint diverges from the live-maintained one
    /// and reads go wrong. The two hint-maintenance paths must produce identical hints.
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
                          // →_sh records is order-isomorphic to 𝔼, so a →_sh record's Seq
                          // corresponds POSITIONALLY to its idx(σ) — it is NOT equal to it (the
                          // counter has also advanced on the interleaved non-→_sh records). M2's
                          // full Seq order is a finer total order (§2). No caller derives idx(σ)
                          // from Seq.
```

**Config & errors** — the knobs the Open-build-decisions section selects; carried on `KernelCfg`.

```rust
pub struct KernelCfg {
    pub journal_path: PathBuf,        // directory for journal segments + checkpoints (Durability::None ignores it)
    pub concurrency: Concurrency,     // SingleApplier (default) | PerKeyMerge | OptimisticCas — API-invariant, but
                                      //   COUPLED to `visibility`: PerKeyMerge/OptimisticCas are necessarily
                                      //   visible-before-durable; DurableBeforeVisible requires SingleApplier (§1/§8)
    pub durability: Durability,       // Fsync | FsyncBatch{window,max_delay} | None
    pub visibility: Visibility,       // DurableBeforeVisible (canonical; SingleApplier ONLY) | VisibleBeforeDurable
                                      //   (the only ordering under PerKeyMerge/OptimisticCas) (§1/§8)
    pub burned_seq: BurnedSeqPolicy,  // Rollback (gap-free, default) | TolerateGap (monotone-only) (§1)
    pub checkpoint: CheckpointPolicy, // EveryN(u64) | Interval(Duration) | JournalBytes(u64) | Manual (§6)
    pub locks: LockLayout,            // Striped{stripes} | PerKey — unused under SingleApplier (§4)
}
pub enum Concurrency { SingleApplier, PerKeyMerge, OptimisticCas }
pub enum Durability  { Fsync, FsyncBatch { window: usize, max_delay: Duration }, None }  // batch closes on
                          // window-fill OR max_delay, whichever fires first (a window-only trigger would stall a
                          // low-traffic batch — and any zero-step op waiting on its barrier — indefinitely, §1);
                          // flush() forces an immediate close.
pub enum Visibility  { DurableBeforeVisible, VisibleBeforeDurable }
pub enum BurnedSeqPolicy { Rollback, TolerateGap }
pub enum CheckpointPolicy { EveryN(u64), Interval(Duration), JournalBytes(u64), Manual }
pub enum LockLayout  { Striped { stripes: usize }, PerKey }

pub enum OpenError {
    Io(io::Error),
    BadCheckpoint,           // checkpoint file unreadable / failed its checksum → fall back to an earlier one or genesis
    Corruption { at: Seq },  // CRC failure BEFORE the committed tip (in the committed prefix) — durable
                             // acked data is corrupt; halt, never drop (§7)
}
pub enum CheckpointError { Io(io::Error), Serialize }
```

**Lifecycle**

```rust
impl<W: WorldState> Kernel<W> {
    /// Recover (latest checkpoint @s → rebuild_derived → replay committed records with
    /// `Seq > s`) or init from `genesis` (= Σ₀, with s = 0).
    pub fn open(cfg: KernelCfg, genesis: W) -> Result<Self, OpenError>;
    /// Persist a checkpoint embodying all records with `Seq ≤ s` and reclaim journal space
    /// (segment-granular — §6); recovery then replays exactly `Seq > s`. Non-blocking to
    /// writers. Cadence is the caller's policy. Returns the checkpointed seq `s`.
    pub fn checkpoint(&self) -> Result<Seq, CheckpointError>;
    /// Drain pending (group-commit) durability barriers; the manual group-commit close
    /// trigger; used at shutdown/checkpoint.
    pub fn flush(&self) -> Result<(), io::Error>;
}
```

**Reads (snapshots)** — discharge MIC clauses 4 & 6.

```rust
/// A pinned, consistent view of one committed state. A NEWTYPE over the loaded root Arc —
/// NOT a bare `Arc<Committed<W>>`, so it can carry the inherent seq()/world() below (the
/// orphan rule forbids an inherent impl on a foreign `Arc`). `Committed` is M2-internal
/// (§Core data model); the field is private.
pub struct Snapshot<W: WorldState>(Arc<Committed<W>>);

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
    /// evaluated against (V1). UNDER GROUP COMMIT a zero-step op whose `base` is the
    /// not-yet-durable working tip first WAITS for the barrier covering `base.seq()`
    /// before returning: it journals nothing, but must not acknowledge a value read off a
    /// state a batch rollback could erase (e.g. an idem-hit deduplicated against a still
    /// in-flight batched incumbent — §1/§3). Under per-commit fsync `base` is already
    /// durable, so no wait.
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
    Durability(io::Error),  // durable-before-visible (SingleApplier) only: a barrier failed BEFORE
                            // install AND the txn's un-acked tail was durably truncated, so
                            // nothing was installed and no failed marker survives → a TRUE no-op;
                            // caller may safely re-invoke. If the truncation ITSELF fails to
                            // complete durably the kernel POISONS instead (a surviving failed
                            // marker + the reused burned Seqs would corrupt — §1), never returning
                            // this as a safe no-op. Under visible-before-durable — the optional
                            // single-applier variant AND the necessary ordering of PerKeyMerge/
                            // OptimisticCas (§8) — a barrier failure instead POISONS (§1): the txn is
                            // already installed and cannot be unwound, so this is never returned there.
    Conflict,               // optimistic-CAS impl ONLY: the root moved between read and install, and
                            // the staged records can be neither re-folded (they would collide on the
                            // moved frontier) nor produced by re-running f (FnOnce) — so the CALLER
                            // re-invokes with a fresh closure. Never under single-applier; never under
                            // merge-install, whose held keys pin the frontier so it re-folds the
                            // already-staged records WITHOUT re-running f.
}
```

**Serialization (held-across-commits variant)** — the explicit clause-5 path when a run must be *separately* committed rather than one transaction (rarely needed; `transact`'s `keys` covers the atomic case).

```rust
impl<W: WorldState> Kernel<W> {
    /// Hold `keys` until the guard drops, issuing inner `transact(&[], f)` calls between
    /// which readers may land (clause 5, reader-visible mid-run). Available ONLY under the
    /// per-key-concurrent and CAS realizations, where the lock table is live and `transact`
    /// honors keys.
    ///
    /// PANICS under `Concurrency::SingleApplier`: there the lock table is unused and the
    /// applier lock is released between the inner commits, so a foreign same-key `transact`
    /// could commit between them and fragment the run — the guard would silently provide NO
    /// run-exclusion. Rather than hand back a do-nothing guard, this method panics under the
    /// single applier; a single-applier run MUST instead be one `transact([keys], f)`
    /// (atomic, over-satisfying clause 5). Prefer the one-`transact` form regardless.
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
| **Working tip** | `Committed<W>` held by the applier across a group-commit batch | volatile (internal to the applier; never externally visible; rebuilt fresh on recovery) | lets a batched txn read its predecessors' not-yet-published records (correct dependent reads); published to **Root** *once*, post-barrier (§1) — **single-applier durable-before-visible only; per-key/CAS install before the barrier and need no tip (§8)** |
| **Checkpoint** | serialized `W` @ `Seq` on disk (temp→fsync→rename) | recoverable cache (a prefix-fold) | bounds replay time; optional; safe to delete |
| **Lock table** | striped `Vec<parking_lot::Mutex<()>>` *or* `DashMap<LockKey, …>` | volatile (locks don't outlive a crash; recovery is single-threaded) | the keyed critical section (clauses 2/5/7) |
| **Sequencer** | `Seq` high-water + the install serialization point (a `Mutex` or actor mailbox) | volatile, recovered as `max committed Seq` | assigns the total order; serializes journal-append + install |

`W` is the engine's composition of all store slices, each an `im` persistent collection (`OrdMap` for address-keyed stores — gives prefix-range scans free — `HashMap`/`Vector` elsewhere). `W: Clone` is O(1) (Arc bumps); `W::apply` returns a structurally-shared successor touching only changed paths. This is the ASN-0134-recommended persistent-immutable representation: the root's identity *is* the version coordinate, making clauses 1/4/6 nearly free.

`Snapshot<W>` is the newtype `Snapshot<W>(Arc<Committed<W>>)` (not a bare `Arc`, so it can carry the inherent `seq()`/`world()` the orphan rule would forbid on `Arc` — §Public interface) — a cheap, pinned, consistent view carrying its own `seq` (so verdicts can be reported as retrospective statements about `Σ_r`, V1).

## Internal design

### 1. The journal & WAL discipline

**Frames.** `[u32 len][u32 crc][payload]`, where `crc` covers **both the `len` field and the `payload`** (so a corrupt length is *detected* rather than silently mis-delimiting the following frame — the recovery scan §7 relies on this to resynchronize past a bad frame). Payload is `LogRecord{ seq, txn, bytes }` (where `bytes` is the serialized `W::Record` — the frame struct is named `LogRecord` so it does not collide with the trait's `W::Record` enum) or `Marker{ txn, last_seq, frame_checksum }`. **The marker is the recovery contract** (ASN-0047): a txn is committed iff its marker is *durable* and its `frame_checksum` validates over the txn's records; record frames past the last valid marker are a torn tail — discarded and truncated.

**Canonical commit ordering: durable-before-visible.** A txn commits in this order — *append records → append marker (terminal frame) → durability barrier → install the root → return `(v, last_seq)`*. Two properties this buys, both load-bearing for sound failure handling:

- **The marker is made durable only as the last step of its *own* commit.** A txn is committed exactly when *its own* marker reaches disk; nothing else may promote it. This closes the **phantom-commit hole**: were the marker merely *appended* before the barrier and left in the file, a later txn's fsync could flush a failed txn's marker, and recovery would replay an operation reported as failed — and, for a same-`(d,S)` allocation, the retried successor (computed against a root without the failed txn) would double-deposit a *colliding* address. The fix is to **truncate the un-acked tail on barrier failure** (below), so a failed marker is physically gone before any later fsync runs.
- **Barrier failure is a true no-op — *conditional on the un-acked-tail truncation succeeding*.** If the durability barrier fails, the txn's record+marker frames are truncated (durably) from the journal tail and the root is *not* installed — so no durable marker survives (recovery omits it) and no in-memory state reflects it. `transact` returns `TxnError::Durability` and the caller may safely re-invoke. The Seqs the txn had been assigned are **burned**; the serializer rolls the `Seq` high-water back to the last committed marker's `last_seq` before releasing, preserving the gap-free invariant. (The alternative — *tolerate* the gap, relaxing the invariant to monotone-only — is an open knob.) **This no-op guarantee is load-bearing on the truncation *itself* completing durably.** The Seq-rollback hands the burned Seqs to the *next* txn to reuse, so if the truncation (or its fsync) fails, two things go wrong at once: the failed records+marker survive on disk (a later fsync can flush them and recovery replays a reported-failed op — the very phantom-commit hole this ordering exists to close), *and* a later txn writes the *same* burned Seqs (a journal Seq-collision, and for a same-`(d,S)` allocation a colliding address). Both are the exact corruption the durable-before-visible ordering is built to prevent. Therefore: **if the un-acked-tail truncation fails to durably complete, the kernel must poison (halt; subsequent calls fail), *not* return `TxnError::Durability` as a safe no-op.** (The poison applies regardless of burned-Seq policy: even under `TolerateGap`, where the next txn does not reuse the burned Seqs, a surviving failed marker would still replay as a phantom commit.)

**Group commit (the throughput realization of the canonical order).** `FsyncBatch{window, max_delay}` amortizes the barrier across a batch, closing it on whichever of *window-fill* or *max_delay* fires first — a window-only trigger would stall a low-traffic batch (and any zero-step op waiting on its barrier, below) indefinitely, so the timeout is mandatory; `flush()` forces an immediate close. Because install must stay *after* durability, no `ArcSwap` root update happens until the batch's barrier — yet a batched txn must still read the state its predecessor left: a COPY pipelined after an INSERT into the same document must see the inserted content, and an allocation must read the frontier its predecessor advanced (H0). The applier therefore threads an **in-memory working tip** — a `Committed<W>` it advances with each batched txn's staged records — and draws each batched txn's `base` from that tip rather than from `root.load()`. So: under the serializer, for each batched txn append its record+marker frames and advance the tip; then *one* durability barrier; then publish the batch's **final tip** to the root in a single atomic install performed by the batch **leader**; each `transact` returns only after *its* batch's barrier. A barrier failure aborts the batch's un-acked tail (truncate + Seq rollback, **or poison if that truncation fails** — see above) and resets the tip to the last durable state, so no partial marker survives and the root never reflected the aborted work. Install stays *after* durability — external readers never see pre-durable state; the working tip is internal to the applier and never externally visible. A **zero-step op** (idem-hit, nullify-hit, or read) that decides off the working tip is the one path that journals nothing yet still acknowledges a value read from the tip: it must therefore *also* wait for the barrier covering its `base.seq()` before returning, because acking an idem-hit deduplicated against a still-in-flight batched incumbent — one a barrier failure would roll back — is exactly the not-yet-durable external-read window the canonical ordering forbids (§3); reading the durable *root* instead is no fix (it would miss the batched predecessor and double-deposit, breaking clause 7), so the zero-step op reads off the tip but waits for its durability. Under per-commit fsync `base` is the durable root, so no such wait arises. (The dependent-*write* bug — a batched dependent txn reading a stale pre-batch root yet landing at a higher `Seq` — is specific to *this* canonical default combined with group commit, and the working tip is its fix; the zero-step wait is its read-side companion.)

**Only authoritative deltas are journaled.** Derived hints are *never* journaled — they are reconstructed by `apply` during replay (mandatory incremental maintenance — §6/§7), and seeded once at load by `rebuild_derived` if the checkpoint skip-serialized them. This is the structural answer to ASN-0134's divergence hazard (OQ10): one logical step is exactly one journal record driving one `apply`, so there is nothing to diverge.

`Durability::{ Fsync, FsyncBatch{window, max_delay}, None }`. `None` is the fully in-memory realization — **MIC-faithful** (ASN-0134 is silent on durability), no journal, no recovery, atomicity/isolation intact.

**Optional variant: visible-before-durable (install-then-fsync).** Install the root *before* the batched barrier, returning only once durable. This is a throughput choice (install latency off the fsync's critical path), justified for *internal* causal dependence by prefix-closure: anything causally dependent on txn T is journaled after T, so "R durable ⟹ T durable," and a reader/writer that acts on a not-yet-durable T either commits (making T durable by prefix) or leaves no persistent effect. **But the install is already visible when the barrier runs, so its failure cannot be a no-op** — readers/writers may already have built on it; the only sound response is to **poison the kernel** (halt; subsequent calls fail), not return `TxnError::Durability`. And prefix-closure does *not* cover an **external read acked by M10**: a client can be told a read result reflecting a committed-but-not-yet-durable state that a crash then rolls back (the resolved ASN-0047/0134 conflict — see *Conflicts resolved*). Choose this variant only when that external-read window is acceptable. (Because it installs the root *before* the barrier, each txn's `base ← root.load()` already reflects its predecessors even under group commit — so this variant needs **no working tip**; the working-tip mechanism above is specific to durable-before-visible under group commit, which is a **single-applier** ordering. The per-key-concurrent and CAS realizations (§8) likewise install before the barrier and so are *themselves necessarily* visible-before-durable — they too need no working tip, and choosing them for throughput adopts this external-read-rollback window not as an option but as a consequence.)

### 2. Sequencer & the linearization point

Each committed record receives the next `Seq` from a monotone counter, assigned inside the serialization point so the order is gap-free and a composite's records are **Seq-contiguous** (no foreign record interleaves a composite). **`Seq` refines ASN-0134's `idx(σ)`, it is not identical to it:** every `→_sh` step (`K.σ`/`K.α`/`K.λ_sh`) receives a `Seq`, but so do the non-`→_sh` records a composite stages (`K.μ⁺`/`K.μ⁻`/`K.ρ`); the subsequence of `Seq`s carrying `→_sh` records is order-isomorphic to `𝔼`, so a `→_sh` record's `Seq` *corresponds positionally* to its `idx(σ)` — it is **not equal** to it (the counter has also advanced on the interleaved non-`→_sh` records), while M2's full `Seq` order is a finer total order; no caller derives `idx(σ)` from `Seq`. A `→_sh` record's `Seq` assignment is its linearization point (A2); one `transact` = one operation = one linearization point (single-step op) or one contiguous composite boundary. M2 fixes it; M10 merely chooses to call `transact` once per operation. Seq-contiguity is a property of M2's *internal* order; it is *not* what delivers W2 chain contiguity — that comes from holding `key(d,s_C)` across the run (§4).

### 3. The transaction / composite boundary

`transact(keys, f)` — recommended single-applier flow, canonical durable-before-visible:

```
acquire keys in resolved-lock order                    // clauses 2/5/7; §4. PerKey: sort+dedup
  (PerKey: bytewise KEYS; Striped: STRIPE INDICES)     //   keys bytewise. Striped: resolve each
                                                        //   key→stripe, then sort+dedup the indices.
                                                        //   no-op under SingleApplier (table unused).
lock the applier (single global serializer)
base ← tip.load()                              // the working tip: == root for per-commit fsync or a
                                               //   batch's FIRST member; == predecessors' fold within
                                               //   a batch (§1) — so a batched COPY reads its INSERT
stg  ← Staging::new(base)
match f(&mut stg) {                            // store logic: reads stg.base()/working(), pushes records
    Err(e)              → return Rejected(e)            // clean rejection; nothing journaled/installed
    Ok(v) if stg empty  →                              // zero-step (A1); V1 referent = base.seq()
        if base is the not-yet-durable working tip:    //   (group commit only)
            await the barrier that makes base.seq() durable   // join the batch's barrier; journals
                                                              //   nothing, but must not ack a read off
                                                              //   rollback-able state — e.g. idem-hit (§1)
        return Ok((v, base.seq()))                     // per-commit fsync: base==durable root, no wait
    Ok(v) ⇒
        seqs ← alloc_seqs(stg.records.len())            // linearization (burned & rolled back on failure)
        journal.append_records(txn, seqs, stg.records)  // PER-TXN
        journal.append_marker(txn, last_seq, checksum)  // PER-TXN — the commit marker, terminal frame
        tip.advance(Committed{ last_seq, stg.working }) // PER-TXN — advance the in-memory working tip

        durability.barrier()                            // PER-COMMIT fsync: here, per-txn.
                                                        // GROUP COMMIT: LEADER-ONLY, once at batch close,
                                                        //   covering every batched txn's frames.
            on Err →                                    // sound failure path (§1):
                if journal.truncate(seqs) durably succeeds:
                    rollback_seq_hi; tip.reset_to_last_durable; return Durability   // TRUE no-op
                else:
                    poison_kernel()                     //   truncation failed → failed marker survives +
                                                        //   Seqs would be reused → corruption; HALT (§1)

        root.store(tip.load())                          // ATOMIC INSTALL — AFTER durability.
                                                        // PER-COMMIT fsync: per-txn.
                                                        // GROUP COMMIT: LEADER-ONLY — publishes the batch's
                                                        //   FINAL tip ONCE; non-leader txns do NOT install.
        return Ok((v, last_seq))                         // commit-before-acknowledge (each txn returns only
                                                        //   after ITS batch's barrier)
}
```

`base` is the applier's **working tip** (§1): under per-commit fsync it equals the current root and for a group-commit batch's *first* member likewise, but within a batch it is the fold of the batch's earlier txns, so a batched txn reads its predecessors' staged records (a batched COPY sees the INSERT it follows; a batched allocation reads the frontier H0 its predecessor advanced). The root — external readers' view — advances only at batch close, after durability, and **only the batch leader installs it**: the per-txn `root.store` shown collapses to a single leader-only install under group commit, and a builder must not install per-txn.

`Staging.working` (= `base` folded with staged records, cheap over persistent `W`) is what lets the store check **intra-composite preconditions** at intermediate states (ASN-0047's "observable intermediate states," e.g. S3★ referential integrity after K.α but before K.μ⁺). Those intermediates are visible only to the executing closure — **never to external readers**, who see only the single atomic install. The J-couplings the closure may check at the boundary (`base`→`working`) are M5's to assert; M2 never does.

The barrier shown is the canonical per-txn durable-before-visible commit; group commit (§1) amortizes it across a batch and publishes the batch's final working tip after its barrier (the leader performing the one install). Either way **install follows durability**, so `TxnError::Durability` is a sound true no-op — *provided the un-acked-tail truncation completes durably; if it does not, the kernel poisons rather than no-ops* (§1). The optional visible-before-durable variant (§1) — and, necessarily, the per-key-concurrent and CAS realizations (§8) — move the install above the barrier and convert a barrier failure into a kernel poison.

### 4. Keyed critical sections

One mechanism serves clauses 2, 5, 7; the key is always caller-supplied bytes. `transact` acquires `keys` before taking its snapshot and holds them through commit, so **read-decide-deposit is atomic for those keys** — exactly what clause 7's idem dedup needs (the dedup-read of the global active set and the deposit are one action under the coverage-class key; cf. G2) and what clause 2 needs (frontier-read-and-deposit under the `(home,subspace)` key — M3 does the `inc(max,·)` math; M2 only locks).

**Acquisition is deadlock-free by acquiring the *resolved lock objects* in a canonical order — and that order is layout-dependent.** Under `LockLayout::PerKey` (one mutex per distinct key) sort + dedup the **keys** bytewise. Under `LockLayout::Striped{stripes}` sort + dedup is over the **stripe indices**, not the keys: resolve each key to its stripe index *first*, then sort and dedup *those*. Sorting/deduping by key under `Striped` is wrong on two counts — two *distinct* keys may hash to one stripe (a key-dedup would then double-acquire one non-reentrant `Mutex` → self-deadlock), and bytewise key order ≠ stripe-index order (two txns could acquire the same two stripes in opposite orders → classic deadlock). This is reachable via the documented two-key M7 emit (`[class_key, key(home, s_L)]`) under `PerKeyMerge`/`OptimisticCas`, so the stripe-index ordering is mandatory there. The bug cannot fire under `SingleApplier`, where the table is unused.

**Run contiguity (W2) is delivered by the held key, not by Seq order.** Staging a multi-atom content run inside one `transact([key(d,s_C)], …)` holds `key(d,s_C)` across every atom, so no foreign `s_C`-allocation to `d` interleaves between the run's first and last atom — *that* is W2 (chain/address contiguity). The single atomic install then *additionally* makes the run atomic-to-readers, over-satisfying clause 5 (no reader lands mid-run at all). Seq-contiguity (§2) is a distinct, internal property and is not the source of W2.

`critical_section` is the rarer guard that holds `keys` across *separate* inner commits — the modeled clause-5 path where readers *may* land mid-run. **It is available only under the per-key-concurrent and CAS realizations**, where the lock table is live and `transact` honors keys. Under the single applier the lock table is **unused** (the global applier lock subsumes every key, and is released between the section's inner commits), so a foreign `transact([key(d,s_C)], …)` — whose key is a no-op there — could commit between the inner commits and fragment the run; the guard would therefore provide **no run-exclusion under the single applier**. So that a builder cannot silently get a fragmented run, **`critical_section` panics when called under `SingleApplier`** rather than handing back a do-nothing guard. A single-applier run must instead be **one `transact([keys], …)`** (atomic, satisfying clause 5 by over-satisfaction); the reader-visible-mid-run flavor of clause 5 is simply unavailable under the single applier, whose runs are atomic.

Lock table: striped `Vec<Mutex>` (bounded memory, possible false contention) or per-key map (no false contention, needs entry GC) — an open decision that *also* sets the acquisition order above (`Striped` → order by stripe index; `PerKey` → order by key). Under the single-applier impl the table is unused; under per-key concurrency it is live and also backs `critical_section`. The `transact`/`snapshot` API is identical across realizations, so moving single-applier → per-key concurrency changes no caller's *call shape* — though it does newly *bind* the footprint-confinement contract on `f` (§8 / Dependencies & seams).

### 5. Snapshot reads

`snapshot()` is one lock-free `ArcSwap::load` → a pinned `Committed<W>` wrapped in the `Snapshot<W>` newtype. Per-call single-state (clause 4 / A3 / V0) is by construction. A multi-read verdict reads all `p` constituents off **one** `Snapshot` → clause 6 / V2 for free (persistent state dissolves the "global" cost ASN-0134 flags). This is the seam contract on M6/M8/M9: thread one `Snapshot` through every constituent of a verdict; do not issue them as separate `snapshot()` calls (the §8 pathology).

### 6. Checkpoint & truncation

Non-blocking: grab a `Snapshot` `Committed{ seq: S, world }` (lock-free) — `world` is the fold of **exactly the records with `Seq ≤ S`**, and `S` is always a committed marker boundary (installs are atomic at commit). Serialize `world()` (authoritative; hints may `#[serde(skip)]`) to `checkpoint.tmp`, fsync, atomic-rename to `checkpoint.<S>`, fsync dir, then **reclaim journal space by dropping whole journal segments all of whose frames have `Seq ≤ S`** — *segment-granular* truncation, not an exact per-frame guarantee: a segment that *straddles* `S` is kept whole, so some `Seq ≤ S` frames may survive on disk. Truncation is therefore a space-reclamation optimization, **not** a correctness mechanism; correctness rests entirely on recovery (§7) replaying **exactly `Seq > S`** — its `Seq > S` filter discards any surviving `≤ S` frames. The checkpoint @S thus *embodies* `Seq ≤ S`, and recovery replays *exactly the complement* `Seq > S` — no overlap, no gap. This complementarity, enforced by that filter over a coarse segment-granular truncation, is essential because `apply` is **not** idempotent (a `Vector`-append record double-applies wrongly): every committed record must be folded into the recovered state exactly once. Writers run throughout — the snapshot's Arc keeps the checkpointed version alive while live installs advance the root. Crash mid-checkpoint leaves an ignored `.tmp` and an unreclaimed journal: always safe (the next recovery just replays more, the filter still bounding it to `Seq > S`). Cadence (every-N / time / size) and representation (full-World vs per-store/incremental) are open knobs.

### 7. Recovery

`open`: load the latest valid checkpoint `checkpoint.<S>` (else `genesis`, with `S = 0`), call **`rebuild_derived`** (seeds, from authoritative state, the hints the checkpoint skip-serialized; `apply` then keeps them current across replay — and a store's `rebuild_derived` override **must** seed exactly the `apply`-fold of the `Seq ≤ S` prefix it stands in for, or the recovered hint diverges from the live-maintained one, a trait contract — §Public interface, §Dependencies & seams), then replay the committed journal records, **filtering to `Seq > S`** (skipping any `Seq ≤ S` frames that survived §6's segment-granular space reclamation) and folding them via `apply` in `Seq` order — exactly the complement of what the checkpoint embodies (§6), no record applied twice or skipped. The `Seq > S` filter is load-bearing precisely because `apply` is non-idempotent: a surviving `≤ S` frame, replayed, would double-apply.

A txn is committed iff its marker is durable and validates (§1). Recovery **first scans the whole journal to locate the last frame that is a CRC-valid `Marker` whose `frame_checksum` validates over its txn's records — the *committed tip*** — and only then classifies failures by position. (Locating the tip requires scanning *past* any earlier bad frame; this is why the frame `crc` covers the `len` field as well as the payload (§1) — a corrupt length is detected rather than silently mis-delimiting, so the scan can resynchronize to later frames and markers.) **The discriminator for any frame failure is its position relative to that committed tip, and it cleanly separates the two cases an undifferentiated "CRC-failed frame → discard" rule would wrongly conflate.** A CRC failure (or an invalid/unvalidated marker) *at or after the committed tip* is the never-acked **torn tail** → discard + truncate: it was never acked, so loss is correct, and a failed-barrier txn's frames were already truncated at failure time (or the kernel poisoned), so no failed marker survives to replay. A CRC failure *in the committed prefix — strictly before the committed tip* — is corruption of durable **acked** data → **halt and report** (`OpenError::Corruption{ at }`); never silently drop it, because a silent discard would leave a `Seq` hole that — `apply` being non-idempotent and `Seq`-ordered — recovers a *wrong* state. `apply` determinism guarantees a clean replay reproduces the exact committed state (A6: every journal prefix up to a marker is a canonical reachable state). Recovery is single-threaded — the volatile lock table and `Seq` high-water are rebuilt fresh (the high-water as the committed tip's `last_seq`).

### 8. Concurrency realizations — the fault line

The `transact`/`snapshot` API is invariant across these; only internal locking — and, as a consequence, the durability-ordering — changes.

- **Single applier (recommended first; ASN-0047's choice).** `f` runs under the global applier lock. With per-commit fsync (or for a group-commit batch's *first* member) `base == current root`; under group commit `base` is the applier's **working tip** (§1/§3), so a later batch member reads its predecessors' staged records. The lock table is unused (keys are no-ops). This makes clauses **1, 2, 4, 5, 7 free**, leaving **clause 6** — which still needs the §5 one-`Snapshot` threading, since the §8 read-drift pathology arises even here, with no per-home concurrency — and the **clause-3** commit-gate ordering to be handled explicitly. Group commit (§1) batches the durability barrier across operations for throughput while keeping install after durability (durable-before-visible). **This is the *only* realization that can be durable-before-visible.** Bounded by one core. *Because `f` always sees the live tip here, a store written against the single applier may freely read state outside its `keys` — which is exactly why the footprint contract below does not bite until migration.*

- **Per-key concurrent with merge-at-install (scaling path; what ASN-0134 G1 blesses).** `f` runs outside the install lock holding only its `keys`; at commit, a short global install section assigns Seqs, re-folds `stg.records` over the *current* root **without re-running `f`**, journals, and **swaps the root** — the batched fsync then following *outside* the install section, with the txn returning only after that fsync (A7). Because the swap precedes the barrier, this realization is **necessarily visible-before-durable** (§1): it uses *no working tip*; in the window between a txn's install and its barrier an external M10-acked **reader** can reflect that committed-but-not-yet-durable state, which a crash rolls back; and a barrier failure **poisons** the kernel (the root is already installed and cannot be unwound) rather than returning a no-op `TxnError::Durability`. Durable-before-visible is **not** available here — it is the single-applier ordering (§1) — so the concurrency and durability-ordering decisions are **coupled**: adopting per-key for throughput adopts visible-before-durable semantics. This re-fold is conflict-free **only under a caller obligation** — *footprint confinement*: `f`'s **entire committed-state read set** — every value it consults to decide *what to stage, whether to reject, or which branch to take*, not merely the values it writes into staged records — must lie under state the txn's held `keys` cover, or be **monotone-safe**. Monotone-safety is *narrower* than "any read of an append-only structure": a *positive* membership test on an append-only set (`a ∈ dom(C)`, whose truth survives every append) is exempt, but a *negative* existence/freshness test (`a ∉ dom(C)`, a uniqueness probe) is **not** — a concurrent append can falsify it — and must be under held keys. The contract is on the *read set* because merge-at-install re-folds the already-decided records over the current root **without re-running `f`**: any unconfined read means a stale *decision* (which records, hit vs miss, reject, branch) commits at a non-serializable position. (Writes are confined by construction — a txn's staged records mutate only its held-key state and append fresh, disjoint entries — so the active obligation is the read set.) This is ASN-0134 G1's full commutativity hypothesis — neither *reads* nor writes state another txn touches — raised here to a **seam contract** (Dependencies & seams). Under it, the held keys guarantee no concurrent writer touched this txn's read-set (G1 commute) and the re-fold reproduces `f`'s decision. **Persistent state alone gives neither the write-concurrency nor the confinement:** root-install still contends (the held keys, not persistence, give concurrency), and a store that *reads* (unconfined) or writes state *outside* its keys compiles and runs correctly under the single applier but **corrupts silently** under merge-at-install. The example seams honor the contract (M3 holds `key(home,subspace)` across the frontier read; M7 holds `class_key` across the active-in-class read), which is why those migrate cleanly; *new* store ops must be checked against it — and since "build single-applier first" authors stores *before* the discipline would otherwise bite, the contract must be stated up front.

- **Optimistic frontier-CAS (optional).** No held locks; read fresh, compute, and attempt to CAS the root. The CAS *is* the install, so this realization is likewise **visible-before-durable** (the barrier follows the successful CAS; a barrier failure after a won CAS **poisons**, the root being already installed) — coupled to visible-before-durable semantics, never durable-before-visible. Because it holds no keys, the frontier may move under it between read and install — and crucially it **cannot internally retry**: re-folding the already-staged records over the moved frontier would collide, and re-running `f` is forbidden (`f: FnOnce`). So an install-time root change surfaces `TxnError::Conflict` for the **caller** to re-invoke with a *fresh* closure. (This is the sole realization that genuinely yields `Conflict`; contrast `PerKeyMerge`, whose held keys pin the frontier so it re-folds the already-staged records at install *without* re-running `f`.) Same footprint-confinement obligation (the full read set, with the same positive-vs-negative monotone caveat) as merge-at-install. Viable when same-key contention is rare; retry termination is open (ASN-0134 OQ1/OQ3).

`critical_section` is available only under the latter two realizations (§4); the single applier offers only the one-`transact` run (and `critical_section` **panics** there).

## Invariants & contracts

**By construction** (falls out of the data model above):
- **Total order, monotone `Seq`, refining `𝔼` — gap-free *only* under `BurnedSeqPolicy::Rollback`** — counter under the serializer (ASN-0134 A1/A2, SequentialTransitionAxiom; ASN-0047 same). A `→_sh` record's `Seq` *corresponds positionally* to its `idx(σ)` (the `→_sh` subsequence is order-isomorphic to `𝔼`) but is **not equal** to it — non-`→_sh` records also carry `Seq`s — so M2's order is a *refinement* of `𝔼`, not an identity (§2). The order-isomorphism to `𝔼` survives gaps, so the *refinement* is **unconditional**; only **gap-freeness** is policy-conditional — it holds under `Rollback`'s Seq-rollback on durability failure (§1) and relaxes to **monotone-only** under `TolerateGap`.
- **No torn read / per-call single-state** — immutable `Committed<W>` + atomic `ArcSwap` install + lock-free load (A0/A3/A4/V0, MIC-4). Under group commit, external readers see only the post-barrier root, never the applier's working tip (§1).
- **Multi-read verdict single-state** — one `Snapshot` threaded through all reads (V2, MIC-6; caller contract, made trivial by persistent root).
- **Composite Seq-contiguity** — a composite's Seqs assigned as a unit; an *internal-order* property only — W2 chain contiguity comes from the held `key(d,s_C)`, not from this (§2/§4).
- **Append-only journal; a committed frame (one whose marker is durable) is immutable; every prefix-to-a-marker is a replayable canonical state** — append-only file + terminal per-txn marker + `apply` determinism (ASN-0047 journaling; ASN-0134 A6).

**By active enforcement** (M2 must guard, named where):
- **Same-key serialization** — keyed critical section §4 / single applier §8 (ASN-0134 H2, MIC-2; M3 builds frontier H0 atop it).
- **Commit-before-acknowledge** — `transact` returns only post-durable+install §3; a zero-step op reading off a not-yet-durable working tip likewise waits for that tip's barrier before returning §1/§3 (A7, MIC-3).
- **Composite atomicity (none-or-all to readers)** — single atomic install §3 + commit-marker recovery discard §7 (ASN-0047).
- **Durability before ack, with a sound failure path** — canonical durable-before-visible: append records+marker → barrier → install (group commit: publish the batch's final tip, leader-only) → return; a barrier failure truncates the txn's un-acked frames and rolls the `Seq` high-water back, so `TxnError::Durability` is a **true no-op** and no failed marker can be promoted by a later fsync — *but only if that truncation itself completes durably; if it does not, the kernel **poisons** rather than no-ops*, since a surviving failed marker plus the reused burned Seqs would corrupt (the very phantom-commit/Seq-collision hazard the ordering exists to prevent) §1/§3 (ASN-0047). The visible-before-durable ordering — the optional single-applier variant **and the necessary ordering of the per-key-concurrent and CAS realizations (§8)** — instead **poisons** on barrier failure and exposes a not-yet-durable state to an external M10-acked read (resolved conflict — see *Conflicts resolved*).
- **Recovery faithfulness** — replay committed records **filtered to `Seq > S`** (skipping any `≤ S` frames surviving §6's segment-granular reclamation) in order; recovery first scans to the **committed tip** (the last validated marker, §7), then a CRC/marker failure *at or after* it is the never-acked torn tail (discard + truncate — a failed-barrier txn already left no marker, or the kernel poisoned), while one *strictly before* it is corruption of acked data (halt, `OpenError::Corruption` — never drop) §6/§7 (A6; ASN-0047).
- **Deadlock-free multi-key acquire** — acquire the *resolved lock objects* in a canonical layout-dependent order: keys sorted + deduped bytewise under `PerKey`, **stripe indices** sorted + deduped under `Striped` (a key-order acquire would self-deadlock or deadlock under striping) §4.
- **idem=⊤ dedup atomicity** — read-decide-deposit under the coverage-class key = one `transact` §4 (I1a/I4/G2, MIC-7).
- **Run contiguity** — a run as one `transact([key(d,s_C)], …)`: the held key delivers W2 chain contiguity, the single atomic install over-satisfies clause 5; or — *concurrent impls only* — `critical_section` held across separate deposits §4 (W2, MIC-5).
- **Live derived-hint correctness** — incremental hint maintenance is folded by `apply` on every commit and every replay step; `rebuild_derived` only seeds skip-serialized hints at load (§1/§7). A store that maintains a hint via `rebuild_derived` alone leaves it stale after every live write — so hint folding in `apply` is mandatory; and a store that *does* override `rebuild_derived` must seed exactly the `apply`-fold of the `Seq ≤ S` prefix, else the recovered hint diverges from the live one (§7).

**Explicitly *not* M2's** (passes through M2, enforced by neighbors):
- store permanence P0–P3/L12 and the J-couplings J0/J1★ (stores' `apply`+API; M5's composite boundary — ASN-0047);
- frontier/address and coverage-class computation (M3, M1/M7);
- register-before-allocate ordering (a store precondition checked against the snapshot, then a clean `Rejected` if unmet);
- the request lifecycle and ack-to-client (M10);
- multi-*step* (`m ≥ 2`) batch atomicity (above the substrate, A5; a single-step `m = 1` fire **is** one atomic `transact`);
- durability *as a requirement* (not a MIC clause — `Durability::None` is faithful);
- **footprint confinement of `f`** — a *caller* obligation under merge-at-install/CAS: `f`'s entire committed-state **read set** — every value consulted to decide what to stage, whether to reject, or which branch to take, not just the staged records' values — must lie under its held `keys` or be **monotone-safe** (a *positive* membership test on an append-only set, e.g. `a ∈ dom(C)`; a *negative* existence/freshness test like `a ∉ dom(C)` is **not** monotone-safe and must be keyed) (§8). Writes are confined by construction (staged records touch only held-key state plus fresh, disjoint appends), so the active obligation is the read set. M2 *relies* on it for the conflict-free re-fold but **cannot itself check it**; violated, it corrupts silently under concurrency. Enforced by the stores, by contract, not by M2's mechanism.

## Dependencies & seams

**Upstream: none.** M2 is a foundation (it carries no edge to M1 — keys and payloads are opaque, ordering of keys is plain bytewise, not tumbler order). Its only dependencies are crates: `im`, `arc_swap`, `serde`, `parking_lot`/`dashmap`, a CRC32C lib.

**Composition seam (dependency-inverted).** The engine crate defines `World` (composing all store slices) and `Record` (the enum union of every store's record-types), implements `WorldState` for `World` by dispatching `apply` to the owning store's logic, and instantiates `Kernel<World>`. "Stores register record-types" = contribute `Record` variants + `apply` arms; "index-rebuilders" = **mandatory** incremental hint maintenance inside `apply` (it runs on every live commit and every replay step — a hint not folded here is stale after every write), plus, optionally, `World::rebuild_derived` to seed hints the checkpoint skip-serialized (it runs once at load, before replay, never on a live commit, so it cannot keep a hint current on its own — and whatever it seeds must equal the `apply`-fold of the `Seq ≤ S` prefix it stands in for, §7). Three hard contracts on store code: **(1)** stage only authoritative deltas, maintain hints incrementally in `apply`, and **never journal a hint**. **(2)** under the per-key-concurrent/CAS realizations, **footprint confinement** — `f`'s entire committed-state **read set** (every value consulted to decide what to stage, whether to reject, or which branch to take — not only the staged records' values) must lie under the state the txn's `keys` cover, or be **monotone-safe**. Monotone-safety is *narrower* than "append-only": a *positive* membership test on an append-only set (`a ∈ dom(C)`) is exempt because its truth survives every append, but a *negative* existence/freshness probe (`a ∉ dom(C)`) is **not** — a concurrent append falsifies it — and must be under held keys. Writes need no separate clause: they are confined by construction (a txn's staged records mutate only its held-key state and append fresh, disjoint entries), so the *active* obligation is on the read set. Because merge-at-install re-folds the decided records without re-running `f`, an unconfined read means a stale decision (which records, hit vs miss, reject, branch) commits at a non-serializable position. A store honoring (2) migrates single-applier → concurrent transparently; one whose *read set* escapes its keys is correct under the single applier but corrupts silently under merge-at-install. M2 cannot check (2); it is the store's contract. **(3)** if a store overrides `rebuild_derived` to reconstruct a skip-serialized hint, that override must seed exactly what folding the `Seq ≤ S` prefix through `apply` would produce — so the load-time seed and the live `apply`-fold can never disagree (§7); M2 cannot check this either.

**Downstream seams (what neighbors code against):**
- **M3 allocation** (frontier under H0): `let (addr, _seq) = kernel.transact(&[key(home, subspace)], |stg| { let φ = recompute_max_under(stg.base(), home, subspace); let addr = inc(φ); stg.push(Record::Alloc{addr, …}); Ok(addr) })?`. M3 supplies the key bytes (1-byte space tag + tumbler bytes) and does all address math; M2 only locks + commits. The frontier read is confined to `key(home,subspace)`, satisfying footprint confinement (it is the only committed-state read `f`'s decision depends on).
- **M5 placement composite** (INSERT/COPY/VERSION): one `transact([key(d, s_C)], …)` staging K.α + K.μ⁺ + K.ρ, returning `(_, last_seq)`; M5 checks S3★ on `stg.working()` and the J-couplings at the boundary; M2 commits atomically. CREATENEWDOCUMENT (M3) is one `transact` registering the entity (returning its `Seq`) — it does *not* materialize an arrangement (M5 keeps that lazy).
- **M7 idem=⊤ emit**: `transact(&[class_key, key(home, s_L)], |stg| { if m7_active_in_class(stg.base(), class).is_some() { Ok(Hit) } else { let ℓ = inc(…); stg.push(Record::LinkEmit{ℓ, tuple}); Ok(Deposited(ℓ)) } })` → `(outcome, seq)`. The class_key serializes same-class emits (clause 7); the alloc key serializes same-home allocation (clause 2); the active-in-class read on which the hit/miss decision turns is confined to the held `class_key` (footprint-confined). Nullify hit-branch = a `transact` that stages nothing (zero-step), returning `(Hit, base.seq())` — and, under group commit, waiting for `base`'s barrier first (§1). The spanfilade is M7's hint, maintained incrementally in `apply` (mandatory — never journaled) and seeded by `rebuild_derived` only if the checkpoint skip-serialized it — that seed obligated to equal the `apply`-fold of the `Seq ≤ S` prefix (§7).
- **M6/M8/M9 readers & verdicts**: `let s = kernel.snapshot();` then read every constituent off `s` (clause 6). M9 reports quiescence as "as of `s.seq()`" (V1 retrospective). For its *writes* (rule fires), M9 takes the fire's index from the `Seq` that `transact` returns — exact even under per-key concurrency, unlike a post-hoc `current_seq()`. A *single-step* (`m = 1`) fire is exactly one atomic `transact` (the "atomic fires" M9 leans on); a *multi-step* (`m ≥ 2`) fire is an A5 batch M9 sequences as several `transact`s above the substrate.
- **M10**: opens/commits each operation's transaction via `transact`, receiving `(result, last_seq)`; acknowledges to the external client only after it returns (commit-before-ack), may report `last_seq`, and surfaces `TxnError::Rejected(E)` as a typed rejection (never a silent skip). (An operation still returns only once *its own* effect is durable in every realization; but under the visible-before-durable realizations — per-key/CAS, §8 — a **reader** can be acked reflecting *another* op's installed-but-not-yet-durable effect, which a crash may roll back. The single applier's durable-before-visible default closes even that window — §1/Conflicts #3.)

## Conflicts resolved

**1. Composite atomicity (ASN-0047) vs "batches are not atomic" (ASN-0134 A5).** The two speak of different units. M2's atomic unit is the **transaction** (one `transact`) — externally none-or-all. ASN-0047's "observable intermediate states" of a composite are precisely `Staging.working`, visible *only to the executing closure* for intra-composite precondition checks, never to external readers. ASN-0134's "batches not atomic" refers to a sequence of *separate* operations (`retract_stale`, a multi-step (`m ≥ 2`) rule firing) whose partial visibility is intended (a single-step `m = 1` fire is one atomic `transact` — §Purpose); M2 deliberately does **not** bundle those into one transaction. The **content run** (one `K.α` per atom) is the boundary case ASN-0134 A5 explicitly classes as a non-atomic batch — and M2 may commit it *either* way, the builder's call (ASN-0134 decision #7): as **one atomic `transact([key(d,s_C)], …)`** (the held key delivers W2, the single install over-satisfies clause 5 — no reader lands mid-run), or, when reader-visible mid-run partial visibility is wanted, as **`critical_section` + separate per-atom commits** (clause-5-faithful, available only under the concurrent realizations — it panics under the single applier — §4). So: M2 delivers transaction (composite) atomicity; multi-transaction batch atomicity is the caller's, "above the substrate"; and the content run sits on the seam, committable either as one atomic unit (over-satisfaction) or as a held-key sequence of commits (faithful clause 5).

**2. Single global writer (ASN-0047) vs per-home serialization suffices (ASN-0134 G1).** The **contract** is the weaker one — per-key serialization (clause 2). The recommended **first implementation** is a single applier (ASN-0047), which over-satisfies it. Because `transact(keys, …)` is identical for both, the migration single-applier → per-key-concurrent (merge-at-install) changes no caller's *call shape* — but it is transparent **iff every store confines its entire committed-state read set — every value `f` consults to decide what to stage, whether to reject, or which branch to take, not just its staged records' values — to its held keys** (modulo monotone-safe reads — *positive* append-only membership only, not negative existence probes; §8), ASN-0134 G1's full commutativity hypothesis (neither reads nor writes shared state) raised to a seam contract (§8 / Dependencies & seams). A store written against the single applier that reads or writes state *outside* its keys compiles and runs correctly there but corrupts silently under merge-at-install; and because "build single-applier first" authors stores *before* this discipline would otherwise bite, the contract must be stated up front. ASN-0047's single-writer is one conservative realization of ASN-0134's contract, not a competing requirement.

**3. Visible-after-durable (ASN-0047) vs durability-orthogonal (ASN-0134).** ASN-0047 says make a composite visible only after its batch is durably committed — natural in its single-threaded model, where *visible* == *acked*. ASN-0134 treats durability as orthogonal (not a MIC clause; `Durability::None` is faithful) and takes *visible* == *committed*. M2 resolves this by making **durable-before-visible the canonical ordering of the single applier** — the recommended first implementation (§1/§3): install follows the marker barrier (under group commit via the working tip), so an external M10-acked read never reflects a state a crash can roll back — *including a zero-step idem-hit, which under group commit waits for the barrier covering the working tip it deduplicated against before acking* (§1/§3) — and `TxnError::Durability` is a sound true no-op *so long as the un-acked-tail truncation completes durably; if it does not, the kernel poisons rather than no-ops* (§1). The **visible-before-durable** ordering (install-then-fsync) takes ASN-0134's weaker stance: prefix-closure keeps it safe for *internal* causal dependence, but an external read acked during the not-yet-durable window can be rolled back by a crash, and a barrier failure must poison the kernel rather than no-op (the install is already visible). This ordering is an **opt-in throughput variant under the single applier** *and the necessary, non-optional ordering of the per-key-concurrent and CAS scaling realizations* (§8) — whose install-before-barrier shape leaves no room for durable-before-visible. **So the concurrency-mechanism and durability-ordering decisions are coupled, not independent:** durable-before-visible requires the single applier; choosing per-key/CAS for throughput adopts visible-before-durable, and with it the external-M10-read-rollback window and poison-on-barrier-failure. The migration single-applier → per-key changes no caller's *call shape*, but it **does** change this externally-visible durability semantics — the one thing "API-invariant" does not cover. The conflict is thus resolved by canon (ASN-0047) for the single applier, with the ASN-0134 reading the mandatory semantics of the scaling path.

**Boundary clarifications (territory that *looks* like M2's but is a neighbor's, resolved by the decomposition's dependency inversion):** the frontier discipline ASN-0134 reasons about (H0) is M3's *allocator*; M2 owns only its *serialization*. The request/response path and pipelining-vs-sequential client model (G0) are re-homed to M10; M2 keeps only the commit-gate mechanism. Neither is a conflict — both are M2 honoring its seam by *not* doing the neighbor's job.

## Open build decisions

- **Concurrency mechanism** — single applier (recommended first) → per-key concurrent with merge-at-install (scaling path; binds the footprint-confinement read-set contract) → optimistic-CAS (only under measured low same-key contention; `Conflict` is caller-re-invoke-with-a-fresh-closure since `f` is `FnOnce`; retry termination unresolved, OQ1/OQ3). Pick by throughput need; the API doesn't change — **but this is *not* independent of the durability-ordering decision below: per-key and CAS are necessarily visible-before-durable (install precedes the barrier; §8), so only the single applier can run the canonical durable-before-visible ordering.**
- **Durability/visibility ordering** (coupled to the concurrency choice above — **only the single applier can be durable-before-visible**) — **durable-before-visible (canonical, single-applier: append records+marker → barrier → install; under group commit `base` is drawn from the applier's working tip and the batch's final tip is published once, post-barrier, by the leader; a `Durability` failure is a sound no-op via truncate + Seq rollback *iff that truncation completes durably — else poison*)** vs visible-before-durable (install-then-batched-fsync; needs no working tip; prefix-closure keeps internal dependence safe, but an external M10-acked read can reflect a rolled-back state, and a barrier failure must poison rather than no-op — §1, Conflicts #3) — the latter an opt-in throughput variant under the single applier and the **forced** ordering under per-key/CAS. Group commit amortizes the barrier under either.
- **Burned-Seq policy on durability failure** — roll the `Seq` high-water back to the last committed marker (keeps the order gap-free; recommended) vs tolerate the gap (relaxes the invariant to monotone-only) (§1). Either way, a *failed* truncation of the burned frames forces a kernel poison, not a no-op (the surviving failed marker would replay as a phantom commit) — §1.
- **Durability mode** — `Fsync` per commit vs `FsyncBatch{window, max_delay}` (group commit, the batch closing on window-fill *or* `max_delay`, whichever fires first — a window-only trigger would stall a low-traffic batch and any zero-step op waiting on its barrier indefinitely; `flush()` is the manual close) vs `None` (in-memory, MIC-faithful, for tests/embedding).
- **Checkpoint cadence & representation** — every-N-commits / time / journal-size; full-`World` serialize vs per-store/incremental; serialize hints vs `#[serde(skip)]` + `rebuild_derived` (checkpoint size vs recovery recompute — and an overriding `rebuild_derived` must match the `apply`-fold of `Seq ≤ S`, §7). The recovery-time-vs-overhead knob ASN-0047/0134 leave open. (The `≤ S` / `> S` checkpoint-vs-replay boundary itself is *fixed*, not a knob — §6/§7; journal truncation against a checkpoint is segment-granular space reclamation, never a correctness mechanism — recovery's `Seq > S` filter handles any `≤ S` frames a straddling segment leaves behind.)
- **Lock-table layout** — striped `Vec<Mutex>` (bounded, false contention) vs per-key `DashMap` (no false contention, entry GC). *This choice also sets the multi-key acquisition order: `Striped` acquires in stripe-index order, `PerKey` in bytewise-key order (§4).*
- **Journal framing** — CRC algorithm (the frame `crc` covering **both `len` and payload**, so a corrupt length is detectable and the recovery scan can resynchronize past a bad frame to find later markers — §1/§7), segment rotation, max frame size, fsync-of-dir on rotate.
- **Whether to build `critical_section` at all** — default to issuing every run as one `transact` (atomic, delivers W2 via the held key, over-satisfies clause 5); build the held-across-commits guard only if a run is genuinely too large to commit atomically or needs intended mid-run reader visibility — and only under the per-key-concurrent/CAS realizations, since under the single applier it provides no run-exclusion and therefore **panics** (§3/§4).
- **Record/key encoding** — `Record` (the trait's `W::Record`) as one serde enum (recommended for a single binary, compile-time dispatch) vs a runtime type-id registry of boxed appliers; `LockKey` as `Vec<u8>` vs `SmallVec`/`Box<[u8]>` vs a fixed-width digest.
