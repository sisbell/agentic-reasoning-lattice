## Question 11 [gregory]

> In `rearrangend`, how does `rearrangecutsectionnd` classify each POOM bottom crum relative to the 3 or 4 cut points — what are the distinct region categories, and which offset is applied to entries in each region?

## KB Synthesis

## `rearrangecutsectionnd` — Region Classification and Offset Application

The KB has detailed coverage of this in [ST-REARRANGE] (Finding 0056).

### Classification Scheme

`rearrangend` first calls `sortknives()` to order cut points ascending, then `makeoffsetsfor3or4cuts()` to compute displacement vectors. `rearrangecutsectionnd` then classifies each POOM bottom crum by its V-position relative to the sorted cuts, assigning it to a numbered section:

**Pivot (3 cuts: `cut0 < cut1 < cut2`)**

| Section | Region | Offset Applied |
|---------|--------|---------------|
| 0 | `v < cut0` (before first cut) | 0 — unchanged |
| 1 | `cut0 ≤ v < cut1` (first region) | `diff[1] = cut2 - cut1` (moves forward by size of region 2) |
| 2 | `cut1 ≤ v < cut2` (second region) | `diff[2] = -(cut1 - cut0)` (moves backward by size of region 1) |
| 3 | `v ≥ cut2` (after last cut) | 0 — unchanged |

**Swap (4 cuts: `cut0 < cut1 < cut2 < cut3`)**

| Section | Region | Offset Applied |
|---------|--------|---------------|
| 0 | `v < cut0` | 0 — unchanged |
| 1 | `cut0 ≤ v < cut1` (first swap region) | `diff[1] = cut2 - cut0` (moves to where region 3 was) |
| 2 | `cut1 ≤ v < cut2` (middle) | `diff[2] = (cut3 - cut2) - (cut1 - cut0)` (shifts by size difference of swapped regions) |
| 3 | `cut2 ≤ v < cut3` (second swap region) | `diff[3] = -(cut2 - cut0)` (moves to where region 1 was) |
| 4 | `v ≥ cut3` | 0 — unchanged |

### Offset Application

The offset is applied unconditionally via `tumbleradd` on the V-dimension displacement only:

```c
tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])
```

Only `cdsp.dsas[V]` is modified — I-addresses are never touched [INV-REARRANGE-IDENTITY].

### Key Properties

- **No subspace guard**: `rearrangecutsectionnd` has no check that the resulting V-position stays within the same subspace digit. Cross-subspace cuts (e.g., spanning `1.x` into `2.x`) produce valid arithmetic but semantically invalid states [PRE-REARRANGE] (Finding 0051), [EC-REARRANGE-CROSS-SUBSPACE].

- **Cut points are in pre-move space**: All classification and offset computation references only the original (pre-operation) V-positions. There is no iterative re-classification [ST-REARRANGE] (Finding 0056).

- **Exterior regions are frame conditions**: Sections 0 and (3 or 4) — the content before `cut0` and after the final cut — satisfy the frame condition [FC-REARRANGE-EXTERIOR]: their V-positions and I-addresses are unchanged.

- **Empty regions are no-ops**: If `cutN == cutN+1`, no crums fall in that section, so no offsets are applied for it. The offset arithmetic is still computed but has no targets [EC-REARRANGE-EMPTY-REGION].

- **I-addresses preserved throughout**: Because only `cdsp.dsas[V]` is modified, the multiset of I-addresses in the document is identical before and after — the pure V-permutation property [INV-REARRANGE-IDENTITY] (Finding 0056).

---

## Code Exploration

I now have all the data I need. Here is the complete analysis.

---

## How `rearrangecutsectionnd` Classifies POOM Bottom Crums

### 1. Prerequisites: Constants and `whereoncrum`

**`common.h:86-90`** defines the five positional constants:

```
TOMYLEFT        = -2   address strictly left of crum
ONMYLEFTBORDER  = -1   address exactly at crum's left edge
THRUME          =  0   address strictly inside crum
ONMYRIGHTBORDER =  1   address exactly at crum's right edge
TOMYRIGHT       =  2   address strictly right of crum
```

**`retrie.c:345-398`** — `whereoncrum` for POOM/SPAN computes the crum's absolute interval in dimension `index` as:

```c
left  = offset->dsas[index] + ptr->cdsp.dsas[index]
right = left + ptr->cwid.dsas[index]
```

and returns where `address` (a blade tumbler) falls relative to `[left, right)`. The critical threshold in the classifier is `cmp <= ONMYLEFTBORDER`, which fires when `address ≤ left` (blade is at or before the crum's start).

---

### 2. The Classifier: `rearrangecutsectionnd`

**`edit.c:191-204`**:

```c
INT rearrangecutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
  INT i, cmp;

    for (i = knives->nblades -1; i >= 0 ; --i) {
        cmp = whereoncrum (ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME) {
            return (-1);
        } else if (cmp <= ONMYLEFTBORDER) {
            return (i+1);
        }
    }
    return (0);
}
```

**Algorithm:** Scan blades right-to-left (highest index first). For each blade `i`:

- `THRUME` → blade falls **strictly inside** the crum → return `-1` (error; impossible after `makecutsnd` has split the tree at all blades)
- `cmp <= ONMYLEFTBORDER` → blade `i` is **at or to the left** of the crum's start → return `i+1`
- Otherwise (`ONMYRIGHTBORDER` or `TOMYRIGHT`) → blade is to the crum's right; keep scanning leftward

If no blade satisfies the condition, return `0`.

The blades are sorted ascending before this call (`sortknives`, **`edit.c:250-263`**), so scanning from the highest index finds the **rightmost blade that is ≤ the crum's left edge**. The region number is that blade's index plus one.

---

### 3. The Five Regions

With `N` blades sorted `B[0] ≤ B[1] ≤ … ≤ B[N-1]`, `rearrangecutsectionnd` partitions every bottom crum into regions 0 through N:

| Return | Name | Condition on crum's left edge `L` | Position |
|--------|------|------------------------------------|----------|
| `0`   | Before all blades | `L < B[0]` | Crum entirely left of first cut |
| `1`   | Region 1 | `B[0] ≤ L < B[1]` | Crum starts at or after B[0] but before B[1] |
| `2`   | Region 2 | `B[1] ≤ L < B[2]` | Crum starts at or after B[1] but before B[2] |
| `3`   | Region 3 | `B[2] ≤ L < B[3]` (4-cut only) | Crum starts at or after B[2] but before B[3] |
| `4`   | After all blades | `B[3] ≤ L` (4-cut only) | Crum entirely right of last cut |

The boundary rule: a crum whose left edge **coincides with** blade `i` (i.e., `ONMYLEFTBORDER`) is classified into region `i+1` — it belongs to the region **to the right** of that blade.

For 3-cut calls, the maximum region is 3. For 4-cut calls, the maximum is 4.

---

### 4. Dispatch and Offset Application in `rearrangend`

**`edit.c:113-136`** applies the classification:

```c
for (ptr = (typecuc*)findleftson(father); ptr; ptr = ...) {
    i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
    switch (i) {
      case -1:
          gerror ("rearrangend can't classify crum\n");
      case 0:  case 4: /* these never move */
          break;
      case 1:  case 2:  case 3: /* 3 only moves in 4 cuts */
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
    }
}
```

- Regions `0` and `4` → **stationary**: no offset applied, crum stays put
- Regions `1`, `2`, `3` → **displaced**: `diff[region]` is added to `ptr->cdsp.dsas[index]`

The comment "3 only moves in 4 cuts" is technically accurate because `diff[3] = 0` in the 3-cut case (see below), making the add a no-op.

---

### 5. The Offset Values: `makeoffsetsfor3or4cuts`

**`edit.c:164-184`** — `diff[0]` is unused (no region 0 displacement). `diff[1..3]` vary by arity:

#### 3-cut case (`edit.c:177-181`)

```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);  // diff[1] = B[2] - B[1]
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]);  // diff[2] = B[1] - B[0]
diff[2].sign = !diff[2].sign;                                    // diff[2] = -(B[1]-B[0]) = B[0]-B[1]
tumblerclear (&(diff[3]));                                       // diff[3] = 0
```

(`tumblersub(a, b, c)` computes `c = a − b`, confirmed at **`tumble.c:406-429`** where the general path negates `b` and calls `tumbleradd`.)

| Region | Offset | Meaning |
|--------|--------|---------|
| 0 | — | Stationary |
| 1 | `B[2] - B[1]` | Forward shift: source content jumps to destination |
| 2 | `B[0] - B[1]` (negative) | Backward shift: the gap between source-end and destination closes |
| 3 | `0` | No-op (region 3 = after destination, nothing moves) |

This implements a **copy/move**: [B[0], B[1]) is the source span, B[2] is the insertion point. The source content (region 1) slides forward to the destination; material between source and destination (region 2) slides backward by the source width to close the hole.

#### 4-cut case (`edit.c:169-176`)

```c
tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));  // diff[1] = B[2] - B[0]
tumblersub (&knives->blades[1], &knives->blades[0], &a);           // a = B[1] - B[0]
tumblersub (&knives->blades[3], &knives->blades[2], &b);           // b = B[3] - B[2]
tumblersub (&b, &a, &(diff[2]));                                   // diff[2] = (B[3]-B[2]) - (B[1]-B[0])
movetumbler (&diff[1], &diff[3]);                                  // diff[3] = B[2] - B[0]
diff[3].sign = !diff[1].sign;                                      // diff[3] = -(B[2]-B[0]) = B[0]-B[2]
```

| Region | Offset | Meaning |
|--------|--------|---------|
| 0 | — | Stationary |
| 1 | `B[2] - B[0]` (positive) | First span slides right to where second span was |
| 2 | `(B[3]-B[2]) - (B[1]-B[0])` | Gap between spans adjusts for size difference |
| 3 | `B[0] - B[2]` (negative) | Second span slides left to where first span was |
| 4 | — | Stationary |

This implements a **transposition**: [B[0],B[1]) and [B[2],B[3]) are two non-overlapping spans; region 1 and region 3 swap positions, and the intervening gap (region 2) adjusts by the difference in their widths.

---

### 6. Entry Point Context

`rearrangend` is the POOM-level worker called from `rearrangepm` (**`orglinks.c:137-142`**), which is invoked by `dorearrange` (**`do1.c:34-43`**). The `cutseqptr` argument carries the 3 or 4 blade tumblers describing the rearrangement; `index = V` (the V dimension of the POOM). The call to `makecutsnd` (**`edit.c:110`**) splits the enfilade at each blade before classification, guaranteeing that no blade ever lands `THRUME` inside a leaf crum during the sweep — any `-1` return is a fatal error.
