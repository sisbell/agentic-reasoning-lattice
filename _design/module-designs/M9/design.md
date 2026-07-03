# M9 — Predicate & Coordination Layer: Detailed Design

## Purpose & boundary

M9 is the substrate's **programmable, self-monitoring automation layer**. It owns three things and nothing else: (1) **PL** — a closed, read-only, statically-typed predicate/query algebra that composes M7's per-type atoms (Observe + BH1–BH4) into decidable Boolean/value verdicts over structural state; (2) **predicate definitions as content** — PL terms persisted as immutable content-addressed artifacts, validated/registered/versioned/certified as `pdef`/`pd_stable` tuples; and (3) a **reactive rule engine with a quiescence theory** — a registry of trigger→action rules, an atomic fire executor, a quiescence detector, a fair scheduler, and a termination lint, all *written in* PL.

The one thing it does well: **turn committed structural substrate state into decidable verdicts and bounded reactions, using composition as the only extension mechanism — never foreign read-path code.**

It does **not** own: any authoritative state (PL reads M7/M3; defs persist as M4 content + M7 tuples; the rule registry is an in-memory working set — see Core data model); the content-region/arrangement query algebra (**M8**, against which ASN-0129 draws a hard lateral boundary — no M9→M8 edge); the request lifecycle, dispatch, or client acknowledgment (**M10**, a parallel surface — M9's fires reach M7's gated write path directly, never through M10); ordering/durability/recovery (**M2**); or any byte content, arrangement, link value, address minting, or registry mutation (**M4/M5/M7/M3** respectively).

---

## Public interface

All handles hang off one `Coordinator<W>` over the engine's `Arc<Kernel<W>>`, where

```rust
W: WorldState + HasLinks + HasM3 + HasContent + HasM5,
W::Record: From<LinkRec> + From<M5Rec> + From<M3Rec> + From<ContentWrite>,
```

(the bounds M9's `LinkStore<W>` / `Vstream<W>` op-handles need). `View`, `Endset`, `Tuple`, `Tip`, `CoverageClass` are M7's; `Kernel`, `Snapshot`, `Seq`, `TxnError`, `WorldState` are M2's; `TypeRegistry`, `ReservedAddrs`, `TypeDecl`, `LinkStore`, `LinkRec` are M7's; `Vstream`, `M5Rec` are M5's; `Address`, `Span` are M1's; `Nat = BigUint`.

**Engine-assembled construction.** `Coordinator::new` is called by the engine assembler and is *injected* everything M9 would otherwise have to construct against an unpublished upstream constructor — so M9 names neither `Vstream::new`, `LinkStore::new`, nor `TypeRegistry::build`:

```rust
impl<W> Coordinator<W> {
    /// Receives: the shared kernel; the ONE engine-built `Arc<TypeRegistry>` behind the
    /// genesis-sealed config (NEVER rebuilt here — item 2), which M9 projects its static
    /// `TypeCatalog` from and then need not retain; the `(ReservedAddrs, decls)` pair that names
    /// the app type-key endsets and the five `ShippedType` endsets for that projection; and two
    /// op-handle FACTORIES minting a borrow-scoped `Vstream`/`LinkStore` off `&Kernel<W>` per call
    /// (the engine — the one crate that can name those constructors — supplies them; HRTB because
    /// each handle borrows the kernel). M9 mints a fresh handle off `Arc<Kernel<W>>` per write.
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

**Assembly obligation (not M9-local).** The injected `mk_vstream`/`mk_link_store` factory *bodies* presuppose that `skep-engine` can construct a `Vstream`/`LinkStore` from `&Kernel<W>` — neither constructor appears in M5's/M7's *for-dependents* surface, so this is an upstream/assembly obligation the engine discharges (the same gap M10 shares), not one M9 builds. M9 only *names* the two factory types and invokes the factories. A second, equally standing assembly obligation is **PR-DISC**: no holder of M7's `emit` other than M9's `register_pred`/`certify_stable` may route a typed emit whose `ty` is `pdef`/`pd_stable` (see Invariants; M7's gate rejects only R-class, so the exclusion is the assembly's/dispatcher's to enforce).

M9 contributes **no `WorldState` slice and no record variant** — it is a pure orchestrator/evaluator. Verdicts carry the `seq()` of the one `Snapshot` they were computed against (M2 V1 retrospective).

### A. The predicate language (PL)

```rust
impl<W> Coordinator<W> {
    /// Type-check `body` UNDER the ordered parameter context `params` (Γ_D — the free parameter
    /// Var sorts in positional order; empty for a closed term, ASN-0129 WT being a Γ-parameterized
    /// CHECKING judgment), EXPAND Reg-quantifiers to concrete-class instances (substituting each
    /// TypeRef::ClassVar to the concrete class), and reject ill-typed / dangling-reference /
    /// unregistered-type / unbound-(value-or-class-)variable / non-Codomain-parameter terms (this
    /// is the DEF-PATH check: a `Tup`-sorted Γ_D parameter is `TupParameter` — a stored def binds
    /// values, never a tuple; a RULE TRIGGER, the one PL context that binds a tuple, is checked via
    /// `type_check_trigger` below). Every `Concrete` TypeKey MUST be a canonical catalog endset
    /// (`reserved_type`/your own decl key): the catalog probe is `Endset`-equality, not coverage,
    /// so a coverage-equal-but-byte-different key misses as `UnregisteredType`. The result
    /// TypedTerm CARRIES Γ_D (so define_predicate / evaluate_def / ST⁺ read it back), an
    /// `is_ref_free()` flag, AND the original PRE-`Reg`-expansion syntactic body (the compact
    /// canonical form `define_predicate` encodes — §Core data model / §Internal 4), and holds ONLY
    /// Concrete TypeRefs in its evaluable projection (no Reg quantifier survives). Reads no
    /// structural state for a ref-free body; consults the immutable signature memo for any Ref.
    /// Once Ok, valid at every reachable state.
    pub fn type_check(&self, params: Vec<(VarId, Sort)>, body: Term) -> Result<TypedTerm, TypeError>;

    /// As `type_check`, but for a RULE TRIGGER — the only PL term that may bind a tuple. Admits a
    /// single `Tup`-sorted parameter in `params` (a tuple-domained rule, `ActiveSlice(K)`/
    /// `AuditSlice(K)`, ASN-0133 ρ_R, fires by binding a `Value::Tuple`, which the V-TUP atoms
    /// consume and `eval` already binds); every OTHER parameter, and every `type_check` (def-path)
    /// Γ_D, stays Codom-only (`TupParameter`). ASN-0129 WT itself admits `Tup`-sorted context
    /// variables, so this is the note's own latitude. One-parameter-Bool is still a `register_rule`
    /// check, not enforced here.
    pub fn type_check_trigger(&self, params: Vec<(VarId, Sort)>, body: Term) -> Result<TypedTerm, TypeError>;

    /// Pure, total, terminating denotation at one view against one committed snapshot.
    /// PRECONDITION: `t.is_ref_free()` — a surviving Ref node is a precondition violation (PANICS,
    /// like `decide` on a non-Bool codomain). Ref-bearing terms evaluate ONLY through `evaluate_def`,
    /// keeping this denotation content-free. INFALLIBLE on a ref-free TypedTerm. Reads ONLY M7 + M3.
    pub fn eval(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> Value;

    /// Convenience for Bool-codomain terms; panics if the codomain is not Bool or `t` is ref-bearing.
    pub fn decide(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> bool;

    /// Static footprint + 4-point stability lattice + the three active-view exceptions +
    /// view-independence flag, computed RELATIVE TO `view` (PC3: the pass binds each
    /// view-parameterized constituent — the core atoms and `M_K` — to it; fixed-view atoms read
    /// their named slices regardless; `view_independent` alone is view-agnostic, the PR-VIEW
    /// syntactic scan). TypedTerm deliberately carries no view (PR-VIEW), so the view is a
    /// parameter here, not an annotation. Sound-but-incomplete; never over-certifies. Reads no
    /// state. PRECONDITION: ref-free (callers classify inline triggers or a flattened expand).
    pub fn classify(&self, t: &TypedTerm, view: View) -> Dynamics;
}
```

### B. Predicate definitions (self-hosting persistence)

```rust
impl<W> Coordinator<W> {
    /// Encode `term`'s COMPACT pre-`Reg`-expansion body (carrying its Γ_D) to one content Val, write
    /// it through M5's placement composite (mint+write+place+R), then validate+register the `pdef`.
    /// Returns the def IDENTITY (content start addr) and the `pdef` EMIT's commit Seq (NOT the
    /// insert's). A concurrent INSERT/DELETE may move/invalidate the computed append position — a
    /// benign retryable `BadPosition`; a `register_pred`-stage failure leaves harmless orphan
    /// content (§Internal 4).
    pub fn define_predicate(&self, d: &Address, term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;

    /// Validate (parse → Γ_D+body, WT+WT-ref, ever-registration of refs, endorsement, home-
    /// residence) the run already at `start` against ONE pinned snapshot, then emit the `pdef`
    /// tuple via M7. Gate-first; idem dedup at M7.
    pub fn register_pred(&self, d: &Address, start: &Address)
        -> Result<(Address /*pdef tuple*/, Seq), RegisterError>;

    /// resolve+expand+denote. Precondition: `start` EVER-registered (not active) — else
    /// `NotEverRegistered`; an ever-registered start whose immutable content fails the PR-ENC
    /// parse/WT (an undisciplined deposit — PR-DISC breach, §Internal 4) is `UndisciplinedDef`.
    /// Binds `args` positionally to Γ_D (= signature(start).params). Pure pin to `snap`.
    pub fn evaluate_def(&self, start: &Address, args: &[Value], view: View, snap: &Snapshot<W>)
        -> Result<Value, EvalError>;

    /// (Γ_D, C_D); defined-signature starts only. Answered from the immutable DefMemo; on a MISS it
    /// pins its OWN snapshot to check ever-registration (`is_K(pdef, start)@audit`); the miss-path
    /// derivation recurses through each referent's `signature` (WT-ref; well-founded by PR2). A
    /// Some answer is memoized PERMANENTLY (content immutable, ever-registration monotone). An
    /// ever-registered start whose content fails the PR-ENC parse/WT (undisciplined — PR-DISC
    /// breach) answers None, memoized as a PERMANENT POISONED entry (content immutable, the failure
    /// cannot heal — the parse is never re-run); a never-registered None is NOT memoized (transient
    /// — a later registration must surface). No snapshot parameter.
    pub fn signature(&self, start: &Address) -> Option<Signature>;
    pub fn is_active_pred(&self, start: &Address, snap: &Snapshot<W>) -> bool;  // is_K(pdef,start)@active
    pub fn is_ever_pred(&self,   start: &Address, snap: &Snapshot<W>) -> bool;  // is_K(pdef,start)@audit

    /// Register `new_term` and record old→new via the shipped `supersedes` type (content-address
    /// endpoints, NOT M7::assert_sup). 3 non-atomic txns; no idempotency key — a lost-ack retry
    /// branches the lineage. Retry-dedup is the DRIVING coordination caller's (this is a
    /// Coordinator method reaching M5/M7 directly, NOT via M10); `create_new_document` is the
    /// *pattern* analogue, not the same dispatcher. Returns the successor's identity.
    pub fn supersede(&self, d: &Address, old_start: &Address, new_term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;
    pub fn current_version(&self, start: &Address, snap: &Snapshot<W>) -> Tip;   // tip over supersedes

    /// CVALID(0..iii): Boolean sort, actively registered, view-independent expansion, ST⁺. Emits pd_stable.
    pub fn certify_stable(&self, d: &Address, start: &Address)
        -> Result<(Address, Seq), CertifyError>;
    pub fn is_certified_stable(&self, start: &Address, snap: &Snapshot<W>) -> bool;

    /// De-register (M7::nullify on the active `pdef` tuple). Content untouched; reversible.
    /// NotActive (no active tuple) is a clean rejection, never a panic.
    pub fn retract_pred(&self, d: &Address, start: &Address) -> Result<(Address, Seq), RetractError>;
}
```

### C. Reactive rules & quiescence

```rust
impl<W> Coordinator<W> {
    /// Validate the rule and add it to the working set. Validation (each failure a typed RuleError,
    /// never a late eval-time panic): `rule.domain` is CHECKED AND NORMALIZED through the same
    /// WT-domain + `Reg`-expansion pass as `type_check` and stored as a checked `TypedDom`
    /// (cataloged Concrete TypeRefs, well-typed Filter/SetTerm bodies, behavior-compatible atoms,
    /// element sort Addr or Tup; a `Reg` QUANTIFIER INSIDE A BODY is legitimate PL and is expanded
    /// away; a BARE `Reg` domain fails the sort check — `IllFormedDomain`; a surviving `Ref` is
    /// `RefBearingDomain`, domains having no `Def` escape — inline the helper); the trigger is a
    /// one-parameter Bool predicate whose single parameter sort EQUALS the domain element sort
    /// (Inline: its carried Γ_D, built via `type_check_trigger`, also ref-free; Def:
    /// signature(addr) ever-registered, Boolean, single Codom-param of the domain sort — so a `Def`
    /// trigger cannot serve a `Tup` domain); a Marker action's `ty` is a cataloged Unary type that
    /// is NOT a PredLayer class (`pdef`/`pd_stable` ⇒ `PredLayerMarkerType` — PR-DISC reserves
    /// those slices for register_pred/certify_stable). REJECTS a ref-bearing
    /// `TriggerRef::Inline` (RefBearingInlineTrigger): the remediation is to persist the trigger as
    /// a def and reference it via `TriggerRef::Def` — AVAILABLE ONLY for a Codom-parametrized
    /// (non-`Tup`) trigger, a stored def's signature being Codom-only; a TUPLE-domained trigger has
    /// no def escape (a `Def` cannot bind a `Tup`) and must instead be made ref-free `Inline` by
    /// INLINING the referenced helper.
    pub fn register_rule(&mut self, rule: Rule) -> Result<RuleId, RuleError>;
    pub fn certify_rule(&self, rule: &Rule) -> RuleCertification;               // SF + Marker + grow-only lint

    pub fn quiescent(&self, snap: &Snapshot<W>) -> bool;                        // Q0

    /// Q7 scoped quiescence. `scope`: a one-`Addr`-parameter `Bool` `TypedTerm`, ref-free, checked
    /// as a PRECONDITION (a violation panics, like `decide`). CONTRACT on the single `ScopeBody`:
    /// the verdict is EXACT iff every scoped rule's domain element sort matches this body's required
    /// sort (`PerAddress`→Addr; `PerEmitter`/`PerTarget`/`PerSource`→Tup); for a mixed-sort registry
    /// the sort-incompatible rules are left UNSCOPED (their full `[D_ρ]`), yielding a STRICT
    /// over-approximation of remaining work — never false quiescence, only possibly-more. Exact
    /// per-rule scoping (ASN-0133's `ρ_R` model) is deferred (Open) pending a per-rule scope-body
    /// field on `Rule`.
    pub fn quiescent_scoped(&self, scope: &TypedTerm, body: ScopeBody, snap: &Snapshot<W>) -> bool; // Q7

    pub fn next_enabled(&self, snap: &Snapshot<W>) -> Option<Enabled>;          // PEEKS a candidate; &mut self `step` owns rotation/fairness
    pub fn fire(&self, e: &Enabled) -> Result<FireOutcome, FireError>;          // 1 deposit (emit|nullify), atomic, H-*
    pub fn step(&mut self, snap: &Snapshot<W>) -> StepOutcome;                  // pick+fire driver

    pub fn fire_count(&self, rule: RuleId, x: &Address) -> u64;                 // divergence backstop
    pub fn armer_cycles(&self) -> Vec<Vec<RuleId>>;                             // static cyclic-coupling warning
}
```

Public datatypes: `Term`/`Dom`/`TypeRef`/`Lit`/`Prim`/`TypedTerm`/`Value`/`Sort`/`Signature`/`Env`/`Dynamics`, `Rule`/`TriggerRef`/`FireAction`/`ScopeBody`/`Enabled`/`RuleId`, and the result/error types (`TypeError`, `DefineError`, `RegisterError`, `EvalError`, `CertifyError`, `RetractError`, `FireError`, `RuleError`, `FireOutcome`, `StepOutcome`, `RuleCertification`) — all in Core data model. (`TypedDom`, the checked rule-domain carrier, is internal to the working set — §Internal 5.)

---

## Core data model

**Authoritative state owned by M9: none.** Predicate definitions live as M4 content (the Val) + M7 `pdef`/`pd_stable` tuples; rule *effects* live as M7 deposits. Everything M9 holds is a **recomputable hint or an in-memory working set**, rebuilt by replay/re-query/re-registration — no journal, no `apply`, no slice. This is the deliberate Lampson outcome: M9 duplicates no authoritative state.

### The PL AST (reified data, not closures)

A finite, acyclic, tagged-union tree in two mutually-recursive families. **Reified, not closure-encoded** — three syntax-directed analyses (type-check, footprint, stability) must read structure. Subterms are `Arc`-shared, optionally interned through a hint table (the persistent-structure win for shared `pdef` bodies — optimization, never load-bearing).

```rust
type ArcTerm = Arc<Term>;  type ArcDom = Arc<Dom>;
/// A PL variable name. The high sub-range `VarId(v)` with `v ≥ EXPANSION_NAME_BASE` is RESERVED for
/// reference-expansion fresh names (§Internal 4): no recorded parameter name and no body binder may
/// inhabit it — enforced at `VarId::new`, the sole public constructor, so PR-ENC's
/// body-binder-disjointness ("no recorded parameter name and no body binder may inhabit" the
/// expansion supply) is structural, not merely intended.
#[derive(Clone, PartialEq, Eq, Hash)] pub struct VarId(u32);
pub const EXPANSION_NAME_BASE: u32 = 1 << 31;   // the reserved-expansion-name watershed
impl VarId {
    /// The sole PUBLIC constructor — the reservation's enforcement point: rejects the reserved
    /// expansion-name range, so no caller-built parameter or binder can inhabit it. Expansion
    /// names are minted only by `expand`'s crate-private fresh-name counter (§Internal 4).
    pub fn new(v: u32) -> Option<VarId>;   // None ⇔ v ≥ EXPANSION_NAME_BASE
}
#[derive(Clone, PartialEq, Eq, Hash)] pub struct TypeKey(Endset);   // a registered/reserved type, named by its key endset

/// A type position: a concrete cataloged type OR a class variable bound by an enclosing `Reg`
/// quantifier (V-IDX). Reg-expansion (type_check) substitutes ClassVar(cvar) → Concrete(class) per
/// registered class, so a TypedTerm's evaluable projection holds ONLY Concrete refs (the evaluator
/// never sees a ClassVar).
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
    Ref{addr:Address, args:Vec<ArcTerm>},        // ASN-0130; only inside stored-def bodies — ref-bearing ⇒ is_ref_free=false
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

A `Forall/Exists` whose `dom` is `Dom::Reg` binds `var` as a **class variable**, referenced inside `body` *only* through `TypeRef::ClassVar(var)` (Reg being outside COD, a class var is never a `Term::Var` value); `Reg`-expansion substitutes it away at type-check. Every other `Forall/Exists` binds a value/tuple var. QD-refl's address-valued domain→term reflection is the **`Term::Reflect(ArcDom)`** former: it reflects *any* address-valued domain (`L_dom`, a filter over an address-valued domain, a set-valued term, `M_K`) as a `℘_fin(T)`-valued term denoting `[D]_Σ`, so a value-returning def body like `{x ∈ L_dom : is_doc(x)}` (= `Reflect(Filter{LinkDom, is_doc})`) is representable; `M_K` *additionally* has its dedicated view-parameterized twin `Atom::Members(TypeRef)` (the direct M7 read). Tuple-valued (`A_K`/`L_K`) and class-valued (`Reg`) domains are **not** reflectable — they reach term position only through the `Dom`-accepting formers (`Exists`/`Forall`/`Count`/`BigUnion`/`SetTerm`). With `Reflect`, the AST is denotationally complete over QD-refl (§Internal 1).

`TypedTerm` is the **post-type-check** form. Its *evaluable projection* is post-`Reg`-expansion: every `Forall/ExistsReg` is rewritten to the finite `And/Or` of its concrete-class instances and every `TypeRef::ClassVar` substituted to `Concrete`, so the evaluator never sees a class variable nor a `ClassVar` type-ref, and `count(Reg)` is a `Lit`. It carries, alongside the synthesized codomain `Sort` per node (an immutable side-table or annotated tree): the **ordered parameter context `Γ_D`** it was checked under (read back via `TypedTerm::params() -> &[(VarId, Sort)]` and `result_sort()`); a **ref-free flag** (`TypedTerm::is_ref_free() -> bool`, false iff any `Ref` node survives — every PL evaluator *but* `evaluate_def` requires it true); **and the original pre-`Reg`-expansion syntactic body** (`TypedTerm::source_body() -> &Term`, the compact canonical form `define_predicate` encodes — §Internal 4, with its `Reg`-quantifiers and `ClassVar` refs intact), distinct from the expanded evaluable tree the evaluator walks. `TypedTerm` deliberately carries **no view** (PR-VIEW): the view is an evaluation/classification parameter (`eval`/`classify`), never a term annotation.

### Values, sorts, signatures

```rust
pub enum Sort { Bool, Addr, AddrSet, OptAddr, AddrSeq, Map, Nat, OptNat, Tup }   // COD ∪ {Tup}
pub enum Value {
    Bool(bool), Addr(Address), AddrSet(im::OrdSet<Tumbler>), OptAddr(Option<Address>),
    AddrSeq(im::Vector<Address>), Map(im::HashMap<CoverageClass,Address>),
    Nat(Nat), OptNat(Option<Nat>), Tuple(Tuple),                                  // Tuple binds a Tup var
}
pub struct Signature { pub params: Vec<(VarId, Sort)>, pub result: Sort }         // (Γ_D, C_D); each param sort ∈ COD

/// Eval environment: free-param + quantifier/Let-bound VarId → Value.
pub struct Env { /* im::HashMap<VarId, Value> */ }
impl Env { pub fn empty() -> Env; pub fn bind(&self, v: VarId, val: Value) -> Env; pub fn get(&self, v: &VarId) -> Option<&Value>; }

/// classify(t, view)'s output — all static, sound-but-incomplete. `footprint`/`stability`/
/// `active_exceptions` are RELATIVE TO classify's `view` argument (PC3 binds the view-parameterized
/// constituents to it); `view_independent` alone is view-agnostic (the PR-VIEW syntactic scan).
pub struct Dynamics { pub footprint: Footprint, pub stability: Stability,
                      pub active_exceptions: ActiveExceptions, pub view_independent: bool }
pub enum Stability { StSf, StOnly, SfOnly, Neither }        // 4-point lattice (ST∩SF / ST / SF / neither)
pub struct Footprint { /* read slices: per-type {active,audit}, L_R, residence dom, home-frontier flag */ }
pub struct ActiveExceptions { pub retraction_shrinks: bool,        // (i) any R-deposit can shrink an active slice
                              pub bh4_home_frontier: bool,         // (ii) BH4 moves with same-home deposits
                              pub targets_keyed_cross_type: bool } // (iii) targets_keyed is cross-type
```

Note `Signature.params` is **Codom-only** (each param sort ∈ COD): a stored def's parameters are bound by `evaluate_def` to *values*, never a tuple — the `Tup`-parameter latitude lives only in the rule-trigger path (`type_check_trigger`), whose result a `Signature` never describes. Set values are `im::OrdSet` (cheap union for `⋃`-folds, dedup = set semantics for `count`); sequences `im::Vector`; the `targets_keyed` join an `im::HashMap` keyed by M7's `CoverageClass`. `im` here buys cheap intermediate values during a fold, not journaled snapshots (those come pinned from M7/M3 slices).

### The type catalog (immutable, build-time-shared)

M9 is constructed (above) with the **same** `(ReservedAddrs, Vec<TypeDecl>)` that seeds M7's `LinkState::genesis` **and the one engine-built `Arc<TypeRegistry>` behind that genesis-sealed config** (the M7↔M9 build-time coordination point). M9 **does not rebuild the registry** (item 2): it receives that instance and folds it — together with the type-key endsets — into a frozen **`TypeCatalog: HashMap<TypeKey, (CoverageClass, Registration)>`** keyed by the verbatim **type-key endset**, plus the five `ShippedType` endsets. The catalog's five **shipped-type `Registration`s are not drawn from `decls`** — they are the genesis-seeded registrations the injected registry already carries (installed *before* the app decls: `retired = Unary/{ReadFilter}`, `supersedes = Binary/{Walk}`, `retraction = Binary/{}`, and — by the PredLayer agreement — `pred_def`/`pred_stable = Unary/{}`); M9 projects that same seeded shipped set, so a behavior guard such as `Succs ⇒ Binary/Walk` resolves against the *shipped* registration identically to M7. There is thus **one** registry across the link subsystem and M9 — no second deterministic build, no divergence trap (item 2). The five `ShippedType` endsets are each computed **once** as `enc(&[reserved.X])` (e.g. `pred_def ↦ enc(&[reserved.pred_def])`) — **coverage-equal** to M7's `reserved_type` by construction (byte-identical in fact, both being `enc(&[reserved.X])`, but only coverage-equality is *required*: M7's `emit`/typed reads identify a type by coverage (I0), so even a non-`enc` stored key would still accept M9's `enc` endset) — and M9 exposes them through its **own** catalog accessor `reserved_type(ShippedType) -> &Endset` (over the cached table, no snapshot), the `&Endset` every `emit(d, reserved_type(…), …)` / PL-`TypeKey` construction reads; this is distinct from M7's snapshot-bound `LinkState::reserved_type`. Keying by `TypeKey` (not by `CoverageClass`) is load-bearing for the guard in item below: a catalog lookup is a plain `Endset`-equality probe that **both authorizes a TypeKey and yields its *precomputed* `CoverageClass`** (computed once at build via `coverage_class` over the genesis-validated, address-denoting keys), so M9 *never* calls M7's `coverage_class` on unvalidated input. This is a *cached copy of genesis-immutable data* (R1 — constant at every reachable state), so it never goes stale; it backs type-checking and footprint analysis without a runtime M7 read. **Caller contract (made explicit — item 5):** because the probe is `Endset`-equality while M7's type identity is by *coverage* (I0), a `TypeKey` built from a coverage-equal but byte-different endset misses as `UnregisteredType`; so every PL-term `Concrete` `TypeKey` **MUST** be built from a canonical catalog endset — `reserved_type(ShippedType)` for a shipped class, the caller's own `TypeDecl.key` for an app class (both verbatim in the catalog). (M9 *could* instead canonicalize a probe key via `coverage_class` before the lookup, but that reintroduces a `coverage_class` call on unvalidated input — exactly what `TypeKey`-keying exists to avoid — so the verbatim-endset contract is preferred.) (If M7 later exposes `registration_of(&Endset)`, the catalog is replaceable by that read — same answer.)

### Hints / working sets (all recomputable)

| structure | shape | recovered from |
|---|---|---|
| `DefMemo` | `addr → (Signature, ResolvedBody)` + `addr → ExpandedTerm` | M4 content (immutable; `ResolvedBody` = the decoded **compact** body; **`Some`-or-permanent-poisoned only** — a not-yet-ever-registered addr is never cached; an ever-registered start whose content fails the PR-ENC parse/WT is cached as a permanent **poisoned** entry, §Internal 4) |
| active/ever pdef lookup | *delegated to M7* `is_K(pdef, start)@{active,audit}` (`is_k` / `observe(pdef, slice::from_ref(start), &[], Audit)`) | M7 spanfilade |
| `RuleRegistry` | `RuleId → CheckedRule` (the internal **`TypedDom`** + validated trigger + view + action — §Internal 5) | re-registered by the coordination layer (effects already durable in M7) |
| agenda (optional) | enabled `(RuleId, x)` set | full Q0 scan / journal replay |
| `FireCounters` | `(RuleId, x) → u64` | replay of M7 deposits + re-evaluation |
| `ArmerGraph` | `RuleId → RuleId` (emits-type ⇝ reads-type) | static, from the registry + footprints |

The **active-pdef-by-start index is *not* materialized by M9** — M7 already indexes `pdef` in its spanfilade, so a per-start `is_K(pdef, start)@{audit,active}` probe (`observe(pdef, slice::from_ref(start), &[], Audit)` / `is_k(pdef, start)`) answers ever/active-registration directly (the one index ASN-0130 "forces" is served upstream). M9 keeps only content-derived memos and the rule working set.

**Interior mutability of the hint caches.** `signature`, `define_predicate`, and `register_pred` take `&self` yet populate the `DefMemo` (memoize a freshly-derived `Some` signature / resolved body / expanded term), so the `DefMemo` is held behind **interior mutability** (a `RwLock` or a concurrent map — **not** a `RefCell`: a `Coordinator<W>` over the `Send + Sync` factories and `Arc<Kernel<W>>` is naturally `Sync`, and `RefCell` is `!Sync`, so it would not compile across the `&self` `signature`/`define_predicate`/`register_pred` API of a shared `Coordinator`), never `&mut self`. This is sound precisely because every memo entry is an *immutable-once-defined hint* (a `Some` — or a poisoned marker — is permanent; §4): concurrent fills race only to write the same value. **`FireCounters` are authoritative-via-journal-replay, not via the cache:** the true per-`(ρ,x)` fire count is recoverable by replaying M7's deposits (the counter table is a recomputable hint — see the table), so a direct `&self` `fire` that does *not* touch the cached counter is still fully covered by the divergence monitor, which recomputes from the journal (a `Deduped`/`NoOp` fire deposits nothing, so it leaves no journal record and is correctly excluded from the authoritative count). The cached counter is only a latency optimization over that authoritative recompute.

### Errors & outcomes

```rust
pub enum TypeError {
    UnboundVariable(VarId),                        // a free Var outside the supplied Γ_D (the missing-context case)
    UnboundClassVar(VarId),                        // a TypeRef::ClassVar under no enclosing Reg binder (V-IDX)
    TupParameter(VarId),                           // a DEF-PATH Γ_D parameter sorted Tup — excluded from Codom
                                                   //   (ASN-0130 SignedTerm); the trigger path (type_check_trigger) admits one
    SortMismatch { expected: Sort, found: Sort },
    BehaviorMissing { ty: TypeKey, needs: Behavior },  // an atom needs a behavior the (concrete) type's registration lacks
    UnregisteredType(TypeKey),                     // concrete TypeKey absent from the catalog (subsumes non-address-denoting:
                                                   //   every cataloged key is genesis-validated address-denoting; also the
                                                   //   coverage-equal-but-byte-different miss, since the probe is Endset-equality)
    NoReverseLookupClass,                          // class-unindexed `targets_keyed` used, but no cataloged class attaches BH3 (V-atom)
    DanglingReference(Address),                    // Ref to an address with NO DEFINED SIGNATURE (WT-ref domain failure):
                                                   //   never-registered, or ever-registered-but-undisciplined (§Internal 4)
    RegInstanceIllTyped(TypeError /* boxed */),    // a Reg-quantified body has an ill-typed concrete instance (V-IDX)
}
pub enum DefineError    { Insert(TxnError<InsertError>), Register(RegisterError), Supersede(TxnError<EmitError>) }
pub enum RegisterError  { NotResident, ParseFailed, IllTyped(TypeError),
                          ReferentNotEverRegistered(Address), ReferentNotActive(Address),
                          HomeNotRegistered, Emit(TxnError<EmitError>) }
pub enum EvalError      { NotEverRegistered,
                          UndisciplinedDef,      // ever-registered start whose immutable content fails the PR-ENC parse/WT —
                                                 //   reachable only under a PR-DISC breach (§Internal 4)
                          ArgArityMismatch, ArgSortMismatch }
pub enum CertifyError   { NotEverRegistered, NotBoolean, NotActive, ViewDependent, NotStable, Emit(TxnError<EmitError>) }
pub enum RetractError   { NotActive, Nullify(TxnError<NullifyError>) }            // NotActive: no active pdef tuple (item 8)
pub enum FireError      { HomeNotRegistered, Emit(TxnError<EmitError>), Nullify(TxnError<NullifyError>) }  // HomeNotRegistered shared by Marker emit + Nullify
pub enum RuleError      { RefBearingInlineTrigger,                                // Inline must be ref-free; persist-as-def + `Def` works only for a Codom-param trigger — a tuple-domained trigger must inline the helper
                          RefBearingDomain,                                       // a Ref inside the rule domain (Filter/SetTerm body) — no Def escape for domains; inline the helper
                          IllFormedDomain(TypeError),                             // rule.domain fails the WT-domain + Reg-expansion pass (incl. a BARE Reg domain — sort check)
                          DomainTriggerSortMismatch { expected: Sort, found: Sort }, // trigger param sort ≠ domain element sort
                          TriggerNotBoolean,                                      // trigger codomain ≠ Bool
                          DefTriggerUnregistered(Address),                        // TriggerRef::Def addr has no defined signature (never-registered or undisciplined)
                          BadTriggerArity,                                        // trigger not single-parameter
                          BadMarkerType(TypeKey),                                 // Marker.ty not a cataloged Unary type
                          PredLayerMarkerType(TypeKey) }                          // Marker.ty ∈ {pdef, pd_stable} — PR-DISC reserves
                                                                                  //   those slices for register_pred/certify_stable

pub struct RuleId(u64);
pub struct Enabled { pub rule: RuleId, pub arg: Value }      // (ρ, x); Value::{Addr | Tuple} per the domain sort
pub enum FireOutcome { NoOp,                                  // trigger false at fire time (Q1)
                       Fired   { effect: Address, seq: Seq }, // a real, fresh deposit (advances the divergence count)
                       Deduped { effect: Address, seq: Seq } } // an idem⊤ dedup hit in the trigger-check↔commit gap: M7
                                                              //   committed NOTHING, returned an incumbent — NOT counted
pub enum StepOutcome { Fired   { rule: RuleId, arg: Address, seq: Seq },
                       Deduped { rule: RuleId, arg: Address, seq: Seq },          // a `fire` that dedup-hit (no real fire)
                       NoOp, Quiescent }
pub enum RuleCertification { CertifiedTerminating,
                            Uncertified { sf: bool, marker: bool, grow_only: bool } }
pub enum ScopeBody { PerEmitter, PerTarget, PerSource, PerAddress }

// `?`-conversions the bodies need:
impl From<TxnError<InsertError>> for DefineError   { /* ::Insert */ }
impl From<RegisterError>         for DefineError   { /* ::Register */ }
impl From<TxnError<EmitError>>   for DefineError   { /* ::Supersede (supersede's supersedes-emit) */ }
impl From<TxnError<EmitError>>   for RegisterError { /* ::Emit */ }
impl From<TxnError<EmitError>>   for CertifyError  { /* ::Emit */ }
impl From<TxnError<NullifyError>> for RetractError { /* ::Nullify */ }
```

**Tuple-domain bookkeeping key.** `Enabled.arg` is a `Value` (`Value::Addr` for an `Addr`-domain rule, `Value::Tuple` for a `Tup`-domain rule), but `fire_count(rule, x: &Address)` and `StepOutcome::{Fired, Deduped}.arg: Address` are `Address`-typed: for a `Tup`-domain rule the bookkeeping **key** and the report are the bound tuple's **`t.addr`** (tuples are address-identified — R1 AddressInjectivity, ASN-0086 — so the projection is total and collision-free); for an `Addr`-domain rule it is the bound address itself. `Enabled` keeps the full `Value` because the trigger/atom dispatch consumes the whole tuple; only the *bookkeeping* projects to the address.

---

## Internal design

### 1. Term representation & the type checker (incl. `Reg` expansion)

A single **bottom-up (post-order) synthesis pass** over the raw `Term`, **checked under the caller-supplied ordered parameter context `Γ_D`** (ASN-0129 WT is a Γ-parameterized *checking* judgment, not a free synthesis). The parameter-sort policy is **split by use**: the **def-path `type_check`** rejects any `Γ_D` parameter whose sort is **not** a codomain — a `Tup`-sorted parameter (`TupParameter`), since a stored def's parameters are bound by `evaluate_def` to *values* and a tuple is never a term value (ASN-0130 SignedTerm); the **trigger-path `type_check_trigger`** is identical *except* it admits a single `Tup`-sorted parameter, because a rule fires by binding its domain element — which for a tuple domain (`A_K`/`L_K`, ASN-0133 `ρ_R`) is a `Value::Tuple` — to the trigger's one parameter, and the V-TUP atoms (`TupAddr`/`TupAddrsF`/…) consume it. ASN-0129 WT itself admits `Tup`-sorted context variables, so this is the note's own latitude; the Codom-only restriction is real only for the stored-def path. The context `Γ` is then **seeded with `Γ_D`** — the free parameter `VarId → Sort` map, kept in positional order so the result `Signature.params` re-emits Γ_D faithfully — and **extended** with bound vars under quantifiers/`Let`/the binder guard (including `Tup` for tuple binders consumed only by V-TUP). Each former has one match arm transcribing its WT rule: connectives `Bool→Bool`; quantifiers `Bool` from `D dom(s)` + body at `Bool`; plain composition substitutes a child sort into a context; the **binder guard** `IfSome` narrows `T∪{⊥}→T` (resp. `ℕ∪{⊥}→ℕ`) in its then-branch via the V-PRIM `def` test; `Count:ℕ`, T1-extrema at `T∪{⊥}`, `⋃:℘_fin(T)`. (QD-refl's address-valued domain→term reflection is the `Reflect(D)` former: `Γ ⊢ Reflect(D) : ℘_fin(T)` from `Γ ⊢ D dom(Addr)`, so `L_dom`, a filter over an address-valued domain, and any set-valued term reach term position directly — a tuple-valued (`A_K`/`L_K`) domain is rejected at the element-sort check (`SortMismatch{expected: Addr, found: Tup}`), and the class-valued `Reg` domain, being quantification-only (V-IDX), has no `Reflect` and is likewise rejected. `M_K` *also* carries its dedicated view-parameterized twin `Atom::Members`. The membership/emptiness *tests* on `L_dom`/filtered domains may be spelled either via `Reflect` and V-PRIM (`SetMem(t, Reflect(D))`, `IsEmpty(Reflect(D))`) or directly through the `Dom`-accepting formers: `t ∈ L_dom` is `Exists{var, dom: LinkDom, body: AddrEq(Var(var), t)}`, `L_dom = ∅` is its negation `¬∃` (equivalently `Count(LinkDom) ≤ 0`), a non-empty test the bare `∃`. **Emptiness is best spelled `¬∃` (or `count ≤ 0`), not `count = 0` — an authoring-precision recommendation, not a well-formedness rule: `count = 0` type-checks fine, the certifier merely lands it in `Neither`:** PD0 places `count(D) = c` in *neither* stability class — only `count ≥ c ∈ ST` and `count ≤ c ∈ SF` — so an `=`-spelled emptiness needlessly forfeits certification precision: a `¬∃` over a grow-only `L_dom` is `SF`, an `= 0` is unclassified.) A `Var` resolved in neither Γ_D nor a binder is **`TypeError::UnboundVariable`** (the missing-context failure mode). Every side condition is a finite match against the static `Codom`/catalog (V-STAT), so the pass **reads no structural state for a ref-free body and is decided once at construction**, valid at every reachable state (WT).

**Atom typing (TypeRef resolution + catalog guard + behavior guard).** Typing an `Atom` (or a `Dom`/`MapGet`) that names a `TypeRef`: a `TypeRef::ClassVar` is valid *only* under an enclosing `Reg` binder that `Reg`-expansion has not yet reached — at the point an instance is type-checked every such ref is already `Concrete`, so a surviving `ClassVar` is rejected **`UnboundClassVar`**. For the `Concrete(k)`: (i) **look `k` up in the cached catalog** — absent ⇒ `TypeError::UnregisteredType`, which *also* rules out a non-address-denoting key (every cataloged key is genesis-validated address-denoting). The lookup is `Endset`-equality, so `k` **must be a verbatim catalog endset** (`reserved_type`/the caller's own decl key) — a coverage-equal but byte-different key misses as `UnregisteredType` (caller contract, §Core data model / §Invariants). This is the single guard that makes every later `coverage_class(ty)`/`MapGet` keying total: only cataloged (registered, address-denoting) **concrete** keys ever reach the evaluator, which keys `Map_fin` lookups through the catalog's *precomputed* `CoverageClass`, never a runtime `coverage_class` on user input. (ii) Check the registration supports the atom's behavior (e.g., `Succs` requires BH2/Binary), else `TypeError::BehaviorMissing`. The class-unindexed **`Atom::TargetsKeyed`** (the BH3 join, which names no `TypeRef`) carries its own guard: it is in the vocabulary only when *some* cataloged class attaches BH3 (V-atom: `targets_keyed` is in `V_atom` iff some class attaches BH3), so with no BH3 type shipped (v1) a bare `TargetsKeyed` is rejected **`NoReverseLookupClass`**; an *indexed* `MapGet(TargetsKeyed(s), Concrete(K))` instead routes the BH3 requirement through (ii)'s per-atom behavior guard on `K` (`BehaviorMissing{ty: K, needs: ReverseLookup}` when `K` is not BH3/Binary).

**`Reg` expansion (V-IDX).** On `Forall/ExistsReg{cvar, dom: Reg, body}`, instantiate `body` once per registered class in the catalog (finite, fixed) — **substituting `TypeRef::ClassVar(cvar) → TypeRef::Concrete(class)` throughout `body`** — type-check each instance, and emit the `And/Or` of the well-typed instances as the `TypedTerm`'s evaluable projection (nested `Reg` binders each substitute their own `cvar`). Well-formedness is *instance-wise*: a body applying a class-indexed behavior atom (`succs`, `target_of`, …) at the bound class is well-typed only if **every** class carries that behavior — discovered by instantiation (the mandatory `R` instance, behaviors=∅, kills any such body, surfaced as `RegInstanceIllTyped`). The one survivor is the class-unindexed `targets_keyed(s)[K]` join — `MapGet(TargetsKeyed(s), ClassVar(cvar))` (well-typed whenever *some* class attaches BH3, the body never applying an atom a class may lack). Expanding here hands the evaluator a plain finite tree whose every `TypeRef` is `Concrete`. (`Count(Dom::Reg)` is the one `Reg` use without a class-variable body: it folds to a `Lit` — the registered-class count, constant by R1/C0.) **`Reg` is admissible under exactly two formers:** `Forall`/`Exists` (where `type_check` expands it away) and `Count` (which folds to a `Lit`). Every *other* `Dom`-accepting former rejects a `Reg` domain at the element-sort check — `Reflect`, `MaxT1`, `MinT1` (each needs an address-valued domain), `BigUnion` (PC2a explicitly excludes `Reg` from `⋃`), and `Filter` (PC1 admits only an address- or tuple-valued domain). `Reg` has no *term* form at all (it is class-valued, outside COD), so it never reaches `SetTerm` — which wraps a `℘_fin(T)`-valued term — nor any value position. The **original compact body** (with its `Reg`-quantifiers and `ClassVar` refs intact) is **retained on the `TypedTerm`** as `source_body()` for canonical content encoding (§4); only the *evaluable* projection is expanded.

**References (WT-ref).** A `Ref{addr, args}` types to `C_r` where `signature(addr) = (⟨xᵢ:Cᵢ⟩, C_r)`, each `argᵢ` checks at `Cᵢ`, and `addr` has a defined signature. A reference to an address with no defined signature — never-registered, or ever-registered-but-undisciplined (§4) — has *no* typing judgment → `TypeError::DanglingReference`. Signature lookup is the only external consultation, and it reads the (immutable) sig memo — so even ref-bearing type-checking is "decided once." **A surviving `Ref` makes the `TypedTerm` ref-bearing** (`is_ref_free() == false`): such a term is admissible only as a stored-def body via `define_predicate`; `eval`/`decide`/`classify` and `TriggerRef::Inline` require ref-free, and `register_rule` rejects a ref-bearing `Inline` trigger (`RuleError::RefBearingInlineTrigger`).

*Tradeoff.* Reified AST + full `Reg` expansion costs term-size (a body × |classes|) and an O(tree) check, bought back by syntax-directed footprint/stability passes that would be impossible over closures, and by re-check being free forever. The expansion blowup is confined to the *in-memory* evaluable projection — the *stored* `Val` holds the compact body (§4).

### 2. The pure evaluator

A **syntax-directed tree-walk** threading `(env: Env, view, snap)`. **Precondition: the `TypedTerm` is ref-free** — `eval` has *no* `Ref` arm; a surviving `Ref` is a precondition violation (panic, exactly as `decide` panics on a non-Bool codomain). By the post-expansion invariant the walk also sees only `Concrete` `TypeRef`s and no `Reg` quantifier. Ref-bearing terms are evaluated only by `evaluate_def`'s DAG-recursive driver (§4), which is `eval`'s walk *plus* the one `Ref` arm. Reads route **only** through M7 (`snap.world().links()`) and M3 (`snap.world().m3()`) — never content or arrangement dereference — which is exactly what discharges *structural-reads-only* as a wiring discipline (PC4). Every constituent read of one verdict comes off the **single pinned `Snapshot`**, discharging the multi-read soundness obligation (ASN-0134/M2 clause 6) by construction.

**Atom dispatch** (the load-bearing table — view threaded; every `K` concrete):

| PL atom @ term view *v* | M7/M3 read |
|---|---|
| `members(K,active)` / `targets_of(K,x,active)` / `M_K` @ active | M7 `members(K,Active)` / `targets_of(K,x,Active)` |
| `members(K,audit)` / `targets_of(K,x,audit)` / `M_K` @ audit | **rebuilt from `observe(K,&[],&[],Audit)` per V-AUD's own equations** — members: `⋃ t.from.addrs()`; `targets_of(x)`: `⋃ t.to.addrs()` over tuples with `x ∈ t.from.addrs()` (AM exact denotation) — so the audit core-atom reads ride the same `observe` seam, with no second audit-honoring method assumed |
| `members(K,default)` / `targets_of(K,x,default)` | M7 `members(K,Active)` / `targets_of(K,x,Active)`, then drop elements `x` with `∃ J ∈ Φ, J ≠ K :: is_k(J, x)` — **per-type BH1 filtering via `is_k`** (UV self-exclusion, never `K`'s own; `is_filtered_J` ≡ `is_k(J,·)`, D2); v1: Φ = {retired} ⇒ `K = retired` unfiltered (OQ1), `K ≠ retired` drops `is_k(retired,·)` — see **View handling** |
| `is_K(x)` @ active/default | `is_k(K,x)` |
| `is_K(x)` @ audit | `!observe(K, slice::from_ref(x), &[], Audit).is_empty()` |
| `A_K` / `L_K` (tuple domains) | `observe(K,&[],&[],Active)` / `…Audit` → `Vec<Tuple>` |
| `L_dom` | `⋃_{K∈catalog} observe(K,&[],&[],Audit) ↦ t.addr` — within M9's declared M7 surface (Observe + BH1–BH4 + is_k/members/targets_of), **not** M8's `type_slice`; every *gated* tuple carries a cataloged type (P6), so this is exactly the gated sublayer's `dom(Σ.L)`. **PL's `L_dom` ranges over the typed-relation sublayer of M7's assembled `LinkState` and excludes MAKELINK open content links** (whose type slots are uncataloged content extents; ASN-0129's Σ.L is the gated store) — and so therefore do `Addr`-over-`L_dom` rule domains and the reflected residence disjunct |
| `is_filtered_J(x)` | `is_k(J, x)` — definitionally BH1's `is_filtered_J` (D2: J's own active membership predicate); per-type-correct for any Φ (M7's aggregate `is_filtered` coincides only while Φ is a singleton — it is used nowhere here) |
| `succs`, `chain`, `tip`, `is_in_chain` | `succs`, `chain`, `tip`, `chain(K,x).contains(t)` |
| `sources_to`, `target_of`, `targets_keyed` | identical M7 BH3 reads (`targets_keyed`'s map keyed by `CoverageClass`; `·[K]` indexes via the catalog's precomputed class for `K`) |
| `age(K,a)` / `stale(K,h)` | `observe(K,&[],&[],Active).iter().any(|t| t.addr == a) ? M7::age(a) : ⊥` (ASN-0129 BH4 totalization: `age(a) = ⊥` exactly when `a` is **not the address of an active K-tuple** — a tuple-identity test, *not* `is_k`'s coverage-of-F membership; M7's `age` is type-agnostic) / `M7::stale(K, clamp_u64(h))` (**saturating** `Nat→u64`: clamp to `u64::MAX`, so a horizon `≥ 2^64` ⇒ `stale = ∅`, all non-stale — never a wrapping truncation that would spuriously mark fresh tuples stale). Dormant in v1: no BH4 type cataloged ⇒ `Age`/`Stale` cannot type-check |
| `is_doc(d)` | **M3** `is_registered_document(d)` |
| V-TUP / V-PRIM | pure, on the bound `Tuple` value / by arithmetic — no state read |

**Audit-slice reliance — one primitive.** Every audit read — `is_K@audit`; the audit core-atom readings (`members(K,audit)`/`targets_of(K,x,audit)`/`M_K@audit`, deliberately **rebuilt from `observe(K,&[],&[],Audit)` via V-AUD's own equations rather than trusting a second `members`/`targets_of`-honors-`Audit` assumption**); `L_K`; `L_dom`; **and every ever-registration read** — passes `View::Audit` to `observe` and requires M7 to return the **audit** slice for it (ASN-0086's hist selector; `A_K`/`L_K` are `Observe_K`'s two selectable slices — the same audit slice M7's own `type_slice` exposes as "L_K (Audit)"). M7's interface prose describes `observe` as "over the active typed slice"; M9's audit reads are correct only because the `View::Audit` parameter selects the audit slice — a **single seam dependency named here** so an M7 build that ignored `Audit` (and silently returned active data for M9's audit reads) is caught at the boundary. Ever-registration is therefore routed through **`observe(pdef, slice::from_ref(start), &[], Audit)`** (= `is_K(pdef, start)@audit`) — *not* a separate, less-documented `members`-honors-`Audit` assumption — so the **whole** audit surface (the `register_pred` (iii) referent checks, `signature`/`evaluate_def`'s ever-registration precondition, `is_ever_pred`, and the ever/active hints) rests on the one `observe`-honors-`Audit` seam, with no second audit-honoring method assumed anywhere in the dispatch.

**View handling.** Core atoms + `M_K` take the *term* view; fixed-view atoms (BH1–BH4, `A_K`, `L_K`) read their named slice regardless. **The UV default-view rewrite is M9's** (M7 only filters `members`/`targets_of` and coerces other collection atoms to active). UV's `K_queried` self-exclusion is load-bearing — *a type never filters its own members* — so `members(K, default)` and `targets_of(K, x, default)` must drop elements filtered by the BH1 types **other than `K`**, never by `K` itself. M9 therefore does **not** delegate `members(K, default)` to M7 (whose `members(_, Default)` filters by the *aggregate* `is_filtered`, including `K` — wrong for `K = retired`, which would self-erase to ∅): it computes `members(K, active)` and drops the elements `x` with `∃ J ∈ Φ, J ≠ K :: is_k(J, x)` — **per-type BH1 filtering over the cataloged BH1 set Φ via `is_k(J, ·)`, which is definitionally BH1's `is_filtered_J`** (D2: the membership predicate on J's own active view), so the `K_queried` exclusion needs **no new M7 surface and is correct for any number of app-registered BH1 types**. In v1 the lone BH1 type is `retired`: `members(retired, default) = members(retired, active)` (unfiltered — the settled OQ1 commitment), and for `K ≠ retired` the drop is exactly `is_k(retired, ·)` (coinciding with M7's aggregate `is_filtered` and with M7's `members(K, Default)` — a coincidence that holds only while Φ is a singleton and off the self-query). `targets_of(K, x, default)` carries the same self-exclusion, but Unary `retired` has `targets_of(retired, ·) = ∅` at every view, so in v1 **only `members` is materially affected**. For the non-core collections — `succs`/`chain`/`sources_to`/`stale` in a `default` term — M9 drops elements `e` with `filtered(e)` (= `∃ J ∈ Φ, J ≠ K_queried :: is_k(J, e)`) from the *returned* collections, while `tip`/`is_in_chain` use the **unfiltered active walk** (verdicts/traversal never rewritten — UV). M7's aggregate `is_filtered` appears nowhere in the UV rewrite.

**Common case + short-circuit.** Most triggers are existence checks. `Exists` returns at the first witness, `Forall` at the first counterexample, `Filter` composes lazily over the materialized slice `Vec`. The full-pass folds — `Count` (single-pass accumulator), `MaxT1`/`MinT1` (the running **global T1-extremum over the address-valued domain** — PC2a's order-extremum, `⊥` at empty, composing through the binder guard), and `BigUnion` and `Reflect(D)` (each materializes an `OrdSet`; `Reflect` enumerates `[D]_snap`'s address denotation via the same base-domain reads as quantifiers/`Count` and returns it as the reflected `℘_fin(T)` value, QD-refl) — cannot short-circuit. (T1-extrema *are* global order extrema: T1 is M1's intrinsic total order on addresses and `max_{T1}`/`min_{T1}` read it directly. The "never read global emission order" caution is a separate **BH4 `age`/`stale`** ordinal-time doctrine — frontier-relative, home-denominated — not a constraint on T1-extrema.) **No feedback/loop former and no arbitrary fold accumulator is offered** — admitting either silently computes `reach`/parity and voids the closed ceiling (PC6a, OQ6).

**Incrementality.** The strong lever is *stability*, not blind memoization: a `⊤`-stable trigger that has fired never re-evaluates (§8). Per-`Snapshot` purity (PC4) makes results memoizable but the polling pattern rewards retiring settled triggers far more.

*Recovery.* Stateless — eval is a pure function of the pinned snapshot. No recovery surface.

*Tradeoff.* M7's `observe`/`members` return materialized `Vec`s, so M9 short-circuits *over* a materialized slice rather than avoiding materialization; a streaming M7 read would let `∃` stop earlier on huge slices (open, §Open).

### 3. The dynamics / stability analyzer

A **second bottom-up pass** (after type-check, over a **ref-free** `TypedTerm` with `Reg` already expanded and every `TypeRef` concrete), **parameterized by the term view `v`** (`classify(t, view)`): PC3 binds each view-parameterized constituent — the core atoms and `M_K` — to `v`, while fixed-view atoms read their named slices regardless, so the view-indexed FP/PD0 rules ("`M_K` *in an audit-view term*", audit vs active `is_K`, the per-view footprints) have a determinate reading. The emitted `footprint`/`stability`/`active_exceptions` are **relative to `v`**; `view_independent` is the view-agnostic PR-VIEW scan. The pass fuses FP footprint and PD0–PD2 stability per node.

- **Footprint** (`Footprint`): per atom — audit-slice atoms read `L_K`; active atoms read `L_K ∪ L_R`; BH4 adds the home-wide frontier of `home(a)`; `targets_keyed` reads every BH3-attached type's active slice; `is_doc` reads the residence domain; default-view collections (when `v = default`) add each BH1 type's footprint. A former's footprint is the union over its children (so `Reflect(D)`'s footprint is `D`'s).
- **Stability** (`Stability`, the 4-point lattice `StSf`/`StOnly`/`SfOnly`/`Neither`) by the PD0 mutual induction. The *grow-only* domain closure the certifier transcribes (its completeness reach): `L_K`; `L_dom`; `M_K` *in an audit-view term* (`v = audit`; V-AUD's union over the growing `L_K`); a `Filter{D, P}` with `D` grow-only and the body `P ∈ ST` for every binding; a *step-constant domain* (a set-valued term reading no state beyond bound parameters); plus the two derived set-valued grow-only forms — `targets_of(x, audit)` at a literal/already-bound argument (an `Atom::TargetsOf` at `v = audit`, or its explicit `observe`-rebuild spelling), and a `⋃(D, f)` fold with `D` grow-only and `f` step-constant per binding. On that closure: step-constants in `ST∩SF`; `is_doc`, audit `is_K` (`IsK` at `v = audit`, or its explicit `∃`-over-`L_K` spelling at any view), and grow-only membership (`t ∈ D`, incl. `SetMem(t, Reflect(D))` over a grow-only `D` at a literal/bound `t`) in `ST`; emptiness (`D = ∅`, incl. `IsEmpty(Reflect(D))` over a grow-only `D`) and upper-bound counts (`count(D) ≤ c`) in `SF`; lower-bound counts (`count(D) ≥ c`) over a grow-only `D` in `ST`; `¬` swaps, `∧`/`∨` preserve, `⇒` combines `SF⇒ST`; quantifiers/aggregates per grow-only/step-constant domain (a step-constant `D` strengthens both quantifier directions and puts every comparison in `ST∩SF`). T1-extrema are in neither, and `count(D) = c` is unclassified (so the certifier lands it in `Neither` — never over-certified).
- **The three active-view exceptions** (`ActiveExceptions`, emitted explicitly — "name them or be surprised"): (i) retractions can shrink *any* active slice; (ii) any **BH4** term moves with same-home deposits of any type (frontier advance); (iii) any `targets_keyed` term is cross-type by construction.
- **View-independence** (`view_independent`): the PR-VIEW syntactic scan — no view-parameterized constituent and no UV-rewritten collection atom — needed for certification; the same answer at every `v`.

The certifier is **sound but incomplete**: it classifies by spelling, surfaces "⊤-stable" / "not certified," and **errs toward not-certified** (over-certifying ⊤-stability would mislead a termination argument). Deciding extensional stability is open theory, not M9's job.

**ST⁺ (ASN-0130 certification).** `certify_stable` runs PD0 over the **flat `expand(start)`** (a ref-free term; its parameters — Γ_D from `sig(start)` — read as bound constants), with the aggregate threshold widened to *ℕ literal **or** bound ℕ parameter* (the one widening; a checker built to literal PD0 would wrongly refuse a certifiable `count(L_W) ≥ x`). **`certify_stable` is unaffected by `classify`'s view parameter:** it certifies only *view-independent* expansions (CVALID (ii)), for which the classification is view-invariant — the certifier passes any fixed view (say `Audit`) and gets the same answer. The certificate asserts every Γ_D-instantiation is ⊤-stable. Materializing the flat term here is mandatory: **ST⁺ is not compositional** — a per-referent ST⁺ cache reused at a call site is *unsound* (`helper(x)=count(L_W)≥x ∈ ST⁺`, but `helper(count(L_X))` flips), so each call site's actual arguments must be substituted into the referent's body before classifying that node. Certification is rare, so the flat-materialize cost is acceptable.

### 4. Predicate definitions as content

**Encoding (n=1).** Because M4 stores arbitrary-size byte `Val`s, a definition is **one `Val` at one content address** — the "contiguous run" of ASN-0130 collapses to a single address (`n=1`), making prefix-freeness/self-delimiting and identity-by-start *trivial* (the `Val`'s own byte length delimits the parse; the start *is* the only address). The `Val` holds a deterministic, decidable, **injective** serialization of the signed term `(Γ_D, body)` — where **`body` is the compact pre-`Reg`-expansion syntactic body** (`TypedTerm::source_body()`, in ASN-0129's grammar *including* `Reg`-quantifiers), the canonical PR-ENC form — encoded as a **length-prefixed envelope** (varint length · param context · body, recommended) so "the run is exactly what the parse consumed" is a one-line check. **Injectivity (`decode∘encode = id`, PR-ENC's encoding discipline) is required, not merely determinism** — identity-by-start (§Invariants) and `register_pred`'s idem dedup both lean on distinct terms encoding to distinct `Val`s. The codec treats a **reserved-range `VarId`** (`≥ EXPANSION_NAME_BASE`) in a decoded parameter context or body as **`ParseFailed`** — the range is not encodable input, so stored defs cannot smuggle expansion names. So a `∀K∈Reg` def stores *one* body, not `body × |classes|`; the `Reg`-expansion is re-run on read-back (re-deriving an identical `sig`/denotation — not load-bearing, only canonical-form-faithful and storage-compact, item 4). Byte-granular multi-address runs (one token per address) remain a supported generalization for a byte-stream content model, but are not the v1 encoding.

**Store + register.** `define_predicate(d, term)` (`term: TypedTerm`, carrying its Γ_D and `source_body()`):
1. Encode `(term.params(), term.source_body())` → `blob: Val` (the compact body, §Encoding).
2. Read `n_C(d)` off a snapshot; `let (a, _insert_seq) = vstream.insert(d, VPos{ subspace: s_C /*=1*/, ordinal: n_C+1 }, vec![blob])?;` — M5's placement composite mints (M3), writes bytes (M4), splices, appends R, **atomically (J0/J1★, run-contiguity by construction)**; `a` = the def identity (`?` lifts `TxnError<InsertError>` via `From … for DefineError`). The `vstream` handle is minted off `Arc<Kernel<W>>` via the engine-injected factory (§Public interface).
   - **Insert-position TOCTOU (benign, item 6).** `at = VPos{ s_C, n_C+1 }` is computed off the snapshot read of `content_count(d)`, then M5's `insert` re-validates `at` against *committed* state inside its own composite. Two interleavings: a concurrent INSERT that grows `d` first lands this def **mid-document** — harmless, since the def's identity is the *returned start address* `a`, not its ordinal; a concurrent DELETE that shrinks `n_C` below `at` yields a clean **`Insert(Rejected(BadPosition))`** — a retryable transient (recompute `n_C`, re-insert), **not** a logic error. A builder must treat the `BadPosition` rejection as retry-the-position, never a defect.
3. `let (_pdef, seq) = self.register_pred(d, &a)?;` (`?` lifts `RegisterError`). **Returns `(a, seq)` — the def identity and the `pdef` emit's commit `Seq`, never the insert's.**
   - **Orphan-on-`register_pred`-failure (benign, item 6).** Steps 2 and 3 are separate transactions; if step 3 rejects, step 2's content is already committed — an **orphan def-content run with no `pdef` tuple**, exactly the harmless-orphan pattern of `create_new_document`'s un-arranged document (content is permanent/immutable but simply unreferenced; a later `register_pred(d, a)` against the same start adopts it, idem⊤ giving ≤1 active pdef).

`register_pred(d, start)` validates **gate-first, against one pinned snapshot σ** (single-coherent-pre-state):
- **(0/i/ii)** parse `value_at(start.tumbler())` off σ → `(Γ_D, body)` (the compact body, re-`Reg`-expanded and WT-checked); failure ⇒ `NotResident`/`ParseFailed` (one `Val`, residence + extent + fully consumed).
- **(iii)** WT+WT-ref under σ (`IllTyped`); each referent `r` ever-registered via `is_K(pdef, r)@audit` (= `!observe(pdef, slice::from_ref(r), &[], Audit).is_empty()`; else `ReferentNotEverRegistered`); sigs via the resolver (an ever-registered-but-undisciplined referent has no defined signature ⇒ `IllTyped(DanglingReference(r))`).
- **(iv) endorsement**: each referent `r` actively registered via `is_K(pdef, r)@active` (= `is_k(pdef, r)`; else `ReferentNotActive`).
- **(P0)** `m3.is_registered_document(d)` (else `HomeNotRegistered`).
- valid ⇒ `emit(d, reserved_type(PredDef), start, &[])` (Unary ⇒ `to = &[]`; `from` is the single `&Address` M7 forces, `|F|=1`); idem⊤ dedups to ≤1 active `pdef` per start. Invalid ⇒ typed rejection, **no emit** (rejection asserts nothing about a standing registration).

**Two-transaction soundness.** The validation reads (against σ) and the emit (M7's own transact at σ′) are **two transactions** — M7 exposes only a transact-wrapped `emit`, so M9 cannot fuse them. Of VALID's conjuncts, parse/extent (0,i,ii) and well-typing + ever-registration (iii) are content-intrinsic and monotone, hence stable σ→σ′ (PR1(ii),(iii)); **only endorsement (iv) — a referent's *active* `pdef` tuple — can be nullified in the gap.** So the split **weakens PR1(iv) from a *deposit-time* guarantee to a *validation-time* one.** That is sound for M9 because **evaluation keys on *ever*-registration and never on endorsement currency** (the standing PR1 discipline): a gap-de-registered referent yields only a dangling-but-live reference, which M9's no-cascade semantics already permit. We explicitly do *not* assert PR1(iv)'s post-deposit guarantee here (that would demand re-validating at σ′), and we make no claim about pre-deposit de-registration, which sits outside PR-DISC's deposit-branch reading.

**Discipline (PR-DISC).** PR1/PR2/PR-SIG and their consequences hold on **registration-disciplined derivations** — every `L_pdef`-growing step `register_pred`'s deposit branch, every `L_pd_stable`-growing step `certify_stable`'s. In-module, `register_rule` closes the one internal route: a `FireAction::Marker` into either PredLayer class is rejected (`PredLayerMarkerType`), so no rule fire can grow those slices. Out-of-module, M7's `emit` is reachable by other holders (M10 dispatches §D ops; M7's gate rejects only R-class), so **PR-DISC is a standing assembly obligation**: no writer routes a typed emit with `ty ∈ {pdef, pd_stable}` except M9's `register_pred`/`certify_stable`. On a breach the degradation is **per-start and defined**: an ever-registered start whose immutable content fails the PR-ENC parse/WT has **no defined signature** — `signature` answers `None` and memoizes a **permanent poisoned entry** (content immutable, the failure cannot heal — distinct from the transient, unmemoized never-registered `None`), `evaluate_def` returns `EvalError::UndisciplinedDef`, and a `Ref` to it has no typing judgment (`DanglingReference` — WT-ref's domain condition, read as "no defined signature").

**Resolution / signature / expansion** (all immutable-once-defined hints; memoize, recompute on a miss, never invalidate, never journal):
- `resolve(a)` — `value_at(a.tumbler())` → decode → `(Γ_D, body)` where `body` is the **compact** decoded body (`ResolvedBody`); reads content only. `evaluate_def`/`sig` re-run `Reg`-expansion on it (cached as the memo's `ExpandedTerm`) to get the evaluable concrete-`TypeRef` form.
- `sig(a)` — `(Γ_D, C_D)`; `C_D` re-derives identically forever (PR-SIG); defined on ever-registered-and-disciplined starts, by induction on registration order (well-founded — references name strictly-earlier defs, PR2). `signature(start)` answers from the `DefMemo`; on a **miss** it pins its own snapshot and checks ever-registration (via `is_K(pdef, start)@audit`): **if ever-registered**, it parses + `Reg`-expands + derives `C_D` — which, by WT-ref, **recurses through each referent's `signature(r)`** (well-founded: every referent is strictly-earlier-registered and ever-registered whenever `start` is, PR2; the recursion bottoms out at ref-free bodies) — and **memoizes the `Some`** (permanent — content immutable, ever-registration monotone, so a once-`Some` answer stays valid); **if ever-registered but the parse/WT of the immutable content fails** (an undisciplined deposit — a PR-DISC breach), it answers `None` and memoizes a **permanent poisoned entry** (the failing parse is never re-run; the start thereafter behaves as having no defined signature); **if not ever-registered**, it returns `None` and **memoizes nothing** (a never-registered `None` is transient — a later registration must be observed).
- `expand(a)` — **for evaluation, never materialized** (the *reference*-expansion, distinct from `Reg`-expansion): `evaluate_def` drives the denotation by **DAG-recursion** — its driver is `eval`'s ref-free walk (§2) *plus the one `Ref` arm `eval` lacks*: at a `Ref{addr,args}` node, resolve `addr` (M4 content read), evaluate `args` to *values* (recursively, so nested refs are handled), and denote the referent's `Reg`-expanded body in a fresh env bound to those values (denotation is compositional → sound, no flat string built). Content reads (resolution) and structural reads (denotation) stay distinct passes, so the denotation remains content-free — *this* is why self-hosting doesn't re-open the structural-reads-only surface, and why `eval` itself can keep its ref-free precondition. **For certification, the flat `expand` is built** (§3) with a **content-deterministic fresh-name counter** — one counter per top-level expand, advanced across the whole traversal, never reset per sub-call, never global; a **crate-private minting path**, not `VarId::new` — drawing names from the reserved `VarId ≥ EXPANSION_NAME_BASE` sub-range (§Core data model), which no recorded parameter nor body binder can inhabit (the guarded `VarId::new` plus the codec's reserved-range rejection), so the renamed expansion names are disjoint from every host binder *by construction* (PR-ENC's reserved supply); two evaluators thus obtain the same concrete term (the cross-evaluator agreement that licenses shared caching). De Bruijn / locally-nameless + hash-consing is the alternative if a flat form must be cached.

**Versioning.** `supersede(d, old, new_term)` registers `new_term` (define-style: insert + `register_pred`), then records `old→new` via **`emit(d, reserved_type(Supersedes), old_start, slice::from_ref(&new_start))`** — content-address endpoints (`from` the single `&Address`, `to` the one-element slice), the shipped `Supersedes` class reused — **not** M7's `assert_sup` (which requires resident *links*; def starts are content addresses). `current_version(start)` = `tip(reserved_type(Supersedes), start)` → `Sink(head)` / `Indeterminate` (branch/cycle). The reference DAG is acyclic by registration order, so the lineage is a strict order with no cycle check. **Retry hazard (handed to the driving caller):** `supersede` is **three non-atomic transactions** (the successor's insert + `register_pred`, then the `supersedes` emit) — M7/M5 expose only transact-wrapped ops, so M9 cannot fuse them. A lost-ack retry re-inserts a *fresh* successor and emits a *second* `old→new'` edge, branching the lineage so `current_version` returns `Indeterminate` — a worse failure than `define_predicate`'s harmless-orphan retry. M9 offers no idempotency key; **retry-dedup / exactly-once is the duty of the driving coordination caller** invoking `supersede` (M9's upward consumer, out of corpus) — *not* M10, which never sees this call (M9 ∥ M10; M9's writes reach M5/M7's transact-wrapped ops directly). This mirrors the `create_new_document` *pattern* (no key; the dispatcher dedups), with the dispatcher being M10 there and the coordination caller here.

**Certification / retraction.** `certify_stable(d, start)` checks CVALID(0..iii) (§3) — `NotEverRegistered`/`NotBoolean`/`NotActive`/`ViewDependent`/`NotStable` — then `emit(d, reserved_type(PredStable), start, &[])`. `retract_pred(d, start)` finds the active `pdef` tuple with **`observe(pdef, slice::from_ref(start), &[], Active).first().ok_or(RetractError::NotActive)?.addr`** (never `[0]`) and `nullify(d, that_addr)` — content untouched, audit retains it, re-registration after nullify deposits afresh (idem class now empty). De-registration **does not cascade** to referents.

*Recovery.* All memos lazily rebuild from immutable content; the active/ever distinction is always re-queryable from M7's journal-recovered spanfilade. Nothing in M9 needs durable storage.

### 5. The reactive rule engine

```rust
pub struct Rule { pub domain: Dom, pub trigger: TriggerRef, pub view: View, pub action: FireAction }
                 // `domain` is the RAW SUBMISSION — register_rule checks + `Reg`-expands it into the
                 //   internal `TypedDom` the working set stores (below)
pub enum TriggerRef {
    Inline(TypedTerm),   // built via `type_check_trigger` (may bind one Tup); MUST be ref-free
                         //   (register_rule rejects otherwise — RuleError::RefBearingInlineTrigger)
    Def(Address),        // pdef-backed; evaluated via evaluate_def, so ref-bearing bodies survive de-registration
}                        //   (eval keys on ever-registration); a Def signature is Codom-only — cannot serve a Tup domain
pub enum FireAction {
    /// Canonical certifiable Marker: emit ONE Unary K-tuple covering the bound argument `a`
    /// at `home`, flipping audit `is_K(a)` false→true. (Binary/coverage_G generalization noted.)
    /// `ty` must NOT be a PredLayer class (`pdef`/`pd_stable`) — PR-DISC (register_rule rejects).
    Marker { home: Address, ty: TypeKey },
    /// Single retraction: `nullify(home, a)` on the bound argument `a` — one atomic M7 `nullify`
    /// transact (H-ATOM/H-FIN exactly as Marker). idem⊤. NOT SF-certifiable (active-state trigger),
    /// so it ships UNCERTIFIED (admitted with divergence monitoring, §8), never CertifiedTerminating.
    /// M7 requires `a` to be a RESIDENT LINK, so this rule's domain must be TUPLE-domained
    /// (`a = t.addr`, itself a resident link) or `Addr`-over-`L_dom` (typed-relation link addresses;
    /// PL's `L_dom` excludes open MAKELINK links — §2); an `Addr`-over-`M_K` domain binds from-side
    /// MEMBER addresses (not links), every fire then tripping `FireError::Nullify(Rejected(BadTarget))`
    /// — a DOCUMENTED CONTRACT, not a `register_rule` check (see register_rule below).
    Nullify { home: Address },
    // multi-DEPOSIT fires (multi-emit, or emit-and-nullify composed atomically within one fire)
    // remain deferred — they alone need M7 to expose a pure `stage_emit` to stage several deposits
    // into one `transact`. See Open.
}
```

**Rule registration & validation.** `register_rule(rule)` validates before admitting to the working set, surfacing each failure as a typed `RuleError` — never the late eval-time panic a malformed rule would otherwise cause. The three independent pieces (`domain`, `trigger`, `action`) are reconciled here, the one place that sees them together:

- **Domain — checked and normalized, then stored.** `rule.domain` is run through the **same check + `Reg`-expansion pass as `type_check`** — the WT domain judgment `⊢ D dom(s)` (closed: a `Filter`/`SetTerm` body binds only its own variable): cataloged `Concrete` `TypeRef`s, well-typed `Filter`/`SetTerm` bodies, behavior-compatible atoms. A `Reg` **quantifier inside a body** is legitimate PL (PC1: filtered domains compose freely) and is **expanded away** exactly as in `type_check`; the **domain itself** must synthesize element sort `s ∈ {Addr, Tup}`, so a *bare* `Dom::Reg` (class-valued) fails the sort check. Any check failure ⇒ `IllFormedDomain(TypeError)`. Any `Ref` surviving in the normalized form ⇒ **`RefBearingDomain`** — domains are enumerated by `eval`'s ref-free walk and have no `Def` escape; the remediation is to inline the helper. (This is the sole narrowing relative to ASN-0133's `D_ρ ∈ QD`: a domain body carrying an applied definitional reference — ASN-0130's grammar extension — is rejected rather than resolved.) The pass yields a **`TypedDom`** — the internal checked carrier, the `Dom` analogue of `TypedTerm`'s evaluable projection (every `TypeRef` `Concrete`, no surviving `Reg` binder, `count(Reg)` folded to a `Lit`, element sort recorded) — and the working set stores **it**, discarding the raw submission; this **establishes the evaluator's post-expansion precondition for domains exactly as `type_check` establishes it for terms**. The derived `s` is carried into the next two checks.
- **Trigger arity & codomain** — the trigger must be a **one-parameter `Bool` predicate**. `Inline(t)`: `t` is a `TypedTerm` built via **`type_check_trigger`** (so its one parameter may be `Tup`), ref-free (else `RefBearingInlineTrigger`), `t.params()` exactly one `(VarId, Sort)` (else `BadTriggerArity`), `t.result_sort() == Bool` (else `TriggerNotBoolean`). `Def(addr)`: `signature(addr)` is `Some` (else `DefTriggerUnregistered(addr)` — covering both never-registered and undisciplined starts, which have no defined signature), with one parameter (else `BadTriggerArity`) and `result == Bool` (else `TriggerNotBoolean`); a `Def` signature is **Codom-only** (a stored def never binds a tuple), so a `Def` trigger cannot serve a `Tup` domain. **Remediation asymmetry for a ref-bearing trigger:** a **Codom-parametrized** trigger may be persisted as a def and switched to `TriggerRef::Def`; a **tuple-domained** ref-bearing trigger cannot (a `Def` signature is Codom-only) and must be made ref-free `Inline` by **inlining the referenced helper**. M9 surfaces only `RefBearingInlineTrigger`; selecting the right escape is the caller's.
- **Domain↔trigger sort** — the trigger's single parameter sort must equal the domain element sort `s` (else `DomainTriggerSortMismatch { expected: s, found }`). This is the reconciliation the two independent type-checks omit and the defect this closes: a `Tup`-domained rule (e.g. `ActiveSlice(K)`, ASN-0133 `ρ_R`) demands a `Tup`-parameter trigger — necessarily an **`Inline`** one built via `type_check_trigger`, since a `Def` signature is Codom-only (a `Def`+`Tup`-domain pairing trips `DomainTriggerSortMismatch { expected: Tup, found: <codom> }`) — and an `Addr`-domained rule (`M_K`/`L_dom`/an address `Filter`) an `Addr`-parameter one. Without it a `Tuple` binds to an `Addr` parameter and the atom dispatch panics at fire time.
- **Marker shape** — a `FireAction::Marker { ty, … }` whose `ty` is not a **cataloged Unary** type is rejected here (`BadMarkerType(ty)`), turning a fire-time `Emit(ShapeViolation)` into a registration-time typed rejection; and a `ty` that **is one of the two PredLayer classes** (`pdef`/`pd_stable` — both cataloged Unary, so `BadMarkerType` alone would admit them) is rejected as **`PredLayerMarkerType(ty)`**: PR-DISC reserves those slices for `register_pred`/`certify_stable`, and this guard closes the one in-module route by which a rule fire could deposit an unvalidated `pdef`/`pd_stable` tuple (§4 Discipline).
- **Nullify domain (documented contract, not enforced)** — a `FireAction::Nullify` rule's domain must yield **resident-link** addresses: a `Tup` domain (`a = t.addr`) or an `Addr` domain over `L_dom` (typed-relation link addresses — PL's `L_dom` excludes open MAKELINK links, §2). An `Addr`-over-`M_K` (member-address) domain is *not* rejected here — "yields a link address" is not statically decidable for an arbitrary `Filter` domain — but every fire then trips M7's `BadTarget`, surfaced as `FireError::Nullify(Rejected(BadTarget))`. Keep `Nullify` rules tuple-domained (or address-over-`L_dom`) so the rejection is structurally impossible.

**Domain enumeration** `[D_ρ]_snap` is the stored **`TypedDom`** evaluated off the snapshot (§2 base-domain reads; its post-expansion invariant established at `register_rule`), finite by QD-fin: `M_K`/`L_dom`/filters/`SetTerm` → address sets; `A_K`/`L_K` → `Vec<Tuple>`. The view-parameterized domain `M_K` is enumerated **at `rule.view`** (not blindly at `active`): a `default`-view rule over `M_K` enumerates the *default* member set, so UV-filtered arguments are excluded and the trigger never fires on an argument the rule's own view hides; the fixed-view domains (`A_K`/`L_K`) ignore the view as always. Coverage is *membership-tested per finite denoted address inside the trigger*, never enumerated.

**Trigger evaluation** `T_ρ(x, snap)` = `eval`/`evaluate_def` of the trigger at `rule.view` with `x` bound (`Enabled.arg` — a `Value::Addr` for an `Addr` domain, a `Value::Tuple` for a `Tup` domain), off the snapshot — `eval` for the ref-free `Inline`, `evaluate_def` for `Def`.

**Fire executor** `fire(Enabled{rule, x})`:
1. snapshot; evaluate `T_ρ(x)`. False ⇒ **`FireOutcome::NoOp`** (absorption Q1 — never fire on a false trigger).
2. True ⇒ run `action` through M7's gated write path (`a` = the bound argument's address, `Value::Addr(a)` or `Value::Tuple(t) → t.addr`):
   - **`Marker { home, ty }`** → one `emit(home, ty_endset, a, &[])`; `effect` = the deposited tuple's address.
   - **`Nullify { home }`** → one `nullify(home, a)`; `effect` = the deposited `[R]` tuple's address.

**Two-transaction race, benignly absorbed (item 5).** The trigger check (step 1, off `fire`'s own snapshot) and the deposit (M7's *separate* `transact` — M9 cannot nest a write inside its own read) are **two transactions**; the trigger can flip true→false in the gap (a concurrent writer plants the witness, or retracts the target). This is benign **because both fire actions are idem⊤**: a Marker `emit` whose witness now exists **dedup-hits** the incumbent (commits nothing), and a `nullify` of an already-retracted target likewise dedups — so the gap never double-deposits and never errors. `fire` **reports the dedup distinctly**: an idem⊤ dedup hit (M7 returns an incumbent address and commits nothing) is **`FireOutcome::Deduped { effect, seq }`**, a fresh deposit **`Fired { effect, seq }`**. `fire` distinguishes them by the fire-snapshot status of the returned `effect` — an incumbent is already active (resp. already a live retraction) in `snap`, a fresh deposit's address is newly minted and absent from `snap` (exact absent concurrency; safe-direction under concurrency — at worst a gap-deposited witness is miscounted as a real fire, and the monitor is only a backstop). **Only `Fired` advances the divergence monitor's count** (§8); `Deduped` and `NoOp` do not — matching the journal truth, where a deduped emit leaves *no* record.

Either real deposit is **one M2 transaction (m=1) ⇒ H-ATOM by M2's per-transact atomicity, H-FIN by single-deposit**; M9 takes the fire's `Seq` from M7's return. The `LinkStore` handle is minted off `Arc<Kernel<W>>` via the engine-injected factory. M7 checks the home is registered ⇒ **H-HOME**: an unregistered home maps to `FireError::HomeNotRegistered` (the shared variant — from `emit` for Marker, from `nullify`'s `NullifyError::HomeNotRegistered` for Nullify), never a silent skip; other emit/nullify rejections wrap in `FireError::Emit`/`FireError::Nullify` respectively. For an **idem⊤ Marker**, absent a concurrent depositor the emit is necessarily a *miss* (the true trigger certifies no covering audit tuple in `snap`), so it grows `L_K` and flips the audit-read trigger — extinction by construction; a concurrent witness instead yields a benign `Deduped` (the slice already grew). A **Nullify** fire instead *shrinks* an active slice, flipping an active-state trigger that PD0 does **not** make ⊥-stable, so it is uncertified (§8) and re-armable. v1 ships single-emit (Marker) and single-nullify; only multi-deposit *atomic* fires await M7's pure `stage_emit` (open).

*Recovery.* Fire effects are durable in M7's journal; the in-memory registry is re-registered on restart by the coordination layer. **SF/Marker** semantics make re-evaluation **idempotent** — already-fired arguments read their audit trigger as false, so no double-fire; a **Nullify** rule (uncertified) carries no such guarantee — its replay-time re-fire is bounded only by the divergence monitor (§8). `FireCounters` rebuild by replay (a `Deduped`/`NoOp` deposits nothing, so it leaves no journal record and is correctly excluded from the replay-recomputed count).

### 6. Quiescence detection & scoping

`quiescent(snap)` evaluates `quiescent_R(Σ) ≡ ⋀_{ρ∈R} ∀ x∈[D_ρ] :: ¬T_ρ(x)` (Q0) **at one pinned snapshot, short-circuiting** on the first enabled `(ρ, x)`. The outer `⋀ ρ∈R` is a finite metalevel expansion, not a PL quantifier. For a **heterogeneous registry**, the operational detector evaluates each conjunct at *its rule's declared view* off the one snapshot (the domain `[D_ρ]` enumerated at that same view, §5) — no single-view rewrite is needed because the soundness obligation is "all reads pinned to one committed state," which one `Snapshot` gives. (The fixed-view-base rewrite to a single top-level-audit PL term would be needed only to *reify* `quiescent_R` as a `pdef` for self-monitoring; **v1 offers no such builder** — per Q0 a `chain`-containing default-view trigger has no fixed-view rebuild, so a general builder would need a stated domain restriction — and the live per-rule-view detector needs no rewrite.)

**Strategy.** The authoritative mechanism is the **full Q0 scan** (always correct, no derived state to corrupt; cost O(total domain size)). An optional **incremental agenda** (RETE-style: maintain enabled occurrences, flip only those touched by each write using the Q-FLIP falsifier inventory + the armer graph) serves the hot "anything enabled?" check — but it is a **hint**: reconcile against a periodic full Q0 scan and on recovery; a buggy delta yields *false quiescence*, the dangerous failure, so Q0 is the authority. This is the journal-as-truth / derived-as-hint discipline.

**Scoped** `quiescent_scoped(scope, body, snap)` (Q7). `scope` is a **one-`Addr`-parameter `Bool` `TypedTerm`** — ASN-0133's "Boolean PL predicate `S` over addresses" — **checked up front as a precondition** (ref-free, single `Addr` parameter, `Bool` codomain, off the already-typed `TypedTerm`; a violation panics like `decide`). It adds a per-rule filter `{x∈[D_ρ] : β_ρ^S(x)}` — `ScopeBody::{PerEmitter|PerTarget|PerSource|PerAddress}` mapping to `S(addr(x))` / `∃y∈addrs_G(x)::S(y)` / `∃y∈addrs_F(x)::S(y)` / `S(x)`. **Caller contract (item 3, promoted onto the method):** the body must sort-match each rule's domain — the three tuple bodies (`PerEmitter`/`PerTarget`/`PerSource`) read V-TUP projections and so require a **`Tup`-domained** rule; `PerAddress` requires an **`Addr`-domained** rule. The verdict is therefore **exact iff every scoped rule's domain element sort matches this body's required sort**; for a **mixed-sort registry** M9 applies the chosen `body` **per-rule only where the rule's domain element sort is compatible, leaving sort-incompatible rules UNSCOPED** (their full `[D_ρ]`). **Leaving a rule unscoped *enlarges* its checked domain**, so this single-body application yields a **strict, safe-direction over-approximation of remaining work** — it can only report *more* potential work, **never false quiescence** — but it is *not* the note's exact per-rule scoping (which the `ρ_R` example implies); exact per-rule scoping (a per-rule scope-body field on `Rule`) is **deferred (Open)**. A caller wanting a uniform exact verdict keeps the registry sort-homogeneous. All four canonical bodies use `S` **only positively**, so each restriction is S-monotone **by construction** and Q9's global⟹scope inference (`quiescent_S ⟹ quiescent_{S'}` for `S' ⟹ S`) holds automatically — there is no non-monotone body to reject, the interface admitting only these four forms and not a caller-supplied `β`. (A future custom-`β` `ScopeBody` would reinstate the positivity-scan obligation; not in v1.) Hazard surfaced to callers: an *out-of-scope* fire can re-arm an in-scope trigger (Q8), detectable per-state by re-evaluating Q7.

### 7. The scheduler

`next_enabled(&self, snap)` **peeks** an enabled `(ρ, x)` — some `x∈[D_ρ]` with `T_ρ(x)` true — but, taking `&self`, it **cannot advance a rotation cursor**, so it is not itself "fair": it is a pure candidate query. The `&mut self` **`step` driver owns the rotation** (round-robin/FIFO over the agenda, de-duplicating re-armed occurrences), and **weak fairness is a property of the `step` loop**, not of a single `next_enabled` call. Weak fairness *suffices to reach and hold* quiescence for the structural route: an all-SF, extinction-disciplined registry over **grow-only** domains on bounded input (Q6 regime (ii)-grow-only, Q5a). **Strong fairness** (turn-fairness machinery) is needed only for *non-grow-only* domains under an adversarial environment that cycles arguments out of phase; it is an open lever, not built in v1. **Design guidance to callers: keep domains grow-only and weak fairness is enough.** The scheduler/violation policy and the *driving* of the loop are explicitly handed upward (ASN-0133) — `step` is a default driver the coordination layer may replace.

### 8. Lint / certifier & divergence monitor

`certify_rule(rule)` is a static, sound-but-incomplete lint returning `RuleCertification`:
- (a) trigger ∈ **SF** (via `classify` **at the rule's declared view** — for a `Def` trigger, over its flat, ref-free expansion; for `Inline`, directly);
- (b) action is the **Marker pattern** — a syntactic match that the emitted tuple's slot-coverage is exactly the witness the trigger's negated-existential quantifies over (canonical: trigger `¬is_K(a)` @ audit ⟺ `Marker{_, K}`); a Marker rule reaching `certify_rule` already carries a cataloged-Unary, non-PredLayer `ty` (`register_rule` rejects otherwise — `BadMarkerType`/`PredLayerMarkerType`), so leg (b) only verifies the witness-coverage match;
- (c) domain **grow-only**.
All three + bounded input ⇒ **`CertifiedTerminating`** under weak fairness; otherwise `Uncertified { sf, marker, grow_only }` naming the failed legs. A **`FireAction::Nullify`** rule fails (b) (it is not the Marker emit) and so is *always* `Uncertified`; it is admissible under the uncertified-rule policy (reject vs admit-with-monitoring, §Open) with the divergence monitor as backstop. The **armer graph** (`ρ → ρ'` when ρ's emitted type ∈ footprint(`T_ρ'`)) is built here; `armer_cycles()` flags cycles, and a cycle of **non-SF** rules is a divergence risk (local extinction discipline alone diverges; SF immunity is what breaks the cycle). Rules outside SF/Marker are `Uncertified` (reject or admit-with-monitoring is a policy choice, §Open).

The **divergence monitor**: `FireCounters` per `(ρ, x)`; for an SF/Marker rule, **count > 1 certifies misbehavior** (Q-EXT bounds each argument to one fire — domain growth adds *new* arguments, never re-fires an existing one), a cheap livelock watchdog paired with the static cycle check. **Only real `Fired` outcomes increment the count** — a `Deduped` (idem⊤ dedup hit in the trigger-check↔commit gap, no deposit) and a `NoOp` do not, so the count matches the journal's deposit record exactly (a deduped emit leaves no record, so the journal-recomputed count agrees with the cached one).

*The honest boundary stated to callers:* recognizability (Q0) and absorption (Q1) are unconditional; **reaching/holding quiescence is conditional** on fairness + bounded input + (for non-grow-only) environment hypotheses the substrate cannot enforce.

---

## Invariants & contracts

**By construction** (fall out of the closed algebra, the immutable-content def store, and single-deposit fires):

- **Termination & decidability of every PL term** — finite substrate, no fixpoint/recursion former (ASN-0129 PC5, PC6a).
- **Well-typing decided once, valid forever** — static vocabulary, checked under a fixed Γ_D; re-check is wasted work (WT, V-STAT).
- **Closed ceiling / no foreign code** — closed algebra, syntax-directed eval, no plugin/callback read path (PC6).
- **Guarded partiality** — the binder guard is the only `⊥`-composition route (PC2).
- **Set-semantics counting; global T1-extrema; per-home ordinal age** (PC2a; BH4 doctrine).
- **Identity by start address; ≤1 valid parse per start** — trivial under n=1; the encoding is **injective** (PR-ENC), so distinct terms never collide on a start (ASN-0130 PR-ENC-uniq, S4).
- **Canonical compact encoding** — the stored `Val` is the pre-`Reg`-expansion signed syntactic body (PR-ENC's canonical form, ASN-0129 grammar *with* `Reg`-quantifiers), so a `Reg`-quantified def stores one body, not `body × |classes|`; read-back re-expansion re-derives an identical `sig`/denotation (round-trips; not load-bearing) (ASN-0130 PR-ENC).
- **Reference DAG acyclic, no cycle check** — refs name only ever-registered (strictly-earlier) defs (PR2) — **under the PR-DISC discipline** (the in-module `register_rule` guard plus the standing assembly obligation, under active enforcement below).
- **Expansion deterministic & well-typed at `C_D`** — immutable content + content-deterministic naming from the reserved `VarId ≥ EXPANSION_NAME_BASE` supply (PR3, PR3a).
- **Parse/typing/certificate permanence** — every fact they record reads only immutable content/signature (PR1, PR5a) — **on registration-disciplined derivations (PR-DISC)**.
- **View-transparency** — a def stores no view; the reader supplies it (PR-VIEW).
- **Run contiguity** — M5's atomic insert composite (and n=1) gives it for free (ASN-0130; ASN-0047 J0).
- **Self-hosting preserves structural-reads-only** — references are resolved in the content-read pass; the denoted term is reference-free, so the denotation never reads content (ASN-0130 guarantee).
- **AST denotational completeness over QD-refl** — `Reflect(ArcDom)` reflects any address-valued domain (`L_dom`, a filter, a set-valued term, `M_K`) as a `℘_fin(T)`-valued term, so every value-returning def body the public surface admits is representable, incl. `L_dom` membership/emptiness (ASN-0129 QD-refl, PC6).
- **One shared type registry; M9 builds none** — M9 receives the engine-built `Arc<TypeRegistry>` behind the genesis-sealed config and projects its static catalog from it; no second deterministic build, no divergence trap (engine-injection, §Core data model).

**By active enforcement** (M9 must guard, at the named site):

- **Γ_D is part of the checking judgment** — `type_check`/`type_check_trigger` are *given* the ordered Γ_D and seed Γ with it; a free `Var` outside it is `UnboundVariable`; every **define-path** Γ_D parameter sort must be a codomain (a `Tup`-sorted parameter is `TupParameter`, since `evaluate_def` binds values, never a tuple), while the **trigger-path `type_check_trigger`** admits one `Tup` parameter (a tuple-domained rule binds a `Value::Tuple`, ASN-0133 ρ_R — so a `Tup`-domained rule needs an `Inline` trigger, a `Def` signature being Codom-only); the `TypedTerm` carries Γ_D so `define_predicate`/`evaluate_def`/ST⁺ have their context (ASN-0129 WT; ASN-0130 SignedTerm/PR5).
- **Class-variable bodies fully expanded** — every type position is a `TypeRef`; `Reg`-expansion substitutes `ClassVar(cvar) → Concrete(class)` per registered class so the `TypedTerm`'s evaluable projection holds only `Concrete` refs; a `ClassVar` no enclosing `Reg` binder substitutes is `UnboundClassVar`; an instance applying a behavior some class lacks is `RegInstanceIllTyped` (ASN-0129 PC1/V-IDX).
- **`Reg` admissible under `Forall`/`Exists`/`Count` only** — every other `Dom`-accepting former (`Reflect`, `MaxT1`, `MinT1`, `BigUnion`, `Filter`) rejects a `Reg` domain at the element-sort check, and `Reg` has no term form so never reaches `SetTerm` or any value position (ASN-0129 V-IDX/PC2a; §Internal 1).
- **Reflection only of address-valued domains** — `Reflect(D)` types at `℘_fin(T)` only when `D` is address-valued; a tuple-valued (`A_K`/`L_K`) or class-valued (`Reg`) domain is rejected at the element-sort check, since those serve as quantification/fold domains only, never term values (ASN-0129 QD-refl).
- **Ref-free for every non-def evaluator** — `eval`/`decide`/`classify` and `TriggerRef::Inline` require `is_ref_free`; `register_rule` rejects a ref-bearing `Inline` (`RefBearingInlineTrigger`) and a ref-bearing domain (`RefBearingDomain`); all ref-bearing terms route only through `define_predicate → evaluate_def`'s resolve-then-denote passes, keeping the denotation content-free (the persist-as-def escape for a ref-bearing trigger is Codom-param-only; a tuple-domained ref-bearing trigger — and any ref-bearing domain — must inline its helper, §Internal 5) (ASN-0130; PC4).
- **Registered/address-denoting TypeKeys only** — `type_check` rejects an uncataloged `Concrete` ref (`UnregisteredType`) and a stray `ClassVar` (`UnboundClassVar`) before any `coverage_class`, and the catalog supplies each class's precomputed `CoverageClass`, so every coverage keying is total. **Caller contract (verbatim endset):** the catalog probe is `Endset`-equality while M7's type identity is by *coverage* (I0), so every PL-term `Concrete` `TypeKey` **MUST** be built from a canonical catalog endset — `reserved_type(ShippedType)` for a shipped class, the caller's own `TypeDecl.key` for an app class (both verbatim in the catalog); a coverage-equal but byte-different key misses as `UnregisteredType`. (Canonicalizing a probe key via `coverage_class` is the alternative, but it reintroduces a `coverage_class` call on unvalidated input — the very thing TypeKey-keying avoids — so the contract is preferred.) The class-unindexed `targets_keyed` join is admitted only when some cataloged class attaches BH3 (`NoReverseLookupClass` otherwise — none does in v1) (ASN-0129 V-atom; M7 I0).
- **PR-DISC — in-module guard + standing assembly obligation** — every `L_pdef`-growing step must be `register_pred`'s deposit branch and every `L_pd_stable`-growing step `certify_stable`'s (ASN-0130 PR-DISC). In-module: `register_rule` rejects a `Marker` into either PredLayer class (`PredLayerMarkerType`), so no rule fire can grow those slices. Out-of-module: M7's `emit` is reachable by other holders (M10 dispatches §D ops; the gate rejects only R-class), so the **assembly** must route no typed emit with `ty ∈ {pdef, pd_stable}` from anywhere but M9's two methods. PR1/PR2/PR-SIG-derived guarantees (acyclic reference DAG, permanence, ≤1-active-per-start) are conditional on this discipline; on a breach the degradation is per-start and defined (§Internal 4): `signature` → `None` with a permanent poisoned memo entry, `evaluate_def` → `UndisciplinedDef`, WT-ref → `DanglingReference`.
- **Default-view `K_queried` self-exclusion** — `members(K, default)`/`targets_of(K, x, default)` filter by the BH1 types *other than* `K`, never by `K`; M9 computes the active reading and drops only the other types' filtered elements — **per-type via `is_k(J, ·)` (≡ BH1's `is_filtered_J`, D2 — no new M7 surface, correct for any Φ)**, never M7's aggregate `is_filtered` (which includes `K` and would self-erase `members(retired, default)` to ∅) (ASN-0129 UV, settled OQ1).
- **BH4 totalization at the dispatch** — `age(K, a)` returns `M7::age(a)` only when `a` is the address of an active K-tuple (`observe(K,&[],&[],Active).iter().any(|t| t.addr == a)` — a tuple-identity test, *not* `is_k`'s coverage-of-F membership), else `⊥`; a `stale` horizon narrows `Nat → u64` **saturating** (clamp to `u64::MAX`, so a horizon `≥ 2^64` ⇒ `stale = ∅`, all non-stale; never a wrapping truncation) at the seam (ASN-0129 BH4; dormant in v1).
- **Single-coherent-pre-state for every multi-read verdict** — read all constituents off one M2 `Snapshot`; sites: `eval`, `quiescent[_scoped]`, `register_pred`/`certify_stable` validation (PC4/ASN-0134 clause 6, ASN-0130 single-coherent-pre-state).
- **Structural-reads-only as a wiring discipline** — the atom dispatch (§2) exposes no M4-content or M5-arrangement-dereference read; only M7 + M3-residence (ASN-0129 "structural reads only"). The `View::Audit` reads (`is_K@audit` / `L_K` / `L_dom` / the audit core-atom rebuilds `members`/`targets_of`/`M_K`@audit) **and ever-registration** (`is_K(pdef, start)@audit`, i.e. `observe(pdef, slice::from_ref(start), &[], Audit)`) all rely on the single M7 `observe`-honors-`Audit` seam (named at the boundary; no second audit-honoring method assumed).
- **No feedback / no arbitrary fold accumulator** — the former set admits neither (PC6a, OQ6).
- **Dynamics certifier soundness (never over-certify)** — classification is per-view (`classify(t, view)`): the certifier honors the view-indexed FP/PD0 rules at the supplied view (`certify_rule` at the rule's declared view; `certify_stable` view-invariant on its view-independent input); honor polarity/footprint rules exactly and err toward "not certified"; in particular `count(D) = c` lands in `Neither` (sound), never over-certified as `ST`/`SF`. Spelling emptiness `¬∃` rather than `count = 0` is then an *authoring-precision* recommendation, not a well-formedness rule (`count = 0` type-checks fine) (ASN-0129; ASN-0130 PR5).
- **≤1 active `pdef` per start** — gate-first idem⊤ dedup at `register_pred`, served by M7's `emit` (single-`&Address` `from`) — under the PR-DISC obligation (I1a's K-surface-emitted hypothesis) (ASN-0130 PR0; ASN-0128 I1a).
- **Endorsement is non-permanent; never key a stored/cached fact on it** — evaluation keys on ever-registration; the two-transaction split weakens (iv) to validation-time, sound for that reason (ASN-0130 PR1).
- **`signature` memoizes `Some` and poisoned entries only** — ever-registration is monotone and content immutable, so a `Some` is permanent and cacheable forever, and an ever-registered-but-unparseable start (PR-DISC breach) is memoized as a **permanent poisoned entry** (the failure cannot heal, the parse is never re-run); a never-registered `None` is transient and never memoized, else a later registration goes unobserved. The miss-path derivation recurses through referent signatures (WT-ref, well-founded by PR2). The `DefMemo` is interior-mutable behind this `&self` API (a `RwLock`/concurrent map — never `RefCell`, which is `!Sync`).
- **Insert-position is best-effort; rejection is retry, not defect** — `define_predicate`'s `at = n_C+1` is a snapshot read; a concurrent INSERT lands the def mid-document (harmless — identity is the returned start), a concurrent DELETE yields a clean retryable `Insert(Rejected(BadPosition))`, and a `register_pred`-stage failure leaves harmless orphan content (the `create_new_document` orphan pattern) (item 6; ASN-0047 J0).
- **Rule well-formedness enforced at `register_rule`** — the domain is checked **and normalized** through the WT-domain + `Reg`-expansion pass into a stored `TypedDom` (body-level `Reg` expanded, bare `Reg` rejected via the sort check — `IllFormedDomain`; a surviving `Ref` rejected — `RefBearingDomain`), establishing the evaluator's post-expansion precondition for domains; the trigger a one-parameter `Bool` predicate whose parameter sort equals the domain element sort (a `Tup` domain ⇒ a `Tup`-parameter `Inline` trigger via `type_check_trigger`; a `Def` trigger, Codom-only, cannot serve a `Tup` domain); and a `Marker.ty` a cataloged Unary, **non-PredLayer** type (`BadMarkerType`/`PredLayerMarkerType`); each failure a typed `RuleError`, never a deferred fire-time panic (ASN-0133 Rule — the domain↔trigger reconciliation the independent type-checks omit).
- **`Nullify` rule domain yields resident links (documented contract)** — a `FireAction::Nullify` rule must be tuple-domained (`a = t.addr`) or `Addr`-over-`L_dom` (typed-relation link addresses — PL's `L_dom` excludes open MAKELINK links, §2), so the bound argument is a resident link; an `Addr`-over-`M_K` (member-address) domain is *not* rejected at `register_rule` ("yields a link address" is undecidable for arbitrary `Filter` domains) but every fire then trips M7's `BadTarget`, surfaced as `FireError::Nullify(Rejected(BadTarget))` (M7 BadTarget; §Internal 5).
- **Rule domain enumerated at `rule.view`** — `[D_ρ]` over a view-parameterized `M_K` is enumerated at the rule's declared view, so a `default`-view rule never fires on UV-hidden arguments (ASN-0129 PC3/UV; §Internal 5).
- **Fire atomicity/finiteness/home; benign two-transaction race** — one M7 `emit` *or* `nullify` per fire; M7 checks the home (Q's H-ATOM/H-FIN/H-HOME). The trigger-check and deposit are two transactions; an idem⊤ dedup hit in the gap is reported `FireOutcome::Deduped` (commits nothing) and **excluded from the divergence count**, which counts only real `Fired` (item 5).
- **At-most-once per argument** — by construction for SF+Marker (Q-EXT); for non-SF rules (every `Nullify` among them), an obligation the divergence monitor watches (recomputable from the M7 journal, where `Deduped`/`NoOp` leave no record, so a cache-untouching `&self` `fire` is still covered). For a `Tup`-domain rule the bookkeeping key/report is the tuple's `t.addr` (R1 AddressInjectivity; §Core data model).
- **`retract_pred` no-active guard** — `.first().ok_or(NotActive)?`, never `[0]` (item 8).
- **`quiescent_scoped` scope precondition + sort-matched body (caller contract)** — `scope` is checked one-`Addr`-param `Bool` ref-free up front; a single `ScopeBody` applies per-rule only where domain-sort-compatible, leaving sort-incompatible rules unscoped — **exact iff the scoped rules share the body's sort, else a strict safe-direction over-approximation (never false quiescence)**, not the note's exact per-rule scoping, which would need per-rule body declarations (Open) (ASN-0133 ScopeRestriction; Q7; item 3).
- **S-monotone scope bodies (by construction)** — the four canonical `ScopeBody` forms use `S` only positively, so Q9's global⟹scope inference holds with no positivity-rejection path (Q9).
- **Reserved expansion-name range** — reference-expansion fresh names are drawn only from `VarId ≥ EXPANSION_NAME_BASE`, a range no recorded parameter name and no body binder can inhabit: **the guarded `VarId::new` (the sole public constructor) rejects the range, expansion names are minted only by `expand`'s crate-private counter, and the def codec rejects a reserved-range `VarId` in a decoded body (`ParseFailed`)** — so PR-ENC's body-binder-disjointness is structural (PR-ENC; §Internal 4).

---

## Dependencies & seams

**Upstream calls (concrete):**

- **M1** — address/span value ops behind `Endset`/coverage handling and the def-identity (`shift` for any byte-granular run; `validate` to lift a §G `Tumbler` to `Address`).
- **M2** — `kernel.snapshot()` for every verdict; reads each slice off `snap.world()`; stamps verdicts with `snap.seq()` (V1). **M9 drives no `transact` directly** — fires/registrations ride M5's and M7's transact-wrapped ops; M9 takes their returned `Seq`. The kernel is the shared `Arc<Kernel<W>>` the engine hands `Coordinator::new`; M9 mints each op-handle off it per write via the engine-injected factory.
- **M3** — `is_registered_document(d)` is PL's `is_doc` *and* the emit home-gate (this maps ASN-0129's `dom(Σ.M)` to M3's registry per the decomposition's eager/lazy split: a registered-but-arrangementless doc is a valid residence). *(No `effective_owner`: residence reduces to `is_registered_document`; no M9 algorithm consults ownership.)*
- **M4** — `value_at(start.tumbler())` for resolve/parse/expand of stored defs (the only content read; lives in the operation-surface pass, never the denotation).
- **M5** — `Vstream::insert(d, at, vec![blob])` to write def content through the placement composite (J0); `content_count(d)` for the append position (a snapshot read — the insert re-validates `at`, item 6). M9 mints its `Vstream<W>` op-handle per call from an **engine-injected factory** off its `Arc<Kernel<W>>` (item 1) — M9 names no `Vstream::new`; the engine, the one crate that can construct it, supplies the factory. (M5 must therefore expose a `&Kernel<W>`→`Vstream` constructor to `skep-engine` — an assembly obligation M9 presupposes but does not discharge, the same gap M10 shares.)
- **M7** — the **entire PL read surface** (`observe`, `members`, `targets_of`, `is_k`, BH1–BH4, `is_active`/`is_nullified`, `coverage_class`, `reserved_type`) — `L_dom` is `⋃_K observe(K,&[],&[],Audit)↦addr`, *not* `type_slice` (that is M8's seam), and it ranges over the **typed-relation sublayer only**: open MAKELINK links (uncataloged type slots) are outside PL's universe (ASN-0129's Σ.L is the gated store). **Audit reliance (one primitive):** `is_K@audit`, `L_K`, `L_dom`, the audit core-atom readings (`members`/`targets_of`/`M_K`@audit — **rebuilt from `observe(K,&[],&[],Audit)` via V-AUD's equations**, never routed through a second `members`/`targets_of`-honors-`Audit` assumption), **and ever-registration** all pass `View::Audit` to `observe` and require it to return the **audit** slice (ASN-0086's hist selector); M7's prose says "active typed slice," so this single audit dependency is named to catch an M7 build that ignored `Audit`. Ever-registration is routed through `observe(pdef, slice::from_ref(start), &[], Audit)` (= `is_K(pdef, start)@audit`), so the whole audit surface (the `register_pred` (iii) referent checks, `signature`/`evaluate_def`, `is_ever_pred`, and the hints) rests on the one `observe`-honors-`Audit` seam. **Per-type BH1 filtering** is served by `is_k(J, ·)` (≡ `is_filtered_J`, D2) — M7's aggregate `is_filtered` is used nowhere in the UV rewrite. **BH4 totalization** is M9's guard (active-K-tuple-address identity — `observe(K,&[],&[],Active).iter().any(|t| t.addr == a)`, *not* `is_k`'s coverage membership — before `M7::age`), with **saturating** `Nat→u64` at the `stale` seam (a horizon `≥ 2^64` ⇒ `stale = ∅`, all non-stale). **Gated writes:** `emit` (`pdef`/`pd_stable`/`supersedes`/Marker tuples; single-`&Address` `from`) and `nullify` (both de-register *and* `FireAction::Nullify` fires; a benign idem⊤ dedup hit in the trigger-check↔commit gap is reported `Deduped`). **PR-DISC (assembly obligation):** no holder of M7's `emit` other than M9's `register_pred`/`certify_stable` may route a typed emit whose `ty` is `pdef`/`pd_stable` — M7's gate rejects only R-class, so the exclusion is the assembly's/dispatcher's to enforce (M10's dispatch above all); M9's own `register_rule` closes the in-module route (`PredLayerMarkerType`). **Construction (engine-injected, no rebuild — items 1, 2):** M9 receives — from the engine assembler — its `LinkStore<W>` op-handle (as a factory off `&Kernel<W>`) and the **one** shared `Arc<TypeRegistry>` behind the genesis-sealed config; M9 names neither `LinkStore::new` nor `TypeRegistry::build`, and projects its static catalog from that injected registry. (M7 must expose a `&Kernel<W>`→`LinkStore` constructor to `skep-engine` for the factory body — an assembly obligation, not M9-local.) The factory carries that same registry, so M9's writes and M7's own go through byte-identical type config. The `reserved_type(PredDef|PredStable|Supersedes|…)` calls resolve through **M9's own** cached catalog accessor (each endset `enc(&[reserved.X])`, **coverage-equal** to M7's — byte-identical in fact, but only coverage-equality is required, M7 identifying a type by coverage (I0) — needing no snapshot). The `Unary/⊤/{}` `pdef`/`pd_stable` registrations and the reserved addresses are M7↔M9 **build-time constants** (the PredLayer agreement); M9 caches the catalog from that same pair.

**No M8 edge** (PL is fenced off from M8's content-region/arrangement queries — ASN-0129). **No M10 edge** (parallel; fires reach M7 directly).

**Downstream seam (the coordination surface M9 exposes upward, out of corpus):** the three capability groups of §Public interface. The contracts a consumer codes against: (1) `type_check` once with the def's Γ_D (or `type_check_trigger` for a tuple-domained rule's trigger — the only PL context that binds a `Tup`), then `eval`/`decide` are pure ref-free verdicts "as of `snap.seq()`" (`classify` per-view); (2) `define_predicate`→identity-by-start (a benign retryable `BadPosition`/orphan-content under concurrency), `evaluate_def` keyed on ever-registration (an undisciplined start is a defined `UndisciplinedDef`), `supersede`/`current_version` for lineage (3 non-atomic txns — retry-dedup is the **driving coordination caller's**, not M10's: `supersede` reaches M5/M7 directly, never via M10), `certify_stable`/`is_certified_stable` for the cached stability verdict; (3) `register_rule` (validated: the domain checked + `Reg`-expanded to a stored `TypedDom`, ref-free — `RefBearingDomain`; ref-free `Inline` via `type_check_trigger` or ever-registered `Def`, one-`Bool`-param trigger sort-matched to the domain element sort — a `Tup` domain requires an `Inline` trigger; a `FireAction::Nullify` rule must be tuple-domained or `Addr`-over-`L_dom`; cataloged-Unary, non-PredLayer `Marker.ty`) + `certify_rule`, `quiescent[_scoped]` as a decidable done-verdict any party can run from state+registry alone (scoped: exact for a sort-homogeneous scoped set, else a safe-direction over-approximation), `next_enabled`/`fire`/`step` as the (replaceable) driver whose weak-fairness guarantee lives in `step`'s rotation, with the explicit "reaching quiescence is conditional" boundary. The activation binding (who may register rules), bounded-input workloads, the scheduler/violation policy, and stochastic rule bodies are *handed further up* — M9 supplies the mechanism, not the policy.

---

## Conflicts resolved

1. **`pdef` shape: Multi (ASN-0130 PS1) vs Unary (M7 interface).** Build against M7 ⇒ **Unary** (`F=enc({a})`, `G=∅`). The note used Multi to make the run `A_def` denotation-recoverable from slot `G`; under Unary the run is recovered instead by **re-parsing the self-delimiting content from the start** — and under the n=1 encoding (below) the run *is* the start, so `G=∅` loses nothing. Emit is `emit(d, reserved_type(PredDef), start, &[])` (single-`&Address` `from`, `to=&[]`).

2. **Def encoding: byte-stream contiguous run (ASN-0130) vs M4's arbitrary-`Val` model.** Resolve to **one `Val` per def (n=1)**. M4 stores arbitrary-size opaque `Val`s, so the entire prefix-free envelope fits one content address; contiguity, prefix-freeness, and "extent-from-start" become trivial, and ASN-0130's run-contiguity-under-concurrency hazard vanishes (one write, one address). (The encoded body is the **compact pre-`Reg`-expansion** signed term — PR-ENC's canonical form, ASN-0129's grammar *with* `Reg`-quantifiers — *not* the expanded evaluable tree, so a `Reg`-quantified def does not blow up storage; read-back re-expansion re-derives an identical `sig`/denotation — item 4.) Byte-granular multi-address runs remain a supported generalization, not v1.

3. **UV default-view rewrite scope: ASN-0129 (all collection atoms) vs M7 (only `members`/`targets_of`; coerces the rest to active).** **M9 owns the full UV default rewrite**, including UV's `K_queried` self-exclusion: for `members(K, default)`/`targets_of(K, x, default)` it computes the *active* reading and drops the elements filtered by the BH1 types **other than `K`** — so it does **not** delegate to M7's `members(_, Default)` (which filters by the aggregate `is_filtered`, including `K`, wrongly self-erasing `members(retired, default)` to ∅). In v1 the lone BH1 type is `retired`, so `members(retired, default) = members(retired, active)` (the settled OQ1 commitment); Unary `retired` makes `targets_of(retired, ·) = ∅` at every view, so **only `members` is materially affected in v1**. For `succs`/`chain`/`sources_to`/`stale` in a default term, M9 post-filters M7's active results through the per-type exclusion, keeping `tip`/`is_in_chain` on the unfiltered active walk. (Per-type filtering rides the given surface: BH1's `is_filtered_J` is definitionally `is_k(J, ·)` — D2 on J's own active view — so the `K_queried` exclusion is computed per-type for any number of app-registered BH1 types; M7's aggregate `is_filtered` is used nowhere in the rewrite.)

4. **Def supersession endpoints: content addresses (ASN-0130 PR4) vs M7::`assert_sup` requiring resident *links*.** Def lineage uses **`emit(d, reserved_type(Supersedes), old_start, slice::from_ref(&new_start))`** with content-address endpoints (`from` single `&Address`, `to` one-element slice) — *not* `assert_sup`, which is M7's link-editing path (resident-link endpoints). `tip(Supersedes, start)` then resolves the lineage head over content-address vertices.

5. **ASN-0129's "denotation receives a reference-free term" vs ASN-0130's "don't materialize `expand`."** Reconciled by **two passes**: a content-read resolve pass (DAG-recursive, memoized) and a structural denotation pass that never re-reads content — so the denotation stays reference-free *and* the flat term is never built for evaluation; `eval` therefore keeps its ref-free precondition while `evaluate_def`'s driver adds the lone `Ref` arm. Certification, where ST⁺ is non-compositional, *does* materialize the flat `expand` (params symbolic).

6. **Rule-registry persistence (ASN-0133 inline vs registry-as-content).** Resolved as a **design choice, not a substrate type**: M9 holds an in-memory rule working set; rule *effects* are durable in M7, and SF/Marker semantics make post-restart re-evaluation idempotent, so re-registering the rules (a coordination-layer responsibility, ASN-0133 hands "who may register" upward) recovers the engine without a new `rule` classifier.

7. **Type-registry build site: M9-built (`TypeRegistry::build`) vs engine-built shared instance.** Resolve to **one engine-built `Arc<TypeRegistry>`** injected at `Coordinator::new` and shared with the genesis-sealed config and M9's `LinkStore` handle factory; M9 builds **no** second registry, only its static `TypeCatalog` as a projection of the injected one. This removes the redundant deterministic build and the divergence trap if `(reserved, decls)` ever drift, and the same injection supplies the `Vstream`/`LinkStore` op-handle factories so M9 names no unpublished upstream constructor.

---

## Open build decisions

- **The def byte format** — length-prefixed envelope (recommended) vs self-terminating grammar; must be prefix-free, self-delimiting, decidable, **injective** (PR-ENC), reject reserved-range `VarId`s on decode, and encode the **compact** pre-`Reg`-expansion body (item 4). **And n=1 single-`Val` (recommended here) vs a byte-granular multi-address run** if a future content model wants token-level addresses.
- **Active-pdef lookup: delegate to M7 vs a local hint.** v1 delegates to a per-start `observe(pdef, slice::from_ref(start), &[], {Audit,Active})` probe; if profiling shows the registration-path lookups hot, materialize a local start→tuple map (active/audit-partitioned) as a recomputable hint.
- **Evaluation streaming.** Short-circuit over M7's materialized slice `Vec`s (v1) vs a streaming M7 read (would let `∃` stop earlier on huge slices) — the latter needs M7 to offer iterator reads.
- **Expansion materialization.** DAG-recursive evaluation (recommended; no flat string) vs a cached α-canonical (de Bruijn / locally-nameless) hash-consed flat form for deep, widely-shared DAGs.
- **Quiescence strategy.** Full Q0 poll (authoritative, simple) vs incremental agenda-as-hint reconciled against periodic Q0 — pick incremental for large domains with sparse change.
- **Scheduler discipline.** Weak fairness + grow-only domains (default) vs strong-fairness turn machinery for non-grow-only domains under an adversarial environment.
- **ST⁺ certifier internals.** The stability-checking algorithm beyond PD0's literal rules is explicitly uncommitted; you may add *sound* certification patterns and choose how to present "not certified," never over-certifying.
- **Rule action language richness.** v1 ships **two** single-deposit `FireAction`s: the SF-certifiable **Marker** `emit` and the (uncertified, monitored) single **`Nullify`** — both one atomic M7 transact (H-ATOM/H-FIN), needing no new M7 surface. Only **multi-deposit** fires (multi-emit, or emit-and-nullify composed atomically within one fire) remain deferred, as they alone require M7 to expose a pure `stage_emit` to stage several deposits into one `transact`. Open: the multi-deposit surface itself (and whether uncertified single-`nullify` rules are admitted — next item).
- **Exact per-rule scoping for `quiescent_scoped`.** v1 applies a single `ScopeBody`, scoping only domain-sort-compatible rules and leaving the rest unscoped — a safe-direction (never-false-quiescence) approximation, exact only for a sort-homogeneous scoped set (now stated as a caller contract on the method, item 3). Exact per-rule scoping (the note's `ρ_R` model) would need per-rule body declarations on the registry (a per-rule scope-body field on `Rule`); deferred.
- **Universal-lint scoping.** How to scope `∀ t∈M_pdef :: is_pd_stable(t)` so legitimately non-Boolean helper defs don't spuriously violate it — a membership-filter to a protocol's own classifier (the language can't read a def's result sort to narrow the domain itself).
- **Divergence-monitor / armer-graph persistence cadence** — both are recomputable hints; how often to reconcile counters against the journal is a policy/latency call.
- **Uncertified-rule policy** — reject at `register_rule` vs admit with runtime divergence monitoring (the lint is sound-but-incomplete; strictness is yours). This policy now also governs every `FireAction::Nullify` rule (always `Uncertified`, §8). *(Distinct from the ref-bearing-`Inline`/`RefBearingDomain` rejections, the PredLayer-Marker guard, and the well-formedness gates of items 1/6, which are hard well-formedness rejections, not a termination-policy choice.)*
