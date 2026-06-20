# M8 — Link Query & Discovery — Detailed Design

## Purpose & boundary

M8 is the **read-only query/presentation layer over the link subsystem**: given a content region it answers *which links touch here*; given a four-set descriptor it answers *which links match*; and it counts, paginates, projects, retrieves endsets, previews delete-orphaning, and traces supersession lineage — all by composing M7's spanfilade and behavior atoms, M5's arrangement, and M3's registry over one M2 snapshot. It does **one thing well: turn upstream link/arrangement/registry state into the answers readers ask, owning no authoritative state and no index.**

What it does *not* do, deferred to neighbors: it does **not** own the spanfilade or any coverage index, and does **not** implement the per-slot matcher or the AND-of-ORs combiner — those are M7's `stab`/`match_links`/`type_slice` (the soft seam, resolved below). It stores no coverage (M7's `followlink`), reads no content bytes (M4), reads no provenance R and runs no R-keyed query — SHOWDELETIONS/FINDDOCSCONTAINING are M6's. It never invokes M5's edit path (the survival check is a pure what-if), never mints or writes anything, and is **fenced off from M9** (ASN-0129): M9 reads its PL surface straight from M7, never through M8. M8 is pure composition; every answer is recomputed from upstream on each call.

## Public interface

Foreign types: `Address/Span/SpanSet/Nat/Tumbler` (M1); `Kernel/Snapshot/Seq/WorldState` (M2); `Run/VPos` (M5); `Endset/View/ShippedType/HasLinks` (M7); `HasM5` (M5); `HasM3` (M3). Slots are 1-based, M7's convention.

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

**Snapshot twins.** Every method `foo(&self, …)` is sugar for `foo_on(&self.kernel.snapshot(), …)`. The pure `foo_on(snap: &Snapshot<W>, …)` free functions are public and are what **M10 calls to read a count and its window — or any multi-call verdict — off one consistent state** (the ASN-0132 snapshot-token need; M2 clause 6). The handle takes a fresh snapshot per call, so each standalone op is self-consistent.

`coverage(a, i)` is **not** re-exposed — it is exactly M7's `followlink(a, i)`; callers use M7 directly.

## Core data model

**M8 owns no `WorldState` slice, no journal record, no fold, and no index.** It contributes nothing to the assembled `World` and journals nothing; it names neither `World` nor `Record` (generic over `W` with `HasLinks + HasM5 + HasM3`). Its crate `skep-linkquery` depends on the pure surfaces of M1/M2/M3/M5/M7 and is depended on only by M10 — it is a query crate, not a store.

Its "data model" is therefore just (a) the request/result value types above and (b) one load-bearing representation decision:

- **Result sets are carried internally as `im::OrdSet<Tumbler>` — M7's native discovery return type — and converted to `Vec<Address>` (each `Tumbler` lifted via M1 `validate`, infallible by M3's mint) only at the output boundary.** This is the whole engine: `union`/`intersection`/`difference`/`range` on a persistent ordered set are cheap and structurally-shared, and **`OrdSet<Tumbler>` is ordered by tumbler = link address = exactly ASN-0108's permanent enumeration key.** So windowing is a `range(Excluded(cursor)..).take(n)` — no M8-side index, no re-sort. This is what lets M8 "own no index" yet page efficiently.

- **Authoritative state owned: none.** The link store, active/audit slices, spanfilade, type registry (M7); arrangements and R (M5); registry (M3). **Recomputable hints owned: none.** M8 recomputes every answer from upstream each call; the only index it leans on (M7's spanfilade) is M7's hint, recovered by M7. The unit of consistency is the M2 `Snapshot` threaded through one operation.

A second, quieter discipline shapes every algorithm: **M8 does essentially no span algebra itself.** Mixed-length covers (a content address and a link address differ in tumbler length) fault M1's `intersect_sets`/`difference_sets` with `LevelMismatch`. M8 sidesteps this entirely — coverage-overlap matching goes through M7's `stab`/`match_links` (M7 handles level classes), I→V projection goes through M5's `project` (handles them internally), and query `Endset`s are built from `Run::iextent()` via `Endset::from_spans` (verbatim, no algebra). M8 never differences or intersects raw covers; it set-operates only on `OrdSet<Tumbler>` (addresses, uniform — no level issue).

## Internal design

Every operation opens with one snapshot and reads `links() / m5() / m3()` off `snap.world()` — never separate snapshots (the (L, M) coherence ASN-0127 forces). "Recovery" is trivial and uniform: M8 persists nothing; each answer is recomputed from upstream state, which M2 recovers by replay. I omit it per capability below.

### 1. Content-region discovery (`image`, `findlinks_v`, `count_v`)

**The document-existence gate is the first act of every V-anchored op.** M5's reads return empty for *both* registered-empty and unallocated documents — it cannot tell them apart. So M8 must:

```rust
if !w.m3().is_registered_document(d) { return Err(QueryError::DocNotRegistered); }
```

A registered-but-empty `d` then yields a legitimate `∅` (defined); an unregistered `d` surfaces as an error, not a masquerading "no links here" (ASN-0127 F-IMG/F-V; ASN-0131; the decomposition seam).

**`image`** resolves the V-region to I-runs through the live arrangement: for each V-span, `m5.resolve(d, span)` → `Vec<Run>`, concatenated. I use `resolve` (runs), **not** `resolve_coverage` (an opaque `SpanSet`) — runs carry `i_start + width`, expose `iextent() -> Span`, and dodge both the `SpanSet`-iteration gap and the level-class trap. `resolve` is defensive (silently clips out-of-range, returns `⟨⟩` for a malformed span), so the image is exactly the currently-arranged subset of the region (ASN-0127's load-bearing `W ∩ dom M(d)` intersection — unarranged positions contribute nothing).

**`findlinks_v`** is the disjunctive ASN-0127 `findlinks(image(W,d))`. Build the query endset from the runs, union per-slot stabs:

```rust
let img: Vec<Run> = self.image(d, region)?;
if img.is_empty() { return Ok(vec![]); }                       // empty-input short-circuit (F-V), no index touch
let q = Endset::from_spans(img.iter().map(Run::iextent));      // coverage(q) = the image
let mut out = im::OrdSet::new();
for i in [FROM, TO, TYPE] { out = out.union(w.links().stab(i, &q, View::Active)); }
// View::Active == addressable == dom(L) \ nullified
```

The OR-across-slots is the union of single-slot stabs (M7 has no slot-collapsed primitive); `View::Active` discharges addressability *for free*. The common case is small — a region resolves to a handful of runs, each stab is a logarithmic spanfilade probe. **Tradeoff / seam gap:** I union slots `{FROM, TO, TYPE}` — the "from-to-three" contract these ops are named for. A fully faithful ASN-0127 disjunction folds in *every* slot of an arity-> 3 link, which M7's per-slot `stab` cannot do without an exposed max-arity or a `stab_any`. Flagged in *Open build decisions*; for v1's arity-3 links it is exact.

**`count_v`** = `findlinks_v(...).len()`. It is the present-tense census of region-reaching links — non-monotone (ASN-0127 D-NONMONO), and a `0` asserts present unreachability, not history (D-ZERO).

### 2. Windowed enumeration (`window_v`, `window_ftt`) — the cursor mechanism

The protocol is **stateless**: the entire continuation is the client's cursor, a permanent **link address** (ASN-0108 W2/W3). No server iterator, no cached list, no generation counter. Each call recomputes the matching set and key-cuts it:

```rust
let matched: im::OrdSet<Tumbler> = /* findlinks_v set, or findlinks_ftt's match set */;
let lo = match cur { None => Unbounded, Some(c) => Excluded(c.tumbler().clone()) };
let batch: Vec<Address> = matched.range((lo, Unbounded))    // ascending = address order = the key
                                 .take(n).map(validate).collect();
let next = batch.last().cloned().map(/* Address */).or(cur); // ≺-max of batch, else cursor unchanged
Window { exhausted: batch.len() < n, batch, next }
```

Why this is correct and cheap:

- **Resume is a key-cut, never an exact-match scan for the cursor link** — `range(Excluded(c)..)` returns the matchers with address strictly greater than `c`, *whether or not `c` is still in `matched`*. This is the one thing Green got wrong (its scan returns an empty batch when the cursor link orphaned out, indistinguishable from exhaustion). The key-cut gives **cursor-survives-orphaning by construction** (W8): the address key is computable from the held cursor with zero lookups, and the cut needs nothing else.
- **The matching set is recomputed each call against the live snapshot** (approach A), but the recompute is itself O(seek + N) because M7 hands back `OrdSet<Tumbler>` *already in key order* — approach A and B collapse into one. M8 owns no cache, so present-tense correctness (W7, never serve a stale view) is free.
- **No duplicate, no skip** of continuously-matching links (W4/W5): the address key's comparisons never move, so a delivered link stays below every later cursor. **Append-at-tail** for newly created links holds within a home document (addresses are allocation-monotone, W6) — the documented cross-home blind spot stands (cross-home order is not state-recoverable).
- **Exhaustion = short window**, zero included: `exhausted = batch.len() < n` (W9). The caller stops on the first short batch.

`window_v`'s set is `findlinks_v` (disjunctive V-region — the ASN-0108 `Match = findlinks_V` reading). `window_ftt`'s set is `findlinks_ftt`'s match (below), with the home filter applied **lazily during the range walk** — range from cursor, drop non-home links, take N — so a home-narrow query never materializes the full filtered set. Caller obligation: `n ≥ 1`.

### 3. Four-set descriptor query (`findlinks_ftt`, `count_ftt`, `window_ftt`)

This is the **address-keyed, conjunctive, link-store-local** family (ASN-0121/0132) — *not* the V-region disjunctive one (ASN-0121 is explicit: neither is a restriction of the other). No document gate (it reads only `Σ.L`, FL-LOC). The request arrives already phrased over addresses (V→I resolution is upstream).

```rust
fn match_core(w, q) -> im::OrdSet<Tumbler> {
    // empty-constrained slot annihilates (FL-EMP):
    if q.from|to|ty|home is Empty (empty coverage) { return OrdSet::new(); }
    let mut cons = vec![];                                  // wildcards drop out (FL-WILD)
    if let Spans(e) = &q.from { cons.push((FROM, e.clone())); }
    if let Spans(e) = &q.to   { cons.push((TO,   e.clone())); }
    if let Spans(e) = &q.ty   { cons.push((TYPE, e.clone())); }
    w.links().match_links(&cons, View::Active)              // AND-of-ORs over constrained slots; [] ⇒ whole active slice
}
fn home_ok(q, a: &Tumbler) -> bool {                       // athome(a,H): home(a) ∈ coverage(H)
    match &q.home { Any => true, Empty => false,
        Spans(h) => h.denotes(document_of(&validate(a)).unwrap().tumbler()) }  // home(a) = M1 document projection
}
```

`findlinks_ftt` = `match_core` filtered by `home_ok`; `count_ftt` = that count; `window_ftt` = range-then-`home_ok`-then-take. The all-wildcard `(∗,∗,∗,∗)` is `match_links(&[], Active)` = the whole addressable slice (FL-WILD). **The home filter is an address projection (`document_of`), never an arrangement-presence test** — a reverse-orphaned link (its own home entry deleted) still satisfies a home-bounded query (CN-STAB; the cautionary CN home note). A home-only query degrades to a full active scan (no slot narrows it) — accepted, since M8 owns no index dimension. This family is **monotone** (FL-MON/CN-MONO): the active slice only grows, coverage is permanent, so a found-and-not-retracted link stays found.

### 4. RETRIEVEENDSETS (`retrieve_endsets`)

Same selection index as `findlinks_v`, a different read-out: report `(slot, endset)` pairs touching the region, **withholding link identity** (ASN-0131 RE-UNIT).

```rust
let img = self.image(d, region)?;                               // gate inside
if img.is_empty() { return Ok(HashSet::new()); }
let q = Endset::from_spans(img.iter().map(Run::iextent));
let candidates = stab(FROM,&q,Active) ∪ stab(TO,&q,Active) ∪ stab(TYPE,&q,Active);  // sel = findlinks_v ∩ active
let mut out = im::HashSet::new();
for c in candidates {
    let link = w.links().readlink(&validate(c)).unwrap();      // resident (from active slice)
    for i in 1..=link.arity() {                                // ALL slots, incl. 4+ on a found candidate
        let e = link.slot(i).unwrap();
        if touches(e, &img) { out.insert((i, e.clone())); }   // WHOLE endset, no clip; dedup by structural Eq
    }
}
```

`touches(e, img)` tests `coverage(e) ∩ image ≠ ∅` per slot — reusing M1 `classify_spans` on the endset's spans vs. the run extents (`ProperOverlap | Containment | Equal`), or equivalently per-slot stab membership. Key decisions, all forced by the note: **whole-endset surfacing** (emit `e.clone()` — the full stored value from `readlink`, never clipped, RE-CLIP), which preserves union-distributivity (RE-UDIST); **dedup by structural endset equality** (`Endset: Eq + Hash`), so value-identical endsets from distinct links collapse to one pair and identity is genuinely withheld (RE-UNIT); **content-identity answer** (I-address endsets — permanent), with V-rendering left to a lossy layer above. The candidate union is `{1,2,3}` (same arity caveat as §1); emission iterates a candidate's full arity, so any extra touching slots on a *found* candidate are surfaced.

### 5. Projection & discoverability (`project`, `discoverable_from`)

`project(a, i, d)` = the V-positions in `d` where link `a`'s slot `i` lands (ASN-0098 `project`):

```rust
if !w.m3().is_registered_document(d) { return Err(DocNotRegistered); }
let cov = w.links().followlink(a, i).map_err(|_| QueryError::NotALink)?;  // slot-i coverage SpanSet
Ok(w.m5().project(d, &cov))                                              // I→V, content subspace, level-class-safe
```

M5's `project` consumes the coverage `SpanSet` directly (no iteration needed) and applies the level-class discipline internally, so this is fault-free for any coverage including cross-length prefix/subtree spans. The result is **content-subspace** V-positions — the per-caller restriction the decomposition names; link-subspace reverse discovery is M7's BH3, not M8's.

`discoverable_from(a, d)` avoids the (opaque, no-`is_empty`) `SpanSet` test by reducing to membership (F-FULL: `findlinks_V(full region) = {a : discoverable_from(a, d)}`):

```rust
let full = content_runs(d) ++ link_runs(d);                  // ran(M(d)), both subspaces
let img  = Endset::from_spans(full.iter().map(Run::iextent));
Ok(findlinks_over(img, [FROM,TO,TYPE], Active).contains(a.tumbler()))
```

Including `link_runs` makes this faithful to LP12's `coverage ∩ ran(M(d))` across both subspaces, with M7's stab handling the level classes.

### 6. Pre-edit link-survival check (`delete_orphans`)

The practical "this delete will break N links *here*." It is a pure what-if over the snapshot — **it never calls M5's delete** — built on the clean set identity that falls out of F-UDIST:

> `orphaned = findlinks(A_del) \ findlinks(retained_range)` (active view),

where `A_del` is the I-coverage of the deleted V-range and `retained_range = ran(M'(d))` is what survives. (Because `ran(M(d)) = retained ∪ A_del^{excl}` and findlinks distributes over union, subtracting `findlinks(retained)` from `findlinks(A_del)` yields exactly the links whose *only* d-witnesses are the exclusively-dropped addresses — ASN-0117's last-witness condition, with no per-pair reasoning and no need to compute `A_del^{excl}` explicitly.)

```rust
if !is_registered_document(d) { return Err(DocNotRegistered); }
let np = ord(p);  let nc = content_count(d);
let del_span = vspan(s_C, np, width);                            // [s_C,np] .. width [0,width]
let a_del    = resolve(d, &del_span);                            // clips silently to arranged positions
let pre   = if np > 1        { Some(vspan(s_C, 1,    np-1))    } else { None };
let suf   = if np+width <= nc{ Some(vspan(s_C, np+width, nc-(np+width)+1)) } else { None };
let mut retained = link_runs(d);                                 // a text delete never touches links
for s in [pre, suf].into_iter().flatten() { retained.extend(resolve(d, &s)); }
let cand = findlinks_over(Endset::from_spans(a_del.iter().map(Run::iextent)),    [1,2,3], Active);
let surv = findlinks_over(Endset::from_spans(retained.iter().map(Run::iextent)), [1,2,3], Active);
Ok(OrphanReport { orphaned: cand.difference(surv).map(validate).collect() })
```

Per-document orphaning is the deliverable. The **global ghost** determination (LP17: discoverable from *no* document) requires checking each orphan against every other document's range — that reaches into provenance R (M5's `docs_containing`) and is M6 territory; M8 stops at the per-document set and a caller composes the escalation. Read-only throughout; `resolve`'s silent clipping means the report reflects exactly what an in-bounds delete would drop.

### 7. Archival supersession/edit lineage (`in_claims`, `out_claims`)

The raw claim enumeration over the edit lineage (ASN-0125 EL11b), composing M7's reverse index — distinct from M7's `succs`/`chain`/`tip`/`current` walks, which stay M7's.

```rust
fn in_claims_on(snap, y, v) -> Vec<SupClaim> {                  // claims with old(e) = y
    let l = snap.world().links();
    let sup = l.reserved_type(ShippedType::Supersedes);
    let hits = l.match_links(&[(FROM, enc(slice::from_ref(y)))], v)   // FROM = old (flipped convention)
                .intersection(l.type_slice(sup, v));                 // restrict to supersession claims
    hits.into_iter().map(|c| { let ca = validate(c); let link = l.readlink(&ca).unwrap();
        SupClaim { old:  validate(link.from_slot().addrs().next().unwrap().clone()),
                   new:  validate(link.to_slot().addrs().next().unwrap().clone()),
                   home: document_of(&ca).unwrap(),
                   active: l.is_active(&ca), claim: ca } }).collect()
}
```

`out_claims(x)` is the mirror with `(TO, enc(&[x]))` (TO = new). This design follows **M7's flipped storage convention — `FROM = old/superseded`, `TO = new/superseding`** (the M7→M8 seam), diverging from ASN-0125's textual Df-DIR; so `in(y)` (old = y) probes FROM, `out(x)` (new = x) probes TO. `v = Active` gives the operative graph (`succ_o`), `v = Audit` the full history (`succ_h`). Attribution is the pure M1 `document_of` projection — no store lookup (EL8b). **Contextual discovery** (EL11a — a claim is visible in `d` iff `d` lists the endpoint) is a one-line refinement: filter `in_claims(y)` by `!m5.project(d, followlink(claim, FROM)).is_empty()` (project FROM for `listed(old)`, TO for `listed(new)`).

## Invariants & contracts

**By construction** (fall out of the data model / faithful composition):

- **Writes nothing; frame `Σ`.** M8 calls only pure reads + `snapshot()`. (all sources; ASN-0121 read-only frame, CN-DEF, RE-DEF)
- **Result determinism at a snapshot; result-as-set, dedup-by-address.** `OrdSet<Tumbler>` is keyed by address, so "transclusion found once" (FL-REACH(b)) and no value-dedup hold for free; window boundaries are objective (W11). (ASN-0127, ASN-0121 FL-REACH, ASN-0108 W3/W11)
- **Existence-anchored monotonicity (FTT family).** Inherited from M7's append-only active slice + coverage permanence. (ASN-0121 FL-MON, ASN-0132 CN-MONO, ASN-0127 E-MONO)
- **Result-drop = present unreachability, not deletion.** Links/coverage/addresses are permanent upstream; a missing link asserts present-tense unreachability. (ASN-0127 D-ZERO, ASN-0098 LP13)
- **Cursor survives orphaning; no duplicate / no skip; append-at-tail.** From the permanent address key + key-cut resume. (ASN-0108 W4/W5/W6/W8)
- **Union-distributivity** of region/findlinks composition; whole-endset RETRIEVEENDSETS preserves it. (ASN-0127 F-UDIST/F-VDIST, ASN-0131 RE-UDIST/RE-CLIP)

**By active enforcement** (M8 must guard):

- **Document-existence gate.** `is_registered_document(d)` *before* any M5 read on every V-anchored op — M5 conflates registered-empty (`∅`, defined) with unregistered (error). Guarded at the top of `image`/`project`/`discoverable_from`/`delete_orphans` and the V-window/count/retrieve. (ASN-0127 F-IMG/F-V, ASN-0131, decomposition seam)
- **Snapshot consistency.** Read L, M, and the registry off **one** `Snapshot` per op (and the `_on` twins let M10 share one across count+window). Guarded by snapshotting once and reading only `snap.world()`. (ASN-0127 Recovery; M2 clause 6)
- **Addressability filter.** Pass `View::Active` (not `Audit`) for every present-state query, so nullified links never appear. Guarded at each `stab`/`match_links`/`type_slice` call site. (ASN-0121 FL-RET, ASN-0132 CN-RETRACT)
- **Home filter via address projection, never arrangement presence.** `home_ok` uses M1 `document_of`. (ASN-0132 CN-STAB)
- **Present-tense discovery (no stale serve).** M8 owns no cache and always recomputes — the enforcement *is* the no-cache design. (ASN-0127 D-NONMONO, ASN-0108 W7)
- **Withhold identity + dedup by structural endset value** in RETRIEVEENDSETS; **no clipping**. Guarded in the projection-and-dedup loop. (ASN-0131 RE-UNIT/RE-CLIP)
- **Last-witness set algebra** in the survival check (`findlinks(A_del) \ findlinks(retained)`), never per-pair. (ASN-0117)
- **No raw mixed-length span algebra.** Coverage overlap → M7; I→V → M5; query endsets → `from_spans(run.iextent())`. Guarded by never calling M1 `intersect_sets`/`difference_sets` on upstream covers. (M5/M7 level-class warnings)

## Dependencies & seams

**Upstream consumed:**

- **M1** — `Tumbler` total order (the `OrdSet` order = enumeration key, cursor cut); `document_of` (home projection for `athome` and claim attribution); `validate` (`Tumbler → Address` at output); `classify_spans` for the RETRIEVEENDSETS touch test; `Endset`/`Span` construction inputs.
- **M2** — `kernel.snapshot()` for one consistent (L, M, registry) read; `snapshot.world()`/`seq()`; no writes.
- **M3** — `is_registered_document(d)` only (the doc-existence gate).
- **M5** — `resolve` (V→I runs, the image source), `project` (I→V content, level-class-safe), `content_runs`/`link_runs` (`ran M(d)` for discoverability/survival), `content_count` (delete bounds), `point`. M8 never reads R.
- **M7** — `stab`/`match_links`/`type_slice` (the spanfilade — *the* matcher; M8 does not reimplement it), `readlink`/`followlink`, `is_active`, `reserved_type(Supersedes)`, `enc`/`Endset::from_spans`, `View::Active`/`Audit`; archival composes `match_links ∩ type_slice` + `readlink`. M8 lifts §G `Tumbler` results to `Address` via `validate` before any `readlink`.

**Downstream / seam contracts M10 builds against:**

- **Region family** (`image`/`findlinks_v`/`count_v`/`window_v`/`retrieve_endsets`): take `(d, region: &[Span])`; **return `Err(DocNotRegistered)` for an unregistered `d`** and a defined empty result for a registered-empty one. Present-tense, non-monotone. M10 phrases the V-region (subspace via the spans).
- **Descriptor family** (`findlinks_ftt`/`count_ftt`/`window_ftt`): take an address-phrased `FourSet`; total (no doc gate); monotone; `count_ftt` is ASN-0132's operation. M10 resolves any reader content-pointings to addresses upstream.
- **Windowing**: cursor is a bare `Address`; `Window.exhausted` is the terminal signal; `next` resumes; stateless across calls. M10 carries the cursor; a partial/empty batch ends the pass.
- **Pure twins** (`*_on(&Snapshot<W>, …)`): M10 uses these to read a count and its window — or any pair — off one snapshot, satisfying the snapshot-token consistency need.
- M8 returns `Vec<Address>` / `usize` / `Window` / `HashSet<(usize, Endset)>` / `SupClaim` / `OrphanReport`; M10 marshals to the wire and surfaces precondition failures as typed rejections (never a silent skip). These are reads — no commit — but still snapshot-isolated.

Crate graph: `skep-linkquery → skep-address, skep-kernel, skep-namespace, skep-arrangement, skep-links` (pure surfaces); `skep-operation (M10) → skep-linkquery`. M8 names no `World`/`Record`; contributes no slice to `skep-engine`. Acyclic, mirroring `M8 → M1, M2, M3, M5, M7`.

## Conflicts resolved

1. **The AND-of-ORs combiner — M7's `Observe`/`match_links` vs. M8's `findlinks` (the decomposition's softest seam).** Resolved in M7's favor, per the recommended factoring: M7 owns the per-slot matcher *and* the combiner (`stab`/`match_links`), and M8 is **pure discovery presentation** — windowing, cursors, count, pagination, projection, RETRIEVEENDSETS, archival, survival — over M7's matcher. M8 implements no slot matching or AND-of-ORs.

2. **Disjunctive `findlinks` (ASN-0127, any slot) vs. conjunctive `findlinks_FTT` (ASN-0121, four-set).** ASN-0121 is explicit they are not restrictions of each other. M8 exposes **both as distinct entry points** — the region family (disjunctive, V-anchored, present-tense, doc-gated) and the descriptor family (conjunctive, address-keyed, monotone, link-store-local). They share M7's per-slot `stab` but combine it oppositely (union vs. AND); neither is built on the other.

3. **The enumeration key (ASN-0108).** The note warns that no permanent key is the spanfilade's *native* (matched-slot) order, and the matched-slot order is unsafe under partial orphaning. In **this** design M7's discovery primitives return `im::OrdSet<Tumbler>` — **address order, the permanent key** — not matched-slot order. So the permanent key *is* the order M8 sees; windowing is a safe range scan with no derived index. The least-covered-tumbler alternative would force M8 to build an index it is forbidden to own. Resolution: address key, full stop.

4. **Existence-anchored (monotone) vs. discovery-anchored (non-monotone).** Kept as distinct families with distinct documented stability: `count_ftt` is the monotone existence census (CN-MONO); `window_v` is the non-monotone present-tense view (the ASN-0108 `Match = findlinks_V` reading). Because M8 owns no cache, present-tense correctness is free.

5. **Supersession slot directionality.** ASN-0125 Df-DIR reads `F = new`; M7's actual storage (per the seam) is **flipped: `F = old/superseded`, `G = new/superseding`.** M8 follows M7's storage — `in(y)` probes FROM, `out(x)` probes TO, contextual projects FROM for `listed(old)` / TO for `listed(new)`. Noted divergence from the source text.

6. **RETRIEVEENDSETS whole-endset vs. touching-spans (ASN-0131 OQ1).** Resolved to **whole-endset** (return `readlink`'s full value), preserving union-distributivity (RE-UDIST) at the cost of one `readlink` per candidate.

7. **Home/residence filter placement (ASN-0121).** M8 owns no index dimension, so home is a **post-filter** via M1 `document_of` (lazy during a window walk). A home-only query degrading to a full active scan is accepted.

## Open build decisions

- **The arity-> 3 disjunction (genuine seam gap).** `findlinks_v`/RETRIEVEENDSETS union slots `{FROM, TO, TYPE}`; a fully faithful ASN-0127 disjunction folds in *every* slot of a higher-arity link, which M7's per-slot `stab` cannot serve without an exposed max-arity or a `stab_any`. **Pick `{1,2,3}` for v1** (arity-3 links); if arity-> 4 links with content-reaching extra slots ship, negotiate the M7 extension. This is the one place M8's fidelity depends on an M7 capability not in the current interface — flag it now.
- **Survival-check scope.** Per-document orphan set (the "breaks N links here" feature — cheap, recommended default) vs. also the **global-ghost** escalation (each orphan checked against every other document via M5's R-index — expensive, and it crosses into M6/provenance). Default per-document; expose global only if a caller needs LP17 ghost determination, and route it through M6.
- **Secondary enumeration key.** Address-only (default; free from M7's order) vs. also offering content-order (least-covered-tumbler) pagination at O(|Match|·log) per-window re-sort. Add the re-sort only if a reader needs content-ordered windows; never build a persistent key index (M8 owns none).
- **Count caching.** M8 recomputes (owns no state). Whether M10 wraps `count_ftt` with an epoch-tagged cache (CN-STAB: changes only on `K.λ`) and whether to special-case the all-wildcard count to `len()` of M7's active slice are M10/M7 choices, not M8's.
- **Cursor token shape.** Bare `Address` (sufficient — the key *is* the address) vs. a fattened opaque token. Default bare; fatten only to skip a (zero-cost here) key recompute, never to carry a server-side materialized list.
- **Region presentation.** `&[Span]` per single document (the contract here) vs. a multi-document SpecSet. Multi-document fan-out is a higher-layer composition, not M8's.
