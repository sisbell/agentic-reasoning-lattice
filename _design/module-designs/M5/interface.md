# M5 — Interface (for dependents)

M5 owns every document's mutable **V→I arrangement** (the POOM — a content subspace + a link subspace per document) and the append‑only content‑provenance relation **R**; it is the only place destructive change lives, exposing editing/versioning ops, link seating for M7, forward/reverse arrangement reads, and the R read surface.

## Public interface

Types `Tumbler/Address/Span/SpanSet/Nat/Level` are M1's; `Kernel/Snapshot/LockKey/Seq/TxnError/WorldState` are M2's; `MintError/PrincipalId/M3Rec/HasM3` are M3's; `Val/ContentWrite/ContentError/HasContent` are M4's. The slice is reached through an accessor trait the engine implements; write‑driving ops are generic over `W` with the upstream `From` bounds.

```rust
pub trait HasM5 { fn m5(&self) -> &M5State; }   // engine: W: WorldState + HasM5
// Subspace convention (ASN-0047): s_C = 1 (content), s_L = 2 (link), value-equal across the system.
//   V-positions are depth-2 tumblers [subspace, ordinal] (m = 2).
```

### A. Engine‑plug surface (slice / record / Run / fold)

```rust
/// Authoritative folded state: per-document POOM + provenance. MUTABLE, recovered by replay.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct M5State { /* private */ }

/// M5's sole journal delta — effect-level. Variants are `#[non_exhaustive]`: no foreign crate
/// can build an `M5Rec` by struct literal; the engine only `From`-lifts and folds it.
#[derive(Clone, Serialize, Deserialize)]
pub enum M5Rec {
    #[non_exhaustive] ContentPlace   { doc: Address, at: Nat, runs: Vec<Run> },  // INSERT/COPY: splice + R-append
    #[non_exhaustive] ContentRemove  { doc: Address, from: Nat, width: Nat },    // DELETE: contract+reseat (no C, no R)
    #[non_exhaustive] ContentReorder { doc: Address, cuts: Vec<Nat> },           // REARRANGE: 3|4 cut ordinals (no C, no R)
    #[non_exhaustive] LinkSeat       { doc: Address, link: Address },            // MAKELINK seating (no R — J-LV)
    #[non_exhaustive] VersionSnapshot{ source: Address, new: Address },          // CREATENEWVERSION (share + R-append)
}

#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
#[non_exhaustive]                                          // seals foreign struct-literal construction
pub struct Run { pub i_start: Address, pub width: Nat }    // standing invariants: EVERY Run has width ≥ 1 AND i_start is element-level (zeros = 3)

impl Run {
    /// Checked constructor — the seam guard for an EXTERNAL producer (none in v1).
    pub fn new(i_start: Address, width: Nat) -> Option<Run>;     // None ⇔ width == 0 ∨ zeros(i_start) ≠ 3

    /// The ONE admissible Run→Span lift: the level-uniform, element-level I-extent
    /// [i_start, shift(i_start, width)). Total given the two standing invariants; never faults.
    pub fn iextent(&self) -> Span;
}

impl M5State {
    pub fn genesis() -> M5State;                       // {} arrangements, {} provenance
    pub fn apply_m5(&self, r: &M5Rec) -> M5State;      // the pure/total/deterministic M2 fold
    pub fn rebuild_derived(self) -> M5State;           // default identity in v1 (no skip-serialized hints)
}
```

### B. Editing & versioning — transact‑driving ops (M10, and INSERT for M9)

```rust
pub struct Vstream<'k, W: WorldState> { /* holds &'k Kernel<W> */ }

impl<'k, W> Vstream<'k, W>
where W: WorldState + HasM5 + HasM3 + HasContent,
      W::Record: From<M5Rec> + From<M3Rec> + From<ContentWrite>   // union bound; each op uses a subset
{
    /// Mint n fresh content addresses (M3), write bytes (M4), splice the run at `at`, record
    /// provenance — one M2 composite. Returns the inserted run's START address + the Seq.
    pub fn insert(&self, doc: &Address, at: VPos, values: Vec<Val>)
        -> Result<(Address, Seq), TxnError<InsertError>>;

    /// Transclude existing content by reference; splice into doc's content subspace at `at`,
    /// record provenance. Allocates NO content.
    pub fn copy(&self, doc: &Address, at: VPos, specs: Vec<VSpec>)
        -> Result<Seq, TxnError<CopyError>>;

    /// Remove content range [p, p+width) and close the gap. Content store and R untouched.
    pub fn delete(&self, doc: &Address, p: VPos, width: Nat)
        -> Result<Seq, TxnError<DeleteError>>;

    /// Pivot (3 cuts) / swap (4 cuts) transpose in the content subspace. Pure permutation;
    /// content, links, R untouched.
    pub fn rearrange(&self, doc: &Address, cuts: Vec<VPos>)
        -> Result<Seq, TxnError<RearrangeError>>;

    /// Fork: mint a new identity (M3), install its content arrangement as a snapshot of d_src's
    /// content subspace, record provenance. Returns the new document address + Seq.
    pub fn version(&self, principal: PrincipalId, d_src: &Address)
        -> Result<(Address, Seq), TxnError<VersionError>>;
}
```

### C. Link seating — pure step composed into M7's MAKELINK

```rust
/// Append an already-allocated home link at doc's next link V-position. SEMANTICS-BLIND: trusts
/// M7 that `link ∈ dom(L)`; checks only CL-OWN and CL-UNIQ. Returns the delta; M7 lifts via `.into()`.
pub fn stage_seat_link(m5: &M5State, doc: &Address, link: &Address) -> Result<M5Rec, SeatError>;

/// STANDALONE transact-wrapped twin of `stage_seat_link`. ISOLATION/TEST USE ONLY — production
/// seats through MAKELINK; committing a seat alone is not a production path.
#[doc(hidden)]
pub fn seat_link<W>(k: &Kernel<W>, doc: &Address, link: &Address)
    -> Result<(Address, Seq), TxnError<SeatError>>
where W: WorldState + HasM5, W::Record: From<M5Rec>;
```

### D. Arrangement reads — pure, over any M2 snapshot (M6, M8)

```rust
impl M5State {
    /// V→I resolution: I-runs covering an ORDINAL-LEVEL depth-2 V-span, V-ordered, clipped.
    /// DEFENSIVE (no Result, cannot fault): returns ⟨⟩ unless `#start == 2 ∧ #width == 2 ∧
    /// span.width().get(1) == 0`; absent doc ⇒ ⟨⟩.
    pub fn resolve(&self, doc: &Address, span: &Span) -> Vec<Run>;
    pub fn point(&self, doc: &Address, v: &VPos) -> Option<Address>;       // M(d)(v)

    /// V→I coverage as a SpanSet: ⋃ r.iextent() over `resolve`'s runs. Total, NOT normalized,
    /// possibly mixed-length — consume under the level-class discipline (per-level-class keys).
    pub fn resolve_coverage(&self, doc: &Address, span: &Span) -> SpanSet;

    pub fn content_runs(&self, doc: &Address) -> Vec<Run>;                 // canonical, V-ordered (COMPARE)
    pub fn link_runs(&self, doc: &Address) -> Vec<Run>;
    pub fn content_count(&self, doc: &Address) -> Nat;                     // n_C(d)
    pub fn link_count(&self, doc: &Address) -> Nat;                       // n_L(d)

    /// I→V (content subspace ONLY): V-positions whose CONTENT I-address falls in `coverage`. Total;
    /// applies the level-class discipline internally, so fault-free for any coverage.
    pub fn project(&self, doc: &Address, coverage: &SpanSet) -> SpanSet;
}
```

### E. Provenance reads — pure (M6: SHOWDELETIONS, FINDDOCSCONTAINING)

```rust
impl M5State {
    pub fn ever_placed(&self, doc: &Address) -> SpanSet;   // R↾doc; raw, possibly mixed-length — consume under the level-class discipline

    /// SHOWDELETIONS primitive: `ever_placed(doc) ∖ content_image(doc)`, computed PER LEVEL-CLASS
    /// inside M5. M6 reads it straight off; fault-free.
    pub fn deletions(&self, doc: &Address) -> SpanSet;

    /// R⁻¹ candidate documents (distinct, deterministic Tumbler order). `Vec<Address>` because
    /// `Address` is not `Ord`. Overlap-superset (no false negatives) — narrow with `project`.
    pub fn docs_containing(&self, coverage: &SpanSet) -> Vec<Address>;
}
```

### Errors & helper types

```rust
pub struct VPos { pub subspace: Nat, pub ordinal: Nat }   // depth-2 V-position [subspace, ordinal]
pub struct VSpec { pub source: Address, pub span: Span }   // one source-span for COPY

pub enum InsertError   { DocNotRegistered, BadPosition, EmptyContent, Mint(MintError), Content(ContentError) }
pub enum CopyError     { DocNotRegistered, BadPosition, SourceNotRegistered, EmptySource,
                         BadSpan, NotContentSubspace, DanglingSource, EmptyResult }
pub enum DeleteError   { DocNotRegistered, NotContentSubspace, NotArranged, OutOfBounds, EmptyWidth }
pub enum RearrangeError{ DocNotRegistered, BadCutCount, NotAscending, NotContentSubspace, OutOfBounds, EmptyContentSubspace }
pub enum VersionError  { SourceNotRegistered, NotAPrincipal, NodeTierCrossOwner, Mint(MintError) }   // NodeTierCrossOwner: P-tier excludes a node-tier cross-owner fork (ASN-0123)
pub enum SeatError     { NotHomeLink, AlreadySeated }

impl From<MintError>    for InsertError  { fn from(e: MintError)    -> Self { InsertError::Mint(e) } }
impl From<ContentError> for InsertError  { fn from(e: ContentError) -> Self { InsertError::Content(e) } }
impl From<MintError>    for VersionError { fn from(e: MintError)    -> Self { VersionError::Mint(e) } }
```

## Caller contracts & obligations

**`insert(doc, at, values)`**
- Caller discharges: `doc` registered (else `DocNotRegistered`); `values` non‑empty (else `EmptyContent`); `at` a valid insertion position — subspace = s_C, depth 2, ordinal ∈ [1, n_C+1] (or = 1 if n_C = 0) (else `BadPosition`).
- May rely on: alloc+write+place+R‑append ride one M2 composite (J0/J1★); returns the inserted run's START address (the predicate‑def identity for M9) and the commit `Seq`.
- Handle: `Mint(MintError)`, `Content(ContentError)`; any `TxnError::Rejected(E)` leaves no state change.

**`copy(doc, at, specs)`**
- Caller discharges: `doc` registered + `at` valid (as INSERT); per spec — `source` registered (`SourceNotRegistered`), source content non‑empty (`EmptySource`), `span` an ordinal‑level depth‑2 V‑span (`BadSpan`) in the content subspace, `span.start().get(1) == s_C` (`NotContentSubspace`); resolved run starts ∈ dom(C) (`DanglingSource`); net placement non‑empty (`EmptyResult`).
- May rely on: transcludes by reference, allocates NO content; cross‑origin runs preserved (never coalesced); source POOMs read off the composite's consistent base (no source lock needed); placed‑run provenance recorded. Returns `Seq`.

**`delete(doc, p, width)`**
- Caller discharges: `doc` registered (`DocNotRegistered`); subspace(p) = s_C (`NotContentSubspace`); `p` arranged (`NotArranged`); `ordinal(p)+width−1 ≤ n_C` (`OutOfBounds`); `width ≥ 1` (`EmptyWidth`).
- May rely on: gap closes; content store and R untouched (NonDestruction); links survive. Returns `Seq`.

**`rearrange(doc, cuts)`**
- Caller discharges: `doc` registered; 3 or 4 cuts (`BadCutCount`); strictly ascending (`NotAscending`); all subspace = s_C at depth 2 (`NotContentSubspace`); `1 ≤ ord(c₀)` and `ord(c_last) ≤ n_C+1` (`OutOfBounds`); content subspace non‑empty (`EmptyContentSubspace`).
- May rely on: pure cut‑determined, value‑blind permutation; content, links, R untouched. Returns `Seq`.

**`version(principal, d_src)`**
- Caller discharges: `d_src` registered (`SourceNotRegistered`); `principal` is a principal (`NotAPrincipal`); a cross‑owner fork needs an account‑tier forker — node‑tier cross‑owner rejected (`NodeTierCrossOwner`).
- May rely on: mints a new identity, installs a multiplicity‑preserving snapshot of d_src's content (V→I map, not the I‑range), records provenance; source untouched, fork diverges copy‑on‑write. Returns new doc address + `Seq`. Handle `Mint(MintError)`.

**`stage_seat_link(m5, doc, link)` (M7)**
- Caller (M7) discharges: `link ∈ dom(L)` — M5 trusts this and never reads M7. M5 checks CL‑OWN (`origin(link) = doc` → `NotHomeLink`) and CL‑UNIQ (not already seated → `AlreadySeated`).
- May rely on: returns an `M5Rec` to lift via `.into()` and stage; appends NO provenance (J‑LV).

**`seat_link<W>(k, doc, link)`** — `#[doc(hidden)]`, isolation/contract‑parity testing only; not a production path. Same checks; returns seated link address + `Seq`.

**Reads (`resolve`, `point`, `resolve_coverage`, `content_runs`, `link_runs`, `content_count`, `link_count`, `project`, `ever_placed`, `deletions`, `docs_containing`)**
- Pure over any M2 `Snapshot`; `(M, R)` is one consistent root — a reader never observes M‑updated‑without‑R.
- Absent doc ⇒ empty result (⟨⟩ / `[]` / `0` / `None`); **M5 does not distinguish registered‑empty from unallocated** — disambiguate via M3.
- `resolve` cannot fault (no `Result`): returns ⟨⟩ on any span that is not a usable ordinal‑level depth‑2 V‑span; out‑of‑range is accept‑and‑intersect (silently clipped).
- `resolve_coverage` / `ever_placed` return **raw, un‑normalized, possibly mixed‑length** covers — consume under the level‑class discipline; M7 must form coverage‑class dedup keys **per level‑class** (one `canonical_key` per endpoint‑length partition), never one `canonical_key` over the raw cover (else `LevelMismatch`).
- `project` / `deletions` apply the level‑class discipline internally — fault‑free for any `coverage`/doc, including cross‑length prefix/subtree spans.
- `docs_containing` is an overlap‑superset (no false negatives); narrow each candidate by `project(d, coverage) ≠ ⟨⟩`.

**Invariants a caller may lean on**
- Every `Address` returned (insert start, `point`, `resolve`/`content_runs`/`link_runs` run `i_start`, `version` new doc) is **T4‑valid**; content I‑starts are **element‑level (`zeros = 3`)**.
- Every `Run` returned has **`width ≥ 1`** and an **element‑level `i_start`**; `Run::iextent` is therefore total. M5 hands out only `&Run`/owned `Run`, never `&mut Run` — fields are read‑only across seams.
- `Run::new` returns `None` ⇔ `width == 0 ∨ zeros(i_start) ≠ 3`; `Run` is `#[non_exhaustive]`, so `Run::new` is the sole external constructor.
- `M5Rec` variants are `#[non_exhaustive]`: build only via `stage_*`/op bodies; the engine moves the whole record (`From`‑lift + fold), never destructures it.
- `apply_m5` is pure/total/deterministic, reads only `M5State` + M1 arithmetic, never re‑mints; `rebuild_derived` is identity in v1.
- Maps key by `Tumbler` (the `Ord`‑bearing type), not `Address`; callers pass `&Address` and M5 converts.

## Seams exposed downstream

- **→ M6** — `resolve`/`point` (RETRIEVEV, extent queries; COMPARE via `content_runs` across docs off one snapshot); `deletions` (SHOWDELETIONS — read straight off it; M5 does the per‑level‑class difference); `docs_containing` + `project` (FINDDOCSCONTAINING: candidate superset narrowed by `project(d, region) ≠ ⟨⟩`). One consistent `(M, R)` snapshot. **M5 owns R and any index over it; M6 owns only the composing query.**
- **→ M7** — `resolve_coverage` (endset V‑regions → I‑coverage `SpanSet`, the centralized `iextent` lift; inherits the per‑level‑class dedup‑key warning) and `stage_seat_link` (pure step folded into MAKELINK, returns `M5Rec`; `#[doc(hidden)]` twin `seat_link<W>` for isolation/parity only). M5 never reads M7.
- **→ M8** — `resolve`/`resolve_coverage` (V→I image), `project` (I→V **content** footprint, fragmentation‑ and length‑class‑tolerant), `content_count`/`link_count`.
- **→ M9** — `Vstream::insert` for predicate‑definition content (rides M5's placement composite, satisfies J0); returns the def's content start‑address as its identity.
- **→ M10** — `insert`/`delete`/`copy`/`rearrange`/`version`, each one `transact` returning `(…, Seq)`; surface `TxnError::Rejected(E)` as typed rejections.
- **→ engine** — `M5State` slice, `M5Rec` record, `HasM5` accessor, `apply_m5` fold, `genesis`; assembler implements `HasM5 for World`, `From<M5Rec> for Record`, dispatches `Record::M5(x) => world.m5().apply_m5(x)` (moving the whole record). M5 contributes **no `Space` lock‑key tag** — every mutation serializes under an **M3** lock key (`content_lock_key`/`version_lock_key`/`document_lock_key`; link seating under M7's `link_lock_key`).
- **Build precondition** — `M5State` serialization needs the `im` crate's `serde` feature and `Tumbler: Serialize/DeserializeOwned`.

## Boundary — NOT provided here

- **No content bytes and no address minting** — M5 orchestrates M4 writes and M3 mints at its composite, but owns neither.
- **No link values or link semantics** — M5 seats an opaque, already‑allocated home‑link address and never reads M7; **interior link withdrawal is not offered**.
- **No link‑to‑link reverse discovery** — `project` is **content subspace only** (no subspace argument); link reverse‑discovery is M7's BH3.
- **No document registration** — a fresh document's arrangement is implicit/empty until M5 first touches it (eager‑lazy split with M3).
- **No content/link *queries*** — M5 exposes the read primitives; RETRIEVEV/SHOWDELETIONS/FINDDOCSCONTAINING are M6's, inverse‑arrangement queries M8's.
- **No `content_image` seam** — it is the M5‑internal `deletions` operand, never public; no raw length‑gated op or mixed‑length cover is differenced/intersected across the M6 boundary.
- **No ordering, durability, or recovery** — those are M2's (`transact`/`snapshot`/replay).
- **No node‑tier cross‑owner VERSION fork** — outside VERSION's domain (rejected as `NodeTierCrossOwner`).
