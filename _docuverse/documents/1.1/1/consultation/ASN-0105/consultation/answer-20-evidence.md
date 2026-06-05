## Question 20 [evidence]

> Across the different physical tree shapes a POOM can take (taller after DELETE, varied split history), does a read of the same logical V-span always produce byte-identical results, confirming [INV-ENFILADE-CONFLUENCE] holds for contiguous span reads?

## KB Synthesis

Yes, reads of the same logical V-span produce byte-identical results regardless of physical POOM tree shape. Three orthogonal mechanisms guarantee this:

**1. Absolute grasp is deterministically reconstructed** — [INV-ENFILADE-RELATIVE-ADDRESSING] proves that `absolute_grasp(node) = Σ ancestor displacements + node.cdsp`, maintained by `setwispnd`. Whether the tree is tall (after disabled `levelpull` per [SS-ENFILADE-TREE]) or compact, the traversal at `retrie.c:337` (`grasp = offset + cdsp`) reconstructs the same absolute V-positions from relative displacements.

**2. Retrieval output is re-sorted regardless of tree traversal order** — [INV-RETRIEVAL-V-SORTED] and [INV-RETRIEVAL-TREE-INDEPENDENCE] confirm that `incontextlistnd()` performs insertion-sort by V-address as contexts are discovered. Even if `setwispnd`'s diagonal rebalancing ([SS-ENFILADE-TREE] Finding 0071) reorganizes sibling order, the accumulated context list is V-sorted before return — independent of tree structure.

**3. I-address → byte mapping is immutable** — [INV-IADDR-IMMUTABILITY] guarantees that the granfilade is append-only and a given I-address always maps to the same bytes, regardless of how many POOM reshapes have occurred since insertion.

**Scope clarification:** [INV-ENFILADE-CONFLUENCE] as stated covers the permanent layer (ispace + spanf) under concurrent additions. For the POOM — which is mutable [SS-POOM-MUTABILITY] — the analog is [INV-ENFILADE-QUERY-INDEPENDENCE]: "Different insertion orderings produce different tree shapes but identical query results." This is the direct confirmation you're looking for.

**One genuine carve-out:** [INV-POOM-BIJECTIVITY] notes that certain DELETE sequences can leave negative-V-position POOM entries — present in the tree but invisible to positive V-span queries. These produce *consistently absent* results (always excluded), so reads remain deterministic; they just return fewer results than the pre-corruption state. That's a state-change effect, not a tree-shape effect.

Bottom line: for any fixed POOM logical state, physical tree shape variation — from split history, disabled `levelpull`, or rebalancing diagonal ordering — does not alter the bytes returned for a contiguous V-span read.

---

## Code Exploration

I have enough information to trace the complete confluence argument. Now let me synthesize the full analysis.

---

# [INV-ENFILADE-CONFLUENCE] for POOM Contiguous V-Span Reads

## Question

Does reading the same logical V-span from a POOM produce byte-identical results regardless of the physical tree shape produced by different DELETE/split histories?

---

## 1. The Retrieval Path

A V-span read enters through `doretrievev` → `permute` → `span2spanset` → `retrieverestricted` → `retrieveinarea` → **`findcbcinarea2d`** [retrie.c:229].

`findcbcnd` [retrie.c:208] handles single-address POOM lookups via the same logic. Both accumulate an absolute offset as they descend:

```c
/* retrie.c:208-227 */
typecontext *findcbcnd(typecorecrum *father, typewid *offsetptr, tumbler *address, INT index)
{
    if ((cmp = whereoncrum(father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME)
        return(NULL);
    if (father->height != 0) {
        prologuend(father, offsetptr, &grasp, NULL);  // grasp = offset + father.cdsp
        for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr))
            if (retr = findcbcnd(ptr, &grasp, address, index))  // pass grasp as new offset
                break;
    } else {
        retr = makecontextfromcbc((typecbc*)father, offsetptr);  // FOUND
    }
    return(retr);
}
```

`prologuend` [retrie.c:334-338] computes:
```c
grasp = offset + ptr->cdsp
reach = grasp + ptr->cwid
```

The `grasp` passed into children is the **accumulated absolute position** — `offset + father.cdsp` — not zero. The absolute V-position of any bottom crum is therefore:

> **abs\_V = Σ (cdsp[level] for each ancestor) = offset + cdsp**

This computation is purely arithmetic over the path from root to leaf. **It is insensitive to the width of the tree, how many siblings exist at each level, or the tree's height.**

---

## 2. How Tree Shape Changes Occur

### 2a. DELETE → shape change via `deletend` [edit.c:31-75]

After a delete, surviving crums whose V-address is above the deletion boundary have their displacement adjusted:

```c
/* edit.c:63-64 */
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
```

This subtracts the deleted width from the V-displacement of every crum that follows the deleted range. The result: absolute V-positions of surviving content shift down by `width`, which is exactly what delete semantics require. The tree then calls `setwispupwards(father, 1)` and `recombine(father)`.

**Tree becomes taller after DELETE because `levelpull` is disabled:**

```c
/* genf.c:318-342 */
int levelpull(typecuc *fullcrumptr) {
    return(0);  // ENTIRE BODY IS COMMENTED OUT
    /* ... */
}
```

`recombineseq` [recombine.c:66] calls `levelpull(father)` but it is a no-op. The tree therefore **never shrinks in height after deletion** — a node with one remaining child stays at the same level. This means a document subjected to multiple deletes accumulates levels. The tree is taller than necessary, but the traversal still visits all reachable bottom crums correctly.

### 2b. Split history → shape change via `splitcrumpm` [split.c:111-120]

When a POOM internal node overflows `MAX2DBCINLOAF` children:

```c
/* split.c:111-119 */
int splitcrumpm(typecuc *father) {
    for (correctone=ptr=findleftson(father); ptr; ptr = findrightbro(ptr))
        if (tumblercmp(&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    peelcrumoffnd(correctone);
}
```

It picks the child with the **largest SPANRANGE displacement** and peels it off via `peelcrumoffnd` [split.c:122-160]:

```c
/* split.c:134-158 */
father = findfather(ptr);
disown(ptr);                              // remove ptr from father's children
new = createcrum(father->height, father->cenftype);
adopt(new, RIGHTBRO, (typecorecrum*)father); // new is right sibling of father
movewisp(&father->cdsp, &new->cdsp);     // new.cdsp = father.cdsp (key!)
adopt(ptr, LEFTMOSTSON, new);            // ptr under new
setwispupwards(father, 0);
setwispupwards((typecuc*)new, 0);
setwispupwards((typecuc*)ptr, 1);
```

After this, `father` and `new` share the **same `cdsp` value** but will have **different `cwid` values** once `setwispupwards` finishes. Two siblings with identical `cdsp` is valid in POOM because the query `crumqualifies2d` uses both `cdsp` and `cwid` to determine intersection — a sibling is skipped if the query range falls entirely outside `[cdsp, cdsp + cwid)`.

---

## 3. The Wid-Maintenance Invariant

The correctness of retrieval depends on internal nodes' `cwid` values being the **minimum bounding box** of all descendant crums. This is maintained by `setwispnd` [wisp.c:171-228].

`setwispnd` performs a non-trivial normalization:

```c
/* wisp.c:193-215 */
/* find minimum dsp across all children */
movewisp(&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro(ptr))
    lockmin(&mindsp, &ptr->cdsp, &mindsp, dspsize(ptr->cenftype));

if (!lockiszerop) {
    /* shift father's cdsp forward by mindsp */
    dspadd(&father->cdsp, &mindsp, &newdsp, father->cenftype);
    /* shift all children's cdsp backward by mindsp */
    dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, ptr->cenftype);
}
/* compute bounding box newwid = max(child.cdsp + child.cwid) */
for (ptr = findleftson(father); ptr; ptr = getrightbro(ptr)) {
    lockadd(&ptr->cdsp, &ptr->cwid, &tempwid, widsize(ptr->cenftype));
    lockmax(&newwid, &tempwid, &newwid, widsize(ptr->cenftype));
}
movewisp(&newdsp, &father->cdsp);
movewisp(&newwid, &father->cwid);
```

This preserves absolute positions:

> **old\_abs = parent\_offset + old\_father.cdsp + old\_child.cdsp**
> **new\_abs = parent\_offset + (old\_father.cdsp + mindsp) + (old\_child.cdsp − mindsp)**
>           **= parent\_offset + old\_father.cdsp + old\_child.cdsp ✓**

The same invariant is maintained in `recombine` operations. `fixdspsofbroschildren` [recombine.c:259-267] converts nephew displacements from relative-to-bro to relative-to-me:

```c
dspadd(&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype); // make absolute
dspsub(&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);  // re-relativize to me
```

> **old\_abs = parent + bro.cdsp + nephew.cdsp**
> **new\_abs = parent + me.cdsp + (bro.cdsp + old\_nephew.cdsp − me.cdsp)**
>           **= parent + bro.cdsp + old\_nephew.cdsp ✓**

`takenephewnd` [recombine.c:235-256] applies the same arithmetic, and `expandcrumleftward` [makeroom.c:52-73] adds `base` to all children's `cdsp[index]` while subtracting it from the father's new position — again preserving absolute positions.

---

## 4. What Changes, What Does Not

| Operation | Tree Shape Change | Bottom Crum Positions | Wid/Dsp Maintained? |
|-----------|------------------|-----------------------|---------------------|
| DELETE | Taller (levelpull is no-op); fewer crums; one crum's cdsp adjusted by `tumblersub` | Surviving content shifts by −width above deletion | Yes — `setwispupwards` called, `recombine` called |
| INSERT | May split nodes; height may increase | New crums inserted at correct V-position | Yes — `setwispupwards` called in `insertnd.c:56-58` |
| `splitcrumpm` | Two siblings where one was; both get same cdsp, different cwid | Unchanged — split is pure structural | Yes — three `setwispupwards` calls in `peelcrumoffnd` |
| `recombinend` | Fewer internal nodes; siblings merged | Unchanged — recombine is pure structural | Yes — `setwispupwards` called in `takeovernephewsnd`, `eatbrossubtreend` |

---

## 5. One Potential Weakness

In `insertnd.c:31-32`:

```c
/* insertnd.c:31-32 (DISTRIBUTION build only) */
/**/fixincoresubtreewids(fullcrumptr);/*1999 // a temp kluge zzz
till we find where setwisp isnt called// this is a brute force
kluge, if this fixes anything it means that the wids aren't being
set properly somewhere else probably near here */
```

And at `insertnd.c:79` (debug build only):

```c
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){
    fprintf(stderr,"insertnd possible error dumping widdiffs...");
```

Both guards — one commented out, one `FALSE&&`-guarded — indicate a **1999-era uncertainty** about whether `setwisp` was being called in all paths. `fixincoresubtreewids` [recombine.c:321-334] is a brute-force wid recomputation of the entire in-core subtree. Its comment says "if this fixes anything it means that the wids aren't being set properly somewhere else."

This code is **disabled in all builds** (both DISTRIBUTION and debug). The implication: either the original bug was located and fixed, or it was accepted that the wids could become stale in certain insert paths. If stale wids occur, `crumqualifies2d` could return FALSE for a node that actually intersects the query — causing the traversal to skip a bottom crum and return **incomplete results** (missing content, not corrupted content).

However: looking at the `makegappm` → `doinsertnd` → `insertcbcnd` path, `setwispupwards` is called at `insertnd.c:56-58`, `insertnd.c:63`, and inside `insertcbcnd` at `insertnd.c:237-238,252-253`. The paths appear covered.

---

## 6. Conclusion

**[INV-ENFILADE-CONFLUENCE] holds for POOM contiguous V-span reads under the following reasoning:**

1. **Retrieval is structurally invariant.** `findcbcnd`/`findcbcinarea2d` compute absolute V-positions by accumulating `cdsp` values down the path from root to leaf [retrie.c:208-227, retrie.c:334-338]. This arithmetic depends only on the path values, not on sibling count, branching factor, or tree height.

2. **All mutations preserve absolute bottom-crum positions.** `setwispnd`, `fixdspsofbroschildren`, `takenephewnd`, `expandcrumleftward`, and the `tumblersub` in `deletend` all maintain the invariant that the accumulated `cdsp` sum equals the true absolute V-address.

3. **Bounding boxes are maintained bottom-up.** `setwispupwards` → `setwispnd` is called after every structural change (delete, insert, split, recombine). Internal nodes' `cwid` values always encompass the bounding box of all descendant crums, ensuring no bottom crum is missed during traversal.

4. **`levelpull` being a no-op [genf.c:318-321] means trees only grow taller** — a performance issue, not a correctness one. A taller tree visits more levels during retrieval but finds the same set of bottom crums.

5. **The `fixincoresubtreewids` kluge [insertnd.c:31-32]** was introduced and then disabled, flagging a historic worry about wid-staleness after inserts. If wids can become stale in the insert path, a retrieval after insert could miss crums whose ancestor's `cwid` was not updated. This is the **one unresolved risk** to the invariant in production code.

**Bottom line:** The design of the POOM enfilade guarantees confluence at the algorithmic level. Every deletion and split produces a different tree shape but identical bottom-crum absolute addresses. The retrieval accumulates those addresses independently of tree structure. The `fixincoresubtreewids` comment is the only code-level evidence of a potential gap — that particular gap was explicitly known and gated out, suggesting it was either fixed or considered negligible in practice.
