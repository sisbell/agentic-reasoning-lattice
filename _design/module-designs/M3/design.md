# M3 — Namespace: Allocation, Registry & Ownership

## Purpose & boundary

M3 owns the **authoritative permanent name space**: it mints every fresh, globally-unique, T4-valid address the system ever uses, records which organizational entities (nodes, accounts, documents) exist, and answers *"is this allocated?"* and *"who owns this?"* by prefix. It is the single minting authority and the single arbiter of the entity/principal sets. One thing well: **it owns identity, not content.** It does *not* store bytes (M4), arrangements (M5), or link values (M7); it does *not* materialize a new document's arrangement (lazy, in M5 — see [Conflicts resolved](#conflicts-resolved)); it does *not* originate node addresses (those arrive from the network-provisioning boundary, NodeBaptism); it does *not* run the request lifecycle or bind sessions to principals (M10). It hands every store a fresh owned address plus two cheap structural answers, and persists its registry + frontier through M2.

## Public interface

Indices 1-based (M1 convention). All types `Tumbler`/`Address`/`Level`/`Span`/`Nat` are M1's; `Kernel`/`Snapshot`/`LockKey`/`Seq`/`TxnError` are M2's.

```rust
pub struct PrincipalId(pub u64);                 // opaque external identity, supplied by M10/session
#[derive(Clone)] pub struct Principal { pub id: PrincipalId, pub prefix: Address }  // prefix: T4-valid, zeros ≤ 1

pub enum MintError    { HomeNotRegistered, SourceNotRegistered, NotAnAccount, Gate(GateViolation) }
pub enum OpError      { NotOwner, NotAnAccount, NotRegistered, Mint(MintError) }
pub enum DelegateError{ DelegatorUnknown, NotAncestor, NotAuthorized, NotAccountTier,
                        NotTopDown, NotFresh, NotNextForm, NotValid }
pub enum NodeError    { NotValid, NotNode, NotFresh, NotDescendantOfBootstrap }
```

### A. Frontier allocation — *pure, composable* (folded into M5/M7 composites; M2 contract 3)

Each returns the minted address and the one journal delta the caller stages. They read the **working** state (so successive mints in one composite each see the prior mint), check only *structural* preconditions, and never touch ownership policy.

```rust
impl M3State {
    /// Next content address under d: namespace (b_C(d), 1), element field [s_C, m+1]. [M5: INSERT]
    pub fn mint_content(&self, home: &Address) -> Result<(Address, M3Rec), MintError>;
    /// Next link address under d: namespace (b_L(d), 1), element field [s_L, m+1]. [M7: MAKELINK]
    pub fn mint_link(&self, home: &Address)    -> Result<(Address, M3Rec), MintError>;
    /// Next version identity: namespace (source, 1) — the version chain, kept SEPARATE
    /// from the document chain below (ASN-0123). [M5: owned CREATENEWVERSION]
    pub fn mint_version(&self, source: &Address) -> Result<(Address, M3Rec), MintError>;
    /// Next document identity under an account: namespace (account, 2).
    /// [CREATENEWDOCUMENT; cross-owner VERSION; fork]
    pub fn mint_document(&self, account: &Address) -> Result<(Address, M3Rec), MintError>;

    /// Lock-key encoding for a namespace — handed to M2's transact so same-namespace
    /// commits serialize (B8) while distinct namespaces run free (B7). M5/M7 reuse this
    /// for their content/link allocation locks so they coincide with M3's.
    pub fn lock_key(home: &Address, g: u8) -> LockKey;     // content: lock_key(d, /*s_C anchor*/ ..)
}
```

### B. Entity operations — *transact-wrapped* (M3 drives the transaction; called by M10)

```rust
impl Namespace { // holds Arc<Kernel<W>>
    /// Baptize a fresh empty document under `account`. Authorization is by EFFECTIVE owner
    /// (ω), not bare containment. Registers d in the entity set; does NOT write M5's
    /// arrangement (lazy). Returns only after commit (commit-before-acknowledge). [ASN-0103]
    pub fn create_new_document(&self, caller: PrincipalId, account: &Address)
        -> Result<Address, TxnError<OpError>>;

    /// Delegation: the 5-condition gate (O15), then baptize the new account prefix AND
    /// register the principal in ONE transaction. [ASN-0042]
    pub fn delegate(&self, delegator: PrincipalId, new_prefix: Tumbler, new_id: PrincipalId)
        -> Result<Address, TxnError<DelegateError>>;

    /// Admit an externally-originated node (NodeBaptism: validate freshness + n₀-lineage;
    /// the ADDRESS is chosen by provisioning, not minted here). [ASN-0047]
    pub fn register_node(&self, addr: Tumbler) -> Result<Address, TxnError<NodeError>>;

    /// Denial-as-fork, allocation half (O10): a fresh document in the caller's OWN account.
    /// Reduces to create_new_document(caller, pfx(caller)); M5 wires the shared content.
    pub fn fork(&self, caller: PrincipalId) -> Result<Address, TxnError<OpError>>;
}
```

### C. Queries — *pure methods* (read off any M2 `Snapshot`; write nothing)

```rust
impl M3State {
    pub fn is_allocated(&self, a: &Address) -> bool;            // any namespace incl. content/link
    pub fn entity_level(&self, a: &Address) -> Option<Level>;   // Some iff registered entity (zeros ≤ 2)
    pub fn is_registered_document(&self, d: &Address) -> bool;  // == entity_level == Some(Document)
    pub fn effective_owner(&self, a: &Address) -> Option<Principal>;        // ω(a), longest-prefix match
    pub fn owns(prefix: &Address, a: &Address) -> bool { is_prefix(prefix.tumbler(), a.tumbler()) } // O1
}
```

### D. Genesis

```rust
impl M3State { pub fn genesis() -> M3State; }   // nodes={[1]}, frontiers={}, Π={ [1] → π₀ }  (Σ₀, O14)
```

## Core data model

M3's slice of M2's `WorldState`. All persistent (`im`) so each commit yields a cheap structurally-shared version — free MVCC snapshots for readers and free historical `ω_Σ` (retain old roots). **The journal is the sole authority** (M2); these three structures are the *recovered working representation*, folded by `apply`, and need no `rebuild_derived` override.

```rust
pub struct M3State {
    /// THE registry, in B1+B2 compressed form. A namespace's entire realized set
    /// {c₁..cₘ} IS the single count m — so a gap is literally unrepresentable (B1 free).
    /// Keyed by (parent, g) — which keeps the document chain (A,2) and the version chain
    /// (d,1) on SEPARATE frontiers (ASN-0123) by construction. Covers every chain:
    /// accounts, documents, versions, content, links. Values are big-ints (B9 unbounded).
    frontiers: im::HashMap<NsKey, Nat>,

    /// Node addresses (zeros = 0). Externally minted (NodeBaptism), so possibly
    /// non-contiguous → explicit, not frontier-encoded. This is ASN-0040's mandatory
    /// auxiliary set for non-child roots, generalized to all nodes. Seeded {[1]}.
    nodes: im::OrdSet<Tumbler>,

    /// Principal registry Π, keyed by ownership prefix. Small (node/account tier only, O1a).
    /// Append-only with immutable prefixes (O12/O13). The ONLY authoritative ownership
    /// state — the delegation forest is recomputable (NestingByDelegation) and never stored.
    principals: im::OrdMap<Tumbler, Principal>,
}

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct NsKey { parent: Tumbler, g: u8 /* 1 | 2 */ }   // == ASN-0040's namespace (p, d)

pub enum M3Rec {                                   // M3's journal deltas, folded by `apply`
    Allocate          { addr: Tumbler },           // mint: advance frontier[namespace(addr)]
    RegisterNode      { addr: Tumbler },           // external node admission
    RegisterPrincipal { prefix: Tumbler, id: PrincipalId },  // delegation's principal half
}
```

**Why these shapes.** A `HashMap` for `frontiers` because the hot operations — mint and membership — are *point* lookups on one namespace; we never iterate namespaces, so we don't pay for order. `BigUint` values are non-negotiable (B9: "each integer has no upper limit"; a fixed-width counter silently violates it). The principal map is `OrdMap` because delegation's top-down check needs a descendant *range* scan, and ordering lets a builder upgrade ω to a range walk. **Authoritative vs hint:** `frontiers`/`nodes`/`principals` are authoritative working state (the compressed allocation journal). The delegation forest and any `address → owner` ω-cache are *hints* — recomputable from `principals` alone — and are deliberately **not** stored.

`apply` (M3's fold) is deterministic, total, side-effect-free:

```rust
M3Rec::Allocate{addr}          => { let (p,g,n) = decompose(&addr); frontiers.insert(NsKey{p,g}, n) }
M3Rec::RegisterNode{addr}      => nodes.insert(addr)
M3Rec::RegisterPrincipal{p,id} => principals.insert(p.clone(), Principal{id, prefix: validate(p).unwrap()})
```

`decompose(addr) = (parent(addr), if zeros(addr)==zeros(parent(addr)) {1} else {2}, ordinal(addr))` — pure M1. One `Allocate` variant suffices for every minted address (entity, content, link) because the frontier map is uniform; the level distinction is recovered at *query* time from `zeros`.

## Internal design

### 1. The frontier allocator (the heart)

For namespace `(p, g)`, ASN-0040's `next(B,p,g)` has a closed form once you store the count `m`: the chain `S(p,g)` is `c₁ = inc(p,g)`, `cₙ₊₁ = inc(cₙ,0)`, so `cₙ = p ++ [0]*(g−1) ++ [n]`. Therefore **the next address is `c_{m+1}` = `p ++ [0]*(g−1) ++ [m+1]`** — read the count, append/replace the trailing ordinal.

```rust
fn next_in(&self, key: &NsKey) -> Result<Address, GateViolation> {
    let m = self.frontiers.get(key).cloned().unwrap_or_else(Nat::zero);
    let parent = validate(key.parent.clone()).expect("registered parents are T4-valid"); // standing inv
    let c1 = checked_inc(&parent, key.g as usize)?;      // M1 gate ⇒ B6(ii)/(iii) enforced (TA5a)
    Ok(if m.is_zero() { c1 } else { with_trailing_ordinal(&c1, m + 1u32) })  // cₘ₊₁
}
```

- **Common case** is a single `HashMap::get` + one M1 `checked_inc` — no scan. (The reference's stateless "find-max-under-prefix-and-increment" is the same answer without the cached count; caching the count *is* the O(log n)→O(1) optimization, and we cache it because we keep the registry anyway.)
- **Level-awareness** (ASN-0123, the load-bearing gotcha): we key by `(p, g)`, never by the predicate "next document under A." A document under account A lives in `(A, 2)`; a version of document d lives in `(d, 1)`. Both classify as `Document`, both have `parent == A`-or-a-document, but their namespace keys differ, so their frontiers advance independently and **never re-mint a colliding address**. This is the entire fix for ASN-0103's version/document collision and ASN-0123's VD obligation — it falls out of the key, requiring no length filter.
- **Determinism (B2):** `next_in` is a pure function of `frontiers` — memoizable, replayable, and the natural property-test oracle.
- **Tradeoff:** the counter representation makes B1 contiguity *free* (a gap is unrepresentable) and registry size O(active namespaces) not O(addresses), at the cost of decomposition on membership (cheap — `parent`/`zeros`/`ordinal`). The alternative (explicit address set/trie) buys fast arbitrary-`t` membership but reintroduces contiguity as something to *enforce*; deferred to [Open decisions](#open-build-decisions).

### 2. The entity registry (membership without a second structure)

The entity set E is *encoded* by the entity-namespace frontiers plus the node root set — no separate `Set<Address>`. Membership is decompose-and-compare (ASN-0040 counter membership):

```rust
fn entity_level(&self, a: &Address) -> Option<Level> {
    match a.level() {
        Level::Node => self.nodes.contains(a.tumbler()).then_some(Level::Node),
        Level::Account | Level::Document => {
            let p = parent(a)?;                                    // M1 longest-valid-prefix
            let key = NsKey{ parent: p.tumbler().clone(), g: if zeros(a)==zeros(&p) {1} else {2} };
            let m = self.frontiers.get(&key).cloned().unwrap_or_else(Nat::zero);
            (Nat::one() <= *ordinal(a.tumbler()) && *ordinal(a.tumbler()) <= m).then_some(a.level())
        }
        Level::Element => None,   // content/link are not entities — use is_allocated
    }
}
```

`is_allocated` is the same probe without the `zeros ≤ 2` restriction, so it answers for content/link too (the referential-integrity oracle M5 needs). Consistency is automatic: a content frontier `(b_C(d),1)` only advances if d is registered (P6 gate), and E is append-only, so a `true` answer is permanent (B0/P1). **Ghost principle:** `is_allocated` reflects *minting*, never byte-presence — a registered-empty document is a valid, addressable ghost (B3); content existence is M4's separate axis.

### 3. Content & link sub-allocators (why the frontier lives here, not in M4/M7)

`mint_content(d)`: anchor `b_C(d) = inc(d, 2) = [d.0.s_C]` (zeros(d)=2 ⇒ B6-safe), chain `(b_C(d), 1)`, emitting `[d.0.s_C.{m+1}]` with element field `[s_C, m+1]`. `mint_link(d)`: `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]`, chain `(b_L(d), 1)`. The subspace identifier is the element-field's **first component** (`s_C=1`, `s_L=2`), read via M1's `subspace()` — *not* the `.0.` separator (a corpus-wide misread to guard against). `s_C ≠ s_L` is exactly what makes content and link address spaces disjoint by construction (SD/L14, T7).

The deep point: M3 cannot read M4's `dom(C)` or M7's `dom(L)` (the DAG forbids `M3 → M4/M7`), so the content/link frontier **is M3's own state**, advanced by the `Allocate` record M5/M7 co-stage with their value-write in one M2 composite. Allocation⇒placement⇒value-write are atomic (J0); M3's frontier and M4's `dom(C)` therefore advance together and can never diverge.

### 4. Admission gate (B6 + P8/P6 + freshness)

- **B6 (well-formedness)** — by construction: minting only ever applies `inc(parent, g)` for B6-valid `(parent, g)` (valid registered parent, g∈{1,2}, zeros budget). M1's `checked_inc` is the TA5a gate; routing every first emission through it is the defensive guard (it can only fire on a corrupted frontier).
- **P8 / P6 (parent/origin registered)** — actively enforced: `mint_document`/`mint_version` check the account/source via `entity_level`; `mint_content`/`mint_link` check the home document via `is_registered_document`. These are the *only* active structural gates — everything else about a minted address is structural.
- **Freshness (B8/V0)** — by construction from monotone frontier advance under serialized commit (below); never a runtime "is it taken?" check, because we mint rather than validate.

### 5. Principal registry & the `ω` resolver

`owns(prefix, a)` is a pure two-tumbler prefix test (O1) — coordination-free, pushable to the edge, consulting no state. **`effective_owner` (ω) is the one operation that consults Π**: longest-prefix match.

```rust
fn effective_owner(&self, a: &Address) -> Option<Principal> {
    // Only zeros ≤ 1 prefixes of `a` can be principal prefixes (O1a). Enumerate them
    // longest-first: account-tier prefixes (N·0·U[..j]) then node-tier (N[..i]).
    self.principal_tier_prefixes(a)             // ≤ depth candidates, longest first
        .find_map(|p| self.principals.get(&p).cloned())
}
```

The account-tier floor (O1a) is the win: we never probe document/element prefixes, so ω is O(depth) lookups, not O(addresses). **Critical discipline** (the ownership-divergence trap): a node operator's prefix *contains* every delegated account, so `owns` is true for several principals at once — only ω (longest match) arbitrates. Authorization must use ω, never bare `owns`, or the node operator falsely appears to own delegated subdomains. O2 exclusivity (exactly one ω) is a *theorem* given prefix-injectivity, which delegation's freshness check (below) enforces — no runtime uniqueness check.

- **Recovery/tradeoff:** Π is replay-recovered like everything else. ASN-0042's recommendation stands: default to a linear scan keeping the longest match (Π is small, per-node); upgrade to a radix trie only when |Π| or query rate demands ([Open decisions](#open-build-decisions)). An `address → owner` cache is a sound hint (a stale entry can only under-resolve to an ancestor, never over-claim, by monotonic refinement).

### 6. Delegation gate

`delegate` runs the 5 conditions of O15 against the snapshot, then **baptizes the new account prefix and registers the principal in one transaction** (atomicity is the crux — M2's `transact` gives it; a two-phase baptize-then-register could half-fail):

```
(i)  ancestry      pfx(delegator) ≺ new_prefix                          is_prefix + strict
(ii) authorization ω(new_prefix) == delegator   (delegator is the longest existing coverer)
(iii)account-tier  zeros(new_prefix) ≤ 1                                 O1a
(iv) top-down      no existing principal strictly under new_prefix       OrdMap range scan
(v)  fresh-valid   T4-valid(new_prefix) ∧ !is_allocated(new_prefix)      O1b prefix-injectivity
     next-form     new_prefix == next_in(namespace(new_prefix))          O17c (builder may relax)
```

Condition (ii) reuses ω directly. Delegation always produces an **account** (zeros=1: (i)+(iii) force it), so it advances an account-chain frontier and adds one principal. This is the *only* non-bootstrap entry for principals.

### 7. CREATENEWDOCUMENT, fork, node baptism, genesis

- **`create_new_document`** locks `(account, 2)`, checks `ω(account).id == caller`, mints via `mint_document`, stages one `Allocate`, returns post-commit. It registers d and **stops** — no `M(d)=∅` write into M5. This is the deliberate divergence from ASN-0103's eager recommendation ([Conflicts resolved](#conflicts-resolved)). No idempotency key (identity is the address, ASN-0103): a retried lost-ack yields a harmless orphan empty document; exactly-once lives at M10's session layer if wanted.
- **`fork`** is `create_new_document(caller, pfx(caller))` — for an account-tier principal that mints a fresh document one tier below its prefix (O10, `zeros(a')=zeros(pfx)+1`), with M5 wiring the shared content separately (mechanism/policy split). A node-tier forker has no account to fork into (must delegate one first) — matching ASN-0123 V9's account-tier scoping.
- **`register_node`** is the provisioning seam: the address is *supplied* (NodeBaptism mints outside the docuverse), M3 only validates freshness, `Level::Node`, and bootstrap lineage `[1] ≼ addr`, then adds to `nodes`. This is the one validate-not-mint path (see conflict 1).
- **`genesis`** = `nodes={[1]}`, `frontiers={}`, `Π={[1]→π₀}` (Σ₀ + O14). "Load empty journal" and "fresh genesis" are the same code path.

### 8. Durability, serialization, recovery

M3 **rides M2** — it builds no WAL of its own. Its three structures are part of `WorldState`, recovered by M2's checkpoint-load + replay; B4 atomicity (frontier advance and record durable *together*) is exactly M2's `transact` commit. The one invariant the durability protects — **never mint an address twice** — holds because the frontier only advances, `apply` is deterministic, and same-namespace commits are serialized by handing M2 the per-namespace `LockKey = lock_key(home, g)`. Distinct namespaces carry distinct keys, so independent owners/documents allocate concurrently (B7); only same-namespace serializes (B8/B-Seq). The minted address is returned only after M2 commits (commit-before-acknowledge), so a crash never loses a handed-out address — over-shooting (a gap) is safe (permanent ghost), reuse is fatal, and we never reuse.

## Invariants & contracts

### By construction (fall out of the data model)
- **Permanence / irrevocability** — `frontiers`/`nodes`/`principals` only grow; there is *no* delete API. [ASN-0040 B0/B0★, ASN-0047 P1/P3, ASN-0042 O12/O13]
- **Contiguity / gap-free** — the count representation makes a gap unrepresentable. [ASN-0040 B1]
- **Determinism & finiteness** — `next_in` is a pure function of the frontier; growth is one-at-a-time. [ASN-0040 B2/B_fin]
- **Unbounded extent** — `Nat = BigUint` for every ordinal and count. [ASN-0040 B9]
- **T4-validity of every minted address** — valid parents + `checked_inc`. [ASN-0040 B10, ASN-0093 StoreT4Validity]
- **Cross-namespace uniqueness; document↔version separation; content↔link disjointness** — distinct `(p,g)` keys, `s_C ≠ s_L`. [ASN-0040 B7/B8-cross, ASN-0093 SD/Cross-doc, ASN-0123 V0/VD, ASN-0034 T10]
- **Content-independence (ghosts)** — registry is M3, content is M4; allocated ≠ has-bytes. [ASN-0040 B3]
- **Ownership exclusivity, refinement, node-locality** — longest-prefix match over an append-only immutable-prefix Π. [ASN-0042 O2/O3/O8/O9]

### By active enforcement (M3 must guard)
- **Same-namespace uniqueness** — serialize commits per namespace via the `(home,g)` `LockKey` to M2. [ASN-0040 B8/B-Seq] → *the allocator + M2 transact*
- **Atomicity (frontier advance + record durable together)** — M2's `transact`/commit marker. [ASN-0040 B4]
- **Parent/origin registered (P8/P6/C2/L1a)** — `entity_level`/`is_registered_document` checks before minting. [ASN-0047 P8/P6, ASN-0093 C2/L1a] → *§4*
- **Prefix-injectivity & account-floor** — delegation (v) freshness + (iii) tier. [ASN-0042 O1b/O1a]
- **Delegation gate (5 conditions)** — `delegate`. [ASN-0042 O15] → *§6*
- **Authorization by ω (never bare `owns`)** — `create_new_document`/`fork`/`delegate`. [ASN-0042 O5, ownership-divergence] → *§5/§7*
- **Node freshness + bootstrap lineage** — `register_node`. [ASN-0047 NodeBaptism] → *§7*
- **Commit-before-return** — address returned only post-commit. [ASN-0040 finality, ASN-0103 commit point]

## Dependencies & seams

**Upstream — M1 (calls):** `checked_inc`/`inc_preserves_t4` (B6 gate on every mint), `inc` (anchors `b_C`/`b_L`), `parent`/`zeros`/`ordinal`/`document_of` (decomposition & membership), `classify`/`Level`/field projections (entity-level + acct/node prefixes for ω), `is_prefix`/`validate`, `subspace` (content vs link). M3 holds **no** address algebra of its own.

**Upstream — M2 (calls):** `transact(&[lock_key(home,g)], …)` for every mutating op (atomic + serialized + durable); `snapshot()` for query reads; M3 implements its slice of `WorldState::apply` (and the default `rebuild_derived`). M3 stages `M3Rec`; M2 owns ordering/durability/recovery.

**Downstream seams M3 exposes (build neighbors against these):**
- **M5 → M3:** `is_registered_document(d)` (edit precondition); `mint_content`/`mint_version`/`mint_document` *pure* (composed inside M5's INSERT/COPY/VERSION composites, using `lock_key` for the serialization key); `is_allocated(a)` (content-side referential-integrity oracle for COPY transclusion). M5 never reads M4 for this — allocation status is M3's.
- **M7 → M3:** `mint_link` *pure* (inside MAKELINK); `is_registered_document(d)` (link's home).
- **M6, M8 → M3:** `is_registered_document(d)` — they convert *registered-but-no-arrangement* → ⟨⟩ and *unregistered* → fail. M3 supplies the bool; the ⟨⟩-vs-fail *query semantics* are theirs.
- **M9 → M3:** `effective_owner`/`is_registered_document` (residence resolution); pred-def content is allocated indirectly via M5's composite (M9→M5→M3).
- **M10 → M3:** dispatches `create_new_document`/`delegate`/`register_node`/`fork`.

## Conflicts resolved

1. **Mint vs validate document addresses (ASN-0093 K.σ vs ASN-0047 K.δ / ASN-0103).** ASN-0093's `K.σ` *validates* a caller-supplied document address; ASN-0047/0103 *mint* it. ASN-0093 itself defers "document-address origination to the entity-allocation layer" — **which is M3**. Resolution: M3 **mints** accounts/documents/versions/content/links via the frontier; the validate-not-mint path survives only for **nodes** (NodeBaptism originates them externally, M3 validates).

2. **"Recompute the cursor from the store" (ASN-0093/0047) vs the module DAG.** Those notes treat C/L/registry as one substrate and recompute the frontier from `dom(C)`/`dom(L)`. Our split forbids `M3 → M4/M7`, so M3 cannot read those stores. Resolution: **M3 owns and persists the frontier for all chains, including content/link**, advanced by `Allocate` records that M5/M7 co-stage with their value-writes in one M2 composite. Same Lampson hint discipline (recomputable by replay), different source-of-truth boundary (M3's own allocation journal, not M4/M7).

3. **Eager `M(d)=∅` (ASN-0103) vs lazy arrangement (decomposition).** ASN-0103 recommends writing the empty arrangement at creation — which would write M5 from M3 and close an `M3 → M5` cycle. Resolution: `create_new_document` **registers d only**; the arrangement is implicit/lazy in M5. M6/M8 read *registered-with-no-arrangement* as ⟨⟩. The DAG stays acyclic (`M5 → M3` only).

4. **`owns` (containment) vs `ω` (longest-match) for authorization.** ASN-0103's literal `pfx(π) ≼ A` precondition is bare containment, but in the multi-tier model a node operator contains delegated accounts. Resolution: every authorization gate uses **`ω`** (the delegate, not the ancestor), per O5 and the ownership-divergence finding.

## Open build decisions

- **Frontier representation:** counter map (recommended; B1 free) vs. explicit allocated-set/trie (fast arbitrary-`t` membership, contiguity becomes enforced) vs. hierarchical tree (only if subtree/range queries are needed elsewhere).
- **ω resolver structure & caching:** linear scan over Π (default, ASN-0042) vs. `OrdMap` descending range-walk vs. radix/PATRICIA trie — sized to |Π| and query rate; plus an optional `address → owner` hint cache.
- **Delegate-prefix policy:** mint the next free slot (Green-faithful, drop the `NotNextForm` check) vs. validate a caller-supplied next-form prefix (O17c) vs. baptize intermediates to reach a chosen prefix.
- **Serialization granularity:** the per-`(home,g)` `LockKey` (recommended — concurrency by B7) vs. a single global writer; and whether `delegate`/`create_new_document` additionally lock Π (only matters if a concurrent delegation can change `ω(account)` mid-transaction).
- **Record delegator identity vs. recompute the forest** (NestingByDelegation): recompute suffices while refinement stays monotonic (no ownership transfer); store it only if transfer is later introduced.
- **Node tracking:** explicit `OrdSet` for all nodes (recommended — tolerates non-contiguous external minting) vs. a node-frontier if provisioning guarantees contiguity.
- **`PrincipalId` shape & session binding:** opaque here; the session→principal binding and idempotency/exactly-once for retried `create_new_document` live at M10.
