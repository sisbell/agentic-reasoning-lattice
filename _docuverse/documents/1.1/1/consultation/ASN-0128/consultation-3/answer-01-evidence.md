## Question 1 [evidence]

> When udanax-green stores and matches link endsets (e.g., in retrieval queries like FINDLINKSFROMTO), does it compare span sets by the region they cover — normalizing containment or abutment — or does it preserve and distinguish the exact span decomposition supplied at link creation?

## KB Synthesis

## Endset Storage and Matching in udanax-green

The system uses two distinct mechanisms: I-span decomposition for **storage** and I-address set intersection for **matching**. These operate independently.

---

### Storage: I-span decomposition is preserved as computed, not normalized

At link creation, V-spans are converted to I-spans (sporgls) via `vspanset2sporglset` → `vspanset2ispanset` → `permute` → `span2spanset`. This produces **one sporgl per contiguous I-address region** in the input V-span [SS-LINK-ENDPOINT/Finding 0037, SS-SPORGL-LINK-INDEX/Finding 0013].

The crucial point is that the decomposition is **driven by I-address structure**, not by the V-span boundaries the caller supplied:

- A single V-span covering content transcluded from two sources (non-contiguous I-addresses) produces two sporgls [SS-LINK-ENDPOINT/Finding 0037]
- A single V-span covering content from one source (contiguous I-addresses) produces one sporgl

Once stored in the spanfilade, the sporgl decomposition is immutable [INV-LINK-PERMANENCE]. There is no post-creation merging or normalization of abutting sporgls — the set of sporgls stored at link creation time is exactly what is returned at retrieval time. The duplication artifacts in [EC-PIVOT-LINK-FRAGMENTATION] and [EC-MULTISPAN-LINK-DUPLICATION] confirm this: rearrangement fragments endsets in ways that are visible at retrieval, and multi-span links can return duplicate span entries, because no normalization step collapses the stored sporgls.

---

### Matching: I-address set intersection, span decomposition is irrelevant

`find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }` [SS-FIND-LINKS/Finding 0028].

The spanfilade is indexed at the I-address level — `insertspanf` makes one `insertnd` call per `typeispan` struct [SS-DOCISPAN/Finding 0047, SS-SPORGL-LINK-INDEX/Finding 0013]. A query converts its V-spec input to I-addresses and checks for intersection with stored I-address ranges. **Partial overlap of even one I-address suffices**; span boundary alignment is irrelevant [SS-FIND-LINKS/Finding 0028, concrete example: "link" (4 chars) discovers link on "hyperlink text" (14 chars)].

This means:
- How many sporgls the stored endset contains does not affect whether a link is found
- Whether the query's span boundaries match, contain, or merely overlap the stored spans does not matter
- The search is a set-membership test at I-address granularity, not a span-shape comparison

---

### Summary

| Aspect | Behavior |
|--------|----------|
| Endset storage unit | Sporgls (I-spans with provenance), one per contiguous I-address region |
| Decomposition at creation | Determined by I-address contiguity in the content, not caller's V-span boundaries |
| Post-creation normalization | None — stored sporgls are immutable and not merged |
| Discovery matching | I-address set intersection; span decomposition irrelevant; partial overlap sufficient |
| Retrieval output | Stored sporgl decomposition returned as-is; abutting sporgls not merged on output |

The exact span decomposition supplied at creation is **preserved in storage and returned in retrieval**, but it has **no effect on discoverability** — that is determined solely by I-address intersection.

---

## Code Exploration

I now have everything needed to give a complete, cited answer.

---

## How udanax-green Stores and Matches Link Endsets

### Summary

udanax-green **preserves the exact span decomposition** at storage time — no normalization, no abutment merging. At match time it performs **interval-overlap testing in permascroll (I) space**, not exact-decomposition comparison. A link created with endset V=[a, a+b+c] will match any FINDLINKSFROMTO query whose translated I-span overlaps the stored I-span, regardless of how either is decomposed.

---

### The Storage Path: `docreatelink` → `insertendsetsinspanf`

**Entry point** — `fns.c:100–112`, `createlink`:
```c
getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)
```

**Core of `docreatelink`** — `do1.c:195–221`:
```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
specset2sporglset(taskptr, threespecset,&threesporglset,NOBERTREQUIRED)
setlinkvsas(&fromvsa, &tovsa, &threevsa)
insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, ...)
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

**Step 1 — V→I translation (`specset2sporglset`)** — `sporgl.c:14–33`:
```c
vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type)
```

Inside `vspanset2sporglset` — `sporgl.c:35–65`:
```c
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V → I via POOM permutation
    for (; ispanset; ispanset = ispanset->next) {
        sporglset->sporglorigin = ispanset->stream;   // I-address
        sporglset->sporglwidth  = ispanset->width;    // I-width
        sporglset->sporgladdress = *docisa;           // home document
    }
}
```

`vspanset2ispanset` calls `permute` → `span2spanset` → `retrieverestricted` on the document's POOM enfilade to look up what I-address material occupies the queried V-positions. The result for each V-span is a list of I-spans. Each I-span becomes a separate sporgl. **No merging of abutting or contained results occurs.**

`context2span` — `context.c:176–212` — clips each resulting I-span to the precise intersection with the input V-span boundary:
```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0, tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0, -tumblerintdiff(&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
}
```
This ensures the stored I-span is exactly the content covered by the supplied V-span — no larger, no smaller.

**Step 2 — Storing in the spanfilade (`insertendsetsinspanf`)** — `do2.c:116–128`:
```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset,LINKTHREESPAN)
```

Inside `insertspanf` — `spanf1.c:15–54`:
```c
for (; sporglset; sporglset = next) {
    crumorigin.dsas[SPANRANGE] = lstream;   // I-address of this endset chunk
    crumwidth.dsas[SPANRANGE]  = lwidth;    // I-width
    crumorigin.dsas[ORGLRANGE] = linkisa prefixed with LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN
    insertnd(taskptr, spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
}
```

**One `insertnd` call per sporgl (per I-span chunk).** There is no code that merges abutting or contained I-spans; the decomposition from the V→I translation is stored verbatim.

**Step 3 — Storing in the link's own POOM (`insertendsetsinorgl`)** — `do2.c:130–149`:
```c
insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // fromvsa = 1.1
insertpm(taskptr, linkisaptr, link, tovsa,   tosporglset)     // tovsa = 2.1
insertpm(taskptr, linkisaptr, link, threevsa,threesporglset)  // threevsa = 3.1
```

The link's POOM records the endsets at fixed virtual addresses (1.1 = FROM, 2.1 = TO, 3.1 = THREE) — set in `setlinkvsas` at `do2.c:169–183`. This is used by `dofollowlink` / `link2sporglset` to retrieve a specific link's endsets; it does not participate in FINDLINKSFROMTO matching.

---

### The Query Path: `FINDLINKSFROMTO` → overlap in I-space

**Entry** — `fns.c:189`, `findlinksfromtothree` → `dofindlinksfromtothree` [do1.c:348] → `findlinksfromtothreesp` [spanf1.c:56].

**Step 1 — Query V→I translation** — `spanf1.c:70–75`:
```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset,   &tosporglset,   NOBERTREQUIRED);
```
The exact same V→I translation path as creation.

**Step 2 — Spanfilade search by overlap** — `sporgl.c:239–268`, `sporglset2linksetinrange`:
```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist(taskptr, linksetptr, &linksa);
}
```

`retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229] walks the spanfilade tree. The key predicate is `crumqualifies2d` [retrie.c:270–305]:

```c
// Does the stored crum's SPANRANGE interval overlap the query I-span?
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return FALSE;          // query ends before crum starts
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return FALSE;                 // query starts after crum ends

// Does the stored crum's ORGLRANGE match the requested endset type (FROM/TO/THREE)?
endcmp = iszerotumbler(span2end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return FALSE;
startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return FALSE;

return TRUE;
```

This is a pure **interval overlap test**: a stored crum qualifies if `query_start < crum_end AND query_end > crum_start`. No equality, no containment, no exact match — overlap suffices.

**Step 3 — Intersection of from/to/three link sets** — `spanf1.c:100`:
```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```
Only links that appear in all non-NULL query sets survive.

---

### What This Means for Decomposition

| Scenario | Result |
|---|---|
| Create link with endset V=[a, a+n]; query with sub-span V=[a, a+k] (k < n) | **Match** — overlap in I-space |
| Create link with endset V=[a, a+n]; query with super-span V=[a-1, a+n+1] | **Match** — overlap in I-space |
| Create link with V=[a,b]+[c,d] (two spans, b < c); query with V=[a,b] alone | **Match** — the [a,b] crum is present in the spanfilade |
| Create link with V=[a,b]+[b,c] (abutting); query with V=[a,c] (merged) | **Match** — V=[a,c] maps to I-span covering both crums |
| Create link with V=[a,b]; query for exact V=[a,b] | **Match** — exact is a special case of overlap |
| Query for a V-span with **zero** overlap in I-space | **No match** |

**The exact V-span decomposition supplied at creation is preserved as-is through the V→I translation and stored as separate I-span crums.** There is no normalization step at creation or at query time. `putvspaninlist` [orglinks.c:329-387], which does merge abutting spans, is only used in the `retrievevspansetpm` path (reading a document's extent), never in the link endset store/match path.

**Matching during FINDLINKSFROMTO is overlap-based in permascroll (I) space.** The system finds all stored I-span crums whose interval intersects the query I-span, regardless of how either was decomposed into individual spans at link creation.
