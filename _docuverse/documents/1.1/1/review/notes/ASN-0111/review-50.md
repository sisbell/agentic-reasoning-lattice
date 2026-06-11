# Review of ASN-0111

## REVISE

No REVISE items. The note was checked claim by claim; the verification performed is recorded below so the verdict is auditable rather than asserted.

**RL0 (totality, screen, insufficiency).** The wp derivation for `R_ok` and `R_⊥` is a genuine substitution argument, and the complementarity of the two weakest preconditions is established (the `⊥ ∉ Link` stipulation is declared where it is needed). The structural screen's left-to-right well-definedness is properly discharged: `T4-valid(a) ∧ zeros(a) = 3 ⟹ #E(a) ≥ 1` is derived from T4a/T4b/T4c, not assumed, and the example `[1, 0, 0, 2, 0, 3]` exercises the guard. Necessity of each conjunct is cited to the correct invariant (L0b, L1, L0, L1b). The insufficiency argument correctly restricts to *satisfiable* predicates and witnesses failure at `Σ₀`, where `dom(Σ₀.L) = ∅`.

**RL1/RL2/RL3.** Definitional, with the right vacuity check: the observation that `Link` is closed under shrinking a connective slot shows completeness is enforced by the definition rather than the type — this is real content, not padding. Role preservation handles arity > 3 explicitly, and the ghost-type case is covered by L8/L9.

**SOV.** The coupling vacuity is argued conjunct by conjunct (J0 over `dom(C') \ dom(C) = ∅`, J1★ over an unchanged content-subspace range, J1'★ over `R' \ R = ∅`), and ValidComposite★'s two clauses are both addressed. The K.δ document case is correctly inside SOV's conditions — registration adds an empty arrangement, so no content-subspace range grows.

**RL4.** The statement plus the failure-branch congruence do jointly yield "function of `(a, Σ.L(a))`," and the distinction from the weaker "function of `(a, Σ.L)`" is correct and load-bearing. The witness construction was checked step by step: the K.δ bootstrap chain (`zeros` side conditions at `n₀` and `[1.0.1]` both satisfied), branch-enabledness of K.λ at the common frontier `a'` (K.λ constrains the value only through L3), and the branch-independence of the second K.λ at `c = inc(a', 0)` (state-dependent conjuncts consult only `dom(L)` and `dom(M)`, identical across branches). The span `(a', δ(1, 8))` is T12-well-formed and `a' ∈ coverage(ℓ_c.e₂)` by PrefixSpanCoverage. Reachability of both endpoints is discharged by SOV, not assumed.

**RL5.** Stability via LP13 is correct. The three permanence families were each re-derived: depth via LP-Sub plus the `#E = 2` form of `F`; lineage via the L1a → P8 → P8 → NodeLineage contradiction chain (each P8 application checked against the stratification); user-field via the account induction, which covers all four account-producing branches of K.δ (case (i) makes nodes; k = 1 takes document operands; k = 2 from a node yields `U = [1]` by TA5(d); k = 0 preserves `#U` by TA5(c)/TA5-SigValid). The exhaustiveness construction for the residual class was checked phase by phase: node baptism (zero-free `N(a)` with `N(a)₁ = 1` is T4-valid and `n₀`-descended), account spawn plus frontier advances (contiguity of realized domains makes "reached or already present" sound), document field realisation (alternating k = 1 appends and k = 0 terminal advances realise every zero-free field, with `parent` conditions satisfied at each step), and the element phase via ChainMembershipForOrigin's contiguous initial segment giving `j₀ < k`. The caching discipline follows; its closing sentence adds the completeness direction (the proofs of (ii) cover the whole permanently-absent class), so it is not duplication.

**Worked read.** Arithmetic verified: `zeros` positions and field projections of `a`, `a'`, `c`, and the three family examples are all correct; `δ(2, 8)` reach and the two-subtree decomposition of the first from-span agree with PrefixSpanCoverage; the LP-Fin Corollary candidate counts (2 + 1) match the stipulated `dom(C)` members. The reachability route is honest about J0 — the unarranged configuration is built by valid K.α+K.μ⁺+K.ρ composites followed by K.μ⁻ contractions with `n'_{s_C} = 0`, whose coupling vacuity is correctly discharged via J2, with P2/P4★/P7a checked at the boundaries.

**Anti-bloat scan.** The flagged patterns were searched for specifically. The single forward deferral ("proved below, at the structural screen") resolves once and is not repeated; SOV's two-sentence introduction states a factoring decision and then delivers the lemma; the RL5 summary sentences each add content (the address-computable test formulations, the `n₀ ≼ N(a) ⟺ N(a)₁ = 1` reduction, the caching-rule completeness). No paragraph addresses a case its carrier excludes, no axiom is wrapped in rationale prose, and no two paragraphs restate each other. Citation hygiene is clean: every reference is to a foundation ASN, and no foundation notation is reinvented.

## OUT_OF_SCOPE

### Topic 1: What a reader may conclude about a relationship's continued *validity* from a read alone
**Why out of scope**: The read deliberately consults no arrangement; semantics of unwitnessed-versus-resolvable endsets belongs to the FOLLOWLINK/projection ASN, and the note already poses this as an open question rather than claiming it.

### Topic 2: Distinguishability guarantees for value-identical links
**Why out of scope**: Address-carried identity under value coincidence (L11b/R1 territory) is a guarantee about how callers consume read results across operations, not about the read itself; correctly deferred in Open Questions.

VERDICT: CONVERGED
