# ASN-0129: Substrate Predicate Composition

*From atomic predicates to the substrate's full query language — Boolean composition, quantification, aggregation, and the expressive ceiling.*

ASN-0128 ships the atomic read surface of the typed-relation substrate: per-type default predicates (D1–D3), behavior-unlocked predicates (BH1–BH4), the address-denotation discipline that types their arguments and results (AD/AM), and the three result-set views (audit, active, default). Each atom is specified singly. This note closes the chain: it defines what is expressible *from* the atoms — the algebra of Boolean composition, finite quantification, value composition, and aggregation under which the atomic vocabulary generates the substrate's full predicate language — and proves the ceiling: the language is *exactly* that closure (PC6), no richer and no poorer. Composition extends expressiveness within a ceiling fixed by the registry's shapes and behaviors; it never raises the ceiling.

The consumers are protocols: any coordination machinery built over the substrate — triggers ("act when P"), termination conditions ("stop when Q"), gating disciplines — is *written in* this language. PL is thereby the substrate's *extension language*: a builder registers types and composes predicates, and composition is the **only** extension mechanism — which is precisely why the guarantees hold for every predicate any builder will ever write, the substrate never executing foreign read-path code, only evaluating terms of a closed algebra. The properties proved here are what such machinery needs: purity (PC4) and termination (PC5) make predicates safe to evaluate concurrently and guaranteed to halt; the closure ceiling (PC6) makes the language's limits knowable; and the dynamics classification (PD0–PD2) tells a protocol author how a predicate's truth *moves* across transitions — the difference between a sound termination condition and a livelock. This note is the complete predicate foundation; what protocols are built, and under what scheduler, is application-layer territory fenced at the end.

**Depends:** ASN-0034 (Tumbler Algebra), ASN-0043 (Link Ontology), ASN-0086 (Typed Relations on Address Sets), ASN-0126 (Substrate Shape Framework), ASN-0127 (Content-Region Link Query — boundary only: the arrangement-reading query layer PL deliberately excludes), ASN-0128 (Substrate Type Operational Semantics).

## What this note commits

- **The atomic vocabulary, generated.** `V_atom` is derived per registered type from its registration record: a core template family every type receives, plus a behavior family per attached behavior — reconciling ASN-0128's fixed catalog with template generation. The vocabulary is static (V-STAT), a theorem of registry invariance rather than a stipulation.
- **Four composition primitives.** Boolean closure (PC0), finite quantification over substrate-derived domains (PC1), value composition with guarded partiality (PC2), and aggregation — counts and T1-extrema over finite domains (PC2a). Aggregation settles the count question: PL counts *sets of addresses in a view*, never bags; cross-type composites sum per-type set cardinalities (settling ASN-0128 Open Question 2).
- **Three-view parametricity.** Every composed predicate evaluates against a view in `{audit, active, default}` (ASN-0128's lenses), with one uniform rule for the default view (UV) that settles ASN-0128 Open Question 1: filtering rewrites enumeration *results* on every surface, never arguments, never traversal, never membership.
- **Evaluation guarantees.** Purity (PC4) and termination (PC5) for every PL term at every reachable state.
- **The ceiling.** PC6 (ExpressiveClosure): substrate-evaluable predicates are exactly PL. Corollary PC6a: PL contains no fixed-point operator, so transitive closure (`reach`) is *provably* outside the language — ASN-0128's deliberate withholding of multi-hop traversal, promoted from a design stance to a theorem.
- **Predicate dynamics.** A classification of PL terms by behavior across `→_sh` steps — monotone (PD0), non-monotone with the retraction counterexample (PD1), frame-stable (PD2) — the minimal stability theory a protocol author needs to choose trigger and termination predicates soundly.

## The atomic vocabulary

ASN-0128's registration record `(shape, idem, behaviors)` determines, per registered coverage class K, which read predicates exist. We make the determination a generator.

**V (AtomicVocabulary).** For each registered K, the *template family* `Tpl(record(K))` is:

- *Core family* — present for every K, whatever the record: the membership atom `is_K : T → Bool` (D2, ASN-0128) and the enumeration atoms `members(K, view) : ℘_fin(T)` (D1) and `targets_of(x, view) : T → ℘_fin(T)` (D3). For Unary K, `targets_of` is constantly ∅ (D3); the template still instantiates — degenerately, not absently.
- *BH1 family* (when read-filter is attached): `is_filtered : T → Bool`.
- *BH2 family* (when determinate-walk is attached): `succs : T → ℘_fin(T)`, `chain : T → Seq_fin(T)`, `tip : T → T ∪ {⊥}`, `is_in_chain : T × T → Bool`.
- *BH3 family* (when typed-reverse-lookup is attached): `sources_to : T → ℘_fin(T)`, `target_of : T → T ∪ {⊥}`, and the join `targets_keyed : T → Map_fin`.
- *BH4 family* (when age-staleness is attached): `age : T → ℕ` (partial: active tuples only), `stale : ℕ → ℘_fin(T)`.

The atomic vocabulary is `V_atom = ⋃_{K registered} Tpl(record(K))`, each atom's semantics exactly its ASN-0128 specification — this note adds no atom and changes none. The `idem` component contributes no atom: it is emit-side machinery (I1, I6), and its one read-side consequence — at-most-one active tuple per I0-class along surface-emitted derivations (I1a) — is a property of states, not a predicate former. Write operations (`Emit_K`, `Nullify_Binary`, `retract_stale`) are outside `V_atom` by construction: predicates read.

Atoms may be *internally iterative*: `chain` walks with a state-dependent step count, bounded by ASN-0128's BH2 termination argument. Internal iteration lives inside the atom, behind its proven bound; the composition primitives below add none. This division is load-bearing for PC6a.

**V-PRIM (PrimitiveAdmission).** The *state-independent primitives* are admitted to the vocabulary as degenerate atoms: address equality, the prefix order `≼`, the total order T1, and intrinsic comparison T2 (ASN-0034) — each Boolean-valued on addresses, reading no state; the finite-set operations on `℘_fin(T)`-valued terms — membership (`t ∈ S`), set equality and the emptiness test (`S = ∅`), each a finite enumeration of an already-finite value; and the meta-level comparisons on ℕ that PC2a's folds produce. They enter terms exactly as atoms do: in Boolean position, in QD filter bodies (the membership and `≼` tests in the worked compositions), and in PC2 chains. Admitting them *as vocabulary*, rather than leaving them ambient, is load-bearing twice over: PC2's typing quantifies over vocabulary members, so a composition through a comparison needs the comparison to be one; and PC6's converse direction enumerates leaf forms exhaustively, which an unadmitted ambient primitive would silently break.

**V-STAT (VocabularyStaticity).** `V_atom` is identical at every reachable state. *Proof.* The vocabulary is a function of the registration records alone, and the extended record is constant at every `→_sh*`-reachable state (R1, ASN-0128). ∎ Registering a new K extends `V_atom` by `Tpl(record(K))` — at construction only (R-VAL, ASN-0128); no transition changes the vocabulary. The expressive ceiling is thereby pinned to `Σ_init`'s registry, inheriting ASN-0128's registry-evolution fence (its Open Question 7).

**COD (Codomains).** Atom and composite codomains are drawn from

`Codom = {Bool, ℘_fin(T), T ∪ {⊥}, Seq_fin(T), Map_fin, ℕ}`

— Boolean, finite address set, optional address, finite address sequence, finite map, natural number. Every entry is realized by some atom above; PC0–PC2a compose within `Codom` and introduce no codomain beyond it.

**Two argument regimes, inherited.** Composition respects ASN-0128's AD/AM discipline: membership atoms test coverage (total, decidable), enumeration atoms return denoted addresses and match their arguments per AM (denotation-keyed forward, coverage-keyed reverse). A composite cannot convert between regimes except where ASN-0128's own bridges license it (the D2 bridge; the `targets_under` recipe — which this note exhibits below as a PL term rather than an atom).

## Quantification domains

**QD (QuantificationDomains).** The class of *domain expressions* is the least class containing the base expressions

`M_K` (the set `members(K, active)`), `A_K` (the active K-slice), `L_K` (the audit K-slice), `C_dom` (`dom(Σ.C)`), `L_dom` (`dom(Σ.L)`), `Reg` (the registered coverage classes)

and closed under *filtering*: if `D ∈ QD` and `P : D × S → Bool` is a Boolean PL predicate, then `{x ∈ D : P(x, ·)} ∈ QD` — a filter body may carry free arguments, making the domain expression *parameterized* (the worked `OPEN(t)` below); evaluation binds the parameters before interpreting. `QD` and `PL` are defined by mutual induction; the induction is well-founded on syntactic depth. Each `D ∈ QD` denotes at state Σ (and a binding of its parameters) a set `[D]_Σ` by the evident interpretation (`[Reg]_Σ` is state-independent by R1).

**QD-fin (DomainFiniteness).** `[D]_Σ` is finite for every `D ∈ QD` at every reachable Σ. *Proof.* Base cases: `dom(Σ.L)` is finite by L-fin (ASN-0043); `A_K^Σ ⊆ L_K^Σ` inject into `dom(Σ.L)`; `M_K` is finite by D1's bound (L-fin plus finitely many spans per endset, AD); `dom(Σ.C)` is finite because every reachable state is reached by a finite `→_sh*`-derivation (Definition Reachability, ASN-0126, as extended by R-TR, ASN-0128) and each step adjoins at most one content address (the K.α step effect, GatedTransitionRelation, ASN-0126); `Reg` is finite by C0 (ASN-0126). Filtering yields subsets. ∎

## The composition primitives

**PC0 (BooleanClosure).** For PL predicates `P, Q : S → Bool`, the pointwise `P ∧ Q`, `P ∨ Q`, `¬P`, `P ⇒ Q`, `P ⇔ Q` are PL predicates of the same signature. Both constituents read the *same* Σ and the same view (PC3). The `S → Bool` functions over fixed Σ form a Boolean algebra under these operations; no further axiomatization is needed.

**PC1 (QuantificationClosure).** For `D ∈ QD` and a PL predicate `P : D × S → Bool`,

`(∀ x ∈ D :: P(x, ·)) : S → Bool`  and  `(∃ x ∈ D :: P(x, ·)) : S → Bool`

are PL predicates: by QD-fin the quantifiers reduce at each Σ to finite conjunctions and disjunctions over `[D]_Σ`, well-defined by PC0. Filtered domains compose freely (a filtered active slice is again in QD), and quantifying over `Reg` expresses cross-type questions no single K's atoms can ask.

**PC2 (ValueComposition).** For PL predicates `f : S → C₁` and `g : C₁ → C₂` with matching types in `Codom`, the composition `g ∘ f : S → C₂` is a PL predicate. *Partiality is guarded, never silent*: the `T ∪ {⊥}` codomain (the `tip`/`target_of` verdicts, ASN-0128) composes only through the guard

`if f(s) ≠ ⊥ then g(f(s)) else c_default`

whose condition is a PC0 Boolean — partiality surfaces as a branch in the term, not as an undefined evaluation. ⊥ is a *verdict*, with meaning fixed by the atom that returns it (a branch, a cycle, multiplicity); the guard propagates the verdict, it does not erase it.

**PC2a (AggregationClosure).** For `D ∈ QD`:

- `count(D) = |[D]_Σ| : ℕ`, with the meta-level arithmetic comparisons (`=`, `≤`) on ℕ admitted in Boolean position;
- `max_{T1}(D)` and `min_{T1}(D)` over address-valued domains: the T1-extremum of `[D]_Σ` when non-empty, ⊥ when empty — well-defined because T1 totally orders tumblers (ASN-0034) and the domain is finite;
- `⋃(D, f) : ℘_fin(T)` for a set-valued PL term `f : D → ℘_fin(T)`: the union `⋃_{x ∈ [D]_Σ} f(x, Σ)` — a finite union of finite sets (the `targets_under` recipe's outer operation).

Both are finite folds over QD-fin domains — the same reduction PC1 performs with ∧/∨, performed with counting and comparison — so aggregation raises no expressiveness beyond the closure and needs no new evaluation machinery. Two commitments ride on PC2a. *Set semantics, settled*: `count` counts the elements of a domain interpretation — a set of addresses or tuples in the selected view — never occurrences; under `idem = ⊤` on surface-emitted derivations a per-class count is 0 or 1 (I1a, ASN-0128), under `idem = ⊥` the count is the deposit count because the *substrate* holds the duplicates as distinct tuples; the algebra itself is everywhere set-valued, and a cross-type composite is a meta-level sum of per-type counts (settling ASN-0128 Open Question 2). *Ordinal extrema, scoped*: `max_{T1}` over link addresses recovers emission order only within one home's chain (the ordinal-time doctrine, BH4, ASN-0128); cross-home T1 comparison is well-defined but temporally meaningless, and any "latest" built from it inherits the per-home scope.

**PC3 (ViewParametricity).** Every PL term evaluates against a view `v ∈ {audit, active, default}` (the lenses, ASN-0128) that fixes which slice its atomic queries consult; the view is fixed once per top-level term and inherited by every constituent, mixed-view terms requiring an explicit per-atom selector (the D2 bridge — `is_K` against `members(K, active)` — is the canonical licensed mix, and ASN-0128 marks why the selector there is load-bearing).

**UV (UniformDefaultView).** The default view's semantics, uniformly: *filtering rewrites enumeration results — on every enumeration surface — and rewrites nothing else.* Under `v = default`, every enumeration atom's result set (or sequence) drops elements `x` with `is_filtered_J(x)` for some BH1 type `J` distinct from the queried type; membership atoms are never rewritten; arguments are never filtered; and traversal is never filtered — `chain` walks the *active* denoted graph and the rewrite drops filtered elements from the returned sequence only, so a retired mid-chain element is traversed but not shown, and `tip` reports the active walk's verdict even when the tip itself is filtered from enumerations. ASN-0128 committed this rule for `members` and `targets_of` and left the behavior surfaces open (its Open Question 1); UV closes the question by generalizing the committed rule rather than inventing a second one, on ASN-0128's own ground: filtering is *presentation*, nullification is *state* — a rewrite that altered traversal or membership would let a presentation-layer mark change query topology, exactly the layer confusion the escape-hatch asymmetry exists to prevent (filtering is undone by selecting `active`; topology changes are undone by nothing).

**PC4 (Purity).** Every PL term is a pure function of `(Σ.C, Σ.M, Σ.L, Σ.registry)`, its arguments, and its view — the registry component constant by R1, so in practice of the three stores. No memoization, no emission-order dependence, no side effects: atoms evaluate through `Observe_K` and the active-subset machinery (ASN-0086), reading state alone; PC0–PC2a preserve purity by induction. Two evaluators of the same term at the same Σ agree — concurrent evaluation is safe by construction, coordination being entirely an emit-side concern.

**PC5 (TerminationOnFiniteSubstrate).** Every PL term's evaluation halts at every reachable state. *Proof sketch.* Atoms terminate by their ASN-0128 bounds (finite enumerations under L-fin/AD; `chain` by BH2's decreasing bound). PC0/PC2 are finite trees fixed by syntax; PC1/PC2a reduce to finite folds over QD-fin domains. ∎ With PC4: every PL predicate is decidable at every reachable state.

## The ceiling

**PC6 (ExpressiveClosure).** Define `PL` as the least class containing `V_atom` (V-PRIM's primitives included) and closed under PC0, PC1, PC2, PC2a. Then the substrate-evaluable predicates are exactly `PL`: every PL term is substrate-evaluable (PC4, PC5), and conversely every function evaluable from the substrate's read primitives lies in PL — the read primitives being exhaustively `Observe_K` (the one read on `Σ.L`), the active-subset machinery derived from it, domain membership against `dom(Σ.C)`/`dom(Σ.L)`, the registry lookup (constant, R1), and the state-independent primitives (V-PRIM). Any substrate evaluation therefore decomposes as a finite tree with Observe-queries, membership tests, and comparisons at the leaves and meta-Boolean, finite-quantifier, composition, and fold nodes internally — and the atoms enumerate the leaf forms (each atom is finitely many Observe queries plus a fixed combinator, ASN-0128), while PC0–PC2a enumerate the node forms. The ceiling moves only when the registry does: a new behavior or shape adds atomic forms; no composition does.

**Structural reads only.** What the enumeration *excludes* is as load-bearing as what it includes: no read primitive dereferences a content value `Σ.C(a)` or an arrangement binding `Σ.M(d)(v)`. PL consumes the structural substrate — the link store and registry, domain membership, address arithmetic — never the value mappings: a function testing the bytes at an address, or which content sits at a V-position, is outside PL and outside this note's claims, an agent-time operation rather than a substrate predicate. The exclusion is what PC6's converse leans on (with value reads excluded, the leaf forms are finitely enumerable), and it draws a deliberate layer boundary rather than leaving a gap: arrangement-reading queries are ASN-0127's territory — the `image`/`findlinks_V` algebra over `Σ.M`, with its own transition dynamics (E-MONO, D-NONMONO) — a separate query layer that meets PL only at the substrate both read. The typed-relation predicate language asks what the link store asserts; the content-region algebra asks what a document's arrangement reaches; neither subsumes the other, by design.

**PC6a (FixpointExclusion).** PL contains no fixed-point or recursion operator: a PL term's composition tree is fixed by its syntax, independent of Σ (atoms' internal iteration is bounded behind their own termination proofs and contributes leaves, not unrolling). Consequently *transitive closure is outside PL*: no PL term computes `reach(x, y)` over the denoted graph at every reachable state. *Sketch.* A PL term over the tuple structure has a fixed quantifier depth `k` determined by its syntax; distinguishing reachability along chains longer than the term can traverse defeats any fixed `k` — the standard inexpressibility of transitive closure in fixed-quantifier-depth first-order logic over finite structures, instantiated at the denoted graph. The walk atoms do not rescue it: `chain` is the *determinate* walk, halting at any branch (BH2), so a target behind a branch is invisible to every atom. ∎ This retires ASN-0128's authority-based withholding of `reach` ("both authorities place multi-hop traversal outside the system") as a theorem: an app computes closure by iterating `succs` at agent time; the substrate cannot be asked for it. Mutually-recursive predicate definitions ("settled iff every dependency is settled") are likewise outside PL and must be unrolled at agent time — a deliberate exclusion, not an oversight, and the first candidate (a least-fixed-point operator PC7) for a successor that consciously raises the ceiling.

## Predicate dynamics

PC4 and PC5 govern one evaluation at one state. A protocol author needs one more thing the language itself cannot say: how a term's truth behaves *across* `→_sh` steps — whether a trigger can be un-triggered, whether a termination condition, once reached, stays reached. PL deliberately has no temporal operators (PC6), so the dynamics live here as a classification of terms by their behavior along transitions, each class grounded in the step effects and frames already proven upstream (the step kinds and their frames: GatedTransitionRelation, ASN-0126, over extended-record states by R-TR, ASN-0128).

**PD0 (AuditMonotonicity).** A PL term whose atomic queries read only audit slices, in existential-positive position — built from `∃` over audit domains (`L_K`, `L_dom`), tests of stored tuple content, PC0's `∧`/`∨`, and PC2/PC2a over the same — is *⊤-stable*: once true at a reachable Σ, it is true at every `→_sh*`-successor. *Ground.* No step kind removes a link address or rewrites a stored value — `dom(Σ.L)` grows monotonically along every derivation (L12a per step) and stored values are immutable (L12), both carried across extended-record steps by ASN-0126's B2 with RP-b (ASN-0128) — so every audit-slice witness persists with its content intact, and an existential witnessed at Σ remains witnessed. *Duality.* A universal over an audit domain is the mirror class, *⊥-stable*: once false (a counterexample deposited), false forever — the counterexample never leaves the slice. "Has this ever happened" is the monotone question; "has nothing of this kind ever happened" is its anti-monotone dual; neither oscillates.

**PD1 (ActiveNonMonotonicity).** Active-view and default-view terms are stable in neither direction, and the perturbations are different in kind. *Active:* `(∃ x ∈ M_K :: P(x))` flips ⊥→⊤ on a K-deposit and ⊤→⊥ on a retraction whose target carries the last witness — `Nullify_Binary` removes the tuple from `A_K^Σ` while `L_K^Σ` keeps it. A fire-until-Q loop whose Q is an active-view term can therefore *un-terminate*: Q true at Σ, false again at a successor, with no monotone measure in the language to forbid the oscillation. *Default:* a default-view term additionally flips on a bare BH1-type emission — `retired` deposited on a witnessing address removes it from every default-view enumeration (UV) with the queried type's own tuples untouched: presentation movement changes trigger truth. A protocol that wants a stable gate over active state must either supply the stability *outside* the language (an operating discipline under which the falsifying steps cannot occur — the move DR makes for C3, ASN-0128) or anchor on PD0's audit class instead.

**PD2 (FrameStability).** Per-step invariance, read off the frames. A PL term whose domains and atoms consult only the link store and registry — no `C_dom` — is invariant under every K.σ and K.α step: both frame `Σ.L` and the registry outright (their frame clauses, ASN-0126), so every atomic query in the term evaluates against identical components. Sharper, per type: a term reading only *audit* slices of types in a set S is invariant under every deposit of a type outside S — the deposit grows only its own slice. The active-view refinement must respect the one cross-type effect the substrate has: a term reading *active* slices of S is invariant under deposits of types outside S **only when** `[R] ∉` the depositing side — an R-deposit nullifies addresses of other types and can shrink any active slice (the same cross-effect I1a's induction handles, ASN-0128). PD2 is the protocol author's non-interference tool: a trigger built from audit slices of its own types is untouched by every unrelated fire, exactly, and a trigger over active slices is untouched by unrelated fires *except retractions* — name the exception or be surprised by it.

The three classes compose with the algebra in the expected way — PC0's `∧` of two ⊤-stable terms is ⊤-stable, `¬` swaps PD0's classes, PC1 over a *growing* domain preserves ∃-stability and breaks ∀-stability — and the classification is the load-bearing input to any termination argument built over this substrate: a sound "stop when Q" wants Q in PD0's class, or wants the discipline that removes PD1's falsifiers stated as an explicit hypothesis. The termination arguments themselves — convergence of fire-until-stable loops, re-opening rules when upstream state moves — are protocol-layer constructions over these classes, outside this note's scope.

## Worked composition

Fix two illustrative app classes alongside ASN-0128's shipped three: `cmt` — Binary, idem=⊥, a comment from a finding address to a target address — and `res` — Binary, idem=⊤, a resolution from a target back to a comment. (These are illustrative registrations exercising the algebra, not standard registrations.)

*The filtered domain.* The open comments on target `t`:

`OPEN(t) = {c ∈ M_cmt : t ∈ targets_of_cmt(c, active) ∧ ¬(∃ r ∈ M_res :: c ∈ targets_of_res(r, active))}`

— a QD filter over the base domain `M_cmt`, whose filter body is PC0 over a membership test, an enumeration atom, and a PC1 existential.

*Quiescence-shaped predicate.* `quiescent(t) ≡ OPEN(t) = ∅` — equivalently `count(OPEN(t)) = 0` (PC2a) or `¬(∃ c ∈ OPEN(t) :: ⊤)` (PC1): one composite, three equivalent spellings, all in PL with signature `T → Bool`. Evaluated against `active`; the `audit` evaluation asks "was every comment ever resolved at some point recorded" — a different and rarely wanted question, which is why the view is fixed per term (PC3).

*Aggregation with a cap.* `under_cap(t, n) ≡ count({c ∈ M_cmt : t ∈ targets_of_cmt(c, active)}) ≤ n` — count and meta-comparison (PC2a); the operator pattern for any bounded-cycles discipline.

*Value composition through a verdict.* "t's current head is unretired": with `supersedes` shipped (S2, ASN-0128) and BH2 attached,

`head_live(t) ≡ if tip(t) ≠ ⊥ then ¬is_retired(tip(t)) else ⊥-case`

— PC2's guarded composition through the `T ∪ {⊥}` codomain; the ⊥-case branch is the term author's explicit decision (a branch or cycle at `t` is a *verdict*, and PC2 forces the author to handle it rather than inheriting an undefined value).

*A derived recipe as a PL term.* ASN-0128's `targets_under(addr)` — "an app-side composition rather than a fourth shipped predicate" — is exactly

`targets_under(addr) = ⋃ {targets_of(x, active) : x ∈ {y ∈ M_K(active) : y ≼ addr}}`

a PC2a-style finite union over a QD filter whose body is the T2-decidable prefix test: the algebra is where ASN-0128's recipe lives.

*Cross-type universal.* "every registered class's active slice is non-empty somewhere under d" — `(∀ K ∈ Reg :: (∃ x ∈ M_K :: d ≼ x))` — the `Reg`-quantification no single type's atoms express (PC1, consequence (c)).

## What this note doesn't cover

- **Protocol constructions.** Triggers paired with write operations, termination conditions and their convergence arguments, re-opening rules, and scheduler disciplines (fairness, fire atomicity, non-interference) are application-layer machinery *written in* PL and *typed by* PD0–PD2, but not part of the predicate foundation: this note supplies the language, its evaluation guarantees, and its dynamics; what is built from them is the builder's.
- **Range-valued predicate atoms.** Inherited from ASN-0128: the surface is address-denoting; a predicate layer over span extents is deferred with it.
- **Normal forms.** Whether PL-modulo-extensional-equivalence admits a normal form, and an effective procedure deciding extensional equivalence of terms, are open theory (Open question 3); well-typing is decidable already (signature unification against COD plus registry lookup).

## Open questions

1. **First-class views.** PC3 fixes one view per top-level term, the D2 bridge being the licensed exception. Should the view be a first-class parameter (`P[v]`) admitting fine-grained mixing — and if so, what invariants must hold across a view boundary inside one term (e.g., is an `audit`-view domain filtered by an `active`-view predicate coherent)?

2. **Existential-witness domains.** QD is base-plus-filter. Domains defined by witness extraction — "the set of x such that some y witnesses P(x, y)" — are expressible only by flattening the witness into PC1's quantifier prefix. Is the flattening always possible within PL, or are there meta-expressible domains PL cannot construct?

3. **Extensional normal form.** Is there an effective procedure deciding whether two PL terms denote the same predicate at every reachable state? Syntactic identity is trivially decidable; extensional equivalence over the reachable-state class is the open half.

4. **The fixpoint successor.** PC6a excludes recursion deliberately. If a forcing case arrives (a protocol whose gating genuinely needs dependency-chain walking rather than agent-time unrolling), the conscious extension is a bounded least-fixed-point operator with an explicit termination measure — raising the ceiling by a named primitive rather than by accident. What measure discipline keeps PC5 for such an operator?

5. **Deciding the dynamics class.** PD0–PD2 classify by syntactic criteria (view, polarity, domains read). Is class membership decidable for arbitrary PL terms — in particular, is there an effective syntactic check that soundly (if incompletely) certifies ⊤-stability for terms mixing views or polarities, so that a protocol checker can validate a termination condition mechanically?
