## Question 10 [gregory]

> In `makegappm`, the V-shift applies `tumbleradd` to every POOM entry at or after the insertion point — does this shift walk the entire tree rightward from the insertion point, or does it exploit the enfilade's displacement-based addressing to apply the shift at an upper crum level without touching every bottom crum?

## KB Synthesis

The KB is explicit on the mechanism but requires synthesizing across several entries.

## Short answer

`makegappm` exploits the 2D enfilade's **displacement-based addressing** to shift entire subtrees by modifying a single ancestor crum's `cdsp.dsas[V]` field — it does **not** walk every bottom crum. This is the core efficiency property of the enfilade.

## Evidence

**Relative displacement encoding** [SS-ENFILADE-TREE, Finding 0066]:

> Children's displacements are stored relative to the root, not as absolute positions. … `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`

When `insertcutsectionnd` applies `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` at `insertnd.c:162`, modifying an upper crum's displacement implicitly shifts the absolute position of every crum in its subtree **without touching the subtree's children**. This is the point of the displacement hierarchy — a single field update propagates through all descendants via the additive traversal formula.

**How the knife interacts with the tree** [SS-TWO-BLADE-KNIFE, SS-WHEREONCRUM, Finding 0062]:

`insertcutsectionnd` classifies each crum it encounters during tree traversal using `whereoncrum()`. When an entire subtree's range falls strictly within `[blade[0], blade[1])` (case 1, THRUME), the shift is applied to that subtree's root crum and the traversal does not descend further into it. Only crums that **straddle** a blade boundary require descent to a lower level — these are the crums where `whereoncrum()` returns `ONMYLEFTBORDER` or `ONMYRIGHTBORDER`, which trigger `slicecbcpm` to split the crum before reclassifying the pieces [PRE-DELETE, Finding 0075, same mechanism applies in the insert cutting path].

**The normalization step** [ST-INSERT, Finding 0066]:

After `makegappm` applies shifts and `insertnd` places the new content, `setwispupwards` recalculates the root's `cdsp` by finding the new minimum displacement across all children and adjusting sibling displacements to remain relative. This is `setwispnd` absorbing the new minimum:

> `setwispnd` finds `mindsp = min(old_root.cdsp, new_position)`, absorbs: `root.cdsp = 0 + 2.1 = 2.1`, child adjusted: `child.cdsp = 2.1 - 2.1 = 0`

This normalization pass visits immediate children of each upper node, not all bottom crums.

## Implication

The shift is O(log N) in the number of crums affected, not O(N). Only crums at tree levels where a knife boundary cuts through a crum's range require descent — crums whose entire subtree falls in one section get the shift applied at their level. The displacement hierarchy propagates the shift downward for free during subsequent reads via the grasp computation `grasp = offset + ptr->cdsp` [SS-WHEREONCRUM, `retrie.c:334-339`].

---

## Code Exploration

Now I have everything needed for a complete answer. Here it is:

---

## Answer

The V-shift in `makegappm` **exploits displacement-based addressing**. It does not walk the entire tree rightward; it modifies only the displacement fields of direct children of the root crum, and the shift propagates to all their descendants implicitly through position accumulation. Here is the full traced evidence.

---

### 1. `newfindintersectionnd` always returns the root

The function that identifies which node to operate on is at `ndinters.c:38-42`:

```c
int newfindintersectionnd(typecuc *fullcrumptr, typeknives *knives, typecuc **ptrptr, typewid *offset)
{
    *ptrptr = fullcrumptr;       // always the root
    clear(offset, sizeof(*offset));
}
```

This is a simplified stub. The original `findintersectionnd` (commented out at `ndinters.c:19-37`) would have descended the tree to find the deepest common ancestor of all nodes spanning the cut. The current implementation unconditionally sets `father = fullcrumptr` (the root). As a result, the shift loop in `makegappm` always operates on the root's direct children.

---

### 2. The shift loop only touches direct children of the root

From `insertnd.c:149-168`:

```c
prologuend((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    i = insertcutsectionnd(ptr, &fgrasp, &knives);
    switch (i) {
      case 0:
      case 2:
        break;
      case -1:      /* THRUME */
        gerror("makegappm can't classify crum\n");
        break;
      case 1:       /* 9-17-87 fix */
        tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
        ivemodified(ptr);
        break;
    }
}
```

The loop iterates over **direct children of `father` (the root)** via `findleftson` / `findrightbro`. There is no recursion, no descent. The number of iterations is bounded by `MAXUCINLOAF = 6` (`enf.h:26`). Only children classified as `case 1` have their `cdsp.dsas[V]` modified — no grandchildren, no bottom crums.

---

### 3. Every crum stores a relative displacement; absolute position is accumulated

From the struct definitions in `enf.h:47-48` (same layout in `typecuc`, `typecorecrum`, `typecbc`):

```c
typewid cwid;   // width in each dimension: range of addresses this crum covers
typedsp cdsp;   // displacement: offset from the parent's context
```

From `prologuend` at `retrie.c:336-338`:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, ...);    // absolute start = parent_grasp + cdsp
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, ...); // absolute end = grasp + cwid
}
```

A bottom crum's absolute V-position is the **sum of all `cdsp.dsas[V]` values along the path from root to leaf** — exactly like a displacement tree or finger tree. When `makegappm` does:

```c
// insertnd.c:162
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

...on an internal (upper-crum) child of the root, **all bottom crums in that child's subtree are implicitly shifted by `width` in V-space**, without any of them being touched. There is no explicit visit to any descendant.

---

### 4. How `insertcutsectionnd` selects which children to shift

Before the loop, `makecutsnd` (`ndcuts.c:15-31`) splits the tree at two knife positions:

```c
// insertnd.c:144-148
movetumbler(&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
knives.dimension = V;
makecutsnd(fullcrumptr, &knives);
```

`blade[0]` is the insertion address; `blade[1]` is a companion point computed from the same address's tumbler structure (designed to provide a clean gap boundary — the comment at `insertnd.c:175` says "for text is 2.1"). After `makecutsnd`, no node spans either cut; each child of the root lies cleanly in one interval.

`insertcutsectionnd` (`edit.c:207-233`) then classifies each child:
- **case 0** — crum is entirely to the left of `blade[0]` → skip (already in place)
- **case 1** — crum starts at or after `blade[0]` but before `blade[1]` → **apply V-shift**
- **case 2** — crum starts at or after `blade[1]` → skip
- **case -1** — crum spans a cut (THRUME) → error

The children that fall in the post-cut interval starting at `blade[0]` receive the shift; their entire subtrees are implicitly moved with them.

---

### 5. The shift logic is the same pattern used for `deletend`

For comparison, `deletend` (`edit.c:31-76`) uses the same blade-and-classify pattern. For delete, `case 2` children (right of the deleted range) have their displacement decremented by `width`:

```c
// edit.c:63
tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

Again: only a small number of upper-level nodes are touched; the shift propagates to bottom crums for free.

---

### Conclusion

The V-shift in `makegappm` is **not** a rightward scan of all bottom crums. It is a constant-width sweep over the direct children of the root (bounded by `MAXUCINLOAF = 6`). For each qualifying child, it modifies only that child's V-displacement (`cdsp.dsas[V]` at `insertnd.c:162`). Because every crum's absolute V-address is computed by accumulating displacements up the tree (`prologuend`, `retrie.c:336`), this single displacement update implicitly shifts the entire subtree beneath that child — which may contain arbitrarily many bottom crums — without visiting any of them.

The one caveat is that `newfindintersectionnd` (`ndinters.c:38-42`) has been simplified to always return the root rather than descending to the deepest common ancestor. The older commented-out version would have found a deeper `father`, which would be a more targeted (but still displacement-based) operation. Even with the simplified version, no bottom crums are ever visited; the O(bottom-crums-to-the-right) walk is entirely avoided in both versions.
