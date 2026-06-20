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
    Spans(Endset),  // populated address-spans (M7's readable Endset)
}

/// q = (H, F, G, Θ). `home` is matched against home(a) (an address projection), NOT a slot.
pub struct FourSet { pub home: SlotSpec, pub from: SlotSpec, pub to: SlotSpec, pub ty: SlotSpec }

pub type Cursor = Option<Address>;                 // None = ⊥ (start); Some(a) = resume strictly past a
pub struct Window  { pub batch: Vec<Address>, pub next: Cursor, pub exhausted: bool }
pub struct SupClaim { pub claim: Address, pub old: Address, pub new: Address,
                      pub home: Address, pub active: bool }
pub struct OrphanReport { pub orphaned: Vec<Address> }   // links the proposed DELETE drops from d

pub enum QueryError { DocNotRegistered, NotALink, BadRegion }

pub struct LinkQuery<'k, W: WorldState> { kernel: &'k Kernel<W> }
```

```rust
impl<'k, W> LinkQuery<'k, W>
where W: WorldState + HasLinks + HasM5 + HasM3
{
    pub fn new(kernel: &'k Kernel<W>) -> Self;

    // ── Content-region discovery (V-anchored, present-tense, doc-gated; disjunctive over slots) ──
    pub fn image(&self, d: &Address, region: &[Span]) -> Result<Vec<Run>, QueryError>;          // V→I
    pub fn findlinks_v(&self, d: &Address, region: &[Span]) -> Result<Vec<Address>, QueryError>;
    pub fn count_v(&self, d: &Address, region: &[Span]) -> Result<usize, QueryError>;           // present-tense census
    pub fn window_v(&self, d: &Address, region: &[Span], cur: Cursor, n: usize)
        -> Result<Window, QueryError>;                                                          // ASN-0108
    pub fn retrieve_endsets(&self, d: &Address, region: &[Span])
        -> Result<im::HashSet<(usize, Endset)>, QueryError>;                                    // ASN-0131

    // ── Four-set descriptor query (address-keyed, conjunctive, link-store-local, monotone) ──
    pub fn findlinks_ftt(&self, q: &FourSet) -> Vec<Address>;                                   // ASN-0121
    pub fn count_ftt(&self, q: &FourSet) -> usize;                                              // ASN-0132 (the count op)
    pub fn window_ftt(&self, q: &FourSet, cur: Cursor, n: usize) -> Window;

    // ── Pointwise projection & discoverability (content subspace) ──
    pub fn project(&self, a: &Address, slot: usize, d: &Address) -> Result<SpanSet, QueryError>;// ASN-0098 I→V
    pub fn discoverable_from(&self, a: &Address, d: &Address) -> Result<bool, QueryError>;

    // ── Pre-edit link-survival (read-only; never touches the edit path) ──
    pub fn delete_orphans(&self, d: &Address, p: &VPos, width: &Nat)
        -> Result<OrphanReport, QueryError>;                                                    // ASN-0117

    // ── Archival supersession/edit lineage ──
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
pub fn retrieve_endsets_on<W>(s: &Snapshot<W>, d: &Address, region: &[Span]) -> Result<im::HashSet<(usize, Endset)>, QueryError>;
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

- **Result sets are carried internally as `im::OrdSet<Tumbler>` — M7's native discovery return type — and converted to `Vec<Address>` only at the output boundary.** M7's primitives yield `&Tumbler` under iteration (`iter`/`range`); M8 **clones each key and `validate`s it at the lift** — infallible, since every key is a T4-valid minted address (M7's §G→§F note). This is the whole engine: `union`/`difference`/`range` on a persistent ordered set are cheap and structurally-shared, and **`OrdSet<Tumbler>` is ordered by tumbler = link address = exactly ASN-0108's permanent enumeration key.** So windowing is a `range(Excluded(cursor)..).take(n)` — no M8-side index, no re-sort. This is what lets M8 "own no index" yet page efficiently.

- **Authoritative state owned: none.** The link store, active/audit slices, spanfilade, type registry (M7); arrangements and R (M5); registry (M3). **Recomputable hints owned: none.** M8 recomputes every answer from upstream each call; the only index it leans on (M7's spanfilade) is M7's hint, recovered by M7. The unit of consistency is the M2 `Snapshot` threaded through one operation.

A second, quieter discipline shapes every algorithm: **M8 does essentially no span algebra itself.** Mixed-length covers (a content address and a link address differ in tumbler length) fault M1's `intersect_sets`/`difference_sets` with `LevelMismatch`. M8 sidesteps this entirely — coverage-overlap matching goes through M7's `stab`/`match_links` (M7 handles level classes), I→V projection goes through M5's `project` (handles them internally), and query `Endset`s are built from `Run::iextent()` via `Endset::from_spans` (verbatim, no algebra). M8 never differences or intersects raw covers; it set-operates only on `OrdSet<Tumbler>` (addresses, uniform — no level issue).

## Internal design

Every operation opens with one snapshot and reads `links() / m5() / m3()` off `snap.world()` — never separate snapshots (the (L, M) coherence ASN-0127 forces). All pseudo-code below is the threaded `foo_on(snap, …)` form: it binds `let w = snap.world();` once and composes internal steps as `image_on(snap, …)` etc. — **never `self.image`, which would open a second snapshot.** "Recovery" is trivial and uniform: M8 persists nothing; each answer is recomputed from upstream state, which M2 recovers by replay. I omit it per capability below.

Two free helpers and a region gate are shared throughout:

```rust
/// Lift M7's native discovery keys to validated addresses, at the OUTPUT boundary only.
fn addrs(keys: &im::OrdSet<Tumbler>) -> Vec<Address> {
    keys.iter().map(|t| validate(t.clone()).unwrap()).collect()   // clone &Tumbler; validate infallible (M3 mint)
}
/// The disjunctive ASN-0127 findlinks(I) core ∩ the chosen view: OR across slots {FROM,TO,TYPE}.
/// Exact over ALL slots by the v1 arity-3 invariant (below). View::Active discharges addressability.
fn stab_union<W>(w: &W, q: &Endset, v: View) -> im::OrdSet<Tumbler> {
    let mut out = im::OrdSet::new();
    for i in [FROM, TO, TYPE] { out = out.union(w.links().stab(i, q, v)); }
    out
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
    let mut runs = vec![];
    for span in region { runs.extend(w.m5().resolve(d, span)); }   // clips silently to arranged positions
    Ok(runs)   // MAY repeat a Run under overlapping input spans — harmless: set-idempotent in from_spans/stab below
}
```

A registered-but-empty `d` then yields a legitimate `∅` (defined); an unregistered `d` surfaces as `DocNotRegistered`, not a masquerading "no links here"; a non-content / non-depth-2 region surfaces as `BadRegion`, not a silently-clipped different query (ASN-0127 F-IMG/F-V; ASN-0131; the decomposition seam).

**`image`** resolves the V-region to I-runs through the live arrangement. I use `resolve` (runs), **not** `resolve_coverage` (an opaque `SpanSet`) — runs carry `i_start + width`, expose `iextent() -> Span`, and dodge both the `SpanSet`-iteration gap and the level-class trap. `resolve` is defensive (silently clips out-of-range, returns `⟨⟩` for a malformed span), so the image is exactly the currently-arranged subset of the region (ASN-0127's load-bearing `W ∩ dom M(d)` intersection — unarranged positions contribute nothing). The returned `Vec<Run>` may repeat a run when input spans overlap; downstream this is harmless (the runs feed a set-valued `from_spans`/`stab` pipeline), and a caller wanting a deduped image dedups at the boundary.

**`findlinks_v`** is the disjunctive ASN-0127 `findlinks(image(W,d))`, **intersected with the active view** (`View::Active` — the addressability the operation owes its readers; reconciled in *Conflicts resolved*):

```rust
fn findlinks_v_set_on(snap, d, region) -> Result<im::OrdSet<Tumbler>, QueryError> {
    let w = snap.world();
    let img = image_on(snap, d, region)?;                      // gate + region-check + resolve, on THIS snap
    if img.is_empty() { return Ok(im::OrdSet::new()); }        // F-V empty short-circuit, no index touch
    let q = Endset::from_spans(img.iter().map(Run::iextent));  // coverage(q) = the image
    Ok(stab_union(w, &q, View::Active))                        // View::Active == addressable == dom(L) \ nullified
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
    let lo = match &cur { None => Unbounded, Some(c) => Excluded(c.tumbler().clone()) };
    let batch: Vec<Address> = matched.range((lo, Unbounded))   // ascending = address order = the key
        .filter(|t| keep(t))
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

`window_v`'s set is `findlinks_v` (disjunctive V-region — the ASN-0108 `Match = findlinks_V` reading). `window_ftt`'s set is `match_core`'s (below), with the home filter applied **lazily during the range walk** (`keep = home_ok`) — so a home-narrow query never materializes the full filtered set. Caller obligation: `n ≥ 1`.

### 3. Four-set descriptor query (`findlinks_ftt`, `count_ftt`, `window_ftt`)

This is the **address-keyed, conjunctive, link-store-local** family (ASN-0121/0132) — *not* the V-region disjunctive one (ASN-0121 is explicit: neither is a restriction of the other). No document gate (it reads only `Σ.L`, FL-LOC). The request arrives already phrased over addresses (V→I resolution is upstream).

```rust
fn match_core<W>(w: &W, q: &FourSet) -> im::OrdSet<Tumbler> {
    for s in [&q.home, &q.from, &q.to, &q.ty] {               // FL-EMP: any constrained-empty slot annihilates
        if let SlotSpec::Empty = s { return im::OrdSet::new(); }
    }
    let mut cons = vec![];                                    // FL-WILD: Any drops out
    if let SlotSpec::Spans(e) = &q.from { cons.push((FROM, e.clone())); }
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
    match_core(snap.world(), q).iter().filter(|t| home_ok(q, t))
        .map(|t| validate(t.clone()).unwrap()).collect()
}
fn count_ftt_on(snap, q) -> usize { match_core(snap.world(), q).iter().filter(|t| home_ok(q, t)).count() }
```

The all-wildcard `(∗,∗,∗,∗)` is `match_links(&[], Active)` = the whole addressable slice (FL-WILD). **The home filter is an address projection (`document_of`), never an arrangement-presence test** — a reverse-orphaned link (its own home entry deleted) still satisfies a home-bounded query (CN-STAB; the cautionary CN home note). A home-only query degrades to a full active scan (no slot narrows it) — accepted, since M8 owns no index dimension. This family is **monotone** (FL-MON/CN-MONO): the active slice only grows, coverage is permanent, so a found-and-not-retracted link stays found.

### 4. RETRIEVEENDSETS (`retrieve_endsets`)

Same selection index as `findlinks_v`, a different read-out: report `(slot, endset)` pairs touching the region, **withholding link identity** (ASN-0131 RE-UNIT).

```rust
fn retrieve_endsets_on(snap, d, region) -> Result<im::HashSet<(usize, Endset)>, QueryError> {
    let w = snap.world();
    let img = image_on(snap, d, region)?;                          // gate + region-check inside, on THIS snap
    if img.is_empty() { return Ok(im::HashSet::new()); }
    let q = Endset::from_spans(img.iter().map(Run::iextent));
    let candidates = stab_union(w, &q, View::Active);             // sel = findlinks_v ∩ active
    let mut out = im::HashSet::new();
    for c in candidates.iter() {
        let link = w.links().readlink(&validate(c.clone()).unwrap()).unwrap();  // resident (from active slice)
        for i in 1..=link.arity() {                              // ALL slots of a found candidate (arity-3 in v1)
            let e = link.slot(i).unwrap();
            if touches(e, &img) { out.insert((i, e.clone())); }  // WHOLE endset, no clip; dedup by structural Eq
        }
    }
    Ok(out)
}
fn touches(e: &Endset, img: &[Run]) -> bool {                    // coverage(e) ∩ image ≠ ∅, per slot
    e.spans().any(|s| img.iter().any(|r| matches!(
        classify_spans(s, &r.iextent()),
        SpanRel::ProperOverlap | SpanRel::Containment | SpanRel::Equal)))
}
```

`touches` reuses M1 `classify_spans` (pure order, no level gate — total on cross-length spans; a link-address endset reports `Separated` against a content image, so it is correctly not surfaced). Key decisions, all forced by the note: **whole-endset surfacing** (emit `e.clone()` — the full stored value from `readlink`, never clipped, RE-CLIP), which preserves union-distributivity (RE-UDIST); **dedup by structural endset equality** (`Endset: Eq + Hash`), so value-identical endsets from distinct links collapse to one pair and identity is genuinely withheld (RE-UNIT); **content-identity answer** (I-address endsets — permanent), with V-rendering left to a lossy layer above. The candidate union is `{1,2,3}` (the v1 arity-3 invariant of §1); emission iterates a candidate's full arity, so any touching slots on a *found* candidate are surfaced.

### 5. Projection & discoverability (`project`, `discoverable_from`)

`project(a, slot, d)` = the V-positions in `d` where link `a`'s slot lands (ASN-0098 `project`):

```rust
fn project_on(snap, a, slot, d) -> Result<SpanSet, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    let cov = w.links().followlink(a, slot).map_err(|_| QueryError::NotALink)?;  // slot-`slot` coverage; Err ⇒ NotALink
    Ok(w.m5().project(d, &cov))                                                  // I→V, content subspace, level-class-safe
}
```

M5's `project` consumes the coverage `SpanSet` directly and applies the level-class discipline internally, so this is fault-free for any coverage including cross-length prefix/subtree spans.

**Scope (content subspace only).** `project` is M5's content-subspace tool (no subspace argument): `project(a, slot, d) ≠ ∅` witnesses discoverability **through content only** — strictly weaker than `discoverable_from`, which also folds in `link_runs` (LP12's `coverage ∩ ran(M(d))` spans both subspaces). A link reachable *solely* through `d`'s **link** subspace has empty `project` yet `discoverable_from = true`; LP12's biconditional, as M8 realizes `project`, holds only within the content subspace. Link-to-link reverse discovery is M7's BH3, never M8's `project`.

**Opacity (the returned `SpanSet`).** M1 exposes no `is_empty`/iterator over a `SpanSet`. A caller testing emptiness uses `equiv(&proj, &SpanSet::empty())?` (the `LevelMismatch` arm is unreachable — the projection's V-positions are all depth-2 `[s_C, ordinal]`, uniform-length, and `empty()` has nothing to mismatch). A caller needing the concrete V-positions enumerates `k ∈ 1..=content_count(d)`, forms `v_k = [s_C, k]`, and keeps those with `proj.denotes(&v_k)` (cross-checkable via `point(d, VPos{s_C, k})`). M8 returns the `SpanSet` verbatim and leaves that choice to the caller; it does **not** itself test the projection for emptiness via M1.

`discoverable_from(a, d)` avoids the opaque-`SpanSet` test by reducing to membership (F-FULL: `findlinks_V(full region) = {a : discoverable_from(a, d)}`), over the active view:

```rust
fn discoverable_from_on(snap, a, d) -> Result<bool, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    if w.links().readlink(a).is_none()   { return Err(QueryError::NotALink); }   // align non-link handling with `project`
    let full: Vec<Run> = w.m5().content_runs(d).into_iter()
                          .chain(w.m5().link_runs(d)).collect();                 // ran(M(d)), BOTH subspaces (LP12)
    let img = Endset::from_spans(full.iter().map(Run::iextent));
    Ok(stab_union(w, &img, View::Active).contains(a.tumbler()))                  // foundation ∩ active
}
```

Including `link_runs` makes this faithful to LP12's `coverage ∩ ran(M(d))` across both subspaces, with M7's stab handling the level classes. **Non-link handling is now aligned:** both `project` and `discoverable_from` answer `Err(NotALink)` when `a ∉ dom(L)` — `project` via `followlink`'s `Invalid`, `discoverable_from` via an explicit `readlink` gate. A *nullified* link is still a link: it passes the gate (`readlink` reads `dom(L)` verbatim) and `discoverable_from` returns `Ok(false)` under the active view — distinguishing "not a link" from "a retracted link."

### 6. Pre-edit link-survival check (`delete_orphans`)

The practical "this delete will break N links *here*." It is a pure what-if over the snapshot — **it never calls M5's delete** — built on the set identity that falls out of F-UDIST:

> `orphaned = findlinks(A_del) \ findlinks(retained_range)` (active view),

where `A_del` is the I-coverage of the deleted V-range and `retained_range = ran(M'(d))` is what survives (ASN-0117's last-witness condition, with no per-pair reasoning and no need to compute `A_del^{excl}` explicitly). It **mirrors DELETE's preconditions** so the preview is of the *requested* delete, never a coerced/clipped one:

```rust
fn delete_orphans_on(snap, d, p, width) -> Result<OrphanReport, QueryError> {
    let w = snap.world();
    if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
    if p.subspace != Nat::one()          { return Err(QueryError::BadRegion); }   // s_C only (mirror NotContentSubspace)
    let np = p.ordinal.clone();  let nc = w.m5().content_count(d);
    if width.is_zero()                                  { return Err(QueryError::BadRegion); }  // EmptyWidth
    if np < Nat::one() || &np + width > &nc + Nat::one() { return Err(QueryError::BadRegion); }  // unarranged / OutOfBounds

    let del_span = vspan(&Nat::one(), &np, width);                    // [s_C, np] width [0, width]
    let a_del    = w.m5().resolve(d, &del_span);                      // no clipping now (bounds checked)
    let pre = if np > Nat::one() { Some(vspan(&Nat::one(), &Nat::one(), &(&np - Nat::one()))) } else { None };
    let suf_start = &np + width;
    let suf = if suf_start <= nc { Some(vspan(&Nat::one(), &suf_start, &(&nc - &suf_start + Nat::one()))) } else { None };
    let mut retained = w.m5().link_runs(d);                           // a text delete never touches links
    for s in [pre, suf].into_iter().flatten() { retained.extend(w.m5().resolve(d, &s)); }
    let cand = stab_union(w, &Endset::from_spans(a_del.iter().map(Run::iextent)),    View::Active);
    let surv = stab_union(w, &Endset::from_spans(retained.iter().map(Run::iextent)), View::Active);
    Ok(OrphanReport { orphaned: addrs(&cand.difference(surv)) })
}
// vspan(subspace, ordinal, width) = Span::new([subspace, ordinal], [0, width]) — a single V-span value, no algebra.
```

Per-document orphaning is the deliverable. Rejecting a non-`s_C` `p` and an out-of-bounds `(p, width)` up front (as `BadRegion`) means the report is of exactly the delete the caller named — `resolve`'s silent clipping never coerces it into a different one. The **global ghost** determination (LP17: discoverable from *no* document) requires checking each orphan against every other document's range — that reaches into provenance R (M5's `docs_containing`) and is M6 territory; M8 stops at the per-document set and a caller composes the escalation. Read-only throughout.

### 7. Archival supersession/edit lineage (`in_claims`, `out_claims`)

The raw claim enumeration over the edit lineage (ASN-0125 EL11b — the **archival, arrangement-independent** half, which is M8's decomposed scope), composing M7's reverse index — distinct from M7's `succs`/`chain`/`tip`/`current` walks, which stay M7's.

```rust
fn in_claims_on (snap, y, v) -> Vec<SupClaim> { claims_on(snap, FROM, y, v) }   // old(e) = y  (FROM = old, flipped)
fn out_claims_on(snap, x, v) -> Vec<SupClaim> { claims_on(snap, TO,   x, v) }   // new(e) = x  (TO   = new)
fn claims_on(snap, slot, key, v) -> Vec<SupClaim> {
    let l   = snap.world().links();
    let sup = l.reserved_type(ShippedType::Supersedes);
    let hits = l.match_links(&[(slot, enc(slice::from_ref(key)))], v)            // claims naming `key` at `slot`
                .intersection(l.type_slice(sup, v));                            // restrict to supersession claims
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

This design follows **M7's flipped storage convention — `FROM = old/superseded`, `TO = new/superseding`** (the M7→M8 seam), diverging from ASN-0125's textual Df-DIR; so `in(y)` (old = y) probes FROM, `out(x)` (new = x) probes TO. `v = Active` gives the operative graph (`succ_o`), `v = Audit` the full history (`succ_h`). Attribution is the pure M1 `document_of` projection — no store lookup (EL8b).

**Contextual discovery (EL11a — a claim visible in `d` iff `d` lists the endpoint) is out of M8's decomposed scope** (M8 owns the *archival* `in/out` = EL11b). A reader needing it composes M8's archival output with an M5/M6 listing check; M8 does not ship it, precisely because the in-place V-listing test would require an emptiness probe on M5's opaque projection that M1 does not provide (§5).

## Invariants & contracts

**By construction** (fall out of the data model / faithful composition):

- **Writes nothing; frame `Σ`.** M8 calls only pure reads + `snapshot()`. (all sources; ASN-0121 read-only frame, CN-DEF, RE-DEF)
- **Result determinism at a snapshot; result-as-set, dedup-by-address.** `OrdSet<Tumbler>` is keyed by address, so "transclusion found once" (FL-REACH(b)) and no value-dedup hold for free; window boundaries are objective (W11). (ASN-0127, ASN-0121 FL-REACH, ASN-0108 W3/W11)
- **Existence-anchored monotonicity (FTT family).** Inherited from M7's append-only active slice + coverage permanence. (ASN-0121 FL-MON, ASN-0132 CN-MONO, ASN-0127 E-MONO)
- **Result-drop = present unreachability *or* retraction, not deletion of the stored object.** Under the uniform `View::Active`, a link leaves a result either because it is no longer arrangement-reachable (the present-tense reading) *or* because it was nullified; neither means the stored link, its coverage, or its address ceased to exist — those are permanent upstream. (ASN-0127 D-ZERO + ASN-0121 FL-RET / ASN-0132 CN-RETRACT; ASN-0098 LP13)
- **Cursor survives orphaning; no duplicate / no skip; append-at-tail.** From the permanent address key + key-cut resume. (ASN-0108 W4/W5/W6/W8)
- **Union-distributivity** of region/findlinks composition; whole-endset RETRIEVEENDSETS preserves it. (ASN-0127 F-UDIST/F-VDIST, ASN-0131 RE-UDIST/RE-CLIP)

**By active enforcement** (M8 must guard):

- **Document-existence + region gate.** `is_registered_document(d)` then `check_region(region)` *before* any M5 read on every V-anchored op — M5 conflates registered-empty (`∅`, defined) with unregistered (error) and silently clips a malformed span. Guarded at the top of `image_on` (inherited by `findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`) and at `project`/`discoverable_from`/`delete_orphans`. `delete_orphans` additionally mirrors DELETE's `s_C`/in-bounds/non-empty-width preconditions (`BadRegion`), never previewing a coerced delete. (ASN-0127 F-IMG/F-V, ASN-0131, ASN-0117, decomposition seam)
- **Snapshot consistency.** Read L, M, and the registry off **one** `Snapshot` per op, and **thread that one `snap` through internal composition** (`image_on`, never `self.image`); the `_on` twins let M10 share a snapshot across count+window. Guarded by snapshotting once and reading only `snap.world()`. (ASN-0127 Recovery; M2 clause 6)
- **Addressability filter.** Pass `View::Active` (not `Audit`) for every present-state query, so nullified links never appear. Guarded at each `stab`/`match_links`/`type_slice` call site. (ASN-0121 FL-RET, ASN-0132 CN-RETRACT)
- **Home filter via address projection, never arrangement presence.** `home_ok` uses M1 `document_of`. (ASN-0132 CN-STAB)
- **Present-tense discovery (no stale serve).** M8 owns no cache and always recomputes — the enforcement *is* the no-cache design. (ASN-0127 D-NONMONO, ASN-0108 W7)
- **Withhold identity + dedup by structural endset value** in RETRIEVEENDSETS; **no clipping**. Guarded in the projection-and-dedup loop. (ASN-0131 RE-UNIT/RE-CLIP)
- **Last-witness set algebra** in the survival check (`findlinks(A_del) \ findlinks(retained)`), never per-pair. (ASN-0117)
- **No raw mixed-length span algebra.** Coverage overlap → M7; I→V → M5; query endsets → `from_spans(run.iextent())`. Guarded by never calling M1 `intersect_sets`/`difference_sets` on upstream covers. (M5/M7 level-class warnings)

## Dependencies & seams

**Upstream consumed:**

- **M1** — `Tumbler` total order (the `OrdSet` order = enumeration key, cursor cut); `document_of` (home projection for `athome` and claim attribution); `validate` (`Tumbler → Address` at output, applied to a *clone* of each iterated `&Tumbler`, infallible by M3's mint); `classify_spans` for the RETRIEVEENDSETS touch test; `Span::new`/`Tumbler::new` for the survival-check V-spans; `Endset`/`Span` construction inputs. (`equiv`/`SpanSet::empty` are the *caller's* recipe for probing `project`'s opaque result — M8 itself never tests a `SpanSet` for emptiness.)
- **M2** — `kernel.snapshot()` for one consistent (L, M, registry) read; `snapshot.world()`/`seq()`; no writes.
- **M3** — `is_registered_document(d)` only (the doc-existence gate).
- **M5** — `resolve` (V→I runs, the image source), `project` (I→V content, level-class-safe), `content_runs`/`link_runs` (`ran M(d)` for discoverability/survival), `content_count` (delete bounds), `point`. M8 never reads R.
- **M7** — `stab`/`match_links`/`type_slice` (the spanfilade — *the* matcher; M8 does not reimplement it), `readlink`/`followlink`, `is_active`, `reserved_type(Supersedes)`, `enc`/`Endset::from_spans`, `View::Active`/`Audit`; archival composes `match_links ∩ type_slice` + `readlink`. M8 lifts a §G `Tumbler` to `Address` via `validate` before any `readlink`.

**Downstream / seam contracts M10 builds against:**

- **Region family** (`image`/`findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`): take `(d, region: &[Span])`; **return `Err(DocNotRegistered)` for an unregistered `d`**, **`Err(BadRegion)` for a region that is not content-subspace ordinal-level depth-2 V-spans**, and a defined empty result for a registered-empty `d`. Present-tense, non-monotone. M10 phrases the V-region (content subspace, depth-2).
- **Descriptor family** (`findlinks_ftt`/`count_ftt`/`window_ftt`): take an address-phrased `FourSet`; total (no doc gate); monotone; `count_ftt` is ASN-0132's operation. M10 resolves any reader content-pointings to addresses upstream.
- **Windowing**: cursor is a bare `Address`; `Window.exhausted` is the terminal signal; `next` resumes; stateless across calls (`n ≥ 1`). M10 carries the cursor; a partial/empty batch ends the pass.
- **Pure twins** (`*_on(&Snapshot<W>, …)`): M10 uses these to read a count and its window — or any pair — off one snapshot, satisfying the snapshot-token consistency need.
- M8 returns `Vec<Address>` / `usize` / `Window` / `HashSet<(usize, Endset)>` / `SupClaim` / `OrphanReport`; M10 marshals to the wire and surfaces precondition failures (`DocNotRegistered`/`NotALink`/`BadRegion`) as typed rejections (never a silent skip). These are reads — no commit — but still snapshot-isolated.

Crate graph: `skep-linkquery → skep-address, skep-kernel, skep-namespace, skep-arrangement, skep-links` (pure surfaces); `skep-operation (M10) → skep-linkquery`. M8 names no `World`/`Record`; contributes no slice to `skep-engine`. Acyclic, mirroring `M8 → M1, M2, M3, M5, M7`.

## Conflicts resolved

1. **The AND-of-ORs combiner — M7's `Observe`/`match_links` vs. M8's `findlinks` (the decomposition's softest seam).** Resolved in M7's favor, per the recommended factoring: M7 owns the per-slot matcher *and* the combiner (`stab`/`match_links`), and M8 is **pure discovery presentation** — windowing, cursors, count, pagination, projection, RETRIEVEENDSETS, archival, survival — over M7's matcher. M8 implements no slot matching or AND-of-ORs.

2. **Disjunctive `findlinks` (ASN-0127, any slot) vs. conjunctive `findlinks_FTT` (ASN-0121, four-set).** ASN-0121 is explicit they are not restrictions of each other. M8 exposes **both as distinct entry points** — the region family (disjunctive, V-anchored, present-tense, doc-gated) and the descriptor family (conjunctive, address-keyed, monotone, link-store-local). They share M7's per-slot `stab` but combine it oppositely (union vs. AND); neither is built on the other.

3. **The enumeration key (ASN-0108).** The note warns that no permanent key is the spanfilade's *native* (matched-slot) order, and the matched-slot order is unsafe under partial orphaning. In **this** design M7's discovery primitives return `im::OrdSet<Tumbler>` — **address order, the permanent key** — not matched-slot order. So the permanent key *is* the order M8 sees; windowing is a safe range scan with no derived index. The least-covered-tumbler alternative would force M8 to build an index it is forbidden to own. Resolution: address key, full stop.

4. **Existence-anchored (monotone) vs. discovery-anchored (non-monotone).** Kept as distinct families with distinct documented stability: `count_ftt` is the monotone existence census (CN-MONO); `window_v` is the non-monotone present-tense view (the ASN-0108 `Match = findlinks_V` reading). Because M8 owns no cache, present-tense correctness is free.

5. **Supersession slot directionality.** ASN-0125 Df-DIR reads `F = new`; M7's actual storage (per the seam) is **flipped: `F = old/superseded`, `G = new/superseding`.** M8 follows M7's storage — `in(y)` probes FROM, `out(x)` probes TO. Noted divergence from the source text. (Contextual EL11a, which would also turn on this convention, is out of M8's scope — see §7.)

6. **RETRIEVEENDSETS whole-endset vs. touching-spans (ASN-0131 OQ1).** Resolved to **whole-endset** (return `readlink`'s full value), preserving union-distributivity (RE-UDIST) at the cost of one `readlink` per candidate.

7. **Home/residence filter placement (ASN-0121).** M8 owns no index dimension, so home is a **post-filter** via M1 `document_of` (lazy during a window walk). A home-only query degrading to a full active scan is accepted.

8. **Addressability: unfiltered foundations vs. addressable operations.** ASN-0127/0098/0108's `findlinks_V`/`discoverable_from`/`Match` range over the *whole* `dom(Σ.L)` — ASN-0121 FL-DEF flags ASN-0127's `findlinks` as "slot-agnostic, unfiltered" and explicitly **not a restriction** of the addressable `findlinks_FTT`. But the operation notes M8 actually *realizes* — RE-DEF, FL-DEF, CN-DEF — all range over `addressable(Σ) = dom(L) \ nullified`. M8 therefore queries every present-state primitive with `View::Active` **uniformly**, so `findlinks_v`/`count_v`/`window_v`/`discoverable_from` are the disjunctive/membership foundation **intersected with the active view** (not the bare foundation — the §1 label is corrected accordingly); `retrieve_endsets`/`findlinks_ftt`/`count_ftt` are already note-exact (their notes are addressable). The consequence for the "result-drop" reading — a missing link asserts present unreachability **or** retraction, never deletion of the stored object — is captured in the refined invariant.

## Open build decisions

- **The arity-≥4 disjunction (genuine seam gap, tied to the v1 invariant).** `findlinks_v`/RETRIEVEENDSETS union slots `{FROM, TO, TYPE}`, which is the **exact** ASN-0127 disjunction *because* the v1 arity-3 invariant holds — every v1 link-creation path (`makelink`/`emit`/`nullify`/`assert_sup`/`editlink`) deposits an arity-3 link (§1). The moment an arity-≥4 type with content-reaching extra slots ships, that invariant breaks and the union is no longer exhaustive; it then needs an M7 `stab_any` or an exposed max-arity. **Pick `{1,2,3}` for v1** and negotiate the M7 extension only if such a type ships — this is the one place M8's fidelity depends on an M7 capability not in the current interface.
- **Survival-check scope.** Per-document orphan set (the "breaks N links here" feature — cheap, recommended default) vs. also the **global-ghost** escalation (each orphan checked against every other document via M5's R-index — expensive, and it crosses into M6/provenance). Default per-document; expose global only if a caller needs LP17 ghost determination, and route it through M6.
- **Contextual claim discovery (EL11a).** Left out of M8 (scope = archival `in/out` = EL11b). If a reader wants "which claims does `d` list," compose M8's archival output with an M5/M6 listing check at a higher layer — do not push an M5-projection-emptiness probe into M8 (M1 gives no such test).
- **Secondary enumeration key.** Address-only (default; free from M7's order) vs. also offering content-order (least-covered-tumbler) pagination at O(|Match|·log) per-window re-sort. Add the re-sort only if a reader needs content-ordered windows; never build a persistent key index (M8 owns none).
- **Count caching.** M8 recomputes (owns no state). Whether M10 wraps `count_ftt` with an epoch-tagged cache (CN-STAB: changes only on `K.λ`) and whether to special-case the all-wildcard count to `len()` of M7's active slice are M10/M7 choices, not M8's.
- **Cursor token shape.** Bare `Address` (sufficient — the key *is* the address) vs. a fattened opaque token. Default bare; fatten only to skip a (zero-cost here) key recompute, never to carry a server-side materialized list.
- **Region presentation.** `&[Span]` per single document (the contract here) vs. a multi-document SpecSet. Multi-document fan-out is a higher-layer composition, not M8's.
