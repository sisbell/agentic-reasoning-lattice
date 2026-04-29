## Question 16 [gregory]

> Is there an ordering invariant on sibling bottom crums within a single POOM loaf — must their V-displacements be sorted left-to-right, or does `incontextlistnd` compensate for arbitrary physical ordering during retrieval?

## KB Synthesis

**Physical sibling order in POOM loafs does not need to be V-sorted. `incontextlistnd` compensates by performing insertion-sort at retrieval time.**

## The Core Answer

[SS-CONTEXT-LIST] makes the distinction explicit:

- **POOM (2D)** uses `incontextlistnd()` — **insertion-sort**, because "tree order does not guarantee V-order"
- **GRAN (1D)** uses `oncontextlistseq()` — **sequential append**, because "sequential order is maintained by tree structure"

The choice of accumulation function is precisely the acknowledgment that POOM sibling order carries no V-ordering guarantee.

## Why Physical Order Is Arbitrary

Three mechanisms contribute to unordered physical sibling sequences in a POOM loaf:

**1. Insertion order (right-brother append)**
[SS-ENFILADE-TREE Finding 0041]: New entries are adopted as the `RIGHTBRO` of the retrieval position — chronological append, not V-position order. Sequential inserts at arbitrary V-positions produce siblings in insertion-time order, not address order.

**2. Rebalancing sorts by diagonal, not V-address**
[SS-ENFILADE-TREE Finding 0071]: `getorderedsons` during `recombinend` sorts children by `cdsp.dsas[0] + cdsp.dsas[1]` (L1 norm / diagonal). For a POOM where dimension 0 is I-space (ORGLRANGE) and dimension 1 is V-space (SPANRANGE), this diagonal ordering is not equivalent to V-address ordering.

**3. Split distributes by diagonal, not by V-address**
[ST-SPLIT-2D Finding 0071]: `splitcrumpm` peels off the child with the largest `dsas[SPANRANGE]` only (ignoring the ORGLRANGE), while `recombinend` uses the diagonal key — further divergence between physical order and V-order.

## How `incontextlistnd` Compensates

[INV-RETRIEVAL-V-SORTED Finding 0078]:

> `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered during B-tree traversal. Each leaf node found by `findcbcinarea2d()` is inserted into a linked list at the position that maintains ascending order of `totaloffset.dsas[index]`

[INV-RETRIEVAL-TREE-INDEPENDENCE Finding 0078] states this as an invariant:

> The V-ordering of retrieval results is independent of the internal B-tree structure … Tree structure affects storage and traversal efficiency, but not the ordering of results.

So the postcondition `contexts[j].totaloffset.dsas[V] ≤ contexts[k].totaloffset.dsas[V]` for all `j < k` holds regardless of physical sibling arrangement.

## Contrast With GRAN

For the 1D granfilade, `oncontextlistseq` simply appends in tree traversal order. This works because GRAN inserts always append as right-brothers in address order (allocation is monotonically increasing [INV-MONOTONIC]), so the left-to-right sibling walk of `findcbcseqcrum` [SS-ENFILADE-TREE Finding 0041] naturally yields sequential order.

POOM lacks this property because V-positions are not monotonically increasing across operations — inserts, rearrangements, and transclusions place content at arbitrary positions — so no insertion discipline could maintain physical V-order in siblings.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer:

---

## Ordering Invariant on POOM Loaf Siblings

**Answer: There is no V-ordering invariant on sibling bottom crums within a POOM loaf.** Physical left-to-right sibling position in a loaf is completely independent of V-displacement. `incontextlistnd` explicitly compensates during area retrieval, and single-point retrieval (`findcbcnd`) also works correctly under arbitrary physical ordering.

---

### 1. `cdsp` Is an Absolute Displacement from the Parent's Grasp — Not Sequential

In a GRAN (sequential) enfilade, the running offset across siblings is cumulative: each sibling's absolute position depends on the widths of all predecessors. POOM is fundamentally different.

From `wisp.h:19-20`:
```c
#define I  0
#define V  1
```

Every POOM crum stores `cdsp.dsas[V]` as an **absolute displacement from its parent's grasp position** in V-space. The position formula, from `whereoncrum` [`retrie.c:356`]:
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
```
is `left = parent_grasp + crum_cdsp`, with no dependence on any sibling's width or position. Sibling crums are independently positioned.

---

### 2. Insertion Always Places New Bottom Crums at the Physical Left

`insertcbcnd` [`insertnd.c:260-263`]:
```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);          /* SON == LEFTMOSTSON */
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);
```
`SON` is `LEFTMOSTSON` [`enf.h:137`]. Every newly inserted bottom crum is physically prepended to the loaf regardless of its V-displacement. A crum with V-address 1000 could be the first child in the loaf while a crum with V-address 1 sits at the rightmost position.

---

### 3. `incontextlistnd` Explicitly Re-Sorts by V During Area Retrieval

The function's own comment is definitive [`context.c:74`]:
```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
```

Its body performs an insertion-sort into the output list [`context.c:90-111`]:
```c
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    /* on beginning */
    c->nextcontext = clist;
    *clistptr = c;
    return(0);
} else {
    for (; nextc = clist->nextcontext; clist = nextc) {
        /* in middle */
        if ((whereoncontext (clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
            && (whereoncontext (nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
            c->nextcontext = nextc;
            clist->nextcontext = c;
            return(0);
        }
    }
}
/* on end */
clist->nextcontext = c;
```
Using `whereoncontext`, which for POOM compares against `totaloffset.dsas[index]` and `contextwid.dsas[index]`, it inserts each discovered bottom crum into the correct position in the sorted output list.

---

### 4. Area Retrieval Traverses Siblings in Physical Order, Then Sorts on Output

`findcbcinarea2d` [`retrie.c:252-265`] iterates siblings physically left-to-right:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (crumptr, offsetptr, ...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, ...);
        findcbcinarea2d (findleftson (...), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);    /* ← sorts here */
    }
}
```

`makecontextfromcbc` computes the crum's absolute V-position internally [`context.c:167`]:
```c
dspadd(&context->totaloffset, &crumptr->cdsp, &context->totaloffset, (INT)crumptr->cenftype);
```
After this, `incontextlistnd` places the new context in the correct sorted position. The traversal order is irrelevant to output correctness.

---

### 5. Single-Point Retrieval (`findcbcnd`) Also Requires No Ordering

`findcbcnd` [`retrie.c:208-227`] does a linear scan of all children:
```c
for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
    if (retr = findcbcnd (ptr, &grasp, address, index))
        break;
```
At the top of each recursive call it checks:
```c
if ((cmp = whereoncrum (father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME)
    return (NULL);
```
Each child is tested independently against the target address using its own `cdsp`. No binary search, no ordering assumption — pure linear scan with independent position tests.

---

### 6. The Split Criterion Is V-Magnitude, Not V-Rank — and Doesn't Reorder

`splitcrumpm` [`split.c:117-128`] selects the child with the **largest** `cdsp.dsas[SPANRANGE]` (= V) to peel off:
```c
for(correctone=ptr=findleftson(father); ptr; ptr = findrightbro(ptr)) {
    if (tumblercmp (&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
        correctone = ptr;
}
peelcrumoffnd(correctone);
```
`peelcrumoffnd` [`split.c:151-155`] then creates a new sibling UC and adopts the selected crum as its `LEFTMOSTSON`. The remaining siblings stay in whatever physical order they had — they are not re-sorted.

`recombinend` uses `getorderedsons` → `shellsort` [`recombine.c:270-310`], which sorts by the **diagonal sum** `cdsp[0] + cdsp[1]`, not by V alone. This ordering is used only to select recombination candidates, not to impose a persistent storage invariant.

---

### 7. `findsontoinsertundernd` Confirms No Ordering Assumption

When finding which UC subtree to descend into for insertion [`insertnd.c:284-298`]:
```c
for (; ptr; ptr = findrightbro(ptr)) {
    tumbleradd(&grasp->dsas[index], &ptr->cdsp.dsas[index], &sonstart);
    if (tumblercmp (&sonstart, &origin->dsas[index]) != GREATER
     && tumblercmp (&ptr->cdsp.dsas[index], &nearestonleft->cdsp.dsas[index]) != LESS) {
        nearestonleft = ptr;
    }
    if (whereoncrum(ptr, grasp, &origin->dsas[index], index) >= ONMYLEFTBORDER
     && whereoncrum(ptr, grasp, &spanend, index) <= ONMYRIGHTBORDER)
        return (ptr);
}
return (nearestonleft);
```
This is a full scan of all siblings; it does not binary-search or short-circuit based on any sorted-order assumption.

---

### Summary

| Claim | Evidence |
|-------|----------|
| No V-ordering invariant maintained during insert | `adopt(new, SON=LEFTMOSTSON, ...)` in `insertcbcnd` [insertnd.c:262] |
| `cdsp` is absolute, not relative to previous sibling | `whereoncrum` [retrie.c:356], POOM case |
| Area retrieval output is V-sorted regardless of storage | `incontextlistnd` called per bottom crum in `findcbcinarea2d` [retrie.c:263], comment "put c on clist in index order" [context.c:74] |
| Single-point retrieval scans all siblings linearly | `findcbcnd` loop [retrie.c:220-222] |
| Split selects by V-magnitude, doesn't reorder | `splitcrumpm` [split.c:122-125] |
| Recombine uses diagonal sort, not V-sort | `shellsort` by `cdsp[0]+cdsp[1]` [recombine.c:296-310] |

**Physical ordering of sibling bottom crums in a POOM loaf is arbitrary and operationally irrelevant.** All position information is self-contained in each crum's `cdsp`. `incontextlistnd` is not a workaround for a broken invariant — it is the intended and sufficient mechanism for producing ordered output from unordered storage.
