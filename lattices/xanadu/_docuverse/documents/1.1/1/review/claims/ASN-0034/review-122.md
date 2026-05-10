# Cone Review — ASN-0034/D2 (cycle 3)

*2026-04-17 03:40*

### TumblerSub Depends omits NAT-discrete despite using "nonzero ⇒ > 0" inference

**Foundation**: (foundation ASN — internal consistency; per-step NAT-* citation convention established by T0 and applied to sister properties TA-Pos and ActionPoint, both of which cite NAT-discrete by name for the same inference)

**ASN**: TumblerSub's precondition-consequence proof, Case (ii) — prefix divergence: *"The padded extension sets `wₖ = 0` for `k > #w`. Since zpd is defined, the longer operand `a` has some nonzero component beyond `#w`; at `k = zpd(a, w)`, `aₖ ≠ 0 = wₖ`, so `aₖ > 0 = wₖ`."* The step `aₖ ≠ 0 ⟹ aₖ > 0` for `aₖ ∈ ℕ` is the "nonzero ⇒ ≥ 1" inference that TA-Pos and ActionPoint discharge with explicit NAT-discrete citations (TA-Pos: *"by NAT-discrete's axiom `m ≤ n < m + 1 ⟹ n = m` instantiated at `m = 0` (no `n ∈ ℕ` with `0 ≤ n < 1` other than `0`)"*; ActionPoint: identical reasoning). TumblerSub's Depends lists T0, T1, Divergence, ZPD, TA-Pos, ActionPoint, NAT-sub, NAT-order — no NAT-discrete.

**Issue**: The case (ii) inference is the load-bearing step that promotes `aₖ ≠ 0` to the strict comparison `aₖ > wₖ` which is then propagated as the "precondition consequence" feeding NAT-sub's strict-positivity and conditional-closure clauses for the entire downstream chain (TumblerSub's positivity postcondition, D0's positivity, D1's `wₖ ≥ 1`, D2's positivity verification). TumblerSub's NAT-order citation only covers the `>` → `≥` conversion at the NAT-sub interface, not the prior `≠ 0` → `> 0` step. A reviser tightening NAT-discrete has no Depends-backed signal that TumblerSub's case (ii) consumes it, even though sister properties applying the same inference cite it explicitly.

**What needs resolving**: TumblerSub's Depends must cite NAT-discrete for the `aₖ ≠ 0 ⟹ aₖ > 0` step in case (ii) of the precondition-consequence proof, matching the per-step convention TA-Pos and ActionPoint already follow. Alternatively, restate the step in terms of NAT-order/NAT-sub facts already in TumblerSub's current Depends.

## Result

Cone not converged after 3 cycles.

*Elapsed: 977s*
