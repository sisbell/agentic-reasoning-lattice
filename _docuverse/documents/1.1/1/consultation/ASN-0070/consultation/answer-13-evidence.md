## Question 13 [evidence]

> When an endset's I-span maps to multiple V-positions in the target document (due to self-transclusion creating multiple POOM entries pointing at the same I-addresses), does `incontextlistnd` return all V-positions or only the first one encountered during 2D tree traversal?

## KB Synthesis

## All V-positions are returned.

The KB provides a direct answer through the interaction of three mechanisms:

**1. `findcbcinarea2d()` is exhaustive** [SS-POOM-MULTIMAP]

The 2D tree traversal "iterates siblings, recurses into subtrees" at every level, accumulating **every** matching leaf node. There is no early-exit on first match — the traversal is designed to find all crums whose I-address dimension (ORGLRANGE) falls within the query range, regardless of how many V-positions reference that I-address.

**2. `incontextlistnd()` never replaces** [SS-POOM-MULTIMAP], [SS-CONTEXT-LIST]

The accumulation function inserts each discovered context into a sorted linked list via insertion-sort. The code path "never replacing existing entries" is explicit — it is an insert-at-position, not an upsert. Every qualifying leaf node from the traversal gets its own entry.

**3. The POOM is a multimap by design** [SS-POOM-MULTIMAP]

The concrete example in the KB directly addresses self-transclusion:

```
Document has "B" at V-positions 1.2, 1.4, and 1.5, all referencing I-address i_B.

ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}

Result set cardinality = 3
```

---

**Downstream consequence for endset retrieval:**

When FOLLOWLINK calls `linksporglset2specset()` → `span2spanset()` → `retrieverestricted()`, the I-address query hits the POOM multimap and returns all V-positions. So for a link whose endpoint I-addresses appear at N locations in the target document (due to N-fold self-transclusion), the returned specset contains N V-spans. [SS-FOLLOWLINK], [SS-SPORGL]

This is why [EC-MULTISPAN-LINK-DUPLICATION] observes that `retrieve_endsets` can return "duplicate" spans — when transcluded content appears multiple times, the endset faithfully reports all of them. The result is sorted by V-position [INV-RETRIEVAL-V-SORTED] and independent of internal tree structure [INV-RETRIEVAL-TREE-INDEPENDENCE].

---

## Code Exploration

I now have everything I need. Let me synthesize the full answer.

---

## Answer: `incontextlistnd` Accumulates ALL V-Positions — None Are Dropped

### The Call Chain for I→V Mapping (Self-Transclusion Case)

When an endset's I-span is permuted to V-positions, the path is:

```
ispan2vspanset [orglinks.c:389]
  → permute [orglinks.c:404]
    → span2spanset [orglinks.c:425]
      → retrieverestricted(orgl, ispanptr, I, NULL, V, NULL) [retrie.c:56]
        → retrieveinarea [retrie.c:87]
          → findcbcinarea2d [retrie.c:97]
            → incontextlistnd [retrie.c:263]
```

For link-following specifically, `link2sporglset` [sporgl.c:67] calls:

```c
retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)
```
[sporgl.c:83] — restricting on V to find the endset's I-span.

### `findcbcinarea2d` Walks the Entire Tree — No Early Exit

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {       // retrie.c:252
    if (!crumqualifies2d(...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson(...), &localoffset, ...); // recurse ALL branches
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
        incontextlistnd(headptr, context, index1);            // retrie.c:263
    }
}
```

The outer loop advances through siblings via `getrightbro`, and internal nodes recurse into **all qualifying children**. There is no `break` anywhere in this traversal. Every qualifying leaf crum calls `incontextlistnd`.

Compare this to `findcbcnd` [retrie.c:208], which **does** early-exit:

```c
for (ptr = findleftson((typecuc*)father); ptr; ptr = getrightbro(ptr))
    if (retr = findcbcnd(ptr, &grasp, address, index))
        break;    // retrie.c:221 — STOPS AT FIRST MATCH
```

But `findcbcnd` is called only from `retrieve()` [retrie.c:44-45], not from `retrieverestricted`. It never calls `incontextlistnd` — it returns a single context directly. The two code paths are entirely separate.

### `incontextlistnd` Is a Sorted Insert — Unconditional

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)   // context.c:75
{
    prologuecontextnd(c, &grasp, (typedsp*)NULL);   // get start position of c
    c->nextcontext = NULL;
    clist = *clistptr;
    if (!clist) { *clistptr = c; return(0); }       // 1st insertion: always inserts
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist; *clistptr = c; return(0);  // beginning
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext(clist, ...) > ONMYLEFTBORDER)
             && (whereoncontext(nextc, ...) < ONMYLEFTBORDER)) {
                c->nextcontext = nextc; clist->nextcontext = c; return(0);  // middle
            }
        }
    }
    c->nextcontext = NULL; clist->nextcontext = c;  // end: always inserts
}
```

There is no guard for duplicate addresses and no early return that could skip an insertion. The function unconditionally inserts `c` into the sorted linked list at the correct position. Sorting is by the V-coordinate of each context's start tumbler (when `index` is `V`), determined via `whereoncontext` [context.c:124] → `intervalcmp`.

### What Happens With Self-Transclusion

In a self-transclusion scenario, the POOM enfilade for a document contains multiple leaf crums with:
- The **same I-address range** (same content origin)
- **Different V-positions** (because the content was inserted at multiple V-slots)

When `findcbcinarea2d` traverses the POOM restricted to a given I-span:
1. `crumqualifies2d` [retrie.c:270] passes for all crums whose I-range intersects the query I-span, regardless of their V-position
2. For each qualifying leaf, `incontextlistnd` adds a new context node to `headptr`
3. The resulting `context` linked list contains **one entry per matching crum**, each with a distinct V-position

This is then consumed by the caller:

```c
for (c = context; c; c = c->nextcontext) {       // span2spanset: orglinks.c:439
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typeitem *)onitemlist(taskptr, (typeitem*)&foundspan, targspansetptr);
}
```

All contexts are converted to spans. `onitemlist` [orglinks.c:464] appends each to the result list.

### Conclusion

**`incontextlistnd` returns all V-positions, not just the first one.**

- `incontextlistnd` itself is a pure sorted-insert with no duplicate-drop logic [context.c:75–111].
- `findcbcinarea2d` — the only caller of `incontextlistnd` — exhaustively walks all siblings and all recursive branches of the POOM tree with no early termination [retrie.c:252–265].
- The resulting context list is fully iterated by every consumer in the I→V or V→I permutation path.

The single-match behavior lives in `findcbcnd` [retrie.c:208] via `retrieve()` — an entirely separate code path used only for point-address lookups, not for span permutation or link following.
