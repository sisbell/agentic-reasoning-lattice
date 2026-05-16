## Question 18 [gregory]

> Can `makeoffsetsfor3or4cuts` produce a negative tumbler offset that, when added to a POOM entry's V-displacement, yields a negative V-position — analogous to the `tumblersub` issue in DELETE?

## KB Synthesis

No. `makeoffsetsfor3or4cuts` can produce negative tumbler offsets, but adding them to valid POOM V-displacements cannot yield a negative V-position — for structural reasons that differ from the DELETE case.

## Why offsets are negative

From [ST-REARRANGE] (Finding 0056), the backward-moving regions receive negative offsets:

- **Pivot**: region 2 (`[cut1, cut2)`) gets `diff[2] = -(cut1 - cut0)`
- **Swap**: region 3 (`[cut2, cut3)`) gets `diff[3] = -(cut2 - cut0)`, and region 2 gets `diff[2] = (cut3-cut2) - (cut1-cut0)` which is negative when the left region is larger

These are applied via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], ...)`, which handles sign-magnitude arithmetic directly — no `strongsub` exponent guard is involved.

## Why negative V-positions cannot result

The key constraint: the displaced entry is always within its region, and the offset magnitude is bounded by the adjacent region's size.

For the pivot case, an entry at V-position `v` in region 2 satisfies `v >= cut1`. Its new position is:

```
v + diff[2] = v - (cut1 - cut0) >= cut1 - (cut1 - cut0) = cut0 > 0
```

For the swap's region 3, entries satisfy `v >= cut2`, and the offset is `-(cut2 - cut0)`:

```
v - (cut2 - cut0) >= cut2 - (cut2 - cut0) = cut0 > 0
```

For swap's region 2 with negative diff, entries satisfy `v >= cut1`, and the worst case is `v = cut1`:

```
cut1 + diff[2] = cut1 + (cut3-cut2) - (cut1-cut0) = cut0 + (cut3-cut2) > 0
```

In all cases, the minimum displaced position equals `cut0`, which is a valid positive V-address. Negative results require `cut0 < 0`, which cannot occur with valid docuverse addresses.

## Contrast with DELETE

DELETE uses `strongsub`, which has an exponent guard: when the deletion width's exponent is less than the entry's displacement exponent, `strongsub` returns the minuend unchanged [SS-TUMBLER] (Finding 0055). This guard protects cross-subspace entries by accident.

REARRANGE uses `tumbleradd` directly — no exponent guard. But rearrange doesn't need one for this purpose: the mathematical structure of the offsets (derived as *differences between cut positions*) ensures the result stays positive. DELETE's problem arose because a fixed-width deletion could underflow an arbitrarily small displacement; rearrange's displacements are always relative to adjacent cuts, so the math is self-bounding.

## Remaining concern: cross-subspace displacement

REARRANGE can still violate the subspace convention ([EC-REARRANGE-CROSS-SUBSPACE], [PRE-REARRANGE] Finding 0051) — moving text into 2.x or links into 1.x — but the displaced V-positions are positive throughout. The `tumbleradd` call in `edit.c:125` has no subspace guard and performs the arithmetic unconditionally, producing valid-but-semantically-wrong positive addresses.

---

## Code Exploration

I now have all the evidence needed. Let me synthesize the complete analysis.

---

## Analysis: Can `makeoffsetsfor3or4cuts` Produce Negative V-Positions?

### Short Answer

**`makeoffsetsfor3or4cuts` intentionally produces negative tumbler offsets, but the mathematical structure of the enfilade bounds prevent them from driving a POOM entry's V-displacement below zero — unlike the DELETE case (Finding 0053).** The structural guarantee holds for valid POOM state; it does not hold if the tree has already been contaminated by the DELETE bug.

---

### 1. What Offsets `makeoffsetsfor3or4cuts` Produces

Full function at `edit.c:164–184`:

```c
int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;
    /* diff[0] is simply ignored */
    if (knives->nblades == 4) {
        tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));       // diff[1] = b2-b0 (+)
        tumblersub (&knives->blades[1], &knives->blades[0], &a);               // a = b1-b0 (+)
        tumblersub (&knives->blades[3], &knives->blades[2], &b);               // b = b3-b2 (+)
        tumblersub (&b, &a, &(diff[2]));                                        // diff[2] = b-a = (b3-b2)-(b1-b0)
/*      tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
        movetumbler (&diff[1], &diff[3]);
        diff[3].sign = !diff[1].sign;                                          // diff[3] = -(b2-b0)
    } else if (knives->nblades == 3) {
        tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);         // diff[1] = b2-b1 (+)
        tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);         /* should be negative */
        diff[2].sign = !diff[2].sign;                                          // diff[2] = -(b1-b0)
        tumblerclear (&(diff[3]));                                             // diff[3] = 0
    } else
        gerror ("Wrong number of cuts.");
}
```

**Negative offsets produced:**

| Case | Offset | Sign | Condition |
|------|--------|------|-----------|
| 3-cut | `diff[2] = -(b1-b0)` | **always negative** | explicit sign flip at `edit.c:180` |
| 4-cut | `diff[3] = -(b2-b0)` | **always negative** | sign flip at `edit.c:176` |
| 4-cut | `diff[2] = (b3-b2)-(b1-b0)` | **negative when region 1 wider than region 3** | depends on cut spacing |

The commented-out line at `edit.c:174` — `/* should be <0 */` — is original author confirmation that signed arithmetic was deliberately used here.

---

### 2. How These Diffs Are Applied

In `rearrangend`, `edit.c:113–135`:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case 0:  case 4: /* these never move */
          break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
    }
}
```

`index` = `V` (`wisp.h:21`) when called via `rearrangepm` at `orglinks.c:139`. The diff is added directly to `ptr->cdsp.dsas[V]` — the V-displacement of the POOM crum — with **no guard against a negative result**.

---

### 3. Section Classification Constrains the Result

`whereoncrum` for a POOM crum (`retrie.c:356`):

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = offset.V + cdsp.V
```

So a crum's absolute V-start is `fgrasp.V + cdsp.V`.

`rearrangecutsectionnd` returns section `i+1` when `blade[i] <= fgrasp.V + cdsp.V` (`edit.c:196–203`). This means a node assigned to **section k** (k = 1, 2, or 3) satisfies:

```
cdsp.V >= b_{k-1} - fgrasp.V
```

Now compute the post-diff minimum:

**3-cut, section 2** (gets `diff[2] = -(b1-b0)`):
```
new_cdsp.V = cdsp.V + diff[2]
           >= (b1 - fgrasp.V) - (b1 - b0)
           = b0 - fgrasp.V
```

**4-cut, section 3** (gets `diff[3] = -(b2-b0)`):
```
new_cdsp.V >= (b2 - fgrasp.V) - (b2 - b0)
           = b0 - fgrasp.V
```

**4-cut, section 2** (gets `diff[2] = (b3-b2)-(b1-b0)`, possibly negative):
```
new_cdsp.V >= (b1 - fgrasp.V) + (b3-b2) - (b1-b0)
           = b3 - b2 + b0 - fgrasp.V
```

In all three cases, the minimum result is `>= b0 - fgrasp.V`.

**The bound holds if and only if `fgrasp.V <= b0`** — i.e., the father's absolute V-start is at or before the smallest cut. This is guaranteed by the enfilade invariant: the "father" returned by `newfindintersectionnd` at `edit.c:111` is the lowest common ancestor of all cut points. Its V-span must contain all blades, so `fgrasp.V <= b0 <= b1 <= b2 (< b3)`. Therefore `b0 - fgrasp.V >= 0`.

**Conclusion**: For a valid POOM, `makeoffsetsfor3or4cuts` cannot drive `cdsp.V` below zero.

---

### 4. The Critical Structural Difference from DELETE

In **DELETE** (`edit.c:63`):
```c
tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```
The `width` subtracted is the deletion span width — a value completely unconstrained relative to `cdsp.V`. A node far to the right of a large deletion will have its cdsp reduced by more than its current value, yielding a negative tumbler (Finding 0053).

In **REARRANGE** (`edit.c:125`):
```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```
The diff for section k is derived from the same cut positions that determine section assignment. The classification lower-bounds `cdsp.V` by exactly enough to absorb the maximum negative diff, leaving the result `>= b0 - fgrasp.V >= 0`.

This is a **self-compensating invariant**: the more negative the diff (wider region 1 compared to region 3), the larger `cdsp.V` must be for the node to be in that section.

---

### 5. Residual Risk: Pre-Contaminated State

The guarantee above depends on **valid POOM state**. If DELETE has already introduced negative V-positions (Finding 0053), those entries sit at `cdsp.V < 0`. Their absolute V-start `fgrasp.V + cdsp.V` is less than `fgrasp.V`, and since all cuts `b0, b1, ... >= fgrasp.V`, `whereoncrum(ptr, fgrasp, b0) == TOMYRIGHT` — the blade is to the right of the crum. The crum falls in **section 0** (never moves). So REARRANGE does **not further damage** already-negative entries, but it also does not repair them.

There is one other subtle risk: if `newfindintersectionnd` returns an incorrect `father` (one whose span doesn't contain all blades), the bound `fgrasp.V <= b0` can be violated. In that case, even REARRANGE could produce a negative displacement. But this would be a separate `ndcuts.c`/`ndinters.c` bug, not a property of `makeoffsetsfor3or4cuts` itself.

---

### Code Citations

| Claim | File:Line |
|-------|-----------|
| `diff[2]` sign-flip (3-cut) | `edit.c:180` |
| `diff[3]` sign-flip (4-cut) | `edit.c:176` |
| Commented `/* should be <0 */` | `edit.c:174` |
| diff applied to `cdsp.dsas[V]` via `tumbleradd` | `edit.c:125` |
| `whereoncrum` computes `left = offset.V + cdsp.V` | `retrie.c:356` |
| `V = 1` constant for POOM | `wisp.h:21` |
| `rearrangepm` calls `rearrangend(…, V)` | `orglinks.c:139` |
| DELETE uses unconstrained `tumblersub` | `edit.c:63` |
| `tumblersub` allows negative results | `tumble.c:424,427` |
| `diff[2] = -(b1-b0)` (3-cut comment "should be negative") | `edit.c:179` |

---

### Summary

Yes, `makeoffsetsfor3or4cuts` **does** produce negative tumbler offsets — this is explicit and intentional (`diff[2]` for 3-cut, `diff[3]` for 4-cut, and conditionally `diff[2]` for 4-cut). These are applied without any post-application guard to `cdsp.dsas[V]`.

However, the mechanism is **not analogous to the DELETE bug** in its outcome. In DELETE, the subtracted `width` is independent of `cdsp.V`, so underflow to negative is possible whenever the deletion span is larger than the node's displacement. In REARRANGE, the negative diff and the minimum `cdsp.V` for section membership are derived from the same cut positions: section assignment guarantees `cdsp.V >= b_{k-1} - fgrasp.V`, and the negative diff for that section is exactly `fgrasp.V - b_{k-1}` in the worst case, making the result `>= 0` whenever the enfilade is in valid state (`fgrasp.V <= b0`).

The only path to a negative V-position via REARRANGE is an already-corrupted POOM (from the DELETE bug) or a malformed `father` from `newfindintersectionnd` — not from `makeoffsetsfor3or4cuts` itself operating on valid state.
