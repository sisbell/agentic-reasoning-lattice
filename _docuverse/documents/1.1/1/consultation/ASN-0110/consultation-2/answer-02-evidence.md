## Question 2 [evidence]

> What representation does RETRIEVEENDSETS take for its query region — a single span, a finite span-set, or something else — and does the search iterate the finite link store performing per-span overlap tests?

## KB Synthesis

**Query representation:** RETRIEVEENDSETS takes a **specset** — a finite sequence of V-specs (each `{doc, start, width}`) — not a single span. [SS-RETRIEVE-ENDSETS] The operation accepts any number of V-spans across one or more documents as its content region.

**Search mechanism:** It does NOT iterate the link store performing per-span tests. The search path is:

1. Convert the input specset to I-addresses (sporglset) via V-to-I translation — `specset → sporglset` [INT-SPORGL-LINK-INDEX]
2. Define three ORGLRANGE dimension prefixes: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 [SS-RETRIEVE-ENDSETS]
3. For each endset type, call `retrievesporglsetinrange()` which searches the **spanfilade B-tree** with dual restrictions: SPANRANGE (the query's I-addresses) and ORGLRANGE (the endset type prefix)

The spanfilade is an I-address → link index [SS-SPANF-OPERATIONS], so lookup goes directly from query I-addresses into the index tree — no sequential scan of all links occurs.

**Key distinction from FOLLOWLINK:** FOLLOWLINK takes a known link ISA and reads one endset from the link orgl directly. RETRIEVEENDSETS searches by content identity through the spanfilade, returning all endsets that intersect a content region, with results expressed in the querying document's V-space (not the link's home document). [SS-RETRIEVE-ENDSETS]

---

## Code Exploration

All lines verified. Here is the complete answer.

---

## RETRIEVEENDSETS: Query Region and Search Mechanism

### Query Region Representation

RETRIEVEENDSETS takes a **finite span-set** — specifically a `typespecset`, which is a singly-linked list of heterogeneous span specifications. The entry point at `fns.c:350–362` receives this as the variable `specset` and passes it directly to `doretrieveendsets`:

```c
// fns.c:350–362
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  bool getretrieveendsets(), doretrieveendsets();
    if (
       getretrieveendsets (taskptr, &specset)
    && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)){
        putretrieveendsets (taskptr, fromset, toset, threeset);
    }else
        putrequestfailed (taskptr);
}
```

`doretrieveendsets` at `do1.c:369–374` is a pure pass-through to `retrieveendsetsfromspanf`:

```c
// do1.c:369–374
bool doretrieveendsets(typetask *taskptr, typespecset specset, ...)
{
  bool retrieveendsetsfromspanf();
   return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

The linked list items can be one of two kinds (`sporgl.c:19–28`):
- `ISPANID` — a direct interval span (already in permascroll coordinates)
- `VSPECID` — a virtual spec that must be resolved through the granfilade to yield one or more interval spans

Normalization from `typespecset` → `typesporglset` (a list of resolved sporgl nodes, each carrying a document address + origin + width tumbler) happens in `specset2sporglset()`:

```c
// sporgl.c:14–33
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {  // walks the entire list
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            *sporglsetptr = (typesporglset)specset;
            sporglsetptr = (typesporglset *)&((typeitemheader *)specset)->next;
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset (taskptr, &((typevspec *)specset)->docisa,
                    ((typevspec *)specset)->vspanset, sporglsetptr, type))){
                return (FALSE);
            }
        }
    }
    *sporglsetptr = NULL;
    return (TRUE);
}
```

`vspanset2sporglset()` at `sporgl.c:35` further expands each VSPEC by calling `findorgl()` (the granfilade lookup) and then `vspanset2ispanset()` (the V→I conversion), potentially expanding one virtual span into multiple interval spans.

So the query region is neither a bare single span nor a flat input format — it is a **typed linked list that may contain a mix of direct and virtual spans, with VSPECID items expanding to multiple interval spans via the granfilade before searching begins**.

---

### Does the Search Iterate the Finite Link Store with Per-Span Overlap Tests?

**Yes — but the structure is more precise than a flat scan.** The search is a **per-input-sporgl, tree-pruned 2D enfilade descent**, not a linear pass over a flat link list. Here is the full call chain:

#### Step 1 — `retrieveendsetsfromspanf` issues two retrieval passes

`spanf1.c:190–235` calls `retrievesporglsetinrange` twice: once with `fromspace` (whose `.stream.mantissa[0] == LINKFROMSPAN`) and once with `tospace` (`.stream.mantissa[0] == LINKTOSPAN`):

```c
// spanf1.c:210–225
fromspace.stream.mantissa[0] = LINKFROMSPAN;
fromspace.width.mantissa[0]  = 1;
tospace.stream.mantissa[0]   = LINKTOSPAN;
tospace.width.mantissa[0]    = 1;
...
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
   && retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
   ...
   && retrievesporglsetinrange(taskptr, sporglset, &tospace, &tosporglset)
   ...))
```

#### Step 2 — `retrievesporglsetinrange` iterates each sporgl

`spanf1.c:237–267` loops over every resolved span in the sporglset and calls `retrieverestricted` for each:

```c
// spanf1.c:244–245
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                                  whichspace, ORGLRANGE, (typeisa*)NULL);
```

The two span arguments are:
- **`span1` / `SPANRANGE`** — the query input sporgl (content region to match)
- **`span2` / `ORGLRANGE`** — the fixed role span (`LINKFROMSPAN` or `LINKTOSPAN`), selecting which end of each link to match

#### Step 3 — `retrieverestricted` converts to tumbler intervals

`retrie.c:56–85` unpacks both spans from (stream, width) into (start, end) tumblers for the overlap arithmetic:

```c
// retrie.c:63–83
if (span1ptr) {
    movetumbler (&span1ptr->stream, &span1start);
    tumbleradd (&span1start, &span1ptr->width, &span1end);
}
if (span2ptr) {
    movetumbler (&span2ptr->stream, &span2start);
    tumbleradd (&span2start, &span2ptr->width, &span2end);
}
temp = retrieveinarea (fullcrumptr, &span1start, &span1end, index1,
                        &span2start, &span2end, index2, ...);
```

#### Step 4 — `findcbcinarea2d` descends the spanfilade tree

`retrie.c:229–268` is the core search loop. It does **not** walk a flat list of links; it recurses into the spanfilade enfilade tree, iterating sibling crums at each level and testing each node's bounding box before descending:

```c
// retrie.c:252–264
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                           span2start, span2end, index2, ...)){
        continue;                    // prune: bounding box does not overlap
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);  // recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // leaf hit: add to results
    }
}
```

#### Step 5 — `crumqualifies2d` performs the per-node 2D overlap test

`retrie.c:270–305` tests each crum against both span dimensions:

```c
// retrie.c:282–304
endcmp = iszerotumbler (span1end) ? TOMYRIGHT
                                  : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return (FALSE);        // query ends before this crum
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME) return (FALSE);               // query starts after this crum

endcmp = iszerotumbler (span2end) ? TOMYRIGHT
                                  : whereoncrum (crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return (FALSE);         // role check: dim 2
startcmp = whereoncrum (crumptr, offset, span2start, index2);
if (startcmp > THRUME) return (FALSE);               // role check: dim 2

return (TRUE);
```

Dimension 1 (`SPANRANGE`) is the content-address overlap; dimension 2 (`ORGLRANGE`) is the link-role filter — the `LINKFROMSPAN`/`LINKTOSPAN` slot that partitions the tree so only links of the correct directional role match.

---

### Summary

| Question | Answer |
|---|---|
| **Query region type** | Finite span-set (`typespecset`): a linked list with items of kind `ISPANID` (direct interval span) or `VSPECID` (virtual span expanded via granfilade lookup). Multiple input spans are all searched. |
| **Does it iterate the link store per-span?** | Yes, per input span — but through a **2D enfilade tree descent with bounding-box pruning**, not a flat linear scan. For each resolved sporgl, `retrievesporglsetinrange` calls `retrieverestricted` → `findcbcinarea2d`, which recurses the spanfilade tree, testing each crum's 2D bounding box with `crumqualifies2d` (overlap in both `SPANRANGE` and `ORGLRANGE`). Subtrees that cannot contain matching links are pruned. |
| **Two separate passes** | Yes — one for from-endsets (`LINKFROMSPAN`) and one for to-endsets (`LINKTOSPAN`), both using the same normalized sporglset as the content-region query. |
