## Question 20 [gregory]

> When `deletend` constructs knives via `makecutsbackuptohere` for a DELETE spanning multiple bottom crums, are the intermediate crums (those entirely consumed by the delete range) freed in a single pass through `disownnd`, or does each one require a separate tree traversal to locate and remove?

## KB Synthesis

The KB does not provide enough low-level detail about `deletend`'s internal loop structure to answer definitively, but what it does say strongly implies a **single traversal pass**.

## What the KB establishes

**[ST-DELETE Finding 0075]** describes a two-phase structure:

- **Phase 1** (cutting): `makecutsbackuptohere()` runs only at boundaries where a cut falls strictly interior to a crum (`whereoncrum() == THRUME`). At boundaries that align exactly with crum edges, no cut is made.
- **Phase 2** (classify and remove/shift): each crum encountered during traversal is classified into cases — Case 1 (entirely within deletion range) triggers `disown` + `subtreefree`.

**[ST-DELETE Finding 0064]** confirms the inline case-dispatch model:

> nodes falling entirely within the deletion range are `disown`ed (removed from parent/sibling pointers) and then `subtreefree`d

This language describes per-crum action during traversal, not a collect-then-free two-pass pattern.

**[ST-DELETE Finding 0058]** shows that `setwispupwards` and `recombine` are called **once** on the father node *after* the removal loop — consistent with a single traversal that handles all consumed crums inline, then rebalances.

## Conclusion

The KB supports a **single traversal**: as `deletend` descends and walks the tree, each bottom crum classified as Case 1 (entirely within the deletion range) is immediately `disown`ed and `subtreefree`d as the traversal encounters it. No separate re-traversal per consumed crum is described or implied. After all crums are processed in this single pass, `setwispupwards` and `recombine` restore tree invariants once.

The KB does not contain the actual `deletend` loop code at sufficient granularity to prove this unambiguously — it would require reading `edit.c:31-76` directly. What is documented is consistent with single-pass inline processing; nothing in the findings describes a multi-pass or per-crum separate-traversal pattern.

---

## Code Exploration

---

## Answer: Intermediate Crum Removal in `deletend`

The question has two distinct sub-parts: (1) how `makecutsbackuptohere` constructs the knives, and (2) how intermediate crums are freed. Here is a precise account based on source.

---

### Phase 1: Knife Construction via `makecutsbackuptohere`

`deletend` [edit.c:44] calls `makecutsnd(fullcrumptr, &knives)`:

```c
// edit.c:40-44
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
knives.nblades = 2;
knives.dimension = index;
makecutsnd (fullcrumptr, &knives);
```

`makecutsnd` [ndcuts.c:15-31] calls `makecutsdownnd`, which descends and then calls `makecutsbackuptohere` [ndcuts.c:54]:

```c
// ndcuts.c:33-67
int makecutsdownnd(typecuc *fullcrumptr, typewid *offset, typeknives *knives) {
    ...
    makecutsbackuptohere(ptr, offset, knives);
    if (toomanysons(ptr)) { levelpush(ptr); makecutsnd(...); }
}
```

Inside `makecutsbackuptohere` [ndcuts.c:69-140], **at height == 0** (bottom crums), each knife that passes through (`THRUME`) the crum causes a split:

```c
// ndcuts.c:77-91
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum(...) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
            ivemodified((typecorecrum*)ptr);
            ivemodified((typecorecrum*)new);
        }
    }
    return(0);
}
```

`slicecbcpm` [ndcuts.c:373-450] cuts the bottom crum in two and calls:

```c
// ndcuts.c:448
adopt(new, RIGHTBRO, ptr);
```

So the new half is inserted as a right brother inline — no tree traversal, just a pointer splice. Both knives are processed in **one pass** through the `for (i = 0; i < knives->nblades; i++)` loop at the bottom level.

At height > 0, `makecutsbackuptohere` [ndcuts.c:92-116] calls `cutsons` → `makecutsbackuptohere` recursively downward into children, then may call `peelsoncorrectly` to reorganize. The outer `makecutsnd` loop [ndcuts.c:24-27] re-runs `makecutsdownnd` from the fullcrum until `sonsarecut` returns false.

---

### Phase 2: Finding the "Father"

`deletend` [edit.c:45] calls `newfindintersectionnd`:

```c
// ndinters.c:38-42
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;
    clear (offset, sizeof(*offset));
}
```

**This is a stub.** The old `findintersectionnd` (commented out at ndinters.c:18-37) would have descended the tree to find the narrowest common ancestor of both cut points. The live `new` version unconditionally sets `father = fullcrumptr` — the root. The offset is zeroed. This means the subsequent loop always operates over the **direct children of the root**.

---

### Phase 3: The Deletion Loop — One Pass, Not Per-Crum Tree Traversals

`deletend` [edit.c:47-73]:

```c
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);   // save next BEFORE modifying
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:
        disown ((typecorecrum*)ptr);
        subtreefree ((typecorecrum*)ptr);
        break;
      case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;
    }
}
```

The `deletecutsectionnd` classifier [edit.c:235-248] works by iterating knives right-to-left, returning `i+1` for the first knife to the right of the crum:
- **0**: crum is to the left of knife 0 (before the delete range — left alone)
- **1**: crum is between knife 0 and knife 1 (inside the delete range — deleted)
- **2**: crum is to the right of knife 1 (after the delete range — displacement adjusted)
- **−1**: a knife passes through the crum (shouldn't happen after `makecutsnd` has split all such crums)

The loop makes **one left-to-right pass** through all direct children of `father` (the fullcrum). `next` is saved at [edit.c:48] before the switch, so the sibling chain is not corrupted when an intermediate crum is unlinked.

---

### What `disown` Actually Does

For each case-1 (intermediate) crum, `disown` is called [genf.c:349-371]:

```c
// genf.c:349-371
int disown(typecorecrum *crumptr) {
    typecuc *father;
    if (!(father = weakfindfather(crumptr))) { gerror(...) }
    disownnomodify(crumptr);
    ivemodified((typecorecrum*)father);
}
```

`weakfindfather` [genf.c:120-138]:

```c
typecuc *functionweakfindfather(typecorecrum *ptr) {
    ...
    for (; ptr && !ptr->isleftmost; ptr = ptr->leftbroorfather)
        ;
    if (ptr) {
        return ((typecuc *)ptr->leftbroorfather);
    }
    ...
}
```

This walks **laterally leftward** through the `leftbroorfather` chain until it finds a crum where `isleftmost == TRUE`, then follows one upward pointer. This is **not a tree traversal from the root** — it is a linked-list walk within a single level. Its cost is O(left siblings), bounded by the fan-out of the parent, not by tree depth or size.

`disownnomodify` [genf.c:373-413] then performs pure pointer surgery:

```c
// genf.c:394-411
right = findrightbro(crumptr);
father->numberofsons -= 1;
if (crumptr->isleftmost) {
    father->leftson = right;
    if (right) { right->leftbroorfather = (typecorecrum *)father; right->isleftmost = TRUE; }
} else {
    left = findleftbro(crumptr);
    left->rightbro = right;
    if (right) { right->leftbroorfather = left; }
}
```

After disowning the leftmost crum, `right->isleftmost` is set to `TRUE` and `right->leftbroorfather = father`. This means the next intermediate crum in the iteration becomes the leftmost child, so the next `weakfindfather` call returns `father` in O(1). For non-leftmost intermediates, `weakfindfather` must walk leftward past any surviving case-0 crums, but still never ascending above the father level.

---

### `subtreefree` for Intermediate Crums with Children

`subtreefree` [credel.c:413-432]:

```c
// credel.c:412-432  (comment: "assumes crum is disowned")
void subtreefree(typecorecrum *ptr) {
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);
        }
    } else if (...GRAN/ORGL...) {
        orglfree(...);
    }
    freecrum(ptr);
}
```

For intermediate crums with height > 0, `subtreefree` recurses into the subtree. It uses `p->rightbro` [credel.c:425] to advance — it does **not** restart from the root. Each recursive level does one pass through that crum's children. This recursive descent is within the subtree of the already-located intermediate crum; it is not a new search from the root.

---

### Conclusion

**The intermediate crums are freed in a single linear pass, not via separate tree traversals.**

1. **Knife construction** (`makecutsbackuptohere`): both blades are handled in one descent. Bottom crums are split inline via `slicecbcpm`/`adopt`; no per-blade tree traversal.

2. **Intersection** (`newfindintersectionnd`): the live version is a stub that unconditionally returns `father = fullcrumptr` (the root) [ndinters.c:38-42]. This flattens the problem: the deletion loop always operates at the first level below the root.

3. **Deletion loop** (`deletend` [edit.c:47-73]): one left-to-right sweep through the children of `father`. Intermediate crums (case 1) are removed inline as they are encountered. The loop pre-fetches `next` [edit.c:48] before any modification, so no restart is needed.

4. **`disown`** [genf.c:349-371]: uses `weakfindfather` [genf.c:120-138] which is a **lateral leftward chain walk** to find the parent pointer — not a root-to-leaf tree search. After the leftmost child is disowned, its successor inherits `isleftmost = TRUE`, keeping subsequent `weakfindfather` calls O(1) for the initial crums in the sweep.

5. **`subtreefree`** [credel.c:413-432]: for intermediate crums with height > 0, recursively descends into the subtree. This descent is within the already-located subtree, not a new search from the root. It iterates via `p->rightbro` without restarting.

The design is: `makecutsnd` pre-splits the enfilade so that every intermediate crum at the level below `father` is a clean, whole-crum deletion target; then `deletend`'s loop sweeps once through those children, removing each in place.
