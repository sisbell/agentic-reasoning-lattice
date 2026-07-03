# M5 — Arrangements & Editing (Vstream): Detailed Design

## Purpose & boundary

M5 owns every document's **mutable V→I arrangement** (the POOM — a content subspace and a link subspace per document) and the **append‑only content‑provenance relation R**, and it is the *only* place in the system where destructive change lives. It provides the editing/versioning operations (INSERT, DELETE, COPY, REARRANGE, CREATENEWVERSION), a semantics‑blind link‑seating step for M7, forward V→I resolution and reverse I→V projection for readers, and the R read surface for provenance queries. It funnels every mutation through one M2 composite, where it enforces the J‑couplings (content‑allocation ⇒ placement ⇒ provenance) and co‑locates each content placement's R‑append with its M‑edit so a reader sees one consistent `(M, R)` root.

It does **not**: store content bytes (M4) or mint addresses (M3) — it *orchestrates* those at its composite boundary; store link values or interpret link semantics (M7 — M5 seats an opaque, already‑allocated link address and never reads M7); register documents (M3, eager‑lazy split — a fresh document's arrangement is left implicit/empty until M5 first touches it); run content/link *queries* (M6/M8); or own ordering, durability, or recovery (M2). One thing well: **the authoritative mutable arrangement plus its write‑local provenance, recovered by replaying one edit‑delta journal.**

---

## Public interface

Types `Tumbler/Address/Span/SpanSet/Nat/Level` are M1's; `Kernel/Snapshot/LockKey/Seq/TxnError` are M2's; `MintError/PrincipalId/M3Rec` are M3's; `Val/ContentWrite/ContentError` are M4's. The slice is reached through an accessor trait the engine implements; write‑driving ops are generic over `W` with the upstream `From` bounds.

```rust
pub trait HasM5 { fn m5(&self) -> &M5State; }   // engine: W: WorldState + HasM5
// Subspace convention (ASN-0047): s_C = 1 (content), s_L = 2 (link). The constants are drawn
// from skep-kernel (M2's crate) — the Engine Composition Contract pins subspace constants there,
// below every store — so every module reaches the one shared definition and value-equality across
// the system holds by construction, not convention. V-positions are depth-2 tumblers
// [subspace, ordinal] (m = 2).
```

### A. Engine‑plug surface (slice / record / accessor / fold)

```rust
/// Authoritative folded state: per-document POOM + provenance. The arrangement is
/// authoritative MUTABLE state recovered by replay — NOT a recomputable hint.
#[derive(Clone, Default, Serialize, Deserialize)]
pub struct M5State { /* private; see Core data model */ }

/// M5's sole journal delta — effect-level (carries concrete addresses/ordinals so the
/// fold needs no upstream access and never re-mints). Each variant is `#[non_exhaustive]`,
/// so NO foreign crate can build an `M5Rec` by struct literal — `stage_*` and the op bodies
/// (all in M5's crate) are the only constructors, and the M/R-coupling cannot be bypassed.
/// (The engine only `From`-lifts and folds an already-built value; `apply_m5` matches in M5's
/// own crate, so it destructures freely — the engine never does.)
#[derive(Clone, Serialize, Deserialize)]
pub enum M5Rec {
    #[non_exhaustive] ContentPlace   { doc: Address, at: Nat, runs: Vec<Run> },  // INSERT/COPY: splice + R-append
    #[non_exhaustive] ContentRemove  { doc: Address, from: Nat, width: Nat },    // DELETE: contract+reseat (no C, no R)
    #[non_exhaustive] ContentReorder { doc: Address, cuts: Vec<Nat> },           // REARRANGE: 3|4 cut ordinals (no C, no R)
    #[non_exhaustive] LinkSeat       { doc: Address, link: Address },            // MAKELINK seating (no R — J-LV)
    /// CREATENEWVERSION (share + R-append). LINEARIZATION-AT-FOLD: the fold reads `source`'s
    /// then-current arrangement at THIS record's commit/replay slot — the record's effect is
    /// defined against the state at its commit position, not a pre-staged value. Exact under
    /// v1's single-applier M2 realization (nothing lands between a transact's base and its
    /// commit); any future M2 concurrency realization that lets disjoint-key commits land in
    /// that window MUST re-examine this record first (or move to the explicit-runs form,
    /// Open decision #4).
    #[non_exhaustive] VersionSnapshot{ source: Address, new: Address },
}

#[derive(Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Run { pub(crate) i_start: Address, pub(crate) width: Nat }
// standing invariants: EVERY Run has width ≥ 1 AND i_start is element-level (zeros = 3).
// Fields are CRATE-PRIVATE (`pub(crate)`): a foreign crate can neither build a Run by struct
// literal nor mutate one it holds — including an OWNED Run returned by `resolve`/`content_runs`/
// `link_runs` — so runs are literally read-only across every seam (M6/M7/M8 read via the
// `i_start()`/`width()` accessors; M5 hands out only `&Run`/owned `Run`, and even the owned value
// is unmodifiable outside M5). `Run::new` is therefore the sole foreign CONSTRUCTOR — sealing the
// same hole M5Rec's `#[non_exhaustive]` variants seal for records. (Derived `Deserialize` is the
// one field-by-field bypass; see `Run::new`'s doc — a recovered Run's shape rests on checkpoint
// integrity, not the type system.) `i_start` is element-level (zeros = 3) by the second standing
// invariant.

impl Run {
    /// Checked constructor — the seam guard for an EXTERNAL producer (none in v1): `None` iff
    /// `width == 0` OR `i_start` is not element-level (`zeros(i_start) ≠ 3`, equivalently
    /// `i_start.level() ≠ Level::Element`). M5's own emission sites (run-list split/coalesce,
    /// `resolve`, `content_runs`/`link_runs`, the folds) build Runs with `width ≥ 1` and an
    /// element-level `i_start` STRUCTURALLY by the in-crate struct literal (which the crate-private
    /// fields permit only inside M5) — their starts are minted element addresses or ordinal-shifts
    /// of one. `new` is the only CONSTRUCTOR a FOREIGN crate can call, and it rejects BOTH width 0
    /// and a non-element `i_start`; field privacy then closes the mutate-after-obtain path — a
    /// foreign holder cannot later set `width = 0` or swap `i_start` on any Run it obtained, owned
    /// or borrowed. One bypass remains: derived `Deserialize` builds a `Run` field-by-field
    /// without calling `Run::new`, so a *recovered* Run's `width ≥ 1` / element-level shape rests
    /// on M2 checkpoint integrity (the same trust posture as all of recovery), NOT on the type
    /// system. So the two standing invariants (`width ≥ 1`; `i_start` element-level) are not
    /// unconditionally type-enforced; they hold for every *minted-or-validly-recovered* Run —
    /// checked by `Run::new` at the foreign-construction seam, unforgeable thereafter (field
    /// privacy), built structurally at M5's internal emission sites, and trusted (via checkpoint
    /// integrity) on the deserialize path. On that basis `iextent`'s `.expect` guards a true
    /// internal invariant: `width ≥ 1` makes it total (`start < reach`, `#start = #reach`), and
    /// the element-level shape makes its raw `shift` advance the ordinal field — not the
    /// text→link separator. Every foreign path to a malformed Run is now closed: struct-literal
    /// construction and post-hoc mutation are sealed by field privacy, `Run::new` `None`-rejects
    /// width 0 and a non-element `i_start`, and the deserialize path is checkpoint-trusted
    /// (v1 internal sites build width ≥ 1, element-level structurally).
    pub fn new(i_start: Address, width: Nat) -> Option<Run>;     // None ⇔ width == 0 ∨ zeros(i_start) ≠ 3

    pub fn i_start(&self) -> &Address;   // read accessors — the only foreign field access
    pub fn width(&self) -> &Nat;

    /// The ONE admissible Run→Span lift: the level-uniform, element-level I-extent
    /// [i_start, shift(i_start, width)). Centralized (public) so no consumer re-derives it
    /// and none writes the malformed `Span(i_start, [0,width])` (element-level start vs depth-2
    /// width ⇒ `#start ≠ #width` ⇒ LevelMismatch downstream). TOTAL given the two standing invariants:
    /// `width ≥ 1` makes `shift` advance (`start < reach`, TS4) and length-preserving
    /// (`#start = #reach`), so `from_endpoints` cannot fault; the element-level `i_start` makes that
    /// `shift` land on the ordinal field, not the text→link separator. Both are enforced at the
    /// `Run::new` seam, unforgeable thereafter (crate-private fields), and structurally built at
    /// M5's internal sites. A SpanSet aggregating iextents across origin-documents is mixed-length —
    /// consume it under the level-class discipline (see Internal design).
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

impl<'k, W: WorldState> Vstream<'k, W> {
    /// The only constructor — M10 (and M9, for predicate-def `insert`) build a Vstream over the
    /// engine's kernel this way.
    pub fn new(k: &'k Kernel<W>) -> Vstream<'k, W>;
}

impl<'k, W> Vstream<'k, W>
where W: WorldState + HasM5 + HasM3 + HasContent,
      W::Record: From<M5Rec> + From<M3Rec> + From<ContentWrite>   // union bound; each op uses a subset
{
    /// Mint n fresh content addresses (M3), write their bytes (M4), splice the run at `at`
    /// (content subspace), record provenance — one M2 composite under key(doc, s_C).
    /// Returns the inserted run's START address (the predicate-def identity for M9) and the Seq.
    pub fn insert(&self, doc: &Address, at: VPos, values: Vec<Val>)
        -> Result<(Address, Seq), TxnError<InsertError>>;

    /// Transclude existing content by reference: resolve `specs` against source arrangements,
    /// splice into doc's content subspace at `at`, record provenance for the placed runs.
    /// Allocates NO content. (Uses From<M5Rec> only; reads M3/M4/M5.)
    pub fn copy(&self, doc: &Address, at: VPos, specs: Vec<VSpec>)
        -> Result<Seq, TxnError<CopyError>>;

    /// Remove content range [p, p+width) and close the gap (shift suffix left). Content store
    /// and R untouched. (From<M5Rec> only.)
    pub fn delete(&self, doc: &Address, p: VPos, width: Nat)
        -> Result<Seq, TxnError<DeleteError>>;

    /// Pivot (3 cuts) / swap (4 cuts) transpose in the content subspace. Pure permutation;
    /// content, links, R untouched. (From<M5Rec> only.)
    pub fn rearrange(&self, doc: &Address, cuts: Vec<VPos>)
        -> Result<Seq, TxnError<RearrangeError>>;

    /// Fork: mint a new identity (M3), install its content arrangement as a snapshot of
    /// d_src's content subspace, record provenance. Returns the new document address + Seq.
    /// (From<M3Rec> + From<M5Rec>.)
    pub fn version(&self, principal: PrincipalId, d_src: &Address)
        -> Result<(Address, Seq), TxnError<VersionError>>;
}
```

### C. Link seating — pure step composed into M7's MAKELINK

```rust
/// Append an already-allocated home link `link` at doc's next link V-position. SEMANTICS-BLIND:
/// trusts M7 that `link ∈ dom(L)`; M5 checks only CL-OWN (origin(link)=doc, via M1) and
/// CL-UNIQ (not already seated — I-extent membership over the link run-list). Returns the
/// delta; M7 lifts via `.into()` and stages it.
pub fn stage_seat_link(m5: &M5State, doc: &Address, link: &Address) -> Result<M5Rec, SeatError>;

/// STANDALONE OP — the Engine-Composition-Contract-required transact-wrapped twin of the pure
/// `stage_seat_link` (the contract demands BOTH forms for any primitive that appears as a step in
/// another store's composite, and `stage_seat_link` is exactly that step for M7's MAKELINK).
/// ISOLATION/TEST USE ONLY: production seats a home link through MAKELINK, which composes
/// `stage_seat_link` into its K.λ + K.μ⁺_L transaction; committing a seat *alone* is not a
/// production path (it would record a link V-position with no link allocation in the same
/// composite). Mirrors M4's `#[doc(hidden)] write`. Returns the seated link address + Seq.
#[doc(hidden)]
pub fn seat_link<W>(k: &Kernel<W>, doc: &Address, link: &Address)
    -> Result<(Address, Seq), TxnError<SeatError>>
where W: WorldState + HasM5, W::Record: From<M5Rec>;
```

### D. Arrangement reads — pure, over any M2 snapshot (M6, M8)

```rust
impl M5State {
    /// V→I resolution: I-runs covering an ORDINAL-LEVEL depth-2 V-span (width [0,n], action
    /// point 2), V-ordered, clipped to the active range (accept-and-intersect). Subspace from
    /// span.start().get(1), count from span.width().get(2). DEFENSIVE (returns ⟨⟩, cannot fault —
    /// no Result) unless the span is a usable ordinal-level depth-2 V-span — the COMPLETE guard is
    /// `#start == 2 ∧ #width == 2 ∧ span.width().get(1) == 0`; in particular #start ≠ 2 (BOTH <2 AND
    /// >2), #width ≠ 2, or a non-ordinal width (span.width().get(1) ≠ 0 — a level-uniform [m,n] with
    /// m>0 is action-point-1, making get(2) the wrong extraction) each yield ⟨⟩. A shape-valid span
    /// whose subspace value `span.start().get(1)` ∉ {s_C, s_L} likewise yields ⟨⟩ — a
    /// `DocArrangement` has exactly the content and link run-lists, so an unknown subspace selects
    /// none. Absent doc ⇒ ⟨⟩ (M6/M8 disambiguate registered-empty vs unallocated via M3).
    pub fn resolve(&self, doc: &Address, span: &Span) -> Vec<Run>;
    pub fn point(&self, doc: &Address, v: &VPos) -> Option<Address>;   // M(d)(v); None when
                                                                       // v.subspace ∉ {s_C, s_L} (no such run-list) or the ordinal is unarranged

    /// V→I coverage as a SpanSet: `⋃ r.iextent()` over the runs `resolve` returns for `span` —
    /// the centralized correct lift, so M7's MAKELINK need not re-derive `iextent`. `union`
    /// (concatenation) only ⇒ total, never faults, NOT normalized; possibly mixed-length when
    /// `span` covers transcluded runs — consume under the level-class discipline. In particular,
    /// because a transcluded endset's I-coverage is mixed-length and M1's `canonical_key` is
    /// length-gated, M7 MUST form its coverage-class dedup key PER LEVEL-CLASS (one `canonical_key`
    /// per endpoint-length partition, the per-class results combined), never by a single
    /// `canonical_key` over the raw cover — which would fault `LevelMismatch`.
    pub fn resolve_coverage(&self, doc: &Address, span: &Span) -> SpanSet;

    pub fn content_runs(&self, doc: &Address) -> Vec<Run>;                 // canonical, V-ordered (COMPARE)
    pub fn link_runs(&self, doc: &Address) -> Vec<Run>;
    pub fn content_count(&self, doc: &Address) -> Nat;                     // n_C(d)
    pub fn link_count(&self, doc: &Address) -> Nat;                       // n_L(d)
    // content_image (I-coverage of the current content arrangement) is M5-INTERNAL — the
    // SHOWDELETIONS operand consumed only by `deletions` (§2/§9). It is NOT a public seam (no
    // downstream module reads it), so its raw mixed-length cover never crosses a boundary and the
    // public SHOWDELETIONS surface is `deletions` alone.

    /// I→V (content subspace ONLY, by construction — link reverse-discovery is M7's BH3, not
    /// this; there is no subspace argument): V-positions of doc whose CONTENT I-address falls in
    /// `coverage` (a link footprint, possibly fragmented and mixed-length). Total. Coverage spans
    /// are level-uniform I-extents; each is matched per the level-class discipline (§2). Scan of
    /// the forward content map by default.
    pub fn project(&self, doc: &Address, coverage: &SpanSet) -> SpanSet;
}
```

### E. Provenance reads — pure (M6: SHOWDELETIONS, FINDDOCSCONTAINING)

```rust
impl M5State {
    pub fn ever_placed(&self, doc: &Address) -> SpanSet;   // R↾doc (content spans ever placed; raw, possibly mixed-length — consume under the level-class discipline)

    /// SHOWDELETIONS primitive: `ever_placed(doc) ∖ content_image(doc)`, computed PER LEVEL-CLASS
    /// inside M5 (§2) — both operands are iextent-covers that mix origin-lengths when `doc`
    /// transcludes across heterogeneous-depth documents, so M5 (owner of R and the iextent
    /// semantics) partitions each by endpoint length, runs `difference_sets` within each class,
    /// and unions the results. Per-class is also the correct semantics (different-length addresses
    /// are distinct and cannot cancel). M6 reads SHOWDELETIONS straight off this — `content_image`
    /// is the M5-internal operand, never a seam; no raw length-gated op crosses the boundary (Conflicts #6).
    pub fn deletions(&self, doc: &Address) -> SpanSet;

    /// R⁻¹ candidate documents (distinct, deterministic Tumbler order). Returns `Vec<Address>`:
    /// `Address` is not `Ord`, so an `im::OrdSet<Address>` keyed surface is impossible; M5 owns R
    /// and any index over it, M6 owns only the FINDDOCSCONTAINING query (Conflicts #6).
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

// `?`-desugaring conversions the in-closure mint/write calls depend on (INSERT: `mint_content(doc)?`,
// `stage_write(…)?`; VERSION: `mint_version/mint_document … ?`). The `Mint(..)`/`Content(..)` variants
// imply these, but the `?` operator needs the `From` impls spelled out:
impl From<MintError>    for InsertError  { fn from(e: MintError)    -> Self { InsertError::Mint(e) } }
impl From<ContentError> for InsertError  { fn from(e: ContentError) -> Self { InsertError::Content(e) } }
impl From<MintError>    for VersionError { fn from(e: MintError)    -> Self { VersionError::Mint(e) } }
```

---

## Core data model

```rust
pub struct M5State {
    // AUTHORITATIVE, journaled, replay-recovered, serialized in checkpoints.
    // Keyed by the document's `Tumbler` — M1's `Address` is NOT `Ord` (only `Tumbler` carries the
    // manual lexicographic `Ord`), and M5 cannot add `Ord` to a foreign type; every `&Address`
    // method converts with `doc.tumbler()`.
    arrangements: im::OrdMap<Tumbler, DocArrangement>,   // sparse: absent doc ⇒ empty arrangement (lazy)
    prov_by_doc:  im::OrdMap<Tumbler, im::Vector<Span>>, // append-only R, keyed by placing document
    // (v1 has NO derived-hint fields ⇒ rebuild_derived is identity; see Open build decisions)
}
#[derive(Clone, Default, Serialize, Deserialize)]        // required transitively by M5State's derives
struct DocArrangement { content: RunList, link: RunList }
```

**The POOM is authoritative mutable state, not a hint** (decomposition; ASN‑0047 P3): it is the only component that *loses* information (`ContentRemove`, `ContentReorder`), it is not recomputable from anything cheaper, and it is recovered by replaying the edit‑delta journal. R is **authoritative and non‑recomputable from the current arrangement** (a deleted address keeps its R pair — ASN‑0047 P2) but, like the POOM, is recovered by replay.

**`RunList` — implicit‑position run‑list, per subspace.** A `RunList` is an ordered sequence of `Run{i_start, width}`. V‑positions are *not stored*: run *j* occupies content/link ordinals `[1 + Σ_{i<j} width_i, …]`. This single choice makes the load‑bearing invariants *free*: density/contiguity/minimum‑position (D‑SEQ★/D‑CTG★/D‑MIN★) hold by construction (a V‑start is always a prefix sum, so no holes), insert/delete shift the suffix for *free* (no renumbering), and storage scales with the number of distinct contiguous transclusions/edit‑runs, not with positions. Depth is fixed at **m = 2** (ASN‑0036 S8‑depth; ASN‑0084 depth‑2 scope; semantically inert — see Open decisions), so a V‑position is just `[subspace, ordinal]` and all V‑side arithmetic is integer ordinal math; only the *I‑addresses* (element‑level, `zeros = 3`) use M1's tumbler arithmetic.

`RunList` exposes a representation‑independent contract — `total_width`, `locate(ord) → (run_idx, offset)`, `point(ord)`, `resolve_range(ord, count)`, `splice_in(ord, runs)`, `remove_range(ord, width)`, `reorder(cuts)`, `iter_runs() → (v_start, i_start, width)`, `image() → SpanSet`. The *physical* persistent structure behind it is an Open build decision (default `im::Vector<Run>`); the algorithms below are stated over the contract.

**Provenance R.** `prov_by_doc` is the authoritative direction (the natural append target: when *d* places a content run, append `iextent(i_start, width)` (§2) to `prov_by_doc[d.tumbler()]`). `ever_placed(d)` reads it directly; `docs_containing(coverage)` scans it, returning a `Vec<Address>` candidate set (an interval‑index hint for scale is an Open decision; **M5 owns this index** — Conflicts #6). Entries are run‑granular (one `Span` per placed run) and may overlap/duplicate — queries treat R as the set‑union of expanded pairs, so redundant appends are harmless (P2).

| state | authoritative? | recovered by |
|---|---|---|
| `arrangements` (POOM) | yes (mutable) | journal replay + checkpoint |
| `prov_by_doc` (R) | yes (append‑only; not recomputable from POOM) | journal replay + checkpoint |
| reverse‑prov / inverse‑arrangement index | hint (recomputable; **M5‑owned**, Conflicts #6) | *not built in v1*; `rebuild_derived` if added |

---

## Internal design

### 1. The run‑list: locate, splice, contract, reorder, coalesce

All four mutators reduce to splits and concatenations of the per‑subspace run‑list; the spec's *displacement* (ASN‑0082 shift) is **never computed** — implicit positions absorb it.

- **locate(ord):** walk runs accumulating widths until the cumulative sum reaches `ord`; return `(run_idx, offset_in_run)`. (`O(#runs)` over `im::Vector`; `O(log #runs)` over a width‑measured tree.) **Append boundary:** at `ord = total_width + 1` — the INSERT/COPY append case `J = N+1` and the link‑seat append `n_L(d)+1` — `locate` returns the **end boundary** (prefix = all runs, offset 0 into an empty suffix), so `splice_in` concatenates the new runs at the tail; `total_width + 1` is the single `ord > total_width` accepted (it names no existing position) and the sole `ord` that addresses past the last run.
- **splice_in(ord, new_runs):** split the run‑list at `ord` (splitting one boundary run if `ord` is interior to it, via `Run(a,w) → Run(a, c), Run(a⊕c, w−c)` where the new I‑start `a⊕c = M1::validate(M1::shift(a.tumbler(), &c))` — see *Address synthesis* below), insert `new_runs`, concat the suffix. The suffix's implicit positions are now `+Σwidth(new_runs)` — the uniform forward shift, *for free*.
- **remove_range(ord, width):** split at `ord` and `ord+width`, drop the middle, concat prefix+suffix. Suffix positions shift left for free; gap closes by construction (ASN‑0117 P2).
- **reorder(cuts):** split at each cut ordinal; **tile by placement** — concatenate `[exterior‑left][β][μ?][α][exterior‑right]` (ASN‑0119's collision/subspace‑safe construction), never offset arithmetic, so the bijection is structural (no possibility of the swap‑α offset bug, ASN‑0084 Q14).
- **Eager seam‑coalesce** after every mutator: at each touched seam, merge adjacent runs `(a₁,w₁),(a₂,w₂)` **iff I‑adjacent** — `M1::shift(a₁.tumbler(), &w₁) == a₂.tumbler()`. I‑adjacency is the *complete and safe* guard: it implies same origin (ASN‑0058 M16a) and excludes shared‑I‑extent (M14a) — and it is vacuously false across origin‑lengths, since `shift` preserves length (`#shift(a₁,w₁) = #a₁`), so two cross‑length runs never merge — so it can never merge across an origin seam (M16) or collapse a transclusion (M14). **Never coalesce on value** (S4). With eager coalesce the resident form is the unique maximally‑merged decomposition (ASN‑0058 M12), so queries over run structure read it directly; choosing lazy mode (Open decision #8) instead requires `resolve`/`content_runs` to coalesce on output.

**Run‑list append helpers** — the eager‑coalesce rule applied *incrementally* as a run‑list is built (INSERT/COPY accumulate runs before staging one `ContentPlace`):
- `extend_or_push_run(runs: &mut Vec<Run>, r)` — if `runs.last()` I‑extends to `r` (`M1::shift(last.i_start.tumbler(), &last.width) == r.i_start.tumbler()`, the §1 I‑adjacency guard), widen it in place (`last.width += r.width`); else `runs.push(r)`. COPY's accumulator: cross‑origin runs are cross‑length (shift preserves length, §1), fail the I‑adjacency test, and so never coalesce — preserving the origin multiset (CP11).
- `extend_run(open: &mut Option<Run>, a)` — the single‑address INSERT specialization: `None ⇒ Some(Run{ i_start: a, width: 1 })`; `Some(r)` with `r` I‑extending to `a` (`M1::shift(r.i_start.tumbler(), &r.width) == a.tumbler()`) ⇒ widen `r.width += 1`. Under INSERT's held content lock every `mint_content` advances the same frontier, so each `a` is I‑adjacent to the open run; `extend_run` therefore only ever widens it and the loop closes with exactly one run.

**Address synthesis through `validate`.** `Run.i_start` is an `Address` but `M1::shift` yields a `Tumbler`; every within‑run I‑address M5 synthesizes — the `splice_in`/`reorder` boundary split, `resolve_range`, `point`, and `iextent` — recovers its `Address` via `M1::validate(M1::shift(…)).expect("T4‑valid by construction")`. Shifting a valid element address by an ordinal offset preserves T4‑validity, so the `expect` flags an internal‑invariant violation, never a domain case (mirroring `point`'s synthesis in §2). The raw `M1::shift` at every one of these sites is *safe* — **not** the text→link hazard M1 flags for a bare subspace base — because each `i_start` is always a **full element position**: `mint_content`/`mint_link` emit element‑level addresses `[…·0·subspace·k]` (`zeros = 3`, ordinal `k` as the last component), and every run‑list operation carries that last‑component‑ordinal shape, so the shift advances the ordinal field — exactly M1's stated safe window for raw `shift`. M5 never holds a `doc·0·subspace` base on which a raw shift would advance text→link, so M1's `shift_ordinal`/`elem_addr` wrappers are unnecessary at these sites. For any `Run` a *foreign* crate could build through `Run::new` rather than mint internally, that same element‑level shape is now enforced at the seam — `Run::new` rejects a non‑element `i_start` (`zeros ≠ 3`), so even an externally‑supplied run carries an `i_start` safe for raw `shift` — and, the fields being crate‑private, one that cannot be degraded after construction.

### 2. resolve / point / project

**Run → I‑extent (the one correct lift).** `Run::iextent` (public, §A) is a run's I‑extent: the **level‑uniform, element‑level** span

```rust
impl Run {
    fn iextent(&self) -> Span {
        Span::from_endpoints(self.i_start.tumbler().clone(), M1::shift(self.i_start.tumbler(), &self.width))
            .expect("width ≥ 1 ⇒ start < reach ∧ #start = #reach ⇒ from_endpoints cannot fault")
    }
}
```

`shift` advances the last component by `width ≥ 1` — and the last component *is* the ordinal because `i_start` is element‑level (Run's second standing invariant) — so `start < reach` (TS4) and `#start = #reach` (length‑preserving). This is the *only* admissible Run→Span conversion: a naïve `Span(i_start, [0,width])` is **malformed** — `i_start` is element‑level (`zeros = 3`, depth ≈ 8) while `[0,width]` is a depth‑2 displacement, so `add` would advance a field separator (garbage reach) and the span would not be level‑uniform (`#start ≠ #width`), faulting every downstream `intersect`/`difference`/`normalize` with `LevelMismatch`. `iextent` is used by `project`, by `resolve_coverage`, by `image()` (which backs the internal `content_image`), and by the R‑append folds (§3, §7).

**Level‑class discipline for span‑set algebra.** A document's content runs may reference I‑addresses minted under *different* documents (transclusion via COPY/VERSION), and element‑address total length varies with the node/account/document field widths of the origin (a length‑7 `[1,0,1,0,1,0,s_C,k]` and a length‑9 `[1,5,0,1,0,1,0,s_C,k]` are both legal element addresses). So a SpanSet aggregated across runs — `content_image`, `ever_placed`, a coverage footprint — is in general **mixed‑length**, and M1's length‑gated set ops (`intersect`, `difference_sets`, `intersect_sets`, `normalize`, `canonical_key`) return `Err(LevelMismatch)` on mixed‑length operands. Two M1 primitives are *not* gated and are preferred wherever they suffice: `classify_spans` (pure‑order span relation) for overlap/separation tests, and `SpanSet::denotes`/`Span::contains` (pure‑order membership) for point tests — both correct across lengths (a shorter‑prefix span can legitimately contain a longer address, so cross‑length pairs are **not** safely treated as disjoint). Where the *geometry* of an intersection or difference is actually needed (not just overlap/membership), M5 (or its caller) partitions each operand into level‑classes by endpoint length `#start`, runs M1's op within each class — operands now equal‑length — and unions the per‑class results; genuine cross‑class containment is recovered through `denotes`. Internal run‑list arithmetic needs none of this: `shift`/`==` are total, and the I‑adjacency coalesce guard is false across lengths (§1), so it never merges cross‑origin runs. **No span‑set operation over a mixed‑length cover is unconditionally fault‑free; the discipline above is how M5 and its readers stay clear of `LevelMismatch`. M5 is deliberately *asymmetric* about where that discipline runs. It is *encapsulated* behind the M6 query methods — `project` and `deletions` perform their per‑class algebra internally (§9, §E), so M6 never receives a length‑gated op or a raw mixed‑length cover. It is *exposed* on the M7/M8 V→I seam and on the `ever_placed` operand surface — `resolve_coverage` hands M7/M8 a raw, un‑normalized, possibly‑mixed‑length cover, and `ever_placed` hands out a raw iextent cover — under the "consume under the level‑class discipline" contract carried on each of those method docs. (`content_image` is M5‑internal — its raw mixed‑length cover never crosses a seam, so `deletions` is the only place it is consumed, per class.)**

- **resolve(d, span):** *precondition* — `span` is an **ordinal‑level** depth‑2 V‑span: width `[0,n]` with action point 2 (the global `m = 2` commitment), the count taken as `span.width().get(2)`. Since `resolve` returns `Vec<Run>` (no `Result`) it cannot signal a malformed span, so it **defensively returns `[]`** unless the span is a usable ordinal‑level depth‑2 V‑span — the COMPLETE guard is `#span.start() == 2 ∧ #span.width() == 2 ∧ span.width().get(1) == 0`. In particular `#span.start() ≠ 2` (rejecting `#start > 2` as well as `< 2`), `#span.width() ≠ 2`, or `span.width().get(1) ≠ 0` (a non‑ordinal width — a level‑uniform `[m,n]` with `m>0` is action‑point‑1 and `get(2)` would extract the wrong count) each yield `[]`. Otherwise `S = span.start().get(1)` selects the subspace run‑list — and `S ∉ {s_C, s_L}` selects none (a `DocArrangement` has exactly the content and link lists), so the result is `[]`; `k = span.start().get(2)`, `n = span.width().get(2)`. Return `resolve_range(k, n)` clipped to `[1, total_width]` (accept‑and‑intersect — out‑of‑range silently dropped, ASN‑0118). Each within‑run I‑address is `M1::validate(M1::shift(run.i_start.tumbler(), &offset)).expect(…)` (see *Address synthesis*, §1). Absent doc ⇒ `[]`.
- **point(d, v):** `locate(v.ordinal)` in the `v.subspace` list (`v.subspace ∉ {s_C, s_L}` names no run‑list ⇒ `None`); `Some(M1::validate(M1::shift(i_start.tumbler(), &offset)).expect("T4-valid by construction"))` or `None` (`validate` returns `Result`, so the synthesis is `.expect`‑ed — an internal‑invariant failure, never a domain case).
- **resolve_coverage(d, span):** `resolve(d, span)` then `union` of each run's `iextent()` — the centralized SpanSet lift for M7/M8. Total (concatenation), not normalized, possibly mixed‑length; consumers operate on the result under the level‑class discipline.
- **content_image(d)** *(private; the `deletions` operand, §9):* `arrangements.get(d.tumbler()).map(|a| a.content.image()).unwrap_or(SpanSet::empty())`, where `image()` is the `union` of `r.iextent()` over the runs — an element‑level cover that is **possibly mixed‑length** across transcluded origins (not, in general, a single level‑class). It is `union` (concatenation, total) only; `deletions` operates on it under the level‑class discipline (§9) and does **not** blindly `normalize` it. Because it never crosses a module seam, its mixed‑length hazard is contained inside M5.
- **project(d, coverage):** *content subspace only* — the scan is over `d`'s content runs and answers "content I‑address falls in `coverage`"; link‑to‑link reverse discovery is M7's BH3, not this, so there is no subspace argument. For each content run `(v_start, i_start, width)` and each span of `coverage`: **(level‑uniform, same length)** when the span `is_level_uniform()` and its endpoint length equals the run's I‑extent length, `intersect` `r.iextent()` with it (M1, within one level‑class); each I‑sub‑extent maps at equal offset to a V‑sub‑range. **(otherwise)** — a different‑length span, *or* a same‑length but non‑level‑uniform span (which `intersect` would fault on) — fall back to per‑coverage‑span `Span::contains` membership (the per‑span point test; equivalently `SpanSet::denotes` on that one span), which is total: because the run's addresses `shift(i_start, k)` are contiguous and a span is order‑convex, the contained subset is a contiguous index range (located by boundary search over the run's offsets) mapping to one V‑sub‑range. Emit each V‑sub‑range as a depth‑2 V‑span; union them (M1 `union` then `normalize` — the output V‑spans are all depth‑2, hence uniform‑length and safe to normalize). `O(#runs · #coverage‑spans)`; fragmentation is correct (ASN‑0119 RA7c).

### 3. INSERT (ASN‑0116; one composite under `M3State::content_lock_key(doc)`)

```
transact([M3State::content_lock_key(doc)], |stg|):
  m3 = stg.working().m3()
  reject DocNotRegistered unless m3.is_registered_document(doc)
  reject EmptyContent if values.is_empty()
  n_c = stg.working().m5().content_count(doc)
  reject BadPosition unless valid_insertion(at, n_c)  // subspace=s_C, depth 2, ordinal ∈ [1, n_c+1] (or =1 if n_c=0)
  first = None; run: Option<Run> = None
  for val in values:
     (a, m3rec) = stg.working().m3().mint_content(doc)? ; stg.push(m3rec.into())   // re-reads advanced frontier
     cw = M4::stage_write(stg.working().content(), &a, val)? ; stg.push(cw.into())
     first.get_or_insert(a.clone()); extend_run(&mut run, a)                       // held lock ⇒ I-adjacent mints ⇒ ONE run
  stg.push(M5Rec::ContentPlace{ doc, at: at.ordinal, runs: vec![run.unwrap()] }.into())  // unwrap safe: EmptyContent ⇒ ≥1 val ⇒ run opened
  Ok(first.unwrap())
```

Successive `mint_content` calls read `stg.working()`, so they advance the *same* frontier under the held lock → contiguous, I‑adjacent addresses → one run; `extend_run` (§1) therefore only ever *widens* the single open run (a second run never opens here — COPY is where `ContentPlace.runs` genuinely carries multiple cross‑origin runs). Concurrency‑freshness is handled by the per‑(doc, content‑subspace) lock (ASN‑0116). The `mint_content(doc)?` / `stage_write(…)?` operators desugar through `From<MintError> for InsertError` / `From<ContentError> for InsertError` (Errors & helper types). **J0/J1★ by construction:** mint + write + place + provenance ride one transaction; the `ContentPlace` fold appends `(run, doc)` to R *with* the splice. Return is the run start = the predicate‑def identity for M9.

**Fold:**
```
apply_m5(ContentPlace{doc, at, runs}):
  k = doc.tumbler()
  arr = arrangements.get(k).cloned().unwrap_or(empty)
  arr.content = arr.content.splice_in(at, runs)                  // + eager coalesce
  R' = prov_by_doc
  for r in runs:                                                 // im::OrdMap[k] is &V and PANICS on absent key, so:
     col = R'.get(k).cloned().unwrap_or_default()                // im::Vector<Span>, empty if doc has no prior R
     col.push_back(r.iextent())                                  // level-uniform element-level I-extent
     R' = R'.update(k.clone(), col)
  M5State{ arrangements: arrangements.update(k.clone(), arr), prov_by_doc: R' }
```

### 4. DELETE (ASN‑0117; `M3State::content_lock_key(doc)`)

Reject unless `doc` registered, `subspace(p)=s_C`, `p ∈ V_{s_C}(d)` and containment `ordinal(p)+width−1 ≤ n_c`, `width ≥ 1`. Stage `ContentRemove{doc, from: p.ordinal, width}`. **NonDestruction is structural** (ASN‑0117 P0): M5 has no path to content reclamation (M4 exposes none); `ContentRemove`'s fold touches neither content nor R. Link survival is automatic — a text delete never touches the link run‑list (ASN‑0117 P4).

**Fold:**
```
apply_m5(ContentRemove{doc, from, width}):
  k = doc.tumbler()
  arr = arrangements.get(k).cloned().unwrap_or(empty)
  arr.content = arr.content.remove_range(from, width)           // split at `from` & `from+width`, drop middle, concat + eager coalesce
  M5State{ arrangements: arrangements.update(k.clone(), arr), prov_by_doc }   // C and R untouched (no append, no removal)
```

### 5. COPY (ASN‑0118; `M3State::content_lock_key(doc)`)

```
transact([M3State::content_lock_key(doc)], |stg|):
  m5,m3,c = stg.working().{m5,m3,content}()
  reject DocNotRegistered / BadPosition as in INSERT
  runs = []
  for VSpec{source, span} in specs:
     reject SourceNotRegistered unless m3.is_registered_document(&source)
     reject BadSpan unless #span.start()==2 ∧ #span.width()==2 ∧ span.width().get(1)==0  // ordinal-level depth-2 V-span (== resolve's complete guard, §2)
     reject NotContentSubspace unless span.start().get(1) == s_C        // content-residence (non-transclusion guard)
     reject EmptySource unless m5.content_count(&source) > 0            // ASN-0118 enabled(COPY): V_{s_C}(d_s) ≠ ∅
     for r in m5.resolve(&source, &span):                              // resolved BEFORE staging ⇒ self-copy sees pre-edit
        reject DanglingSource unless c.contains(r.i_start.tumbler())   // content-side referential gate (S3★)
        extend_or_push_run(&mut runs, r)                              // §1 helper: widen if I-adjacent, else push (cross-origin never merges)
  reject EmptyResult if total_width(&runs) == 0
  stg.push(M5Rec::ContentPlace{ doc, at: at.ordinal, runs }.into())    // same fold as INSERT ⇒ R-append for placed runs
  Ok(())
```

No minting — COPY transcludes existing addresses by reference (CP1/CP2). Resolution reads source POOMs off the composite's **consistent base** (`stg.working()`/`stg.base()` — the operation's linearization snapshot under v1's single‑linearization realization), so the arrangement read matches the linearization point; **no source lock is needed**. COPY then bakes the concrete resolved addresses into the record, and those addresses stay valid forever by content immutability (S0), so the record is correct regardless of later source edits. The per‑spec `BadSpan` guard rejects a source span that is well‑formed for M1 but is *not* an ordinal‑level depth‑2 V‑span (e.g. a level‑uniform `[m,n]` width): without it such a span would `resolve` to nothing and surface as `EmptyResult`, indistinguishable from an empty range — so the guard hands M10 a precise verdict instead of a skip (the contract‑narrowing this records is Conflicts #7). The per‑spec `EmptySource` guard surfaces ASN‑0118's "source subspace non‑empty" admissibility clause as a typed rejection (rather than silently dropping a registered‑but‑empty source — M10 wants a verdict, not a skip); span‑level out‑of‑range hits remain accept‑and‑intersect (clipped by `resolve`). Recording the *whole* placed run as provenance is correct: range‑new addresses are genuinely new pairs; already‑referenced ones are P2 no‑ops (CP8). Cross‑origin runs never coalesce (`extend_or_push_run`'s I‑adjacency guard, §1), preserving the origin multiset (CP11) and transclusion independence (CP4/M14).

### 6. REARRANGE (ASN‑0119/0084; `M3State::content_lock_key(doc)`)

Validate R‑PRE: 3 or 4 cuts (`BadCutCount`), strictly ascending (`NotAscending`), all `subspace=s_C` at depth 2 (`NotContentSubspace`), the affected interval within the active content run — both the **CS5 lower bound** `1 ≤ ord(c₀)` and the upper bound `ord(c_last) ≤ n_c+1` (both `OutOfBounds`) — and the content subspace non‑empty `V_{s_C}(d)≠∅` (`EmptyContentSubspace`, R‑PRE(ii)). Strict ascent (`NotAscending`) already forces every region width ≥ 1, so no separate per‑region emptiness check is reachable, and — given ascent — checking `ord(c₀) ≥ 1` discharges CS5 for every cut. (The CS5 lower bound is in fact harmless to omit — the fold *tiles by placement*, so a split at ordinal 0 and a split at ordinal 1 coincide — but it is checked for completeness against the cited R‑PRE/CS5.) Stage `ContentReorder{doc, cuts: ordinals}`. The permutation is **cut‑determined and value‑blind** — read from cut geometry, never from content values (so a duplicate‑I interval correctly yields `π≠id` with `M'=M`, ASN‑0119). Referential integrity and permanence are automatic (range unchanged, RA1).

**Fold:**
```
apply_m5(ContentReorder{doc, cuts}):
  k = doc.tumbler()
  arr = arrangements.get(k).cloned().unwrap_or(empty)
  arr.content = arr.content.reorder(cuts)                       // split at cut ordinals, tile by placement (§1) + eager coalesce
  M5State{ arrangements: arrangements.update(k.clone(), arr), prov_by_doc }   // C, L, R untouched (pure permutation)
```

### 7. CREATENEWVERSION (ASN‑0123)

Pre‑read `ω(d_src)` off a snapshot (stable for an existing document, per M3) to choose branch + lock:

```
snap = k.snapshot(); m3 = snap.world().m3()
if !m3.is_registered_document(d_src) { return Err(TxnError::Rejected(VersionError::SourceNotRegistered)) }
(lock, branch) = match m3.effective_owner(d_src) {
   Some(p) if p.id == principal => (M3State::version_lock_key(d_src), Owned),         // owned fork: serializes forks of d_src (OQ4)
   _ => {                                                                              // cross-owner fork
      let pfx = m3.principal_prefix(principal)
                  .ok_or(TxnError::Rejected(VersionError::NotAPrincipal))?;            // Option → Result before `?`
      // P-tier (ASN-0123): a cross-owner fork requires an ACCOUNT-tier forker; node-tier is scoped out.
      if M1::zeros(pfx.tumbler()) != 1 {
         return Err(TxnError::Rejected(VersionError::NodeTierCrossOwner))              // explicit, self-describing — not a downstream Mint(NotAnAccount)
      }
      (M3State::document_lock_key(&pfx), Cross(pfx))
   }
}
transact([lock], |stg|):
   m3 = stg.working().m3()
   (v, m3rec) = match branch { Owned => m3.mint_version(d_src), Cross(pfx) => m3.mint_document(&pfx) }?  // From<MintError> for VersionError; pfx account-tier by the P-tier gate above
   stg.push(m3rec.into())
   stg.push(M5Rec::VersionSnapshot{ source: d_src.clone(), new: v.clone() }.into())
   Ok(v)
```

The node‑tier cross‑owner case is genuinely outside VERSION's domain (ASN‑0123 P‑tier), and the explicit `zeros(pfx)==1` check at the branch surfaces it as a self‑describing `NodeTierCrossOwner` *before* any mint — rather than letting it surface obliquely as `mint_document`'s `Mint(NotAnAccount)` — so M10 returns a clear rejection. The in‑closure `… ?` desugars through `From<MintError> for VersionError` (Errors & helper types).

**Fold** shares `source`'s *then‑current* content run‑list into `new` (structural `im` share — O(1)) and appends each shared run as provenance `(run, new)`:
```
apply_m5(VersionSnapshot{source, new}):
  src = arrangements.get(source.tumbler()).map(|a| a.content.clone()).unwrap_or(empty)  // read at fold point = fork linearization
  nk  = new.tumbler()
  R'  = prov_by_doc
  for (_, i_start, width) in src.iter_runs():                   // empty src ⇒ zero iterations ⇒ R unchanged
     col = R'.get(nk).cloned().unwrap_or_default()              // im::OrdMap[nk] panics on absent key; .get is the safe form
     col.push_back(Run{i_start, width}.iextent())              // in-crate struct literal (allowed inside M5)
     R' = R'.update(nk.clone(), col)
  if src.total_width() == 0:                                    // n = 0: leave `new` ABSENT (absent ⇒ empty); no redundant entry, R' == prov_by_doc
     M5State{ arrangements, prov_by_doc: R' }
  else:
     arr = DocArrangement{ content: src, link: empty }
     M5State{ arrangements: arrangements.update(nk.clone(), arr), prov_by_doc: R' }
```
This **copies the V→I map, not the I‑range** (ASN‑0123 V2): the share preserves multiplicity, so within‑document transclusion duplicates survive into the fork — a set/range copy would silently drop them. Fixing m = 2 dissolves the depth‑rebasing case, so the O(1) share always applies. When the source content subspace is empty (`n = 0`) the fold appends no provenance and **skips the `arrangements.update`**, leaving `new` absent under the lazy convention (≡ an empty arrangement) — ASN‑0123 V1's zero‑content footprint, with no redundant empty entry to muddy the "absent ⇒ empty" equivalence. Source is untouched (V3); the new arrangement diverges copy‑on‑write under later edits (V11).

### 8. Link seating (for M7's MAKELINK)

`stage_seat_link(m5, doc, link)`: reject `NotHomeLink` unless `M1::document_of(link).as_ref() == Some(doc)` (CL‑OWN — `document_of` yields `Option<Address>`, so `.as_ref()` lines it up with `Some(doc): Option<&Address>`); reject `AlreadySeated` if any run in `m5.link_runs(doc)` has `iextent().contains(link.tumbler())` — I‑extent membership over the link run‑list (CL‑UNIQ), which also catches a `link` already interior to a coalesced link run. Else return `LinkSeat{doc, link}`. The fold appends `link` at the next link V‑position (`n_L(d)+1`), coalescing with the prior link run if I‑adjacent (sequential `A_L(d)` allocations are). This eager coalesce can make `link_runs` return a width>1 link run, which does **not** violate ASN‑0047 S8★: S8★ retains run‑*uniqueness* only on the content subspace and asks merely for *a* finite run decomposition of the link subspace — its cited "trivial length‑1 decomposition" is one witness, not a requirement, so the maximally‑merged (ASN‑0058 M12) link run‑list this design produces is an equally valid S8★ witness, and immediate seating in `A_L(d)` allocation order keeps successive link addresses I‑contiguous so they collapse to that one run. **M5 trusts that M7 allocated the link** (it never reads M7 — no back‑edge) and **appends no provenance** (J‑LV: link placements are uncoupled from R). This is the deliberately *trusting* seam: M5's only guards are pure‑M1 (origin) and self‑readable (uniqueness/position); the link‑side referential integrity `M(d)(v_ℓ)∈dom(L)` is discharged by construction inside MAKELINK. The contract‑required standalone twin `seat_link<W>` (Section C, `#[doc(hidden)]`) wraps this same pure step in its own `transact` for isolation/contract‑parity testing only — production always composes `stage_seat_link` inside MAKELINK's K.λ + K.μ⁺_L transaction and never commits a seat alone.

**Fold:**
```
apply_m5(LinkSeat{doc, link}):
  k = doc.tumbler()
  arr = arrangements.get(k).cloned().unwrap_or(empty)
  w = arr.link.total_width()
  arr.link = arr.link.splice_in(w + 1, vec![Run{ i_start: link, width: 1 }])  // append at n_L(d)+1 (the append boundary, §1) + coalesce if I-adjacent
  M5State{ arrangements: arrangements.update(k.clone(), arr), prov_by_doc }   // NO R append (J-LV)
```

### 9. Provenance R and the single `(M, R)` snapshot

Because `ContentPlace`/`VersionSnapshot` update `arrangements` **and** `prov_by_doc` in one fold → one new `M5State` → one M2 root install, a reader never observes M‑updated‑without‑R. This is exactly ASN‑0075's atomic root‑swap of the M edit and the R append, achieved by **co‑location** rather than a cross‑store protocol. M6 reads both off **one** `Snapshot`:
- **SHOWDELETIONS(d)** — M6 reads M5's `deletions(d)` directly, which computes `ever_placed(d) \ content_image(d)` **per level‑class inside M5** (§2, §E): both operands are iextent‑covers that may mix origin‑lengths when `d` transcludes across heterogeneous‑depth documents, so M5 partitions each by endpoint length, runs `difference_sets` within each class, and unions the per‑class results — never a bare `difference_sets` over the mixed set. `content_image` is the M5‑internal operand (never a seam); keeping the algebra in M5 (owner of R and the iextent semantics) stops a consumer from naively faulting on a length‑gated op; per‑class is also the *correct* semantics (iextent addresses of different length are distinct addresses and cannot cancel — a currently‑arranged length‑ℓ address removes only ever‑placed length‑ℓ addresses).
- **FINDDOCSCONTAINING(region)** — `docs_containing(region)` (a `Vec<Address>` candidate superset) filtered per candidate by `project(d, region) ≠ ⟨⟩` (current‑containment; `project` already applies the level‑class discipline internally, so the filter is fault‑free for any `region`, including cross‑length prefix/subtree spans) — both primitives off the one snapshot, so the historical/current join is consistent. Current‑containment is in principle computable either way — `project(d, region) ≠ ⟨⟩` or membership against the internal `content_image(d)` — and FINDDOCSCONTAINING uses **`project`**, since it is the discipline‑encapsulating method; `content_image`'s role is therefore confined to the **SHOWDELETIONS operand** consumed only by `deletions`, never the FINDDOCSCONTAINING filter, and it stays M5‑internal rather than a public seam.

`docs_containing` scans `prov_by_doc` in v1, including a document `d` when some placed span is **not `Separated`** from some span of `coverage` under M1's `classify_spans` (pure order, total — it never faults on a length mismatch), and reconstructing each candidate's `Address` from its registered‑document `Tumbler` key via `M1::validate`; this yields an overlap‑superset (no false negatives — a genuinely contained address forces order‑overlap) that FINDDOCSCONTAINING narrows by the current‑containment filter (an interval index over R is an Open decision). **M5 owns R and any index over it; M6 owns only the FINDDOCSCONTAINING query** that composes these two primitives — see Conflicts #6.

### 10. Recovery

`M5State` is recovered by M2: load checkpoint, replay `M5Rec` deltas via `apply_m5`. `apply_m5` is pure/total/deterministic and reads only `M5State` (+ pure M1 arithmetic) — it never re‑mints or touches M3/M4 (those replay as their own records). Determinism holds for `VersionSnapshot` because records replay in journal order, so `source`'s arrangement is reconstructed to its fork‑point value before the snapshot reads it. v1 has no skip‑serialized hints, so `rebuild_derived` is the identity; adding the inverse‑arrangement or reverse‑provenance hint obliges an override that reseeds *exactly* the fold‑equivalent state. Persistent structures keep *in‑memory* snapshots cheap and VERSION's fork share O(1) (structural sharing of `im` subtrees until copy‑on‑write divergence). This sharing is an **in‑memory property only**: standard `serde` checkpoint serialization does **not** preserve cross‑value `im` structural sharing, so a checkpoint materializes the fork's shared runs as two independent copies — still correct, merely not smaller — unless a sharing‑aware codec is used (an Open decision if checkpoint size becomes a concern). A checkpoint‑recovered `Run` is built field‑by‑field through derived `Deserialize` (bypassing `Run::new`), so its `width ≥ 1` / element‑level shape rests on M2 checkpoint integrity — the same trust posture as the rest of recovery — which is what keeps `iextent` total on every recovered Run.

---

## Invariants & contracts

**By construction** (fall out of the data model above):

- **Functionality S2** — one I‑address per V‑position: the run‑list is a coverage‑disjoint partition (ASN‑0036 S2; ASN‑0058 B1∧B2).
- **Density / contiguity / minimum‑position** D‑SEQ★/D‑CTG★/D‑MIN★ — implicit positions make every V‑start a prefix sum, so no subspace can be sparse (ASN‑0047 D‑SEQ★; ASN‑0036 D‑CTG/D‑MIN/D‑SEQ).
- **Depth uniformity** S8‑depth — m = 2 everywhere (ASN‑0036 S8‑depth; ASN‑0084 scope).
- **Subspace confinement / document isolation** — per‑subspace run‑lists keyed per document: an edit on one `(doc, subspace)` cannot name another (ASN‑0082 I3‑X/D‑CS; ASN‑0084 SUBCONF; ASN‑0119 RA9).
- **Content/address permanence (NonDestruction)** — DELETE only drops arrangement entries; M5 has no content‑reclamation path (ASN‑0117 P0; ASN‑0047 P0/P3).
- **Origin invariance, no cross‑origin merge, transclusion independence** — I‑addresses are carried verbatim and coalesce only on I‑adjacency (ASN‑0036 S7; ASN‑0058 M16/M14; ASN‑0118 CP5/CP11; ASN‑0119 RA1).
- **VERSION copies the map not the range** — multiplicity‑preserving structural share (ASN‑0123 V2).
- **J0 / J1★ / J‑LV** — enforced at M5's composite boundary: INSERT binds alloc+write+place+provenance in one transaction; `ContentPlace`/`VersionSnapshot` fold M+R together; `LinkSeat` folds no R and link allocation is uncoupled (ASN‑0047 J0/J1★/J‑LV).
- **R permanence P2** — no `M5Rec` removes from `prov_by_doc` (ASN‑0047 P2).
- **Composite‑boundary provenance P4★ / P4a / P7a** — maintained by the same couplings, not separately enforced. Content enters `dom(C)` only through INSERT's K.α, and INSERT's `ContentPlace` binds that allocation to a witnessed placement‑plus‑R‑append in one composite, so **J0 + J1★ ⇒ P7a** (every `a ∈ dom(C)` carries a provenance record). Every content *placement* — INSERT and COPY's `ContentPlace`, VERSION's `VersionSnapshot` — appends each placed run's iextent to R in the same fold, so **J1★ ⇒ P4★** (`Contains_C(Σ) ⊆ R`: every currently content‑arranged pair was recorded when placed). Because that append happens *at the placement step*, **J1★ append‑at‑placement ⇒ P4a** (every R pair is witnessed by a content‑subspace V‑position in the trace state that made it). P2 monotonicity carries all three across later edits — DELETE drops a pair from `Contains_C` yet keeps its R entry, so P4★'s ⊆ only ever loses left‑hand members and P7a/P4a stand (ASN‑0047 P4★/P4a/P7a).
- **Link survival under edits** — links anchor I‑addresses; text edits never touch the link store or its anchors (ASN‑0116 IP4; ASN‑0117 P4; ASN‑0119 RA6).
- **Canonical run uniqueness** — eager coalesce keeps the resident form maximally merged (ASN‑0058 M12), recomputed never stored.
- **Well‑formed I‑extents** — every Run→Span lift goes through `Run::iextent`, which is *internally* level‑uniform by construction: the `width ≥ 1` standing invariant gives `start < reach ∧ #start = #reach` (so `from_endpoints` never faults), and the element‑level standing invariant (`zeros(i_start) = 3`) makes its raw `shift` advance the ordinal field, not the text→link separator. `Run`'s fields are crate‑private, so `Run::new` — which rejects **both** width 0 and a non‑element `i_start` — is the sole foreign *constructor*, and no foreign holder can mutate a Run it obtained (owned or borrowed; reads go through `i_start()`/`width()`) — closing the mutate‑after‑obtain path alongside foreign construction; M5's internal emission sites build them structurally, and the one remaining path (derived `Deserialize`) rests on M2 checkpoint integrity rather than the type system. The invariants therefore hold for every *minted‑or‑validly‑recovered* Run — which is exactly what justifies `iextent`'s `.expect`. A SpanSet that aggregates iextents across origin‑documents is in general **mixed‑length** (transclusion), so every set operation over R spans, the internal `content_image`, or a coverage footprint follows the level‑class discipline (§2 — per‑class `intersect`/`difference_sets` with `union`, or the total `classify_spans`/`denotes` where overlap/membership suffices), never a bare length‑gated op over the mixed set (M1 span contract).

**By active enforcement** (M5 must guard; *where*):

- **Content‑side referential integrity S3★** — COPY asserts each resolved run start `∈ dom(C)` via `M4::contains` (§5); INSERT is automatic (fresh write in the same composite) (ASN‑0047 S3★; ASN‑0036 S3).
- **Non‑transclusion / subspace routing** — COPY content‑residence (`span.start().get(1) == s_C`, §5); content placements only ever carry content addresses, link seating only the link subspace (ASN‑0118 `enabled(COPY)`; ASN‑0047 S3★‑aux).
- **CL‑OWN / CL‑UNIQ** — `stage_seat_link` checks `document_of(link).as_ref() == Some(doc)` and not‑already‑seated by I‑extent membership over the link run‑list (§8) (ASN‑0047 CL‑OWN/CL‑UNIQ).
- **Valid insertion / delete‑containment / cut preconditions / COPY source admissibility** — validated before any record is staged; rejection leaves no state change. COPY rejects an unregistered or content‑empty source (`SourceNotRegistered`/`EmptySource`, ASN‑0118 `enabled(COPY)`) and a malformed source span (`BadSpan` — not an ordinal‑level depth‑2 V‑span); REARRANGE checks both cut bounds, the CS5 lower bound `ord(c₀) ≥ 1` and the upper bound `ord(c_last) ≤ n_c+1` (both `OutOfBounds`) (ASN‑0036 ValidInsertionPosition; ASN‑0117 containment; ASN‑0084 R‑PRE/CS5).
- **VERSION P‑tier** — a cross‑owner fork requires an account‑tier forker (`M1::zeros(pfx)==1`); the node‑tier cross‑owner case is rejected explicitly as `NodeTierCrossOwner` before any mint (§7) (ASN‑0123 P‑tier).
- **Composite atomicity** — one `transact` per operation; M2 makes the contract‑then‑extend interior of INSERT/COPY non‑observable and a torn composite never visible.
- **Span‑set level‑class discipline** — every `intersect`/`difference_sets`/`intersect_sets`/`normalize` over a possibly‑mixed‑length cover is run per level‑class with `union` (or replaced by the total `classify_spans`/`denotes`). The discipline is **encapsulated inside M5** for the M6 query surface: `project` and `deletions` perform their per‑class algebra internally (§2, §E, §9), so M6 never differences/intersects a raw mixed‑length cover. The raw covers M5 *does* expose — `resolve_coverage` (→M7/M8) and `ever_placed` (operand surface) — carry the "consume under the level‑class discipline" contract on their method docs (`content_image` is M5‑internal — its mixed‑length cover never crosses a seam).

---

## Dependencies & seams

**Upstream (call as given):**
- **M1** — `Tumbler/Address/Span/SpanSet`; `shift`/`validate` (run coalescing I‑adjacency, within‑run address synthesis, `iextent`, ordinal math — raw `shift` only ever on **full element I‑starts**, M1's stated safe window, never a bare subspace base); `zeros` (VERSION P‑tier account‑tier check, and the `Run::new` element‑level seam guard); `document_of` (CL‑OWN origin check); `from_endpoints` (the `iextent` lift); `classify_spans`/`denotes`/`contains` (the **total**, length‑gate‑free overlap/membership primitives — `docs_containing`, `project`'s cross‑class fallback via `Span::contains`, FINDDOCSCONTAINING's filter, the CL‑UNIQ I‑extent membership test) and the length‑gated `intersect`/`union`/`normalize`/`difference_sets` (project within‑class, image, ever_placed, deletions) used only under the level‑class discipline (§2). V‑positions read first/second components directly (`get(1)/get(2)`) — *not* `subspace()`, which is for element‑level I‑addresses. Maps key by `Tumbler` (the `Ord`‑bearing type), not `Address`.
- **M2** — `transact` (every composite, under the M3 lock key), returns `(T, Seq)`; `snapshot` (VERSION's `ω` pre‑read; all reader access). `M5State` is the WorldState slice, `M5Rec` the delta, `apply_m5` the fold.
- **M3** — pure mints `mint_content` (INSERT), `mint_version`/`mint_document` (VERSION), each with its lock key (`M3State::content_lock_key`/`version_lock_key`/`document_lock_key`) taken *before* the closure; `is_registered_document` (edit preconditions); `effective_owner`/`principal_prefix` (VERSION branch, pre‑read off a snapshot). M5 → M3 only.
- **M4** — `stage_write` (INSERT byte write, composed into M5's transaction); `contains` (COPY content‑side referential gate). M5 → M4, no back‑edge.

**Serialization key (M5 has no `Space` tag of its own).** Every M5 mutation serializes under an **M3** lock key for the touched document's allocation domain: content edits (INSERT/DELETE/COPY/REARRANGE) under `content_lock_key(doc)` (taken by M5 before its `transact`); VERSION under `version_lock_key`/`document_lock_key`; link seating under `link_lock_key(doc)` (taken by M7's MAKELINK, which composes M5's `stage_seat_link`). A document's arrangement edits and their R‑appends are therefore co‑serialized under that one key, and **the engine assembler allocates no M5 `LockKey` space tag** — M5 contributes a slice and a record, but no `Space` enum variant.

**Build precondition.** `M5State`'s `Serialize`/`Deserialize` derive requires the **`im` crate built with its `serde` feature** (M5 owns `im::OrdMap`/`im::Vector`) *and* `Tumbler: Serialize/DeserializeOwned` (M1's `num-bigint` serde feature, on the crate owning `Tumbler`); without either, no M5 checkpoint serializes. `DocArrangement` carries `#[derive(Clone, Default, Serialize, Deserialize)]` (Core data model), required transitively by `M5State`'s derives.

**Downstream (seam contracts neighbors build against):**
- **→ M6** — `resolve`/`point` (RETRIEVEV, extent queries, COMPARE via `content_runs` on multiple docs off one snapshot); `deletions` (SHOWDELETIONS — M5 computes the per‑level‑class `ever_placed ∖ content_image` difference, §E/§9; `content_image` is the M5‑internal operand, not a seam) and `docs_containing` + `project` (FINDDOCSCONTAINING) — both read one consistent `(M,R)` snapshot. M6 reads SHOWDELETIONS straight off `deletions`, and computes the FINDDOCSCONTAINING current‑containment filter as `project(d, region) ≠ ⟨⟩` (`project` applies the level‑class discipline internally, so the filter is fault‑free for any `region`, including cross‑length prefix/subtree spans). `content_image` is **not** a public seam — it is the M5‑internal `deletions` operand (§9), so M6 touches it only transitively through `deletions`, never directly, and the FINDDOCSCONTAINING filter is `project`, not `content_image`. Because `resolve`/`point` are **defensive** — they fold every malformed request into ⟨⟩/`None` rather than returning a `Result` — **M6 pre‑validates request‑built V‑spans against the published complete guard** (`#start == 2 ∧ #width == 2 ∧ width.get(1) == 0`, with `start.get(1) ∈ {s_C, s_L}`) and rejects a failing request with its own typed error *before* calling; the guard is published as COMPLETE precisely so M6 can distinguish "bad request" from "genuinely empty" up front rather than inferring it from ⟨⟩. `docs_containing` hands M6 a `Vec<Address>` candidate superset; **M5 owns R, the iextent algebra, and any index over R; M6 owns only the composing query** (Conflicts #6). M5 returns ⟨⟩ for an absent doc; M6 disambiguates registered‑empty vs unallocated via M3.
- **→ M7** — `resolve_coverage` (turn endset V‑regions into I‑coverage as a `SpanSet` — the centralized `iextent` lift, so M7 doesn't re‑derive it and inherits the level‑class warning, including that its coverage‑class dedup key is formed *per level‑class*, never one `canonical_key` over the raw cover — see the `resolve_coverage` doc, §D; `resolve` remains for run‑level needs) and `stage_seat_link` (pure step folded into MAKELINK, returns `M5Rec`; its `#[doc(hidden)]` standalone twin `seat_link<W>` exists for isolation/contract‑parity only). M5 never reads M7.
- **→ M8** — `resolve`/`resolve_coverage` (V→I image), `project` (I→V *content* footprint, fragmentation‑ and length‑class‑tolerant; content subspace only — link reverse‑discovery is M7's BH3), `content_count`/`link_count`. The materialized inverse‑arrangement hint, if built, lives here.
- **→ M9** — `Vstream::insert` for predicate‑definition content (rides M5's placement composite, satisfies J0); returns the def's content start‑address as its identity. (M9 reads the def back via M4 `value_at`; M9's M7 writes are not M5's concern.)
- **→ M10** — `insert`/`delete`/`copy`/`rearrange`/`version`, each one `transact` returning `(…, Seq)`; M10 (like M9) obtains the surface via `Vstream::new(&kernel)`, acknowledges only after commit, and surfaces `TxnError::Rejected(E)` as typed rejections.
- **→ engine** — `M5State` slice, `M5Rec` record, `HasM5` accessor, `apply_m5` fold, `genesis`; the assembler implements `HasM5 for World`, `From<M5Rec> for Record`, and dispatches `Record::M5(x) => world.m5().apply_m5(x)` — moving the whole `M5Rec`, never destructuring it (the `#[non_exhaustive]` variants forbid that outside M5's crate anyway). M5 names neither `World` nor the central `Record`, and contributes **no `Space` tag** (it serializes on M3's keys — see *Serialization key* above).

---

## Conflicts resolved

1. **Link‑subspace gaplessness.** ASN‑0036/0082 model the link subspace as sparse/tombstone‑permitted; ASN‑0047 (the integrating note) *strengthens* it to dense‑gapless (D‑SEQ★, suffix‑only `K.μ⁻`). **Resolution:** follow ASN‑0047 — both subspaces are dense run‑lists, links seated by append; **interior link withdrawal is not offered** (ASN‑0047 leaves it open and Green's behavior is contested). Content interior deletion *is* offered (DELETE = contract‑then‑reseat, keeping the content subspace dense — ASN‑0117). (Eager link coalescing produces width>1 link runs; this is reconciled with S8★'s "trivial length‑1 decomposition" in §8 — S8★ requires *a* link decomposition, not the length‑1 one.)
2. **"Referential‑integrity gate checked via M3" (decomposition) vs. the content‑presence oracle.** The S3★ predicate that matters for resolve/retrieve is content *presence*, whose declared oracle is `M4::contains` (M4 interface). **Resolution:** COPY gates on `M4::contains` (presence); `M3::is_allocated` is the distinct allocation‑axis check, not used here. INSERT needs no gate (fresh write in‑composite).
3. **COPY run‑coalescing guard.** ASN‑0118 notes udanax coalesces on `homedoc` equality (immediate source), while bare I‑contiguity coalesces strictly more and drops the immediate‑source distinction (its OQ4). **Resolution:** coalesce on **I‑adjacency** — the spec‑correct, M16‑safe guard; the immediate‑source/correspondence distinction is not carried (consistent with not building the correspondence relation).
4. **Journal granularity (intent vs. effect).** ASN‑0116/0119 weigh logging the operation vs. the effect. **Resolution:** **effect‑level** deltas (concrete addresses/ordinals) — *forced* by M2's fold being pure and upstream‑blind (it cannot re‑mint). `VersionSnapshot{source,new}` is the one structural‑share record whose fold reads source (O(1)); an explicit‑runs alternative is noted in Open decisions.
5. **R recomputability.** The decomposition calls R "non‑recomputable." **Resolution:** non‑recomputable *from the current arrangement* (P2 keeps deleted pairs), but recovered by *journal replay* like the POOM — authoritative journaled slice state, not a hint.
6. **Reverse‑provenance index ownership (decomposition vs. seam reality).** The decomposition lists "the reverse‑index hint over R" under **M6** (alongside FINDDOCSCONTAINING). But M6 sees only M5's pure `docs_containing` surface and **cannot iterate R** to build such an index. **Resolution:** **M5 owns R and any index over it** — the candidate‑set primitive `docs_containing`, and the optional coverage→docs interval index of Open decision #3 if built; **M6 owns only the FINDDOCSCONTAINING *query*** that composes `docs_containing` (historical candidates) with `project` (current‑containment filter) over one snapshot. The decomposition's placement is read as naming the *query*, not the index.
7. **COPY source‑span shape: ASN‑0118's general‑T12 VSpec vs. ASN‑0058's ordinal‑displacement form.** ASN‑0118's VSpec admits any T12‑well‑formed source span; M5's COPY `BadSpan` guard (§5) narrows that to an **ordinal‑level depth‑2 V‑span** — ASN‑0058 C0's ordinal‑displacement form (width `[0,n]`, action point 2). **Resolution:** accept only the ordinal form. At the committed m = 2 this is **lossless**: every legitimate copy — including a "to end" over‑reach — is an over‑reaching ordinal span clipped by accept‑and‑intersect (`resolve`), and the only T12 shapes it rejects (action‑point‑1, level‑uniform `[m,n]` widths) are degenerate cross‑subspace at m = 2. So the narrowing refuses no real transclusion and hands M10 a precise `BadSpan` verdict where ASN‑0118's literal VSpec would silently `resolve` to nothing (an `EmptyResult` indistinguishable from an empty range).

---

## Open build decisions

1. **Physical `RunList` structure** (meets one contract either way): `im::Vector<Run>` (v1 default — free structural sharing, `O(#runs)` linear locate, splice via split/insert/concat; fine because #runs scales with transclusions/edit‑sessions, not characters); a **custom `Arc`‑shared width‑measured tree** (`O(log #runs)` locate/splice, no re‑keying) when profiling shows large run counts; or `im::OrdMap<ordinal, Run>` (predecessor‑search locate, `O(suffix)` re‑key on splice).
2. **Inverse‑arrangement (I→V) hint** for `project`: scan the forward map (v1 default) vs. a materialized, skip‑serialized hint in `M5State` (rebuilt by `rebuild_derived`, maintained by `apply_m5`) if footprint projection is measured hot — note that a splice shifts the suffix, so incremental maintenance is non‑trivial.
3. **Reverse‑provenance (coverage→docs) index** for FINDDOCSCONTAINING — **M5‑owned** (M6 cannot build one from the pure `docs_containing` surface; Conflicts #6): scan `prov_by_doc` (v1) vs. an interval/segment index hint at scale.
4. **`VersionSnapshot` record form:** `{source, new}` with the fold sharing source's run‑list (recommended; O(1), structural share) vs. explicit `{new, runs}` (larger record, self‑contained, decoupled from source's replay state).
5. **COPY referential‑gate strength:** assert resolved run *starts* via `M4::contains` (recommended; cheap, relies on source S3★ for interiors) vs. full‑run `contains` (expensive) vs. trust the source arrangement's S3★ validity and skip.
6. **Depth m:** fixed at 2 (recommended; semantically inert, matches the reference implementation and ASN‑0084's scope) vs. general depth behind the V‑side arithmetic seam — which reopens ASN‑0082's contraction inverse‑law gap at depth > 1 and a depth‑compatibility precondition on INSERT.
7. **Checkpoint structural‑sharing codec:** plain `serde` (v1 default — correct, but materializes VERSION's shared runs as independent copies on disk) vs. a sharing‑aware checkpoint codec that preserves cross‑value `im` sharing, if checkpoint size on heavily‑forked docuverses becomes a concern (§10).
8. **Coalesce timing:** **eager** seam‑coalesce after every mutator (v1 default — the resident run‑list is always the unique maximally‑merged decomposition (ASN‑0058 M12), so `resolve`/`content_runs`/`link_runs` read run structure directly, and `extend_run`/`extend_or_push_run` apply the same rule incrementally during INSERT/COPY accumulation) vs. **lazy** (store possibly‑splittable runs, coalesce on output in `resolve`/`content_runs`) — the latter trades a cheaper mutator for a coalescing pass on every structural read. Either meets the run‑structure contract; §1 is written against eager.
