## Question 20 [gregory]

> After REARRANGE moves entries within the POOM's 2D enfilade, does `recombinend` fire to rebalance the tree, and if so, does the diagonal-sum reordering ever change the logical V-address ordering of the result — or is confluence guaranteed regardless of post-rearrange tree shape?

## KB Synthesis

Two separate questions here — whether `recombinend` fires, and whether confluence is preserved. The KB answers them independently.

## Does `recombinend` fire after REARRANGE?

Almost certainly not. The rebalancing triggers are purely occupancy-based: `toomanysons` fires when a node exceeds its branching limit, `toofewsons` fires when a node falls below it [INV-ENFILADE-OCCUPANCY, SS-ENFILADE-TREE/Finding 0070]. REARRANGE adds no crums and removes no crums — it only mutates existing crums' `cdsp.dsas[V]` fields in-place via `tumbleradd` [ST-REARRANGE/Finding 0056]. Occupancy counts are unchanged, so neither split nor merge is triggered.

What does happen is `setwispupwards` after displacement mutations, which recalculates each ancestor node's `cdsp` (minimum displacement) and `cwid` (extent width) to reflect the new V-position distribution [INV-ENFILADE-RELATIVE-ADDRESSING/Finding 0066]. This is structural bookkeeping, not rebalancing. Compare with INSERT, which explicitly calls `splitcrumupwards` after adding a crum [ST-INSERT/Finding 0060], or DELETE, which explicitly calls `recombinend` after removing crums [ST-DELETE/Finding 0058]. The REARRANGE code path has neither.

## Does the diagonal-sum reordering ever change logical V-address ordering?

No. Confluence is guaranteed regardless of tree shape.

The diagonal sort in `recombinend` — ordering children by `cdsp.dsas[0] + cdsp.dsas[1]` (L1-norm) — determines which pairs of siblings are *considered* for merging, and determines the resulting tree shape after rebalancing [ST-REBALANCE-2D/Finding 0071]. Different insertion histories or rearrangement sequences can produce different tree shapes with different sibling orderings.

But retrieval is insulated from this at the collection layer. `incontextlistnd()` performs explicit insertion-sort by V-address on every context discovered during B-tree traversal [INV-RETRIEVAL-V-SORTED/Finding 0078]. The discovery order — which follows tree sibling structure, itself a product of diagonal ordering — is irrelevant to the final result:

> "The V-ordering of retrieval results is independent of the internal B-tree structure... even if split/rebalance operations or out-of-order insertions produce a tree where sibling order does not match V-address order, the `incontextlistnd` insertion-sort re-establishes V-ordering during retrieval." [INV-RETRIEVAL-TREE-INDEPENDENCE/Finding 0078]

This is consistent with [INV-ENFILADE-CONFLUENCE/Finding 0041]:

> "Confluence holds at the abstraction boundary (query results) but NOT at the physical level (tree shape, sibling ordering, split points differ based on insertion order)."

## Summary

`recombinend` does not fire after REARRANGE because occupancy is unchanged. Even in cases where rebalancing does fire (e.g., after DELETE), the diagonal reordering is a physical tree property, not an observable one — `incontextlistnd`'s insertion-sort guarantees V-address ordering in all retrieval results regardless of how the 2D enfilade is shaped internally.

---

## Code Exploration

I have all the code I need. Let me now compose the full answer.

---

## Answer: `recombinend` After REARRANGE — Confluence and Diagonal-Sum Ordering

### 1. Does `recombinend` fire?

**Yes, unconditionally for POOM.** The call chain is:

`rearrangend` [edit.c:139]:
```c
recombine (fullcrumptr);
```

`recombine` [recombine.c:22–34]:
```c
int recombine(typecuc *father)
{
    switch (father->cenftype) {
      case POOM:
            recombinend (father);
    }
}
```

Note that `rearrangend` passes `fullcrumptr` — the full-crum root — not just `father` (the intersection node found at line 111). So `recombinend` is called on the entire POOM tree, not only on the subtree that was mutated. This is a wider sweep than, for example, `deletend`, which only calls `recombine(father)` on the local intersection node [edit.c:75].

**The `modified` guard is also satisfied.** During the offset-adjustment loop [edit.c:125–127], every moved crum calls `ivemodified(ptr)`. `ivemodified` [genf.c:539] chains upward setting `modified = TRUE` on each leftmost-ancestor. The preceding `setwispupwards(father, 1)` call [edit.c:137] propagates wid sums. Thus by the time `recombine` fires, the `modified` flag is set through the path from moved crums up to the root, satisfying the guard in `recombinend` [recombine.c:112]:

```c
if (father->height < 2  || !father->modified)
    return(0);
```

---

### 2. What `recombinend` actually does

`recombinend` [recombine.c:104–131] is a post-order bottom-up tree rebalancing pass:

```c
int recombinend(typecuc *father)
{
    // depth-first: process children first
    for (ptr = getleftson(father); ptr; ptr=(typecorecrum *)getrightbro(ptr)){
        recombinend(ptr);
    }

    getorderedsons (father, sons);  // sort sons by diagonal sum
    n = father->numberofsons;
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){
                takeovernephewsnd (&sons[i], &sons[j]);
            }
        }
    }
    if (father->isapex)
        levelpull(father);
}
```

The goal is to **collapse under-full sibling upper-crums** (UCs) by moving grandchildren from one sibling into another. The pair selection is driven by `ishouldbother` [recombine.c:150–163], which checks that `dest->numberofsons + src->numberofsons <= MAX2DBCINLOAF` (or `MAXUCINLOAF` for height > 1).

---

### 3. The Diagonal-Sum Sort

`getorderedsons` [recombine.c:270–280] collects sons into an array and calls `shellsort`:

```c
int shellsort(typecorecrum *v[], INT n)
{
    for(i=0;i<n;i++){
        tumbleradd(&v[i]->cdsp.dsas[0],&v[i]->cdsp.dsas[1],&tarray[i]);
        tarrayp[i] = &tarray[i];
    }
    // shell-sort by tarray[i] ascending
}
```

The key [recombine.c:298]: `tarray[i] = cdsp.dsas[0] + cdsp.dsas[1]`. For POOM, `dsas[0]` = I-space displacement, `dsas[1]` = V-space displacement. The sort key is the tumbler sum of both dimensions — the "diagonal" in I×V space. Sons with smaller diagonal sums are listed first and become **merge destinations** (outer-`i` position), while sons with larger diagonal sums are **merge sources** (inner-`j` position).

This ordering is purely a **merge-priority heuristic**. It does not reorder the content in logical V-space, nor does it control which bottom crums end up in which UC — only in what sequence merges are attempted.

---

### 4. Does the diagonal-sum reordering change logical V-address ordering?

**No. Confluence is guaranteed.**

The logical V-address of any bottom crum is the sum of all `cdsp.dsas[V]` values along the path from root to that crum. Every merge operation (`eatbrossubtreend` and `takenephewnd`) performs an exact coordinate-frame transform that preserves this absolute address.

**`eatbrossubtreend`** [recombine.c:205–233]:
```c
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);
fixdspsofbroschildren (me, bro);
// splice bro's children onto the right end of me's child list
getleftson(bro)->leftbroorfather = getrightmostbro(getleftson(me));
getrightmostbro(getleftson(me))->rightbro = getleftson(bro);
```

`fixdspsofbroschildren` [recombine.c:259–268]:
```c
for (nephew = getleftson(bro); nephew; nephew = getrightbro(nephew)){
    dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);
    dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
    ivemodified(nephew);
}
```

This transforms each nephew's cdsp from bro-relative → absolute → me-relative. The absolute V-address is:

```
before: bro->cdsp[V] + nephew_old_cdsp[V]
after:  me->cdsp[V]  + nephew_new_cdsp[V]
      = me->cdsp[V]  + (bro->cdsp[V] + nephew_old_cdsp[V] - me->cdsp[V])
      = bro->cdsp[V] + nephew_old_cdsp[V]   ← identical
```

**`takenephewnd`** [recombine.c:235–257] performs the same transform for the partial-merge case:
```c
dspadd(&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);  // → absolute
// ... adopt nephew under me ...
dspsub(&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);    // → me-relative
```

Again, absolute address is invariant.

**Retrieval is address-based, not sibling-position-based.** `prologuend` [retrie.c:334–339] computes absolute addresses:
```c
dspadd(offset, &ptr->cdsp, grasp, ...);
dspadd(grasp, &ptr->cwid, reach, ...);
```

And `whereoncrum` [retrie.c:345–398] classifies a query address against `[grasp, grasp+cwid)`. No code in the retrieval path uses sibling position to determine whether a crum's content is relevant — only `cdsp` and `cwid` values matter. Similarly, `findsontoinsertundernd` [insertnd.c:277–298] iterates all siblings and selects by DSP comparison, not by position in the sibling list.

---

### 5. The POOM Split/Merge Metric Mismatch

One architectural oddity: `recombinend` uses **diagonal sum** (V+I) as its merge priority [recombine.c:298], but `splitcrumpm` [split.c:117–128] uses a **maximum SPANRANGE** criterion:

```c
int splitcrumpm(typecuc *father)
{
    for(correctone=ptr=findleftson(father);ptr;ptr=findrightbro(ptr)) {
        if (tumblercmp(&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);
}
```

And notably [edit.c:141] after `recombine`, `rearrangend` also calls:
```c
(void)splitcrumupwards(fullcrumptr);/* can we move this before recombine ?*/
```

The comment "can we move this before recombine?" shows the authors were uncertain about the ordering. These two passes (merge by diagonal-sum priority, then split by max-SPANRANGE) are different heuristics operating on the same tree. Neither affects confluence — they affect tree balance and I/O performance, not logical content.

---

### Summary

| Question | Answer | Key evidence |
|---|---|---|
| Does `recombinend` fire after REARRANGE? | **Yes**, on the full-crum root | `edit.c:139`, `recombine.c:31` |
| Guard conditions satisfied? | Yes — `ivemodified` [edit.c:127] sets `modified=TRUE` up the ancestor chain | `genf.c:539`, `recombine.c:112` |
| What does diagonal-sum sort control? | **Merge priority** only — which sibling pairs are attempted first | `recombine.c:296-310` |
| Does it change logical V-address ordering? | **No** — each merge performs an exact coordinate transform preserving absolute addresses | `recombine.c:259-268`, `recombine.c:243` |
| Is confluence guaranteed? | **Yes** — retrieval uses `cdsp`/`cwid` arithmetic, not sibling position | `retrie.c:334-398` |
| Any caveats? | POOM split uses SPANRANGE-max metric, merge uses diagonal-sum; ordering of split-vs-recombine is unresolved in the code itself | `split.c:123`, `edit.c:141` comment |
