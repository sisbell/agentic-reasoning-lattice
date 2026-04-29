## Question 15 [gregory]

> Is the fan-out from I-space to V-space unbounded — can any number of documents map V-addresses to the same I-address range — or was there a practical or design limit on how many V→I references could share a single I-address span?

## KB Synthesis

The fan-out is **unbounded by design**. Multiple KB entries converge on this:

**POOM multimap within a single document**

[SS-POOM-MULTIMAP] (Finding 0039) establishes that the POOM is explicitly a multimap. `findcbcinarea2d()` accumulates *every* matching leaf node; `incontextlistnd()` inserts each into a sorted list and never replaces. A query by I-address returns all V-positions referencing it. [EC-SELF-TRANSCLUSION] confirms "no limit observed on number of V-positions per I-address" — tested at N=2 and N=3, with the mechanism making N unbounded.

**Cross-document fan-out via the spanfilade**

[SS-DOCISPAN] (Finding 0047): each COPY/INSERT creates one DOCISPAN entry per I-span in the spanfilade, mapping that I-address range to the document. Any number of documents can accumulate entries for the same I-address range. [INV-SPANF-WRITE-ONLY] (Finding 0057) confirms the spanfilade is append-only — entries are never removed. [PRE-COPY] (Finding 0046) confirms COPY performs no duplicate checking whatsoever.

**The design requires unbounded fan-out**

The entire Xanadu transclusion model depends on it. [INT-LINK-TRANSCLUSION] states links are discoverable from *any* document sharing content identity — which only works if an arbitrary number of documents can reference the same I-address range. [INV-IADDRESS-PERMANENT] and [INV-NO-IADDR-REUSE] ensure I-addresses persist forever, meaning the fan-out set can only grow.

**Practical constraints (not design limits)**

The only limits are resource-level:
- Memory: the grim reaper cache (all enfilades share one pool per [SS-CACHE-MECHANISM])
- Disk: `enf.enf` block allocator capacity per [SS-UNIFIED-STORAGE]
- Spanfilade growth: O(number of COPY/INSERT operations) per [INV-SPANF-GROWTH], not O(total bytes), so each transclusion event adds exactly one entry regardless of content size

There is no architectural cap, no reference-count limit, and no structural mechanism that would reject an N+1th document transcluding an already-N-times-transcluded I-address span.

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## Fan-out from I-space to V-space in udanax-green

**Short answer:** The fan-out is architecturally unbounded in both directions. Any number of documents can map V-addresses to the same I-address range, and within a single document the same I-range can appear at multiple V-positions. There is no designed cap — the opposite is true: the entire infrastructure exists to support unlimited sharing.

---

### How V→I and I→V mappings are stored

Each document has an **orgl** — a POOM (permutation-matrix) enfilade. A POOM crum carries a two-dimensional width/displacement: `dsas[I]` for I-space and `dsas[V]` for V-space [wisp.h:19-21]. Every crum records one contiguous V→I mapping for one document.

```c
/* wisp.h:19-21 */
#define I  0
#define V  1
```

A global **spanfilade** (SPAN enfilade) serves as an inverted index: it maps I-address ranges back to document ISAs. Its crums use `dsas[ORGLRANGE]` (the document's prefix-tumbler'd ISA) and `dsas[SPANRANGE]` (the I-address range) [wisp.h:15-16].

---

### Cross-document fan-out: every `docopy` adds one more reference

When content is transcluded into a document, `docopy` [do1.c:45-65] does two things:

```c
/* do1.c:60-62 */
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

1. **`insertpm`** [orglinks.c:75-134] inserts a crum into *this document's orgl* mapping the requested V-address to the I-span.
2. **`insertspanf`** [spanf1.c:15-54] inserts a crum into the *global spanfilade* recording that this document now contains that I-span:

```c
/* spanf1.c:49-51 */
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

There is **no limit check** and **no deduplication across documents** anywhere in this path. Each call to `docopy` from a different document adds one more crum to the spanfilade for the same I-range. Ten thousand documents can independently reference the same I-span; the spanfilade accumulates ten thousand crums.

---

### How I→V fan-out is retrieved

`finddocscontainingsp` [spanf1.c:151-188] answers "which documents contain this I-span?" It calls `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` [retrie.c:229-268]:

```c
/* retrie.c:252-264 */
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) {
        continue;
    }
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

This is a recursive traversal of the entire matching subtree. Every qualifying crum is appended to `headptr` — a linked list. Back in `finddocscontainingsp`:

```c
/* spanf1.c:170-180 */
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE, ispanset, SPANRANGE, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        ...
        addresssetptr = (typelinkset *) onitemlist(taskptr, (typeitem*)&document, (typeitemset*)addresssetptr);
    }
    contextfree (context);
}
```

The inner loop has no `break`, no maximum count, no page size. It collects every document that references the I-span. The result list is as long as the fan-out is deep.

---

### Per-document fan-out: same I-range at multiple V-positions

Within a single document, the same I-range can appear at multiple V-addresses. `insertpm` [orglinks.c:100-132] loops over `sporglset` and calls `insertnd` for each entry:

```c
/* orglinks.c:100-131 */
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);
    movetumbler (vsaptr, &crumorigin.dsas[V]);
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

Calling `docopy` twice with the same `ispanset` and different `vsaptr` values yields two crums in the orgl with the same `dsas[I]` but different `dsas[V]`. There is no uniqueness constraint on I-addresses within an orgl. The I→V conversion `ispan2vspanset` [orglinks.c:389-394] → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` returns all matching crums — again without a limit.

---

### The one place fan-out is *reduced*: `isanextensionnd`

In `insertcbcnd` [insertnd.c:242-275], before creating a new bottom crum the code checks whether the incoming span is a contiguous extension of an existing one from the *same* source document:

```c
/* insertnd.c:249-258 */
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

`isanextensionnd` [insertnd.c:301-309] checks two things: the `homedoc` fields must match (same source document), and the new span must start exactly where the existing crum ends (`reach == origin`). If both are true, the existing crum is widened rather than a new one created.

This is a **fragmentation-reduction optimization**, not a fan-out cap. It only merges runs *within the same document* that are strictly contiguous in both dimensions. Two different documents referencing the same I-range never trigger this merge, so cross-document fan-out is never pruned.

---

### What the constants actually bound

| Constant | Value | What it limits |
|---|---|---|
| `NPLACES` [common.h:53] | 16 | Depth of tumbler addresses (16 digit levels, each `uint32_t`) |
| `MAXUCINLOAF` [enf.h:26] | 6 | Children per upper crum in one on-disk loaf |
| `MAX2DBCINLOAF` [enf.h:27] | 4 | 2D bottom crums per loaf |
| `MAXCUTS` [common.h:108] | 4 | Cut positions in one `dorearrange` call |

None of these is a logical cap on the number of documents sharing an I-span. `MAXUCINLOAF` and `MAX2DBCINLOAF` are disk storage granularity constants; the `splitcrumupwards` mechanism [called from `insertcbcnd` line 272] grows the tree upward when a loaf fills up, so the enfilade height is unbounded.

The only genuine constraint is the address space: `NPLACES = 16` mantissa digits of `tdigit = uint32_t` per tumbler. This makes the I-address space astronomically large (up to ~(2³²)¹⁶ positions per document) but not literally infinite. In practice, storage exhaustion (heap + disk) is the effective limit long before the address space runs out.

---

### Conclusion

**The fan-out is unbounded by design.** The architecture explicitly expects — and is engineered to support — an arbitrary number of documents referencing any single I-address span. The spanfilade exists precisely to make that many-to-one reverse mapping queryable at scale. There is no counter, cap, `MAX_TRANSCLUSIONS` constant, or any other limiting mechanism anywhere in the code path from `docopy` through `insertspanf` through `finddocscontainingsp`. The only thing that narrows this in practice is available memory and disk, moderated by the grim reaper cache eviction (`age` field, [enf.h:41]).
