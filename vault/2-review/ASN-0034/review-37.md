# Proof Verification: TumblerSub

## Verification

I need to check the proofs of TA1/TA1-strict, TA3/TA3-strict, and TA4 within the TumblerSub property section against the provided dependencies.

**Checklist items 1–4 (Preconditions, Case coverage, Postcondition establishment, Conjuncts):** The proofs are thorough. TA1 local proof correctly handles three cases on the relationship between action point `k` and divergence `j`. TA3 exhaustively partitions into prefix (Case 0) and component-divergence (Cases 0a, 1–3), with appropriate sub-cases for the relationship between operands and `w`. TA3-strict correctly eliminates Case 0 via the equal-length precondition, and the remaining cases all yield strict inequality. TA4's restricted preconditions (`k = #a`, `#w = k`, zero-prefix) are necessary — general cancellation fails (e.g., `a = [1,5]`, `w = [2]` gives `(a ⊕ w) ⊖ w = [1] ≠ a`).

**Checklist item 5 (Dependency correctness):** The TA3 proof references **TA6** by name in three locations:

1. Case 0, sub-case `a = w`: *"every zero tumbler is less than every positive tumbler (TA6)"*
2. Case 0, sub-case `a > w` without divergence: *"a ⊖ w (all zeros) is strictly less by TA6"*
3. Case 0a: *"By TA6, a ⊖ w < b ⊖ w"*

**TA6 does not appear in the listed dependencies** (Divergence, T1, TA1, TA1-strict, TA2, TA3). While TA6's content is derivable from T1 — a zero tumbler `z` compared to a positive tumbler `p` with first nonzero at position `j`: if `j ≤ #z`, T1 case (i) gives `z < p`; if `j > #z`, T1 case (ii) gives `z < p` as a proper prefix — it is cited as a named, standalone property rather than derived inline. A dependency used but not declared.

```
RESULT: FOUND

**Problem**: The TA3 proof invokes "TA6" (every zero tumbler is strictly less than every positive tumbler) in three separate cases, but TA6 is not listed in the dependency section. The dependency list contains only: Divergence, T1, TA1, TA1-strict, TA2, TA3.

**Required**: Add TA6 to the dependency list with its statement and formal contract, or replace each TA6 citation with an inline derivation from T1 (which is already a declared dependency).
```
