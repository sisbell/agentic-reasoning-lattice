## Question 1 [evidence]

> In the udanax-green link search, when a matching link's endset spans multiple content I-addresses, does the insertion-sort that builds the result list key on the specific I-address through which discoverability was established in that traversal (so the key differs if a later traversal matches the link via a different endpoint), or on a fixed/canonical I-address derived from the endset alone (e.g., the least covered I-address, independent of which endpoint currently matches)?

## KB Synthesis

## Answer

The KB cannot definitively resolve this question. Here is what it does and does not establish.

---

### What the KB tells us about the accumulation mechanism

[SS-CONTEXT-LIST] and [INV-RETRIEVAL-V-SORTED] describe `incontextlistnd()` as performing insertion-sort by `totaloffset.dsas[index]` — "the left boundary in the specified dimension." The sort key is a function of a single dimension parameter `index`, not a compound of multiple fields.

[INV-RETRIEVAL-TREE-INDEPENDENCE] confirms the resulting ordering is independent of the physical B-tree sibling order — the same logical context set always produces the same sorted list regardless of tree structure.

---

### What the KB tells us about SPAN enfilade dimensions

[SS-ENFILADE-TREE Finding 0066] makes the dimension layout explicit:

> For SPAN enfilades, dimension 0 is ORGLRANGE (I-space) and dimension 1 is SPANRANGE (V-space)

So in the spanfilade used for link search:
- `dsas[0]` = ORGLRANGE → the link ISA (orgl address, a fixed canonical property of the link)
- `dsas[1]` = SPANRANGE → the content I-address (the specific I-address through which discoverability was established in that traversal)

[INV-RETRIEVAL-V-SORTED] describes the sort as producing "V-sorted" results. If this label maps onto the SPANRANGE dimension (called "V-space" in Finding 0066) when `incontextlistnd` is called during spanfilade traversal, then the sort key is the **content I-address** — i.e., the specific I-address through which the link was found, not a canonical property of the link itself.

---

### The critical gap

The KB does not state which value `index` takes when `incontextlistnd` is invoked during `findlinksfromtothreesp` / `retrievesporglsetinrange`. It is described for the POOM case (where "V-sorted" unambiguously means physical V-address), and for SPAN enfilades the "V-space" label on SPANRANGE in Finding 0066 is made in the context of rebalancing's diagonal sort key — not retrieval's `index` parameter.

---

### What can be inferred from the final result structure

[SS-PAGINATE-LINKS] shows the paginated link result list uses a **link ISA tumbler** as the cursor, scanned by `tumblereq()` match. [SS-FIND-LINKS Finding 0035] notes that `intersectlinksets()` combines per-endpoint result sets. If intermediate per-endpoint lists were sorted by the discovery I-address (SPANRANGE), the same link appearing at multiple matching I-addresses would produce duplicate entries. The intersection step would need to collapse these. Whether that collapsing happens before or within `intersectlinksets` is not described in the KB.

---

### Summary

The KB establishes that `incontextlistnd` sorts by `totaloffset.dsas[index]` [SS-CONTEXT-LIST], that the SPAN enfilade's two dimensions are ORGLRANGE (link ISA) and SPANRANGE (content I-address) [SS-ENFILADE-TREE], and that the final paginated result is navigated by link ISA [SS-PAGINATE-LINKS]. It does not specify which dimension is `index` during spanfilade link-search traversal. The question of whether the sort key is the traversal-specific discovery I-address (SPANRANGE) or the canonical link ISA (ORGLRANGE) is **not answerable from the KB as written**.

---

## Code Exploration

I have all the source I need. Here is the complete answer with full citations.

---

## Answer

**The question's premise is incorrect: there is no insertion-sort in the link-search result-list builder.** The function that accumulates links into the result is `onlinklist` (`spanf2.c:26-44`), which is an **append-with-dedup**. The dedup key is the **link ISA** — the tumbler address of the link document itself — and that key is completely independent of any I-address from the link's endset.

---

### Full call chain

**Entry:** `dofindlinksfromtothree` (`do1.c:348-353`) delegates immediately to `findlinksfromtothreesp`:

```c
bool dofindlinksfromtothree(...) {
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                  threevspecset, orglrangeptr, linksetptr);
}
```

**`findlinksfromtothreesp`** (`spanf1.c:56-103`):

```c
if (fromvspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                      &fromlinkset, orglrange, LINKFROMSPAN);       // line 77
if (tovspecset)
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset,
                      &tolinkset, orglrange, LINKTOSPAN);           // line 85
...
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
```

Each `sporglset2linkset` call builds a flat list of link ISAs that touch the given content I-spans via the named endpoint role. The three lists are then intersected.

**`sporglset2linkset`** (`sporgl.c:222-237`):

```c
if (TRUE||!homeset) {           // guard always fires — homeset is always overridden
    nullhomeset.width.mantissa[0] = 100;
    homeset = &nullhomeset;
}
for (; homeset; homeset = homeset->next)
    sporglset2linksetinrange(taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
```

The `TRUE||` short-circuit at `sporgl.c:227` means the caller-supplied `homeset` is always discarded. The search always runs over the full orgl range (width 100).

**`sporglset2linksetinrange`** (`sporgl.c:239-269`) — the innermost loop:

```c
for (; sporglset; sporglset = ...) {         // walk every I-span in the query
    if (orglrange) {
        prefixtumbler(&orglrange->stream, spantype, &range.stream);   // line 257
        prefixtumbler(&orglrange->width, 0, &range.width);            // line 258
        context = retrieverestricted(spanfptr, (typespan*)sporglset,
                     SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);// line 259
    }
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);      // line 264
        onlinklist(taskptr, linksetptr, &linksa);                      // line 265
    }
    contextfree(context);
}
```

`retrieverestricted` queries the spanfilade asking: *which ORGLRANGE entries (link ISAs, prefixed with `spantype`) overlap this SPANRANGE I-span?* It returns context records whose `totaloffset.dsas[ORGLRANGE]` encodes `spantype ++ linkISA`. `beheadtumbler` strips the `spantype` prefix, leaving the bare link ISA in `linksa`.

**`onlinklist`** (`spanf2.c:26-44`) — the actual list builder:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr)
{
    linkset = makelinkitem(taskptr, linkisaptr);     // new node: only stores linkisa

    if (*linksetptr == NULL) {
        *linksetptr = linkset;
        return(0);
    }
    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq(&temp->address, linkisaptr))  // dedup key = link ISA
            return(0);
    }
    temp->next = linkset;   // append at end
}
```

The result node is built by `makelinkitem` (`spanf2.c:122-135`):

```c
typelink *makelinkitem(typetask *taskptr, typeisa *linkisa)
{
    link = (typelink *) taskalloc(taskptr, sizeof(typelink));
    movetumbler(linkisa, &link->address);    // only field: the link ISA
    link->itemid = LINKID;
    link->next = NULL;
    return (link);
}
```

And `typelink` (`xanadu.h:98-106`) has exactly three fields:

```c
typedef struct structtypeaddress {
    struct structtypeaddress *next;
    typeitemid itemid;
    typeisa    address;    // = the link's tumbler ISA — nothing else
} typeaddress;
typedef typeaddress typelink;
```

---

### Direct answers to the question

**Is the "sort key" the specific I-address through which discoverability was established (varies per traversal)?**

No. `onlinklist`'s dedup check is `tumblereq(&temp->address, linkisaptr)` (`spanf2.c:39`), where `temp->address` is the link ISA and `linkisaptr` is the link ISA just extracted by `beheadtumbler` at `sporgl.c:264`. Neither the current query I-span nor any I-address from the link's endset appears anywhere in this comparison or in the stored node.

**Is the "sort key" a fixed/canonical I-address derived from the endset alone (e.g., the least covered)?**

No. No endset I-address is ever extracted, stored in, or compared against the result list. The `typelink` node has no field for it.

**What actually happens when a link's endset spans multiple I-addresses?**

`sporglset2linksetinrange` walks every I-span in the query sporglset (`sporgl.c:250`). For each query I-span, `retrieverestricted` finds all link ISAs whose stored endset overlaps it. If a link's stored endset covers N query I-spans, the same `linksa` will be handed to `onlinklist` N times. The first call appends the link; subsequent calls hit the `tumblereq` duplicate check and `return(0)` silently (`spanf2.c:39-40`). Only one copy of the link ISA ends up in the list.

**What determines the position of the link in the result list (i.e., the ordering)?**

Pure traversal order: the position is set by whichever query I-span first yields a match for that link during the outer loop in `sporglset2linksetinrange`. Within a single `retrieverestricted` call, context records come back in enfilade traversal order (ORGLRANGE order, i.e., ascending link ISA order). Across different query I-spans, the first I-span to encounter a link "wins" its position. This is incidental, not a deliberate sorted insertion, and no canonical endset I-address is involved.

---

### Summary

There is no insertion-sort. The accumulation function `onlinklist` is append-with-dedup. The identity key for dedup is the **link ISA** (`typeisa address` in `typelink`), derived by stripping the endpoint-type prefix from the ORGLRANGE context offset (`beheadtumbler` at `sporgl.c:264`). This key is the same regardless of which I-address in the link's endset happened to match the query during this traversal. Neither the traversal-specific I-address (option A) nor a canonical endset I-address (option B) plays any role.
