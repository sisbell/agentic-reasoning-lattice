## Question 12 [evidence]

> Is the count computed by fully materializing the matching link set into a transient list and then taking its length, or is there an incremental counter that avoids building the list?

## KB Synthesis

The count is computed by fully materializing the complete list first, then walking it to count elements. There is no incremental counter.

From [SS-FIND-LINKS] (Finding 0035):

> FINDNUMOFLINKSFROMTOTHREE (opcode 29) is a trivial wrapper around FINDLINKSFROMTOTHREE. It calls `findlinksfromtothreesp()` to materialize the complete linked list of matching links, then walks the list counting elements. There is no count-only optimization — the full search executes (V-to-I translation, spanfilade search per endset, intersection of result sets), then the list is linearly counted.

Code references: `backend/spanf1.c:105-115` — calls full search then counts.

---

## Code Exploration

## How Link Count is Computed in udanax-green

**Short answer: full materialization, then linear scan. There is no incremental counter.**

---

### The Call Chain

The entry point for counting is `dofindnumoflinksfromtothree()` in `do2.c`, which calls into `spanf1.c`.

#### `findnumoflinksfromtothreesp` — `backend/spanf1.c:105–115`

```c
bool findnumoflinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrange, INT *numptr)
{
    typelinkset linkset;
    INT n;

    if (!findlinksfromtothreesp(taskptr, spanfptr, fromvspecset, tovspecset,
            threevspecset, orglrange, &linkset))
        return(FALSE);
    for (n = 0; linkset; linkset = linkset->next, ++n);   /* line 112 */
    *numptr = n;
    return(TRUE);
}
```

Line 112 is the entire count operation: a plain `for` loop traversing the already-built linked list. The count is derived **after** materialization, not during it.

---

### How the List Is Built

`findlinksfromtothreesp` (`backend/spanf1.c:56–103`) builds three separate link lists — one each for `from`, `to`, and `three` span constraints — by calling `sporglset2linkset()` for each, then intersects them:

```c
if (fromvspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
        &fromlinkset, orglrange, LINKFROMSPAN);
...
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linkset` (`backend/sporgl.c:222–237`) iterates over ranges and calls `sporglset2linksetinrange()`, which adds each matching link to a transient linked list via `onlinklist()`.

`onlinklist` (`backend/spanf2.c:26–44`) allocates a new node via `makelinkitem()` and appends it, with a linear scan to suppress duplicates:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);          /* duplicate — skip */
}
temp->next = linkset;       /* append new node */
```

`intersectlinksets` (`backend/spanf2.c:46–120`) then does a nested loop over all three materialized lists, emitting a fourth materialized intersection list — again via `makelinkitem()`, not a counter:

```c
for (; temp1; temp1 = temp1->next)
    for (temp2 = linkset2; temp2; temp2 = temp2->next)
        if (tumblereq(&temp1->address, &temp2->address)) {
            linkset4 = makelinkitem(taskptr, &temp1->address);
            *linkset4ptr = linkset4;
            linkset4ptr = &linkset4->next;
        }
```

---

### Summary

The complete materialization sequence is:

| Step | Function | Location | What happens |
|------|----------|----------|--------------|
| 1 | `dofindnumoflinksfromtothree` | `do2.c` | FEBE dispatch |
| 2 | `findnumoflinksfromtothreesp` | `spanf1.c:105` | Calls step 3, then counts |
| 3 | `findlinksfromtothreesp` | `spanf1.c:56` | Builds 3 lists, intersects them |
| 4 | `sporglset2linkset` | `sporgl.c:222` | Materializes per-constraint list |
| 5 | `onlinklist` | `spanf2.c:26` | Appends each link node, deduplicates |
| 6 | `intersectlinksets` | `spanf2.c:46` | Builds a 4th materialized intersection list |
| 7 | back in step 2 | `spanf1.c:112` | `for (n=0; linkset; linkset=linkset->next, ++n)` |

**There is no incremental counter, no lazy evaluation, and no early-exit counting path.** The entire matching link set is allocated in transient task memory (`taskalloc`) as a singly-linked list, and the length is obtained by walking that list from head to tail. For a query matching *N* links, this incurs O(N) allocation cost for all three per-constraint lists, O(N²) or O(N³) work in `intersectlinksets` for the cross-product intersection scan, and then a final O(N) walk just to produce the integer count — which is then returned to the FEBE client while the transient lists are discarded.
