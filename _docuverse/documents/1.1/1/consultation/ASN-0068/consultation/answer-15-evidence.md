## Question 15 [evidence]

> When correspondence is computed, are I-address spans matched by exact equality, by overlap, or by containment — and what does the result look like when doc1 contains I:[.0.1.1,.0.1.10] and doc2 contains I:[.0.1.3,.0.1.7] (a strict subset)?

## KB Synthesis

## Correspondence Matching: Intersection

The matching criterion is **I-address range intersection**, not exact equality or containment. [INT-SPORGL-VERSION-COMPARE] states the shared-content predicate explicitly:

```
shared(A, B) = { s ∈ sporgls(A) | ∃ t ∈ sporgls(B) :: s.origin ∩ t.origin ≠ ∅ }
```

[SS-COMPARE-VERSIONS] confirms: `correspond.c` implements a "nested loop computing I-span intersections." The result postcondition is that each pair `(span_a, span_b)` satisfies `VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)` — meaning the V-spans are mapped back from the **intersection region**, not from the full spans of either document.

## Your Specific Case

- doc1: I-span `[.0.1.1, .0.1.10)`, width 9
- doc2: I-span `[.0.1.3, .0.1.7)`, width 4 (strict subset)

The intersection is `[.0.1.3, .0.1.7)` — doc2's entire span.

**Result:** one correspondence pair:
- doc1's V-span: the sub-region of doc1 whose I-addresses are `.0.1.3`–`.0.1.7` (4 units somewhere mid-stream)
- doc2's V-span: all of doc2's content (since doc2's I-span is wholly within the intersection)

This is directly analogous to the version-insert example in [ST-INSERT] Finding 0030, where "CDE" in the original maps to a shifted sub-range in the modified version — two V-spans of equal width paired by their shared I-address region.

**One pair is returned, not two.** The result does not separately report the non-overlapping prefix `[.0.1.1, .0.1.3)` of doc1, since doc2 contains nothing in that range. [SS-COMPARE-VERSIONS] specifies completeness: "every shared permascroll address range appears in exactly one pair" — and only the intersection qualifies as shared.

---

## Code Exploration

Now I have all the verified code. Here is my full answer.

---

## How Correspondence Is Computed: Intersection, Not Equality or Containment

### The Short Answer

Correspondence uses **interval intersection (overlap)** at every layer. Neither exact equality nor strict containment is required. Any overlap — including one span being a strict subset of the other — qualifies. The result represents only the overlapping sub-span, not the full extents of either side.

---

### Layer 1 — Enfilade Traversal: `crumqualifies2d` [retrie.c:270]

This is the innermost and hottest function in the retrieval path (comment says "40% of CPU"). It decides whether a given crum should be included in the result:

```c
bool crumqualifies2d(..., tumbler *span1start, tumbler *span1end, INT index1, ...)
{
    endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER)   /* crum ends before span starts → reject */
        return(FALSE);

    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME)          /* crum starts after span ends → reject */
        return(FALSE);

    ...  /* same test on second dimension */
    return(TRUE);
}
```

The five position codes [common.h:86–90]:

| Code | Value | Meaning |
|------|-------|---------|
| `TOMYLEFT` | −2 | address is left of crum |
| `ONMYLEFTBORDER` | −1 | address is at crum's left edge |
| `THRUME` | 0 | address is strictly inside crum |
| `ONMYRIGHTBORDER` | +1 | address is at crum's right edge |
| `TOMYRIGHT` | +2 | address is right of crum |

The two guards together implement the standard open-interval overlap test:

- **Reject** if `span1end` falls on or before the crum's left border (`endcmp <= ONMYLEFTBORDER`)
- **Reject** if `span1start` starts strictly past the crum's right edge (`startcmp > THRUME`)
- **Accept** everything else — any amount of overlap counts

Note the asymmetry: the first guard uses `<=` (touching the left border rejects), but the second guard uses `>` (touching the right border does *not* reject). This means left-edge-touching is treated as non-overlapping, right-edge-touching as overlapping. The comment `/*=*/` on line 283 marks where that boundary decision was made.

---

### Layer 2 — Clipping to the Overlap: `context2span` [context.c:176]

Once a qualifying crum is found, `context2span` computes what portion of the crum falls within the restriction span, and projects that clipped portion into the target dimension (V or I):

```c
int context2span(typecontext *context, typespan *restrictionspanptr,
                 INT idx1, typespan *foundspanptr, INT idx2)
{
    movetumbler(&restrictionspanptr->stream, &lowerbound);
    tumbleradd(&lowerbound, &restrictionspanptr->width, &upperbound);
    prologuecontextnd(context, &grasp, &reach);   /* gets crum's full extent */

    if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) /* crum starts before span */
        tumblerincrement(&grasp.dsas[idx2], 0,
            tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),  /* shift grasp forward */
            &grasp.dsas[idx2]);

    if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) /* crum ends after span */
        tumblerincrement(&reach.dsas[idx2], 0,
            -tumblerintdiff(&reach.dsas[idx1], &upperbound),  /* pull reach back */
            &reach.dsas[idx2]);

    movetumbler(&grasp.dsas[idx2], &foundspanptr->stream);
    tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
}
```

This is the **projection with clipping**: the output V-span is the part of the crum's V-coverage that corresponds to the overlap between the crum's I-range and the query I-span. A crum that covers I:[.0.1.1, .0.1.10]→V:[Va, Va+9] queried with I:[.0.1.3, .0.1.7] will produce the clipped output V:[Va+2, Va+6], not the full V:[Va, Va+9].

---

### Layer 3 — Enfilade Query Entry: `span2spanset` [orglinks.c:425]

`span2spanset` drives the retrieval for each input span:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);
}
```

The second span argument to `retrieverestricted` is `NULL` [line 435], meaning the second dimension (V) is unconstrained — the function finds all crums whose I-coordinate overlaps the restriction I-span, regardless of where they live in V-space.

`permute` [orglinks.c:404] iterates over all spans in the restriction set and calls `span2spanset` for each, accumulating results.

---

### Layer 4 — Document-Level V-Span Intersection: `spanintersection` [correspond.c:210]

At the top level, when comparing two documents, each document's I-spans are converted to V-span sets via their own ORGLs. Then `spanintersection` computes the geometric overlap of corresponding V-spans:

```c
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr)
{
    tumbleradd(&bptr->stream, &bptr->width, &bend);
    if (tumblercmp(&aptr->stream, &bend) >= EQUAL)  /* a starts at or after b ends */
        return(FALSE);
    tumbleradd(&aptr->stream, &aptr->width, &aend);
    if (tumblercmp(&bptr->stream, &aend) >= EQUAL)  /* b starts at or after a ends */
        return(FALSE);
    /* ... compute the actual intersection span into cptr ... */
    return(TRUE);
}
```

`intersectspansets` [correspond.c:145] calls this pairwise over all span combinations and collects the non-empty intersections.

---

### Applied to the Specific Example

**Setup:** doc1 has content at I:[.0.1.1, .0.1.10]. doc2 has content derived from that, at I:[.0.1.3, .0.1.7]. (These are I-addresses in separate documents, hence in separate I-spaces. Correspondence passes through V-space.)

**Step 1 — I→V for doc1.**  
ORGL1 contains a crum mapping I:[.0.1.1, .0.1.10]→V:[Va, Va+9].  
Query restriction: I:[.0.1.1, .0.1.10]. Crum qualifies trivially (exact match).  
`context2span` produces V:[Va, Va+9] (no clipping needed).  
doc1 V-span set: {V:[Va, Va+9]}.

**Step 2 — I→V for doc2.**  
ORGL2 contains a crum mapping I:[.0.1.3, .0.1.7]→V:[Va+2, Va+6] (these V-addresses are the same content, just a different slice).  
Query restriction: I:[.0.1.3, .0.1.7]. Crum qualifies; `context2span` produces V:[Va+2, Va+6].  
doc2 V-span set: {V:[Va+2, Va+6]}.

**Step 3 — Intersect V-spans.**  
`spanintersection(V:[Va, Va+9], V:[Va+2, Va+6])`:  
- `Va+9 > Va+2` → not disjoint left  
- `Va+6 > Va` → not disjoint right  
- Result: stream = max(Va, Va+2) = Va+2, width = min(Va+9, Va+6) − Va+2 = Va+6 − Va+2  
- Intersection: **V:[Va+2, Va+6]**

**Step 4 — V→I for each document.**  
- In doc1: V:[Va+2, Va+6] maps back to I:[.0.1.3, .0.1.7] (the strict subset of doc1's range)
- In doc2: V:[Va+2, Va+6] maps back to I:[.0.1.3, .0.1.7] (the full I-range of doc2)

**Result:** The correspondence is the narrower span — the strict subset I:[.0.1.3, .0.1.7]. Doc1's I:[.0.1.1, .0.1.10] contributes only the portion [.0.1.3, .0.1.7] to the correspondence; the flanking content at [.0.1.1, .0.1.3) and (.0.1.7, .0.1.10] in doc1 has no corresponding content in doc2 and is not included.

---

### Summary

| Property | Value |
|----------|-------|
| Matching rule | Intersection (overlap) — `crumqualifies2d` [retrie.c:270] |
| Exact equality required? | No |
| Containment required? | No |
| Strict subset case | Qualifies — the smaller span wins |
| Output computation | Clipped to actual overlap — `context2span` [context.c:176] then `spanintersection` [correspond.c:210] |
| Asymmetric boundary | Left-edge touch rejects; right-edge touch does not (note `<=` vs `>` in `crumqualifies2d` lines 283/287) |
