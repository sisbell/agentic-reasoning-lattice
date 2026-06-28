Reading the ASN as a system — five claims forming a small dependency lattice: two axioms (AX-1, AX-2), one root posit (S0), one derived store property (S1), and one inductive invariant (S3).

**AX-1, AX-2, S0** are axioms and correctly labeled as protocol design posits. Their formal contracts are consistent with how S3 invokes them.

**S1** proof is a single correct step: `a ∈ dom(Σ.C)` → (by S0) → `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` → first conjunct → `a ∈ dom(Σ'.C)`. Dependency declared; proof complete.

**S3** proof. Base case: AX-1 makes the quantifier range empty at Σ₀, vacuously true. Inductive step: fix any `v ∈ dom(Σ'.M(d))`. Case split — inherited vs. new-or-redirected — is exhaustive (the two cases are complements) and mutually exclusive. Inherited case: J0 gives `Σ.M(d)(v) ∈ dom(Σ.C)`, then S1 lifts to `dom(Σ'.C)`. New-or-redirected case: the AX-2 range predicate matches exactly, yielding `Σ'.M(d)(v) ∈ dom(Σ'.C)` directly. Both cases discharge. The step closes the induction correctly.

Formal contracts accurately reflect the dependency structure throughout.

---

### "S0 and S1 together" characterization is self-referential
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S1 (StoreMonotonicity) body — "S0 and S1 together establish `C` as an *append-only log*"
**Issue**: S1 is derived from S0 (S0's first conjunct `a ∈ dom(Σ'.C)` is precisely domain monotonicity). Invoking "S0 and S1 together" in S1's own body frames S1 as an independent co-contributor alongside S0, but S1 contributes nothing that S0 does not already imply. The factual claim — that S0's value-immutability clause and S1's domain-monotonicity clause together characterize an append-only log — is correct; the framing misleads a reader into thinking the two claims are independent.
**What needs resolving**: Rephrase to reflect that S0 entails domain monotonicity (S1 is a named consequence) and that the append-only characterization follows from S0 alone, with S1 providing a separately usable handle on the domain-inclusion fragment.

---

### Meta-announcing sentence in S3's closing remark
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), closing paragraph — "We record this as a remark on the reach of store monotonicity, not as a step in the proof above."
**Issue**: This sentence tells the reader what the paragraph is (a remark, not a proof step) rather than contributing to the argument. The remark itself — that S3 imposes no obligation on stored content to be referenced, and that Nelson requires this for history — is substantive and correctly placed. The announcing sentence is pure meta-prose that a reader must skip past.
**What needs resolving**: Remove the self-describing sentence. The paragraph's status as supplementary context is clear from its position and content.

---

VERDICT: OBSERVE