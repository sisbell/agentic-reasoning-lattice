The foundation set covers tumblers through displacement and subtraction. ASN-0053 builds five span-level claims on top. I will trace each proof against the foundation contracts.

**S0 (Convexity).** The proof distributes `start(σ) ≤ p ≤ q` and `q ≤ r < reach(σ)` into four cases and two cases respectively, reducing each to T1(c) or substitution of equals. Coverage is complete: the four cases for the lower-bound composition are `(<, <)`, `(<, =)`, `(=, <)`, `(=, =)`, all handled. The two cases for the upper-bound composition are `q < r` and `q = r`. T1 is the only foundation needed once span membership is unfolded by the local Definition clause. The carrier obligation `q ∈ T` is correctly identified as the consumer's to supply. No gap.

**WF (WellFormedSpanFromEndpoints).** The proof has three phases: eliminate T1 case (ii), discharge D1's fifth precondition, then read off T12 well-formedness from TumblerSub. The elimination of T1 case (ii) is complete: `#s + 1 ≤ #s` unfolds by NAT-order's `≤`-definition into `#s + 1 < #s` (contradicted by chaining NAT-addcompat's `#s < #s + 1` via NAT-order transitivity) and `#s + 1 = #s` (contradicted by substituting into the same successor inequality). The divergence bound `divergence(s, r) ≤ #s` follows from identifying T1's case-(i) witness `k` with `divergence(s, r)` via Divergence's uniqueness clause, giving `k ≤ #s`. D1 then applies cleanly. TumblerSub's postconditions — carrier, Pos, action-point identification, length `max(#r, #s) = #s` — discharge T12's four preconditions. Level-uniformity `#width(γ) = #start(γ)` falls out of the length postcondition. No gap.

**S6 (LevelConstraint).** The chain `#reach(σ) = #(s ⊕ ℓ) = #ℓ = #s` uses exactly TumblerAdd's result-length identity `#(a ⊕ w) = #w` at `(a, w) = (s, ℓ)`, with the well-formedness preconditions discharging TumblerAdd's own preconditions, and level-uniformity `#ℓ = #s` closing the chain. The claim that TumblerAdd is the unique source is correct: neither TumblerSub nor D1 yields this identity for a general width. No gap.

**S2 (EmptyDistinction).** A single-step proof: apply T12(b) to obtain `s ∈ span(s, ℓ)`, which equals `s ∈ ⟦s, ℓ⟧`. T12's preconditions are S2's own hypotheses. No gap.

**S11 (DifferenceBound).** This is the most intricate claim. I trace each sub-argument:

- *Reach carrier.* `reach(α), reach(β) ∈ T` via TumblerAdd's carrier postcondition at each span's well-formedness. Consumed in both the boundary derivation and the ρ-construction.

- *Boundary characterisation.* Start bound: `start(β) ∈ ⟦β⟧` follows from S2 (which re-exports T12(b)), giving `start(β) ∈ ⟦α⟧` and hence `start(α) ≤ start(β)`. Reach bound: contradiction argument places `reach(α)` in `⟦β⟧` (three membership conjuncts all discharged — carrier from TumblerAdd, lower bound from `start(β) < reach(α)`, upper bound from the contradiction hypothesis) and then in `⟦α⟧`, yielding `reach(α) < reach(α)`, refuted by T1 irreflexivity.

- *Three-way partition.* Exhaustive and disjoint by T1's totality: compare `t` with `start(β)`, then with `reach(β)`. Sub-range (M) equals `⟦β⟧` given `⟦β⟧ ⊆ ⟦α⟧` and the boundary bounds.

- *λ-construction.* WF applies at `(start(α), start(β))`: carrier immediate (span starts), order from case condition, length from `level_compat`. `reach(λ) = start(β)`. ✓

- *ρ-construction.* WF applies at `(reach(β), reach(α))`: carrier from TumblerAdd (established at outset), order from case condition, length `#reach(β) = #reach(α)` via S6 applied to β and α and then composed with `level_compat`. `reach(ρ) = reach(α)`. ✓

- *Tightness.* Pick `t ∈ ⟦β⟧` (non-empty by S2). In the two-span case, `start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧` and `reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧` (each checked: start(α) < start(β) = reach(λ) licenses start(α) ∈ ⟦λ⟧; reach(β) < reach(α) licenses reach(β) ∈ ⟦ρ⟧). The bracketing `start(α) ≤ t ≤ reach(β)` is discharged: upper half by weakening `t < reach(β)`; lower half by case-splitting `start(β) ≤ t` and composing with `start(α) < start(β)` via T1(c) or substitution of equals — precisely the technique S0 itself uses. S0 then forces `t ∈ ⟦γ⟧`. But `t ≥ start(β) = reach(λ)` puts `t ∉ ⟦λ⟧` and `t < reach(β) = start(ρ)` puts `t ∉ ⟦ρ⟧`. Contradiction. ✓

All five proofs are sound. Precondition chains are unbroken. Case analyses are exhaustive. No cross-claim inconsistency.

VERDICT: CONVERGED