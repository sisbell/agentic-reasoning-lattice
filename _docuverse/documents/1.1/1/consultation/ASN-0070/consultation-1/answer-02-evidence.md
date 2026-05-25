## Question 2 [evidence]

> Does the udanax-green follow-equivalent operation normalize its result to a canonical span-set form, or return whatever decomposition the computation produces?

## KB Synthesis

The operation returns whatever decomposition the computation produces — there is no normalization to a canonical span-set form.

**The conversion pipeline** [SS-FOLLOWLINK] is: link orgl I-addresses → `link2sporglset()` → `linksporglset2specset()` → `span2spanset()` via `retrieverestricted()` against the queried document's POOM. Each stored I-span in the endset produces a separate V-span in the result; no consolidation or deduplication step exists in this path.

**Empirical evidence of non-normalization:**

- [EC-PIVOT-LINK-FRAGMENTATION]: After rearranging linked content with a pivot, `retrieve_endsets` reports **four spans** for what was originally a single linked region, with the same link appearing twice in `find_links` results. The endset reports `1.2 width 0.1` twice and `1.5 width 0.1` twice.
- [EC-MULTISPAN-LINK-DUPLICATION]: Creating a link with multiple source spans can produce duplicate spans in `retrieve_endsets` output (e.g., `1.16` appears twice among 3 returned spans).

**Structural reason:** [SS-LINK-ENDPOINT] (Finding 0037) explains that an endset is internally a `set<Sporgl>`, where each sporgl is one contiguous I-address run. A single user-visible V-span over transcluded content from multiple sources decomposes into multiple sporgls at creation time. On retrieval, each sporgl independently maps back to a V-span via the POOM, with no merging of adjacent or equal results.

**Contrast with document V-spans:** [INV-VSPAN-CONSOLIDATION] applies to `retrieve_vspanset` (the POOM's natural coalescing of contiguous crums during insert), but this consolidation operates at the enfilade level, not in the sporgl-to-specset conversion path used by endset retrieval.

The result cardinality is `|result| ≥ |stored_sporgls|`, potentially greater due to duplication artifacts.

---

## Code Exploration

I now have everything I need. Here is my full answer:

---

## Does `dofollow` Normalize Its Result?

**No. The follow-equivalent operation returns the raw computation output — whatever decomposition the enfilade traversal produces — without any normalization.**

---

### Full Call Chain

```
fns.c:followlink
  → do1.c:dofollowlink
    → sporgl.c:link2sporglset
    → sporgl.c:linksporglset2specset
      → sporgl.c:linksporglset2vspec
        → sporgl.c:sporglset2vspanset
          → orglinks.c:ispan2vspanset
            → orglinks.c:permute
              → orglinks.c:span2spanset   ← KEY: appends, does not normalize
```

**`dofollowlink`** (backend/do1.c:223-232) takes two steps: extract sporgls from the link ISA, then convert to a specset. There is no normalization pass before or after either step.

---

### The Critical Junction: `span2spanset`

```c
/* backend/orglinks.c:435-444 */
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);
}
```

`retrieverestricted()` walks the enfilade and yields contexts in tree-traversal order. For each context, `context2span()` converts it to a span, and **`onitemlist()`** (backend/orglinks.c:464) appends it to the result list. That append is purely structural — no sorting, no merging, no deduplication.

---

### The Normalization Machinery Exists But Is Bypassed

Two mechanisms exist that *would* normalize the result, but neither is active in the dofollow path:

**1. `putvspaninlist`** (backend/orglinks.c:329-387) — a fully functional sorted-insert-with-merge routine. It maintains sorted order and merges adjacent/overlapping spans (lines 346–386). It is called from `retrievevspansetpm()` (lines 189, 216, 217) for PM content retrieval, and from a dead `#ifdef UnDEFined` block (line 289). It is **not** called from `span2spanset`.

**2. `consolidatespans`** — commented out directly in `permute()`, which is the I→V conversion function on the dofollow path:

```c
/* backend/orglinks.c:412-413 */
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */
```

There is also a stub of a `consolidatespanset()` function (backend/orglinks.c:456-462) that was never completed:

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

Both normalization paths were written, then commented out or left dead. The active code path through `span2spanset` → `onitemlist` was left as a raw append.

---

### Output Stage

`putfollowlink` (backend/putfe.c:339-343) simply calls `putitemset()` on the raw specset:

```c
int putfollowlink(typetask *taskptr, typespecset specset) {
    putnumber(taskptr->outp, FOLLOWLINK);
    putitemset(taskptr, (typeitemset)specset);
}
```

No normalization at the serialization stage either.

---

### Summary

| Property | Actual Behavior |
|---|---|
| Sorted by span position | No — enfilade traversal order |
| Adjacent spans merged | No — `putvspaninlist` not called |
| Overlapping spans merged | No |
| Duplicates removed | No |
| Deterministic | Yes — same data structure, same traversal order |
| Canonical | No — result depends on internal tree decomposition |

The normalization machinery (`putvspaninlist` with its full merge logic, `consolidatespans`) exists in the source but was explicitly commented out of the active `permute()` code path. The dofollow result is deterministic given a fixed enfilade state, but it is not canonical — two logically equivalent span sets stored differently in the enfilade would produce different output decompositions.
