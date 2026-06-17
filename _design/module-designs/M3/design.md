# M3 — Namespace: Allocation, Registry & Ownership — Detailed Design

## Purpose & boundary

M3 owns the **authoritative permanent name/entity space**: the baptismal/entity registry (which nodes, accounts, documents, and versions *exist*), the one frontier-discipline allocator that mints the next fresh, gap-free, monotone, globally-unique, T4-valid address on *any* chain (entity, content, link), the admission gate (B6/T4 well-formedness, P8 parent-exists, content/link home-scoping), and the principal registry with `owns` / longest-prefix `ω` / delegation / fork. **One thing well: be the single source of truth for *what addresses exist and who owns them*, and the single algorithm that hands out the next one.** It does **not** store content or link *values* (M4/M7 hold those at M3-minted addresses), materialize a new document's arrangement (M5 owns `M(d)`, left lazy — so no `M3 → M5` edge), own a journal or recovery (it registers record-types with M2 and rides M2's WAL), or mint node addresses (external `NodeBaptism`; M3 only *records* them after a lineage check). Allocation is deliberately decoupled from content (ghost elements, B3): "is registered?" never means "has bytes."

## Public interface

M3 is generic over the engine's world `W` via a thin composition seam; `Principal` is an ownership prefix (an account/node-tier `Address`; human/session binding is the access layer's job, not M3's).

```rust
use m1::{Address, Tumbler, Nat, Level, is_prefix, classify, checked_inc, subtree_of, validate};
use m2::{Kernel, Snapshot, Seq, LockKey, TxnError, WorldState};

pub type Principal = Address;                 // an ownership-root prefix (zeros ≤ 1), O1b-injective

#[derive(Clone)] pub enum EntityKind { Node, Account, Document, Version }

/// M3's slice of M2's World. The ONLY authoritative state M3 owns; lives inside W, durability is M2's.
#[derive(Clone, Serialize, Deserialize)]
pub struct NamespaceState {
    entities:   im::OrdSet<Tumbler>,          // authoritative: nodes/accounts/documents/versions (zeros ≤ 2)
    principals: im::OrdSet<Tumbler>,          // authoritative: ownership-root prefixes (zeros ≤ 1); ⊆ entities
    // optional #[serde(skip)] hints (ω prefix-trie, per-chain frontier counters) — see Open decisions
}

/// Engine-composition seam: how M3's slice & records sit inside the concrete W.
pub trait HasNamespace: WorldState {
    fn ns(&self) -> &NamespaceState;
    fn wrap(r: NsRecord) -> Self::Record;     // lift an M3 record into W::Record
}

#[derive(Clone, Serialize, Deserialize)] pub enum NsRecord {
    RegisterEntity   { addr: Tumbler, kind: EntityKind },   // folds into entities
    RegisterPrincipal{ prefix: Tumbler },                   // folds into principals
}
pub fn apply(ns: &NamespaceState, r: &NsRecord) -> NamespaceState;   // pure fold (M2 calls via W::apply)
```

### A. The frontier allocator (pure — the one algorithm)

```rust
/// A named address chain S(anchor, g): first = inc(anchor, g), then inc(·,0). g ∈ {1,2}.
pub struct Chain { anchor: Tumbler, g: u8 }
impl Chain {
    pub fn account (node: &Address)    -> Chain;  // (node, 2)   → zeros 1
    pub fn document(account: &Address) -> Chain;  // (account,2) → zeros 2
    pub fn subaccount(acct: &Address)  -> Chain;  // (acct, 1)   → zeros 1 (nested account)
    pub fn version (doc: &Address)     -> Chain;  // (doc, 1)    → zeros 2
    pub fn content (doc: &Address)     -> Chain;  // (b_C(doc),1) → element, s_C
    pub fn link    (doc: &Address)     -> Chain;  // (b_L(doc),1) → element, s_L

    /// The frontier address for this chain given the relevant member collection
    /// (entities for entity chains; M4/M7's slice for content/link — generic over V).
    pub fn next<'a>(&self, members: impl DoubleEndedIterator<Item=&'a Tumbler>) -> Address;
    pub fn first(&self) -> Address;               // inc(anchor, g)
}

pub fn b_c(d: &Address) -> Address;               // inc(d,2)  = [d.0.s_C]
pub fn b_l(d: &Address) -> Address;               // inc(b_c,0)= [d.0.s_L]
```

### B. Entity operations (single-family; M3 owns the whole transaction)

```rust
impl<W: HasNamespace> Namespace<'_, W> {           // thin façade over &Kernel<W>
    /// CREATENEWDOCUMENT (ASN-0103). Allocates a document under `account`, registers it. Does NOT
    /// materialize M(d) (M5, lazy). Pre: account registered & Account-class; `by` owns `account`.
    pub fn create_document(&self, account:&Address, by:&Principal)
        -> Result<(Address, Seq), TxnError<CreateDocErr>>;

    /// Delegation = account/sub-account creation (ASN-0042). Allocates the next ownership-tier child
    /// under `by` (g=2 if `by` is a node, g=1 if an account → result zeros ≤ 1 by construction),
    /// registers it as BOTH an entity and a principal in one transaction.
    pub fn delegate(&self, by:&Principal) -> Result<(Principal, Seq), TxnError<DelegateErr>>;

    /// Denial-as-fork (O10): allocate a fresh document under the forker's OWN account. Mechanically
    /// = create_document(by_account, by); content transclusion is M5's COPY. The trigger is upstream.
    pub fn fork(&self, by:&Principal) -> Result<(Address, Seq), TxnError<CreateDocErr>>;

    /// External NodeBaptism (ASN-0047): record an externally-minted node. Checks T4, NodeLineage
    /// (n₀ ≼ e), freshness. Optionally also registers it as a principal.
    pub fn register_node(&self, node:Address, principal:bool)
        -> Result<((), Seq), TxnError<RegisterNodeErr>>;
}

pub enum CreateDocErr   { NotAnAccount, Unauthorized }
pub enum DelegateErr    { NotAPrincipal, AccountFloor }     // (i),(ii),(iv) by construction; (iii),(v) checked
pub enum RegisterNodeErr{ NotT4, BadLineage, AlreadyExists }
```

### C. Allocation for composites (pure — folded by M5/M7 per M2 contract (3))

```rust
/// Content address under d (A_C(d), ASN-0093). M5 passes &stg.working().content; M5 pushes M4's
/// ContentAlloc record. M3 records NOTHING for content (it is zeros=3, lives in M4's dom(C)).
pub fn alloc_content_address<V>(content:&im::OrdMap<Tumbler,V>, d:&Address) -> Address;

/// Link address under d (A_L(d)). M7 passes &stg.working().links; M7 pushes M7's LinkAlloc record.
pub fn alloc_link_address<V>(links:&im::OrdMap<Tumbler,V>, d:&Address) -> Address;

/// Version identity (ASN-0123). Owned (ω(src)=by) → next_version(src); cross-owner account-tier
/// (zeros(by)=1) → next_document under by's account; cross-owner node-tier → reject (P-tier).
/// M5 folds this into VERSION and pushes RegisterEntity{v, kind}.
pub fn alloc_version_identity(ns:&NamespaceState, src:&Address, by:&Principal)
    -> Result<(Address, EntityKind), VersionAllocErr>;
pub enum VersionAllocErr { SourceNotDocument, NodeTierCrossOwner }

pub fn ns_record_register(addr:&Address, kind:EntityKind) -> NsRecord;   // for M5 to push
```

### D. Ownership & registry queries (read-only over a Snapshot)

```rust
pub fn owns(owner:&Address, a:&Tumbler) -> bool;             // O1: pfx ≼ a — pure, stateless (delegates to M1)
pub fn effective_owner(ns:&NamespaceState, a:&Tumbler) -> Option<Principal>; // ω: LONGEST-prefix match (O2)

pub fn is_registered(ns:&NamespaceState, e:&Address) -> bool;            // e ∈ E
pub fn registration_of(ns:&NamespaceState, e:&Address) -> Registration;  // Registered{level} | Unregistered
pub enum Registration { Registered(Level), Unregistered }

pub fn frontier_key(home:&Tumbler, mode:ChainMode) -> LockKey;          // M2 keyed-serialization seam
pub enum ChainMode { Account, Document, Version, Content, Link }

pub fn genesis() -> NamespaceState;                          // Σ₀ slice: {[1]:Node} + Π₀ (O14)
```

## Core data model

M3 holds **no persistent state of its own** — its authoritative state is two `im::OrdSet<Tumbler>` *inside* M2's `World`, and durability/recovery is entirely M2's.

| Structure | Shape | Authority | Why |
|---|---|---|---|
| **Entity registry** | `im::OrdSet<Tumbler>` (nodes/accounts/documents/versions, all zeros ≤ 2) | **authoritative**, append-only | An *ordered* set (not the counter-map of ASN-0040) because M3 needs prefix-range queries — frontier max-under-prefix, version enumeration, descendant scans, `ω` — not just `next`. Ordered keys give the rightmost-descent frontier max in O(log n) and range scans free (the granfilade shape, ASN-0093). Membership-only: kind is derivable from the address (M1 `classify` + `document_field` length), so nothing to keep consistent. Structural sharing makes each baptism a cheap new version. |
| **Principal registry** | `im::OrdSet<Tumbler>` of ownership prefixes (zeros ≤ 1; ⊆ entities) | **authoritative**, append-only, immutable values (O12/O13) | The prefix *is* the principal (O1b injective). Everything else — domains, effective owner, the delegation forest — is derived (ASN-0042). Small (one entry per principal, per node), so this is the only ownership state. |
| **Frontier** | *(none by default)* | **recomputable hint** | A pure function of the registry (B2; ASN-0093 stateless query-and-increment). Recompute on each allocation (range-max). No counter to drift or recover. |
| **ω index / frontier counters** | optional `#[serde(skip)]` trie / `HashMap<(Tumbler,mode),Nat>` | **recomputable hints** | Materialize only under measured pressure; maintained in `apply`, reseeded by M2's `rebuild_derived` (Open decisions). |

Critically, **content/link element addresses (zeros = 3) are NOT in M3's registry** — they live in M4's `dom(C)` / M7's `dom(L)`. M3 *computes* them and *gates their home*, but records only organizational entities. This is the ASN-0047 partition (`E` = entities; element-level addresses ∈ `dom(C)`), and it is what keeps M3's "is registered?" query about *documents*, not bytes.

## Internal design

### 1. The frontier allocator — one `Chain`, level-aware by construction

Every chain — account, document, version, content, link — is `S(anchor, g)`: first emission `inc(anchor, g)`, siblings `inc(·, 0)` (ASN-0040 `SiblingStream`). The single algorithm:

```
Chain{anchor, g}.next(members):
    sub_anchor = anchor ++ [0]*(g-1)          // common prefix of all chain members
    exact_len  = #anchor + g                  // every member has exactly this length
    span       = subtree_of(sub_anchor)       // M1: half-open [sub_anchor, shift(sub_anchor,1))
    match members.range(span).rev().find(|k| #k == exact_len) {   // lex-MAX member of this length
        None      => self.first()             // inc(anchor, g)
        Some(max) => checked_inc(validate(max), 0)   // inc(max, 0); T4 preserved (always for k=0)
    }
```

**This is the level-awareness ASN-0103/0123 demand, and it falls out of `(sub_anchor, exact_len)`.** A document under account `A` is `Chain::document(A) = (A, g=2)` → `sub_anchor=[A,0]`, `exact_len=#A+2`. A version of document `d` is `Chain::version(d) = (d, g=1)` → `sub_anchor=d`, `exact_len=#d+1`. The two scans never see each other's members: a version `[A,0,k,m]` (length `#A+3`) is filtered out of the document scan by `exact_len=#A+2`, and a base document `[A,0,k]` is filtered out of the version scan by `exact_len=#d+1`. So `next_document` never re-mints an address a version fork will claim, and vice-versa — exactly ASN-0123's V0 / CND.monotone, achieved by separate frontiers, not by inspecting kinds.

- **Common-case path:** the reverse range-scan skips only the lex-max document's own (few) versions before hitting it; `inc(·,0)` touches one component (M1 has no carry). O(log n + v).
- **Why the length filter, and the Green-equivalent shortcut:** `truncate-then-increment` (take the overall lex-max under `sub_anchor`, truncate to `exact_len`, `inc(·,0)`) is the O(1)-after-max Green variant (ASN-0103) and is **provably equal** to the length-filter given P8 (a version's parent document exists, so no version ordinal exceeds the max document's). Use either; the length-filter is the spec statement, truncate-then-increment the faster impl. (Recommended choice in Open decisions.)
- **Content/link** read M4/M7's slice generically (`OrdMap<Tumbler, V>`), so M3's code never names their value types — no `M3 → M4/M7` edge. `Chain::content(d)` anchors at `b_C(d)=inc(d,2)=[d.0.s_C]`, `Chain::link(d)` at `b_L(d)=inc(b_C(d),0)=[d.0.s_L]`, with `s_C=1, s_L=2` the fixed substrate convention (ASN-0093 SubspaceConventionAxiom). Subspace distinctness makes content/link freshness cross-subspace structural (T7).
- **Determinism & freshness by construction:** `next` is a pure function of the member set (B2), so it is memoizable, replayable, and the natural property-test oracle. Freshness is structural — the frontier is strictly past the max (FirstEmissionFreshness / SubsequentEmissionFreshness); M3 mints, never validates a caller-supplied address, so no active freshness check is needed.

### 2. The entity registry & admission gate

Registration is one `RegisterEntity` record folded into `entities` by `apply` (append-only insert; never removes — B0/P1). The gate, evaluated in the `transact` closure against `stg.working()`:

- **B6 / T4** (well-formedness): minting goes through M1's `checked_inc`; `inc(·,0)`/`inc(·,1)` always preserve T4, `inc(·,2)` from a valid account/document satisfies the `zeros ≤ 2` gate, so a gate failure means a corrupt parent slipped the registry — surfaced as an internal error, never expected.
- **P8** (parent-exists, ASN-0047): for a non-node entity, `parent(e) ∈ entities`. This is the one place M3 *strengthens* ASN-0040 (which imposes no parent-baptized precondition). Resolution of that tension: the "baptize beneath an unbaptized parent" freedom is for **content ghosts** (which aren't in M3's registry); for **entities**, P8 holds — you cannot create a document under a non-existent account. Enforced by `is_registered(parent)`.
- **Content/link home-scoping** (C2/L1a): before M5/M7 allocate content/link under `d`, they call `is_registered(document_of(a))`. M3 owns this check; the origin is recoverable from the address (M1 `document_of`), only its registration status needs the registry.
- **Atomicity** (B4): a registration (and, for delegation, the principal) is one M2 transaction — one commit marker, none-or-all. M3 needs no journal of its own.

`create_document` (ASN-0103): pre-checks `account ∈ entities ∧ Account`, `owns(by, account)`; allocates `Chain::document(account).next(entities)`; pushes `RegisterEntity{d, Document}`; returns `d`. It does **not** touch `M` — the arrangement is M5's, lazy (CND.empty realized as "absent until first edit"). Idempotency: each call baptizes a fresh address (no value-identity), so retry-dedup, if wanted, lives at M10's session layer (CND open decision).

### 3. Ownership: `owns`, `ω`, delegation, fork

- **`owns(owner, a) = is_prefix(owner, a)`** — pure containment (O1), evaluable anywhere, no state. May be true for several principals at once.
- **`ω(a)` = longest-prefix match** over `principals` (O2). Default impl: `principals.range(..=a).rev()`, return the first element that `is_prefix(·, a)` — the largest set-element ≤ a that is a prefix of a is the longest prefix. Π is small (per node), so this is fine; a radix/PATRICIA trie or a cached `address→owner` hint (a stale entry can only be a prefix-*ancestor* of the true owner by monotonic refinement O3, so it never over-claims) are the scale-ups (Open decisions). **`owns` and `ω` must never be conflated** (ASN-0042 O2; the `tumbleraccounteq` divergence): a node operator's prefix *contains* every delegated account, so authorizing by containment hands it ownership of delegated subdomains — the exact violation of O2/O3/O8 that longest-match exists to prevent. Authorization over a possibly-delegated region uses `ω`; containment is sound only within a principal's own *undelegated* subtree.
- **`delegate(by)`** = the account/sub-account creation gate (ASN-0042 O15). It allocates the next ownership-tier child under `by` — `Chain::account(by)` if `by` is a node (g=2 → zeros 1), `Chain::subaccount(by)` if `by` is an account (g=1 → zeros 1) — and pushes `RegisterEntity{p, Account} + RegisterPrincipal{p}` in **one** transaction. Of the five conditions, **(i) ancestry**, **(ii) authorization** (the new prefix is `by`'s own child, so `by` is its most-specific coverer), and **(iv) top-down-order** (frontier slot, nothing extends it yet) hold *by construction*; **(iii) account-floor** holds because `zeros(by) ≤ 1 ⇒ result zeros ≤ 1`; **(v) fresh-valid** is the frontier+`checked_inc` guarantee. Allocating at the frontier (not an arbitrary prefix) honors O17c (no delegating account #5 while #1–4 are unbaptized). Delegator identity is *not* stored — it is recomputable as the most-specific coverer (NestingByDelegation), valid while refinement stays monotone (Open decisions).
- **`fork(by)`** ≡ `create_document` under `by`'s own account (O10): a fresh document one tier below the principal, owned outright (`zeros(a') = zeros(pfx)+1`), original untouched. M3 does only the allocation; the content transclusion is M5's COPY, the denial-trigger is M5/M10 policy.

### 4. Version identity (for M5's VERSION)

`alloc_version_identity(ns, src, by)` is the pure branch M5 folds into its VERSION composite (ASN-0123): **owned** (`ω(src)=by`) → `Chain::version(src).next(entities)`; **cross-owner account-tier** (`zeros(by)=1`) → `Chain::document(account_of(by)).next(entities)` (the fork lands in *the forker's own* account namespace — severance V9, server-side confinement, never the foreign document's subtree); **cross-owner node-tier** → `NodeTierCrossOwner` (out of VERSION's single-identity domain, P-tier). M5 pushes the returned `RegisterEntity{v, kind}`; M3 records the identity, M5 records the snapshot+provenance. (VD: reading the address as *derivation* is sound only while nothing but VERSION allocates into a version namespace — an allocator discipline, Open decisions.)

### 5. Genesis & node provisioning

`genesis()` returns the Σ₀ slice: `entities = {[1]:Node}` (the bootstrap node `n₀`, ASN-0047 Σ₀) plus any seed accounts/documents, and `principals = Π₀` satisfying O14 (nonempty, finite, account-tier, injective, T4-valid, pairwise non-nesting, covering the seed addresses, each prefix ∈ entities). The engine composes this into the genesis `W` passed to `kernel.open`. Because the registry is an ordered set (not a counter-map), seed roots like `[1]` are ordinary keys — no auxiliary non-child-root set is needed (resolving ASN-0040's counter-only-can't-represent-`[1]` problem). `register_node` is the external `NodeBaptism` path: validate T4, check `NodeLineage` (`n₀ ≼ e`) and freshness, push `RegisterEntity{e, Node}` (the inc-allocator is *not* used for nodes).

### 6. Recovery

**None in M3.** The registry and principal set are M2-resident; M2 recovers them by replaying `RegisterEntity`/`RegisterPrincipal` records and the checkpoint. M3's `apply` is the deterministic fold; if M3 materializes any hint (ω-trie, frontier counters) it is `#[serde(skip)]`, maintained incrementally in `apply` and reseeded by `rebuild_derived` from `entities`/`principals` — the seed obligated to equal the `apply`-fold of the checkpointed prefix (M2's contract). Default: no hints, identity `rebuild_derived`.

## Invariants & contracts

**By construction** (from the data model / a pure function):
- **Permanence / irrevocability** (B0/B0★ ASN-0040; P1 ASN-0047): `entities`/`principals` are append-only; no code path removes. The guarantee *is* the absence of a delete API.
- **Determinism** (B2 ASN-0040): `Chain::next` is a pure function of the member set.
- **Contiguity / gap-freeness** (B1 ASN-0040): `next` always returns `inc(max,0)` (or `first`), and allocation is the sole growth path.
- **Cross-namespace uniqueness** (B7/B8-cross ASN-0040; GlobalUniqueness/T10 ASN-0034): structural from prefix-disjoint anchors under the full B6 gate — no coordination.
- **T4-validity of every allocated address** (B10 ASN-0040; T10a.4 ASN-0034): valid roots + `checked_inc` discipline.
- **Store/subspace disjointness** of the addresses M3 hands out (SD/L0 ASN-0093): content vs link anchors carry distinct `s_C`/`s_L`.
- **Ownership by prefix, no side table** (O1 ASN-0042); **exclusivity** (O2: longest-match + injectivity); **monotonic refinement** (O3); **node-locality** (O9: delegation extends, never crosses, the node component); **immutable prefixes / no expiry** (O12/O13).
- **Content-independence / ghosts** (B3 ASN-0040): registration never consults bytes; immediate referability (CND.refer) = membership.
- **Document-level shape** (M0 ASN-0093): documents have `zeros=2` by the allocator's mode-2 minting.

**By active enforcement** (a named gate guards):
- **Same-namespace uniqueness** (B8-same / B-Seq ASN-0040): serialize same-chain commits via M2's keyed critical section, key = `frontier_key(home, mode)`. *Where:* every alloc `transact`.
- **B6 / T4 admission** (B6 ASN-0040): `checked_inc` before every mint. *Where:* `Chain::next`/`first`.
- **Parent-exists** (P8 ASN-0047): `is_registered(parent)` before entity creation. *Where:* entity ops.
- **Content/link home-scoping** (C2/L1a ASN-0093): `is_registered(document_of(a))` before content/link alloc. *Where:* M5/M7 call M3's check.
- **Atomicity** (B4 ASN-0040): registration (+ principal) = one M2 transaction. *Where:* the `transact` boundary.
- **Prefix-injectivity & account-floor** (O1b/O1a/iii ASN-0042): delegation rejects non-fresh or `zeros>1` prefixes. *Where:* `delegate`.
- **Delegation gate** (O15 ASN-0042): five conditions — three by construction, account-floor + fresh-valid checked. *Where:* `delegate`.
- **`ω` is longest-match, not containment** (O2 ASN-0042): the resolver picks the longest prefix. *Where:* `effective_owner`.
- **Level-aware frontier separation** (ASN-0103, ASN-0123 V0): `(sub_anchor, exact_len)` keep document and version chains disjoint. *Where:* `Chain`.
- **Cross-owner version confinement** (V9 ASN-0123): seat the fork in the forker's own account, server-side. *Where:* `alloc_version_identity`.
- **Unbounded extent** (B9 ASN-0040): ordinals are M1 `Nat` (bignum). *Where:* the value type.
- **Bootstrap conformance** (O14 ASN-0042): `genesis()` satisfies all eight clauses.
- **Node lineage** (NodeBaptism/NodeLineage ASN-0047): `register_node` checks `n₀ ≼ e` + freshness.

## Dependencies & seams

**Upstream — M1 (Address & Span Algebra):**
- `Tumbler`/`Address`, `Ord` — registry keys.
- `checked_inc`/`inc_preserves_t4` — the B6-gated mint (M3 enforces the gate M1 supplies).
- `is_prefix` — `owns`, `ω`, delegation ancestry.
- `classify`/`Level`, `document_field` length — derived entity kind, version-vs-document.
- `parent`, `document_of` — P8 parent, content/link origin-scoping.
- `subtree_of` — the frontier range-scan span.
- `validate` — admission of external node addresses; re-Address-ing a registry max.

**Upstream — M2 (Transaction/Journal/Concurrency):**
- `transact` — all M3 mutations (single-family ops standalone; pure forms folded by M5/M7).
- `snapshot`/`Snapshot`/`Seq` — read-only queries report against a single pinned state.
- `WorldState`/`Record`/`apply` — M3 contributes `NamespaceState`, `NsRecord`, `apply` (via `HasNamespace`).
- `LockKey` — `frontier_key(home, mode)` from the central tag enum (clause-2 serialization seam; subsumed by M2 v1's single applier but the standing seam for the per-key realization).
- recovery — M3's registry is replay-recovered by M2; no M3 journal.

**Downstream seams (the contracts neighbors build against):**
- **→ M4:** content addresses arrive as parameters — M3 mints via `alloc_content_address`, M4 stores the value; M4 calls no allocator and M3 records nothing in M4's slice.
- **→ M5:** `alloc_content_address` and `alloc_version_identity` are **pure** functions M5 folds into its placement/VERSION composites (M2 contract (3) — never nested `transact`s), plus `ns_record_register` to push; `is_registered(d)` is M5's edit precondition (the only `M5 → M3` read). M3 never materializes `M(d)` (no `M3 → M5`).
- **→ M6 / M8:** `is_registered` / `registration_of` — M6/M8 own the *registered-empty (⟨⟩) vs unallocated (fail)* distinction by combining M3's membership with M5's arrangement; M3 answers only "registered?".
- **→ M7:** `alloc_link_address` (pure) + `is_registered(document_of(ℓ))` (L1a scoping). M7 stores the link value and supplies its own dedup coverage-class key to M2.
- **→ M9:** `effective_owner` for residence resolution; `is_registered`.
- **→ M10:** `create_document`, `delegate`, `fork`, `register_node` — the standalone transact ops M10 dispatches and acks after commit.

## Conflicts resolved

- **No parent-baptized precondition (ASN-0040 Bop) vs parent-exists (ASN-0047 P8).** The "baptize beneath an unbaptized parent" freedom is for **content ghosts** (not in M3's registry); for **entities**, M3 enforces P8 (`is_registered(parent)`). The two notes describe different layers, not a contradiction.
- **Unified store Σ=(C,L,M) with one allocator (ASN-0093) / `s.B` holding all baptized incl. content (ASN-0040) vs M3 owning only entities.** Resolution (per ASN-0047 `E` ⊆ {zeros ≤ 2}): M3 owns the **allocation discipline** (one `Chain` algorithm for every chain) and the **entity registry**; content/link **membership** lives in M4/M7. The allocator reads the relevant slice for its frontier — its own `entities` for entity chains, M4/M7's slice (generically, no edge) for content/link. This splits ASN-0093's unified state across modules while keeping one minting algorithm.
- **Eager `M(d)=∅` at creation (ASN-0103) vs lazy arrangement.** Per the decomposition, M3 registers `d` in `E` only; `M(d)=∅` is M5's lazy state. This breaks the `M3 → M5` cycle the eager form would create.
- **Counter-only registry (ASN-0040 recommendation) vs ordered map.** Resolved to an **ordered set**: M3 needs prefix-range queries (`ω`, version/descendant enumeration, level-filtered frontier max), which counters cannot serve; the ordered set also subsumes ASN-0040's auxiliary non-child-seed-root set.
- **Frontier authoritative ("persists frontier", decomposition) vs recomputable (ASN-0040/0093).** The **registry is authoritative**; the **frontier is a recomputable hint** (recompute-default). "Persists frontier" means: any cached frontier hint rides in M2's `W` and is recovered by replay — never an authoritative counter.
- **`owns` (containment) vs `ω` (longest-match).** Provided as distinct functions; authorization over possibly-delegated regions uses `ω`, never containment — the `tumbleraccounteq`/node-operator divergence (O2/O3/O8).
- **Reserve-then-confirm finality (ASN-0040 option) vs commit-as-finality.** Baptism is final at M2's commit marker; no two-phase reserve window (which would add semantics beyond the notes and risk B1 gaps).
- **Terminology:** "account" is canonical for the zeros=1 tier (M1's resolution); "user"/`U` is retained only as M1's field-projection symbol.

## Open build decisions

- **Frontier max impl:** length-filter reverse-scan (the spec form) vs **truncate-then-increment** (Green's O(1)-after-max, provably equal given P8; recommended — needs a truncate-to-length helper over M1's `Tumbler::new`).
- **Frontier strategy:** recompute-from-registry (recommended default) vs a cached `(home,mode)→ordinal` hint in `W` (only under measured allocation pressure; content/link frontier caches, if any, belong in M4/M7's slice, not M3's).
- **Content/link frontier-source coupling:** generic `OrdMap<Tumbler,V>` (recommended, dependency-clean) vs a `ChainView` trait vs caller-extracts-max-and-passes-it.
- **`ω` resolver structure:** linear/floor-walk scan (small Π, default) vs radix/PATRICIA trie vs cached `address→owner` hint (stale entries are safe ancestors by O3).
- **Delegate-prefix policy:** next-available-slot (Green-faithful, O17c; recommended) vs baptize-intermediates to reach a chosen prefix.
- **Delegator identity:** recompute via most-specific-cover (recommended while transfer is absent) vs store it (needed if ownership transfer is ever introduced).
- **Entity record content:** membership-only `OrdSet` (recommended; kind derived) vs a stored `EntityKind` tag for convenience.
- **VD enforcement:** enforce "only VERSION allocates into a version namespace" (so the address decodes as derivation) vs accept the final component as *allocation* order and recover derivation otherwise.
- **Batch content allocator:** offer M5 an `m`-consecutive-addresses helper (one `base()` read + count) vs per-atom recompute-against-`working()` (both correct; the latter is the M2-seam default).
- **Cross-owner node-tier version:** reject (P-tier, recommended) vs extend VERSION to mint the account+document pair.
- **Idempotency/retry for `create_document`/`fork`:** none in M3 (each call baptizes fresh — no value identity); decide whether M10's session layer dedups retries.
