# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 is labeled "weakest precondition" but `K ≁ R` is only sufficient, not necessary

**ASN-0086, Weakest-Precondition Analysis, Case 2 (Result)**: "the weakest precondition is `wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ K ≁ R`"

**Problem**: A weakest precondition must be *exactly* the set of pre-states from which the operation establishes the postcondition — both sufficient and necessary. The note proves sufficiency (the Derivation) and "load-bearingness" (dropping a conjunct admits *a* counterexample), but never proves necessity, and necessity is false.

Counterexample within the stated domain (substrate-conforming Σ satisfying the unit-depth discipline): take the call with `K ~ R` and to-set `G = ∅`. The fresh tuple `(a, F, ∅)` enters `L_R^{Σ'}` (since `K ~ R`), but its to-coverage is `coverage(∅) = ∅`, so it does not self-nullify `a`. Pre-existing `L_R^Σ` tuples do not cover the fresh `a` (antichain + unit-depth discipline — exactly the Derivation's argument). Hence `a ∉ nullified(Σ')` and `(a, F, ∅) ∈ A_K^{Σ'}` — the postcondition holds. Yet `K ≁ R` is false, so the stated formula evaluates to false for every Σ. The formula therefore strictly under-approximates the wp: it is a *sufficient* precondition, not the weakest.

The self-nullification the note cites only arises when the emitted **to-set covers `a`**, i.e. `a_emit(Σ, d) ∈ coverage(G)` — not from `K ~ R` per se. "Load-bearing for the conjunction's sufficiency" (which the note proves) is not "necessary for the postcondition" (which weakestness requires).

There is also an internal inconsistency: if the relational layer's Nullify-as-sole-`R`-producer rule forbids `K ~ R` calls outright, then `K ≁ R` is trivially true on every admissible call and cannot be "load-bearing"; if `K ~ R` calls are admitted, the G=∅ counterexample defeats weakestness.

**Required**: Either (a) relabel Case 2 as a *sufficient* precondition (as Case 1 honestly does), or (b) state the actual weakest precondition over the restricted domain:
`d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`
and prove both directions. The disjunct is what the postcondition actually demands: when `K ~ R`, the fresh tuple self-nullifies iff its own to-set covers `a`.

### Issue 2: The at-most-one-key-per-home / frontier-landing discipline is restated three times in different words

**ASN-0086, Definition — substrate-conforming state; R0a-Cor1 proof; R7a discharge (4)(i)/(iii)**: the "at-most-one-key-per-home discipline" and its "frontier-landing consequence" are stated in the Definition ("if a step adds a fresh key at home d whose homed-set occupied chain indices 0..J before the step, that key occupies exactly chain index J+1"), then re-derived inline in R0a-Cor1's induction step ("by the frontier-landing consequence ... that key occupies chain index J+1"), then re-narrated again in R7a discharge (4)(iii) ("the deposit lands at chain index J_{d_k}^Σ + 1 ... one past the pre-existing prefix").

**Problem**: Per the anti-bloat patterns this note carries, this is "two paragraphs say the same thing in different words" across three sections. The Definition's "the index-contiguity fact used downstream" is also a use-site inventory phrasing — the definition advertises its consumers instead of advancing its own meaning.

**Required**: State the discipline and its frontier-landing consequence once, authoritatively, in the Definition; have R0a-Cor1 and R7a cite it by name without re-narrating the J+1 mechanics. Drop "used downstream."

### Issue 3: Definition — state-local-conforming state carries an inline worked counterexample in a definition slot

**ASN-0086, Definition — state-local-conforming state**: "a higher layer may, for instance, emit `a'' = inc(a, 1)` at the same home as an existing link address `a` (the `k = 1` step appends `[1]`, preserving `zeros = 3` ...), yielding a nested pair `a ≼ a''` ..."

**Problem**: A multi-clause counterexample construction sits inside a definition. Concrete examples are not noise, but their placement here interrupts the four-way containment definition with a witness that is re-used later (Issue-1's counterexample, wp Case 2's second failure mode). The witness should live in a labeled remark the later sites can reference, not inside the definition body.

**Required**: Move the `a'' = inc(a, 1)` witness to a named remark; have the definition state only the containment and point to the remark for the separating witness.

## OUT_OF_SCOPE

### Topic 1: Invariants coupling `L_K`/`A_K` to arrangement visibility (`Σ.M`)
**Why out of scope**: The note explicitly defers (Open Question 1) the question of what must hold between typed relations and arrangements when a predicate depends on whether endset content is currently arranged in some document. ASN-0093's M2 keeps arrangements empty here, so the coupling cannot even be exercised at this layer — it is genuinely future territory, not a gap in this note.

### Topic 2: Atomicity/consistency model for concurrent Emit vs Observe
**Why out of scope**: Concurrency semantics (Open Questions 5, 4) require a transition-interleaving model the substrate does not yet expose; the present `→` is a sequential, totally-ordered relation (SequentialTransitionAxiom, ASN-0093). A future ASN, not a revision here.

VERDICT: REVISE
