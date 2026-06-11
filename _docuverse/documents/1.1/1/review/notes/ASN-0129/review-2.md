# Review of ASN-0129

## REVISE

### Issue 1: PC6's converse is circular as argued, and its unqualified statement contradicts C-reach
**ASN-0129, PC6 (ExpressiveClosure)**: "The predicates evaluable from that base are exactly PL. … Any substrate evaluation therefore decomposes as a finite tree with Observe-filters, per-tuple reads, domain memberships, registry lookups, and V-PRIM leaves…"
**Problem**: "Evaluable" is never defined, and the equality is false or vacuous depending on the reading. Under the natural reading — decidable by a terminating procedure whose only state access is the enumerated base — transitive closure *is* evaluable: at every reachable state the denoted graph is finite (L-fin, QD-fin), so `R := {x}; repeat R := R ∪ ⋃_{y∈R} succs(y) until stable` terminates and decides `reach(x, y)` using only base reads. The note itself concedes this procedure exists ("an app computes closure by iterating `succs`"), and C-reach conjectures `reach ∉ PL` — so the unqualified equality is (conjecturally) false. Under the alternative reading — "substrate evaluation" means evaluation of a PL term — the theorem is a tautology. The "therefore" derives tree-decomposability from the leaf analysis alone; tree shape (no evaluation-time control flow, iteration confined to registry-fixed atoms behind per-atom termination proofs) is an *assumption about the evaluation class*, not a consequence. The note states that division ("Internal iteration lives inside the atom… the composition primitives below add none") as a property of PL, not as the definition of the class PC6 quantifies over. Relatedly, the forward direction's parenthetical "(each ASN-0128 atom is itself such a tree: finitely many Observe queries plus a fixed combinator)" is wrong for `chain`: its number of reads is state-dependent; it is a bounded-iteration combinator, not a fixed finite tree.
**Required**: Define the evaluation class non-circularly (e.g., computations whose base-call structure is a finite tree fixed by syntax, with iteration permitted only inside the fixed atom set), restate PC6 relative to that class, and state explicitly that against unrestricted base-read computation the ceiling claim is exactly as conjectural as C-reach. Fix the "fixed combinator" parenthetical to admit bounded internal iteration.

### Issue 2: PC2's typing excludes its own worked example, and the guard has no narrowing rule
**ASN-0129, PC2 (ValueComposition) / V-PRIM / Worked composition**: "For PL predicates `f : S → C₁` and `g : C₁ → C₂` with matching types in Codom, the composition `g ∘ f : S → C₂` is a PL predicate… compose only through the guard `if def(f(s)) then g(f(s)) else c_default`" and "no equality operation on a ⊥-adjoined codomain itself is needed, and none is admitted."
**Problem**: Two typing gaps. (a) `g : C₁ → C₂` admits only state-independent outer functions, but `head_live(t) = if def(tip(t)) then ¬is_retired(tip(t)) else …` composes through `is_retired`, which reads Σ. PC0 states the same-Σ/same-view provision; PC2 does not. (b) Inside the then-branch, `f(s)` still has type `T ∪ {⊥}` while `g`'s domain and the equality `f(s) = c` are typed over `T`; no narrowing or coercion rule is admitted, and the note explicitly declines operations on ⊥-adjoined codomains beyond `def`. Under the note's own typing discipline — which V-PRIM declares load-bearing for PC6's leaf enumeration — `g(f(s))` and `f(s) = c` are ill-typed even under the guard; `head_live` does not type-check in its own language.
**Required**: Restate PC2 over state-indexed functions evaluated at the same Σ and view, and give the guard a typing rule — either a binder form (`if f(s) is some y then … y … else c_default`) or an explicit narrowing rule keyed to the `def`-test.

### Issue 3: QD-fin's base case rests on an uncited premise
**ASN-0129, QD-fin (DomainFiniteness)**: "the base, `|dom(Σ_init.C)| < ∞ ∧ |dom(Σ_init.M)| < ∞`, holds because `Σ_init`'s three stores are ASN-0086's initial components verbatim (R-VAL, ASN-0128), finite stores"
**Problem**: R-VAL gives verbatim-ness and `Σ_init.L = ∅` only. No foundation claim supplied — in ASN-0086, ASN-0126, or ASN-0128 — states that ASN-0086's initial content and arrangement stores are finite. "Finite stores" is asserted, not cited. QD-fin carries PC1, PC2a, and PC5; the load justifies precision here.
**Required**: Cite the foundation clause that fixes `Σ_init^{0086}`'s C and M components (empty or finite), or state initial-store finiteness as an explicit named hypothesis of this note.

### Issue 4: A QD domain expression is used in term position with no licensing rule
**ASN-0129, Worked composition**: "`quiescent(t) ≡ OPEN(t) = ∅` — equivalently `count(OPEN(t)) = 0` (PC2a) or `¬(∃ c ∈ OPEN(t) :: ⊤)` (PC1…): one composite, three equivalent spellings, all in PL"
**Problem**: `OPEN(t) = ∅` places a set-builder domain expression in term position as an operand of V-PRIM's set equality, which is defined "on `℘_fin(T)`-valued terms." QD closes terms into domains; no rule closes domains into terms (and no singleton constructor exists to rebuild the set via `⋃`). The first spelling is not generated by the stated grammar. Note that a general domain→term rule must be restricted to address-valued domains — `A_K`/`L_K` are tuple-valued and `Reg` class-valued, outside `℘_fin(T)`.
**Required**: Add the explicit rule (every address-valued QD domain expression is a `℘_fin(T)`-valued PL term), or strike the first spelling and keep the count and quantifier forms.

### Issue 5: The "activeness test composition otherwise lacks" justification is refuted by the note's own algebra
**ASN-0129, V (BH4 family)**: "with ⊥ a value, the definedness test `age(a) ≠ ⊥` (V-PRIM) is the activeness test composition otherwise lacks (no atom tests tuple-address activeness — `is_K` tests F-coverage, not tuple addresses)"
**Problem**: Composition does not lack it. `(∃ x ∈ A_K :: addr(x) = a)` is a PL term — PC1 over the QD base `A_K`, V-TUP's `addr`, V-PRIM's address equality — testing exactly tuple-address activeness, and it works for *every* registered K. By contrast `age` exists only for BH4-attached (`idem = ⊥`) types, so it could not be the language's activeness test even in principle. The atom-level parenthetical is true; the "composition otherwise lacks" clause is false. The first half of the rationale (an unguarded partial atom would make definedness state-dependent, poisoning PC4/PC5 and the dynamics) is correct and sufficient on its own.
**Required**: Delete or correct the "otherwise lacks" clause; rest the totalization on the definedness-stability ground alone.

### Issue 6: FP under-reports `targets_keyed`'s footprint, making PD2's per-type clause unsound for terms containing it
**ASN-0129, FP (ReadFootprints)**: "BH2 and BH3 atoms of K: `L_K` and `L_R` (active-view reads, ASN-0128)"
**Problem**: `targets_keyed` "joins `target_of` across every Binary type K registered with BH3" (ASN-0128, BH3), so its footprint is the union of `L_J` over *all* BH3-attached Binary types J, plus `L_R` — it is not indexed by one K at all. As written, PD2's active clause ("a BH4-free term reading active slices of types in S is invariant under deposits of types outside S with [R] not on the depositing side") certifies invariance for a `targets_keyed`-bearing term with S = {K}, which is false: a deposit of another BH3-attached type J changes `targets_keyed`'s value. The footprint table is PD2's soundness input; it must be exact — the note takes exactly this care for BH4's home-wide footprint and should take it here.
**Required**: Add `targets_keyed`'s cross-type footprint and name the exception in PD2 the way the BH4 exception is named.

### Issue 7: The two enumerations of "exactly three admissions" disagree
**ASN-0129, What this note commits**: "Three admissions are this note's own…: audit readings for the core family (V-AUD), per-tuple projections and coverage-membership tests (V-TUP), and the state-independent primitives, constants, and literals (V-PRIM)." versus **V (AtomicVocabulary)**: "This note's own additions to the read surface are exactly three…: the audit readings of the core family (V-AUD), the per-tuple projections (V-TUP), and `age`'s ⊥-totalization above."
**Problem**: The third member differs (V-PRIM vs. the ⊥-totalization), and by the texts' own accounting there are four additions in total. A self-contradiction in the note's bookkeeping of its own read-surface extensions — precisely the accounting PC6's converse leans on being exhaustive.
**Required**: One consistent enumeration in both places — presumably four additions, or three plus an explicit argument for why the omitted item is not a read-surface addition.

### Issue 8: The `elems`/`chain` count identity fails at the default view
**ASN-0129, V-PRIM**: "(on `chain`'s output it loses no count: the walk's elements are pairwise distinct, BH2, so `count(elems(chain(t)))` is the walk's length)"
**Problem**: At view `default`, UV rewrites `chain`'s returned sequence by dropping filtered elements while traversal is unfiltered ("a retired mid-chain element is traversed but not shown in the returned sequence"). The count is then the rewritten sequence's length, strictly less than the walk's length whenever a traversed element is filtered. The identity as stated is unqualified.
**Required**: Qualify the identity to the audit/active views, or restate it as "the returned sequence's length" with the default-view caveat.

### Issue 9: `Map_fin` is an admitted codomain with zero admitted operations
**ASN-0129, COD**: "Every entry is realized: … `Map_fin` by `targets_keyed`"
**Problem**: No node form consumes `Map_fin`: PC2 has no vocabulary member with domain `Map_fin`, and V-PRIM admits no map lookup, map equality, or key-set projection. A `targets_keyed` result can therefore appear only at a term's root — it composes with nothing, and cannot even be compared. An admitted codomain with no admitted operations is unflagged dead vocabulary in an algebra whose converse direction claims the leaf and node forms are exhaustively enumerated; by the project's own ethos, unused machinery is unverified obligation.
**Required**: Either admit a consumer (lookup `m[K] : T ∪ {⊥}` — noting its redundancy with `target_of` — and/or a key-set projection), or state explicitly that `Map_fin` is root-position-only and why it is worth carrying in COD.

### Issue 10: T2 is listed as an atom; it is a computability theorem, not a relation
**ASN-0129, V-PRIM**: "the comparisons on addresses: address equality, the prefix order ≼, the total order T1, and intrinsic comparison T2 (ASN-0034) — each Boolean-valued, reading no state"
**Problem**: T2 (IntrinsicComparison) is not a relation distinct from T1; it is the theorem that the T1 ordering is computable from the two tumblers alone. Listing it as a separate Boolean-valued atom puts a non-form into the leaf enumeration that V-PRIM itself declares must be exact for PC6's converse. The note uses T2 correctly elsewhere ("the T2-decidable prefix test").
**Required**: List the comparison atom once (T1 order, ≼, equality) and cite T2 as its computability warrant rather than as an atom.

### Issue 11: PC3's view discipline is presented as a semantic boundary, but it fences no expressiveness
**ASN-0129, PC3 (ViewParametricity)**: "There is no author-selectable per-constituent view in PL: a term 'mixes' views only through fixed-view constituents, whose slice is fixed by definition, never by selection — first-class view parameters, and the coherence conditions they would need, are deferred (Open Question 1)."
**Problem**: The deferral is of surface syntax only. The audit core readings are reconstructible inside a term of any view from the named slices: `⋃(L_K, addrs_F)` is exactly `members(K, audit)` (V-AUD), `(∃ x ∈ L_K :: t ∈ coverage_F(x))` is audit `is_K`, and the filter `{x ∈ L_K : P_active(x)}` is precisely Open Question 1's "audit-view domain filtered by an active-view predicate" — already a well-formed PL term whose semantics this note has therefore already fixed, not deferred. The one-view-per-term rule governs only which reading the core atom *names* denote; full cross-view data mixing is expressible today. In a note whose deliverable is exactly-what-is-expressible, presenting a thin naming convention as a deferred semantic capability misstates the ceiling.
**Required**: State that cross-view readings are derivable now via `A_K`/`L_K` + V-TUP + PC2a, restate PC3's claim as a convention about atom-name binding, and re-scope Open Question 1 to first-class syntax and pragmatics (its coherence example being already answered by the existing semantics).

## OUT_OF_SCOPE

### Topic 1: Evaluation atomicity under interleaved transitions
PC4 fixes determinism at a single Σ; nothing specifies that a multi-atom evaluation observes one consistent state while `→_sh` steps interleave (torn reads across a long conjunction). **Why out of scope**: this is an obligation on the evaluation engine/scheduler, which the note correctly fences to the application layer; every claim here is per-fixed-Σ. A future runtime/protocol ASN should name the snapshot assumption.

### Topic 2: Cost model
No complexity accounting (Observe-call counts, per-atom costs, term-size bounds on evaluation). **Why out of scope**: the chain has specified no performance model anywhere; the guarantees here are purity and termination only, and a cost model is its own territory.

### Topic 3: Positive expressiveness characterization
Beyond the closure definition and the negative C-reach conjecture, there is no characterization of which classes of state properties PL captures (e.g., relative to counting first-order logic with built-in order on finite structures). **Why out of scope**: Open Question 6 covers the negative side; a positive characterization is new theory, not an error in this note.

VERDICT: REVISE
