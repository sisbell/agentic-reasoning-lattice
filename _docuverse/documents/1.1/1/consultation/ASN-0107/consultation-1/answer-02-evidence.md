## Question 2 [evidence]

> Does the udanax-green FINDNUMOFLINKSFROMTOTHREE (or its enumeration path) filter out nullified/deleted links before counting, or count every resident link whose endsets match?

## KB Synthesis

## FINDNUMOFLINKSFROMTOTHREE: Counting Behavior

**Short answer:** It counts every resident spanfilade link whose endpoint I-addresses intersect the query — no explicit filtering, no special nullification pass.

---

### The counting mechanism

[SS-FIND-LINKS/Finding 0035] is definitive:

> FINDNUMOFLINKSFROMTOTHREE is a trivial wrapper around FINDLINKSFROMTOTHREE. It calls `findlinksfromtothreesp()` to materialize the complete linked list of matching links, then walks the list counting elements. There is no count-only optimization.

The same full search executes: V-to-I translation, spanfilade search per endset, `intersectlinksets()` across constraints. Then it linearly counts the result list.

---

### Why there is nothing to filter

**Links cannot be deleted.** [INV-LINK-PERMANENCE] (Findings 0024, 0029, 0040):

> There is no DELETELINK operation in the FEBE protocol. Once created, a link exists forever.

**The spanfilade is append-only.** [INV-SPANF-WRITE-ONLY] (Findings 0057, 0067):

> No deletion function exists anywhere in the spanf codebase. The set of spanfilade entries is monotonically non-decreasing.

Even `DELETEVSPAN(2.x)` on a link's home document removes only the POOM entry. The link orgl in I-space and the spanfilade entries remain intact. [EC-REVERSE-ORPHAN] confirms such a link is **still returned** by `find_links` and therefore still counted.

---

### How apparent "filtering" actually works

The only selectivity comes from the query side, not the result side. The query specset is converted to I-addresses via V-to-I (POOM lookup). If queried content has been deleted from the V-stream, the POOM has no mapping for those V-positions, so the V-to-I step produces no I-addresses, and the spanfilade intersection returns nothing. [SS-FIND-LINKS/Finding 0029]:

> `find_links()` requires that the searched endpoint content exists in the V-stream. If the linked content has been deleted from the V-stream, the intersection is empty and the link is not found.

This is implicit exclusion via empty query input — not explicit filtering of links.

---

### Stale spanfilade entries

[EC-STALE-SPANF-REFERENCE] documents that deleted content leaves stale DOCISPAN entries, but these don't inflate link counts because the count depends on the *link* index, not the DOCISPAN index. A stale DOCISPAN entry affects `find_documents` results, not `find_links` results. The link endpoint entries in the spanfilade are only added at `create_link` time and never removed.

---

**Conclusion:** FINDNUMOFLINKSFROMTOTHREE counts every link in the spanfilade whose endpoint I-addresses satisfy the query intersection. No nullification concept exists; no filtering pass runs. The count reflects all historically created matching links, minus only those whose query I-addresses fail to generate a match (because the searched content is no longer in any V-stream).

---

## Code Exploration

I now have a complete verified trace. Here is my full answer.

---

## FINDNUMOFLINKSFROMTOTHREE: Does it filter nullified/deleted links?

**Short answer: No. It counts every link resident in the spanfilade whose endsets overlap the query spans. There is no filtering for deleted content or nullified links anywhere in the path.**

---

### Call chain

**`fns.c:204`** — FEBE handler (request #29, `requests.h:38`):
```c
void findnumoflinksfromtothree(typetask *taskptr)
{
    if (
       getfindnumoflinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
    && dofindnumoflinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset, homeset, &numberoflinks))
        putfindnumoflinksfromtothree(taskptr, numberoflinks);
```

**`do1.c:355`** — thin pass-through to the spanfilade layer:
```c
bool dofindnumoflinksfromtothree(...)
{
    return findnumoflinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                       threevspecset, orglrangeptr, numptr);
}
```

**`spanf1.c:105-115`** — the counter itself:
```c
bool findnumoflinksfromtothreesp(...)
{
    typelinkset linkset;
    INT n;

    if (!findlinksfromtothreesp(taskptr, spanfptr, fromvspecset, tovspecset,
                                 threevspecset, orglrange, &linkset))
        return(FALSE);
    for (n = 0; linkset; linkset = linkset->next, ++n);   // line 112
    *numptr = n;
    return(TRUE);
}
```

Line 112 is a bare linked-list traversal. No predicate. No state check. Every node in `linkset` increments `n`.

---

### How `linkset` is built — `findlinksfromtothreesp` (`spanf1.c:56-103`)

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);   // line 71
if (tovspecset)
    specset2sporglset(taskptr, tovspecset,   &tosporglset,   NOBERTREQUIRED);   // line 73
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED); // line 75

if (fromvspecset)
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset,
                      orglrange, LINKFROMSPAN);    // line 77
if (tovspecset)
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset,
                      orglrange, LINKTOSPAN);      // line 85
if (threevspecset)
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset,
                      orglrange, LINKTHREESPAN);   // line 93

intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
```

Three independent spanfilade lookups; the result is their intersection. Still no link-state filter.

---

### Spanfilade walk — `sporglset2linksetinrange` (`sporgl.c:239-269`)

```c
for (; sporglset; sporglset = ...) {
    // line 251 — version-filtering kludge permanently disabled:
    if (FALSE /*trying to kluge links followable thru versions*/
        && ((typeitemheader*)sporglset)->itemid == SPORGLID) {
        ...
    } else
        infoptr = NULL;

    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                  &range, ORGLRANGE, (typeisa*)infoptr); // line 259

    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);     // line 265
    }
    contextfree(context);
}
```

`infoptr` is forced to `NULL` by the `if (FALSE...)` at line 251. Every matching context node is added to the linkset unconditionally.

---

### Enfilade tree walk — `crumqualifies2d` (`retrie.c:270-310`)

The only per-node guard in the retrieval path:

```c
// line 274
if ((crumptr->height == 0) && infoptr
    && !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc))) {
    return(FALSE);
}
```

This `homedoc` check fires only when `infoptr != NULL`. Because `sporglset2linksetinrange` forces `infoptr = NULL` via the `FALSE` guard at `sporgl.c:251`, this branch is **never taken** in normal operation.

The remaining qualifications (`whereoncrum` span-range intersection checks, lines 282–300) are purely geometric: does the crum's span overlap the query span? That is the match criterion, not a validity/liveness check.

---

### `typelink` has no status field

From `xanadu.h:98-107`:
```c
typedef struct structtypeaddress {
    struct structtypeaddress *next;
    typeitemid  itemid;
    typeisa     address;
} typeaddress;

typedef typeaddress  typelink;
typedef typelink    *typelinkset;
```

A link is a tumbler address and nothing else. There is no `deleted`, `nullified`, `active`, or any other status flag in the structure.

---

### No DELETELINK operation exists

From `requests.h`, the complete FEBE request set includes:
- `DELETEVSPAN 12` — deletes V-space content from a document poom
- `CREATELINK 27`
- `FINDNUMOFLINKSFROMTOTHREE 29`
- ...

There is no `DELETELINK` request. Once a link is created, it cannot be explicitly deleted via the FEBE protocol.

---

### What DELETEVSPAN does — and does NOT do

`dodeletevspan` (`do1.c:158`):
```c
return (
   findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
);
```

`deletevspanpm` (`orglinks.c:145-152`):
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return(FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

`deletend` operates on `docorgl` — the document's poom tree. It does **not** touch `spanf`, the spanfilade. The spanfilade entries created by `insertendsetsinspanf` (`spanf1.c:15`) during `docreatelink` are permanent; no code path removes them.

---

### Conclusion

**FINDNUMOFLINKSFROMTOTHREE counts every link resident in the spanfilade whose endsets geometrically overlap the query spans. It performs no filtering whatsoever for:**

1. **Links to deleted content** — if V-space content is removed via DELETEVSPAN, the spanfilade entries mapping those V-positions to link I-space addresses survive intact. The link is still counted.

2. **Links themselves "being deleted"** — there is no delete-link operation in the FEBE protocol (`requests.h`), no nullification flag in `typelink` (`xanadu.h:98-102`), and no code path that removes an entry from the spanfilade after creation.

3. **Version/document filtering** — the one guard that could have filtered by `homedoc` is permanently short-circuited by `if (FALSE...)` at `sporgl.c:251`.

The system is designed with append-only semantics for link metadata: links are written into the spanfilade at creation time (`insertendsetsinspanf`, `spanf1.c:15`), and the spanfilade is never pruned. FINDNUMOFLINKSFROMTOTHREE reflects the raw content of the spanfilade for the queried span region.
