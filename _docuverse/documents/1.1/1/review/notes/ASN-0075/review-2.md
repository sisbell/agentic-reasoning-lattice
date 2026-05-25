# Review of ASN-0075

## REVISE

### Issue 1: D-DISCR construction omits K.ρ steps required for J1★

**ASN-0075, §"Why the Provenance Relation Is Load-Bearing"**: History 1 lists steps `... → K.α(a, d) → K.μ⁺(d, v ↦ a) → K.μ⁺(d', v' ↦ a) → K.μ⁻(d) [retain n'_{s_C} = 0]`.

**Problem**: K.μ⁺'s frame in ASN-0047 explicitly states `R' = R` — K.μ⁺ does not modify R. J1★ is a coupling constraint that holds end-to-end on every valid composite, including each elementary step (a degenerate single-step composite). At the elementary step K.μ⁺(d, v ↦ a) where (a, d) ∉ R_before, J1★ requires (a, d) ∈ R_after, but the frame guarantees (a, d) ∉ R_after. The composite as written is therefore invalid — yet the proof depends on (a, d) ∈ R_1. The author writes "by J1★ in the extended state, the composite records `(a, d) ∈ R_1`," but J1★ is a constraint, not an action.

**Required**: Make K.ρ(a, d) and K.ρ(a, d') explicit in History 1 (and K.ρ(a, d') in History 2). K.ρ's frame leaves (C, E, M) unchanged, so the (C, M) agreement between Σ_1 and Σ_2 is preserved, and the lemma's conclusion stands.

### Issue 2: Worked example K.μ~(d_B) is the identity permutation

**ASN-0075, §"A Worked Example"**: The setup lists `→* K.μ~(d_B) [permute so b at [1,2], c at [1,3]]`.

**Problem**: At that point M(d_B) = {[1,1]↦a, [1,2]↦b, [1,3]↦c} — b is already at [1,2] and c is already at [1,3]. The described permutation is π = id. K.μ~'s admissibility clause (ii) requires π ≠ id, so this step is not a valid K.μ~.

**Required**: Remove the K.μ~(d_B) step. K.μ⁻(d_B) [retain n'_{s_C} = 2] alone truncates c at [1,3] without needing prior rearrangement. The resulting M_1(d_B) = {[1,1]↦a, [1,2]↦b} matches the rest of the example.

### Issue 3: Worked example omits K.ρ steps

**ASN-0075, §"A Worked Example"**: After each K.α / K.μ⁺ pair the author claims "J1★ records `R ⊇ {(a, d_A), (b, d_A), (c, d_A), (a, d_B), (b, d_B), (c, d_B)}`."

**Problem**: Same issue as Issue 1 — K.μ⁺'s frame says R' = R, so K.μ⁺ alone cannot satisfy J1★ when the new mapping introduces (x, d) not already in R. The composite must include explicit K.ρ steps (compare ASN-0047's J4 fork composite, which makes K.ρ explicit as step (iii)).

**Required**: Interleave K.ρ(a, d_A), K.ρ(b, d_A), K.ρ(c, d_A) after the three K.α / K.μ⁺ pairs in d_A, and K.ρ(a, d_B), K.ρ(b, d_B), K.ρ(c, d_B) after the K.μ⁺(d_B, ...) step.

### Issue 4: D-ACT uses reflexive-transitive closure where equivalence closure is needed

**ASN-0075, §"Actionability"**: "Define adjacency on the deletion set: two addresses `a, a'` are *I-adjacent* iff `a' = shift(a, 1)` and `origin(a) = origin(a')`. The reflexive-transitive closure of I-adjacency partitions the deletion set into equivalence classes."

**Problem**: I-adjacency as defined is asymmetric — `a' = shift(a, 1)` is a directed relation (the relation does not assert that `a = shift(a', 1)`). The reflexive-transitive closure of an asymmetric relation is a quasi-order, not an equivalence relation, and does not partition the set into equivalence classes. For a chain a₁ → a₂ → a₃, the closure gives (a₁, a₃) but not (a₃, a₁), so the "class of a₁" and "class of a₃" would differ.

**Required**: Either symmetrize the relation in the definition ("a and a' are I-adjacent iff a' = shift(a, 1) OR a = shift(a', 1), with shared origin") or take the *reflexive-symmetric-transitive closure* (equivalence closure). The intended partition then follows.

VERDICT: REVISE
