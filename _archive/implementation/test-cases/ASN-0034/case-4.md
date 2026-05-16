# Test Cases — Example 4: TA4 — Partial inverse at the precondition boundary

Source: vault/5-examples/ASN-NNNN/examples-1.md, Example 4

## TC-001: TA4 ordinal round-trip succeeds when preconditions hold
**Property:** TA4 (ordinal case — all preconditions satisfied)
**Given:**
```
o = [2]
w = [3]
```
**Assert:** `subtract(add(o, w), w) == [2]`

---

## TC-002: TA4 round-trip returns intermediate result when zero-prefix violated
**Property:** TA4 (precondition necessity — zero-prefix condition violated)
**Given:**
```
a = [1, 0, 3, 0, 2, 0, 1, 2]
w = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `subtract(add(a, w), w) == [1, 0, 3, 0, 2, 0, 1, 5]`

---

## TC-003: TA2 subtraction precondition holds after addition
**Property:** TA2 (r ≥ w → subtraction well-defined)
**Given:**
```
r = [1, 0, 3, 0, 2, 0, 1, 5]
w = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `compare(r, w) == Greater`

---

## TC-004: TA6 self-subtraction yields zero sentinel
**Property:** TA6 (sentinel)
**Given:**
```
o = [3]
```
**Assert:** `subtract(o, o) == [0]`

---

## TC-005: TA6 zero tumbler strictly less than positive tumbler
**Property:** TA6 (ordering)
**Given:**
```
z = [0]
p = [1, 0, 3, 0, 2, 0, 1, 1]
```
**Assert:** `compare(z, p) == Less`

---

## Skipped
- TA7a: describes structural semantics of ordinal representation (N=1 as context, not operand) — no computable operation to call or result to check