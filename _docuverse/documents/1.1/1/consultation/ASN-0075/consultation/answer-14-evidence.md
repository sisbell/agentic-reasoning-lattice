## Question 14 [evidence]

> Does the spanfilade's monotonic-growth property mean a "deleted content" query could intersect spanfilade DOCISPAN entries against current POOM I-spans to identify ranges no longer present?

## KB Synthesis

Yes, this is theoretically sound, and follows directly from the architecture — but with significant implementation constraints.

**The math works**

From [INV-SPANF-WRITE-ONLY] and [INT-DELETE-SPANF-DIVERGENCE]: after `DELETE(D, vspan)`, the spanfilade retains DOCISPAN entries for those I-addresses while the POOM no longer maps them. The invariant from [EC-STALE-SPANF-REFERENCE] formalizes this as:

```
current_poom_iaddrs(D) ⊆ spanfilade_docispan_iaddrs(D)
```

The difference `spanfilade_docispan_iaddrs(D) − current_poom_iaddrs(D)` is exactly the set of I-addresses ever placed into D but subsequently deleted. Since the granfilade is append-only [INV-IADDR-IMMUTABILITY], the content bytes at those I-addresses still exist and are retrievable.

**What you'd recover**

[SS-DOCISPAN] confirms DOCISPAN entries track at I-span granularity (one entry per contiguous I-address range per INSERT/COPY operation), and [INV-NO-IADDR-REUSE] guarantees no I-address is ever reused, so the recovered spans unambiguously identify original content.

**Implementation blockers**

Three problems prevent using this directly today:

1. **No reverse-lookup API**: `finddocscontaining` goes I-address → documents. There is no "enumerate all DOCISPAN entries for document D" operation. The orgl-range filter that would provide this is permanently disabled via the `TRUE||!homeset` guard [EC-FIND-LINKS-GLOBAL].

2. **COPY entries contaminate the result**: DOCISPAN is written for both INSERT and COPY [ST-COPY]. The difference set includes I-addresses that were transcluded-then-deleted, not just originally-created-then-deleted — you can't distinguish provenance from DOCISPAN alone without cross-referencing [INV-IADDR-PROVENANCE].

3. **POOM state access**: Enumerating `current_poom_iaddrs(D)` requires open-document traversal [SS-DOCUMENT-LIFECYCLE], and the POOM's multimap structure [SS-POOM-MULTIMAP] means the same I-address can appear at multiple V-positions.

**In sum**: The monotonic spanfilade + permanent granfilade design makes deleted-content recovery *architecturally possible* — the information is preserved. But the current query interface would need the orgl-range filter repaired and a document-scoped DOCISPAN enumeration operation to make it practical.

---

## Code Exploration

I now have all the evidence needed. Here is my full analysis.

---

## Deleted-Content Detection via Spanfilade↔POOM Intersection

**Short answer: Yes, the query is architecturally sound and supported by the code.** The spanfilade's monotonic-growth property is real and provable from the source. The proposed intersection algorithm falls directly out of the design.

---

### 1. The Monotonic-Growth Property Is Proven, Not Assumed

Every content insertion calls `insertspanf` exactly once for `DOCISPAN`:

```c
/* do1.c:62 */
&& insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The same pattern holds for `docopyinternal` at `do1.c:79`. For link endpoints, `insertendsetsinspanf` at `do2.c:116-128` calls `insertspanf` with `LINKFROMSPAN` (1), `LINKTOSPAN` (2), and `LINKTHREESPAN` (3).

The delete path is `dodeletevspan` at `do1.c:158-167`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` at `orglinks.c:145-151` calls only `deletend` on the POOM:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

A grep for `deletespanf` or any `deletend(.*spanf` returns no matches anywhere in the codebase. **The spanfilade is append-only by construction, not convention.** There is simply no code path that removes from it.

---

### 2. What a DOCISPAN Entry Encodes

`insertspanf` at `spanf1.c:15-54` builds a 2D crum for the spanfilade with two independent dimensions:

```c
/* spanf1.c:22-23 */
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
```

```c
/* spanf1.c:49-51 */
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

`prefixtumbler` at `tumble.c:641-651` prepends the `spantype` integer as the leading mantissa digit of the tumbler, then shifts the document ISA to the sub-address:

```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr)
{
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;       /* spantype = DOCISPAN (4) */
    movetumbler (aptr, &temp2);
    if (!iszerotumbler (&temp2))
        temp2.exp -= 1;             /* shift ISA to sub-address */
    tumbleradd (&temp1, &temp2, cptr);
}
```

So a DOCISPAN entry occupies:
- **ORGLRANGE**: `4.docISA` (spantype prefix 4 = `DOCISPAN`, defined at `xanadu.h:39`)
- **SPANRANGE**: the I-span `(stream, width)`
- **`linfo.homedoc`**: the doc ISA again (for `2dinfo`)

The constants are `xanadu.h:36-39`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

---

### 3. Existing Machinery Already Uses This Intersection

`finddocscontainingsp` at `spanf1.c:151-188` shows the span→document direction of the same query:

```c
/* spanf1.c:167-174 */
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
```

The `docspace` range covers all ORGLRANGE addresses that carry prefix digit 4 (DOCISPAN). `retrieverestricted` performs the 2D intersection: restrict ORGLRANGE to DOCISPAN-prefixed addresses, find crums whose SPANRANGE overlaps `ispanset`. The result `c->totaloffset.dsas[ORGLRANGE]` is the `4.docISA` compound, and `beheadtumbler` strips the prefix to recover the raw document ISA.

This answers: "given I-spans, which documents ever held them?" The deleted-content query inverts the direction: given a document ISA, what I-spans does the spanfilade record vs. what does its POOM currently hold?

---

### 4. The Proposed Algorithm, Grounded in Code

**Step A — Historical I-spans from the spanfilade.**

Construct an ORGLRANGE restriction for a specific document: `prefixtumbler(docISA, DOCISPAN, orglspan)`. Then call `retrievesporglsetinrange` at `spanf1.c:237-267`, which iterates over the document's sporglset entries and calls `retrieverestricted((typecuc*)spanf, sporglptr, SPANRANGE, whichspace, ORGLRANGE, NULL)`. The returned contexts carry `SPANRANGE` coordinates — the historical I-spans.

**Step B — Current I-spans from the POOM.**

`vspanset2ispanset` at `orglinks.c:397-402` → `permute(taskptr, orgl, vspanptr, V, ispansetptr, I)` → `span2spanset` → `retrieverestricted((typecuc*)orgl, restrictionspanptr, V, NULL, I, NULL)`.

This traverses the POOM for the document's full V-range and returns all currently active I-span mappings.

**Step C — Set difference.**

I-spans present in Step A but absent in Step B are content that was once inserted into the document (permanently recorded in the spanfilade via `insertspanf`/`DOCISPAN`) but subsequently removed from the POOM (via `deletend` called through `deletevspanpm`). These are the deleted ranges.

---

### 5. Important Constraints

**Transclusion does not pollute this query** — `docopy` at `do1.c:45-65` records the *target* document's ISA in the DOCISPAN entry (the `docisaptr` parameter to `insertspanf`), not the source. So if doc A copies content from doc B, doc A's DOCISPAN entries record the I-spans in doc A's ORGLRANGE address space. Deletion from doc A removes the POOM entries for doc A only. The set difference correctly identifies what was deleted from doc A, regardless of whether the same I-spans still live in doc B.

**The POOM is the sole mutable state for content presence** — `rearrangend` (called through `dorearrange`) reshuffles V-positions but does not change which I-spans exist in the POOM. It does not affect the spanfilade at all. Rearranged content is not "deleted content" by this definition.

**No direct high-level API exists for the inverse direction** — `finddocscontainingsp` queries "given I-spans → docs." The inverse "given doc → historical I-spans" uses the same `retrieverestricted` engine but requires constructing the ORGLRANGE restriction for a specific document ISA. The building blocks (`retrievesporglsetinrange`, `retrieverestricted`) are present; the composite function is not.

**Granfilade content is permanent regardless** — the byte content stored in the granfilade via `inserttextingranf` never disappears. "Deleted" here means the document's POOM no longer maps any V-address to those I-spans. The content remains retrievable if another document still references those I-spans, or via direct I-address lookup.

---

### 6. Conclusion

The spanfilade's monotonic growth is structurally guaranteed: `insertspanf` is the only write path (`do1.c:62`, `do1.c:79`, `do2.c:119-124`); `dodeletevspan` at `do1.c:158-167` modifies only `docorgl` (the POOM), leaving the spanfilade untouched. The DOCISPAN entries at ORGLRANGE prefix 4 permanently index every I-span ever inserted into a document.

The proposed intersection query is valid: `{DOCISPAN SPANRANGE entries for docX in spanfilade}` − `{I-spans from docX's current POOM via vspanset2ispanset}` = content I-spans that were once part of the document but are no longer present in any V-position. This is a precise characterization of "deleted content ranges" in I-space, and it emerges directly from the append-only nature of the spanfilade and the mutable-only nature of the POOM.
