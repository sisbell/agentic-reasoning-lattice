# M4 — Content Store (Istream) — Detailed Design

## Purpose & boundary

M4 is the permascroll: an append-only, write-once map from allocated I-address to opaque content value, plus the two point queries over it — *is content stored here?* and *what is stored here?* It owns the immutable, never-GC'd half of the two-layer state and **does exactly that one thing.** It does **not** mint addresses (M3), arrange or reference content (M5), enforce referential integrity (M5 — M4 only *answers* the check), resolve V→I, attribute origin, or compare versions (M6), store links (M7 — the parallel value store for `L`), or own a journal/snapshot/recovery story (M2). Addresses arrive as parameters already minted and validated upstream; M4 trusts them and stores bytes. The one-thing-well statement: **store an immutable value at an address forever, and look it up — never mutate, never delete, never reclaim, never key on the value.**

## Public interface

Three groups. The first is the engine-composition plug; the second is the read contract; the third is the write surface other stores compose.

### A. Engine-plug surface (slice / record / accessor / fold)

Named to match the Engine Composition Contract's assembler (`content: ContentStore`, `HasContent::content`, `apply_write`, `Record::Content(ContentWrite)`), so M4 drops into `skep-engine` unchanged.

```rust
/// M4's authoritative folded slice: dom(C) ↦ Val. The only state M4 owns.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct ContentStore { map: im::HashMap<Tumbler, Val, FixedHasher> }

/// M4's sole authoritative journal delta. Carries the FLAT Tumbler (M1: the
/// Tumbler is the storage/journal key; Address is the past-the-door value).
/// FIELDS ARE PRIVATE: `stage_write` is thereby the compiler-enforced sole
/// constructor, so no caller can hand-build a record into the total fold and skip
/// the AlreadyPresent guard. serde deserializes the private fields for M2's replay
/// (derive expands at the definition site); the engine only `From`-lifts and folds,
/// never constructs one from scratch.
#[derive(Clone, Serialize, Deserialize)]
pub struct ContentWrite { addr: Tumbler, val: Val }

/// The engine implements this for `World`; M4 reaches its slice off any `&W`.
pub trait HasContent { fn content(&self) -> &ContentStore; }

impl ContentStore {
    /// The fold — pure, total, deterministic (M2's `apply` obligation). Insert only.
    /// `stage_write` guarantees `r.addr ∉ dom(C)`, so this never overwrites a live value;
    /// the `debug_assert!` is a release-free second net behind that guard (stays total/
    /// infallible in release).
    pub fn apply_write(&self, r: &ContentWrite) -> ContentStore {
        debug_assert!(!self.map.contains_key(&r.addr),
            "S0(b): apply_write must not overwrite — stage_write guards this");
        ContentStore { map: self.map.update(r.addr.clone(), r.val.clone()) }
    }
}
```

### B. Read API (membership & value-at — point queries over a pinned slice)

```rust
impl ContentStore {
    /// S3 referential-integrity oracle: a ∈ dom(C). CONTENT-PRESENCE — not "allocated"
    /// (M3) and not "registered" (M3). M5 calls this on the content side of placement.
    pub fn contains(&self, a: &Tumbler) -> bool;

    /// C(a): the immutable value at a, else None. The returned borrow lives THROUGH the
    /// pinning Snapshot — bind the snapshot first (see Internal design). RETRIEVEV
    /// (M6, ASN-0115) and predicate-def read-back (M9) call this.
    pub fn value_at(&self, a: &Tumbler) -> Option<&Val>;

    pub fn len(&self) -> usize;        // |dom(C)| — diagnostics only
    pub fn is_empty(&self) -> bool;
}
```

### C. Write surface (the two composable forms — M2 contract 3)

```rust
/// PURE STEP — the storage half of K.α. Reads off a supplied working slice, returns the
/// record, commits nothing. THIS is M4's real export: M5's placement composite (and, via
/// M5, M9's predicate-def creation) calls it and lifts the result with `.into()`.
/// Enforces S0's no-overwrite (`AlreadyPresent`); otherwise trusts the address. As the
/// only constructor of the private-field `ContentWrite`, it is the guard's chokepoint.
pub fn stage_write(c: &ContentStore, addr: &Address, val: Val)
    -> Result<ContentWrite, ContentError>;

/// STANDALONE OP — the contract-required transact-wrapped form. Generic over W.
/// ISOLATION/TEST USE ONLY: committing a content write *alone* creates content with no
/// placement, violating J0 (content-allocation ⇒ placement). Production content writes
/// MUST ride M5's J0/J1★-coupled composite via `stage_write`.
/// Body: derives the lock key `key(document_of(addr), s_C)` via the shared key constructor,
/// then `transact([key], |stg| { let r = stage_write(stg.working().content(), addr, val)?;
/// stg.push(r.into()); Ok(addr.tumbler().clone()) })`. A content address has zeros = 3, so
/// `document_of(addr)` is always `Some`; a `None` is an internal-invariant violation on this
/// trusted-address-only op (documented `expect`), never a domain rejection.
pub fn write<W>(k: &Kernel<W>, addr: &Address, val: Val)
    -> Result<(Tumbler, Seq), TxnError<ContentError>>
where W: WorldState + HasContent, W::Record: From<ContentWrite>;
```

### Types & errors

```rust
/// Opaque, immutable content payload. Write-once ⇒ never edited ⇒ needs no internal COW;
/// Arc gives O(1) clone for the map's structural sharing. The derive below requires serde's
/// `rc` feature (for the `Arc<[u8]>` impls); the rc-free alternative is a manual
/// `&[u8]` ⇄ `Vec<u8>`→`Arc::from` round-trip. Serializes as a plain byte blob either way.
#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Val(Arc<[u8]>);
impl Val { pub fn new(b: impl Into<Arc<[u8]>>) -> Val; pub fn as_bytes(&self) -> &[u8]; pub fn len(&self) -> usize; }

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ContentError {
    /// Defensive S0 guard: a value is already stored at this address. Cannot occur in
    /// production (M3 mints fresh; M5 writes once) — converts an upstream bug into a clean
    /// rejection instead of a silent permascroll overwrite.
    AlreadyPresent(Tumbler),
    /// Optional defense-in-depth (debug/off by default): not a content-subspace element
    /// address. Routing is M5's job, mint-conformance M3's — see Open build decisions.
    NotContentAddress(Tumbler),
}
```

## Core data model

**One authoritative structure, no derived hint.** M4's slice is `ContentStore { map: im::HashMap<Tumbler, Val> }` — the direct fold of `ContentWrite` records.

- **Why `im::HashMap` (not `OrdMap`).** M4's *entire* query surface is point membership (`contains`) and point value-at (`value_at`). Nobody needs ordered iteration, range, or prefix scans: the one consumer that would (M3's allocator, for "max content address under document `d`") reads **M3's own frontier**, never M4 — the DAG has no `M3 → M4` edge, and content allocation is decoupled from content storage (ghost elements). So pay nothing for ordering: HAMT gives O(1)-effective lookup/insert. (`OrdMap` is the fallback *only if* a content-prefix-scan consumer — e.g. "all content originated by `d`" — or a hot RETRIEVEV native-run range-fetch ever appears; today none does.)
- **Why persistent (`im::`) at all.** Not for snapshot-taking — M2's `Snapshot(Arc<Committed<W>>)` makes that an O(1) Arc clone of the whole `World`. It is for the **commit path**: each `transact` produces a *new* `World` via `apply`, and outstanding snapshots pin *old* Worlds. With `im::HashMap`, `apply_write` is O(log₃₂ n) and old/new maps share all untouched structure, so retaining prior versions for live snapshots is nearly free. A clone-on-write `std::HashMap` would copy the whole map per commit — untenable for a store that only grows.
- **Why `Val = Arc<[u8]>`, opaque.** Content is write-once, so a value is never edited and needs no internal persistent structure; an `Arc<[u8]>` is an immutable, O(1)-cloneable leaf (the map's structural sharing just bumps refcounts). M4 is **value-oblivious**: it never inspects bytes. *Kind* (text vs. anything else) is recovered from the I-address structure via M1 (`subspace`/`classify`), never from a stored tag — there is no type discriminator on the value (ASN-0036 content-typing).
- **Fixed (deterministic) hasher.** Keys are trusted internal tumblers, not adversarial input, so flooding-resistance buys nothing; pick a fixed-seed hasher (`FxHasher`-class) so checkpoint serialization is reproducible across runs.
- **Authoritative vs hint.** The journal of `ContentWrite` records (held by **M2**) is ground truth; the `im::HashMap` is its fold — M4's authoritative *slice* in the contract's sense, fully serialized in checkpoints (no skip-serialize, so the engine's `rebuild_derived` is identity for M4). The single *optional* hint M4 might own is an internal value-dedup table (see Open build decisions); the base design has none.

## Internal design

M4 is deliberately thin in mechanism; each component is a few lines, but the disciplines they encode are the substrate floor.

**The address→value map (the store itself).** A content write is one `ContentWrite { addr, val }` record; `apply_write` does a single HAMT `update`. The placement composite (M5) inserting `m` content atoms stages `m` such records in one `transact`; M2 commits them under one marker. *Common case:* O(log₃₂ n) per atom. M4 keys by `Tumbler` and is granularity-agnostic — for text, one address ≈ one atom (many small values, the inline-`Arc` default); a larger element is just a larger `Val`. M4 never groups addresses into runs — that compression is M5's (V-space) concern; M4 is purely per-address.

**Membership & value-at.** `contains`/`value_at` are HAMT point lookups over a slice obtained from a pinned snapshot. The returned `&Val` borrows *through* the pinning `Snapshot`, so the caller **binds the snapshot first** — `let s = k.snapshot(); s.world().content().value_at(a)` — never `k.snapshot().world().content().value_at(a)`, which borrows into a dropped temporary and won't compile. O(1)-effective, lock-free (the snapshot is an immutable pinned `World`). These are the hot paths — `contains` on every placement (S3), `value_at` on every retrieval — so they must be cheap, and they are.

**Write-once / immutability discipline.** Two layers. *By construction:* the API and the fold expose **no** modify/delete/GC operation — a `ContentWrite` can only add, so existing entries can never change or vanish (S0 domain-persistence, S1/C0 growth fall straight out; cf. Green's protocol having no MODIFY). *By active guard:* because the fold is total (it cannot reject), the no-**overwrite**-of-an-occupied-address half of S0(b) is enforced in `stage_write` — which, because `ContentWrite`'s fields are private, is the *compiler-enforced* sole constructor of the record, so no caller can hand-build a record into the total fold and skip the check. It returns `AlreadyPresent` if `addr ∈ dom(C)`. Without this guard, a buggy double-stage would reach the total fold and `update` would replace the value, silently violating S0; with it, the most sacred invariant degrades to a clean typed rejection. (`apply_write`'s `debug_assert!` is a release-free backstop behind the guard.) The guard never fires in correct operation (M3 freshness + M5 single-write), but it is the cheap correct-the-rare-case insurance over the permascroll.

**Origin-identity discipline (no value-as-identity).** Identity is the full allocated address; M4 keys by address and *never* by value, so two equal byte-runs at two addresses are simply two entries (S4). There is no value→address index and no content-addressed identity. Any value-dedup is permitted only *beneath* the map as a blob-compression layer (`value-hash → blobref`, many addresses → one stored byte-run) and must never surface through the `Tumbler`-keyed interface as identity. *Tradeoff:* you forgo automatic content-collapse at the identity level (mandatory — S4 forbids it) in exchange for transclusion-as-address-sharing being decidable by address equality alone.

**No-GC / permanence & unbounded sharing.** M4 holds no refcount, no reference set, no cap, and no reclamation path. Unreferenced ("orphan") content persists unconditionally (S0 frame) because M4 doesn't even know about references — the V→I reference relation lives entirely in M5, and the inverse "who references `a`?" index is M5/M8 territory, never built here. So S5 (unbounded sharing) holds *by omission*: M4 stores each address once and is indifferent to reference multiplicity. *Watch:* never introduce a fixed-width refcount that could cap or overflow.

**Recovery (M2-driven — M4 owns none).** This is the deliberate re-homing from the source notes. M4 keeps **no** journal, replay loop, or snapshot machinery. `ContentWrite` is the authoritative delta M2 journals; the slice is `Serialize`/`Deserialize`, so M2's `open` loads the latest checkpoint (deserializing the map) and replays the tail by folding records through `apply` → `apply_write`; a torn/un-acked tail is discarded by M2. Records carry the address verbatim, so replay re-applies (no re-derivation; M2 applies each committed record exactly once) — the deterministic-remint self-check ASN-0093 offered is M3's option for *Alloc* records, not M4's. *Tradeoff to flag for cadence:* an inline-value slice serializes all bytes into every checkpoint, so M2's `CheckpointPolicy` trades recovery time against checkpoint size; out-of-line values (Open decisions) shrink the serialized slice to address→ref and make checkpoints cheap regardless of content volume.

**Concurrency.** None of M4's own. Content writes ride M5's composite under the per-(document, content-subspace) lock key `key(d, s_C)` (the *same* key M3's content allocation holds — alloc, write, and placement serialize on one key, in one composite). Distinct documents' content writes carry distinct keys, which *delimit independent serialization scopes* — the invariant `LockKey` seam; whether distinct keys actually execute concurrently is M2's later realization (v1 serializes all writers under the global applier lock, with the `transact`/`LockKey` signatures unchanged across that change). M4's correctness does not hinge on it anyway: because every content address is written exactly once (M3 freshness), no two writers ever target the same address — there is no logical content write-write conflict to resolve, ever.

## Invariants & contracts

**By construction** (falls out of the data model / API shape):

- **S0(a) domain-persistence; S1 / C0 growth** (ASN-0036 S0/S1; ASN-0093 C0): only-insert fold, no removal op ⇒ `dom(C) ⊆ dom(C')`.
- **S0(b) value-preservation, modify half** (ASN-0036 S0; ASN-0093 C0): no modify operation exists. (The overwrite half is actively guarded — below.)
- **S4 origin-based identity** (ASN-0036 S4): keyed by address, never by value; no value→identity collapse.
- **S5 unbounded sharing** (ASN-0036 S5): by omission — no refcount, no cap; references live in M5.
- **S7 structural attribution** (ASN-0036 S7): origin is structural — recovered via M1's `document_of` (surfaced as SHOWORIGIN in M6) — so M4 stores no author/source/origin metadata; it holds only `address → Val`.
- **C-fin finiteness** (ASN-0093 C-fin): `|dom(C)| < ∞` — each commit adds finitely many entries and there is no growth path to infinity.
- **No-GC / unconditional permanence** (ASN-0036 S0 frame): no reclamation path, not refcount-gated.
- **S3 at every committed state** (ASN-0036 S3): because M5's composite writes content (M4) and places it (M5) in one atomic M2 transaction, no committed snapshot ever shows a placement referencing absent content — the strongest S3 timing, achieved by M2's atomicity, not by M4. (M4 supplies the oracle; M5 is the enforcer.)

**By active enforcement** (M4 must guard — located in `stage_write`):

- **S0(b) no-overwrite-of-occupied-address** (ASN-0036 S0; ASN-0093 C0): `stage_write` rejects `AlreadyPresent(addr)` because the total fold cannot; `ContentWrite`'s private fields make `stage_write` the compiler-enforced sole producer of the record, so the guard cannot be bypassed. This is M4's *one* genuine guard.

**Discharged upstream — M4 relies on, does not re-enforce:**

- **T4-validity** of every address: M1's standing invariant (every `Address` is T4-valid).
- **C1 / C1b / L0** element-level, `#E≥2`, subspace `s_C` (ASN-0093): M3 mints conforming content addresses; M5 routes content V-positions to M4. M4 stores by-address; an optional boundary assertion (`NotContentAddress`) is defense-in-depth, not the source of truth.
- **C1c allocator conformance, C2 origin-registered scoping** (ASN-0093): M3's mint + register-before-allocate gate.

## Dependencies & seams

**Upstream — concrete use:**

- **M1.** `Tumbler` (slice/record key, `Ord/Eq/Hash` — **plus serde `Serialize/Deserialize`**, which M4's serializable slice/record require for M2's checkpoints+journal; M1 designates `Tumbler` "the storage/journal key," which implies this, but if M1's published derive list genuinely omits serde it is an upstream precondition gap to escalate, since no store could journal without it), `Address` (the value `stage_write`/`write` accept — fresh from M3's `checked_inc`), `document_of` (derive the lock key for the standalone op), and — *only if* the optional content-address assertion is on — `subspace`/`classify`/`Level`. No span/span-set use: M4 stores scalar values, not spans.
- **M2.** Provides `apply`-driven commit + replay (engine wires `apply_write`), `Snapshot`/`world()` (readers obtain `&ContentStore`), `Kernel::transact` (standalone `write` only), `LockKey`, `Seq`. **M4 owns no journal, replay, snapshot, or recovery** — all M2's. The per-(document, content-subspace) `LockKey` is built by the *shared* key constructor (below the stores, drawing its 1-byte space tag from the central enum) so M3 alloc / M4 write / M5 placement produce identical bytes; `s_C` comes from the shared SubspaceConventionAxiom constant, not a locally invented value.

**Downstream — seam contracts neighbors build against:**

- **→ M5 (placement composite).** `stage_write(c, addr, val) -> Result<ContentWrite, _>` is the storage half of K.α that M5 composes inside its `transact([key(d, s_C)], …)`: M5 calls it against `stg.working().content()`, then `stg.push(rec.into())` (engine's `From<ContentWrite> for Record`). `contains(a) -> bool` is the S3 referential-integrity oracle on the content side. The J0/J1★ couplings (content-alloc ⇒ placement ⇒ provenance) are M5's to enforce *around* the write; M4 contributes only the content-write step. M4 never reads M5 (no back-edge).
- **→ M6 (RETRIEVEV, ASN-0115).** `value_at(a) -> Option<&Val>` over a bound snapshot, after M6 resolves V→I (M5). M4 does **not** own the registered-empty-vs-unallocated distinction — that is M6's, against M3's registry.
- **→ M9 (predicate-def read-back).** `value_at(a)` reads a def's bytes by its content start-address (the def's identity); def *creation* rides M5's composite, which calls M4's `stage_write`.
- **→ engine crate.** `ContentStore` slice, `ContentWrite` record, `HasContent` trait, `apply_write` fold; the assembler implements `HasContent for World` and `From<ContentWrite> for Record`. It `From`-lifts and folds the record only — it never constructs a `ContentWrite` (private fields), so the `stage_write`-sole-constructor invariant survives assembly.

**Seam clarifications the builder must hold:** M4's `contains`/`value_at` mean **content-presence**, decoupled from allocation (M3) and registration (M3) — a content address can be allocated yet content-absent (a ghost), and M4 reports presence only. M4 is **never read by the link layer** (M7/M8 don't touch it); M7 is the parallel value-only store for `L`. M4 reads no module above M1/M2.

## Conflicts resolved

The two source notes largely agree on M4's territory; the substantive resolutions are against M2's re-homing and the M3/M4 split, not between the notes.

1. **Journal & recovery ownership** (both notes: "append-only journal recovered by replay," owned by the store). Resolved against M2: M4 owns no journal/replay/snapshot/recovery; `ContentWrite` is the authoritative delta M2 journals, the `im::HashMap` is its fold, and M2 drives recovery. The notes' "the in-memory index is a recomputable hint over the journal" becomes "the map is M4's authoritative slice, itself the fold of M2's journal" — same recomputability, ownership moved to the kernel. *Why:* the whole corpus leans on one recovery story; duplicating it in M4 would be redundant authoritative machinery.

2. **Membership semantics, and the M5 seam's "allocated in M4, checked via M3."** ASN-0093's invariants are about *allocation*; ASN-0036's S3 is about `dom(C)` *content-presence*. Resolved: S3's canonical oracle is M4's `contains` (content-presence); "allocated" (M3) and "content-present" (M4) **coincide** for content addresses written through M5's J0-coupled composite, so M5 may also check registration/allocation via M3 for the source-exists precondition, but the referential-integrity test proper is M4's `contains`. *Why:* keeps S3 exactly where the formal statement puts it (`dom(C)`), and keeps M4 free of any M3 dependency.

3. **Ordered tumbler map vs hash** (ASN-0093 recommends an *ordered* map for the allocator's max-under-prefix and prefix-range scans). Resolved by the M3/M4 split: M4 hosts no allocator and has no prefix-scan consumer, so the ordered-map rationale applies to M3's frontier, not M4's content map — M4 picks `im::HashMap`. *Why:* don't pay for ordering nobody queries.

4. **Unified `C+L` store (ASN-0093) vs split (M4/M7).** Resolved by the decomposition: M4 owns only `C`; `L` is M7's parallel value-only store. The append-only by-address mechanism is shared but instantiated separately, and M4 stores only content-subspace values.

5. **`Val` typing** (ASN-0036 leaves it open — uniform? tagged?). Resolved: opaque untyped bytes, no value tag; kind is recovered from the I-address structure (M1). The differing element-field numbering across the notes' examples doesn't reach M4 — M4 stores by whatever address it's handed and depends on no specific subspace numeral beyond the shared `s_C` for its lock key.

## Open build decisions

1. **Inline vs out-of-line values.** Default: inline `Val(Arc<[u8]>)` in record and slice — simplest, bytes durable in M2's journal, good for many small text atoms. Switch to an out-of-line blob store (slice holds `address → blobref`) **when** content volume makes per-checkpoint slice serialization the bottleneck — it shrinks the serialized slice and cheapens M2's checkpoints, at the cost of reintroducing a blob-durability concern (either M4-owned, a deviation from "M2 owns durability," or rebuildable by replaying M2's `ContentWrite` records, which still carry the bytes). Pick under measurement of content-size distribution and checkpoint cost.
2. **Internal value-dedup (CAS-underneath).** Optional `value-hash → blobref` compression layer beneath the map (many addresses → one stored byte-run), naturally paired with out-of-line blobs. Pure optimization; **must never surface as identity** (S4). If skip-serialized, it becomes the one derived hint requiring an engine `rebuild_derived` contribution. Enable only if content has high byte-level duplication and space matters.
3. **Record granularity.** Single `ContentWrite` per atom (matches K.α, `m` records per INSERT) vs a batched `ContentWriteRun { writes: Vec<(Tumbler, Val)> }` folded as `m` inserts. Default single; batch if per-record overhead in M2's journal dominates for large contiguous inserts. (A batched record keeps private fields + a `stage_write`-style sole constructor for the same S0(b) guarantee.)
4. **Defensive content-address assertion strength.** `stage_write` can additionally check `addr.level()==Element ∧ addr.subspace()==Some(s_C)` (→ `NotContentAddress`). Choose: full runtime guard (paranoid, couples M4 to `s_C`), `debug_assert!` only (recommended — catches routing bugs in test, free in release), or off (trust M5's routing + M3's mint entirely). Recommend debug-only.
5. **HashMap hasher.** A fixed-seed deterministic hasher is decided (reproducible checkpoints); the *specific* one (`FxHasher` / fixed-key SipHash / aHash-fixed-seed) is a minor pick under microbenchmark.
6. **`value_at` return type — borrowed vs cloned.** Default `Option<&Val>`, which ties the value's lifetime to the pinning `Snapshot` (caller binds the snapshot first). Since `Val` is `Arc<[u8]>` with O(1) clone, returning `Option<Val>` would decouple the value's lifetime from the snapshot for callers like M6/M9, at the cost of one Arc refcount bump per read. Minor ergonomics call; default to the borrowed form, switch to cloned if the snapshot-lifetime coupling proves awkward at a call site.
