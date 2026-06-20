# M8 — Interface (for dependents)

M8 owns the **read-only query/presentation layer over the link subsystem**: it turns upstream link/arrangement/registry state into the answers readers ask (which links touch here, which match a descriptor, counts, pages, projections, endsets, delete-orphan previews, supersession lineage) — owning **no authoritative state and no index**, recomputing every answer from upstream on each call.

## Public interface

Foreign types (referenced, not owned): `Address/Span/SpanSet/Nat/Tumbler` (M1); `Kernel/Snapshot/Seq/WorldState` (M2); `Run/VPos` (M5); `Endset/View/ShippedType/HasLinks` (M7); `HasM5` (M5); `HasM3` (M3). Slots are 1-based (M7's convention); `s_C = 1` (content subspace).

```rust
pub const FROM: usize = 1;  pub const TO: usize = 2;  pub const TYPE: usize = 3;

/// Per-slot request component for the four-set descriptor query (ASN-0121).
pub enum SlotSpec {
    Any,            // ∗ / NOSPECS — the unit: drops out of the conjunction
    Empty,          // ∅ constrained-empty — the zero: annihilates the whole result
    Spans(Endset),  // populated address-spans (M7's Endset); MUST be NON-EMPTY (empty normalizes to the Empty/zero path)
}

/// q = (H, F, G, Θ). `home` is matched against home(a) (an address projection), NOT a slot.
pub struct FourSet { pub home: SlotSpec, pub from: SlotSpec, pub to: SlotSpec, pub ty: SlotSpec }

pub type Cursor = Option<Address>;                 // None = ⊥ (start); Some(a) = resume strictly past a
pub struct Window  { pub batch: Vec<Address>, pub next: Cursor, pub exhausted: bool }
pub struct SupClaim { pub claim: Address, pub old: Address, pub new: Address,
                      pub home: Address, pub active: bool }
pub struct OrphanReport { pub orphaned: Vec<Address> }   // links the proposed DELETE drops from d

pub enum QueryError { DocNotRegistered, NotALink, BadRegion,
                      NotContentSubspace, EmptyWidth, OutOfBounds }  // last three: delete_orphans preview, mirroring M5 DeleteError

pub struct LinkQuery<'k, W: WorldState> { kernel: &'k Kernel<W> }
```

```rust
impl<'k, W> LinkQuery<'k, W>
where W: WorldState + HasLinks + HasM5 + HasM3
{
    pub fn new(kernel: &'k Kernel<W>) -> Self;

    // ── Content-region discovery (V-anchored, present-tense, doc-gated; disjunctive; foundation ∩ active) ──
    /// V→I resolution of `region` through d's live arrangement; result is a SET (deduped by `Run: Eq`).
    pub fn image(&self, d: &Address, region: &[Span]) -> Result<Vec<Run>, QueryError>;          // V→I
    /// Links touching `region`; result = foundation ∩ active — nullified links never surface.
    pub fn findlinks_v(&self, d: &Address, region: &[Span]) -> Result<Vec<Address>, QueryError>;
    /// Present-tense census; result = foundation ∩ active — nullified links never surface.
    pub fn count_v(&self, d: &Address, region: &[Span]) -> Result<usize, QueryError>;
    /// Windowed enumeration (ASN-0108); foundation ∩ active; `n = 0` is clamped to 1 (total API).
    pub fn window_v(&self, d: &Address, region: &[Span], cur: Cursor, n: usize)
        -> Result<Window, QueryError>;
    pub fn retrieve_endsets(&self, d: &Address, region: &[Span])
        -> Result<Vec<(usize, Endset)>, QueryError>;                                            // ASN-0131

    // ── Four-set descriptor query (address-keyed, conjunctive, link-store-local, monotone) ──
    pub fn findlinks_ftt(&self, q: &FourSet) -> Vec<Address>;                                   // ASN-0121
    pub fn count_ftt(&self, q: &FourSet) -> usize;                                              // ASN-0132 (the count op)
    pub fn window_ftt(&self, q: &FourSet, cur: Cursor, n: usize) -> Window;                     // ASN-0108 (FTT Match reading)

    // ── Pointwise projection & discoverability (content subspace) ──
    /// I→V projection of link `a`'s slot into d's CONTENT subspace (ASN-0098); content-subspace ONLY.
    /// `NotALink` subsumes BOTH `a ∉ dom(L)` AND an out-of-range `slot`.
    pub fn project(&self, a: &Address, slot: usize, d: &Address) -> Result<SpanSet, QueryError>;// ASN-0098 I→V
    /// Compound "arrangement-reachable AND active", NOT pure LP12: a nullified-but-reachable link
    /// returns Ok(false). NotALink if a ∉ dom(L).
    pub fn discoverable_from(&self, a: &Address, d: &Address) -> Result<bool, QueryError>;

    // ── Pre-edit link-survival (read-only; never touches the edit path) ──
    /// Pre-edit what-if; orphans over active view. Mirrors DELETE preconditions:
    /// NotContentSubspace / EmptyWidth / OutOfBounds.
    pub fn delete_orphans(&self, d: &Address, p: &VPos, width: &Nat)
        -> Result<OrphanReport, QueryError>;                                                    // ASN-0117

    // ── Archival supersession/edit lineage (y/x intended as resident link addresses — dom(L)) ──
    pub fn in_claims(&self, y: &Address, v: View) -> Vec<SupClaim>;   // claims with old = y
    pub fn out_claims(&self, x: &Address, v: View) -> Vec<SupClaim>;  // claims with new = x
}
```

**Snapshot twins.** Every method `foo(&self, args…) -> R` is *exactly* `foo_on(&self.kernel.snapshot(), args…)` — the handle takes one fresh snapshot and delegates. The pure `*_on` free functions are public, generic over `W: WorldState + HasLinks + HasM5 + HasM3`, and are what a caller uses to read a count and its window — or any multi-call verdict — off **one** consistent state.

```rust
pub fn image_on           <W>(s: &Snapshot<W>, d: &Address, region: &[Span]) -> Result<Vec<Run>, QueryError>;
pub fn findlinks_v_on     <W>(s: &Snapshot<W>, d: &Address, region: &[Span]) -> Result<Vec<Address>, QueryError>;
pub fn count_v_on         <W>(s: &Snapshot<W>, d: &Address, region: &[Span]) -> Result<usize, QueryError>;
pub fn window_v_on        <W>(s: &Snapshot<W>, d: &Address, region: &[Span], cur: Cursor, n: usize) -> Result<Window, QueryError>;
pub fn retrieve_endsets_on<W>(s: &Snapshot<W>, d: &Address, region: &[Span]) -> Result<Vec<(usize, Endset)>, QueryError>;
pub fn findlinks_ftt_on   <W>(s: &Snapshot<W>, q: &FourSet) -> Vec<Address>;
pub fn count_ftt_on       <W>(s: &Snapshot<W>, q: &FourSet) -> usize;
pub fn window_ftt_on      <W>(s: &Snapshot<W>, q: &FourSet, cur: Cursor, n: usize) -> Window;
pub fn project_on         <W>(s: &Snapshot<W>, a: &Address, slot: usize, d: &Address) -> Result<SpanSet, QueryError>;
pub fn discoverable_from_on<W>(s: &Snapshot<W>, a: &Address, d: &Address) -> Result<bool, QueryError>;
pub fn delete_orphans_on  <W>(s: &Snapshot<W>, d: &Address, p: &VPos, width: &Nat) -> Result<OrphanReport, QueryError>;
pub fn in_claims_on       <W>(s: &Snapshot<W>, y: &Address, v: View) -> Vec<SupClaim>;
pub fn out_claims_on      <W>(s: &Snapshot<W>, x: &Address, v: View) -> Vec<SupClaim>;
// each: where W: WorldState + HasLinks + HasM5 + HasM3
```

## Caller contracts & obligations

**General**
- Construct a handle via `LinkQuery::new(kernel)`; `W` must satisfy `WorldState + HasLinks + HasM5 + HasM3`.
- Every `Address` returned is T4-valid (minted by M3) — usable directly, no caller validation.
- All methods are read-only: none writes, mints, or mutates `Σ`; `Σ` is framed.
- Each handle method takes **one** fresh snapshot. For a consistent multi-call verdict (e.g. count + its window), use the `*_on` twins threaded over **one** shared `&Snapshot<W>`.
- Results are determinate at a snapshot and deduped by address (a link is found at most once); no caller value-dedup needed.

**Region family** (`image`/`findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`)
- Pass `(d, region: &[Span])`; an unregistered `d` returns `Err(DocNotRegistered)`, **not** an empty result.
- `region` MUST be content-subspace, ordinal-level, depth-2 V-spans (`start[1] = s_C = 1`, `width[1] = 0`); else `Err(BadRegion)`.
- A registered-but-empty `d` returns a defined empty result (`Ok(vec![])` / `Ok(0)`), distinct from `DocNotRegistered`.
- Results are present-tense, **non-monotone**, and *foundation ∩ active* — a nullified link never surfaces, even if still arrangement-reachable.
- `image` is deduped at the boundary (`Run: Eq`): no exact-equal `Run` repeat; no caller dedup obligation.
- `retrieve_endsets` withholds link identity — value-identical endsets from distinct links collapse to one `(slot, endset)` pair; endsets are whole (never clipped) and content-identity (I-address); the `Vec` carries no `im` container.
- Exhaustiveness of `findlinks_v`/`retrieve_endsets` over slots `{FROM, TO, TYPE}` holds under v1's arity-3 invariant (every v1 link is arity-3).

**Descriptor family** (`findlinks_ftt`/`count_ftt`/`window_ftt`)
- Total — no doc gate, no error; reads only the link store. `count_ftt` is ASN-0132's count operation.
- The `FourSet` is address-phrased: caller resolves any reader content-pointings to addresses **upstream**.
- A `SlotSpec::Spans` MUST carry a **non-empty** `Endset`; an empty one is treated as `Empty` (annihilates to ∅) — never reaches M7.
- `home` is matched against `home(a)` (an M1 `document_of` address projection), NOT a slot and NOT an arrangement-presence test — a reverse-orphaned link still satisfies a home-bounded query.
- **Monotone**: a found-and-not-retracted link stays found (active slice only grows, coverage permanent).
- `(∗,∗,∗,∗)` returns the whole addressable slice; a home-only query degrades to a full active scan.

**Projection / discoverability**
- `project(a, slot, d)`: `Err(DocNotRegistered)` for unregistered `d`; `Err(NotALink)` covers BOTH `a ∉ dom(L)` AND an out-of-range `slot` (not separated).
- `project` is **content-subspace only** (strictly weaker than ASN-0098): a link reachable solely through `d`'s LINK subspace projects ∅ here.
- The returned `SpanSet` is **opaque** (M1 exposes no `is_empty`/iterator). To test emptiness use `equiv(&proj, &SpanSet::empty())?`; to enumerate, form `v_k = [s_C, k]` for `k ∈ 1..=content_count(d)` and keep those with `proj.denotes(&v_k)`. M8 does not test the projection.
- `discoverable_from(a, d)`: compound "reachable AND active", **NOT** raw LP12 — a nullified-but-reachable link answers `Ok(false)`; for raw LP12 compose `followlink` + M5 `project` yourself. `Err(DocNotRegistered)` / `Err(NotALink)` (`a ∉ dom(L)`). A *nullified* link is still a link: it passes the gate and returns `Ok(false)`.

**Pre-edit survival** (`delete_orphans`)
- Read-only what-if; never calls M5's delete.
- Preconditions mirror DELETE with M5 granularity: `Err(DocNotRegistered)`; non-`s_C` `p` → `Err(NotContentSubspace)`; zero `width` → `Err(EmptyWidth)`; out-of-range `(p, width)` → `Err(OutOfBounds)` — an *actionable* rejection, not an opaque `BadRegion`.
- `OrphanReport.orphaned` is the **per-document** orphan set over the **active view** — a nullified link that lost its last witness in `d` is NOT reported (diverges from ASN-0117's `D(d,Σ)` over `dom(L)`).
- Global-ghost / LP17 determination (discoverable from *no* document) is NOT computed — compose the M6 escalation yourself.

**Windowing** (`window_v`/`window_ftt`)
- Cursor is a bare `Address`: `Cursor = None` starts; `Some(a)` resumes strictly past `a`. Stateless across calls — the whole continuation is the cursor.
- Caller obligation `n ≥ 1`; a passed `n = 0` is clamped to 1 (API total), never a false non-terminal.
- Each call recomputes against the live snapshot (present-tense, never stale). `Window.exhausted` (a batch shorter than `n`) is the terminal signal; `next` resumes; stop on the first short/empty batch.
- Cursor survives orphaning (key is the permanent address); no duplicate / no skip of continuously-matching links; append-at-tail holds **within a home document** — cross-home order is not state-recoverable (documented blind spot).

**Archival lineage** (`in_claims`/`out_claims`)
- `y`/`x` are intended as resident link addresses (`dom(L)`); a non-link key is gated internally and returns `[]` (not an over-match) — but pass resident addresses regardless.
- Storage convention is **flipped**: `FROM = old/superseded`, `TO = new/superseding`; `in(y)` = claims with `old = y`, `out(x)` = claims with `new = x`.
- `v = View::Active` yields the operative graph; `v = View::Audit` the full history. `View` is consumed **by value** (it is not `Copy`).
- `SupClaim.home` is the M1 `document_of` attribution; `SupClaim.active` is `is_active(claim)`.

## Seams exposed downstream

**→ M10 (the sole consumer):**
- **Region family**: takes `(d, region: &[Span])`; returns `Err(DocNotRegistered)` for an unregistered `d`, `Err(BadRegion)` for a non-content-subspace/non-depth-2 region, and a defined empty result for a registered-empty `d`. Present-tense, non-monotone, addressable-filtered. `image` deduped at M8's boundary; `retrieve_endsets` returns `Vec<(usize, Endset)>` (no `im` container crosses the seam). M10 phrases the V-region (content subspace, depth-2).
- **Descriptor family**: takes an address-phrased `FourSet`; total (no doc gate); monotone; `count_ftt` is ASN-0132's operation; a `SlotSpec::Spans` must carry a non-empty `Endset`. M10 resolves reader content-pointings to addresses upstream.
- **Projection**: content-subspace only; `NotALink` covers a non-link `a` and an out-of-range `slot`. **Discoverability**: compound "reachable AND active", not raw LP12 (a nullified-but-reachable link answers `Ok(false)`).
- **Pre-edit survival**: read-only what-if; orphans over the active view; rejects with M5-matching granularity (`NotContentSubspace`/`EmptyWidth`/`OutOfBounds`).
- **Archival lineage**: resident link addresses; a non-link key is gated internally (`[]`); `Active` = operative graph, `Audit` = full history.
- **Windowing**: cursor is a bare `Address`; `Window.exhausted` is terminal; `next` resumes; stateless (`n ≥ 1`; `n = 0` clamped). M10 carries the cursor; a partial/empty batch ends the pass.
- **Pure twins** (`*_on(&Snapshot<W>, …)`): use to read a count and its window — or any pair — off one snapshot.
- M8 returns `Vec<Address>` / `usize` / `Window` / `Vec<(usize, Endset)>` / `SupClaim` / `OrphanReport`; M10 marshals to the wire and surfaces precondition failures (`DocNotRegistered`/`NotALink`/`BadRegion`/`NotContentSubspace`/`EmptyWidth`/`OutOfBounds`) as typed rejections, never a silent skip. Reads only — no commit — but snapshot-isolated.

**→ M9:** fenced off (ASN-0129). M9 reads its PL surface straight from M7, **never** through M8.

**Crate graph:** `skep-linkquery → skep-address, skep-kernel, skep-namespace, skep-arrangement, skep-links` (pure surfaces); consumed only by `skep-operation (M10) → skep-linkquery`. Acyclic, mirroring `M8 → M1, M2, M3, M5, M7`. M8 names no `World`/`Record` and contributes no slice to `skep-engine`.

## Boundary — NOT provided here

- **No spanfilade / coverage index, no per-slot matcher, no AND-of-ORs combiner** — those are M7's `stab`/`match_links`/`type_slice`; M8 implements no slot matching.
- **`coverage(a, i)` is NOT re-exposed** — it is exactly M7's `followlink(a, i)`; call M7 directly.
- **No content bytes** (M4); **no provenance R and no R-keyed query** — SHOWDELETIONS / FINDDOCSCONTAINING are M6's.
- **No global-ghost / LP17 ghost determination** (discoverable from no document) — M6 territory; M8 stops at the per-document orphan set.
- **No contextual claim discovery (EL11a)** — "which claims does `d` list" is out of scope; compose archival `in/out` with an M5/M6 listing check above M8.
- **No link-subspace positional projection** — `project` is content-subspace only; M7's BH3 is typed target→sources lookup, not V-position projection.
- **No `BadSlot` split** (`project`'s `NotALink` subsumes a non-link `a` and a bad `slot`); **no raw-LP12 `discoverable_from`**; present-state queries are uniformly active-filtered, never Audit-by-default.
- **Never invokes M5's edit path** — `delete_orphans` is a pure what-if; M8 mints/writes nothing and owns no authoritative state or index, recomputing every answer from upstream per call.
