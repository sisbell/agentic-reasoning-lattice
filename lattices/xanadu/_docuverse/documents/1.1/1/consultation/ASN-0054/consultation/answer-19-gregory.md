## Question 19 [gregory]

> In the 2D POOM enfilade, does the root's I-displacement track the minimum I-address across all entries via `setwispnd`, and does this minimum ever become stale after DELETE removes the entry that held the minimum?

## KB Synthesis

Yes on both counts — with one important nuance on staleness.

## Root I-Displacement Tracks the Minimum

The POOM is a 2D enfilade (per [SS-ENFILADE-TREE Finding 0060], POOM uses `is2dcrum = TRUE`). For all 2D enfilades, `setwispnd` at `wisp.c:171-228` maintains the root's `cdsp` as the minimum displacement across all children in **both** dimensions simultaneously [SS-ENFILADE-TREE Finding 0066]:

> `root.cdsp` is the upper-left corner (minimum address), `root.cdsp + root.cwid` is the lower-right corner (maximum extent)

The `cdsp` field is a multi-dimensional displacement struct (`dsas[I]` and `dsas[V]`). So `root.cdsp.dsas[I]` does track the minimum I-address (ORGLRANGE dimension) across all entries, updated after every insertion by `setwispnd`.

## Does DELETE Cause Staleness?

**No — `setwispupwards` corrects it after every deletion.**

DELETE operates via `deletend` which classifies crums by their V-range:
- **Case 1** (fully within deletion range): `disown` + `subtreefree` — physically removes the crum [ST-DELETE Finding 0064]
- **Case 2** (after deletion range): shifts V-displacement via `tumblersub`, **I-dimension unchanged** [ST-DELETE Finding 0055]

After processing, `deletend` calls `setwispupwards` on the father node [SS-ENFILADE-TREE Finding 0058], which propagates `setwispnd` up to the root. `setwispnd` scans all remaining children, finds the new minimum in every dimension, absorbs it into the parent's `cdsp`, and adjusts children to relative displacements. If the minimum-I-address crum was a case-1 deletion, the new minimum is found among survivors.

The key formula from [SS-ENFILADE-TREE Finding 0066]:

```
setwispnd:
  mindsp = min(child.cdsp) across all children   // both dims
  root.cdsp += mindsp
  each child.cdsp -= mindsp                        // remain relative
```

After the bottom-up `setwispupwards` reaches the root, `root.cdsp.dsas[I]` correctly reflects the minimum I-address of surviving entries.

## The One Complication: Disabled `levelpull`

[SS-ENFILADE-TREE Finding 0058] notes that `levelpull` is disabled, so tree height never decreases after deletions. Empty intermediate nodes persist. However, `setwispnd` on an empty node (no remaining children) clears both `cdsp` and `cwid` to zero [`wisp.c:187-189`], so even the fully-deleted case is handled correctly — it doesn't corrupt the I-displacement tracking, it just leaves a taller-than-necessary tree structure.

**Summary:** Root I-displacement is never stale after DELETE. The `setwispupwards` → `setwispnd` chain that follows every structural modification recomputes the minimum across surviving entries. Staleness could only arise if `setwispupwards` were skipped, but `deletend` always calls it on the father before returning.

---

## Code Exploration

I now have all the source I need. Here is my complete answer:

---

## POOM Root I-Displacement: `setwispnd` and DELETE Staleness

### 1. Does `setwispnd` track the minimum I-address in the root's `cdsp`?

**Yes — by construction, through a bottom-up pass.**

`setwispnd` is the "widditive operation for nd" (N-dimensional enfilades, i.e. POOM and SPAN). Its definition is at `backend/wisp.c:171–228`. The key passage:

```c
/* find new upper-left corner */
movewisp (&ptr->cdsp, &mindsp);                                     // wisp.c:193
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))   {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp,           // wisp.c:195
             (tumbler*)&mindsp, (unsigned)dspsize(ptr->cenftype));
}
```

Starting from the leftmost child's `cdsp`, it takes the element-wise tumbler minimum (`lockmin`) across all surviving children. For POOM, `dspsize(POOM)` covers both the I and V dimensions simultaneously, so **both components of the minimum are recomputed**.

The result `mindsp` is the minimum child-relative displacement. The new absolute `cdsp` for the father is:

```c
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype); // wisp.c:200
```

Then the children's `cdsp` values are re-relativized by subtracting `mindsp`:

```c
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);    // wisp.c:211
```

This ensures the invariant: every internal node's `cdsp` is the minimum displacement of its children relative to itself. At the root, `cdsp` therefore encodes the **absolute minimum I-address** (and V-address) of all entries in the tree.

`setwispnd` is reached via `setwisp` [`wisp.c:121–140`], dispatching on `POOM` or `SPAN`:
```c
case POOM:
    return (setwispnd ((typecuc*)ptr));                           // wisp.c:131
```

And `setwisp` is called in the upward sweep `setwispupwards` [`wisp.c:83–111`]:
```c
for (changed = TRUE; changed && ptr; ptr = father) {
    father = findfather ((typecorecrum*)ptr);
    changed = setwisp ((typecorecrum*)ptr);                       // wisp.c:97
}
```

---

### 2. Does the minimum become stale after DELETE removes the entry that held it?

**No — the minimum is fully recomputed from surviving children after every delete.**

The delete path is:

```
dodeletevspan()       [do1.c:158]
  → deletevspanpm()  [orglinks.c:145]
    → deletend()     [edit.c:31]
      → setwispupwards(father, 1)   [edit.c:74]
```

`deletevspanpm` calls `deletend` with `index = V` [`orglinks.c:149`]:
```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

Inside `deletend`, the loop over children classifies each child via `deletecutsectionnd` [`edit.c:49`]:
- **Case 1** (fully within the deleted V-range): child is removed via `disown` + `subtreefree` [`edit.c:59–60`]
- **Case 2** (after the deleted V-range): child's V-displacement is decremented [`edit.c:63`]
- **Case 0** (before the deleted V-range): left untouched

After the loop, unconditionally:
```c
setwispupwards (father, 1);    // edit.c:74
recombine (father);            // edit.c:75
```

`setwispupwards` cascades `setwispnd` calls upward to the root. At each level, `setwispnd` does a **full rescan of all surviving children** to find the new minimum — it does not cache or increment from the old minimum. If the deleted child held the minimum I-address, the next minimum among the survivors is found fresh.

There is one special case `setwispnd` handles correctly: if delete removes *all* children of a node, `findleftson(father)` returns `NULL`, and both `cdsp` and `cwid` are zeroed [`wisp.c:185–190`]:
```c
if ((ptr = findleftson (father)) == NULL) {
    clear (&father->cdsp, sizeof(father->cdsp));
    clear (&father->cwid, sizeof(father->cwid));
    ivemodified((typecorecrum*)father);
    return (TRUE);
}
```

---

### Summary

| Question | Answer | Key location |
|----------|--------|--------------|
| Does `setwispnd` track minimum I-address in root `cdsp`? | **Yes** — element-wise `lockmin` over all children, propagated bottom-up | `wisp.c:193–196` |
| Does the minimum go stale after DELETE removes the minimum-holding entry? | **No** — `setwispupwards` triggers a full rescan at every level post-delete | `edit.c:74` → `wisp.c:193–196` |

The system is correct for this case: `setwispnd` is not incremental. It always recomputes from the current child set, so no cached minimum survives a delete. The only way staleness could occur would be if `setwispupwards` were not called after a structural change — and the delete path calls it unconditionally at `edit.c:74`.
