## Question 9 [gregory]

> When INSERT splits an existing POOM bottom crum at the insertion point, does `insertnd` produce exactly two child crums from the original (one for content before, one for content after), or can the split cascade into more fragments?

## KB Synthesis

The split produces exactly **two** fragments from the original bottom crum, with no further fragmentation of that crum.

## Mechanism

When INSERT at position `v` encounters a bottom crum whose range `[grasp, reach)` straddles the insertion point (`whereoncrum` returns `THRUME`), `makegappm` constructs a **two-blade knife** [SS-TWO-BLADE-KNIFE]:

- `blade[0]` = insertion V-position `v`
- `blade[1]` = next subspace boundary `(N+1).1`

`slicecbcpm` is invoked for `blade[0]` only when `grasp < v < reach` (strictly interior). It cuts the crum into **exactly two pieces**: `[grasp, v)` and `[v, reach)`. A third, separate crum is then allocated for the inserted content `[v, v+width)`. [ST-INSERT / Finding 0062]

The concrete example from the KB confirms this count:

```
INSERT "X" at 1.3 into crum₁ [1.1, 1.6):
  crum₁ → [crum₂: 1.1..1.3, crum₃: 1.4..1.6]   (two fragments)
  new crum₄: [1.3..1.4) for "X"                  (the insert content)
  crums = 3  (Δ = +2)
```

## Why Only Two Fragments

`blade[1]` is placed at the **next subspace boundary**, not within the current crum. Since a well-formed bottom crum cannot span across subspace boundaries (that would violate [INV-SUBSPACE-CONVENTION]), `blade[1]` never falls interior to the same crum that `blade[0]` is cutting. Each blade independently calls `slicecbcpm` only when `THRUME` — and a single crum can satisfy `THRUME` for at most one blade. [SS-TWO-BLADE-KNIFE / Finding 0054, PRE-DELETE / Finding 0075]

## B-tree Structural Splits Are Separate

Parent-level B-tree splits (`splitcrumupwards`) **can** cascade upward through internal nodes when a parent accumulates too many children after receiving the two new bottom crums. [SS-ENFILADE-TREE / Finding 0060] But this reorganizes internal (upper) nodes — it does not re-fragment the bottom crums. The bottom level always ends with exactly the two pieces from the original plus the new insert crum.

## The Coalescing Exception

If the insertion point equals an existing crum's **reach** (`ONMYRIGHTBORDER`), `makegappm` early-exits without cutting at all. [SS-WHEREONCRUM / Finding 0062] `isanextensionnd` then extends the existing crum in place, producing **zero** new crums (Δ = 0). This is the coalescing path for sequential interior typing. [ST-INSERT / Finding 0062]

---

## Code Exploration

Now I have all the information needed to give a complete, cited answer. Let me synthesize the full execution path.

---

## Answer: Two-Fragment or Three-Fragment Split — Both Are Possible, With the Second a True Cascade

### The Execution Path

For a POOM enfilade, `insertnd` [insertnd.c:51–61] does two distinct phases:

1. **`makegappm`** — cuts existing crums to open a gap in V-space
2. **`doinsertnd`** — inserts the new mapping entry into the gap

The question concerns phase 1 only.

---

### Phase 1: `makegappm` Places Two Knives

```c
/* insertnd.c:144-148 */
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```

`makegappm` always creates **two** knife blades — not one:

- **`blades[0]`** = the insertion point in V-space
- **`blades[1]`** = a derived second address, computed by `findaddressofsecondcutforinsert` [insertnd.c:174–183]:

```c
/* insertnd.c:174-183 */
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut) {
    tumbler zero, intpart;
    tumblerclear(&zero);
    tumblerincrement(position, -1, 1, secondcut);
    beheadtumbler(position, &intpart);
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut);
    tumblerincrement(secondcut, 1, 1, secondcut);
}
```

This produces `blades[1]` as a tumbler address just offset from `blades[0]` — a neighboring fractional address. The function comment says "needs this to give it a place to find intersection of for text is 2.1", implying the second cut is at a sub-integer tumbler address adjacent to the first.

---

### The Cutting Mechanism: `slicecbcpm`

`makecutsnd` → `makecutsdownnd` → `makecutsbackuptohere` reaches the bottom crums. At height 0 [ndcuts.c:77–91]:

```c
/* ndcuts.c:77-91 */
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
            setwisp((typecorecrum*)ptr);
        }
    }
    return(0);
}
```

`slicecbcpm` [ndcuts.c:373–450] always and only produces **exactly two pieces** from one:

```c
/* ndcuts.c:444-448 */
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, (unsigned)widsize(enftype));
movewisp(&newwid, &ptr->cwid);                    /* ptr = left portion */
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype); /* new starts where ptr ends */
move2dinfo(&((type2dcbc *)ptr)->c2dinfo, &((type2dcbc *)new)->c2dinfo);
adopt(new, RIGHTBRO, ptr);                        /* new is inserted as right sibling */
```

`ptr` becomes the left fragment `[A, blade[i])`, `new` becomes the right fragment `[blade[i], B)`, adopted as `ptr`'s right sibling.

---

### The First Cut Alone Gives Two Fragments — But One More Pass Follows

In the bottom-crum loop, for i=0: if `blades[0]` falls THRUME the original crum, `slicecbcpm` runs, splitting it into:
- `ptr` = `[A, blades[0])` (left fragment)
- `new` = `[blades[0], B)` (right sibling)

Then for i=1: the loop checks `ptr` again against `blades[1]`. Since `ptr` now ends at `blades[0]` and `blades[1] > blades[0]`, `whereoncrum(ptr, ..., blades[1], ...)` returns `TOMYRIGHT` — **not** `THRUME`. The second knife does nothing to `ptr`.

`new` (the right fragment `[blades[0], B)`) is NOT revisited in this inner loop — it was just created and adopted, but the `for (i ...)` loop only operates on the fixed `ptr`.

---

### The Cascade: `makecutsnd`'s Outer Loop Applies the Second Knife to `new`

This is the crucial mechanism. Back in `makecutsnd` [ndcuts.c:15–31]:

```c
/* ndcuts.c:22-27 */
makecutsdownnd(fullcrumptr, &offset, knives);
clear(&offset, sizeof(offset));
for (fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr);
     sonsarecut(fullcrumptr, &offset, knives);
     fullcrumptr = findfullcrum((typecorecrum*)fullcrumptr)) {
    clear(&offset, sizeof(offset));
    makecutsdownnd(fullcrumptr, &offset, knives);
}
```

`sonsarecut` [ndcuts.c:359–371] scans all siblings under the intersection node:

```c
/* ndcuts.c:359-371 */
bool sonsarecut(typecuc *ptr, typewid *offset, typeknives *knives) {
    prologuend((typecorecrum*)ptr, offset, &grasp, (typedsp*)NULL);
    for (son = ...; son; son = ...) {
        if (crumiscut(son, &grasp, knives))
            return(TRUE);
    }
    return(FALSE);
}
```

After the first pass, `new` = `[blades[0], B)` is now a son. If `blades[1]` falls strictly inside `[blades[0], B)` — meaning `blades[0] < blades[1] < B` — then `crumiscut` returns TRUE for `new`, and `sonsarecut` returns TRUE.

A **second pass** of `makecutsdownnd` then finds `new` and calls `makecutsbackuptohere(new, ...)`. This time, for i=1, `blades[1]` IS `THRUME` through `new`, and `slicecbcpm` runs again:

- `new` → `[blades[0], blades[1])` (middle fragment)
- `new2` → `[blades[1], B)` (right fragment)

---

### Result: Three Fragments from One Original

When the insertion point falls strictly inside an existing POOM bottom crum and both knives intersect it (i.e., `blades[0]` and `blades[1]` both lie within `[A, B)`):

| Fragment | V-range | Source |
|---|---|---|
| Left piece | `[A, blades[0])` | first `slicecbcpm` pass on original |
| Middle piece | `[blades[0], blades[1])` | second `slicecbcpm` pass on right fragment |
| Right piece | `[blades[1], B)` | right sibling created in second pass |

**The original crum is replaced by three crums, not two.** The cascade is real — it is driven by the outer `sonsarecut` loop in `makecutsnd` re-running `makecutsdownnd` until no sons remain THRUME by any knife.

---

### When Only Two Fragments Result

If `blades[0]` falls THRUME an existing crum but `blades[1]` does **not** (e.g., `blades[1] >= B`), then only the first knife cuts, and exactly two fragments result. This occurs when the original crum's V-range is narrow — wide enough to include the insertion point but not the second cut address.

Similarly, if the insertion is at the exact **left boundary** of a crum (`whereoncrum` returns `ONMYLEFTBORDER`, not `THRUME`), no slicing occurs at all — the crum is simply a candidate for displacement adjustment in `makegappm`'s post-cut shift loop.

---

### The Maximum Fragment Count Per Original Crum

With exactly `nblades = 2` [insertnd.c:146], at most **two** cuts can apply to any single crum, yielding at most **three** fragments. The split does **not** cascade further because:

1. `slicecbcpm` always produces exactly two pieces per call — it is not self-recursive.
2. `makegappm` fixes `knives.nblades = 2` unconditionally — no additional knives are added mid-operation.
3. After three fragments exist (`[A, b0)`, `[b0, b1)`, `[b1, B)`), none of them is THRUME by either knife, so `sonsarecut` returns FALSE and the loop terminates.

The structural tree-rebalancing (`splitcrumupwards` [split.c:16], `levelpush` [genf.c:263]) that may follow is a b-tree overflow response — it reorganizes parent nodes but does NOT further fragment the content-carrying bottom crums.

---

### Summary

> **The split can cascade to produce exactly three fragments from one original crum** when both knife blades (`blades[0]` at the insertion point and `blades[1]` from `findaddressofsecondcutforinsert`) fall inside the original crum's V-range. Each individual `slicecbcpm` call strictly produces two pieces; the cascade comes from the outer `sonsarecut` loop in `makecutsnd` driving a second pass. The maximum is three fragments — the architecture is bounded by `knives.nblades = 2`.
