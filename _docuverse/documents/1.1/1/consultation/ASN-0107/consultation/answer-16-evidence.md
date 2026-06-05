## Question 16 [evidence]

> After a DELETE removes a link endpoint's V→I mapping from a document's POOM while leaving spanfilade entries intact, does the reported count stay the same or decrease?

## KB Synthesis

**The reported count decreases** when the query is issued from the document whose endpoint content was deleted.

Here is why the stale spanfilade entries do not help:

**FINDNUMOFLINKSFROMTOTHREE** is a trivial wrapper over FINDLINKSFROMTOTHREE — it re-executes the full `findlinksfromtothreesp()` search and counts the resulting list [SS-FIND-LINKS, Finding 0035].

That search has a V→I conversion step as its first act: the query specset is passed through `specset2ispanset` → `permute` → the document's POOM to produce the I-addresses that are then matched against spanfilade entries [SS-FIND-LINKS, Finding 0028]. DELETE removes the V→I entries from the POOM [ST-DELETE, Finding 0064]. With no POOM mappings surviving for those V-addresses, the conversion returns empty — no I-addresses are produced, the spanfilade is never consulted, and the search returns zero results [SS-FIND-LINKS, Finding 0029].

The persistent spanfilade entries matter only for **FIND_DOCUMENTS**, which is queried directly by I-address without a V→I step [INT-DELETE-SPANF-DIVERGENCE, Finding 0057]. For FIND_LINKS the POOM is a prerequisite, not a shortcut.

One exception: if the deleted content was previously transcluded to another document, a query **from that other document** still resolves the same I-addresses through its own intact POOM, finds the same stale spanfilade entries, and returns an unchanged count [INT-TRANSCLUSION-LINK-SEARCH, Finding 0029]. The count only drops when queried from the document that sustained the deletion.

---

## Code Exploration

I now have enough verified data to answer precisely.

---

## Answer

**The reported count DECREASES** — by exactly the width of the deleted V-span. The spanfilade entries are left as orphaned dangling pointers and play no role in the count calculation.

---

### Execution Path: DELETE

**Entry** — `fns.c:307-311`:
```c
bool getretrievedocvspan(), doretrievedocvspan();
    ...
&& doretrievedocvspan (taskptr, &docisa, &vspan)
```

The FEBE delete handler routes to `dodeletevspan` at `do1.c:158-167`:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

There are **two** operations in INSERT for a link endpoint (`do1.c:181-192`): `docopy` (POOM) **and** `insertendsetsinspanf` (spanfilade). DELETE has **one**: `deletevspanpm` only. No `deletespanf` counterpart exists anywhere in the codebase.

**`deletevspanpm`** at `orglinks.c:145-152`:
```c
bool deletevspanpm(..., typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`deletend`** at `edit.c:31-76` classifies each crum in the intersection:
- **Case 1** (`edit.c:58-61`): Crum fully within the deleted range → `disown()` + `subtreefree()` (gone)
- **Case 2** (`edit.c:62-65`): Crum comes after the deleted range → `tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])` (shifted left)
- **Case 0** (`edit.c:56-57`): Crum entirely before range → unchanged

Then `edit.c:74`: `setwispupwards(father, 1)` propagates the structural change upward.

---

### Width Recalculation: `setwispnd` at `wisp.c:171-228`

```c
if ((ptr = findleftson (father)) == NULL) {
    /* All children deleted - clear width and mark modified */
    clear (&father->cwid, sizeof(father->cwid));   // wisp.c:188
    ...
}
...
clear (&newwid, sizeof(newwid));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, ...); // tempwid = cdsp + cwid
    lockmax(&newwid, &tempwid, &newwid, ...);        // newwid = max(endpoints)
}                                                    // wisp.c:207-215
...
movewisp (&newwid, &father->cwid);                  // wisp.c:225
```

The new root `cwid` = **max endpoint of remaining children**. Since Case 2 crums have been shifted left by `width`, every endpoint after the deletion is reduced by `width`. The result: `new_cwid = old_cwid − deleted_width`.

---

### How Count Is Read

`doretrievedocvspan` at `do1.c:312-320` calls `retrievevspanpm` at `orglinks.c:165-172`:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    ...
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);  // line 170
    return (TRUE);
}
```

The reported width is read **directly from the POOM root's `cwid.dsas[V]`** — not from spanfilade entry counts, not from I-span sets, not from link counts. Whatever `setwispupwards` propagated into that field is what the client receives.

---

### The Orphaned Spanfilade Entries

`domakelink` at `do1.c:169-193` inserts into the spanfilade via `insertendsetsinspanf`. After DELETE removes the corresponding POOM crums, the spanfilade entry for that link endpoint's VSA still exists — pointing to a V-address range that no longer exists in the document's POOM. These orphaned entries are never consulted by `retrievevspanpm` or `doretrievedocvspan`, so they have **zero effect** on the reported count.

---

### Summary

| Component | After DELETE | Effect on count |
|-----------|-------------|-----------------|
| POOM crums for link endpoint | Removed by `disown`/`subtreefree` (edit.c:59-60) | Root `cwid` shrinks |
| POOM crums after the deleted span | Shifted left by `width` (edit.c:63) | Endpoints decrease |
| Spanfilade entry | Untouched — no `deletespanf` exists (do1.c:163-167) | None — not read by retrieve |
| Reported count (`cwid.dsas[V]`) | Recomputed by `setwispnd` as max of remaining endpoints (wisp.c:213-215) | **DECREASES** |

The count decreases by exactly the deleted V-span width. The spanfilade's intact entries represent a structural inconsistency — link endpoints registered in the index pointing into virtual address space that the POOM no longer covers — but that inconsistency is invisible to the count path.
