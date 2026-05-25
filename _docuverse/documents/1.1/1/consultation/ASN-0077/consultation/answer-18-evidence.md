## Question 18 [evidence]

> For a span originating from APPEND'd content (which skips `insertspanf` per [EC-APPEND-NO-DOCISPAN]), is there any backend mechanism to identify the origin document, or is such content origin-anonymous?

## KB Synthesis

APPEND'd content is **origin-anonymous** at the system's reverse-lookup level. Here is the synthesis:

## The Only Reverse-Lookup Mechanism Is DOCISPAN

[SS-DOCISPAN] establishes that the spanfilade's DOCISPAN sub-index is the sole backend mechanism for answering "which document contains this I-address?" — the mechanism underlying `FINDDOCSCONTAINING`. [EC-APPEND-NO-DOCISPAN] and [FC-APPEND-NO-DOCISPAN] both confirm that `doappend()` has the `insertspanf(..., DOCISPAN)` call commented out. Therefore, APPEND'd I-addresses produce no DOCISPAN entry, and `find_documents` will not return the containing document.

## Three Partial Mitigations, None Sufficient

**1. POOM crum `homedoc` field** [INV-IADDR-PROVENANCE]: Every POOM crum carries the origin document ISA in its `homedoc` field. But this metadata is only accessible when *already traversing a known document's POOM* — it answers "where did this crum's content originate?" not "which document contains this I-address?" It is per-crum metadata, not a searchable index.

**2. I-address tumbler structure** [SS-ADDRESS-SPACE, Finding 0065]: Text I-addresses are allocated under the document's address namespace (element field 3: `account.0.doc.0.3.N`), so the allocating document is structurally inferable via tumbler containment [SS-TUMBLER-CONTAINMENT]. However: the KB does not confirm APPEND uses the same `findisatoinsertmolecule` allocation path as INSERT, and tumbler-prefix inference is structural reasoning — not a backend query primitive.

**3. Direct POOM traversal** [SS-SPORGL, ST-VSPAN-TO-SPORGL]: `vspanset2sporglset` on a known document produces sporgls carrying provenance (`sporgladdress`). But this presupposes already knowing which document to query — exactly the information DOCISPAN would have provided.

## Conclusion

[INV-SPANF-GROWTH] characterizes the DOCISPAN index as growing with the number of distinct content placements via INSERT/COPY. APPEND is explicitly excluded from that accounting. Content placed via APPEND inhabits the granf but is invisible to the spanf's reverse index. Without DOCISPAN, no backend operation can discover the origin document from an APPEND'd I-address alone.

---

## Code Exploration

I now have everything I need to give a definitive answer. The finding [EC-APPEND-NO-DOCISPAN] rests on a code-reading error that I can show from the source.

---

## Finding: [EC-APPEND-NO-DOCISPAN] Is Incorrect — APPEND Content Is Origin-Trackable

The premise of the question is false. Tracing the actual call chain shows APPEND **does** reach `insertspanf` and **does** create DOCISPAN entries.

---

### The Actual APPEND Call Chain

**Step 1 — `doappend` [do1.c:25-32]:**
```c
bool doappend(typetask *taskptr, typeisa *docptr, typetextset textset)
{
  bool appendpm(),insertspanf(); /*zzz dies this put in granf?*/

    return (appendpm (taskptr, docptr, textset)/*&&
       appendpm includes insertspanf!   insertspanf(taskptr,spanf,docptr,textset,DOCISPAN)*/
    );
}
```

The `insertspanf` call is commented out. The source comment says **"appendpm includes insertspanf!"** — this is the author's explanation for why the explicit call is absent. The `/*zzz dies this put in granf?*/` is a historical uncertainty note from Gregory at the time he was writing/modifying `appendpm`. The question is whether the claim is true.

**Step 2 — `appendpm` [orglinks.c:17-27]:**
```c
bool appendpm(typetask *taskptr, typeisa *docisaptr, typetextset textset)
{
  typeorgl orglptr;
  tumbler vsa;
  bool findorgl(), doinsert();

    if (!findorgl(taskptr, granf, docisaptr, &orglptr, WRITEBERT))
        return(FALSE);
    findvsatoappend((typecorecrum*)orglptr, &vsa);
    return (doinsert(taskptr, docisaptr, &vsa, textset));
}
```

`appendpm` calls `doinsert`. Not a special stripped-down insert — the **same** `doinsert` used by the FEBE INSERT command.

**Step 3 — `doinsert` [do1.c:87-123]:**
```c
bool doinsert(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typetextset textset)
{
    makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
    ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
        && docopy (taskptr, docisaptr, vsaptr, ispanset)
    );
    return(ret);
}
```

`doinsert` calls `inserttextingranf` (allocates ispan addresses in granf, returns `ispanset` with `ISPANID` items), then calls `docopy`.

**Step 4 — `docopy` [do1.c:45-65]:**
```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && acceptablevsa (vsaptr, docorgl)
    && asserttreeisok(docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
    &&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)   // ← line 62
    && asserttreeisok(docorgl)
    );
}
```

`insertspanf` IS called, with `DOCISPAN` span type and `docisaptr` as the document identity.

**Step 5 — `insertspanf` [spanf1.c:15-54], ISPANID branch:**
```c
if (((typeitemheader *)sporglset)->itemid == ISPANID) {
    movetumbler (&((typeispan *)sporglset)->stream, &lstream);   // ispan stream address
    movetumbler (&((typeispan *)sporglset)->width, &lwidth);     // ispan width
    movetumbler (isaptr, &linfo.homedoc);                        // line 29: homedoc = docisaptr
}
...
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // line 51
```

`linfo.homedoc` is set to `*docisaptr` — the document to which APPEND'd text was written — and inserted into the spanfilade.

---

### Why the Finding Was Wrong

Finding 0036 / [EC-APPEND-NO-DOCISPAN] read `doappend` [do1.c:25-32] and concluded: *"`insertspanf` is commented out, therefore APPEND creates no DOCISPAN entries."*

This missed the full chain. The commented-out explicit call:
```c
insertspanf(taskptr, spanf, docptr, textset, DOCISPAN)
```
would have passed raw `textset` (TEXTID items) to `insertspanf`, hitting the TEXTID branch where `lstream = *isaptr` (the document ISA — semantically wrong as a content address). The author removed it precisely because the correct path through `appendpm` → `doinsert` → `docopy` reaches `insertspanf` with proper ISPANID items. The comment "appendpm includes insertspanf!" is **accurate**.

---

### Answer to the Question

**APPEND content is not origin-anonymous.**

The origin document is recorded in the spanfilade with `homedoc = docisaptr` [spanf1.c:29] for every ispan produced by the append. The recovery mechanism is `finddocscontainingsp` [spanf1.c:151-188], which traverses the spanfilade via `retrieverestricted` using the DOCISPAN subspace, reading `c->totaloffset.dsas[ORGLRANGE]` to recover the document tumbler [spanf1.c:173-174]. This is the same mechanism that serves `find_documents_containing` for INSERT'd content.

**The complete call chain for APPEND:**

```
doappend [do1.c:25]
  → appendpm [orglinks.c:17]
    → doinsert [do1.c:87]
      → inserttextingranf  (allocates ispans in granf)
      → docopy [do1.c:45]
        → insertspanf [spanf1.c:15] with DOCISPAN
          → linfo.homedoc = *docisaptr  [spanf1.c:29]
          → insertnd [spanf1.c:51]  (writes into spanfilade)
```

**[EC-APPEND-NO-DOCISPAN] should be withdrawn or corrected.** It is not an edge case — it is a misreading. APPEND and INSERT are indistinguishable in their DOCISPAN postcondition; they diverge only in the V-address chosen (APPEND uses `findvsatoappend`; INSERT uses the caller-supplied `vsaptr`).
