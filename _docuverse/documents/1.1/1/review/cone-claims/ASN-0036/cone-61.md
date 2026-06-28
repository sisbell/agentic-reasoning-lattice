**Dependency DAG trace (AX-1, AX-2, S0, S1, S3):**

- AX-1, AX-2, S0 are axioms; no internal preconditions.
- S1 depends on S0 only: the single proof step extracts the first conjunct of S0's implication. Sound.
- S3 depends on AX-1, AX-2, S1: base case vacuous (AX-1), inductive step splits into two exhaustive cases.

**AX-2 range correctness.** The outer guard `v ∈ dom(Σ'.M(d))` makes the body application `Σ'.M(d)(v)` well-defined. The inner disjunction `(v ∉ dom(Σ.M(d)) ∨ (v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) ≠ Σ.M(d)(v)))` covers exactly the non-inherited positions. The redundant guard in the second disjunct is correctly explained as a strict-partial-function discipline, not a classical addition. The prose and formal statement agree.

**S3 case split coverage.** For fixed `v ∈ dom(Σ'.M(d))`, the two cases — `(v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v))` vs. its negation — are exhaustive and mutually exclusive under classical logic. Case 1 discharges by IH + S1. Case 2 range coincides exactly with AX-2's inner disjunction (with `v ∈ dom(Σ'.M(d))` already fixed), so AX-2 fires precisely when needed. Both cases land `a ∈ dom(Σ'.C)`.

**Precondition chain integrity.** S3's proof invokes S1 in Case 1. S1 is proved from S0. S0 is an axiom valid for every transition. No step reaches outside its declared preconditions.

**AX-2 invocation soundness.** The proof correctly notes that S1 alone cannot discharge Case 2 — S1 preserves existing addresses in `dom(C)` but is silent on whether a fresh mapping may target an unstored address. AX-2 is the independent protocol posit that closes this gap. The argument distinguishing the two axioms' domains of responsibility is accurate.

**Declared dependencies vs. actual use.** S1 uses S0 (declared). S3 uses S1, AX-1, AX-2 (all declared). No undeclared dependency is invoked; no declared dependency is unused.

**Frame conditions.** S3's quantifier ranges over `dom(M(d))`, so content in `dom(C) \ ⋃_d ran(Σ.M(d))` is unconstrained. The frame claim in the Formal Contract follows directly from the quantifier structure.

VERDICT: CONVERGED