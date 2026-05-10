## Question 12 [gregory]

> After DELETE shifts surviving POOM entries left via `tumblersub`, is there any mechanism that detects when two formerly non-adjacent entries become I-address-contiguous and merges them via `isanextensionnd`, or do they remain as separate crums permanently?

## KB Synthesis

**No, there is no such mechanism. Crums that become I-address-contiguous after DELETE remain permanently separate.**

Here is why:

**`isanextensionnd` is INSERT-only**

From [ST-INSERT] (Finding 0062), `isanextensionnd` at `insertnd.c:293-301` fires exclusively during the INSERT code path when new content is being placed. It checks two conditions: same `homedoc` AND `new_content.origin == existing_crum.reach`. This is a guard on *new incoming content*, not a post-hoc scan of existing crums. The DELETE code path never calls `isanextensionnd` or anything equivalent.

**`recombinend` after DELETE is structural, not I-space-aware**

From [ST-DELETE] (Finding 0058), after `deletend` removes and shifts crums, it calls `setwispupwards` and `recombinend`. From [ST-REBALANCE-2D] (Finding 0071), `recombinend` merges tree nodes based on `ishouldbother`, which tests combined `numberofsons` against the branching limit — a pure B-tree occupancy criterion. It has no awareness of I-address ranges. When `eatbrossubtreend` consolidates two sibling nodes, it moves their *children* together; bottom crums (height-0 leaves) are moved as opaque units. Their `origin` and `width` fields are never compared for contiguity.

**The consequence**

Consider "ABXCD" where "AB" and "CD" are separate crums because "X" was inserted between them (paying the +2 crum cost from [ST-CRUM-BOUND]). After DELETE removes "X", the two crums are shifted and become I-address-adjacent in V-space, but they remain as two distinct POOM entries indefinitely. The crum count decreases only by the number of crums that fell entirely within the deletion range (Case 1: `disown` + `subtreefree` from [ST-DELETE] Finding 0064), never by post-shift contiguity detection.

This also means the crum bound `c ≤ 1 + 2C + 2L + 3R + 3P` from [ST-CRUM-BOUND] is monotonically non-decreasing with respect to interior insertion events, and DELETE does not recover the +2 penalty paid for each cursor repositioning.

---

## Code Exploration

Here is the full answer.

---

## Answer: No Contiguity-Based Merging Occurs After DELETE

The short answer is: **after `tumblersub` shifts surviving POOM crums left, there is no mechanism that detects newly-contiguous I-addresses and merges the crums. They remain as separate bottom crums permanently.** `isanextensionnd` is exclusively an INSERT-path function and is never invoked during delete or recombine.

---

### 1. The DELETE Path

Entry: `fns.c:deletevspan()` → `do1.c:dodeletevspan()` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr) );
}
```

`deletevspanpm` ultimately calls `deletend()` in `edit.c:31–76`, which handles the 2D (SPAN/POOM) case.

Inside `deletend()`, after cuts are placed and the intersection region is found, each surviving crum that lies entirely to the right of the deleted region gets **case 2**:

```c
case 2:
    tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    /* This will get set to modified in setwisp */
    break;
```
[edit.c:63–65]

This shifts the crum's displacement left by `width`. After all crums are processed:

```c
setwispupwards (father,1);
recombine (father);          // edit.c:74–75
```

---

### 2. What `recombine()` Does — and Does NOT Do

`recombine()` [recombine.c:22–34] dispatches on enfilade type. For POOM it calls `recombinend()`:

```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case GRAN:  recombineseq (father); break;
      case SPAN:  recombinend (father);  break;
      case POOM:  recombinend (father);             // ← POOM goes here
    }
}
```

`recombinend()` [recombine.c:104–131]:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2  || !father->modified)
        return(0);
    for (ptr = getleftson (father); ptr; ...)
        recombinend (ptr);                          // recurse on children

    getorderedsons (father, sons);
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);
            }
        }
    }
    if (father->isapex)
        levelpull (father);
}
```

`ishouldbother()` [recombine.c:150–163] is the gate:

```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons <=
            (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
            && randomness(.3));
}
```

And `randomness()` [recombine.c:132–147] **always returns TRUE** — the probabilistic body is commented out:

```c
bool randomness(float probability)
{
  static float i = 0;
  return(TRUE);
  /* i += probability; ... */
}
```

**Critical observation**: `ishouldbother` decides whether to merge two internal nodes based solely on **capacity** (whether the combined son-count fits within `MAXUCINLOAF`/`MAX2DBCINLOAF`). It does not inspect the I-address layout of the content at the leaves. The subsequent `takeovernephewsnd()` / `eatbrossubtreend()` re-parents children between internal nodes — this is tree **rebalancing**, not content **consolidation**.

The bottom crums (the actual POOM leaf entries holding `homedoc`, `cdsp`, `cwid`) are moved between internal nodes but are **never merged into one another** by `recombine`.

---

### 3. Where `isanextensionnd` Is Called — And Is Not

`isanextensionnd` [insertnd.c:301–309]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

It computes the crum's `reach` (absolute end address) and compares it against the `origin` of incoming new content. If they are equal **and** the homedoc matches, the new content is an I-address-contiguous extension — so no new crum is created; instead the existing crum's width is widened in place.

`isanextensionnd` has exactly **one call site** in the entire codebase:

```c
// insertnd.c:249–258
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

This is inside `insertcbcnd()` [insertnd.c:242–275], reachable only through the `insertmorend()` → `insertcbcnd()` call chain, which is called from `insertnd()` [insertnd.c:15], which is called from the INSERT operation. It is **not** on any path reachable from `deletend()`, `recombine()`, `recombinend()`, `takeovernephewsnd()`, or `eatbrossubtreend()`.

---

### 4. Summary

| Step | What Happens |
|------|-------------|
| DELETE issued | `dodeletevspan()` [do1.c:158] → `deletevspanpm()` → `deletend()` [edit.c:31] |
| Surviving crums shifted | `tumblersub(&ptr->cdsp.dsas[index], width, ...)` [edit.c:63] per crum |
| Post-delete hook | `recombine(father)` [edit.c:75] |
| `recombine` for POOM | `recombinend()` [recombine.c:32, 104] — merges **internal tree nodes** by capacity |
| I-contiguity check | **Never happens** — `isanextensionnd` is INSERT-only [insertnd.c:250] |
| Result | Two formerly non-adjacent crums that are now I-address-contiguous **remain as separate crums permanently** |

The `recombine` step is a tree-balance operation over internal enfilade nodes, not a content-level compaction of leaf crums. Nothing in the delete path looks at whether the I-address `reach` of one surviving crum now equals the I-address `origin` of its neighbor. That adjacency check (`isanextensionnd`) is wired only into the insertion code path, where it prevents creating a redundant new crum when an extension is being appended.

**The POOM enfilade therefore accumulates permanent leaf-level fragmentation through repeated delete/insert cycles.** Each contiguous run that was once a single crum can be split into arbitrarily many separate crums, and no compaction ever re-merges them except when new content is appended at exactly the right address during a subsequent insert.
