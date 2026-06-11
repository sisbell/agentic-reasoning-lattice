# ASN-0129 Claim Statements

*Source: ASN-0129-substrate-predicate-composition.md (revised unknown) — Extracted: 2026-06-11*

## V — AtomicVocabulary (DEF, definition)

For each registered K, the *template family* `Tpl(record(K))` is:

- *Core family* — present for every K, whatever the record: `is_K : T → Bool` (D2, ASN-0128); `members(K, view) : ℘_fin(T)` (D1); `targets_of(x, view) : T → ℘_fin(T)` (D3). For Unary K, `targets_of` is constantly ∅.
- *BH1 family* (when read-filter is attached): `is_filtered : T → Bool`.
- *BH2 family* (when determinate-walk is attached): `succs : T → ℘_fin(T)`, `chain : T → Seq_fin(T)`, `tip : T → T ∪ {⊥}`, `is_in_chain : T × T → Bool`.
- *BH3 family* (when typed-reverse-lookup is attached): `sources_to : T → ℘_fin(T)`, `target_of : T → T ∪ {⊥}`, and the join `targets_keyed : T → Map_fin`.
- *BH4 family* (when age-staleness is attached): `age : T → ℕ ∪ {⊥}` and `stale : ℕ → ℘_fin(T)`. PL totalizes `age` by adjoining the verdict — `age(a) = ⊥` exactly when `a` is not the address of an active K-tuple.

`V_atom = ⋃_{K registered} Tpl(record(K))`, each atom's active- and default-view semantics exactly its ASN-0128 specification.

---

## V-AUD — AuditReadings (DEF, definition)

`members(K, audit) = ⋃ { addrs(F) : (a, F, G) ∈ L_K^Σ }`

`targets_of(x, audit) = ⋃ { addrs(G) : (a, F, G) ∈ L_K^Σ ∧ x ∈ addrs(F) }`

`is_K(addr)` at audit ≡ `(∃ (a, F, G) ∈ L_K^Σ :: addr ∈ coverage(F))`

The behavior atoms receive *no* audit reading: BH2's walk "reads the active view, never the audit slice" (ASN-0128), and BH1, BH3, and BH4 are likewise defined against active slices — they are *fixed-view* atoms (PC3).

---

## V-TUP — TupleProjections (DEF, definition)

For a variable `x` bound to a tuple `(a, F, G)` (the slices are triple-restricted, ASN-0086):

- `addr(x) : T` — the tuple address;
- `addrs_F(x) : ℘_fin(T)` and `addrs_G(x) : ℘_fin(T)` — the denoted sets of the from- and to-endsets (AD's `addrs(·)`);
- `t ∈ coverage_F(x)` and `t ∈ coverage_G(x)` : `Bool` — coverage-membership tests, decidable span-by-span over the finitely many spans (AD): per span `(s, ℓ)`, form the upper bound `s ⊕ ℓ` and compare — TumblerAdd with T2, the pair CoverageEqualityDecidable's procedure names (ASN-0086), and the pair Gregory's read path computes.

Membership only: `coverage(F)` itself is an infinite address set, outside COD, and never a term value.

---

## V-PRIM — PrimitiveAdmission (DEF, definition)

The *state-independent primitives* admitted to the vocabulary:

- Address comparisons: address equality, the prefix order `≼`, and the total order T1 (ASN-0034) — each Boolean-valued, reading no state;
- Finite-set operations on `℘_fin(T)`-valued terms: membership (`t ∈ S`), set equality, emptiness test (`S = ∅`), and `elems : Seq_fin(T) → ℘_fin(T)`;
- ℕ operations: comparisons (`=`, `≤`) and addition (`+`) on ℕ-valued terms;
- Map lookup, per registered class: `·[K] : Map_fin → T ∪ {⊥}` on `Map_fin`-valued terms, with absent keys reading ⊥;
- Constants and literals: `⊤`, `⊥` (Boolean); ℕ literals; address literals; the verdict constant `⊥` of each ⊥-adjoined codomain;
- Definedness tests on ⊥-adjoined codomains: `def : (T ∪ {⊥}) → Bool` and `def : (ℕ ∪ {⊥}) → Bool`, written `· ≠ ⊥`.

---

## V-STAT — VocabularyStaticity (THM, lemma)

`V_atom` is identical at every reachable state.

*Proof.* The template families and V-AUD/V-TUP are functions of the registration records alone, the extended record is constant at every `→_sh*`-reachable state (R1, ASN-0128), and V-PRIM reads no state. ∎

Registering a new K extends `V_atom` by `Tpl(record(K))` — at construction only (R-VAL, ASN-0128); no transition changes the vocabulary.

---

## COD — Codomains (DEF, definition)

`Codom = {Bool, ℘_fin(T), T ∪ {⊥}, Seq_fin(T), Map_fin, ℕ, ℕ ∪ {⊥}}`

— Boolean, finite address set, optional address, finite address sequence, finite map, natural number, optional natural number. PC0–PC2a compose within `Codom` and introduce no codomain beyond it.

---

## QD — QuantificationDomains (DEF, definition)

The class of *domain expressions* is the least class containing the base expressions

`M_K`, `A_K` (the active K-slice — view-fixed by name), `L_K` (the audit K-slice — view-fixed by name), `C_dom` (`dom(Σ.C)`), `M_dom` (`dom(Σ.M)`), `L_dom` (`dom(Σ.L)`), `Reg` (the registered coverage classes)

and closed under two formations:

- *Filtering*: if `D ∈ QD` is address- or tuple-valued (every base but `Reg`) and `P : D × S → Bool` is a Boolean PL predicate, then `{x ∈ D : P(x, ·)} ∈ QD`;
- *Set-valued terms*: every `℘_fin(T)`-valued PL term, its parameters bound, is a domain expression denoting its own value.

*`Reg` is quantification-only.* A filter `{K ∈ Reg : P(K)}` or a fold `⋃(Reg, f)` is not in the grammar; cross-type questions are asked two admitted ways: V-IDX's static expansion for quantified bodies, V-PRIM's `+` over named per-type counts for totals (PC2a).

`QD` and `PL` are defined by mutual induction; the induction is well-founded on syntactic depth. Each `D ∈ QD` denotes at state Σ (and a binding of its parameters) a set `[D]_Σ` by the evident interpretation (`[Reg]_Σ` is state-independent by R1).

---

## QD-refl — TermReflection (DEF, typing rule)

Every *address-valued* domain expression — one whose denotation is a subset of `T`: `M_K`, `C_dom`, `M_dom`, `L_dom`, a filter over an address-valued domain, and trivially every set-valued term — is itself a `℘_fin(T)`-valued PL term denoting `[D]_Σ`, the typing sound by QD-fin.

The address-valued restriction is load-bearing: `A_K` and `L_K` are tuple-valued and `Reg` class-valued — outside `℘_fin(T)`, indeed outside COD — so the tuple-valued slices serve as quantification and fold domains only, never as term values, and `Reg` more narrowly still: quantification and bare `count` only.

---

## H-init — InitialStoreFiniteness (HYP, precondition)

`|dom(Σ_init.C)| < ∞ ∧ |dom(Σ_init.M)| < ∞`

The natural reading — empty initial stores — satisfies it trivially. Everything downstream of QD-fin (PC1, PC2a, PC5) inherits it.

---

## QD-fin — DomainFiniteness (THM, lemma)

`[D]_Σ` is finite for every `D ∈ QD` at every reachable Σ.

*Proof.* Base cases: `dom(Σ.C)`, `dom(Σ.M)`, and `dom(Σ.L)` are finite by induction on the reaching derivation — the base is H-init for the content and arrangement stores and `Σ_init.L = ∅` (R-VAL, ASN-0128) for the link store; the step, because each K.α adjoins at most one content address, each K.σ at most one document key, and each K.λ_sh at most one link key. `A_K^Σ ⊆ L_K^Σ` inject into `dom(Σ.L)`, hence are finite; `M_K` is finite by D1's bound and V-AUD's (finitely many tuples by the link-store case, finitely many spans per endset, AD); `Reg` is finite by C0 (ASN-0126). Filtering yields subsets; a set-valued term denotes a finite set by its COD typing. ∎

---

## PC0 — BooleanClosure (AX, closure rule)

For PL predicates `P, Q : S → Bool`, the pointwise `P ∧ Q`, `P ∨ Q`, `¬P`, `P ⇒ Q`, `P ⇔ Q` are PL predicates of the same signature. Both constituents read the *same* Σ and the same view (PC3).

---

## PC1 — QuantificationClosure (AX, closure rule)

For `D ∈ QD` and a PL predicate `P : D × S → Bool`,

`(∀ x ∈ D :: P(x, ·)) : S → Bool`  and  `(∃ x ∈ D :: P(x, ·)) : S → Bool`

are PL predicates: by QD-fin the quantifiers reduce at each Σ to finite conjunctions and disjunctions over `[D]_Σ`, well-defined by PC0.

---

## V-IDX — IndexedFamilies (DEF, definition)

Quantification over `Reg` binds a *class variable*: in `(∀ K ∈ Reg :: Φ(K))` the body applies atom families at the bound class. It is defined by *static expansion*: `[Reg]_Σ` is the same finite set at every state (R1, C0, via V-STAT), so the quantified term denotes the finite conjunction (disjunction) of the closed instances `Φ(K₀)`, one per registered class.

*Well-formedness is instance-wise*: a `Reg`-quantified term is well-formed iff each of its finitely many expansion instances `Φ(K₀)` is a PL term.

A body confined to the core family and the fixed-view slices is well-formed unconditionally. A body applying a *class-indexed* behavior-family atom at the bound class is well-formed only if the behavior is attached at *every* registered class — vacuously excluded: **no constructible registry attaches any behavior family universally** (R-C1/R-C0/S1–S3, ASN-0128 ruling out universal attachment).

---

## PC2 — ValueComposition (AX, closure rule)

For a PL term `f : S → C₁` and a *state-indexed* PL term `g : C₁ × S → C₂` with matching types in `Codom`, the composition `s ↦ g(f(s), s) : S → C₂` is a PL term. Both constituents read the *same* Σ and the same view.

*Partiality is guarded, never silent*: the ⊥-adjoined codomains `T ∪ {⊥}` and `ℕ ∪ {⊥}` compose only through the *binder guard*

`if f(s) is some y then g(y, s) else c_default`

whose condition is V-PRIM's definedness test `def(f(s))`, and whose binder types `y` at the narrowed base type (`T` from `T ∪ {⊥}`, `ℕ` from `ℕ ∪ {⊥}`) in the then-branch.

---

## PC2a — AggregationClosure (AX, closure rule)

For `D ∈ QD`:

- `count(D) = |[D]_Σ| : ℕ`, with V-PRIM's ℕ comparisons in Boolean position and V-PRIM's `+` combining counts — admitted at every `D ∈ QD`, the variable-free `count(Reg)` included (a constant by R1/C0);
- `max_{T1}(D)` and `min_{T1}(D)` over address-valued domains: the T1-extremum of `[D]_Σ` when non-empty, ⊥ when empty — typed into `T ∪ {⊥}` and composing through PC2's binder guard;
- `⋃(D, f) : ℘_fin(T)` for an address- or tuple-valued `D` (`Reg` excluded) and a set-valued PL term `f : D → ℘_fin(T)`: the union `⋃_{x ∈ [D]_Σ} f(x, Σ)` — a finite union of finite sets.

*Set semantics, settled*: `count` counts the elements of a domain interpretation — a set of addresses or tuples in the selected view — never occurrences. Cross-type totals are per-type set cardinalities combined by meta-level `+` (settling ASN-0128 Open Question 2).

---

## PC3 — ViewParametricity (AX, closure rule)

Every PL term carries one view `v ∈ {audit, active, default}`, fixed at the top level. The view binds the *view-parameterized* constituents: the core-family atoms — `members`, `targets_of`, `is_K` — and the QD base `M_K` read the slice `v` selects.

The *fixed-view* constituents are not rebound: the named slices `A_K` and `L_K` denote the active and audit K-slices at every term view, and the behavior atoms (BH1–BH4) read the active slices their ASN-0128 definitions name.

---

## UV — UniformDefaultView (DEF, definition)

The default view's semantics, given per codomain under one principle: *filtering is presentation — it rewrites collection-valued results elementwise and rewrites nothing else: never verdicts, never arguments, never traversal, never membership.* Write `filtered(x)` for `(∃ J ∈ Φ, J ≠ K_queried :: is_filtered_J(x))`, BH1's rewrite predicate (ASN-0128). Under `v = default`:

- *Collections* (`℘_fin(T)`, `Seq_fin(T)`): the result drops exactly the elements `x` with `filtered(x)` — `members`, `targets_of`, `succs`, `sources_to`, the sequence `chain` returns, and BH4's `stale` alike.
- *Verdicts and optionals* (`T ∪ {⊥}`, `ℕ ∪ {⊥}`, `Map_fin`): never rewritten. `tip` and `target_of` report the active structure's verdict even when the reported address is filtered; `age` reports its count; `targets_keyed` keeps all its keys and values.
- *Booleans*: never rewritten — `is_K`, `is_filtered`, and `is_in_chain`. `is_in_chain` is a verdict about the active walk (`target ∈ chain(addr)` evaluated against the unrewritten walk), not a read of the default-view result sequence.
- *Arguments and traversal*: never filtered — `chain` walks the active denoted graph; a retired mid-chain element is traversed but not shown in the returned sequence.

---

## PC4 — Purity (THM, lemma)

Every PL term is a pure function of `(dom(Σ.C), dom(Σ.M), Σ.L, Σ.registry)`, its arguments, and its view — the registry component constant by R1, and the content and arrangement stores entering through their *domains* alone: no atom or domain expression reads a content value `Σ.C(a)` or an arrangement binding `Σ.M(d)(v)`, so in practice a term is a function of the link store and two domain sets.

No memoization, no emission-order dependence, no side effects: atoms evaluate through `Observe_K` and the active-subset machinery (ASN-0086), reading state alone; PC0–PC2a and QD-refl's reflected domains preserve purity by induction. Two evaluators of the same term at the same Σ agree.

---

## PC5 — TerminationOnFiniteSubstrate (THM, lemma)

Every PL term's evaluation halts at every reachable state.

*Proof sketch.* Atoms terminate by their ASN-0128 bounds (finite enumerations under L-fin/AD; `chain` by BH2's decreasing bound); V-AUD's readings and V-TUP's tests by the same bounds (L-fin, finitely many spans, one TumblerAdd and a bounded pair of T2 comparisons per span); V-PRIM's primitives are finite operations on finite values. PC0/PC2 are finite trees fixed by syntax; PC1/PC2a reduce to finite folds over QD-fin domains; a QD-refl reflected domain evaluates by the domain's own finite interpretation (QD-fin). ∎

Corollary: every PL predicate is decidable at every reachable state.

---

## PC6 — ExpressiveClosure (THM, theorem)

Define `PL` as the least class containing `V_atom` (V-AUD's readings, V-TUP's projections, and V-PRIM's primitives included) and closed under PC0, PC1 (with V-IDX), PC2, PC2a, and QD-refl's term reflection.

*The base* is the substrate's read surface at atom granularity: `Observe_K`; the atoms of `V_atom`, each a single base call; enumeration reads of `dom(Σ.C)`, `dom(Σ.M)`, `dom(Σ.L)`; V-TUP's per-tuple reads; the registry lookup (constant, R1); the state-independent primitives (V-PRIM).

*The evaluation class* is *syntax-directed evaluation*: computations whose control structure is a finite tree fixed by the evaluated expression's syntax and traversed once — each node a base call (internal iteration permitted only here, behind the atom's own termination bound), a combinator from the admitted vocabulary (PC0's connectives, PC2's binder guard, V-PRIM's operations), or a single-pass fold over an already-computed finite collection (PC1's quantifiers, PC2a's aggregates). What the class excludes is *feedback*: control flow that re-drives base reads from the evaluation's own accumulating output.

*Statement:* The COD-valued functions computable by syntax-directed evaluation over the base are exactly those the terms of `PL` denote; restricted to Boolean codomain, the predicates so computable are exactly `PL`'s predicates.

*Forward:* structural induction — a PL term's control tree is its syntax tree (PC6a), its leaves are base calls by the base's own enumeration, its formers are the admitted combinators and folds, and evaluation is pure and halting (PC4, PC5).

*Converse:* Every base primitive must be PL-expressible, or normalization fails at that leaf. The one non-trivial case is `Observe_K` itself — a call `Observe_K(Σ, F̂, Ĝ, view)` returns its matching set, which is the QD filter

`{x ∈ S_view : (⋀_{t ∈ F̂} t ∈ coverage_F(x)) ∧ (⋀_{t ∈ Ĝ} t ∈ coverage_G(x))}`

with `S_view` the selected slice (`L_K` or `A_K`), the pattern sets being finite query data, so the conjunctions are finite syntax over V-TUP's per-tuple coverage tests. Of the remaining leaves: the atoms, V-TUP's reads, and V-PRIM's primitives are vocabulary by admission; the domain enumerations are QD's bases; a registry lookup is constant-folded (state-constant by R1) — leaving no registry-reading leaf to normalize.

*What the relativization costs:* Three restrictions are load-bearing — the base's atom granularity, the node vocabulary, the control class. Drop the *control class* (admit feedback loops): the base provably decides `reach(x, y)`, the denoted graph being finite at every reachable state (L-fin, QD-fin): `R := {x}; repeat R := R ∪ ⋃_{y ∈ R} succs(y) until stable` halts and answers from base reads alone. An unrestricted ceiling claim — feedback computation over the base computes exactly what PL terms denote — would *entail* ¬C-reach; contrapositively, if C-reach holds, feedback computation strictly exceeds PL.

---

## PC6a — FixpointExclusion (THM, lemma)

PL contains no fixed-point or recursion operator: every former PC0–PC2a admits is non-recursive (QD-refl likewise — a typing rule, not a recursion), so a PL term's composition tree is fixed by its syntax, independent of Σ. Atoms' internal iteration (the `chain` walk) is bounded behind its own termination proof and contributes a leaf, not an unrolling.

---

## C-reach — ReachInexpressibility (CONJ, conjecture)

*No PL term computes `reach(x, y)` — transitive closure over the denoted graph — at every reachable state.*

Status: **conjecture**, deliberately not a theorem. An earlier framing argued it from the inexpressibility of transitive closure in fixed-quantifier-depth first-order logic over finite structures; that argument is unsound for PL as actually defined, on three counts:

(i) The walk atoms traverse unboundedly at fixed syntax: on states whose denoted K-graph has out-degree ≤ 1 throughout, `is_in_chain(x, y)` *is* `reach(x, y)` at arbitrary distance — a lower bound must be fought on *branchy* graph families, where the determinate walk halts (BH2) and the walk atoms go blind.

(ii) PC2a's counting exceeds plain first-order logic — Ehrenfeucht–Fraïssé arguments for FO do not handle cardinality comparison.

(iii) V-PRIM builds total orders (T1, `≼`) into every structure, and locality-based lower bounds for counting logics degrade over ordered structures.

A genuine proof must exhibit branchy, cardinality-balanced state families on which every atom denotation, every aggregate, and every order-sensitive composite agree while `reach` differs. Recorded as Open Question 6.

---

## FP — ReadFootprints (DEF, definition)

The *footprint* of an atom — the state its evaluation consults:

- core atoms of K at view `audit`: `L_K`;
- core atoms of K at view `active`: `L_K` and `L_R`;
- `is_filtered` of a BH1 type J: `L_J` and `L_R`;
- BH2 and BH3 atoms of K: `L_K` and `L_R` — except `targets_keyed`, whose footprint is cross-type: `⋃ {L_J : J Binary with BH3 attached} ∪ L_R`;
- BH4 atoms of K: `L_K`, `L_R`, *and the homed segments of `dom(Σ.L)`* — the frontier counts deposits of every type homed at the same document;
- *default-view increment, codomain-uniform*: under `v = default`, every *collection-valued* atom has as its footprint its active-view footprint plus, for each BH1 type J, the footprint of `is_filtered_J` (`L_J` and `L_R`). The verdict-, Boolean-, and `Map_fin`-valued atoms take no increment;
- base domain footprints: `C_dom` reads `dom(Σ.C)`; `M_dom` reads `dom(Σ.M)`; `L_dom` reads `dom(Σ.L)` whole; `M_K`, `A_K`, `L_K` read the corresponding core footprints; `Reg` reads the constant registry; V-PRIM reads nothing; V-TUP reads the bound tuple's stored value.

A term's footprint is the union over its atoms and domain expressions.

---

## PD0 — AuditMonotonicity (THM, theorem)

Call a domain expression *grow-only* iff it is one of `L_K`, `L_dom`, `C_dom`, `M_dom` — each only ever extended along `→_sh` — or `M_K` in an audit-view term, or a filter `{x ∈ D : P(x, ·)}` with `D` grow-only and `P(x, ·) ∈ ST` for every binding. Define `ST` (the ⊤-stable forms) and `SF` (the ⊥-stable forms) by mutual induction:

- *Step-constants* — in `ST ∩ SF`: terms reading no state beyond already-bound values — V-PRIM primitives and constants over literals and bound addresses, and V-TUP reads of a bound tuple (stored value immutable: L12).
- *Boolean nodes*: `∧` and `∨` preserve `ST` and preserve `SF`; `¬` swaps `ST` and `SF`; `P ⇒ Q ∈ ST` when `P ∈ SF` and `Q ∈ ST`.
- *Quantifiers*: `(∃ x ∈ D :: P) ∈ ST` when `D` is grow-only and `P(x, ·) ∈ ST`; `(∀ x ∈ D :: P) ∈ SF` when `D` is grow-only and `P(x, ·) ∈ SF`.
- *Aggregates*, over grow-only `D`, against ℕ literals: `count(D) ≥ c ∈ ST` and `count(D) ≤ c ∈ SF`. Equality and wrong-polarity bounds are in *neither* class.

*Statement.* Every `ST` term is *⊤-stable*: once true at a reachable Σ, true at every `→_sh*`-successor. Dually, every `SF` term is *⊥-stable*: once false, false forever.

*Ground, by induction:* a grow-only domain's denotation at Σ is contained in its denotation at every successor; no step removes a link address or rewrites a stored value (L12a per step and L12, carried across extended-record steps by ASN-0126's B2 with RP-b, ASN-0128); an existential witness persists with its content intact; a count over a growing set never decreases. ∎

---

## PD1 — ActiveNonMonotonicity (THM, theorem)

Active-view and default-view terms are stable in neither direction.

*Active:* `(∃ x ∈ M_K :: P(x))` at view `active` flips ⊥→⊤ on a K-deposit and ⊤→⊥ on a retraction whose target carries the last witness — `Nullify_Binary` removes the tuple from `A_K^Σ` while `L_K^Σ` keeps it.

*Default:* the same term at view `default` additionally flips on a bare BH1-type emission — `retired` deposited on a witnessing address removes it from every default-view enumeration (UV) with the queried type's own tuples untouched.

The value sequence of `quiescent(t) ≡ OPEN(t) = ∅` along the worked trace is ⊥ (at Σ₁), ⊤ (at Σ₂), ⊥ (at Σ₃): a fire-until-`quiescent(t)` loop that observed Σ₂ has terminated against a condition Σ₃ falsifies, with no link ever leaving the store.

---

## PD2 — FrameStability (THM, theorem)

A term whose footprint excludes `dom(Σ.C)` is invariant under every K.α step, and one whose footprint excludes `dom(Σ.M)` is invariant under every K.σ step: each step kind frames every component outside its one extended store (frame clauses, ASN-0126).

For terms whose domains are per-type slices: a term reading only *audit* slices of types in S is invariant under every deposit of a type outside S.

The active-view refinement: a *BH4-free, `targets_keyed`-free* term reading active slices of types in S is invariant under deposits of types outside S with `[R]` not on the depositing side; the exceptions are:

- *Retraction:* an R-deposit nullifies addresses of any type and can shrink any active slice — the clause requires `[R]` off the depositing side;
- *BH4 home-chain arithmetic:* a deposit of *any* type homed at a document carrying one of K's active tuples advances that home's frontier `f_d` and increments `age` at every K-tuple homed there — a term containing BH4 atoms is additionally perturbed by same-home traffic of every type;
- *`targets_keyed` cross-type footprint:* a term containing `targets_keyed` is perturbed by deposits of every BH3-attached Binary type.

A default-view term adds, through each collection-valued atom it contains, every BH1 type's active slice to its footprint, shrinking its non-interference set by Φ.
