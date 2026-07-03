# M8 — Link Query & Discovery — Detailed Design

## Purpose & boundary

M8 is the **read-only query/presentation layer over the link subsystem**: given a content region it answers *which links touch here*; given a four-set descriptor it answers *which links match*; and it counts, paginates, projects, retrieves endsets, previews delete-orphaning, and traces supersession lineage — all by composing M7's spanfilade and behavior atoms, M5's arrangement, and M3's registry over one M2 snapshot. It does **one thing well: turn upstream link/arrangement/registry state into the answers readers ask, owning no authoritative state and no index.**

What it does *not* do, deferred to neighbors: it does **not** own the spanfilade or any coverage index, and does **not** implement the per-slot matcher or the AND-of-ORs combiner — those are M7's `stab`/`match_links`/`type_slice` (the soft seam, resolved below). It stores no coverage (M7's `followlink`), reads no content bytes (M4), reads no provenance R and runs no R-keyed query — SHOWDELETIONS/FINDDOCSCONTAINING are M6's. It never invokes M5's edit path (the survival check is a pure what-if), never mints or writes anything, and is **fenced off from M9** (ASN-0129): M9 reads its PL surface straight from M7, never through M8. M8 is pure composition; every answer is recomputed from upstream on each call.

## Public interface

Foreign types: `Address/Span/SpanSet/Nat/Tumbler` (M1); `Kernel/Snapshot/Seq/WorldState` (M2); `Run/VPos` (M5); `Endset/View/ShippedType/HasLinks` (M7); `HasM5` (M5); `HasM3` (M3). Slots are 1-based, M7's convention; `s_C = 1` (content subspace, ASN-0047).

```rust
pub const FROM: usize = 1;  pub const TO: usize = 2;  pub const TYPE: usize = 3;

/// Per-slot request component for the four-set descriptor query (the three-way distinction
/// the conjunction needs — ASN-0121).
pub enum SlotSpec {
    Any,            // ∗ / NOSPECS — the unit: drops out of the conjunction
    Empty,          // ∅ constrained-empty — the zero: annihilates the whole result
    Spans(Endset),  // populated address-spans (M7's readable Endset); MUST be NON-EMPTY — an empty
                    // Endset is normalized onto the Empty/zero path (M7 forbids an empty match_links Endset)
}

/// q = (H, F, G, Θ). `home` is matched against home(a) (an address projection), NOT a slot.
pub struct FourSet { pub home: SlotSpec, pub from: SlotSpec, pub to: SlotSpec, pub ty: SlotSpec }

pub type Cursor = Option<Address>;                 // None = ⊥ (start); Some(a) = resume strictly past a
pub struct Window  { pub batch: Vec<Address>, pub next: Cursor, pub exhausted: bool }
pub struct SupClaim { pub claim: Address, pub old: Address, pub new: Address,
                      pub home: Address, pub active: bool }
pub struct OrphanReport { pub orphaned: Vec<Address> }   // links the proposed DELETE drops from d

pub enum QueryError { DocNotRegistered, NotALink, BadRegion,
                      NotContentSubspace, EmptyWidth, OutOfBounds }  // last three: delete_orphans preview, mirroring M5
                                                                     // DeleteError (OutOfBounds folds M5's NotArranged — §6)

pub struct LinkQuery<'k, W: WorldState> { kernel: &'k Kernel<W> }
```

```rust
impl<'k, W> LinkQuery<'k, W>
where W: WorldState + HasLinks + HasM5 + HasM3
{
    pub fn new(kernel: &'k Kernel<W>) -> Self;

    // ── Content-region discovery (V-anchored, present-tense, doc-gated; disjunctive over slots; ──
    // ── every result is foundation ∩ View::Active = addressable, so nullified links never appear) ──
    /// V→I resolution of `region` through d's live arrangement (ASN-0127 image). Deduped at the
    /// boundary by `Run: Eq` — no exact-equal Run repeat; overlapping INPUT region spans may still
    /// yield partially-overlapping runs (not an address-disjoint partition — don't sum widths).
    pub fn image(&self, d: &Address, region: &[Span]) -> Result<Vec<Run>, QueryError>;          // V→I
    /// result = foundation ∩ active (View::Active) — nullified links never surface; diverges from
    /// ASN-0127's UNFILTERED findlinks_V (active only).
    pub fn findlinks_v(&self, d: &Address, region: &[Span]) -> Result<Vec<Address>, QueryError>;
    /// Present-tense census; result = foundation ∩ active — nullified links never surface.
    pub fn count_v(&self, d: &Address, region: &[Span]) -> Result<usize, QueryError>;
    /// Windowed enumeration (ASN-0108); result = foundation ∩ active — nullified links never
    /// surface. `n = 0` is clamped to 1 (the API is total).
    pub fn window_v(&self, d: &Address, region: &[Span], cur: Cursor, n: usize)
        -> Result<Window, QueryError>;
    pub fn retrieve_endsets(&self, d: &Address, region: &[Span])
        -> Result<Vec<(usize, Endset)>, QueryError>;                                            // ASN-0131

    // ── Four-set descriptor query (address-keyed, conjunctive, link-store-local, monotone absent retraction) ──
    pub fn findlinks_ftt(&self, q: &FourSet) -> Vec<Address>;                                   // ASN-0121
    pub fn count_ftt(&self, q: &FourSet) -> usize;                                              // ASN-0132 (the count op)
    pub fn window_ftt(&self, q: &FourSet, cur: Cursor, n: usize) -> Window;                     // ASN-0108 (FTT Match reading)

    // ── Pointwise projection & discoverability (content subspace) ──
    /// I→V projection of link `a`'s slot into d's CONTENT subspace (ASN-0098 project). Content-
    /// subspace ONLY — strictly weaker than ASN-0098's subspace-agnostic project; a link reachable
    /// solely through d's LINK subspace projects ∅ here. The link-subspace POSITIONAL projection that
    /// would close that gap is NOT M7's BH3 (BH3 is typed reverse *lookup*, target→sources) — it is
    /// the scoped-out contextual EL11a (§7, via an M5/M6 listing check).
    /// `NotALink` subsumes BOTH `a ∉ dom(L)` AND an out-of-range `slot` (M7's followlink conflates them).
    pub fn project(&self, a: &Address, slot: usize, d: &Address) -> Result<SpanSet, QueryError>;// ASN-0098 I→V
    /// NOT pure LP12 — active-filtered. Compound "arrangement-reachable AND active": a
    /// nullified-but-reachable link returns Ok(false) where LP12 would call it discoverable. For
    /// raw LP12 compose `followlink` + M5 `project`. NotALink if a ∉ dom(L).
    pub fn discoverable_from(&self, a: &Address, d: &Address) -> Result<bool, QueryError>;

    // ── Pre-edit link-survival (read-only; never touches the edit path) ──
    /// Pre-edit what-if (read-only; never the edit path). result = foundation ∩ active — a nullified
    /// link that lost its last witness in d is NOT reported (diverges from ASN-0117's D(d,Σ) over
    /// dom(L)). Mirrors DELETE's preconditions: NotContentSubspace / EmptyWidth / OutOfBounds —
    /// OutOfBounds deliberately folds M5's NotArranged + OutOfBounds (jointly equivalent under width ≥ 1).
    pub fn delete_orphans(&self, d: &Address, p: &VPos, width: &Nat)
        -> Result<OrphanReport, QueryError>;                                                    // ASN-0117

    // ── Archival supersession/edit lineage (y/x intended as resident link addresses — dom(L)) ──
    /// v: Active = operative graph (succ_o), Audit = full history (succ_h); Default behaves as
    /// Active (M7's §G primitives coerce it).
    pub fn in_claims(&self, y: &Address, v: View) -> Vec<SupClaim>;   // claims with old = y
    pub fn out_claims(&self, x: &Address, v: View) -> Vec<SupClaim>;  // claims with new = x
}
```

**Snapshot twins.** Every method `foo(&self, args…) -> R` is *exactly* `foo_on(&self.kernel.snapshot(), args…)`: the handle takes **one** fresh snapshot and delegates; **all internal composition then threads that one `snap`** (an op never re-snapshots — that is what discharges the one-`(L, M, registry)` coherence ASN-0127 forces). The pure `foo_on(snap: &Snapshot<W>, …)` free functions are public, generic over `W: WorldState + HasLinks + HasM5 + HasM3`, and are what **M10 calls to read a count and its window — or any multi-call verdict — off one consistent state** (the ASN-0132 snapshot-token need; M2 clause 6). The twin signatures:

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

`coverage(a, i)` is **not** re-exposed — it is exactly M7's `followlink(a, i)`; callers use M7 directly.

## Core data model

**M8 owns no `WorldState` slice, no journal record, no fold, and no index.** It contributes nothing to the assembled `World` and journals nothing; it names neither `World` nor `Record` (generic over `W` with `HasLinks + HasM5 + HasM3`). Its crate `skep-linkquery` depends on the pure surfaces of M1/M2/M3/M5/M7 and is depended on only by M10 — it is a query crate, not a store.

Its "data model" is therefore just (a) the request/result value types above and (b) one load-bearing representation decision:

- **Result sets are carried internally as `im::OrdSet<Tumbler>` — M7's native discovery return type — and converted to `Vec<Address>` only at the output boundary.** M7's primitives yield `&Tumbler` under iteration (`iter`/`range`); M8 **clones each key and `validate`s it at the lift** — infallible, since every key is a T4-valid minted address (M7's §G→§F note). This is the whole engine: `union`/`difference`/`range` on a persistent ordered set are cheap and structurally-shared, and **`OrdSet<Tumbler>` is ordered by tumbler = link address = exactly ASN-0108's permanent enumeration key.** So windowing is a `range(Excluded(cursor)..).take(n)` — no M8-side index, no re-sort. This is what lets M8 "own no index" yet page efficiently. The same convert-at-the-boundary discipline applies to every M7 `im` container M8 touches: each result `OrdSet<Tumbler>` is collected to `Vec<Address>` before it crosses the public seam. (RETRIEVEENDSETS deduplicates its `(slot, endset)` pairs in a throwaway `std::collections::HashSet` — *not* an `im` container — so nothing `im`-shaped reaches that seam either.)

- **Authoritative state owned: none.** The link store, active/audit slices, spanfilade, type registry (M7); arrangements and R (M5); registry (M3). **Recomputable hints owned: none.** M8 recomputes every answer from upstream each call; the only index it leans on (M7's spanfilade) is M7's hint, recovered by M7. The unit of consistency is the M2 `Snapshot` threaded through one operation.

A second, quieter discipline shapes every algorithm: **M8 does almost no span algebra itself — and never the level-gated kind.** Mixed-length covers (a content address and a link address differ in tumbler length) fault M1's `intersect_sets`/`difference_sets` with `LevelMismatch`. M8 sidesteps this entirely — coverage-overlap matching goes through M7's `stab`/`match_links` (M7 handles level classes), I→V projection goes through M5's `project` (handles them internally), and query `Endset`s are built from `Run::iextent()` via `Endset::from_spans` (verbatim, no algebra). M8 never differences or intersects raw covers; it set-operates only on `OrdSet<Tumbler>` (addresses, uniform — no level issue). The lone span-level computation it performs is `discoverable_from`'s per-link `classify_spans` touch test (§5) — a pure, *level-gate-free* order relation (total on cross-length spans, never faulting), categorically distinct from the level-gated set algebra it avoids; even RETRIEVEENDSETS' slot attribution is read off M7's per-slot stab sets rather than tested locally (§4).

## Internal design

Every operation opens with one snapshot and reads `links() / m5() / m3()` off `snap.world()` — never separate snapshots (the (L, M) coherence ASN-0127 forces). All pseudo-code below is the threaded `foo_on(snap, …)` form: it binds `let w = snap.world();` once and composes internal steps as `image_on(snap, …)` etc. — **never `self.image`, which would open a second snapshot.** "Recovery" is trivial and uniform: M8 persists nothing; each answer is recomputed from upstream state, which M2 recovers by replay. I omit it per capability below.

Three free helpers and a region gate are shared throughout:

```rust
/// Lift M7's native discovery keys to validated addresses, at the OUTPUT boundary only.
fn addrs(keys: &im::OrdSet<Tumbler>) -> Vec<Address> {
    keys.iter().map(|t| validate(t.clone()).unwrap()).collect()   // clone &Tumbler; validate infallible (M3 mint)
}
/// Per-slot Active stabs over {FROM, TO, TYPE}, kept SEPARATE (slot attribution reads them — §4).
/// Exact over ALL slots by the v1 arity-3 invariant (§1). View::Active discharges addressability.
fn stab_slots<W: HasLinks>(w: &W, q: &Endset) -> [im::OrdSet<Tumbler>; 3] {
    [FROM, TO, TYPE].map(|i| w.links().stab(i, q, View::Active))  // fresh View::Active literal per slot — no `View: Copy` needed
}
/// The disjunctive ASN-0127 findlinks(I) core ∩ the active view: OR across slots {FROM,TO,TYPE}.
fn stab_union<W: HasLinks>(w: &W, q: &Endset) -> im::OrdSet<Tumbler> {
    let [f, t, y] = stab_slots(w, q);
    f.union(t).union(y)
}
/// Region gate: each span must be a CONTENT-subspace, ordinal-level, depth-2 V-span (else BadRegion).
fn check_region(region: &[Span]) -> Result<(), QueryError> {
    for s in region {
        let (st, wd) = (s.start(), s.width());
        let ok = st.len() == 2 && wd.len() == 2
              && *st.get(1) == Nat::one()    // start[1] = subspace = s_C (= 1)
              && wd.get(1).is_zero();         // width[1] = 0 ⇒ ordinal-level displacement
        if !ok { return Err(QueryError::BadRegion); }
    }
    Ok(())
}
```

### 1. Content-region discovery (`image`, `findlinks_v`, `count_v`)

**The document-existence gate is the first act of every V-anchored op, immediately followed by the region gate.** M5's reads return empty for *both* registered-empty and unallocated documents — it cannot tell them apart — and silently clip a malformed span rather than rejecting it. So `image_on` discharges both before any resolve:

```rust
fn image_on(snap, d, region) -> Result<Vec<Run>, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    check_region(region)?;                                  // BadRegion: not content-subspace depth-2 V-spans
    let mut runs: Vec<Run> = vec![];
    for span in region {
        for r in w.m5().resolve(d, span) {                 // resolve clips silently to arranged positions
            if !runs.contains(&r) { runs.push(r); }        // dedup by Run: Eq — no exact-equal repeat (overlapping inputs may still yield overlapping runs)
        }
    }
    Ok(runs)
}
```

A registered-but-empty `d` then yields a legitimate `∅` (defined); an unregistered `d` surfaces as `DocNotRegistered`, not a masquerading "no links here"; a non-content / non-depth-2 region surfaces as `BadRegion`, not a silently-clipped different query (ASN-0127 F-IMG/F-V; ASN-0131; the decomposition seam).

**`image`** resolves the V-region to I-runs through the live arrangement. I use `resolve` (runs), **not** `resolve_coverage` (an opaque `SpanSet`) — runs carry `i_start + width`, expose `iextent() -> Span`, and dodge both the `SpanSet`-iteration gap and the level-class trap. `resolve` is defensive (silently clips out-of-range, returns `⟨⟩` for a malformed span), so the image is exactly the currently-arranged subset of the region (ASN-0127's load-bearing `W ∩ dom M(d)` intersection — unarranged positions contribute nothing). The returned `Vec<Run>` is **deduped at the boundary** (by `Run: Eq`), so it carries no exact-equal repeat — but that is the extent of the set claim: overlapping *input* region spans can resolve to partially-overlapping runs, so the list is not an address-disjoint partition and a caller summing widths overcounts |image| (coalescing would need run-level span algebra M8 deliberately avoids — the doc-comment scopes the claim instead). Downstream the dedup is belt-and-suspenders, the runs feeding a set-valued `from_spans`/`stab` pipeline that is repeat- and overlap-idempotent.

**`findlinks_v`** is the disjunctive ASN-0127 `findlinks(image(W,d))`, **intersected with the active view** (`View::Active` — the addressability the operation owes its readers; reconciled in *Conflicts resolved* #8). So `findlinks_v`/`count_v`/`window_v` realize *foundation ∩ addressable*, **not** ASN-0127/0108's unfiltered `findlinks_V`/`Match`: a nullified link never appears, even when still arrangement-reachable.

```rust
fn findlinks_v_set_on(snap, d, region) -> Result<im::OrdSet<Tumbler>, QueryError> {
    let w = snap.world();
    let img = image_on(snap, d, region)?;                      // gate + region-check + resolve, on THIS snap
    if img.is_empty() { return Ok(im::OrdSet::new()); }        // F-V empty short-circuit, no index touch
    let q = Endset::from_spans(img.iter().map(Run::iextent));  // coverage(q) = the image
    Ok(stab_union(w, &q))                                      // stab_union is View::Active internally == addressable == dom(L) \ nullified
}
fn findlinks_v_on(snap, d, region) -> Result<Vec<Address>, QueryError> { Ok(addrs(&findlinks_v_set_on(snap, d, region)?)) }
fn count_v_on    (snap, d, region) -> Result<usize, QueryError>        { Ok(findlinks_v_set_on(snap, d, region)?.len()) }
```

The OR-across-slots is the union of single-slot stabs (M7 has no slot-collapsed primitive); `View::Active` discharges addressability *for free*. The common case is small — a region resolves to a handful of runs, each stab is a logarithmic spanfilade probe.

**v1 arity-3 invariant (the exactness of `{FROM, TO, TYPE}`).** Every v1 link-creation path — `makelink` (from/to/ty), `emit`/`nullify`/`assert_sup` (3-slot tuples), `editlink` (rejects arity ≠ 3) (all M7) — deposits an **arity-3** link. So slots `{FROM, TO, TYPE}` *are* all slots of every v1 link, and the union over `{1,2,3}` is the **exact** ASN-0127 disjunction, not an approximation. Should a future arity-≥4 type with content-reaching extra slots ship, this union ceases to be exhaustive and needs an M7 `stab_any`/exposed-max-arity extension — the one place M8's fidelity depends on an M7 capability not in the current interface (pinned in *Open build decisions*).

**`count_v`** = `findlinks_v_set_on(...).len()`. It is the present-tense census of region-reaching links — non-monotone (ASN-0127 D-NONMONO), and a `0` asserts present unreachability (over the active view), not history (D-ZERO; refined invariant below).

### 2. Windowed enumeration (`window_v`, `window_ftt`) — the cursor mechanism

The protocol is **stateless**: the entire continuation is the client's cursor, a permanent **link address** (ASN-0108 W2/W3). No server iterator, no cached list, no generation counter. Each call recomputes the matching set and key-cuts it. One combinator drives both windows:

```rust
fn window_over(matched: &im::OrdSet<Tumbler>, cur: Cursor, n: usize,
               keep: impl Fn(&Tumbler) -> bool) -> Window {
    let n = n.max(1);                                          // total API: n = 0 would give exhausted = (0<0) = false,
                                                              // an empty batch with an unchanged cursor — a silent non-terminal
    let lo = match &cur { None => Unbounded, Some(c) => Excluded(c.tumbler().clone()) };
    let batch: Vec<Address> = matched.range((lo, Unbounded))   // ascending = address order = the key
        .filter(|t| keep(*t))                                  // t: &&Tumbler → deref to &Tumbler
        .take(n)
        .map(|t| validate(t.clone()).unwrap())                 // clone &Tumbler at the lift; infallible
        .collect();
    let next = batch.last().cloned().or(cur);                  // ≺-max of batch, else cursor unchanged
    Window { exhausted: batch.len() < n, batch, next }
}
fn window_v_on  (snap, d, region, cur, n) -> Result<Window, QueryError> {
    let m = findlinks_v_set_on(snap, d, region)?;              // gate + region-check inside
    Ok(window_over(&m, cur, n, |_| true))
}
fn window_ftt_on(snap, q, cur, n) -> Window {
    let m = match_core(snap.world(), q);                       // §3
    window_over(&m, cur, n, |t| home_ok(q, t))                // home filter LAZILY during the range walk
}
```

Why this is correct and cheap:

- **Resume is a key-cut, never an exact-match scan for the cursor link** — `range(Excluded(c)..)` returns the matchers with address strictly greater than `c`, *whether or not `c` is still in `matched`*. The key-cut gives **cursor-survives-orphaning by construction** (W8): the address key is computable from the held cursor with zero lookups, and the cut needs nothing else.
- **The matching set is recomputed each call against the live snapshot**, but the recompute is itself O(seek + N) because M7 hands back `OrdSet<Tumbler>` *already in key order*. M8 owns no cache, so present-tense correctness (W7, never serve a stale view) is free.
- **No duplicate, no skip** of continuously-matching links (W4/W5): the address key's comparisons never move, so a delivered link stays below every later cursor. **Append-at-tail** for newly created links holds within a home document (addresses are allocation-monotone, W6) — the documented cross-home blind spot stands (cross-home order is not state-recoverable).
- **Exhaustion = short window**, zero included: `exhausted = batch.len() < n` (W9). The caller stops on the first short batch.

`window_v`'s set is `findlinks_v` (disjunctive V-region — the ASN-0108 `Match = findlinks_V` reading); `window_ftt`'s set is `match_core`'s (below) — ASN-0108's *other* Match reading, `Match = findlinks_FTT`, the **same windowing mechanism instantiated over the conjunctive descriptor family** — with the home filter applied **lazily during the range walk** (`keep = home_ok`) — so a home-narrow query never materializes the full filtered set. (ASN-0108's cursor/window theory is thus instantiated over *both* Match readings.) Caller obligation: `n ≥ 1` — and a passed `n = 0` is **clamped to `1`** in `window_over` (an unclamped `n = 0` yields `exhausted = (0 < 0) = false` with an empty batch and an unchanged cursor, a silent non-terminating signal), so the windowed API is total.

### 3. Four-set descriptor query (`findlinks_ftt`, `count_ftt`, `window_ftt`)

This is the **address-keyed, conjunctive, link-store-local** family (ASN-0121/0132) — *not* the V-region disjunctive one (ASN-0121 is explicit: neither is a restriction of the other). No document gate (it reads only `Σ.L`, FL-LOC). The request arrives already phrased over addresses (V→I resolution is upstream).

```rust
fn match_core<W: HasLinks>(w: &W, q: &FourSet) -> im::OrdSet<Tumbler> {
    for s in [&q.home, &q.from, &q.to, &q.ty] {               // FL-EMP: any constrained-empty slot annihilates
        match s {                                             // an empty Spans Endset ≡ Empty (the zero) — never reaches M7
            SlotSpec::Empty => return im::OrdSet::new(),
            SlotSpec::Spans(e) if e.is_empty() => return im::OrdSet::new(),
            _ => {}
        }
    }
    let mut cons = vec![];                                    // FL-WILD: Any drops out
    if let SlotSpec::Spans(e) = &q.from { cons.push((FROM, e.clone())); }   // e non-empty (checked above)
    if let SlotSpec::Spans(e) = &q.to   { cons.push((TO,   e.clone())); }
    if let SlotSpec::Spans(e) = &q.ty   { cons.push((TYPE, e.clone())); }
    w.links().match_links(&cons, View::Active)               // AND-of-ORs over constrained slots; [] ⇒ whole active slice
}
fn home_ok(q: &FourSet, a: &Tumbler) -> bool {              // athome(a, H): home(a) ∈ coverage(H)
    match &q.home {
        SlotSpec::Any      => true,
        SlotSpec::Empty    => false,                         // already short-circuited in match_core
        SlotSpec::Spans(h) => {
            let aa  = validate(a.clone()).unwrap();          // clone &Tumbler; infallible
            let doc = document_of(&aa).unwrap();             // home(a); Some for any link address (zeros = 3)
            h.denotes(doc.tumbler())
        }
    }
}
fn findlinks_ftt_on(snap, q) -> Vec<Address> {
    match_core(snap.world(), q).iter().filter(|t| home_ok(q, *t))
        .map(|t| validate(t.clone()).unwrap()).collect()
}
fn count_ftt_on(snap, q) -> usize { match_core(snap.world(), q).iter().filter(|t| home_ok(q, *t)).count() }
```

The all-wildcard `(∗,∗,∗,∗)` is `match_links(&[], Active)` = the whole addressable slice (FL-WILD). Normalizing an empty-coverage `SlotSpec::Spans` onto the zero path means M7's `match_links` is **never handed an empty `Endset`** (which it forbids) — and the result, `∅`, is exactly FL-EMP. **The home filter is an address projection (`document_of`), never an arrangement-presence test** — a reverse-orphaned link (its own home entry deleted) still satisfies a home-bounded query (CN-STAB; the cautionary CN home note). A home-only query degrades to a full active scan (no slot narrows it) — accepted, since M8 owns no index dimension. This family is **monotone absent retraction** (FL-MON/CN-MONO carry exactly that hypothesis): `dom(L)` only grows and coverage is permanent, so a found link stays found *unless retracted* — the active slice itself shrinks under nullification.

### 4. RETRIEVEENDSETS (`retrieve_endsets`)

Same selection index as `findlinks_v`, a different read-out: report `(slot, endset)` pairs touching the region, **withholding link identity** (ASN-0131 RE-UNIT).

```rust
fn retrieve_endsets_on(snap, d, region) -> Result<Vec<(usize, Endset)>, QueryError> {
    let w = snap.world();
    let img = image_on(snap, d, region)?;                        // gate + region-check inside, on THIS snap
    if img.is_empty() { return Ok(vec![]); }
    let q = Endset::from_spans(img.iter().map(Run::iextent));
    let s = stab_slots(w, &q);                                   // per-slot stabs KEPT SEPARATE — slot i of a
                                                                 // touches iff a ∈ s[i-1]; sel = findlinks_v ∩ active
    let cand = s[0].clone().union(s[1].clone()).union(s[2].clone());
    let mut out = std::collections::HashSet::new();              // INTERNAL throwaway dedup by structural Eq — never crosses a seam
    for c in cand.iter() {
        let link = w.links().readlink(&validate(c.clone()).unwrap()).unwrap();  // resident (from active slice)
        for i in [FROM, TO, TYPE] {                              // = ALL slots in v1 (arity-3 invariant)
            if s[i - 1].contains(c) {                            // M7's overlap verdict IS the touch test
                out.insert((i, link.slot(i).unwrap().clone()));  // WHOLE endset, no clip (arity ≥ 3 ⇒ unwrap safe)
            }
        }
    }
    let mut pairs: Vec<(usize, Endset)> = out.into_iter().collect();
    pairs.sort_by(|(i, e), (j, f)| i.cmp(j).then_with(||         // pinned total order: slot, then lexicographic
        e.spans().map(|sp| (sp.start(), sp.width()))             // span-sequence — deterministic at a snapshot
         .cmp(f.spans().map(|sp| (sp.start(), sp.width())))));
    Ok(pairs)
}
```

Slot attribution is read straight off M7's per-slot stab sets — `(i, eᵢ)` is surfaced iff `a ∈ stab(i, q, Active)` — so M7's overlap semantics (ProperOverlap | Containment | Equal, never Adjacent) is the *only* touch test here and M8 carries no span comparison of its own (a link-address endset never stabs a content-image query, so it is correctly not surfaced — RE-NCD's cross-subspace disjointness, discharged by M7). Key decisions, all forced by the note: **whole-endset surfacing** (emit `link.slot(i).clone()` — the full stored value from `readlink`, never clipped, RE-CLIP/RE-WHOLE), which preserves union-distributivity (RE-UDIST); **dedup by structural endset equality** (`Endset: Eq + Hash`) in an internal `std::collections::HashSet` — a throwaway local that never crosses a seam, so it needs none of `im`'s structural-sharing machinery — **converted to a sorted `Vec` at the output boundary** with a **pinned total order** (slot, then lexicographic span-sequence): value-identical endsets from distinct links collapse to one pair, identity is genuinely withheld (RE-UNIT), and the pair list is deterministic at a snapshot — hash-iteration order never leaks; **content-identity answer** (I-address endsets — permanent), with V-rendering left to a lossy layer above. The per-slot stabs cover slots `{1,2,3}`, which are *all* slots of every v1 link (the arity-3 invariant of §1), so every touching slot of every addressable link is surfaced (RE-CMP); an arity-≥4 extension moves with the same M7 seam extension the invariant is pinned to (*Open build decisions*).

### 5. Projection & discoverability (`project`, `discoverable_from`)

`project(a, slot, d)` = the V-positions in `d` where link `a`'s slot lands (ASN-0098 `project`):

```rust
fn project_on(snap, a, slot, d) -> Result<SpanSet, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    let cov = w.links().followlink(a, slot).map_err(|_| QueryError::NotALink)?;  // Err(Invalid) ⇒ NotALink (a∉dom(L) OR slot OOB)
    Ok(w.m5().project(d, &cov))                                                  // I→V, content subspace, level-class-safe
}
```

M5's `project` consumes the coverage `SpanSet` directly and applies the level-class discipline internally, so this is fault-free for any coverage including cross-length prefix/subtree spans.

**Error disambiguation.** `followlink`'s `Err(Invalid)` means "link or slot absent", so `NotALink` here subsumes both `a ∉ dom(L)` *and* an out-of-range `slot` (M8 does not separate them; a `BadSlot` split would cost an extra `readlink` to read arity and is deferred). The public `project` doc-comment states this.

**Scope (content subspace only).** `project` is M5's content-subspace tool (no subspace argument): `project(a, slot, d) ≠ ∅` witnesses discoverability **through content only** — strictly weaker than `discoverable_from`, which also folds in `link_runs` (LP12's `coverage ∩ ran(M(d))` spans both subspaces). A link reachable *solely* through `d`'s **link** subspace has empty `project` yet `discoverable_from = true`; LP12's biconditional, as M8 realizes `project`, holds only within the content subspace. The link-subspace *positional* projection that would close this gap — *which link-subspace V-positions of `d`* a slot lands in — is **not** M7's BH3: BH3 (`sources_to`/`target_of`) is typed reverse *lookup* (target→sources), a different question that yields no V-positions. The positional link-subspace projection is the scoped-out contextual EL11a (§7, composed with an M5/M6 listing check), never M8's `project`. The content-subspace-only restriction is stated in the public method doc-comment, not only here.

**Opacity (the returned `SpanSet`).** M1 exposes no `is_empty`/iterator over a `SpanSet`. A caller testing emptiness uses `equiv(&proj, &SpanSet::empty())?` (the `LevelMismatch` arm is unreachable — the projection's V-positions are all depth-2 `[s_C, ordinal]`, uniform-length, and `empty()` has nothing to mismatch). A caller needing the concrete V-positions enumerates `k ∈ 1..=content_count(d)`, forms `v_k = [s_C, k]`, and keeps those with `proj.denotes(&v_k)` (cross-checkable via `point(d, VPos{s_C, k})`). M8 returns the `SpanSet` verbatim and leaves that choice to the caller; it does **not** itself test the projection for emptiness via M1.

`discoverable_from(a, d)` tests LP12's characterisation directly per link — `∃ i : coverage(Σ.L(a).eᵢ) ∩ ran(M(d)) ≠ ∅` — conjoined with `is_active(a)`, avoiding both the opaque-`SpanSet` probe and a whole-document stab (the F-FULL membership route — stab the full range, test membership of one address — would materialize every doc-reaching link to answer a single-link question; this form is O(arity × |runs|) with identical semantics):

```rust
fn discoverable_from_on(snap, a, d) -> Result<bool, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    let link = w.links().readlink(a).ok_or(QueryError::NotALink)?;   // align non-link handling with `project`
    if !w.links().is_active(a) { return Ok(false); }                 // the ACTIVE half of the compound (Conflicts #8)
    let full: Vec<Run> = w.m5().content_runs(d).into_iter()
                          .chain(w.m5().link_runs(d)).collect();     // ran(M(d)), BOTH subspaces (LP12)
    if full.is_empty() { return Ok(false); }                         // registered-empty d ⇒ nothing reachable (cheap early-out)
    Ok((1..=link.arity()).any(|i| touches(link.slot(i).unwrap(), &full)))  // per-link LP12: O(arity × |runs|)
}
fn touches(e: &Endset, runs: &[Run]) -> bool {   // coverage(e) ∩ ⋃ runs ≠ ∅ — pointwise; mirrors M7's stab
    e.spans().any(|s| runs.iter().any(|r| matches!(  // overlap relations (ProperOverlap|Containment|Equal, never Adjacent)
        classify_spans(s, &r.iextent()),
        SpanRel::ProperOverlap | SpanRel::Containment | SpanRel::Equal)))
}
```

Including `link_runs` makes this faithful to LP12's `coverage ∩ ran(M(d))` across both subspaces; `classify_spans` is a pure, level-gate-free order relation, total on cross-length spans (a link-address span against a content run classifies by plain tumbler order — no fault), so the cross-subspace cases just work. The test iterates the link's full arity (not a hard-coded `{1,2,3}`), so it carries no arity-3 caveat; `touches` over an empty run list is vacuously false, so the `full.is_empty()` short-circuit is a cheap early-out, not a correctness guard. **`discoverable_from` is the compound "arrangement-reachable AND active", not pure LP12:** the explicit `is_active(a)` conjunct means a nullified-but-still-reachable link returns `Ok(false)`, whereas LP12 (which predates retraction) would call it discoverable — a caller wanting raw LP12 composes `followlink` + M5 `project` itself (and the public doc-comment leads with this NOT-LP12 warning). **Non-link handling is aligned:** both `project` and `discoverable_from` answer `Err(NotALink)` when `a ∉ dom(L)` — `project` via `followlink`'s `Invalid`, `discoverable_from` via its `readlink` gate. A *nullified* link is still a link: it passes the gate (`readlink` reads `dom(L)` verbatim) and returns `Ok(false)` through the `is_active` conjunct — distinguishing "not a link" from "a retracted link."

### 6. Pre-edit link-survival check (`delete_orphans`)

The practical "this delete will break N links *here*." It is a pure what-if over the snapshot — **it never calls M5's delete** — built on the set identity that falls out of F-UDIST:

> `orphaned = findlinks(A_del) \ findlinks(retained_range)` (active view — so a nullified link that lost its last witness in `d` is **not** reported, diverging from ASN-0117's `D(d,Σ)` over `dom(L)`; see invariants),

where `A_del` is the I-coverage of the deleted V-range and `retained_range = ran(M'(d))` is what survives (ASN-0117's last-witness condition, with no per-pair reasoning and no need to compute `A_del^{excl}` explicitly). It **mirrors DELETE's preconditions** so the preview is of the *requested* delete, never a coerced/clipped one:

```rust
fn delete_orphans_on(snap, d, p, width) -> Result<OrphanReport, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    if p.subspace != Nat::one()          { return Err(QueryError::NotContentSubspace); }  // s_C only (mirror M5 DeleteError)
    let np = p.ordinal.clone();  let nc = w.m5().content_count(d);
    if width.is_zero()                                  { return Err(QueryError::EmptyWidth); }   // mirror M5 EmptyWidth
    if np < Nat::one() || &np + width > &nc + Nat::one() { return Err(QueryError::OutOfBounds); }  // folds M5's NotArranged + OutOfBounds
                                                                                                   // (jointly equivalent under width ≥ 1)

    let del_span = vspan(&Nat::one(), &np, width);                    // [s_C, np] width [0, width]
    let a_del    = w.m5().resolve(d, &del_span);                      // no clipping now (bounds checked)
    let pre = if np > Nat::one() { Some(vspan(&Nat::one(), &Nat::one(), &(&np - Nat::one()))) } else { None };
    let suf_start = &np + width;
    let suf = if suf_start <= nc { Some(vspan(&Nat::one(), &suf_start, &(&nc - &suf_start + Nat::one()))) } else { None };
    let mut retained = w.m5().link_runs(d);                           // a text delete never touches links
    for s in [pre, suf].into_iter().flatten() { retained.extend(w.m5().resolve(d, &s)); }
    let cand = stab_union(w, &Endset::from_spans(a_del.iter().map(Run::iextent)));    // the a_del QUERY endset is non-empty under the
                                                                                      // bounds check; cand (the stab RESULT) may be ∅
    let surv = if retained.is_empty() { im::OrdSet::new() }                           // mirror findlinks_v: keep ∅-query off M7's stab
               else { stab_union(w, &Endset::from_spans(retained.iter().map(Run::iextent))) };
    // relative_complement = cand \ surv (im's `difference` is SYMMETRIC difference — NOT what we want)
    Ok(OrphanReport { orphaned: addrs(&cand.relative_complement(surv)) })
}

fn vspan(subspace: &Nat, ordinal: &Nat, width: &Nat) -> Span {           // a single V-span value, no algebra
    let start = Tumbler::new([subspace.clone(), ordinal.clone()]).unwrap(); // [subspace, ordinal]; non-empty ⇒ infallible
    let disp  = Tumbler::new([Nat::zero(), width.clone()]).unwrap();        // [0, width]: ordinal-level displacement
    Span::new(start, disp).unwrap()  // T12 holds for width ≥ 1: actionPoint([0,w]) = 2 ≤ #start = 2 (callers guard width ≥ 1)
}
```

Per-document orphaning is the deliverable. Rejecting a non-`s_C` `p` (`NotContentSubspace`), a zero `width` (`EmptyWidth`), and an out-of-range `(p, width)` (`OutOfBounds`) up front — mirroring M5's `DeleteError` so the preview's rejection is *actionable*, the caller fixing the delete before issuing it — means the report is of exactly the delete the caller named (`resolve`'s silent clipping never coerces it into a different one) and pins every `vspan` width to `≥ 1`, so its `Span::new` lift never faults. One deliberate fold in that mirror: M8's single bounds check returns `OutOfBounds` for **both** of M5's cases — `NotArranged` (`ord(p) > n_C`, the start beyond the arranged run) and `OutOfBounds` (range overrun) — which the check `np < 1 ∨ np + width > n_C + 1` is jointly equivalent to under the width ≥ 1 guard; nothing is accepted or rejected differently, but the preview's variant label does not match M5's byte-for-byte on the `np > n_C` case. When `retained` is empty (delete-everything from a link-free document), `surv` short-circuits to `∅` rather than handing M7's `stab` an empty query — mirroring `findlinks_v` so the empty-query reliance stays off the `stab` surface uniformly; on the `cand` side no such guard is needed because the **`a_del` query endset** fed to `stab_union` is always non-empty under the bounds check (every deleted position is arranged, so `resolve` returns at least one run) — `cand` itself, the stab *result*, is legitimately empty whenever no link touches the deleted range, so do not assert its non-emptiness (a `debug_assert!(!cand.is_empty())` would fire in normal operation). The final set is the **relative complement** `cand \ surv` — `im::OrdSet::relative_complement(self, other)` returns `self \ other`; the similarly-named `difference` is `im`'s alias for *symmetric* difference and would wrongly fold in `surv \ cand` (every link reaching the retained range, i.e. links that plainly survive), so the call site uses `relative_complement` and nothing else. The **global ghost** determination (LP17: discoverable from *no* document) requires checking each orphan against every other document's range — that reaches into provenance R (M5's `docs_containing`) and is M6 territory; M8 stops at the per-document set and a caller composes the escalation. Read-only throughout.

### 7. Archival supersession/edit lineage (`in_claims`, `out_claims`)

The raw claim enumeration over the edit lineage (ASN-0125 EL11b — the **archival, arrangement-independent** half, which is M8's decomposed scope), composing M7's reverse index — distinct from M7's `succs`/`chain`/`tip`/`current` walks, which stay M7's.

```rust
fn in_claims_on (snap, y, v) -> Vec<SupClaim> { claims_on(snap, FROM, y, v) }   // old(e) = y  (FROM = old, flipped)
fn out_claims_on(snap, x, v) -> Vec<SupClaim> { claims_on(snap, TO,   x, v) }   // new(e) = x  (TO   = new)
fn claims_on(snap, slot, key, v) -> Vec<SupClaim> {
    let l   = snap.world().links();
    if l.readlink(key).is_none() { return vec![]; }   // RESIDENCE GATE: a non-link key's enc([key]) prefix-
                                                       // coverage would over-match prefix-comparable claims (EL4 + R0a)
    let sup  = l.reserved_type(ShippedType::Supersedes);
    let v_ts = match v { View::Audit => View::Audit, View::Active => View::Active, View::Default => View::Default };  // rebind: View is not Copy; a Default passes through (M7 §G coerces it to Active)
    let hits = l.match_links(&[(slot, enc(slice::from_ref(key)))], v)            // claims naming `key` at `slot`
                .intersection(l.type_slice(sup, v_ts));                         // restrict to supersession claims (S^Σ — see Ŝ=S note)
    hits.iter().map(|c| {
        let ca   = validate(c.clone()).unwrap();
        let link = l.readlink(&ca).unwrap();
        SupClaim {
            old:  validate(link.from_slot().addrs().next().unwrap().clone()).unwrap(),   // FROM = old/superseded
            new:  validate(link.to_slot().addrs().next().unwrap().clone()).unwrap(),     // TO   = new/superseding
            home: document_of(&ca).unwrap(),                                              // EL8b attribution (pure M1)
            active: l.is_active(&ca), claim: ca,
        }
    }).collect()
}
```

This design follows **M7's flipped storage convention — `FROM = old/superseded`, `TO = new/superseding`** (the M7→M8 seam), diverging from ASN-0125's textual Df-DIR; so `in(y)` (old = y) probes FROM, `out(x)` (new = x) probes TO. `v = Active` gives the operative graph (`succ_o`), `v = Audit` the full history (`succ_h`); a passed `View::Default` behaves as `Active` (M7's §G primitives coerce it). Attribution is the pure M1 `document_of` projection — no store lookup (EL8b). Both probes need `v` twice (`match_links` then `type_slice`); since M7 does **not** derive `Copy` on `View`, `claims_on` rebinds it locally (a fieldless-enum match) for the second use — no `View: Copy` dependency.

**Schema-conformance reliance (Ŝ^Σ = S^Σ).** ASN-0125 EL11(b) defines `in/out` over the *schema-conforming* claims Ŝ^Σ (EL4 introduces Ŝ precisely because S^Σ may hold non-conformers); `claims_on` ranges over `type_slice(Supersedes) = S^Σ` with **no** per-claim conformance filter. The two coincide because the *assembled* system is edit-disciplined (ASN-0125 EL-DM): every supersession claim is born through M7's `assert_sup`/`editlink`, which schema-conform their emission (canonical unit-depth, irreflexive); `makelink` cannot mint a Supersedes-typed link (its `ty` resolves into the content subspace); and no component raw-`emit`s the Supersedes class — the last an **assembled-system convention, not an enforced invariant**: M7's `emit` gates only the retraction class (`RetractionClass`), and `Supersedes` is a registered Binary type, so an `emit(home, reserved(Supersedes), from, to)` with non-resident or self-referential endpoints is upstream-representable. Even under such a violation, `claims_on`'s read-out is **panic-free**: every emit-shaped `[K_sup]` tuple still carries unit-depth single-address F and G (`|F| = 1` forced, Binary `to`-cardinality shape-checked), so `addrs().next().unwrap()` cannot fault — the discipline reliance is *semantic* (the reported lineage is genuine, irreflexive supersession over resident endpoints), never safety-bearing; no unwrap in `claims_on` depends on EL-DM discipline, all depend only on M7's shape gates. Under that convention, at every reachable state Ŝ^Σ = S^Σ, and M8's unfiltered slice is faithful — *and* the endpoint read-out (`from_slot().addrs().next()`, `to_slot().addrs().next()`) is well-defined, each endset being a single unit-depth span. M8 leans on this discipline rather than re-checking it; the residence gate below is the one defensive backstop it keeps — against a *non-link key argument* (which discipline does not constrain), not against a malformed stored claim.

**Resident-key gate (enforced, not merely documented).** Exactness of `match_links(slot, enc([key])) ∩ type_slice(Supersedes)` ⟺ "a claim names `key` at that slot" rests on the `dom(L)` prefix-antichain (EL4 + R0a): for a non-link `key`, `enc([key])`'s prefix coverage `{t : key ≼ t}` could overlap a prefix-comparable claim and **over-match**, returning a silently wrong lineage. Because these reads return `Vec` (not `Result`), M8 **gates internally** rather than leaving a trap behind a comment: `claims_on` short-circuits to `[]` when `readlink(key).is_none()`, so a non-link `y`/`x` yields the (correct) empty lineage. Callers should still pass resident link addresses; the gate is a defensive backstop, not a license to pass arbitrary tumblers.

**Contextual discovery (EL11a — a claim visible in `d` iff `d` lists the endpoint) is out of M8's decomposed scope** (M8 owns the *archival* `in/out` = EL11b). A reader needing it composes M8's archival output with an M5/M6 listing check; M8 does not ship it, precisely because the in-place V-listing test would require an emptiness probe on M5's opaque projection that M1 does not provide (§5).

## Invariants & contracts

**By construction** (fall out of the data model / faithful composition):

- **Writes nothing; frame `Σ`.** M8 calls only pure reads + `snapshot()`. (all sources; ASN-0121 read-only frame, CN-DEF, RE-DEF)
- **Result determinism at a snapshot; result-as-set, dedup-by-address.** `OrdSet<Tumbler>` is keyed by address, so "transclusion found once" (FL-REACH(b)) and no value-dedup hold for free; window boundaries are objective (W11). (ASN-0127, ASN-0121 FL-REACH, ASN-0108 W3/W11)
- **Existence-anchored monotonicity (FTT family, absent retraction).** `dom(L)` only grows and coverage is permanent, so a found link stays found *unless retracted* — FL-MON/CN-MONO carry exactly that absent-retraction hypothesis; the active slice itself shrinks under nullification. (ASN-0121 FL-MON, ASN-0132 CN-MONO, ASN-0127 E-MONO)
- **Result-drop = present unreachability *or* retraction, not deletion of the stored object.** Under the uniform `View::Active`, a link leaves a result either because it is no longer arrangement-reachable (the present-tense reading) *or* because it was nullified; neither means the stored link, its coverage, or its address ceased to exist — those are permanent upstream. (ASN-0127 D-ZERO + ASN-0121 FL-RET / ASN-0132 CN-RETRACT; ASN-0098 LP13)
- **Cursor survives orphaning; no duplicate / no skip; append-at-tail.** From the permanent address key + key-cut resume. (ASN-0108 W4/W5/W6/W8)
- **Union-distributivity** of region/findlinks composition; whole-endset RETRIEVEENDSETS preserves it. (ASN-0127 F-UDIST/F-VDIST, ASN-0131 RE-UDIST/RE-CLIP)

**By active enforcement** (M8 must guard):

- **Document-existence + region gate.** `is_registered_document(d)` then `check_region(region)` *before* any M5 read on every V-anchored op — M5 conflates registered-empty (`∅`, defined) with unregistered (error) and silently clips a malformed span. Guarded at the top of `image_on` (inherited by `findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`) and at `project`/`discoverable_from`/`delete_orphans`. `delete_orphans` additionally mirrors DELETE's preconditions — non-`s_C` `p` → `NotContentSubspace`, zero `width` → `EmptyWidth`, out-of-range `(p, width)` → `OutOfBounds`, the last deliberately folding M5's `NotArranged` and `OutOfBounds` into one variant (jointly equivalent to M5's pair under the width ≥ 1 guard — §6) — an *actionable* rejection a caller can fix before issuing the delete, not an opaque `BadRegion`; never previews a coerced delete, and thereby pins every survival-check `vspan` to width ≥ 1. (ASN-0127 F-IMG/F-V, ASN-0131, ASN-0117, decomposition seam)
- **Snapshot consistency.** Read L, M, and the registry off **one** `Snapshot` per op, and **thread that one `snap` through internal composition** (`image_on`, never `self.image`); the `_on` twins let M10 share a snapshot across count+window. Guarded by snapshotting once and reading only `snap.world()`. (ASN-0127 Recovery; M2 clause 6)
- **Relative complement, not symmetric difference, in the survival check.** `delete_orphans` computes `findlinks(A_del) \ findlinks(retained)` via `OrdSet::relative_complement`; `im`'s `difference` is symmetric difference and would invert the report. Guarded at the one call site. (ASN-0117)
- **Addressability filter (foundation ∩ active).** Pass `View::Active` (not `Audit`) for every present-state query, so nullified links never appear — making `findlinks_v`/`count_v`/`window_v`/`discoverable_from`/`delete_orphans` realize *foundation ∩ addressable*, a deliberate divergence from ASN-0127/0098/0108/0117's UNFILTERED `findlinks_V`/`discoverable_from`/`Match`/`D(d,Σ)` (Conflicts #8). In particular `discoverable_from` is the compound "arrangement-reachable AND active", not pure LP12: a nullified-but-reachable link returns `Ok(false)`; and `delete_orphans` reports orphans over the active view, so a nullified link that loses its last witness in `d` is **not** reported, where ASN-0117's `D(d,Σ) = {a ∈ dom(Σ.L) : …}` ranges over `dom(L)`. Guarded at each `stab`/`match_links`/`type_slice` call site (`View::Active`), and by the explicit `is_active(a)` conjunct in `discoverable_from`'s per-link test. (ASN-0121 FL-RET, ASN-0132 CN-RETRACT, ASN-0117)
- **Empty constrained slot → zero, never an empty M7 query.** `match_core` annihilates to `∅` on any `SlotSpec::Empty` *or* empty-coverage `SlotSpec::Spans` before building constraints, so M7's `match_links` never receives an empty `Endset` (which it forbids) — exactly FL-EMP respected by construction. (ASN-0121 FL-EMP; M7 `match_links` contract)
- **Resident-key gate on archival lineage.** `claims_on` returns `[]` when `readlink(key).is_none()`, so a non-link `y`/`x` cannot over-match prefix-comparable claims. Guarded at the top of `claims_on`. (ASN-0125 EL4; ASN-0086 R0a)
- **Home filter via address projection, never arrangement presence.** `home_ok` uses M1 `document_of`. (ASN-0132 CN-STAB)
- **Present-tense discovery (no stale serve).** M8 owns no cache and always recomputes — the enforcement *is* the no-cache design. (ASN-0127 D-NONMONO, ASN-0108 W7)
- **Total windowing API.** `window_over` clamps `n` to `≥ 1` (`n.max(1)`), so a misusing `n = 0` never produces `exhausted = false` with an empty batch and an unchanged cursor (a silent non-terminating signal). Guarded once in the shared combinator, covering both `window_v` and `window_ftt`. (ASN-0108 W9)
- **Withhold identity + dedup by structural endset value** in RETRIEVEENDSETS; **no clipping**; converted to a **sorted** `Vec` at the seam with a **pinned output order** (slot, then lexicographic span-sequence — restoring the ordering half of the determinism invariant that hash-iteration would otherwise break); the dedup uses a throwaway `std::collections::HashSet`, never an `im` container. Guarded in the attribution-and-dedup loop and the final sort. (ASN-0131 RE-UNIT/RE-CLIP)
- **No raw mixed-length span algebra.** Coverage-overlap matching → M7; I→V → M5; query endsets → `from_spans(run.iextent())`; the one pointwise exception is `discoverable_from`'s per-link `classify_spans` test — a level-gate-free order classification, never level-gated set algebra. Guarded by never calling M1 `intersect_sets`/`difference_sets` on upstream covers. (M5/M7 level-class warnings)

## Dependencies & seams

**Upstream consumed:**

- **M1** — `Tumbler` total order (the `OrdSet` order = enumeration key, cursor cut); `document_of` (home projection for `athome` and claim attribution); `validate` (`Tumbler → Address` at output, applied to a *clone* of each iterated `&Tumbler`, infallible by M3's mint); `classify_spans` for `discoverable_from`'s per-link touch test (§5 — M8's one pointwise span comparison; RETRIEVEENDSETS attribution reads M7's per-slot stabs instead); `Span::new`/`Tumbler::new` for the survival-check V-spans (the `vspan` helper, unwrap-safe under the width ≥ 1 guard); `Endset`/`Span` construction inputs. (`equiv`/`SpanSet::empty` are the *caller's* recipe for probing `project`'s opaque result — M8 itself never tests a `SpanSet` for emptiness.)
- **M2** — `kernel.snapshot()` for one consistent (L, M, registry) read; `snapshot.world()`/`seq()`; no writes.
- **M3** — `is_registered_document(d)` only (the doc-existence gate).
- **M5** — `resolve` (V→I runs, the image source), `project` (I→V content, level-class-safe), `content_runs`/`link_runs` (`ran M(d)` for discoverability/survival), `content_count` (delete bounds). (`point` appears only in the §5 *caller* recipe for enumerating a projection — M8 itself never calls it.) M8 never reads R.
- **M7** — `stab`/`match_links`/`type_slice` (the spanfilade — *the* matcher; M8 does not reimplement it), `readlink`/`followlink`, `is_active`, `reserved_type(Supersedes)`, `enc`/`Endset::from_spans`, `View::Active`/`Audit`; archival composes `match_links ∩ type_slice` + `readlink`. M8 lifts a §G `Tumbler` to `Address` via `validate` before any `readlink`. **Build-time note: M8 uses `View` more than once within an op (`stab_slots`' 3-slot loop, `claims_on`'s two probes). M7 does *not* derive `Copy` on `View`, so M8 does not lean on it — `stab_slots` constructs a fresh `View::Active` literal per slot (the view is always active there), and `claims_on` rebinds `v` locally (a fieldless-enum match) for its second use. No upstream derive or API is required; an M7 `Copy` on `View` would only let those two spots shed the rebinds.**

**Downstream / seam contracts M10 builds against:**

- **Region family** (`image`/`findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`): take `(d, region: &[Span])`; **return `Err(DocNotRegistered)` for an unregistered `d`**, **`Err(BadRegion)` for a region that is not content-subspace ordinal-level depth-2 V-spans**, and a defined empty result for a registered-empty `d`. Present-tense, non-monotone, and **addressable-filtered** — every result is *foundation ∩ active*, so nullified links never surface. `image` is **deduped at M8's boundary** (`Run: Eq`) — no exact-equal Run repeat; overlapping *input* spans may still yield partially-overlapping runs (not an address-disjoint partition — don't sum widths for |image|). `retrieve_endsets` returns a `Vec<(usize, Endset)>` (deduped internally in a throwaway `std::collections::HashSet`; no `im` container crosses the seam; output order pinned — slot, then lexicographic span-sequence — so it is deterministic at a snapshot). M10 phrases the V-region (content subspace, depth-2).
- **Descriptor family** (`findlinks_ftt`/`count_ftt`/`window_ftt`): take an address-phrased `FourSet`; total (no doc gate); monotone absent retraction — a found link stays found unless nullified, `dom(L)` only grows; `count_ftt` is ASN-0132's operation. A `SlotSpec::Spans` **must carry a non-empty `Endset`** — an empty one is normalized onto the zero (`Empty`/annihilate) path (FL-EMP), so M7 never sees an empty `match_links` `Endset`. M10 resolves any reader content-pointings to addresses upstream.
- **Projection** (`project`): content-subspace only; `NotALink` covers both a non-link `a` and an out-of-range `slot`. **Discoverability** (`discoverable_from`): compound "reachable AND active", **not** raw LP12 (its doc-comment leads with the NOT-LP12 warning); a nullified-but-reachable link answers `Ok(false)`.
- **Pre-edit survival** (`delete_orphans`): read-only what-if; orphans over the active view (a nullified link that lost its last witness in `d` is not reported — divergence from ASN-0117's `D(d,Σ)` over `dom(L)`); rejects with M5-mirroring granularity — `NotContentSubspace` (non-`s_C` `p`), `EmptyWidth` (zero `width`), `OutOfBounds` (out-of-range `(p, width)`; deliberately folds M5's `NotArranged` and `OutOfBounds`, jointly equivalent under width ≥ 1 — §6) — so the rejection is *actionable*, never an opaque `BadRegion`.
- **Archival lineage** (`in_claims`/`out_claims`): intended for resident link addresses (`dom(L)`); a non-link key is **gated internally** (returns `[]`) rather than over-matching prefix-comparable claims; `v = Active` yields the operative graph, `Audit` the full history, and `Default` behaves as `Active` (coerced by M7's §G primitives). Faithful because the assembled system keeps the Supersedes slice schema-conforming (Ŝ^Σ = S^Σ — §7; a convention whose violation would degrade result purity only, never panic-safety — the read-out leans solely on M7's shape gates).
- **Windowing**: cursor is a bare `Address`; `Window.exhausted` is the terminal signal; `next` resumes; stateless across calls (`n ≥ 1`; `n = 0` is clamped to `1`, never a false non-terminal). M10 carries the cursor; a partial/empty batch ends the pass.
- **Pure twins** (`*_on(&Snapshot<W>, …)`): M10 uses these to read a count and its window — or any pair — off one snapshot, satisfying the snapshot-token consistency need.
- M8 returns `Vec<Address>` / `usize` / `Window` / `Vec<(usize, Endset)>` / `SupClaim` / `OrphanReport`; M10 marshals to the wire and surfaces precondition failures (`DocNotRegistered`/`NotALink`/`BadRegion`/`NotContentSubspace`/`EmptyWidth`/`OutOfBounds`) as typed rejections (never a silent skip). These are reads — no commit — but still snapshot-isolated.

Crate graph: `skep-linkquery → skep-address, skep-kernel, skep-namespace, skep-arrangement, skep-links` (pure surfaces); `skep-operation (M10) → skep-linkquery`. M8 names no `World`/`Record`; contributes no slice to `skep-engine`. Acyclic, mirroring `M8 → M1, M2, M3, M5, M7`.

## Conflicts resolved

1. **The AND-of-ORs combiner — M7's `Observe`/`match_links` vs. M8's `findlinks` (the decomposition's softest seam).** Resolved in M7's favor, per the recommended factoring: M7 owns the per-slot matcher *and* the combiner (`stab`/`match_links`), and M8 is **pure discovery presentation** — windowing, cursors, count, pagination, projection, RETRIEVEENDSETS, archival, survival — over M7's matcher. M8 implements no query-side slot matching and no AND-of-ORs: even `retrieve_endsets`' slot attribution is read off M7's per-slot `stab` sets (§4), not a local touch test. The one pointwise overlap test M8 retains is `discoverable_from`'s per-link LP12 check (§5) — a single-link point query mirroring M7's overlap relations, not a matcher over the store.

2. **Disjunctive `findlinks` (ASN-0127, any slot) vs. conjunctive `findlinks_FTT` (ASN-0121, four-set).** ASN-0121 is explicit they are not restrictions of each other. M8 exposes **both as distinct entry points** — the region family (disjunctive, V-anchored, present-tense, doc-gated) and the descriptor family (conjunctive, address-keyed, monotone absent retraction, link-store-local). They share M7's per-slot `stab` but combine it oppositely (union vs. AND); neither is built on the other.

3. **The enumeration key (ASN-0108).** The note warns that no permanent key is the spanfilade's *native* (matched-slot) order, and the matched-slot order is unsafe under partial orphaning. In **this** design M7's discovery primitives return `im::OrdSet<Tumbler>` — **address order, the permanent key** — not matched-slot order. So the permanent key *is* the order M8 sees; windowing is a safe range scan with no derived index. The least-covered-tumbler alternative would force M8 to build an index it is forbidden to own. Resolution: address key, full stop.

4. **Existence-anchored (monotone absent retraction) vs. discovery-anchored (non-monotone).** Kept as distinct families with distinct documented stability: `count_ftt` is the existence census — monotone absent retraction (CN-MONO); `window_v` is the non-monotone present-tense view (the ASN-0108 `Match = findlinks_V` reading). Because M8 owns no cache, present-tense correctness is free.

5. **Supersession slot directionality.** ASN-0125 Df-DIR reads `F = new`; M7's actual storage (per the seam) is **flipped: `F = old/superseded`, `G = new/superseding`.** M8 follows M7's storage — `in(y)` probes FROM, `out(x)` probes TO. Noted divergence from the source text. (Contextual EL11a, which would also turn on this convention, is out of M8's scope — see §7.)

6. **RETRIEVEENDSETS whole-endset vs. touching-spans (ASN-0131 OQ1).** Resolved to **whole-endset** (return `readlink`'s full value), preserving union-distributivity (RE-UDIST) at the cost of one `readlink` per candidate.

7. **Home/residence filter placement (ASN-0121).** M8 owns no index dimension, so home is a **post-filter** via M1 `document_of` (lazy during a window walk). A home-only query degrading to a full active scan is accepted.

8. **Addressability: unfiltered foundations vs. addressable operations.** ASN-0127/0098/0108/0117's `findlinks_V`/`discoverable_from`/`Match`/`D(d,Σ)` range over the *whole* `dom(Σ.L)` — ASN-0121 FL-DEF flags ASN-0127's `findlinks` as "slot-agnostic, unfiltered" and explicitly **not a restriction** of the addressable `findlinks_FTT`. But the operation notes M8 actually *realizes* — RE-DEF, FL-DEF, CN-DEF — all range over `addressable(Σ) = dom(L) \ nullified`. M8 therefore queries every present-state primitive with `View::Active` **uniformly**, so `findlinks_v`/`count_v`/`window_v`/`discoverable_from`/`delete_orphans` are the disjunctive/membership/orphan foundation **intersected with the active view** (not the bare foundation — the §1 label is corrected accordingly); in particular **`discoverable_from` is the compound "reachable AND active", not pure LP12** — a nullified-but-reachable link answers `Ok(false)`, and a caller wanting raw LP12 composes `followlink` + M5 `project` itself (and the public doc-comment leads with this NOT-LP12 warning); and **`delete_orphans` reports orphans over the active view** (diverging from ASN-0117's `D(d,Σ)` over `dom(L)` — a nullified link losing its last witness in `d` is not reported). `retrieve_endsets`/`findlinks_ftt`/`count_ftt` are already note-exact (their notes are addressable). The consequence for the "result-drop" reading — a missing link asserts present unreachability **or** retraction, never deletion of the stored object — is captured in the refined invariant.

## Open build decisions

- **The arity-≥4 disjunction (genuine seam gap, tied to the v1 invariant).** `findlinks_v` unions — and RETRIEVEENDSETS attributes over — slots `{FROM, TO, TYPE}`, which is the **exact** ASN-0127 coverage *because* the v1 arity-3 invariant holds — every v1 link-creation path (`makelink`/`emit`/`nullify`/`assert_sup`/`editlink`) deposits an arity-3 link (§1). The moment an arity-≥4 type with content-reaching extra slots ships, that invariant breaks and the per-slot coverage is no longer exhaustive; it then needs an M7 `stab_any` or an exposed max-arity (RETRIEVEENDSETS' slot attribution, read off the same per-slot stab sets, extends with it; `discoverable_from`, now a per-link full-arity test, is exempt). **Pick `{1,2,3}` for v1** and negotiate the M7 extension only if such a type ships — this is the one place M8's fidelity depends on an M7 capability not in the current interface.
- **Survival-check scope.** Per-document orphan set (the "breaks N links here" feature — cheap, recommended default) vs. also the **global-ghost** escalation (each orphan checked against every other document via M5's R-index — expensive, and it crosses into M6/provenance). Default per-document; expose global only if a caller needs LP17 ghost determination, and route it through M6.
- **Contextual claim discovery (EL11a).** Left out of M8 (scope = archival `in/out` = EL11b). If a reader wants "which claims does `d` list," compose M8's archival output with an M5/M6 listing check at a higher layer — do not push an M5-projection-emptiness probe into M8 (M1 gives no such test). This is also the accurate home for the link-subspace *positional* projection §5 declines (BH3 is the wrong tool — it is target→sources lookup, not V-position projection).
- **`project` error granularity.** `NotALink` currently subsumes both a non-link `a` and an out-of-range `slot` (M7's `followlink` conflates them). A `BadSlot` split is deferred — it would cost an extra `readlink` to read arity; add it only if a caller needs to distinguish the two failures.
- **`View: Copy` (optional upstream nicety, not relied on).** M8 builds against M7 *as given*: `View` is **not** `Copy`, so `stab_slots` uses a fresh `View::Active` literal per slot (it is always the active view) and `claims_on` rebinds `v` locally (a fieldless-enum match) for its second use — no upstream derive assumed. The one-line ask to M7 — derive `Copy` on `View` (a fieldless tag enum, as `Shape`/`Behavior` already are) — is *filed* with M7 as a cosmetic simplification that would let those two spots shed the rebinds; it is **never a dependency** and not a structural choice.
- **Secondary enumeration key.** Address-only (default; free from M7's order) vs. also offering content-order (least-covered-tumbler) pagination at O(|Match|·log) per-window re-sort. Add the re-sort only if a reader needs content-ordered windows; never build a persistent key index (M8 owns none).
- **Count caching.** M8 recomputes (owns no state). Whether M10 wraps `count_ftt` with an epoch-tagged cache (CN-STAB: changes only on `K.λ`) and whether to special-case the all-wildcard count to `len()` of M7's active slice are M10/M7 choices, not M8's.
- **Cursor token shape.** Bare `Address` (sufficient — the key *is* the address) vs. a fattened opaque token. Default bare; fatten only to skip a (zero-cost here) key recompute, never to carry a server-side materialized list.
- **Region presentation.** `&[Span]` per single document (the contract here) vs. a multi-document SpecSet. Multi-document fan-out is a higher-layer composition, not M8's.
