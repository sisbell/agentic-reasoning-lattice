# Revision Consultation — ASN-0006

**Review:** review-3.md
**Date:** 2026-03-06 22:26

## Summary

8 REVISE items analyzed: 6 internal, 2 consulted (0 nelson, 2 gregory)

## Consultation Results

### Issue 3: AX1 claims universality but verifies only four operations

**Category:** GREGORY
**Reason:** The key question is whether MAKELINK modifies POOMs of multiple documents (e.g., registering link ISAs in each endpoint document's link subspace), which would falsify AX1. This requires implementation evidence.

**Gregory question:** Does MAKELINK modify the POOM of more than one document — specifically, does it register link ISAs in the link subspace of each document whose content appears in the link's endsets, or only in a single document's POOM?

**Gregory's Answer:**

## KB Synthesis

MAKELINK modifies the POOM of exactly **one document** — the home document. The POOMs of documents whose content appears in the link's endsets are not touched.

## What MAKELINK does to each layer

From [ST-CREATE-LINK] (Finding 0012), `docreatelink` performs three steps:

1. **Create link orgl in granf** — allocates a fresh ISA for the link object
2. **Copy link ISA into home document's POOM** — `findnextlinkvsa()` finds the next available 2.x V-position in the home document, then `docopy()` places the link ISA there
3. **Index endpoints in spanf** — `insertendsetsinspanf()` records the FROM/TO/THREE endpoint I-addresses in the spanfilade

Step 2 touches exactly one document's POOM: the home document, identified by the first parameter to `create_link(home_doc, ...)`. [SS-LINK-HOME-DOCUMENT] makes this explicit:

> The home document determines where the link's address is allocated... `address(link)` is allocated under `home`.

The source and target documents — whose content appears in the link's endsets — have their I-addresses recorded in the **spanf** (step 3), not in any POOM. This is why link discovery via `find_links` is content-identity-based (searches the spanf by I-address) rather than document-structure-based.

## Why the distinction matters

The spanf indexing in step 3 is what makes links discoverable from any document sharing endpoint content identity — including documents not involved in link creation. But this is a spanf operation, not a POOM operation. [FC-CONTENT-SPANF-ISOLATION] (Finding 0012) confirms: "only link creation and link following cross the boundary" between granf and spanf.

[SS-THREE-LAYER-MODEL] (Finding 0040) crystallizes the architecture:

- **I-space** (link orgl): permanent home for the link object
- **Spanfilade** (DOCISPAN entries): indexes endpoint I-addresses for discovery — written for all endpoint documents transitively via content identity
- **POOM** (document V-stream at 2.x): records the link in the home document's visible structure — written for **home document only**

So: one POOM write (home document's 2.x subspace), one spanf write (all endpoint I-addresses), zero POOM writes to source/target documents.

---

## Code Exploration

I now have a complete picture of the execution path. Here is the full analysis:

---

## Does MAKELINK Modify More Than One Document's POOM?

**Short answer: No. MAKELINK registers the link ISA in exactly one document's POOM — the single home document (`docisaptr`) passed to the operation. Documents referenced in the endsets have their POOMs read (for V→I conversion) but never written.**

---

### Execution path: `createlink` → `docreatelink`

`fns.c:100-112` — `createlink` calls `docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)`. `docisa` is the single home document.

`do1.c:195-221` — `docreatelink` executes this chain:

```c
createorglingranf(taskptr, granf, &hint, linkisaptr)       // 1. allocate link ISA in granfilade
&& tumbler2spanset(taskptr, linkisaptr, &ispanset)          // 2. link ISA as an ispan
&& findnextlinkvsa(taskptr, docisaptr, &linkvsa)            // 3. find next link-subspace VSA in home doc
&& docopy(taskptr, docisaptr, &linkvsa, ispanset)           // 4. *** WRITE HOME DOC'S POOM ***
&& findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED) // 5. get link's own orgl
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED) // 6. READ-ONLY V→I
&& specset2sporglset(taskptr, tospecset,  &tosporglset,   NOBERTREQUIRED) // 7. READ-ONLY V→I
&& specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // 8. READ-ONLY V→I
&& setlinkvsas(&fromvsa, &tovsa, &threevsa)                 // 9. compute link-internal VSAs
&& insertendsetsinorgl(taskptr, linkisaptr, link, ...)      // 10. *** WRITE LINK'S OWN POOM ***
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)    // 11. *** WRITE GLOBAL SPANFILADE ***
```

---

### Step 4 — Only `docisaptr`'s POOM is written

`do1.c:212`: `docopy(taskptr, docisaptr, &linkvsa, ispanset)`

`ispanset` is the link's own ISA (created by `tumbler2spanset(linkisaptr)` at `do2.c:48-60`). `linkvsa` is the next available position in `docisaptr`'s link subspace, computed by `findnextlinkvsa` (`do2.c:151-167`):

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{   ...
    (void) doretrievedocvspan(taskptr, docisaptr, &vspan);
    tumbleradd(&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp(&vspanreach, &firstlink) == LESS)
        movetumbler(&firstlink, vsaptr);   // first link VSA if no prior links
    else
        movetumbler(&vspanreach, vsaptr);  // else just past current end
    return (TRUE);
}
```

This reads `docisaptr`'s vspan and returns the next available link-subspace VSA — entirely within the home document. `docopy` then calls `insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)` (`do1.c:60`), which calls `insertnd(taskptr, (typecuc*)orgl, ...)` (`orglinks.c:130`) — `orgl` is `docisaptr`'s granfilade entry.

**Only `docisaptr`'s POOM is touched here.**

---

### Steps 6–8 — Endset documents are read, not written

`sporgl.c:14-65` — `specset2sporglset` with `NOBERTREQUIRED`:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset, typesporglset *sporglsetptr, int type)
{   ...
    for (; specset; ...) {
        if (...VSPECID...) {
            sporglsetptr = vspanset2sporglset(taskptr,
                &((typevspec *)specset)->docisa,
                ((typevspec *)specset)->vspanset,
                sporglsetptr, type);   // type = NOBERTREQUIRED
        }
    }
}
```

`vspanset2sporglset` (`sporgl.c:35-65`) calls `findorgl` (read-only) and `vspanset2ispanset` (read-only permutation) to translate V-coordinates to I-coordinates (permascroll addresses). It allocates `typesporgl` structs in task memory from the results, but **never calls `insertpm`, `insertnd`, or any write operation on the endset documents' POOMs**.

---

### Step 10 — The link's own POOM is written (not any content document)

`do2.c:130-149` — `insertendsetsinorgl`:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset, ...)
{   bool insertpm();
    if (!(insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset)))
            return (FALSE);
    if (threevsa && threesporglset)
        insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
    ...
}
```

`insertpm` (`orglinks.c:75-134`):

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{   ...
    logbertmodified(orglisa, user);           // orglisa = linkisaptr
    for (; sporglset; ...) {
        unpacksporgl(sporglset, &lstream, &lwidth, &linfo);
        ...
        insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orgl = link
    }
}
```

`orgl` here is `link` — the link's own granfilade entry found at step 5 via `findorgl(taskptr, granf, linkisaptr, &link, ...)`. The VSAs used are set by `setlinkvsas` (`do2.c:169-183`):

```c
fromvsa  = 0.1.1   // tumblerincrement(fromvsaptr, 0, 1); tumblerincrement(fromvsaptr, 1, 1)
tovsa    = 0.2.1   // tumblerincrement(tovsaptr, 0, 2); tumblerincrement(tovsaptr, 1, 1)
threevsa = 0.3.1   // tumblerincrement(threevsaptr, 0, 3); tumblerincrement(threevsaptr, 1, 1)
```

These V-positions are in the link's internal address space, not any content document's. **Only the link's own POOM is written.**

---

### Step 11 — Global spanfilade written (not a POOM)

`do2.c:116-128` — `insertendsetsinspanf` calls `insertspanf(taskptr, spanf, linkisaptr, fromsporglset, LINKFROMSPAN)` etc. `spanf` is the global spanfilade — a separate 2D enfilade indexed by `[ORGLRANGE × SPANRANGE]`, not a per-document POOM. This is what enables FIND queries to discover which links touch a given piece of content. It does not modify any document's POOM.

`spanf1.c:15-54` — `insertspanf` prefixes the link's ISA into `crumorigin.dsas[ORGLRANGE]` and calls `insertnd(taskptr, (typecuc*)spanfptr, ...)` — into `spanfptr`, the global spanfilade root.

---

### Conclusion

MAKELINK (`docreatelink`) modifies **exactly one document's POOM** — `docisaptr`, the home document passed to the operation. Its link subspace (V < 1.0) receives one entry: the new link's ISA, placed at the next available link-subspace address.

Documents referenced in the from/to/three endsets are accessed **read-only** via `specset2sporglset` (called with `NOBERTREQUIRED`) to translate their V-coordinates to I-coordinates. Their POOMs are not written; they receive no link ISA registration.

The endsets themselves are stored in two places:
1. **The link's own POOM** — at V-positions 0.1.1 (from), 0.2.1 (to), 0.3.1 (three), as I-addresses (permascroll coordinates) tagged with their home document ISAs. This is the link's internal structure (`insertendsetsinorgl`, `do1.c:218`).
2. **The global spanfilade** — indexed by content I-address, pointing to the link's ISA. This enables FIND queries (`insertendsetsinspanf`, `do1.c:219`).

If a link's endsets reference content in documents B and C, only the home document A's POOM is modified. B and C can be discovered later via the spanfilade (FIND), but are not modified by MAKELINK itself.

### Issue 7: Source specification inconsistency

**Category:** GREGORY
**Reason:** TC3 describes COPY as operating on a multi-document specset while all other formal properties use a single source_span from a single source_doc. Resolving the inconsistency requires knowing whether the implementation's COPY primitive accepts multi-document specsets or only single-span sources.

**Gregory question:** Does the COPY implementation accept a multi-document, multi-span specset as its source argument, or does it operate on a single contiguous V-span from a single source document (with multi-span COPY being a caller-level composition)?

**Gregory's Answer:**

## KB Synthesis

The KB is clear: `docopy()` accepts a multi-document, multi-span SpecSet directly. Multi-span COPY is not a caller-level composition.

**Direct evidence:**

From [SS-SPECSET] (Finding 0003): "A SpecSet can contain VSpecs referencing different documents and non-contiguous regions within the same document." Tests `vcopy_multiple_spans` and `vcopy_from_multiple_documents` both pass.

From [ST-VCOPY] (Finding 0003): "Cross-document vcopy (SpecSet referencing spans from multiple source documents) works **atomically**; all spans are placed into the target in a single operation."

From [PRE-COPY] (Finding 0046): The precondition analysis is written for `docopy()` receiving a specset — not just a single span. The code at `do1.c:45-65` calls `specset2ispanset` which iterates over all VSpecs in the SpecSet, resolving each to I-spans (potentially from different source documents' POOMs), producing a combined ispanset. Then `insertpm` places them all sequentially into the target, and `insertspanf` indexes them.

**Mechanism confirmation:**

[ST-COPY] (Finding 0047) notes: "COPY of fragmented source content (e.g., 3 non-contiguous regions) creates **3 DOCISPAN entries**" — this is a property of the single `docopy()` call, not of 3 separate calls. The `insertspanf` loop iterates over the full ispanset produced by `specset2ispanset`.

**One caveat from [PRE-VCOPY]:** `docopy()` has no type validation — a caller who constructs a SpecSet from `retrieve_vspanset` on a document with links will inadvertently include link ISAs in the source, which `docopy()` will copy into the target's POOM without complaint (`acceptablevsa()` always returns TRUE).

**Summary:** `docopy()` natively handles a multi-document, multi-span SpecSet in a single call. The `specset2ispanset` conversion layer does the per-VSpec resolution work internally.

---

## Code Exploration

I now have the complete call chain from wire format through to POOM insertion. Here is the full answer.

---

## COPY Source Argument: Multi-Document, Multi-Span Specset

**The COPY implementation natively accepts a multi-document, multi-span specset.** Multi-span copying is a single-operation primitive built into `docopy`, not a caller-level composition.

---

### Type Structure

`xanadu.h:78-89` defines the specset type:

```c
typedef struct structtypevspec{
    struct structtypevspec *next;   // linked-list pointer
    typeitemid      itemid;         // VSPECID
    typeisa docisa;                 // per-vspec document address
    typevspanset vspanset;          // multi-span list within that document
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A `typespecset` is a **linked list** of `typespec` nodes. Each node is either:
- A `VSPECID` (`typevspec`): carries its own `docisa` (document address) plus a `vspanset` (linked list of V-spans within that document).
- An `ISPANID` (`typeispan`): a raw I-span passed through directly.

Critically, each `typevspec` node carries its own independent `docisa`. There is no single-document restriction in the type.

---

### Wire-Format Parsing (FEBE Protocol)

`get1fe.c:54-63` — `getcopy` in the FEBE frontend:

```c
bool getcopy(typetask *taskptr, typeisa *docisaptr, typeisa *vsaptr, typespecset *localspecsetptr)
{
    return (
       gettumbler (taskptr, docisaptr)
    && gettumbler (taskptr, vsaptr)
    && getspecset(taskptr, localspecsetptr));
}
```

The source argument is a `typespecset`, read by the shared `getspecset` routine — the same routine used by `CREATELINK` and `RETRIEVEV`.

`get2fe.c:147-179` — `getspecset` in the FEBE frontend:

```c
bool getspecset(typetask *taskptr, typespecset *specsetptr)
{
    if (!getnumber (taskptr, &num)) return (FALSE);
    if (num == 0) return (TRUE);
    while (num--) {                                   // loop: N specs
        c = pullc(taskptr);
        if (c == SPANFLAG) {
            specset = (typespecset)taskalloc(...sizeof(typespan));
            getspan(taskptr, specset, ISPANID);
        } else {                                      // VSPECFLAG
            specset = (typespecset)taskalloc(...sizeof(typevspec));
            getvspec(taskptr, specset);               // reads docisa + vspanset
        }
        *specsetptr = specset;
        specsetptr = (typespecset*)&((typeitemheader *)specset)->next;
    }
    return (TRUE);
}
```

`get2fe.c:182-189` — `getvspec`:

```c
bool getvspec(typetask *taskptr, typevspec *vspecptr)
{
    vspecptr->itemid = VSPECID;
    vspecptr->next = NULL;
    return (
       gettumbler (taskptr, &vspecptr->docisa)       // one document ISA
    && getspanset (taskptr, &vspecptr->vspanset, VSPANID));  // N V-spans in it
}
```

`get2fe.c:192-210` — `getspanset` itself loops:

```c
while (num--) {                                       // loop: N spans per vspec
    spanset = (typespanset)taskalloc(...sizeof(typespan));
    getspan(taskptr, spanset, id);
    ...
}
```

So the wire format carries: `<N-specs> [<SPANFLAG|VSPECFLAG> <docisa> <N-spans> <span>...]...` — fully supporting multiple documents and multiple spans per document in a single COPY message.

---

### `docopy`: The Backend Entry Point

`do1.c:45-65`:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    typeispanset ispanset;
    typeorgl docorgl;

    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // V→I conversion
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // insert all I-spans
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
    && asserttreeisok(docorgl));
}
```

There is a single `specset2ispanset` call that consumes the entire specset and produces a single flat `ispanset`. That ispanset is then handed to `insertpm` in one call.

---

### `specset2ispanset`: Per-Document V→I Conversion

`do2.c:14-46`:

```c
bool specset2ispanset(typetask *taskptr, typespec *specset, typeispanset *ispansetptr, int type)
{
    typeorgl docorgl;
    ...
    *ispansetptr = NULL;
    for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {  // loop over all specs
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            *ispansetptr = (typeispanset)specset;          // pass-through I-span
            ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (!(
              findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // look up THIS spec's document
            && (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)))){
                return (FALSE);
            }
        }
    }
    return (TRUE);
}
```

The loop at `do2.c:23` walks the entire specset. At line 35, `findorgl` is called with **`((typevspec *)specset)->docisa`** — the `docisa` of the current spec node, not any global document. Each vspec independently resolves its V-spans through its own document's permutation matrix. The resulting I-spans are accumulated into one flat list.

---

### `insertpm`: Single-Call Multi-Span Insertion

`orglinks.c:75-134`:

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr, typesporglset sporglset)
{
    ...
    for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
        unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance VSA after each span
    }
    return (TRUE);
}
```

Every I-span in the accumulated list is inserted consecutively into the target document's POOM in a single `insertpm` call. The VSA auto-advances at `orglinks.c:131` so each span occupies the next available position.

---

### Conclusion

**COPY accepts a multi-document, multi-span specset natively.** The source argument is a `typespecset` — a linked list where each node independently specifies a document ISA and a set of V-spans within it. `specset2ispanset` resolves each node through its own document's permutation matrix. `insertpm` inserts all resulting I-spans consecutively at the target VSA in a single call.

Multi-span COPY is **not** caller-level composition. It is a single atomic operation. A client can specify source content drawn from arbitrarily many documents and arbitrarily many non-contiguous spans within each, and `docopy` handles the full resolution and insertion in one invocation.
