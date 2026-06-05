## Question 12 [evidence]

> If the requested V-span includes positions that have no POOM entry (a gap between two crums), does the read skip those positions silently, return a placeholder, or truncate the result at the first gap?

## KB Synthesis

## Gap Handling During V-Span Reads

The system **silently skips** positions with no POOM entry. No placeholder is returned and results are not truncated at the first gap — the retrieval simply returns content only for covered positions.

### Mechanism

The core retrieval path for `retrieve_contents` is:

```
doretrievev → specset2ispanset → [POOM traversal] → ispanset2vstuffset
```

The POOM traversal uses `findcbcinarea2d()`, which walks the B-tree and accumulates only leaf nodes (crums) that actually cover some portion of the queried V-range [SS-POOM-MULTIMAP]. If no crum covers a given sub-range, no context is added to the accumulation list — `incontextlistnd()` is only called per matching leaf [SS-CONTEXT-LIST].

The resulting `ispanset` therefore contains only I-spans corresponding to *occupied* V-positions. The permascroll lookup `ispanset2vstuffset` then fetches bytes for those I-spans only. Gap positions contribute nothing.

### Confirmed by the I→V Direction

The same silent-skip behavior appears in the reverse direction (I→V). From [SS-FOLLOWLINK] (Finding 0048):

> If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is **silently dropped** — no V-span is added to the result.

[INV-ITOV-FILTERING] makes this a universal property of the conversion layer: unreferenced addresses are always silently excluded.

### Practical Consequence

A retrieval spanning two crums with a V-space gap between them returns **concatenated content from both crums with the gap elided** — the caller receives no indication a gap existed. This is especially relevant for mixed-subspace reads: querying a V-range that crosses the boundary between the text subspace (1.x) and link subspace (2.x, normalized to 0.x in output) silently omits the unoccupied inter-subspace addresses, which is why [PRE-RETRIEVE-CONTENTS] requires callers to restrict specsets to one subspace at a time [PRE-RETRIEVE-CONTENTS].

---

## Code Exploration

Now I have a complete picture of the execution path. Here is the full answer:

---

## What Happens When a V-Span Retrieval Hits a Gap

### Answer: Gap positions are silently skipped. No placeholder, no error, no truncation.

The retrieval returns only the content that exists within the requested V-span. Positions with no POOM crum mapping are simply absent from the result.

---

### Execution Path

The entry point is `fns.c:175` (`retrievev`), which calls `doretrievev` (`do1.c:338`):

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

Two phases: translate V-spans → I-spans, then retrieve content for those I-spans.

---

### Phase 1: V→I Translation via the POOM (`specset2ispanset` → `vspanset2ispanset` → `permute` → `span2spanset`)

In `orglinks.c:435`, `span2spanset` calls:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```

This reaches `findcbcinarea2d` in `retrie.c:229`. The critical loop is:

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr)) {
        continue;              // <- skip crums that don't intersect requested span
    }
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);  // recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);              // <- record match
    }
}
```

`crumqualifies2d` (`retrie.c:270`) tests whether the requested V-span intersects the crum's V-coverage. The two disqualifying conditions are:

```c
// Span ends before crum starts:
endcmp = whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return FALSE;

// Span starts after crum ends:
startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return FALSE;
```

**The critical point:** The loop iterates over POOM crums — physical tree nodes. A gap in V-space means there is no crum whose V-interval covers those addresses. The loop passes right through, producing zero context entries for the gap.

`whereoncrum` (`retrie.c:345`) returns positional relationship codes (`TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME`, `ONMYRIGHTBORDER`, `TOMYRIGHT`). For a crum to the left of the gap, `startcmp` returns `TOMYRIGHT` (> `THRUME`) — disqualified. For a crum to the right of the gap, `endcmp` returns `TOMYLEFT` (< `ONMYLEFTBORDER`) — disqualified. If the requested span straddles the gap, the crums on both sides individually qualify and both contribute context entries. But the gap itself produces nothing.

---

### Phase 2: Context → I-Spans

Back in `span2spanset` (`orglinks.c:439`):

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
if (!context) {
    return (targspansetptr);   // <- returns unchanged list if no context at all
}
```

`context2span` (`context.c:176`) clips each context's I-interval to the intersection of the crum's V-coverage with the requested V-span, then produces one I-span per crum. No I-span is emitted for gap positions.

If the V-span spans a gap, the resulting `ispanset` is a **list of disjoint I-spans** — one for each non-gap segment, in V-order. The gap produces nothing in this list.

---

### Phase 3: I-Spans → Content

`ispanset2vstuffset` (`granf1.c:58`) iterates the I-span list:

```c
for (; ispanset; ispanset = ispanset->next) {
    vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
}
return (TRUE);     // <- always returns TRUE regardless of how many spans found
```

`ispan2vstuffset` (`granf2.c:286`) calls `retrieveinspan` on the granfilade for each I-span. Each I-span returns one or more text chunks (granfilade atoms). Chunks are appended into the output `vstuffset`.

**Important:** `ispanset2vstuffset` always returns `TRUE` — even when the ispanset is empty (i.e., the entire requested V-span was in a gap). No error is signaled. The caller gets an empty `vstuffset`.

---

### Summary

| Scenario | Behavior |
|---|---|
| Requested V-span entirely in a gap | Empty `vstuffset` returned, no error |
| Requested V-span straddles a gap | `vstuffset` contains chunks from non-gap segments only; gap is absent |
| Gap in the middle of a long V-span | Result has entries for both sides; no placeholder at gap boundary |

The POOM enfilade traversal in `findcbcinarea2d` is crum-driven, not position-driven. V-positions with no crum mapping are invisible to the traversal. The design intentionally treats gap positions as simply absent — the document's V-space is sparse, and reads into unmapped regions silently return nothing.
