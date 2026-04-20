## Question 17 [gregory]

> The V→I mapping within a single document can become arbitrarily fragmented (many small spans rather than a few large ones) through editing — does this fragmentation degrade any system behavior beyond requiring more mapping entries, or is it purely a representation cost?

## KB Synthesis

Fragmentation is not purely a representation cost. It has several behavioral consequences:

## Observable behavioral changes

**Link endset fragmentation** [ST-LINK-CREATE/Finding 0037]: When a vcopy or link endpoint spans content assembled from multiple non-contiguous I-address regions, `vspanset2sporglset` creates one sporgl per contiguous I-address run. Fragmented source content → more sporgls per endpoint. This is observable: `retrieve_endsets` returns more V-spans, and the bugs [EC-PIVOT-LINK-FRAGMENTATION], [EC-MULTISPAN-LINK-DUPLICATION] arise directly from this — after pivot rearrangement, links can appear duplicated in `find_links` results because the endset decomposes into redundant entries.

**Spanfilade growth** [SS-DOCISPAN/Finding 0047, INV-SPANF-GROWTH]: COPY of fragmented content creates DOCISPAN entries proportional to the number of I-spans, not bytes. A heavily edited document used as a VCOPY source permanently increases the spanfilade entry count per copy operation. Since the spanfilade is write-only [INV-SPANF-WRITE-ONLY], these entries accumulate forever.

## Permanent structural degradation

**Tree height ratchet** [SS-ENFILADE-TREE/Finding 0058]: Each cursor repositioning costs +2 crums [ST-CRUM-BOUND], and the POOM tree height grows monotonically (`levelpull` is disabled). The tree never shrinks even after delete-everything. This means heavily-edited documents carry permanently inflated lookup overhead — O(log N) where N is the lifetime crum count, not the current content size.

**CREATELINK breaks I-address contiguity** [INT-LINK-INSERT/Finding 0063]: CREATELINK allocates an orgl in the granfilade's content address range, causing all subsequent text inserts to allocate non-contiguous I-addresses relative to pre-link text. This makes `compare_versions` report two spans instead of one for otherwise contiguous text, and increases DOCISPAN entry count for any COPY spanning the gap.

## Purely representational costs

The following are costs without behavioral change:
- More crums in the cache → more memory pressure → more grim-reaper evictions [EC-CROSS-ENFILADE-EVICTION], but this affects durability ordering, not correctness
- V-span output is consolidated [INV-VSPAN-CONSOLIDATION] — `retrieve_vspanset` hides I-space fragmentation from callers retrieving text content

## Summary

The critical threshold is whether fragmented content is used as a **link endpoint or vcopy source**. At that point, fragmentation propagates into the spanfilade as permanent additional entries [SS-DOCISPAN], produces observable endset fragmentation bugs [EC-PIVOT-LINK-FRAGMENTATION], and increases the complexity of `find_links` intersection [SS-FIND-LINKS/Finding 0035]. For documents that are only read, fragmentation is representational overhead only.

---

## Code Exploration

Now I have everything I need to give a complete answer.

---

## V→I Fragmentation: Behavioral Degradation Beyond Representation Cost

Fragmentation is **not** purely a representation cost. The code shows six concrete degradation mechanisms, each tied to specific source lines.

---

### 1. `permute()` multiplies every V↔I conversion into N independent enfilade traversals

Both `vspanset2ispanset()` and `ispan2vspanset()` route through a single function [orglinks.c:397-401, 389-394]:

```c
typespanset *permute(...) {
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                      restrictionindex, targspansetptr, targindex);
    }
    return (save);
}
```
[orglinks.c:404-422]

Each iteration calls `span2spanset()` [orglinks.c:425-453], which calls `retrieverestricted()` — a full 2D POOM tree walk. For N fragments, this is **N independent enfilade traversals**, not one.

---

### 2. The retrieval inner loop is the documented CPU hotspot — and fragmentation fires it repeatedly

`retrieverestricted()` → `retrieveinarea()` → `findcbcinarea2d()` [retrie.c:229-268] recursively walks the POOM tree, calling `crumqualifies2d()` at every node. The comment on that function [retrie.c:270]:

```c
bool crumqualifies2d(...) /* 6-28-84 old code; NOTE in retrieves this is ---40% -- of cpu */
```

This is the identified bottleneck. Every fragment fires it from the root.

---

### 3. Each fragment permanently grows the POOM and spanfilade

`insertpm()` [orglinks.c:100-132] loops over the sporglset (one entry per ispan fragment) and calls `insertnd()` for each:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
}
```

Likewise `insertspanf()` [spanf1.c:25-52] adds one spanfilade node per fragment:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

After `insertnd()`, `recombine()` is called [insertnd.c:76] to rebalance — but the enfilade can only grow (see next point).

---

### 4. `levelpull` is completely stubbed — the enfilade never shrinks

`recombinend()` [recombine.c:104-131] tries to shrink the tree when it's underpopulated [recombine.c:129-130]:

```c
if (father->isapex)
    levelpull (father);
```

But `levelpull` [genf.c:318-342] is dead code:

```c
int levelpull(typecuc *fullcrumptr)
{
    return(0);
    /*
        [entire implementation commented out]
    */
}
```

The enfilade trees — POOM and spanfilade — are monotonically increasing. Every fragmented insertion adds permanent nodes. Since the tree height grows logarithmically with node count, a heavily-fragmented document has a deeper tree, and all future retrievals pay deeper recursion in `findcbcinarea2d()`.

---

### 5. `finddocscontainingsp()` and `retrievesporglsetinrange()` both loop per fragment

"Find which documents contain this content" [spanf1.c:170-182]:

```c
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted ((typecuc*)spanf, &docspace, ORGLRANGE,
                                  ispanset, SPANRANGE, (typeisa*)NULL);
    ...
    contextfree (context);
}
```

And the link-following path's `retrievesporglsetinrange()` [do2.c:244-266]:

```c
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr,
                                  SPANRANGE, whichspace, ORGLRANGE, ...);
    ...
}
```

Both are: one enfilade traversal per fragment. A logical content range split into N fragments by editing causes both queries to cost N× what they would for an unfragmented document.

---

### 6. Result list accumulation is O(N²) via `onitemlist()`

Every result span is appended by scanning to the list tail [orglinks.c:522-534]:

```c
for (temp = *itemsetptr;
     temp && ((typeitemheader *)temp)->next;
     temp = (typeitem *)((typeitemheader *)temp)->next)
    ;
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

With N fragments each producing results, the accumulation cost is quadratic in the total result count.

---

### 7. Consolidation was recognized as the fix — and abandoned

Inside `permute()`, there is a commented-out call [orglinks.c:412-413]:

```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

At the end of the file there's an incomplete stub [orglinks.c:456-462]:

```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

The body stops mid-expression. `cleanupvspanlist()` [orglinks.c:297-311], which does merge adjacent spans, exists inside an `#ifdef UnDEFined` block — also disabled.

The developers diagnosed the problem, attempted a fix, and abandoned it.

---

### Summary

| Operation | Fragmentation effect |
|---|---|
| `vspanset2ispanset` / `ispan2vspanset` | N enfilade traversals instead of 1, at the documented 40%-of-CPU hotspot |
| `finddocscontainingsp` | N enfilade traversals instead of 1 |
| `retrievesporglsetinrange` (link follow) | N enfilade traversals instead of 1 |
| `insertpm` / `insertspanf` (copy/insert) | N permanent POOM/spanfilade nodes added |
| `onitemlist` result accumulation | O(N²) list-scan overhead |
| Enfilade tree height | Monotonically increases; `levelpull` is stubbed, so fragmentation-induced growth is permanent |

The enfilade's log-depth guarantee applies **per query**, not across a span set. N fragments = N queries = N × log(height) work. And because `levelpull` is stubbed, every fragmented insertion ratchets the tree permanently deeper, making all future traversals more expensive. There is no consolidation, no self-healing, and no upper bound on fragment count.
