**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. T4 gives `t_{#t} ≠ 0`. T0 fixes the carrier as ℕ, so `t_{#t} ∈ ℕ`. NAT-zero supplies `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` excludes the equality branch, leaving `0 < t_{#t}`.

Since `t_{#t} > 0`, by TA5-SIG, `sig(t) = max(S)` where `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}`; the range predicate `1 ≤ i ≤ #t` reads through NAT-order's `≤` definition. The index `#t` satisfies `1 ≤ #t ≤ #t` — the left bound by T0's `#t ≥ 1` lifted through the same definition, the right bound by reflexivity of `=` — and `t_{#t} ≠ 0` by T4, so `#t ∈ S` and `sig(t) ≥ #t`. TA5-SIG's postcondition gives `sig(t) ≤ #t`. Combining the two through antisymmetry of `≤` — supplied by NAT-order via exactly-one trichotomy, which eliminates the three disjoint-pair cases `m < n ∧ n < m`, `m < n ∧ m = n`, and `m = n ∧ n < m` from the four-way distribution of the conjoined disjunctions — yields `sig(t) = #t`. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies `t_{#t} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ, giving `t_{#t} ∈ ℕ`, and supplies `#t ≥ 1` for every `t ∈ T`.
  - NAT-zero (NatZeroMinimum) — supplies the disjunction `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` eliminates the equality branch, yielding `0 < t_{#t}`.
  - NAT-order (NatStrictTotalOrder) — supplies the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`, used (a) to interpret TA5-SIG's range predicate `1 ≤ i ≤ #t` and the postcondition `sig(t) ≤ #t`, (b) to witness `1 ≤ #t ≤ #t` (hence `#t ∈ S`); supplies antisymmetry of `≤` — derived from the exactly-one trichotomy clauses `¬(m < n ∧ n < m)`, `¬(m < n ∧ m = n)`, `¬(m = n ∧ n < m)` — to combine `sig(t) ≥ #t` and `sig(t) ≤ #t` into `sig(t) = #t`.
  - TA5-SIG (LastSignificantPosition) — unfolds `sig(t)` as the maximum-position formula when `t_{#t} > 0` and supplies the range postcondition `sig(t) ≤ #t`.
- *Guarantee:* `sig(t) = #t`.
