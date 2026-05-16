# Test Cases — Example 5: T10 + TA5 — Allocation streams, child-spawning, and partition independence

Source: vault/5-examples/{ASN label}/examples-1.md, Example 5

## TC-001: inc with k=2 produces correct child address
**Property:** TA5(d) (k≥1 result)
**Given:** n = [1]
**Assert:** inc(n, 2) = [1, 0, 1]

## TC-002: inc with k=2 produces length |n|+k
**Property:** TA5(d) (length formula)
**Given:** n = [1]
**Assert:** len(inc(n, 2)) = 3

## TC-003: inc with k=2 places zero separator at position |n|+1
**Property:** TA5(d) (separator placement)
**Given:** n = [1]
**Assert:** at(inc(n, 2), 2) = 0

## TC-004: inc with k=2 places one at final position
**Property:** TA5(d) (fresh address)
**Given:** n = [1]
**Assert:** at(inc(n, 2), 3) = 1

## TC-005: sig identifies last nonzero position
**Property:** TA5(c) (sig definition)
**Given:** u₁ = [1, 0, 1]
**Assert:** sig(u₁) = 3

## TC-006: inc with k=0 increments at sig position
**Property:** TA5(c) (k=0 result)
**Given:** u₁ = [1, 0, 1]
**Assert:** inc(u₁, 0) = [1, 0, 2]

## TC-007: inc with k=0 preserves length
**Property:** TA5(c) (k=0 length invariant)
**Given:** u₁ = [1, 0, 1]
**Assert:** len(inc(u₁, 0)) = 3

## TC-008: zeros counts interior zero components
**Property:** TA5 T4 preservation (zeros at user level)
**Given:** u₁ = [1, 0, 1]
**Assert:** zeros(u₁) = 1

## TC-009: zeros count for depth-2 address
**Property:** TA5 T4 preservation (zeros at document level)
**Given:** d₁ = [1, 0, 1, 0, 1]
**Assert:** zeros(d₁) = 2

## TC-010: inc_valid allows k=2 when zeros=0
**Property:** TA5 T4 preservation (node-level)
**Given:** n = [1]
**Assert:** inc_valid(n, 2) = true

## TC-011: inc_valid blocks k=2 when zeros=3
**Property:** TA5 T4 preservation (depth-3 blocked)
**Given:** e₁ = [1, 0, 1, 0, 1, 0, 1]
**Assert:** inc_valid(e₁, 2) = false

## TC-012: partition independence — outputs under distinct parents are unequal
**Property:** T10 (non-nesting outputs differ)
**Given:** d₁ = [1, 0, 1, 0, 1]; d₂ = [1, 0, 2, 0, 1]
**Assert:** eq(d₁, d₂) = false

## TC-013: proper prefix gives strict order
**Property:** TA5(a) (T1 case ii — prefix)
**Given:** n = [1]; u₁ = [1, 0, 1]
**Assert:** lt(n, u₁) = true

## TC-014: position-wise difference gives strict order
**Property:** TA5(a) (T1 case i — position-wise)
**Given:** u₁ = [1, 0, 1]; u₂ = [1, 0, 2]
**Assert:** lt(u₁, u₂) = true

## TC-015: ordering extends to children
**Property:** TA5(a) (extension ordering)
**Given:** d₁ = [1, 0, 1, 0, 1]; d₂ = [1, 0, 2, 0, 1]
**Assert:** lt(d₁, d₂) = true

## TC-016: same-length differing addresses are non-nested
**Property:** T10 (non-nesting)
**Given:** u₁ = [1, 0, 1]; u₂ = [1, 0, 2]
**Assert:** is_prefix(u₁, u₂) = false

## TC-017: inc with k=0 yields strictly greater sibling
**Property:** T9 (monotone stream)
**Given:** d₁ = [1, 0, 1, 0, 1]
**Assert:** inc(d₁, 0) = [1, 0, 1, 0, 2]

## TC-018: T4 permits k=2 at the boundary (zeros = 2)
**Property:** TA5 T4 preservation (zeros = 2 → k=2 allowed)
**Given:** d₁ = [1, 0, 1, 0, 1]
**Assert:** inc_valid(d₁, 2) = true

## Skipped
- T10 (general): "all u₁-outputs ≠ all u₂-outputs" requires universal quantification over all future allocations; the specific instance is TC-012
- T10a: inc(·,0) vs inc(·,2) variant selection — describes algorithm behavior, not a result of calling a named operation on specific values
- T6(a): d₁ and d₂ share node field [1] — structural interpretation; no named field() operation invoked in the example
- T6(b): d₁ user=[1], d₂ user=[2] — same reason as T6(a)