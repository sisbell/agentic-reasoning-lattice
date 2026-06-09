## Question 17 [evidence]

> Since CREATELINK uses `insertpm`+`makegappm` and places links at document end via `findnextlinkvsa`, does the link-creation shift ever actually move existing POOM entries, or is the shift always a no-op because nothing exists beyond the insertion point?

## KB Synthesis

In sequential operation, the shift is **always a no-op** — but for structural reasons that are worth unpacking precisely.

## Why the shift never fires in practice

`findnextlinkvsa` places each new link at `2.1` (first link) or `vspanreach` (subsequent links) [SS-LINK-SUBSPACE, Finding 0052]. `vspanreach` is the current end of the document's V-extent — by definition, no POOM entries exist beyond it. So at the moment `makegappm` runs, the set `{entry ∈ poom(doc) : entry.vpos >= insertion_point}` is empty. Nothing qualifies for the case-1 shift path.

The two-blade knife [SS-TWO-BLADE-KNIFE, Finding 0054] would bound any shifts to `[insertion_point, 3.1)`, but even this bounded region is vacuous: no entries live there before the first link is placed.

The KB makes this explicit [ST-CREATE-LINK, Finding 0052]:

> "The 'no shifting' behavior of CREATELINK is an emergent property of append-at-end placement, not a fundamental property of the operation."

## But the mechanism is live

The underlying machinery is fully capable of shifting. If `findnextlinkvsa` were bypassed or two operations raced [EC-CONCURRENT-LINK-CREATION]:

> "If operation A calls `findnextlinkvsa` to get position P, then operation B inserts a link before P, then A inserts at P — B's link would be shifted by A's insertion."

This would be observable: B's link (previously at `P`) would be displaced to `P + width` by A's insertion. The shift code at `insertnd.c:162` would execute for real.

## In sequential execution

[INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY] guarantee that no interleaving occurs. So the append-at-end invariant holds strictly: each CREATELINK appends beyond all existing entries, and `makegappm`'s shift region `[insertion_point, 3.1)` is always empty at the time of insertion.

**Bottom line**: The shift is structurally a no-op in sequential operation because append-at-end leaves nothing to shift — but the code path that would shift is live and would execute correctly under concurrent access.

---

## Code Exploration

I now have everything needed to give a complete, cited answer. Let me compile it.

---

## Answer: The Link-Creation Shift Is Always a No-Op

The shift never moves any existing POOM entries during link creation. Here is the complete code trace that proves it.

---

### Call Chain

`docreatelink` [do1.c:195] → `docopy` [do1.c:212] → `insertpm` [orglinks.c:75] → `insertnd` [insertnd.c:15] → `makegappm` [insertnd.c:124]

---

### Step 1 — `findnextlinkvsa` returns the exact POOM reach

```c
// do2.c:151-166
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);
    tumblerincrement (&firstlink, 1, 1, &firstlink);

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

`doretrievedocvspan` calls `retrievevspanpm` [orglinks.c:165], which reads the root POOM crum directly:

```c
// orglinks.c:165-172
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->stream = orgl->cdsp.dsas[V];  // root's V-displacement
    vspanptr->width  = orgl->cwid.dsas[V];  // root's total V-width
    ...
}
```

So `vspanreach = root.cdsp.V + root.cwid.V`.

---

### Step 2 — `makegappm` computes `reach` from the same root fields

```c
// insertnd.c:138-143
clear (&offset, sizeof(offset)); /* fullcrum always has zero offset */
prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

`prologuend` is [retrie.c:334-339]:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

With `offset = 0`:
- `grasp = 0 + fullcrumptr->cdsp.V = fullcrumptr->cdsp.V`
- `reach = grasp + fullcrumptr->cwid.V = fullcrumptr->cdsp.V + fullcrumptr->cwid.V`

**This is identical to `vspanreach`.**

---

### Step 3 — The guard always fires

Because `linkvsa = vspanreach = reach`, the test:

```c
tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS   // origin == reach → EQUAL → NOT LESS
```

is `TRUE`, and `makegappm` returns `0` before executing the for-loop over children [insertnd.c:151-169] that performs the actual shifts.

**Two distinct no-op paths:**

| Document state | Firing guard condition [insertnd.c:140-142] |
|---|---|
| Empty document | `iszerotumbler(&fullcrumptr->cwid.dsas[V])` — first clause fires |
| Non-empty document | `tumblercmp(origin, reach) != LESS` — third clause fires (EQUAL) |

---

### Why `insertpm` uses `makegappm` at all

`insertnd` [insertnd.c:51-61] is a general insertion function shared between text and link insertion:

```c
case POOM:
    makegappm (taskptr, fullcrumptr, origin, width);
    ...
    bothertorecombine=doinsertnd(fullcrumptr,origin,width,infoptr,index);
```

For **text insertions** (`doinsert`), inserting into the middle of existing content produces `origin < reach`, so the guard does NOT fire and `makegappm` performs real V-address shifts on existing entries (case 1 in [insertnd.c:161-164]). For **link creation**, `findnextlinkvsa` is specifically designed to return the boundary position, making the shift permanently a no-op.

The comment in `makegappm`'s guard [insertnd.c:143] — *"this if for extensions to bc without calling cut"* — confirms this boundary case was deliberate design: appending beyond the current extent bypasses the cut-and-shift machinery entirely.

---

### Conclusion

The shift is **structurally guaranteed to be a no-op** for every link creation. `findnextlinkvsa` [do2.c:151] returns exactly `root.cdsp.V + root.cwid.V`, which equals `reach` as computed by `prologuend` in `makegappm` [insertnd.c:139]. The third guard clause fires unconditionally, returning 0 before any child crum has its V-displacement modified. The `makegappm` call in the link-creation path is present only because `insertnd` is a shared primitive — in the link context, it is dead code.
