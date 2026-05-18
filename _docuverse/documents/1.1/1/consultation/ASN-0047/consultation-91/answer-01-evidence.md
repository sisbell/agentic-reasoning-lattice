## Question 1 [evidence]

> When `dounlinkdoc` or the equivalent link-withdrawal path executes in udanax-green, does the link's V-position in the document arrangement persist as a tombstone, or is the arrangement contracted? What does the spanfilade look like after withdrawal at an interior link position?

## KB Synthesis

## Link Withdrawal in udanax-green

The KB does not mention `dounlinkdoc` by name. The mechanism described for removing a link from a document is `DELETEVSPAN` targeting the 2.x link subspace, handled by `dodeletevspan` → `deletevspanpm` → `deletend`.

### POOM: Contracted, Not Tombstoned

The POOM entry is **physically removed**, not tombstoned. `deletend` uses Case 1 (`disown` + `subtreefree`) for crums entirely within the deletion range, followed by `setwispupwards` and `recombine` rebalancing. The link crum is freed from memory; the arrangement contracts [ST-DELETE, Finding 0040].

```
Before DELETEVSPAN(2.1):
  POOM: V(2.1) → link orgl ISA (present)
  vspanset (output): [{"start": "0", "width": "0.1"}, {"start": "1", "width": "1"}]

After:
  POOM: entry freed (no tombstone)
  vspanset: [{"start": "1.1", "width": "0.11"}]
```

[SS-THREE-LAYER-MODEL]

### Interior Positions: No Shift

When deleting a link at interior position 2.2 (width `0.1`, exponent `-1`), adjacent links at 2.3, 2.4, etc. are **not shifted**. The deletion knife blades are `[2.2, 2.3)`. The link at 2.3 is classified Case 2 (shift), but `tumblersub(2.3, 0.1)` via `strongsub` hits the exponent guard — `0.1.exp(−1) < 2.3.exp(0)` — and returns `2.3` unchanged [FC-SUBSPACE, Finding 0055; INT-DELETE-SUBSPACE-ASYMMETRY].

This leaves a gap in the V-position sequence (`2.1`, *[gap]*, `2.3`). Unlike text deletion in 1.x where same-exponent entries shift, link deletions using a 0.1-width span do not shift peer links.

### Spanfilade: Entirely Unchanged

The spanfilade is **write-only** — no deletion function exists in `spanf1.c` or `spanf2.c`. After link withdrawal [INV-SPANF-WRITE-ONLY, Finding 0057]:

- The link's DOCISPAN entry persists → `find_links()` by content identity still returns the link
- The link orgl persists in I-space → `follow_link(link_id)` still works
- The removed document has no POOM entry, but spanfilade still claims it "contains" the link's I-addresses (stale reference) [INT-DELETE-SPANF-DIVERGENCE, EC-STALE-SPANF-REFERENCE]

This produces the "reverse orphan" state: `retrieve_vspanset(doc)` shows no link span, but `find_links(source_content)` and `follow_link(link_id)` both succeed [EC-REVERSE-ORPHAN, FC-LINK-DELETE-ISOLATION].

### Summary

| Layer | After Withdrawal |
|-------|-----------------|
| POOM (2.x) | Crum freed via `subtreefree`; no tombstone; peers not shifted |
| I-space (link orgl) | Permanent; unchanged [INV-LINK-PERMANENCE] |
| Spanfilade | Append-only; all entries persist; link remains discoverable |

---

## Code Exploration

I now have all the information needed to give the complete answer. Let me also verify the `insertendsetsinspanf` wiring from `spanf1.c:15-54` is well understood for the final answer on spanfilade state.

---

## Answer

### The Premise Is Wrong: `dounlinkdoc` Does Not Exist

**There is no link withdrawal operation in udanax-green.** A grep of the entire `backend/` tree for `dounlinkdoc`, `unlinkdoc`, `withdrawlink`, `deletelink`, and variants returns zero matches. `requests.h` enumerates all 40 FEBE protocol operations (line 20: `#define NREQUESTS 40`), and none is a link deletion or withdrawal:

```c
// requests.h — complete operation list, links highlighted:
#define CREATELINK               27
#define RETRIEVEENDSETS          28
#define FINDNUMOFLINKSFROMTOTHREE 29
#define FINDLINKSFROMTOTHREE     30
#define FINDNEXTNLINKSFROMTOTHREE 31
#define FOLLOWLINK               18
```

No `DELETELINK`, `WITHDRAWLINK`, `UNLINKDOC`. Links are created and queried. They are never withdrawn.

---

### What a Link Actually Is in the Arrangement

`docreatelink` [do1.c:195-221] wires a link into three separate structures:

**1. The document's POOM — the link ISA gets a V-slot**

```c
// do1.c:207-212
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)  // link gets a global ORGL
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)        // convert ISA → I-span
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)          // find V-slot in document
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         // write ISA into doc POOM
```

`findnextlinkvsa` [do2.c:151-167] computes where in the document's V-space the link's ISA reference lives:

```c
// do2.c:156-165
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2.0
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1

(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);   // first link: V = 2.1
else
    movetumbler (&vspanreach, vsaptr);  // subsequent: V = current reach
```

Link ISA references occupy V ≥ 2.1 in the document arrangement. Text occupies V ∈ [1.1, 2.0). `findvsatoappend` [orglinks.c:37] confirms the boundary: `tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart)` — link space starts at V = 2.0.

**2. The link's own ORGL — endpoint specs stored at fixed internal V-positions**

`setlinkvsas` [do2.c:169-183] assigns the three endpoint slots at fixed relative positions inside the link's own ORGL:

```c
fromvsa = 1.1   // mantissa[0]=1, mantissa[1]=1
tovsa   = 2.1   // mantissa[0]=2, mantissa[1]=1
threevsa= 3.1   // mantissa[0]=3, mantissa[1]=1
```

These are internal to the link ORGL, not the document POOM.

**3. The global spanfilade — endpoint I-addresses indexed by link ISA**

`insertendsetsinspanf` [do2.c:116-128] calls `insertspanf` three times with span types `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [xanadu.h:36-38]. The spanfilade stores a 2D index: ORGLRANGE = the link ISA (with endpoint type prefix), SPANRANGE = the endpoint's permascroll I-address.

---

### The Nearest Approximation to Link Withdrawal: `DELETEVSPAN` on the Link's V-Slot

If `DELETEVSPAN` (request 12) is called on the V-range occupied by a link's ISA reference in the document POOM, the call chain is:

```
fns.c:333  deletevspan()
  do1.c:158  dodeletevspan(taskptr, docisaptr, vspanptr)
    orglinks.c:145  deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
      edit.c:31  deletend(docorgl, &vspanptr->stream, &vspanptr->width, V)
```

`deletevspanpm` [orglinks.c:145-152]:

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

Only `deletend` and `logbertmodified`. The spanfilade is not touched. The link's own ORGL is not touched.

---

### `deletend` Contracts the Arrangement — No Tombstone

`deletend` [edit.c:31-76]:

```c
movetumbler (origin, &knives.blades[0]);        // edit.c:40
tumbleradd (origin, width, &knives.blades[1]);  // edit.c:41
knives.nblades = 2;
knives.dimension = index;                        // index = V
makecutsnd (fullcrumptr, &knives);               // split crums at deletion boundaries
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
...
for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
    next = (typecuc *) findrightbro((typecorecrum*)ptr);
    switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
      case 1:                           // edit.c:58 — crum entirely inside deleted range
        disown ((typecorecrum*)ptr);
        subtreefree ((typecorecrum*)ptr);   // DELETED: no trace remains
        break;
      case 2:                           // edit.c:62 — crum after deleted range
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);  // edit.c:63
        break;
    }
}
setwispupwards (father, 1);
recombine (father);
```

**Case 1** (crums inside the deleted span): `disown` + `subtreefree`. Completely removed. No tombstone.

**Case 2** (crums after the deleted span): `tumblersub(..., width, ...)` — their V-displacement is decremented by the deletion width. All subsequent crums shift down.

**The V-space contracts.** If link 1 occupies V = [2.1, 2.2) and link 2 occupies V = [2.2, 2.3), deleting link 1 removes its crum from the POOM tree and subtracts `width=0.1` from link 2's displacement: link 2 now sits at V = [2.1, 2.2). There is no gap, no tombstone, no placeholder.

---

### Spanfilade State After Deletion at an Interior Link Position

This is the crux of the asymmetry: **`DELETEVSPAN` operates only on the document's POOM.** It does not update the spanfilade.

After calling `DELETEVSPAN` on link L's V-slot in document D:

| Structure | State |
|---|---|
| Document D's POOM | Link L's ISA crum removed; all later crums shifted down by L's width |
| Link L's own ORGL (granfilade) | Untouched. from/to/three endpoint data still present |
| Spanfilade LINKFROMSPAN entries for L | Untouched. L's from-endpoint I-address still indexed under L's ISA |
| Spanfilade LINKTOSPAN entries for L | Untouched. Same |
| `findlinksfromtothree` result | L is still returned — it's found via spanfilade, not via document POOM |
| `retrievedocvspanset` result for D | L's V-range no longer present — the document doesn't "contain" L anymore |

`findlinksfromtothreesp` [spanf1.c:56-103] searches the spanfilade by I-address range. It has no dependency on the document's POOM. So a "deleted" link is still a live link in the global sense — it simply no longer has a V-position in that document's arrangement. `followlink` still works on it.

---

### Summary

1. **`dounlinkdoc` does not exist.** This function name is not present anywhere in the codebase. There is no link withdrawal operation in the FEBE protocol.

2. **The document's V-arrangement contracts, not tombstones.** If `DELETEVSPAN` is called on the V-range containing a link's ISA reference, `deletend` [edit.c:31-76] surgically removes the crum and shifts all subsequent crums' displacements down by `tumblersub` [edit.c:63]. No gap is left.

3. **The spanfilade is not updated.** `deletevspanpm` [orglinks.c:145-152] calls only `deletend` on the POOM and `logbertmodified`. The link's `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` records in `spanf` survive intact. The link's own ORGL also survives intact.

4. **The result is a dangling link.** After calling `DELETEVSPAN` on a link's V-slot, the link exists in the global index (findable via `findlinksfromtothree`) but has no V-position in the document arrangement (not visible via `retrievedocvspanset`). There is no mechanism in this codebase to remove a link from the spanfilade or destroy its ORGL.
