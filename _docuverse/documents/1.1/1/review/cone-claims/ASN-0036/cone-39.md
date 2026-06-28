**Dependency graph trace.** AX-1, AX-2, S0 are axioms — no proofs to audit. S1 is proved in a single step from S0. S3 is proved by structural induction on transition sequences, invoking AX-1 (base), then S1 and AX-2 on the inductive step.

**S0 → S1.** S0 gives `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The proof projects the first conjunct. The step is valid and complete.

**AX-1 + S1 + AX-2 → S3.**

*Base case.* AX-1 sets `dom(Σ₀.M(d)) = ∅`, so S3's quantifier range is empty and the invariant holds vacuously. Sound.

*Inductive step.* Fix d and v ∈ dom(Σ'.M(d)), let a = Σ'.M(d)(v). The proof splits on whether the mapping at (d, v) is inherited unchanged. The two cases — Case 1: `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)`; Case 2: the logical complement — are mutually exclusive and exhaustive over dom(Σ'.M(d)). No gap.

*Case 1 (inherited).* `a = Σ.M(d)(v)`, so IH gives `a ∈ dom(Σ.C)`, then S1 gives `a ∈ dom(Σ'.C)`. Sound.

*Case 2 (new or redirected).* The antecedent of AX-2 requires `v ∈ dom(Σ'.M(d)) ∧ (v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v))`. The outer fix supplies `v ∈ dom(Σ'.M(d))`; Case 2 is exactly the disjunction. AX-2 discharges and yields `a ∈ dom(Σ'.C)` directly. Sound.

**Dependency declarations.** S1's single direct dependency is S0; correct. S3's declared dependencies — AX-1, AX-2, S1 — match the proof's invocations exactly. S0 is a transitive dependency through S1, not listed directly; consistent with the spec's convention of listing immediate dependencies only.

**AX-2 scope check.** AX-2 quantifies over all transitions, all d, all v satisfying its antecedent. No restriction to reachable states is needed: the axiom is a constraint on the transition relation itself, and S3's induction applies it per-transition. No circularity or scope mismatch.

**Frame conditions.** S3's frame correctly notes that dom(C) may exceed the union of the ranges of M(d) — orphaned content is never reclaimed, which is the correct reading of S1's unconditioned monotonicity. The remark is accurate and properly labeled as a remark rather than a proof step.

**Induction well-foundedness.** "Reachable" is defined as reachable from Σ₀; induction on path length from Σ₀ is the standard invariant-proof instrument. The implicit induction variable (path length) is conventional and unambiguous in context.

VERDICT: CONVERGED