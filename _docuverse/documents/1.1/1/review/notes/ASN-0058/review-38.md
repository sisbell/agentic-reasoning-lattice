# Review of ASN-0058

After thorough review, this is a substantial and largely rigorous ASN. The proofs are detailed, edge cases are handled (n=1, c=0, empty arrangement), foundation references are properly cited, and two worked examples verify the algebra concretely. The structural lemma M-int is well-developed, the canonical decomposition theorems (M11, M12) factor cleanly through M12a/M12b, and the cross-origin separation (M16a, M16b) is carefully derived.

I identify a few minor clarity issues.

## REVISE

### Issue 1: M-int's "Prefix agreement" leaves implicit a witness identification
**ASN-0058, M-int proof, Prefix agreement paragraph**: "Since `x ≤ y`, T1(i) gives `(y)_{j₀} > (x)_{j₀} = (x + n)_{j₀}` (prefix-copy again)."

**Problem**: T1(i) supplies a least divergence position `j'` of (x, y) as its witness; the proof concludes `(y)_{j₀} > (x)_{j₀}` without spelling out why `j' = j₀`. The analogous step in M-int's "Subspace agreement" *is* handled explicitly ("Any `j > 1` would similarly force `(y)_1 = (x)_1`..."), so the asymmetry stands out. The required chain — J ≠ ∅ forces x ≠ y, hence x < y; T1(ii) excluded by #x = #y = m; the least divergence `j'` satisfies `j' ≤ j₀` (since `j₀ ∈ J`) and `j' ≥ j₀` (since x, y agree on [1, j₀−1] by minimality of j₀) — is short but should be stated.

**Required**: Either explicitly identify `j' = j₀` (matching the explicitness of the Subspace agreement paragraph) or factor the identification into a small sub-lemma reused at both sites.

### Issue 2: C0a case (b) repeats the same implicit witness identification
**ASN-0058, C0a proof, case (b)**: "since `u ≤ t`, T1(i) (ASN-0034) gives `t_{j₀} > u_{j₀}`."

**Problem**: Same gap as Issue 1 — the proof claims "the divergence of t and u is at position j₀" and invokes T1(i) at j₀ without arguing that T1(i)'s least-divergence witness coincides with j₀. The reasoning chain is the same shape as Issue 1 and would benefit from the same explicit identification (or a shared sub-lemma).

**Required**: Spell out the witness identification, or cross-reference Issue 1's resolution.

### Issue 3: C2's enumeration argument elides an inclusion chain
**ASN-0058, C2 proof**: "Conversely, dom(f) contains no other elements: C0a fixes all components before m, and S8-depth ensures every position in V_{u₁}(d_s) has depth m, so the enumeration is exhaustive."

**Problem**: The argument that `|dom(f)| = ℓₘ` requires combining three facts: (a) well-formedness places `{depth-m positions in ⟦σ⟧} ⊆ dom(M(d_s))`; (b) C0a restricts ⟦σ⟧ to subspace u₁; (c) S8-depth makes the depth-m subset of V_{u₁}(d_s) exact. The proof states the conclusion but leaves the inclusion chain `{depth-m positions in ⟦σ⟧} ⊆ dom(f) ⊆ {depth-m positions in ⟦σ⟧}` implicit.

**Required**: Make both inclusions explicit so `|dom(f)| = ℓₘ` follows from set equality, not from a one-line gesture.

### Issue 4: M12 (⟸) condenses a multi-step derivation
**ASN-0058, M12 proof, (⟸) paragraph**: "The set of maximal runs is trivially maximally merged: any two V-adjacent maximal runs have a correspondence discontinuity at their boundary (by condition 3 of the left run), so they are not I-adjacent and cannot satisfy M7."

**Problem**: The chain — R₂'s condition 1 places `v₂ = v₁ + n₁ ∈ dom(f)` with `f(v₂) = a₂`; R₁'s condition 3 then forces `a₂ ≠ a₁ + n₁`; hence I-adjacency fails — is correct but compressed. Given that condition 3 of a maximal run is a disjunction (first disjunct ruled out, second disjunct then forced), the reader has to work through the disjunction unfolding implicitly.

**Required**: Expand to spell out which disjunct of condition 3 is being eliminated and why.

## OUT_OF_SCOPE

None — the five "Open Questions" listed at the end are appropriately flagged as future work, not gaps in this ASN.

VERDICT: REVISE
