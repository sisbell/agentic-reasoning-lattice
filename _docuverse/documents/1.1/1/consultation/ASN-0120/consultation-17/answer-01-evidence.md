## Question 1 [evidence]

> Do the sporgls emitted by `vspanset2sporglset` during CREATELINK always have I-widths tracing exactly the currently-allocated istream content, or can a stored sporgl's width extend past the allocation frontier into not-yet-allocated I-addresses?

## KB Synthesis

Sporgls emitted by `vspanset2sporglset` during CREATELINK always trace **exactly** the allocated istream content. They cannot extend past the allocation frontier.

## Why the widths are bounded precisely

The pipeline is:

```
CREATELINK → domakelink → vspanset2sporglset
  → vspanset2ispanset → permute → span2spanset → retrieverestricted
  → one sporgl per contiguous I-address region in the POOM
```

The sporgl's I-width comes entirely from **POOM crum data**. At the bottom of the tree, each crum stores `origin.dsas[I]` and `width.dsas[I]` — set at INSERT time and never modified afterward [SS-POOM-BOTTOM-CRUM].

## How those I-widths get established

During INSERT, `inserttextingranf` allocates I-addresses via `tumblerincrement(&lsa, 0, textset->length, &lsa)` — advancing by **exactly** the byte count of the text [ST-INSERT, Finding 0031]. The resulting I-span width is `tumblersub(endAddr, startAddr)`, which equals the number of bytes actually written to the granfilade. No rounding, no speculation about future content.

The POOM crum created by `insertpm` stores this exact I-width [SS-POOM-BOTTOM-CRUM, Finding 0076]. The I-width field is a direct copy of the I-span width from `inserttextingranf`.

## What `retrieverestricted` returns

`span2spanset` calls `retrieverestricted` to find all POOM contexts overlapping the query V-span. Each returned context carries the crum's recorded I-address and I-width — both of which were grounded in an actual allocation at creation time. There is no interpolation or projection beyond stored crum boundaries.

## VCOPY preserves the same bounds

When content is transcluded, `insertpm` copies the source I-width into the destination POOM crum unchanged [ST-VCOPY, PRE-COPY]. So transcluded content also has POOM crums whose I-widths match the original allocation exactly.

## Structural impossibility of over-extension

Three invariants together rule out any frontier overshoot:

- **[INV-MONOTONIC]**: I-address allocation is strictly increasing and never backtracks. The allocation frontier only advances.
- **[INV-NO-IADDR-REUSE]**: No I-address is ever freed and reused. The granfilade is append-only.
- **[INV-IADDR-IMMUTABILITY]**: Once written to a POOM crum, I-widths are never modified by any subsequent operation.

Because POOM crum widths are set from actual allocations, and `vspanset2sporglset` reads those widths without modification, the sporgl's I-width cannot describe I-addresses that haven't been allocated. There is no path in the code that could cause a sporgl width to point past the end of written granfilade content.

**Summary**: The sporgls are precise — each one describes an I-address range whose every byte was allocated and written to the granfilade at INSERT or COPY time. The allocation frontier is always ahead of (or at) the maximum extent of any sporgl's `origin + width`.

---

## Code Exploration

Now I have everything needed. I've traced the complete execution path from `createlink` through `vspanset2sporglset` to `context2span`, including the struct layouts. Here is my full analysis.

---

## Answer

### The I-widths in stored sporgls are strictly bounded by existing POOM crum allocations — they cannot extend past the allocation frontier.

---

### Full Call Chain

**Entry point** — `fns.c:100`:
```c
void createlink(typetask *taskptr) {
    if (getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
     && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
```

**`docreatelink`** — `do1.c:195–221`:
```c
return (
     createorglingranf(taskptr, granf, &hint, linkisaptr)   // allocates LINKATOM in granf
  && tumbler2spanset(taskptr, linkisaptr, &ispanset)         // I-span of link atom
  && findnextlinkvsa(taskptr, docisaptr, &linkvsa)           // V-address in hosting doc
  && docopy(taskptr, docisaptr, &linkvsa, ispanset)          // places link in doc's V-space
  && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // <<< HERE
  && specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
  && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
  && setlinkvsas(&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl(taskptr, linkisaptr, link, ...)
  && insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)
);
```

**`specset2sporglset`** — `sporgl.c:14–33` — iterates the specset; for each `VSPECID` item:
```c
sporglsetptr = vspanset2sporglset(taskptr, &((typevspec*)specset)->docisa,
                                  ((typevspec*)specset)->vspanset,
                                  sporglsetptr, type);
```

**`vspanset2sporglset`** — `sporgl.c:35–65`:
```c
typesporglset *vspanset2sporglset(..., typeisa *docisa, typevspanset vspanset, ...)
{
    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type))
        return(NULL);
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);   // V→I via POOM
        for (; ispanset; ispanset = ispanset->next) {
            sporglset = taskalloc(taskptr, sizeof(typesporgl));
            sporglset->itemid = SPORGLID;
            movetumbler(docisa,              &sporglset->sporgladdress);  // home doc
            movetumbler(&ispanset->stream,   &sporglset->sporglorigin);   // I-start
            movetumbler(&ispanset->width,    &sporglset->sporglwidth);    // I-width ← KEY
            *sporglsetptr = (typesporglset)sporglset;
            sporglsetptr = (typesporglset*)&sporglset->next;
        }
    }
    return(sporglsetptr);
}
```

The `sporglwidth` is set directly from `ispanset->width`. Everything turns on where that `ispan` comes from.

---

### How ispanset->width is computed

`vspanset2ispanset` (`orglinks.c:397`):
```c
return permute(taskptr, orgl, vspanset, V, ispansetptr, I);
```

`permute` (`orglinks.c:404`) → calls `span2spanset` for each vspan.

`span2spanset` (`orglinks.c:425`):
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, V, &foundspan, I);   // clip to query, map to I
    nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`retrieverestricted` (`retrie.c:56`) → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229`):

```c
int findcbcinarea2d(typecorecrum *crumptr, ..., tumbler *span1start, tumbler *span1end, INT index1, ...)
{
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumqualifies2d(crumptr, ..., span1start, span1end, index1, ...))
            continue;
        if (crumptr->height != 0) {
            findcbcinarea2d(findleftson(crumptr), ...);   // recurse
        } else {
            context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
            incontextlistnd(headptr, context, index1);
        }
    }
}
```

This traverses **existing crums in the POOM**. Only crums that are actually in the enfilade — i.e., crums that were previously inserted by `insertpm` during a real content insertion — can be found here.

`makecontextfromcbc` (`context.c:151`):
```c
context = createcontext(crumptr->cenftype);
movewisp(offsetptr, &context->totaloffset);        // absolute start of crum in both I and V
movewisp(&crumptr->cwid, &context->contextwid);    // crum's width in both I and V
if (crumptr->cenftype != GRAN)
    dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, crumptr->cenftype);
```

So `context.totaloffset.dsas[I]` = the crum's I-start, and `context.contextwid.dsas[I]` = the crum's I-width — both coming directly from the crum struct's `cwid.dsas[I=0]` and `cdsp.dsas[I=0]` (see `wisp.h:19`: `#define I 0`, `#define V 1`).

---

### The clipping in context2span

`context2span` (`context.c:176`) with `idx1=V`, `idx2=I`:

```c
movetumbler(&restrictionspanptr->stream, &lowerbound);
tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd(context, &grasp, &reach);
// grasp.dsas[V] = crum's V-start;  reach.dsas[V] = crum's V-end
// grasp.dsas[I] = crum's I-start;  reach.dsas[I] = crum's I-end

// Clip left: if crum V-start < query V-lower, advance I-start inward
if (tumblercmp(&grasp.dsas[V], &lowerbound) == LESS)
    tumblerincrement(&grasp.dsas[I], 0, tumblerintdiff(&lowerbound, &grasp.dsas[V]),
                     &grasp.dsas[I]);

// Clip right: if crum V-end > query V-upper, retract I-end inward
if (tumblercmp(&reach.dsas[V], &upperbound) == GREATER)
    tumblerincrement(&reach.dsas[I], 0, -tumblerintdiff(&reach.dsas[V], &upperbound),
                     &reach.dsas[I]);

movetumbler(&grasp.dsas[I], &foundspanptr->stream);
tumblersub(&reach.dsas[I], &grasp.dsas[I], &foundspanptr->width);   // ← ispanset->width
```

This computes the intersection of the client's V-query with each crum's V-extent, then maps that intersection proportionally to the I-dimension (1:1, since the POOM is a permutation matrix). The result is **strictly clipped**:

- If the client's V-span overshoots the crum on the left: the I-start is advanced inward.
- If the client's V-span overshoots the crum on the right: the I-end is retracted inward.
- If the client's V-span extends entirely past the crum: `crumqualifies2d` rejects the crum, so no ispan is produced at all.

In no case does `context2span` widen an I-span beyond the crum's own I-extent.

---

### Why crums cannot reference unallocated I-addresses

POOM crums are created only by `insertpm` (`orglinks.c:75`), which is called as part of `docopy`. `docopy` (`do1.c:45`) is always preceded by `specset2ispanset` which produces `ispanset` from already-inserted granfilade content. Before `docopy`, the actual text/orgl atom must be written to the granfilade via `inserttextingranf` (in `doinsert`) or `createorglingranf` (in `docreatelink`). Those functions allocate the I-addresses. The POOM crum records exactly those I-addresses. There is no "pre-claim" mechanism — crum insertion (`insertnd` at `orglinks.c:130`) follows allocation, never precedes it.

`acceptablevsa` (`do2.c:110`) is nominally the gate for checking V-span validity but:
```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);   // unconditional
}
```

It performs no actual check. However, the specset passed to `specset2sporglset` during `docreatelink` is **the client's own V-span describing existing content they want to link to**, not a new insertion address. If the client names a V-span that extends past existing content, `findcbcinarea2d` simply finds no crums for the out-of-bounds portion and produces no sporgls for those addresses — it doesn't generate phantom sporgls with oversized widths.

---

### Summary

The `sporglwidth` stored in each sporgl emitted by `vspanset2sporglset` is computed by:

1. **`findcbcinarea2d`**: traverses only crums that actually exist in the referenced document's POOM enfilade — crums created only when content was allocated.
2. **`context2span`**: clips each crum's I-extent to the intersection with the client's V-query (can only narrow, never widen).
3. **`vspanset2sporglset`**: copies the resulting I-width directly into `sporglset->sporglwidth`.

A stored sporgl's I-width therefore traces **exactly the allocated istream content** that falls within the client's V-span. It cannot extend past the allocation frontier, because there are no POOM crums pointing to unallocated I-addresses, and `context2span` cannot manufacture I-extent beyond what a crum records.
