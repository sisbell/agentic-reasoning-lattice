# Cone Review — ASN-0034/OrdinalShift (cycle 1)

*2026-04-17 21:55*

### OrdinalShift omits arithmetic axiom citations for `vₘ + n ≥ 1`
**Foundation**: (internal) T0 (CarrierSetDefinition) — establishes the per-step citation discipline for ℕ facts via its exhaustive NAT-* enumeration (NAT-zero, NAT-addcompat, NAT-closure, NAT-order, etc.), which the sister property TumblerAdd applies rigorously.
**ASN**: OrdinalShift (OrdinalShift) — the proof concludes "Since n ≥ 1, component positivity holds unconditionally: shift(v, n)ₘ = vₘ + n ≥ 1 for all vₘ ≥ 0", which is promulgated as the Postcondition "shift(v, n)ₘ = vₘ + n ≥ 1". The Depends lists only OrdinalDisplacement, T0, TA-Pos, TA0, TumblerAdd — no NAT-* axioms.
**Issue**: The inference `vₘ + n ≥ 1` is not a TumblerAdd postcondition (TumblerAdd supplies only `rₘ = vₘ + n`, not a lower bound on the sum). Deriving `≥ 1` from `vₘ ≥ 0` (NAT-zero, applied under `vₘ ∈ ℕ` from T0) and `n ≥ 1` (precondition) requires NAT-addcompat's right order-compatibility (to lift `0 ≤ vₘ` into `0 + n ≤ vₘ + n`), NAT-closure's additive identity (`0 + n = n`), and NAT-order transitivity (to chain `vₘ + n ≥ n ≥ 1`). None of these are cited — identical to the axiom-enumeration breaks that TumblerAdd's Depends meticulously discharges at its analogous strict/non-strict arithmetic sites.
**What needs resolving**: Either the postcondition's arithmetic lower bound must be dropped, or NAT-zero, NAT-addcompat, NAT-closure, and NAT-order (as applicable) must be added to the Depends with the per-step routing explanation this ASN's citation discipline requires — and the proof text must name the axiom at each step rather than asserting the bound holds "unconditionally".

### OrdinalDisplacement omits citation for component-membership `0 ∈ ℕ`
**Foundation**: (internal) T0 — the carrier-set criterion requires "each component ∈ ℕ"; zero's membership in ℕ is routed through NAT-zero per T0's own prescription ("`0 ∈ ℕ` *membership* of padding or separator positions … is routed separately through NAT-zero, whose axiom `(A n ∈ ℕ :: 0 ≤ n)` quantifies `0` as a lower bound of ℕ and thereby presupposes `0 ∈ ℕ`").
**ASN**: OrdinalDisplacement (OrdinalDisplacement) — "Since δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, it satisfies the carrier set criterion, so δ(n, m) ∈ T by T0." The Depends lists T0, TA-Pos, ActionPoint — no NAT-zero.
**Issue**: δ(n, m) has m − 1 leading components equal to 0. Satisfying T0's "over ℕ" clause for those components requires `0 ∈ ℕ`, which T0 itself explicitly directs downstream properties to route through NAT-zero. This citation is absent; the sister proof TA-Pos cites NAT-zero at an analogous `0 ∈ ℕ`-adjacent step, so the discipline is established in-document.
**What needs resolving**: Add NAT-zero to OrdinalDisplacement's Depends with the "0 ∈ ℕ for positions 1..m−1" routing note, matching the per-step citation discipline this ASN enforces at every other NAT-* site.

### OrdinalShift does not discharge OrdinalDisplacement's `m ≥ 1` precondition
**Foundation**: (internal) OrdinalDisplacement — Preconditions: `n ≥ 1, m ≥ 1`. T0 — `(A a ∈ T :: #a ≥ 1)` via the length axiom.
**ASN**: OrdinalShift — invokes OrdinalDisplacement with `m = #v`, asserting "by OrdinalDisplacement, δ(n, m) = [0, …, 0, n] is a finite sequence of length m ≥ 1 over ℕ". The precondition `n ≥ 1` transfers directly from OrdinalShift's own precondition, but `m ≥ 1` requires `#v ≥ 1`.
**Issue**: OrdinalShift's preconditions are `v ∈ T, n ≥ 1`. The precondition `m ≥ 1` of OrdinalDisplacement is silently discharged from T0's length axiom applied to `v ∈ T`, but the proof text never names this step. Given the ASN's otherwise explicit per-precondition discharge pattern (OrdinalShift crisply enumerates and discharges all four TA0 preconditions), omitting the `m ≥ 1 ⇐ #v ≥ 1 ⇐ T0` step is an inconsistency in discipline.
**What needs resolving**: Add an explicit sentence discharging `m ≥ 1` from T0's length axiom at the site where OrdinalDisplacement is first invoked, so every invoked-property precondition has a named source.
