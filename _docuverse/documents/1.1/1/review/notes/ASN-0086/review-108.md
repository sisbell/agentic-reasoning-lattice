# Review of ASN-0086

## REVISE

### Issue 1: ConformingHomedContiguity induction step only covers single-key extension, but R7a admits multi-key composite transitions

**ASN-0086, Sub-lemma ConformingHomedContiguity (proof, Step case)**: "A conforming transition `Σ_k ↝ Σ_{k+1}` extends `dom(·.L)` only by fresh keys, and clause (b) emits each fresh key at its home's sibling frontier — at first-emission `[d.0.s_L.1]` ... or at `inc(max H_d^{Σ_k}, 0)` ... In the first case `H_d` grows from `∅` to `{inc⁰(...)}`; in the second, from `{incʲ : 0 ≤ j ≤ J}` to `{incʲ : 0 ≤ j ≤ J+1}`."

**Problem**: The induction step is written for **exactly one** fresh key added per home per transition (`J → J+1`). But R7a's premise quantifies over composite `↝`-steps that may add **several** fresh link keys in one atomic step — the entire decomposition (the `Δ = {a_1,…,a_n}` enumeration, the "subsequent occurrences (both cases)" discharge of R7a (4)(iii)) exists precisely to reconstruct such multi-key composites. For R0a-Cor1 (and R7a's discharge (4)) to invoke the sub-lemma at a composite post-state `Σ'`, the sub-lemma's induction must cover a single conforming transition that emits two keys at the **same** home — taking `H_d` from `{0..J}` to `{0..J+2}`. Clause (b) ("emit every fresh link key at its home document's sibling frontier") does not, as written, rule out a step that deposits `t_{J+1}` and `t_{J+3}` (skipping `t_{J+2}`), since only one of the two simultaneously-emitted keys sits at the *current* frontier. The contiguity preservation for multi-key steps is asserted nowhere.

**Required**: Either (a) extend the sub-lemma's induction step to cover a transition emitting a finite set of fresh keys at a common home, showing clause (b) forces them to fill a contiguous frontier block `{J+1, …, J+r}`; or (b) sharpen the *Definition — substrate-conforming state* clause (b) to state that the set of fresh keys emitted at each home in any single step is the next contiguous chain segment, and cite that here.

### Issue 2: No worked example exercises R7a's multi-key-same-home replay path

**ASN-0086, Worked example (R7a, create-two-fresh-documents)**: the example allocates two documents `d_A, d_B` with **one** link each (distinct homes).

**Problem**: The non-trivial machinery in R7a discharge (4)(iii) — "Subsequent occurrences (both cases)," where the chain-order re-enumeration and per-home `ℓ_prev` tracking do real work — fires only when a single composite `↝`-step deposits **multiple** links at the **same** home. The provided example exercises only the distinct-home, single-link-per-home path (each home hits the first-emission branch). The hardest case the proof claims to handle has no concrete check, contrary to the "concrete example mandatory for key postconditions" standard.

**Required**: Add (or extend the worked example to include) a composite that emits two links at one home in a single `↝`-step, and trace the decomposition through the subsequent-emission branch (the `B2` / "subsequent occurrence" path) showing the chain element selected at each replay step equals the intended `a_k`.

### Issue 3: Nullify P1 labeled both "does not gate emission" and "executing precondition"

**ASN-0086, Definition — Nullify**: "It has two further *postcondition-establishing conditions* that do **not** gate emission: (P1) `a ∈ A_rel^Σ` ... Neither P1 nor P2 gates emission" — then immediately: "Under the executing preconditions P0 and P1, Nullify is the composition `Nullify(Σ, d_retr, a) ≡ Emit_R(...)`."

**Problem**: P1 is first classified as a non-gating postcondition-establishing condition and then promoted to an "executing precondition." This is a direct terminological contradiction in adjacent sentences. It matters because WP Case 1 leans on the precise gating role (`wp ≡ P0 ∧ P1 ∧ P2c`, with P1 there required only for the *postcondition* `a ∈ A_rel^{Σ'}`, not for emission).

**Required**: Pick one classification. If P1 does not gate emission (consistent with the WP Case 1 necessity argument), rephrase the composition clause to "Under P0 (the sole executing precondition); P1 additionally establishes the `a ∈ nullified(Σ')` postcondition."

### Issue 4: Repeated "derives from clause (b), not the →-scoped ChainMembershipForOrigin" justification (anti-bloat)

**ASN-0086**: the same scope-justification recurs across at least four sites:
- Sub-lemma proof: "we do not appeal to ASN-0093's ChainMembershipForOrigin, whose stated scope is `→`-reachability."
- R0a Case 2: "the ConformingHomedContiguity sub-lemma — which derives contiguity from conformance clause (b) directly, so it holds whether Σ is `→*`-reachable or an `↝`-reachable conforming-layer post-state."
- R0a-Cor1 proof: "(rather than from ASN-0093's ChainMembershipForOrigin, whose stated scope is `→`-reachability)."
- R0a-Cor2 / R7a (4)(i): further restatements of the same point.

**Problem**: Under the `review-mode.anti-bloat` classifier, "multiple paragraphs in different sections defer to the same downstream location" and "two paragraphs say the same thing in different words" are flagged patterns. The justification for *why* the sub-lemma is used in place of ChainMembershipForOrigin belongs once — at the sub-lemma — not re-litigated at every consumer.

**Required**: State the clause-(b)-vs-ChainMembershipForOrigin scope point once at the sub-lemma. At each consumer, cite the sub-lemma by name without re-explaining its reachability scope.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
The Open Questions correctly defer the consistency model for concurrent `Emit`/`Observe` and the atomicity of `A_K` transitions. This is genuinely new territory (a concurrency layer), not a defect in the present single-authority sequential model (SequentialTransitionAxiom, ASN-0093).

### Topic 2: Higher-arity typed relations (`L_K^{(n)}`, `n > 3`)
The note restricts to standard triples and explicitly defers `|Σ.L(a)| > 3` projections. Correctly future work.

VERDICT: REVISE
