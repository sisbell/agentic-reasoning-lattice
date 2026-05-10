## Question 10 [gregory]

> Is the intersection of two overlapping tumbler spans always representable as a single span, or can hierarchical boundary crossings produce a result that requires multiple spans?

## KB Synthesis

The intersection of two overlapping tumbler spans is **always representable as a single span** in the mathematical sense, but **hierarchical boundary crossings can make that single span semantically degenerate**, requiring callers to split it for correct content access.

## Why the Intersection Is Always a Single Span

Tumblers form a total order per [INV-TUMBLER-TOTAL-ORDER]: `tumblercmp` is total, antisymmetric, and transitive, with lexicographic digit comparison after exponent alignment. Because the ordering is total and dense, any two overlapping half-open intervals `[a, b)` and `[c, d)` have intersection `[max(a,c), min(b,d))` — a single contiguous interval with no gaps.

The five-way `intervalcmp` predicate ([SS-INTERVAL-CMP]) treats the interval as a simple convex set in this total order: TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT. There is no concept of internal discontinuity at the level of the ordering relation itself.

Crucially, the `.0.` separators in docuverse addresses are **semantic convention, not structural enforcement** ([SS-TUMBLER] Finding 0001): "The zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." The address `1.1.0.2.0.5` and the address `1.1.0.3.0.1` are just two tumblers with a well-defined ordering relationship. Nothing in `tumblercmp` skips over `.0.` boundaries.

## Where Hierarchical Crossings Cause Practical Problems

While the intersection is mathematically one span, crossing a `.0.` boundary produces a span that is **semantically non-contiguous**. The critical case is the subspace boundary between `1.x` (text) and `2.x` (links):

- `RETRIEVEDOCVSPAN` returns a single bounding span like `1.1 for 1.2` for a document with both text and links — this span is mathematically valid but semantically degenerate, spanning two distinct content types with a semantic gap between them ([EC-VSPAN-MISLEADING-SIZE], [SS-VSPAN-VS-VSPANSET])
- When `compare_versions` receives a specset that includes the link subspace, the V-to-I conversion produces link orgl ISAs and permascroll addresses — address types in different spaces that will never intersect, causing the correspond.c loop to crash ([EC-COMPARE-VERSIONS-LINK-CRASH], [PRE-COMPARE-VERSIONS])
- `RETRIEVEDOCVSPANSET` exists precisely because a single bounding span is insufficient — it returns separate spans per subspace ([SS-VSPAN-VS-VSPANSET] Finding 0035)

The subspace isolation mechanism for INSERT ([SS-TWO-BLADE-KNIFE]) tells the same story from the other direction: `findaddressofsecondcutforinsert()` deliberately places the second knife blade at `(N+1).1` to keep shifts within one subspace. If the intersection of a shift region with the occupied space could naturally span subspaces, this explicit boundary would be unnecessary.

## Summary

| Property | Value |
|----------|-------|
| Mathematical intersection | Always a single span (total order, no gaps) |
| Span width computation | `tumblersub(min_end, max_start)` — well-defined |
| Hierarchical boundary crossings | Produce a single span that may be *semantically* degenerate |
| Caller responsibility | Must split at subspace boundaries before content access (per [SS-VSPAN-VS-VSPANSET], [PRE-COMPARE-VERSIONS]) |

The system's design acknowledges this by providing `RETRIEVEDOCVSPANSET` (returns multiple spans, one per subspace) alongside `RETRIEVEDOCVSPAN` (returns the raw bounding span), and by requiring that operations like `compare_versions` and `retrieve_contents` receive text-subspace-only specsets as a precondition.

---

## Code Exploration

Now I have all the source evidence I need. Let me compile the answer.

---

## Answer

**The intersection of two overlapping tumbler spans is always representable as a single span.** Hierarchical boundary crossings cannot fragment it into multiple spans. Here is the complete code-traced reasoning.

---

### 1. What a tumbler span is

A span is defined in `xanadu.h:65-71`:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid      itemid;
    tumbler stream;   /* start address */
    tumbler width;    /* extent */
} typespan;
```

A span represents the closed-half-open interval `[stream, stream+width)` in the **total order** on tumblers. The total order is defined by `tumblercmp` (`tumble.c:72-85`), which delegates to `abscmp` (`tumble.c:87-111`): lexicographic comparison of the `exp` field, then each mantissa digit in order. This is a strict total order over all tumblers regardless of how many "stories" they have.

---

### 2. The intersection function

The only function that computes the intersection of two individual spans is `spanintersection` in `correspond.c:210-265`:

```c
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr)
{
  tumbler aend, bend;

    tumblerclear (&cptr->stream);
    tumblerclear (&cptr->width);
    tumbleradd (&bptr->stream, &bptr->width, &bend);
    if (tumblercmp (&aptr->stream, &bend) >= EQUAL)
        return (FALSE);                             /* A starts at or after B ends → no overlap */
    tumbleradd (&aptr->stream, &aptr->width, &aend);
    if (tumblercmp (&bptr->stream, &aend) >= EQUAL)
        return (FALSE);                             /* B starts at or after A ends → no overlap */
    switch (tumblercmp (&aptr->stream, &bptr->stream)) {
      case EQUAL:
        movetumbler (&aptr->stream, &cptr->stream);
        /* width = min(aend, bend) - stream */
        ...
      case GREATER:  /* astart > bstart */
        movetumbler (&aptr->stream, &cptr->stream);  /* intersection starts at A */
        /* width = min(aend, bend) - astart */
        ...
      case LESS:     /* astart < bstart */
        movetumbler (&bptr->stream, &cptr->stream);  /* intersection starts at B */
        /* width = min(aend, bend) - bstart */
        ...
    }
    return (TRUE);                                  /* always exactly ONE output span */
}
```

This function always writes into a **single** `cptr` and returns exactly `TRUE` (overlap) or `FALSE` (empty). There is no code path that creates a list or produces two disjoint spans. This is `correspond.c:210-265`.

---

### 3. Why the mathematics guarantees this

Two intervals `[A_start, A_end)` and `[B_start, B_end)` in any total order intersect as:

```
∅                          if A_end ≤ B_start or B_end ≤ A_start
[max(A_start, B_start),    otherwise
 min(A_end,   B_end))
```

This is a topological fact. Two contiguous intervals cannot intersect as a disconnected set in a total order. `spanintersection` implements exactly this formula:

- `cptr->stream = max(astart, bstart)` (the `switch` on `tumblercmp`)
- `cptr->width  = min(aend, bend) - max(astart, bstart)` (the inner `switch` on `tumblercmp(&aend, &bend)`)

---

### 4. The role of hierarchical structure

Tumblers are hierarchical: `1.2.3` has three levels, and in tumbler ordering `1.2 < 1.2.1 < 1.3` (because each level is compared lexicographically by `abscmp`, `tumble.c:99-108`). A span `[1.2, 1.3)` therefore contains `1.2.1`, `1.2.99`, `1.2.1.1`, etc. — the full sub-tree between those two addresses.

But this structure does **not** make the interval non-contiguous. The total order is still linear. Sub-addresses are simply between their parent addresses in the order. Crossing a "hierarchical boundary" (e.g., from within `1.*` to `2.*`) is just crossing one point in the total order: `2.0` itself. There is no gap or disconnection.

---

### 5. Where multiple spans actually arise

Multiple spans **do** arise, but not from the intersection of two individual spans. They arise from:

**V→I or I→V coordinate mapping.**  `permute` → `span2spanset` in `orglinks.c:404-453` calls `retrieverestricted` (`retrie.c:56-85`) to walk the POOM enfilade and collect all crums that overlap the query span. Each crum produces one context, and `context2span` (`context.c:176-212`) clips it to the query restriction. The results from all crums are collected into a `targspanset` list — potentially many spans.

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset, ...)
{
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(...);    /* may grow the list */
    }
}
```

`span2spanset` (`orglinks.c:425-454`) appends one span per context:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *) onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

So a single vspan query can return many non-contiguous ispans if the document content is fragmented across multiple POOM crums (i.e., has been cut, copied, or rearranged).

**Spanset intersection.** `intersectspansets` in `correspond.c:145-188` does produce multiple output spans, by iterating over all pairs:

```c
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;        /* appends one span per overlapping pair */
    }
}
```

If set1 has M spans and set2 has N spans, the output can have up to M×N spans. But this is the intersection of two **spansets**, not two individual spans.

---

### 6. A subtle limitation in coordinate-space clipping

`context2span` (`context.c:194`) uses `tumblerintdiff` to compute offsets:

```c
tumblerincrement (&grasp.dsas[idx2], 0,
    (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
    &grasp.dsas[idx2]);
```

`tumblerintdiff` (`tumble.c:591-597`) returns only `c.mantissa[0]` — the first digit of the tumbler subtraction. If the clipping offset is a multi-story tumbler (e.g., the restriction span starts deep within a sub-address that is many levels removed from the crum origin), only the top digit is used. This is a precision limitation of the coordinate mapping, not of span intersection itself, and it affects V→I/I→V fidelity rather than the pure geometric intersection.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Is intersection of two single tumbler spans always one span? | **Yes** | `spanintersection`, `correspond.c:210-265` — always at most one output span |
| Can hierarchical boundaries fragment a span intersection? | **No** | `tumblercmp` defines a total order; two intervals in any total order intersect as 0 or 1 intervals |
| Where do multiple spans arise? | V→I/I→V mapping across POOM crums | `permute`, `orglinks.c:404-453`; `intersectspansets`, `correspond.c:145-188` |
| Are there known imprecisions in span computations? | Yes, in clipping | `context2span` uses `tumblerintdiff` returning only `mantissa[0]`, `context.c:194` |

The intersection of two overlapping tumbler spans is always exactly one span. The multi-span results that appear in practice arise from the POOM permutation mapping that converts between V-space and I-space, where content fragmentation across crum boundaries produces a set of non-contiguous output spans — but that is coordinate mapping, not geometric span intersection.
