# Review of ASN-0036

## REVISE

### Issue 1: Positivity misattributed to T4 in the S7 proof
**ASN-0036, S7 proof, "Well-definedness"**: "T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component."
**Problem**: T4 has no "positive-component constraint." The foundation contract for T4 states explicitly: "Positivity of non-zero components is not a separate axiom clause: T0's carrier ℕ already makes `tᵢ ≠ 0 ⇔ tᵢ > 0`." The strict positivity of non-separator components is discharged from T0, not T4; the "each present field is non-empty" reading is T4a. The proof's earlier line "each as a finite sequence of strictly positive natural numbers" inherits the same misattribution. Given ASN-0034's emphasized per-step citation convention, this is a citation error in a load-bearing step of the only nontrivial well-definedness argument here.
**Required**: Attribute strict positivity to T0's carrier ℕ and the non-empty-field reading to T4a (SyntacticEquivalence); reserve T4 for the separator/zero-count structure.

### Issue 2: S8 conjunct (b) carries defer-to-proof bookkeeping, with an inaccurate description of the case split
**ASN-0036, S8 statement, conjunct (b)**: "The well-definedness of `shift(a, k)` as a tumbler and its membership in `dom(Σ.C)` are established in the proof, where the `k = 0` and `k ≥ 1` cases are handled separately."
**Problem**: Two defects. (1) This sentence advances no part of the claim — it is a forward pointer into the proof, exactly the defer-to-downstream accretion the `review-mode.anti-bloat` classifier targets. (2) It is also inaccurate: in the proof the `k = 0` / `k ≥ 1` split is performed on the *V-side* (`shift(v, i)` well-formedness via OrdShiftHom), while `shift(a, i) ∈ dom(Σ.C)` is established uniformly as `M(d)(vⁱ) ∈ ran(M(d)) ⊆ dom(C)` ("in either case"). The membership of `shift(a,k)` is not what gets the separate-case treatment.
**Required**: Delete the sentence. The substance ("`a ∈ dom(Σ.C)` by S3, each lockstep image likewise") is already stated; the proof carries the rest.

### Issue 3: S5 restates the vacuous-satisfaction argument three times
**ASN-0036, S5 proof and contract**: the "Shared facts" paragraph establishes that S0/S1 hold vacuously under an empty transition relation and S2/S3 hold on the state; the **Conclusion** repeats "S0 and S1 vacuously satisfied by the empty transition relation, S2 and S3 verified on the state"; the **Postconditions** slot repeats it a third time ("with S0, S1 vacuously satisfied by the empty transition relation and S2, S3 verified on the state").
**Problem**: The same justification appears in three places, including a formal-contract slot — essay restatement of an argument already discharged in the proof body. This is the cross-cycle accretion the anti-bloat classifier asks to surface at source.
**Required**: State the vacuous-satisfaction argument once (in "Shared facts"); reduce Conclusion and Postconditions to the bare claim (initial state of a model of S0–S3 with multiplicity > N).

### Issue 4: S8a stated twice in equivalent forms, and again in the Properties table
**ASN-0036, "Definition (S8a — V-position well-formedness)" and Properties table row "Σ.M(d) domain restriction"**: the set form `zeros(t) = 0 ∧ #t ≥ 2` and the per-component form ("zero-free tumbler of depth at least 2 with all components positive") are given as equivalent restatements in the definition, then the table reproduces both forms again.
**Problem**: Two statements saying the same thing in different words, duplicated across definition and table. The per-component form is used downstream, but it need only be stated once; the table reproduction is pure duplication.
**Required**: Keep the per-component equivalence at the definition site; in the table, point to S8a rather than re-deriving both forms.

## OUT_OF_SCOPE

None. Link-subspace (S=2) contiguity, operation frame conditions, and the depth-`m` allocation convention are already correctly deferred in the Scope section and Open Questions.

VERDICT: REVISE
