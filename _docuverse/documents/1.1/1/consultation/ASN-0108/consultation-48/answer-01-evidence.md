## Question 1 [evidence]

> In udanax-green's link search, which endset slot(s) of a link does the spanfilade index it under — from, to, three, or some fixed union — and is that position a fixed function of the link's immutable endsets, independent of whichever endpoint a given query currently matches?

## KB Synthesis

## Spanfilade Indexing of Link Endsets

**All three endsets are indexed, each under a separate ORGLRANGE tag, fixed at creation time.**

### What gets indexed, and where

When `docreatelink` runs, `insertendsetsinspanf()` is called once and inserts **all three** endpoint sporglsets — FROM, TO, and THREE — into the spanfilade [ST-CREATE-LINK, Finding 0012]:

```
spanf: from-endpoint I-addrs → link_ISA  (tagged LINKFROMSPAN = 1)
     + to-endpoint I-addrs   → link_ISA  (tagged LINKTOSPAN   = 2)
     + three-endpoint I-addrs → link_ISA (tagged LINKTHREESPAN = 3)
```

The internal representation is `I-address → set of (link ISA, endpoint-type)` pairs [INT-SPORGL-LINK-INDEX, Finding 0013]. Each entry carries the endpoint-type tag as part of the key, so the same I-address range can appear three times in the spanfilade — once per slot — if a link's endpoints overlap.

### Queries use ORGLRANGE to select which slot to match

FINDLINKS and RETRIEVEENDSETS both search the spanfilade in two dimensions simultaneously:

- **SPANRANGE**: the I-address dimension — restricts to links whose endpoint content intersects the query's content identity
- **ORGLRANGE**: selects the endpoint slot via the LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN prefix constants

RETRIEVEENDSETS makes this explicit: it calls `retrievesporglsetinrange()` three times, once per endset type, each with the appropriate ORGLRANGE prefix [SS-RETRIEVE-ENDSETS, Finding 0035]. FINDLINKS similarly takes three specset arguments (from, to, three) and intersects the results — `find_links(source, target)` is equivalent to `find_links(source) ∩ find_links(target)` [SS-FIND-LINKS, Finding 0029].

### The indexing is a fixed function of the link's endsets, independent of query matches

The spanfilade entries are written exactly once, at link creation, from the link's immutable endsets. No subsequent operation modifies them — the spanfilade is write-only [INV-SPANF-WRITE-ONLY, Finding 0057]. Which endpoint a particular query happens to match against has no effect on the index structure; it only determines which ORGLRANGE tag the query uses as a restriction. A link found by matching its FROM endpoint via one query is indexed identically as when found by matching its TO endpoint via another query — both lookups hit the same physical spanfilade entries, just with different ORGLRANGE filters applied at query time.

One caveat: the `find_links` orgl-dimension scoping parameter (intended to restrict which documents are searched) is disabled by a `TRUE||` guard in `sporglset2linkset`, making all link searches effectively global in the orgl dimension [EC-FIND-LINKS-GLOBAL, Finding 0069]. This does not affect the from/to/three ORGLRANGE tags — those function correctly via RETRIEVEENDSETS — but it does mean FINDLINKS cannot be scoped to a specific home document.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Link Indexing in the Spanfilade: Complete Analysis

### Short answer

A link is indexed **three separate times** in the spanfilade — once for each of its endsets (from, to, three) — under three distinct, compile-time-constant span-type tags. The indexing position is fixed at link creation time and is entirely independent of which endpoint any future query happens to match.

---

### The constants: `xanadu.h:35–39`

```c
/* spanfilade span types */
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

These four integers are the only "column" discriminators in the spanfilade's ORGL dimension. The first three partition the link-endpoint space; DOCISPAN is for document content.

---

### Link creation: `do1.c:195–221` — `docreatelink`

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset, typespecset threespecset,
    typeisa *linkisaptr)
{
  ...
  && specset2sporglset(taskptr, fromspecset,  &fromsporglset, NOBERTREQUIRED)
  && specset2sporglset(taskptr, tospecset,    &tosporglset,   NOBERTREQUIRED)
  && specset2sporglset(taskptr, threespecset, &threesporglset,NOBERTREQUIRED)
  && setlinkvsas(&fromvsa, &tovsa, &threevsa)
  && insertendsetsinorgl(taskptr, linkisaptr, link,
         &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
  && insertendsetsinspanf(taskptr, spanf, linkisaptr,
         fromsporglset, tosporglset, threesporglset)    // line 219
```

There is also an older two-endset path in `do1.c:169` — `domakelink` — which passes `NULL` for the third endset:

```c
  && insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, NULL)
  // do1.c:191
```

---

### The dispatcher: `do2.c:116–128` — `insertendsetsinspanf`

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset,
    typesporglset threesporglset)
{
  if (!(
     insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // line 119
  && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)))   // line 120
        return (FALSE);
  if (threesporglset) {
    if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))  // line 123
        return (FALSE);
  }
  return (TRUE);
}
```

`from` and `to` are always indexed. `three` is indexed only when non-NULL. No conditional logic touches the tag value — `LINKFROMSPAN` is always 1, `LINKTOSPAN` always 2, `LINKTHREESPAN` always 3, bound at the call site, not computed from the endset content.

---

### How the tag is physically stored: `spanf1.c:15–54` — `insertspanf`

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *isaptr, typesporglset sporglset, INT spantype)
{
  ...
  prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // line 22
  ...
  for (; sporglset; ...) {
      movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
      movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
      insertnd(taskptr, (typecuc*)spanfptr,
               &crumorigin, &crumwidth, &linfo, SPANRANGE);     // line 51
  }
```

The spanfilade is a 2-dimensional structure. At insertion:

- **ORGL dimension** (the "who" axis): the link's ISA (`isaptr`) is prefixed by `spantype`. A link with ISA `A` gets stored at ORGL coordinate `1.A` for its from-endset, `2.A` for to, `3.A` for three.
- **SPAN dimension** (the "what" axis): the ispan (permascroll address range) of the endset content — the result of translating the vspan through V↔I conversion.

This is the only place the tag is consumed in the write path. It is passed in as a compile-time constant and not modified.

---

### The V-space addresses of the endsets in the link document: `do2.c:169–183` — `setlinkvsas`

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
  tumblerclear(fromvsaptr);
  tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // from endset → V=1.x
  tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);
  tumblerclear(tovsaptr);
  tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // to endset → V=2.x
  tumblerincrement(tovsaptr, 1, 1, tovsaptr);
  if (threevsaptr) {
      tumblerclear(threevsaptr);
      tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // three endset → V=3.x
      tumblerincrement(threevsaptr, 1, 1, threevsaptr);
  }
```

Inside the link's own document, the three endsets are stored at VSA positions 1.x, 2.x, and 3.x respectively. These V-positions mirror the LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN constants exactly — from endset sits at V=1.x, to at V=2.x, three at V=3.x — though this is by convention, not by sharing the same variable.

---

### Link search: `spanf1.c:56–103` — `findlinksfromtothreesp`

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr,
    typespecset fromvspecset, typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrange, typelinkset *linksetptr)
{
  ...
  if (fromvspecset)
      sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset,
                        &fromlinkset, orglrange, LINKFROMSPAN);   // line 77
  if (tovspecset)
      sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset,
                        &tolinkset, orglrange, LINKTOSPAN);       // line 85
  if (threevspecset)
      sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset,
                        &threelinkset, orglrange, LINKTHREESPAN); // line 93
  intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // line 100
```

The search side is the mirror image of insertion: each of the three specset arguments is queried independently against its own slot in the ORGL dimension, and the three result link-sets are intersected. A NULL argument for any slot means that slot is skipped and its result-set stays NULL; `intersectlinksets` treats a NULL input as "no constraint" (equivalent to the universal set), so omitting a slot widens rather than narrows the result.

The same three hard-coded constants appear here that appeared in `insertendsetsinspanf`. There is no runtime path that remaps a query's "from" specset to the "to" slot or vice versa.

---

### Endset retrieval: `spanf1.c:190–235` — `retrieveendsetsfromspanf`

When the caller wants to read back a known link's endsets (e.g., after `dofollowlink`), the function scans the spanfilade using explicit ORGL-range windows:

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // line 210
fromspace.width.mantissa[0]   = 1;
tospace.stream.mantissa[0]    = LINKTOSPAN;     // line 213
tospace.width.mantissa[0]     = 1;
threespace.stream.mantissa[0] = LINKTHREESPAN;  // line 216
threespace.width.mantissa[0]  = 1;
...
retrievesporglsetinrange(taskptr, sporglset, &fromspace,  &fromsporglset)   // line 223
retrievesporglsetinrange(taskptr, sporglset, &tospace,    &tosporglset)     // line 225
retrievesporglsetinrange(taskptr, sporglset, &threespace, &threesporglset)  // line 230
```

The window is a single ORGL unit wide, centered on the constant (1, 2, or 3). This retrieval is also fully position-fixed.

---

### Summary

| Question | Answer |
|---|---|
| Which endset slot(s) are indexed? | All three (from, to, three) — each in its own slot |
| How is each slot distinguished? | By a compile-time integer prefix on the link ISA in the ORGL dimension: LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 (`xanadu.h:36–38`) |
| Is `three` always indexed? | No — only when `threesporglset != NULL` (`do2.c:122`). `domakelink` always passes NULL for three (`do1.c:191`); `docreatelink` passes it through (`do1.c:219`). |
| Is the position fixed? | Yes, absolutely. The tag is a compile-time constant assigned by structural role (from/to/three), not by endset content. It is identical at write time (`insertendsetsinspanf`, `do2.c:119–123`) and read time (`findlinksfromtothreesp`, `spanf1.c:77,85,93`). |
| Is it query-independent? | Yes. The spanfilade stores a link's from-endset content at ORGL=`1.linkISA` regardless of what any future query will ask. The query function (`findlinksfromtothreesp`) hard-codes the same constant for the same slot. No runtime remapping exists. |
