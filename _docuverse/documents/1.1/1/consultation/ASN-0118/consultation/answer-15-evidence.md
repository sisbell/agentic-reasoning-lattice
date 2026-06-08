## Question 15 [evidence]

> Does COPY create a DOCISPAN entry in the spanfilade for the target document while the source document's spanfilade entries remain untouched?

## KB Synthesis

Yes. `docopy()` calls `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` where `docisaptr` is the **target** document's ISA [SS-DOCISPAN/Finding 0036, code ref `do1.c:62`]. It registers the copied I-addresses as belonging to the target, creating one DOCISPAN entry per contiguous I-span [ST-COPY/Finding 0047].

The source document's DOCISPAN entries — created when that content was first placed via INSERT or an earlier COPY — are completely untouched. Because the spanfilade is append-only with no delete operation [INV-SPANF-WRITE-ONLY], those source entries persist permanently.

The net effect: after COPY, **both** source and target documents are registered in the spanfilade for the copied I-addresses. `find_documents` on those I-addresses returns both [INT-CROSS-SESSION-TRANSCLUSION, FC-CONTENT-SPANF-ISOLATION]. This is the mechanism underlying transitive content identity — the spanfilade accumulates provenance across all documents that have ever held given I-addresses, regardless of subsequent deletions [INV-IADDRESS-PERMANENT].

---

## Code Exploration

The key line numbers are verified. Here is the full answer:

---

## COPY and DOCISPAN: Full Code Trace

**Short answer: Yes.** COPY creates a DOCISPAN entry in the spanfilade for the target document. The source document's spanfilade is never touched — it is only read to convert V-space addresses to I-space.

---

### 1. Entry Point: `fns.c:35–46`

```c
void copy(typetask *taskptr)
{
  typeisa docisa, vsa;
  typespecset localspecset;
  bool getcopy(), docopy();

    if (
       getcopy (taskptr, &docisa, &vsa, &localspecset)
    && docopy (taskptr, &docisa, &vsa, localspecset))
        putcopy (taskptr);
      else
        putrequestfailed (taskptr);
}
```

`copy()` parses the incoming FEBE request, then delegates entirely to `docopy()`.

---

### 2. Core Logic: `do1.c:45–65`

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  typeispanset ispanset;
  typeorgl docorgl;
  ...

    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  /* line 54 */
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)       /* line 55 */
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)

    /* the meat of docopy: */
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)        /* line 60 */
    &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)    /* line 62 */
    && asserttreeisok(docorgl)
    );
}
```

Two writes to the target, one read from the source:

| Call | Target? | What it does |
|---|---|---|
| `specset2ispanset()` [line 54] | **Source read** | Converts V-spans to I-spans; never modifies source |
| `insertpm()` [line 60] | **Target write** | Updates target document's POOM (permutation enfilade) |
| `insertspanf(..., DOCISPAN)` [line 62] | **Target write** | Creates DOCISPAN entries in the global spanfilade for the target document |

---

### 3. DOCISPAN Insertion: `spanf1.c:15–54`

```c
bool insertspanf(typetask *taskptr, typespanf spanfptr, typeisa *isaptr,
                 typesporglset sporglset, INT spantype)
{
  typedsp crumorigin;
  ...
        prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  /* line 22 */
        tumblerclear (&crumwidth.dsas[ORGLRANGE]);
        clear (&linfo, sizeof(linfo));
        for (; sporglset; ...) {
                if (itemid == ISPANID) {
                        movetumbler (&((typeispan *)sporglset)->stream, &lstream);
                        movetumbler (&((typeispan *)sporglset)->width, &lwidth);
                        movetumbler (isaptr, &linfo.homedoc);          /* line 29 */
                }
                ...
                movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
                movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
             insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); /* line 51 */
        }
        return (TRUE);
}
```

**`spanf1.c:22`** — `prefixtumbler(isaptr, spantype, ...)` builds the ORGLRANGE dimension of the new spanfilade crum key from `isaptr` (the **target document** ISA) and `spantype` (= `DOCISPAN` as passed from `do1.c:62`).

**`spanf1.c:29`** — `linfo.homedoc` is also set to the target ISA.

**`spanf1.c:51`** — `insertnd()` commits this crum into the global spanfilade. The key encodes `(target_doc_isa, DOCISPAN, i_stream_origin)` in the ORGLRANGE × SPANRANGE space.

The **source document ISA** never appears in `insertspanf`. The spans passed in (`ispanset`) are I-space coordinates extracted from the source, but the spanfilade records them under the **target document's** DOCISPAN slot.

---

### 4. Target Document Marked Modified: `orglinks.c:99`

```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl, tumbler *vsaptr,
              typesporglset sporglset)
{
  ...
    logbertmodified(orglisa, user);   /* line 99 — TARGET document only */
    for (; sporglset; ...) {
        ...
        insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
        ...
    }
    return (TRUE);
}
```

`logbertmodified()` is called once, with `orglisa` = the **target** document ISA. The source document has no corresponding call anywhere in the COPY path.

---

### 5. Source Document: Read-Only

`specset2ispanset()` [do1.c:54] calls:

```
specset2ispanset → vspanset2ispanset [orglinks.c] → permute → span2spanset
                                                              → retrieverestricted()
```

`retrieverestricted()` (in `retrie.c`) traverses the source document's POOM enfilade to convert V-addresses to I-addresses. It **returns context structures**; it makes no calls to `insertnd`, `logbertmodified`, or any write operation. The source's spanfilade is not accessed at all during this conversion.

---

### Summary

| Part of the system | Source doc | Target doc |
|---|---|---|
| Spanfilade (`spanf`) | **Untouched** | **New DOCISPAN crums inserted** via `insertspanf` [spanf1.c:51] keyed on target ISA [spanf1.c:22] |
| POOM granfilade | Read-only (V→I lookup) | Updated by `insertpm` [orglinks.c:99+] |
| Bert (open-doc log) | Not marked | Marked modified [orglinks.c:99] |

COPY records *what content the target document contains and where it came from* by inserting DOCISPAN entries into the spanfilade under the target's ISA. The source document's spanfilade entries are never modified — they remain as the permanent record of where that content originally lives.
