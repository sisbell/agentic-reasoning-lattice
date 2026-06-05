## Question 14 [evidence]

> If the requested endset references content across multiple non-contiguous I-address ranges (a split endset from CREATELINK's automatic sporgl splitting), does the returned spec-set preserve all those spans as separate VSpecs?

## KB Synthesis

Yes. The returned spec-set preserves all spans as separate VSpecs, with one VSpec per resolvable contiguous I-address region. Here is the full chain:

---

**At creation time: single V-span → multiple sporgls**

`vspanset2sporglset` iterates over every I-span returned by `vspanset2ispanset` and produces a separate sporgl for each contiguous I-address region [ST-LINK-CREATE/Finding 0037]. So a V-span covering transcluded content from two sources produces two sporgls in the endset, not one.

> "one V-span input may produce multiple I-span entries in the link endset. `|link.source_endset| >= |input_vspans|`" — [SS-LINK-ENDPOINT/Finding 0037]

---

**At retrieval time: multiple sporgls → multiple VSpecs**

FOLLOWLINK calls `link2sporglset()` to extract all sporgls from the endset position, then passes the entire sporglset to `linksporglset2specset()`, which calls `span2spanset()` independently for each sporgl [SS-FOLLOWLINK/Finding 0048]. Each resolving I-span contributes one VSpec to the output specset. Unresolvable I-spans (no current POOM mapping) are silently dropped [INV-ITOV-FILTERING].

RETRIEVEENDSETS uses the same `linksporglset2specset()` conversion path [SS-RETRIEVE-ENDSETS/Finding 0035].

> "retrieve_endsets reports multiple V-spans corresponding to the stored I-spans, one per contiguous I-region" — [SS-LINK-ENDPOINT/Finding 0037]

---

**Caveats**

1. **Silent filtering**: If some sporgls in the endset have I-addresses unreferenced in the queried document's POOM (deleted or never present), those sporgls are dropped — the returned specset may have *fewer* VSpecs than the stored endset has sporgls [INV-ITOV-FILTERING/Finding 0048].

2. **Duplicate spans**: Multi-span link creation can produce duplicate VSpecs in the returned endset — `retrieve_endsets` may return the same V-position more than once [EC-MULTISPAN-LINK-DUPLICATION/Finding 0019].

3. **POOM multimap amplification**: Because the POOM is a multimap [SS-POOM-MULTIMAP/Finding 0039], a single I-span can resolve to *multiple* V-positions if the content was internally transcluded. This can produce more VSpecs than there are sporgls in the endset.

4. **Result ordering**: Whatever VSpecs are returned are sorted by V-address via `incontextlistnd()` insertion-sort [INV-RETRIEVAL-V-SORTED/Finding 0078].

---

## Code Exploration

I now have all the actual source needed to answer definitively.

---

## Answer: Does FOLLOW preserve split endset spans as separate VSpecs?

**Short answer:** No — they return as **one VSpec with multiple VSpans**, not as separate VSpec items.

---

## Full Code Trace

### Phase 1: CREATELINK stores the endset

**`fns.c:100-112`** — `createlink` calls `docreatelink`.

**`do1.c:195-221`** — `docreatelink` converts each specset to a sporglset:

```c
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)   /* do1.c:215 */
&& insertendsetsinorgl (...)                                               /* do1.c:218 */
```

**`sporgl.c:14-33`** — `specset2sporglset` iterates each spec, calling `vspanset2sporglset` for VSPECID items.

**`sporgl.c:35-65`** — `vspanset2sporglset` is where splitting happens. For each vspan, it calls `vspanset2ispanset` (V→I), then creates one sporgl per resulting I-span:

```c
for (; vspanset; vspanset = vspanset->next) {                          /* sporgl.c:47 */
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        sporglset->itemid = SPORGLID;
        movetumbler (docisa, &sporglset->sporgladdress);                /* same docisa for ALL */
        movetumbler(&ispanset->stream,&sporglset->sporglorigin);
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

**Critical:** every sporgl for content from the same document gets the **identical `sporgladdress`** (= docisa). Multiple non-contiguous I-ranges → multiple sporgls, all sharing the same address.

---

### Phase 2: FOLLOW retrieves the endset

**`fns.c:114-127`** → **`do1.c:223-232`** — `dofollowlink`:

```c
return (
   link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                          sporglset, specsetptr, NOBERTREQUIRED));    /* do1.c:229-230 */
```

Note: `homedoc` passed to `linksporglset2specset` is the **first sporgl's `sporgladdress`** — the document ISA.

**`sporgl.c:67-95`** — `link2sporglset` retrieves stored I-spans via `retrieverestricted`, creating one sporgl per context (one per stored non-contiguous range).

---

### Phase 3: Converting sporgls back to specset — the grouping point

**`sporgl.c:97-123`** — `linksporglset2specset` outer loop:

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    specset = (typespecset) taskalloc (taskptr, sizeof (typevspec));
    ...
    linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type); /* &sporglset passed by reference */
    ...
    *specsetptr = specset;
    specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
}
```

**`sporgl.c:127-137`** — `linksporglset2vspec` creates one VSpec, then calls `sporglset2vspanset`.

**`sporgl.c:141-176`** — `sporglset2vspanset` — **this is the key grouping function**:

```c
sporglptr = (typesporgl *)*sporglsetptr;
// process first sporgl → convert its I-span to V-span(s)
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
for (;;) {
    sporglptr = sporglptr->next;
    if (
       !sporglptr
    || !(sporglptr->itemid == SPORGLID)
    || !tumblereq (&((typesporgl *)sporglptr)->sporgladdress,          /* sporgl.c:163 */
                   &((typesporgl *)(*sporglsetptr))->sporgladdress))   /* stop if address changes */
        return(0);
    *sporglsetptr = (typesporglset)sporglptr;                          /* ADVANCE outer-loop cursor */
    // process this sporgl too → add more V-spans to same vspanset
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr); /* sporgl.c:174 */
}
```

Because all sporgls from the same document share the same `sporgladdress`, `tumblereq` at **`sporgl.c:163`** is always true, and the inner loop **consumes ALL of them**, adding each I-span's V-span(s) to the same VSpec's `vspanset`. When the inner loop exits (end of list), `*sporglsetptr` points to the last consumed sporgl; the outer loop's `.next` then hits NULL, ending iteration.

**Result: one VSpec is created, with multiple VSpans appended to its vspanset.**

---

### Phase 4: V-span preservation — no merging

**`orglinks.c:389-394`** — `ispan2vspanset` calls `permute(... I, vspansetptr, V)`.

**`orglinks.c:404-422`** — `permute` iterates restriction spans and calls `span2spanset` per span. Note explicitly commented-out consolidation:

```c
/*consolidatespans(restrictionspanset);   /* orglinks.c:412-413 — DISABLED */
```

**`orglinks.c:425-454`** — `span2spanset` calls `retrieverestricted`, then for each returned context:

```c
for (c = context; c; c = c->nextcontext) {        /* orglinks.c:439 */
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

**`orglinks.c:464-537`** — `onitemlist` allocates a new item and appends it to the tail of the list — **no merging, no deduplication**. Each context produces exactly one separate VSpan in the result.

---

## Conclusion

When CREATELINK's sporgl splitting produces sporgls referencing multiple non-contiguous I-address ranges **within the same document**, FOLLOW returns:

- **One VSpec** (because `sporglset2vspanset` at `sporgl.c:158-175` groups all sporgls sharing the same `sporgladdress` into a single VSpec)
- With **multiple VSpans** in that VSpec's `vspanset` — one per non-contiguous range, preserved individually (no merging, consolidation explicitly disabled at `orglinks.c:412-413`)

The spec-set does **not** produce separate VSpec items per I-range. All spans appear as sibling VSpans within one VSpec. The only scenario producing multiple VSpecs would be an endset spanning content from **different documents** (different `sporgladdress` values), which causes `sporglset2vspanset` to stop at `sporgl.c:163` and the outer loop to allocate a fresh VSpec for the next group.
