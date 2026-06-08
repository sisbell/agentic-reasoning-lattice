## Question 16 [evidence]

> After DELETE, do the corresponding DOCISPAN entries remain in the spanfilade (since no `deletespanf` exists), causing `find_documents_containing` to still return this document for the deleted I-addresses?

## KB Synthesis

Yes. DOCISPAN entries persist unconditionally after DELETE.

**The mechanism:**

`dodeletevspan` calls only `deletevspanpm` (which runs `deletend` on the document's POOM) and `logbertmodified`. There is no call to any spanfilade function. No `deletespanf` exists anywhere in `spanf1.c` or `spanf2.c`. [ST-DELETE, Finding 0057]

**The invariant:**

The spanfilade is write-only: `∀ t₁ < t₂ : spanf_entries(t₁) ⊆ spanf_entries(t₂)`. [INV-SPANF-WRITE-ONLY]

**The observable consequence:**

After DELETE, POOM and spanfilade diverge. The document's POOM no longer maps the deleted I-addresses to V-positions, but the spanfilade still claims the document contains them. `FINDDOCSCONTAINING` returns a **superset** of documents currently holding the queried I-addresses: `actual_docs(i) ⊆ find_documents(i)`, not equality. [INT-DELETE-SPANF-DIVERGENCE, EC-STALE-SPANF-REFERENCE]

Golden evidence confirms: after deleting transcluded content from a document, `find_documents` still reports that document, but I-to-V conversion for those I-addresses within it returns empty. [INV-IADDRESS-PERMANENT]

**Implication for callers:**

Consumers of `FINDDOCSCONTAINING` must post-filter via I-to-V conversion (the `span2spanset`/`retrieverestricted` path silently drops unresolvable I-addresses) to distinguish live from stale results. [INV-ITOV-FILTERING]

---

## Code Exploration

All citations verified. Here is my complete answer.

---

## After DELETE, DOCISPAN Entries Persist in the Spanfilade

**Yes — the DOCISPAN entries remain, and `finddocscontainingsp` will return the document for deleted I-addresses.** Here is the complete evidence chain from source code.

---

### 1. What `dodeletevspan` actually does

`backend/do1.c:158–167`:
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

Two operations only: `findorgl` to locate the document in the granf, and `deletevspanpm`. No reference to `spanf` at all.

---

### 2. What `deletevspanpm` does

`backend/orglinks.c:145–152`:
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

`deletend` operates on `docorgl` — the document's node in the **granf** (the enfilade/permutation matrix). The argument is `(typecuc*)docorgl`, not `(typecuc*)spanf`. The spanfilade is never touched.

---

### 3. No `deletespanf` exists anywhere

A grep for `deletespanf` across all backend C files returns **zero matches**. Compare the asymmetry:

- **INSERT path**: `docopy` at `backend/do1.c:62` calls `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — DOCISPAN entries are written to the spanfilade.
- **DELETE path**: `deletevspanpm` at `backend/orglinks.c:149` calls only `deletend((typecuc*)docorgl, ...)` — no corresponding removal from the spanfilade.

The `insertspanf` function itself (`backend/spanf1.c:15–54`) inserts nodes into the spanfilade via `insertnd` at line 51. There is no mirror function for removal.

---

### 4. How `finddocscontainingsp` queries the spanfilade

`backend/spanf1.c:151–188`, the function called by `dofinddocscontaining` (`backend/do1.c:15–23`):

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    ...
    tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);  // line 168
    tumblerincrement (&docspace.width, 0, 1, &docspace.width);
    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,   // line 171
                                      ispanset, SPANRANGE, (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);
            ...
            addresssetptr = (typelinkset *) onitemlist(...);
        }
    }
    return (TRUE);
}
```

At `spanf1.c:168`, it constructs a range covering the `DOCISPAN` subspace. At `spanf1.c:171`, it calls `retrieverestricted` on `spanf` (the spanfilade) — looking for any DOCISPAN entry whose SPAN dimension overlaps the given I-address set. The document ID is then extracted from the ORGL dimension of whatever nodes are found.

Since those DOCISPAN nodes were never removed, they will still be found.

---

### Conclusion

The DELETE operation is **incomplete with respect to the secondary index**. The call chain is:

```
DELETE (fns.c)
  → dodeletevspan (do1.c:158)
    → deletevspanpm (orglinks.c:145)
      → deletend on docorgl/granf (orglinks.c:149)
         [spanfilade untouched — no deletespanf called or defined]
```

While the granf correctly removes the V-span mapping (so the deleted content is no longer addressable by V-address and `retrieve` will not return it), the corresponding DOCISPAN nodes in the spanfilade remain intact. Any subsequent `find_documents_containing` call that resolves to those same I-addresses will still find the document, because `finddocscontainingsp` (`spanf1.c:171`) reads directly from `spanf` with no validation against the current granf state.

This is a classic orphaned secondary-index problem: insertion updates both structures (`do1.c:60–62`: `insertpm` + `insertspanf`), but deletion updates only one.
