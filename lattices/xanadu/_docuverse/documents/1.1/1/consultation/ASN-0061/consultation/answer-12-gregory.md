## Question 12 [gregory]

> After DELETE shifts surviving POOM entries left via `tumblersub`, is there any reconciliation pass that detects when two formerly non-adjacent crums become I-address-contiguous and merges them, or do they remain as separate POOM entries permanently?

## KB Synthesis

No reconciliation pass exists. After DELETE shifts surviving POOM entries left, they remain as permanently separate crums.

Here is what the KB tells us about each stage of DELETE's aftermath:

**Phase 1 & 2 (cutting and classification)** [PRE-DELETE, ST-DELETE]: `deletend()` slices crums that straddle the deletion boundary, removes crums entirely within the deleted range, and shifts crums after the deletion via `tumblersub`. At no point does this pass check I-address relationships between survivor crums.

**Post-deletion rebalancing** [ST-REBALANCE-2D, INV-ENFILADE-OCCUPANCY]: After `setwispupwards` recalculates widths, `recombinend` rebalances the tree. Its merge criterion in `ishouldbother` is purely occupancy-based: `dest->numberofsons + src->numberofsons <= max_children`. It reorganizes which parent nodes group which content crums — it never examines or exploits I-address contiguity between leaf-level mappings.

**Why contiguity can't emerge anyway**: Even if two crums become V-adjacent after deletion (crum A's reach == crum B's grasp), they are I-address non-adjacent. The deleted content occupied I-addresses between them, and those I-addresses remain allocated in the append-only granfilade [FC-GRANF-ON-DELETE, INV-NO-IADDR-REUSE]. The gap in I-address space persists. So `isanextensionnd()`'s criterion — same `homedoc` AND reach equals origin in I-space [ST-INSERT, Finding 0062] — would fail even if it were invoked.

**The extension check is INSERT-only**: `isanextensionnd()` is called only from `insertnd()` during content insertion [ST-INSERT]. DELETE does not invoke this path. There is no equivalent "merge if now contiguous" scan in the DELETE or rebalancing code paths.

**Structural consequence**: This is consistent with [INV-VSPAN-CONSOLIDATION] — the single-span consolidation guarantee holds because `isanextensionnd()` catches contiguity at insertion time. DELETE can fragment what was once contiguous, and that fragmentation is permanent. The crum count after a sequence of insertions and deletions follows the bound `c ≤ 1 + 2C + ...` from [ST-CRUM-BOUND, Finding 0062], where each interior insertion costs +2 crums that deletion never reclaims through merging.

**Bottom line**: Formerly non-adjacent crums that become V-adjacent after DELETE shifting remain as separate POOM entries permanently. The rebalancing that does occur operates on tree occupancy (B-tree node consolidation [ST-REBALANCE-2D]), not on content-level crum consolidation.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Answer: No Reconciliation Pass Exists After DELETE

### The Complete Delete Execution Path

**Entry point** — `dodeletevspan` [do1.c:158–167]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

**`deletevspanpm`** [orglinks.c:145–152] — a thin wrapper with no post-processing:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```
No merge opportunity here. Just `deletend` + a bert log entry.

**`deletend`** [edit.c:31–76] — where the actual work happens:

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    makecutsnd (fullcrumptr, &knives);                    // [edit.c:44] cut at origin and origin+width
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);  // [edit.c:45]
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {  // [edit.c:47]
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);       // [edit.c:59] fully deleted crum: remove
            subtreefree ((typecorecrum*)ptr);  // [edit.c:60]
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
            // [edit.c:63] surviving crum after the hole: shift I-address left
            break;
        }
    }
    setwispupwards (father,1);  // [edit.c:74] update wid counts upward
    recombine (father);          // [edit.c:75] ← the only post-delete pass
}
```

Case 2 is the `tumblersub` shift. After it, `recombine(father)` is called. This is the **sole post-delete operation**.

---

### What `recombine` Actually Does

**`recombine`** [recombine.c:22–34] dispatches to `recombinend` for POOM:
```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case POOM:
        recombinend (father);   // [recombine.c:32]
    }
}
```

**`recombinend`** [recombine.c:104–131]:
```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);           // [recombine.c:112] guard: interior nodes only, height ≥ 2

    for (ptr = getleftson (father); ptr; ptr=(typecorecrum *)getrightbro (ptr)){
        recombinend (ptr);   // [recombine.c:114–116] recurse into children
    }

    getorderedsons (father, sons);   // [recombine.c:118] sort siblings by diagonal magnitude
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);  // [recombine.c:123] balance siblings
            }
        }
    }
    if (father->isapex)
        levelpull (father);   // [recombine.c:130]
}
```

The decision criterion is `ishouldbother` [recombine.c:150–163]:
```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons
            <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
            && randomness(.3));   // [recombine.c:162]
}
```

**This is a pure tree-balance criterion**: "will the combined child count fit in one loaf node?" There is no check for I-address adjacency between the bottom crums those interior nodes contain.

`eatbrossubtreend` [recombine.c:205–233] and `takenephewnd` [recombine.c:235–257] merge or relocate children of sibling interior nodes (moving height-1 subtrees around), adjusting DSPs accordingly via `makeroomonleftnd` and `dspadd`/`dspsub`. Neither inspects whether the **bottom crums** (height-0 leaves) in those subtrees happen to be I-address-adjacent.

`comparecrumsdiagonally` [recombine.c:313–320] — used by `getorderedsons` for sort order — is also not an adjacency test:
```c
INT comparecrumsdiagonally(typecorecrum *a, typecorecrum *b)
{
    tumbleradd (&a->cdsp.dsas[0], &a->cdsp.dsas[1], &amagnitude);  // sum of I+V
    tumbleradd (&b->cdsp.dsas[0], &b->cdsp.dsas[1], &bmagnitude);
    return (tumblercmp (&amagnitude, &bmagnitude));
}
```

It sorts by `I+V` magnitude, not I-address end-meets-start.

---

### Where I-Address Contiguity IS Checked (Only on Insert)

The only place that checks whether two POOM crums are I-address-adjacent is `isanextensionnd` [insertnd.c:301–309], called exclusively inside `insertcbcnd` [insertnd.c:242–275]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);                            // [insertnd.c:305] same home doc?
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
    // [insertnd.c:308] does this crum's right edge equal the new insertion's origin?
}
```

If it returns `TRUE`, `insertcbcnd` simply widens the existing crum's width instead of allocating a new one [insertnd.c:251]:
```c
if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // [insertnd.c:251]
    ...
    return(FALSE);
}
```

This path is only reachable via `insertnd` → `insertmorend` → `insertcbcnd`. There is no equivalent call chain triggered by `deletend`.

---

### Conclusion

**Yes, two formerly non-adjacent POOM crums that become I-address-contiguous after DELETE remain as separate entries permanently** (unless a subsequent INSERT happens to land exactly at the boundary, in which case `isanextensionnd` would merge the new insertion with one of them — but that would not merge the two survivors with each other).

The call `recombine(father)` at [edit.c:75] is a **B-tree balance pass**, not a semantic merge. It operates at interior-node level (height ≥ 2 guard at [recombine.c:112]), relocates subtrees to balance loaf occupancy, and has no awareness of I-address adjacency between bottom crums. The only I-address contiguity check in the entire codebase — `isanextensionnd` at [insertnd.c:301–309] — is insert-path-only and never fires during or after delete.
