# Review of ASN-0042

## REVISE

### Issue 1: Worked Example mislabels a₂ as a document address

**ASN-0042, Worked Example, "Allocation" section**: "π_A allocates document address a₂ = [1, 0, 2, 0, 5, 0, 1]."

**Problem**: a₂ has three zeros (positions 2, 4, 6), so zeros(a₂) = 3, which by T4c (LevelDetermination) is an element-level address, not a document address. The level label contradicts the address structure.

**Required**: Either rename a₂ to a document-level address (e.g., [1, 0, 2, 0, 5]) or relabel as "element address." The downstream O5/O6 verifications happen to work either way, but the level mislabel introduces confusion.

### Issue 2: Worked Example contradicts itself about a₁'s allocator

**ASN-0042, Worked Example**: State Σ₁ section asserts "a₁ = [1, 0, 2, 0, 3, 0, 1] ... was allocated by π_N before delegation, so a₁ ∈ Σ₀.B." But the Fork (O10) section's *Trajectory* paragraph asserts "Σ_pre is reached after π_A's earlier allocations a₁ = [1, 0, 2, 0, 3, 0, 1] and a₂ = [1, 0, 2, 0, 5, 0, 1] have established hwm = 5."

**Problem**: a₁ has the same address in both sections but conflicting allocator attribution (π_N pre-delegation in one, "π_A's earlier allocation" in the other). The worked example is the only concrete verification of the proofs against a specific scenario; internal inconsistency undermines its load-bearing role.

**Required**: Decide whether the Fork section continues State Σ₁'s scenario (in which case rephrase "π_A's earlier allocations" — perhaps "the prior allocations a₁ and a₂ established by π_N's pre-delegation baptisms and π_A's subsequent baptisms have established hwm = 5") or constitutes a different trajectory (in which case use distinct address labels to avoid collision).

### Issue 3: AccountPrefix proof leaves an implicit zeros-count step in the O6 forward direction

**ASN-0042, O6 forward direction, case zeros(pfx(π)) = 1**: "The prefix relation pfx(π) ≼ a forces a_{α+1} = 0. By T4's positive-component constraint applied to a, all components before this zero are positive ... so by T4a (SyntacticEquivalence) this zero cannot be adjacent to another zero or appear at position 1 — it must be a's node-user field separator."

**Problem**: The argument implicitly relies on a having zeros(a) ≥ 1 (otherwise position α+1 of a couldn't be zero, contradicting pfx(π) ≼ a with α+1 ≤ #pfx(π) ≤ #a). The "must be a's node-user separator" leap also presumes T4b's uniqueness of field decomposition — both implicit.

**Required**: Add a one-line lemma: "Since pfx(π) ≼ a and pfx(π)_{α+1} = 0, transitivity of the prefix relation forces a_{α+1} = 0, hence zeros(a) ≥ 1. T4b (UniqueParse) then identifies position α+1 as a's node-user separator since it is the first zero of a (positions 1..α being positive by the prefix relation transferring pfx(π)'s positive components)."

### Issue 4: O8 quantifier semantics underspecified

**ASN-0042, O8 statement**: "(A π, π', a, Σ, Σ' : Σ reachable from Σ₀ ∧ delegated_Σ(π, π') ∧ a ∈ dom(π') ∩ Σ'.B ∧ Σ →⁺ Σ' : ω_{Σ'}(a) ≠ π)"

**Problem**: delegated_Σ(π, π') is defined to denote "transition Σ → Σ'" with its own implicit successor state, but in O8 the symbol Σ' is rebound by the outer quantifier to range over all states reachable from Σ. The proof body resolves this by introducing Σ_d as the delegation state explicitly and considering Σ_d →⁺ Σ', tacitly assuming the path Σ →⁺ Σ' passes through Σ_d. The formal statement does not enforce this; if a path Σ →⁺ Σ' avoids the delegation, π' ∉ Π_{Σ'} and dom(π') becomes ill-defined (or vacuously satisfies the precondition, depending on convention).

**Required**: Either restate as "delegated_Σ(π, π') witnesses a transition Σ → Σ_d, and for every Σ' with Σ_d →* Σ'..." or add a note that delegated_Σ asserts the delegation actually occurred along the trajectory leading to Σ', not merely that it was possible at Σ.

### Issue 5: O10 Form B trailing-zero exclusion left implicit

**ASN-0042, O10 proof, Form B classification under zeros(pfx(π)) = 0**: "A Form B sub-delegate of length exactly #pfx(π) + 2 (so pfx(π_i) = pfx(π).0.U^{(i)}_1) covers a' iff U^{(i)}_1 = hwm_0 + 1."

**Problem**: The proof skips the case #pfx(π_i) = #pfx(π) + 1, which would be pfx(π_i) = pfx(π).0 (trailing zero). This is invalid by T4a but the exclusion is not stated. Similarly, the "Form B is empty when zeros(pfx(π)) = 1" argument doesn't explicitly note that pfx(π).0 of length #pfx(π)+1 is T4a-invalid before invoking the O1a zero-count contradiction.

**Required**: Add one sentence: "Length #pfx(π) + 1 is excluded by T4a's no-trailing-zero clause, since pfx(π_i) would end in the zero at position #pfx(π) + 1."

### Issue 6: Sub-account namespace example skips intermediate baptisms

**ASN-0042, Worked Example, Sub-account namespace section**: "Now suppose π_A creates sub-account position [1, 0, 2, 3] as an organizational namespace — not delegated to a new principal."

**Problem**: By ASN-0040's next() semantics, π_A's depth-1 baptism from pfx(π_A) = [1, 0, 2] produces [1, 0, 2, 1] first, then [1, 0, 2, 2], then [1, 0, 2, 3]. The example hand-waves this. The worked example is intended to verify the framework concretely; skipping the contiguous-prefix dependency obscures whether the trajectory is reachable.

**Required**: One sentence noting that this position is the third baptism in S(pfx(π_A), 1), preceded by [1, 0, 2, 1] and [1, 0, 2, 2], with B1 (contiguous prefix) thereby satisfied.

## OUT_OF_SCOPE

The Open Questions section already enumerates the principal out-of-scope items (ownership transfer mechanism, domain density, cross-node federation, delegation event recording). No additions needed.

VERDICT: REVISE
