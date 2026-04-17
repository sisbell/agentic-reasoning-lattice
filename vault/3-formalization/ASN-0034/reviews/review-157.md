# Cone Review — ASN-0034/Divergence (cycle 1)

*2026-04-17 12:26*

### `min` used as a structural operator in Divergence without definition or Depends citation
**Foundation**: N/A (internal consistency of Divergence against T0, NAT-order, NAT-wellorder)
**ASN**: Divergence *Definition* and supporting uniqueness argument:
> "if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` … then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`."

and the uniqueness proof's set `S := {i ∈ ℕ : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}`.

**Issue**: `min(·, ·)` appears as a load-bearing operator in three places (case (i)'s bound, case (ii)'s value, the minimization set `S`), yet it is never defined in the ASN and no axiom in the Depends list discharges it. T0 supplies `#·` but not a binary minimum on ℕ; NAT-order supplies strict total order but the ASN never states that `min(m, n)` is the unique element of `{m, n}` satisfying `min ≤ m ∧ min ≤ n`. Downstream results that cite Divergence (TA1-strict's combined precondition `actionPoint(w) ≤ min(#a, #b)`, the prefix-case inequality `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`) inherit this gap: they reason about `min` as if it were an axiomatized operator.
**What needs resolving**: Either define `min` explicitly (axiom or derivation from NAT-order trichotomy), or rewrite the Divergence Definition in a form that avoids `min` (e.g., bound `k` by `k ≤ #a ∧ k ≤ #b`, and give case (ii)'s value by a case split on `#a < #b` vs `#b < #a`), and ensure the Depends list mentions the source of whichever formulation is used.

### Divergence's Depends list omits T1's Case 2/Case 3 correspondence it claims to "bijection" with
**Foundation**: N/A (internal coherence between Divergence and T1)
**ASN**: Divergence preamble:
> "the two cases here are in bijection with T1's two ordering clauses (case (i) with T1 case (i), case (ii) with T1 case (ii))"

and Divergence's Depends on T1:
> "T1 (LexicographicOrder) — Divergence formalizes the 'first divergence position' that T1's trichotomy proof introduces ad hoc; the two cases here are in bijection with T1's two ordering clauses …"

**Issue**: The claimed bijection is between Divergence's two cases and T1's two *definitional clauses* ((i) shared-position strict comparison, (ii) proper prefix). But Divergence case (i) requires only `aₖ ≠ bₖ`, not a strict order. Bridging from `aₖ ≠ bₖ` to "either `aₖ < bₖ` (T1 case (i) for `a < b`) or `bₖ < aₖ` (T1 case (i) for `b < a`)" requires NAT-order trichotomy on the component pair. Without that step the bijection is only with *unordered* disagreement, not with T1's (directed) clauses. The Depends list does not cite NAT-order, so the bridging axiom is not declared.
**What needs resolving**: Either narrow the stated bijection (Divergence case (i) corresponds to T1 case (i) *in whichever direction holds*, mediated by NAT-order's trichotomy at the divergent component), adding NAT-order to Divergence's Depends; or relocate the component-level direction split so it is clearly part of callers (TA1, T5, etc.) rather than of Divergence's semantics.
