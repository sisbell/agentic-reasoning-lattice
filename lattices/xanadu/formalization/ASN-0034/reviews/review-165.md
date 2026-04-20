# Cone Review — ASN-0034/ActionPoint (cycle 1)

*2026-04-17 14:30*

### ActionPoint depends list omits NAT-zero and NAT-order needed for `w_{actionPoint(w)} ≥ 1`
**Foundation**: NAT-zero (NatZeroMinimum) and NAT-order (NatStrictTotalOrder); TA-Pos's own Case `#z ≥ k` argument sets the precedent, chaining NAT-zero → NAT-order's definition of `≤` → exclusion of the equality disjunct to derive `0 < tₖ` from `tₖ ≠ 0`.
**ASN**: ActionPoint, third postcondition *"w_{actionPoint(w)} ≥ 1"*, whose Depends text says the inference "`nonzero ⇒ ≥ 1`" is "discharged from NAT-discrete rather than left implicit," and parenthetically notes "no `n ∈ ℕ` with `0 ≤ n < 1` other than `0` itself".
**Issue**: The parenthetical gloss smuggles in `0 ≤ w_{actionPoint(w)}` without citing its source. NAT-discrete's axiom `m ≤ n < m + 1 ⟹ n = m` applied at `m = 0` requires both (a) the premise `0 ≤ w_{actionPoint(w)}` — supplied only by NAT-zero's `(A n ∈ ℕ :: 0 ≤ n)`, exactly as TA-Pos makes explicit — and (b) NAT-order's definition of `≤` / trichotomy / irreflexivity to convert `0 ≤ n ∧ n ≠ 0` into `0 < n` and then complete the contrapositive of NAT-discrete (TA-Pos Case `#z < k` composes these similarly). Neither NAT-zero nor NAT-order appears in ActionPoint's Depends list, so the chain from `w_{actionPoint(w)} ≠ 0` to `w_{actionPoint(w)} ≥ 1` is not licensed by the cited foundations.
**What needs resolving**: ActionPoint must either add NAT-zero and NAT-order to its Depends list with the inference steps they discharge spelled out (matching TA-Pos's precedent), or restructure the third postcondition's derivation so that NAT-discrete alone — with only T0 and TA-Pos — suffices.
