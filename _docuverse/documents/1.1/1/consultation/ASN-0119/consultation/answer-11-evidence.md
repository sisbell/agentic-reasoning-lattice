## Question 11 [evidence]

> In a 4-cut swap REARRANGE exchanging regions `[a,b)` and `[c,d)`, does `makeoffsetsfor3or4cuts` compute the offset for the intervening region `[b,c)` as pure tumbler arithmetic, and what net V-displacement does that middle region receive?

## KB Synthesis

Yes, pure tumbler arithmetic. From the concrete example in `edit.c:164-183`, `makeoffsetsfor3or4cuts` computes all four offsets directly from `knives->blades[]` with no special-case logic.

**Offsets for 4-cut swap at `cut0 < cut1 < cut2 < cut3`:**

| Region | Range | Offset (diff[i]) |
|--------|-------|-----------------|
| 1 | `[cut0, cut1)` | `cut2 - cut0` |
| 2 (middle) | `[cut1, cut2)` | `(cut3 - cut2) - (cut1 - cut0)` |
| 3 | `[cut2, cut3)` | `-(cut2 - cut0)` |

The middle region `[b,c)` = region 2 receives `diff[2] = |right_region| - |left_region|`, the difference in sizes of the two swapped regions.

**Concrete verification (from [ST-REARRANGE] Finding 0056):**

Cuts at `1.2, 1.4, 1.6, 1.8` (equal-size regions "BC" and "FG"):
- Middle "DE" offset: `(1.8 - 1.6) - (1.4 - 1.2)` = `0.2 - 0.2` = **0**

For unequal regions, say cuts at `1.2, 1.5, 1.7, 1.8` (region1="BCD" width 0.3, region3="G" width 0.1):
- Middle offset: `(1.8 - 1.7) - (1.5 - 1.2)` = `0.1 - 0.3` = **−0.2** (shifts left)

The frame condition [FC-REARRANGE-EXTERIOR] holds: content outside `[cut0, cut3)` receives zero displacement. The identity invariant [INV-REARRANGE-IDENTITY] holds for all three regions: only `cdsp.dsas[V]` is modified via `tumbleradd`, never the I-addresses.

---

## Code Exploration

I now have all the information needed. Here is the complete answer.

---

## `makeoffsetsfor3or4cuts`: Middle Region Offset in a 4-Cut Swap

### Setup: how the 4 blades map to sections

After `sortknives` at `edit.c:107`, `blades[0..3]` are ordered `a < b < c < d`. `rearrangecutsectionnd` (`edit.c:191–203`) scans blades right-to-left and returns `i+1` for the first blade to the left of the crum, giving five sections:

| Return value | Region | Movement |
|---|---|---|
| 0 | before `a` | stays (`case 0` at line 122) |
| 1 | `[a, b)` | `diff[1]` |
| 2 | **`[b, c)`** | **`diff[2]`** |
| 3 | `[c, d)` | `diff[3]` |
| 4 | after `d` | stays (`case 4` at line 122) |

The displacement is applied at `edit.c:125`:
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

---

### Tracing `makeoffsetsfor3or4cuts` for the 4-cut case

Full function at `edit.c:164–184`. For `knives->nblades == 4`:

```c
// edit.c:170
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));
//   diff[1] = c − a
```

```c
// edit.c:171
tumblersub (&knives->blades[1], &knives->blades[0], &a);
//   local a = b − a  (= w₁, width of [a,b))
```

```c
// edit.c:172
tumblersub (&knives->blades[3], &knives->blades[2], &b);
//   local b = d − c  (= w₂, width of [c,d))
```

```c
// edit.c:173
tumblersub (&b, &a, &(diff[2]));
//   diff[2] = (d−c) − (b−a)  =  w₂ − w₁
```

```c
// edit.c:175–176  — NOT arithmetic, direct bit flip
movetumbler (&diff[1], &diff[3]);
diff[3].sign = !diff[1].sign;
//   diff[3] = −(c−a) = a−c  (commented-out line at 174 calls this "should be <0")
```

---

### Is `diff[2]` pure tumbler arithmetic?

**Yes — entirely.** It is computed by three sequential `tumblersub` calls with no sign-bit manipulation, no special-casing, and no direct struct access. `tumblersub` itself (`tumble.c:406–440`) handles the signed result naturally: when the minuend is smaller than the subtrahend, it negates the subtrahend, calls `tumbleradd`, and inherits the sign from the dominant operand. Specifically, when `w₁ > w₂`, the code reaches:

```c
// tumble.c:426–429
movetumbler (bptr, &temp);
temp.sign = !temp.sign;    // negate the second arg
tumbleradd (aptr, &temp, cptr);
```

leaving `cptr->sign == 1` (negative). By contrast, `diff[3]` is *not* pure arithmetic — its sign is set by direct struct field manipulation (`diff[3].sign = !diff[1].sign` at `edit.c:176`).

---

### Net V-displacement for `[b, c)`

```
diff[2]  =  (d − c) − (b − a)  =  w₂ − w₁
```

where `w₁ = b − a` is the width of the first swapped region and `w₂ = d − c` is the width of the second.

Three cases:

| Condition | `diff[2]` | Effect |
|---|---|---|
| `w₁ == w₂` | zero | middle does not move |
| `w₂ > w₁` | positive | middle shifts **forward** by `w₂ − w₁` |
| `w₁ > w₂` | negative (`sign = 1`) | middle shifts **backward** by `w₁ − w₂` |

This is geometrically correct: region 1 `[a,b)` moves forward to fill `[c, c+w₁)` and region 2 `[c,d)` moves backward to fill `[a, a+w₂)`. For the middle `[b,c)` to remain contiguous, it must shift by exactly `w₂ − w₁` — the size imbalance of the two swapped regions.

---

### Summary of all three displacements

| Section | Code line | Formula | Signed? |
|---|---|---|---|
| `[a,b)` | `edit.c:170` | `c − a` | always positive (a < c) |
| **`[b,c)`** | **`edit.c:173`** | **`(d−c) − (b−a)`** | **±, set by `tumblersub`** |
| `[c,d)` | `edit.c:175–176` | `a − c` | always negative, set by bit flip |
