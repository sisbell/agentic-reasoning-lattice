The five-claim system (AX-1, AX-2, S0, S1, S3) is internally consistent. I traced every proof step.

**S1:** Follows from the first conjunct of S0 alone; the proof is one line and correct.

**S3 base case:** AX-1 empties the quantifier domain; holds vacuously. Correct.

**S3 inductive step:** The case split `[v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)]` vs. its complement is exhaustive and mutually exclusive. Case A invokes the IH plus S1 (monotonicity carries `a ∈ dom(Σ.C)` to `a ∈ dom(Σ'.C)`). Case B matches AX-2's guard exactly: `v ∈ dom(Σ'.M(d))` is in scope from the outer fix, and the disjunction is Case B by construction; AX-2's body gives `a ∈ dom(Σ'.C)` directly. Both cases are discharged; the induction is sound.

**AX-2 well-formedness:** The domain guard `v ∈ dom(Σ.M(d))` in the second disjunct is classically equivalent to its absence (since `¬A ∧ Q ∨ A = Q ∨ A`), but the write-out is a legitimate partial-function discipline. No semantic gap.

**Declared axioms:** AX-1, AX-2, S0 are consistent — a model with Σ₀ = (C=∅, M(d)=∅) and one transition adding `{a₁↦c₁}` to C and `{v₁↦a₁}` to M(d₁) satisfies all three.

**Dependency graph:** S1 → S0; S3 → {AX-1, S1, AX-2}. No transitive gaps; S3's Formal Contract correctly lists only direct dependencies.

Two observations follow.

---

### AX-2 body — meta-prose about notational form, not axiom content

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: AX-2 (GroundedExtension), prose block beginning "We carry the domain guard `v ∈ dom(Σ.M(d))` explicitly into this second disjunct..."
**Issue**: The three-sentence block explains why the domain guard is written out (partial-function well-definedness, classical redundancy) rather than what the axiom asserts. This is prose about the author's notational choice, not a statement of the axiom's content or range. A reader parsing AX-2 must skip this block to reach the axiom's substantive claim. Fits the reviser-drift pattern: new prose around an axiom explaining why it is written the way it is, rather than what it says.
**What needs resolving**: Move the well-definedness justification to a Remarks or Formal Contract annotation. The axiom body should state the predicate, describe what the range selects, and state the body's requirement — nothing more. If the partial-function obligation needs recording, one sentence in the Formal Contract suffices.

---

### S3 — "earlier reading" sentence is revision history, not proof content

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), final sentence of the post-proof paragraph: "The earlier reading, that S1 alone forces `a ∈ dom(Σ'.C)` for any mapping established by a transition, conflated these: it assumed precisely the new-reference half that AX-2, not S1, supplies."
**Issue**: This sentence records why an abandoned proof direction failed. The surrounding paragraph ("It is worth saying why S1 alone does not close the argument...") does advance reasoning by articulating the two-part structure of the proof. But the final sentence crosses into revision history — it names a prior incorrect reading and explains why it was wrong, rather than saying anything about the current proof. This matches the reviser-drift pattern: a paragraph that looks like a prior finding's content relocated rather than removed.
**What needs resolving**: Remove the "The earlier reading..." sentence. The preceding material already explains the necessity of both S1 and AX-2; the sentence adds nothing to a reader who has not seen the revision history.

---

VERDICT: OBSERVE