# TA-assoc — Contract FLAG

*2026-04-09 08:36*

preconditions use strict `<` instead of `≤`; extra ensures not in contract

**Issue 1 — Strengthened preconditions (`<` vs `≤`)**

The formal contract specifies:
  Preconditions: `k_b ≤ #a`, `k_c ≤ #b`

The Dafny code has:
  `requires TA.ActionPoint(b) < |a.components|`
  `requires TA.ActionPoint(c) < |b.components|`

Missing/extra/wrong:
  The contract uses `≤` but the Dafny uses `<`, excluding the boundary case where `k_b = |a.components|` or `k_c = |b.components|`. This is a strictly stronger precondition — the lemma fails to cover part of the domain the contract claims is valid.

**Issue 2 — Extra ensures not in postconditions**

The formal contract specifies:
  Postconditions: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`

The Dafny code has:
  `ensures IsPositive(TA.TumblerAdd(b, c))`

Missing/extra/wrong:
  `IsPositive(b ⊕ c)` is not a listed postcondition. It is established in the proof body as an intermediate result needed for well-definedness, and is implied by the action-point postcondition (a tumbler with a defined action point is positive). This is an added guarantee — correct but not contract-specified.
