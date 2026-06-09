## Question 2 [evidence]

> Does the back end ever store or index a link whose from- or to-endset is empty, and if so, is that empty slot simply absent from the per-slot link index (so a constrained from/to request never returns it, while a wildcard request still does)?

## KB Synthesis

## Link Endset Storage and the Empty-Slot Question

**Short answer:** The backend never initially stores a link with an empty from- or to-endset. After content deletion, the spanfilade entries persist and the slot is not absent — but constrained queries behave *as if* it were absent for a specific reason.

---

### At Creation Time: Empty Endsets Cannot Exist

Zero-width endpoints crash the backend (Bug 0017) [PRE-LINK-CREATE / Finding 0028]. A `create_link` call with zero-width source or target never completes — no orgl is allocated, no spanfilade entries are written. So a link with an initially empty from- or to-slot is structurally impossible.

At creation, `insertendsetsinspanf()` inserts sporgls for all three endpoint types into the spanfilade, keyed by:
- **SPANRANGE dimension**: the I-addresses of the endpoint content
- **ORGLRANGE dimension**: endpoint type (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3)

[INT-SPORGL-LINK-INDEX / Finding 0013]

---

### After Content Deletion: Entries Persist, But Queries Fail on the Query Side

The spanfilade is write-only [INV-SPANF-WRITE-ONLY / Finding 0057]. No operation removes spanfilade entries — the index slots for both from and to endsets persist permanently after deletion.

What actually changes is the **query path**, not the index. `find_links` first converts the caller's specset through the *querying document's current POOM* (V→I conversion). If that document has deleted the relevant content, V→I conversion returns empty — so the intersection with the (still-present) spanfilade entries is empty, and the link is not returned. [FC-LINK-DELETE-ISOLATION / Finding 0029]

This means:

| Source state | Target state | `find_links(source, NOSPECS)` | `find_links(NOSPECS, target)` |
|---|---|---|---|
| Intact | Intact | Found | Found |
| Deleted | Intact | Not found | Found |
| Intact | Deleted | Found | Not found |
| Deleted | Deleted | Not found | Not found |

The per-slot distinction (LINKFROMSPAN vs LINKTOSPAN) is structural and survives content deletion — these are separate ORGLRANGE subspaces in the spanfilade [SS-RETRIEVE-ENDSETS / Finding 0035]. So a "wildcard" operation that probes both slots can still find a link via its surviving endpoint even after the other endpoint's content is deleted.

---

### Special Case: THREE (Type) Endpoint

If a type specset is provided at creation, LINKTHREESPAN=3 entries are written. If the caller passes NOSPECS for the type, no entries exist in the LINKTHREESPAN subspace for that link — a type-constrained search would never return it. This is the one case where a slot is genuinely absent from the per-slot index.

The anomalous behavior noted in [EC-ORPHANED-LINK / Finding 0024] — `follow_link(link, TYPE)` returning empty when both other endpoints are deleted — is described as unexpected and unexplained by the KB.

---

### Summary

The backend never stores a link with an empty from- or to-endset at creation time (crashes on zero-width). After deletion, the index entries are **not removed** (write-only spanfilade). Constrained queries (`find_links(from=spec, to=NOSPECS)`) fail not because the slot is absent, but because the query-side V→I conversion returns empty — producing the same observable result as absence, through a different mechanism.

---

## Code Exploration

The finding write was denied. Here is the full answer:

---

## Answer: Empty-Endset Links — Storage, Indexing, and Query Asymmetry

### 1. Does the backend store a link with an empty from- or to-endset?

**Yes.** There is no validation guard.

`docreatelink` [do1.c:195–221] calls `specset2sporglset` on all three endsets [do1.c:214–216] and proceeds directly to indexing regardless of whether the results are NULL:

```c
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // do1.c:214
&& specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // do1.c:215
&& specset2sporglset(taskptr, threespecset,&threesporglset,NOBERTREQUIRED)  // do1.c:216
&& setlinkvsas(...)
&& insertendsetsinorgl(...)
&& insertendsetsinspanf(...)
```

The client can send an empty endset: `getspecset` [get2.c:162–192] returns `*specsetptr = NULL` and `TRUE` whenever the client answers `any = false` [get2.c:173–175]. `specset2sporglset` receiving a NULL specset also returns TRUE with `*sporglsetptr = NULL`. No rejection happens anywhere in the chain.

---

### 2. Is the empty slot absent from the per-slot index?

**Yes — in both indexes, via the same mechanism: a `for` loop that silently no-ops on a NULL head pointer.**

#### Spanfilade index (`insertspanf`)

`insertendsetsinspanf` [do2.c:116–128] unconditionally calls `insertspanf` for from and to [do2.c:119–120]:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // do2.c:119
&& insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)    // do2.c:120
```

`insertspanf` [spanf1.c:15–54]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // ... insertnd(...) ...
}
return (TRUE);   // spanf1.c:53
```
[spanf1.c:25–53]

If `sporglset` is NULL, the `for` condition fails immediately. No `insertnd` fires. The function returns TRUE silently. **No spanfilade entry is written for the empty slot.**

#### Orgl (POOM) index (`insertpm`)

`insertpm` [orglinks.c:75–134] has the identical pattern [orglinks.c:100–133]. For the three-endset, `insertendsetsinorgl` [do2.c:136] adds an explicit guard `if (threevsa && threesporglset)` in addition to the implicit loop. From and to rely solely on the loop.

---

### 3. Does a constrained from/to request ever return a link with an empty slot?

**No.** The query early-exits with an empty result.

`findlinksfromtothreesp` [spanf1.c:56–103] — the function behind `dofindlinksfromtothree` [do1.c:348–353] and all `FINDLINKSFROMTOTHREE` FEBE requests — guards each slot lookup:

```c
if (fromvspecset) {                                           // spanf1.c:70
    sporglset2linkset(..., fromsporglset, &fromlinkset, ..., LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }  // spanf1.c:78–82
}
if (tovspecset) {                                            // spanf1.c:84
    sporglset2linkset(..., tosporglset, &tolinkset, ..., LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }    // spanf1.c:86–90
}
```

If the client provides a non-null `fromvspecset` for a link whose from-endset was empty at creation time: the spanfilade has no entry for it, `sporglset2linkset` returns nothing, `fromlinkset` stays NULL, and the early exit fires. **Link not returned.**

---

### 4. Does a wildcard request (NULL specset for the empty slot) still return the link?

**Yes.** The NULL guard at the top of each slot's block means the empty slot's index is never consulted.

When `fromvspecset = NULL` (client sent `any = false`):
- `if (fromvspecset)` at [spanf1.c:70] is false → from index skipped entirely
- `fromlinkset` stays NULL
- `intersectlinksets(taskptr, NULL, tolinkset, NULL, linksetptr)` [spanf1.c:100]

`intersectlinksets` [spanf2.c:46–115] handles this directly:

```c
if  (linkset1 && !linkset2 && !linkset3) *linkset4ptr = linkset1;    // spanf2.c:64
else if (!linkset1 && linkset2 && !linkset3) *linkset4ptr = linkset2; // spanf2.c:66
else if (!linkset1 && !linkset2 && linkset3) *linkset4ptr = linkset3; // spanf2.c:68
```

A NULL in a slot means "unconstrained by that slot." If only `tolinkset` is non-null, it is returned directly [spanf2.c:66]. **Link is returned** if its to-slot was indexed and matches (or to is also wildcarded).

---

### Summary Table

| Scenario | Outcome | Key code |
|---|---|---|
| Create link, empty from-endset | Stored in POOM; no from-slot index entry | `insertspanf` loop [spanf1.c:25], `insertpm` loop [orglinks.c:100] |
| Create link, empty to-endset | Same | Same |
| Query `from=<specset>`, link has empty from | **Not returned** — index miss, early exit | [spanf1.c:78–82] |
| Query `from=NULL` (wildcard), link has empty from | **Returned** if to-slot matches | [spanf1.c:70], [spanf2.c:64–68] |
| Query `from=NULL`, `to=NULL` | All stored links returned | All slot guards false |

The behavior is consistent and emerges from two independent mechanisms operating at opposite ends of the pipeline: a `for (; sporglset; ...)` loop that silently no-ops during index writes, and an `if (vspecset)` guard that skips the slot entirely during index reads.
