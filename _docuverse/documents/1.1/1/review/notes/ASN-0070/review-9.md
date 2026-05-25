# Review of ASN-0070

I conducted a thorough review of ASN-0070 (FOLLOWLINK Operation), examining the proofs, case analyses, foundation citations, and derived properties. The work is rigorous and the proofs are detailed.

## REVISE

After careful examination of each section — F0 (inverse-image relation), F-subspace, V-restricted denotation, F1 (follow operation), F-canonical (with its three-step uniqueness proof), the worked example's four configurations, and all 16 derived properties (F-det, F-sound, F-complete, F-empty, F-multi, F-frame, F-slot, F-origin, F-persist, F-state, F-multidoc, F-contig, F-canonical, and the F-subspace consequence) — I found no substantive correctness issues:

- The case analysis in F-canonical Step 1 (`k < m_S(d)` infinite vs. `k = m_S(d)` finite) is exhaustive over `actionPoint(ℓ) ∈ {1, ..., #ℓ}` with T12's `actionPoint(ℓ) ≤ #s` bounding `k ≤ m_S(d)`.
- The consecutivity characterization in Step 2 (forward + reverse via induction) is sound, with T0 discreteness correctly applied to force `t''_m = t_m`.
- The right-closure and left-closure arguments correctly establish that maximal runs match components, with the `j = 1` vacuous case explicitly noted.
- The contiguity proof for `I(β) ∩ ⟦σ⟧` correctly handles both `k₁ ≥ 1` (via TS5) and `k₁ = 0` (via TS4 + OrdinalShiftBase).
- F-multi properly separates the implication (from F0 + F1 + F-subspace) from structural admissibility (via S5's within-document multiplicity clause).
- F-empty's representational conclusion (only `⟨⟩` is canonical for empty V-restricted denotation) is established via T12(b) + the positivity convention.
- The worked example's Configuration 4 verifies K.μ⁻'s precondition `n'_{s_C} = 3 < 6 = n_{s_C}` and produces a contracted state satisfying D-CTG★/D-MIN★.
- All foundation citations (ASN-0034, 0036, 0043, 0047, 0053, 0058) are appropriate and used correctly.
- F-sound and F-complete are correctly identified as the two halves of the postcondition's set equality, with both directions established.
- The "convention" for `m_S(d)` undefined is internally consistent: `⟦⟨⟩⟧_V := ∅` agrees with the general formula when `m_S(d)` is defined.

## OUT_OF_SCOPE

The open questions section appropriately defers downstream questions (partial reach reporting, multi-document lineage relationships, concurrency semantics, implementation interface for canonicalisation).

VERDICT: CONVERGED
