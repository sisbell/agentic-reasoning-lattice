## Question 17 [gregory]

> After a 3-cut pivot fragments a previously contiguous I-span across two non-adjacent V-regions, does `incontextlistnd` correctly return both V-positions when resolving that I-span back to V-space for link endset retrieval?

## KB Synthesis

## Short answer: Yes for V-position retrieval, but with duplication artifacts in link endsets.

---

### 1. POOM multimap accumulation is correct

After a 3-cut pivot, the POOM is a multimap in which the queried I-span maps to two non-adjacent V-regions. The traversal mechanism is designed for exactly this case.

From [SS-POOM-MULTIMAP] (Finding 0039), `ispan2vspanset` calls `permute()` → `findcbcinarea2d()`, which "traverses all siblings at each B-tree level and recursively descends into all qualifying subtrees, accumulating every matching leaf node." `incontextlistnd()` "inserts each found context into a sorted linked list, never replacing existing entries."

From [INV-RETRIEVAL-V-SORTED] (Finding 0078), `incontextlistnd()` performs explicit insertion-sort by V-address as contexts are discovered. The postcondition is:

```
∀ j < k : result[j].totaloffset.dsas[V] ≤ result[k].totaloffset.dsas[V]
```

This holds regardless of tree structure — [INV-RETRIEVAL-TREE-INDEPENDENCE] confirms the sorted-result postcondition is independent of B-tree sibling ordering, split history, or insertion order.

So both V-positions are returned, correctly sorted.

---

### 2. But the link endset layer has duplication artifacts

The duplication arises one level up, in how the endset itself was encoded at link-creation time.

From [SS-LINK-ENDPOINT] (Finding 0037), `vspanset2sporglset()` decomposes each V-span into one sporgl per **contiguous I-address region**. If the V-span covers content transcluded from two sources, it produces two sporgls. These two sporgls are independently indexed in the spanfilade — two separate `insertnd` calls via `insertendsetsinspanf` [ST-CREATE-LINK].

After a pivot rearranges content so that a previously contiguous I-span is split across two non-adjacent V-regions, the same fragmentation logic applies in reverse: `ispan2vspanset` returns two V-regions, yielding two sporgls, and the link is found twice in the spanfilade search — once per sporgl match.

[EC-PIVOT-LINK-FRAGMENTATION] (Finding 0019) documents this directly: after a pivot rearranges linked content, `retrieve_endsets` reports **four spans** for a link originally created on two characters ("CD"), and `find_links` returns the link **twice**. The note is: "This suggests that rearrangement can cause internal fragmentation in the enfilade structure that is visible through the endset API. The duplication may be a bug or may reflect the internal representation of fragmented spans."

---

### 3. Mechanism summary

| Layer | Behavior |
|-------|----------|
| POOM traversal (`findcbcinarea2d`) | Finds all matching crums across both V-regions — correct |
| `incontextlistnd` accumulation | Inserts both into a sorted list — correct |
| I-to-V conversion (`span2spanset`) | Returns both V-spans — correct |
| Spanfilade lookup | Independently matches both sporgls — produces duplication |
| `find_links` result | Link returned twice — artifact |

The retrieval machinery in [SS-CONTEXT-LIST] / [INV-RETRIEVAL-V-SORTED] works correctly. The duplication is not a failure of `incontextlistnd` but a consequence of the spanfilade indexing each sporgl independently: after pivot, the single link's endset is represented as two independent I-span records in the spanfilade, and each matches the query separately.

---

## Code Exploration

I now have everything needed to answer this definitively. Here is the full analysis, with every claim tied to source.

---

## Full Answer

### The 3-Cut Pivot and What It Does to the POOM

`rearrangend` in `edit.c:78` performs the pivot on the document's POOM (permutation matrix enfilade) in V-space. For 3 blades `[c0, c1, c2]`, `makeoffsetsfor3or4cuts` at `edit.c:177-183` computes:

```c
diff[1] = c2 - c1   // section 1 (between c0 and c1) shifts right
diff[2] = -(c1 - c0) // section 2 (between c1 and c2) shifts left
diff[3] = 0          // section 3 (after c2) doesn't move
```

After `makecutsnd` splits crums at V-positions c0, c1, c2, then `rearrangend:125` adds each `diff[i]` to `ptr->cdsp.dsas[V]` for each section:

```c
tumbleradd (&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index]);  // edit.c:125
ivemodified((typecorecrum*)ptr);
```

The I-coordinates (`dsas[I]`) are never touched. This is the critical point: **a 3-cut pivot changes V-displacement while preserving I-addresses**. A contiguous I-span [i_start, i_end) that occupied a contiguous V-range [v_start, v_end) before the pivot now appears in the POOM as two or more leaf crums with the same I-addresses but with V-displacements shuffled into non-adjacent positions.

---

### Resolving an I-Span to V-Space: The Call Chain

When link endset retrieval must resolve a stored I-span back to V-positions, the chain is:

```
dofollowlink [do1.c:223]
  → link2sporglset [sporgl.c:67]
      → retrieverestricted on the link POOM [retrie.c:56]
  → linksporglset2specset [sporgl.c:97]
      → sporglset2vspanset [sporgl.c:141]
          → ispan2vspanset [orglinks.c:389]
              → permute(..., I, ..., V) [orglinks.c:404]
                  → span2spanset [orglinks.c:425]
                      → retrieverestricted [retrie.c:56]
                          → retrieveinarea [retrie.c:87]
                              → findcbcinarea2d [retrie.c:229]
                                  → incontextlistnd [context.c:75]
                      → context2span (for each context) [context.c:176]
```

---

### What `findcbcinarea2d` Sees After the Pivot

`retrieverestricted` at `retrie.c:56` is called from `span2spanset` as:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
// restrictionindex = I,  targindex = V
```

This calls `retrieveinarea` → `findcbcinarea2d` [retrie.c:229]. The function walks all right-siblings in the POOM recursively, calling `crumqualifies2d` [retrie.c:270] to filter. `crumqualifies2d` checks:

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT :
         whereoncrum(crumptr, offset, span1end, index1);   // I-end check
if (endcmp <= ONMYLEFTBORDER) return FALSE;                // retrie.c:283

startcmp = whereoncrum(crumptr, offset, span1start, index1); // I-start check
if (startcmp > THRUME) return FALSE;                          // retrie.c:287

// V range: span2start = span2end = 0 (NULL restriction)
endcmp = iszerotumbler(span2end) ? TOMYRIGHT : ...;           // retrie.c:292
// always TOMYRIGHT since span2ptr was NULL → always passes
startcmp = whereoncrum(crumptr, offset, span2start, index2); // retrie.c:297
// span2start=0, so any crum with V >= 0 qualifies
```

**After the 3-cut pivot**, a previously-contiguous I-span [i_start, i_end) that was split by the cuts at [c0, c1, c2] now exists as at least two separate POOM leaf crums — e.g.:

- Leaf crum A: I=[i_start, i_mid), V=[v2, v2+k)   ← section 2 after pivot
- Leaf crum B: I=[i_mid, i_end), V=[v1, v1+m)     ← section 1 after pivot

Both satisfy the I-span restriction since both have I-extents overlapping [i_start, i_end). Both pass `crumqualifies2d` with no V restriction. `findcbcinarea2d` calls `incontextlistnd` for each:

```c
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr); // retrie.c:262
incontextlistnd(headptr, context, index1);                            // retrie.c:263
```

---

### Inside `incontextlistnd` [context.c:75]

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
  prologuecontextnd(c, &grasp, (typedsp*)NULL);  // sets grasp = c's totaloffset
  // grasp.dsas[index] = c's I-start (since index = I)

  if (!clist) { *clistptr = c; return(0); }      // first insertion

  if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c; return(0); // insert at beginning
  } else {
    for (; nextc = clist->nextcontext; clist = nextc) {
      if ((whereoncontext(clist, &grasp.dsas[index], index) > ONMYLEFTBORDER)
       && (whereoncontext(nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c; return(0); // middle
      }
    }
  }
  clist->nextcontext = c; // append at end
}
```

`prologuecontextnd` [context.c:216] extracts `grasp.dsas[I]` = the I-start of the new context. The list is **sorted by I-position**.

For Crum A (I-start = i_start) inserted first into an empty list: trivially inserted.

For Crum B (I-start = i_mid > i_start) inserted second:
- `whereoncontext(A, i_mid, I)`: A covers [i_start, i_mid). `intervalcmp(i_start, i_mid, i_mid)` → address equals right → `ONMYRIGHTBORDER`.
- `ONMYRIGHTBORDER < THRUME`? The return values in order are: TOMYLEFT < ONMYLEFTBORDER < THRUME < ONMYRIGHTBORDER < TOMYRIGHT. So **NO** — the "beginning" condition fails.
- The `for` loop has no iterations (A has no nextcontext).
- Crum B is appended at end.

**Result: the context list correctly contains both [A, B] in I-order.**

---

### `context2span` Maps Each Fragment to Its V-Position [context.c:176]

For each context in the list, `span2spanset` [orglinks.c:439] calls:

```c
context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
// idx1 = I,  idx2 = V
```

`context2span` [context.c:191-211] does:

```c
prologuecontextnd(context, &grasp, &reach);
// grasp.dsas[I] = crum's I-start,  grasp.dsas[V] = crum's V-start
// reach.dsas[I] = crum's I-end,    reach.dsas[V] = crum's V-end

if (tumblercmp(&grasp.dsas[I], &lowerbound) == LESS)
    // trim V-start if I-start is before restriction's I-start
    tumblerincrement(&grasp.dsas[V], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[I]), &grasp.dsas[V]);

if (tumblercmp(&reach.dsas[I], &upperbound) == GREATER)
    // trim V-end if I-end is past restriction's I-end
    tumblerincrement(&reach.dsas[V], 0,
        -tumblerintdiff(&reach.dsas[I], &upperbound), &reach.dsas[V]);

movetumbler(&grasp.dsas[V], &foundspanptr->stream);
tumblersub(&reach.dsas[V], &grasp.dsas[V], &foundspanptr->width);
```

For Crum A (I=[i_start, i_mid), V=[v2, v2+k)), restriction [i_start, i_end):
- I-start == lowerbound → first `if` skips → V-start stays at v2
- I-end < upperbound → second `if` skips → V-end stays at v2+k
- **foundspan = V=[v2, v2+k)**

For Crum B (I=[i_mid, i_end), V=[v1, v1+m)), restriction [i_start, i_end):
- I-start > lowerbound → first `if` skips → V-start stays at v1
- I-end == upperbound → second `if` skips → V-end stays at v1+m
- **foundspan = V=[v1, v1+m)**

Both are added to `targspansetptr` via `onitemlist` [orglinks.c:464], which appends them in order.

---

### Answer to the Question

**Yes — `incontextlistnd` correctly identifies and returns both V-positions.** Here is why:

1. **The POOM after a 3-cut pivot contains distinct leaf crums** for each fragment. The fragments have non-overlapping I-extents (split at cut-points) and non-adjacent V-displacements. Nothing in `rearrangend` [edit.c:78] merges crums that were separated by cuts — `recombine` [edit.c:139] and `splitcrumupwards` [edit.c:141] operate on structural housekeeping, not on re-fusing semantically distinct spans.

2. **`findcbcinarea2d` [retrie.c:229] finds all qualifying leaf crums** regardless of their V-positions, because `crumqualifies2d` [retrie.c:270] uses `iszerotumbler(span2end) ? TOMYRIGHT` when there is no V restriction — passing `TOMYRIGHT` to the `endcmp <= ONMYLEFTBORDER` guard, which always lets through.

3. **`incontextlistnd` [context.c:75] correctly inserts both fragments** because they have different I-starts (split at the cut). The sorted insertion logic places Crum A (lower I-start) before Crum B (higher I-start), and the append-at-end fall-through at `context.c:109-110` correctly handles the adjacent-I-boundary case where `whereoncontext` returns `ONMYRIGHTBORDER` rather than the `< THRUME` threshold.

4. **`context2span` [context.c:176] correctly maps each fragment's I-range to its corresponding V-range** independently, clipping only to the restriction I-span, which doesn't affect either fragment in the common case where the restriction spans the full original I-range.

---

### One Real Defect in `incontextlistnd`

The "in middle" insertion condition at `context.c:99` requires:

```c
&& (whereoncontext(nextc, &grasp.dsas[index], index) < ONMYLEFTBORDER)
```

`< ONMYLEFTBORDER` means strictly `TOMYLEFT`. If two contexts have identical I-starts — which cannot happen from a 3-cut pivot (cuts produce distinct fragments), but could theoretically arise from independent insertions — this condition would fail to detect the correct insertion point, and the second context would be appended at the end rather than interleaved. **This bug does not affect the 3-cut pivot scenario** because the cut positions always produce fragments with strictly distinct I-starts.

---

### Conclusion

For the specific case described — a 3-cut pivot that fragments a contiguous I-span into two crums across non-adjacent V-regions — the system works correctly end-to-end. `findcbcinarea2d` discovers both crums, `incontextlistnd` inserts both into the context list in I-order (the sorting being harmless since `context2span` processes each independently), and `context2span` emits the correct non-adjacent V-spans. Both V-positions are returned.
