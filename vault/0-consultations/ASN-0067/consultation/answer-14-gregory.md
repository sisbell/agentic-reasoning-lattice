## Question 14 [gregory]

> When copying a V-span that includes content from multiple original insertions (and therefore multiple contiguous I-address runs), does the ordering of the resulting sporgl entries in the target POOM preserve the source document's V-ordering, or could the 2D enfilade's diagonal-sort rebalancing (`recombinend`) reorder them?

## KB Synthesis

## Answer: V-Ordering Is Preserved, Rebalancing Cannot Change It

The answer has two independent parts: (1) does insertion preserve V-ordering, and (2) can rebalancing corrupt it?

---

### Part 1 — Insertion Preserves V-Ordering

When `docopy` processes a multi-sporgl copy, the pipeline is:

```
source V-span
  → vspanset2ispanset → permute → span2spanset → retrieverestricted
  → incontextlistnd (insertion-sort by V-address)
  → sporgls in V-sorted order
  → insertpm, one call per sporgl, in that V-sorted order
  → target POOM entries at consecutive target V-positions
```

The critical step is `incontextlistnd` [SS-CONTEXT-LIST, INV-RETRIEVAL-V-SORTED]. It performs explicit insertion-sort by left-boundary V-address (`totaloffset.dsas[V]`) during tree traversal, regardless of sibling order in the source POOM. The resulting sporgl list is always V-sorted before it reaches `insertpm`.

Each sporgl is then placed at a target V-position (source offset mapped to target space). Since the sporgls arrive in V-address order, the target POOM receives them at monotonically increasing V-positions. [ST-INSERT, ST-VCOPY Finding 0046]

---

### Part 2 — Diagonal-Sort Rebalancing Cannot Corrupt V-Ordering

`recombinend` sorts children by diagonal key `cdsp.dsas[0] + cdsp.dsas[1]` before considering merges [SS-ENFILADE-TREE Finding 0071, ST-REBALANCE-2D]. For POOM, dimension 0 = I-space and dimension 1 = V-space. Two sporgls with the same diagonal sum but different individual coordinates (e.g., high-I/low-V and low-I/high-V) could become siblings in any order after rebalancing.

But this does not affect observable results because of [INV-RETRIEVAL-TREE-INDEPENDENCE] and [INV-RETRIEVAL-V-SORTED]:

> "The V-ordering of retrieval results is **independent of the internal B-tree structure**... `incontextlistnd` re-sorts during retrieval regardless of discovery order."

Rebalancing only moves crums between sibling slots. It never changes the `cdsp.dsas[V]` value stored in any individual crum — it only changes which crums are adjacent siblings. When a subsequent query traverses the POOM via `findcbcinarea2d`, it walks siblings in whatever tree order they land in, then `incontextlistnd` insertion-sorts the discovered contexts into V-order before returning.

---

### Summary

| Phase | Mechanism | V-ordering guaranteed? |
|-------|-----------|----------------------|
| Source extraction | `incontextlistnd` insertion-sort | Yes — V-sorted by construction |
| Target insertion | Sporgls inserted in V-sorted order | Yes — positions assigned monotonically |
| Post-insert rebalancing | Diagonal-sort changes sibling order only | Does not affect assignments |
| Retrieval from target | `incontextlistnd` re-sorts unconditionally | Yes — tree-structure-independent |

V-ordering of the copy result is preserved both in the assignments (structural guarantee from insertion order) and in all retrieval operations (query-layer guarantee from [INV-RETRIEVAL-V-SORTED]). The 2D diagonal-sort rebalancing [ST-REBALANCE-2D] is irrelevant to this question — it optimizes merge candidates spatially but cannot change what V-address any crum is responsible for.

---

## Code Exploration

Now I have enough source to answer definitively. Let me trace the full execution path.

---

## Answer

The source document's **V-ordering is fully preserved** in the copy. `recombinend`'s diagonal sort operates only on internal tree nodes and is **coordinate-preserving** — it cannot reorder the semantic (I↔V) mapping of bottom crums.

Here is the chain of evidence, cited line-by-line.

---

### 1. The entry point: `docopy`

`do1.c:45–65` shows the copy pipeline:

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)
    && findorgl (...)
    && acceptablevsa (vsaptr, docorgl)
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)  // ← the meat
    && insertspanf (...) );
}
```

The specset (source V-specs) is first converted to an I-span set, then passed to `insertpm`.

---

### 2. V→I conversion produces a V-ordered sporgl list

`specset2ispanset` → `permute` → `span2spanset` → `retrieverestricted` → `findcbcinarea2d`:

`retrie.c:252–264`:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson(...), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);  // index1 = V
    }
}
```

Each bottom crum that overlaps the source V-span is collected by `incontextlistnd`, which **sorts by V-coordinate**:

`context.c:75–111` — the function walks the list and inserts each new context in ascending V-address order:
```c
// on beginning
if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {
    c->nextcontext = clist; *clistptr = c;  return(0);
}
// in middle
for (; nextc = clist->nextcontext; clist = nextc) {
    if ((whereoncontext(clist,...) > ONMYLEFTBORDER)
     && (whereoncontext(nextc,...) < ONMYLEFTBORDER)) {
        c->nextcontext = nextc; clist->nextcontext = c;  return(0);
    }
}
// on end
clist->nextcontext = c;
```

So the resulting context (and therefore sporgl) list is **in ascending V-order** from the source document.

---

### 3. `insertpm` assigns target V-addresses in that V-order

`orglinks.c:100–132`:
```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   // I-address of this run
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   // V-address = current vsaptr
    shift = tumblerlength (vsaptr) - 1;
    inc   = tumblerintdiff (&lwidth, &zero);
    tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
/**/tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // ← advance vsaptr
}
```

Because `sporglset` is V-ordered (step 2), each successive I-run is given the next sequential target V-address. If the source had runs at V=10 and V=20, they are inserted at Vtarget and Vtarget+10, respectively — preserving document order.

---

### 4. `insertnd` calls `recombinend`; what does it do?

`insertnd.c:70–77`:
```c
if (bothertorecombine || (fullcrumptr->height != oldheight)) {
    recombine (fullcrumptr);
}
```

For a POOM, `recombine` calls `recombinend` (`recombine.c:31`).

`recombinend` (`recombine.c:104–131`):
```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified) return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend (ptr);                  // recurse first

    getorderedsons (father, sons);          // sort sons by diagonal
    n = father->numberofsons;
    for (i = 0; i < n-1; i++)
        for (j = i+1; sons[i] && j < n; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd (&sons[i], &sons[j]);  // merge subtrees

    if (father->isapex) levelpull (father);
}
```

`getorderedsons` sorts internal-node children by **diagonal magnitude** (`dsas[0] + dsas[1]`):

`recombine.c:296–310`:
```c
for (i = 0; i < n; i++) {
    tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);
    tarrayp[i] = &tarray[i];
}
// shellsort by that sum
```

This sort determines **which pairs of sibling internal nodes to merge** — it is a storage-efficiency heuristic. It does **not** touch bottom crums.

---

### 5. The merge operations are coordinate-preserving

**`eatbrossubtreend`** (`recombine.c:205–233`) merges bro's children into me by re-linking the sibling pointers, then calling `fixdspsofbroschildren`:

`recombine.c:259–268`:
```c
int fixdspsofbroschildren(typecuc *me, typecuc *bro)
{
    for (nephew = getleftson(bro); nephew; nephew = getrightbro(nephew)) {
        dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);  // make absolute
        dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);   // re-relativize to me
        ivemodified(nephew);
    }
}
```

**`takenephewnd`** (`recombine.c:235–257`) does the same for individual nodes:
```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype); // absolute
adopt (nephew, RIGHTMOSTSON, me);
...
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);   // re-relativize
```

In both cases, the nephew/bro's **absolute (I, V) coordinates are preserved**. Only the stored relative displacement (`cdsp`) is updated to reflect the new parent. No crum ever changes its semantic address in the 2D space.

---

### 6. Retrieval never depends on sibling order

POOM retrieval (`findcbcinarea2d`, `retrie.c:229–268`) scans all siblings and uses `crumqualifies2d` / `whereoncrum` for coordinate-based filtering. It does not rely on siblings being in any particular left-to-right order. The result of `recombinend` restructuring has zero impact on what coordinates get returned.

---

## Conclusion

**V-ordering is preserved; `recombinend` cannot reorder it.**

The path is:

1. **`incontextlistnd`** (`context.c:75`) builds the sporgl list in **ascending V-order** from the source.
2. **`insertpm`** (`orglinks.c:100–132`) assigns target V-addresses sequentially to each I-run, preserving the source V-order in the target POOM.
3. **`recombinend`** (`recombine.c:104`) restructures internal POOM nodes using a diagonal-sort to guide merging, but both merge operations (`eatbrossubtreend`, `takenephewnd`) recalculate stored displacements so that every bottom crum's **absolute (I, V) position is unchanged**.
4. POOM retrieval is coordinate-based, not sibling-order-based, so the restructuring is semantically invisible.

The only thing `recombinend`'s diagonal sort determines is which internal subtrees become siblings — a performance question, not a correctness one. The copied content in the target POOM faithfully encodes the source V-ordering across all I-address runs.
