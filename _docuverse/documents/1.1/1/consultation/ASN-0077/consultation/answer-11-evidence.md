## Question 11 [evidence]

> When `find_documents_containing` queries the spanfilade with an I-address span, does it return the originating document first or in spanfilade-traversal order?

## KB Synthesis

The KB does not explicitly document the result ordering of `finddocscontainingsp`, but the general 2D enfilade retrieval principles answer this definitively.

**Results come back in document ISA address order, not "originating document first."**

Here's the reasoning:

The SPAN enfilade is a 2D enfilade. All 2D enfilade retrieval accumulates results via `incontextlistnd()`, which performs insertion-sort by the left boundary of each found context in the queried dimension — regardless of the order in which the B-tree traversal discovers them [SS-CONTEXT-LIST]. This ordering is independent of tree structure [INV-RETRIEVAL-TREE-INDEPENDENCE].

For FINDDOCSCONTAINING, the query restricts the SPANRANGE dimension (I-address span) and returns matches along the ORGLRANGE dimension (document ISAs). The `incontextlistnd()` sort key is `totaloffset.dsas[index]` — the document ISA left boundary. Results therefore emerge sorted by document address, ascending.

Since document addresses are monotonically increasing per account [INV-MONOTONIC], the originating document (which INSERTed the content first) may coincidentally have a lower address than documents that later transcluded the content — but this is not guaranteed. A document that transcluded the content but was created under a lower-numbered account would appear first.

**No "originating document first" semantic exists** — the spanfilade index stores I-address→document mappings with no provenance timestamp or origin flag. DOCISPAN entries are per-span granularity [SS-DOCISPAN] and the insertion order into the spanfilade (which could indicate origin) is not preserved in retrieval output.

---

## Code Exploration

I now have everything needed to give a complete, line-cited answer.

---

## Answer: `find_documents_containing` Returns in ORGLRANGE-Ascending (Tumbler) Order — No Originating-Document Priority

### Full Call Chain

```
fns.c:20    finddocscontaining()
  fns.c:28  → dofinddocscontaining()          [do1.c:15]
  do1.c:21  → specset2ispanset()              [do2.c:14]  (V-spec → I-spans)
  do1.c:22  → finddocscontainingsp()          [spanf1.c:151]
```

---

### What `finddocscontainingsp` Does (`spanf1.c:151–188`)

```c
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);   // [168]
tumblerincrement (&docspace.width, 0, 1, &docspace.width);            // [169]
for (; ispanset; ispanset = ispanset->next) {                          // [170]
    context = retrieverestricted (
        (typecuc*)spanf,
        &docspace, ORGLRANGE,      // restrict dim1 to DOCISPAN-prefixed docs
        ispanset,  SPANRANGE,      // restrict dim2 to the query I-span
        (typeisa*)NULL);           // [171]
    for (c = context; c; c = c->nextcontext) {                         // [172]
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);         // [173]
        beheadtumbler (&docid, &document.address);                     // [174]
        if (isinlinklist(*headptr, &document.address)) continue;       // [175]
        ...
        addresssetptr = (typelinkset *) onitemlist(...);               // [179]
    }
}
```

`DOCISPAN = 4` (`xanadu.h:39`). The `docspace` range `[DOCISPAN, DOCISPAN+1)` in tumbler arithmetic covers every document ISA address that has 4 as its leading component — i.e., **all documents** in the spanfilade, not a single origin. There is no concept of "originating document" in this query.

---

### How Results Are Ordered

`retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229`):

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {         // [252]
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), ...);            // [259] recurse
    } else {
        context = makecontextfromcbc (...);                 // [262]
        incontextlistnd (headptr, context, index1);         // [263] index1 = ORGLRANGE
    }
}
```

Every matching leaf crum is inserted via `incontextlistnd(..., ORGLRANGE)`.

`incontextlistnd` (`context.c:74–111`) is an **insertion-sort that maintains ascending ORGLRANGE order**:

```c
/* put c on clist in index order */                         // [74]
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    ...
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;  *clistptr = c; return;    // [90–94] prepend (smaller)
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext(clist,...) > ONMYLEFTBORDER)
             && (whereoncontext(nextc,...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc; clist->nextcontext = c; return; // [98–103] insert middle
            }
        }
    }
    clist->nextcontext = c;                                 // [109–110] append (largest)
}
```

The context list exiting `retrieverestricted` is sorted by **ascending document tumbler address** in the ORGLRANGE dimension.

`finddocscontainingsp` then iterates that sorted list (`spanf1.c:172`) and appends document IDs to the result in that order. `isinlinklist` (`spanf1.c:175`) performs deduplication but imposes no reordering.

---

### Conclusion

`find_documents_containing` returns documents in **ascending ORGLRANGE tumbler order** — i.e., the order imposed by `incontextlistnd`'s insertion-sort keyed on document tumbler address.

The **originating document receives no special treatment**. It appears wherever its document tumbler address falls in the sorted sequence. If it happens to hold the numerically smallest tumbler among the matching documents, it appears first; otherwise it does not.

There is no code path anywhere in `finddocscontainingsp`, `retrieverestricted`, `findcbcinarea2d`, or `incontextlistnd` that identifies, tests for, or promotes the document from which the query I-span was drawn.
