# Review of ASN-0098

## REVISE

### Issue 1: LP12a boundary case ("content-subspace empty") hand-waves the coverage-subspace argument
**ASN-0098, LP12a, "Boundary case — content-subspace empty, link-subspace retained"**: "every span (s, ℓ) ∈ Σ.L(a).eᵢ for every slot i satisfies subspace_I(s) = s_C **and similarly along the span**, ensured by canonical construction in content-subspace coverage"
**Problem**: The phrase "and similarly along the span" is a one-line gesture replacing what is actually a structural argument: that for canonical content-subspace constructions, `coverage(eᵢ) ∩ dom(L) = ∅`. The subsequent inference "project(a, i, d, Σ) ⊆ V_{s_C}(d)" rests on this premise but it is never derived. The premise actually requires LP-Fin's structural analysis — that F-candidates inside a canonical span's coverage all share the span's subspace identifier at position #d_0 + 2 — which is established in fragments across LP-Fin's Case A but not stated as the corollary the boundary case needs.
**Required**: State and prove a corollary of LP-Fin: for canonical span (s, ℓ) with `s = [d_0, 0, X, k_s]`, every `t ∈ F ∩ [s, s ⊕ ℓ)` has `t = [d_0, 0, X, k]` for some `k ∈ [k_s, k_s + n)`, hence `subspace_I(t) = X`. The LP12a boundary case can then invoke this corollary to conclude `coverage(eᵢ) ∩ dom(L) = ∅`, completing the chain to `project ⊆ V_{s_C}(d)`.

### Issue 2: LP-Fin's finiteness conclusion is asserted rather than derived case-by-case
**ASN-0098, LP-Fin proof**: "For each admissible #d, the remaining components s'' ∈ {s_C, s_L} (a 2-element set) and k ≥ 1 (bounded above by the comparison constraints a ≥ s and a < s ⊕ ℓ, hence a finite range) yield finitely many candidates per #d."
**Problem**: The proof establishes #d ≤ #d_0 with care and shows d ≼ d_0, but then collapses the remaining argument into a single phrase. The actual situation is sharper than "finite": for `z_2 < #d < #d_0` (where z_1, z_2 are d_0's zero positions), zero candidates contribute because at position #d + 1, `a_{#d+1} = 0 < d_0[#d+1] = s_{#d+1}` (since #d + 1 > z_2 ≥ z_1 means d_0[#d+1] is non-zero), forcing `a < s` against `a ≥ s`. Only #d = #d_0 contributes, with exactly n candidates (k ∈ [k_s, k_s + n)). The proof's phrase "bounded by comparison constraints" papers over this case decomposition; the bound on k is in fact only operative in the #d = #d_0 case, and is vacuous (no candidates exist) in the #d < #d_0 case.
**Required**: Make the case decomposition explicit. State that for `z_2 < #d < #d_0`, the position-(#d+1) comparison excludes all candidates. State that for #d = #d_0, the position-(#d_0+2) and position-#s comparisons restrict (s'', k) to exactly n combinations. The finiteness then follows as `0 + ... + 0 + n = n`.

OUT_OF_SCOPE: (none — the open questions enumerated in the ASN itself correctly defer reverse-discovery, V-order preservation under K.μ~, link-to-link reference semantics, and inter-document projection comparison to future ASNs)

VERDICT: REVISE
