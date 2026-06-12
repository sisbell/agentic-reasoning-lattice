## Question 18 [evidence]

> If document A's shared content has been rearranged so that a single contiguous I-span in B maps to multiple non-contiguous V-positions in A, does the operation fragment the correspondence into multiple pairs, and is the fragmentation count equal to the number of POOM bottom crums covering that I-span?

## KB Synthesis

## Fragmentation of `compare_versions` After Rearrangement

Yes, the correspondence fragments. The fragmentation count equals the number of POOM bottom crums covering that I-span in document A after the rearrangement. Here is the chain of evidence.

---

### The Core Mechanism: POOM as a Multimap

[SS-POOM-MULTIMAP] establishes the key structural fact: the POOM is not a bijection — it is a multimap. A single I-address range can map to **multiple distinct V-positions** in the same document. `ispan2vspanset` returns a `Set<VSpan>`, not a single value. `findcbcinarea2d()` walks all qualifying subtrees and accumulates every matching leaf node via `incontextlistnd`, producing one context per contiguous V-region found.

### How `compare_versions` Uses This

[SS-COMPARE-VERSIONS] and [INT-SPORGL-VERSION-COMPARE] describe the operation:

1. Both documents' V-spans are converted to sporgls (I-address + provenance) via `vspanset2sporglset`
2. I-span intersection identifies shared content
3. Intersection ranges are mapped **back** to V-spans in each document via `linksporglset2specset` → `span2spanset` → `retrieverestricted`

Step 3 uses the same `ispan2vspanset` path that is a multimap query. If document A has the shared I-span mapped to N non-contiguous V-regions, step 3 produces N separate V-spans for document A's side of each pair.

### Why Rearrangement Creates the Non-Contiguity

[INV-REARRANGE-IDENTITY] and [ST-REARRANGE] (Finding 0056) confirm: rearrangement modifies only `cdsp.dsas[V]` (V-address displacements). I-addresses are completely untouched. What was one contiguous `[V-range → I-range]` crum can be split by Phase 1 cutting at pivot boundaries (via `slicecbcpm`, which `whereoncrumm == THRUME` triggers per [PRE-DELETE]), producing two crums covering sub-ranges of the original I-span. Phase 2 then applies different V-displacement offsets to each piece, scattering them to non-contiguous V-positions.

After the rearrangement, the bottom crums covering the I-span are at disjoint V-positions. There is no mechanism to merge them back: `isanextensionnd` [ST-INSERT, Finding 0062] only coalesces during *new insertions* at a crum's right boundary, not retroactively after rearrangement.

### The Fragmentation Count

[INV-RETRIEVAL-V-SORTED] ensures `incontextlistnd` inserts each discovered crum into a V-sorted linked list. Each bottom crum covering the I-span produces exactly one entry. Adjacent crums contiguous in V-space would be consolidated [INV-VSPAN-CONSOLIDATION], but rearrangement deliberately introduces non-contiguity, so consolidation does not apply.

Therefore: **the number of correspondence pairs equals the number of POOM bottom crums covering the I-span in document A**.

This is structurally identical to the fragmentation observed in link endsets after pivot, documented in [EC-PIVOT-LINK-FRAGMENTATION]:

> When linked content is rearranged via pivot, the link's endsets become fragmented into multiple spans

The mechanism is the same because `retrieve_endsets` and `compare_versions` both bottom out in `ispan2vspanset` → `span2spanset` → `retrieverestricted`.

---

### Concrete Example

Before pivot in document A (single crum):
```
Crum: V[1.3..1.8) → I[α₁..α₆]
Document B: V[1.1..1.6) → I[α₁..α₆]  (contiguous, unchanged)
compare_versions → 1 pair: (A: 1.3 for 0.5, B: 1.1 for 0.5)
```

After pivot in A with cut at V 1.6 (Phase 1 slices crum, Phase 2 shifts α₁..α₃):
```
Crum_a: V[1.9..1.12) → I[α₁..α₃]   (shifted to end)
Crum_b: V[1.3..1.6)  → I[α₄..α₆]   (stayed in place)
compare_versions → 2 pairs:
  (A: 1.3 for 0.3, B: 1.4 for 0.3)   ← α₄..α₆
  (A: 1.9 for 0.3, B: 1.1 for 0.3)   ← α₁..α₃
```

Two crums covering the I-span → two pairs.

---

### Caveat: Not Directly Confirmed in KB for `compare_versions`

The KB establishes the fragmentation claim by synthesis across [SS-POOM-MULTIMAP], [SS-COMPARE-VERSIONS], [INT-SPORGL-VERSION-COMPARE], [ST-REARRANGE], and [EC-PIVOT-LINK-FRAGMENTATION]. No finding directly states "compare_versions fragments equal to crum count after rearrangement." If the answer matters for a formal spec, an empirical finding targeting this specific scenario (INSERT + REARRANGE + compare_versions) would be needed to confirm the crum count claim precisely.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Yes — Fragmentation Is Real and the Count Is Exact

The correspondence produced by `doshowrelationof2versions` does fragment into one pair per POOM bottom crum in A that covers the shared I-span. The mechanism is a direct consequence of how `findcbcinarea2d` reports crums, and how the zipper in `makespanpairsforispan` consumes them. Every link in the chain is traceable.

---

### How Rearrangement Creates Multiple Crums

`dorearrange` [do1.c:34] → `rearrangepm` [orglinks.c:137] → `rearrangend` [edit.c:78].

`rearrangend` calls `makecutsnd` at the V-cut positions [edit.c:110], which splits any existing crum that straddles a cut into two crums along the V axis. It then applies a per-section offset to each crum's `cdsp.dsas[V]`:

```c
/* edit.c:125 */
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);
ivemodified((typecorecrum*)ptr);
```

The I-coordinates of those crums are untouched. After a rearrange of A, the single crum that originally mapped [I₀, I₀+w] to a contiguous [V₀, V₀+w] is replaced by N crums, each covering an I-sub-interval [I₀+wₖ₋₁, I₀+wₖ], each displaced to a different, non-contiguous V-position. N equals the number of V-cuts that passed through that original crum.

---

### V → I Conversion: One Context Per Crum

`specset2ispanset` [do2.c:14] calls `vspanset2ispanset` [orglinks.c:397], which calls `permute(V→I)` [orglinks.c:404], which calls `span2spanset` for each input V-span:

```c
/* orglinks.c:435 */
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                      (typeitemset*)targspansetptr);
}
```

`retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229]. The critical loop:

```c
/* retrie.c:252-264 */
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, ...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);
    }
}
```

Every qualifying **bottom crum** (`height == 0`) produces exactly one `typecontext` entry appended to the list via `incontextlistnd` [context.c:75]. The list is sorted by the restriction-dimension coordinate. There is no merging at this stage.

`context2span` [context.c:176] clips each context's I-range to the intersection with the restriction V-span and returns one `typespan`. `onitemlist` [orglinks.c:464] appends — it does not merge spans.

**Result for A**: N I-sub-spans, one per crum, in I-order. B's single crum produces one I-span [I₀, I₀+w].

---

### Intersection Preserves the N-way Split

`intersectspansets` [correspond.c:145]:

```c
/* correspond.c:177-182 */
for (; set1; set1 = set1->next) {       /* B: 1 entry [I₀, I₀+w] */
    for (p = set2; p; p = p->next) {    /* A: N entries            */
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
```

B's single I-span [I₀, I₀+w] intersected with each of A's N contiguous sub-spans gives exactly N sub-spans back. The outer loop runs once; the inner loop runs N times; `comparespans` [correspond.c:191] calls `spanintersection` [correspond.c:210] which computes the non-empty overlap for each, producing N entries in `commonispans`.

---

### Restriction Builds One V-Span List Per Document

`restrictvspecsetovercommonispans` [correspond.c:52] calls `ispan2vspanset` [orglinks.c:389] → `permute(I→V)` [orglinks.c:404] which walks the full `ispanset` list (all N common I-sub-spans) in one pass:

```c
/* orglinks.c:414-416 */
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, ...);
}
```

For B: N I-sub-spans → N contiguous V-sub-spans (B was not rearranged).  
For A: N I-sub-spans → N non-contiguous V-spans at the rearranged positions.

Both results are stored as a single `typevspec` with a linked `vspanset` of N entries.

---

### The Zipper Produces Exactly One Pair Per Sub-Span

`makespanpairset` [correspond.c:267] iterates over the N common I-sub-spans. For each it calls `makespanpairsforispan` [correspond.c:290], which is a zipper of the two V-span lists:

```c
/* correspond.c:308-329 */
while (span1 && span2 && tumblercmp (iwidth, &sum) == GREATER) {
    cmp = tumblercmp (&span1->width, &span2->width);
    switch (cmp) {
      case EQUAL:
        *pairsetptr = makespanpair (taskptr, &spec1->docisa, &span1->stream,
                                    &spec2->docisa, &span2->stream, &span1->width);
        ...
        span1 = span1->next;
        span2 = span2->next;
```

Because A's rearrangement preserves I-widths per crum (the crum is only moved in V, not resized), each I-sub-span has the same width as the corresponding V-spans in both B and A. The zipper's EQUAL branch fires once per sub-span, consuming one entry from each list and emitting one `typespanpair`. The `pairsetptr` advances at [correspond.c:344]:

```c
pairsetptr = &(*pairsetptr)->nextspanpair;
```

After N iterations of `makespanpairset`'s outer loop: **N pairs total**.

---

### Summary

| Stage | Source | Per-crum count |
|-------|--------|---------------|
| `rearrangend` creates N crums in A | edit.c:110 | 1 crum per V-cut crossing |
| `findcbcinarea2d` yields N contexts | retrie.c:262-263 | 1 context per bottom crum |
| `span2spanset` yields N I-sub-spans | orglinks.c:439-444 | 1 span per context |
| `intersectspansets` yields N common spans | correspond.c:177-182 | 1 intersection per A-sub-span |
| `makespanpairsforispan` yields N pairs | correspond.c:308-344 | 1 pair per common I-sub-span |

**Yes** — the correspondence is fragmented into multiple pairs.

**Yes** — the fragmentation count equals the number of POOM bottom crums in A's orgl whose I-range intersects the shared I-span. Each such crum contributes exactly one `typecontext` from `findcbcinarea2d` [retrie.c:263], exactly one I-sub-span from `context2span` [context.c:176], exactly one intersection from `comparespans` [correspond.c:191], and exactly one `typespanpair` from `makespanpair` [correspond.c:351].

The only caveat: if B itself has more than one crum covering [I₀, I₀+w] (e.g. B was also assembled from parts), the total pair count is determined by the union of both documents' sub-spans after `intersectspansets`, which is max(count\_B, count\_A) or more in pathological overlap cases. For the stated premise — one contiguous I-span in B, N crums in A — the count is exactly N.
