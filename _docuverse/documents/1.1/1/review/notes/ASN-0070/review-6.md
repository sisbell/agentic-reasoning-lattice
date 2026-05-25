# Review of ASN-0070

## REVISE

### Issue 1: F-canonical Step 2's "Unique reconstruction" missing leftward closure

**ASN-0070, "Canonical Form" / Step 2 / "Inter-component gap"**: The argument shows `r_j := reach(σ_j) ∉ ⟦Σ̂⟧_V`, then concludes "The maximal run of consecutive tumblers in ⟦Σ̂⟧_V containing max(⟦σ_j⟧_V) cannot extend past max(⟦σ_j⟧_V)." This closes runs on the **right** but does not close them on the **left** (does not establish that the consecutive predecessor `p_j = [s_j.1, ..., s_j.{m-1}, s_j.m − 1]` of `s_j` is also excluded from `⟦Σ̂⟧_V`).

**Problem**: For "⟦Σ̂⟧_V decomposes into exactly |Σ̂| maximal runs of consecutive depth-m_S(d) subspace-S tumblers, one per component σ_j" to follow, three sub-claims must hold: (i) internal contiguity of each `⟦σ_j⟧_V` (established), (ii) right-closure via `r_j ∉ ⟦Σ̂⟧_V` (established), and (iii) left-closure via `p_j ∉ ⟦Σ̂⟧_V` (not established). Without (iii), the run containing `s_j` could in principle extend backward into a different component's chain, breaking the one-run-per-component bijection that the recovery of `(s_j, c_j)` from each maximal run depends on. The leftward bound does hold — for `k < j`, prefix-agreement and prefix-disagreement sub-cases both give `reach(σ_k) ≤ p_j`, so either `p_j = reach(σ_k) ∉ ⟦σ_k⟧_V` (half-open) or `p_j > reach(σ_k) ∉ ⟦σ_k⟧_V` (out of range); for `k ≥ j` it is immediate — but the case analysis is non-trivial and the ASN does not present it.

**Required**: Add an explicit "left-closure" sub-paragraph parallel to the "Inter-component gap" argument, deriving `p_j ∉ ⟦Σ̂⟧_V` from N2 (chained) and the consecutive-tumbler characterisation. Alternatively, note that runs cannot merge because N2-strict (`reach(σ_j) < start(σ_{j+1})`) directly excludes `s_{j+1} = r_j`, so `max(⟦σ_j⟧_V)` and `s_{j+1}` are not consecutive — but the predecessor case `j = 1` (no σ_0 to bound against) still needs its own argument (predecessor of `s_1` excluded because no σ_k with `k < 1` exists, hence the predecessor cannot be in any `⟦σ_k⟧_V`).

### Issue 2: CanonicalForm definition leaves V-position constraint on starts implicit

**ASN-0070, "Canonical Form" / Definition (CanonicalForm) clause (i)**: "Each component span in each Σ_V^S has start s with #s = m_S(d) and subspace(s) = S, and width of the form δ(c, m_S(d))..."

**Problem**: The definition does not require `s` to be a V-position (positive components per S8a). But the postcondition `⟦Σ_V^S⟧_V = R(d, e)|_S` forces this implicitly: by T12(b), `s ∈ ⟦σ⟧`, and the V-restricted filter (subspace + depth) admits `s` to `⟦σ⟧_V`; meanwhile `R(d, e)|_S ⊆ dom(M(d))` consists only of V-positions (S8a). So a canonical-form component with `s` having any zero component (including `s.m = 0`) would contribute a non-V-position to `⟦Σ_V^S⟧_V`, contradicting the postcondition equality. The constraint is real but never stated. Step 1's case analysis restricts widths but not starts, leaving the start positivity to be inferred by the reader.

**Required**: Add explicit positivity to the CanonicalForm definition: "start s with `#s = m_S(d)`, `subspace(s) = S`, and `(A i : 1 ≤ i ≤ m_S(d) : s_i ≥ 1)` (s is a V-position)." Alternatively, sharpen the V-restricted denotation definition to "{ t ∈ ⟦Σ_V^S⟧ : t is a V-position of d in subspace S at depth m_S(d) }" — adding positivity to the V-restriction — so that the postcondition equality directly enforces start positivity.

### Issue 3: Citation imprecision — TA-strict vs T12(b)

**ASN-0070, "Canonical Form" / Step 2 / "Bridge"**: "By TA-strict (StrictIncrease, ASN-0034), `s ∈ ⟦σ⟧` (the start is always in its own span's denotation)..."

Also **F-empty / "Derivation" / final paragraph**: "By TA-strict (StrictIncrease, ASN-0034), `s ∈ ⟦σ⟧`..."

**Problem**: TA-strict gives `s ⊕ ℓ > s` (the strict-increase advancement); the claim `s ∈ span(s, ℓ)` is T12(b), whose proof invokes TA-strict. The cited foundation lemma is one step removed from the claim being made. Two distinct sites in the ASN attribute `s ∈ ⟦σ⟧` directly to TA-strict.

**Required**: Replace "TA-strict (StrictIncrease, ASN-0034)" with "T12(b) (SpanWellDefinedness postcondition (b), ASN-0034)" at both sites.

### Issue 4: F-canonical Step 2 cites T1 case (a) for ℕ-irreflexivity

**ASN-0070, "Canonical Form" / Step 2 / "Reverse" direction, "Inductive step at p" case "q = p ∧ q' = p"**: "the case q = p ∧ q' = p gives t_p < t''_p < t'_p = t_p, contradicting T1 case (a) irreflexivity"

**Problem**: T1 case (a) is irreflexivity of `<` on tumblers (`¬(a < a)` for `a ∈ T`). The chain `t_p < t''_p < t_p` is on natural-number components, not tumblers. The applicable irreflexivity is from T0 (NAT-order). The conclusion is correct, but the citation is wrong-level.

**Required**: Replace "T1 case (a) irreflexivity" with "T0's NAT-order irreflexivity on ℕ" (or equivalent), and similarly for any other ℕ-level irreflexivity invocations in the same proof.

## OUT_OF_SCOPE

None — the ASN stays within FOLLOWLINK and does not stray into INSERT/DELETE/COPY/REARRANGE, link/version creation, or replication.

VERDICT: REVISE
