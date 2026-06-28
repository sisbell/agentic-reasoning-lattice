Reading the full dependency structure before diving into individual claims.

**Dependency graph**: S1 ← S0; S3 ← {S0 (via S1), S1, AX-1, AX-2}; S5 ← {S0, S1, S2, S3, T3}. AX-1, AX-2, S0, S2 are axioms; S1, S3, S5 are theorems. ASN-0034 contributes T3.

---

**AX-1, AX-2, S0, S2 (axioms)**. All four are correctly labeled as design posits. S0's scope note ("grounds the dependence of S3 and S5") is accurate: S3 depends on S0 via S1; S5 lists S0 as a dependency because the witnesses must model the transition-level invariant, which holds vacuously on their empty relation. AX-2's domain guard `v ∈ dom(Σ.M(d))` inside the second disjunct is correctly motivated: the application `Σ.M(d)(v)` is only evaluated after the guard is established, so the partial-function precondition is always met. No issues with any axiom.

**S1 (StoreMonotonicity)**. Proof: Let `a ∈ dom(Σ.C)` be arbitrary; S0 gives `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`; project the first conjunct. One-step, correct. Forward reference to GlobalUniqueness (ASN-0034) is correctly marked non-load-bearing. No issues.

**S3 (ReferentialIntegrity)**. The induction is on reachable states from `Σ₀`. Base case: AX-1 gives `dom(Σ₀.M(d)) = ∅`; S3's quantifier ranges over the empty set; holds vacuously. Inductive step: for `v ∈ dom(Σ'.M(d))`, the case split is `(v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))` versus its negation — exhaustive by `P ∨ ¬P`. Inherited case: IH gives `Σ.M(d)(v) ∈ dom(Σ.C)`; S1 gives `dom(Σ.C) ⊆ dom(Σ'.C)`; compose. New-or-redirected case: the disjunctive condition plus the outer `v ∈ dom(Σ'.M(d))` exactly matches AX-2's range; AX-2 delivers `Σ'.M(d)(v) ∈ dom(Σ'.C)`. The domain guard in the new-or-redirected case (`v ∈ dom(Σ.M(d))` preceding the application `Σ.M(d)(v)`) is consistent with AX-2's guard. Cases are exhaustive, each is correctly discharged, dependencies in the Formal Contract match the proof. No issues.

**S5 (UnrestrictedSharing)**. The construction device — taking each witness as the initial state of the trivial transition system with empty relation — correctly makes S0 and S1 hold vacuously (no transitions to quantify over) while requiring only the state-level verification of S2 and S3. Cross-document: `dᵢ = [1,0,1,0,i]` — same length 5, same components 1–4, distinct component 5; T3 gives pairwise distinctness. Within-document: `vₖ = [1,k]` — same length 2, same component 1, distinct component 2; T3 gives pairwise distinctness. S2 holds in both constructions (each arrangement is a well-defined partial function: distinct domain elements, each mapping to `a`). S3 holds in both (sole referenced address is `a ∈ dom(C) = {a}`). For each `N ∈ ℕ` the witnesses provide `N+1` pairwise-distinct pairs, establishing the formal postcondition. T3 is applied correctly in both constructions via contrapositive: tumblers with the same length but differing last component are unequal. No issues with the proof or the Formal Contract.

The body's remark that "finiteness is not entailed" is a stronger claim than the proved postcondition ("no finite uniform bound"), but the very next sentence explicitly acknowledges this distinction ("The displayed statement above asserts only the separate fact that no invariant imposes a uniform bound holding across all states"). The informal argument supporting it ("S0–S3 bound neither the number of documents nor the size of any dom(Σ.M(d))") is sound in a standard set-theoretic reading. The Formal Contract captures precisely what is proved. No downstream consumer is left with an unverified obligation.

---

VERDICT: CONVERGED