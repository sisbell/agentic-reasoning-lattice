# M10 — Interface (for dependents)

M10 owns the uniform FEBE request lifecycle — *parse → authorize → linearize → commit-gate → marshal → surface* — driven by a static dispatch table, plus ephemeral session→principal binding and best-effort retry de-duplication. It owns no per-store operation logic, no automation, no ordering/durability/recovery, and no journaled state.

## Public interface

M10 is **generic over `W`** and names no concrete `World`/`Record`. The only consumer is the transport (binary) that drives it.

```rust
pub trait Stores<W: WorldState>: Send + Sync {
    fn kernel(&self) -> &Kernel<W>;          // M2 — reads/snapshots/current_seq/latent transact
    fn namespace(&self) -> Namespace<W>;     // M3 driver — owns an Arc<Kernel<W>> clone (no borrow)
    fn vstream(&self) -> Vstream<'_, W>;     // M5 driver — borrows the held kernel for the call
    fn linkstore(&self) -> LinkStore<'_, W>; // M7 driver — borrows kernel, holds the registry
}
```

```rust
pub struct Operation<W: WorldState> { /* private */ }

impl<W> Operation<W>
where
    W: WorldState + HasM3 + HasM5 + HasLinks + HasContent,
    W::Record: From<M3Rec> + From<M5Rec> + From<LinkRec> + From<ContentWrite>,
{
    pub fn new(stores: Box<dyn Stores<W>>) -> Self;

    // ── session binding (M10-owned, ephemeral) ──
    pub fn open_session(&self, principal: PrincipalId) -> SessionId;
    pub fn close_session(&self, s: SessionId);
    pub fn bootstrap_session(&self) -> SessionId;          // bound to BOOTSTRAP_PRINCIPAL

    pub fn execute(&self, s: SessionId, req: Request) -> Response;

    pub fn log_position(&self) -> Seq;                     // bare "where is the log?" (stores.kernel().current_seq())
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
    // ── namespace reads (→ M3) ──
    NextAccountPrefix { parent: Address },   // M3's next-form delegable prefix — what Delegate demands
    PrincipalPrefix   { id: PrincipalId },   // any principal's (public, immutable) account Address — what CreateNewDocument demands
    // ── arrangement writes (→ M5) ──
    Insert    { doc: Address, at: VPos, values: Vec<Val> },     // Val from M4 (type-only M10→M4 edge)
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
    // ── raw link reads (→ M7) ──
    ReadLink { a: Address }, FollowLink { a: Address, slot: usize },
    // ── content/provenance reads (→ M6) ──
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

/// EditLink's successor is assembled by M10 from content V-specs.
pub struct SuccessorSpec { pub from: Vec<VSpec>, pub to: Vec<VSpec>, pub ty: TypeArg }
pub enum TypeArg { Addrs(Vec<Address>), Resolve(Vec<VSpec>) }   // type slot: address-set or content-resolved
```

**The marshaled `Response`** (every write carries the committed `Seq`, every read the snapshot `Seq`; `Response` derives **no** `Clone`):

```rust
pub enum Response {
    Ack       { at: Seq },                                  // delete/copy/rearrange
    AckAddr   { addr: Address, at: Seq },                   // create/insert/version/makelink/emit/nullify/sup/fork/delegate/node
    AckEdit   { successor: Address, claim: Address, at: Seq },
    Delivery  { items: Delivery, as_of: Seq },
    SpanSet   { set: SpanSet, as_of: Seq },                 // vspan/vspanset/project
    Addrs     { addrs: Vec<Address>, as_of: Seq },          // origins/docs-containing/findlinks
    MaybeAddr { addr: Option<Address>, as_of: Seq },        // next-account-prefix / principal-prefix (None = absent/ineligible)
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

**Typed rejection** (`code` is authoritative, `disposition` is an advisory hint, `site` localizes the fault, `detail` is an optional message):

```rust
pub struct Rejection {
    pub op: OpKind, pub code: RejectCode, pub disposition: Disposition,
    pub site: Option<FaultSite>, pub detail: Option<String>,
}
pub enum Disposition { Permanent, Reorder, Retry, Halt }   // hint: client may reissue under Reorder/Retry

pub struct FaultSite {
    pub operand: Option<Operand>, pub region: Option<usize>,
    pub index: Option<usize>, pub fault: Option<SpecFault>,
    pub addr: Option<Address>,   // offending document of RetrieveError/DeletionsError/CompareError/FindError::DocNotRegistered(Address)
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum OpKind { /* CreateNewDocument … OutClaims — one per Op — plus Unparseable */ }

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum RejectCode {
    // ── M10-originated ──
    Unauthenticated, Malformed, Durability, Poisoned,
    // ── registration / residence (M3/M5/M7/M8) ──
    HomeNotRegistered, DocNotRegistered, SourceNotRegistered, ParentNotRegistered,
    NotRegistered, OriginalNotResident, EndpointNotResident,
    // ── M3 namespace / authority ──
    NotOwner, NotAnAccount, Gate, DelegatorUnknown, DuplicateId, NotAncestor, NotAuthorized,
    NotAccountTier, NotTopDown, NotNextForm, NotValid, NotNode, NotDescendantOfBootstrap, NotFresh,
    // ── M5 arrangement ──
    BadPosition, EmptyContent, Content, EmptySource, BadSpan, DanglingSource, EmptyResult, NotArranged,
    OutOfBounds, EmptyWidth, BadCutCount, NotAscending, EmptyContentSubspace, NotAPrincipal,
    NodeTierCrossOwner, NotHomeLink, AlreadySeated, NotContentSubspace,
    // ── M7 link ──
    IllFormedSpec, EmptyTypeResolution, ShapeViolation, RetractionClass, NonAddressDenotingType,
    BadTarget, SelfSupersession, IllFormedSuccessor, DcViolation,
    // ── M6 content/provenance read (MalformedSpan also covers RetrieveError::MalformedSpec) ──
    NoSuchSubspace, EmptySubspace, DepthIncompatible, RangeNotPresent, MalformedSpan,
    // ── M8 link discovery read ──
    NotALink, BadRegion,
}
```

**The wire codec is a seam — the builder supplies one concrete impl:**

```rust
pub trait Codec {                                          // builder supplies one concrete impl
    fn parse(&self, frame: &[u8]) -> Result<Request, ParseError>;   // wire → Op (+ id)
    fn marshal(&self, resp: &Response) -> Vec<u8>;
}
pub struct ParseError { /* unknown op / bad arg encoding */ }
```

## Caller contracts & obligations

**`Operation::new(stores: Box<dyn Stores<W>>)`**
- Caller (binary) MUST call `Kernel::open` (M2 recovery) and handle `OpenError::{Corruption, BadCheckpoint}` *before* constructing.
- Caller MUST build and inject the `Stores<W>` factory (wrapping the recovered kernel + M7's genesis-immutable `Arc<TypeRegistry>`) before construction; M10 holds neither the kernel nor the registry directly.
- The `W` bounds (`HasM3 + HasM5 + HasLinks + HasContent`, `W::Record: From<…>`) must be satisfied by the caller's `World` type.

**`open_session(principal) -> SessionId`**
- Caller supplies the authenticated `PrincipalId` (the connection→`PrincipalId` authentication mechanism is the transport's, not M10's).
- Returns a fresh `SessionId`, unique within one M10 uptime (reset on restart — clients re-authenticate).

**`bootstrap_session() -> SessionId`**
- Returns a session bound to `BOOTSTRAP_PRINCIPAL`, so the first `delegate`/`create`/`register_node` can run; also the session under which `register_node` provisioning runs.

**`close_session(s)`**
- Drops the binding; the id is retired permanently and never reissued within the uptime.

**`execute(s, req) -> Response` — the lifecycle entry**
- **Total**: always yields a `Response` to send (a rejection is the `Rejected` variant); never panics. **Reentrant & `Sync`** — the transport may call it concurrently for pipelined requests.
- **Caller precondition (non-forgeability):** `s` MUST originate in the transport's connection state (injected from the connection's authenticated binding), **never** read off the wire. M10 cannot enforce this; the write-auth gate and the idempotency cache's cross-principal confinement are sound only under it.
- `req.id` is optional and used **only** as the per-session idempotency key; the client guarantees `ReqId` uniqueness within its session. The principal is taken from the session — never put it in `Op`.
- **Guarantees a caller may rely on:** commit-before-acknowledge per write op; `committed_at` (`at`) on every write / `as_of` on every read; typed `Rejection`, never a silent skip, for any failure of a *parsed* `Op`; read-your-writes for a sequential client (post-commit acks + non-regressing `current_seq`); serializability (not sequential consistency — no cross-op program-order promise; a sequential client recovers SC by its own ack-before-next discipline).
- **Error/absence cases:** write on an unbound session → `Rejected{code: Unauthenticated, disposition: Permanent}`; on a poisoned kernel, writes fail fast → `Rejected{code: Poisoned, disposition: Halt}` while reads keep being served; `MaybeAddr.addr == None` ⇒ absent/ineligible.
- The returned `Response` carries **no** `ReqId`; request↔response correlation is the caller's.
- Idempotency is a **hint**: a retry *after an M10 restart* re-executes (duplicate by design); *concurrent* same-`(SessionId, ReqId)` requests are not serialized; a `ReqId` reused across op-kinds misses and re-executes; rejections and reads are never memoized (a `Reorder`/`Retry` reissue always re-executes).

**`log_position() -> Seq`**
- Returns the current log position; `current_seq()` never regresses.

**Per-`Op` request→`Response` shape (what each call returns):**
- `Ack{at}` ⇐ `Delete`, `Copy`, `Rearrange`
- `AckAddr{addr,at}` ⇐ `CreateNewDocument`, `Insert` (start addr), `Version`, `MakeLink`, `Emit`, `Nullify`, `AssertSup`, `Fork`, `Delegate`, `RegisterNode`
- `AckEdit{successor,claim,at}` ⇐ `EditLink`
- `MaybeAddr{addr,as_of}` ⇐ `NextAccountPrefix`, `PrincipalPrefix` (`None` = absent/ineligible; no fault path)
- `Delivery` ⇐ `RetrieveV`; `SpanSet` ⇐ `RetrieveDocVSpan`, `RetrieveDocVSpanSet`, `Project`
- `Addrs` ⇐ `ShowOrigin`, `FindDocsContaining`, `FindLinksV`, `FindLinksFtt`
- `Count` ⇐ `CountV`, `CountFtt`; `Page` ⇐ `WindowV`, `WindowFtt`; `Endsets` ⇐ `RetrieveEndsets`; `Runs` ⇐ `Image`; `Bool` ⇐ `DiscoverableFrom`
- `LinkValue` ⇐ `ReadLink`; `Follow` ⇐ `FollowLink` (carries its own `Result<SpanSet, Invalid>`)
- `Deletions` ⇐ `ShowDeletions`; `Compare` ⇐ `Compare`; `Orphans` ⇐ `DeleteOrphans`; `Claims` ⇐ `InClaims`, `OutClaims`
- `Rejected(Rejection)` ⇐ any failure of a parsed `Op`

**Op-specific semantic contracts a caller must not misread:**
- **`Fork` ≠ `Version`.** `Fork` mints an **empty** account-tier document in the caller's own account, sharing **no** content; the content-sharing copy-on-write fork is `Version`. Do not expect `Fork` to share content.
- **`PrincipalPrefix.id` is an explicit wire id, not the session principal** — any account `Address` is public, immutable registry data derivable by anyone holding the `PrincipalId`. A client resolves *its own* prefix by passing its own `PrincipalId` (surfaced by the transport at session-open).
- **`NextAccountPrefix`/`PrincipalPrefix`** hand the client the M3-internal frontier/registry values that `Delegate`/`CreateNewDocument` demand but cannot otherwise compute; the common create flow needs neither (`Delegate` returns the minted `Address` directly).
- **`EditLink`** — caller supplies `SuccessorSpec{from, to, ty}` in content V-specs; M10 resolves them to build M7's `Link`. `TypeArg::Addrs` ⇒ address-denoting type slot; `TypeArg::Resolve` ⇒ content-resolved (mirrors `MakeLink`). M7 owns the slot-shape/schema verdict (`IllFormedSuccessor`/`DcViolation`); an ill-formed content VSpec is rejected `IllFormedSpec`.

**Interpreting `Rejection`:**
- `code` (`RejectCode`) is authoritative; `disposition` is an advisory Lampson hint only (`Permanent` | `Reorder` | `Retry` | `Halt`). A client that knows its own op-context may reissue despite a conservative hint.
- `disposition == Reorder` ⇒ a *future* committed state may satisfy the precondition (e.g. `BadTarget`, `DocNotRegistered`, `HomeNotRegistered`, `SourceNotRegistered`, `NotAnAccount`, `OriginalNotResident`, `EndpointNotResident`, `ParentNotRegistered`) — the client/coordination layer may reissue once it clears. **M10 surfaces, it does not reorder.**
- `disposition == Retry` ⇒ transient true no-op (`Durability`). `Halt` ⇒ kernel stopped (`Poisoned`). Anything not explicitly `Reorder`/`Retry`/`Halt` is `Permanent`.
- `NotNextForm`/`NotFresh` are `Permanent`: recovery is to re-derive a **fresh** prefix via `NextAccountPrefix` and reissue a *different* request — not a hinted retry of the same one.
- `site` (`FaultSite`) is populated only from **M6**'s variant-carried localization (span `index`/`fault`, `Compare`'s `operand`/`region`, and the offending document `addr` of multi-document `DocNotRegistered`); M5's and M8's errors fill only `code` (`site == None`).

**`Codec` (caller implements):**
- The dependent supplies one concrete `Codec`; M10 fixes only the typed `Op`/`Response`/`Rejection` targets.
- `parse` failure never reaches `execute`. The **transport** surfaces it by building `Response::Rejected(Rejection{ op: OpKind::Unparseable, code: Malformed, disposition: Permanent, site: None, detail })` and marshaling it — the one never-silent obligation M10 does not enforce itself.

## Seams exposed downstream

**→ the external FEBE client / transport (the only consumer):** build against `Operation<W>::execute(SessionId, Request) -> Response` plus a `Codec`.

Guarantees the client may rely on:
- commit-before-acknowledge; `committed_at`/`as_of` on every response;
- typed `Rejection` with an advisory `disposition` and a structured fault `site` (including the offending document `Address` for multi-document `DocNotRegistered`);
- per-session idempotency-key honoring within M10's uptime (sequential retries, op-kind-matched);
- session→principal binding;
- the two namespace-structure reads (`NextAccountPrefix`/`PrincipalPrefix`) needed to obtain the prefixes `delegate`/`create_new_document` demand.

The transport supplies:
- a concrete `Codec`;
- the connection→`PrincipalId` authentication (and surfaces that `PrincipalId` to the client at session-open, so it can name its own account in `PrincipalPrefix`);
- the **per-connection `SessionId` injection** (drawn from the connection binding, never read off the wire — the non-forgeability precondition);
- the concurrency policy (sequential vs pipelined);
- the **request↔response correlation** (M10 returns a bare `Response` with no `ReqId`; the transport pairs each reply with the in-flight `Request`'s `id`);
- the parse-failure `Response::Rejected` (stamped `OpKind::Unparseable`);
- at startup, the `Stores` factory passed to `Operation::new`, built via the engine-facing store-driver constructors `Namespace::new(Arc<Kernel<W>>)`, `Vstream::new(&Kernel<W>)`, `LinkStore::new(&Kernel<W>, Arc<TypeRegistry>)` (a required interface amendment to M3/M5/M7).

**→ M9:** **M10 ⟂ M9** (parallel, not stacked). M9's rule fires reach M7's gated write path directly; M10 never sees them except as committed state in later snapshots — no edge, no shared lifecycle.

## Boundary — NOT provided here

- **No per-store operation logic** (M5/M6/M7/M8 own it), **no automation** (M9), **no ordering/durability/recovery** (M2).
- **No journaled state and no recovery** — M10 names no concrete `World`/`Record`.
- **No cross-family write composite** in v1 — the capability is latent with zero occupants.
- **No fine-grained ownership (`ω`) check** — M3's atomic check is passed through verbatim; M10 only pre-checks "is there a principal at all" (`Unauthenticated`).
- **No wire codec byte format** — the `Codec` impl is the transport's.
- **No request↔response correlation and no `ReqId` echo** — the transport's.
- **No reorder/retry buffering** — M10 surfaces `Reorder`/`Retry` rejections; buffering/reordering is policy above M10.
- **No cross-restart exactly-once** — the idempotency cache is an in-memory, best-effort, per-`(SessionId, ReqId)` hint, committed-write acks only.
- **No `SessionId` non-forgeability enforcement and no authentication mechanism** — both are the transport's preconditions.
- **No M4 function calls** — the `M10 → M4` edge is type-only (`Val`/`ContentWrite`/`ContentError`/`HasContent` named only to satisfy `Vstream::insert`'s bound).
