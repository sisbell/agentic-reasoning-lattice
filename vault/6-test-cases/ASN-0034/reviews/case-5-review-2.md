```
VERDICT: REVISE
```

### Missing TC — TA5 T4 preservation: u₁ zeros = 1

The T4 preservation bullet names four explicit checkpoints: n (zeros=0), u₁ (zeros=1), d₁ (zeros=2), and e₁ (zeros=3→blocked). TC-008 covers n, TC-009 covers d₁, TC-011 covers e₁. The u₁ case has no corresponding TC.

**Fix:**
```
## TC-017: T4 permits k=2 when zeros count is one
**Property:** TA5 T4 preservation (zeros = 1)
**Given:** u₁ = [1, 0, 1]
**Assert:** zeros(u₁) = 1
```

---

### TC-011 — asserts precondition, not blocking outcome

The property label claims "T4 blocks k=2 when zeros count exceeds the boundary," but the assert is `zeros(e₁) = 3`. That checks the precondition, not the consequence. A test for blocking must assert that the operation is refused.

**Fix:**
```
**Assert:** inc_valid(e₁, 2) = false
```

(The `zeros(e₁) = 3` check is useful as TC-017's analogue — add it as a separate fixture or fold it into TC-017's companion — but it does not stand in for a blocking test.)