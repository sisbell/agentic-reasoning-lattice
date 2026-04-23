**TA5a (IncrementPreservesT4).** The operation `inc(t, k)` on a T4-valid address `t` preserves T4 iff `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`. For `k ≥ 3`, T4 is violated.

*Proof.* Let `t` satisfy T4, `t' = inc(t, k)`. T4 requires: (i) `zeros(t) ≤ 3`, (ii) no two zeros adjacent, (iii) `t₁ ≠ 0`, (iv) `t_{#t} ≠ 0`. On ℕ, "non-zero component" means "strictly positive" via NAT-zero's `0 ≤ n` and NAT-discrete instantiated at `m = 0`.

*Case `k = 0`.* By TA5(c), `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1`; by TA5(b), `t'` agrees with `t` at every position `≠ sig(t)`. By TA5-SigValid, `sig(t) = #t`; by T4(iv), `t_{#t} ≠ 0`; hence `t_{sig(t)} ≠ 0`. By NAT-closure, `t_{sig(t)} + 1 ∈ ℕ`; by NAT-zero and NAT-addcompat, `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0`, so `t_{sig(t)} + 1 ≠ 0`. Therefore `zeros(t') = zeros(t)` and no new adjacencies arise. T4 preserved unconditionally.

*Case `k = 1`.* By TA5(d), `#t' = #t + 1` and `t'_{#t+1} = 1`; by TA5(b), `t'` agrees with `t` on original positions. Zero count unchanged: `zeros(t') = zeros(t)`. Left-flank `t'_{#t} = t_{#t} ≠ 0` by T4(iv), so no adjacent zeros; boundary `t'_{#t'} = 1 ≠ 0`. T4 preserved unconditionally.

*Case `k = 2`.* By TA5(d), `#t' = #t + 2`, `t'_{#t+1} = 0`, `t'_{#t+2} = 1`; by TA5(b), original positions agree. So `zeros(t') = zeros(t) + 1`. Left-flank `t'_{#t} = t_{#t} ≠ 0` by T4(iv); right-flank is `1`; boundary `t'_{#t'} = 1 ≠ 0`. T4 preserved iff `zeros(t) + 1 ≤ 3`, i.e., `zeros(t) ≤ 2`.

*Case `k ≥ 3`.* By TA5(d), positions `#t + 1` through `#t + k - 1` are zero. By NAT-sub, `k - 1 ∈ ℕ` and `k - 1 ≥ 2`, so `t'_{#t+1} = t'_{#t+2} = 0`. Instantiating T4(ii) at `i = #t + 1` gives `¬(0 = 0 ∧ 0 = 0)`, which fails. Witness: `inc([1], 3) = [1, 0, 0, 1]`. T4 violated. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4; `k ≥ 0`.
- *Depends:*
  - T4 (HierarchicalParsing) — the four positional clauses being checked; boundary clause `t_{#t} ≠ 0` used in cases `k = 0, 1, 2`; no-adjacent-zeros clause is the violated clause at `k ≥ 3`.
  - T4a (SyntacticEquivalence) — bridges T4's positional conditions with the non-empty-field-segment reading, supporting the case `k ≥ 3` interpretation that adjacent zeros create an empty field.
  - T0 (CarrierSetDefinition) — fixes carrier ℕ so every `tᵢ ∈ ℕ`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` on ℕ.
  - NAT-discrete (NatDiscreteness) — with NAT-zero yields non-zero ⇒ strictly positive on ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` with `1 ∈ ℕ` from the same axiom places `t_{sig(t)} + 1 ∈ ℕ` at case `k = 0`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` at case `k = 0`.
  - NAT-sub (NatPartialSubtraction) — places `k - 1 ∈ ℕ` and sharpens `k ≥ 3` to `k - 1 ≥ 2` at case `k ≥ 3`.
  - TA5 (HierarchicalIncrement) — TA5(b) agreement clauses; TA5(c) for `k = 0`; TA5(d) for `k ≥ 1`.
  - TA5-SigValid (SigOnValidAddresses) — `sig(t) = #t` on T4-valid `t` at case `k = 0`.
- *Guarantee:* `inc(t, k)` satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`.
- *Failure:* For `k ≥ 3`, `inc(t, k)` violates T4 (adjacent zeros create an empty field).
