## Question 19 [gregory]

> When multiple I-address spans compose an endset, does their ordering within the endset carry semantic meaning (first span is primary, etc.), or is the endset an unordered set where only membership matters?

## KB Synthesis

The KB does not explicitly address whether endset span ordering carries semantic primacy (e.g., "first span is primary"), but the relevant entries let me give a clear synthesis.

## Endsets are semantically sets — ordering is a V-sorted artifact

**At the I-span (internal) level**, Finding 0037 [SS-LINK-ENDPOINT] explicitly calls an endset "a set of I-spans (sporgls)." The creation path (`vspanset2sporglset` at `sporgl.c:35-65`) iterates over every I-span returned by `vspanset2ispanset` and creates one sporgl per contiguous I-address region. There is no weighting, ranking, or primacy — the loop accumulates all qualifying regions unconditionally.

**The ordering that does exist is V-sorted.** [SS-CONTEXT-LIST] (Finding 0078) establishes that `incontextlistnd()` — used during POOM retrieval — maintains ascending V-address order via insertion-sort, regardless of tree structure. Since sporgls are produced from POOM retrieval results, the I-spans in an endset will be ordered by the V-address of the content they represent in the source document.

**At the SpecSet (output) level**, [INV-SPECSET-ORDER] and [SS-SPECSET] confirm that SpecSet operations (retrieve, vcopy, compare) process VSpecs in sequence order and results are order-sensitive. But this ordering is determined by the V-sorted POOM retrieval, not by any "primary span" designation at link creation time.

## No primary-span semantics are documented

[SS-FOLLOW-LINK] (Finding 0028) and [SS-FOLLOWLINK] (Finding 0048) describe `follow_link` as returning "the complete, original SpecSet for the requested endpoint" — the full set without any filtering or ordering based on semantic priority. [PRE-FOLLOWLINK] confirms the operation has no precondition tied to endset span count or ordering.

The [EC-MULTISPAN-LINK-DUPLICATION] edge case (Finding 0019) shows that multi-span links can produce *duplicate* spans in endset results. If ordering carried semantic meaning (first = primary), duplicates would require disambiguation, but no such logic exists.

## Summary

Endset membership matters; ordering does not carry defined semantics. The V-sorted order is an implementation artifact of `incontextlistnd` [SS-CONTEXT-LIST] and should not be interpreted as expressing primacy among spans. Any code depending on "first span = primary" would be relying on an undocumented convention not supported by the KB.

---

## Code Exploration

I now have all the evidence needed for a definitive answer. Here it is:

---

## Endset Span Ordering: Semantics in udanax-green

**Short answer: The ordering of I-address spans within an endset carries no semantic meaning. The endset is an unordered set — only membership (the set of I-addresses covered) matters.**

---

### 1. The Three Endsets Are Distinguished by V-Address Range

`setlinkvsas` in `do2.c:169-182` hard-codes the starting V-addresses for the three endsets:

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // from-endset: V starts at 1.1
tumblerincrement (tovsaptr,   0, 2, tovsaptr);    // to-endset:   V starts at 2.1
tumblerincrement (threevsaptr,0, 3, threevsaptr); // three-endset: V starts at 3.1
```

This is what distinguishes FROM from TO from THREE. The distinction is *between* endsets, not *within* them.

---

### 2. Storage: Spans Get Sequential V-Addresses Based on Insertion Order

`insertpm` in `orglinks.c:100-131` iterates through a sporglset and inserts each I-span at the current V-address, then advances it:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);    // line 101
    movetumbler (&lstream, &crumorigin.dsas[I]);            // line 105
    movetumbler (vsaptr,   &crumorigin.dsas[V]);            // line 113
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // line 130
    tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);        // line 131 — advance V-cursor
}
```

The first span in the sporglset gets V-address 1.1, the second gets 1.1+width1, etc. So insertion order does determine *where* each span sits in the permutation matrix. But that V-address assignment is an implementation detail of enfilade storage, not a semantic role.

---

### 3. Retrieval: Order Is Lost — Spans Come Back Ordered by I-Address

`link2sporglset` in `sporgl.c:67-95` retrieves an endset with a single `retrieverestricted` call over the V-range of that endset:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // line 81 — V-range = (whichend, 1)
tumblerincrement (&zero, 0, 1, &vspan.width);          // line 82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {         // line 84
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I); // line 86
        *sporglsetptr = (typesporglset)sporglptr;      // line 87
    }
}
```

`retrieverestricted` traverses the enfilade and returns contexts ordered by the **I-axis** value (enfilade traversal order), not by V-axis insertion order. The retrieved sporglset is therefore ordered by I-address stream value — which may differ from the original insertion sequence. Insertion order is not preserved or recoverable.

---

### 4. Link-Finding Is Purely Set-Based

`sporglset2linksetinrange` in `sporgl.c:250-268` iterates every span in the sporglset, looks up which link addresses overlap it in the spanfilade, and accumulates results. The iteration order is irrelevant — each span contributes its links to the same output set.

`onlinklist` in `spanf2.c:26-44` deduplicates by equality (`tumblereq`) as it builds the result:

```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))  // line 39
        return(0);  // already present — skip
}
```

No position is consulted.

---

### 5. Link Intersection Is Purely Set-Based

`intersectlinksets` in `spanf2.c:96-118` computes intersection with nested loops comparing addresses by value:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq (&temp1->address, &temp2->address)) {  // line 98
            // include in result
        }
    }
}
```

Order within each input set is irrelevant to the result.

---

### 6. The Commented-Out Consolidation Code

`orglinks.c:412-413` and `456-462` contain a commented-out (and incomplete) `consolidatespanset` function:

```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

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

This was never implemented. The system works correctly without normalizing or reordering spans — further evidence that span order has no operational significance.

---

### 7. No Code Treats Any Span as Primary or Indexed

A search across all endset construction and traversal code finds:
- No index-based access (e.g., `sporglset[0]`)
- No guard that checks whether a span is first or last
- No "primary span" flag or convention
- No logic that short-circuits on the first span found

All traversals over a sporglset (endset) are uniform: `for (; sporglset; sporglset = sporglset->next)` iterating every element equivalently.

---

### Conclusion

An endset is architecturally an **unordered set of I-address spans**. The specific ordering that appears during construction (`insertpm`, `orglinks.c:100-131`) is a consequence of linked-list traversal order and determines which V-address each span occupies within the link document — but that assignment is never consulted by any higher-level operation. Upon retrieval, the original insertion order is not preserved; spans come back ordered by I-address value. All link-following (`link2sporglset`), link-finding (`sporglset2linksetinrange`), and intersection (`intersectlinksets`) operations treat the endset as a plain set: only address membership matters.
