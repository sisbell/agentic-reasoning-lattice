## Question 4 [evidence]

> Does udanax-green coalesce or normalize adjacent contiguous spans within an endset, so a coverage-contiguous source is always represented as one span?

## KB Synthesis

## Endset Span Coalescing in udanax-green

**Short answer: No, there is no explicit normalization of adjacent contiguous endset spans.** Whether you get one span depends entirely on how the content's I-addresses are structured when the link is created and what operations have occurred since.

---

### What determines endset cardinality

The endset is built through `vspanset2sporglset`, which calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`. The key rule [SS-LINK-ENDPOINT, Finding 0037]:

> `vspanset2sporglset` creates **one sporgl per contiguous I-address region**. A single user-visible V-span may correspond to multiple I-spans when the V-span covers content transcluded from multiple sources.

The cardinality of the endset is determined by I-space fragmentation, not V-space contiguity.

---

### Case 1: Simply-inserted content (one span, naturally)

If a V-span maps to a single contiguous I-address region — i.e., the content was inserted sequentially without interleaved transclusion from multiple sources — `vspanset2ispanset` returns one I-span, producing one sporgl. The endset contains one span.

This is a *natural consequence* of [INV-MONOTONIC] (I-addresses are monotonically increasing) and the POOM's coalescing behavior [SS-WHEREONCRUM, Finding 0062]: sequential inserts at adjacent positions get merged into a single crum via `isanextensionnd`, so the V→I conversion traverses one crum and returns one I-span.

---

### Case 2: Transcluded content (multiple spans at creation)

When the source V-span covers content assembled from multiple sources (e.g., "AA" from document A and "BB" from document B), `permute` returns two non-contiguous I-spans [SS-LINK-ENDPOINT, Finding 0037]:

> Input: 1 V-span covering all of "AABB"  
> Output: 2 sporgls in source endset (one per distinct I-address origin)

**There is no coalescing step** that would merge these back to one span.

---

### Case 3: After rearrangement (fragmentation)

Even a link created against a single-span source can fragment after `REARRANGE` [EC-PIVOT-LINK-FRAGMENTATION, Finding 0019]:

> Link on "CD" at V 1.3 width 0.2. After pivot, endsets report **FOUR spans** (with duplication).

The I-addresses remain the same (rearrange is identity-preserving [INV-REARRANGE-IDENTITY]), but the POOM now maps those I-addresses to non-contiguous V-positions. When `linksporglset2specset` converts back via the POOM, it calls `span2spanset` per sporgl, which finds all V-positions for each I-address region — and the fragmentation is visible and persistent.

---

### Why there is no normalization

The retrieval path `linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset` operates **per-sporgl** with no inter-sporgl consolidation step. [EC-MULTISPAN-LINK-DUPLICATION, Finding 0019] confirms this directly:

> Creating a link with multiple source spans results in `retrieve_endsets` returning duplicate spans — 3 spans where 2 were expected.

The [INV-VSPAN-CONSOLIDATION] invariant (that `retrieve_vspanset` returns maximally consolidated spans) describes POOM *storage* structure for the document's own content — it does not apply to the sporgl-to-vspan conversion in the endset retrieval path.

---

### Summary

| Source condition | Endset span count |
|---|---|
| Contiguous V-span, single-source insert | 1 (naturally, no coalescing needed) |
| Contiguous V-span, multi-source transclusion | ≥ 1 per distinct I-origin |
| After `REARRANGE`/pivot on linked content | May fragment and duplicate |
| Multi-span link creation | May produce duplicates |

Coverage-contiguous V-span → single endset span **only holds reliably for the simple case of non-transcluded content that has not been rearranged**. The system provides no normalization mechanism to guarantee it in the general case [SS-LINK-ENDPOINT Finding 0037, EC-PIVOT-LINK-FRAGMENTATION, EC-MULTISPAN-LINK-DUPLICATION].

---

## Code Exploration

I now have enough to give a definitive answer.

---

## Does udanax-green Coalesce Adjacent Spans in Endsets?

**No. Udanax-green does NOT coalesce or normalize adjacent contiguous spans within an endset.**

Adjacent spans that are coverage-contiguous in the source document are stored and returned as separate spans. Here is the complete evidence.

---

### What `putvspaninlist()` Does — and Where It Is NOT Used

`orglinks.c:329-387` contains genuine span-coalescing logic in `putvspaninlist()`:

```c
/* orglinks.c:345-348 — new span touches end of existing: merge */
spancmp = tumblercmp (&spanptr->stream, &oldspanend);
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);
    return(0);
}
/* orglinks.c:351-355 — existing span touches end of new: merge */
spancmp = tumblercmp (&ptr->stream, &newspanend);
if (!spancmp) {
    movetumbler (&spanptr->stream, &ptr->stream);
    tumbleradd (&spanptr->width, &ptr->width, &ptr->width);
    return(0);
}
```

This correctly merges touching and overlapping spans. **But it is only called from two functions in document-coverage paths, not in any endset path:**

- `retrievevspansetpm()` — `orglinks.c:189, 216, 217` — computes V-span coverage of a POOM node
- `maxtextwid()` — `orglinks.c:289` — computes max text width across crum children

Neither is on the endset create or retrieve path.

---

### Endset Storage Path — No Coalescing

`docreatelink()` at `do1.c:195-221` stores endsets by calling `insertendsetsinspanf()`, which delegates to `insertspanf()` at `spanf1.c:15-53`:

```c
/* spanf1.c:25-52 */
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
```

Each span in the sporglset is inserted as a distinct enfilade node via `insertnd()`. There is no merge step. Two adjacent spans from the client are stored as two separate crums in the spanfilade.

---

### Endset Retrieval Path — No Coalescing

**`followlink` → `dofollowlink` path** (`fns.c:114`, `do1.c:223-232`):

```c
/* do1.c:228-230 */
return (
   link2sporglset (taskptr, linkisa, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &..., sporglset, specsetptr, NOBERTREQUIRED));
```

1. **`link2sporglset()`** at `sporgl.c:67-95` calls `retrieverestricted()` and converts each context node to a sporgl via `contextintosporgl()`. Each stored crum becomes a separate sporgl — no merging.

2. **`linksporglset2specset()`** at `sporgl.c:97-123` appends each sporgl as a separate specset item:

```c
/* sporgl.c:119-120 */
*specsetptr = specset;
specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
```

Pure list append. No adjacency check, no coalescing.

3. When vspecs are built via `sporglset2vspanset()` at `sporgl.c:141-176` → `ispan2vspanset()` → `permute()` at `orglinks.c:404-422`, the consolidation hook is **commented out**:

```c
/* orglinks.c:412-413 */
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

4. `span2spanset()` at `orglinks.c:425-454` calls `onitemlist()` at `orglinks.c:464+`, which simply allocates and appends — no adjacency check.

**`retrieveendsets` path** (`fns.c:350`, `do1.c:369-374`) leads to `retrieveendsetsfromspanf()` at `spanf1.c:190-235`, which chains `specset2sporglset()` → `retrievesporglsetinrange()` → `linksporglset2specset()` — the same no-coalescing path as above.

---

### Dead Consolidation Code

A stub for consolidation was started and abandoned at `orglinks.c:455-462`:

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

The function body is incomplete and commented out. It was never shipped.

---

### Conclusion

If you create a link whose from-endset contains two adjacent contiguous spans — say `[1.0.1, width 5]` and `[1.0.6, width 5]` in the same document — udanax-green stores them as two separate crum nodes in the spanfilade (`spanf1.c:51`) and returns them as two separate span items in the specset (`sporgl.c:119`). No normalization occurs at storage time, during V↔I permutation (consolidation commented out at `orglinks.c:412-413`), or during retrieval (`sporgl.c:119-120`, `onitemlist` at `orglinks.c:517`).

The coalescing implementation in `putvspaninlist()` exists only for computing document V-span coverage, not for link endsets. A coverage-contiguous source is **never** represented as a single merged span in an endset — it remains as however many spans the client originally provided.
