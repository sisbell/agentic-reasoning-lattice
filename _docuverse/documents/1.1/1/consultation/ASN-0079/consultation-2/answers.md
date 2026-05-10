# Revision Consultation — ASN-0079

**Review:** review-2.md
**Date:** 2026-03-23 01:19

## Summary

4 REVISE items analyzed: 3 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 4: F19 scaling requirement internally inconsistent

**Category:** BOTH
**Reason:** Nelson's phrase "does not in principle impede" could mean O(1) independence or merely sublinear growth — this is a design-intent question. The spanfilade's actual complexity characteristics determine which formalization the implementation supports.

**Nelson question:** When you wrote that the quantity of non-satisfying links must not "in principle impede" search, did you mean cost must be strictly independent of total link count, or that it must not grow linearly (admitting logarithmic overhead from tree-based indexing)?

**Nelson's Answer:**

Let me check the raw pages around 4/57–4/60 for the full context surrounding that statement.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-224.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-225.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-226.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-227.txt"}}
</tool_call>

**Gregory question:** What is the actual complexity of a spanfilade lookup in udanax-green as a function of total link count — is it O(log n) from tree traversal, O(1) from hashing, or something else?

**Gregory's Answer:**

## KB Synthesis

## Spanfilade Lookup Complexity

The spanfilade is a **2D B-tree**, not a hash table, so lookup is O(log n) from tree traversal — but with important qualifications.

### Tree structure

[SS-ENFILADE-TREE (Finding 0060)] and [SS-ENFILADE-BRANCHING (Finding 0070)] establish the branching factors for the SPAN enfilade:

| Level | Constant | Value |
|-------|----------|-------|
| Bottom crums (height = 1) | `MAX2DBCINLOAF` | 4 |
| Upper crums (height > 1) | `MAXUCINLOAF` | 6 |

Tree height is therefore O(log₄ N) for leaves, O(log₆ N) for upper levels. This gives O(log N) to reach the right leaf region.

### Retrieval traversal

[SS-CONTEXT-LIST (Finding 0078)] confirms the 2D enfilade traversal via `findcbcinarea2d()` (`retrie.c:229-268`) iterates all siblings at each B-tree level and recurses into all qualifying subtrees, accumulating every matching leaf. This is not a point lookup — it collects all I-address ranges that intersect the query span. Cost: **O(log N + k)** where k is the number of matching entries.

### Full `find_links` complexity

[SS-FIND-LINKS (Finding 0035)] makes this significantly worse: `findlinksfromtothreesp()` executes three separate spanfilade searches (FROM, TO, THREE endpoints) and then calls `intersectlinksets()` to combine them. The KB records its complexity directly:

> `intersectlinksets()`: `backend/spanf2.c:46-120` — O(n×m) or O(n×m×p) intersection

So for the full search:

1. **Three B-tree scans**: O(log N) each → O(log N)
2. **Result collection**: O(k₁ + k₂ + k₃) where k_i = matching links per endpoint type
3. **Intersection**: O(k₁ × k₂) for two-endpoint search, O(k₁ × k₂ × k₃) for three-endpoint

The total is **O(log N + k₁×k₂×k₃)** in the worst case, where N is the total number of spanfilade entries and k_i is the number of links whose i-th endpoint overlaps the query I-address range.

### Additionally: FINDNUMOFLINKSFROMTOTHREE

[SS-FIND-LINKS (Finding 0035)] notes that the count operation is not optimized — it materializes the full result list and walks it linearly. No count-only path exists.

### Summary

| Component | Complexity |
|-----------|-----------|
| Tree traversal to matching region | O(log N) |
| Collecting matching leaves | O(k) per endpoint type |
| Result set intersection | O(k₁ × k₂ × k₃) |
| FINDNUMOFLINKSFROMTOTHREE | O(full search + linear count) |

The lookup is O(log N) in the pure tree-traversal sense, but full link search is superlinear in the number of result candidates due to the unoptimized set intersection at `intersectlinksets()`.

---

## Code Exploration

---

## Spanfilade Lookup Complexity: Full Analysis

### The data structure

The spanfilade is a **two-dimensional B-tree-like enfilade** — not a hash table, and not a simple binary tree. The node types are:

- `typecuc` (upper crum) — internal nodes with `height`, `leftson`, `numberofsons` [`enf.h:54-82`]
- `type2dcbc` (2D bottom crum) — leaf nodes, where `height == 0` [`enf.h:109-131`]

Branching factors are defined at [`enf.h:26-28`]:
```c
#define MAXUCINLOAF 6       // max children for internal nodes at height > 1
#define MAXBCINLOAF    1    // max children for 1D leaf-level internal nodes
#define MAX2DBCINLOAF   4   // max children for 2D leaf-level internal nodes (used by SPAN)
```

So the SPAN type uses branching factor 4–6. With `n` leaf crums (each representing one link-endpoint entry), the tree height is `O(log₄ n) = O(log n)`.

---

### The lookup call chain

**`findlinksfromtothreesp`** [`spanf1.c:56`] is the top-level entry point. It:
1. Converts from/to/three specsets → sporgl sets via `specset2sporglset`
2. Calls `sporglset2linkset` for each endpoint set [`spanf1.c:77,85,93`]
3. Intersects the three resulting link lists via `intersectlinksets`

**`sporglset2linksetinrange`** [`sporgl.c:239`] iterates over sporgls and issues the actual tree query:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```
[`sporgl.c:259`]

**`retrieverestricted`** [`retrie.c:56`] → **`retrieveinarea`** [`retrie.c:87`] → **`findcbcinarea2d`** [`retrie.c:229`].

---

### The tree traversal: O(log n + k)

`findcbcinarea2d` [`retrie.c:229`] is the recursive B-tree range scan:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {          // walk siblings
    if (!crumqualifies2d(crumptr, offsetptr, span1start, span1end, index1,
                          span2start, span2end, index2, ...))
        continue;                                          // prune non-overlapping subtrees
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, ...);
        findcbcinarea2d(findleftson(crumptr), &localoffset, ...);  // recurse
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, ...);
        incontextlistnd(headptr, context, index1);         // collect leaf
    }
}
```

`crumqualifies2d` [`retrie.c:270`] does two interval comparisons per dimension and prunes any crum whose span doesn't overlap the query range. For a tight span query (few matching leaves), this prunes all but O(log n) nodes. For a query returning `k` matching leaves, the traversal visits O(log n + k) nodes.

**This part is genuinely O(log n)** for a point query.

---

### The result pipeline: where O(k²) enters

**Deduplication in `onlinklist`** [`spanf2.c:26-44`]:

```c
bool onlinklist(typetask *taskptr, typelinkset *linksetptr, typeisa *linkisaptr) {
    linkset = makelinkitem(taskptr, linkisaptr);
    if (*linksetptr == NULL) { *linksetptr = linkset; return(0); }
    for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
        if (tumblereq(&temp->address, linkisaptr))
            return(0);          // already present — linear scan to check
    }
    temp->next = linkset;
}
```

This is called once per matched leaf by `sporglset2linksetinrange` [`sporgl.c:263-265`]. Each call scans the entire accumulated result list. **No hash table. No sorted set.** If `k` links accumulate, the total deduplication cost is **O(k²)**.

**Intersection in `intersectlinksets`** [`spanf2.c:96-104`]:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq(&temp1->address, &temp2->address)) {
            linkset4 = makelinkitem(taskptr, &temp1->address);
            ...
        }
    }
}
```

Nested linear loops over the from-endpoint list and to-endpoint list. **O(|L_from| × |L_to|)**. No sorting, no hashing.

**Pagination cursor scan** in `findnextnlinksfromtothreesp` [`spanf1.c:128-134`]:

```c
for (; linkset; linkset = linkset->next) {
    if (tumblereq(&linkset->address, lastlinkisaptr)) {
        *nextlinksetptr = linkset->next;
        break;
    }
}
```

Linear scan to find offset position — **O(k)**.

---

### Summary table

Let `L` = total link count, `n` = spanfilade leaf entries (≈ 2–3× L), `k` = links matching a single endpoint query.

| Step | Function | Complexity |
|------|----------|-----------|
| Tree traversal | `findcbcinarea2d` [`retrie.c:229`] | O(log n + k) |
| Deduplication | `onlinklist` [`spanf2.c:26`] | O(k²) total |
| Intersection | `intersectlinksets` [`spanf2.c:96`] | O(\|from\| × \|to\|) |
| Pagination cursor | `findnextnlinksfromtothreesp` [`spanf1.c:128`] | O(k) |

---

### Answer

**The spanfilade tree traversal itself is O(log n)** — it's a genuine B-tree with branching factor 4–6, and `findcbcinarea2d` prunes non-matching subtrees with a 2D interval test at each node. For a point query, only O(log n) nodes are visited.

**But the overall lookup is O(k²)** in the result set size `k`, not O(log n). The reason: result accumulation (`onlinklist`) uses an **unsorted linked list with linear deduplication**, and intersection (`intersectlinksets`) uses **nested linear loops** — there is no hash table, no sorted index, and no smarter set data structure anywhere in the pipeline.

When `k` scales with `L` (e.g., querying a span touched by many links), the dominant cost becomes the quadratic accumulation and intersection steps. In the worst case (all `L` links touch the queried span), the effective complexity is **O(L²)**, not O(log L).

The O(log n) complexity belongs to the enfilade tree structure. The O(k²) regression belongs to the post-retrieval result handling in `sporgl.c` and `spanf2.c`.
