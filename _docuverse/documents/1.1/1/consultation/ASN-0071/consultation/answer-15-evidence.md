## Question 15 [evidence]

> Because the spanfilade has no delete function, does FINDDOCSCONTAINING return documents that previously contained the queried I-spans but have since had them removed from their POOM via DELETEVSPAN — and is there any post-filter against the live POOM?

## KB Synthesis

## FINDDOCSCONTAINING and Stale Spanfilade References

**Yes, it returns stale documents. No, there is no built-in post-filter.**

### Why stale documents appear

DELETEVSPAN modifies only the POOM (granf layer) — it calls `deletevspanpm` → `deletend` on the document's orgl, then `logbertmodified`. There is no call to any spanf function. [INV-SPANF-WRITE-ONLY, INT-DELETE-SPANF-DIVERGENCE]

The spanfilade has no delete operation at all — only `insertspanf`, query functions, and no `deletespanf` anywhere in `spanf1.c` or `spanf2.c`. [INV-SPANF-WRITE-ONLY]

Therefore, after `DELETEVSPAN`, the POOM no longer maps the deleted I-addresses to V-positions, but the spanfilade's DOCISPAN entries still assert that document contains those I-addresses. FINDDOCSCONTAINING queries the spanfilade and returns the now-stale document. The formal relationship is:

> `actual_docs(i) ⊆ find_documents(i)` — actual containment implies discoverability, but not vice versa.

This is confirmed empirically: `find_documents_after_delete` golden test shows Dest still returned after "Findable" is deleted from its V-stream. [INV-IADDRESS-PERMANENT, EC-STALE-SPANF-REFERENCE]

### Why there is no post-filter in FINDDOCSCONTAINING

The silent I-to-V filtering described in [INV-ITOV-FILTERING] exists in the FOLLOWLINK and RETRIEVEENDSETS paths: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()`, which silently drops I-addresses with no POOM mapping. That filter operates because those operations return **V-address spans** and must resolve I→V.

FINDDOCSCONTAINING (`finddocscontainingsp`) returns **document ISAs**, not V-spans. No I→V conversion occurs in this path, so the `retrieverestricted()` null-drop mechanism never runs.

The KB is explicit: callers must apply their own post-filter via I-to-V conversion to distinguish live from stale results. [EC-STALE-SPANF-REFERENCE]

### Summary

| Layer | After DELETEVSPAN |
|-------|------------------|
| POOM (granf) | I-address mapping removed |
| Spanfilade DOCISPAN | Entry persists (write-only) |
| FINDDOCSCONTAINING result | Stale document included |
| Built-in post-filter | None — caller responsibility |

---

## Code Exploration

I now have everything needed for a complete, cited answer.

---

## FINDDOCSCONTAINING and the Spanfilade: Full Analysis

### The Call Chain

**`fns.c:20-32`** — top-level FEBE handler:
```c
void finddocscontaining(typetask *taskptr)
{
    if (getfinddocscontaining(taskptr, &specset)
     && dofinddocscontaining(taskptr, specset, &addressset))
        putfinddocscontaining(taskptr, (typeitemset)addressset);
    else
        putrequestfailed(taskptr);
}
```

**`do1.c:15-23`** — converts vspecs to I-spans, then delegates:
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
    typeispanset ispanset;
    return (
        specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)
     && finddocscontainingsp(taskptr, ispanset, addresssetptr));
}
```

**`spanf1.c:151-188`** — the core implementation:
```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
    ...
    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted((typecuc*)spanf, &docspace, ORGLRANGE,
                                     ispanset, SPANRANGE, (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {
            movetumbler(&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler(&docid, &document.address);
            if (isinlinklist(*headptr, &document.address)) continue;
            ...
            addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, ...);
        }
        contextfree(context);
    }
    return(TRUE);
}
```

The query is **entirely against `spanf`** (the spanfilade). The `ORGLRANGE` dimension holds document addresses; `SPANRANGE` holds I-span coordinates. `docspace` is constructed at `spanf1.c:167-169` to restrict results to the `DOCISPAN` subspace (prefix `0.DOCISPAN`), filtering out link entries. No other data structure is consulted.

---

### The Spanfilade Has No Delete Function

A grep for `deletespanf`, `removespanf`, `uninsertspanf` across the entire `backend/` directory returns nothing. The only spanfilade mutation function is `insertspanf()` at `spanf1.c:15-54`, which adds crums. There is no inverse.

`edit.c:30` has a comment `/* use with SPAN and POOM */` above `deletend()`, showing that the generic N-dimensional delete *could* operate on a spanfilade node — but nothing in the codebase ever passes `(typecuc*)spanf` to `deletend`.

---

### DELETEVSPAN Never Touches the Spanfilade

**`fns.c:333-347`** → **`do1.c:158-167`**:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
        findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
     && deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
    /*&& TRUE*/ /* ht stuff */ );
}
```

`findorgl` is called with **`granf`** (the granfilade/POOM), not `spanf`. Then:

**`orglinks.c:145-152`**:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return(FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

`deletend` receives `(typecuc*)docorgl` — the POOM node for this document. The spanfilade is never touched at any point in this chain.

The comment `/* ht stuff */` at `do1.c:166` is a tombstone: hypertext maintenance (which would have been responsible for spanfilade bookkeeping) was planned but never implemented.

---

### No Post-filter Against the Live POOM

After `finddocscontainingsp()` returns its address set, `dofinddocscontaining()` passes it directly to the caller (`do1.c:22`). `finddocscontaining()` passes it directly to `putfinddocscontaining()` (`fns.c:29`). There is no POOM consultation, no liveness check, no intersection with the live document content.

---

### Answer

**Yes, FINDDOCSCONTAINING is a stale-index query.** It reads only the spanfilade, which is an append-only structure: entries are written by `insertspanf()` during `docopy` and `createlink`, and are *never removed*. Because `dodeletevspan` calls `deletend` on the POOM (`docorgl`) and ignores the spanfilade entirely, any document from which I-spans were later removed via DELETEVSPAN will still appear in the spanfilade index and will still be returned by FINDDOCSCONTAINING. There is no post-filter against the live POOM anywhere in the `finddocscontaining → dofinddocscontaining → finddocscontainingsp` path.

The missing inverse of `insertspanf` is the gap. The `/* ht stuff */` comment at `do1.c:166` marks where that cleanup was intended to go.
