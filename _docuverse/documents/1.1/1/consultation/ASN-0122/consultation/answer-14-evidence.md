## Question 14 [evidence]

> What determines the ordering of returned correspondence pairs — V-address order in the first specset, V-address order in the second, or I-address order from the traversal of the underlying enfilades?

## KB Synthesis

The KB does not expose the exact loop structure of `correspond.c`, but the ordering can be reasoned from several converging sources.

## What the KB Says Directly

**[SS-COMPARE-VERSIONS]** describes the algorithm as "a nested loop computing I-span intersections and mapping back to V-spans." The algorithm flow is: retrieve V-spans from both documents → convert to I-spans → intersect on I-address → map back to V-spans.

**[INV-RETRIEVAL-V-SORTED]** establishes that POOM retrieval (`incontextlistnd`) always produces results sorted by V-address in the queried document, regardless of tree structure or traversal order. This is the mechanism that produces the I-span inputs to the intersection loop.

**[SS-CONTEXT-LIST]** confirms POOM (2D) queries yield `SortedSeq<Context>` with a V-sorted invariant; sequential GRAN queries yield tree-traversal order.

## What the Concrete Examples Show

**[ST-INSERT]** (Finding 0030) gives a direct example:
```
compare_versions returns:
  [{version_before: 1.1 for 0.2, current: 1.1 for 0.2},   // "AB"
   {version_before: 1.3 for 0.3, current: 1.5 for 0.3}]   // "CDE"
```

**[SS-COMPARE-VERSIONS]** (Finding 0015) gives another:
```
[(A: V 1.1 for 5, B: V 1.1 for 5),    // "Hello"
 (A: V 1.6 for 6, B: V 1.11 for 6)]   // "World"
```

Both examples show pairs ordered by **ascending V-address in the first document** — the A/`version_before` position advances monotonically.

## The Conclusion

The ordering is V-address order in the first specset's document. The chain works as follows:

1. The POOM retrieval for each document yields I-spans in V-sorted order of that document [INV-RETRIEVAL-V-SORTED].
2. For the first document, V-order and I-order are aligned: I-addresses are allocated monotonically [INV-MONOTONIC], so earlier V-positions (older insertions) map to lower I-addresses, and POOM retrieval returns them in ascending I-address order.
3. The nested loop in `correspond.c` processes the first document's I-spans in this V/I-order and finds the corresponding I-address range in the second document for each.
4. The result list therefore advances in V-address order of the first document.

One important caveat the KB flags: **[PRE-COMPARE-VERSIONS]** notes that `correspond.c` has no subspace filtering, and **[EC-COMPARE-VERSIONS-LINK-CRASH]** notes the operation crashes when link-subspace spans are included. If link spans are present, the I-address types are incompatible (link orgl ISAs vs. permascroll addresses) and the nested loop's assumption of at-most-one-match-per-ispan is violated — so the ordering question is moot in that case, and the operation aborts.

---

## Code Exploration

I have all I need. Let me now compose the full answer by synthesizing the complete call chain.

---

## Ordering of Correspondence Pairs in `doshowrelationof2versions`

The short answer: **V-address order of the first specset drives the output order.** The I-address traversal of the underlying enfilade is internally resorted before it can influence ordering, and the second specset's V-addresses follow as a dependent consequence.

Here is the complete traced path.

---

### Entry point

`fns.c:250-261` — `showrelationof2versions` calls `doshowrelationof2versions`, which calls `putshowrelationof2versions`, which calls `putspanpairset` (`putfe.c:222-231`). The serialization loop is a plain linked-list walk with no resorting:

```c
for (; spanpairset; spanpairset = spanpairset->nextspanpair)
    putspanpair (taskptr, spanpairset);
```

So whatever order the pair list is in when `makespanpairset` finishes is the order the client receives. **No reordering at output time.**

---

### Building `commonispans` — the spine of the pair ordering

`do1.c:428-449` — `doshowrelationof2versions`:

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)
&&    specset2ispanset(taskptr, version2, &version2ispans, READBERT)
&&    intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&&    ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

#### Step 1: `specset2ispanset` — how is `version1ispans` ordered?

`specset2ispanset` (`do2.c:34-36`) calls `vspanset2ispanset` (`orglinks.c:389-393`) which calls:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

`permute` (`orglinks.c:404-422`) iterates over the input V-spans, calling `span2spanset` for each. Inside `span2spanset` (`orglinks.c:425-454`):

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`restrictionindex=V`, `targindex=I`. The context list comes from `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (`retrie.c:229-268`). The bottom-level crums found are inserted via:

```c
incontextlistnd (headptr, context, index1);   /* retrie.c:263 */
```

where `index1 = restrictionindex = V`. In `context.c:75-111`, `incontextlistnd` does a **sorted insertion by the `index` dimension** — in this case, **V**:

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    ...
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        /* on beginning */
        c->nextcontext = clist; *clistptr = c; return;
    }
    for (/* middle scan */) { ... insert in sorted position ... }
    /* on end */ clist->nextcontext = c;
}
```

The enfilade itself is traversed in structural left-to-right sibling order (`for (; crumptr; crumptr = getrightbro (crumptr))`, `retrie.c:252`), but **every context is re-inserted into the output list sorted by V**. The I-address traversal order of the POOM tree is therefore neutralised before it can propagate.

After `incontextlistnd`, each context is converted to an I-span via `context2span(..., V, ..., I)` and appended to the ispan list by `onitemlist` (`orglinks.c:444-445`), which is a plain append-to-tail loop:

```c
((typeitemheader *)temp)->next = (typeitemheader *)newitem;  /* orglinks.c:534 */
```

No sorting at append time either. The ispan list inherits its order from the V-sorted context list.

**Result: `version1ispans` is a list of I-spans ordered by V-address of version1.**

#### Step 2: `intersectspansets` — which order does `commonispans` inherit?

`correspond.c:145-188`:

```c
for (; set1; set1 = set1->next) {          /* outer: version1ispans */
    for (p = set2; p; p = p->next) {       /* inner: version2ispans */
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;
    }
}
```

Intersections are appended in the order of the **outer loop** (set1 = `version1ispans`). The inner loop (set2 = `version2ispans`) only controls whether a particular outer element produces an output entry.

**Result: `commonispans` is in V-address order of version1.**

---

### Building the pair list — `makespanpairset` and `makespanpairsforispan`

`do2.c:196-197`:
```c
restrictspecsetsaccordingtoispans(taskptr, ispanset, &specset1, &specset2);
makespanpairset (taskptr, ispanset, specset1, specset2, pairsetptr);
```

`correspond.c:267-288` — `makespanpairset`:

```c
for (; ispanset; ispanset = ispanset->next) {
    movetumbler (&ispanset->width, &iwidth);
    makespanpairsforispan (taskptr, &iwidth, &specset1, &specset2, &pairset);
    *pairsetptr = pairset;
    pairsetptr = &pairset->nextspanpair;
}
```

The **outer loop is over `ispanset` = `commonispans`**, in V-address order of version1. One pair is emitted per ispan.

Inside `makespanpairsforispan` (`correspond.c:290-348`), the logic is a zipper over span1 (specset1's V-spans) and span2 (specset2's V-spans):

```c
while (span1 && span2 && tumblercmp (iwidth, &sum) == GREATER) {
    cmp = tumblercmp (&span1->width, &span2->width);
    switch (cmp) {
      case LESS:
      case EQUAL:
        *pairsetptr = makespanpair (taskptr, &spec1->docisa, &span1->stream,
                                             &spec2->docisa, &span2->stream, &span1->width);
        ...
        span1 = span1->next;
        break;
      case GREATER:
        *pairsetptr = makespanpair (taskptr, &spec1->docisa, &span1->stream,
                                             &spec2->docisa, &span2->stream, &span2->width);
        ...
        span2 = span2->next;
    }
    pairsetptr = &(*pairsetptr)->nextspanpair;
}
```

`span1` advances monotonically through specset1's V-spans. `span2` advances in lockstep. Pairs are appended in consumption order. Since both span lists are in ascending V-address order (specset1 and specset2 are both V-ordered after `restrictspecsetsaccordingtoispans`), the output pairs are ordered by the V-address of `span1->stream`, which is the V-address of version1 (the first specset).

The width comparison at `correspond.c:309` only determines the *size* of each emitted pair — it never reverses or reorders the position-ordered walk through span1 and span2.

---

### Summary

| Stage | Function | Ordering established |
|-------|----------|----------------------|
| POOM traversal | `findcbcinarea2d` (`retrie.c:252`) | Structural tree order |
| Context insertion | `incontextlistnd` (`context.c:75`) | **Re-sorted by V-address** (index1) |
| I-span assembly | `span2spanset` (`orglinks.c:439`) | V-address order of the restriction spans |
| Common span intersection | `intersectspansets` (`correspond.c:177`) | **Outer loop = version1ispans order** |
| Pair emission | `makespanpairset` (`correspond.c:278`) | Iterates `commonispans` in its list order |
| Pair zipper | `makespanpairsforispan` (`correspond.c:308`) | V-address order of span1 (specset1) |
| Serialization | `putspanpairset` (`putfe.c:229`) | List order, unmodified |

**The ordering of returned correspondence pairs is determined by V-address order of the first specset (version1 as passed to `doshowrelationof2versions`).** The pairs are emitted in the order that span1 (version1's V-spans) is consumed by the zipper in `makespanpairsforispan`.

The I-address traversal order of the POOM enfilade does participate in the computation, but it is **overridden by `incontextlistnd`** (`context.c:75`), which re-sorts every retrieved context by the restriction dimension (V) before the contexts are converted to I-spans. By the time I-spans appear in `commonispans`, they have already been sorted into V-address order of version1, and I-address order plays no further role.

The second specset's V-address order is a dependent consequence: because both specsets are mapped through the same common I-spans, the pairs advance in version1's V-address order and version2's V-address order simultaneously — but version1's order is the primary, independent axis. Version2's order is whatever the I→V permutation of version2's POOM produces for the same I-ranges.
