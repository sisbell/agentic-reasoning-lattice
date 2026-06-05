## Question 12 [evidence]

> What overlap relation must a returned endset's I-span bear to the queried region's I-span — full containment, partial overlap, or any non-empty intersection?

## KB Synthesis

**Any non-empty intersection** — a single shared I-address is sufficient.

[SS-FIND-LINKS] (Finding 0028) states this explicitly: "The search is purely set-intersection on I-addresses: `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`." The concrete example confirms partial overlap suffices — searching with I-addresses {I.5, I.6} discovers a link whose source spans {I.4, I.5, I.6}. The queried region need not contain the full endpoint span, nor need the endpoint span contain the query region.

[SS-RETRIEVE-ENDSETS] (Finding 0035) uses the same underlying mechanism: `retrievesporglsetinrange()` searches the spanfilade with SPANRANGE and ORGLRANGE restrictions, applying the same I-address intersection logic. There is no containment requirement at this layer either.

[INT-SPORGL-LINK-INDEX] confirms both operations share the same spanfilade search path, so the overlap semantics are identical: `∃ i : i ∈ query_iaddrs ∧ i ∈ endpoint_iaddrs` is the sole condition for inclusion.

---

## Code Exploration

Now I have everything needed for a precise, fully cited answer.

---

## Answer: Overlap Relation for Returned Endsets

**The relation is: any non-empty strict intersection.**

A returned endset's I-span must overlap the queried region's I-span by at least one point (exclusive endpoints). Neither full containment nor query-containment of the endset is required.

---

### Call Chain

The endset-retrieval path is:

1. `fns.c:350` → `doretrieveendsets` (`do1.c:369`) → `retrieveendsetsfromspanf`
2. Inside spanfilade retrieval: `sporglset2linksetinrange` (`sporgl.c:239`) calls `retrieverestricted` (`retrie.c:56`) with the query sporgl cast as `(typespan*)sporglset` for the `SPANRANGE` dimension.
3. `retrieverestricted` (`retrie.c:83`) calls `retrieveinarea` (`retrie.c:87`), which dispatches to `findcbcinarea2d` (`retrie.c:97`).
4. `findcbcinarea2d` (`retrie.c:252–253`) calls `crumqualifies2d` on each candidate crum.

---

### The Overlap Predicate: `crumqualifies2d`

The decision function at `retrie.c:270–305`:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
    tumbler *span1start, tumbler *span1end, INT index1, ...)
{
    // span1 = the query I-span [span1start, span1end)
    // crumptr = candidate endset node

    endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <=/*=*/ ONMYLEFTBORDER)   // retrie.c:283
        return(FALSE);                    // query_end ≤ endset_start → no overlap

    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME)               // retrie.c:287
        return(FALSE);                   // query_start ≥ endset_end → no overlap

    return(TRUE);
```

---

### Position Constants (`common.h:86–90`)

```c
#define TOMYLEFT       -2   // address <  crum_start
#define ONMYLEFTBORDER -1   // address == crum_start
#define THRUME          0   // crum_start < address < crum_end
#define ONMYRIGHTBORDER 1   // address == crum_end
#define TOMYRIGHT       2   // address >  crum_end
```

`whereoncrum` returns where `address` falls **relative to the crum's interval** `[crum_start, crum_end)` (`retrie.c:345–398`).

---

### Predicate Decoded

| Rejection condition | Meaning | Geometrically |
|---|---|---|
| `endcmp <= ONMYLEFTBORDER` | query_end ≤ endset_start | query is entirely left of endset |
| `startcmp > THRUME` | query_start ≥ endset_end | query is entirely right of endset |

Acceptance = neither rejection fires:

> **`query_start < endset_end`  AND  `query_end > endset_start`**

This is the standard **half-open interval intersection** predicate. Touching at endpoints alone (query_end == endset_start, or query_start == endset_end) is explicitly rejected.

---

### Confirmed in the 1D Case

`crumintersectsspanseq` (`retrie.c:423–430`) handles granfilade retrieval with identical semantics:

```c
bool crumintersectsspanseq(typecorecrum *crumptr, tumbler *offsetptr,
    tumbler *spanstart, tumbler *spanend)
{
    if (iszerotumbler(&crumptr->cwid.dsas[WIDTH]))
        return(FALSE);              // zero-width crum never qualifies
    return (
        whereoncrum(crumptr, (typewid*)offsetptr, spanstart, WIDTH) < ONMYRIGHTBORDER
     && whereoncrum(crumptr, (typewid*)offsetptr, spanend, WIDTH) >/*=*/ ONMYLEFTBORDER);
}
```

Translates to: `query_start < endset_end AND query_end > endset_start` — identical predicate.

---

### Additional Guard: Zero-Width Crums

`crumintersectsspanseq` (`retrie.c:425–427`) explicitly rejects any crum with zero width (`iszerotumbler` check). The 2D function relies on the enfilade invariant that no zero-width nodes exist at interior levels.

---

### Summary

The overlap relation is **any non-empty strict intersection** of half-open intervals. An endset is returned if and only if its I-span `[endset_start, endset_end)` and the query region `[query_start, query_end)` share at least one point — i.e., `query_start < endset_end AND query_end > endset_start`. Full containment in either direction is not required; neither is any minimum amount of overlap beyond a single point.
