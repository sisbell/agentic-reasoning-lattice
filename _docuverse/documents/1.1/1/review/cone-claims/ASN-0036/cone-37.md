## Dependency and Proof Audit

**Precondition chain for S3.** S3 depends on AX-1, AX-2, and S1. S1 depends on S0. S0 is an axiom. AX-1 and AX-2 are axioms. Every precondition cited in S3's formal contract traces back to an axiom or a proven claim; the chain is unbroken.

**S1's proof.** One step: S0's consequent `a ∈ dom(Σ'.C)` is the first conjunct of the implication. Universal generalization closes the subset. Sound.

**S3's inductive step case split.** The split at `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)` is exhaustive: Case 2 is the Boolean negation of Case 1, so every `v ∈ dom(Σ'.M(d))` falls into exactly one. In Case 1 the IH precondition `v ∈ dom(Σ.M(d))` is met, J0 discharges, and S1 carries the address forward. In Case 2 the joint condition `v ∈ dom(Σ'.M(d)) ∧ (v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v))` is exactly AX-2's hypothesis, and AX-2 discharges directly. Both cases are walked; no third case exists. Proof is sound.

**AX-2 applied atomically.** AX-2 requires `Σ'.M(d)(v) ∈ dom(Σ'.C)` — the post-state store — permitting content and arrangement to be committed in one transition. The prose acknowledges this explicitly. No hidden pre-state assumption imported into the axiom.

**Reachability and induction well-foundedness.** The induction is on the natural-number length of the path from Σ₀. ℕ is well-ordered; the induction is valid without a separate finitary-reachability axiom.

**Append-only characterisation.** S0 and S1 together give address-persistence and value-fixity. The prose claim "append-only log" is accurate.

---

### Claim S1 presented before its dependency S0

**Class**: OBSERVE
**Foundation**: N/A — internal ordering
**ASN**: S1 (StoreMonotonicity) — "By S0 (content immutability), a ∈ dom(Σ.C) implies the conjunction..."
**Issue**: The document ordering is AX-2 → S1 → AX-1 → S0 → S3. S1's only proof step invokes S0, which appears two sections later. A reader following the document top-to-bottom encounters a forward reference to S0 from inside S1's proof. Logical dependency order would be AX-1, AX-2, S0, S1, S3.
**What needs resolving**: N/A — S0 is an axiom and the proof is sound regardless of presentation order; reordering is a presentational improvement only.

---

VERDICT: OBSERVE