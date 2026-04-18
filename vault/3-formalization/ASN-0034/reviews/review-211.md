# Cone Review — ASN-0034/TA-assoc (cycle 7)

*2026-04-17 23:34*

### TA-assoc *Action point of `s`* elides "≥ 1 → > 0" at each sub-case's positivity conclusion

**Foundation**: ActionPoint (sister property in this ASN) — supplies minimum-nonzero `w_{actionPoint(w)} ≥ 1`; NAT-order (NatStrictTotalOrder) — supplies the defining clause `m ≤ n ⟺ m < n ∨ m = n` that unfolds a non-strict lower bound into the strict disjunct; NAT-zero (NatZeroMinimum) — supplies `0 ≤ n` for components in ℕ.

**ASN**: TA-assoc (AdditionAssociative), *Action point of `s`*, the three trichotomy sub-cases each conclude with a strict `> 0` claim:
- `k_b < k_c`: "`s_{k_b} = b_{k_b} > 0`, since `k_b` is the action point of `b`".
- `k_b = k_c`: after routing NAT-addcompat to obtain `b_{k_b} + c_{k_b} > b_{k_b}`, the paragraph writes "and ActionPoint's minimum-nonzero at `w = b` giving `b_{k_b} ≥ 1` yields `s_{k_b} = b_{k_b} + c_{k_b} > 0`".
- `k_b > k_c`: "`s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c} > 0`".

**Issue**: In every sub-case, ActionPoint's minimum-nonzero supplies only a non-strict `≥ 1` on the relevant component (`b_{k_b} ≥ 1`, resp. `c_{k_c} ≥ 1`). The step from `≥ 1` to `> 0` on ℕ is not a postcondition of ActionPoint — it is a NAT-order + NAT-zero unfolding (`0 ≤ b_{k_b}` by NAT-zero, unfolded to `0 < b_{k_b} ∨ 0 = b_{k_b}` by NAT-order's defining clause, with the equality ruled out by `b_{k_b} ≥ 1` via NAT-order's irreflexivity or trichotomy), followed by transitivity to reach `> 0`. In the `k_b = k_c` sub-case the gap is compounded: the explicitly-derived strict inequality is `s_{k_b} > b_{k_b}` (relative to `b_{k_b}`, not `0`), and the stated conclusion `s_{k_b} > 0` requires composing `s_{k_b} > b_{k_b}` with a separately-derived `b_{k_b} > 0` via NAT-order's transitivity of `<`. None of these intermediate steps is cited. This violates the per-step citation discipline the rest of this paragraph applies — including the carefully-sourced NAT-addcompat + NAT-order + NAT-closure chain that derives `s_{k_b} > b_{k_b}` in the same sub-case — and the analogous `≥ 1 → > 0` elision at TumblerAdd's dominance-proof sites does not appear (that proof routes strict positivity through the explicitly-derived `aₖ + wₖ > wₖ`, not through a `≥ 1`-to-`> 0` shortcut).

**What needs resolving**: For each of the three sub-cases, either (a) make the `≥ 1 → > 0` step explicit with citations to NAT-zero (for `0 ≤ x`), NAT-order (for unfolding `0 ≤ x` into `0 < x ∨ 0 = x` and ruling out the equality disjunct against `x ≥ 1`), and — in the `k_b = k_c` sub-case — NAT-order's transitivity of `<` to compose `s_{k_b} > b_{k_b}` with `b_{k_b} > 0`; or (b) rephrase each sub-case to conclude a weaker but sufficient fact (e.g., `s_{min(k_b,k_c)} ≠ 0`) that TA-Pos's defining existential consumes directly without requiring the strict `> 0` lift.
