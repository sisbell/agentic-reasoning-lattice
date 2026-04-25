# Regional Review — ASN-0034/ActionPoint (cycle 1)

*2026-04-24 03:30*

### NAT-discrete Equivalence note is meta-prose
**Class**: REVISE
**Foundation**: (internal — this is a foundation ASN)
**ASN**: NAT-discrete (NatDiscreteness), the block labeled *"Equivalence note (separate from the Consequence derivation)."* through *"— `<` jumps by one step on ℕ."*
**Issue**: The note is self-described as "record the observation only to justify the presentational choice of which form to posit" and ends with "We take the discreteness form as the axiom because it directly states the intended content." Nothing downstream uses the converse direction; it neither strengthens the Consequence (the note admits this explicitly) nor is cited by any other claim in the ASN. The Depends slot even carries a separate clause ("The separate equivalence note additionally cites…") solely to support this unused walk. This is defensive justification of a presentational choice — axiom-choice rationale rather than axiom content — which is the meta-prose pattern the reviewer is asked to flag.
**What needs resolving**: The ASN must either remove the Equivalence note and its dedicated Depends clause, or show that the converse direction is actually invoked by some downstream claim in this ASN.

### NAT-closure distinctness derivation is unused prose
**Class**: REVISE
**Foundation**: (internal)
**ASN**: NAT-closure (NatArithmeticClosureAndIdentity), prose paragraph "`0 < 1` entails `0 ≠ 1` against NAT-order's exactly-one trichotomy, which forbids `0 < 1 ∧ 0 = 1`. Beyond distinctness, `0 < 1` pins `1` strictly above `0`." and the matching Depends clause on NAT-order's exactly-one-trichotomy mutual-exclusion conjunct.
**Issue**: The prose derives `0 ≠ 1` from `0 < 1` but the ASN records no Consequence for it, and no subsequent claim (ActionPoint, TA-Pos, NAT-discrete, NAT-wellorder) cites `0 ≠ 1`. The Depends clause on NAT-order's exactly-one-trichotomy conjunct exists only to license this unused prose derivation. The second sentence ("Beyond distinctness, `0 < 1` pins `1` strictly above `0`") merely restates the axiom. Same pattern as above: prose-only derivation with no load-bearing role.
**What needs resolving**: Either lift `0 ≠ 1` to a Consequence that is genuinely cited elsewhere, or remove the derivation and the supporting Depends clause. If the sentence "Beyond distinctness, `0 < 1` pins `1` strictly above `0`" is retained, it needs to do work beyond restating the axiom.

### ActionPoint's S set-builder lacks an explicit carrier for i
**Class**: REVISE
**Foundation**: (internal — T0, TA-Pos, NAT-wellorder)
**ASN**: ActionPoint — both the prose ("`S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`") and the Formal Contract's *Definition* ("where S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}").
**Issue**: The set-builder binds `i` without declaring a carrier. NAT-wellorder's axiom is stated with an explicit precondition `S ⊆ ℕ`, so invoking it on this S requires showing `S ⊆ ℕ`. The derivation prose does argue this (citing T0's index-domain commitment), but the Definition slot itself should be readable without leaning on the derivation — and the ASN is already careful about typing in analogous positions (TA-Pos writes `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` and `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` with explicit `i ∈ ℕ`). The inconsistency is a gap a downstream consumer reading only the Formal Contract would hit.
**What needs resolving**: The set-builder in both prose and Definition should either carry an explicit carrier (e.g. `S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`) or the ASN should state and cite the convention making the carrier implicit consistently across TA-Pos and ActionPoint.

VERDICT: REVISE
