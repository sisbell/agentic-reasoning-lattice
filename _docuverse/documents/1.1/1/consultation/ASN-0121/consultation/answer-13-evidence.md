## Question 13 [evidence]

> How does the operation convert each of the from-set, to-set, and third-set V-spans into I-address spans before searching the spanfilade, and does it walk each document's POOM independently to resolve them?

## KB Synthesis

## V-span to I-address Conversion in FINDLINKSFROMTOTHREE

The operation proceeds in two distinct phases: per-document POOM traversal to produce sporgls, then spanfilade search over those I-address ranges.

### Phase 1 — V-span → sporgl (per-document POOM walk)

Each specset (from, to, or three) is converted by `specset2sporglset()` → `vspanset2sporglset()`, which iterates over every VSpec in the specset [SS-SPORGL]. For each VSpec, the call chain is:

```
vspanset2ispanset()
  → permute()
    → span2spanset()
      → retrieverestricted()   ← queries that document's POOM
```

`retrieverestricted()` walks the target document's POOM enfilade to find every contiguous I-address region that maps to the requested V-range [SS-VSPAN-TO-SPORGL]. If the specset references multiple documents, each document's POOM is walked independently — there is one traversal per referenced document [SS-DOCUMENT-LIFECYCLE].

The output is a sporglset: one `Sporgl = {origin: IAddress, width: TumblerWidth, source_doc: ISA}` per contiguous I-region found. A single V-span spanning content from two transclusion sources produces two sporgls, not one [ST-LINK-CREATE, Finding 0037].

### Phase 2 — Spanfilade search

`findlinksfromtothreesp()` passes each sporglset to `sporglset2linkset()`, which:

1. **Overrides the orgl dimension** unconditionally with a hardcoded width-100 range starting at zero — the `if (TRUE||!homeset)` guard disables any caller-specified orgl scoping [EC-FIND-LINKS-GLOBAL]. The search is effectively global in the orgl dimension.
2. **Restricts the SPAN dimension** to the I-address range `[sporgl.origin, sporgl.origin + sporgl.width)` — this is the content-identity filter that actually works [SS-SPANF-OPERATIONS].

When all three specsets are non-empty, the three result sets are intersected via `intersectlinksets()` at O(n×m×p) cost [SS-FIND-LINKS, Finding 0035].

### Summary

Yes, each document's POOM is walked independently during V→I conversion — one traversal per document referenced in any VSpec. The sporgls produced carry both the I-address range and the source document ISA, but the source document ISA is discarded when the orgl-dimension filter is overridden in the spanfilade search. Effectively, link discovery is purely a span-dimension (I-address) intersection with no per-document scoping [PRE-FIND-LINKS, Finding 0069].

---

## Code Exploration

I now have all the source I need. Here is the full answer.

---

## How V-spans Are Converted to I-spans Before Spanfilade Operations

The question concerns the `docreatelink` path — specifically how three endpoint specsets (from, to, three) each containing V-spans are converted to I-address spans before being stored in the spanfilade. The short answer is: each specset is converted independently via its own `specset2sporglset` call, which loads the referenced document's POOM once and then walks it for every V-span in that specset. Documents referenced by different endpoint sets are walked independently.

---

### Entry Point: `docreatelink` — `do1.c:195–221`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
```

Three back-to-back calls convert each specset:

```c
&& specset2sporglset (taskptr, fromspecset,   &fromsporglset,  NOBERTREQUIRED)  // line 214
&& specset2sporglset (taskptr, tospecset,     &tosporglset,    NOBERTREQUIRED)  // line 215
&& specset2sporglset (taskptr, threespecset,  &threesporglset, NOBERTREQUIRED)  // line 216
```

The three resulting sporglsets are then:

- stored in the link's POOM at fixed V-addresses (from=`1.1`, to=`2.1`, three=`3.1`) via `insertendsetsinorgl` [do2.c:130], which calls `insertpm` [orglinks.c:75] for each
- registered in the spanfilade index via `insertendsetsinspanf` [do2.c:116]

---

### Stage 1: specset2sporglset — `sporgl.c:14–33`

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
    typesporglset *sporglsetptr, int type)
```

Walks the specset list. For each element:

- **`ISPANID`** (line 20–22): the item is already an I-span; splice it directly into the output list
- **`VSPECID`** (line 23–28): call `vspanset2sporglset(taskptr, &vspec->docisa, vspec->vspanset, sporglsetptr, type)` — the docisa field names which document's POOM to consult

---

### Stage 2: vspanset2sporglset — `sporgl.c:35–65`

```c
typesporglset *vspanset2sporglset(typetask *taskptr,
    typeisa *docisa, typevspanset vspanset,
    typesporglset *sporglsetptr, int type)
```

**Line 44:** `findorgl(taskptr, granf, docisa, &orgl, type)`

This loads the POOM for `docisa` — **one load per docisa**, shared across all vspans in this call. If from-set and to-set reference different documents their `docisa` values differ, so `findorgl` is called separately for each, walking a different POOM tree.

**Lines 47–58:** For each vspan in the vspanset:

```c
(void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // line 48
for (; ispanset; ispanset = ispanset->next) {                   // line 49
    sporglset->sporgladdress = *docisa;                         // line 53
    sporglset->sporglorigin  = ispanset->stream;                // line 54
    sporglset->sporglwidth   = ispanset->width;                 // line 55
}
```

Each resulting sporgl carries the home-document ISA (`sporgladdress`) alongside its I-span (`sporglorigin`, `sporglwidth`). This is the record that will be stored in both the link's POOM and the spanfilade.

---

### Stage 3: vspanset2ispanset → permute → span2spanset — `orglinks.c:397–454`

`vspanset2ispanset` [orglinks.c:397] is a thin wrapper:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` [orglinks.c:404] loops through the vspanset:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next)  // line 414
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
```

`span2spanset` [orglinks.c:425] does the actual work for each individual V-span:

**Line 435:**
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V,
                              (typespan*)NULL, I, (typeisa*)NULL);
```

This queries the POOM enfilade with the V-span as a restriction, asking for the I dimension. `retrieverestricted` [retrie.c:56] expands the span into start/end tumblers:

```c
movetumbler(&span1ptr->stream, &span1start);              // line 64
tumbleradd(&span1start, &span1ptr->width, &span1end);     // line 65
```

Then delegates to `retrieveinarea` [retrie.c:87] which calls `findcbcinarea2d` — the recursive POOM tree walk that finds all crums overlapping the specified V-range.

**Lines 439–445:** For each returned context, clip it to the restriction span and extract the I coordinates:

```c
context2span(c, restrictionspanptr, V, &foundspan, I);    // line 443
onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);  // line 444
```

`context2span` [context.c:176] uses `prologuecontextnd` to extract the context's `totaloffset` (grasp) and computes reach = grasp + `contextwid`. It clips both to the V restriction bounds, then reads off the I dimension:

```c
movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);           // line 206
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);  // line 207
foundspanptr->itemid = index2itemid(idx2, context);              // line 209
```

`index2itemid` [context.c:223] returns `ISPANID` when `idx2 == I` on a POOM context — confirming the output is typed as an I-span.

---

### Stage 4: insertendsetsinspanf — `do2.c:116–128`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr,
    typesporglset fromsporglset,
    typesporglset tosporglset,
    typesporglset threesporglset)
{
    insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset,  LINKFROMSPAN)   // line 119
    && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,  LINKTOSPAN)    // line 120
    ...
    if (threesporglset) {
        insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)  // line 123
    }
}
```

Each sporglset is inserted into the spanfilade with a distinct `spantype` tag (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN`). The third set is **conditional** — if `threesporglset` is NULL the call is skipped entirely. `insertspanf` [spanf1.c:15] handles ISPANID items (line 26–29) by reading `stream` and `width` directly from the ispan fields and inserting them at `SPANRANGE` into the spanfilade's 2D enfilade.

The POOM insertion (`insertendsetsinorgl` → `insertpm`) follows the same three-set conditional pattern at `do2.c:136`: `if (threevsa && threesporglset)`.

---

### Does Each Document's POOM Get Walked Independently?

**Yes — one `findorgl` call per distinct docisa.** The proof is in `vspanset2sporglset` [sporgl.c:44]:

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) return (NULL);
```

This call is made once per invocation of `vspanset2sporglset`, before the inner loop over the vspanset. If the from-set references document A and the to-set references document B, `specset2sporglset` is called separately for each [do1.c:214–216], each calls `vspanset2sporglset` with its own `docisa`, and each loads a different `orgl`. The POOM walk (`retrieverestricted → retrieveinarea → findcbcinarea2d`) is then performed on A's POOM for from-spans and B's POOM for to-spans — entirely independent tree traversals.

Within a single specset, if all vspans share the same docisa (the normal case for one endpoint), `vspanset2sporglset` loads the POOM once and reuses `orgl` across all vspans in its inner loop [sporgl.c:47–58].

---

### Summary of the Conversion Chain

| Step | Function | File:Lines | What Happens |
|------|----------|------------|--------------|
| 1 | `docreatelink` | do1.c:214–216 | Calls `specset2sporglset` three times, once per endpoint set |
| 2 | `specset2sporglset` | sporgl.c:14–33 | Dispatches on item type; VSPECID items go to step 3 |
| 3 | `vspanset2sporglset` | sporgl.c:35–65 | `findorgl` loads docisa's POOM; calls `vspanset2ispanset` per vspan |
| 4 | `vspanset2ispanset` | orglinks.c:397–402 | Delegates to `permute(orgl, vspan, V, ispanset, I)` |
| 5 | `permute` | orglinks.c:404–422 | Loops over input spans, calls `span2spanset` for each |
| 6 | `span2spanset` | orglinks.c:425–454 | `retrieverestricted` queries POOM for V-span → contexts; `context2span` clips each context and extracts I coordinates |
| 7 | `retrieverestricted` | retrie.c:56–85 | Expands span to start/end tumblers; calls `retrieveinarea` |
| 8 | `retrieveinarea` | retrie.c:87–110 | Dispatches to `findcbcinarea2d` for POOM/SPAN enfilade tree walk |
| 9 | `context2span` | context.c:176–212 | Clips context to V restriction; reads off I-dimension stream/width; sets `ISPANID` |
| 10 | `insertendsetsinspanf` | do2.c:116–128 | `insertspanf` per set with LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN tags; third set is conditional |
