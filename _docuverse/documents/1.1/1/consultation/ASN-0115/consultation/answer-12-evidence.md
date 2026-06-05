## Question 12 [evidence]

> How does content delivery walk the POOM to resolve each VSpec to I-addresses, and does it route through `vspanset2sporglset` before the granfilade lookup?

## KB Synthesis

## Content Delivery: POOM Walk and Granfilade Lookup

The retrieve path does **not** route through `vspanset2sporglset`. The two paths share the same underlying POOM walk (`permute`) but diverge in what they attach to the results.

---

### The Retrieval Call Chain

Content delivery (RETRIEVE_CONTENTS / opcode 5) runs through `doretrievev` with this call chain [PRE-RETRIEVE-CONTENTS]:

```
doretrievev
  → specset2ispanset          (V → I, calls findorgl per referenced doc)
      → permute() V→I direction
          → span2spanset()
              → retrieverestricted()
                  → findcbcinarea2d()   (2D POOM B-tree traversal)
  → ispanset2vstuffset(granf, ispanset)  (granfilade B-tree lookup → bytes)
```

`specset2ispanset` first calls `findorgl` to verify every document in the SpecSet is currently open — an open-document precondition the caller must satisfy [PRE-RETRIEVE-CONTENTS, Finding 0027]. If any referenced document is closed, `findorgl` returns FALSE and the operation fails before the POOM is consulted.

---

### The POOM Walk Itself

`permute()` (`orglinks.c:389–422`) drives the V→I direction by restricting the POOM's span dimension to the query V-range, calling `span2spanset()` per span, which calls `retrieverestricted()` which calls `findcbcinarea2d()` [SS-POOM-MULTIMAP, SS-CONTENT-IDENTITY Finding 0009].

`findcbcinarea2d()` traverses the 2D POOM enfilade left-to-right via sibling links, recursively descending into qualifying subtrees and accumulating every matching leaf [SS-POOM-MULTIMAP]. At each crum, `whereoncrum()` classifies the query address against the crum's `[grasp, reach)` interval using the five-way `{ToLeft, OnLeft, Through, OnRight, ToRight}` result [SS-WHEREONCRUM]. Absolute grasp is reconstructed by accumulating ancestor displacements: `grasp = offset + ptr->cdsp` [INV-ENFILADE-RELATIVE-ADDRESSING].

Results are insertion-sorted by V-address via `incontextlistnd()` as leaves are discovered, ensuring the returned I-span list is V-sorted regardless of tree sibling order [INV-RETRIEVAL-V-SORTED, SS-CONTEXT-LIST]. Because the POOM is a multimap, the same I-address can appear at multiple V-positions; all are collected [SS-POOM-MULTIMAP].

---

### `vspanset2sporglset` Is a Different Path

`vspanset2sporglset` (`sporgl.c:35–65`) also calls `vspanset2ispanset` → `permute()` internally, so it shares the same POOM walk [SS-VSPAN-TO-SPORGL]. The difference is what it attaches afterward: it annotates each I-span with the source document's ISA to produce a **sporgl** (origin, width, source_doc).

Sporgls are used by:
- Link creation — endpoint indexing into spanfilade [INT-SPORGL-LINK-INDEX]
- RETRIEVEENDSETS — content-identity-based link discovery [SS-RETRIEVE-ENDSETS]
- Version comparison via `correspond.c` [INT-SPORGL-VERSION-COMPARE]
- Transclusion (vcopy) to preserve provenance through `docopy` [INT-SPORGL-TRANSCLUSION]

Plain content retrieval needs none of that provenance. `specset2ispanset` produces bare I-spans; `ispanset2vstuffset` then walks the granfilade B-tree by I-address to retrieve the actual bytes [SS-GRANF-OPERATIONS, Finding 0012]. The granfilade is indexed by I-address and returns raw byte sequences with no encoding interpretation [SS-CONTENT-IDENTITY Finding 0034].

---

### Subspace Warning

`ispanset2vstuffset` passes all I-spans to the granfilade without type discrimination [SS-DUAL-ENFILADE Finding 0011]. If the SpecSet includes V-positions from the link subspace (2.x internally), `permute()` produces link orgl ISAs rather than permascroll addresses. Dereferencing those in the granfilade yields garbage silently — the precondition that all V-addresses be in the text subspace (1.x) is caller-enforced, not backend-enforced [PRE-RETRIEVE-CONTENTS Finding 0010, INV-SUBSPACE-CONVENTION].

---

## Code Exploration

I now have all I need. Here is the complete traced answer.

---

## Content Delivery: VSpec → I-address Resolution

### Top-level entry: `retrievev()` → `doretrievev()`

The FEBE handler is `retrievev()` [fns.c:175–187]:

```c
void retrievev(typetask *taskptr) {
    if (getretrievev(taskptr, &specset)
     && doretrievev(taskptr, specset, &vstuffset))
        putretrievev(taskptr, &vstuffset);
    else
        putrequestfailed(taskptr);
}
```

`doretrievev()` [do1.c:338–346] is the real driver. It decomposes the problem into two sequential phases:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr) {
    typeispanset ispanset;
    return
       specset2ispanset(taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr);
}
```

**Phase 1:** convert every VSpec to a set of I-spans.  
**Phase 2:** fetch content for those I-spans from the granfilade.

---

### Phase 1, Step 1: `specset2ispanset()` — iterating VSpecs [do2.c:14–46]

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
  typeorgl docorgl;
  ...
  for (; specset; specset = ...) {
      if (...itemid == ISPANID) {         // pass raw I-spans through unchanged
          ...
      } else if (...itemid == VSPECID) {
          if (!(
            findorgl(taskptr, granf, &((typevspec*)specset)->docisa, &docorgl, type)  // line 35
          && (ispansetptr = vspanset2ispanset(taskptr, docorgl,                        // line 36
                ((typevspec*)specset)->vspanset, ispansetptr)))) {
              return FALSE;
          }
      }
  }
  return TRUE;
}
```

Two calls per VSPEC item:

1. **`findorgl()`** [do2.c:35] — looks up the document's ORGL in the granfilade.
2. **`vspanset2ispanset()`** [do2.c:36] — uses that ORGL to permute the V-addresses into I-addresses.

---

### Phase 1, Step 2: `findorgl()` — granfilade lookup [granf1.c:17–41]

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {   // BERT check [line 22]
        ...return FALSE if not open...
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);      // line 39
    return (*orglptr ? TRUE : FALSE);
}
```

`fetchorglgr()` [granf2.c:22–81] walks the global granfilade tree using `retrievecrums()` to find the crum whose `totaloffset` equals `docisa`, then loads the on-disk ORGL if needed. This is the **granfilade lookup** — it returns a `typeorgl` pointer which is the document's own POOM enfilade.

---

### Phase 1, Step 3: `vspanset2ispanset()` → `permute()` — the per-document POOM walk [orglinks.c:397–422]

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);   // orglinks.c:401
}

typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset,
                     INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {   // line 414
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return save;
}
```

`permute()` iterates every V-span and calls `span2spanset()` for each one.

---

### Phase 1, Step 4: `span2spanset()` → `retrieverestricted()` — the actual POOM traversal [orglinks.c:425–454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                          INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                  (typespan*)NULL, targindex, (typeisa*)NULL);  // line 435
    for (c = context; c; c = c->nextcontext) {
        context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    ...
}
```

`retrieverestricted()` [retrie.c:56–85] unpacks the span bounds, then calls `retrieveinarea()` [retrie.c:87–110]:

```c
typecontext *retrieveinarea(...) {
    switch (fullcrumptr->cenftype) {
      case SPAN:
      case POOM:
          findcbcinarea2d((typecorecrum*)fullcrumptr, &offset,
                          span1start, span1end, index1,
                          span2start, span2end, index2, &context, infoptr);  // retrie.c:97
          break;
    }
    return context;
}
```

`findcbcinarea2d()` recursively descends the POOM enfilade tree, collecting every bottom crum whose V-dimension intersects the restriction span. Each crum's `totaloffset.dsas[I]` gives the corresponding I-address. The result is a context list that `context2span()` translates into `typeispanset` items.

---

### Phase 2: `ispanset2vstuffset()` → `ispan2vstuffset()` — fetching content [granf1.c:58–74, granf2.c:286–318]

For each I-span now in hand, `ispan2vstuffset()` calls `retrieveinspan()` [retrie.c:112] which walks the **granfilade** (the global text store, `cenftype == GRAN`) via `findcbcinspanseq()` to retrieve the actual text crums, then `context2vstuff()` assembles them into the returned `vstuffset`.

---

### Does it route through `vspanset2sporglset`?

**No.** `vspanset2sporglset()` [sporgl.c:35–65] exists and does internally call both `findorgl()` and `vspanset2ispanset()`, but it is never in the content delivery path. Every call to `specset2sporglset()` (the outer wrapper at sporgl.c:14) comes exclusively from link operations:

- `do1.c:187–188` — `docreatelink` (creating a 2-endpoint link)
- `do1.c:214–216` — `domakelink` (3-endpoint link)
- `spanf1.c:71–75` — `findlinksfromtothreesp` (querying links)
- `spanf1.c:222` — `insertendsetsinspanf` (recording link endpoints into spanfilade)

The content delivery path never touches `sporgl.c`. The sporgl layer is the link indexing substrate: it packages `(docisa, I-origin, I-width)` tuples into `typesporgl` items for insertion into the spanfilade so that link-following queries can work. Content retrieval has no need for it.

---

### Complete Call Chain

```
retrievev()                     [fns.c:175]
  doretrievev()                 [do1.c:338]
    specset2ispanset()          [do2.c:14]     — for each VSPEC item:
      findorgl(granf, docisa)   [granf1.c:17]  ← GRANFILADE lookup → returns document ORGL
        fetchorglgr()           [granf2.c:22]
          retrievecrums()       [retrie.c:15]  ← walks granfilade to locate orgl crum
      vspanset2ispanset(orgl)   [orglinks.c:397]
        permute(orgl, V→I)      [orglinks.c:404]  — for each V-span:
          span2spanset()        [orglinks.c:425]
            retrieverestricted(orgl, vspan, V, NULL, I)  [retrie.c:56]
              retrieveinarea()  [retrie.c:87]
                findcbcinarea2d()  [retrie.c:97]  ← walks document POOM, returns I-addresses
    ispanset2vstuffset(granf)   [granf1.c:58]  — for each I-span:
      ispan2vstuffset()         [granf2.c:286]
        retrieveinspan(granf)   [retrie.c:112] ← walks granfilade for text crums
          findcbcinspanseq()
          context2vstuff()      ← assembles final content
```

The granfilade is entered **twice**: once (via `findorgl`) to locate the per-document POOM enfilade, and once (via `ispan2vstuffset`) to fetch the raw text. The POOM walk (`findcbcinarea2d`) happens in between and operates on the per-document ORGL, not on the global granfilade. `vspanset2sporglset` is never on this path.
