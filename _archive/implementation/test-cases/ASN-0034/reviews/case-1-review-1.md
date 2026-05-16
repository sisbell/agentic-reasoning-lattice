**TC-001:** Runnable. Values match example exactly. Covers T1(ii) p < d. ✓

**TC-002:** Runnable. Values match example exactly. Covers T1(ii) d < e₁. ✓

**TC-003:** Runnable. Values match example exactly. Covers T1(i) e₁ < e₂. ✓

**T2 skip:** Justified — the observable result of `compare(a, b)` is the ordering outcome, not the number of components read. Testing T2 would require an instrumented comparator that counts accesses; that is out of scope for a behavioral test against these inputs.

**T5 skip:** Justified — T5 is a universal property over all tumblers in the interval [e₁, e₂]. No finite set of concrete inputs can discharge a "for all" claim.

```
VERDICT: CONVERGED
```