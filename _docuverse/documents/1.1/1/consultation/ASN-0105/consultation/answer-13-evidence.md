## Question 13 [evidence]

> When the read span straddles two non-contiguous I-spans (e.g., text split by the CREATELINK allocation gap), does the result preserve V-order via `incontextlistnd`'s insertion-sort, or does it reflect I-address ordering?

## KB Synthesis

**V-order is preserved via `incontextlistnd`'s insertion-sort, regardless of I-address ordering.**

Here is the full trace:

**The CREATELINK gap scenario** [INT-LINK-INSERT, EC-LINK-INSERT]:
`INSERT "ABC"` allocates I.1–I.3. `CREATELINK` consumes I-address space via `createorglingranf`. `INSERT "DEF"` allocates I.2.1+ (non-contiguous with "ABC"). In V-space, "ABCDEF" is contiguous. In I-space, two disjoint I-spans with a link-orgl gap between them.

**Retrieval path through the POOM** [INV-RETRIEVAL-V-SORTED, SS-CONTEXT-LIST]:
`specset2ispanset` calls `permute` → `findcbcinarea2d()`, which traverses the POOM B-tree discovering both bottom crums. Crums are found in tree-sibling order, which is NOT guaranteed to be V-order (due to the 2D diagonal rebalancing in [ST-REBALANCE-2D]).

Each discovered leaf is fed to `incontextlistnd()`, which performs **insertion-sort by `totaloffset.dsas[V]`** — the V-dimension left boundary. The result list is sorted by V-address regardless of discovery order or I-address values.

**Consequence**:
- Context for "ABC" (V: 1.1–1.3 → I.1–I.3) appears first in the sorted list
- Context for "DEF" (V: 1.4–1.6 → I.2.1–I.2.3) appears second
- `ispanset2vstuffset` then retrieves bytes from the permascroll in that order → yields "ABCDEF"

**Contrast with GRAN**: [SS-CONTEXT-LIST] notes that `oncontextlistseq` (used for 1D GRAN enfilades) appends in tree-traversal order without sorting — because GRAN tree structure guarantees sequential order already. The POOM uses `incontextlistnd` precisely *because* 2D tree structure does not preserve V-order.

**This is also tree-structure-independent** [INV-RETRIEVAL-TREE-INDEPENDENCE]: splits, rebalances, and diagonal ordering of siblings cannot change the sorted result.

**Summary**: The I-address gap from CREATELINK is invisible to retrieval. The POOM returns two disjoint I-spans, sorted by their V-positions, yielding content in correct reading order.

---

## Code Exploration

I now have a complete trace. Here is the full answer.

---

## Answer: V-Order, Not I-Address Order

The retrieval pipeline explicitly sorts results by V-address. Here is the full execution trace with citations.

---

### Call Chain

**Entry point — `doretrievev`** [`do1.c:338`]:
```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
  return
     specset2ispanset (taskptr, specset, &ispanset, READBERT)
  && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```
The V-spec is converted to I-spans first, then the I-spans are used to retrieve content.

---

**`specset2ispanset`** [`do2.c:14`] — for a `VSPECID` entry calls `vspanset2ispanset`:
```c
vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
```

---

**`vspanset2ispanset`** [`orglinks.c:397`] — calls `permute` with `V` as the restriction index and `I` as the target index:
```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
// (note: the visible call is vspanset2ispanset → permute(taskptr, orgl, vspanptr, V, ispansetptr, I))
```
Concretely [`orglinks.c:401`]:
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```

---

**`permute`** [`orglinks.c:404`] iterates over each input V-span and calls `span2spanset`:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, restrictionindex, targspansetptr, targindex);
}
```

---

**`span2spanset`** [`orglinks.c:425`] — calls `retrieverestricted` with `restrictionindex=V`, `targindex=I`:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
```
[`orglinks.c:435`]

---

**`retrieverestricted`** [`retrie.c:56`] → **`retrieveinarea`** [`retrie.c:87`] → **`findcbcinarea2d`** [`retrie.c:97`], all passing `index1=V` and `index2=I` through unchanged.

---

### The Critical Line

**`findcbcinarea2d`** [`retrie.c:229`], at line **263**:
```c
context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd (headptr, context, index1);   // index1 = V
```

`incontextlistnd` is called with `index = V`.

---

### What `incontextlistnd` Does

**`incontextlistnd`** [`context.c:75`]:
```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  typecontext *clist, *nextc;
  typedsp grasp;

    prologuecontextnd (c, &grasp, (typedsp*)NULL);   // grasp = c's absolute offsets (V and I)
    ...
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
        // insert at beginning
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
              && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
                // insert in middle
            }
        }
    }
    // append at end
```
[`context.c:80–111`]

`grasp.dsas[index]` with `index=V` is the **V-address of the new context**. `whereoncontext` computes `left = ptr->totaloffset.dsas[V]`, `right = left + ptr->contextwid.dsas[V]` [`context.c:138–139`], then calls `intervalcmp`. The insertion-sort therefore places each context in ascending **V-address order**.

---

### Outputting I-spans in V-Order

Back in **`span2spanset`** [`orglinks.c:439–444`]:
```c
for (c = context; c; c = c->nextcontext) {          // iterates contexts in V-order
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```
`context2span` is called with `idx1=V` (restriction) and `idx2=I` (target) — it extracts the **I-span** covered by each V-context chunk.

**`onitemlist`** [`orglinks.c:464`] simply appends to the end of the list (`for (temp = *itemsetptr; ...; temp = ...) ; then temp->next = newitem`) — no re-sorting. The I-spans land in the list in exactly the order the contexts were visited: **V-order**.

---

### Applied to the CREATELINK Gap Scenario

After a `doinsert` followed by a `docreatelink` followed by another `doinsert`, the POOM contains two leaf crums, e.g.:

| Crum | V-range | I-range |
|------|---------|---------|
| A | `[1.0.1.1, 1.0.1.5]` | `[1.0.1.1, 1.0.1.5]` |
| B | `[1.0.1.6, 1.0.1.10]` | `[1.0.1.9, 1.0.1.13]` ← gap at `1.0.1.6–1.0.1.8` (CREATELINK alloc) |

A V-span `[1.0.1.1 to 1.0.1.10]` straddles both. `findcbcinarea2d` finds both crums and calls `incontextlistnd(..., V)` for each. The context list is sorted **by V-address**: crum A first, crum B second.

`span2spanset` then emits I-spans in that V-order: `[1.0.1.1–1.0.1.5]` then `[1.0.1.9–1.0.1.13]`.

In this sequential-insert case V-order and I-address order happen to coincide. But if the document were rearranged (e.g., text with high I-addresses moved to an earlier V-position), the two orderings would diverge — and `incontextlistnd(index=V)` would still produce **V-order**, reflecting the document's current virtual structure, not the underlying permascroll storage order.

---

### Summary

**The result preserves V-order.** The mechanism is `incontextlistnd` at [`retrie.c:263`] called with `index1=V`. It insertion-sorts leaf crum contexts by their absolute V-address [`context.c:80,90,98`]. I-spans are then extracted from this V-ordered context list [`orglinks.c:439–444`] and appended in sequence by `onitemlist` [`orglinks.c:534`] — no further reordering occurs. The CREATELINK allocation gap creates non-contiguous I-spans, but the retrieval output lists them in V-order (document order), not I-address order.
