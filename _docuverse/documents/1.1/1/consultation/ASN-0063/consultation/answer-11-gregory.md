## Question 11 [gregory]

> When `docreatelink` creates the link orgl in the granfilade, what is the exact internal structure stored — how are the three endsets (source, target, type) laid out within the orgl, and does each endset support multiple disjoint I-spans or only a single contiguous span?

## KB Synthesis

## Link Orgl Internal Structure

The KB answers this partially but has a gap at the byte-level serialization layer.

### What the KB confirms

**Endset positions within the link orgl** [SS-FOLLOWLINK]:

`link2sporglset()` extracts each endset by calling `retrieverestricted()` against the link orgl at one of three internal positions:
- `0.1` — FROM endset (source)
- `0.2` — TO endset (target)
- `0.3` — THREE endset (type)

These are I-space sub-addresses within the link orgl itself. The same position constants map to the spanfilade ORGLRANGE subspaces: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [SS-RETRIEVE-ENDSETS].

**Each endset supports multiple disjoint I-spans — confirmed** [SS-LINK-ENDPOINT, Finding 0037]:

> A single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources. Each I-span independently tracks its content identity.

Formally: `Endset = set<Sporgl>` where `|Endset| >= |input_vspans|`. The inner loop in `vspanset2sporglset` (`sporgl.c:49-58`) iterates over every I-span returned by `vspanset2ispanset` and creates a **separate sporgl per contiguous I-address region**. So a V-span over "AABB" (where "AA" came from doc A and "BB" from doc B) produces two sporgls in the endset, not one.

This splitting happens automatically at link creation time — the front end provides contiguous V-spans; the backend decomposes them [ST-LINK-CREATE, Finding 0037].

**What a sporgl contains** [SS-SPORGL]:

```
Sporgl = { origin: IAddress, width: TumblerWidth, source_doc: ISA }
```

Stored as `typesporglset` (linked list), interchangeable with `typeispan` via a union type `typesporglitem`.

### What the KB does not cover

The exact serialization of how a sporglset (linked list of sporgls) is encoded within the granfilade at position 0.1/0.2/0.3 of the link orgl is **not described in the KB**. The KB documents that `retrieverestricted()` is used to access these positions — implying the link orgl has its own internal addressable structure — but does not describe the granfilade node layout for link orgls versus text atoms. The `typegrantext` byte-buffer layout [SS-CONTENT-IDENTITY, Finding 0034] is documented for text atoms, but no equivalent entry exists for link orgl node layout.

### Summary

| Question | Answer | Source |
|----------|--------|--------|
| How many endsets? | Three: FROM (0.1), TO (0.2), TYPE (0.3) | [SS-FOLLOWLINK] |
| Single contiguous span or multiple? | Multiple disjoint I-spans supported | [SS-LINK-ENDPOINT] |
| Internal format of each endset | Sporglset (linked list of sporgls) | [SS-SPORGL] |
| Byte-level serialization in granfilade | Not in KB | — |

---

## Code Exploration

I now have all the code I need. Here is the complete answer.

---

## How `docreatelink` lays out the link orgl

### The call sequence [`do1.c:195–221`]

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    typehint hint;
    tumbler linkvsa, fromvsa, tovsa, threevsa;
    typesporglset fromsporglset, tosporglset, threesporglset;
    typeorgl link;

    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)   // 1. alloc new orgl
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)         // 2. link ISA as I-span
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)           // 3. find V-slot in doc
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)          // 4. insert ref in doc
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)  // 5. fetch the orgl
      && specset2sporglset(taskptr, fromspecset, &fromsporglset, ...)  // 6. from→sporgls
      && specset2sporglset(taskptr, tospecset, &tosporglset, ...)      // 7. to→sporgls
      && specset2sporglset(taskptr, threespecset, &threesporglset, ...) // 8. type→sporgls
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)                 // 9. assign V-slots
      && insertendsetsinorgl(taskptr, linkisaptr, link,           // 10. write to orgl
                             &fromvsa, fromsporglset,
                             &tovsa, tosporglset,
                             &threevsa, threesporglset)
      && insertendsetsinspanf(taskptr, spanf, linkisaptr,         // 11. cross-index
                              fromsporglset, tosporglset, threesporglset)
    );
}
```

---

### Step 1: the orgl is a fresh POOM enfilade

`createorglingranf` → `createorglgr` [`granf2.c:111–128`]:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // <-- POOM, not GRAN or SPAN
```

Every link's orgl is a **POOM (Permutation Object-Oriented Matrix) enfilade**. A POOM bottom crum has two dimensions [`wisp.h:19–20`]:

- `I` (index 0) — permascroll address (I-span origin + width)
- `V` (index 1) — virtual address within the link's private V-space

These are stored as a `typewid` pair in each crum's `cdsp`/`cwid` fields [`enf.h:53–82`].

---

### Step 2: three fixed V-slots

`setlinkvsas` [`do2.c:169–183`] assigns the starting V-address for each of the three endsets:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear(fromvsaptr);
    tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // → 1
    tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);   // → 1.1   (FROM)

    tumblerclear(tovsaptr);
    tumblerincrement(tovsaptr, 0, 2, tovsaptr);       // → 2
    tumblerincrement(tovsaptr, 1, 1, tovsaptr);       // → 2.1   (TO)

    if (threevsaptr) {
        tumblerclear(threevsaptr);
        tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // → 3
        tumblerincrement(threevsaptr, 1, 1, threevsaptr);  // → 3.1  (THREE/type)
    }
}
```

`tumblerincrement(src, rightshift, inc, dst)` [`tumble.c:599–623`]: when `src` is zero, sets `dst->exp = -rightshift; dst->mantissa[0] = inc`. When non-zero, it appends a sub-digit by adding `inc` at `mantissa[idx + rightshift]`. The two-call sequence produces a **two-digit tumbler** 1.1, 2.1, or 3.1 — a hierarchical address where the first digit (1/2/3) is the endset discriminant and the second (.1) is the sub-address start.

The V-space layout of every link orgl is therefore:

| V-range | Endset |
|---------|--------|
| [1, 2)  | FROM (source) |
| [2, 3)  | TO (target) |
| [3, 4)  | THREE (type) |

---

### Step 3: writing into the orgl — `insertendsetsinorgl`

[`do2.c:130–149`]:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
                         tumbler *fromvsa, typesporglset fromsporglset,
                         tumbler *tovsa, typesporglset tosporglset,
                         tumbler *threevsa, typesporglset threesporglset)
{
    if (!(insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
       && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)))
        return FALSE;
    if (threevsa && threesporglset)
        insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
    ...
}
```

Each `insertpm` call operates on the link's POOM. The inner loop [`orglinks.c:100–131`]:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
              tumbler *vsaptr, typesporglset sporglset)
{
    for (; sporglset; sporglset = sporglset->xxxxsporgl.next) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);  // one I-span

        movetumbler(&lstream, &crumorigin.dsas[I]);    // I-origin = I-span start
        movetumbler(&lwidth,  &crumwidth.dsas[I]);     // I-width  = I-span width
        movetumbler(vsaptr,   &crumorigin.dsas[V]);    // V-origin = current slot position

        shift = tumblerlength(vsaptr) - 1;             // sub-digit level
        inc   = tumblerintdiff(&lwidth, &zero);        // integer count
        tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width ∝ I-span width

        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);

        tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);  // advance V for next sporgl
    }
}
```

**One POOM crum is created per `typesporgl` in the endset.** Each crum stores:
- `cdsp.dsas[I]` / `cwid.dsas[I]` — the I-span (permascroll origin + width)
- `cdsp.dsas[V]` / `cwid.dsas[V]` — a V-sub-address within this endset's slot
- `c2dinfo.homedoc` — the home-document ISA for the sporgl

After each crum, `vsaptr` advances by `crumwidth.dsas[V]`, so the next I-span occupies the next consecutive sub-address within the same [1,2)/[2,3)/[3,4) window.

---

### Does each endset support multiple disjoint I-spans?

**Yes, unconditionally.** The input sporglset is a linked list, and `insertpm` iterates over every element:

```c
for (; sporglset; sporglset = sporglset->xxxxsporgl.next) { ... }
```

Each disjoint I-span in the endset produces its own POOM bottom crum at a distinct V-sub-address within the slot. There is no merging, no single-span limit, and no guard against multi-span endsets.

The sporgl conversion in `specset2sporglset` / `vspanset2sporglset` [`sporgl.c:14–65`] already iterates over all `vspanset->next` entries — a single specset can produce arbitrarily many sporgls (one per V-span × I-span pair).

---

### Retrieval confirms the layout

`link2sporglset` [`sporgl.c:67–95`] reads back a given endset:

```c
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // stream = 1, 2, or 3
tumblerincrement(&zero, 0/*1*/, 1,   &vspan.width);   // width  = 1

context = retrieverestricted((typecuc*)orgl, &vspan, V,
                             (typespan*)NULL, I, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    contextintosporgl((type2dcontext*)c, NULL, sporglptr, I);
    ...
}
```

The V-window `[whichend, whichend+1)` (e.g. [1, 2) for FROM) captures every POOM crum stored under that endset, however many there are. Each returned context corresponds to one disjoint I-span. The I-dimension content (`c->totaloffset.dsas[I]` and `c->contextwid.dsas[I]`) gives the permascroll origin and width for that span.

---

### Spanfilade cross-index

In parallel, `insertendsetsinspanf` → `insertspanf` [`do2.c:116–128`, `spanf1.c:15–54`] registers the link in the global spanfilade for reverse lookup. Each I-span in each endset is stored under a prefixed orgl-address:

```c
prefixtumbler(linkisaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// spantype = LINKFROMSPAN(1), LINKTOSPAN(2), or LINKTHREESPAN(3)
```

So the spanfilade key is `1.<linkISA>`, `2.<linkISA>`, `3.<linkISA>` for FROM/TO/THREE respectively [`xanadu.h:36–39`]. This is the index used by `findlinksfromtothreesp` to find links by content.

---

### Summary

| Property | Value |
|----------|-------|
| Orgl enfilade type | POOM [`granf2.c:120`, `enf.h:14`] |
| Dimensions | I (permascroll) × V (link virtual space) |
| FROM endset V-slot | [1, 2), entries start at V=1.1 |
| TO endset V-slot | [2, 3), entries start at V=2.1 |
| THREE/type endset V-slot | [3, 4), entries start at V=3.1 |
| Multiple disjoint I-spans per endset | **Yes** — one POOM crum per I-span, each at consecutive V-sub-addresses within the slot [`orglinks.c:100–131`] |
| V-sub-address spacing | Proportional to I-span integer width; set via `tumblerincrement(&zero, shift=len-1, inc=width, ...)` |
| Retrieval window | `[whichend, whichend+1)` in V; returns all I-spans for that endset [`sporgl.c:80–83`] |

The three endsets (source=FROM=1, target=TO=2, type=THREE=3) are separated by their first V-digit, not by separate data structures. Multiple disjoint I-spans are first-class: each becomes its own POOM crum at a distinct V-sub-address, and `link2sporglset` recovers all of them in a single `retrieverestricted` call.
