# Cross-cutting Review — ASN-0034 (cycle 3)

*2026-04-17 08:39*

Reading the ASN end-to-end with a focus on cross-property precondition chains, I'll check for gaps that live between properties rather than within individual proofs.

### D2 Step 2 silently bridges zpd to divergence without citing ZPD
**Foundation**: N/A (foundation ASN — internal consistency)
**ASN**: D2 (DisplacementUnique), Step 2. The proof writes: *"For b ⊖ a: let k = divergence(a, b). By hypothesis k ≤ #a. Since a < b, the divergence occurs at a position where bₖ > aₖ (by T1), so `(b ⊖ a)ₖ = bₖ − aₖ ∈ ℕ` by NAT-sub (conditional closure...) and `(b ⊖ a)ₖ = bₖ − aₖ ≥ 1` by NAT-sub (strict positivity...). Every component before position k is zero (TumblerSub copies the agreement prefix as zeros). Therefore Pos(b ⊖ a) with action point k, and k ≤ #a satisfies TA0."*
**Issue**: TumblerSub's component formulas are parameterised by `zpd(b, a)`, not by `divergence(a, b)`: the definition gives `rᵢ = 0` for `i < zpd(b, a)`, `r_{zpd(b,a)} = b_{zpd(b,a)} − a_{zpd(b,a)}`, and TumblerSub's conditional postcondition gives `actionPoint(b ⊖ a) = zpd(b, a)`. To use these formulas at `k = divergence(a, b)` — as D2 does — one must invoke the ZPD–Divergence relationship in case (i) (`zpd(b, a) = divergence(b, a) = divergence(a, b)`) to identify the two indices. D1, which runs a structurally identical argument, explicitly cites ZPD and performs this identification. D2 does not: its Depends list (D1, D0, T1, TumblerSub, TumblerAdd, ActionPoint, TA-Pos, TA0, TA-LC, NAT-sub, NAT-order) omits ZPD. The step "`(b ⊖ a)ₖ = bₖ − aₖ`" at `k = divergence(a, b)`, the "every component before position k is zero" claim, and the "action point k" identification all consume the zpd-to-divergence bridge that is not discharged.
**What needs resolving**: Either add ZPD to D2's Depends and perform the `zpd(b, a) = divergence(a, b)` identification explicitly in Step 2 (as D1 does), or restate Step 2 in terms of `zpd(b, a)` throughout and derive its equality with `divergence(a, b)` at a single bridge step that cites ZPD.
