## Question 18 [gregory]

> When DELETE removes transcluded content from doc2 (content originally from doc1), the DOCISPAN entry for doc2 remains in the spanfilade — does `find_documents_containing` then return doc2 as still containing that content, and is there any mechanism in the retrieval path that verifies the DOCISPAN against doc2's current POOM before returning results?

## KB Synthesis

## find_documents_containing After DELETE of Transcluded Content

**Short answer:** Yes, `find_documents_containing` returns doc2 as still containing the content. No, there is no POOM-verification step in the retrieval path — `find_documents_containing` queries the spanfilade directly, and the spanfilade is never updated by DELETE.

---

### Why the DOCISPAN entry persists

DELETE operates exclusively on the POOM (granf layer) via `deletevspanpm` → `deletend`. The spanfilade is never touched:

> `dodeletevspan`: calls `findorgl` + `deletevspanpm`, no spanf call. Contrast with `docopy`: calls both `insertpm` AND `insertspanf`. [ST-DELETE, Finding 0057]

The spanfilade is structurally append-only — no deletion function exists anywhere in `spanf1.c` or `spanf2.c`:

> "No `deletespanf`, `removespanf`, or any removal mechanism exists." [INV-SPANF-WRITE-ONLY, Finding 0057]

So when doc2 originally received the transcluded content via COPY/VCOPY, `insertspanf(..., DOCISPAN)` was called and recorded doc2 as a container of those I-addresses. That entry is permanent.

---

### What find_documents_containing actually returns

The result is a **superset** of documents currently containing the I-addresses:

> `actual_docs(i) ⊆ find_documents(i)` where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The reverse inclusion does NOT hold. [EC-STALE-SPANF-REFERENCE, Finding 0057]

Doc2 appears in the result because the DOCISPAN entry asserts it, even though doc2's POOM no longer maps those I-addresses to any V-position. This creates a permanent divergence between the two layers:

> "Before DELETE, both layers agree... After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses. This divergence is permanent." [INT-DELETE-SPANF-DIVERGENCE, Finding 0057]

This is also explicitly confirmed for the doc1-persists case in [INV-IADDRESS-PERMANENT] (Finding 0023) and [FC-CONTENT-SPANF-ISOLATION] (Finding 0018): even after deletion from doc2's V-stream, `find_documents` returns doc2.

---

### No POOM verification in find_documents_containing

`finddocscontainingsp` queries the spanfilade and returns whatever documents are registered there. There is no cross-check against those documents' current POOM state at query time.

The only verification that exists is downstream, in the **I-to-V conversion path**:

> "Both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V conversion path that silently filters unreferenced I-addresses. At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), the I-address is silently dropped." [INV-ITOV-FILTERING, Finding 0048]

This filtering happens when a caller subsequently attempts to resolve the I-addresses to V-positions within doc2 (e.g., via FOLLOWLINK or RETRIEVEENDSETS). It does not happen inside `find_documents_containing` itself.

---

### Summary

| Operation | Queries | Filters stale DOCISPAN? |
|-----------|---------|------------------------|
| `find_documents_containing` | Spanfilade only | **No** — returns superset |
| I-to-V conversion (FOLLOWLINK, RETRIEVEENDSETS) | Doc POOM | **Yes** — silently drops unresolvable I-addresses |

Consumers of `find_documents_containing` must post-filter via I-to-V conversion to distinguish live from stale results [EC-STALE-SPANF-REFERENCE]. The spanfilade is a historical journal of all content placements ever made, not a current-state index.

---

## Code Exploration

I now have everything needed. Here is the complete answer.

---

## Answer: Spanfilade Ghost Entries After DELETE

### The Short Answer

**Yes** — the DOCISPAN entry for doc2 persists in the spanfilade after a DELETE. **Yes** — `finddocscontainingsp` returns doc2 as still containing that content. **No** — there is no mechanism anywhere in the retrieval path that cross-checks the spanfilade against doc2's current POOM.

---

### 1. How the DOCISPAN Entry Gets Written (INSERT/COPY)

When content is transcluded into doc2 via `docopy` [`do1.c:45-65`], two independent writes happen:

```c
/* the meat of docopy: */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)   // → POOM
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // → spanfilade
```

`insertpm` [`orglinks.c:75-134`] writes a crum into doc2's POOM mapping V-space → I-space. `insertspanf` [`spanf1.c:15-54`] writes a separate crum into the global `spanf`, keyed on the content's I-span in SPANRANGE and doc2's ISA in ORGLRANGE, with type `DOCISPAN`. These are entirely independent data structures — the POOM lives inside doc2's granfilade entry; the spanfilade is a global index.

---

### 2. What DELETE Actually Touches

`dodeletevspan` [`do1.c:158-167`]:

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

`deletevspanpm` [`orglinks.c:145-152`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [`edit.c:31-76`] operates on `(typecuc*)docorgl` — **doc2's POOM only** — in dimension `V`. It calls `makecutsnd`, `newfindintersectionnd`, and a loop over children that calls `deletecutsectionnd` and `disown`/`subtreefree` on matching crums. These crums live in doc2's POOM.

**There is no `deletend` or any other call on `spanf` in this entire path.** The DELETE operation is POOM-only.

---

### 3. What `finddocscontainingsp` Actually Does

The call chain: `finddocscontaining` [`fns.c:20-32`] → `dofinddocscontaining` [`do1.c:15-23`] → `finddocscontainingsp` [`spanf1.c:151-188`].

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset,NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

Inside `finddocscontainingsp` [`spanf1.c:151-188`]:

```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
}
```

This queries the **global `spanf`** (not any document's POOM) with `retrieverestricted`, restricting:
- ORGLRANGE to the `DOCISPAN` bucket (spans that record "document X contains I-span Y")
- SPANRANGE to the requested `ispanset`

It extracts doc ISAs from `ORGLRANGE` and returns them. **It never opens, reads, or consults doc2's POOM.** The spanfilade is the sole oracle for this query.

---

### 4. Is There Any POOM Verification in the Retrieval Path?

`retrieverestricted` [`retrie.c:56-85`] is called with the last argument `(typeisa*)NULL` — no `docisaptr`. This means `infoptr` is set to `NULL`:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;
}
temp = retrieveinarea(fullcrumptr, ..., (typebottomcruminfo*)infoptr);
```

Inside `findcbcinarea2d` [`retrie.c:229-268`], the per-leaf filter `crumqualifies2d` is:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

Because `infoptr == NULL`, this guard is **never evaluated**. Even if it were, it would only filter by document identity (restricting to one specific doc's entries), not by whether the POOM actually contains those spans anymore. There is no POOM lookup, no V-space range check, no cross-referencing of the retrieved spanfilade crum against doc2's current content tree.

---

### 5. Conclusion

The spanfilade and the POOM are **write-paired on INSERT but not on DELETE**. At `docopy` time, both `insertpm` and `insertspanf` are called [`do1.c:60-62`]. At `dodeletevspan` time, only `deletevspanpm` → `deletend` on the POOM is called [`do1.c:163-166`]; the corresponding spanfilade crum is never removed.

After doc2 deletes transcluded content:
- doc2's **POOM** correctly reflects the removal — the V→I mapping for those spans is gone
- the **spanfilade** still holds the DOCISPAN crum claiming doc2 contains those I-spans
- `finddocscontainingsp` queries only the spanfilade and returns doc2 as a positive match
- `retrieverestricted` / `findcbcinarea2d` / `crumqualifies2d` perform **no POOM cross-check** at any level

The DOCISPAN crum in the spanfilade is a **permanent ghost entry**. The only way it would be cleaned up is if something explicitly deleted it from `spanf`, and no such call exists in the delete path.
