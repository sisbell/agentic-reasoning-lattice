## Question 19 [evidence]

> In self-transclusion (source and target ranges within the same document), does the I→V mapping via incontextlistnd correctly return all V-positions bound to the shared I-address, including overlapping copy ranges?

## KB Synthesis

**Yes — all V-positions are returned correctly, including overlapping copy scenarios.**

Three KB entries converge on this:

**The POOM is a multimap, not a function** [SS-POOM-MULTIMAP]. `findcbcinarea2d()` traverses *all qualifying subtrees* and `incontextlistnd()` accumulates every matching leaf into a sorted linked list *without replacing existing entries*. A query by I-address returns all V-positions referencing it. The test concrete example shows three V-positions (1.2, 1.4, 1.5) all referencing `i_B` — all three appear in the result.

**Overlapping transclusions share I-addresses at character granularity** [INV-IDENTITY-OVERLAP]. When two copy ranges overlap — whether the overlap is from a self-transclusion whose source and destination ranges intersect, or from two independent partial copies — the overlapping positions in the destination each receive the correct I-address from the source. The `ispan2vspanset` path then discovers all of them via the multimap traversal.

**The result is V-sorted and tree-structure-independent** [INV-RETRIEVAL-V-SORTED, INV-RETRIEVAL-TREE-INDEPENDENCE]. `incontextlistnd()` performs insertion-sort on V-address regardless of tree traversal order, so the ordering of results is stable even when the underlying B-tree's sibling order (determined by insertion history) doesn't match V-order.

The only caveat from [EC-SELF-TRANSCLUSION] is that comparing the overlapping region to itself via `compare_versions` returns it as shared, which is expected behavior — not a defect in the mapping.

---

## Code Exploration

---

## Analysis: Self-Transclusion and I→V Mapping via `incontextlistnd`

### Short answer

**Yes, `incontextlistnd` returns all V-positions.** No contexts are dropped. There is a sort-order anomaly in one specific case that does not affect completeness, but which deserves documentation.

---

### 1. What `docopy` produces in the POOM for self-transclusion

`docopy` [do1.c:45-65] chains: `insertpm` → `insertnd(…, V)` → `setwispupwards`.

`insertpm` [orglinks.c:100-131] iterates source I-spans and for each calls:
```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
[orglinks.c:130]

Each call to `insertnd` [insertnd.c:15] (via `doinsertnd` → `insertmorend` → `insertcbcnd`) creates a new POOM leaf node storing:
- `cdsp.dsas[I]` = source I-address
- `cdsp.dsas[V]` = target V-address
- `cwid.dsas[I]` = I-width, `cwid.dsas[V]` = V-width

After insertion, `setwispupwards` [insertnd.c:56-58, wisp.c:83] propagates updated bounding boxes to every ancestor. All internal POOM nodes therefore maintain bounding boxes that correctly encompass all their descendants' I-ranges and V-ranges simultaneously.

**Result**: After self-transclusion (copy from V-range A to V-range B within the same document), the POOM tree contains multiple leaf nodes sharing the same I-range but with distinct V-addresses:
- Original: I=[x, x+n] → V=[a, a+n]
- Copy 1:   I=[x, x+n] → V=[b, b+n]
- Copy 2:   I=[x, x+n] → V=[c, c+n]

---

### 2. The I→V mapping call chain

```
ispan2vspanset  [orglinks.c:389]
  → permute(…, I, …, V)  [orglinks.c:404]
    → span2spanset(…, restrictionindex=I, targindex=V)  [orglinks.c:425]
      → retrieverestricted(…, index1=I, span2ptr=NULL, index2=V)  [retrie.c:56]
        → retrieveinarea(…)  [retrie.c:87]
          → findcbcinarea2d(…, index1=I, index2=V)  [retrie.c:229]
```

In `retrieverestricted` [retrie.c:56-85], when `span2ptr` is NULL both bounds are zeroed:
```c
} else {
    tumblerclear (&span2start);   // retrie.c:74
    tumblerclear (&span2end);     // retrie.c:75
}
```
This suppresses any V-dimension restriction.

---

### 3. `findcbcinarea2d` is exhaustive for all I-matching nodes

`findcbcinarea2d` [retrie.c:252-265]:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, infoptr)){
        continue;
    }
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // sorted by I
    }
}
```

**Key**: the outer loop is `for (; crumptr; crumptr = getrightbro(crumptr))` — it visits ALL siblings, not just the one whose V-range contains the query point. The POOM is organized by V-space, so an I-query cannot prune branches by V; the code correctly does not try.

`crumqualifies2d` [retrie.c:270-305] checks the I restriction:
```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER) return(FALSE);
startcmp = whereoncrum (crumptr, offset, span1start, index1);
if( (startcmp > THRUME)) return(FALSE);
```
For the V restriction, since `span2end` is zero:
```c
endcmp = iszerotumbler (span2end) ? TOMYRIGHT : ...;  // always TOMYRIGHT — never rejects
```
So every node whose I-bounding-box overlaps the queried I-range qualifies, regardless of V-address.

Because internal nodes' I-bounding boxes encompass all descendants (maintained by `setwispupwards`), no branch containing a relevant leaf node is pruned. All leaf nodes with matching I-ranges are reached.

---

### 4. `incontextlistnd` — all contexts are inserted, with one sort-order caveat

Constants from `common.h:86-90`:
```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT       2
```

`incontextlistnd` [context.c:75-111] inserts context `c` (I-start = `grasp.dsas[I]`, from `prologuecontextnd`) into the sorted list by I-position. Three paths:

**Path A — "on beginning"** [context.c:90]:
```c
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
```
`< THRUME` = `< 0`, which is true for both `TOMYLEFT(-2)` and `ONMYLEFTBORDER(-1)`.

For self-transclusion: if the new context has the **same I-start** as the current list head, `whereoncontext(clist, &same_I_start, I)` returns `ONMYLEFTBORDER(-1)`, which satisfies `< 0`. The new context is **prepended**. ✓

Each successive copy of the same I-range also satisfies this test and is prepended, so the first-element case is always handled.

**Path B — "in middle"** [context.c:98-99]:
```c
if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
    && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
```
Condition 2 requires `< ONMYLEFTBORDER` = `< -1` = only `TOMYLEFT(-2)`.

**Sort-order anomaly**: if `nextc`'s I-start equals the new context's I-start, `whereoncontext(nextc, …)` returns `ONMYLEFTBORDER(-1)`, which is NOT `< -1`. The insertion before `nextc` is skipped. The loop exhausts and falls through to:

**Path C — "on end"** [context.c:108-110]:
```c
c->nextcontext = NULL;
clist->nextcontext = c;
```
The new context is appended **at the tail**, even if its I-start is identical to a context already in the middle of the list.

**The invariant violation**: Consider list `[C_a(I=1.3), C_b(I=1.3), C_d(I=1.7)]`. If C_b and a new C_c share I-start 1.3 but C_b was already in the middle when C_c is inserted (C_b's I-start = 1.3 is not equal to C_a's 1.3 for the "on beginning" test because C_a was already prepended ahead of it):

Actually let me be precise. The anomaly only occurs for the scenario where:
1. The list already contains a context at the beginning with I-start X
2. Another context with the same I-start X was inserted but ended up past it (because X is THRUME relative to some earlier element when the earlier element was the head)

In practice this means: when the first two or more contexts share the same I-start, they'll all go through Path A (prepend). But if a third context with the same I-start arrives AFTER a context with a LATER I-start was already prepended, the ordering can diverge. The full picture:

- Three copies with identical I-range I=[x,x+n], inserted in order C1, C2, C3:
  - Insert C1 into empty list: `[C1]`
  - Insert C2: `whereoncontext(C1, &x, I)` = `ONMYLEFTBORDER(-1) < 0` → Path A → `[C2, C1]`
  - Insert C3: `whereoncontext(C2, &x, I)` = `ONMYLEFTBORDER(-1) < 0` → Path A → `[C3, C2, C1]`

All three present. ✓

The anomaly manifests only when there is at least one context with a DIFFERENT, INTERMEDIATE I-start separating duplicates — a configuration that requires delete+reinsert operations or complex interleaving of copy operations. Even then, **no context is ever lost**: Path C always appends.

---

### 5. `context2span` correctly clips overlapping ranges

`context2span` [context.c:176-212] converts each context (a POOM leaf node's 2D extent) to a V-span within the I-restriction:

```c
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement (&grasp.dsas[idx2], 0,
                      (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
                      &grasp.dsas[idx2]);
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement (&reach.dsas[idx2], 0,
                      - tumblerintdiff (&reach.dsas[idx1], &upperbound),
                      &reach.dsas[idx2]);
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```
[context.c:194-207]

`idx1=I`, `idx2=V`. If a leaf node's I-range extends beyond the queried bounds on either side, the corresponding V-start/end is adjusted proportionally. For partially overlapping copy ranges this yields the exact sub-V-span that corresponds to the queried I-range. ✓

---

### 6. Why all V-positions survive to the caller

`span2spanset` [orglinks.c:439-453] iterates the context list linearly:
```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

This is a simple linked-list walk — it visits every element, including any tailing elements appended by Path C. The sort-order anomaly causes no missed entries here.

---

### Conclusion

`ispan2vspanset` via `incontextlistnd` **correctly returns all V-positions bound to a shared I-address in self-transclusion**, including overlapping copy ranges. The reasoning:

1. **`docopy` / `insertpm` / `insertnd`** [do1.c:45, orglinks.c:75, insertnd.c:15]: each copy inserts a new POOM leaf node with the same I-range and a distinct V-address. `setwispupwards` ensures internal node bounding boxes cover all leaves.

2. **`findcbcinarea2d`** [retrie.c:229]: walks ALL siblings at every level. The zeroed V-restriction means `crumqualifies2d` admits all nodes overlapping the I-query. No copy is pruned from the tree walk.

3. **`incontextlistnd`** [context.c:75]: inserts every context. No context is ever discarded — they go to the head (Path A), middle (Path B), or tail (Path C). The **sort-order anomaly** (Path C places a duplicate-I-start context at the tail rather than adjacent to its I-duplicate) does NOT affect completeness.

4. **`context2span`** [context.c:176]: clips each context to the I-restriction, computing the correct V-span for partial overlaps.

5. **`span2spanset`** [orglinks.c:439]: linear iteration — visits all contexts including out-of-order tail entries.

**One warning**: any consumer of the raw `typecontext *` list returned by `retrieverestricted` that assumes the list is strictly sorted by I-start (for binary search or early termination) would miss entries in the anomalous case. The existing `span2spanset` uses a full linear scan and is safe. New code touching the context list should not assume sorted order when I-duplicates are possible.
