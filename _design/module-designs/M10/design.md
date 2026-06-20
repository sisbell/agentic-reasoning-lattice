# M10 — Operation Surface (FEBE Command Layer)

## Purpose & boundary

M10 is the engine's front door. It turns each external FEBE request into exactly one call on the owning store/query module, gates the response on commit (A7), reports the linearization coordinate, and surfaces every failure as a *typed, classified, never-silent* rejection. **One thing well: the uniform request lifecycle — parse → authorize → linearize → commit-gate → marshal → surface — driven by a static dispatch table.**

It owns **no** per-store operation logic (that is M5/M6/M7/M8), **no** automation (M9 — a parallel surface, not below it), **no** ordering/durability/recovery (M2), and **no** journaled state. Its only authority is *ephemeral connection state* (which principal a session speaks for) plus best-effort retry de-duplication. The decomposition lists "cross-family composite orchestration" as a capability; this design resolves that **no v1 operation requires it** (see *Conflicts resolved*), so M10 v1 is, concretely, a lifecycle wrapper + dispatch table + client-model adapter.

## Public interface

M10 is **generic over `W`** and names no concrete `World`/`Record` (it follows M6/M8: a non-store consumer below the engine in the crate graph). The transport (binary) drives it.

```rust
// W must support every store M10 dispatches into. ContentWrite/Val/HasContent are M4 types named
// only to satisfy Vstream::insert's public bound (see Conflicts resolved).
pub struct Operation<W: WorldState> { /* private */ }

impl<W> Operation<W>
where
    W: WorldState + HasM3 + HasM5 + HasLinks + HasContent,
    W::Record: From<M3Rec> + From<M5Rec> + From<LinkRec> + From<ContentWrite>,
{
    /// Hold the recovered kernel + M7's genesis-immutable registry. The binary calls Kernel::open
    /// (M2 recovery) first and handles OpenError::{Corruption,BadCheckpoint} before constructing us.
    pub fn new(kernel: Arc<Kernel<W>>, registry: Arc<TypeRegistry>) -> Self;

    // ── session binding (M10-owned, ephemeral) ──
    pub fn open_session(&self, principal: PrincipalId) -> SessionId;
    pub fn close_session(&self, s: SessionId);
    pub fn bootstrap_session(&self) -> SessionId;          // bound to BOOTSTRAP_PRINCIPAL

    /// THE lifecycle entry. Total: always yields a Response to send (rejections are a Response
    /// variant). Reentrant & Sync — the transport may call it concurrently for pipelined requests.
    pub fn execute(&self, s: SessionId, req: Request) -> Response;

    pub fn log_position(&self) -> Seq;                     // bare "where is the log?" (M2::current_seq)
}
```

```rust
pub struct Request { pub id: Option<ReqId>, pub op: Op }   // id = client idempotency key (optional)
#[derive(Clone, Copy, PartialEq, Eq, Hash)] pub struct SessionId(u64);
#[derive(Clone, PartialEq, Eq, Hash)]       pub struct ReqId(pub Vec<u8>);  // client-unique
```

**The parsed request `Op`** — one variant per FEBE operation (args in M1/M5/M7/M8 types; principal comes from the session, never the wire):

```rust
pub enum Op {
    // ── namespace writes (→ M3) ──
    CreateNewDocument { account: Address },
    Delegate { new_prefix: Tumbler, new_id: PrincipalId },
    RegisterNode { addr: Tumbler },
    Fork,
    // ── arrangement writes (→ M5) ──
    Insert    { doc: Address, at: VPos, values: Vec<Val> },     // Val via M5 re-export
    Delete    { doc: Address, p: VPos, width: Nat },
    Copy      { doc: Address, at: VPos, specs: Vec<VSpec> },
    Rearrange { doc: Address, cuts: Vec<VPos> },
    Version   { d_src: Address },
    // ── link writes (→ M7) ──
    MakeLink  { home: Address, from: Vec<VSpec>, to: Vec<VSpec>, ty: Vec<VSpec> },
    Emit      { home: Address, ty: Endset, from: Address, to: Vec<Address> },
    Nullify   { home: Address, target: Address },
    AssertSup { home: Address, old: Address, new: Address },
    EditLink  { original: Address, successor: SuccessorSpec, d_s: Address, d_a: Address },
    // ── content/provenance reads (→ M6) ──
    ReadLink { a: Address }, FollowLink { a: Address, slot: usize },          // (→ M7 reads)
    RetrieveV { specs: Vec<Spec> }, RetrieveDocVSpan { doc: Address },
    RetrieveDocVSpanSet { doc: Address }, ShowOrigin { doc: Address, span: Span },
    ShowDeletions { d_a: Address, d_b: Address },
    Compare { rho1: Vec<Region>, rho2: Vec<Region> },
    FindDocsContaining { regions: Vec<Region> },
    // ── link discovery reads (→ M8) ──
    Image { d: Address, region: Vec<Span> },
    FindLinksV { d: Address, region: Vec<Span> }, FindLinksFtt { q: FourSet },
    CountV { d: Address, region: Vec<Span> },     CountFtt { q: FourSet },
    WindowV { d: Address, region: Vec<Span>, cur: Cursor, n: usize },
    WindowFtt { q: FourSet, cur: Cursor, n: usize },
    RetrieveEndsets { d: Address, region: Vec<Span> },
    Project { a: Address, slot: usize, d: Address }, DiscoverableFrom { a: Address, d: Address },
    DeleteOrphans { d: Address, p: VPos, width: Nat },
    InClaims { y: Address, view: View }, OutClaims { x: Address, view: View },
}

/// EditLink's successor is assembled by M10 from content V-specs (see Internal design).
pub struct SuccessorSpec { pub from: Vec<VSpec>, pub to: Vec<VSpec>, pub ty: TypeArg }
pub enum TypeArg { Addrs(Vec<Address>), Resolve(Vec<VSpec>) }   // type slot: address-set or content-resolved
```

**The marshaled `Response`** (consolidated by shape; every write carries the committed `Seq`, every read the snapshot `Seq`):

```rust
pub enum Response {
    Ack       { at: Seq },                                  // delete/copy/rearrange
    AckAddr   { addr: Address, at: Seq },                   // create/insert/version/makelink/emit/nullify/sup/fork/delegate/node
    AckEdit   { successor: Address, claim: Address, at: Seq },
    Delivery  { items: Delivery, as_of: Seq },
    SpanSet   { set: SpanSet, as_of: Seq },                 // vspan/vspanset/project
    Addrs     { addrs: Vec<Address>, as_of: Seq },          // origins/docs-containing/findlinks
    Count     { n: usize, as_of: Seq },
    Page      { window: Window, as_of: Seq },
    Endsets   { pairs: Vec<(usize, Endset)>, as_of: Seq },
    Runs      { runs: Vec<Run>, as_of: Seq },
    Bool      { val: bool, as_of: Seq },
    LinkValue { link: Option<Link>, as_of: Seq },
    Follow    { result: Result<SpanSet, Invalid>, as_of: Seq },
    Deletions { rep: Deletions, as_of: Seq },
    Compare   { rep: CompareReport, as_of: Seq },
    Orphans   { report: OrphanReport, as_of: Seq },
    Claims    { claims: Vec<SupClaim>, as_of: Seq },
    Rejected(Rejection),
}
```

**Typed rejection** (the never-silent contract; `disposition` is an advisory hint, `code` is authoritative):

```rust
pub struct Rejection { pub op: OpKind, pub code: RejectCode, pub disposition: Disposition, pub detail: Option<String> }
pub enum Disposition { Permanent, Reorder, Retry, Halt }   // hint: client may reissue under Reorder/Retry
pub enum RejectCode { /* deduped union of every store error variant + Unauthenticated + Durability + Poisoned + Malformed */ }
```

**The wire codec is a seam, not decided here** (no source note fixes the FEBE byte format):

```rust
pub trait Codec {                                          // builder supplies one concrete impl
    fn parse(&self, frame: &[u8]) -> Result<Request, ParseError>;   // wire → Op (+ id)
    fn marshal(&self, resp: &Response) -> Vec<u8>;
}
pub struct ParseError { /* unknown op / bad arg encoding — surfaced as RejectCode::Malformed, Permanent */ }
```

## Core data model

M10 owns **no authoritative substrate state and no `im` structure** — it takes no snapshots of itself and journals nothing, so structural sharing buys it nothing. Its fields are the cheapest thing that meets the contract:

| Field | Kind | Recovery on M10 restart |
|---|---|---|
| `kernel: Arc<Kernel<W>>` | borrowed authority (M2 owns real state) | n/a |
| `registry: Arc<TypeRegistry>` | borrowed (M7 genesis-immutable) | n/a |
| `sessions: Mutex<HashMap<SessionId, PrincipalId>>` | **ephemeral authoritative** connection state | lost — clients re-authenticate |
| `idem: Mutex<LruCache<ReqId, Response>>` | **hint** (best-effort retry memo) | lost — a post-restart retry re-executes (duplicate, by design — ASN-0134 §A7) |
| `poisoned: AtomicBool` | **hint** (recomputable by attempting `transact`) | re-derived on first `TxnError::Poisoned` |

The dispatch table is a `match`, not data. Plain `Mutex<HashMap>`/`LruCache` (or a sharded map) — **not `im`** — because no field is ever snapshotted or replayed; the system-wide "persistent collection" discipline is for journaled slices, which M10 has none of. This is the one module that legitimately departs from the `im`-everywhere convention, and saying so is the point.

## Internal design

### 1. Dispatch & the lifecycle entry

`execute` is the whole module on the hot path:

```rust
pub fn execute(&self, s: SessionId, req: Request) -> Response {
    // (a) idempotency: a repeated client key returns the cached response, never re-executing.
    if let Some(id) = &req.id { if let Some(r) = self.idem_get(id) { return r; } }
    // (b) session: a write needs a bound principal; reads tolerate an unbound session.
    let ctx = match self.sessions.lock().get(&s) {
        Some(p) => SessionCtx { sid: s, principal: *p },
        None if req.op.is_read() => SessionCtx::anon(s),
        None => return reject(req.op.kind(), RejectCode::Unauthenticated, Disposition::Permanent),
    };
    // (c) poisoned fast-path: refuse writes, keep serving reads (M2 snapshots survive poisoning).
    if self.poisoned.load() && req.op.is_write() {
        return reject(req.op.kind(), RejectCode::Poisoned, Disposition::Halt);
    }
    let resp = self.dispatch(&ctx, req.op).unwrap_or_else(Response::Rejected);
    if let Some(id) = req.id { self.idem_put(id, resp.clone()); }     // (d) cache after the fact
    resp
}
```

`dispatch(&self, &SessionCtx, Op) -> Result<Response, Rejection>` is the static table; every arm is one of four shapes below. There is **no fallthrough that turns an error into a success** — the `never-silent` invariant is enforced by exhaustiveness.

### 2. The read path — M10 owns the snapshot

Every read op takes **one** snapshot in M10 and reads through the *snapshot-based* surfaces (`Query::new(&snap)` for M6; M8's pure `*_on(&snap, …)` twins, **not** the self-snapshotting handle methods). Two reasons: M10 reports the exact `as_of = snap.seq()` (V1 retrospective), and any read whose verdict spans several constituents reads them all off one root — discharging MIC clause 6 *by construction* (ASN-0134 §V2/§clause 6).

```rust
Op::RetrieveV { specs } => {
    let snap = self.kernel.snapshot();                       // ONE pinned committed state
    let d = Query::new(&snap).retrieve_v(&specs).map_err(|e| map_read(OpKind::RetrieveV, e))?;
    Ok(Response::Delivery { items: d, as_of: snap.seq() })
}
Op::CountV { d, region } => {
    let snap = self.kernel.snapshot();
    let n = count_v_on(&snap, &d, &region).map_err(|e| map_read(OpKind::CountV, e))?;
    Ok(Response::Count { n, as_of: snap.seq() })
}
```

Reads hold no lock against writers (M2 snapshot is a pinned `Arc` root), are zero-step (A1), and have **no** commit-before-ack obligation. Common case: one `snapshot()` + pure compute + marshal.

### 3. The write path — commit-before-ack falls out of the call order

A write arm calls the owning store's transact-driving op and returns only its post-commit value. **A7 is upheld structurally**: the only thing M10 can put on the wire is the driver's return, and the driver returns at/after `lin(op)` (M2 installs and — under `Fsync` — fsyncs before `transact` returns). M10 cannot respond early because it has nothing to respond with until then. (This is exactly where the udanax reference failed — response-before-check; M10 makes that unrepresentable.)

```rust
Op::Insert { doc, at, values } => {
    let (start, at_seq) = Vstream::new(&self.kernel).insert(&doc, at, values)
        .map_err(|e| map_txn(OpKind::Insert, e))?;          // returns post-commit
    Ok(Response::AckAddr { addr: start, at: at_seq })        // committed_at = the exact V1 coordinate
}
Op::Version { d_src } => {
    let (addr, seq) = Vstream::new(&self.kernel).version(ctx.principal, &d_src)
        .map_err(|e| map_txn(OpKind::Version, e))?;          // M5 does the owned/cross-owner branch
    Ok(Response::AckAddr { addr, at: seq })
}
Op::MakeLink { home, from, to, ty } => {
    let (addr, seq) = LinkStore::new(&self.kernel, self.registry.clone())
        .makelink(&home, from, to, ty).map_err(|e| map_txn(OpKind::MakeLink, e))?;
    Ok(Response::AckAddr { addr, at: seq })                  // M7 resolves V-specs INSIDE its transact
}
```

**Idempotent zero-step ops need no special case**: `emit`/`nullify` on a dedup hit return `(incumbent, base_seq)` with no commit; M10 marshals them identically to a miss (`AckAddr`). The client cannot — and need not — distinguish (ASN-0134 §A1). **Linearization-entry invariant: one operation ⇒ at most one M2 transaction.** The one shape M10 must *never* collapse is a multi-step batch (`retract_stale`, dormant in v1): M2's boundary forbids fusing a witnessed batch into one transact (it would suppress intended partial visibility, A5). If M10 ever exposes a batch op it surfaces it as the sequence it is.

### 4. EditLink — the one read-assembled request

`editlink` is the only op where M10 itself reads another family to *build an argument*. M7 takes a pre-formed `Link`; M10 resolves the content V-specs through M5 to construct it. The resolve is a **zero-step read off a prior snapshot**, deliberately *not* in editlink's write transaction — recorded I-addresses are permanent (the link names permascroll I-positions, not V-positions), so `d_s`'s arrangement may move underneath with no hazard (M7 blesses "off any prior snapshot"). So the *operation* still maps to one M2 write; the assembling read is zero-step.

```rust
Op::EditLink { original, successor, d_s, d_a } => {
    let snap = self.kernel.snapshot();                       // prior snapshot — safe, I-addrs permanent
    let m5 = snap.world().m5();
    let from = endset_from_vspecs(m5, &successor.from)?;     // M5 resolve → Run::iextent → Endset::from_spans
    let to   = endset_from_vspecs(m5, &successor.to)?;
    let ty   = match &successor.ty {                         // TYPE slot: addresses or content-resolved
        TypeArg::Addrs(a) => enc(a),
        TypeArg::Resolve(v) => endset_from_vspecs(m5, v)?,
    };
    let link = Link::new([from, to, ty]).ok_or_else(|| reject1(OpKind::EditLink, RejectCode::IllFormedSpec))?;
    let (succ, claim, seq) = LinkStore::new(&self.kernel, self.registry.clone())
        .editlink(&original, link, &d_s, &d_a).map_err(|e| map_txn(OpKind::EditLink, e))?;
    Ok(Response::AckEdit { successor: succ, claim, at: seq })
}
```

This is *request marshaling that reads*, not a cross-family atomic composite (no atomicity spans the read and the write). The asymmetry with `makelink` — which keeps its V→I resolve *inside* M7's transact — is dictated by the upstream signatures (`makelink` builds links over *new* references at creation time; `editlink`'s successor is built from *existing recorded* I-addresses). M10 honors both as given.

### 5. Rejection surfacing & the disposition hint

Two converters map every upstream failure to a `Rejection`; neither ever returns `Ok`:

```rust
fn map_txn<E: Into<RejectCode>>(op: OpKind, e: TxnError<E>) -> Rejection { match e {
    TxnError::Rejected(inner) => Rejection::classified(op, inner.into()),     // typed precondition
    TxnError::Durability(_)   => Rejection { op, code: Durability, disposition: Retry,  detail: None },
    TxnError::Poisoned        => { /* set self.poisoned */ Rejection { op, code: Poisoned, disposition: Halt, .. } }
}}
fn map_read<E: Into<RejectCode>>(op: OpKind, e: E) -> Rejection { Rejection::classified(op, e.into()) }
```

`RejectCode` is the **deduped union of every store error variant** (`HomeNotRegistered`, `BadTarget`, `MalformedSpec(SpecFault)`, …) plus M10's own `Unauthenticated`, `Malformed` (codec), `Durability`, `Poisoned`. The `From<E>` impls are mechanical, one per store error enum. M10's *design content* here is the **disposition policy** — an advisory Lampson hint (recomputable, the client's `code` is the truth):

| Disposition | When | Examples |
|---|---|---|
| **Permanent** | reissuing identically cannot succeed | `Malformed`, `MalformedSpec/Span`, `BadRegion`, `BadPosition`, `BadCutCount`, `NotAscending`, `Empty*`, `NotOwner`, `NotAuthorized`, `SelfSupersession`, `NodeTierCrossOwner`, `DcViolation`, `Unauthenticated` |
| **Reorder** | a *future* committed state may satisfy the precondition (the ASN-0134 out-of-order case) | `BadTarget` (target not yet present), `DocNotRegistered`, `HomeNotRegistered`, `SourceNotRegistered`, `OriginalNotResident`, `EndpointNotResident`, `NotFresh`, `ParentNotRegistered`, `NotRegistered`(type) |
| **Retry** | transient, true no-op | `Durability` (barrier failed before install; M2 truncated the tail — safe to re-invoke) |
| **Halt** | kernel stopped | `Poisoned` |

This is the surfaced-typed-re-orderable contract (ASN-0134 rejection path): the canonical out-of-order retraction — `nullify` whose target isn't present — returns `Rejection { code: BadTarget, disposition: Reorder }`, so a coordination layer or client can reissue once the target exists. M10 **surfaces, it does not reorder** — buffering/reordering is policy that belongs above M10. Ambiguous codes (`DocNotRegistered` could be a typo *or* an out-of-order create) are classed optimistically as `Reorder`; the hint is advisory and the `code` lets the client decide.

### 6. Session binding & authorization pass-through

M10 owns the *policy* "which principal does this connection speak for" (`sessions` map); M3 owns the *mechanism* "is this principal the effective owner" (the atomic `ω` check inside `create_new_document`/`version`/`fork`/`delegate`). M10 passes `ctx.principal` down and **never duplicates the `ω` check** — duplicating it would race against the committed state M3 checks atomically. The only pre-check M10 does is "is there a principal at all" (`Unauthenticated`), which avoids opening a doomed transaction. The authentication *mechanism* that yields a `PrincipalId` for a connection is the transport's seam (not specified in the corpus); M10 records the result. The bootstrap session is bound to `BOOTSTRAP_PRINCIPAL` so the first `delegate`/`create` can happen.

### 7. Idempotency cache

Per M3's boundary ("exactly-once/idempotency for retried `create_new_document` are M10's"), M10 memoizes `ReqId → Response`. A retried request with the same client key returns the cached response without re-executing — defeating the lost-acknowledgment duplicate that A7 explicitly does *not* prevent (ASN-0134 §A7/§SAFE(b)(iii)). Scope: keyed by client-supplied `ReqId` (the client guarantees uniqueness); LRU/TTL eviction. **It is a hint, not a guarantee**: in-memory, so a retry *after an M10 restart* re-executes (a duplicate INSERT / `idem=⊥` emit) — which is exactly ASN-0134's "by design, needs a client key, not a substrate clause." Journaling the cache for cross-restart exactly-once is an open decision (§ Open build decisions).

### 8. Client model — pipelining vs sequential

`execute` is `&self` and reentrant (no nested `transact`; the session/idem maps are independently locked), so the transport may have many in-flight calls on one connection. M10 echoes `req.id` into the response, letting the client match out-of-order completions. The contract M10 presents (ASN-0134 §G0):

- **Commit-before-acknowledge** per op (§3) — always.
- **Serializability**, not sequential consistency. M10 makes *no* cross-op program-order promise; a single client's ops into distinct homes are `≺`-incomparable and M2 may commit them in either order (H1/G1 — benign for distinct homes; the third-party-observer window of G0 is real and unhidden).
- **A sequential client recovers SC** by its own ack-before-next discipline — and gets **read-your-writes for free**: a write's ack is post-commit at `Seq S`, and `current_seq()` never regresses, so any later `snapshot()` is `≥ S`. M10 supplies the building block (`committed_at`/`as_of` on every response) and otherwise stays out of the way.

The *concurrency policy* — sequential dispatch vs bounded/unbounded pipeline, threadpool vs async — lives in the transport and is an open decision; M10 supports any of them because `execute` is thread-safe and stateless-per-call.

### 9. Poisoned-halt & startup

M10 has no journaled state, so it has nothing to recover. The binary calls `Kernel::open` (M2 replays the world) and handles `OpenError::{Corruption, BadCheckpoint}` (operator intervention, not auto-retry) *before* constructing `Operation`. At runtime, the first `TxnError::Poisoned` sets `self.poisoned`; thereafter writes fail fast with `Disposition::Halt` while **reads keep being served** (M2 snapshots survive a poisoned kernel) — a clean degraded mode until an operator restarts.

### 10. Cross-family composite orchestration (latent)

M10 retains direct `kernel.transact` access as the home for an operation whose atomic effect spans ≥2 store *families* and that no single store owns. The closure would call several stores' **pure** step functions and `stg.push(rec.into())` each, committing as one transaction — e.g. a hypothetical "create-document-and-insert-atomically" (so a reader never witnesses a registered-empty doc):

```rust
// HYPOTHETICAL — no v1 op needs this. Requires M3+M5 to publish pure stage_* steps first.
self.kernel.transact(&[M3State::document_lock_key(acct), M3State::content_lock_key(&d)], |stg| {
    let (d, ns_rec) = stg.working().m3().mint_document(acct)?;  stg.push(ns_rec.into());
    /* … M5::stage_register + M5::stage_content_place over stg.working() … */  Ok(d)
})
```

**In v1 this path has zero occupants** (see *Conflicts resolved*), and the pure-step surfaces it would need (a pure M5 insert step) are deliberately *not* published, because nothing requires them. The trigger to populate it is the three-part criterion in *Conflicts resolved*.

## Invariants & contracts

**By construction**
- **Commit-before-acknowledge (A7, ASN-0134).** M10's wire response is the store driver's post-commit return value; there is nothing to send earlier. Reads are zero-step and exempt.
- **One operation → one linearization point (A1/A2, ASN-0134).** Each write op = one store `transact` = one `Seq` (reported as `committed_at`); each read = one snapshot (reported as `as_of`).
- **Snapshot-consistent reads / clause-6 by construction (A3/V2, ASN-0134).** M10 takes one snapshot per read op and reads every constituent off it via the snapshot-based surfaces.
- **No journaled state ⇒ no recovery hazard.** M10 contributes no slice/record; the engine-composition contract is satisfied trivially (it names no `World`/`Record`).
- **Read-your-writes for a sequential client (G0, ASN-0134).** Falls out of post-commit acks + non-regressing `current_seq`.

**By active enforcement**
- **Never a silent skip (ASN-0134 rejection path).** `map_txn`/`map_read` are total; `dispatch` is exhaustive with no error-swallowing fallthrough — *enforced at every dispatch arm*.
- **Typed, classified rejections (ASN-0134, OQ8).** `Rejection` carries the upstream `code` verbatim plus a disposition hint — *enforced in the two converters*.
- **Session-principal binding & write authorization gate.** A write on an unbound session is rejected `Unauthenticated` before any transaction — *enforced in `execute` step (b)*; fine-grained `ω` is M3's atomic check, passed through.
- **Best-effort exactly-once for retried writes (M3 boundary; ASN-0134 §A7).** The idempotency cache short-circuits a repeated `ReqId` — *enforced in `execute` steps (a)/(d)*.
- **Poisoned halt (M2 `TxnError::Poisoned`).** First poison latches `self.poisoned`; subsequent writes fail fast, reads continue — *enforced in `execute` step (c)*.
- **No batch fusion (A5, M2 boundary).** A multi-step batch is surfaced as a sequence, never collapsed into one `transact`.

## Dependencies & seams

**Upstream calls (as given — not redesigned):**
- **M2** — `kernel.snapshot()` (every read; owns `as_of`); `kernel.current_seq()` (`log_position`); `kernel.transact` directly *only* for the latent composite (none in v1). Consumes `TxnError::{Rejected,Durability,Poisoned}`. The binary, not M10, calls `Kernel::open` and handles `OpenError`.
- **M3** — `Namespace::{create_new_document, delegate, register_node, fork}`; passes `ctx.principal` as caller/delegator. (M5/M7 do their own M3 mints internally.)
- **M5** — `Vstream::{insert, delete, copy, rearrange, version}`; for `editlink`, `M5State::resolve` + `Run::iextent` off a snapshot to assemble the successor. Names M4's `Val`/`ContentWrite`/`HasContent` only to satisfy `insert`'s public bound (see below).
- **M6** — `Query::{retrieve_v, doc_vspan, doc_vspanset, show_origin_v, show_deletions, compare, find_docs_containing}` over M10's snapshot; `VPos` named via M6's re-export.
- **M7** — `LinkStore::{makelink, emit, nullify, assert_sup, editlink}`; `LinkState::{readlink, followlink}`; `Endset`/`enc`/`Link::new`/`View`/`TypeRegistry` for arg construction.
- **M8** — the `*_on(&snap, …)` pure twins for all discovery/window/projection/orphan/lineage reads (so M10 owns the snapshot and reports `as_of`).
- **M1** — `Address/Tumbler/Span/SpanSet/Nat` for parsing/marshaling.
- **Not M4 directly** (only M4 *type names*, via M5 re-export — below). **Not M9** (parallel).

**Downstream seam — the external FEBE client (the only consumer of M10):**
The contract neighbors (the transport in the binary) build against is `Operation<W>::execute(SessionId, Request) -> Response` plus a `Codec`. Guarantees the client may rely on: commit-before-acknowledge; `committed_at`/`as_of` on every response; typed `Rejection` with an advisory `disposition`; idempotency-key honoring within M10's uptime; session→principal binding. The transport supplies: a concrete `Codec`, the connection→`PrincipalId` authentication, and the concurrency policy (sequential vs pipelined). **M10 ⟂ M9:** M9's rule fires reach M7's gated write path directly; M10 never sees them except as committed state in later snapshots — no edge, no shared lifecycle.

## Conflicts resolved

1. **Cross-family composite ownership (decomposition Open Q a).** *Resolved: M10 orchestrates zero cross-family write composites in v1.* The decomposition deliberately pushed each operation's cross-module reach *down* into the store that owns its semantics — M5 owns INSERT/COPY/VERSION (reaching M3+M4 in one `transact`), M7 owns MAKELINK/editlink (reaching M3+M5). An op qualifies for M10 only if **(i)** its atomic effect spans ≥2 store *families*, **(ii)** no single store owns its semantics, **and (iii)** the spanning effect needs atomicity. No v1 op meets all three (editlink's M5 resolve fails (iii) — I-addresses are permanent). So the capability is latent; building it later also requires the owning stores to first publish pure `stage_*` steps (the composition contract), which they deliberately don't in v1 because nothing needs them. This is the honest call, and it keeps M10 thin.

2. **M9/M10 relationship (decomposition Open Q b).** *Resolved: parallel, not stacked.* M9's fires are internal automation — no parse, auth, marshal, idempotency, or wire response — so routing them through M10's lifecycle would add a useless hop and a false coupling. They go straight to M7's gated write path; M10 and M9 share only the substrate.

3. **ASN-0134 re-homing (A7).** *Resolved: M2 keeps the commit-gate mechanism (`transact` returns post-commit); M10 keeps the request/response path and the client model.* M10 does not re-implement the gate — it *leverages* it (§3), which is why the udanax response-before-check defect is unrepresentable here rather than merely discouraged.

4. **M4 types leak through M5's public `insert` signature.** The DAG omits `M10 → M4`, yet `Vstream::insert` exposes `Vec<Val>` and a `W::Record: From<ContentWrite>` / `W: HasContent` bound that M10 must name to call it. *Resolved, preferred:* M5 re-exports `Val`, `ContentWrite`, `ContentError`, `HasContent` (the M6/`VPos` precedent), so M10 names them via M5 and the DAG holds. *Fallback:* a **type/trait-only** `M10 → M4` edge — benign (still acyclic, carries no logic). This is flagged as an assumption on M5's surface.

5. **Reader snapshot ownership.** M8 offers self-snapshotting handle methods *and* pure `*_on` twins; M6 offers `Query::new(&snap)`. *Resolved: M10 always owns the snapshot* (takes it, passes to the snapshot-based surfaces), so it can report the exact `as_of` and discharge clause 6 for any future multi-constituent read — it never uses M8's self-snapshotting handles.

## Open build decisions

1. **FEBE wire codec** — the concrete byte format (`Codec::parse`/`marshal`) is fixed by no source note; pick it when you build the transport. The typed `Op`/`Response`/`Rejection` above are the codec's target.
2. **Transport & concurrency policy** — TCP/IPC/framing, and sequential vs bounded-pipeline vs unbounded, threadpool vs async. M10 supports all (reentrant `execute`); M2's v1 single applier serializes writes regardless, so unbounded pipelining buys read concurrency only.
3. **Idempotency durability** — in-memory LRU (v1, best-effort within uptime) vs a journaled key→`Seq` record for cross-restart exactly-once (heavier; would make the cache authoritative). Also: cache scope (per-session vs global) and eviction (LRU/TTL).
4. **Snapshot-pinned read sessions** — v1 reads are present-tense, each a fresh snapshot (pagination tolerates this — cursors survive across snapshots). Add an explicit "pin a snapshot for this session's reads" only if a client needs strict repeatable-read across multiple FEBE requests.
5. **Out-of-order policy** — v1 *surfaces* `Reorder` rejections and stops. Whether to add an M10-side reorder/retry buffer (vs leaving it to the client/coordination layer) is a policy choice deliberately left out of the mechanism.
6. **`RejectCode` shape** — a flat deduped enum (ergonomic Rust client) vs a `(category, store_code)` pair (smaller, more stable across store-error churn). The disposition policy table is the same either way.
7. **Disposition refinement** — the `Reorder`/`Permanent` split for ambiguous codes (`DocNotRegistered`) is a heuristic hint; tune it (or expose both the raw code and let the client decide entirely) under real client traffic.
