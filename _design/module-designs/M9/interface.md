# M9 — Interface (for dependents)

M9 owns the substrate's predicate/coordination layer: a closed, read-only, statically-typed predicate/query algebra (PL), predicate definitions persisted as content, and a reactive rule engine with a quiescence theory — turning committed structural state into decidable verdicts and bounded reactions.

## Public interface

All handles hang off one `Coordinator<W>` over the engine's `Arc<Kernel<W>>`, under these bounds:

```rust
W: WorldState + HasLinks + HasM3 + HasContent + HasM5,
W::Record: From<LinkRec> + From<M5Rec> + From<M3Rec> + From<ContentWrite>,
```

Imported types: `View`, `Endset`, `Tuple`, `Tip`, `CoverageClass` are M7's; `Kernel`, `Snapshot`, `Seq`, `TxnError`, `WorldState` are M2's; `TypeRegistry`, `ReservedAddrs`, `TypeDecl`, `LinkStore`, `LinkRec` are M7's; `Vstream`, `M5Rec` are M5's; `Address`, `Span` are M1's; `Nat = BigUint`.

M9 contributes **no `WorldState` slice and no record variant**. Verdicts carry the `seq()` of the one `Snapshot` they were computed against.

### Construction (engine-assembled)

```rust
impl<W> Coordinator<W> {
    pub fn new(
        kernel:        Arc<Kernel<W>>,
        registry:      Arc<TypeRegistry>,
        reserved:      ReservedAddrs,
        decls:         Vec<TypeDecl>,
        mk_vstream:    Box<dyn for<'k> Fn(&'k Kernel<W>) -> Vstream<'k, W>   + Send + Sync>,
        mk_link_store: Box<dyn for<'k> Fn(&'k Kernel<W>) -> LinkStore<'k, W> + Send + Sync>,
    ) -> Coordinator<W>;
}
```

Catalog accessor (M9's own cached accessor — **not** M7's snapshot-bound `LinkState::reserved_type`):

```rust
reserved_type(ShippedType) -> &Endset
// ShippedType names the five shipped classes (PredDef, PredStable, Supersedes, retired, retraction).
// Used to build canonical Concrete TypeKeys for shipped classes; no snapshot.
```

### A. The predicate language (PL)

```rust
impl<W> Coordinator<W> {
    pub fn type_check(&self, params: Vec<(VarId, Sort)>, body: Term) -> Result<TypedTerm, TypeError>;
    pub fn type_check_trigger(&self, params: Vec<(VarId, Sort)>, body: Term) -> Result<TypedTerm, TypeError>;
    pub fn eval(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> Value;
    pub fn decide(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> bool;
    pub fn classify(&self, t: &TypedTerm) -> Dynamics;
}
```

### B. Predicate definitions

```rust
impl<W> Coordinator<W> {
    pub fn define_predicate(&self, d: &Address, term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;
    pub fn register_pred(&self, d: &Address, start: &Address)
        -> Result<(Address /*pdef tuple*/, Seq), RegisterError>;
    pub fn evaluate_def(&self, start: &Address, args: &[Value], view: View, snap: &Snapshot<W>)
        -> Result<Value, EvalError>;
    pub fn signature(&self, start: &Address) -> Option<Signature>;
    pub fn is_active_pred(&self, start: &Address, snap: &Snapshot<W>) -> bool;  // is_K(pdef,start)@active
    pub fn is_ever_pred(&self,   start: &Address, snap: &Snapshot<W>) -> bool;  // is_K(pdef,start)@audit
    pub fn supersede(&self, d: &Address, old_start: &Address, new_term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;
    pub fn current_version(&self, start: &Address, snap: &Snapshot<W>) -> Tip;   // tip over supersedes
    pub fn certify_stable(&self, d: &Address, start: &Address)
        -> Result<(Address, Seq), CertifyError>;
    pub fn is_certified_stable(&self, start: &Address, snap: &Snapshot<W>) -> bool;
    pub fn retract_pred(&self, d: &Address, start: &Address) -> Result<(Address, Seq), RetractError>;
}
```

### C. Reactive rules & quiescence

```rust
impl<W> Coordinator<W> {
    pub fn register_rule(&mut self, rule: Rule) -> Result<RuleId, RuleError>;
    pub fn certify_rule(&self, rule: &Rule) -> RuleCertification;               // SF + Marker + grow-only lint
    pub fn quiescent(&self, snap: &Snapshot<W>) -> bool;                        // Q0
    pub fn quiescent_scoped(&self, scope: &TypedTerm, body: ScopeBody, snap: &Snapshot<W>) -> bool; // Q7
    pub fn next_enabled(&self, snap: &Snapshot<W>) -> Option<Enabled>;          // PEEKS a candidate; &mut self `step` owns rotation/fairness
    pub fn fire(&self, e: &Enabled) -> Result<FireOutcome, FireError>;          // 1 deposit (emit|nullify), atomic, H-*
    pub fn step(&mut self, snap: &Snapshot<W>) -> StepOutcome;                  // pick+fire driver
    pub fn fire_count(&self, rule: RuleId, x: &Address) -> u64;                 // divergence backstop
    pub fn armer_cycles(&self) -> Vec<Vec<RuleId>>;                             // static cyclic-coupling warning
}
```

### `TypedTerm` accessors

```rust
impl TypedTerm {
    pub fn params(&self) -> &[(VarId, Sort)];
    pub fn result_sort(&self) -> Sort;          // return type Sort (design names the method; type evident from `t.result_sort() == Bool`)
    pub fn is_ref_free(&self) -> bool;
    pub fn source_body(&self) -> &Term;
}
```

### Public datatypes — the PL AST

```rust
type ArcTerm = Arc<Term>;  type ArcDom = Arc<Dom>;
#[derive(Clone, PartialEq, Eq, Hash)] pub struct VarId(u32);
pub const EXPANSION_NAME_BASE: u32 = 1 << 31;   // the reserved-expansion-name watershed
#[derive(Clone, PartialEq, Eq, Hash)] pub struct TypeKey(Endset);   // a registered/reserved type, named by its key endset

#[derive(Clone, PartialEq, Eq, Hash)] pub enum TypeRef { Concrete(TypeKey), ClassVar(VarId) }

pub enum Term {
    Var(VarId),
    Lit(Lit),                 // ⊤ ⊥ ℕ-lit addr-lit ; ⊥:T∪{⊥} ; ⊥:ℕ∪{⊥}
    Atom(Atom),               // state-reading atoms (below)
    Prim(Prim),               // V-PRIM ops: = ≼ T1 ∈ set= =∅ elems ℕ(= ≤ +) ·[K] def
    And(ArcTerm,ArcTerm), Or(ArcTerm,ArcTerm), Not(ArcTerm),
    Implies(ArcTerm,ArcTerm), Iff(ArcTerm,ArcTerm),                     // PC0
    Forall{var:VarId,dom:ArcDom,body:ArcTerm},                          // PC1 (Reg-quantifiers
    Exists{var:VarId,dom:ArcDom,body:ArcTerm},                          //   expanded away by type_check)
    Let{var:VarId,bound:ArcTerm,body:ArcTerm},                          // PC2 plain composition
    IfSome{opt:ArcTerm,var:VarId,then_:ArcTerm,else_:ArcTerm},          // PC2 binder guard
    Count(ArcDom), MaxT1(ArcDom), MinT1(ArcDom),                        // PC2a
    BigUnion{dom:ArcDom,var:VarId,body:ArcTerm},                        // PC2a ⋃(D,f)
    Reflect(ArcDom),                             // QD-refl: address-valued domain → ℘_fin(T) term
    Ref{addr:Address, args:Vec<ArcTerm>},        // only inside stored-def bodies — ref-bearing ⇒ is_ref_free=false
}
pub enum Atom {
    IsK(TypeRef,ArcTerm), Members(TypeRef), TargetsOf(TypeRef,ArcTerm),          // core (view-parameterized)
    IsFiltered(TypeRef,ArcTerm),                                                 // BH1
    Succs(TypeRef,ArcTerm), Chain(TypeRef,ArcTerm), Tip(TypeRef,ArcTerm),
        IsInChain(TypeRef,ArcTerm,ArcTerm),                                      // BH2 (fixed active)
    SourcesTo(TypeRef,ArcTerm), TargetOf(TypeRef,ArcTerm), TargetsKeyed(ArcTerm),// BH3 (fixed active; TargetsKeyed class-unindexed)
    Age(TypeRef,ArcTerm), Stale(TypeRef,ArcTerm),                                // BH4 (fixed active + home-frontier)
    IsDoc(ArcTerm),                                                              // V-DOC
    TupAddr(VarId), TupAddrsF(VarId), TupAddrsG(VarId),
        InCoverageF(ArcTerm,VarId), InCoverageG(ArcTerm,VarId),                  // V-TUP (state-independent)
}
pub enum Dom {
    MembersDom(TypeRef),   // M_K   : dom(T), view-parameterized
    ActiveSlice(TypeRef),  // A_K   : dom(Tup), fixed active
    AuditSlice(TypeRef),   // L_K   : dom(Tup), fixed audit
    LinkDom,               // L_dom : dom(T)
    Reg,                   // class-valued; quantification-only; expanded at type_check
    Filter{dom:ArcDom,var:VarId,pred:ArcTerm},
    SetTerm(ArcTerm),      // QD set-valued-term closure: a ℘_fin(T)-valued term reflected as a domain
}

pub enum Lit { True, False, Nat(Nat), Addr(Address), BotAddr, BotNat }   // BotAddr:T∪{⊥}, BotNat:ℕ∪{⊥}
pub enum Prim {
    AddrEq(ArcTerm,ArcTerm), Prefix(ArcTerm,ArcTerm), T1Lt(ArcTerm,ArcTerm),   // address =, ≼, T1
    SetMem(ArcTerm,ArcTerm), SetEq(ArcTerm,ArcTerm), IsEmpty(ArcTerm),         // ℘_fin(T): ∈, =, =∅
    Elems(ArcTerm),                                                            // Seq_fin(T)→℘_fin(T)
    NatEq(ArcTerm,ArcTerm), NatLe(ArcTerm,ArcTerm), NatAdd(ArcTerm,ArcTerm),   // ℕ: =, ≤, +
    MapGet(ArcTerm,TypeRef),                                                   // ·[K] on Map_fin
    Def(ArcTerm),                                                              // definedness · ≠ ⊥
}
```

### Public datatypes — values, sorts, signatures, dynamics

```rust
pub enum Sort { Bool, Addr, AddrSet, OptAddr, AddrSeq, Map, Nat, OptNat, Tup }   // COD ∪ {Tup}
pub enum Value {
    Bool(bool), Addr(Address), AddrSet(im::OrdSet<Tumbler>), OptAddr(Option<Address>),
    AddrSeq(im::Vector<Address>), Map(im::HashMap<CoverageClass,Address>),
    Nat(Nat), OptNat(Option<Nat>), Tuple(Tuple),                                  // Tuple binds a Tup var
}
pub struct Signature { pub params: Vec<(VarId, Sort)>, pub result: Sort }         // (Γ_D, C_D); each param sort ∈ COD

pub struct Env { /* im::HashMap<VarId, Value> */ }
impl Env { pub fn empty() -> Env; pub fn bind(&self, v: VarId, val: Value) -> Env; pub fn get(&self, v: &VarId) -> Option<&Value>; }

pub struct Dynamics { pub footprint: Footprint, pub stability: Stability,
                      pub active_exceptions: ActiveExceptions, pub view_independent: bool }
pub enum Stability { StSf, StOnly, SfOnly, Neither }        // 4-point lattice (ST∩SF / ST / SF / neither)
pub struct Footprint { /* read slices: per-type {active,audit}, L_R, residence dom, home-frontier flag */ }
pub struct ActiveExceptions { pub retraction_shrinks: bool,        // (i) any R-deposit can shrink an active slice
                              pub bh4_home_frontier: bool,         // (ii) BH4 moves with same-home deposits
                              pub targets_keyed_cross_type: bool } // (iii) targets_keyed is cross-type
```

### Public datatypes — rules, outcomes, errors

```rust
pub struct Rule { pub domain: Dom, pub trigger: TriggerRef, pub view: View, pub action: FireAction }
pub enum TriggerRef {
    Inline(TypedTerm),   // built via `type_check_trigger` (may bind one Tup); MUST be ref-free
    Def(Address),        // pdef-backed; evaluated via evaluate_def, so ref-bearing bodies survive de-registration
}
pub enum FireAction {
    Marker { home: Address, ty: TypeKey },   // emit ONE Unary K-tuple covering bound arg `a` at `home`
    Nullify { home: Address },               // nullify(home, a); uncertified, monitored
}
pub enum ScopeBody { PerEmitter, PerTarget, PerSource, PerAddress }

pub struct RuleId(u64);
pub struct Enabled { pub rule: RuleId, pub arg: Value }      // (ρ, x); Value::{Addr | Tuple} per the domain sort

pub enum FireOutcome { NoOp,                                  // trigger false at fire time (Q1)
                       Fired   { effect: Address, seq: Seq }, // a real, fresh deposit (advances divergence count)
                       Deduped { effect: Address, seq: Seq } } // an idem⊤ dedup hit; committed NOTHING; NOT counted
pub enum StepOutcome { Fired   { rule: RuleId, arg: Address, seq: Seq },
                       Deduped { rule: RuleId, arg: Address, seq: Seq },
                       NoOp, Quiescent }
pub enum RuleCertification { CertifiedTerminating,
                            Uncertified { sf: bool, marker: bool, grow_only: bool } }

pub enum TypeError {
    UnboundVariable(VarId),                        // a free Var outside the supplied Γ_D (the missing-context case)
    UnboundClassVar(VarId),                        // a TypeRef::ClassVar under no enclosing Reg binder (V-IDX)
    TupParameter(VarId),                           // a DEF-PATH Γ_D parameter sorted Tup — excluded from Codom
    SortMismatch { expected: Sort, found: Sort },
    BehaviorMissing { ty: TypeKey, needs: Behavior },  // an atom needs a behavior the (concrete) type's registration lacks
    UnregisteredType(TypeKey),                     // concrete TypeKey absent from the catalog
    NoReverseLookupClass,                          // class-unindexed `targets_keyed` used, but no cataloged class attaches BH3
    DanglingReference(Address),                    // Ref to a never-registered address (WT-ref domain failure)
    RegInstanceIllTyped(TypeError /* boxed */),    // a Reg-quantified body has an ill-typed concrete instance (V-IDX)
}
pub enum DefineError    { Insert(TxnError<InsertError>), Register(RegisterError), Supersede(TxnError<EmitError>) }
pub enum RegisterError  { NotResident, ParseFailed, IllTyped(TypeError),
                          ReferentNotEverRegistered(Address), ReferentNotActive(Address),
                          HomeNotRegistered, Emit(TxnError<EmitError>) }
pub enum EvalError      { NotEverRegistered, ArgArityMismatch, ArgSortMismatch }
pub enum CertifyError   { NotEverRegistered, NotBoolean, NotActive, ViewDependent, NotStable, Emit(TxnError<EmitError>) }
pub enum RetractError   { NotActive, Nullify(TxnError<NullifyError>) }            // NotActive: no active pdef tuple
pub enum FireError      { HomeNotRegistered, Emit(TxnError<EmitError>), Nullify(TxnError<NullifyError>) }
pub enum RuleError      { RefBearingInlineTrigger,                                // Inline must be ref-free
                          IllFormedDomain(TypeError),                             // rule.domain not a well-formed/ref-free QD domain
                          DomainTriggerSortMismatch { expected: Sort, found: Sort }, // trigger param sort ≠ domain element sort
                          TriggerNotBoolean,                                      // trigger codomain ≠ Bool
                          DefTriggerUnregistered(Address),                        // TriggerRef::Def addr not ever-registered
                          BadTriggerArity,                                        // trigger not single-parameter
                          BadMarkerType(TypeKey) }                                // Marker.ty not a cataloged Unary type

// `?`-conversions the bodies provide:
impl From<TxnError<InsertError>> for DefineError   { /* ::Insert */ }
impl From<RegisterError>         for DefineError   { /* ::Register */ }
impl From<TxnError<EmitError>>   for DefineError   { /* ::Supersede */ }
impl From<TxnError<EmitError>>   for RegisterError { /* ::Emit */ }
impl From<TxnError<EmitError>>   for CertifyError  { /* ::Emit */ }
impl From<TxnError<NullifyError>> for RetractError { /* ::Nullify */ }
```

## Caller contracts & obligations

**Construction (`new`)**
- Engine-assembled: caller injects the shared `Arc<Kernel<W>>`, the **one** engine-built `Arc<TypeRegistry>` behind the genesis-sealed config (M9 never rebuilds it), the same `(reserved, decls)` that seeds M7's `LinkState::genesis`, and two op-handle factories.
- Assembly obligation (not M9-local): the `mk_vstream`/`mk_link_store` factory bodies presuppose `skep-engine` can construct a `Vstream`/`LinkStore` from `&Kernel<W>` — neither constructor is in M5's/M7's for-dependents surface, so the engine discharges this, not M9.

**PL — `type_check` / `type_check_trigger`**
- Caller supplies the ordered `Γ_D` (free-parameter sorts in positional order; empty for a closed term). Every `Var` outside Γ_D ⇒ `UnboundVariable`.
- `type_check` (def-path): every Γ_D param sort MUST be a codomain — a `Tup` param ⇒ `TupParameter`. `type_check_trigger` (trigger-path): admits exactly one `Tup`-sorted parameter (for a tuple-domained rule); the one-parameter-Bool requirement is checked at `register_rule`, not here.
- Every `Concrete` `TypeKey` MUST be built from a **canonical catalog endset** — `reserved_type(ShippedType)` for a shipped class, your own `TypeDecl.key` for an app class. The catalog probe is `Endset`-equality, so a coverage-equal-but-byte-different key misses as `UnregisteredType`.
- Never put a parameter name or body binder in `VarId(v)` with `v ≥ EXPANSION_NAME_BASE` — that range is reserved for reference-expansion.
- Guarantee: a successful `TypedTerm` is **valid at every reachable state** (re-check is wasted work). Reads no structural state for a ref-free body. Errors: `UnboundClassVar`, `SortMismatch`, `BehaviorMissing`, `UnregisteredType`, `NoReverseLookupClass`, `DanglingReference`, `RegInstanceIllTyped`.

**PL — `eval` / `decide` / `classify`**
- PRECONDITION: `t.is_ref_free()` — a ref-bearing term is a **precondition violation (panics)**; route ref-bearing terms through `evaluate_def`. `decide` **also panics** if `t.result_sort()` is not `Bool`. `classify` requires ref-free.
- Caller passes one committed `Snapshot` (from `kernel.snapshot()`); M9 reads all constituents off it, so the verdict is single-coherent and **as-of `snap.seq()`**.
- Guarantee: `eval`/`decide` are pure, total, terminating, and **infallible** on a ref-free `TypedTerm`. Reads only M7 + M3 (no content/arrangement). `classify` is static, sound-but-incomplete, and **never over-certifies** (errs toward not-certified; `count(D)=c` lands in `Neither`).

**Definitions — `define_predicate` / `register_pred`**
- `define_predicate` returns `(def-identity = content **start** address, the **pdef emit's** commit `Seq` — NOT the insert's)`.
- Under concurrency: a concurrent INSERT lands the def mid-document (harmless — identity is the returned start); a concurrent DELETE ⇒ retryable `Insert(Rejected(BadPosition))` (recompute position, re-insert — **not** a defect); a `register_pred`-stage failure leaves harmless orphan content that a later `register_pred(d, start)` adopts.
- `register_pred` errors: `NotResident`/`ParseFailed` (parse/extent), `IllTyped`, `ReferentNotEverRegistered`, `ReferentNotActive`, `HomeNotRegistered`. Idem⊤ ⇒ **≤1 active `pdef` per start**.

**Definitions — `evaluate_def` / `signature`**
- `evaluate_def` PRECONDITION: `start` is **ever-registered** (not necessarily active) — else `EvalError::NotEverRegistered`. `args` bind positionally to `Γ_D = signature(start).params`; arity/sort mismatch ⇒ `ArgArityMismatch`/`ArgSortMismatch`. Pure pin to `snap`.
- `signature` takes **no snapshot**. Returns `None` for a not-yet-ever-registered address — `None` is **transient** (re-query after registration); a `Some` is **permanent** and cacheable forever.

**Definitions — `supersede` / `current_version` / `certify_stable` / `retract_pred`**
- `supersede` is **3 non-atomic transactions with NO idempotency key**: a lost-ack retry branches the lineage (so `current_version` returns `Indeterminate`). **Retry-dedup / exactly-once is the driving coordination caller's duty** (NOT M10 — `supersede` reaches M5/M7 directly). Returns the successor's identity.
- `current_version` returns a `Tip`: `Sink(head)` for a linear lineage, `Indeterminate` for branch/cycle.
- `certify_stable` requires ever-registered; rejects `NotBoolean`/`NotActive`/`ViewDependent`/`NotStable`. Sound-but-incomplete — never over-certifies.
- `retract_pred`: `NotActive` (no active `pdef` tuple) is a **clean rejection, never a panic**. Content untouched; reversible (re-register deposits afresh). **Does not cascade** to referents.

**Rules & quiescence — `register_rule` (&mut self)**
- Validates before admitting; each failure is a typed `RuleError`, never a late fire-time panic. Domain must be a well-formed ref-free QD expression with element sort ∈ {Addr, Tup} (`IllFormedDomain`); trigger must be a one-parameter `Bool` predicate (`BadTriggerArity`/`TriggerNotBoolean`); domain↔trigger sort must match (`DomainTriggerSortMismatch`); a `Marker.ty` must be cataloged Unary (`BadMarkerType`).
- A `Tup` domain requires a `Tup`-param **`Inline`** trigger (built via `type_check_trigger`) — a `Def` signature is Codom-only and **cannot** serve a `Tup` domain. A ref-bearing `Inline` is rejected `RefBearingInlineTrigger`; remediation is persist-as-`Def` (Codom-param triggers only) or inline the helper (tuple-domained triggers).
- `register_rule` enforces **well-formedness only**, not termination — an uncertified-but-well-formed rule (every `Nullify` among them) is admitted; use `certify_rule` and apply your own uncertified-rule policy.
- **Documented contract (not enforced):** a `FireAction::Nullify` rule's domain must yield resident links — tuple-domained (`a = t.addr`) or `Addr`-over-`L_dom`. An `Addr`-over-`M_K` (member-address) domain passes `register_rule` but trips `FireError::Nullify(Rejected(BadTarget))` on every fire.

**Rules & quiescence — `certify_rule` / `quiescent` / `quiescent_scoped`**
- `certify_rule` returns `CertifiedTerminating` only for SF trigger + Marker action + grow-only domain (under weak fairness + bounded input); else `Uncertified { sf, marker, grow_only }` naming the failed legs. Sound-but-incomplete.
- `quiescent` is a decidable Q0 done-verdict any party can run from state + registry, evaluated at one pinned snapshot (each conjunct at its rule's declared view).
- `quiescent_scoped` PRECONDITION: `scope` is a one-`Addr`-parameter `Bool` ref-free `TypedTerm` — a violation **panics** (like `decide`). CONTRACT: verdict is **exact iff every scoped rule's domain element sort matches `body`'s required sort** (`PerAddress`→Addr; `PerEmitter`/`PerTarget`/`PerSource`→Tup); for a mixed-sort registry, sort-incompatible rules are left unscoped, yielding a **strict over-approximation of remaining work — never false quiescence**. Keep the registry sort-homogeneous for an exact verdict.

**Rules & quiescence — `next_enabled` / `fire` / `step` / `fire_count` / `armer_cycles`**
- `next_enabled` (&self) **peeks** a candidate; it does **not** advance rotation and is **not fair on its own**. Returns `None` when nothing is enabled.
- `fire` performs one atomic deposit (emit | nullify). Reports `Fired` / `Deduped` / `NoOp`; **only `Fired` advances the divergence count** (`Deduped`/`NoOp` leave no journal record). Home-unregistered ⇒ `FireError::HomeNotRegistered`; other rejections wrap `FireError::Emit`/`Nullify`.
- `step` (&mut self) is the pick+fire driver that **owns rotation** — weak fairness is a property of the `step` loop, sufficient to reach/hold quiescence for an all-SF, grow-only, bounded-input registry. It is a **replaceable** default driver. Returns `Quiescent` when nothing fires.
- `fire_count(rule, x: &Address)`: bookkeeping key is an `Address` — for a `Tup`-domain rule it is the bound tuple's `t.addr`, for an `Addr`-domain rule the bound address. For SF/Marker rules, count > 1 certifies misbehavior.
- `armer_cycles` is a static warning; a cycle of non-SF rules is a divergence risk.

**Cross-cutting guarantees a caller may rely on**
- Every PL term terminates and is decidable (no fixpoint/recursion former); the algebra is closed (no foreign read-path code).
- Identity by start address; ≤1 valid parse per start (encoding is injective); the reference DAG is acyclic with no cycle check.
- Evaluation keys on **ever-registration, never on endorsement currency** — a gap-de-registered referent yields a dangling-but-live reference (no cascade).
- M9 owns no authoritative state; every verdict/effect recomputes from M7/M3/M4.

## Seams exposed downstream

**→ coordination layer (the upward consumer, out of corpus)** — three capability groups:
1. **PL evaluation:** `type_check` once with the def's Γ_D (or `type_check_trigger` for a tuple-domained rule's trigger — the only PL context that binds a `Tup`), then `eval`/`decide` are pure ref-free verdicts "as of `snap.seq()`".
2. **Definitions:** `define_predicate` → identity-by-start (benign retryable `BadPosition`/orphan-content under concurrency); `evaluate_def` keyed on ever-registration; `supersede`/`current_version` for lineage (3 non-atomic txns — retry-dedup is the **driving coordination caller's**, not M10's); `certify_stable`/`is_certified_stable` for the cached stability verdict.
3. **Rules & quiescence:** `register_rule` (validated: ref-free `Inline` via `type_check_trigger` or ever-registered `Def`, one-`Bool`-param trigger sort-matched to the domain element sort; `Nullify` must be tuple-domained or `Addr`-over-`L_dom`; cataloged-Unary `Marker.ty`) + `certify_rule`; `quiescent[_scoped]` as a decidable done-verdict any party can run from state + registry alone (scoped: exact for a sort-homogeneous scoped set, else a safe over-approximation); `next_enabled`/`fire`/`step` as the **replaceable** driver whose weak-fairness guarantee lives in `step`'s rotation — with the explicit boundary that **reaching/holding quiescence is conditional** on fairness + bounded input + (for non-grow-only) environment hypotheses the substrate cannot enforce.

**Handed further up (NOT M9's to decide):** the activation binding (who may register rules), bounded-input workloads, the scheduler/violation policy, and stochastic rule bodies — M9 supplies the mechanism, not the policy.

## Boundary — NOT provided here

- **No authoritative state** — PL reads M7/M3; defs persist as M4 content + M7 tuples; the rule registry is an in-memory working set. No `WorldState` slice, no record variant.
- **No content-region / arrangement query algebra (M8)** — hard lateral boundary; **no M9→M8 edge**.
- **No request lifecycle / dispatch / client acknowledgment (M10)** — parallel surface; M9's fires reach M7's gated write path **directly, never through M10**.
- **No ordering / durability / recovery (M2).**
- **No byte content / arrangement / link value / address minting / registry mutation (M4/M5/M7/M3).** M9 builds **no second `TypeRegistry`** (it projects the injected one).
- **No ownership consultation** (no `effective_owner`); residence reduces to `is_registered_document`.
- **No feedback/loop former and no arbitrary fold accumulator** (closed ceiling).
- **v1 limits:** only single-deposit fires (Marker emit / single Nullify) — no multi-deposit atomic fires; `quiescent_scoped` applies a single `ScopeBody` (no exact per-rule scoping); no BH3/BH4 type cataloged, so `targets_keyed`/`Age`/`Stale` do not type-check.
