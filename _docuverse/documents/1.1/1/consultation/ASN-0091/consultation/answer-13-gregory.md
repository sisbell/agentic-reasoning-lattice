## Question 13 [gregory]

> In `makeoffsetsfor3or4cuts`, how are the tumbler offsets for each region derived from the cut positions — is it pure arithmetic on the cut-point differences, and does the computation use `tumblersub`/`tumbleradd` or a different mechanism?

## KB Synthesis

Yes, the computation is pure arithmetic on cut-point differences, and it uses `tumblersub`/`tumbleradd` throughout. The full picture from the KB:

## Offset derivation: `makeoffsetsfor3or4cuts`

The function takes only `knives->blades[]` as input — no content, no enfilade state. It computes a displacement tumbler `diff[i]` for each region purely from cut-position arithmetic [ST-REARRANGE, Finding 0056].

**Pivot (3 cuts), `cut0 < cut1 < cut2`:**
- `diff[1] = cut2 - cut1` (region 1 shifts forward by the size of region 2)
- `diff[2] = -(cut1 - cut0)` (region 2 shifts backward by the size of region 1)

**Swap (4 cuts), `cut0 < cut1 < cut2 < cut3`:**
- `diff[1] = cut2 - cut0`
- `diff[2] = (cut3 - cut2) - (cut1 - cut0)` (middle shifts by the size difference)
- `diff[3] = -(cut2 - cut0)`

The subtracted quantities (`cut2 - cut1`, etc.) are computed via `tumblersub`. Negative offsets like `-(cut1 - cut0)` are produced using the sign-magnitude mechanism: `tumblersub(a, b)` where `b > a` sets `sign=1` on the result, yielding a valid negative tumbler rather than underflow [SS-TUMBLER, Finding 0053].

The offsets are then applied by `rearrangend` via `tumbleradd(&ptr->cdsp.dsas[V], &diff[i], &ptr->cdsp.dsas[V])` — the V-address component of each matching POOM crum is updated in place, I-addresses untouched [ST-REARRANGE, Finding 0056, code ref `edit.c:125`].

**One pre-processing step:** `sortknives()` normalizes the cuts to ascending order before `makeoffsetsfor3or4cuts` runs, so misordered input is silently accepted [PRE-REARRANGE, Finding 0056]. All cut-point references are in the pre-move address space; there is no reference to post-move state anywhere in the computation.

---

## Code Exploration

Now I have everything needed. Here is the full analysis.

---

## `makeoffsetsfor3or4cuts`: Complete Analysis

### Function Location

`backend/edit.c:164–184`

```c
/* Prepares offsets for both 3 and 4 cut rearranges */

int makeoffsetsfor3or4cuts(typeknives *knives, tumbler diff[])
{
  tumbler a, b;

	/* diff[0] is simply ignored */
	if (knives->nblades == 4) {
		tumblersub (&knives->blades[2], &knives->blades[0], &(diff[1]));
		tumblersub (&knives->blades[1], &knives->blades[0], &a);
		tumblersub (&knives->blades[3], &knives->blades[2], &b);
		tumblersub (&b, &a, &(diff[2]));
/*		tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*//* should be <0 */
		movetumbler (&diff[1], &diff[3]);
		diff[3].sign = !diff[1].sign;
	} else if (knives->nblades == 3) {
		tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
		tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); /* should be negative */
		diff[2].sign = !diff[2].sign;
		tumblerclear (&(diff[3]));
	} else
		gerror ("Wrong number of cuts.");
}
```

### Context: What `diff[]` Is For

The caller is `rearrangend` [`edit.c:78`]. After computing the cuts and classifying each crum into a numbered section (0–4), it applies the offset:

```c
// edit.c:125
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
```

So `diff[i]` is the signed displacement to add to every crum's stored address offset (`dsas`) in region `i`. Region 0 and (in 4-cut) region 4 never move — they are short-circuited before this line. `diff[0]` is explicitly ignored [`edit.c:168`].

The blades array is sorted ascending by `sortknives` before `makeoffsetsfor3or4cuts` is called [`edit.c:107`]. Denote the sorted cuts as **C0 < C1 < C2 < C3**.

---

### 4-Cut Case (`nblades == 4`)

```c
tumblersub(&blades[2], &blades[0], &diff[1]);   // diff[1] = C2 - C0
tumblersub(&blades[1], &blades[0], &a);          // a      = C1 - C0  (width of region 1)
tumblersub(&blades[3], &blades[2], &b);          // b      = C3 - C2  (width of region 3)
tumblersub(&b, &a, &diff[2]);                    // diff[2] = b - a = (C3-C2) - (C1-C0)
movetumbler(&diff[1], &diff[3]);                 // diff[3] = copy of diff[1]
diff[3].sign = !diff[1].sign;                    // diff[3] = -(C2 - C0)
```

| Region | Shift applied | Expression |
|--------|--------------|------------|
| 1 (`[C0,C1)`) | `+diff[1]` | `+(C2 − C0)` |
| 2 (`[C1,C2)`) | `+diff[2]` | `+(C3−C2) − (C1−C0)` = width(region 3) − width(region 1) |
| 3 (`[C2,C3)`) | `+diff[3]` | `−(C2 − C0)` |

**Semantic result:** Region 1 jumps forward by `C2−C0` (the combined span of itself and region 2), landing at position `C2`. Region 3 jumps backward by the same `C2−C0`, landing at `C0`. Region 2 shifts by the width difference between the two swapped outer regions. This is a transposition: regions 1 and 3 swap positions in address space, with region 2 adjusting to remain between them.

**Note on the commented-out line** [`edit.c:174`]:
```c
/*  tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3])); */ /* should be <0 */
```
The original approach computed `diff[3] = C0 − C2` (which is naturally negative). The current code replaces this with a copy-and-sign-flip: `movetumbler(&diff[1], &diff[3]); diff[3].sign = !diff[1].sign;`. Both produce `-(C2−C0)`, but the current version avoids a redundant subtraction.

---

### 3-Cut Case (`nblades == 3`)

```c
tumblersub(&blades[2], &blades[1], &diff[1]);    // diff[1] = C2 - C1  (width of region 2)
tumblersub(&blades[1], &blades[0], &diff[2]);    // diff[2] = C1 - C0  (width of region 1)
diff[2].sign = !diff[2].sign;                    // diff[2] = -(C1 - C0)  [comment: "should be negative"]
tumblerclear(&diff[3]);                          // diff[3] = 0 (unused)
```

| Region | Shift applied | Expression |
|--------|--------------|------------|
| 1 (`[C0,C1)`) | `+diff[1]` | `+(C2 − C1)` = width of region 2 |
| 2 (`[C1,C2)`) | `+diff[2]` | `−(C1 − C0)` = −width of region 1 |
| 3 (unused)    | `+0`       | no movement |

**Semantic result:** Region 1 steps forward by the width of region 2; region 2 steps backward by the width of region 1. Their positions swap. This is a two-block cut-and-paste.

---

### How `tumblersub` Works

`tumblersub(a, b, c)` at `backend/tumble.c:406` computes `c = a − b`:

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler(bptr))
        movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr))
        tumblerclear(cptr);
    else if (iszerotumbler(aptr)) {
        movetumbler(bptr, cptr);
        cptr->sign = !cptr->sign;
    } else {
        movetumbler(bptr, &temp);
        temp.sign = !temp.sign;   // negate b
        tumbleradd(aptr, &temp, cptr);  // then add
    }
    tumblerjustify(cptr);
}
```

It implements subtraction by **negating `b` (flipping its `.sign` flag) and calling `tumbleradd`**. `tumbleradd` (`tumble.c:365`) then dispatches to `absadd`, `strongsub`, or `weaksub` depending on whether the signs match.

So the chain is: `tumblersub` → negate sign → `tumbleradd` → (`absadd` | `strongsub` | `weaksub`). The subtraction in `makeoffsetsfor3or4cuts` always resolves to differences of sorted cut positions, so inputs to `tumblersub` are always non-negative tumblers with the larger value first — meaning `tumbleradd` always routes through `absadd` or `strongsub`, never `weaksub`.

---

### The Direct Sign Flip (Not `tumblersub`)

For `diff[3]` in the 4-cut branch and `diff[2]` in the 3-cut branch, negation is accomplished by **directly flipping `.sign`**, not by calling `tumblersub`:

```c
// 4-cut:
diff[3].sign = !diff[1].sign;    // edit.c:176

// 3-cut:
diff[2].sign = !diff[2].sign;    // edit.c:180
```

This is cheaper than a subtraction call. It relies on the fact that the magnitude is already correct and only the direction needs flipping. `tumblerclear` is never called to zero a diff before use in the signed arithmetic — the sign bit is simply toggled in-place on an already-computed result.

---

### Summary

Yes, the computation is **pure arithmetic on cut-point differences**, exclusively using `tumblersub` (which internally delegates to `tumbleradd`). `tumbleradd` does not appear directly in `makeoffsetsfor3or4cuts` — all arithmetic enters through `tumblersub`. Negation of already-computed results is done by **direct `.sign` bit toggling** (`!diff[i].sign`), not by calling `tumblersub` again. The offsets are derived from three geometric quantities: the span between the outer cut pair (`C2−C0`), and the individual widths of the two outer regions (`C1−C0`, `C3−C2`), combined to produce signed displacements that swap the outer regions while adjusting the middle.
