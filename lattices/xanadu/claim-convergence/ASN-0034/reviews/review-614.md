# Cone Review — ASN-0034/TA3-strict (cycle 1)

*2026-04-26 08:15*

### Native projections used where padded projections are required (TA3-strict)
**Class**: REVISE
**Foundation**: (none — internal)
**ASN**: TA3-strict, Cases 1 and 3 (and Setup), e.g. Case 1 subcase `j = d`: "`(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`, both in ℕ by NAT-sub (conditional closure) under `a_d, b_d ≥ w_d`"; Case 3: "`(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0` by NAT-sub strict positivity"; Case A: "`wⱼ = aⱼ < bⱼ`".
**Issue**: `d = d_a` (and `d_b`) is only known to satisfy `d ≤ #a` (and `d ≤ #b`); it is not generally bounded by `#w`. When `d > #w`, the native symbol `w_d` is outside the index domain of `w` (T0 restricts `wᵢ` to `{j ∈ ℕ : 1 ≤ j ≤ #w}`), so `a_d - w_d` is not a well-formed expression and NAT-sub's preconditions are not stated on the right operand. TumblerSub itself defines components via the *padded* projections `âₖ − ŵₖ`, and the divergence-point inequality it exports is `âₖ > ŵₖ`. TA3-strict reverts to native notation throughout, eliding the fact that NAT-sub must be invoked on `â_d, ŵ_d ∈ ℕ`.
**What needs resolving**: state the divergence-point arithmetic and the NAT-sub invocations on ZPD's padded projections (or otherwise discharge that the relevant indices lie in the shared native domain in the cases where native notation is used).

### Setup justification of `a_{d_a} > w_{d_a}` is muddled
**Class**: REVISE
**Foundation**: (none — internal)
**ASN**: TA3-strict, Setup: "`d_a = zpd(a, w)` is well-defined with `a_{d_a} > w_{d_a}` (from `a > w`, via T3's contrapositive giving `a ≠ w`, then T1 trichotomy)."
**Issue**: The inferential chain is incoherent. `a > w` already entails `a ≠ w` directly (T1 irreflexivity / exactly-one trichotomy), so T3's contrapositive is not needed for that step. The thing actually needing justification is the divergence-point inequality `â_{d_a} > ŵ_{d_a}` (on padded projections) — which is exactly TumblerSub's precondition-discharging derivation under `a ≥ w` and `zpd(a, w)` defined. The current parenthetical does not name that derivation, and silently drops the padding distinction (writes `a_{d_a} > w_{d_a}`).
**What needs resolving**: state the inequality on padded projections and cite the established source (TumblerSub's precondition derivation, or ZPD together with the `a ≥ w` precondition reproduced inline) rather than the spurious T3+T1 chain.

### Case A elides wᵢ undefined when #a > #w
**Class**: REVISE
**Foundation**: (none — internal)
**ASN**: TA3-strict, Case A: "For `i < j`: `bᵢ = aᵢ = wᵢ`" and "At position `j`: `wⱼ = aⱼ < bⱼ`, so `(b, w)` diverges at `j`".
**Issue**: Zero-padded equality of `a` and `w` under `a ≥ w` permits `#a > #w` (e.g., `a = [3,0]`, `w = [3]`). For `#w < i ≤ #a`, `wᵢ` is not in `w`'s native index domain, so `aᵢ = wᵢ` is not well-formed; the correct statement is `âᵢ = ŵᵢ = 0`. Likewise the divergence claim at `j` and the identification `d_b = j` need to be argued on padded projections together with `j ≤ #b = #a`. The conclusion is recoverable, but the proof as written conflates native and padded notation in the same way as the previous finding.
**What needs resolving**: rewrite Case A's component reasoning on padded projections, or restrict to `j ≤ #w` and handle `j > #w` explicitly via the padding clause `ŵⱼ = 0`.

### Unused set `Z` introduced in TA-Pos
**Class**: OBSERVE
**Foundation**: (none — internal)
**ASN**: TA-Pos: "`**Z** = {t ∈ T : Zero(t)}`" appears in the Definition slot but is not cited in any subsequent depends list, postcondition, or proof in this ASN.
**Issue**: Introducing `Z` adds a symbol that no downstream claim consumes. Either it is anticipatory (intended for a downstream ASN, in which case it could live there) or it is unmoored.
**What needs resolving**: (none — observation).

VERDICT: REVISE
