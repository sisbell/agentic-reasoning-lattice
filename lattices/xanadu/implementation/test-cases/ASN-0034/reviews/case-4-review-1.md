Checking each TC against the worked example.

**TC-001.** add([2],[3])=[5]; subtract([5],[3])=[2]. Given/assert match example exactly. ✓

**TC-002.** add(a,w): positions 1–7 copy from a, position 8: 2+3=5 → [1,0,3,0,2,0,1,5]. subtract([1,0,3,0,2,0,1,5],[0,0,0,0,0,0,0,3]): divergence at position 1 (1≠0); position 1 gets 1−0=1; positions 2–8 copy → [1,0,3,0,2,0,1,5]. Matches assert. ✓

**TC-003.** compare([1,0,3,0,2,0,1,5],[0,0,0,0,0,0,0,3]): position 1, 1>0 → Greater. Matches example's TA2 check. ✓

**TC-004.** subtract([3],[3]): no divergence → zero sentinel [0]. Matches example. ✓

**TC-005.** compare([0],[1,0,3,0,2,0,1,1]): position 1, 0<1 → Less by T1 case (i). Matches example. ✓

**Completeness.** Six properties listed; five have TCs (TC-001 through TC-005); TA7a is skipped. The skip is legitimate — the property is structural (N=1 as context, not operand), no computable operation to call.

```
VERDICT: CONVERGED
```