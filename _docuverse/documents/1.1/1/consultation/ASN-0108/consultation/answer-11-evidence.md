## Question 11 [evidence]

> When FINDNEXTNLINKSFROMTOTHREE returns a window of links, what determines the order of links within that window — spanfilade I-address span ordering, link orgl I-address, or the insertion-sort by V-address in `incontextlistnd`?

## KB Synthesis

## Link Window Ordering in FINDNEXTNLINKSFROMTOTHREE

The ordering is determined by **I-address (SPANRANGE) ordering** from the spanfilade traversal — not by link orgl I-address, and not by the V-address insertion-sort of `incontextlistnd`.

### Why

**The spanfilade is a 2D SPAN enfilade** [SS-DUAL-ENFILADE]. 2D enfilades use `incontextlistnd()` during retrieval, which performs insertion-sort by the *left boundary in the queried dimension* [SS-CONTEXT-LIST], [INV-RETRIEVAL-V-SORTED]. For FINDLINKSFROMTOTHREE, the queried dimension is SPANRANGE (the I-address content dimension). The ORGLRANGE filter is effectively disabled by the `TRUE||!homeset` guard in `sporglset2linkset` [EC-FIND-LINKS-GLOBAL].

So the full result list from `findlinksfromtothreesp()` — which FINDNEXTNLINKSFROMTOTHREE re-executes on every call [SS-PAGINATE-LINKS] — is sorted by the I-address of the content that matched each link's endpoint.

**The cursor walk** then linearly scans this I-address-ordered list for an exact link-ISA tumbler match, returning N items after it [SS-PAGINATE-LINKS]. The cursor is a link ISA tumbler, not an I-address — so cursor position is stable only as long as that link remains in the result set.

### Gap

The KB does not explicitly document the output ordering of `intersectlinksets()` (which combines from/to/three sub-results at `spanf2.c:46-120`). The I-address-ordered claim applies to each sub-result list, but whether the intersection preserves that ordering or produces a different ordering is unresolvable from the KB alone.

### Summary

Within the window: **I-address (SPANRANGE left boundary) order**, inherited from `incontextlistnd()` sorting during 2D spanfilade traversal. V-address sorting from `incontextlistnd` is the POOM's mechanism for content retrieval — it is not operative here because link search never touches the POOM.

---

## Code Exploration

The key constants are confirmed: `ORGLRANGE=0`, `SPANRANGE=1` (`wisp.h:15-16`), and `retrieverestricted` is called with `SPANRANGE` as `index1` and `ORGLRANGE` as `index2` (`sporgl.c:259`).

---

## What Determines Link Order in FINDNEXTNLINKSFROMTOTHREE

**Answer: option (c) — the insertion-sort by V-address in `incontextlistnd` — determines the order.** The spanfilade I-address traversal order and the link orgl I-address are both irrelevant to the final ordering.

Here is the complete traced call chain with citations:

---

### Call Chain

**`fns.c:229-231`** — handler calls `dofindnextnlinksfromtothree`, then paginate via `lastlink`:
```c
getfindnextnlinksfromtothree(..., &lastlink, &n)
&& dofindnextnlinksfromtothree(taskptr, from, to, three, homeset, &lastlink, &nextlinkset, &n)
putfindnextnlinksfromtothree(taskptr, n, nextlinkset);
```

**`do1.c:362-366`** — `dofindnextnlinksfromtothree` is a thin wrapper:
```c
return findnextnlinksfromtothreesp(taskptr, ..., lastlinkisaptr, nextlinksetptr, nptr);
```

**`spanf1.c:124`** — `findnextnlinksfromtothreesp` calls the underlying full-fetch:
```c
findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, &linkset)
```
It then does a linear scan of the result list to find `lastlink`, and truncates to `n` items. **The order is set before this function sees the list.**

**`spanf1.c:77,85,93`** — `findlinksfromtothreesp` calls `sporglset2linkset` three times (once per vspecset endpoint), then `intersectlinksets` at `spanf1.c:100`. The intersection walks the sorted from-set and filters against to/three sets, preserving the from-set's order.

**`sporgl.c:259`** — `sporglset2linksetinrange` calls `retrieverestricted` with:
```c
retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...)
//                                                  ^index1              ^index2
```
`index1 = SPANRANGE = 1`, `index2 = ORGLRANGE = 0` (from `wisp.h:15-16`).

**`retrie.c:263`** — `findcbcinarea2d` (the recursive spanfilade tree walker) inserts each found bottom crum into the context list:
```c
incontextlistnd(headptr, context, index1);   // index1 = SPANRANGE
```
Even though the tree is walked sibling-by-sibling (`getrightbro()`) in enfilade structural order, **each result is sorted into position**, not appended.

---

### The Sort: `incontextlistnd` (`context.c:75-111`)

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd(c, &grasp, (typedsp*)NULL);   // line 80: compute V-address
    ...
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {  // line 90: insert before
        c->nextcontext = clist;
        *clistptr = c;
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {           // line 96: scan for position
            if ((whereoncontext(clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext(nextc, ...) < ONMYLEFTBORDER)) {     // lines 98-99: insert in middle
                c->nextcontext = nextc;
                clist->nextcontext = c;
            }
        }
    }
    clist->nextcontext = c;  // line 110: or append at end
}
```

The sort key is `grasp.dsas[index]` where `index = SPANRANGE = 1`. `grasp` is the context's total V-address offset computed by `prologuecontextnd`. So the list is maintained in ascending V-address order of each link's matched span endpoint — not I-address order, not orgl I-address order.

`whereoncontext` (`context.c:124`) computes `left = totaloffset.dsas[SPANRANGE]` and `right = left + contextwid.dsas[SPANRANGE]` for each existing context and calls `intervalcmp` against the new context's address. This is a pure tumbler (V-address) comparison.

---

### Why I-Address Traversal Order Is Irrelevant

The spanfilade tree (`findcbcinarea2d`, `retrie.c:229`) iterates siblings via `getrightbro` and descends recursively. This traversal happens in I-address (enfilade structural) order. But every bottom-level crum found is passed to `incontextlistnd`, which **discards the arrival order** and re-sorts by V-address. Structural traversal order is completely overwritten by the insertion sort.

### Why Orgl I-Address Is Irrelevant

`ORGLRANGE = 0` is `index2`, not `index1`. `incontextlistnd` is called with `index1 = SPANRANGE = 1`. The orgl I-address dimension is used only to **filter** which crums qualify (via `crumqualifies2d`), not to sort the results.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Spanfilade I-address traversal order? | No | `incontextlistnd` re-sorts, discarding arrival order (`retrie.c:263`, `context.c:75-111`) |
| Link orgl I-address? | No | Sort key is `dsas[SPANRANGE]`, not `dsas[ORGLRANGE]` (`context.c:90`; `wisp.h:15-16`) |
| V-address insertion-sort in `incontextlistnd`? | **Yes** | `context.c:90,98-99`: insertion sort on `grasp.dsas[SPANRANGE]` = V-address of matched span endpoint |

Links within the window returned by `FINDNEXTNLINKSFROMTOTHREE` are ordered by the **V-address of the matched span endpoint** (ascending tumbler order), established by the insertion-sort in `incontextlistnd` at `retrie.c:263` with `index = SPANRANGE`. The enfilade structural (I-address) traversal order and orgl I-address play no role in the final ordering.
