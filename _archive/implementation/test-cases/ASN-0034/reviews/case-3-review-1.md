**TC-001/TC-002 — Can I run it?** Asserts are boolean expressions (`len(w) <= min(len(a), len(b))`) rather than `f(inputs) == expected_value`. Expected result is implicit `True`. Both are fully mechanically checkable; the form is acceptable.

**TC-003 — Is it right?** `add(a, w_deep)` → [1,0,3,0,2,0,1,5], ordLt([1,0,3,0,2,0,1,2], [1,0,3,0,2,0,1,5]) at position 8: 2 < 5. ✓

**TC-004 — Is it right?** `add(a, w_shallow)` → [4], ordLt([1,0,3,0,2,0,1,2], [4]) at position 1: 1 < 4. Example confirms: "[4] > a (position 1: 4>1)". ✓

**TC-005 — Is it right?** add(a, w_deep)=[1,0,3,0,2,0,1,5], add(b, w_deep)=[1,0,3,0,2,0,1,8], ordLt at position 8: 5 < 8. ✓

**TC-006/TC-007 — Is it right?** add(a, w_shallow)=[4], add(b, w_shallow)=[4]. ordLe([4],[4]) and [4]==[4] both hold. ✓

**TC-008/TC-009 — Is it right?** len([1,0,3,0,2,0,1,5])=8=len(w_deep); len([4])=1=len(w_shallow). ✓

**Skipped (Tail replacement) — Is it complete?** The observable consequence (equality of results) is captured by TC-007. The prose claim about "erasing divergence" has no computable assertion beyond what TC-007 already checks. Skip is justified.

**Coverage check:** All nine Properties exercised bullets map to test cases. No gaps.

```
VERDICT: CONVERGED
```