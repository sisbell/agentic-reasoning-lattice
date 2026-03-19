# Revision Consultation — ASN-0025

**Review:** review-3.md
**Date:** 2026-03-07 07:56

## Summary

3 REVISE items analyzed: 2 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 2: CREATE LINK has conditional J0 verification and no document target

**Category:** BOTH
**Reason:** The ASN already implies links have V-space presence (DELETE section mentions "links at 2.x") but never specifies which document receives a link entry. Resolving this requires Nelson's design intent on whether every link belongs to a specific document, and Gregory's implementation evidence for which document the code targets.

**Nelson question:** When a link is created between spans in two documents, does Nelson's design require the link to reside in a specific document's V-space (e.g., the creating user's document), or can links exist in I-space without any V-space representation?

**Nelson's Answer:**

## Links Must Have a Home Document

Yes, my design absolutely requires every link to reside in a specific document. There are no free-floating objects in the system:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist." [LM 2/29]

The MAKELINK operation requires specifying a home document explicitly:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

> "The document must be specified because that determines the actual residence of the link—since a document may contain a link between two other documents." [LM 4/63]

That last point is crucial. When you create a link between spans in two other documents, the link lives in *your* document — the one you specify as home. The home document determines ownership, not destination:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

## Links Are I-Space Entities, Not V-Space

Links and bytes are the only two things actually stored in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

But links behave differently from bytes in a critical way. Bytes have both an I-space identity (permanent) and a V-space arrangement (mutable — shifts with insertions, deletions, rearrangements). Links do not participate in V-space rearrangement:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Links occupy the `0.2.N` subspace within a document, addressed sequentially by creation order:

```
N.0.U.0.D.V.0.2.1    → first link created in this document
N.0.U.0.D.V.0.2.755  → 755th link created
```

This address is permanent. Deleting link `2.5` does not renumber `2.6` onward. There is no "rearrange links" operation analogous to REARRANGE for text.

## Summary

| Property | Bytes | Links |
|----------|-------|-------|
| Stored in tumbler-space | Yes | Yes |
| Must belong to a document | Yes | Yes |
| Has permanent creation-order address | Yes (I-space) | Yes |
| Has mutable V-space arrangement | Yes | **No** |
| Can be rearranged by editing | Yes | No |

So to answer directly: a link **must** reside in a specific document — the home document specified at creation time, which is typically the creating user's document. The home document provides both addressability and ownership. But links are essentially I-space entities with permanent addresses in their creation order. They do not have a separate V-space "arrangement" the way bytes do. They cannot exist outside a document, but within their document they are fixed in their permanent order of arrival, not subject to V-space manipulation.

**Gregory question:** In the implementation, when `docreatelink` (or equivalent) creates a link, which document's POOM receives the link entry at element prefix 2.x — and is it always exactly one document?

**Gregory's Answer:**

## KB Synthesis

Exactly **one document** receives the link entry in its POOM — the **home document**, i.e., the first argument to `create_link(home_doc, source_specs, target_specs, type_specs)`.

## Mechanism

[ST-CREATE-LINK] (Finding 0012) documents the three-step sequence in `docreatelink`:

1. Create link orgl in `granf` via `createorglingranf()` → fresh ISA
2. **Copy the ISA into the home document's link subspace via `docopy()`**
3. Index endpoint I-addresses in `spanf` via `insertendsetsinspanf()`

Step 2 calls `findnextlinkvsa()` to compute the V-position within the home document, then `docopy()` → `insertpm()` to insert into that document's POOM. The code reference is `do1.c:199-225`.

## V-Position Details

[SS-LINK-SUBSPACE] (Finding 0052) specifies that `findnextlinkvsa()` always operates on the home document's POOM:
- First link: placed at `2.1` (internally); subsequent links at `vspanreach` (end of document's `2.x` extent)
- [SS-DUAL-ENFILADE] (Finding 0038) clarifies that `2.x` is the actual stored position; `retrieve_vspanset` normalizes to `0.x` in output when the document also contains text

## Why Only One

The source and target endpoint documents are **not** modified in their POOMs by link creation. [SS-THREE-LAYER-MODEL] (Finding 0040) makes this explicit:

> CREATELINK writes to all three layers: (1) I-space — link orgl; (2) Spanfilade — endpoint I-address index entries; (3) POOM — **the document's** V-stream at V-position 2.x

The "document" in layer 3 is the home document exclusively. Endpoint documents receive no POOM modifications; the spanfilade receives index entries for discovery, but that's a separate structure from any document's POOM.

[SS-LINK-HOME-DOCUMENT] (Finding 0025) further confirms: "The home document is distinct from the source document — a link's home document need not be the document containing the link's source endpoint." A link's source and target documents are identified only at discovery time (via spanfilade I-address intersection), never by POOM mutation.

---

## Code Exploration

I now have a complete picture. Here is the full analysis:

---

## Answer: Which Document's POOM Receives the Link Entry at Element Prefix 2.x?

### The short answer

**The hosting document — `docisaptr`, the document argument passed to `createlink` — is the only document whose POOM receives a link entry at V-address 2.x. It is always exactly one document. The from-, to-, and three-documents' POOMs are never written.**

---

### Tracing `docreatelink` [do1.c:195–221]

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);         // [207]
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)     // [209]
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)          // [210]
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)            // [211]
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)           // [212]
      && ...
      && insertendsetsinorgl (taskptr, linkisaptr, link, ...)      // [218]
      && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)    // [219]
    );
}
```

There are **three distinct "2.x" occurrences** in this call chain, all of which involve exactly one organule each.

---

### Occurrence 1 — The hosting document's POOM at V = 2.x

`findnextlinkvsa` [do2.c:151–167] computes where in `docisaptr`'s virtual address space to write the link reference:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // exp=0, mantissa[0]=2 → "2"
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // mantissa[1]+=1       → "2.1"
    // [do2.c:156–158]

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   // first link → V = 2.1
    else
        movetumbler (&vspanreach, vsaptr);  // nth link → V = (end of prior links)
}
```

`puttumbler` [put.c:26–46] prints `mantissa[0]=2, mantissa[1]=1` as **"2.1"**. Each additional link appended after the previous one continues the 2.x sequence (2.2, 2.3, ...).

`docopy(taskptr, docisaptr, &linkvsa, ispanset)` [do1.c:212] then inserts the link's ISA into **`docisaptr`'s POOM** at that V-address. The `ispanset` is the unit-width span around the link's ISA (`tumbler2spanset`, do2.c:48–61).

`docisaptr` is the only document whose POOM is written here.

The text–link boundary is confirmed by `findvsatoappend` [orglinks.c:29–49]:

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // → "2"
// text is placed below V=2; links start at V=2.1
```

V-space layout in `docisaptr`'s POOM:

| V-address | Content |
|-----------|---------|
| 1.x (mantissa[0]=1) | Text content — first text at 1.1 |
| 2.x (mantissa[0]=2) | Link ISA references — first link at 2.1 |
| 3.x (mantissa[0]=3) | (Type/three subspace — link internal) |

---

### Occurrence 2 — The link organule's own POOM at V = 2.1

`setlinkvsas` [do2.c:169–183] sets the internal endpoint positions within the link's own POOM:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    // fromvsa → 1.1
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);

    // tovsa → 2.1
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);

    // threevsa → 3.1
    tumblerincrement (threevsaptr, 0, 3, threevsaptr);
    tumblerincrement (threevsaptr, 1, 1, threevsaptr);
}
```

`insertendsetsinorgl` [do2.c:130–149] then calls:

```c
insertpm(taskptr, linkisaptr, link, fromvsa,   fromsporglset)   // V=1.1 in link's POOM
insertpm(taskptr, linkisaptr, link, tovsa,     tosporglset)     // V=2.1 in link's POOM
insertpm(taskptr, linkisaptr, link, threevsa,  threesporglset)  // V=3.1 in link's POOM
```

The first argument to `insertpm` is `linkisaptr`, **not** `docisaptr`. The "to" endpoint sporglset goes into the **link's own POOM** at V=2.1 — one fixed position per link, always. This is an internal structure of the link atom itself, not a document.

---

### Occurrence 3 — The link's I-address element subspace 2

`makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [do1.c:207] sets `atomtype = LINKATOM = 2` [xanadu.h:146].

`createorglingranf` → `findisatoinsertmolecule` [granf2.c:158–181] allocates the link's permanent I-address:

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // docISA → docISA.0.2
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);           // → docISA.0.2.1 (first link)
    else
        tumblerincrement (&lowerbound, 0, 1, isaptr);      // → subsequent links
```

Result: link ISA = `docISA.0.2.N`. For doc `1.1.0.1.0.1`, the first link ISA is `1.1.0.1.0.1.0.2.1`. The `0.2` part is: one zero-padding slot from rightshift=2, then value=LINKATOM=2 — the "element subspace 2" marker. Finding 0065 confirms this with golden output.

This I-address is allocated **per-document** in a bounded search anchored to `docisaptr`. Always one link's I-address per `createlink` call; always under `docisaptr`.

---

### Why only one document?

From/to/three specsets are converted to sporglsets [do1.c:214–216] and then written **only into `linkisaptr`'s POOM** via `insertendsetsinorgl`. No `docopy` or `insertpm` is called on the from-, to-, or three-document. Their organules are read (via `specset2sporglset` → `findorgl`) but never written.

Only `docopy(taskptr, docisaptr, &linkvsa, ispanset)` [do1.c:212] writes to a document POOM, and it writes to `docisaptr` exactly once.

---

### Summary table

| What | Where (V-address) | Whose POOM | Count per `createlink` |
|------|-------------------|------------|----------------------|
| Link ISA reference | 2.1, 2.2, … in `docisaptr`'s POOM | Hosting document (`docisaptr`) | **Exactly 1** |
| "to" endpoint | 2.1 in link's own POOM | The link organule (`linkisaptr`) | Exactly 1 |
| Link's I-address | `docISA.0.2.N` in granfilade | Under `docisaptr` | Exactly 1 |

**Conclusion:** The POOM entry at element prefix 2.x goes into `docisaptr` — the hosting document explicitly named in the `createlink` call — and only that document. It is invariably exactly one document. No matter how many endpoint documents the link points to, none of them receive a POOM modification at any V-address.
