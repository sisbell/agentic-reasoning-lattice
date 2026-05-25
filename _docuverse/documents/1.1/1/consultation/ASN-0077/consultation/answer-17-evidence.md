## Question 17 [evidence]

> If the originating document has been entirely DELETE'd from its POOM but the spanfilade still contains its DOCISPAN entries [FC-SPANFILADE-MONOTONIC], does the origin document still appear in `find_documents_containing` results?

## KB Synthesis

**Yes.** The document still appears in `find_documents_containing` results even after its POOM has been entirely emptied by DELETE.

## The Mechanism

**DELETE touches only the POOM layer.** [ST-DELETE] (Finding 0057) is explicit: `dodeletevspan` → `deletevspanpm` → `deletend` modifies only the document's orgl enfilade (granf/POOM layer). There is no call to any spanf function in this path.

**The spanfilade is append-only.** [INV-SPANF-WRITE-ONLY] documents that no `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. Every DOCISPAN entry ever created by INSERT or COPY persists indefinitely — they cannot be removed.

**This exact scenario is an established invariant.** [INV-IADDRESS-PERMANENT] (Finding 0023) states directly: "Once an I-address is associated with a document (via insert or vcopy), `find_documents` continues to report that document even after the content is deleted from the document's V-stream." The golden test `find_documents_after_delete` confirms this empirically.

## The Resulting State

After deleting all content from document D:

```
POOM(D):     ∅               — no V-to-I mappings remain
spanfilade:  α₁..αₙ → {D}   — DOCISPAN entries unchanged
```

`find_documents_containing(α₁..αₙ)` → returns D (stale reference)

[EC-STALE-SPANF-REFERENCE] names this precisely: D appears as a "ghost reference." The formal invariant from [INT-DELETE-SPANF-DIVERGENCE] is:

> `actual_docs(i) ⊆ find_documents(i)` — but not equality

Consumers must post-filter via I-to-V conversion ([INV-ITOV-FILTERING]) to distinguish live from stale results: attempting to resolve those I-addresses in D's POOM yields ∅, confirming the reference is stale.

---

## Code Exploration

The code is confirmed. Here is the full answer.

---

## Answer: Entirely-Deleted Documents in `find_documents_containing`

**Yes — a document whose content has been entirely deleted from its POOM will still appear in `find_documents_containing` results, as long as its DOCISPAN entries remain in the spanfilade.**

This is not a hypothetical edge case. It is structural: the two data structures are updated independently, and no cleanup path connects them.

---

### The find path queries only the spanfilade

`finddocscontaining` [fns.c:20] calls `dofinddocscontaining` [do1.c:15], which calls `finddocscontainingsp` [spanf1.c:151]. The implementation is the complete picture:

```c
// spanf1.c:167-182
clear (&docspace, sizeof(typespan));
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        if (isinlinklist(*headptr, &document.address))
            continue;
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
}
```

The `docspace` filter is set to `DOCISPAN` span type [spanf1.c:168]. It calls `retrieverestricted` on `spanf` (the spanfilade) [spanf1.c:171], reads the `ORGLRANGE` offset as the document ISA [spanf1.c:173–174], and returns it. **There is no consultation of the granfilade (POOM).** There is no validation that the document ISA corresponds to a non-empty document.

---

### Deletion only modifies the POOM

`dodeletevspan` [do1.c:158] calls `findorgl` to locate the document's POOM node in the granfilade, then delegates entirely to `deletevspanpm` [orglinks.c:145]:

```c
// orglinks.c:145-152
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates on `docorgl` — the POOM node — in the V (version) dimension. **The spanfilade (`spanf`) is never touched.** There is no `deletespanf`, no `removespanf`, no such function exists in the codebase (confirmed: no matches for those symbols anywhere in `backend/`).

---

### The empty-POOM guard is absent from the find path

The only place the codebase checks whether a document's POOM is empty is `doretrievedocvspanset` [do1.c:322]:

```c
// do1.c:330-333
if (isemptyorgl (docorgl)) {
    *vspansetptr = NULL;
    return TRUE;
}
```

`isemptyorgl` [orglinks.c:539] checks whether the POOM node's `cwid` and `cdsp` fields are zero:

```c
// orglinks.c:539-544
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock ((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

This guard is invoked only for content retrieval (`doretrievedocvspanset`). **`finddocscontainingsp` never calls `isemptyorgl`, never calls `findorgl`, and never touches the granfilade at all.**

---

### Conclusion

The spanfilade is append-only with respect to deletion. DOCISPAN entries written at insertion time are permanent residents. When `find_documents_containing` is called with a span that the now-empty document once contained, `retrieverestricted` finds those stale entries, extracts the document ISA from the `ORGLRANGE` offset, and returns it as a match — exactly as if the document still had content.

The fix would require either: (a) a compensating deletion into the spanfilade during `dodeletevspan`, or (b) a post-filter in `finddocscontainingsp` that calls `findorgl` + `isemptyorgl` on each candidate before adding it to the result set. Neither mechanism exists.
