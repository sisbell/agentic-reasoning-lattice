## Question 17 [gregory]

> When inserting into a document that has entries in both text subspace (1.x) and link subspace (2.x internally), does `insertnd` traverse the entire POOM tree including link-subspace crums during the shift pass, classifying each as case 0/1/2, or does the two-blade mechanism prune the traversal so link-subspace nodes are never visited?

## KB Synthesis

## Traversal Depth vs. Classification

The KB directly addresses this, though it distinguishes two separate levels.

### What the KB does confirm: classification, not pruning

**[FC-SUBSPACE]** (Finding 0054) is the most precise source. For INSERT at `1.x` with blades `[1.x, 2.1)`:

> "For a link crum at `2.1` with `blade[1] = 2.1`, `whereoncrum` returns `ONMYLEFTBORDER` (-1). Since `cmp <= ONMYLEFTBORDER`, the crum is classified as **case 2** (no shift) and the `blade[0]` check is never reached."

The phrasing — that `whereoncrum` is called on the link crum and produces a specific classification — indicates the link-subspace crum **is visited** during `insertcutsectionnd`, not pruned before reaching it. The subspace isolation guarantee comes from the classification result, not from a pre-traversal skip.

**[SS-TWO-BLADE-KNIFE]** (Finding 0054) confirms that `insertcutsectionnd` has a three-case structure driven by the two blades, with case 2 (`>= blade[1]`) being the "no shift" path. The structural guarantee is: link crums encounter case 2 and are left untouched.

### What the KB does not confirm: B-tree subtree pruning

**[INV-ENFILADE-RELATIVE-ADDRESSING]** (Finding 0066) establishes that each POOM internal node carries a bounding box (`cdsp` = minimum V-address, `cwid` = extent). This structure *could* support pruning entire subtrees whose bounding box lies entirely at `>= blade[1]` — the internal node's displacement would indicate all children are in the link subspace. However, the KB does not document `makegappm`/`insertcutsectionnd` using this optimization. The retrieval path (`findcbcinarea2d` from **[SS-CONTEXT-LIST]**, Finding 0078) explicitly uses bounding boxes to prune descent, but the gap-making path is a different code path with different semantics.

### Summary

The KB supports this conclusion: **link-subspace crums are visited and classified as case 2 (no shift)** via the `whereoncrum` check against `blade[1]`. The subspace isolation invariant in **[FC-SUBSPACE]** is guaranteed by the knife classification mechanism, not by traversal pruning. Whether the 2D bounding boxes allow entire link-subtrees to be skipped before reaching individual leaf crums is not documented in the KB — you would need to read `insertcutsectionnd`/`makegappm` directly to confirm whether that optimization is present.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Answer: The shift pass visits link-subspace nodes but classifies them as case 2 (no-op). The two-blade mechanism does not prune them.

### Execution path

**Entry: `insertnd` [insertnd.c:51-61]**

For a POOM enfilade, `insertnd` dispatches to `makegappm` before calling `doinsertnd`:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);  // insertnd.c:54
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

---

**`makegappm` [insertnd.c:124-172] — the shift pass**

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);         // insertnd.c:144
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);  // insertnd.c:145
knives.nblades = 2;
knives.dimension = V;                                       // insertnd.c:147
```

Both blades are in the **V dimension**, and both are computed from `origin->dsas[V]` — a position in the text subspace (1.x range). `findaddressofsecondcutforinsert` [insertnd.c:174-183] computes a ghost cut nearby within the same 1.x subspace. Neither blade ever touches the link subspace (2.x range).

After slicing the tree with `makecutsnd`, the intersection node is found:

```c
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // insertnd.c:149
```

**`newfindintersectionnd` [ndinters.c:38-42] is a stub:**

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives,
                          typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;          // always returns the fullcrum
    clear (offset,sizeof(*offset)); // zero offset
}
```

The old descent-based `findintersectionnd` (which would have walked down the tree to find a minimal containing node) is entirely commented out [ndinters.c:18-37]. The new version unconditionally sets `father = fullcrumptr` with zero offset. **There is no subspace-aware pruning here.**

---

**The shift-pass loop [insertnd.c:151-169]**

With `father = fullcrumptr` and `foffset = 0`, `fgrasp = {0,0}` (the fullcrum always has zero displacement). The loop iterates over **every direct child** of the fullcrum:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    i=insertcutsectionnd(ptr,&fgrasp,&knives);
    switch (i) {
      case 0:
      case 2:
            break;
      case -1:      /* THRUME*/
            gerror ("makegappm can't classify crum\n");
      case 1:
            tumbleradd(&ptr->cdsp.dsas[V],&width->dsas[V],&ptr->cdsp.dsas[V]);
            ivemodified (ptr);
            break;
    }
}
```

This visits all top-level children — including any link-subspace UCCs.

---

**`insertcutsectionnd` [edit.c:207-233] — classification**

```c
INT insertcutsectionnd(typecorecrum *ptr, typewid *offset, typeknives *knives)
{
    if (knives->nblades == 2) {
        i = 1;
        cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
        if (cmp == THRUME)          return (-1);
        else if (cmp <= ONMYLEFTBORDER)  return (2);
    }
    i = 0;
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp == THRUME)              return (-1);
    else if (cmp <= ONMYLEFTBORDER) return (1);
    return (0);
}
```

**`whereoncrum` [retrie.c:345-398]** for POOM uses `index == V`:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    cmp = tumblercmp(address, &left);
    if (cmp == LESS)  return (TOMYLEFT);
    ...
```

---

**Constants [common.h:86-90]:**

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER  1
#define TOMYRIGHT        2
```

---

### What happens for a link-subspace node

A link-subspace upper crum has `ptr->cdsp.dsas[V]` in the 2.x range. Both knives are in 1.x.

Inside `whereoncrum`, with `offset = {0,0}` (fgrasp is zero):

```
left = 0 + ptr->cdsp.dsas[V] = 2.x
address = blades[1]           = 1.x
tumblercmp(1.x, 2.x) → LESS      [tumble.c:87-111, abscmp: mantissa[0] 1 < 2]
→ returns TOMYLEFT (-2)
```

Back in `insertcutsectionnd`:

```
cmp = TOMYLEFT = -2
cmp == THRUME?            -2 == 0 → FALSE
cmp <= ONMYLEFTBORDER?    -2 <= -1 → TRUE  → return 2
```

**Every link-subspace child of the fullcrum returns case 2.** In the switch: `case 2: break` — no modification.

---

### Conclusion

The two-blade mechanism does **not** prune link-subspace nodes from the traversal. `newfindintersectionnd` [ndinters.c:38-42] is a no-op stub that always sets the intersection to the fullcrum; the old descent-based pruner is commented out. The shift loop [insertnd.c:151] therefore visits every direct child of the fullcrum, regardless of subspace.

For link-subspace children (V coords in 2.x): the insert-point blades (1.x) fall `TOMYLEFT` of those crums; `insertcutsectionnd` returns case 2, which is identical in effect to case 0 — the `switch` hits `break` with no V-displacement change.

The blades provide **classification correctness** — link crums correctly receive no shift — but they provide **no traversal pruning**. A document with many link-subspace entries at the top level of the POOM will still have all of them visited on every text insertion; each is merely classified as a no-op after evaluating `whereoncrum` once (checking blade[1] only, since that returns case 2 immediately without reaching the blade[0] check).
