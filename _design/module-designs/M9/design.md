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

(the bounds M9's internal `LinkStore<W>` / `Vstream<W>` handles need). `View`, `Endset`, `Tuple`, `Tip`, `CoverageClass` are M7's; `Snapshot`, `Seq`, `TxnError` are M2's; `Address`, `Span` are M1's; `Nat = BigUint`.

M9 contributes **no `WorldState` slice and no record variant** — it is a pure orchestrator/evaluator. Verdicts carry the `seq()` of the one `Snapshot` they were computed against (M2 V1 retrospective).

### A. The predicate language (PL)

```rust
impl<W> Coordinator<W> {
    /// Construction-time: type-check, EXPAND Reg-quantifiers to concrete-class instances,
    /// reject ill-typed terms. Reads no structural state for a ref-free term; consults the
    /// (immutable) signature memo for any Ref node. Once Ok, valid at every reachable state.
    pub fn type_check(&self, term: Term) -> Result<TypedTerm, TypeError>;

    /// Pure, total, terminating denotation at one view against one committed snapshot.
    /// INFALLIBLE on a TypedTerm (well-typed + ref-free post-expansion). Reads ONLY M7 + M3.
    pub fn eval(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> Value;

    /// Convenience for Bool-codomain terms; panics if the codomain is not Bool.
    pub fn decide(&self, t: &TypedTerm, env: &Env, view: View, snap: &Snapshot<W>) -> bool;

    /// Static footprint + 4-point stability lattice + the three active-view exceptions +
    /// view-independence flag. Sound-but-incomplete; never over-certifies. Reads no state.
    pub fn classify(&self, t: &TypedTerm) -> Dynamics;
}
```

### B. Predicate definitions (self-hosting persistence)

```rust
impl<W> Coordinator<W> {
    /// Encode `term` to one content Val, write it through M5's placement composite (mint+write+
    /// place+R), then validate+register the `pdef`. Returns the def IDENTITY (content start addr).
    pub fn define_predicate(&self, d: &Address, term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;

    /// Validate (parse, WT+WT-ref, ever-registration of refs, endorsement, home-residence) the run
    /// already at `start`, then emit the `pdef` tuple via M7. Gate-first; idem dedup at M7.
    pub fn register_pred(&self, d: &Address, start: &Address)
        -> Result<(Address /*pdef tuple*/, Seq), RegisterError>;

    /// resolve+expand+denote. Precondition: `start` EVER-registered (not active). Pure pin to `snap`.
    pub fn evaluate_def(&self, start: &Address, args: &[Value], view: View, snap: &Snapshot<W>)
        -> Result<Value, EvalError>;

    pub fn signature(&self, start: &Address) -> Option<Signature>;          // (Γ_D, C_D); ever-registered only
    pub fn is_active_pred(&self, start: &Address, snap: &Snapshot<W>) -> bool;
    pub fn is_ever_pred(&self,   start: &Address, snap: &Snapshot<W>) -> bool;

    /// Register `new_term` and record old→new via the shipped `supersedes` type (content-address
    /// endpoints, NOT M7::assert_sup). Returns the successor's identity.
    pub fn supersede(&self, d: &Address, old_start: &Address, new_term: TypedTerm)
        -> Result<(Address, Seq), DefineError>;
    pub fn current_version(&self, start: &Address, snap: &Snapshot<W>) -> Tip;   // tip over supersedes

    /// CVALID(0..iii): Boolean sort, actively registered, view-independent expansion, ST⁺. Emits pd_stable.
    pub fn certify_stable(&self, d: &Address, start: &Address)
        -> Result<(Address, Seq), CertifyError>;
    pub fn is_certified_stable(&self, start: &Address, snap: &Snapshot<W>) -> bool;

    /// De-register (M7::nullify on the active `pdef` tuple). Content untouched; reversible.
    pub fn retract_pred(&self, d: &Address, start: &Address) -> Result<(Address, Seq), RetractError>;
}
```

### C. Reactive rules & quiescence

```rust
impl<W> Coordinator<W> {
    pub fn register_rule(&mut self, rule: Rule) -> RuleId;                    // working-set
    pub fn certify_rule(&self, rule: &Rule) -> RuleCertification;            // SF + Marker + grow-only lint

    pub fn quiescent(&self, snap: &Snapshot<W>) -> bool;                      // Q0
    pub fn quiescent_scoped(&self, scope: &TypedTerm, body: ScopeBody, snap: &Snapshot<W>) -> bool; // Q7

    pub fn next_enabled(&self, snap: &Snapshot<W>) -> Option<Enabled>;        // fair scheduler pick
    pub fn fire(&self, e: &Enabled) -> Result<FireOutcome, FireError>;        // 1 emit, atomic, H-*
    pub fn step(&mut self, snap: &Snapshot<W>) -> StepOutcome;                // pick+fire driver

    pub fn fire_count(&self, rule: RuleId, x: &Address) -> u64;               // divergence backstop
    pub fn armer_cycles(&self) -> Vec<Vec<RuleId>>;                           // static cyclic-coupling warning
}
```

Public datatypes: `Term`/`Dom`/`TypedTerm`/`Value`/`Sort`/`Signature`/`Dynamics`/`Rule`/`FireAction`/`ScopeBody`/`Enabled` (Core data model), and the error enums (`TypeError`, `DefineError`, `RegisterError`, `EvalError`, `CertifyError`, `RetractError`, `FireError`).

---

## Core data model

**Authoritative state owned by M9: none.** Predicate definitions live as M4 content (the Val) + M7 `pdef`/`pd_stable` tuples; rule *effects* live as M7 deposits. Everything M9 holds is a **recomputable hint or an in-memory working set**, rebuilt by replay/re-query/re-registration — no journal, no `apply`, no slice. This is the deliberate Lampson outcome: M9 duplicates no authoritative state.

### The PL AST (reified data, not closures)

A finite, acyclic, tagged-union tree in two mutually-recursive families. **Reified, not closure-encoded** — three syntax-directed analyses (type-check, footprint, stability) must read structure. Subterms are `Arc`-shared, optionally interned through a hint table (the persistent-structure win for shared `pdef` bodies — optimization, never load-bearing).

```rust
type ArcTerm = Arc<Term>;  type ArcDom = Arc<Dom>;
#[derive(Clone, PartialEq, Eq, Hash)] pub struct VarId(u32);
#[derive(Clone, PartialEq, Eq, Hash)] pub struct TypeKey(Endset);   // a registered/reserved type, named by its key endset

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
    Ref{addr:Address, args:Vec<ArcTerm>},                              // ASN-0130; only inside stored-def bodies
}
pub enum Atom {
    IsK(TypeKey,ArcTerm), Members(TypeKey), TargetsOf(TypeKey,ArcTerm),          // core (view-parameterized)
    IsFiltered(TypeKey,ArcTerm),                                                 // BH1
    Succs(TypeKey,ArcTerm), Chain(TypeKey,ArcTerm), Tip(TypeKey,ArcTerm),
        IsInChain(TypeKey,ArcTerm,ArcTerm),                                      // BH2 (fixed active)
    SourcesTo(TypeKey,ArcTerm), TargetOf(TypeKey,ArcTerm), TargetsKeyed(ArcTerm),// BH3 (fixed active)
    Age(TypeKey,ArcTerm), Stale(TypeKey,ArcTerm),                                // BH4 (fixed active + home-frontier)
    IsDoc(ArcTerm),                                                              // V-DOC
    TupAddr(VarId), TupAddrsF(VarId), TupAddrsG(VarId),
        InCoverageF(ArcTerm,VarId), InCoverageG(ArcTerm,VarId),                  // V-TUP (state-independent)
}
pub enum Dom {
    MembersDom(TypeKey),   // M_K   : dom(T), view-parameterized
    ActiveSlice(TypeKey),  // A_K   : dom(Tup), fixed active
    AuditSlice(TypeKey),   // L_K   : dom(Tup), fixed audit
    LinkDom,               // L_dom : dom(T)
    Reg,                   // class-valued; quantification-only; expanded at type_check
    Filter{dom:ArcDom,var:VarId,pred:ArcTerm},
    SetTerm(ArcTerm),      // QD-refl: a ℘_fin(T)-valued term reflected as a domain
}
```

`TypedTerm` is the **post-type-check, post-`Reg`-expansion** form: every `Forall/ExistsReg` is rewritten to the finite `And/Or` of its concrete-class instances, so the evaluator never sees a class variable, and `count(Reg)` is a `Lit`. A `TypedTerm` carries the synthesized codomain `Sort` per node (an immutable side-table or annotated tree).

### Values, sorts, signatures

```rust
pub enum Sort { Bool, Addr, AddrSet, OptAddr, AddrSeq, Map, Nat, OptNat, Tup }   // COD ∪ {Tup}
pub enum Value {
    Bool(bool), Addr(Address), AddrSet(im::OrdSet<Tumbler>), OptAddr(Option<Address>),
    AddrSeq(im::Vector<Address>), Map(im::HashMap<CoverageClass,Address>),
    Nat(Nat), OptNat(Option<Nat>), Tuple(Tuple),                                  // Tuple binds a Tup var
}
pub struct Signature { pub params: Vec<(VarId, Sort)>, pub result: Sort }         // (Γ_D, C_D)
```

Set values are `im::OrdSet` (cheap union for `⋃`-folds, dedup = set semantics for `count`); sequences `im::Vector`; the `targets_keyed` join an `im::HashMap` keyed by M7's `CoverageClass`. `im` here buys cheap intermediate values during a fold, not journaled snapshots (those come pinned from M7/M3 slices).

### The type catalog (immutable, build-time-shared)

M9 is constructed with the **same** `(ReservedAddrs, Vec<TypeDecl>)` that seeds M7's `LinkState::genesis` (the M7↔M9 build-time coordination point), and folds it into a frozen `TypeCatalog: HashMap<CoverageClass, Registration>` plus the five `ShippedType` endsets. This is a *cached copy of genesis-immutable data* (R1 — constant at every reachable state), so it never goes stale; it backs type-checking and footprint analysis without a runtime M7 read. (If M7 later exposes `registration_of(&Endset)`, the catalog is replaceable by that read — same answer.)

### Hints / working sets (all recomputable)

| structure | shape | recovered from |
|---|---|---|
| `DefMemo` | `addr → (Signature, ResolvedBody)` + `addr → ExpandedTerm` | M4 content (immutable; never invalidate) |
| active/ever pdef lookup | *delegated to M7* `members(pdef, {Active,Audit})` | M7 spanfilade |
| `RuleRegistry` | `RuleId → Rule` | re-registered by the coordination layer (effects already durable in M7) |
| agenda (optional) | enabled `(RuleId, x)` set | full Q0 scan / journal replay |
| `FireCounters` | `(RuleId, x) → u64` | replay of M7 deposits + re-evaluation |
| `ArmerGraph` | `RuleId → RuleId` (emits-type ⇝ reads-type) | static, from the registry + footprints |

The **active-pdef-by-start index is *not* materialized by M9** — M7 already indexes `pdef` in its spanfilade, so `members(pdef, Active/Audit)` answers ever/active-registration directly (the one index ASN-0130 "forces" is served upstream). M9 keeps only content-derived memos and the rule working set.

---

## Internal design

### 1. Term representation & the type checker (incl. `Reg` expansion)

A single **bottom-up (post-order) synthesis pass** over the raw `Term`. Each former has one match arm transcribing its WT rule (ASN-0129 WT): connectives `Bool→Bool`; quantifiers `Bool` from `D dom(s)` + body at `Bool`; plain composition substitutes a child sort into a context; the **binder guard** `IfSome` narrows `T∪{⊥}→T` (resp. `ℕ∪{⊥}→ℕ`) in its then-branch via the V-PRIM `def` test; `Count:ℕ`, T1-extrema at `T∪{⊥}`, `⋃:℘_fin(T)`; QD-refl types an address-valued domain as a `℘_fin(T)` term. The context `Γ` maps bound `VarId → Sort` (including `Tup` for tuple binders consumed only by V-TUP). Every side condition is a finite match against the static `Codom`/catalog (V-STAT), so the pass **reads no structural state and is decided once at construction**, valid at every reachable state (WT).

**`Reg` expansion (V-IDX).** On `Forall/ExistsReg{cvar, body}`, instantiate `body` once per registered class in the catalog (finite, fixed), type-check each instance, and emit the `And/Or` of the well-typed instances as the `TypedTerm`. Well-formedness is *instance-wise*: a body applying a class-indexed behavior atom (`succs`, `target_of`, …) at the bound class is well-typed only if **every** class carries that behavior — discovered by instantiation (the mandatory `R` instance, behaviors=∅, kills any such body). The one survivor is the class-unindexed `targets_keyed(s)[K]` join (well-typed whenever *some* class attaches BH3, the body never applying an atom a class may lack). Expanding here hands the evaluator a plain finite tree.

**Atom families** come from the catalog: core always; BH1–BH4 conditionally on the registration's behaviors; the single class-unindexed `targets_keyed` symbol globally iff some class attaches BH3. Type-checking an `Atom` checks the named `TypeKey`'s registration supports it (e.g., `Succs` requires BH2/Binary), else `TypeError::BehaviorMissing`.

**References (WT-ref).** A `Ref{addr, args}` types to `C_r` where `signature(addr) = (⟨xᵢ:Cᵢ⟩, C_r)`, each `argᵢ` checks at `Cᵢ`, and `addr` is ever-registered (signature defined). A reference to a never-registered address has *no* typing judgment → `TypeError::DanglingReference`. Signature lookup is the only external consultation, and it reads the (immutable) sig memo — so even ref-bearing type-checking is "decided once."

*Tradeoff.* Reified AST + full `Reg` expansion costs term-size (a body × |classes|) and an O(tree) check, bought back by syntax-directed footprint/stability passes that would be impossible over closures, and by re-check being free forever.

### 2. The pure evaluator

A **syntax-directed tree-walk** threading `(env: Env, view, snap)`. Reads route **only** through M7 (`snap.world().links()`) and M3 (`snap.world().m3()`) — never content or arrangement dereference — which is exactly what discharges *structural-reads-only* as a wiring discipline (PC4). Every constituent read of one verdict comes off the **single pinned `Snapshot`**, discharging the multi-read soundness obligation (ASN-0134/M2 clause 6) by construction.

**Atom dispatch** (the load-bearing table — view threaded):

| PL atom @ term view *v* | M7/M3 read |
|---|---|
| `members(K,v)` / `targets_of(K,x,v)` / `M_K` | `members(K,v)` / `targets_of(K,x,v)` |
| `is_K(x)` @ active/default | `is_k(K,x)` |
| `is_K(x)` @ audit | `!observe(K,&[x],&[],Audit).is_empty()` |
| `A_K` / `L_K` (tuple domains) | `observe(K,&[],&[],Active)` / `…Audit` → `Vec<Tuple>` |
| `L_dom` | `⋃_{K∈catalog} type_slice(K,Audit)` |
| `is_filtered`, `succs`, `chain`, `tip`, `is_in_chain` | `is_filtered`, `succs`, `chain`, `tip`, `chain(K,x).contains(t)` |
| `sources_to`, `target_of`, `targets_keyed` | identical M7 BH3 reads |
| `age`, `stale` | `age`, `stale` |
| `is_doc(d)` | **M3** `is_registered_document(d)` |
| V-TUP / V-PRIM | pure, on the bound `Tuple` value / by arithmetic — no state read |

**View handling.** Core atoms + `M_K` take the *term* view; fixed-view atoms (BH1–BH4, `A_K`, `L_K`) read their named slice regardless. **The UV default-view rewrite is M9's** (M7 only filters `members`/`targets_of` and coerces other collection atoms to active): for a `default` term, M9 drops elements `e` with `is_filtered(e)` from the *returned* collections of `succs`/`chain`/`sources_to`/`stale`, while `tip`/`is_in_chain` use the **unfiltered active walk** (verdicts/traversal never rewritten — UV). In v1 the single shipped BH1 type is `retired`, so `filtered(x) = M7::is_filtered(x)` directly; adding a second BH1 type requires per-type `is_filtered` with the `K_queried` exclusion (M7 currently exposes only the aggregate — flagged below).

**Common case + short-circuit.** Most triggers are existence checks. `Exists` returns at the first witness, `Forall` at the first counterexample, `Filter` composes lazily over the materialized slice `Vec`. The full-pass folds — `Count` (single-pass accumulator), `MaxT1`/`MinT1` (running T1-extremum, `⊥` at empty, composing through the binder guard), `BigUnion` (the only fold that materializes an `OrdSet`) — cannot short-circuit. T1-extrema are *per-home-scoped*: never read global emission order off a global `max_{T1}` (BH4 ordinal-time doctrine). **No feedback/loop former and no arbitrary fold accumulator is offered** — admitting either silently computes `reach`/parity and voids the closed ceiling (PC6a, OQ6).

**Incrementality.** The strong lever is *stability*, not blind memoization: a `⊤`-stable trigger that has fired never re-evaluates (§8). Per-`Snapshot` purity (PC4) makes results memoizable but the polling pattern rewards retiring settled triggers far more.

*Recovery.* Stateless — eval is a pure function of the pinned snapshot. No recovery surface.

*Tradeoff.* M7's `observe`/`members` return materialized `Vec`s, so M9 short-circuits *over* a materialized slice rather than avoiding materialization; a streaming M7 read would let `∃` stop earlier on huge slices (open, §Open).

### 3. The dynamics / stability analyzer

A **second bottom-up pass** (after type-check), fusing FP footprint and PD0–PD2 stability per node, with `Reg` already expanded.

- **Footprint** (`Footprint`): per atom — audit-slice atoms read `L_K`; active atoms read `L_K ∪ L_R`; BH4 adds the home-wide frontier of `home(a)`; `targets_keyed` reads every BH3-attached type's active slice; `is_doc` reads the residence domain; default-view collections add each BH1 type's footprint.
- **Stability** (`Stability`, the 4-point lattice ST∩SF / ST-only / SF-only / neither) by the PD0 mutual induction: step-constants in `ST∩SF`; `is_doc`, audit `is_K`, grow-only membership in `ST`; emptiness/upper-bound counts in `SF`; `¬` swaps, `∧`/`∨` preserve, `⇒` combines `SF⇒ST`; quantifiers/aggregates per grow-only/step-constant domain. T1-extrema are in neither.
- **The three active-view exceptions** (`ActiveExceptions`, emitted explicitly — "name them or be surprised"): (i) retractions can shrink *any* active slice; (ii) any **BH4** term moves with same-home deposits of any type (frontier advance); (iii) any `targets_keyed` term is cross-type by construction.
- **View-independence** (`view_independent`): the PR-VIEW syntactic scan — no view-parameterized constituent and no UV-rewritten collection atom — needed for certification.

The certifier is **sound but incomplete**: it classifies by spelling, surfaces "⊤-stable" / "not certified," and **errs toward not-certified** (over-certifying ⊤-stability would mislead a termination argument). Deciding extensional stability is open theory, not M9's job.

**ST⁺ (ASN-0130 certification).** `certify_stable` runs PD0 over the **flat `expand(start)`** (params as bound constants), with the aggregate threshold widened to *ℕ literal **or** bound ℕ parameter* (the one widening; a checker built to literal PD0 would wrongly refuse a certifiable `count(L_W) ≥ x`). Materializing the flat term here is mandatory: **ST⁺ is not compositional** — a per-referent ST⁺ cache reused at a call site is *unsound* (`helper(x)=count(L_W)≥x ∈ ST⁺`, but `helper(count(L_X))` flips), so each call site's actual arguments must be substituted into the referent's body before classifying that node. Certification is rare, so the flat-materialize cost is acceptable.

### 4. Predicate definitions as content

**Encoding (n=1).** Because M4 stores arbitrary-size byte `Val`s, a definition is **one `Val` at one content address** — the "contiguous run" of ASN-0130 collapses to a single address (`n=1`), making prefix-freeness/self-delimiting and identity-by-start *trivial* (the `Val`'s own byte length delimits the parse; the start *is* the only address). The `Val` holds a deterministic, decidable serialization of the signed term `(Γ_D, body)` — a **length-prefixed envelope** (varint length · param context · body, recommended) so "the run is exactly what the parse consumed" is a one-line check. Byte-granular multi-address runs (one token per address) remain a supported generalization for a byte-stream content model, but are not the v1 encoding.

**Store + register.** `define_predicate(d, term)`:
1. Encode `term` → `blob: Val`.
2. Read `n_C(d)` off a snapshot; `let (a, _) = vstream.insert(d, VPos{s_C, n_C+1}, vec![blob])?;` — M5's placement composite mints (M3), writes bytes (M4), splices, appends R, **atomically (J0/J1★, run-contiguity by construction)**; `a` = the def identity.
3. `register_pred(d, a)`.

`register_pred(d, start)` validates **gate-first, against one pinned snapshot σ** (single-coherent-pre-state):
- **(0/i/ii)** parse `value_at(start)` off σ → `(Γ_D, body)`; success ⇒ residence + extent + parse-validity (one `Val`, fully consumed).
- **(iii)** WT+WT-ref under σ: each referent ever-registered via `members(pdef, Audit)`, sig via the resolver.
- **(iv) endorsement**: each referent actively registered via `members(pdef, Active)`.
- **(P0)** `m3.is_registered_document(d)`.
- valid ⇒ `links.emit(d, reserved(PredDef), &[start], &[])` (Unary ⇒ `to=&[]`); idem⊤ dedups to ≤1 active `pdef` per start. Invalid ⇒ typed rejection, **no emit** (rejection asserts nothing about a standing registration).

The validation reads (σ) and the emit (M7's own transact) are **two transactions** — M7 exposes only a transact-wrapped `emit`, so M9 cannot fuse them. This is sound: parse/typing are content-intrinsic/monotone (stable across the gap, PR1); endorsement (iv) is *deposit-time, non-permanent* by design, so a referent de-registered in the gap merely yields an OQ3-class dangling-live-reference — exactly the state the committed "no cascade" behavior already tolerates. **Evaluation keys on *ever*-registration, never endorsement-currency** — the standing rule that keeps de-registration from corrupting standing defs.

**Resolution / signature / expansion** (all immutable-once-defined hints; memoize, recompute on a miss, never invalidate, never journal):
- `resolve(a)` — `value_at(a)` → decode → `(Γ_D, body)`; reads content only.
- `sig(a)` — `(Γ_D, C_D)`; `C_D` re-derives identically forever (PR-SIG); defined on ever-registered, by induction on registration order (well-founded — references name strictly-earlier defs, PR2).
- `expand(a)` — **for evaluation, never materialized**: `evaluate_def` drives the denotation by **DAG-recursion**, evaluating each `Ref{addr,args}` node by resolving `addr`, evaluating `args` to *values*, and denoting the referent's body in a fresh env (denotation is compositional → sound, no flat string built). Content reads (resolution) and structural reads (denotation) stay distinct passes, so the denotation remains content-free — *this* is why self-hosting doesn't re-open the structural-reads-only surface. **For certification, the flat `expand` is built** (§3) with a **content-deterministic fresh-name counter** — one counter per top-level expand, advanced across the whole traversal, never reset per sub-call, never global — so two evaluators obtain the same concrete term (the cross-evaluator agreement that licenses shared caching). De Bruijn / locally-nameless + hash-consing is the alternative if a flat form must be cached.

**Versioning.** `supersede(d, old, new_term)` registers `new_term`, then records `old→new` via **`emit(d, reserved(Supersedes), &[old], &[new])`** — content-address endpoints, the shipped `Supersedes` class reused — **not** M7's `assert_sup` (which requires resident *links*; def starts are content addresses). `current_version(start)` = `tip(reserved(Supersedes), start)` → `Sink(head)` / `Indeterminate` (branch/cycle). The reference DAG is acyclic by registration order, so the lineage is a strict order with no cycle check.

**Certification / retraction.** `certify_stable(d, start)` checks CVALID(0..iii) (§3) then `emit(d, reserved(PredStable), &[start], &[])`. `retract_pred(d, start)` finds the active `pdef` tuple (`observe(pdef,&[start],&[],Active)[0].addr`) and `nullify(d, that_addr)` — content untouched, audit retains it, re-registration after nullify deposits afresh (idem class now empty). De-registration **does not cascade** to referents.

*Recovery.* All memos lazily rebuild from immutable content; the active/ever distinction is always re-queryable from M7's journal-recovered spanfilade. Nothing in M9 needs durable storage.

### 5. The reactive rule engine

```rust
pub struct Rule { pub domain: Dom, pub trigger: TriggerRef, pub view: View, pub action: FireAction }
pub enum TriggerRef { Inline(TypedTerm), Def(Address) }   // pdef-backed triggers survive de-registration (eval keys on ever-reg)
pub enum FireAction {
    /// Canonical certifiable Marker: emit ONE Unary K-tuple covering the bound argument `a`
    /// at `home`, flipping audit `is_K(a)` false→true. (Binary/coverage_G generalization noted.)
    Marker { home: Address, ty: TypeKey },
    // richer / multi-emit / nullify actions deferred — see Open build decisions.
}
```

**Domain enumeration** `[D_ρ]_snap` is a `Dom` evaluated off the snapshot (§2 base-domain reads), finite by QD-fin: `M_K`/`L_dom`/filters/`SetTerm` → address sets; `A_K`/`L_K` → `Vec<Tuple>`. Coverage is *membership-tested per finite denoted address inside the trigger*, never enumerated.

**Trigger evaluation** `T_ρ(x, snap)` = `eval`/`evaluate_def` of the trigger at `rule.view` with `x` bound, off the snapshot.

**Fire executor** `fire(Enabled{rule, x})`:
1. snapshot; evaluate `T_ρ(x)`. False ⇒ **no-op** (absorption Q1 — never fire on a false trigger).
2. True ⇒ run `action` → one `emit(home, ty, &[x], &[])` (canonical Marker) through M7's gated write path.

This is **one M2 transaction (m=1) ⇒ H-ATOM by M2's per-transact atomicity, H-FIN by single-emit**; M9 takes the fire's `Seq` from M7's return. M7's `emit` checks the home is registered ⇒ **H-HOME**; an unregistered home yields `FireError::HomeNotRegistered` (no admissible emission), never a silent skip. For an **idem⊤ Marker** the emit is necessarily a *miss* (the true trigger certifies no covering audit tuple), so it grows `L_K` and flips the audit-read trigger — extinction by construction. v1 fires are single-emit; multi-emit *atomic* fires would need M7 to expose a pure `stage_emit` (open).

*Recovery.* Fire effects are durable in M7's journal; the in-memory registry is re-registered on restart by the coordination layer. SF/Marker semantics make re-evaluation **idempotent** — already-fired arguments read their audit trigger as false, so no double-fire. `FireCounters` rebuild by replay.

### 6. Quiescence detection & scoping

`quiescent(snap)` evaluates `quiescent_R(Σ) ≡ ⋀_{ρ∈R} ∀ x∈[D_ρ] :: ¬T_ρ(x)` (Q0) **at one pinned snapshot, short-circuiting** on the first enabled `(ρ, x)`. The outer `⋀ ρ∈R` is a finite metalevel expansion, not a PL quantifier. For a **heterogeneous registry**, the operational detector evaluates each conjunct at *its rule's declared view* off the one snapshot — no single-view rewrite is needed because the soundness obligation is "all reads pinned to one committed state," which one `Snapshot` gives. (The fixed-view-base rewrite to a single top-level-audit PL term is only required if `quiescent_R` must itself be *reified as a `pdef`* for self-monitoring; M9 provides that rewrite as a separate term-builder, but the live detector skips it.)

**Strategy.** The authoritative mechanism is the **full Q0 scan** (always correct, no derived state to corrupt; cost O(total domain size)). An optional **incremental agenda** (RETE-style: maintain enabled occurrences, flip only those touched by each write using the Q-FLIP falsifier inventory + the armer graph) serves the hot "anything enabled?" check — but it is a **hint**: reconcile against a periodic full Q0 scan and on recovery; a buggy delta yields *false quiescence*, the dangerous failure, so Q0 is the authority. This is the journal-as-truth / derived-as-hint discipline.

**Scoped** `quiescent_scoped(scope, body, snap)` (Q7) adds a per-rule filter `{x∈[D_ρ] : β_ρ^S(x)}` — `ScopeBody::{PerEmitter|PerTarget|PerSource|PerAddress}` mapping to `S(addr(x))` / `∃y∈addrs_G(x)::S(y)` / `∃y∈addrs_F(x)::S(y)` / `S(x)`. The scope body **must be S-monotone** (`S` positive) to preserve the global⟹scope inference (Q9 anti-monotonicity); M9 rejects a non-monotone scope-body declaration (a syntactic positivity scan) rather than silently voiding the inference. Hazard surfaced to callers: an *out-of-scope* fire can re-arm an in-scope trigger (Q8), detectable per-state by re-evaluating Q7.

### 7. The scheduler

`next_enabled(snap)` selects the next `(ρ, x)` with `x∈[D_ρ]` and `T_ρ(x)` true, **fairly**. Default: **weak fairness** (round-robin/FIFO over the agenda, de-duplicating re-armed occurrences) — which *suffices to reach and hold* quiescence for the structural route: an all-SF, extinction-disciplined registry over **grow-only** domains on bounded input (Q6 regime (ii)-grow-only, Q5a). **Strong fairness** (turn-fairness machinery) is needed only for *non-grow-only* domains under an adversarial environment that cycles arguments out of phase; it is an open lever, not built in v1. **Design guidance to callers: keep domains grow-only and weak fairness is enough.** The scheduler/violation policy and the *driving* of the loop are explicitly handed upward (ASN-0133) — `step` is a default driver the coordination layer may replace.

### 8. Lint / certifier & divergence monitor

`certify_rule(rule)` is a static, sound-but-incomplete lint:
- (a) trigger ∈ **SF** (via `classify`);
- (b) action is the **Marker pattern** — a syntactic match that the emitted tuple's slot-coverage is exactly the witness the trigger's negated-existential quantifies over (canonical: trigger `¬is_K(a)` @ audit ⟺ `Marker{_, K}`);
- (c) domain **grow-only**.
All three + bounded input ⇒ **certified terminating under weak fairness**. The **armer graph** (`ρ → ρ'` when ρ's emitted type ∈ footprint(`T_ρ'`)) is built here; `armer_cycles()` flags cycles, and a cycle of **non-SF** rules is a divergence risk (local extinction discipline alone diverges; SF immunity is what breaks the cycle). Rules outside SF/Marker are returned `Uncertified` (reject or admit-with-monitoring is a policy choice, §Open).

The **divergence monitor**: `FireCounters` per `(ρ, x)`; for an SF/Marker rule, **count > 1 certifies misbehavior** (Q-EXT bounds each argument to one fire — domain growth adds *new* arguments, never re-fires an existing one), a cheap livelock watchdog paired with the static cycle check.

*The honest boundary stated to callers:* recognizability (Q0) and absorption (Q1) are unconditional; **reaching/holding quiescence is conditional** on fairness + bounded input + (for non-grow-only) environment hypotheses the substrate cannot enforce.

---

## Invariants & contracts

**By construction** (fall out of the closed algebra, the immutable-content def store, and single-emit fires):

- **Termination & decidability of every PL term** — finite substrate, no fixpoint/recursion former (ASN-0129 PC5, PC6a).
- **Well-typing decided once, valid forever** — static vocabulary; re-check is wasted work (WT, V-STAT).
- **Closed ceiling / no foreign code** — closed algebra, syntax-directed eval, no plugin/callback read path (PC6).
- **Guarded partiality** — the binder guard is the only `⊥`-composition route (PC2).
- **Set-semantics counting; per-home ordinal extrema** (PC2a, BH4 doctrine).
- **Identity by start address; ≤1 valid parse per start** — trivial under n=1 (ASN-0130 PR-ENC-uniq, S4).
- **Reference DAG acyclic, no cycle check** — refs name only ever-registered (strictly-earlier) defs (PR2).
- **Expansion deterministic & well-typed at `C_D`** — immutable content + content-deterministic naming (PR3, PR3a).
- **Parse/typing/certificate permanence** — every fact they record reads only immutable content/signature (PR1, PR5a).
- **View-transparency** — a def stores no view; the reader supplies it (PR-VIEW).
- **Run contiguity** — M5's atomic insert composite (and n=1) gives it for free (ASN-0130; ASN-0047 J0).
- **Self-hosting preserves structural-reads-only** — references are resolved in the content-read pass; the denoted term is reference-free, so the denotation never reads content (ASN-0130 guarantee).

**By active enforcement** (M9 must guard, at the named site):

- **Single-coherent-pre-state for every multi-read verdict** — read all constituents off one M2 `Snapshot`; sites: `eval`, `quiescent[_scoped]`, `register_pred`/`certify_stable` validation (PC4/ASN-0134 clause 6, ASN-0130 single-coherent-pre-state).
- **Structural-reads-only as a wiring discipline** — the atom dispatch (§2) exposes no M4-content or M5-arrangement-dereference read; only M7 + M3-residence (ASN-0129 "structural reads only").
- **No feedback / no arbitrary fold accumulator** — the former set admits neither (PC6a, OQ6).
- **Dynamics certifier soundness** — honor polarity/footprint rules exactly; err toward "not certified" (ASN-0129; ASN-0130 PR5).
- **≤1 active `pdef` per start** — gate-first idem⊤ dedup at `register_pred`, served by M7's `emit` (ASN-0130 PR0; ASN-0128 I1a).
- **Endorsement is non-permanent; never key a stored/cached fact on it** — evaluation keys on ever-registration (ASN-0130 PR1).
- **Fire atomicity/finiteness/home** — one M7 `emit` per fire; M7 checks the home (Q's H-ATOM/H-FIN/H-HOME).
- **At-most-once per argument** — by construction for SF+Marker (Q-EXT); for non-SF rules, an obligation the divergence monitor watches.
- **S-monotone scope bodies** — reject non-monotone declarations to keep the global⟹scope inference (Q9).

---

## Dependencies & seams

**Upstream calls (concrete):**

- **M1** — address/span value ops behind `Endset`/coverage handling and the def-identity (`shift` for any byte-granular run; `validate` to lift a §G `Tumbler` to `Address`).
- **M2** — `kernel.snapshot()` for every verdict; reads each slice off `snap.world()`; stamps verdicts with `snap.seq()` (V1). **M9 drives no `transact` directly** — fires/registrations ride M5's and M7's transact-wrapped ops; M9 takes their returned `Seq`.
- **M3** — `is_registered_document(d)` is PL's `is_doc` *and* the emit home-gate (this maps ASN-0129's `dom(Σ.M)` to M3's registry per the decomposition's eager/lazy split: a registered-but-arrangementless doc is a valid residence); `effective_owner` for residence resolution.
- **M4** — `value_at(start)` for resolve/parse/expand of stored defs (the only content read; lives in the operation-surface pass, never the denotation).
- **M5** — `Vstream::insert(d, at, vec![blob])` to write def content through the placement composite (J0); `content_count(d)` for the append position.
- **M7** — the **entire PL read surface** (`observe`, `members`, `targets_of`, `is_k`, BH1–BH4, `type_slice`, `is_active`/`is_nullified`, `coverage_class`, `reserved_type`) plus gated writes `emit` (`pdef`/`pd_stable`/`supersedes`/Marker tuples) and `nullify` (de-register). `reserved_type(PredDef|PredStable)` and the `Unary/⊤/{}` registrations are M7↔M9 **build-time constants** (the PredLayer agreement); M9 caches the catalog from the same `(ReservedAddrs, Vec<TypeDecl>)`.

**No M8 edge** (PL is fenced off from M8's content-region/arrangement queries — ASN-0129). **No M10 edge** (parallel; fires reach M7 directly).

**Downstream seam (the coordination surface M9 exposes upward, out of corpus):** the three capability groups of §Public interface. The contracts a consumer codes against: (1) `type_check` once, then `eval`/`decide` are pure verdicts "as of `snap.seq()`"; (2) `define_predicate`→identity-by-start, `evaluate_def` keyed on ever-registration, `supersede`/`current_version` for lineage, `certify_stable`/`is_certified_stable` for the cached stability verdict; (3) `register_rule` + `certify_rule`, `quiescent[_scoped]` as a decidable done-verdict any party can run from state+registry alone, `next_enabled`/`fire`/`step` as the (replaceable) driver, with the explicit "reaching quiescence is conditional" boundary. The activation binding (who may register rules), bounded-input workloads, the scheduler/violation policy, and stochastic rule bodies are *handed further up* — M9 supplies the mechanism, not the policy.

---

## Conflicts resolved

1. **`pdef` shape: Multi (ASN-0130 PS1) vs Unary (M7 interface).** Build against M7 ⇒ **Unary** (`F=enc({a})`, `G=∅`). The note used Multi to make the run `A_def` denotation-recoverable from slot `G`; under Unary the run is recovered instead by **re-parsing the self-delimiting content from the start** — and under the n=1 encoding (below) the run *is* the start, so `G=∅` loses nothing. Emit is `emit(d, PredDef, &[start], &[])`.

2. **Def encoding: byte-stream contiguous run (ASN-0130) vs M4's arbitrary-`Val` model.** Resolve to **one `Val` per def (n=1)**. M4 stores arbitrary-size opaque `Val`s, so the entire prefix-free envelope fits one content address; contiguity, prefix-freeness, and "extent-from-start" become trivial, and ASN-0130's run-contiguity-under-concurrency hazard vanishes (one write, one address). Byte-granular multi-address runs remain a supported generalization, not v1.

3. **UV default-view rewrite scope: ASN-0129 (all collection atoms) vs M7 (only `members`/`targets_of`; coerces the rest to active).** **M9 owns the full UV default rewrite**: it delegates `members`/`targets_of` default to M7 and, for `succs`/`chain`/`sources_to`/`stale` in a default term, post-filters M7's active results through `is_filtered` (v1: the single BH1 `retired`), keeping `tip`/`is_in_chain` on the unfiltered active walk. (v1 limitation: M7 exposes only an aggregate `is_filtered`; a second BH1 type would need per-type filtering with the `K_queried` exclusion — flagged.)

4. **Def supersession endpoints: content addresses (ASN-0130 PR4) vs M7::`assert_sup` requiring resident *links*.** Def lineage uses **`emit(d, Supersedes, &[old_start], &[new_start])`** with content-address endpoints — *not* `assert_sup`, which is M7's link-editing path (resident-link endpoints). `tip(Supersedes, start)` then resolves the lineage head over content-address vertices.

5. **ASN-0129's "denotation receives a reference-free term" vs ASN-0130's "don't materialize `expand`."** Reconciled by **two passes**: a content-read resolve pass (DAG-recursive, memoized) and a structural denotation pass that never re-reads content — so the denotation stays reference-free *and* the flat term is never built for evaluation. Certification, where ST⁺ is non-compositional, *does* materialize the flat `expand` (params symbolic).

6. **Rule-registry persistence (ASN-0133 inline vs registry-as-content).** Resolved as a **design choice, not a substrate type**: M9 holds an in-memory rule working set; rule *effects* are durable in M7, and SF/Marker semantics make post-restart re-evaluation idempotent, so re-registering the rules (a coordination-layer responsibility, ASN-0133 hands "who may register" upward) recovers the engine without a new `rule` classifier.

---

## Open build decisions

- **The def byte format** — length-prefixed envelope (recommended) vs self-terminating grammar; must be prefix-free, self-delimiting, decidable. **And n=1 single-`Val` (recommended here) vs a byte-granular multi-address run** if a future content model wants token-level addresses.
- **Active-pdef lookup: delegate to M7 vs a local hint.** v1 delegates to `members(pdef, {Active,Audit})`; if profiling shows the registration-path lookups hot, materialize a local start→tuple map (active/audit-partitioned) as a recomputable hint.
- **Evaluation streaming.** Short-circuit over M7's materialized slice `Vec`s (v1) vs a streaming M7 read (would let `∃` stop earlier on huge slices) — the latter needs M7 to offer iterator reads.
- **Expansion materialization.** DAG-recursive evaluation (recommended; no flat string) vs a cached α-canonical (de Bruijn / locally-nameless) hash-consed flat form for deep, widely-shared DAGs.
- **Quiescence strategy.** Full Q0 poll (authoritative, simple) vs incremental agenda-as-hint reconciled against periodic Q0 — pick incremental for large domains with sparse change.
- **Scheduler discipline.** Weak fairness + grow-only domains (default) vs strong-fairness turn machinery for non-grow-only domains under an adversarial environment.
- **ST⁺ certifier internals.** The stability-checking algorithm beyond PD0's literal rules is explicitly uncommitted; you may add *sound* certification patterns and choose how to present "not certified," never over-certifying.
- **Rule action language richness.** v1 ships the single-emit Marker `FireAction`; multi-emit *atomic* fires, nullify-actions, and computed endsets are deferred and require M7 to expose a pure `stage_emit` to compose multiple deposits into one atomic transaction.
- **Universal-lint scoping.** How to scope `∀ t∈M_pdef :: is_pd_stable(t)` so legitimately non-Boolean helper defs don't spuriously violate it — a membership-filter to a protocol's own classifier (the language can't read a def's result sort to narrow the domain itself).
- **Divergence-monitor / armer-graph persistence cadence** — both are recomputable hints; how often to reconcile counters against the journal is a policy/latency call.
- **Uncertified-rule policy** — reject at `register_rule` vs admit with runtime divergence monitoring (the lint is sound-but-incomplete; strictness is yours).
