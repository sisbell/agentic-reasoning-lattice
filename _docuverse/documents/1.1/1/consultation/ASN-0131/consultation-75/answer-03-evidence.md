## Question 3 [evidence]

> What form does the region argument of RETRIEVEENDSETS take in udanax-green — a single contiguous span of V-positions (a vspan, presented as a start and width), or an arbitrary set of V-positions?

## KB Synthesis

RETRIEVEENDSETS (opcode 28) takes an arbitrary set of V-positions — specifically a **SpecSet** (sequence of VSpecs), not a single contiguous span.

From [SS-RETRIEVE-ENDSETS]:

> RETRIEVEENDSETS (opcode 28) takes a **specset** (V-spec of a content region) and returns three specsets simultaneously: from-endset, to-endset, and three-endset.

The call chain confirms this: `retrieveendsetsfromspanf()` first converts the input specset to a **sporglset** via `specset2sporglset()` (V-to-I translation), then searches the spanfilade with SPANRANGE and ORGLRANGE restrictions per endset type. The input is processed exactly as `find_links` processes its search input — the entire specset is converted to I-addresses en masse, and the spanfilade is searched for link endpoints whose I-addresses intersect.

This is consistent with the general SpecSet model [SS-SPECSET]: a SpecSet is a `seq<VSpec>` where each VSpec is a `(doc, start, width)` triple. It can contain multiple non-contiguous spans across one or more documents.

The contrast with RETRIEVEDOCVSPAN / RETRIEVEDOCVSPANSET (which return single-span or spanset results describing a document's extent) is relevant here — those operations describe document structure, while RETRIEVEENDSETS takes an arbitrary user-specified content region as input [SS-VSPAN-VS-VSPANSET].

So: the region argument is a **SpecSet** — an ordered sequence of VSpecs, each identifying a (document, start, width) triple, capable of covering non-contiguous regions across multiple documents.

---

## Code Exploration

I now have a complete picture from the source code. Here is my answer.

---

## The RETRIEVEENDSETS Region Argument

The region argument to RETRIEVEENDSETS is **an arbitrary set of V-positions**, not a single contiguous vspan. The type is `typespecset`, a linked list of heterogeneous spec elements.

---

### Type Structure

From `backend/xanadu.h`:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid itemid;
    tumbler stream;        // start position
    tumbler width;         // width
} typespan;

typedef typespan typevspan;
typedef typevspan * typevspanset;   // linked list of V-spans

typedef struct structtypevspec{
    struct structtypevspec *next;
    typeitemid itemid;
    typeisa docisa;           // document ISA (tumbler)
    typevspanset vspanset;    // linked list of V-spans
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;   // linked list of specs
```
[`xanadu.h:65-89`]

So a `typespecset` is a **linked list of specs**, where each spec is either an I-span (direct permascroll interval) or a V-spec (document + set of V-spans).

---

### Wire Protocol Parsing

`getretrieveendsets` in `get1fe.c:192` does nothing but call `getspecset`:

```c
bool getretrieveendsets(typetask *taskptr, typespecset *specsetptr)
{
    return (getspecset (taskptr, specsetptr));
}
```
[`get1fe.c:192-195`]

`getspecset` in `get2fe.c:147-180` reads the argument as:

```c
if (!getnumber (taskptr, &num)) { ... }   // outer count N
while (num--) {
    c = pullc(taskptr);
    if ((c != SPANFLAG) && (c != VSPECFLAG))  // 's' or 'v'
        return(FALSE);
    if (c == SPANFLAG) {
        specset = taskalloc(taskptr, sizeof(typespan));
        getspan(taskptr, specset, ISPANID);         // stream + width tumblers
    } else {
        specset = taskalloc(taskptr, sizeof(typevspec));
        getvspec(taskptr, specset);                 // docisa + vspanset
    }
}
```
[`get2fe.c:147-179`]

`getvspec` at `get2fe.c:182-189` reads the V-spec case:
```c
vspecptr->itemid = VSPECID;
return (
   gettumbler (taskptr, &vspecptr->docisa)           // document ISA
&& getspanset (taskptr, &vspecptr->vspanset, VSPANID)); // M vspans
```

`getspanset` at `get2fe.c:192-210` reads M spans (each a start + width tumbler pair) as a **linked list** — so a single V-spec can contain **multiple non-contiguous V-spans**.

`getspan` at `get2fe.c:213-221` reads each individual span as exactly two tumblers: stream (start) and width.

---

### Wire Format (BNF)

```
<spec set>    ::= <count>~ (<spec>)*
<spec>        ::= 's'~ <tumbler> <tumbler>          ; I-span: start width
               |  'v'~ <tumbler> <count>~ (<tumbler> <tumbler>)*  ; V-spec: docisa nvspans vspan*
```

Flag constants: `SPANFLAG = 's'`, `VSPECFLAG = 'v'`, `WORDELIM = '~'` [`get2fe.c:15-18`].

---

### How `doretrieveendsets` Consumes the Specset

`doretrieveendsets` in `do1.c:369-373` delegates directly to `retrieveendsetsfromspanf`:

```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, typespecset *fromsetptr, typespecset *tosetptr, typespecset *threesetptr)
{
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```
[`do1.c:369-374`]

`retrieveendsetsfromspanf` at `spanf1.c:190-235` calls `specset2sporglset` first, which walks the **entire** linked list of specs:

```c
for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        // direct I-span: pass through as sporgl
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        // V-spec: translate each vspan to I-addresses via orgl
        vspanset2sporglset(taskptr, &((typevspec*)specset)->docisa,
                           ((typevspec*)specset)->vspanset, ...)
    }
}
```
[`sporgl.c:14-33`]

`vspanset2sporglset` at `sporgl.c:35-65` iterates the full `vspanset` (inner linked list), calling `vspanset2ispanset` for each V-span to translate it to I-addresses. Multiple non-contiguous V-spans within a single V-spec are each converted.

---

### One Important Quirk

After the specset-to-sporglset conversion, `retrieveendsetsfromspanf` uses a blind cast to extract the doc ISA for the I-to-V return conversion:

```c
linksporglset2specset(taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, ...)
```
[`spanf1.c:224`]

This casts the *first* element of `specset` directly to `typevspec *` to get `docisa`. If the specset contained only I-spans (no V-spec first), or if there were multiple V-specs with different docisas, this would use only the first spec's docisa for all I-to-V output resolution. In practice RETRIEVEENDSETS is always called with a V-spec as the first element.

---

### Answer

**RETRIEVEENDSETS takes an arbitrary set of V-positions — not a single contiguous vspan.**

The region argument is a `typespecset`: a linked list of specs tagged as either:
- An **I-span** (`'s'` flag): a direct permascroll interval, represented as a start tumbler + width tumbler.
- A **V-spec** (`'v'` flag): a document ISA tumbler + a linked list of V-spans, each a start tumbler + width tumbler.

The outer list can contain multiple specs. A single V-spec element can itself contain multiple non-contiguous V-spans in its inner `vspanset`. The combination makes the argument a fully general **set of V-intervals across potentially multiple documents**, not a single start/width pair.

In the typical call the argument is one V-spec containing one or a few contiguous V-spans that identify a content region, but the protocol and implementation handle the general case at every level.
