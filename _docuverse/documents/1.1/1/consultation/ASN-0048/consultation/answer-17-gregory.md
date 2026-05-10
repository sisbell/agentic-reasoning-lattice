## Question 17 [gregory]

> After INSERT creates a new granfilade leaf with `MAXBCINLOAF=1`, what determines whether this triggers a `splitcrumupwards` and `levelpush` in the granfilade tree — is it purely the occupancy exceeding 1 in the parent loaf, and how does this interact with the disabled `levelpull`?

## KB Synthesis

## Granfilade Split Mechanics After INSERT

### What triggers `splitcrumupwards`

After INSERT allocates a new granfilade leaf via `insertseq`, it adopts the new height-0 bottom crum as the **right sibling** of the existing bottom crum under the parent height-1 node [SS-DUAL-ENFILADE, Finding 0041]. Immediately after `adopt`, the code calls `splitcrumupwards(father)`.

The trigger condition is purely occupancy: `toomanysons(father)` returns TRUE when `father->numberofsons > MAXBCINLOAF` — that is, `> 1` [SS-GRAN-BOTTOM-SINGLETON, SS-ENFILADE-BRANCHING]. So any height-1 node holding 2 bottom crums immediately satisfies `toomanysons`. Since `MAXBCINLOAF = 1`, this triggers on **every second insert** that lands under the same height-1 node.

### What determines `levelpush` vs. `splitcrum`

`splitcrumupwards` checks `isfullcrum(ptr)` — whether the node is the apex [SS-SPLIT, Finding 0070]:

- **If the height-1 node IS the fullcrum (root):** `levelpush` is called first, incrementing the fullcrum's height from 1→2 and pushing its existing children down one level. Then `splitcrum` splits the now-demoted former root into two height-1 children under the new height-2 fullcrum.
- **If the height-1 node is NOT the fullcrum:** `splitcrum` directly creates a new sibling height-1 node, distributing children between original and sibling. The parent gains one child. This may cascade upward — `splitcrumupwards` loops while `toomanysons` is true.

[SS-ENFILADE-TREE, Finding 0060] documents the exact consequence: inserting the 3rd bottom crum when the tree is at height-2 with two height-1 nodes (each with 1 child) triggers a split at a non-root height-1 node, adding a third child to the fullcrum. Since `MAXUCINLOAF = 6` applies to upper crums, the fullcrum won't itself split until it accumulates 7 children — so height growth is relatively rare.

### The `levelpull` asymmetry

`levelpull` is disabled — it immediately `return(0)` without executing the collapse logic [SS-ENFILADE-TREE, Finding 0058]. This has two concrete consequences:

1. **Tree height is monotonically non-decreasing** [INV-ENFILADE-MINIMALITY]. Every `levelpush` is permanent. A granfilade that grew to height-3 during content insertion will remain height-3 even after delete-everything.

2. **The two "empty document" states are non-equivalent** [EC-EMPTY-DOC, Finding 0058]: a never-filled document (height-1, one zero-width bottom node) differs structurally from a post-delete-all document (height-H, empty intermediate nodes, zero bottom nodes). The latter causes Bug 0019 — INSERT crashes because `firstinsertionnd` expects a bottom crum to exist.

### Summary

The trigger is purely occupancy: `numberofsons > 1` at any height-1 granfilade node, which fires on every second insert into that node. Whether this causes `levelpush` (height growth) depends solely on whether that height-1 node is the current fullcrum. Because `levelpull` is disabled, height growth from `levelpush` is permanent — the granfilade can only grow taller, never shorter, making its height a monotonically non-decreasing value over the document's lifetime [INV-ENFILADE-MINIMALITY].

---

## Code Exploration

I now have all the code needed for a complete, cited answer.

---

## What Determines `splitcrumupwards` and `levelpush` in the GRAN Granfilade Tree

### The Call Chain

Every granfilade insert routes through `insertseq()` in `insert.c`. The two entry points are:
- `inserttextgr` [granf2.c:82] calls `insertseq()` [granf2.c:99]
- `createorglgr` [granf2.c:110] calls `insertseq()` [granf2.c:125]

Inside `insertseq` [insert.c:17], there is a **fast path** that avoids creating a new leaf entirely:

```c
if (info->infotype == GRANTEXT
 && ptr->cinfo.infotype == GRANTEXT
 && ptr->cinfo.granstuff.textstuff.textlength < GRANTEXTLENGTH) {
    if (!fillupcbcseq(ptr, &nextaddress, info)) {   // pack text into existing leaf
        ivemodified((typecorecrum*)ptr);
        return(0);   // ← NO splitcrumupwards on this path
    }
}
```
[insert.c:34–41]

When the existing bottom crum has room (`textlength < GRANTEXTLENGTH`) and the text fits, `fillupcbcseq` packs it in and returns without calling `splitcrumupwards` at all.

---

### When a New Leaf Is Created

If the fast path fails (non-text content like `GRANORGL`, full crum, or text that didn't fit), `insertseq` creates and adopts a new leaf:

```c
new = createcrum(0, (INT)ptr->cenftype);
reserve(new);
adopt(new, RIGHTBRO, (typecorecrum*)ptr);   // ← new sibling added to father
ivemodified(new);
splitsomething = splitcrumupwards(findfather(new));   // ← FIRST CALL [line 48]
...
splitsomething |= splitcrumupwards(findfather(ptr)); // ← SECOND CALL [line 64]
```
[insert.c:43–64]

`splitcrumupwards` is called **twice** — once on the parent of the new leaf, once on the parent of the split point — before `recombine()` is conditionally called [insert.c:67–69].

---

### What `toomanysons` Actually Tests

`splitcrumupwards` [split.c:16] loops on the `toomanysons` predicate [genf.c:239]:

```c
bool toomanysons(typecuc *ptr)
{
    ...
    return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum(...)?MAX2DBCINLOAF:MAXBCINLOAF)));
}
```

The constants [enf.h:26–28]:
```c
#define MAXUCINLOAF     6
#define MAXBCINLOAF     1     /* so text will fit */
#define MAX2DBCINLOAF   4
```

For a GRAN tree (`is2dcrum` returns FALSE for `GRAN` [genf.c:19]):

| Height of node | Threshold | Overflows when |
|---|---|---|
| `height == 1` (direct parent of leaves) | `MAXBCINLOAF = 1` | `numberofsons > 1`, i.e., ≥ 2 leaves |
| `height > 1` (internal nodes, apex) | `MAXUCINLOAF = 6` | `numberofsons > 6`, i.e., ≥ 7 children |

**Yes: occupancy exceeding 1 is the precise test at height 1.** After `adopt(new, RIGHTBRO, ptr)` adds the new leaf, the height-1 parent goes from 1 to 2 sons — immediately triggering `toomanysons`. So every successful new-leaf insertion (that isn't the fill-in-existing-leaf fast path) triggers a height-1 split.

---

### What `splitcrumupwards` Does on Each Overfull Node

```c
bool splitcrumupwards(typecuc *father)
{
    for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
        if (isfullcrum((typecorecrum*)father)) {
            levelpush(father);
            splitcrum((typecuc*)findleftson(father));
            return(TRUE);
        }
        splitcrum(father);   // ← non-apex path
        splitsomething = TRUE;
    }
    return(splitsomething);
}
```
[split.c:26–43]

For GRAN, `splitcrum` dispatches to `splitcrumseq` [split.c:47–48], which creates a right sibling for `father` and migrates `numberofsons/2` children to it [split.c:81–88]. With `MAXBCINLOAF=1`, a 2-child height-1 node splits into two 1-child height-1 nodes, incrementing the parent's `numberofsons` by 1.

The loop **walks up** the tree. At each level it:
1. Calls `splitcrum(father)` if not apex → parent gains one more child
2. Checks parent → if `numberofsons > MAXUCINLOAF=6`, splits parent too
3. Continues until either `toomanysons` is false or it reaches the apex

---

### When `levelpush` Fires

`levelpush` fires **only** when the loop reaches the fullcrum (`isfullcrum` is TRUE) and `toomanysons` is still TRUE there. At the apex, the threshold is still `MAXUCINLOAF=6` (since apex height is always > 1 after the first push). `levelpush` [genf.c:263]:

```c
new = createcrum(fullcrumptr->height, fullcrumptr->cenftype);
new->isleftmost = TRUE;
transferloaf(fullcrumptr, new);       // move all children to new intermediate node
fullcrumptr->height++;                // apex grows by one level
adopt((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);  // new becomes sole child
new->sonorigin = temploafptr;
setwispupwards(new, 1);
```
[genf.c:273–292]

Then `splitcrum(findleftson(father))` immediately splits the now-overfull intermediate node [split.c:29].

**So `levelpush` is NOT triggered by `MAXBCINLOAF=1` directly.** `MAXBCINLOAF=1` determines that height-1 nodes split after every single new-leaf insertion, causing height-2 (and higher) nodes to accumulate children rapidly. `levelpush` fires when the fullcrum's `numberofsons` exceeds `MAXUCINLOAF=6` — which is determined by how many times height-level splits have propagated to the apex.

In a fresh GRAN tree at height 2 (apex directly above height-1 nodes), the progression is:
- Insertions 1–7 each cause a height-1 split → apex gains a height-1 child each time
- When the apex reaches 7 children: `toomanysons` fires at apex → `levelpush` → apex height becomes 3

After `levelpush`, the apex has one intermediate child (height 2) with ≤6 grandchildren, so further insertions must propagate all the way up again before another `levelpush` fires.

---

### The Disabled `levelpull` and Its Effect

`levelpull` [genf.c:318] is completely gutted:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson(fullcrumptr);
    dspadd(&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown(ptr);
    fullcrumptr->height--;
    transferloaf(ptr, fullcrumptr);
    setwispupwards(fullcrumptr, 1);
    freecrum(ptr);
*/
}
```
[genf.c:318–342]

The only live code is `return(0)`. The commented-out body would have collapsed the apex one level when it had exactly 1 child — the inverse of `levelpush`.

`recombineseq` calls `levelpull(father)` when `father->isapex` [recombine.c:66–67]:
```c
if (father->isapex)
    levelpull(father);
```

Since `levelpull` is a no-op, `recombineseq` never shrinks the tree height. The consequences:

1. **The apex height only ever increases** via `levelpush`; it never decreases regardless of deletions
2. After deletes that leave the tree sparse, the apex height remains at whatever maximum it reached during insertion — future inserts re-use that height rather than needing another `levelpush`
3. **`recombineseq` itself has an early return** [recombine.c:41]: `if (father->height < 3 || !father->modified) return(0)` — recombine is only attempted for trees of height ≥ 3, so shallow trees after deletes get no consolidation at all from that path
4. The structural invariant is asymmetric: the tree is a ratchet that grows in height during bulk inserts but never compresses, so a session that inserts many documents and then deletes most of them will retain an oversized tree skeleton

---

### Summary

| Question | Answer | Source |
|---|---|---|
| What triggers `splitcrumupwards`? | Creating a new leaf: `adopt(new, RIGHTBRO, ptr)` → parent goes from 1 to 2 bottom crums → `toomanysons` at height-1 returns TRUE (`numberofsons > MAXBCINLOAF=1`) | insert.c:46–48, genf.c:239, enf.h:27 |
| Is it purely occupancy > 1? | Yes, for height-1 nodes. Every new leaf insert immediately fires the condition. Text-pack fast path (`fillupcbcseq`) is the only escape | insert.c:34–41, genf.c:239–244 |
| What triggers `levelpush`? | `splitcrumupwards` loop reaching the fullcrum when `toomanysons` is still TRUE there; threshold is `MAXUCINLOAF=6` at the apex regardless of `MAXBCINLOAF` | split.c:26–31, genf.c:263, enf.h:26 |
| How does disabled `levelpull` interact? | `recombineseq` calls `levelpull` when `isapex`, but `levelpull` is a no-op (`return(0)`, body commented out). Tree height never decreases. This creates a ratchet: `levelpush` grows the apex, nothing shrinks it | genf.c:318–342, recombine.c:66–67 |
