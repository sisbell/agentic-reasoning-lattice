## Question 16 [evidence]

> When reading transcluded content shared across documents (same I-address, different V-positions), does the read from each document's V-space return byte-identical content, and does the read path differ at all from reading natively-inserted content?

## KB Synthesis

Yes to both, with one path difference at the POOM lookup stage.

## Byte identity

Since vcopy shares I-addresses rather than copying content [ST-VCOPY, Finding 0002], both V-positions—in whichever documents—map to the same I-address range in the permascroll. The granfilade stores bytes at I-addresses immutably and permanently [INV-IADDR-IMMUTABILITY, Finding 0064]. Retrieval dereferences I-addresses to raw bytes via `ispanset2vstuffset` using `movmem` with no encoding conversion [SS-CONTENT-IDENTITY, Finding 0034]. Same I-address range → identical bytes, always.

## Read path

The path has two stages:

**Stage 1 — V → I (per-document POOM lookup):** Each document has its own POOM [SS-POOM-MUTABILITY, Finding 0072]. `specset2ispanset` calls `findorgl` on the specific document's orgl and traverses that document's POOM to convert V-spans to I-spans. This stage differs per document. Precondition: the document must be open [PRE-RETRIEVE-CONTENTS, Finding 0027].

**Stage 2 — I → bytes (global granfilade):** `ispanset2vstuffset` looks up the I-address range in the single global `granf` [SS-GRANF-OPERATIONS, Finding 0012]. Because the I-addresses are identical, this stage is completely identical regardless of which document, which V-position, or whether the content was originally inserted or transcluded.

Natively-inserted content follows the same two stages. The POOM entry for inserted content has the same structure as one created by vcopy [FC-INSERT-IADDR, Finding 0030]—the granfilade is indifferent to how the V→I mapping was established.

**Only observable difference:** each referencing document must independently satisfy the open-document precondition before `findorgl` will proceed [PRE-RETRIEVE-CONTENTS, Finding 0027]. The bytes produced are guaranteed identical [INV-IADDR-IMMUTABILITY].

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full analysis:

---

## Transcluded Content Retrieval: Read Path and Content Identity

### Architecture Overview

The store has three layers relevant to this question:

1. **Granfilade** — a global sequential store indexed by I-address (tumbler). Stores actual text bytes. An I-address is a permanent, global identifier. Text is written here once; it never moves.

2. **Per-document POOM** (orgl, a 2D enfilade) — maps V-positions → I-addresses for one document. A 2D bottom crum (`type2dcbc`) records `{cdsp[I], cwid[I], cdsp[V], cwid[V], homedoc}`.

3. **Spanfilade** — records which documents contain which I-spans (for link following; not involved in content retrieval).

---

### Insertion: Native vs. Transcluded

**Native insert** (`doinsert` → `inserttextingranf` → `docopy`):

```
doinsert() [do1.c:87]
  makehint(DOCUMENT, ATOM, TEXTATOM, ...)
  inserttextingranf() [granf1.c:44] → inserttextgr() [granf2.c:63]
    → allocates new I-address, stores bytes in granfilade
    → returns ispanset = {stream: I-start, width: I-len}
  docopy() [do1.c:45]
    → insertpm() [orglinks.c:75]
        → insertnd() [insertnd.c:15]  (inserts 2D crum into POOM)
           crum: {I: new-ispan, V: requested-vsa, homedoc: docisa}
    → insertspanf()  (spanfilade bookkeeping only)
```

**Transcluded copy** (`docopy` only, called from `doinsert`'s internal use of `docopy`, or directly via `copy` FEBE command):

```
docopy() [do1.c:45]
  specset2ispanset() [do2.c:14]
    → findorgl() [granf1.c:17]  (finds SOURCE document's POOM)
    → vspanset2ispanset() [orglinks.c:397]
        → permute() [orglinks.c:404]
            → span2spanset() [orglinks.c:425]
                → retrieverestricted() [retrie.c:56]  (walks SOURCE POOM)
                    → retrieveinarea() → findcbcinarea2d() [retrie.c:229]
                → context2span()   (extracts I-range from 2D crum)
    → returns ispanset = same I-addresses as original
  findorgl() [granf1.c:17]  (finds DESTINATION document's POOM)
  insertpm() [orglinks.c:75]
    → insertnd() [insertnd.c:15]  (inserts 2D crum into DEST POOM)
       crum: {I: SAME-ispan, V: new-dest-vsa, homedoc: dest-docisa}
  insertspanf()  (spanfilade bookkeeping only)
```

**Key fact:** No bytes are written to the granfilade during transclusion. The destination POOM receives a crum pointing to the **identical I-address range**. The crums in both POOMs are structurally identical `type2dcbc` records; neither is marked "native" or "transcluded." There is no such flag in the data structure.

---

### Retrieval Path (identical for both cases)

```
doretrievev() [do1.c:338]
  specset2ispanset(taskptr, specset, &ispanset, READBERT)  [do2.c:14]
    → findorgl(taskptr, granf, &docisa, &docorgl, READBERT)  [granf1.c:17]
        → fetchorglgr() [granf2.c:22]  (fetches POOM root from granfilade)
    → vspanset2ispanset(taskptr, docorgl, vspanset, ispansetptr)  [orglinks.c:397]
        → permute(taskptr, orgl, vspanptr, V, ispansetptr, I)  [orglinks.c:404]
            → span2spanset()  [orglinks.c:425]
                → retrieverestricted(orgl, vspan, V, NULL, I, NULL)  [retrie.c:56]
                    → retrieveinarea()  [retrie.c:87]
                        → findcbcinarea2d()  [retrie.c:229]
                           walks POOM crums, returns all crums overlapping V-range
                → context2span()  extracts I-range from each found crum
    returns: ispanset of I-addresses
  ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)  [granf1.c:58]
    → ispan2vstuffset(taskptr, granfptr, ispanset, vstuffsetptr)  [granf2.c:198]
        → retrieveinspan(granf, lowerbound, upperbound, WIDTH)  [retrie.c:112]
            → findcbcinspanseq()  [retrie.c:307]
               walks granfilade crums at those I-addresses, returns text bytes
```

This path is **exactly the same** whether the POOM crum was created by native insert or by transclusion. The retrieval code never inspects any "origin" flag — it only cares about the 2D spatial coordinates of each crum.

---

### Does the homedoc Field Differentiate Them?

The `crumqualifies2d()` guard in `retrie.c:274` does check `homedoc`:

```c
/* retrie.c:274 */
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc*)crumptr)->c2dinfo.homedoc)))
    return (FALSE);
```

But this guard only fires when `infoptr != NULL`. Trace `span2spanset()` [orglinks.c:425]:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
                                                            ^^^^^^^^^^^^^^
```

The last argument is `(typeisa*)NULL`, so in `retrieverestricted()` [retrie.c:77–82]:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;   /* ← always taken */
}
```

`infoptr` is always `NULL` in the V→I conversion path. The homedoc filter is **never applied** during content retrieval. The POOM walk is purely spatial.

---

### Byte Identity Guarantee

Both documents' POOMs point to the **same I-address range** in the granfilade. The granfilade is a deterministic sequential store: `retrieveinspan(granf, lowerbound, upperbound, WIDTH)` [retrie.c:112] returns a context from `findcbcinspanseq()`, which walks granfilade crums by I-address with no document context at all. Given identical I-spans, it returns identical bytes.

**Answer: Yes, byte-identical content. No path difference.**

Reads of transcluded content (same I-address, different V-positions in different documents) follow exactly the same code path as reads of natively inserted content. The retrieval path is:

```
V-spec → POOM walk (findcbcinarea2d) → I-span → granfilade walk (findcbcinspanseq) → bytes
```

This path is taken in full for every `doretrievev()` call, regardless of whether the POOM crum was created by `inserttextingranf`+`insertpm` (native) or by `vspanset2ispanset`+`insertpm` (transclusion). The granfilade itself has no concept of document ownership — it stores bytes at I-addresses and returns them when asked. The bytes at a given I-address are written once and never change, so every reader of that I-address, from any document, gets the same bytes.
