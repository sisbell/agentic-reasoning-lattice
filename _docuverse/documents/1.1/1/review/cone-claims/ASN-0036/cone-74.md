Reading the full ASN before flagging anything.

**Dependency structure:** S0 (axiom) → S1; AX-1, AX-2 (axioms); AX-1 + AX-2 + S1 → S3. This is the logical order.

**AX-1, AX-2, S0.** All are stated as posits on the transition relation or the designated start state. No derivation required. Formal Contracts are self-consistent. AX-2's domain guard `v ∈ dom(Σ.M(d))` in the second disjunct is correctly motivated: it keeps `Σ.M(d)(v)` inside its domain under the strict partial-function reading. Classically the guard is redundant (∀ v: ¬A ∨ ¬B ≡ ¬A ∨ (A ∧ ¬B)); the explanation is accurate.

**S1.** Proof is one step: S0's consequent `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` gives `a ∈ dom(Σ'.C)` as the first conjunct; universalising over arbitrary `a ∈ dom(Σ.C)` yields the subset claim. Correct and complete. Formal Contract and Depends are consistent.

**S3.** Induction on transition sequences from Σ₀.

- *Base:* AX-1 empties dom(Σ₀.M(d)) for all d; S3's quantifier range is empty; holds vacuously. ✓
- *Inductive step:* Fix d, v ∈ dom(Σ'.M(d)), a = Σ'.M(d)(v). Case split on whether the mapping is inherited unchanged.
  - *Inherited:* v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v). J0 gives a ∈ dom(Σ.C); S1 lifts to dom(Σ'.C). ✓
  - *New or redirected:* ¬(v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)), i.e., v ∉ dom(Σ.M(d)) ∨ (v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) ≠ Σ.M(d)(v)). Together with v ∈ dom(Σ'.M(d)) from the IS quantifier, this is exactly AX-2's range; AX-2 yields a ∈ dom(Σ'.C) directly. ✓

The two cases are exhaustive and mutually exclusive — they partition on a tautology. AX-2's range matches Case 2 exactly (the logical equivalence ¬A ∨ ¬B ≡ ¬A ∨ (A ∧ ¬B) is sound). Both cases reach a ∈ dom(Σ'.C). Induction is complete. Formal Contract and Depends match the proof.

The closing remark — that S1 holds unconditioned on reachability from ran(M(d)), so orphaned content persists — correctly attributes this to S1 and does not assert it as a proof step.

**One observation on document layout.**

---

### S1 presented before S0 in document order, creating a forward citation

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S1 (StoreMonotonicity) proof — "By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction…"
**Issue**: S1 appears second in the document, but its proof invokes S0, which appears fourth. A reader encounters the citation "By S0" before S0 has been introduced. The logical dependency order is S0, AX-1, AX-2 (axioms) → S1 → S3; the presentation order is AX-2, S1, AX-1, S0, S3. The proof is sound — S0 exists and supplies exactly the needed implication — but the document forces a forward reference at the first proof step.
**What needs resolving**: Reorder the claims to present axioms before the lemmas that depend on them: S0, AX-1, AX-2 first, then S1, then S3. No change to proof content is required.

---

VERDICT: OBSERVE