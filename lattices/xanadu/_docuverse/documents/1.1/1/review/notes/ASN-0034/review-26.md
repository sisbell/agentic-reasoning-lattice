# Proof Verification: TA3

Now I have the full picture. Let me verify the TA3 proof.

**TA3 Claim**: `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`

**Proof text**: "Immediate from TA2: `a ⊖ w < b ⊖ w` implies `a ⊖ w ≤ b ⊖ w`, since `<` ⊂ `≤`."

**Verification:**

1. **Precondition completeness** — TA3's preconditions (`a < b ∧ a ≥ w ∧ b ≥ w`) exactly match TA2's preconditions. ✓

2. **Case coverage** — The precondition is `a < b` (strict), so only the strict-inequality case arises. No need for a separate `a = b` case. ✓

3. **Postcondition establishment** — TA2 gives `a ⊖ w < b ⊖ w`; weakening `<` to `≤` is elementary. ✓

4. **All conjuncts addressed** — Single conclusion, addressed. ✓

5. **Dependency correctness** — The proof cites TA2 and uses it correctly. However, the appeal to TA2 is only valid if `a ⊖ w` and `b ⊖ w` are well-formed tumblers (otherwise the `<` comparison is undefined). Well-formedness of these differences follows from **TA0** (tumbler subtraction closure) applied to the preconditions `a ≥ w` and `b ≥ w`. TA0 is not cited.

---

```
RESULT: FOUND

**Problem**: The proof invokes TA2 to obtain `a ⊖ w < b ⊖ w`, but this comparison presupposes that both differences are well-formed tumblers. That guarantee comes from TA0 (tumbler subtraction closure), which is used but not declared as a dependency. Without TA0, the expressions `a ⊖ w` and `b ⊖ w` are not known to be valid tumblers, and the ordering relation `<` between them is undefined.

**Required**: Cite TA0 as a dependency and add a sentence noting that TA0 + the preconditions `a ≥ w` and `b ≥ w` guarantee `a ⊖ w` and `b ⊖ w` are well-formed, making the appeal to TA2 legitimate.
```
