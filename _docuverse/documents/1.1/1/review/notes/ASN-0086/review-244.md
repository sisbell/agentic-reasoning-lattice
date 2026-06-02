# Review of ASN-0086

I checked the proofs, edge cases, worked-example arithmetic, and the two wp derivations against the foundation contracts. The substantive content is sound: R0a's cross-home/same-home split is complete, R-Scope's self-emit branch correctly invokes R0a at Σ' (not Σ), the wp Case 2 escape branch (`a_emit ∉ coverage(G)`) is genuinely non-redundant, and the worked sketch's tumblers compute correctly (a₁=`1.0.1.0.1.0.2.1` through a₃=`…2.5`, zeros=3, E-fields `[2,k]`). No correctness or completeness defect surfaced. The findings below are anti-bloat only — this note carries the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Defensive value-independence prose in R0's "Value-shape consequence"
**ASN-0086, R0 → Value-shape consequence**: "Every L-invariant at the fresh emitter key is value-independent given `Endset`-typed inputs: the L/S/M/C catalog is discharged structurally by the single K.λ-step via RT-closure, not consulting the triple's content."
**Problem**: The load-bearing content of this paragraph is its *second* sentence (the standard triple discharges L3: arity 3, `F,G ∈ Endset`, `K ∈ T_admissible` non-empty). The first sentence asserts robustness ("value-independent… not consulting the triple's content") rather than advancing R0's existential — it justifies *why* the discharge is clean instead of stating what is discharged. This is the "explains why rather than what" pattern.
**Required**: Drop the first sentence; keep the L3-discharge sentence, which is what Emit_K's definition actually cites.

### Issue 2: Discharge induction re-derives content already fixed by Definition — Nullify
**ASN-0086, Definition — relational layer (discharge induction)**: "The target residency `a ∈ A_rel^{Σ'}` holds because P-tgt admits exactly the two branches P1 and self-emit (Definition — Nullify), which are therefore exhaustive…" and "Everything else is unconstrained: the substrate's document- and content-allocation steps `K.σ` and `K.α` and non-`R` `Emit_K` steps may be freely interleaved."
**Problem**: P-tgt's two-branch exhaustiveness is stated at its definition site (Definition — Nullify); re-deriving it inside the induction is duplication. The "Everything else is unconstrained…" clause restates the negative space the commitment already implies. Both are scaffolding around the induction, not steps of it.
**Required**: Within the induction, cite P-tgt residency by reference (the target lands in `A_rel^{Σ'}` by P-tgt, Definition — Nullify) without re-arguing exhaustiveness; delete the "Everything else is unconstrained" restatement.

## OUT_OF_SCOPE

### Topic 1: Substrate-level retraction K-operation
**Why out of scope**: Open Question 8 (elevating the unit-depth retraction discipline to a substrate-level `L_R` to-span guarantee, e.g. a dedicated retraction K-operation) is correctly future territory. The layer-convention treatment here is internally consistent; whether the substrate should expose a value-shape constraint is a new-ASN decision, not a defect in this one.

VERDICT: REVISE
