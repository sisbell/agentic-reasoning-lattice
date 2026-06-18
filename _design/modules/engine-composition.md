# Engine Composition Contract

How a store module plugs into the assembled engine. This is a **cross-cutting
invariant**, not a per-note contract: every store that contributes state to M2's
`WorldState` realizes the *same* seam, so the engine crate can assemble one
concrete world from all of them **without a dependency cycle**. M3 established
this pattern; every store module (M3–M9, and any store-like slice of M10) MUST
follow it identically. A module that names the concrete `World`/`Record` is
**wrong** — it would force the store crate to depend on the engine crate that
already depends on it.

## The model

- **M2 (`skep-kernel`) is generic** over an engine-supplied `W: WorldState`. It
  knows no store; it calls *down* through `WorldState::apply` and serializes on
  opaque `LockKey` bytes.
- **Each store crate is generic** and self-contained: it owns a *slice* type, a
  *record* type, an *accessor trait*, and a *fold*. It never names the concrete
  world or the central record enum.
- **The engine crate (`skep-engine`) is the single assembler**: it defines the
  one concrete `World` (all slices) and the one central `Record` enum (all
  variants), implements `WorldState` for `World` (dispatching `apply`), and
  implements every store's accessor trait + record-lift for `World`/`Record`.
  **Nothing depends on the engine crate except the binary.**

## What every store crate provides

For a store `X` (e.g. `Namespace`, `ContentStore`):

1. **A slice type** `XState` — its authoritative folded state (`im::…` for cheap
   structural-sharing snapshots). `Clone + Serialize + Deserialize`.
2. **A record type** `XRec` — its own journal-delta enum, the *only* authoritative
   deltas it owns. `Clone + Serialize + Deserialize`. **Not** the central `Record`.
3. **A read-accessor trait** `HasX { fn x(&self) -> &XState; }` — the engine
   implements it for `World`. This is how the store reaches its slice off a
   `&W` (M2's "read your store's slice off this").
4. **A fold** `fn apply_x(&self, r: &XRec) -> XState` — pure, total, deterministic
   (M2's `apply` obligation). The engine's `World::apply` dispatches the `Record::X`
   variant here.
5. **Its two composable forms** (M2 contract 3), both generic over `W`:
   - **pure step** — `fn stage_x(&XState, …) -> Result<XRec, XError>` (read off
     `base()`/`working()` via `HasX::x()`); returns **`XRec`**, commits nothing.
   - **standalone op** — `fn op<W: WorldState + HasX>(k: &Kernel<W>, …) -> Result<(…, Seq), TxnError<XError>>`
     where `W::Record: From<XRec>`, staging via `stg.push(rec.into())`.

## The hard rules

- **Be generic over `W`.** Transact-driving ops are `impl<W: WorldState + HasX [+ HasY …]> Store<W> where W::Record: From<XRec> [+ From<YRec> …]`. A store **never** names the concrete `World`.
- **Return your own `XRec`, never the central `Record`.** The *caller* lifts with
  `.into()` (the `From<XRec>` bound). A `stage_*` that returns `Record` couples the
  store to the engine — the cycle.
- **Reach slices through accessor traits**, never field access on a concrete world:
  `stg.working().x()`, `stg.base().y()`, `snapshot.world().x()`.
- **Cross-store reads compose by trait bounds.** A store that reads an upstream
  store's slice in a closure adds that store's accessor to its bound
  (`W: … + HasNamespace + HasContent`) and calls the upstream's **pure** function —
  never a nested `transact`, never the concrete type.
- **Shared low-level types live below every store.** The central `LockKey`
  **space-tag enum** (M2's 1-byte cross-store tag) and any type every store must
  name live in `skep-kernel` (or a shared base crate) — **never** in the engine
  assembly crate — so a generic store can reference its tag without depending on
  the assembler. (Each store is assigned one tag; tags are unique by living in the
  one enum.)

## The engine crate assembles

```rust
pub struct World { ns: NamespaceState, content: ContentStore, /* … one slice per store … */ }
pub enum   Record { Ns(NsRec), Content(ContentWrite), /* … one variant per store … */ }

impl WorldState for World {
    type Record = Record;
    fn apply(&self, r: &Record) -> World { match r {
        Record::Ns(x)      => World { ns:      self.ns.apply_ns(x),      ..self.clone() },
        Record::Content(x) => World { content: self.content.apply_write(x), ..self.clone() },
        /* … */
    }}
}
impl HasNamespace for World { fn ns(&self) -> &NamespaceState { &self.ns } }
impl HasContent   for World { fn content(&self) -> &ContentStore { &self.content } }
impl From<NsRec>       for Record { fn from(r: NsRec)       -> Record { Record::Ns(r) } }
impl From<ContentWrite> for Record { fn from(r: ContentWrite) -> Record { Record::Content(r) } }
```

## Crate-graph consequence (acyclic by construction)

```
skep-kernel (M2, + the central Space tag enum)   ← every store; no store deps
skep-address (M1)                                 ← every store; no deps
skep-<store>  → skep-address, skep-kernel, + its UPSTREAM store crates (pure surfaces)
skep-engine   → ALL store crates                  (the only assembler; nothing depends on it)
binary        → skep-engine
```

Because no store names `World`/`Record`, no store edge points at the engine, so
the graph is a DAG mirroring `modules.yaml` — and Rust's crate system *enforces*
it (a violation is a compile-time cycle, not a review finding).

## Reviewer checklist (apply to every store module)

- [ ] Slice, record, accessor trait, and fold are all present and named per the pattern.
- [ ] Transact-driving ops are **generic over `W`** with `HasX` bounds and `W::Record: From<XRec>`; **no** mention of a concrete `World`/`Record` type.
- [ ] `stage_*` returns the store's **own** `XRec`, not `Record`; the caller lifts via `.into()`.
- [ ] Slices reached via accessor traits (`world().x()`), never concrete-field access.
- [ ] Cross-store use is the upstream's **pure** function under an added `HasY` bound — never a nested `transact`, never the concrete type.
- [ ] The store's `LockKey` space tag is drawn from the shared central enum (below the store), not invented locally.
- [ ] Public record/value types are **constructible by upstream producers and readable by downstream consumers** (no private-field type that crosses a seam unusably).
