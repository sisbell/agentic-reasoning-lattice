# Cone Review — ASN-0034/OrdinalShift (cycle 2)

*2026-04-17 22:10*

### OrdinalDisplacement silently crosses `n ≥ 1 ⟹ n ≠ 0` in two load-bearing steps
**Foundation**: (internal) T0 (CarrierSetDefinition) — establishes the per-step citation discipline for ℕ facts via its exhaustive NAT-* enumeration; sister proofs (TumblerAdd, TA-Pos) rigorously cite NAT-order and NAT-addcompat at analogous `≥`/`≠`/`<` transformations.
**ASN**: OrdinalDisplacement (OrdinalDisplacement) — (i) "Since n ≥ 1, the m-th component of δ(n, m) is nonzero, whence Pos(δ(n, m)) by TA-Pos" and (ii) "since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≥ 1, the minimum is m". Depends lists T0, NAT-zero, TA-Pos, ActionPoint — no NAT-order, no NAT-addcompat.
**Issue**: Both steps convert `n ≥ 1` into `n ≠ 0`: Pos(t)'s definition requires `(E i : tᵢ ≠ 0)` (so establishing Pos(δ) needs δₘ ≠ 0, i.e., n ≠ 0), and ActionPoint's minimum is over `{i : δᵢ ≠ 0}` (so concluding m is in that set needs n ≠ 0). On ℕ, `n ≥ 1 ⟹ n ≠ 0` requires NAT-addcompat's strict successor inequality (`0 < 1` via `n < n+1` at n=0) composed with NAT-order's trichotomy/irreflexivity — neither cited. This is exactly the strict-from-`≥` promotion pattern TumblerAdd's Depends meticulously discharges at every analogous site (e.g., the `rₖ = aₖ + wₖ ≥ aₖ + 1 > aₖ` chain), and that TA-Pos's Case `#z ≥ k` discharges at the structurally identical step `0 ≤ tₖ` + `tₖ ≠ 0` ⟹ `0 < tₖ`.
**What needs resolving**: Either add the missing NAT-order (and NAT-addcompat, as applicable) citations with the per-step routing note for the `n ≥ 1 ⟹ n ≠ 0` inference at both sites, or restructure the proof to route `δₘ ≠ 0` through an already-cited axiom. Matching the citation discipline this ASN enforces elsewhere makes the reasoning auditable rather than implicit.

## Result

Cone converged after 3 cycles.

*Elapsed: 1800s*
