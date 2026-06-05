## Question 15 [evidence]

> Because the spanfilade is write-only and monotonic, can the query return endsets pointing at content that has been deleted from every current POOM (stale DOCISPAN entries)?

## KB Synthesis

Yes, with an important distinction between two layers of the spanfilade.

## DOCISPAN queries: stale results are directly observable

FINDDOCSCONTAINING **does** return documents whose POOM no longer contains the queried I-addresses. The spanfilade is append-only [INV-SPANF-WRITE-ONLY]; DELETE modifies only the POOM, never the spanfilade [ST-DELETE, Finding 0057]. So after deleting transcluded content, FINDDOCSCONTAINING still returns the document as a match [EC-STALE-SPANF-REFERENCE]. The formal invariant is asymmetric: `actual_docs(i) ⊆ find_documents(i)` — the spanfilade is a superset of current POOM membership.

## Link endset queries: stale entries exist, but I-to-V filtering masks them

The link endset entries (LINKFROMSPAN, LINKTOSPAN) in the spanfilade are also never deleted. However, a universal filter intervenes before results reach the caller.

Both RETRIEVEENDSETS and FOLLOWLINK resolve I-addresses back to V-spans through the queried document's POOM via `linksporglset2specset` → `span2spanset` → `retrieverestricted`. When an I-address has no current POOM mapping, `retrieverestricted` returns NULL and the address is **silently dropped** [INV-ITOV-FILTERING]. The result is an empty endset span, not a stale V-address pointer [EC-GHOST-LINK].

So: stale entries exist in the spanfilade, but callers receive **empty spans** rather than dangling V-addresses pointing at deleted content.

## The reachability constraint on discovery itself

When endpoint content is deleted from *every* current POOM, FINDLINKSFROMTOTHREE also stops discovering the link through normal search paths. The search converts a caller-supplied V-spec to I-addresses [ST-FIND-LINKS]. Since those I-addresses are no longer in any live POOM, no V-spec query can produce them as input. The link becomes unreachable via content-based discovery — the "orphaned link" state [EC-ORPHANED-LINK] — even though the spanfilade entry persists.

**Summary:** Stale spanfilade entries exist and cause FINDDOCSCONTAINING to return supersets. For link endset queries, the stale entries exist but the mandatory I-to-V conversion layer [INV-ITOV-FILTERING] ensures callers receive empty spans rather than stale V-span pointers. The net effect is ghost links [EC-GHOST-LINK], not corrupted address references.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer, verified against actual source lines.

---

## Yes — The Spanfilade Query Returns Stale DOCISPAN Entries

This is confirmed by reading the full execution chain. The answer has three interlocking parts: (1) deletion leaves spanfilade entries untouched, (2) the query path passes `NULL` where a version filter should go, and (3) the code that *could* have filtered by homedoc is permanently disabled — and the comment reveals the authors knew it.

---

### Part 1: Deletion Only Touches the POOM

`dodeletevspan` [`do1.c:158-167`] calls `deletevspanpm` and nothing else:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

`deletevspanpm` [`orglinks.c:145-151`]:

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

`deletend` removes the V-space nodes from the POOM. There is no call to any spanfilade function here — no cleanup, no invalidation. The DOCISPAN entries written at insert time remain in the spanfilade permanently.

---

### Part 2: The Query Passes NULL Where the Version Filter Would Go

`dofinddocscontaining` [`do1.c:15-23`] calls `finddocscontainingsp`. The critical call is at `spanf1.c:171`:

```c
context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                               ispanset, SPANRANGE,
                               (typeisa*)NULL);          /* ← no docisaptr */
```

The sixth argument to `retrieverestricted` is `docisaptr` — the document identity used to validate whether a crum belongs to the right version. It is explicitly passed as `NULL`.

`retrieverestricted` [`retrie.c:56-85`] propagates this:

```c
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;           /* ← always taken for spanfilade queries */
}
temp = retrieveinarea(..., (typebottomcruminfo*)infoptr);
```

`infoptr` arrives at `findcbcinarea2d` as `NULL`, and then at `crumqualifies2d` [`retrie.c:270-305`] as `NULL`:

```c
if ((crumptr->height == 0) && infoptr &&
    !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

With `infoptr == NULL`, the short-circuit (`&& infoptr`) means this check **never fires**. Every crum passes, regardless of whether its `homedoc` is still a live document.

---

### Part 3: The homedoc Filter Is Actively Disabled — With a Date-Stamped Comment

The decisive evidence is in `findcbcinarea2d` [`retrie.c:229-268`]. This is the function that traverses the enfilade and feeds crums to `crumqualifies2d`. It contains this guard, *before* the traversal loop:

```c
#ifndef DISTRIBUTION
if(infoptr){
    fprintf(stderr,"not NULL infoptr versions mumble specialcase "
                   "11/27/84 shouldent happen till we try something fancier\n");
    gerror("findcbcinarea2d");
}
#else
    if (infoptr)
        gerror("!NULL");
#endif
```

[`retrie.c:244-251`]

This is not a passive no-op. In debug builds it prints a datestamped admission — *11/27/84* — and then calls `gerror`, which is a fatal abort. In distribution builds it also calls `gerror`. **Passing a non-NULL `docisaptr` to `retrieverestricted` in any spanfilade query path would crash the server.**

The homedoc filter in `crumqualifies2d:274` is therefore unreachable dead code for this query path — not just skipped, but guarded by a hard abort.

A confirming comment exists in `retrievesporglsetinrange` [`spanf1.c:245`]:

```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                              whichspace, ORGLRANGE,
                              (typeisa*)NULL/*kluge to make links show thru to version
                                              &sporglptr->sporgladdress*/);
```

The commented-out `&sporglptr->sporgladdress` is the version address that *was intended* as the filter. It was replaced with `NULL` — annotated as a "kluge" — to make links "show thru" across versions. This is the endset retrieval path (used by `doretrieveendsets` → `retrieveendsetsfromspanf`), and it exhibits the same stale-entry exposure.

---

### Summary: The Full Vulnerability Chain

| Step | Location | What Happens |
|------|----------|--------------|
| Insert | `do1.c:62` / `spanf1.c:51` | DOCISPAN crum written with `linfo.homedoc = *isaptr` |
| Delete | `do1.c:165` / `orglinks.c:149` | `deletend()` removes V-span from POOM; spanfilade untouched |
| Query | `spanf1.c:171` | `retrieverestricted(..., (typeisa*)NULL)` — no version filter |
| Propagation | `retrie.c:81` | `infoptr = NULL` |
| Guard | `retrie.c:244-251` | Non-NULL `infoptr` triggers `gerror` — filter is permanently disabled |
| Result | `crumqualifies2d:274` | Homedoc check dead; stale crum passes |
| Return | `spanf1.c:172-179` | Caller receives document address from deleted content |

**The spanfilade is write-only and the homedoc filter that would have caught stale entries was recognized as incomplete on 11/27/84 and disabled via a fatal abort guard.** Any DOCISPAN entry ever written — regardless of subsequent deletions — can be returned by a query. The caller has no way to distinguish a live result from a stale one.
