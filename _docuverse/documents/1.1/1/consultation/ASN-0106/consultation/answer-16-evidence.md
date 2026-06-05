## Question 16 [evidence]

> If a requested span crosses a POOM crum boundary, does whereoncrum classification split it into multiple returned sub-fragments, and are those sub-fragments tagged with their I-addresses?

## KB Synthesis

## Cross-Crum Span Queries: Fragmentation and I-Address Tagging

**Short answer:** `whereoncrum` itself classifies a *single point*, not a range. When a requested V-span crosses crum boundaries, the B-tree traversal collects *multiple context entries*, one per qualifying crum, each carrying the crum's I-address. Higher-level functions then present these as separate I-spans.

---

### The Retrieval Mechanism

`whereoncrum` [SS-WHEREONCRUM] is a five-way point classifier — it determines where one address falls relative to one crum's interval `[grasp, reach)`. It does not itself handle spanning.

The actual cross-boundary work happens in `findcbcinarea2d()` [SS-POOM-MULTIMAP]:

> "traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees, accumulating every matching leaf node"

Every leaf (bottom crum) whose V-interval overlaps the query range contributes a separate context to the result. `incontextlistnd()` [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED] insertion-sorts these by V-left-boundary, producing an ordered list of fragments.

---

### I-Address Tagging

Yes — each fragment carries its own I-address. Each POOM bottom crum stores **dual-space coordinates** [SS-POOM-BOTTOM-CRUM]:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

When a context is accumulated from a leaf crum, it captures both the V-offset and the corresponding I-origin/width. The result list is thus a sequence of `(V-range, I-range)` pairs, sorted by V-position.

---

### What Higher Layers See

`vspanset2ispanset` (called via `permute` → `span2spanset` → `retrieverestricted`) [SS-VSPAN-TO-SPORGL, ST-LINK-CREATE Finding 0037] walks this context list and emits **one I-span per contiguous I-address region**. If two adjacent crums happen to map to contiguous I-addresses (normal sequential inserts), they may coalesce [INV-VSPAN-CONSOLIDATION]. If they map to non-contiguous I-addresses (content from different insertions or transclusions), they remain separate.

This is why [ST-LINK-CREATE] Finding 0037 observes:

> "a single user-visible V-span may correspond to multiple I-spans in the endset when the V-span covers content transcluded from multiple sources"

The `sporgl.c:49-58` inner loop creates one sporgl per I-span returned — preserving the fragmentation exactly as the crum structure dictates.

---

### Summary

| Layer | What happens at crum boundary |
|-------|-------------------------------|
| `whereoncrum` | Classifies one point; not relevant to spanning |
| `findcbcinarea2d` | Collects all overlapping crums as separate contexts |
| `incontextlistnd` | Sorts contexts by V-position |
| `retrieverestricted` / `permute` | Returns one I-span per contiguous I-address region |
| `vspanset2sporglset` | Packages each I-span as a tagged sporgl (I-addr + width + source doc) |

So: a query spanning N crums returns up to N I-address-tagged sub-fragments from retrieval, potentially consolidated if adjacent crums happen to have contiguous I-addresses [INV-VSPAN-CONSOLIDATION], but never merged across non-contiguous I-address regions [ST-LINK-CREATE Finding 0037].

---

## Code Exploration

---

## Answer

### Short Answer

`whereoncrum` is a **pure point-vs-interval classifier** — it does not split anything. The splitting into sub-fragments is done by the sibling traversal loop inside `findcbcinarea2d`. Yes, each resulting sub-fragment is tagged with its I-address.

---

### Detailed Trace

#### 1. `whereoncrum` — what it actually does

**`retrie.c:345–398`**:

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index)
{
  tumbler left, right;
  INT cmp;
    switch (ptr->cenftype) {
      case GRAN:
         tumbleradd (&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
         return (intervalcmp (&offset->dsas[WIDTH], &right, address));
      case SPAN:
      case POOM:
            tumbleradd(&offset->dsas[index],&ptr->cdsp.dsas[index], &left);
            cmp = tumblercmp(address,&left);
            if(cmp == LESS) return(TOMYLEFT);
            else if(cmp == EQUAL) return(ONMYLEFTBORDER);
            tumbleradd (&left, &ptr->cwid.dsas[index], &right);
            cmp = tumblercmp(address,&right);
            if(cmp == LESS) return(THRUME);
            else if (cmp == EQUAL) return(ONMYRIGHTBORDER);
            else return(TOMYRIGHT);
    }
}
```

For a POOM crum with `index = I` (`wisp.h:19: #define I 0`) or `index = V` (`wisp.h:20: #define V 1`):

- `left = offset->dsas[index] + crum->cdsp.dsas[index]` — absolute start of this crum in the selected dimension
- `right = left + crum->cwid.dsas[index]` — absolute end
- Returns one of the five codes defined at `common.h:86–90`: `TOMYLEFT (−2)`, `ONMYLEFTBORDER (−1)`, `THRUME (0)`, `ONMYRIGHTBORDER (+1)`, `TOMYRIGHT (+2)`

`whereoncrum` classifies **one address against one crum in one dimension**. It has no knowledge of spans, it returns no fragments, and it modifies no state.

---

#### 2. `crumqualifies2d` — span-vs-crum overlap test

**`retrie.c:270–305`** calls `whereoncrum` four times — once per endpoint per dimension:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);           // span ends before crum starts

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);                  // span starts after crum ends

endcmp = ... whereoncrum(crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return(FALSE);

startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return(FALSE);
```

This is a pure predicate. It does not create fragments.

---

#### 3. `findcbcinarea2d` — where the splitting happens

**`retrie.c:229–268`**:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {
    if (!crumqualifies2d(crumptr, offsetptr, span1start, span1end, index1,
                         span2start, span2end, index2, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);  // retrie.c:263
    }
}
```

The loop walks every sibling crum via `getrightbro`. For each non-leaf, it descends. For each **leaf** (`height == 0`) that passes `crumqualifies2d`, it calls `makecontextfromcbc` and appends to the result list.

**Consequence**: if a requested span overlaps N leaf crums, the loop produces N separate `typecontext` objects. The span is not tracked as a unit — each crum-boundary crossing causes a new fragment.

---

#### 4. `makecontextfromcbc` — I-address tagging

**`context.c:151–174`**:

```c
typecontext *makecontextfromcbc(typecbc *crumptr, typewid *offsetptr)
{
    context = createcontext(crumptr->cenftype);
    movewisp(offsetptr, &context->totaloffset);           // line 160: copy accumulated offset
    movewisp(&crumptr->cwid, &context->contextwid);       // line 161: copy width
    if (is2dcrum((typecorecrum*)crumptr))
        move2dinfo(&((type2dcbc*)crumptr)->c2dinfo, &((type2dcontext*)context)->context2dinfo);
    else
        moveinfo(&crumptr->cinfo, &context->contextinfo);
    if (crumptr->cenftype != GRAN)
        dspadd(&context->totaloffset, &crumptr->cdsp,
               &context->totaloffset, (INT)crumptr->cenftype); // line 167: add crum displacement
    ...
}
```

For a POOM crum:

- Line 160: `context->totaloffset` receives the accumulated offset from enfilade traversal
- Line 167: `cdsp` (the crum's own local displacement within its parent) is added in **both** I and V dimensions

The result: `context->totaloffset.dsas[I]` is the **absolute I-space start address** of this leaf crum. `context->contextwid.dsas[I]` is its I-space width. Together these define the I-span of the fragment.

`incontextlistnd` (`context.c:75–111`) inserts the new context into the result list in sorted `index1`-dimension order, using `whereoncontext` (which parallels `whereoncrum` but operates on already-built context objects).

---

#### 5. Clipping is deferred

The fragments at this stage represent **full crum extents**, not clipped sub-spans. Clipping to the requested span boundaries is applied later in `context2span` (`context.c:176–212`):

```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement(&grasp.dsas[idx2], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);   // advance I-start by overhang in V-dimension
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement(&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);   // shrink I-end by overhang
```

This clips the I-extent of the fragment proportionally to the overhang in the other dimension — a cross-dimensional adjustment meaningful for POOM's I↔V coupling.

---

### Conclusion

| Question | Answer |
|---|---|
| Does `whereoncrum` split a span crossing a crum boundary? | **No.** `whereoncrum` (`retrie.c:345`) is a pure 5-way point classifier. It returns a single integer. |
| What actually produces the split? | `findcbcinarea2d`'s sibling loop (`retrie.c:252–265`). One `typecontext` per qualifying leaf crum. |
| Are sub-fragments tagged with I-addresses? | **Yes.** `makecontextfromcbc` (`context.c:160,167`) sets `context->totaloffset.dsas[I]` to the absolute I-space start of each leaf crum. |
| Are fragments clipped to the requested span? | **Not at creation time.** Clipping is applied later in `context2span` (`context.c:176–212`). |

The enfilade traversal in `findcbcinarea2d` is the physical splitting mechanism. `whereoncrum` is only the predicate that `crumqualifies2d` uses to ask "does this crum overlap the requested span?" — called once per span endpoint per dimension, four times per crum visited.
