# Cone Review — ASN-0034/TA3 (cycle 2)

*2026-04-26 06:30*

### Sub-case A2 of TA3 still uses native notation at the divergence point in the prefix-divergence regime
**Class**: REVISE
**Foundation**: (n/a — internal)
**ASN**: TA3 Sub-case A2 ("a > w with divergence"):
> "At position d: both compute `a_d - w_d = b_d - w_d`, each in ℕ by NAT-sub's conditional closure under `a_d, b_d ≥ w_d` (from the divergence-point inequalities via NAT-order)"

This sub-case bifurcates over how `a > w` is witnessed: T1 case (i) places `d ≤ #a ∧ d ≤ #w` (native projections coincide with padded), but T1 case (ii) — explicitly cited in the same paragraph ("`a > w` by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` is the first `i > #w` with `aᵢ > 0`") — places `d > #w`, in which case `w_d` is undefined natively and the inequality the proof is invoking lives on ZPD's padded projections (`â_d > ŵ_d` with `ŵ_d = 0`).

**Issue**: Sub-cases B2–B4 of TA3 were updated to padded notation (`â_{dₐ}`, `ŵ_{dₐ}`, `b̂_{d_b}`, `ŵ_{d_b}`) consistent with TumblerSub's now-exported divergence-point postcondition, but sub-case A2 still writes `a_d`, `w_d`, `b_d`, `w_d` as if all references are native. In the T1(ii) branch of A2 (and the corresponding tail handling, where `(a ⊖ w)ᵢ = 0` "from a's zero-padding" only makes sense via `âᵢ` for `i > #a`), the cited inequality `a_d, b_d ≥ w_d` references an undefined `w_d`. The minuend formulas at `i = d` and `i > d` should similarly be on `â`, `ŵ`, `b̂` to be well-typed in the prefix-divergence sub-case. The previous-cycle finding's closing instruction — "TA3's notation should distinguish padded from native components at indices that may lie in a padding zone" — was applied in B2–B4 but not in A2/A3.

**What needs resolving**: Rewrite Sub-case A2's divergence-point and tail steps using `â`, `ŵ`, `b̂` whenever the index `d` (or a tail index `i > d`) may lie in a padding zone, then lift to native only at indices known to satisfy `i ≤ #a`, `i ≤ #w`, `i ≤ #b` respectively. Sub-case A3, which inherits the same structural setup (`L_{a,w} = #a`, `b ⊖ w` indexed up to `L_{b,w} = #b`), should be audited for the same drift.

VERDICT: REVISE
