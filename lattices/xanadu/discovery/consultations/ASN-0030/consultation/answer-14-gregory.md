## Question 14 [gregory]

> When FOLLOWLINK resolves endset I-addresses back to V-addresses via `span2spanset`, what exactly happens at the I→V conversion step for an I-address that exists in the granfilade but appears in zero POOMs — is the filtering per-span or per-byte?

## KB Synthesis

The filtering is **per-span** (per sporgl / per I-span), not per-byte. Here's the precise mechanism:

**The conversion chain** [SS-FOLLOWLINK]:

`link2sporglset()` extracts I-address spans from the link orgl via `retrieverestricted()` against the link orgl itself (granfilade read, no POOM involved at this stage). This produces a sporglset — each sporgl carries `(origin: IAddress, width: TumblerWidth, source_doc: ISA)`.

`linksporglset2specset()` then calls `span2spanset()` per sporgl, which calls `retrieverestricted()` against the **queried document's POOM**. This is the filtering step.

**What happens at zero-POOM I-spans** [INV-ITOV-FILTERING]:

`retrieverestricted()` searches the document's POOM B-tree for crums whose I-address range overlaps the query span. If the I-address exists in the granfilade but no POOM in the queried document maps it, `retrieverestricted()` returns NULL. `span2spanset()` at `orglinks.c:446-448` detects this and silently skips the span — no V-span is added to the result.

**Granularity is per-sporgl, not per-byte:**

The sporgl represents a contiguous I-address range. The drop-or-keep decision operates on that entire range when `retrieverestricted()` returns NULL. However, if only *part* of an I-span has POOM mappings (e.g., the span covers I-addresses `a..a+10`, but the POOM only maps `a..a+3`), `retrieverestricted()` returns context entries for just the mapped sub-range — `incontextlistnd()` assembles those into V-spans [SS-CONTEXT-LIST]. So partial presence yields partial V-span results.

**Observable consequences** [EC-GHOST-LINK]:

- All I-spans unreferenced → empty result `[]`, operation succeeds (not an error)
- Some I-spans unreferenced → partial result, only live I-spans converted
- The call chain is identical for FOLLOWLINK and RETRIEVEENDSETS — both share `linksporglset2specset()` [SS-RETRIEVE-ENDSETS]

The granfilade is irrelevant to this filtering step. The granfilade stores the content bytes permanently [INV-IADDR-IMMUTABILITY]; whether those bytes are visible through any POOM is a separate question answered entirely by the POOM lookup.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## I→V Conversion in `span2spanset`: Per-Span or Per-Byte?

The I→V conversion that happens when FOLLOWLINK resolves endset I-addresses to V-addresses runs through two distinct filtering phases. For an I-address that exists in the granfilade but has **zero POOM crums** in the target document, the answer is: **the filtering is per-span (per-crum), and the entire I-span is dropped atomically** — the per-byte clipping phase is never reached.

---

### Full Call Chain

**`followlink` [fns.c:114-127]** → `dofollowlink`

```c
void followlink(typetask *taskptr)
{
  ...
  if (
     getfollowlink (taskptr, &linkisa, &whichend)
  && dofollowlink (taskptr, &linkisa, &specset, whichend)){
      putfollowlink (taskptr, specset);
```

**`dofollowlink` [do1.c:223-232]** is the pivot. It performs two steps:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

**Step 1 — `link2sporglset` [sporgl.c:67-95]**: Looks up the link's own POOM by V-address (`whichend` maps to a V-address like `0.1.1` for FROM, `0.2.1` for TO). Calls `retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)` to extract I-spans from that POOM. These become sporgls — records of `(homedoc, ispan_origin, ispan_width)`.

**Step 2 — `linksporglset2specset` [sporgl.c:97-123]**: For each sporgl with a non-zero `sporgladdress`, calls `linksporglset2vspec` [sporgl.c:127] → `sporglset2vspanset` [sporgl.c:141] → `ispan2vspanset` [orglinks.c:389].

```c
// sporglset2vspanset [sporgl.c:150-157]
sporglptr = (typesporgl *)*sporglsetptr;
(void) findorgl (taskptr, granf, homedoc, &orgl, type);
ispan.itemid = ISPANID;
ispan.next = NULL;
movetumbler (&sporglptr->sporglorigin, &ispan.stream);
movetumbler (&sporglptr->sporglwidth, &ispan.width);
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

**`ispan2vspanset` [orglinks.c:389-393]**: Immediately delegates to `permute` with the I→V direction:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

**`permute` [orglinks.c:404-422]**: Iterates over each span in the input spanset and calls `span2spanset` once per span:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

This is the **per-span loop**: each I-span is processed atomically as a unit.

---

### The Core I→V Lookup: `span2spanset` [orglinks.c:425-454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                           INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  typespan foundspan;
  typespan *nextptr;
  typeitem *onitemlist();

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL);

    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    if(!context){
        return(targspansetptr);      // ← zero-POOM exit point
    }
    contextfree (context);
    return (&nextptr->next);
}
```

There are two phases here. The `if(!context)` guard at line 446 is the zero-POOM exit.

---

### Phase 1 — Per-Crum Filtering: `retrieverestricted` → `findcbcinarea2d` → `crumqualifies2d`

`retrieverestricted` [retrie.c:56-85] converts the I-span into `span1start`/`span1end` bounds:

```c
if (span1ptr) {
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd (&span1start, &span1ptr->width, &span1end);
} else {
    tumblerclear (&span1start);
    tumblerclear (&span1end);
}
```

Since `span2ptr = NULL` (no V-restriction), `span2start` and `span2end` are cleared to zero. Then it calls `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229].

`findcbcinarea2d` [retrie.c:229-268] walks the POOM crum tree, calling `crumqualifies2d` on every crum:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

`crumqualifies2d` [retrie.c:270-305] performs span-level intersection for both I and V dimensions using `whereoncrum`. For the I-dimension:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER){
    return(FALSE);   // query ends before or at crum's left edge
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME){
    return (FALSE);  // query starts at or after crum's right edge
}
```

`whereoncrum` [retrie.c:345-398] for a POOM crum computes:

```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
tumbleradd (&left, &ptr->cwid.dsas[index], &right);
// then returns TOMYLEFT / ONMYLEFTBORDER / THRUME / ONMYRIGHTBORDER / TOMYRIGHT
```

The qualification test is: **does the crum's I-address range `[left, right)` overlap the query `[span1start, span1end)`?** This is a span-level test — a single arithmetic comparison per crum edge. There is no iteration over individual bytes.

For the V-dimension: since `span2end` is zero, `iszerotumbler(span2end)` is true at line 292, so `endcmp = TOMYRIGHT`, which means the V constraint is unbounded — any V-address is acceptable. The sole filter is the I-address range.

**If no POOM crums cover the I-address**, `findcbcinarea2d` returns without adding anything to the context list. `retrieverestricted` returns `NULL`. `span2spanset` hits:

```c
if(!context){
    return(targspansetptr);   // orglinks.c:446-448
}
```

The I-span is **dropped as a whole**. The output `vspanset` is unchanged.

---

### Phase 2 — Per-Byte Clipping: `context2span` [context.c:176-212]

This phase only runs for **qualifying crums**. For each context returned by `retrieverestricted`, `span2spanset` calls:

```c
context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
```

`context2span` [context.c:176-212] clips the crum's V-span to exactly match the I-address intersection:

```c
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    // crum starts before the I-restriction: advance V-start by the overshoot
    tumblerincrement (&grasp.dsas[idx2], 0,
                      (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                      &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    // crum ends after the I-restriction: shrink V-end by the overshoot
    tumblerincrement (&reach.dsas[idx2], 0,
                      -tumblerintdiff (&reach.dsas[idx1], &upperbound),
                      &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

This is **per-byte**: the offset arithmetic with `tumblerintdiff` computes exact byte counts. If the query I-span `[15, 25)` partially overlaps a crum covering `[10, 30)` in I-space and `[100, 120)` in V-space, `context2span` outputs V-span `[105, 115)` — shifted by 5 bytes at start, trimmed by 5 bytes at end.

This phase is never reached in the zero-POOM case.

---

### Summary

| Phase | Where | Granularity | Zero-POOM behavior |
|-------|-------|-------------|-------------------|
| Crum qualification | `crumqualifies2d` [retrie.c:270] | Per-crum (span-level) | No crums qualify → NULL context |
| Output clipping | `context2span` [context.c:176] | Per-byte (exact arithmetic) | Never reached |
| Zero-crum exit | `span2spanset` [orglinks.c:446] | Per-span (whole I-span dropped) | Returns unchanged target set |

**The filtering is per-span.** When an I-address exists in the granfilade but appears in zero POOMs for the queried document, `findcbcinarea2d` finds no qualifying crums, `retrieverestricted` returns `NULL`, and `span2spanset` drops the entire I-span in one shot at the `if(!context)` guard [orglinks.c:446]. The per-byte clipping in `context2span` is only invoked for POOM crums that actually contain the I-address; with zero such crums, it never runs. No partial result, no error — the I-span simply produces no V-addresses.
