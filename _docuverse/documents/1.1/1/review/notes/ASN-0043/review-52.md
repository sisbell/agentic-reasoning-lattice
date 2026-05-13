# Review of ASN-0043

## REVISE

### Issue 1: L9 proof Case A — "element-level allocator not yet initialized" misleading
**ASN-0043, L9 proof, L1c verification, Case A**: "Case A — d' has no prior link allocations under Σ ({b ∈ dom(Σ.L) : home(b) = d'} = ∅). The element-level allocator for d' has not yet been initialized; the full child-spawning chain from d' to the first link address a = d'.0.s_L.1 ... is required: (i) inc(d', 2) → d'.0.1 — establishes d's element-level allocator at element field depth 1, subspace 1..."

**Problem**: The discriminator "no prior link allocations under d'" does not imply "the element-level allocator under d' is uninitialized". In case (i) of d' selection (d' chosen from existing dom(Σ.M)), d' may have content allocations that already initialized the depth-1 allocator via inc(d', 2). Under the natural reading of step (i) as a new T10a event introduced by the transition Σ → Σ', this would violate T10a's at-most-once-per-(t, k') rule. Under the alternate structural reading — where step (i) describes the chain's producibility regardless of when each event happened — the chain is sound, but the verb "establishes" hides which interpretation is intended.

**Required**: Either (a) refine the case split into Case A1 (no allocations of any kind under d' — depth-1 uninitialized) and Case A2 (content allocations under d' but no link allocations — depth-1 initialized, link allocator yet to be spawned), giving reasoning for each; or (b) make explicit that steps (i)–(iii) describe the chain's structural producibility (T10a-conforming whether or not each individual step is a new event in the transition) and identify which steps must be new events in the worst case (the link-allocator child-spawn at d'.0.s_L, and the first sibling allocation in that allocator).

### Issue 2: L11b proof — "a as the allocator's current frontier" incorrect
**ASN-0043, L11b proof, Construction of fresh a'**: "By L1c on Σ, the existing link a was produced by a T10a-conforming allocator chain emanating from home(a)'s link subspace, terminating in a as the allocator's current frontier within that subspace."

**Problem**: "Current frontier" reads as the frontier in state Σ. This is false in general — a was the allocator's frontier at the time of a's allocation event, but subsequent link allocations under home(a) (other links with the same home document) may have advanced the frontier past a. The proof's subsequent "least i ≥ 1 with a⁽ⁱ⁾ ∉ dom(Σ.L)" search correctly compensates by searching past a, so the conclusion is sound — but the initial framing misrepresents what L1c on Σ delivers.

**Required**: Replace the claim with an accurate statement — the chain producing a terminates at a's allocation event (a was the frontier at that time), and the sibling stream a⁽⁰⁾, a⁽¹⁾, a⁽²⁾, ... may include addresses already allocated under home(a) by subsequent events. The "least i with a⁽ⁱ⁾ ∉ dom(Σ.L)" search then finds the first sibling past the actual current frontier.

### Issue 3: L9 proof — L6 "vacuously" justification incorrect
**ASN-0043, L9 proof, Remaining properties**: "L6 vacuously (F = G = ∅ makes the antecedent false)"

**Problem**: The witness link is (∅, ∅, Θ) with Θ = {(g, δ(1, #g))} non-empty. L6's antecedent is `(E i : Σ.L(a).e_{π(i)} ≠ Σ.L(a).eᵢ)`. For the permutation π = (1 3): e_{π(1)} = e_3 = Θ ≠ ∅ = e_1, so the antecedent is satisfied with i = 1 as witness. The proof's claim "F = G = ∅ makes the antecedent false" is therefore incorrect — whether the antecedent is true depends on which slots π permutes, and permutations involving slot 3 (the only non-empty slot in the witness) produce a true antecedent. L6 itself still holds (permute((∅, ∅, Θ), (1 3)) = (Θ, ∅, ∅) ≠ (∅, ∅, Θ) by tuple inequality, so the conclusion is satisfied), but the justification needs replacement.

**Required**: Verify L6 non-vacuously — note that L6 follows tautologically from tuple equality (component-wise equality), so for any permutation π that moves at least one slot to a position holding a different value, the antecedent is true and the conclusion holds by tuple inequality. Cite the witness π = (1 3) explicitly to show the non-vacuous case.

## OUT_OF_SCOPE

None. The Scope section explicitly excludes operations, V-stream mechanics, indexing implementation, version semantics, and other adjacent topics. Within scope, I've raised specific REVISE items rather than out-of-scope gaps.

VERDICT: REVISE
