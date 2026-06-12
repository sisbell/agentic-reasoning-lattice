## Question 16 [evidence]

> When a specset is compared against itself (same document, same span), does correspond.c return the trivial identity pair covering the whole span, one pair per POOM bottom crum, or also the off-diagonal pairs arising from within-document shared I-addresses?

## KB Synthesis

The KB lets me answer this precisely for the simple case and honestly flag the gap for the internal-transclusion case.

---

## Simple self-comparison (no internal transclusion)

**One pair per contiguous I-span block, not one per POOM crum.**

`correspond.c` operates at the I-span level, not the POOM-crum level. It converts each specset to I-spans via `specset2ispanset` / `permute`, intersects the two I-span sets, then maps back to V-spans via `ispan2vspanset`. [SS-COMPARE-VERSIONS, PRE-COMPARE-VERSIONS]

For a document with unfragmented I-addresses, the full specset converts to one contiguous I-span, which intersects itself and maps back to one pair. [EC-SELF-COMPARISON] confirms this: a 17-char document returns `(Span(1.1, 0.17), Span(1.1, 0.17))` — one pair, not 17.

If the document has fragmented I-addresses — for example, because CREATELINK was issued between two inserts, advancing the I-space allocator mid-document — then `specset2ispanset` yields multiple non-contiguous I-spans and `correspond.c` returns one pair per fragment. [INT-LINK-INSERT, INV-MONOTONIC] Those pairs are still diagonal (each fragment maps to itself) but the count is > 1.

---

## Self-comparison with internally transcluded content

**The KB cannot answer this definitively — and the implementation behavior is likely undefined.**

When a document contains internal transclusion (self-vcopy), the POOM is a genuine multimap: a single I-address can appear at multiple V-positions. [SS-POOM-MULTIMAP] `ispan2vspanset` returns the full set — `{VSpan(1.2), VSpan(1.4), VSpan(1.5)}` for an I-address present at three V-positions.

`correspond.c` uses this same I-to-V path for both output columns. That means for I-span `{i₁..i₃}` shared between V:1.1 and V:1.10 within the same document, the reverse map produces two V-spans in each column, not one. The off-diagonal pairs `(V:1.1, V:1.10)` and `(V:1.10, V:1.1)` would fall out of the Cartesian product.

However, the KB records that `correspond.c`'s nested loop **"assumes each ispan matches at most one vspec"** [EC-COMPARE-VERSIONS-LINK-CRASH] — the comment is in the context of the link-subspace crash, but the structural assumption is general. Whether the loop enumerates all pairs or takes the first match and proceeds (possibly producing only the diagonal) is **not documented in the KB**. The implementation may produce incorrect or undefined results in this case, analogous to the link-crash edge case.

---

## Summary

| Scenario | What the KB says |
|---|---|
| No internal transclusion | Trivial diagonal pair(s), one per contiguous I-span fragment [EC-SELF-COMPARISON] |
| Fragmented I-addresses (e.g., CREATELINK between inserts) | Multiple diagonal pairs, one per I-span block [INT-LINK-INSERT] |
| Internally transcluded content (self-vcopy) | Off-diagonal pairs would arise from the multimap [SS-POOM-MULTIMAP]; but `correspond.c`'s assumed 1:1 I-to-V mapping means actual behavior is not documented and likely undefined [EC-COMPARE-VERSIONS-LINK-CRASH] |
| Per POOM bottom crum | No — crum granularity is internal structure invisible at the I-span abstraction level |

---

## Code Exploration

I have everything needed. Let me now write the full answer.

---

## Self-Comparison in `correspond.c`: What Pairs Are Produced?

### The Full Pipeline (`do1.c:428–449`)

`doshowrelationof2versions` orchestrates four steps:

```c
filter_specset_to_text_subspace(taskptr, version1);        // do1.c:440
filter_specset_to_text_subspace(taskptr, version2);        // do1.c:441
specset2ispanset(taskptr, version1, &version1ispans, ...)  // do1.c:444
&&  specset2ispanset(taskptr, version2, &version2ispans, ...) // do1.c:445
&&  intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID) // do1.c:446
&&  ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation) // do1.c:447
```

When `version1 == version2` (same document, same span), steps 1–3 are trivially symmetric: `version1ispans == version2ispans`, so `commonispans` is the same I-span set.

---

### Step 4: `ispansetandspecsets2spanpairset` (`do2.c:185`)

```c
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2); // do2.c:196
makespanpairset(taskptr, ispanset, specset1, specset2, pairsetptr);          // do2.c:197
```

`specset1` and `specset2` are **local copies** (passed by value at `do2.c:185`), so mutating them inside `restrictspecsetsaccordingtoispans` does not alias.

---

### Restriction phase: V→I→V round-trip (`correspond.c:18–50`, `do2.c:52–90`)

`restrictspecsetsaccordingtoispans` calls `restrictvspecsetovercommonispans` (`correspond.c:52`), which for each I-span calls:

```c
ispan2vspanset(taskptr, versionorgl, ispanset, &docvspanset);   // correspond.c:74
```

`ispan2vspanset` → `permute(..., I, ..., V)` (`orglinks.c:389–393`) walks the POOM and returns **every V-location** that holds content at that I-address. For a document with no copies this is one V-span; for a document with N copies at the same I-address, it is N V-spans. All are collected into `docvspanset` for a single `typevspec` node.

`removespansnotinoriginal` (`correspond.c:92–135`) then intersects `docvspanset` with the original query spans via `intersectspansets`. For self-comparison where the query covers the whole document, all N V-spans survive.

After restriction, both `specset1` and `specset2` contain **identical** structures: the same `docisa`, the same `vspanset` (a list of V-spans in I-address order, at POOM bottom-crum granularity).

---

### Pair-generation: the zipper (`correspond.c:290–349`)

`makespanpairsforispan` is the critical function. It is a **merge-style linear zipper**, not a nested double loop:

```c
spec1 = (typevspec *)*specset1ptr;   // correspond.c:304
span1 = spec1->vspanset;             // correspond.c:305
spec2 = (typevspec *)*specset2ptr;   // correspond.c:306
span2 = spec2->vspanset;             // correspond.c:307

while (span1 && span2 && tumblercmp(iwidth, &sum) == GREATER) {  // correspond.c:308
    cmp = tumblercmp(&span1->width, &span2->width);              // correspond.c:309
    switch (cmp) {
      case EQUAL:
        *pairsetptr = makespanpair(taskptr,
            &spec1->docisa, &span1->stream,    // doc1, V-start1
            &spec2->docisa, &span2->stream,    // doc2, V-start2
            &span1->width);                    // width
        span1 = span1->next;    // correspond.c:317 — advance span1
        span2 = span2->next;    // correspond.c:316 — advance span2
        break;
      case LESS:
        // span1 is shorter: consume span1->width from span2, advance span1
      case GREATER:
        // span2 is shorter: consume span2->width from span1, advance span2
    }
    pairsetptr = &(*pairsetptr)->nextspanpair;  // correspond.c:344
}
```

This is a **single pass** where `span1` and `span2` each move forward. There is no outer-inner nesting that would pair every element of `span1` against every element of `span2`. The algorithm enforces a strict sequential one-to-one matching in I-address order.

---

### Self-comparison result

Suppose the document has V-spans `[V1=(stream=s1,width=w1), V2=(stream=s2,width=w2)]` (e.g., from a copy that placed the same content at two V-locations). After restriction, both `specset1` and `specset2` hold:

```
vspanset = [V1, V2]
```

The zipper iterates:

| Iteration | span1 | span2 | cmp   | Pair produced         |
|-----------|-------|-------|-------|-----------------------|
| 1         | V1    | V1    | EQUAL | (doc.s1, doc.s1, w1)  |
| 2         | V2    | V2    | EQUAL | (doc.s2, doc.s2, w2)  |

The off-diagonal pair `(doc.s1, doc.s2, w1)` is **never computed**. The zipper advances `span1` and `span2` symmetrically — V1 is consumed before the algorithm ever points `span2` at V2 while `span1` still points at V1.

`makespanpair` packs the result as a full tumbler (`docidandvstream2tumbler`, `correspond.c:357`):

```c
docidandvstream2tumbler(doc1, start1, &spanpair->stream1);   // correspond.c:357
docidandvstream2tumbler(doc2, start2, &spanpair->stream2);   // correspond.c:358
movetumbler(width, &spanpair->widthofspan);                  // correspond.c:359
```

For the diagonal pairs, `stream1 == stream2` and `widthofspan == original V-span width`.

---

### Answer

**`correspond.c` produces neither the trivial single identity pair covering the whole span, nor the off-diagonal cross-pairs. It produces one pair per V-span segment at POOM bottom-crum granularity, and those pairs are strictly diagonal.**

Specifically:

1. **Not a single covering pair.** The algorithm does not aggregate; it emits one `typespanpair` node per V-span chunk processed by the zipper.

2. **One pair per POOM bottom crum (or per V-span segment after V→I→V round-trip).** The granularity is determined by what `ispan2vspanset` → `permute` → `span2spanset` → `retrieverestricted` returns from the POOM (`orglinks.c:404–421`, `retrie.c:56–85`). Each bottom crum of the POOM yields one V-span; those are the units the zipper consumes.

3. **No off-diagonal pairs from within-document shared I-addresses.** If content was copied (V1 and V2 both holding the same I-content), the restricted specsets contain both V-spans, but the zipper's sequential advancement pairs V1↔V1 and V2↔V2 exclusively. The cross-pairs (V1↔V2, V2↔V1) are mathematically valid correspondences (the copied content does share an I-origin), but `makespanpairsforispan` is architecturally incapable of emitting them: there is no code path that rewinds `span2` to pair an already-consumed `span2` element against a later `span1`. See `correspond.c:308–344`.

The off-diagonal pairs would require a full Cartesian product over the V-spans that share an I-address — that is not how `makespanpairsforispan` is structured. The function is designed for the inter-document case (where V-spans from document A are mapped against V-spans from document B via a shared I-space), and it assumes the mapping is injective in I-address order on both sides. Self-comparison exercises only the diagonal of that mapping.
