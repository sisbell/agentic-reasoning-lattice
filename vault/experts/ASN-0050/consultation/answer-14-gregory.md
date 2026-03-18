## Question 14 [gregory]

> If a document has content transcluded into three other documents and that content is DELETEd from the source, do the DOCISPAN entries in the spanfilade for the source document remain searchable by `findlinksfromtothreesp`, and does the source document still appear in `find_documents_containing` results despite having no current POOM mapping?

## KB Synthesis

Yes on both counts, and the two mechanisms are distinct sub-indices within the same append-only spanfilade.

**DOCISPAN entries persist after DELETE**

DELETE modifies only the document's POOM in the granfilade. `dodeletevspan` → `deletevspanpm` → `deletend` — none of these functions call any spanfilade function. [ST-DELETE] (Finding 0057) states the frame condition explicitly: `delete(D, vspan) ⟹ spanf_entries_after = spanf_entries_before`. The spanfilade has no delete operation anywhere in `spanf1.c` or `spanf2.c`. [INV-SPANF-WRITE-ONLY] formalizes this: the set of spanfilade entries is monotonically non-decreasing, forever.

**`find_documents_containing` still returns the source document**

This is confirmed by [EC-STALE-SPANF-REFERENCE] and [INV-IADDRESS-PERMANENT]. The DOCISPAN entries created when those I-addresses were first inserted into the source document remain in the spanfilade. `finddocscontainingsp` queries these entries and returns the source document alongside the three transcluding documents — even though the source's POOM no longer maps those I-addresses to any V-position. The correct invariant is:

```
actual_docs(i) ⊆ find_documents(i)
```

where `actual_docs(i) = {D | ∃ v : poom.D(v) = i}`. The reverse does not hold. [INT-DELETE-SPANF-DIVERGENCE] labels this the permanent divergence between POOM and spanfilade state.

**A note on `findlinksfromtothreesp` specifically**

`findlinksfromtothreesp` does not search DOCISPAN entries. It searches the link endset sub-index (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 in the ORGLRANGE dimension), not the type-4 DOCISPAN sub-index. [SS-DOCISPAN] and [SS-SPANF-OPERATIONS] distinguish these as separate sub-structures within the spanfilade. If links were created on those I-addresses, their endset entries also persist (same write-only guarantee), so `findlinksfromtothreesp` continues to discover them — including from the three transcluding documents, whose POOMs are completely unaffected by the source DELETE per [FC-DELETE-CROSS-DOC].

**The three transcluding documents are entirely unaffected**

DELETE is strictly per-document POOM surgery. [FC-DELETE-CROSS-DOC] confirms: `∀ D' ≠ D : delete(D, vspan) ⟹ poom(D') = poom_before(D')`. The transcluding documents' POOMs still map those I-addresses to V-positions, their DOCISPAN entries persist, and link discovery via `find_links` on any of those three documents continues to work normally.

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## Answer

### The Two Relevant Structures

- **Granfilade (`granf`)**: Per-document POOMs (Permutation Object Ordering Matrices) that map virtual V-addresses to I-addresses (permascroll positions).
- **Spanfilade (`spanf`)**: A single global 2D enfilade indexed by `(SPANRANGE, ORGLRANGE)`. The `ORGLRANGE` dimension encodes both a document ISA and a **span type** prefix. Four span types are defined [xanadu.h:36-39]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

---

### What Happens When Content Is Transcluded (COPY)

`docopy` [do1.c:45-65] calls both:
1. `insertpm(...)` — writes a crum into the destination document's POOM (granfilade)
2. `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` — writes an entry into the spanfilade

`insertspanf` [spanf1.c:22] encodes the entry:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ...
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

The **ORGLRANGE key is `4.docISA`** (spantype=4 prefixed to the document address). The **SPANRANGE key is the ispan** (permascroll address of the content). This DOCISPAN entry permanently records: *"document `docISA` contains ispan `I`."*

When source doc **S** has content (at ispan I, vspan V), and that content is transcluded into docs **A**, **B**, **C** — each `docopy` writes a DOCISPAN entry for the respective transclusion target (A, B, or C), embedding the same ispan I in SPANRANGE. S itself also has its own DOCISPAN entry written during its original `doinsert` → `docopy` chain.

---

### What `dodeletevspan` Actually Modifies

```c
// do1.c:158-167
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

`deletend` [edit.c:31] operates on `docorgl` (a handle into the **granfilade**). It removes the V→I mapping from S's POOM.

**The spanfilade (`spanf`) is never touched.** A grep over the entire backend for `deletend.*spanf`, `spanf.*delete`, and `removefromspan` returns zero matches. There is no code path anywhere in the system that removes DOCISPAN (or any other) spanfilade entries when content is deleted.

---

### Q1: Do the DOCISPAN Entries for S Remain Searchable by `findlinksfromtothreesp`?

**First, a structural clarification**: `findlinksfromtothreesp` does **not** search DOCISPAN entries at all. It operates on LINKFROMSPAN (1), LINKTOSPAN (2), and LINKTHREESPAN (3) entries — which are in an entirely different numeric range of the ORGLRANGE dimension of the spanfilade (keys `1.x`, `2.x`, `3.x` vs. DOCISPAN's `4.x`).

`findlinksfromtothreesp` [spanf1.c:56-103] drives through `sporglset2linkset` → `sporglset2linksetinrange` [sporgl.c:239-269]:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
// spantype = 1, 2, or 3 — never 4
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

DOCISPAN entries never appear in any `retrieverestricted` call issued by this path. They are invisible to `findlinksfromtothreesp` regardless of whether they persist or not.

**What `findlinksfromtothreesp` does require** is resolving the input specset to an ispan via S's POOM. The path is:

`findlinksfromtothreesp` → `specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65] → `findorgl(granf, S)` + `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted(S's POOM, vspanptr, V, NULL, I, NULL)`

Since `dodeletevspan` removed the V→I mapping from S's POOM, `retrieverestricted` on that POOM returns an empty context. The ispan lookup yields nothing. The sporglset is empty. `sporglset2linksetinrange` loops over nothing. `findlinksfromtothreesp` returns `*linksetptr = NULL`.

**Conclusion for Q1**: After deleting S's content at vspan V:
- The DOCISPAN entries for S in the spanfilade **do persist** (they are never removed).
- They are **not searchable by `findlinksfromtothreesp`** — not because they disappear, but because that function never queries DOCISPAN entries. If the specset is expressed as a vspec in terms of S, the POOM resolution step fails silently and the function returns no links. If the specset is expressed in terms of A, B, or C (which still have valid POOM mappings to ispan I), `findlinksfromtothreesp` still works and returns any links attached to that ispan.

---

### Q2: Does S Still Appear in `find_documents_containing` Results?

`dofinddocscontaining` [do1.c:15-23]:
```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));
}
```

`finddocscontainingsp` [spanf1.c:151-188]:
```c
tumblerincrement (&docspace.stream, 0, DOCISPAN, &docspace.stream);
tumblerincrement (&docspace.width, 0, 1, &docspace.width);
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                   ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        // add document to result set
    }
}
```

This function queries the spanfilade **directly** for DOCISPAN entries in `ORGLRANGE` that intersect the given ispanset in `SPANRANGE`. It does **not** consult any document's POOM. The DOCISPAN entry for S (recording that S once contained ispan I) was written when S's content was originally inserted and was **never removed** by `dodeletevspan`.

**Conclusion for Q2**: **Yes.** Source document S will still appear in `find_documents_containing` results, even though S's POOM has no current mapping for that content. The spanfilade retains the phantom DOCISPAN entry from S's original content insertion, and `finddocscontainingsp` finds it directly without any POOM consultation.

---

### The Structural Inconsistency

This reveals a fundamental post-delete inconsistency in udanax-green's storage model:

| Data structure | After `dodeletevspan` |
|---|---|
| S's POOM (granfilade) | V→I mapping removed; S no longer maps vspan V to ispan I |
| Spanfilade DOCISPAN entries | S's entry `(4.S, I)` remains permanently |
| Spanfilade link endpoint entries | Entries for any links referencing S's content remain, but are unreachable if the specset is expressed as an S vspec, because POOM lookup fails |

The spanfilade is an **append-only** structure from the perspective of content operations. DELETE removes content from the POOM but leaves all spanfilade traces intact. Any query path that routes through the spanfilade directly (like `finddocscontainingsp`) will observe S as a containing document. Any query path that must first resolve a vspec through S's POOM (like `findlinksfromtothreesp`) will silently fail to map the now-deleted vspan and return empty results — but not because the spanfilade was cleaned up; rather because the POOM resolution step upstream of the spanfilade query returns nothing.
