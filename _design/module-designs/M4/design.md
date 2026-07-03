# M4 — Content Store (Istream) — Detailed Design

## Purpose & boundary

M4 is the permascroll: an append-only, write-once map from allocated I-address to opaque content value, plus the two point queries over it — *is content stored here?* and *what is stored here?* It owns the immutable, never-GC'd half of the two-layer state and **does exactly that one thing.** It does **not** mint addresses (M3), arrange or reference content (M5), enforce referential integrity (M5 — M4 only *answers* the check), resolve V→I, attribute origin, or compare versions (M6), store links (M7 — the parallel value store for `L`), or own a journal/snapshot/recovery story (M2). Addresses arrive as parameters already minted and validated upstream; M4 trusts them and stores bytes. The one-thing-well statement: **store an immutable value at an address forever, and look it up — never mutate, never delete, never reclaim, never key on the value.**

## Public interface

Three groups. The first is the engine-composition plug; the second is the read contract; the third is the write surface other stores compose.

### A. Engine-plug surface (slice / record / accessor / fold)

Named to match the Engine Composition Contract's assembler (`content: ContentStore`, `HasContent::content`, `apply_write`, `Record::Content(ContentWrite)`), so M4 drops into `skep-engine` unchanged.

```rust
/// Fixed-seed deterministic build-hasher → reproducible checkpoint serialization across runs.
/// MUST be `BuildHasher + Default + Clone + Send + Sync + 'static`: the first three so
/// `ContentStore`'s `Default`/`Clone`/`Deserialize` derives hold; the last three because
/// `ContentStore` becomes a field of the engine's `W`, and M2's `WorldState` bound requires
/// `Send + Sync + 'static` — a pick missing them surfaces as an opaque compile error in
/// `skep-engine`, far from the decision point that caused it. The *specific* hasher is Open
/// decision #5; this alias is the one place it is named.
type FixedHasher = BuildHasherDefault<FxHasher>;   // placeholder concrete pick — see Open #5

/// M4's authoritative folded slice: dom(C) ↦ Val. The only state M4 owns.
/// The `Serialize`/`Deserialize` derive requires the `im` crate built with its `serde` feature
/// (`im::HashMap`'s serde impls are feature-gated) — an M4-local dependency knob, not an upstream one.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct ContentStore { map: im::HashMap<Tumbler, Val, FixedHasher> }

/// M4's sole authoritative journal delta. Carries the FLAT Tumbler (M1: the
/// Tumbler is the storage/journal key; Address is the past-the-door value).
/// CONSTRUCTOR-PRIVATE, READ-PUBLIC: the fields are private so `stage_write` is the
/// compiler-enforced sole constructor — no caller can hand-build a record into the
/// total fold and skip the AlreadyPresent guard — while the `addr()`/`val()` accessors
/// and the `Debug` impl below give full read access (the S0(b) guard needs constructor
/// privacy only, not read privacy). serde deserializes the private fields for M2's
/// replay (derive expands at the definition site); the engine only `From`-lifts and
/// folds, never constructs one from scratch. This SATISFIES the composition-contract
/// checklist's "constructible by upstream producers, readable by downstream consumers"
/// item in full: the one sanctioned producer (`stage_write`) is public to M5, serde
/// replays at the definition site, and downstream consumers — including engine-side
/// journal-inspection/diagnostic tooling — read records through the public accessors
/// and `Debug`.
#[derive(Clone, Serialize, Deserialize)]
pub struct ContentWrite { addr: Tumbler, val: Val }

impl ContentWrite {
    pub fn addr(&self) -> &Tumbler;   // read-only; the sole constructor stays `stage_write`
    pub fn val(&self)  -> &Val;
}

/// MANUAL impl, not a derive: `Tumbler` (M1, as given) derives no `Debug`, so a derived
/// `Debug` would not compile against the upstream interface. Renders the address by its
/// components via Tumbler's public `len()`/`get(i)` (`Nat = BigUint` is `Debug`) and the
/// value by byte length.
impl fmt::Debug for ContentWrite { /* addr = [c₁, …, c_#t] via len/get; val = byte length */ }

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
    /// `None` CONTRACT for those callers: under S3 plus single-snapshot consistency, an
    /// I-address obtained from a successful V→I resolve against the SAME Snapshot always
    /// yields Some — a None there is an internal invariant violation (report/halt), never
    /// a domain-level "not found"; do not invent a user-visible not-found semantics from it.
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
///
/// Body (base build):
///   `if c.contains(addr.tumbler()) { Err(ContentError::AlreadyPresent(addr.tumbler().clone())) }
///    else { Ok(ContentWrite { addr: addr.tumbler().clone(), val }) }`.
/// With Open #4's `content-addr-guard` feature on, a routing check is PREPENDED (cfg-gated),
/// running BEFORE the overwrite check:
///   `#[cfg(feature = "content-addr-guard")]
///    if addr.level() != Level::Element || addr.subspace() != Some(S_C_SUBSPACE.clone()) {
///        return Err(ContentError::NotContentAddress(addr.tumbler().clone()));  // full-guard sub-choice;
///    }`                                                                        //  debug_assert! sub-choice panics instead
/// Check order: NotContentAddress (routing) precedes AlreadyPresent (overwrite), so a
/// mis-routed address is rejected on its own terms, never masked by a coincidental occupancy.
pub fn stage_write(c: &ContentStore, addr: &Address, val: Val)
    -> Result<ContentWrite, ContentError>;

/// STANDALONE OP — the contract-required transact-wrapped form. Generic over W.
/// ISOLATION/TEST USE ONLY: committing a content write *alone* creates content with no
/// placement, violating J0 (content-allocation ⇒ placement). Production content writes
/// MUST ride M5's J0/J1★-coupled composite via `stage_write`.
/// `#[doc(hidden)]` — exists ONLY to satisfy the contract's two-composable-forms rule; hidden
/// from docs so callers reach for M5's J0-coupled composite instead. The symbol is KEPT in the
/// production build (NOT `#[cfg(test)]`-gated) — the contract requires the form to exist.
/// Body: with `content-addr-guard` ON, the routing check is PREPENDED here too, BEFORE
/// lock-key derivation (mirroring the sub-choice: full-guard returns
/// `Err(TxnError::Rejected(ContentError::NotContentAddress(..)))`, debug_assert! panics) —
/// without this hoist a zeros<2 (Node/Account) input would panic at the `.expect` below
/// during key derivation before `stage_write`'s guard could fire, and "routing rejected on
/// its own terms" would hold on this path only for wrong-subspace *element* addresses.
/// Then (all builds): `let home = document_of(addr).expect("content address ⇒ zeros=3");` then
/// `k.transact(&[key(&home, s_C)], |stg| { let r = stage_write(stg.working().content(), addr, val)?;
/// stg.push(r.into()); Ok(addr.tumbler().clone()) })` — deriving the lock key via the shared
/// `key(...)` constructor with the `s_C` LockKey space-tag. A content address has zeros = 3, so
/// `document_of(addr)` is always `Some`; in the base build (guard off) the `.expect` IS the
/// trusted-address contract — it turns the unreachable `None` into a documented internal-invariant
/// violation on this trusted-address-only op, never a domain rejection.
#[doc(hidden)]
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

/// Content-subspace numeral — ASN-0093's SubspaceConventionAxiom fixes s_C = 1, matching M1's
/// documented `subspace()` convention (1 = text, 2 = link). Defined HERE, M4-locally, cfg-gated
/// with its only consumer (Open #4's routing guard): the feature is M4-local and off by default,
/// so a debug-only assertion does not warrant a shared-base-crate export, and the axiom-pinned
/// value cannot drift. `Nat` (BigUint) has no const constructor, hence a lazy static, not a
/// `const`. NOT the skep-kernel `s_C` LockKey space-tag — different constant, different layer.
#[cfg(feature = "content-addr-guard")]
pub(crate) static S_C_SUBSPACE: std::sync::LazyLock<Nat> =
    std::sync::LazyLock::new(|| Nat::from(1u32));

/// `#[non_exhaustive]`: the `content-addr-guard` feature adds/removes `NotContentAddress`,
/// changing the variant set across build configs, so every downstream matcher — chiefly M10's
/// surfacing of `TxnError::Rejected(ContentError)` — must carry a wildcard arm; flipping the
/// feature then cannot break a `match`.
#[derive(Clone, Debug, PartialEq, Eq)]
#[non_exhaustive]
pub enum ContentError {
    /// Defensive S0 guard: a value is already stored at this address. Cannot occur in
    /// production (M3 mints fresh; M5 writes once) — converts an upstream bug into a clean
    /// rejection instead of a silent permascroll overwrite.
    AlreadyPresent(Tumbler),
    /// Optional defense-in-depth (debug/off by default): not a content-subspace element
    /// address. Routing is M5's job, mint-conformance M3's — see Open build decision #4.
    /// SHIPS ONLY with Open #4: `cfg`-gated behind `content-addr-guard` so the base build
    /// carries no dead variant (and no dead `S_C_SUBSPACE` static / `subspace` / `Level`
    /// usage). Off by default; debug-only when on.
    #[cfg(feature = "content-addr-guard")]
    NotContentAddress(Tumbler),
}
```

## Core data model

**One authoritative structure, no derived hint.** M4's slice is `ContentStore { map: im::HashMap<Tumbler, Val> }` — the direct fold of `ContentWrite` records.

- **Why `im::HashMap` (not `OrdMap`).** M4's *entire* query surface is point membership (`contains`) and point value-at (`value_at`). Nobody needs ordered iteration, range, or prefix scans: the one consumer that would (M3's allocator, for "max content address under document `d`") reads **M3's own frontier**, never M4 — the DAG has no `M3 → M4` edge, and content allocation is decoupled from content storage (ghost elements). So pay nothing for ordering: HAMT gives O(1)-effective lookup/insert. (`OrdMap` is the fallback *only if* a content-prefix-scan consumer — e.g. "all content originated by `d`" — or a hot RETRIEVEV native-run range-fetch ever appears; today none does.)
- **Why persistent (`im::`) at all.** Not for snapshot-taking — M2's `Snapshot(Arc<Committed<W>>)` makes that an O(1) Arc clone of the whole `World`. It is for the **commit path**: each `transact` produces a *new* `World` via `apply`, and outstanding snapshots pin *old* Worlds. With `im::HashMap`, `apply_write` is O(log₃₂ n) and old/new maps share all untouched structure, so retaining prior versions for live snapshots is nearly free. A clone-on-write `std::HashMap` would copy the whole map per commit — untenable for a store that only grows.
- **Why `Val = Arc<[u8]>`, opaque.** Content is write-once, so a value is never edited and needs no internal persistent structure; an `Arc<[u8]>` is an immutable, O(1)-cloneable leaf (the map's structural sharing just bumps refcounts). M4 is **value-oblivious**: it never inspects bytes. *Kind* (text vs. anything else) is recovered from the I-address structure via M1 (`subspace`/`classify`), never from a stored tag — there is no type discriminator on the value (ASN-0036 content-typing).
- **Fixed (deterministic) hasher.** Keys are trusted internal tumblers, not adversarial input, so flooding-resistance buys nothing; pick a fixed-seed hasher (`FxHasher`-class, surfaced as the `FixedHasher` alias) so checkpoint serialization is reproducible across runs.
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
- **C-fin finiteness** (ASN-0093 C-fin): `|dom(C)| < ∞` — each commit adds finitely many entries and there is no growth path to infinity.
- **No-GC / unconditional permanence** (ASN-0036 S0 frame): no reclamation path, not refcount-gated.
- **S3 at every committed state** (ASN-0036 S3): because M5's composite writes content (M4) and places it (M5) in one atomic M2 transaction, no committed snapshot ever shows a placement referencing absent content — the strongest S3 timing, achieved by M2's atomicity, not by M4. (M4 supplies the oracle; M5 is the enforcer.)

**By active enforcement** (M4 must guard — located in `stage_write`):

- **S0(b) no-overwrite-of-occupied-address** (ASN-0036 S0; ASN-0093 C0): `stage_write` rejects `AlreadyPresent(addr)` because the total fold cannot; `ContentWrite`'s private fields make `stage_write` the compiler-enforced sole producer of the record, so the guard cannot be bypassed. This is M4's *one* genuine guard.

**Discharged upstream / cross-store — M4 relies on, does not re-enforce:**

- **T4-validity** of every address: M1's standing invariant (every `Address` is T4-valid).
- **C1 / C1b / L0** element-level, `#E≥2`, content-subspace numeral `S_C_SUBSPACE` (ASN-0093's `s_C` = 1; see Dependencies for why M4 keeps this address numeral distinct from the `s_C` LockKey space-tag): M3 mints conforming content addresses; M5 routes content V-positions to M4. M4 stores by-address; an optional boundary assertion (`NotContentAddress`, Open #4) is defense-in-depth, not the source of truth.
- **C1c allocator conformance, C2 origin-registered scoping** (ASN-0093): M3's mint + register-before-allocate gate.
- **S7 structural attribution** (ASN-0036 S7): a *theorem* established by the allocation discipline (S7a/S7b/S7d, T4, T10a — all M3) and computed pointwise by M1's `document_of` (surfaced as the SHOWORIGIN operation in M6); M4 neither establishes nor enforces it. M4's lone, complementary contribution is by-construction: it stores **no** author/source/origin metadata — only `address → Val` — so there is no redundant origin field that could diverge from the structural origin.
- **SD store-disjointness** (`dom(C) ∩ dom(L) = ∅`, ASN-0093, from L0 + SC-NEQ + StoreT4Validity + T7): a cross-store guarantee M4 cannot enforce alone. StoreT4Validity discharges T7's T4-validity precondition (with `zeros(·) = 3` from C1/L1 discharging the rest); M4 upholds its half by storing only the content-subspace (`S_C_SUBSPACE`) addresses M5 routes to it, with M7 the disjoint `L` value store. The optional `NotContentAddress` assertion (Open #4) is M4's only local guard against a mis-routed `s_L` address ever landing in `dom(C)`.

## Dependencies & seams

**Upstream — concrete use:**

- **M1.** `Tumbler` (slice/record key — M4 relies only on its `Eq + Hash` for the `im::HashMap`, never `Ord`; see Conflict #3 for why ordering is deliberately unused), `Tumbler::len`/`get` (the manual `Debug` rendering of `ContentWrite` formats address components through them — `Tumbler` as given derives no `Debug`), `Address` (the value `stage_write`/`write` accept — fresh from M3's `checked_inc`), `document_of` (derive the lock key for the standalone op), and — *only if* the optional content-address assertion is on (Open #4, `cfg(content-addr-guard)`) — `subspace`/`Level` (the guard body uses only `level()` and `subspace()`; `classify` is not needed). The content-subspace numeral `S_C_SUBSPACE: Nat` the guard compares against is **defined M4-locally** under the same gate (see Types & errors), not imported: the feature is M4-local and off by default, so a debug-only guard warrants no shared-crate export, and the value (1) is pinned by ASN-0093's SubspaceConventionAxiom — matching M1's documented `subspace()` convention (1 = text) — so local definition cannot drift; it is *not* the skep-kernel LockKey tag. These guard usages are cfg-gated behind `content-addr-guard`, so the base build carries none of them dead. No span/span-set use: M4 stores scalar values, not spans.
  - **Serde preconditions (M1's part already met; the rest are M4-local).** M4's slice (`ContentStore`) and record (`ContentWrite`) both `#[derive(Serialize, Deserialize)]`, which requires `Tumbler: Serialize + DeserializeOwned` (and transitively `Nat = BigUint: Serialize`). **M1 as given already provides this:** it derives `#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]` on both `Tumbler` and `Address`, and its overview already requires `num-bigint` built with its `serde` feature. M4 relies on that standing M1 guarantee — there is no missing upstream derive and nothing to escalate. The serde knobs M4 must turn on are **local to M4's own dependencies**: (i) the `im` crate's `serde` feature, since `im::HashMap`'s `Serialize`/`Deserialize` impls are feature-gated (this is what makes `ContentStore`'s derive compile); and (ii) serde's `rc` feature for the `Arc<[u8]>` impls behind `Val` (already flagged at `Val`'s definition; the rc-free `&[u8] ⇄ Vec<u8>→Arc::from` round-trip is the alternative). M4 owns the `im` and `serde` dependencies, so it enables both features itself.
- **M2.** Provides `apply`-driven commit + replay (engine wires `apply_write`), `Snapshot`/`world()` (readers obtain `&ContentStore`), `Kernel::transact` (standalone `write` only), `LockKey`, `Seq`. **M4 owns no journal, replay, snapshot, or recovery** — all M2's. The per-(document, content-subspace) `LockKey` must be byte-identical across M3 alloc / M4 write / M5 placement, so M4 imports both pieces from their composition-contract homes rather than re-spelling either — and those homes are *split* by what each names: the `s_C` **LockKey space-tag** (the 1-byte content-subspace discriminator the key carries) names only M2 types, so it lives in **`skep-kernel`** beside the central 1-byte space-tag enum the key draws its tag from; the `key(home: &Address, …) -> LockKey` *constructor* names **both** `Address` (M1) and `LockKey` (M2), so it cannot live in `skep-kernel` (M2 has no edge to M1) and instead lives in the **shared base crate over `skep-address` + `skep-kernel`**. M4 imports the `s_C` tag from `skep-kernel` and `key(...)` from the shared base crate; it does not re-define `key(...)` or re-spell the `s_C` tag locally, and neither do M3 or M5 — the three modules emit identical bytes precisely because there is exactly one source for each. This `s_C` tag is the *only* `s_C` on M4's core path; the homonymous **address-subspace numeral** (`S_C_SUBSPACE: Nat`, ASN-0093's `s_C = 1`) is a different constant at a different layer (an M4-local, cfg-gated lazy static pinned by ASN-0093's SubspaceConventionAxiom — see Types & errors), enters M4 only through Open-#4's optional assertion, and is never the byte the lock key carries — keeping the two apart is what makes that assertion typecheck (`addr.subspace(): Option<Nat>` compares against the `Nat` numeral, never the kernel tag).

**Downstream — seam contracts neighbors build against:**

- **→ M5 (placement composite).** `stage_write(c, addr, val) -> Result<ContentWrite, _>` is the storage half of K.α that M5 composes inside its `transact([key(d, s_C)], …)`: M5 calls it against `stg.working().content()`, then `stg.push(rec.into())` (engine's `From<ContentWrite> for Record`). `contains(a) -> bool` is the S3 referential-integrity oracle on the content side. The J0/J1★ couplings (content-alloc ⇒ placement ⇒ provenance) are M5's to enforce *around* the write; M4 contributes only the content-write step. M4 never reads M5 (no back-edge).
- **→ M6 (RETRIEVEV, ASN-0115).** `value_at(a) -> Option<&Val>` over a bound snapshot, after M6 resolves V→I (M5). Per `value_at`'s `None` contract, an I-address obtained from a successful V→I resolve against the *same* Snapshot always yields `Some`; M6 must treat `None` there as an internal invariant violation, never invent a user-visible not-found from it. M4 does **not** own the registered-empty-vs-unallocated distinction — that is M6's, against M3's registry.
- **→ M9 (predicate-def read-back).** `value_at(a)` reads a def's bytes by its content start-address (the def's identity); def *creation* rides M5's composite, which calls M4's `stage_write`. The same `None` contract applies: a registered def's start-address always yields `Some` (S0/S1 permanence of `dom(C)`); `None` is an internal invariant violation, not a domain-level not-found.
- **→ engine crate.** `ContentStore` slice, `ContentWrite` record, `HasContent` trait, `apply_write` fold; the assembler implements `HasContent for World` and `From<ContentWrite> for Record`. It `From`-lifts and folds the record only — it never constructs a `ContentWrite` (private fields), so the `stage_write`-sole-constructor invariant survives assembly; engine-side journal-inspection/diagnostic tooling reads records through the public `addr()`/`val()` accessors and the manual `Debug`.

**Seam clarifications the builder must hold:** M4's `contains`/`value_at` mean **content-presence**, decoupled from allocation (M3) and registration (M3) — a content address can be allocated yet content-absent (a ghost), and M4 reports presence only. M4 is **never read by the link layer** (M7/M8 don't touch it); M7 is the parallel value-only store for `L`. M4 reads no module above M1/M2.

## Conflicts resolved

The two source notes largely agree on M4's territory; the substantive resolutions are against M2's re-homing and the M3/M4 split, not between the notes.

1. **Journal & recovery ownership** (both notes: "append-only journal recovered by replay," owned by the store). Resolved against M2: M4 owns no journal/replay/snapshot/recovery; `ContentWrite` is the authoritative delta M2 journals, the `im::HashMap` is its fold, and M2 drives recovery. The notes' "the in-memory index is a recomputable hint over the journal" becomes "the map is M4's authoritative slice, itself the fold of M2's journal" — same recomputability, ownership moved to the kernel. *Why:* the whole corpus leans on one recovery story; duplicating it in M4 would be redundant authoritative machinery.

2. **Membership semantics, and the M5 seam's "allocated in M4, checked via M3."** ASN-0093's invariants are about *allocation*; ASN-0036's S3 is about `dom(C)` *content-presence*. Resolved: S3's canonical oracle is M4's `contains` (content-presence); "allocated" (M3) and "content-present" (M4) **coincide** for content addresses written through M5's J0-coupled composite, so M5 may also check registration/allocation via M3 for the source-exists precondition, but the referential-integrity test proper is M4's `contains`. *Why:* keeps S3 exactly where the formal statement puts it (`dom(C)`), and keeps M4 free of any M3 dependency.

3. **Ordered tumbler map vs hash** (ASN-0093 recommends an *ordered* map for the allocator's max-under-prefix and prefix-range scans). Resolved by the M3/M4 split: M4 hosts no allocator and has no prefix-scan consumer, so the ordered-map rationale applies to M3's frontier, not M4's content map — M4 picks `im::HashMap`. *Why:* don't pay for ordering nobody queries. **Reconciling the M2 seam phrasing:** M2's placement-composite example reads "Each K.α mints from `stg.working().content()` + M1's pure `inc`." The minting **frontier** that `inc` advances there is **M3's content sub-allocator, held in M3's namespace slice** — the per-(d, s_C) content frontier — *not* M4's `ContentStore` value map and *not* `HasContent::content`. There is no `M3 → M4` edge and content allocation is decoupled from content storage (ghost elements), so the mint reads M3's frontier and never M4's map. M4's own `stg.working().content()` reads — inside `stage_write`, and in M5's placement step that calls it — touch M4's value map only to enforce S0(b) no-overwrite, never to mint. This is exactly why M4 owes no max-under-prefix / ordered-iteration surface and needs no `Ord` on `Tumbler`; a reader cross-referencing M2 must not infer that the `content()` in that example is `HasContent::content`. **Erratum routed upstream:** this reconciliation must not live only inside M4 — M2's M5-seam sentence ("Each K.α mints from `stg.working().content()`") is flagged for correction in the M2 and M5 documents themselves, to read the content-allocation frontier in M3's `ns()` slice; a future M5 builder reading M2's text cold would otherwise trip on the same phrase.

4. **Unified `C+L` store (ASN-0093) vs split (M4/M7).** Resolved by the decomposition: M4 owns only `C`; `L` is M7's parallel value-only store. The append-only by-address mechanism is shared but instantiated separately, and M4 stores only content-subspace values.

5. **`Val` typing** (ASN-0036 leaves it open — uniform? tagged?). Resolved: opaque untyped bytes, no value tag; kind is recovered from the I-address structure (M1). The differing element-field numbering across the notes' examples doesn't reach M4 — M4 stores by whatever address it's handed and, in its base build, depends on no specific subspace *numeral* at all: the lock key carries the `s_C` LockKey space-tag (skep-kernel), not the address-level subspace numeral, and the `S_C_SUBSPACE` numeral is consulted only by Open-#4's optional assertion.

## Open build decisions

1. **Inline vs out-of-line values.** Default: inline `Val(Arc<[u8]>)` in record and slice — simplest, bytes durable in M2's journal, good for many small text atoms. Switch to an out-of-line blob store (slice holds `address → blobref`) **when** content volume makes per-checkpoint slice serialization the bottleneck — it shrinks the serialized slice and cheapens M2's checkpoints, at the cost of reintroducing a blob-durability concern (either M4-owned, a deviation from "M2 owns durability," or rebuildable by replaying M2's `ContentWrite` records, which still carry the bytes). **Hard constraint on any out-of-line variant:** M2's `apply` obligation — deterministic, total, side-effect-free — forbids blob-file I/O inside the fold, so blobs must be materialized *outside* `apply`: written at stage/commit time before the record reaches the fold, or reconstructed as a `rebuild_derived`-seeded cache; `apply` itself folds only the pure `address → blobref` entry. Pick under measurement of content-size distribution and checkpoint cost.
2. **Internal value-dedup (CAS-underneath).** Optional `value-hash → blobref` compression layer beneath the map (many addresses → one stored byte-run), naturally paired with out-of-line blobs. Pure optimization; **must never surface as identity** (S4). If skip-serialized, it becomes the one derived hint requiring an engine `rebuild_derived` contribution. Enable only if content has high byte-level duplication and space matters.
3. **Record granularity.** Single `ContentWrite` per atom (matches K.α, `m` records per INSERT) vs a batched `ContentWriteRun { writes: Vec<(Tumbler, Val)> }` folded as `m` inserts. Default single; batch if per-record overhead in M2's journal dominates for large contiguous inserts. (A batched record keeps private fields + a `stage_write`-style sole constructor — and the same read-accessor/`Debug` surface — for the same S0(b) guarantee.)
4. **Defensive content-address assertion strength.** `stage_write` can additionally check `addr.level()==Element ∧ addr.subspace()==Some(S_C_SUBSPACE)` (→ `NotContentAddress`), where `S_C_SUBSPACE` is the content-subspace numeral defined **M4-locally** under the same feature gate (see Types & errors; value 1, pinned by ASN-0093's SubspaceConventionAxiom and matching M1's documented `subspace()` convention — *not* the `s_C` LockKey space-tag, against which `addr.subspace(): Option<Nat>` would not even typecheck). This whole surface — the added check in `stage_write` (which runs *before* the `AlreadyPresent` overwrite check, per the body sketch), the matching check PREPENDED in the standalone `write` before lock-key derivation (§C — without it, a zeros<2 input would panic at the `.expect` before the guard could fire), the `NotContentAddress` variant, the `S_C_SUBSPACE` static, and the `subspace`/`Level` usage — is `cfg`-gated behind the `content-addr-guard` feature so the base build stays dead-code/unused-import clean. Choose: full runtime guard (paranoid, returns `NotContentAddress`), `debug_assert!` only (recommended — catches routing bugs in test, free in release), or off (trust M5's routing + M3's mint entirely). Recommend debug-only, with the feature off by default.
5. **HashMap hasher.** A fixed-seed deterministic hasher is decided (reproducible checkpoints), surfaced as the `FixedHasher` alias on `ContentStore`'s `map`; the *specific* type that alias resolves to (`BuildHasherDefault<FxHasher>` / fixed-key SipHash / aHash-fixed-seed) is a minor pick under microbenchmark, constrained only to be `BuildHasher + Default + Clone + Send + Sync + 'static` — the first three so the slice's `Default`/`Clone`/`Deserialize` derives hold, the last three because `ContentStore` is a field of the engine's `W` and M2's `WorldState` bound requires `Send + Sync + 'static` (a non-conforming pick fails to compile in `skep-engine`, far from the decision point that caused it).
6. **`value_at` return type — borrowed vs cloned.** Default `Option<&Val>`, which ties the value's lifetime to the pinning `Snapshot` (caller binds the snapshot first). Since `Val` is `Arc<[u8]>` with O(1) clone, returning `Option<Val>` would decouple the value's lifetime from the snapshot for callers like M6/M9, at the cost of one Arc refcount bump per read. Minor ergonomics call; default to the borrowed form, switch to cloned if the snapshot-lifetime coupling proves awkward at a call site.
