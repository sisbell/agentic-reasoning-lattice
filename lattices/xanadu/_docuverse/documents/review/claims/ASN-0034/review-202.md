# Cone Review — ASN-0034/D1 (cycle 2)

*2026-04-17 21:42*

### TumblerSub uses `0 ∈ ℕ` throughout but does not cite NAT-zero
**Foundation**: NAT-zero (NatZeroMinimum) — axiom `(A n ∈ ℕ :: 0 ≤ n)` supplies the missing membership premise `0 ∈ ℕ` that T0's carrier-set definition does not assert. Sister properties in this ASN follow a per-step convention for discharging `0`-related premises: ZPD's Depends explicitly cites NAT-zero with rationale "T0 supplies component-membership in ℕ only for *existing* positions … so `0 ∈ ℕ` is not among T0's assertions"; TumblerAdd, TA-Pos, and ActionPoint likewise cite NAT-zero wherever the literal `0` is used.
**ASN**: TumblerSub. The Definition's piecewise formula uses `rᵢ = 0 for i < k` and the entire no-divergence branch `a ⊖ w = [0, …, 0]`. The Definition's "zero-padded values" stipulation writes `aᵢ = 0 for i > #a` and `wᵢ = 0 for i > #w`. The membership proof says "for `i < k`, `rᵢ = 0 ∈ ℕ` … or `0 ∈ ℕ` (when `i > #a`) … In the equal case (no divergence), every component is `0 ∈ ℕ`." The precondition-consequence proof writes "The padded extension sets `wₖ = 0` for `k > #w` … `aₖ ≠ 0 = wₖ`, so `aₖ > 0 = wₖ`". The Pos postcondition proof says "Components before position `k` are zero by construction". TumblerSub's Depends lists T0, T1, Divergence, ZPD, TA-Pos, ActionPoint, NAT-sub, NAT-discrete, NAT-order — **no NAT-zero**.
**Issue**: Every occurrence of the literal `0` in TumblerSub's Definition, membership proof, and precondition-consequence proof presupposes `0 ∈ ℕ` so that `a ⊖ w` has ℕ-valued components (required for `a ⊖ w ∈ T` by T0) and so that the equalities `wₖ = 0`, `aₖ ≠ 0`, and the no-divergence zero tumbler are well-formed ℕ-valued comparisons. T0's exhaustive NAT-* enumeration does not fix `0 ∈ ℕ`; only NAT-zero's `(A n ∈ ℕ :: 0 ≤ n)` presupposes it. TumblerSub's zero-padding of operands is an ASN-internal construction — it cannot rely on ZPD's NAT-zero citation (scoped to ZPD's padded projections `â`, `ŵ`), and the propagation of ZPD's postconditions into TumblerSub does not carry along ZPD's Depends entries. Without NAT-zero cited, the literal `0` in TumblerSub is an unsourced constant, breaking the per-step citation discipline the sister properties enforce.
**What needs resolving**: TumblerSub must either (a) add NAT-zero to its Depends with per-site discharge notes for the literal `0` in the definition's "i < k" clause, the zero-padding stipulation for minuend and subtrahend operands, the no-divergence zero-tumbler result, and the precondition-consequence's `wₖ = 0` equality; or (b) restructure the Definition to avoid introducing the literal `0` directly (e.g., by routing all zero-valued components through ZPD's already-cited padded projections). The current formulation leaves `0 ∈ ℕ` undischarged.

## Result

Cone converged after 3 cycles.

*Elapsed: 1881s*
