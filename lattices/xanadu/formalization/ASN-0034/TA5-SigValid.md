**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. T4 gives `t_{#t} ≠ 0`. T0 fixes the carrier as ℕ, so `t_{#t} ∈ ℕ`; NAT-zero gives `0 ≤ t_{#t}`; NAT-discrete at `m = 0` rules out `0 ≤ t_{#t} < 1` under `t_{#t} ≠ 0`. Therefore `t_{#t} > 0`.

Since `t_{#t} > 0`, by TA5-SIG, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`. The index `#t` belongs to this set, so `sig(t) ≥ #t`. The range guarantee of TA5-SIG gives `sig(t) ≤ #t`. Therefore `sig(t) = #t`. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies `t_{#t} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ, giving `t_{#t} ∈ ℕ`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ t_{#t}`.
  - NAT-discrete (NatDiscreteness) — at `m = 0`, converts `0 ≤ t_{#t}` with `t_{#t} ≠ 0` into `t_{#t} > 0`.
  - TA5-SIG (LastSignificantPosition) — unfolds `sig(t)` as the maximum-position formula and supplies the range guarantee `sig(t) ≤ #t`.
- *Guarantee:* `sig(t) = #t`.
