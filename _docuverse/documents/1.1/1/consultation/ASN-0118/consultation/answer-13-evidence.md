## Question 13 [evidence]

> When a copied V-span maps to non-contiguous I-addresses in the source, does vspanset2sporglset automatically split it into multiple sporgls without front-end pre-splitting?

## KB Synthesis

Yes, the splitting is automatic. The front end does not need to pre-split.

When `vspanset2sporglset` receives a V-span, it calls `vspanset2ispanset` → `permute` → `span2spanset` → `retrieverestricted`, which walks the POOM and discovers all contiguous I-address regions covered by that V-span. The inner loop at `sporgl.c:49-58` creates one sporgl per returned `typeispan` struct. So a single contiguous V-span over content transcluded from two sources ("AA" from doc A, "BB" from doc B) produces two sporgls in the output — one for each source's I-address region. [ST-LINK-CREATE, Finding 0037]

This applies to link creation (`domakelink`) and anywhere else the sporgl conversion chain is invoked. The postcondition is: `|output_sporgls| >= |input_vspans|`, with cardinality determined by the I-address fragmentation of the content, not the V-span count. [SS-LINK-ENDPOINT, Finding 0037]

The concrete example from the KB:

```
Document C: "AABB" where "AA"→doc A I-addresses, "BB"→doc B I-addresses
Input:  1 V-span covering all of "AABB"
Output: 2 sporgls (one per contiguous I-region)
```

---

## Code Exploration

I now have all the code needed. Let me trace the complete execution path and write the answer.

---

## Answer: V-span to Non-contiguous I-spans — Auto-splitting in `vspanset2sporglset`

**Yes.** `vspanset2sporglset` automatically splits a V-span that maps to non-contiguous I-addresses into multiple sporgls. No front-end pre-splitting is needed or performed. Here is the full trace.

---

### Call Chain

```
vspanset2sporglset  (sporgl.c:35)
  └─ vspanset2ispanset  (orglinks.c:397)
       └─ permute  (orglinks.c:404)
            └─ span2spanset  (orglinks.c:425)
                 └─ retrieverestricted  (retrie.c:56)
                      └─ retrieveinarea  (retrie.c:87)
                           └─ findcbcinarea2d  (retrie.c:229)   ← splits here
```

---

### Step 1 — `vspanset2sporglset` (sporgl.c:47–58)

```c
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {      /* one sporgl per ispan */
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        movetumbler (docisa, &sporglset->sporgladdress);
        movetumbler(&ispanset->stream, &sporglset->sporglorigin);
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        ...
    }
}
```

The outer loop iterates over input V-spans. The inner loop at `sporgl.c:49` walks every ispan that `vspanset2ispanset` returns and emits one sporgl per ispan. So if `vspanset2ispanset` returns three ispans from a single V-span, three sporgls are emitted.

---

### Step 2 — `vspanset2ispanset` → `permute` (orglinks.c:397–422)

```c
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  /* orglinks.c:401 */
}
```

`permute` (orglinks.c:414–416) iterates the restriction span-set and calls `span2spanset` for each element, accumulating results in a running `targspansetptr`:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
```

---

### Step 3 — `span2spanset` produces one ispan per matching crum (orglinks.c:435–453)

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                              restrictionindex, (typespan*)NULL,
                              targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                      (typeitemset*)targspansetptr);
}
```

The loop at `orglinks.c:439` iterates over every context item returned by `retrieverestricted`, converting each to an ispan. If the V-span hits `N` distinct I-space regions, `context` has `N` entries and `N` ispans are appended.

---

### Step 4 — The split happens in `findcbcinarea2d` (retrie.c:229–268)

This is where physical splitting occurs. The function recursively traverses the POOM enfilade tree:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr,
                          span1start, span1end, index1,
                          span2start, span2end, index2, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);  /* recurse */
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   /* retrie.c:263 — emit one context */
    }
}
```

Each bottom crum represents one contiguous (V-start, V-width) ↔ (I-start, I-width) mapping segment. `crumqualifies2d` (retrie.c:270–305) tests whether the V-extent of a crum intersects `[span1start, span1end)`. Every qualifying bottom crum — regardless of how its I-address relates to any other qualifying crum — is emitted independently via `incontextlistnd`.

When a V-span has been built from non-contiguous I-material (e.g., a document that assembled text from two separate I-streams), the POOM contains separate bottom crums for each I-region. All of them qualify the V-space check, so all appear in the returned context list. Their I-origins are non-contiguous by construction.

---

### Step 5 — `crumqualifies2d` imposes no I-contiguity requirement (retrie.c:282–300)

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT
       : whereoncrum (crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) { return(FALSE); }
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if (startcmp > THRUME) { return(FALSE); }
```

`index1` is `V` (the restriction axis). The I-axis (`index2`) qualification at retrie.c:292–300 is unrestricted when `span2ptr` is NULL (which `span2spanset` passes: `(typespan*)NULL` at orglinks.c:435). So any bottom crum whose V-extent overlaps the query passes, with no I-contiguity constraint.

---

### Summary of the Splitting Mechanism

| Layer | File | What happens |
|---|---|---|
| `findcbcinarea2d` | retrie.c:252–264 | Walks all enfilade bottom crums; each qualifying crum becomes one context item |
| `span2spanset` | orglinks.c:439–445 | One ispan per context item — non-contiguous I-regions produce separate ispans |
| `permute` | orglinks.c:414–416 | Accumulates ispans across all input V-spans |
| `vspanset2sporglset` | sporgl.c:49–57 | One sporgl per ispan — the final split product |

**`vspanset2sporglset` does no splitting itself.** The splitting is a natural consequence of the enfilade traversal in `findcbcinarea2d`: the POOM stores mappings as atomic (V-segment ↔ I-segment) crums, and a V-query spanning multiple such crums returns one context per crum. Each context becomes one ispan, and each ispan becomes one sporgl. The front-end passes a single vspan; it receives back a sporgl-set of however many contiguous I-runs that vspan covers.
