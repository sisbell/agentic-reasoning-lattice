## Question 18 [gregory]

> The spanfilade DOCISPAN entries persist after DELETE with no cleanup — if document D1 once contained I-span X and D1 is later queried via `find_documents_containing(X)`, does the system return D1 even though D1's current POOM no longer maps to X, or is there a POOM cross-check?

## KB Synthesis

Yes — `find_documents_containing(X)` returns D1 even after DELETE has removed X from D1's POOM. There is no POOM cross-check.

**The spanfilade is write-only.** [INV-SPANF-WRITE-ONLY] establishes that no delete function exists anywhere in `spanf1.c` or `spanf2.c`. DELETE calls only `deletevspanpm` → `deletend` on the document's POOM (granf layer) with no spanf call. [ST-DELETE / Finding 0057] confirms this explicitly: `dodeletevspan` has no call to any spanf removal function.

**The result is permanent divergence.** [INT-DELETE-SPANF-DIVERGENCE] formalizes exactly this situation: after DELETE, the POOM and spanfilade diverge. The spanfilade continues to assert D1 contains X; the POOM no longer maps any V-address to X. This divergence is permanent — no reconciliation mechanism exists.

**`find_documents_containing` queries the spanfilade, not the POOM.** [SS-DOCISPAN / Finding 0036] establishes that DOCISPAN is the type-4 spanfilade index that `FINDDOCSCONTAINING` queries. It is populated on INSERT/COPY via `insertspanf(..., DOCISPAN)` and never pruned.

**Observational confirmation.** [INV-IADDRESS-PERMANENT / Finding 0023] documents this directly with golden test evidence: after deleting content from D, `find_documents("Findable")` still returns D — the I-address association persists in the spanf index despite V-stream removal. The spanf index for a document only grows over its lifetime.

**The invariant is asymmetric.** [EC-STALE-SPANF-REFERENCE] states the formal relationship: `actual_docs(i) ⊆ find_documents(i)` — the spanfilade returns a **superset** of documents currently containing X. Consumers who need current-state accuracy must post-filter via I-to-V conversion. [INV-ITOV-FILTERING] provides that post-filter: `linksporglset2specset` silently drops I-addresses with no POOM mapping, so converting the stale spanfilade hit back to a V-address yields empty — distinguishing live from ghost references.

In summary: `find_documents_containing(X)` returns D1 (stale reference). No POOM cross-check occurs at query time. The caller must apply I→V conversion to determine whether D1 actually has a current V-position for X.

---

## Code Exploration

I now have all the evidence. Here is the complete answer.

---

## Answer: No POOM Cross-Check — Stale DOCISPAN Entries Cause False Positives

### The Short Answer

**Yes, `find_documents_containing(X)` returns D1 even after D1's content was deleted.** There is no POOM cross-check. The spanfilade is append-only with respect to DOCISPAN entries; DELETE never writes to it.

---

### Traced Call Chain

#### 1. How DOCISPAN entries enter the spanfilade (INSERT)

`doinsert` [do1.c:117-123] → `docopy` [do1.c:45-65]:

```c
// do1.c:62
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

`insertspanf` [spanf1.c:15-54]:

```c
// spanf1.c:22
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

This writes a 2D spanfilade crum keyed on:
- **ORGLRANGE** = `DOCISPAN.docisa` (the constant `4` [xanadu.h:39] prefixed to D1's ISA)
- **SPANRANGE** = the I-span X being inserted

Then at [spanf1.c:51]: `insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE)` actually places the crum into the spanfilade tree.

#### 2. What DELETE does (nothing to the spanfilade)

`dodeletevspan` [do1.c:158-167]:

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

`deletevspanpm` [orglinks.c:145-152]:

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

`deletend` operates only on `docorgl` — the document's own POOM (permutation matrix enfilade) in the V dimension. **`spanf` is never mentioned.** A codebase-wide search for `deletend.*spanf` or `spanf.*deletend` returns zero matches.

There is no counterpart to `insertspanf` on the delete path. No tombstone, no inverse write, nothing.

#### 3. How `find_documents_containing` queries (spanfilade only, no POOM check)

`finddocscontaining` in `fns.c` [line 24-28] → `dofinddocscontaining` [do1.c:15-23] → `finddocscontainingsp` [spanf1.c:151-188]:

```c
// spanf1.c:167-171
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
```

This calls `retrieverestricted` [retrie.c:56-85] which calls `retrieveinarea` → `findcbcinarea2d` [retrie.c:229-268]. The 2D search finds every spanfilade crum whose:
- ORGLRANGE intersects `docspace` (i.e., has DOCISPAN prefix = 4)
- SPANRANGE overlaps the query I-span

For each match [spanf1.c:172-179]:

```c
for (c = context; c; c = c->nextcontext) {
    movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
    beheadtumbler (&docid, &document.address);  // strip DOCISPAN prefix
    if (isinlinklist(*headptr, &document.address))
        continue;
    document.itemid = LINKID;
    document.next = NULL;
    addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
}
```

The `beheadtumbler` [tumble.c:673] strips the DOCISPAN digit to recover D1's ISA, then adds D1 to the result set.

**There is no further step.** The function returns after `contextfree(context)`. It never:
- Opens D1's POOM via `findorgl`
- Calls `permute` or `vspanset2ispanset` to check whether I-span X still maps to a V-position in D1
- Discards the result if D1's POOM no longer covers X

#### 4. `crumqualifies2d` does not help

The filter inside `findcbcinarea2d` is `crumqualifies2d` [retrie.c:270-305], which matches based on the ORGLRANGE and SPANRANGE tumbler intervals stored in the crum itself. It compares crum origin/width against the query bounds. Since the stale crum still has the same SPANRANGE (I-span X) and ORGLRANGE (DOCISPAN.D1-ISA), it passes the filter. The POOM's current state is not consulted during this filter.

---

### Conclusion

The spanfilade DOCISPAN index is **write-once, never retracted**. When D1 inserts content at I-span X, a crum is written to the spanfilade at [ORGLRANGE=DOCISPAN.D1, SPANRANGE=X]. When D1's content is later deleted:
- The POOM removes the V→I mapping (`deletend` on `docorgl`)
- The spanfilade crum at [DOCISPAN.D1, X] is **left in place**

`find_documents_containing(X)` queries only the spanfilade, finds the stale crum, strips the DOCISPAN prefix, and returns D1 — **a false positive**. The system has no POOM cross-check. D1 will be returned as containing X indefinitely, regardless of how many times its content is deleted or replaced.
