**ZPD (ZeroPaddedDivergence).** For tumblers `a, w ∈ T`, the *zero-padded divergence* `zpd(a, w)` is defined on the zero-padded extensions of both operands to a common length `L`, selected by NAT-order's trichotomy on `(#a, #w)`: (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. The *padded projections* `â`, `ŵ` on `{1, ..., L}` are given by `âᵢ = aᵢ` for `1 ≤ i ≤ #a` and `âᵢ = 0` for `#a < i ≤ L`, and symmetrically `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w` and `ŵᵢ = 0` for `#w < i ≤ L`. If `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)`, then `zpd(a, w)` is *undefined* and we say `a` and `w` are *zero-padded-equal*. Otherwise, `zpd(a, w)` is the least `k` with `1 ≤ k ≤ L` such that `âₖ ≠ ŵₖ`.

The function is partial: undefined precisely when `â` and `ŵ` agree everywhere on `{1, ..., L}`, as when one operand is a proper prefix of the other with all trailing components zero (e.g., `a = [3, 0]`, `w = [3]` give `â = ŵ = [3, 0]`). Equal tumblers are trivially zero-padded-equal.

**Relationship to Divergence.** When `a ≠ w`, formal Divergence and `zpd` may disagree. In Divergence case (i) — component divergence at shared position `k` with `k ≤ #a ∧ k ≤ #w` — the padded projections coincide with the native projections through `1, ..., k`, so `zpd(a, w) = divergence(a, w) = k`. In Divergence case (ii) — proper prefix, falling in sub-case (β) or (γ) — Divergence reports `#a + 1` (β) or `#w + 1` (γ), while `zpd` scans the padded components of the shorter operand (all zero) against the longer operand's native components: if the longer operand has a nonzero component past the shorter's last position, `zpd(a, w)` is the least such index, which is ≥ `divergence(a, w)`; if all such trailing components are zero, `zpd(a, w)` is undefined.

*Formal Contract:*
- *Domain:* a ∈ T, w ∈ T
- *Definition:* NAT-order trichotomy on `(#a, #w)` selects (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. Padded projections `â`, `ŵ` on `{1, ..., L}`: `âᵢ = aᵢ` for `1 ≤ i ≤ #a`, `âᵢ = 0` for `#a < i ≤ L`; `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w`, `ŵᵢ = 0` for `#w < i ≤ L`. If `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)`, `zpd(a, w)` is undefined. Otherwise, `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
- *Depends:*
  - T0 (CarrierSetDefinition) — `a, w ∈ T`, lengths `#a`, `#w`, native-domain component projections `aᵢ`, `wᵢ`, ℕ-valuation of native components.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding clauses `âᵢ = 0`, `ŵᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` selects `L` and dispatches the shared-position bound `k ≤ #a ∧ k ≤ #w` and sub-case boundaries `#a + 1`, `#w + 1`.
  - NAT-wellorder (NatWellOrdering) — least-element principle for `min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#w, 1)`, with `1 ∈ ℕ` from the same axiom, places `#a + 1` and `#w + 1` in ℕ in the postcondition.
  - Divergence (Divergence) — two-case structure (component divergence; prefix divergence) and domain restriction `a ≠ b` consumed by the Relationship-to-Divergence postcondition.
- *Codomain:* When defined, `zpd(a, w) ∈ {1, ..., L}`, with `L = #a` in sub-cases (α), (γ) and `L = #w` in sub-case (β).
- *Partiality:* `zpd(a, w)` is undefined iff `a` and `w` are zero-padded-equal.
- *Postconditions (Symmetry):* `zpd(a, w)` is defined iff `zpd(w, a)` is defined, and when defined, `zpd(a, w) = zpd(w, a)`. Sub-case (α) is self-symmetric; sub-cases (β) and (γ) swap under exchange, yielding the same `L`; the disagreement predicate is symmetric.
- *Postconditions (Relationship to Divergence):* For `a ≠ w`: in Divergence case (i) with divergence at `k` satisfying `k ≤ #a ∧ k ≤ #w`, `zpd(a, w) = divergence(a, w)`. In Divergence case (ii), under sub-case (β) or (γ): if the longer operand has a nonzero component beyond the shorter's last position, `zpd(a, w)` is defined and `zpd(a, w) ≥ divergence(a, w)`; if all such components are zero, `zpd(a, w)` is undefined.
