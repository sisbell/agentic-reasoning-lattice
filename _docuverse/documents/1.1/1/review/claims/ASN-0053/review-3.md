Tracing the five claims against the foundation contracts.

**S0** is immediate from T1 transitivity; the membership derivation `start(σ) ≤ q < reach(σ)` follows by composing `≤` chains under the total order. Sound.

**WF** is the most intricate claim. The divergence-exclusion step (case (ii) is barred by `#s = #r` since `#s + 1 ≤ #s` contradicts `#s < #s + 1`) is sound. Identifying the T1 witness `k` with `divergence(s, r)` via Divergence case (i) uniqueness is sound — the universal conjunct `∀ i < k : sᵢ = rᵢ` in T1's case (i) is exactly the minimality condition. TumblerSub preconditions are correctly verified; `#r = #s` eliminates the padding zone, letting padded projections coincide with native components. D1's five preconditions are all discharged. Level-uniformity `#(r ⊖ s) = max(#r, #s) = #s = #start(γ)` follows from TumblerSub's length postcondition. Sound.

**S6** is a definitional section; `#reach(σ) = #start(σ)` for level-uniform spans follows from TumblerAdd's result-length identity `#(a ⊕ w) = #w` composed with `#w = #s`. Used correctly by S11.

**S11** — the boundary derivation (start(α) ≤ start(β) and reach(β) ≤ reach(α) from containment) is sound. The three-sub-range partition is exhaustive and pairwise disjoint under T1. Construction of λ via WF with `#start(α) = #start(β)` (from level_compat) is correct. Construction of ρ via WF with `#reach(β) = #start(β) = #start(α) = #reach(α)` (from S6 applied to both spans and level_compat) is correct. The tightness argument applies S0 to γ with witnesses start(α) and reach(β) as bracket points; t ∈ ⟦β⟧ (non-empty by S2) supplies the intermediate element; the exclusions `t ∉ ⟦λ⟧` and `t ∉ ⟦ρ⟧` follow from the boundary identities `reach(λ) = start(β)` and `start(ρ) = reach(β)`. Sound.

**S2** has a material error.

---

### S2 precondition is type-incoherent, and TA-strict/T12 attributions are inverted

**Class**: REVISE
**Foundation**: TA-strict postcondition `a ⊕ w > a`; T12 postconditions (a) `s ⊕ ℓ ∈ T`, (b) `s ∈ span(s, ℓ)`, (c) convexity
**ASN**: S2 (EmptyDistinction) — Formal Contract Preconditions: *"k ≤ #s, where k is the end offset s ⊕ ℓ"*; Axiom: *"Axiom (TA-strict): Every well-formed span has strictly positive length: ℓ > 0"*; Depends TA-strict: *"supplies the axiom ℓ > 0"*; Depends T12: *"supplies strict monotonicity of advancement (s ⊕ ℓ > s given ℓ > 0 and k ≤ #s)"*
**Issue**: Three errors, all rooted in the same inversion.

First: the Definition sets `k = s ⊕ ℓ ∈ T`, then the Preconditions write `k ≤ #s`. This compares a tumbler to a natural number — a type-incoherent expression under the foundation contracts, which define `≤` on T (tumblers) and separately on ℕ. T12's actual precondition is `actionPoint(ℓ) ≤ #s`, a well-typed ℕ comparison.

Second: the proof body and Axiom field say "by TA-strict the length is strictly positive, ℓ > 0." TA-strict's postcondition is `a ⊕ w > a`; it takes `Pos(w)` as an input precondition. TA-strict does not supply `Pos(ℓ)` — it requires it. The premise `Pos(ℓ)` is a well-formedness precondition (from T12's precondition list), not a consequence of TA-strict.

Third: the Depends entry attributes `s ⊕ ℓ > s` (strict monotonicity) to T12, but this is TA-strict's direct postcondition. T12's exported postconditions are (a) `s ⊕ ℓ ∈ T`, (b) `s ∈ span(s, ℓ)`, (c) convexity — none of which are `s ⊕ ℓ > s` as a named postcondition. A verifier checking the Depends against the foundation contracts would find TA-strict's postcondition missing from T12's contract and `Pos(ℓ)` absent from TA-strict's postconditions.

**What needs resolving**: The precondition must name `actionPoint(ℓ) ≤ #s` (not `k ≤ #s` with `k = s ⊕ ℓ`). The Axiom and Depends fields must correctly identify that `Pos(ℓ)` comes from the definition of well-formedness (T12's precondition) and that `s ⊕ ℓ > s` is TA-strict's postcondition, not T12's.

---

VERDICT: REVISE