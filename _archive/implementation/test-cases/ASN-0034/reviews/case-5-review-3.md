**VERDICT: REVISE**

### TC-012: Assert is not in function-call form
`d₁ ≠ d₂` uses inequality notation rather than a function call with an expected result. Every other TC in this suite uses the form `f(args) = value`. This cannot be mechanically dispatched to a single named operation.

**Fix:**
```
Assert: eq(d₁, d₂) = false
```

### Missing TC — T4 boundary allowed case (zeros = 2, k = 2 permitted)
Operation 3 of the worked example explicitly demonstrates `inc(d₁, 2)` producing e₁ = [1, 0, 1, 0, 1, 0, 1]. This is the boundary-allowed case: zeros(d₁) = 2, which is exactly the T4 limit. TC-011 tests the blocked side (zeros = 3 → false). TC-009 checks the zeros count. But no TC asserts that k = 2 is actually valid when zeros = 2. Without the allowed side, the boundary is only half-covered — an off-by-one in the T4 check (e.g., `< 2` instead of `<= 2`) would go undetected.

**Fix:** Add a test case:
```
## TC-018: T4 permits k=2 at the boundary (zeros = 2)
**Property:** TA5 T4 preservation (zeros = 2 → k=2 allowed)
**Given:** d₁ = [1, 0, 1, 0, 1]
**Assert:** inc_valid(d₁, 2) = true
```