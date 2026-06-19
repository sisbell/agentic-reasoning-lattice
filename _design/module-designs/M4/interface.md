# M4 — Interface (for dependents)

M4 owns the permascroll: an append-only, write-once map from allocated I-address to opaque content `Val`, plus the two point queries over it — *is content stored here?* (`contains`) and *what is stored here?* (`value_at`).

## Public interface

### A. Engine-plug surface (slice / record / accessor / fold)

```rust
/// MUST be `BuildHasher + Default + Clone` so `ContentStore`'s `Default`/`Clone`/`Deserialize` derives hold.
type FixedHasher = BuildHasherDefault<FxHasher>;

/// M4's authoritative folded slice: dom(C) ↦ Val. The only state M4 owns.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct ContentStore { map: im::HashMap<Tumbler, Val, FixedHasher> }

/// M4's sole authoritative journal delta. FIELDS ARE PRIVATE: `stage_write` is the
/// compiler-enforced sole constructor.
#[derive(Clone, Serialize, Deserialize)]
pub struct ContentWrite { addr: Tumbler, val: Val }

/// The engine implements this for `World`; M4 reaches its slice off any `&W`.
pub trait HasContent { fn content(&self) -> &ContentStore; }

impl ContentStore {
    /// The fold — pure, total, deterministic. Insert only; never overwrites a live value.
    pub fn apply_write(&self, r: &ContentWrite) -> ContentStore;
}
```

### B. Read API (membership & value-at — point queries over a pinned slice)

```rust
impl ContentStore {
    /// S3 referential-integrity oracle: a ∈ dom(C). CONTENT-PRESENCE — not "allocated" and not "registered".
    pub fn contains(&self, a: &Tumbler) -> bool;

    /// C(a): the immutable value at a, else None. The returned borrow lives THROUGH the pinning Snapshot.
    pub fn value_at(&self, a: &Tumbler) -> Option<&Val>;

    pub fn len(&self) -> usize;        // |dom(C)| — diagnostics only
    pub fn is_empty(&self) -> bool;
}
```

### C. Write surface (the two composable forms)

```rust
/// PURE STEP — the storage half of K.α. Reads off a supplied working slice, returns the
/// record, commits nothing. Enforces S0's no-overwrite (`AlreadyPresent`); otherwise trusts the address.
pub fn stage_write(c: &ContentStore, addr: &Address, val: Val)
    -> Result<ContentWrite, ContentError>;

/// STANDALONE OP — the contract-required transact-wrapped form. ISOLATION/TEST USE ONLY:
/// committing a content write *alone* violates J0 (content-allocation ⇒ placement).
#[doc(hidden)]
pub fn write<W>(k: &Kernel<W>, addr: &Address, val: Val)
    -> Result<(Tumbler, Seq), TxnError<ContentError>>
where W: WorldState + HasContent, W::Record: From<ContentWrite>;
```

### Types & errors

```rust
/// Opaque, immutable content payload. M4 never inspects bytes.
#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Val(Arc<[u8]>);
impl Val { pub fn new(b: impl Into<Arc<[u8]>>) -> Val; pub fn as_bytes(&self) -> &[u8]; pub fn len(&self) -> usize; }

#[derive(Clone, Debug, PartialEq, Eq)]
#[non_exhaustive]
pub enum ContentError {
    /// A value is already stored at this address. Defensive — cannot occur in production.
    AlreadyPresent(Tumbler),
    /// Not a content-subspace element address. Ships only with the `content-addr-guard` feature.
    #[cfg(feature = "content-addr-guard")]
    NotContentAddress(Tumbler),
}
```

## Caller contracts & obligations

**`stage_write(c, addr, val) -> Result<ContentWrite, ContentError>`**
- Caller supplies the working slice — call it against `stg.working().content()` inside its own `transact`.
- `addr: &Address` must be already minted and validated upstream (M3); M4 trusts it and stores bytes.
- On `Ok`, lift the record with `.into()` and `stg.push(rec.into())`; `stage_write` commits nothing itself.
- `Err(AlreadyPresent(addr.tumbler()))` if `addr ∈ dom(C)` — never fires in correct operation (M3 mints fresh; M5 writes once); handle it as a clean rejection rather than a panic.
- With the `content-addr-guard` feature on, may also return `NotContentAddress` (routing check runs *before* the overwrite check).
- A caller **cannot** hand-build a `ContentWrite` (private fields) — `stage_write` is the only constructor; route every content write through it.

**`write<W>(k, addr, val) -> Result<(Tumbler, Seq), TxnError<ContentError>>`**
- `#[doc(hidden)]`, isolation/test use only — production content writes MUST ride M5's J0/J1★-coupled composite via `stage_write`, not this.
- Caller must satisfy `W: WorldState + HasContent` and `W::Record: From<ContentWrite>`.
- Returns `Err(TxnError<ContentError>)` on rejection (wrapping the same `ContentError` cases).

**`contains(a) -> bool`**
- Read off a `&ContentStore` obtained from a pinned snapshot (`snapshot().world().content()`).
- Means **content-presence**, decoupled from allocation/registration: a content address can be allocated yet content-absent (a ghost), and `contains` reports only presence.
- `a: &Tumbler` is the flat storage/journal key.

**`value_at(a) -> Option<&Val>`**
- Returns `None` if `a ∉ dom(C)`.
- The returned `&Val` borrows **through** the pinning `Snapshot` — caller MUST bind the snapshot to a local first (`let s = k.snapshot(); s.world().content().value_at(a)`); chaining off a temporary won't compile.
- Does **not** distinguish registered-empty vs unallocated — that distinction is M6's, against M3's registry.

**`apply_write(&self, r) -> ContentStore`** — engine-only fold; pure, total, deterministic, insert-only. The engine `From`-lifts and folds records; it never constructs a `ContentWrite`.

**`HasContent::content(&self) -> &ContentStore`** — engine implements for `World`; readers reach M4's slice off any `&W`.

**`Val`** — opaque, immutable bytes with no type tag; construct via `Val::new(impl Into<Arc<[u8]>>)`, read via `as_bytes`/`len`. *Kind* (text vs. else) is recovered from the I-address structure (M1), never from the value.

**Invariants a caller may rely on (M4 does not re-validate, but upholds):**
- Every `Address`/`Tumbler` M4 handles is T4-valid (M1 standing invariant).
- Write-once: a stored value never changes or vanishes — no modify/delete/GC/reclamation operation exists (S0/S1/C0).
- No-GC / unconditional permanence: unreferenced ("orphan") content persists; no refcount, no cap.
- Identity is by address, never value (S4): two equal byte-runs at two addresses are two distinct entries — no content-addressed collapse.
- Unbounded sharing (S5): M4 stores each address once and is indifferent to reference multiplicity.
- Store-disjointness: `dom(C) ∩ dom(L) = ∅` — M4 holds only content-subspace addresses.
- `ContentError` is `#[non_exhaustive]` — every downstream matcher MUST carry a wildcard arm (the variant set changes with the `content-addr-guard` feature).

## Seams exposed downstream

- **→ M5 (placement composite).** `stage_write(c, addr, val) -> Result<ContentWrite, _>` is the storage half of K.α that M5 composes inside its `transact([key(d, s_C)], …)`: call against `stg.working().content()`, then `stg.push(rec.into())`. `contains(a) -> bool` is the S3 referential-integrity oracle on the content side. The J0/J1★ couplings (content-alloc ⇒ placement ⇒ provenance) are M5's to enforce *around* the write; M4 contributes only the content-write step. M4 never reads M5 (no back-edge).
- **→ M6 (RETRIEVEV, ASN-0115).** `value_at(a) -> Option<&Val>` over a bound snapshot, after M6 resolves V→I (via M5). M4 does **not** own the registered-empty-vs-unallocated distinction — that is M6's, against M3's registry.
- **→ M9 (predicate-def read-back).** `value_at(a)` reads a def's bytes by its content start-address (the def's identity); def *creation* rides M5's composite, which calls `stage_write`.
- **→ engine crate.** `ContentStore` slice, `ContentWrite` record, `HasContent` trait, `apply_write` fold; the assembler implements `HasContent for World` and `From<ContentWrite> for Record`. The engine only `From`-lifts and folds the record — it never constructs a `ContentWrite` (private fields), so the `stage_write`-sole-constructor invariant survives assembly.
- **→ everyone.** `contains`/`value_at` mean **content-presence**, decoupled from allocation (M3) and registration (M3). M4 is **never read by the link layer** (M7/M8 do not touch it); M7 is the parallel value-only store for `L`.

## Boundary — NOT provided here

- Does **not** mint or validate addresses (M3) — addresses arrive already minted and T4-valid.
- Does **not** arrange, reference, or route content, and does **not** enforce referential integrity (M5 — M4 only *answers* the check via `contains`).
- Does **not** resolve V→I, attribute origin, or compare versions (M6); does **not** own the registered-empty-vs-unallocated distinction (M6).
- Does **not** store links / the `L` value store (M7).
- Does **not** own any journal, replay loop, snapshot, or recovery story (M2).
- No modify, delete, GC, reclamation, or refcount — never mutates, never deletes, never reclaims, never keys on the value.
- Stores **no** author/source/origin metadata — origin (S7) is established by M3 and computed structurally by M1, not held here.
- No ordered iteration, range, prefix-scan, or max-under-prefix surface — `Tumbler`'s `Ord` is deliberately unused; M4 relies only on `Eq + Hash`.
