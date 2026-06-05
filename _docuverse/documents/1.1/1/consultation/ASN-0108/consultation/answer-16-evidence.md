## Question 16 [evidence]

> Does the windowed enumeration order remain stable across calls regardless of spanfilade tree height growth, consistent with INV-ENFILADE-CONFLUENCE, or can tree restructuring between calls permute the order?

## KB Synthesis

## Windowed Enumeration Order Stability

The answer splits cleanly into two claims that the KB supports independently.

### Tree Restructuring Alone Does Not Permute Order

When the set of matching links is fixed between calls, tree height growth and structural reorganization cannot permute the enumeration order.

The mechanism is `incontextlistnd()` [SS-CONTEXT-LIST], which performs explicit insertion-sort on every retrieval, regardless of B-tree traversal order. Because the SPAN enfilade is 2D (not GRAN), it uses `incontextlistnd()` rather than `oncontextlistseq()`. The sorted dimension is the ORGLRANGE boundary (`totaloffset.dsas[index]`).

[INV-RETRIEVAL-TREE-INDEPENDENCE] states this directly: "tree-internal reorganization (splits, rebalances, rotations) does not change the observable result ordering of retrieval operations... the `incontextlistnd` insertion-sort re-establishes ordering during retrieval." [INV-ENFILADE-CONFLUENCE] reinforces this at the set level: different tree shapes from concurrent insertions "produce the same set of I-address mappings and the same results for retrieve and retrieveinspan queries."

The SPAN-specific split strategy ([ST-SPLIT-2D]) and diagonal rebalancing ([ST-REBALANCE-2D]) affect tree shape but not retrieval output ordering, because that ordering is re-derived fresh on each call via insertion-sort.

### New Link Creation Between Calls Breaks Stability

[SS-PAGINATE-LINKS] and [EC-CURSOR-INVALIDATION] document the actual instability source. FINDNEXTNLINKSFROMTOTHREE **re-executes the full `findlinksfromtothreesp()` search on every call** — no server-side cursor state persists. If new links are created between paginated calls:

- Their ISA tumblers interleave into the sorted result list
- Links with ISAs between the cursor and position N shift to later pages
- Links with ISAs before the cursor are silently missed
- If the cursor link ISA is deleted, the cursor walk returns empty with count=0

This instability comes from **content change** (new entries in the spanfilade), not from tree restructuring. The fact that new links also trigger `levelpush` / splits (height growth) is irrelevant — [INV-RETRIEVAL-TREE-INDEPENDENCE] insulates ordering from those structural changes.

### Conclusion

Consistent with [INV-ENFILADE-CONFLUENCE]: tree height growth per se does not permute enumeration order. The `incontextlistnd` insertion-sort on the SPAN enfilade produces identical sorted output regardless of tree shape. But [EC-CURSOR-INVALIDATION] documents that the stateless re-execution model provides no cross-call consistency — new link insertions (which happen to grow the tree) alter the result *set*, causing pages to shift.

---

## Code Exploration

I now have everything I need. Let me write the full analysis.

---

## Windowed Enumeration Order Stability in udanax-green

**Short answer:** The enumeration order is stable across calls regardless of tree height growth. The invariant holds through different mechanisms in the two enfilade types (GRAN sequential, SPAN/POOM 2D), and `levelpull` is entirely disabled so height can only increase.

---

### The Two Retrieval Paths

There are two distinct enumeration functions, one per enfilade type, with fundamentally different ordering guarantees.

**GRAN — `findcbcinspanseq` (retrie.c:307–329)**

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumintersectsspanseq (...)) {
        dspadd (...);
        continue;
    }
    if (crumptr->height == 0) {
        context = makecontextfromcbc (...);
        oncontextlistseq (headptr, context);        // appends to tail
    } else {
        findcbcinspanseq(findleftson((typecuc*)crumptr), ...);
    }
    dspadd (&localoffset, &crumptr->cwid, &localoffset, ...);
}
```

`oncontextlistseq` (context.c:113–123) unconditionally appends to the end of the list. The final result order **is** the left-to-right leaf traversal order. No sort is performed. Order stability therefore depends entirely on whether restructuring preserves the sibling chain's left-to-right semantic ordering.

**SPAN/POOM — `findcbcinarea2d` (retrie.c:229–268)**

```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, ...);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // sorted insertion
    }
}
```

`incontextlistnd` (context.c:75–111) inserts each new context into a **sorted position** in the output list, comparing by `whereoncontext` which reads `totaloffset` — the crum's address-space position. The output is always ordered by tumbler address regardless of the order in which crums are visited during traversal.

---

### GRAN Stability: Restructuring Preserves Sibling Chain Order

The sequential enfilade's invariant: left-to-right sibling order at each level corresponds to increasing sequential content address. Every restructuring operation preserves this.

**`splitcrumseq` (split.c:70–93)**

```c
halfsons = father->numberofsons / 2;
for (i = 0, ptr = findrightmostson(father); i < halfsons && ptr; ++i, ptr = next) {
    next = findleftbro(ptr);
    disown(ptr);
    adopt(ptr, LEFTMOSTSON, new);   // each successive node pushes prior right
}
```

Starting from the rightmost son and repeatedly adopting as LEFTMOSTSON causes the moved nodes to be re-inserted in reverse-of-reverse order, which is the original order. If `father` had children `[A, B, C, D, E]` and `halfsons = 2`:
- Iteration 1: disown E, adopt E as LEFTMOSTSON → `new = [E]`
- Iteration 2: disown D, adopt D as LEFTMOSTSON → `new = [D, E]`
- Result: `father = [A, B, C]` ← rightbro → `new = [D, E]`

The left-to-right content order is completely preserved [split.c:83–88].

**`levelpush` (genf.c:263–294)**

```c
new=(typecuc *)createcrum ((INT)fullcrumptr->height,(INT)fullcrumptr->cenftype);
transferloaf (fullcrumptr, new);       // moves children to new
fullcrumptr->height++;                 // [genf.c:285]
adopt ((typecorecrum*)new, SON, (typecorecrum*)fullcrumptr);
```

`transferloaf` (genf.c:296–315) moves the entire child chain wholesale: it copies `from->leftson` to `to->leftson`, repoints `ptr->leftbroorfather` to the new parent, and zeroes `from->leftson`. The sibling relationships among children are unchanged — only the parent pointer is updated. The new intermediate node `new` becomes the sole child of the grown fullcrum. Traversal now descends through one extra level, but visits the same leaves in the same order.

**`recombineseq` — `takeovernephewsseq` (recombine.c:70–85)**

```c
for(ptr=(typecuc *)getleftson(routinegetrightbro(me)); ptr && roomformoresons(me); ptr=(typecuc *)next){
    next = (typecorecrum *)routinegetrightbro (ptr);
    disown (ptr);
    adopt (ptr, RIGHTMOSTSON, me);    // stolen left-to-right, appended right
}
```

Children are stolen from the right brother in left-to-right order and appended as RIGHTMOSTSON of `me`. Content order is preserved.

**`eatbrossubtreeseq` (recombine.c:87–100)**

```c
getleftson (bro)->leftbroorfather = getrightmostbro (getleftson (me));
getrightmostbro (getleftson (me))->rightbro = bro->leftson;
bro->leftson->isleftmost = FALSE;
me->numberofsons += bro->numberofsons;
disown (bro);
freecrum (bro);
```

This directly splices `bro`'s entire child chain onto the right tail of `me`'s chain — pointer surgery that preserves both chains' internal ordering.

---

### SPAN/POOM Stability: Algebraic Sorting Absorbs Structural Changes

The 2D enumeration order does not depend on sibling order at internal nodes. It depends on the absolute tumbler addresses carried in leaf crums' `cdsp` fields.

`incontextlistnd` (context.c:75–111) sorts by calling `whereoncontext` which computes `left = totaloffset[index]`, `right = left + contextwid[index]` and uses `intervalcmp`. The sort key is the crum's absolute address-space position, not its position in the tree.

Restructuring operations maintain correct `cdsp` values by adjusting them when crums change parents:

**`takenephewnd` (recombine.c:235–257):**

```c
disown (nephew);
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype);   // abs = parent_dsp + relative_dsp
adopt (nephew, RIGHTMOSTSON, me);
makeroomonleftnd (me, &offset, &nephew->cdsp, &grasp);
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);     // new_relative = abs - new_parent_dsp
```

The nephew's displacement is converted to absolute and then back to relative in the new parent's coordinate frame. Its absolute position in address space is unchanged.

**`fixdspsofbroschildren` (recombine.c:259–268):**

```c
for (nephew = getleftson (bro); nephew; nephew =(typecorecrum *)getrightbro (nephew)){
    dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);
    dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);
}
```

Same absolute-position-preserving transform applied to all children when they move.

**`setwispnd` (wisp.c:171–228):**

```c
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr))
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp, (tumbler*)&mindsp, ...);
// ... adjust all children relative to new father origin:
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);
```

This is the widditive operation called by `setwispupwards` after every structural change. It recomputes the parent's `cdsp` as the minimum of its children's displacements, then normalizes all children's `cdsp` values relative to the new origin. Absolute positions are preserved; only relative representations change.

Because `incontextlistnd` sorts by these absolute tumbler addresses, its output is invariant to any restructuring that preserves absolute positions — and all the restructuring code does exactly that.

---

### `levelpull` Is Dead Code

The comment at genf.c:318–342 shows `levelpull` returns immediately:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr)) ...
    if (fullcrumptr->numberofsons > 1) return;
    ...
    fullcrumptr->height--;
    ...
*/
}
```

The entire body is commented out [genf.c:321]. Tree height can only grow (via `levelpush` when a fullcrum overflows). There is no shrinking. This eliminates the only operation that would reduce height and potentially revisit a degenerate case.

---

### Verdict

The windowed enumeration order is stable across calls regardless of tree height growth, consistent with INV-ENFILADE-CONFLUENCE, through two complementary mechanisms:

| Enfilade | Ordering guarantee | Mechanism |
|----------|-------------------|-----------|
| GRAN | Structural: sibling chain order = content order | All restructuring operations (`splitcrumseq`, `levelpush`, `eatbrossubtreeseq`, `takeovernephewsseq`) preserve left-to-right sibling order |
| SPAN/POOM | Algebraic: output list sorted by tumbler address | `incontextlistnd` [context.c:75] sorts by absolute address; restructuring preserves absolute `cdsp` values via coordinate-frame transforms [recombine.c:243, 264] |

Tree height growth via `levelpush` [genf.c:285] changes traversal depth but not the logical ordering of content. `levelpull`, which would be the destabilizing inverse, is entirely disabled [genf.c:321].
