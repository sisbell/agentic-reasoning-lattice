## Question 19 [evidence]

> If the queried region covers multiple non-contiguous I-address ranges (from CREATELINK or insert gaps), is one spanfilade search issued per I-span and the matching endsets unioned?

## KB Synthesis

Yes — the spanfilade issues one search per I-span in the sporglset, and the per-span results are accumulated (effectively unioned) before any cross-endpoint intersection.

## Mechanism

**Step 1 — V→I decomposition**

`vspanset2sporglset` (or `specset2sporglset`) walks the queried V-spans through the POOM, producing one sporgl per *contiguous I-address region* [SS-SPORGL]. A queried region that covers content from two INSERT runs separated by a CREATELINK gap [INT-LINK-INSERT] therefore yields two sporgls with disjoint I-address ranges.

**Step 2 — Per-I-span spanfilade searches**

The clearest evidence comes from RETRIEVEENDSETS: `retrieveendsetsfromspanf()` *iterates over the `ispanset` linked list* and calls `retrievesporglsetinrange()` once per `typeispan` struct [SS-RETRIEVE-ENDSETS]. Each call performs a spanfilade search restricted to that individual I-address range in the SPANRANGE dimension.

The same structure governs FINDLINKS: `findlinksfromtothreesp` feeds a sporglset into `sporglset2linkset` / `sporglset2linksetinrange` [EC-FIND-LINKS-GLOBAL], which operates on the per-sporgl unit.

**Step 3 — Union then intersect**

Results from each I-span search are accumulated into a growing link set. After all I-spans of a given endpoint (FROM, TO, or THREE) are processed, `intersectlinksets()` performs the cross-endpoint AND — at O(n·m) or O(n·m·p) complexity — to enforce the requirement that all provided endpoints must match [ST-FIND-LINKS].

## Consequence

A single logical query spanning two non-contiguous I-ranges (e.g., "ABC" at I.1–I.3 and "DEF" at I.2.1–I.2.3 after a CREATELINK gap) issues **two** spanfilade probes, and their matching link sets are **unioned** before any cross-endpoint intersection. A link whose endpoint touches *either* I-range is included in the final candidate set, consistent with the partial-overlap rule: `I-addresses(S) ∩ I-addresses(L.source) ≠ ∅` is satisfied by any overlap across any sub-span [SS-FIND-LINKS].

---

## Code Exploration

Now I have enough to answer precisely. Let me trace the full path.

---

## Answer

**Yes — one spanfilade `retrieverestricted` call is issued per I-span, and results are union-accumulated across all I-spans within each endpoint set.** Here is the exact call chain, with line citations.

---

### Step 1: V-spec → sporgl list (one I-span per sporgl)

When a query carries a V-spec (virtual address specification), the entry point is `specset2sporglset` [`sporgl.c:14`], which calls `vspanset2sporglset` [`sporgl.c:35`] for each vspec item:

```c
// sporgl.c:47-58
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc (taskptr, sizeof(typesporgl));
        ...
        movetumbler(&ispanset->stream,&sporglset->sporglorigin);
        movetumbler (&ispanset->width, &sporglset->sporglwidth);
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
    }
}
```

`vspanset2ispanset` → `permute` [`orglinks.c:404`]:

```c
// orglinks.c:414-416
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, ...);
}
```

`span2spanset` [`orglinks.c:425`] calls `retrieverestricted` **once per V-span** against the POOM (permutation matrix):

```c
// orglinks.c:435
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```

The resulting I-spans are **appended** to `targspansetptr` (union, not replacement). So if a single V-span maps to two disjoint I-ranges (due to gaps from inserts or multiple transclusion sources), those become two separate `typeispan` entries in the list, and therefore two separate sporgls after `vspanset2sporglset`.

---

### Step 2: Sporgl list → spanfilade searches (one per I-span)

For link-finding, `findlinksfromtothreesp` [`spanf1.c:56`] calls:

```c
// spanf1.c:77
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

`sporglset2linkset` [`sporgl.c:222`] passes the whole sporgl list into `sporglset2linksetinrange` [`sporgl.c:239`], which loops:

```c
// sporgl.c:250-268
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                                  &range, ORGLRANGE, (typeisa*)infoptr);
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);
        onlinklist (taskptr, linksetptr, &linksa);
    }
    contextfree (context);
}
```

**One `retrieverestricted` call per sporgl (I-span).** Each call searches the spanfilade for links whose stored I-span overlaps the queried I-span. Matching link addresses are accumulated onto `linksetptr` via `onlinklist` — a **union** across all I-spans.

The same per-I-span loop appears in `retrievesporglsetinrange` [`spanf1.c:244`], used by `retrieveendsetsfromspanf`:

```c
// spanf1.c:244-265
for (; sporglptr; sporglptr = (typesporglset)sporglptr->xxxxsporgl.next) {
    context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                                  whichspace, ORGLRANGE, (typeisa*)NULL);
    for (c = context; c;) {
        ...
        *sporglsetptr = (typesporglset)sporglset;
        sporglsetptr = (typesporglset *)&sporglset->next;
        ...
    }
    contextfree(context);
}
```

Again: one spanfilade search per I-span; results appended (unioned).

---

### Step 3: Across endpoint sets — intersection, not union

After the per-I-span union is collected for each endpoint class, `findlinksfromtothreesp` [`spanf1.c:100`] intersects across endpoint classes (from / to / three):

```c
// spanf1.c:100
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

So the final result is:

> **(union over I-spans within each endpoint) ∩ (across from/to/three endpoints)**

---

### Summary

| Layer | Loop construct | Call | Accumulation |
|---|---|---|---|
| POOM V→I | `permute` [`orglinks.c:414`] one call per V-span | `retrieverestricted` on orgl | union into I-span list |
| Sporgl build | `vspanset2sporglset` [`sporgl.c:47`] one sporgl per I-span | — | append |
| Spanfilade search | `sporglset2linksetinrange` [`sporgl.c:250`] one call per sporgl | `retrieverestricted` on spanf | union via `onlinklist` |
| Endpoint combine | `findlinksfromtothreesp` [`spanf1.c:100`] | `intersectlinksets` | **intersection** across from/to/three |

There is no batching or single-shot range query across multiple non-contiguous I-spans. The code issues one `retrieverestricted` per I-span and unions the results within each endpoint class.
