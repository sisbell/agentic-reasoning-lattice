## Question 19 [evidence]

> Does SHOWRELATIONOF2VERSIONS read only the two documents' POOMs, or does it consult the spanfilade — and therefore can stale DOCISPAN entries for deleted content ever cause a correspondence to be reported that no current POOM entry supports?

## KB Synthesis

**SHOWRELATIONOF2VERSIONS reads only the POOMs. Stale DOCISPAN entries cannot produce false correspondences.**

## What the operation reads

`correspond.c` computes correspondences by:
1. Converting each document's V-spans to I-spans via `vspanset2ispanset` → `permute` → `retrieverestricted` — this walks each document's **POOM** (the granfilade's V→I mapping tree)
2. Computing I-span set intersection
3. Mapping surviving I-spans back to V-addresses in each document, again through each POOM

[INT-SPORGL-VERSION-COMPARE] confirms this: "Both documents' content is converted to sporgls, then intersection is computed by I-address (`sporglorigin` field)." The conversion is `vspanset2sporglset` → `vspanset2ispanset` → POOM reads. [SS-COMPARE-VERSIONS] cites `correspond.c` and no spanf function.

The spanfilade is never consulted. [FC-CONTENT-SPANF-ISOLATION] establishes the general rule: content retrieval operations access only `granf`; link search operations access only `spanf`. Compare_versions is a content retrieval operation.

## Why stale DOCISPAN entries cannot affect it

The DOCISPAN sub-index is only queried by `finddocscontainingsp` / `FINDDOCSCONTAINING`. That operation has well-documented stale-superset behavior [EC-STALE-SPANF-REFERENCE]: after DELETE, the spanfilade retains the entry while the POOM loses the V→I mapping, causing FIND_DOCUMENTS to return a superset of actual current holders. But `correspond.c` never calls any spanf function, so this divergence is invisible to it.

DELETE removes V→I mappings from the POOM via `deletend` / `disown` + `subtreefree` [ST-DELETE, Finding 0064]. After that removal, `retrieverestricted` on the POOM finds nothing for those I-addresses, and they drop out of the `vspanset2ispanset` output. The intersection step in `correspond.c` therefore operates only on live, POOM-resident I-addresses.

## The definitive invariant

From [ST-DELETE] (Finding 0057): "DELETE modifies only the POOM (granf layer) — the spanfilade is completely untouched." Combined with [INV-SPANF-WRITE-ONLY]: the spanfilade grows monotonically; deleted content's DOCISPAN entries persist there forever. But since `correspond.c` never reads the spanfilade, those ghost entries have zero influence on correspondence results.

**Conclusion:** A false correspondence requires an I-address to appear in both documents' `vspanset2ispanset` outputs simultaneously. That function reads only POOM state. Deleted content has no POOM entry. Therefore no stale spanfilade record can manufacture a correspondence that no current POOM entry supports.

---

## Code Exploration

I have everything needed. Here is the complete answer:

---

## `SHOWRELATIONOF2VERSIONS` — Data Structures Read, and the Stale-DOCISPAN Question

### 1. `SHOWRELATIONOF2VERSIONS` reads only the two documents' POOMs. The spanfilade is never consulted.

**Entry point:** `fns.c:250` `showrelationof2versions` → `do1.c:428` `doshowrelationof2versions`.

```c
// do1.c:443-448
return
    specset2ispanset(taskptr, version1, &version1ispans, READBERT)
  &&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
  &&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
  &&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
;
```

The complete V→I conversion path for each document:

| Step | Call | File | Structure read |
|------|------|------|----------------|
| 1 | `specset2ispanset(taskptr, version, &ispans, READBERT)` | `do2.c:14` | – |
| 2 | `findorgl(taskptr, granf, &docisa, &docorgl, READBERT)` | `do2.c:35` | granfilade (to locate the POOM) |
| 3 | `fetchorglgr(...)` returns `orglptr` with `cenftype == POOM` | `granf2.c:62, 80` | granfilade bottom crum |
| 4 | `vspanset2ispanset(taskptr, docorgl, vspanset, ispansetptr)` | `do2.c:36` | – |
| 5 | `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` | `orglinks.c:401` | – |
| 6 | `span2spanset(taskptr, orgl, ...)` | `orglinks.c:415` | – |
| 7 | `retrieverestricted((typecuc*)orgl, vspan, V, NULL, I, NULL)` | `orglinks.c:435` | – |
| 8 | `retrieveinarea(fullcrumptr, ...)` → case POOM: `findcbcinarea2d(...)` | `retrie.c:94–98` | **POOM** |

The `orgl` pointer is a `typecuc *` with `cenftype == POOM` — confirmed by how it is created in `granf2.c:120`:

```c
// granf2.c:120
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
```

The dimension constants (from `wisp.h:19–20`) confirm the traversal direction:

```c
#define I  0    // ispan (global content) dimension of POOM
#define V  1    // virtual (document-local) dimension of POOM
```

`permute` is called with `restrictionindex=V, targindex=I` for the forward pass, and `restrictionindex=I, targindex=V` for the reverse pass in `restrictvspecsetovercommonispans` (`correspond.c:74`). Both passes traverse the POOM via `findcbcinarea2d`.

The global `spanf` pointer is never passed into any function in this call chain. The spanfilade is structurally irrelevant to `SHOWRELATIONOF2VERSIONS`.

---

### 2. Stale DOCISPAN entries cannot cause phantom correspondences in `SHOWRELATIONOF2VERSIONS`

**Why stale entries exist:** `DOCISPAN` entries are written when content is inserted:

```c
// do1.c:62 (docopy)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)

// do1.c:79 (doinsert, inside insertpm path)
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

`insertspanf` (`spanf1.c:15`) uses `ORGLRANGE=0` and `SPANRANGE=1` dimensions of the spanfilade (`spanf` pointer) to record that document `docisaptr` contains ispan `ispanset`.

**When content is deleted,** `dodeletevspan` (`do1.c:158`) calls:

```c
// orglinks.c:145-151
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` (`edit.c:31`) is a pure POOM tree operation. It removes the V→I mapping from the POOM. It has no knowledge of the spanfilade and does not call `insertspanf`, `deletend` on `spanf`, or any spanfilade function. **The DOCISPAN entry in `spanf` is never removed.**

**Why this doesn't matter for `SHOWRELATIONOF2VERSIONS`:**

The correspondence check is entirely POOM-based. After a deletion:

1. The POOM no longer contains a V→I entry for the deleted V-range. `findcbcinarea2d` traversing the POOM will find nothing at those V-coordinates.
2. Therefore the deleted content's ispans do not appear in `version1ispans` or `version2ispans`.
3. `intersectspansets` (`correspond.c:145`) is pure arithmetic on the ispan sets — it cannot produce a common ispan that neither POOM produced.
4. No phantom correspondence can reach the output.

The staleness of DOCISPAN entries is invisible to `SHOWRELATIONOF2VERSIONS` because the spanfilade is not in the query path.

---

### 3. Where stale DOCISPAN entries DO cause a real bug

The dangerous path is `FINDDOCSCONTAINING`, not `SHOWRELATIONOF2VERSIONS`.

`finddocscontainingsp` (`spanf1.c:151`) queries the spanfilade directly:

```c
// spanf1.c:168-171
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
```

This retrieves every document whose DOCISPAN entry covers the requested ispans. Because deletion never removes these spanfilade entries, a document that previously contained a given ispan but has since had that content deleted will still be returned by `FINDDOCSCONTAINING` — a false positive.

`dofinddocscontaining` (`do1.c:15`) first converts V-specs to ispans via the POOM (which is correct), then calls `finddocscontainingsp` on those ispans against the stale spanfilade. So the ispan set is accurate, but the document membership lookup against `spanf` may be wrong.

---

### Summary

| Question | Answer |
|----------|--------|
| Does `SHOWRELATIONOF2VERSIONS` read the spanfilade? | **No.** It reads only the two documents' POOMs via `vspanset2ispanset` → `permute` → `retrieverestricted((typecuc*)orgl, ...)` where `orgl` has `cenftype == POOM`. |
| Can stale DOCISPAN entries produce phantom correspondences? | **No** — because `SHOWRELATIONOF2VERSIONS` never reads the spanfilade. Deletions correctly update the POOM (`deletend` at `orglinks.c:149`), and the V→I conversion is POOM-only. |
| Is the stale-DOCISPAN problem real? | **Yes, but in a different operation.** `finddocscontainingsp` (`spanf1.c:151`) queries `spanf` with DOCISPAN type and will return documents that formerly contained an ispan but have since deleted it. This affects `FINDDOCSCONTAINING`, not `SHOWRELATIONOF2VERSIONS`. |
