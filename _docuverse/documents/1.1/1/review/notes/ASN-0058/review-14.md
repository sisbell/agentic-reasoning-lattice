# Review of ASN-0058

## REVISE

### Issue 1: Incorrect citation of OrdShiftHom

**ASN-0058, M12 proof (uniqueness paragraph)**: "OrdShiftHom (ASN-0034) ordinal shift preserves subspace, so v shares its subspace with v₁ and with v₂"

**Problem**: OrdShiftHom is defined in ASN-0036, not ASN-0034. ASN-0034 has OrdinalShift, TS1–TS5 but no claim named OrdShiftHom.

**Required**: Change citation to "OrdShiftHom (ASN-0036)" (the (b) clause: `subspace(shift(v, n)) = subspace(v)`).

### Issue 2: Gap and redundancy in M12 intermediate-tumbler argument

**ASN-0058, M12 (⟹) Case 1 — "condition 3 fails" branch**: "Any V-position t with v + (n − 1) < t < v + n must satisfy t₁ = v₁ (by T1 at position 1, ...); hence t ∈ V_{v₁}(d) and, by S8-depth ... t has depth m. But the only depth-m tumblers with first m − 1 components matching v's are [v₁, ..., v_{m−1}, j] for natural j, and no integer falls strictly between v_m + n − 1 and v_m + n."

**Problem**: The argument establishes only t₁ = v₁ (via T1 at position 1). It then asserts t shares components 2 through m−1 with v without derivation — a non-trivial step requiring T1 divergence analysis (e.g., showing the divergence of t against v+n and v+(n−1) must occur at position m, forcing agreement at positions 1..m−1). Moreover the entire intermediate-tumbler analysis is redundant: from the established v' ≥ v + n (contradiction with v' < v + n via B2) plus v + n ∈ V(β') = {v' + j : 0 ≤ j < n'} (which immediately yields v' ≤ v + n), one concludes v' = v + n directly. The proof currently mixes a partial structural argument with an unnecessary detour.

**Required**: Either (a) replace the intermediate-tumbler paragraph with the direct argument: "v + n ∈ V(β') so v + n = v' + j for some 0 ≤ j < n'; combined with v' ≥ v + n and TS4/TS5, this forces j = 0 and v' = v + n", or (b) complete the T1 divergence analysis showing tᵢ = vᵢ for 2 ≤ i ≤ m−1.

### Issue 3: Hand-wave in M7 necessity argument for overlap case

**ASN-0058, M7 (MergeCondition)**: "(The case v₂ < v₁ + n₁ (overlap) cannot occur when β₁, β₂ ∈ B: it would force v₂ ∈ V(β₁) ∩ V(β₂), violating B2 of the original decomposition.)"

**Problem**: "v₂ ∈ V(β₁)" is asserted, not derived. Under v₁ < v₂ < v₁ + n₁, one must show v₂ = v₁ + k for some 1 ≤ k ≤ n₁ − 1. This requires (i) v₁ and v₂ share subspace — provable by T1 at position 1 since (v₁)₁ ≤ (v₂)₁ ≤ (v₁ + n₁)₁ = (v₁)₁; (ii) v₂ has the same depth m as v₁ — by S8-depth on the shared subspace; (iii) v₂ agrees with v₁ on positions 2..m−1 — by T1 divergence analysis. The proof skips all three steps and writes the conclusion as if obvious. Particularly since β₁ and β₂ could a priori lie in different subspaces (the decomposition spans all subspaces by B1), the subspace-alignment step is genuinely load-bearing.

**Required**: Spell out the chain (i)–(iii) explicitly, or cite an established lemma that consolidates them.

VERDICT: REVISE
