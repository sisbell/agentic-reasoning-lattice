## Question 14 [gregory]

> Does `insertspanf` create one DOCISPAN entry per COPY operation in the target document, or does it create one entry per contiguous I-span within the copied specset — and if the source specset contains three non-contiguous I-ranges, does the target get exactly three DOCISPAN entries?

## KB Synthesis

`insertspanf` creates one DOCISPAN entry **per contiguous I-span**, not per COPY operation. A specset covering three non-contiguous I-ranges produces exactly three DOCISPAN entries.

The mechanism is documented in [SS-DOCISPAN] (Finding 0047):

> `insertspanf` iterates over the `ispanset` linked list and makes one `insertnd` call per `typeispan` struct. Each `typeispan` represents a contiguous range of I-addresses with a `stream` start and `width`.

The loop in `spanf1.c:15-53` is:
```c
for (; sporglset; sporglset = next) { ... insertnd(...); }
```
— one `insertnd` per I-span, not per operation.

**What determines the I-span count?** The conversion upstream. `docopy` calls `specset2ispanset`, which converts V-spans to I-spans by walking the source document's POOM. The POOM returns one I-span per *contiguous I-address region*. If your source specset selects content that maps to three non-contiguous I-address regions (because the content was assembled from three independent insertions, or from insertions interleaved with CREATELINK operations per [INT-LINK-INSERT]), you get three I-spans, and therefore three DOCISPAN entries.

Confirmed by [ST-COPY] (Finding 0047):

> COPY of fragmented source content (e.g., 3 non-contiguous regions) creates 3 DOCISPAN entries. The number of new index entries depends on the I-space fragmentation of the copied content, not its V-space extent.

**Corollary:** A single COPY of a V-span covering contiguous text (even if large) creates exactly **1** DOCISPAN entry, because `vspanset2ispanset` collapses it into one I-span [SS-DOCISPAN, Finding 0033].

**Storage cost** therefore tracks editorial fragmentation, not byte count — [INV-SPANF-GROWTH] formalizes this: `|DOCISPAN| ≤ Σ_{all INSERT/COPY ops} |ispanset(op)|`, where `|ispanset(op)|` equals the number of contiguous I-address runs in the content placed by that operation.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: One DOCISPAN entry per contiguous I-span, not per COPY operation

### The call chain

`docopy` [`do1.c:45–65`] is the entry point for a COPY:

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)   // [do1.c:54]
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)       // [do1.c:60]
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)    // [do1.c:62]
```

The **same `ispanset`** feeds both `insertpm` (into the POOM) and `insertspanf` (into the spanfilade).

---

### Step 1: How `specset2ispanset` builds the `ispanset`

`specset2ispanset` [`do2.c:14–46`] walks the specset. For each `VSPECID` item it calls `vspanset2ispanset` → `permute` [`orglinks.c:397–422`] → `span2spanset` per V-span → `retrieverestricted` to map each V-span to its constituent I-spans, appending one `typeispan` per contiguous I-range to the output list.

The result is a **flat linked list of `typeispan` nodes**, one node per contiguous I-range that the V-span maps to in the permascroll. If the V-specset projects onto three non-contiguous I-ranges, `ispanset` is a three-element linked list.

---

### Step 2: The `insertspanf` loop is per-item

`insertspanf` [`spanf1.c:15–54`]:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler(&((typeispan *)sporglset)->stream, &lstream);   // [spanf1.c:27]
        movetumbler(&((typeispan *)sporglset)->width,  &lwidth);    // [spanf1.c:28]
        movetumbler(isaptr, &linfo.homedoc);                        // [spanf1.c:29]
    } ...
    movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);             // [spanf1.c:49]
    movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);              // [spanf1.c:50]
    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE); // [spanf1.c:51]
}
```

**`insertnd` is called exactly once per iteration — one call per item in the list.** There is no batching, no consolidation before calling `insertnd`.

The ORGLRANGE key — the spanfilade's "which document" axis — is set once before the loop:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // [spanf1.c:22]
tumblerclear(&crumwidth.dsas[ORGLRANGE]);                       // [spanf1.c:23]
```
`prefixtumbler` [`tumble.c:641–651`] prepends the `spantype` integer (`DOCISPAN`) as the high digit of the tumbler address, then appends the document ISA. This is identical for every iteration — all three crums get the same ORGLRANGE origin, recording them as belonging to the same target document.

---

### Step 3: Does `insertnd` merge adjacent spans?

`insertcbcnd` [`insertnd.c:242–275`] contains the only place where a new insertion might be collapsed into an existing bottom crum. It calls `isanextensionnd` [`insertnd.c:301–309`]:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))  // [insertnd.c:305]
        return(FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return(lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype))); // [insertnd.c:308]
}
```

Merging requires **both**:
1. Same `homedoc` (target document ISA) — this is satisfied, all three crums have the same `isaptr`
2. The existing crum's `reach` (end boundary across **all** dimensions) equals the new crum's `origin` — i.e., the new I-span starts exactly where the previous one ends in SPANRANGE

For three **non-contiguous** I-ranges, condition 2 fails for every pair. The SPANRANGE end of crum N does not equal the SPANRANGE start of crum N+1. `isanextensionnd` returns `FALSE`, and `insertcbcnd` falls through to `createcrum` + `adopt` [`insertnd.c:260–274`], allocating a new bottom crum each time.

---

### Conclusion

**`insertspanf` creates one DOCISPAN entry (one spanfilade bottom crum) per contiguous I-span in the `ispanset` passed to it — not one per COPY operation.**

If the source specset converts to an `ispanset` with three non-contiguous I-ranges, `insertspanf` calls `insertnd` three times [`spanf1.c:51`], and the spanfilade gains exactly **three** new DOCISPAN bottom crums. They share the same ORGLRANGE key (target document ISA + `DOCISPAN` type) but have distinct SPANRANGE coordinates corresponding to each of the three I-ranges.

The only case where fewer than N crums would result is if two of the I-ranges are **contiguous** (adjacent with no gap) and were inserted in sequence — `isanextensionnd` would then merge the second into the first. By definition, non-contiguous ranges cannot trigger this merge.
