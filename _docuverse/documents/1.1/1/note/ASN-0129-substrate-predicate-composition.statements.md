# ASN-0129 Claim Statements

*Source: ASN-0129-substrate-predicate-composition.md (revised unknown) — Extracted: 2026-06-12*

## V — AtomicVocabulary (DEF, definition)

For each registered K, the *template family* `Tpl(record(K))` is:

- *Core family* — present for every K, whatever the record: `is_K : T → Bool` (D2, ASN-0128) and `members(K, view) : ℘_fin(T)` (D1) and `targets_of(x, view) : T → ℘_fin(T)` (D3). For Unary K, `targets_of` is constantly ∅.
- *BH1 family* (when read-filter is attached): `is_filtered : T → Bool`.
- *BH2 family* (when determinate-walk is attached): `succs : T → ℘_fin(T)`, `chain : T → Seq_fin(T)`, `tip : T → T ∪ {⊥}`, `is_in_chain : T × T → Bool`.
- *BH3 family* (when typed-reverse-lookup is attached): `sources_to : T → ℘_fin(T)` and `target_of : T → T ∪ {⊥}`, class-indexed; and the join `targets_keyed : T → Map_fin` — class-unindexed: a single global atom joining `target_of` across every BH3-attached Binary type, in `V_atom` iff some registered class attaches BH3.
- *BH4 family* (when age-staleness is attached): `age : T → ℕ ∪ {⊥}` and `stale : ℕ → ℘_fin(T)`. `age(a) = ⊥` exactly when `a` is not the address of an active K-tuple.

`V_atom = ⋃_{K registered} Tpl(record(K)) ∪ V-TUP ∪ V-PRIM ∪ V-DOC`

---

## V-AUD — AuditReadings (DEF, definition)

The core family's readings at view `audit`:

```
members(K, audit) = ⋃ { addrs(F) : (a, F, G) ∈ L_K^Σ }

targets_of(x, audit) = ⋃ { addrs(G) : (a, F, G) ∈ L_K^Σ ∧ x ∈ addrs(F) }

is_K(addr) at audit ≡ (∃ (a, F, G) ∈ L_K^Σ :: addr ∈ coverage(F))
```

The behavior atoms receive no audit reading: BH2's walk "reads the active view, never the audit slice," and BH1, BH3, and BH4 are likewise defined against active slices — they are fixed-view atoms, their slice part of their meaning.

---

## V-TUP — TupleProjections (DEF, definition)

For a variable `x` bound to a tuple `(a, F, G)`:

- `addr(x) : T` — the tuple address
- `addrs_F(x) : ℘_fin(T)` and `addrs_G(x) : ℘_fin(T)` — the denoted sets of the from- and to-endsets (AD's `addrs(·)`)
- `t ∈ coverage_F(x)` and `t ∈ coverage_G(x)` : `Bool` — coverage-membership tests, decidable span-by-span over the finitely many spans (AD): per span `(s, ℓ)`, form the upper bound `s ⊕ ℓ` and compare — TumblerAdd with T2.

For a fixed binding of `x`, every V-TUP read is constant across states, the stored value being immutable (L12).

---

## V-PRIM — PrimitiveAdmission (DEF, definition)

The state-independent primitives admitted to the vocabulary as degenerate atoms:

- The comparisons on addresses: address equality, the prefix order `≼`, and the total order T1 (ASN-0034) — each Boolean-valued, reading no state.
- The finite-set operations on `℘_fin(T)`-valued terms: membership (`t ∈ S`), set equality, and the emptiness test (`S = ∅`); and `elems : Seq_fin(T) → ℘_fin(T)`, the order-forgetting projection.
- The meta-level ℕ operations: the comparisons (`=`, `≤`) and addition (`+`) on ℕ-valued terms.
- The map lookup, per registered class: `·[K] : Map_fin → T ∪ {⊥}` on `Map_fin`-valued terms, `K` entering as an index (a named class or a V-IDX-bound class variable). For BH3-attached Binary `K`: `targets_keyed(s)[K] = target_of(s, K)`, an absent key reading ⊥ exactly where `target_of` verdicts ⊥.
- Constants and literals: `⊤` and `⊥` (Boolean), ℕ literals, address literals, and the verdict constant `⊥` of each ⊥-adjoined codomain.
- The definedness tests on the ⊥-adjoined codomains: `def : (T ∪ {⊥}) → Bool` and `def : (ℕ ∪ {⊥}) → Bool`, written `· ≠ ⊥`.

---

## V-DOC — ResidenceAtom (DEF, definition)

The membership atom `is_doc : T → Bool`, with `is_doc(d)` true at Σ iff `d ∈ dom(Σ.M)` — document-residence, the language's one document-store read. Membership only: `dom(Σ.M)` is not a QD base.

---

## V-STAT — VocabularyStaticity (LEMMA, lemma)

`V_atom` is identical at every reachable state.

*Proof.* The template families and V-PRIM's per-class lookup family are functions of the registration records alone, and the extended record is constant at every `→_sh*`-reachable state (R1, ASN-0128); the remaining V-TUP, V-PRIM, and V-DOC symbols form fixed sets, independent of registry and state alike. ∎

---

## COD — Codomains (DEF, definition)

```
Codom = {Bool, T, ℘_fin(T), T ∪ {⊥}, Seq_fin(T), Map_fin, ℕ, ℕ ∪ {⊥}}
```

where `Map_fin` is the finite partial maps from registered coverage classes to `T`.

The two base types embed in their ⊥-adjoined companions — `T ⊆ T ∪ {⊥}` and `ℕ ⊆ ℕ ∪ {⊥}` — and PC2's binder guard is the only traffic the other way, narrowing a ⊥-adjoined value to its base type behind a definedness test.

---

## QD — QuantificationDomains (DEF, definition)

The class of *domain expressions* is the least class containing the base expressions

```
M_K   ([M_K]_Σ = members(K, v) for the view v PC3 binds)
A_K   (the active K-slice — view-fixed by name)
L_K   (the audit K-slice — view-fixed by name)
L_dom (dom(Σ.L))
Reg   (the registered coverage classes)
```

and closed under two formations:

- *Filtering*: if `D ∈ QD` is address- or tuple-valued and `P : D × S → Bool` is a Boolean PL predicate, then `{x ∈ D : P(x, ·)} ∈ QD`.
- *Set-valued terms*: every `℘_fin(T)`-valued PL term, its parameters bound, is a domain expression denoting its own value.

`Reg` is quantification-only: the one variable-free `Reg` position is `count(Reg)` (PC2a), a state-independent constant by R1 and C0.

`QD` and `PL` are defined by mutual induction; the induction is well-founded on syntactic depth. Each `D ∈ QD` denotes at state Σ a set `[D]_Σ`.

---

## QD-refl — TermReflection (DEF, definition)

Every *address-valued* domain expression — one whose denotation is a subset of `T`: `M_K`, `L_dom`, a filter over an address-valued domain, and trivially every set-valued term — is itself a `℘_fin(T)`-valued PL term denoting `[D]_Σ`, the typing sound by QD-fin.

The address-valued restriction is load-bearing: `A_K` and `L_K` are tuple-valued and `Reg` class-valued — outside `℘_fin(T)`, indeed outside COD — so the tuple-valued slices serve as quantification and fold domains only, never as term values, and `Reg` more narrowly still: quantification and bare `count` (its restriction above).

---

## QD-audit — BaseReadAudit (DEF, definition)

The bases measured against the upstream read surface:

- `A_K` and `L_K` are `Observe_K`'s two selectable slices (empty patterns enumerate a whole slice, ASN-0086).
- `M_K` is D1/V-AUD over them.
- `L_dom` is recoverable as the union of the audit slices over the registered classes — every stored tuple carries a registered type (P6, ASN-0126, at extended-record states via RP-a, ASN-0128).
- `Reg` is the constant registry (R1).
- The document store contributes the membership atom `is_doc` (V-DOC), not a base.
- `dom(Σ.C)` has no base and no membership atom (Structural reads only).

The link store's analogous P-tgt disjunct — self-emit `a = a_emit(Σ, d_retr)` — has no PL spelling (C-emit).

---

## QD-fin — DomainFiniteness (LEMMA, lemma)

`[D]_Σ` is finite for every `D ∈ QD` at every reachable Σ.

*Proof.* Base case: `dom(Σ.L)` is finite by induction on the reaching derivation — the base is `Σ_init.L = ∅` (R-VAL, ASN-0128); the step, because each K.λ_sh adjoins at most one link key and K.σ and K.α steps leave the link store framed (step effects, GatedTransitionRelation, ASN-0126, as extended by R-TR, ASN-0128). `A_K^Σ ⊆ L_K^Σ` inject into `dom(Σ.L)` via `addr` (R1 AddressInjectivity, ASN-0086), hence are finite; `M_K` is finite by D1's bound and V-AUD's (finitely many tuples by the link-store case, finitely many spans per endset, AD); `Reg` is finite by C0 (ASN-0126). Filtering yields subsets; a set-valued term denotes a finite set by its COD typing. ∎

---

## PC0 — BooleanClosure (DEF, definition)

For PL predicates `P, Q : S → Bool`, the pointwise `P ∧ Q`, `P ∨ Q`, `¬P`, `P ⇒ Q`, `P ⇔ Q` are PL predicates of the same signature. Both constituents read the same Σ and the same view (PC3).

---

## PC1 — QuantificationClosure (DEF, definition)

For `D ∈ QD` and a PL predicate `P : D × S → Bool`,

```
(∀ x ∈ D :: P(x, ·)) : S → Bool
(∃ x ∈ D :: P(x, ·)) : S → Bool
```

are PL predicates: by QD-fin the quantifiers reduce at each Σ to finite conjunctions and disjunctions over `[D]_Σ`, well-defined by PC0.

---

## V-IDX — IndexedFamilies (DEF, definition)

Quantification over `Reg` binds a class variable: in `(∀ K ∈ Reg :: Φ(K))` the body applies atom families at the bound class. Defined by *static expansion*: `[Reg]_Σ` is the same finite set at every state (R1, C0, via V-STAT), so the quantified term denotes the finite conjunction (disjunction) of the closed instances `Φ(K₀)`, one per registered class.

*Well-formedness is instance-wise*: a `Reg`-quantified term is well-formed iff each of its finitely many expansion instances `Φ(K₀)` is a PL term.

What survives for `Reg`-bodies: the core family and the fixed-view slices at the bound class; the class-unindexed `targets_keyed` (well-formed iff some registered class attaches BH3); and V-PRIM's keyed lookup `·[K]` at the bound class (absent keys reading ⊥). A body applying a class-indexed behavior-family atom at the bound class is never a PL term at any constructible registry (since R-C1 makes `R`'s record attach no behavior family — every constructible registry contains a class lacking every family).

---

## PC2 — ValueComposition (DEF, definition)

For a PL term `f : S → C₁` and a state-indexed PL term `g : C₁ × S → C₂` with matching types in `Codom`, the composition `s ↦ g(f(s), s) : S → C₂` is a PL term. Both constituents read the same Σ and the same view.

*Partiality is guarded, never silent*: the ⊥-adjoined codomains `T ∪ {⊥}` and `ℕ ∪ {⊥}` compose only through the binder guard

```
if f(s) is some y then g(y, s) else c_default
```

whose condition is V-PRIM's definedness test `def(f(s))`, a PC0 Boolean, and whose binder narrows the type: in the then-branch, `y` names the defined value at the narrowed base type — `T` from `T ∪ {⊥}`, `ℕ` from `ℕ ∪ {⊥}`. The else-branch `c_default` is any PL term of codomain `C₂`, evaluated at the same Σ and view.

---

## PC2a — AggregationClosure (DEF, definition)

For `D ∈ QD`:

- `count(D) = |[D]_Σ| : ℕ`, with V-PRIM's ℕ comparisons in Boolean position and V-PRIM's `+` combining counts — admitted at every `D ∈ QD`, the variable-free `count(Reg)` included.
- `max_{T1}(D)` and `min_{T1}(D)` over address-valued domains: the T1-extremum of `[D]_Σ` when non-empty, ⊥ when empty — typed into `T ∪ {⊥}` and composing through PC2's binder guard.
- `⋃(D, f) : ℘_fin(T)` for an address- or tuple-valued `D` (`Reg` excluded) and a set-valued PL term `f : D × S → ℘_fin(T)`: the union `⋃_{x ∈ [D]_Σ} f(x, Σ)`.

*Set semantics, settled*: `count` counts the elements of a domain interpretation — a set of addresses or tuples in the selected view — never occurrences. Cross-type totals are PL terms — per-type set cardinalities combined by meta-level arithmetic with V-PRIM's admitted `+`.

---

## WT — WellTyping (DEF, definition)

A *context* Γ assigns each free variable a sort: a codomain `C ∈ Codom` or the *tuple sort* `Tup` (for binders over `A_K` and `L_K`). Two judgments are defined by mutual induction on syntax (the `S` argument elided):

```
Γ ⊢ e : C      (terms, C ∈ Codom)
Γ ⊢ D dom(s)   (domain expressions, s ∈ {T, Tup})
```

Rules (one per former):
- A codomain-sorted variable is a term at its context sort.
- An atom, projection, or primitive types by its stated signature at matching argument sorts (V, V-TUP, V-PRIM, V-DOC).
- PC0's connectives: `Bool` to `Bool`.
- PC1: yields `(∀/∃ x ∈ D :: P) : Bool` from `Γ ⊢ D dom(s)` and `Γ, x : s ⊢ P : Bool`.
- PC2 plain composition: `Γ ⊢ g[x := f] : C₂` from `Γ ⊢ f : C₁` and `Γ, x : C₁ ⊢ g : C₂`.
- PC2 binder guard: yields `C₂` from `Γ ⊢ f : C ∪ {⊥}`, `Γ, y : C ⊢ g : C₂`, and `Γ ⊢ c_default : C₂`.
- PC2a: `count(D) : ℕ`; T1-extrema at `T ∪ {⊥}` over address-valued domains; `⋃(D, f) : ℘_fin(T)` from `Γ ⊢ D dom(s)` and `Γ, x : s ⊢ f : ℘_fin(T)`.
- QD bases: `M_K` and `L_dom` at `dom(T)`, `A_K` and `L_K` at `dom(Tup)`.
- Filter `{x ∈ D : P}` is at `dom(s)` from `Γ ⊢ D dom(s)` and `Γ, x : s ⊢ P : Bool`.
- A `℘_fin(T)`-valued term is a domain at `dom(T)` (QD's set-valued closure).
- QD-refl types an address-valued domain as a term at `℘_fin(T)`.
- `Reg`: PC1 binders typed instance-wise (V-IDX); `count(Reg) : ℕ`.

*Decidability.* The rules are syntax-directed and every side condition is a finite match against the finite, state-constant `V_atom` (V-STAT); a bottom-up pass over the finite syntax tree decides both judgments, reading no state. ∎

---

## PC3 — ViewParametricity (DEF, definition)

Every PL term carries one view `v ∈ {audit, active, default}`, fixed at the top level.

*View-parameterized* constituents — `members`, `targets_of`, `is_K`, `M_K` — read the slice `v` selects (active and default per ASN-0128, audit per V-AUD; `is_K` under default equals its active reading).

*Fixed-view* constituents are not rebound: `A_K` and `L_K` denote the active and audit K-slices at every term view; the behavior atoms (BH1–BH4) read the active slices their ASN-0128 definitions name — under `v = default` UV's presentation rewrite applies to their collection-valued results.

Cross-view readings are derivable through the fixed-view slices: `⋃(L_K, addrs_F)` rebuilds `members(K, audit)` within an active-view term; `(∃ x ∈ L_K :: t ∈ coverage_F(x))` is the audit `is_K`.

---

## UV — UniformDefaultView (DEF, definition)

The default view's semantics, given per codomain: *filtering is presentation — it rewrites collection-valued results elementwise and rewrites nothing else: never verdicts, never arguments, never traversal, never membership, never stored values.*

Write `filtered(x)` for `(∃ J ∈ Φ, J ≠ K_queried :: is_filtered_J(x))`. Under `v = default`:

- *Collections* — `members`, `targets_of`, `succs`, `sources_to`, the sequence `chain` returns, and `stale` — the result drops exactly the elements `x` with `filtered(x)`.
- *Verdicts and optionals* (`T ∪ {⊥}`, `ℕ ∪ {⊥}`, `Map_fin`): never rewritten. `tip`, `target_of`, `age`, and `targets_keyed` report the active structure's verdict even when the reported address is filtered from every enumeration.
- *Booleans*: never rewritten — `is_K`, `is_filtered`, and `is_in_chain` (which is a verdict about the active walk `target ∈ chain(addr)` evaluated against the unrewritten walk).
- *Arguments and traversal*: never filtered — `chain` walks the active denoted graph; a retired mid-chain element is traversed but not shown in the returned sequence.

---

## PC4 — Purity (LEMMA, lemma)

Every PL term is a pure function of `(dom(Σ.M), Σ.L, Σ.registry)`, its arguments, and its view — the registry component constant by R1, the arrangement store entering through its domain alone, and the content store not entering at all.

No memoization, no emission-order dependence, no side effects: atoms and bases evaluate along the base's three read routes reading state alone; PC0–PC2a and QD-refl's reflected domains preserve purity by induction. Two evaluators of the same term at the same Σ agree.

---

## PC5 — TerminationOnFiniteSubstrate (LEMMA, lemma)

Every PL term's evaluation halts at every reachable state.

*Proof sketch.* Atoms terminate by their ASN-0128 bounds (finite enumerations under L-fin/AD; `chain` by BH2's decreasing bound); V-AUD's readings and V-TUP's tests by the same bounds (L-fin, finitely many spans, one TumblerAdd and a bounded pair of T2 comparisons per span); V-PRIM's primitives are finite operations on finite values; `is_doc` is a single membership check on `dom(Σ.M)` (V-DOC). PC0/PC2 are finite trees fixed by syntax; PC1/PC2a reduce to finite folds over QD-fin domains; a QD-refl reflected domain evaluates by the domain's own finite interpretation (QD-fin). ∎

With PC4: every PL predicate is decidable at every reachable state.

---

## PC6 — ExpressiveClosure (THEOREM, theorem)

Define `PL` as the least class containing `V_atom` and closed under PC0, PC1 (with V-IDX), PC2, PC2a, and QD-refl's term reflection.

**The base** is the substrate's read surface at atom granularity: `Observe_K` (empty patterns enumerate whole slices `L_K` and `A_K`); the template atoms of `V_atom`; an enumeration read of `dom(Σ.L)`; a membership read of `dom(Σ.M)` (`is_doc`; `dom(Σ.C)` has no base read); V-TUP's per-tuple reads; the registry lookup (constant, R1); and the state-independent primitives (V-PRIM).

**The evaluation class** is *syntax-directed evaluation*: computations whose control structure is a finite tree fixed by the evaluated expression's syntax and traversed once — each node a base call (internal iteration only here, behind the atom's own termination bound), a combinator from the admitted vocabulary (PC0's connectives, PC2's binder guard, V-PRIM's operations), a domain interpretation from QD (filter evaluation: a single-pass select over the interpreted base domain; or reflected-domain enumeration), or a single-pass fold over an already-computed finite collection (PC1's quantifiers, PC2a's aggregates). The class excludes *feedback*: control flow that re-drives base reads from the evaluation's own accumulating output.

*Statement*: The COD-valued functions computable by syntax-directed evaluation over the base are exactly those the terms of `PL` denote; restricted to Boolean codomain, the predicates so computable are exactly `PL`'s predicates.

*Forward*: structural induction — a PL term's control tree is its syntax tree (PC6a), its leaves are base calls, its formers are the admitted combinators, folds, and domain interpretations — evaluation is pure and halting (PC4, PC5).

*Converse*: every base primitive must be PL-expressible. The one non-trivial case is `Observe_K` itself — a call `Observe_K(Σ, F̂, Ĝ, view)` returns its matching set, which is the QD filter

```
{x ∈ D_view : (⋀_{t ∈ F̂} t ∈ coverage_F(x)) ∧ (⋀_{t ∈ Ĝ} t ∈ coverage_G(x))}
```

with `D_view` the selected slice (`L_K` or `A_K`): the pattern sets are finite query data, so the conjunctions are finite syntax over V-TUP's per-tuple coverage tests, and the filter is a computation the class generates. Of the remaining leaves: the atoms, V-TUP's reads, and V-PRIM's primitives are vocabulary by admission; the domain enumeration is QD's base; a registry lookup is not (constant-folded rather than admitted: the lookup is state-constant by R1, so a computation containing it is extensionally equal to one with the looked-up value inlined — V-PRIM constant, a branch taken statically, or a `Reg` expansion via V-IDX).

The ceiling moves only when the registry does: a new behavior or shape adds atomic forms; no composition does. The vocabulary being construction-pinned (V-STAT), the ceiling is pinned to `Σ_init`'s registry.

---

## PC6a — FixpointExclusion (LEMMA, lemma)

PL contains no fixed-point or recursion operator: every former PC0–PC2a admits is non-recursive (QD-refl likewise — a typing rule, not a recursion), so a PL term's composition tree is fixed by its syntax, independent of Σ — atoms' internal iteration contributes a leaf, not an unrolling (bounded per PC6's evaluation class).

---

## C-reach — ReachInexpressibility (CONJECTURE, conjecture)

*No PL term computes `reach(x, y)` — transitive closure over the denoted graph — at every reachable state.*

Status: **conjecture**, deliberately not a theorem.

A proof cannot proceed by citing the inexpressibility of transitive closure in fixed-quantifier-depth first-order logic over finite structures — that route is unsound for PL as actually defined, on three counts:

(i) The walk atoms traverse unboundedly at fixed syntax: on states whose denoted K-graph has out-degree ≤ 1 throughout, `is_in_chain(x, y)` *is* `reach(x, y)` at arbitrary distance — a lower bound must be fought on *branchy* graph families, where the determinate walk halts (BH2) and the walk atoms go blind.

(ii) PC2a's counting exceeds plain first-order logic — Ehrenfeucht–Fraïssé arguments for FO do not handle cardinality comparison.

(iii) V-PRIM builds total orders (T1, `≼`) into every structure, and locality-based lower bounds for counting logics degrade over ordered structures.

A genuine proof must exhibit branchy, cardinality-balanced state families on which every atom denotation, every aggregate, and every order-sensitive composite agree while `reach` differs — an invariance argument in a counting-plus-order regime.

What stands without it: PL ships no closure operator (PC6a, a grammar fact); closure is computed at agent time — iterate `succs`, unroll the recursion — and the substrate cannot be handed the loop. The conjecture's polarity against PC6's control restriction: feedback evaluation over the base decides `reach` (PC6's loop), so a feedback-ceiling claim would entail ¬C-reach.

---

## C-emit — SelfEmitInexpressibility (CONJECTURE, conjecture)

*No PL term computes the self-emit test `a = a_emit(Σ, d)` — "is `a` the address the next emission homed at `d` would receive" — at every reachable state.*

The baseline is a grammar fact, read off V: `a_emit(Σ, d) = chain_d(f_d^Σ)` (FrontierUnification, ASN-0126) reads the frontier of the home's chain assembled from the homed-set (`home(a') = d`, which no atom exposes and prefix testing cannot characterize — PC6's granularity discussion) and the chain arithmetic `inc(·, 0)` that V-PRIM excludes — so no direct spelling exists in the grammar.

Status: **conjecture**, because the grammar fact blocks only the direct spelling; whether some extensionally equal term computes the test is an invariance question.

A proof must be an invariance argument over every atom denotation, handling in particular the two frontier-derived routes the vocabulary does admit:

- BH4's `age` is defined from `f_d^Σ` (its home-wide footprint recorded at FP), its narrowed values entering ℕ position through PC2's binder guard wherever BH4 is attached.
- The link-domain data of which `a_emit(Σ, d)` is a function enters term position through the reflected `L_dom` (QD-refl).

Conjecture: neither route closes the gap — `age` reads chain indices relative to the frontier, never the frontier slot's address, and `L_dom` delivers the homed-set only as an undifferentiated subset of the link domain.

---

## FP — ReadFootprints (DEF, definition)

The footprint of an atom — the state its evaluation consults:

- Core atoms of K at view `audit`: `L_K`.
- Core atoms of K at view `active`: `L_K` and `L_R` (the active slice is the audit slice minus `nullified(Σ)`, computed from the retraction audit slice).
- `is_filtered` of a BH1 type J: `L_J` and `L_R` (an active-view read).
- BH2 and BH3 atoms of K: `L_K` and `L_R` (active-view reads) — except `targets_keyed`, whose footprint is `⋃ {L_J : J Binary with BH3 attached} ∪ L_R`.
- BH4 atoms of K: `L_K`, `L_R`, *and the homed segments of `dom(Σ.L)`* — `age(a) = f_d^Σ − 1 − j` at `d = home(a)` is arithmetic on the home's full chain; the footprint is home-wide, not slice-local.
- *The default-view increment*: under `v = default`, each atom on UV's Collections list — `members`, `targets_of`, `succs`, `sources_to`, `chain`, `stale` — has as its footprint its active-view footprint plus, for each BH1 type J, the footprint of `is_filtered_J` (`L_J` and `L_R`). Every other atom — verdict-, Boolean-, and `Map_fin`-valued — takes no increment.
- `is_doc`: `dom(Σ.M)`.
- Bases: `L_dom` reads `dom(Σ.L)` whole; `M_K`, `A_K`, `L_K` read the corresponding core footprints; `Reg` reads the constant registry; V-PRIM reads nothing; V-TUP reads the bound tuple's stored value.

A term's footprint is the union over its atoms and domain expressions.

---

## PD0 — AuditMonotonicity (DEF+LEMMA, lemma)

**Definitions.** Call a domain expression *grow-only* iff it is `L_K` or `L_dom`, or `M_K` in an audit-view term (V-AUD's union over the growing `L_K`), or a filter `{x ∈ D : P(x, ·)}` with `D` grow-only and `P(x, ·) ∈ ST` for every binding, or a *step-constant domain* (a set-valued term reading no state beyond its bound parameters).

Define `ST` (the ⊤-stable forms) and `SF` (the ⊥-stable forms) by mutual induction:

- *Step-constants* — in `ST ∩ SF`: terms reading no state beyond already-bound values — V-PRIM primitives and constants over literals and bound addresses, and V-TUP reads of a bound tuple (stored value immutable: L12).
- *Residence*: `is_doc(d)` (argument a literal or bound address) is in `ST`; not in `SF`.
- *Audit membership*: `is_K(addr)` at view `audit` (argument a literal or bound address) is in `ST`; not in `SF`.
- *Reflected-set tests*: for a grow-only address-valued domain `D` in term position (QD-refl) and `t` a literal or bound address: `t ∈ D` is in `ST`; `D = ∅` is in `SF`.
- *Boolean nodes*: `∧` and `∨` preserve `ST` and preserve `SF`; `¬` swaps `ST` and `SF`; `P ⇒ Q ∈ ST` when `P ∈ SF` and `Q ∈ ST`.
- *Quantifiers*: `(∃ x ∈ D :: P) ∈ ST` when `D` is grow-only and `P(x, ·) ∈ ST`; `(∀ x ∈ D :: P) ∈ SF` when `D` is grow-only and `P(x, ·) ∈ SF`. Over a step-constant `D`: additionally `(∀ x ∈ D :: P) ∈ ST` when `P(x, ·) ∈ ST`, and `(∃ x ∈ D :: P) ∈ SF` when `P(x, ·) ∈ SF`.
- *Aggregates*, over grow-only `D`, against ℕ literals: `count(D) ≥ c ∈ ST` and `count(D) ≤ c ∈ SF`. `count(D) = c` lives in neither. T1-extrema are excluded from both classes.

**Statement.** Every `ST` term is *⊤-stable*: once true at a reachable Σ, true at every `→_sh*`-successor. Every `SF` term is *⊥-stable*: once false, false forever.

*Ground*, by induction on the rules: a grow-only domain's denotation at Σ is contained in its denotation at every successor (bases by step effects; audit `M_K` because a union over a growing index set grows; filters because membership persists — element stays in base by growth, `ST` body stays true by induction; step-constant domains trivially — a constant set is contained in itself); no step removes a link address or rewrites a stored value (L12a and L12, carried across extended-record steps by B2 with RP-b, ASN-0128), so an existential witness persists with its content intact; a universal counterexample never leaves its domain; a count over a growing set never decreases, so satisfied lower bounds persist and violated upper bounds stay violated. ∎

---

## PD1 — ActiveNonMonotonicity (LEMMA, lemma)

Active-view and default-view terms are stable in neither direction, and the perturbations are different in kind.

*Active:* `(∃ x ∈ M_K :: P(x))` at view `active` flips ⊥→⊤ on a K-deposit and ⊤→⊥ on a retraction whose target carries the last witness — `Nullify_Binary` removes the tuple from `A_K^Σ` while `L_K^Σ` keeps it.

*Default:* the same term at view `default` additionally flips on a bare BH1-type emission — a `retired` deposit on a witnessing address removes it from every default-view enumeration (UV) with the queried type's own tuples untouched: presentation movement changes trigger truth.

---

## PD2 — FrameStability (LEMMA, lemma)

Per-step invariance, read off the frames and FP's footprints:

- Every PL term is invariant under every K.α step: no footprint reaches `dom(Σ.C)` (FP), and K.α frames everything a footprint can name.
- A term whose footprint excludes `dom(Σ.M)` is invariant under every K.σ step.
- For any set 𝒦 of registered coverage classes, a term reading only *audit* slices of types in 𝒦 is invariant under every deposit of a type outside 𝒦.
- The active-view clause reads: a *BH4-free, `targets_keyed`-free* term reading active slices of types in 𝒦 is invariant under deposits of types outside 𝒦 with `[R]` not on the depositing side.
  - A term containing BH4 atoms is additionally perturbed by same-home traffic of every type.
  - A term containing `targets_keyed` is perturbed by deposits of every BH3-attached Binary type.
  - A default-view term adds, through each UV-rewritten collection atom it contains, every BH1 type's active slice to its footprint (FP's default-view increment), shrinking the non-interference set by Φ.
