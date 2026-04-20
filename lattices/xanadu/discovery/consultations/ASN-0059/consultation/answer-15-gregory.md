## Question 15 [gregory]

> After INSERT creates a new POOM entry and shifts existing entries, does `insertnd` trigger `recombinend` (2D rebalancing) or `splitcrumupwards` on the POOM, and what determines which rebalancing path is taken?

## KB Synthesis

After INSERT, the POOM follows the **split path** (`splitcrumupwards`), not the rebalance path (`recombinend`). Here's the full mechanism:

## INSERT's POOM Update Path

**Step 1 — Gap creation and crum placement**

`insertnd` calls `makegappm` to shift existing POOM entries (only those in `[blade[0], blade[1])`, i.e., within the insertion subspace) [SS-TWO-BLADE-KNIFE, FC-SUBSPACE]. Then it either:
- **Extends** an existing crum if `isanextensionnd` succeeds (same `homedoc`, contiguous I-address at crum's reach → zero new crums) [ST-INSERT Finding 0062], or
- **Creates** a new bottom crum and inserts it into the appropriate height-1 parent via `insertcbcnd` [INV-ENFILADE-OCCUPANCY Finding 0070].

**Step 2 — Overflow check → `splitcrumupwards`**

After adding a child, `insertcbcnd` triggers `splitcrumupwards(parent)`, which loops while `toomanysons(ptr)` is TRUE. For the POOM, the threshold is `MAX2DBCINLOAF = 4` at height-1 and `MAXUCINLOAF = 6` at height > 1 [SS-ENFILADE-BRANCHING].

The split path branches on `isfullcrum(ptr)`:
- **Root overflow**: `levelpush` increments tree height, then `splitcrum` divides the demoted root's children between two new siblings [SS-ENFILADE-TREE Finding 0058].
- **Internal node overflow**: `splitcrum` → for POOM specifically, `splitcrumpm` peels off the child with the **largest SPANRANGE displacement** (`cdsp.dsas[SPANRANGE]`), not the diagonal key [ST-SPLIT-2D Finding 0071].

After insertion, `setwispupwards` recalculates the 2D displacement (root `cdsp` = minimum address across children) to maintain the relative-addressing invariant [INV-ENFILADE-RELATIVE-ADDRESSING].

## Why `recombinend` Is Not Triggered by INSERT

`recombinend` is the **underflow** response. It is called when `toofewsons(ptr)` is TRUE (`sons < B-1`), which can only happen after **DELETE** removes children from a node [ST-DELETE Finding 0058, ST-REBALANCE-2D Finding 0071]. INSERT only adds children — it can cause overflow (→ split) but never underflow (→ merge/steal).

## Determining Factor

The branching factor constants and `whereoncrum`/`isanextensionnd` together determine which path INSERT takes:

| Condition | Path | Δ crums |
|-----------|------|---------|
| `origin == crum.reach` AND same `homedoc` | Extension (no split) | 0 |
| `origin < crum.reach` (THRUME) | Knife cut → new crum | +2 (split original, add new) |
| Parent overflow after new crum | `splitcrumupwards` → `splitcrumpm` | net +1 node at parent level |
| Parent at capacity but not overflow | Absorbed into existing node, no split | 0 at parent level |

The coalescing behavior means **continuous interior typing costs +2 crums once** (for the first character at a new position), then +0 per subsequent character at the same position [ST-CRUM-BOUND Finding 0062]. CREATELINK breaks this coalescing by advancing the I-address allocation pointer, causing the next INSERT to fail `isanextensionnd` [ST-CRUM-BOUND Finding 0063, INT-LINK-INSERT].

---

## Code Exploration

---

## Answer: POOM Rebalancing After INSERT — `splitcrumupwards` vs. `recombinend`

The two operations are **not alternative paths** — they are **sequential**, and `recombinend` only fires as a consequence of whether `splitcrumupwards` did work. Here is the complete trace.

---

### 1. Entry point: `insertnd` (`insertnd.c:15`)

```c
int insertnd(typetask *taskptr, typecuc *fullcrumptr, typewid *origin,
             typewid *width, type2dbottomcruminfo *infoptr, INT index)
```

For a POOM insert, the function body at `insertnd.c:46-77` does the following in order:

1. **Record current state**: `oldheight = fullcrumptr->height` [line 47]
2. **Create gap**: `makegappm(...)` [line 54] — shifts existing POOM entries to make room (POOM-only step, not done for SPAN)
3. **Insert**: `bothertorecombine = doinsertnd(fullcrumptr, origin, width, infoptr, index)` [line 57]
4. **Conditionally recombine** [lines 70–77]:

```c
if(/*TRUE||*/bothertorecombine||(fullcrumptr->height != oldheight)){
    recombine (fullcrumptr);
}
```

---

### 2. The descent: `doinsertnd` → `insertmorend` → `insertcbcnd`

`doinsertnd` (`insertnd.c:185`) handles two cases:
- **Empty enfilade**: calls `firstinsertionnd` [line 192], returns `FALSE` — no split, no recombine
- **Non-empty**: calls `insertmorend` [line 196]

`insertmorend` (`insertnd.c:219`) recurses to the leaf level. At `height == 1` it calls `insertcbcnd` [line 231]; the return value (`splitsomething`) bubbles all the way back to `bothertorecombine` in `insertnd`.

---

### 3. The fork point: `insertcbcnd` (`insertnd.c:242`)

This function contains the critical branch:

**Path A — Extension (adjacent insert):**
```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        if(!isfullcrum((typecorecrum*)father)){
            return(setwispupwards(findfather((typecorecrum*)father),1));
        }
        return(FALSE);   // ← bothertorecombine = FALSE
    }
}
```
[`insertnd.c:250–258`]

`isanextensionnd` (`insertnd.c:301`) checks whether the new content is contiguous with an existing crum (same homedoc, and `reach == origin`). If so, it widens the existing crum in-place. **`splitcrumupwards` is never called. `recombine` will not be triggered.**

**Path B — New crum created:**
```c
new = createcrum (0, (INT)father->cenftype);   // insertnd.c:260
reserve (new);
adopt (new, SON, (typecorecrum*)father);        // insertnd.c:262
...
splitsomething = splitcrumupwards (father);    // insertnd.c:272
rejuvinate (new);
return(splitsomething);                        // ← becomes bothertorecombine
```
[`insertnd.c:260–274`]

When the insert is not adjacent to any existing crum, a new bottom crum is created. `splitcrumupwards` is **always** called here.

---

### 4. `splitcrumupwards` (`split.c:16`)

```c
bool splitcrumupwards(typecuc *father)
{
    splitsomething = FALSE;
    for (; toomanysons(father); father = (typecuc *)findfather((typecorecrum*)father)) {
        if (isfullcrum((typecorecrum*)father)) {
            levelpush(father);                           // grow tree height
            splitcrum((typecuc*)findleftson(father));
            return(TRUE);
        }
        splitcrum (father);
        splitsomething = TRUE;
    }
    return(splitsomething);
}
```
[`split.c:17–44`]

`toomanysons` (`genf.c:239`) checks:
```c
ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum(ptr) ? MAX2DBCINLOAF : MAXBCINLOAF))
```
- Interior nodes (height > 1): capacity = **6** (`MAXUCINLOAF`, `enf.h:26`)
- 2D bottom nodes (POOM/SPAN, height == 1): capacity = **4** (`MAX2DBCINLOAF`, `enf.h:28`)

The loop walks upward. At each overfull node:
- **If it's the fullcrum (apex)** [`split.c:28`]: calls `levelpush(father)` — inserts a new intermediate node between the apex and its current children, incrementing `fullcrumptr->height` — then calls `splitcrum` on the new intermediate node. Returns `TRUE` immediately.
- **Otherwise** [`split.c:37`]: calls `splitcrum(father)`.

For POOM, `splitcrum` dispatches to `splitcrumpm` (`split.c:53–55`), which calls `peelcrumoffnd` on the son with the largest `cdsp.dsas[SPANRANGE]` (most diagonally displaced). `peelcrumoffnd` disowns that son and rehomes it under a newly created sibling of `father` (`split.c:130–168`).

---

### 5. `recombine` → `recombinend` (`recombine.c:22`, `recombine.c:104`)

Back in `insertnd`:
```c
if(bothertorecombine || (fullcrumptr->height != oldheight)) {
    recombine(fullcrumptr);
}
```
[`insertnd.c:70–77`]

`recombine` dispatches to `recombinend` for both POOM and SPAN [`recombine.c:29–32`].

`recombinend` is a **2D consolidation pass**:
```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);                        // recurse first
    getorderedsons(father, sons);                // sort by diagonal position
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if (sons[j] && ishouldbother(sons[i],sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);
        }
    }
    if (father->isapex)
        levelpull(father);                       // stubbed out — returns 0
}
```
[`recombine.c:104–131`]

`ishouldbother` merges two sibling subtrees if their combined child count fits within capacity (`MAXUCINLOAF` or `MAX2DBCINLOAF`). Sons are sorted diagonally (by `cdsp[0] + cdsp[1]`) before pairwise comparison, which groups spatially nearby nodes for consolidation.

Note: `levelpull` is a stub at `genf.c:318–342` (`return(0)` immediately) — tree height never shrinks after a `recombine`.

---

### Summary

| Condition | `splitcrumupwards` triggered? | `recombine` triggered? |
|---|---|---|
| Insert extends existing crum | **No** | **No** |
| Insert creates new crum, no overflow | **Yes** (called, returns FALSE) | **No** |
| Insert creates new crum, interior overflow | **Yes**, returns TRUE | **Yes** |
| Insert creates new crum, apex overflow (`levelpush`) | **Yes**, returns TRUE + height increases | **Yes** (both conditions fire) |

**What determines which rebalancing path is taken:**

1. **`splitcrumupwards` fires** iff `isanextensionnd` returns FALSE for every existing sibling in `insertcbcnd` — i.e., the new content is not contiguous with any existing crum. It is the **1D overflow handler**: splits loaves with too many sons by peeling the most-displaced child off into a new sibling, walking upward until no loaf is overfull. If the root itself overflows, `levelpush` grows the tree by one level.

2. **`recombine` fires** iff `splitcrumupwards` returned TRUE **or** the fullcrum's height changed. It is the **2D consolidation pass**: merges underloaded siblings to reduce fragmentation. The guard `father->height < 2 || !father->modified` at `recombine.c:112` means it only processes modified non-leaf nodes, so it does not run on trees that were untouched.
