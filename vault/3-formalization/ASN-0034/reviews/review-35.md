# Cone Review — ASN-0034/TA3 (cycle 1)

*2026-04-14 03:13*

I'll read through this carefully as a system, checking cross-property consistency, precondition chains, and case exhaustiveness.

### TA3 Sub-case A2: improper prefix cited under T1 case (ii)
**Foundation**: T1 (LexicographicOrder), specifically case (ii) — proper prefix ordering
**ASN**: TA3 proof, Sub-case A2, the paragraph beginning "If no disagreement exists on positions `1, ..., max(#a, #w)`"
**Issue**: The proof concludes: "then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii)." T1 case (ii) requires a *proper* prefix — `k = m+1 ≤ n`, i.e., strict length inequality. But when `#w ≥ #b`, both results have length `max(#a, #w) = #w = max(#b, #w)`, and the "prefix" is actually equality.

Concrete witness: `a = [2, 1]`, `b = [2, 1, 0, 0]`, `w = [1, 0, 0, 0]`. All preconditions hold (`a < b` by T1 case (ii), `a > w` and `b > w` by T1 case (i)). Both subtractions yield `[1, 1, 0, 0]` of length 4. The results are equal by T3, not ordered by T1 case (ii). The conclusion `a ⊖ w ≤ b ⊖ w` is correct (via equality), but the cited justification is invalid for this sub-case.

The same misapplication appears in the subsequent sentence: "if `(b ⊖ w)_p = 0` at all such positions, then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii)" — though this branch is additionally vacuous (a "first disagreement" position where both sides are zero is not a disagreement).

**What needs resolving**: The proof must distinguish the case `#(a ⊖ w) < #(b ⊖ w)` — where T1 case (ii) properly applies — from the case `#(a ⊖ w) = #(b ⊖ w)` (triggered when `#w ≥ #b`), where full component agreement yields `a ⊖ w = b ⊖ w` by T3, and `≤` follows from equality. A TLA+ encoding would require this case split.

## Result

Cone converged after 2 cycles.

*Elapsed: 3121s*
