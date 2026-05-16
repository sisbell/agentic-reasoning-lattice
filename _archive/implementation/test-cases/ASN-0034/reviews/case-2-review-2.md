```
VERDICT: REVISE

### T3 (canonical representation): missing test case for v
TC-006 through TC-009 cover x₁–x₄ satisfying T3, but the worked example states "all five are distinct canonical tumblers." v is not tested for T3, leaving the property incompletely covered.

**Fix:** Add TC-010:
**Property:** T3 (canonical representation)
**Given:** addr = [1, 0, 3, 0, 2, 0, 1, 5]
**Assert:** t3(addr) == Valid
```

TC-001 through TC-009 are otherwise correct — all values match the worked example exactly, and TC-002 through TC-005 correctly cover the three structural failure modes enumerated under T4.