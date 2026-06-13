## Question 15 [evidence]

> After DELETE removes a V-span from a document's POOM, the DOCISPAN entry persists in the write-only spanfilade — does FINDDOCSCONTAINING verify candidates against the current POOM (the way FOLLOWLINK filters during I→V conversion), or does it return ghost documents that no longer contain the material?

## KB Synthesis

## FINDDOCSCONTAINING returns ghost documents — no POOM verification occurs.

The two operations have fundamentally different architectures, and the KB is explicit about the asymmetry.

### FINDDOCSCONTAINING: spanfilade only, no POOM check

[INT-DELETE-SPANF-DIVERGENCE] (Finding 0057) states the core fact: DELETE calls only `deletevspanpm` → `deletend` on the document's POOM orgl, with no call to any spanf function. The DOCISPAN entry that was written at INSERT/COPY time persists permanently. After DELETE, both layers diverge — the POOM says the document no longer contains those I-addresses, but the spanfilade still asserts it does.

[INV-SPANF-WRITE-ONLY] (Findings 0057, 0067) confirms there is no `deletespanf` or any removal mechanism anywhere in `spanf1.c` or `spanf2.c`. Growth is monotonic; DOCISPAN entries survive indefinitely.

FINDDOCSCONTAINING queries the spanfilade index directly and returns whatever document ISAs are registered against the queried I-address range. It does not consult any document's POOM.

[EC-STALE-SPANF-REFERENCE] (Finding 0057) makes this observable behavior explicit:

> After DELETE removes transcluded content, FIND_DOCUMENTS still returns the document as containing those I-addresses. […] attempting to convert the I-addresses to V-addresses in that document yields empty — the POOM has no mapping.

The formal invariant: `actual_docs(i) ⊆ find_documents(i)` — a strict superset relationship. Ghost documents appear in the result set.

[INV-IADDRESS-PERMANENT] (Finding 0023) states this as a monotonicity invariant: once an I-address is associated with a document, `FINDDOCSCONTAINING` continues to report it for all future states regardless of deletions.

### FOLLOWLINK/RETRIEVEENDSETS: actively filter through POOM

The contrast is with I→V conversion operations. [INV-ITOV-FILTERING] (Finding 0048) describes a universal filtering invariant: `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()` searches the target document's POOM for each I-address. When `retrieverestricted()` returns NULL (no POOM mapping), the I-address is silently dropped from the result. This produces the "ghost link" edge case [EC-GHOST-LINK] — FOLLOWLINK succeeds but returns empty spans.

### Summary

| Operation | Consults spanfilade | Verifies against POOM | Returns ghost refs |
|---|---|---|---|
| FINDDOCSCONTAINING | Yes | **No** | **Yes** |
| FOLLOWLINK / RETRIEVEENDSETS | No | **Yes** (via `retrieverestricted`) | No (silently filters) |

FINDDOCSCONTAINING is a historical journal query, not a current-state query. Callers that need to know whether content is *currently* accessible in a returned document must post-filter via I→V conversion — which is exactly what [EC-STALE-SPANF-REFERENCE] recommends.

---

## Code Exploration

I now have everything I need. Here is the complete, code-traced answer.

---

## Answer

**`FINDDOCSCONTAINING` does not verify candidates against the current POOM. It returns ghost documents.**

---

### The Full Call Chain for `FINDDOCSCONTAINING`

```
fns.c:20          finddocscontaining()
do1.c:15          dofinddocscontaining()
do2.c:14          specset2ispanset()          ← V→I on the INPUT spec
spanf1.c:151      finddocscontainingsp()      ← spanfilade query only, no POOM check
```

#### Step 1 — V→I conversion of the input spec (`do1.c:15–23`)

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

`specset2ispanset` (`do2.c:14–46`) converts the caller's V-spec into I-spans by querying the *source* document's POOM. This is the only POOM interaction in the entire operation — and it is on the document the caller specified as search content, not on the candidate documents that will be returned.

#### Step 2 — The spanfilade query (`spanf1.c:151–188`)

This is the entire body of `finddocscontainingsp`:

```c
bool finddocscontainingsp(typetask *taskptr, typespanset ispanset, typelinkset *addresssetptr)
{
  tumbler docid;
  typecontext *context, *c;
  typelinkset *headptr;
  typelink document;
  typespan docspace;

    headptr = addresssetptr;
    *addresssetptr = NULL;
    clear (&docspace, sizeof(typespan));
    tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);   // line 168
    tumblerincrement (&docspace.width,  0, 1,        &docspace.width);    // line 169

    for (; ispanset; ispanset = ispanset->next) {
        context = retrieverestricted(                  // line 171
            (typecuc*)spanf,          // ← the SPANFILADE, not granf/POOM
            &docspace, ORGLRANGE,
            ispanset, SPANRANGE,
            (typeisa*)NULL);
        for (c = context; c; c = c->nextcontext) {
            movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
            beheadtumbler (&docid, &document.address);    // extract document ISA
            if (isinlinklist(*headptr, &document.address))
                continue;                                  // deduplicate
            document.itemid = LINKID;
            document.next = NULL;
            addresssetptr = (typelinkset *) onitemlist(taskptr, ...);
        }
        contextfree (context);
    }
    return (TRUE);                                        // line 187 — always succeeds
}
```

**The function queries `spanf` (the spanfilade) and returns document addresses directly. There is no call to `findorgl`, no call to `ispan2vspanset`, no call to `permute`, and no call to `retrieverestricted` on `granf`. After finding candidate documents from the spanfilade, there is zero verification against any document's current POOM.**

---

### Why the Spanfilade Contains Ghost Entries

The spanfilade is populated during `docopy` (`do1.c:62`):

```c
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

DELETE removes only from the POOM. `dodeletevspan` (`do1.c:158–167`) calls:

```c
findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
```

`deletevspanpm` (`orglinks.c:145–152`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // POOM only
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

**`deletend` is called only on `docorgl` — the document's POOM node inside `granf`. There is no corresponding call to remove the DOCISPAN entry from `spanf`.** Furthermore, no deletion function exists for the spanfilade at all — `spanf1.c` and `spanf2.c` expose `insertspanf`, `finddocscontainingsp`, `findlinksfromtothreesp`, and `retrieveendsetsfromspanf`, but no `deletespanf` or equivalent.

---

### How FOLLOWLINK Differs During I→V Conversion

FOLLOWLINK (`do1.c:223–232`) takes the opposite path:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

`linksporglset2specset` (`sporgl.c:97–123`) calls `linksporglset2vspec` → `sporglset2vspanset` (`sporgl.c:141–176`):

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc,
                       typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    (void) findorgl (taskptr, granf, homedoc, &orgl, type);  // line 152 — open the POOM
    ispan.itemid = ISPANID;
    ...
    vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // line 157
    ...
}
```

`ispan2vspanset` (`orglinks.c:389–393`) calls `permute` → `span2spanset` → `retrieverestricted` on the POOM. If the V-span was deleted, the POOM has no mapping for those I-spans. `span2spanset` (`orglinks.c:425–454`) returns without adding anything when `context` is NULL:

```c
    if(!context){
        return(targspansetptr);   // silently drops the I-span — line 446
    }
```

So FOLLOWLINK's "filtering" is not an explicit check — it is a *natural consequence* of running the I→V conversion through the live POOM. Deleted content falls out because the POOM node was removed by `deletend`. The result is an empty or partial V-span set for the affected endpoint (confirmed by golden test: `golden/links/orphaned_link_target_all_deleted.json`, which shows `result: []` after deletion).

---

### Structural Comparison

| | FINDDOCSCONTAINING | FOLLOWLINK (I→V) |
|---|---|---|
| Primary lookup | `spanf` (spanfilade) | Link orgl via `granf` |
| Post-lookup check | **None** | `retrieverestricted` on candidate document's POOM |
| After DELETE | Returns deleted document | Dropped — POOM has no mapping |
| Return type | Document ISAs | V-spans in a document |
| Ghost behavior | **Returns ghost documents** | Returns empty/partial V-spans |

---

### Conclusion

`FINDDOCSCONTAINING` queries the write-only spanfilade and returns whatever DOCISPAN entries it finds there — with no subsequent POOM cross-check. Because `insertspanf` is called during COPY but `deletevspanpm` never removes the corresponding entry from `spanf`, a document that received transcluded content and later deleted it continues to appear in `FINDDOCSCONTAINING` results for those I-spans.

This makes `FINDDOCSCONTAINING` a *historical journal* query — "which documents have ever contained this I-material?" — not a *current-content* query. The ghost documents are real: the backend returns them, the caller receives the document ISA, but when any attempt is made to convert those I-addresses to V-positions in the returned document, the POOM lookup yields nothing (exactly the silent-drop mechanism that FOLLOWLINK uses).

FOLLOWLINK's "filtering" is not a deliberate guard but a side effect of the mandatory I→V conversion through the live POOM. `FINDDOCSCONTAINING` skips that conversion entirely — it returns raw addresses — so the natural filter never fires.

**Supporting findings:** Finding 0057 (`spanfilade-no-cleanup-on-delete.md`) confirms the write-only spanfilade architecture and documents the absence of any `deletespanf`. Finding 0023 (`find-documents-delete-semantics.md`) provides golden-test evidence of the ghost-document return. Finding 0048 (`followlink-returns-unreferenced-addresses.md`) traces the I→V filtering in FOLLOWLINK's path.
