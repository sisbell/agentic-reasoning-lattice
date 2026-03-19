# Test Cases — Example 3: Boundary between strict and weak order preservation under addition

Source: vault/5-examples/{ASN label}/examples-1.md, Example 3

## TC-001: TA0 — deep weight operation is well-defined
**Property:** TA0 (k=8 case)
**Given:**
```
a        = [1, 0, 3, 0, 2, 0, 1, 2]
b        = [1, 0, 3, 0, 2, 0, 1, 5]
w_deep   = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `len(w_deep) <= min(len(a), len(b))` — i.e., `8 <= min(8, 8)`

---

## TC-002: TA0 — shallow weight operation is well-defined
**Property:** TA0 (k=1 case)
**Given:**
```
a          = [1, 0, 3, 0, 2, 0, 1, 2]
b          = [1, 0, 3, 0, 2, 0, 1, 5]
w_shallow  = [3]
```
**Assert:** `len(w_shallow) <= min(len(a), len(b))` — i.e., `1 <= min(8, 8)`

---

## TC-003: TA-strict — deep addition strictly increases a
**Property:** TA-strict (deep weight case)
**Given:**
```
a       = [1, 0, 3, 0, 2, 0, 1, 2]
w_deep  = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `ordLt(a, add(a, w_deep))` — i.e., `[1,0,3,0,2,0,1,2] < [1,0,3,0,2,0,1,5]`

---

## TC-004: TA-strict — shallow addition strictly increases a
**Property:** TA-strict (shallow weight case)
**Given:**
```
a          = [1, 0, 3, 0, 2, 0, 1, 2]
w_shallow  = [3]
```
**Assert:** `ordLt(a, add(a, w_shallow))` — i.e., `[1,0,3,0,2,0,1,2] < [4]`

---

## TC-005: TA1-strict — k = divergence preserves strict order under addition
**Property:** TA1-strict (k ≥ divergence case)
**Given:**
```
a       = [1, 0, 3, 0, 2, 0, 1, 2]
b       = [1, 0, 3, 0, 2, 0, 1, 5]
w_deep  = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `ordLt(add(a, w_deep), add(b, w_deep))` — i.e., `[1,0,3,0,2,0,1,5] < [1,0,3,0,2,0,1,8]`

---

## TC-006: TA1 (weak) — k < divergence satisfies weak order
**Property:** TA1 (weak), shallow weight
**Given:**
```
a          = [1, 0, 3, 0, 2, 0, 1, 2]
b          = [1, 0, 3, 0, 2, 0, 1, 5]
w_shallow  = [3]
```
**Assert:** `ordLe(add(a, w_shallow), add(b, w_shallow))` — i.e., `[4] <= [4]`

---

## TC-007: TA1-strict (negative) — k < divergence collapses strict order to equality
**Property:** TA1-strict (negative), shallow weight
**Given:**
```
a          = [1, 0, 3, 0, 2, 0, 1, 2]
b          = [1, 0, 3, 0, 2, 0, 1, 5]
w_shallow  = [3]
```
**Assert:** `add(a, w_shallow) == add(b, w_shallow)` — i.e., `[4] == [4]`

---

## TC-008: Result-length identity — output length equals weight length (deep)
**Property:** Result-length identity (deep weight)
**Given:**
```
a       = [1, 0, 3, 0, 2, 0, 1, 2]
w_deep  = [0, 0, 0, 0, 0, 0, 0, 3]
```
**Assert:** `len(add(a, w_deep)) == len(w_deep)` — i.e., `8 == 8`

---

## TC-009: Result-length identity — output length equals weight length (shallow)
**Property:** Result-length identity (shallow weight)
**Given:**
```
a          = [1, 0, 3, 0, 2, 0, 1, 2]
w_shallow  = [3]
```
**Assert:** `len(add(a, w_shallow)) == len(w_shallow)` — i.e., `1 == 1`

---

## Skipped
- Tail replacement: describes algorithm behavior ("erases the divergence", "carries no information") — not a computable assertion over specific input/output values; the observable consequence is already captured by TC-007.