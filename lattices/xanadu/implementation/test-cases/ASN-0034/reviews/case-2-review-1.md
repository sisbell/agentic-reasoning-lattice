TC-001 through TC-005 all pass all three checks. Inputs and outputs match the worked example exactly, and each TC is mechanically executable as written.

One issue: the skip.

```
VERDICT: REVISE

### T3 (canonical representation): skip justification is invalid — property is testable

"For-all assertion across five inputs, not a single computable fact" is not a valid
skip reason. Four known inputs over one predicate is four test cases. The property
asserts that x₁–x₄ each satisfy T3 (canonical representation) despite failing T4 —
the structural point of the example is that T4 invalidity does not imply T3 invalidity.
Each input yields a single, independent, computable result.

**Fix:** Add:

TC-006: Given: addr = [1, 0, 0, 3]      Assert: t3(addr) == Valid
TC-007: Given: addr = [0, 1, 0, 3]      Assert: t3(addr) == Valid
TC-008: Given: addr = [1, 0, 3, 0]      Assert: t3(addr) == Valid
TC-009: Given: addr = [1, 0, 3, 0, 2, 0, 1, 0]  Assert: t3(addr) == Valid
```