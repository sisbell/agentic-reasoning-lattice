Reviewing this cone required tracing the `Σ.M(d)` notation discipline across S8a, D-CTG, subspace, V-sub, S8-depth, D-INJ, S8-fin, Σ.M(d) itself, D-PRED, NAT-induction, AX-1, and D-CTG-depth, plus re-checking the D-INJ and D-CTG-depth proofs case-by-case. The proofs themselves (D-INJ's induction, D-PRED's induction, D-CTG-depth's contradiction) are sound and complete their case coverage. I found a residual notation defect: the recent fix commits explicitly targeted "bare `M(d)`" as an ungrounded-symbol bug and swept it from D-CTG's quantifier and "remaining spots" in D-CTG-depth, but several instances survived in three claims' prose.

### S8a intro prose retains ungrounded `dom(M(d))`
**Class**: REVISE
**Foundation**: Σ.M(d) (Arrangement)
**ASN**: S8a (ArrangementDomainRestriction), body prose: "OrdShiftHom part (b) carries it as the hypothesis it shows `shift(v, n)` preserves, and S8's forward lockstep walk takes it as the base-case guarantee that every `v ∈ dom(M(d))` is a well-formed V-position."
**Issue**: Only `Σ.M(d)` (or `Σ₀.M(d)` at the base state) is a defined symbol, established by the Arrangement claim as a state-indexed family. Bare `M(d)` is never defined anywhere in the Formal Contracts. Every other occurrence of the arrangement domain in this same claim — including its own Axiom and Consequence clauses — correctly writes `Σ.M(d)`, so this is a residual instance of exactly the defect class the pipeline already fixed elsewhere (git history: "replace bare M(d) with Σ.M(d) in remaining spots").
**What needs resolving**: Replace `dom(M(d))` with `dom(Σ.M(d))` in this sentence.

### S8-fin intro prose retains ungrounded `dom(M(d))` (two instances)
**Class**: REVISE
**Foundation**: Σ.M(d) (Arrangement)
**ASN**: S8-fin (FiniteArrangement), body prose: (1) "several downstream proofs need an explicit, citable finiteness premise, most sharply S8, whose forward lockstep walk on `dom(M(d))` terminates only because the domain is finite and whose maximal-run decomposition is finite for the same reason"; (2) "Every consumer (S8, D-SEQ, D-CTG-depth, D-MIN) reads S8-fin solely as the property that `dom(M(d))` is finite — forward walks terminate, a non-empty subset has a least element, no infinite strictly-increasing sequence of positions fits inside it"
**Issue**: Same ungrounded-symbol defect as above. S8-fin's own Formal Contract Axiom and Depends entries are meticulous about always writing `Σ.M(d)`/`Σ₀.M(d)` (and even explain, for the `T0` dependency, exactly which symbols T0 does and does not export) — the two bare instances in the surrounding prose are inconsistent with that same claim's own rigor.
**What needs resolving**: Replace both `dom(M(d))` occurrences with `dom(Σ.M(d))`.

### D-CTG-depth proof body retains ungrounded `dom(M(d))` (two instances)
**Class**: REVISE
**Foundation**: Σ.M(d) (Arrangement); S8a (ArrangementDomainRestriction)
**ASN**: D-CTG-depth (SharedPrefixReduction), proof body: (1) "wᵢ = uᵢ > 0 for i ≤ j by S8a's positivity *Consequence*, which exports `(A i : 1 ≤ i ≤ #u : uᵢ > 0)` and so gives u's components their strict positivity directly (u ∈ V_1(d) ⊆ dom(M(d)), so S8a applies)"; (2) "D-CTG's conclusion places w in V_1(d) ⊆ dom(M(d)), where every position satisfies S8a"
**Issue**: Same ungrounded-symbol defect, and here it is self-inconsistent within the same claim: D-CTG-depth's own Depends entry for S8a, explaining this exact same positivity step, correctly writes "applied to u ∈ V_1(d) ⊆ dom(Σ.M(d)) it gives u's components their strict positivity" — so the proof body and the Depends section disagree on the notation for the identical inference. This is precisely the pattern the prior commit (fix(asn-36/D-CTG-depth): replace bare M(d) with Σ.M(d) in remaining spots) targeted but did not fully clear.
**What needs resolving**: Replace both `dom(M(d))` occurrences with `dom(Σ.M(d))`, matching the Depends section's own phrasing of the same step.

VERDICT: REVISE