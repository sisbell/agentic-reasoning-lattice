## Question 16 [evidence]

> For a deeply orphaned link whose endpoint content has been deleted from every POOM, does the count still include it via its never-removed spanfilade endset entries, or is there an I→V filtering step (as in FOLLOWLINK's `span2spanset`) — i.e., can a count of zero coexist with matching link orgls still present in the granfilade?

## KB Synthesis

## Answer

Yes, a count of zero can coexist with the link orgl permanently present in the granfilade. The reason is not an I→V filtering step analogous to FOLLOWLINK's `span2spanset`, but rather a failure at the upstream content-based search stage.

### How FINDNUMOFLINKSFROMTOTHREE works

[SS-FIND-LINKS, Finding 0035] establishes that FINDNUMOFLINKSFROMTOTHREE is a trivial wrapper that calls `findlinksfromtothreesp()` to materialize matching links, then counts them. `findlinksfromtothreesp()` is identical in search semantics to FINDLINKSFROMTOTHREE — it does not add or remove I→V filtering.

The search pipeline for FINDLINKS is [SS-FIND-LINKS, Finding 0028]:

1. The caller supplies a **V-specset**
2. That V-specset is converted to I-addresses via the POOM of some document
3. Those I-addresses are matched against the spanfilade's link-endset index (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN)
4. Matching link ISAs are returned and counted

There is **no** I→V filtering on the found links themselves. FINDLINKS returns link ISAs, not resolved V-spans, so it has no need for the `span2spanset` / `linksporglset2specset` filtering that FOLLOWLINK performs.

### Why the deeply orphaned link isn't counted

The link's endpoint I-addresses are **permanently** present in the spanfilade link-endset index [INV-SPANF-WRITE-ONLY]. The entries never disappear. But the search reaches those entries only if step 2 above produces I-addresses that overlap with them.

Since the endpoint content has been deleted from every POOM, no V-specset from any document can yield those I-addresses through V→I conversion. The POOM no longer maps any V-position to those I-addresses [ST-DELETE, FC-GRANF-ON-DELETE]. The spanfilade entries are permanently present but unreachable by any content-based query.

[EC-ORPHANED-LINK, Finding 0005] directly confirms this:

> "it cannot be discovered via `find_links()` because no document contains content identities matching its endpoints"

And the full deletion matrix from [EC-ORPHANED-LINK, Finding 0024] shows: **Both source & target deleted → `find_links` returns Empty**.

### The contrast with FOLLOWLINK

FOLLOWLINK uses a fundamentally different access path [SS-FOLLOWLINK, Finding 0048]:

- **FOLLOWLINK**: Direct ISA lookup → reads link orgl from granfilade → *then* calls `linksporglset2specset()` → `span2spanset()` → I→V filtering that silently drops unreferenced I-addresses → empty result
- **FINDLINKS**: V-specset → I-addresses (via POOM) → spanfilade search → fails to reach the link's entries because search I-addresses don't overlap → count = 0

The zero count arises at different points in the pipeline:
- FINDLINKS: zero because the **search can't reach** the link's spanfilade entries
- FOLLOWLINK: link **is found** (directly by ISA), then I→V filtering produces empty spans [INV-ITOV-FILTERING]

### Summary

A count of zero coexists with the link orgl in the granfilade because FINDNUMOFLINKSFROMTOTHREE's underlying search requires I-address overlap between the query and the link's stored endpoints. The link's spanfilade endset entries are permanent [INV-LINK-PERMANENCE, INV-SPANF-WRITE-ONLY], but they can only be reached if the query's POOM-derived I-addresses intersect them — which is impossible once the endpoint content is deleted from every document. No I→V filtering step in FINDLINKS is needed to explain the zero count; the exclusion happens earlier in the pipeline at the V→I conversion of the search specset.

---

## Code Exploration

I now have a complete picture from the code. Here is the full analysis.

---

## Answer

### The Short Answer

Yes: **a count of zero can coexist with matching link orgls still present in the granfilade.** The count path filters through V→I POOM conversion at its *input* step. When endpoint content has been deleted from the POOM via `deletevspan`, that conversion returns empty — the link's spanfilade endset entries and granfilade orgl are both still present but are structurally unreachable via any V-spec query.

---

### The Count Path, Step by Step

**`fns.c:204–217`** — `findnumoflinksfromtothree`:
```c
void findnumoflinksfromtothree(typetask *taskptr)
{
  ...
  dofindnumoflinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, homeset, &numberoflinks)
}
```

**`do1.c:355–359`** — `dofindnumoflinksfromtothree`:
```c
bool dofindnumoflinksfromtothree(...) {
  return findnumoflinksfromtothreesp (taskptr, spanf, fromvspecset, ...);
}
```

**`spanf1.c:105–115`** — `findnumoflinksfromtothreesp`:
```c
bool findnumoflinksfromtothreesp(...) {
  typelinkset linkset;
  if (!findlinksfromtothreesp (taskptr, spanfptr, fromvspecset, ...))
          return(FALSE);
  for (n = 0; linkset; linkset = linkset->next, ++n);
  *numptr = n;
  return (TRUE);
}
```
The count is just the length of the list returned by `findlinksfromtothreesp`.

---

**`spanf1.c:56–103`** — `findlinksfromtothreesp` — this is where the critical branch is:

```c
if (fromvspecset)
        specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
...
if (fromvspecset) {
        sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
        if (!fromlinkset) {
                *linksetptr = NULL;
                return (TRUE);   // <--- returns success with zero links
        }
}
```

If `fromsporglset` is empty after the `specset2sporglset` call, `fromlinkset` will be NULL and the function returns immediately with `*linksetptr = NULL`. The spanfilade is never even queried in the intersection step.

---

### The V→I Gate: `specset2sporglset` → `vspanset2sporglset`

**`sporgl.c:14–33`** — `specset2sporglset`:
```c
for (; specset; ...) {
    if (... itemid == ISPANID) {
        // direct I-span: no POOM lookup — bypasses the gate
    } else if (... itemid == VSPECID) {
        if (!(sporglsetptr = vspanset2sporglset (taskptr, &vspec->docisa,
                                                 vspec->vspanset, sporglsetptr, type)))
                return (FALSE);
    }
}
```

**`sporgl.c:35–65`** — `vspanset2sporglset`: this is the gating function:
```c
ispanset = NULL;
if (!findorgl (taskptr, granf, docisa, &orgl, type))
        return (NULL);
for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
        for (; ispanset; ispanset = ispanset->next) {
                // build sporgl from ispan
        }
}
```

`vspanset2ispanset` [orglinks.c:397–402] calls `permute` which calls `span2spanset` [orglinks.c:425–454], which calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
        context2span (...);
        ...
}
if (!context) {
        return(targspansetptr);   // returns pointer to unchanged (empty) output
}
```

`retrieverestricted` walks the POOM tree of the document. If the virtual span has been removed by `deletend`, no matching crums exist, `context` is NULL, and `span2spanset` returns with `targspansetptr` unchanged — meaning the output ispanset remains NULL.

Result: `vspanset2sporglset` produces zero sporgls. `specset2sporglset` produces an empty sporglset. `sporglset2linkset` is called with an empty set, its inner loop never executes, `fromlinkset` stays NULL. `findlinksfromtothreesp` short-circuits and returns `*linksetptr = NULL`. Count = 0.

---

### Why the Spanfilade Endset Entries Are Never Removed

`deletevspan` calls `dodeletevspan` [do1.c:158–167]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr) {
  ...
  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  );
}
```

`deletevspanpm` [orglinks.c:145–152]:
```c
bool deletevspanpm(...) {
    if (iszerotumbler(&vspanptr->width)) return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates **only** on `docorgl` — the document's POOM. There is no corresponding `deletend` call on `spanf` (the spanfilade). The link endset entries inserted by `insertendsetsinspanf` [do2.c:116–128] at link creation time are **never touched**. A grep across the entire backend confirms there are no `deletelink`, `deletespanf`, `removeendset`, or `deleteorgl` operations anywhere in the codebase.

---

### Why the Link Orgl Also Persists

`createorglingranf` creates the link's orgl in the granfilade at link-creation time [do1.c:209]. There is no API call that removes an orgl from the granfilade. So the link's ISA address remains registered, and `findorgl(linkisa)` would succeed indefinitely.

---

### Contrast with FOLLOWLINK's I→V Filter

`dofollowlink` [do1.c:223–232]:
```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &sporglset->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
```

`link2sporglset` [sporgl.c:67–95] retrieves the endset I-spans from the **link's own POOM** via `retrieverestricted(orgl, vspan, V, NULL, I, ...)`. This is reading the link document's POOM, not the endpoint document's POOM — so it succeeds as long as the link itself has not been deleted.

`linksporglset2specset` [sporgl.c:97–123] → `linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` [orglinks.c:389–394] → `permute` → `span2spanset` → `retrieverestricted` on the **endpoint document's POOM**.

This is the symmetric I→V step that the question refers to. If the endpoint content has been deleted from the endpoint POOM, `retrieverestricted` returns NULL context, `span2spanset` returns empty, and FOLLOWLINK produces an empty vspanset. The orphan is invisible in both directions.

---

### Structural Summary

| Structure | Affected by `deletevspan`? | Survives as orphan? |
|---|---|---|
| Endpoint document POOM (`docorgl`) | **Yes** — `deletend` removes the V→I mapping | V→I returns empty |
| Link spanfilade endset entries | **No** — `deletend` never touches `spanf` | Entries remain, but unreachable via V-spec |
| Link granfilade orgl | **No** — no orgl deletion operation exists | Orgl survives indefinitely |

The V→I POOM conversion is the only filter between a V-spec query and the spanfilade. Once that mapping is gone, the link's endset entries are orphaned in place — present but structurally dark. Count = 0 is therefore fully consistent with the granfilade containing the link's orgl and the spanfilade containing its endset crums. The POOM acts as the live index; the spanfilade and granfilade are append-only and never garbage-collected.
