## Question 5 [evidence]

> How does udanax-green handle DELETE of the exact coverage range and INSERT strictly inside a coverage range — does it produce one projection cluster or split into multiple?

## KB Synthesis

## DELETE of Exact Coverage Range

When both deletion boundaries align exactly with a crum's grasp and reach, `whereoncrum` returns `ONMYLEFTBORDER` and `ONMYRIGHTBORDER` respectively — neither is `THRUME`. The guard in `makecutsbackuptohere` only calls `slicecbcpm` for `THRUME`, so Phase 1 produces **no cuts**. The crum is handled whole in Phase 2 as Case 1 (fully within deletion range): it is `disown`ed and freed as a single unit. No proliferation — exactly one crum is removed. [PRE-DELETE / Finding 0075]

## INSERT Strictly Inside a Coverage Range

An interior insertion where `crum.grasp < v < crum.reach` triggers `whereoncrum = THRUME`. `makegappm` constructs its two-blade knife, `slicecbcpm` splits the existing crum at the cut, and a new crum is created for the inserted content. Net result: **1 crum becomes 3** (left half + new content crum + right half, Δ = +2). [ST-INSERT / Finding 0062]

Subsequent inserts at `v+1`, `v+2`, ... hit `ONMYRIGHTBORDER` on the new content crum, triggering `isanextensionnd` coalescing — so only the *first* interior insert at a new position pays the +2 penalty; continued typing there costs +0. [ST-CRUM-BOUND / Finding 0062]

**Summary:** boundary-aligned DELETE leaves no residual crums; interior INSERT splits into three, with subsequent adjacent inserts merging back into the new crum rather than fragmenting further.

---

## Code Exploration

Now I have all the source I need. Let me write the precise answer.

---

## How udanax-green Handles DELETE of Exact Coverage and INSERT Strictly Inside

### Architecture Background

The document POOM (permutation matrix enfilade) stores 2D crums, each mapping a contiguous V-range to a contiguous I-range at 1:1 width. One bottom crum = one projection cluster: V[a, b) ↔ I[x, y) where b-a == y-x.

Link endpoints are stored as I-spans in the link's own orgl and in the spanfilade. Following a link projects I-spans through the target document's POOM via `permute` → `span2spanset` → `context2span`. The number of V-spans returned equals the number of POOM crums that overlap the query I-span.

---

### Case 1: DELETE of the Exact Coverage Range

**Call chain:**
```
dodeletevspan [do1.c:158]
  → findorgl + deletevspanpm [orglinks.c:145]
      → deletend [edit.c:31]
```

`deletevspanpm` [orglinks.c:145-152]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` [edit.c:31-76]:
```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    movetumbler (origin, &knives.blades[0]);          // [edit.c:40] cut at delete-start
    tumbleradd (origin, width, &knives.blades[1]);    // [edit.c:41] cut at delete-end
    knives.nblades = 2;
    makecutsnd (fullcrumptr, &knives);                // split crums at both boundaries
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    ...
    for (ptr = findleftson(father); ptr; ptr = next) {
        switch (deletecutsectionnd(ptr, &fgrasp, &knives)) {
          case 1:
            disown((typecorecrum*)ptr);               // [edit.c:59]
            subtreefree((typecorecrum*)ptr);          // completely removed
            break;
          case 2:
            tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // [edit.c:63] shift back
            break;
        }
    }
    setwispupwards(father, 1);
    recombine(father);                                // [edit.c:75]
}
```

`deletecutsectionnd` [edit.c:235-248] iterates knives from right to left. For a crum sitting exactly at [a, b) with knives at a (`blades[0]`) and b (`blades[1]`):

- i=1: `whereoncrum(crum_[a,b), blades[1]=b)` → `ONMYRIGHTBORDER`, which is **greater than** `ONMYLEFTBORDER` → not case 2
- i=0: `whereoncrum(crum_[a,b), blades[0]=a)` → `ONMYLEFTBORDER` ≤ `ONMYLEFTBORDER` → **returns case 1**

**Case 1 → `disown` + `subtreefree`.** The crum is removed from the tree entirely.

After deletion, a subsequent `permute` call querying the link's I-span [x, y) calls `retrieverestricted` [retrie.c:56-85] → `findcbcinarea2d` [retrie.c:229-268]. `crumqualifies2d` [retrie.c:270-305] finds **no crums** whose I-range overlaps [x, y) — all were deleted. `span2spanset` [orglinks.c:439] iterates an empty context list.

**Result: ZERO projection clusters.** The link endpoint becomes invisible; its content no longer exists in the document's V-space.

---

### Case 2: INSERT Strictly Inside a Coverage Range

**Call chain:**
```
doinsert [do1.c:87]
  → inserttextingranf + docopy [do1.c:119]
      → insertpm [orglinks.c:75]
          → insertnd [insertnd.c:15]
              → makegappm [insertnd.c:54,124]  ← splits the spanning crum
              → doinsertnd                      ← places new content
              → recombine [insertnd.c:76]
```

`makegappm` [insertnd.c:124-172] opens a gap in the POOM at the insert position p:

```c
int makegappm(typetask *taskptr, typecuc *fullcrumptr, typewid *origin, typewid *width)
{
    ...
    if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
    || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
    || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
        return(0);                                   // [insertnd.c:143] guard: p outside range

    movetumbler(&origin->dsas[V], &knives.blades[0]);     // [insertnd.c:144] cut at p
    findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]); // [insertnd.c:145]
    knives.nblades = 2;
    makecutsnd(fullcrumptr, &knives);               // [insertnd.c:148] split crum spanning p
    ...
    for (ptr = findleftson(father); ptr; ...) {
        switch (insertcutsectionnd(ptr, &fgrasp, &knives)) {  // [insertnd.c:152]
          case 1:
            tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]); // [insertnd.c:162]
            ivemodified(ptr);
            break;
        }
    }
    ...
}
```

`makecutsnd` is called with cuts at p (`blades[0]`) and `secondCut` (`blades[1]`). Any POOM bottom crum that has p strictly inside it — i.e., the crum spanning [a, b) where a < p < b — is **split at p** by `makecutsnd`. After splitting, two crums exist:

- Crum A: V [a, p) → I [x, x+(p−a))  
- Crum B: V [p, b) → I [x+(p−a), y)

`insertcutsectionnd` [edit.c:207-233] then classifies Crum B (which starts at p) as **case 1** → its V-displacement is shifted forward by insertion width w:

- Crum A: V [a, p) → I [x, x+(p−a))  **unchanged**
- Crum B: V [p+w, b+w) → I [x+(p−a), y)  **shifted forward**

Then `recombine(fullcrumptr)` [insertnd.c:76] runs `recombinend` [recombine.c:104-131]. `recombinend` calls `ishouldbother` [recombine.c:150-163] and `takeovernephewsnd` [recombine.c:165-203] to attempt merges. **Crucially, Crum A and Crum B cannot be merged** because they are now separated in V-space by a gap [p, p+w) containing the newly inserted content (which has its own I-span from the granfilade). Their I-spans [x, x+(p-a)) and [x+(p-a), y) are adjacent but their V-spans are not contiguous, so no structural merging of their mappings occurs.

When following the link with I-span [x, y), `span2spanset` [orglinks.c:425-454] calls `retrieverestricted` → `findcbcinarea2d` [retrie.c:229-268]. `crumqualifies2d` [retrie.c:270-305] returns TRUE for **both** Crum A and Crum B since both overlap [x, y) in the I-dimension. Both are threaded onto the context list via `incontextlistnd` [context.c:75-111]. The loop at [orglinks.c:439]:

```c
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`context2span` [context.c:176-212] converts each context (Crum A and Crum B) into a V-span by clipping to the restriction I-span and reading the corresponding V coordinates. Crum A produces V-span [a, p); Crum B produces V-span [p+w, b+w). Both are appended to `targspansetptr` via `onitemlist`.

**Result: TWO projection clusters.** The link endpoint now projects to two non-contiguous V-spans — [a, p) and [p+w, b+w) — separated by the inserted content at [p, p+w).

---

### Summary Table

| Operation | What Happens to POOM Crum | Projection Clusters |
|-----------|--------------------------|---------------------|
| DELETE of exact [a, b) | `deletecutsectionnd` case 1 → `disown` + `subtreefree` [edit.c:59-60] | **0** (crum gone; `findcbcinarea2d` finds nothing) |
| INSERT at p strictly inside [a, b) | `makecutsnd` splits spanning crum; `insertcutsectionnd` case 1 shifts right half forward [insertnd.c:162] | **2** (both halves qualify in `crumqualifies2d`; both returned by `span2spanset`) |

The critical asymmetry: deletion at an exact boundary hits `deletecutsectionnd` case 1 because `whereoncrum` at the crum's own left-border address returns `ONMYLEFTBORDER` ≤ `ONMYLEFTBORDER` [edit.c:243]. An insert strictly inside hits `makecutsnd` first, which physically splits the crum at the insert point [insertnd.c:148], then `recombine` cannot re-merge the two halves because their V-spans are no longer contiguous.
