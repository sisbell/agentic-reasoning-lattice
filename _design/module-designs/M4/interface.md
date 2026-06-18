# M4 — Interface (for dependents)

**M4 owns the permascroll:** an append-only, write-once map from allocated I-address to opaque content value (`dom(C) ↦ Val`), plus the two point queries over it — *is content stored here?* (`contains`) and *what is stored here?* (`value_at`). Nothing else.

## Public interface

### A. Engine-plug surface (slice / record / accessor / fold)

```rust
/// M4's authoritative folded slice: dom(C) ↦ Val. The only state M4 owns.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct ContentStore { /* private: the folded dom(C) ↦ Val slice */ }

/// M4's sole authoritative journal delta (the FLAT Tumbler key).
/// Fields private ⇒ `stage_write` is the compiler-enforced sole constructor.
#[derive(Clone, Serialize, Deserialize)]
pub struct ContentWrite { /* private fields */ }

/// The engine implements this for `World`; M4 reaches its slice off any `&W`.
pub trait HasContent { fn content(&self) -> &ContentStore; }

impl ContentStore {
    /// The fold — pure, total, deterministic (M2's `apply` obligation). Insert only.
    pub fn apply_write(&self, r: &ContentWrite) -> ContentStore;
}
```

### B. Read API (membership & value-at — point queries over a pinned slice)

```rust
impl ContentStore {
    /// S3 referential-integrity oracle: a ∈ dom(C). CONTENT-PRESENCE — not "allocated"
    /// and not "registered" (both M3).
    pub fn contains(&self, a: &Tumbler) -> bool;

    /// C(a): the immutable value at a, else None. The returned borrow lives THROUGH the
    /// pinning Snapshot — bind the snapshot first.
    pub fn value_at(&self, a: &Tumbler) -> Option<&Val>;

    pub fn len(&self) -> usize;        // |dom(C)| — diagnostics only
    pub fn is_empty(&self) -> bool;
}
```

### C. Write surface (the two composable forms)

```rust
/// PURE STEP — the storage half of K.α. Reads off a supplied working slice, returns the
/// record, commits nothing. Enforces S0's no-overwrite (`AlreadyPresent`); otherwise
/// trusts the address. Sole constructor of `ContentWrite`.
pub fn stage_write(c: &ContentStore, addr: &Address, val: Val)
    -> Result<ContentWrite, ContentError>;

/// STANDALONE OP — transact-wrapped form. ISOLATION/TEST USE ONLY: committing a content
/// write alone violates J0; production content writes MUST ride M5's composite via `stage_write`.
pub fn write<W>(k: &Kernel<W>, addr: &Address, val: Val)
    -> Result<(Tumbler, Seq), TxnError<ContentError>>
where W: WorldState + HasContent, W::Record: From<ContentWrite>;
```

### Types & errors

```rust
/// Opaque, immutable content payload (write-once). M4 never inspects the bytes.
#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Val(/* opaque bytes */);
impl Val { pub fn new(b: impl Into<Arc<[u8]>>) -> Val; pub fn as_bytes(&self) -> &[u8]; pub fn len(&self) -> usize; }

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ContentError {
    /// Defensive S0 guard: a value is already stored at this address. Cannot occur in
    /// correct production (M3 mints fresh; M5 writes once).
    AlreadyPresent(Tumbler),
    /// Optional defense-in-depth (debug/off by default): not a content-subspace address.
    NotContentAddress(Tumbler),
}
```

## Caller contracts & obligations

**`stage_write(c, addr, val) -> Result<ContentWrite, ContentError>`** *(the real export — M5 composes it)*
- Caller supplies the *working* slice `c` (e.g. `stg.working().content()`), an `Address` freshly minted+validated upstream (M3), and the value; M4 trusts the address and stores bytes.
- On `Ok`, lift the record into the engine record and stage it: `stg.push(rec.into())` — `stage_write` **commits nothing** itself.
- `Err(AlreadyPresent(addr))` iff `addr ∈ dom(C)`; this is the one guard, and cannot fire under correct M3 freshness + M5 single-write — handle it as an upstream-bug rejection, not a domain case.
- `ContentWrite`'s fields are private, so this is the **only** way to build a record — a caller cannot hand-build one and skip the guard.
- The J0/J1★ couplings (content-alloc ⇒ placement ⇒ provenance) are the caller's (M5's) to enforce **around** this step; M4 contributes only the content-write step.

**`write<W>(k, addr, val) -> Result<(Tumbler, Seq), TxnError<ContentError>>`**
- **TEST/ISOLATION ONLY.** Committing a content write alone creates content with no placement (violates J0); production callers must use `stage_write` inside M5's composite.
- Caller must satisfy the bounds `W: WorldState + HasContent` and `W::Record: From<ContentWrite>`.
- `addr` must be a real content address (zeros = 3); M4 derives the lock key internally — the caller does not supply it. A non-content address is an internal-invariant violation (panics via `expect`), **not** a domain `Err`.
- On `Ok`, returns the stored content `Tumbler` and the commit `Seq`.

**`contains(a: &Tumbler) -> bool`**
- Call on a `&ContentStore` obtained from a **pinned snapshot** (`s.world().content()`).
- Returns `true` iff `a ∈ dom(C)` — **content-presence**, decoupled from allocation and registration (both M3): a content address can be allocated yet content-absent (a ghost), and this reports presence only.
- Total (no error); O(1)-effective, lock-free. This is the S3 referential-integrity oracle on the content side.

**`value_at(a: &Tumbler) -> Option<&Val>`**
- **Bind the snapshot first** — `let s = k.snapshot(); s.world().content().value_at(a)`. The returned `&Val` borrows *through* the pinning `Snapshot`; chaining off a temporary snapshot will not compile.
- `Some(&Val)` if `a ∈ dom(C)`, else `None`. M4 does **not** distinguish *registered-empty* from *unallocated* — that distinction is M6's, against M3's registry; `None` means only "content-absent at `a`".
- Caller resolves V→I (via M5) before calling, where applicable (the M6 path).

**`apply_write(&self, r: &ContentWrite) -> ContentStore`** *(engine-only fold)*
- The M2 `apply` fold: pure, total, deterministic, insert-only; returns a new `ContentStore` with `r` inserted.
- Relies on `stage_write`'s guarantee that `r.addr ∉ dom(C)` — the engine `From`-lifts and folds records but never constructs a `ContentWrite` itself.

**`HasContent::content(&self) -> &ContentStore`** — implemented by the engine for `World`; readers reach the slice via `s.world().content()`.

**`Val::new / as_bytes / len`** — construct from any byte source, borrow the bytes, byte length. M4 is value-oblivious: *kind* (text vs. anything else) is recovered from the I-address via M1, never from `Val`.

**`ContentStore::len / is_empty`** — `|dom(C)|`, diagnostics only; not a domain query.

**Invariants a caller may rely on**
- Every entry persists **forever** — no modify, delete, GC, or reclamation (S0/S1/C0); `dom(C)` only grows.
- Identity is by **address, never by value** (S4): two equal byte-runs at two addresses are two distinct entries — no content-addressed dedup surfaces through the interface.
- Unbounded sharing (S5): M4 is indifferent to reference multiplicity; orphan content persists unconditionally.
- M4 stores **no** origin/author metadata — origin is structural (M1 `document_of`, surfaced as SHOWORIGIN in M6).
- Across any committed snapshot, S3 holds (no placement references absent content) — achieved by M5's atomic composite via M2, not by M4 alone.
- Every `Address` handed to M4 is T4-valid (M1 standing invariant); M4 does not re-validate.

**Build precondition (on the shared base crate, not on the caller):** M4's slice and record derive `Serialize + Deserialize`, which requires `Tumbler: Serialize + DeserializeOwned` (transitively `num-bigint`'s `serde` feature) in the crate that owns `Tumbler`. M4 cannot supply this itself (orphan rule); without it no store can journal or checkpoint.

## Seams exposed downstream

- **→ M5 (placement composite).** `stage_write(c, addr, val)` is the storage half of K.α that M5 composes inside its `transact([key(d, s_C)], …)`: M5 calls it against `stg.working().content()`, then `stg.push(rec.into())`. `contains(a)` is the S3 referential-integrity oracle on the content side. J0/J1★ couplings are M5's to enforce around the write. M4 never reads M5 (no back-edge).
- **→ M6 (RETRIEVEV, ASN-0115).** `value_at(a)` over a bound snapshot, after M6 resolves V→I (via M5). M4 does **not** own the registered-empty-vs-unallocated distinction — that is M6's, against M3's registry.
- **→ M9 (predicate-def read-back).** `value_at(a)` reads a def's bytes by its content start-address (the def's identity); def *creation* rides M5's composite, which calls `stage_write`.
- **→ engine crate.** `ContentStore` slice, `ContentWrite` record, `HasContent` trait, `apply_write` fold; the assembler implements `HasContent for World` and `From<ContentWrite> for Record`. It `From`-lifts and folds the record only — it never constructs a `ContentWrite` (private fields), so the `stage_write`-sole-constructor invariant survives assembly.
- **→ everyone.** `contains`/`value_at` mean **content-presence**, decoupled from allocation (M3) and registration (M3) — a content address can be allocated yet content-absent (a ghost). M4 is **never read by the link layer** (M7/M8); M7 is the parallel value-only store for `L`.

## Boundary — NOT provided here

- Does **not** mint or validate addresses (M3) — addresses arrive minted+validated; M4 trusts them.
- Does **not** arrange, reference, or place content, nor enforce referential integrity (M5) — M4 only *answers* the check via `contains`.
- Does **not** resolve V→I, attribute origin, compare versions, or surface SHOWORIGIN (M6 / M1 `document_of`).
- Does **not** store links — `L` is M7's parallel value store; M4 is never read by M7/M8.
- Does **not** own a journal, replay, snapshot, recovery, or checkpoint story (M2) — M4 supplies only the `ContentWrite` delta and a serde-able slice; M2 drives all of it.
- Does **not** distinguish registered-empty vs unallocated (M6, against M3's registry) — `value_at` returns `None` for any content-absent address.
- **No** modify / delete / GC / reclamation / refcount — write-once and permanent by construction.
- **No** value-as-identity and no content-addressed dedup at the interface (S4) — keyed by address only.
- **No** ordered iteration, range, or prefix scan — point queries only (`contains`, `value_at`).
- **No** concurrency of its own — content writes ride M5's composite under `key(d, s_C)`; serialization is M2's.
- Does **not** inspect or type the value bytes — `Val` is opaque; kind comes from the I-address (M1).
- Standalone `write` is **not** for production (violates J0) — test/isolation only.
