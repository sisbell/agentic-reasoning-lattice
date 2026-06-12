## Question 13 [evidence]

> When a shared I-span overlaps only partially with the queried specset boundaries, does SHOWRELATIONOF2VERSIONS clip the returned correspondence pair to the specset boundary, and are the V-offsets within each returned pair guaranteed to denote the same I-width on both sides?

## KB Synthesis

Two separate questions — let me address each from mechanism up.

---

## 1. Does SHOWRELATIONOF2VERSIONS clip to the specset boundary on partial I-span overlap?

**Yes.** The clip is structural, not optional.

The conversion pipeline is: specset → `specset2ispanset` → V-to-I lookup in the document's POOM → intersection → I-to-V back.

The `specset2ispanset` step queries the POOM only within the V-range described by the specset. If a bottom crum covers `[V 1.1, V 1.9]` mapping to `[I α₁ .. I α₉]`, and the specset covers only `V 1.4 to V 1.7`, then `findcbcinarea2d` returns only the contexts within that range, yielding `[I α₄ .. I α₇]`. The crum is not returned whole; its intersection with the query window is what participates.

This is confirmed by [ST-SPECSET-COMPARE]:

> "compare(specset_A, specset_B) reports only identity overlaps between content referenced by specset_A and content referenced by specset_B. Content in either document but outside the specified spans does not appear in results."

And from [SS-COMPARE-VERSIONS]:

> "each pair (span_a, span_b) in the result satisfies: VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)"

The I-intersection therefore operates on already-clipped I-spans. A shared region that straddles a specset boundary appears in the output only as the sub-segment within the specset — not the full shared I-span.

---

## 2. Are the V-widths in each returned pair guaranteed equal?

**Yes, by construction** — with one structural caveat about internal transclusion.

Each pair `(span_a, span_b)` is produced by:
1. Computing the intersection of I-spans from both documents' specsets → yields a shared I-region of some width W
2. Mapping that I-region back to V-spans via `ispan2vspanset` in each document

Because both sides are derived from the **same** shared I-region [SS-COMPARE-VERSIONS]:

> "VSpanToISpan(doc_a, span_a) == VSpanToISpan(doc_b, span_b)"

the I-address count is identical by definition. In the standard case (no internal transclusion), there is a 1:1 correspondence between I-addresses and V-positions within a contiguous span, so the V-width equals the I-width on both sides — the same numeric value, though encoded at different tumbler precision per [SS-INSERT-VWIDTH-ENCODING] and [INV-WIDTH-VALUE-EQUIVALENCE].

The example in [SS-COMPARE-VERSIONS] bears this out directly:

```
[(A: V 1.1 for 5,  B: V 1.1 for 5),
 (A: V 1.6 for 6,  B: V 1.11 for 6)]
```

Both spans in every pair carry the same width.

**Caveat — internal transclusion:** If the same I-address appears at multiple V-positions within one document (SS-POOM-MULTIMAP), then `ispan2vspanset` returns a *set* of V-spans for that I-region, not a single span. The KB has no finding that directly tests how `correspond.c` handles multimap returns for this case, and [EC-COMPARE-VERSIONS-LINK-CRASH] shows the operation already crashes on link-subspace inputs, suggesting the implementation assumes a simple 1:1 POOM structure. For content accessed solely via `1.x` text spans in the normal transclusion case (multiple V-positions sharing an I-address), the pair structure and any width guarantees become undefined by the KB evidence.

---

**Summary:**  
Clipping to the specset boundary is mechanically guaranteed by how `specset2ispanset` restricts POOM traversal [ST-SPECSET-COMPARE]. Within each returned pair, both sides encode the same I-width, so their V-widths are numerically equal [SS-COMPARE-VERSIONS] — provided the document's POOM is a simple surjection (no internal transclusion), which is the precondition the implementation implicitly assumes.

---

## Code Exploration

I now have all the source I need. Let me assemble the complete, cited answer.

---

## Answer: Clipping at Specset Boundaries in SHOWRELATIONOF2VERSIONS

### Execution path overview

`SHOWRELATIONOF2VERSIONS` dispatches to `showrelationof2versions` [fns.c:250], which calls `doshowrelationof2versions` [do1.c:428] via the `get`/`do`/`put` triad. The `do` function runs a four-step pipeline:

```c
// do1.c:443-448
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
&&  specset2ispanset(taskptr, version2, &version2ispans, READBERT)
&&  intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&&  ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

Each step participates in the clipping. There is a pre-filter step too:

```c
// do1.c:440-441
filter_specset_to_text_subspace(taskptr, version1);
filter_specset_to_text_subspace(taskptr, version2);
```

That discards any link-subspace spans (V < 1.0) before any further processing.

---

### Step 1 – V→I conversion with symmetric clipping (`context2span`)

`specset2ispanset` [do2.c:14] walks the specset list. For a `VSPECID` element it calls `vspanset2ispanset` [orglinks.c:397], which is just:

```c
// orglinks.c:397-402
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` [orglinks.c:404] iterates over every input V-span and calls `span2spanset` [orglinks.c:425], which calls `retrieverestricted` to walk the document's POOM enfilade and collect leaf crums that overlap the query V-span, then calls `context2span` [context.c:176] for each one.

`context2span` is where partial-overlap clipping first occurs:

```c
// context.c:186-207
movetumbler (&restrictionspanptr->stream, &lowerbound);
tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
prologuecontextnd (context, &grasp, &reach);

if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement (&reach.dsas[idx2], 0,
        - tumblerintdiff (&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);       
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

The POOM axis constants are defined in `wisp.h`:

```c
// wisp.h:19-20
#define I  0
#define V  1
```

When called for V→I conversion, `idx1 = V` and `idx2 = I`. If the leaf crum's V-extent starts *before* the query's `lowerbound`, the code shifts `grasp[I]` (the I-axis start) forward by exactly the integer difference `tumblerintdiff(lowerbound, grasp[V])`. The same symmetric treatment applies to the high end: if `reach[V]` overshoots `upperbound`, `reach[I]` is decremented by the same integer difference. The resulting I-span width `reach[I] - grasp[I]` equals the V-span width of the query that fell within this crum — no more, no less.

This is the POOM bijection property at work: each leaf crum stores one I-origin, one V-origin, and one shared integer width. There is no scaling between I and V dimensions inside a crum. An overhang of *n* characters on the V-axis clips exactly *n* characters on the I-axis.

---

### Step 2 – I-span intersection (`intersectspansets` → `spanintersection`)

`intersectspansets` [correspond.c:145] pairs every I-span from version1 with every I-span from version2 and calls `spanintersection` [correspond.c:210]:

```c
// correspond.c:210-265
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr)
{
    tumbleradd (&bptr->stream, &bptr->width, &bend);
    if (tumblercmp (&aptr->stream, &bend) >= EQUAL) return (FALSE);
    tumbleradd (&aptr->stream, &aptr->width, &aend);
    if (tumblercmp (&bptr->stream, &aend) >= EQUAL) return (FALSE);
    switch (tumblercmp (&aptr->stream, &bptr->stream)) {
      case LESS:
        movetumbler (&bptr->stream, &cptr->stream);
        // ... picks the narrower upper bound
    }
    return (TRUE);
}
```

The result `commonispans` contains only the I-addresses that appear in both V→I mappings. Any I-span that exists in only one version is dropped entirely. A partially-overlapping I-span pair is trimmed to their overlap.

Note the comment at correspond.c:222: `/* these following assignments are clearly wrong 12/4/84 */`. That comment predates the final switch body; the actual assignments in the switch arms below it compute the correct clipped start and narrower width.

---

### Step 3 – Restriction of both specsets to common I-spans

`ispansetandspecsets2spanpairset` [do2.c:185] calls:

```c
// do2.c:196-197
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);
makespanpairset(taskptr, ispanset, specset1, specset2, pairsetptr);
```

`restrictspecsetsaccordingtoispans` [correspond.c:18] runs two passes on each specset:

**Pass A** — `restrictvspecsetovercommonispans` [correspond.c:52]: for each common I-span and each specset element, calls `ispan2vspanset` (the inverse permute, I→V) using the document's own POOM. The same `context2span` clipping logic applies here with `idx1 = I, idx2 = V`: if a POOM leaf crum's I-extent only partially overlaps the common I-span, its V-contribution is trimmed by the same integer delta. The resulting V-spans are precisely the V-addresses that correspond to the common I-addresses in that version.

**Pass B** — `removespansnotinoriginal` [correspond.c:92]: takes the V-spans from pass A and intersects them with the *original* query specset's V-spans via `intersectspansets`:

```c
// correspond.c:116
if (intersectspansets(taskptr, ((typevspec *)new)->vspanset,
                               ((typevspec *)old)->vspanset,
                               &newspanset, VSPANID)) {
```

`new` is the pass-A V-span (derived from common I-spans); `old` is the caller's original query specset V-span. This `spanintersection` call clips the V-spans to the **minimum** of what the I-correspondence produced and what the user queried. Any V-content that maps through a shared I-span but lies outside the caller's query window is discarded here.

After `restrictspecsetsaccordingtoispans` returns, both `specset1` and `specset2` contain only the V-spans that are:

1. Backed by I-addresses present in both versions (common origin), and  
2. Within the original query specset boundary for that version.

---

### Step 4 – Pairing with a single shared width (`makespanpairsforispan`)

`makespanpairset` [correspond.c:267] iterates `commonispans`, forwarding the I-width:

```c
// correspond.c:279-280
movetumbler (&ispanset->width, &iwidth);
makespanpairsforispan(taskptr, &iwidth, &specset1, &specset2, &pairset);
```

`makespanpairsforispan` [correspond.c:290] walks the two restricted V-span lists in lock-step, consuming both by the minimum at each step:

```c
// correspond.c:308-328
while (span1 && span2 && tumblercmp (iwidth, &sum) == GREATER) {
    cmp = tumblercmp (&span1->width, &span2->width);
    switch (cmp) {
      case LESS:
      case EQUAL:
        *pairsetptr = makespanpair(..., &span1->width);   // use span1->width
        tumbleradd (&span2->stream, &span1->width, &span2->stream);
        tumblersub (&span2->width, &span1->width, &span2->width);
        span1 = span1->next;
        break;
      case GREATER:
        *pairsetptr = makespanpair(..., &span2->width);   // use span2->width
        tumbleradd (&span1->stream, &span2->width, &span1->stream);
        tumblersub (&span1->width, &span2->width, &span1->width);
        span2 = span2->next;
    }
}
```

In every case, exactly `min(span1->width, span2->width)` is consumed from *both* sides. The other side's `stream` is advanced by the same amount and its `width` reduced by the same amount. The pair itself is constructed as:

```c
// correspond.c:351-361
spanpair = taskalloc(taskptr, sizeof(typespanpair));
docidandvstream2tumbler(doc1, start1, &spanpair->stream1);
docidandvstream2tumbler(doc2, start2, &spanpair->stream2);
movetumbler(width, &spanpair->widthofspan);       // single width
```

There is only one `widthofspan` field. The serialiser confirms this [putfe.c:233-237]:

```c
puttumbler(taskptr->outp, &spanpair->stream1);
puttumbler(taskptr->outp, &spanpair->stream2);
puttumbler(taskptr->outp, &spanpair->widthofspan);
```

---

### Conclusion

**Does SHOWRELATIONOF2VERSIONS clip to the specset boundary?**

Yes, unconditionally, through a three-layer clip:

| Layer | Where | Mechanism |
|---|---|---|
| V-overhang on query span | `context2span` [context.c:191-202] | symmetric integer delta on opposing axis |
| I-span intersection | `spanintersection` [correspond.c:210-265] | pick narrower overlap |
| Restricted V back to query | `removespansnotinoriginal` [correspond.c:92-135] | `intersectspansets` in V-space |

A shared I-span that only partially falls within the queried specset will produce a returned V-span that is the intersection of (a) the portion of the I-span reachable via the POOM bijection and (b) the original query V-span.

**Are the V-offsets in each returned pair guaranteed to denote the same I-width on both sides?**

Yes. The guarantee rests on:

1. **`context2span` applies the same integer delta to both axes** [context.c:194, 200]: clipping *n* characters from the V-axis boundary clips exactly *n* characters from the I-axis boundary (and vice versa on the return trip). No scaling exists inside a single POOM leaf crum.

2. **Both restricted V-span lists derive from the same `commonispans`**: after `restrictspecsetsaccordingtoispans`, span1 and span2 are each the V-image of the same I-address range, so their widths are equal per I-segment.

3. **`makespanpairsforispan` advances both pointers by the same amount** [correspond.c:318-319, 326-327]: the `widthofspan` stored in the pair is the amount consumed from both sides simultaneously. The "LESS" and "GREATER" cases are boundary-fragment handling for POOM splits across a single I-segment; each such fragment is still a valid pair with a single shared width.

**One caveat**: `makespanpairsforispan` uses `tumblerintdiff` internally (via the V-width comparisons), which truncates non-integer tumblers to a platform `INT`. If any span's width is a multi-digit tumbler that does not fit in an integer, the arithmetic in `context2span` [context.c:194, 200] and the width comparisons in `makespanpairsforispan` will silently truncate. In practice the current tests all use small integer V-spans, so this does not surface.
