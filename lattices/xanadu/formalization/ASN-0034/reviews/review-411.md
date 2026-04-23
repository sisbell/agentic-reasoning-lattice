# Regional Review — ASN-0034/T4b (cycle 1)

*2026-04-23 01:42*

I'll review this ASN as a connected system, checking definitions, precondition chains, and exhaustion claims across claims.

### T4a preamble asserts `k ∈ {0,1,2,3}` under weaker preconditions than T4's Exhaustion Consequence covers
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — Exhaustion Consequence scoped to "every T4-valid tumbler"
**ASN**: T4a, derivation preamble: "Set `k = zeros(t) ∈ {0, 1, 2, 3}` with zeros at positions `s₁ < s₂ < … < s_k`"
**Issue**: T4a's Preconditions are "`t ∈ T` with `zeros(t) ≤ 3`; full T4-validity is not assumed." The only available source for `k ∈ {0, 1, 2, 3}` is T4's Consequence, but that Consequence is stated for "every T4-valid tumbler" — a strictly stronger hypothesis. The underlying derivation of exhaustion in T4 uses only `zeros(t) ≤ 3` plus NAT axioms, so the bare membership claim is true, but the citation chain as currently written does not discharge it. The claim is not load-bearing — T4a's case analysis decomposes by `k = 0 / k ≥ 1` and by `1 ≤ i < k`, neither of which requires the specific enumeration `{0, 1, 2, 3}` — so "∈ {0, 1, 2, 3}" is decorative rather than structural. T4b handles the same situation with the per-`k` style ("For each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`"), which sidesteps exhaustion entirely; T4a has not been brought to the same idiom.

### T4's Exhaustion Consequence states a narrower scope than its derivation establishes
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing) — Consequence bullet
**ASN**: T4, Consequence: "`zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler `t`"
**Issue**: The derivation walked in the Exhaustion paragraph uses only the bound `zeros(t) ≤ 3`, NAT-zero's `0 ≤ zeros(t)`, NAT-order's trichotomy, NAT-discrete, and NAT-card's ℕ-typed codomain. It does not appeal to the field-segment constraint, to `t₁ ≠ 0`, or to `t_{#t} ≠ 0`. The Consequence is therefore true under the weaker hypothesis `t ∈ T ∧ zeros(t) ≤ 3`. Stating it under "T4-valid" is a self-inflicted scope narrowing that makes the Consequence awkward to cite at T4a's precondition level (see prior finding).

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 167s*
