## Question 3 [evidence]

> Does udanax-green's enfilade representation maintain a canonical (e.g., maximal-merged) run decomposition, or can the same arrangement be represented by multiple decompositions of different cardinality — and does the abandoned consolidation function suggest the implementation tolerates non-canonical forms?

## KB Synthesis

## Enfilade Canonicity in udanax-green

The answer is: **non-canonical representations are tolerated at multiple levels**, and the disabled consolidation function is direct evidence of this.

---

### What canonicity would require

A canonical run decomposition would demand that any two logically equivalent V→I mappings produce identical crum cardinality — i.e., contiguous same-provenance runs are always maximally merged into a single crum.

---

### Where canonicity holds (partially)

The `isanextensionnd` check in `insertnd.c:293-301` provides **write-time coalescing** [ST-INSERT, Finding 0062]:

- If new content's I-address origin equals an existing crum's reach, AND
- both share the same `homedoc`

then the existing crum is extended in-place rather than a new crum allocated. This is why [INV-VSPAN-CONSOLIDATION] observes that 100 sequential single-character inserts yield `span_count: 1` — the extension mechanism prevents fragmentation during contiguous typing.

But this is opportunistic consolidation at write time, not a canonical invariant.

---

### Where canonicity breaks down

**1. Different-provenance content in V-contiguous positions**

`isanextensionnd` fails the homedoc check when content from different source documents occupies contiguous V-positions [ST-VCOPY, Finding 0046]. Two crums remain where one logically could suffice. The same logical content arrangement has different cardinality depending on insertion origin.

**2. Tree height is monotonically non-decreasing**

`levelpull` — the abandoned consolidation function [SS-ENFILADE-TREE, Finding 0058] — was intended to reduce tree height when the fullcrum has only one child. It is disabled: `genf.c:318-342` returns 0 immediately without executing. The consequence is explicit in [INV-ENFILADE-MINIMALITY]:

> The actual invariant is `enf.height ≥ 1` (lower bound only, no upper bound tightness guarantee). The intended invariant `enf.height = min_height(content)` does not hold.

A document reduced to a single byte after growing to N bytes retains the full tree height from its growth phase, with empty intermediate nodes. This is a different structural representation than a freshly-created document containing the same byte.

**3. Post-split crums are not remerged**

An interior insert costs +2 crums (split existing crum, add new) [ST-CRUM-BOUND, Finding 0062]. These are not later consolidated even if subsequent operations make them logically mergeable. `recombinend` [ST-REBALANCE-2D, Finding 0071] consolidates **upper-level** nodes to maintain occupancy invariants, but bottom crums (the content leaves) are not subject to that merging pass.

**4. [INV-ENFILADE-CONFLUENCE] confirms insertion-order dependence**

> Different insertion orderings produce different tree shapes (sibling ordering, split points, disk layout) but identical query results.

Two different physical representations yield identical query results — precisely because the system doesn't normalize to a canonical form. Canonicity is sacrificed in favor of confluence at the query interface.

---

### The GRAN singleton anomaly

For granfilades specifically, `MAXBCINLOAF = 1` [SS-GRAN-MB-ONE, SS-GRAN-BOTTOM-SINGLETON] makes each bottom crum hold exactly one text entry — making the notion of "maximal merging" at the bottom level vacuous. There is nothing to merge. The effective representation is always a list of singleton crums at height-0.

---

### Summary

The enfilade tolerates non-canonical forms at both levels:

| Level | Canonicity? | Reason |
|-------|-------------|--------|
| Bottom crum content | Partial only | `isanextensionnd` coalesces same-homedoc rightward-contiguous content at write time; cross-provenance or non-contiguous content stays split |
| Tree height | No | `levelpull` disabled; height monotonically non-decreasing regardless of content |
| Sibling order | No | Insertion-order-dependent [INV-ENFILADE-CONFLUENCE] |

The abandoned `levelpull` is the clearest signal that the system was *designed* with canonicity in mind (height should reflect content) but the implementation explicitly abandons the height-reduction half of that contract. The spec should state [INV-ENFILADE-MINIMALITY]: tree minimality is not an invariant.

---

## Code Exploration

I now have all the evidence I need. Let me compile the full answer.

---

## Does udanax-green maintain a canonical run decomposition?

**No.** The enfilade representation does not maintain a canonical (maximally-merged) form. The same logical arrangement can be represented by multiple crum-tree decompositions of different cardinality. The abandoned consolidation code is not merely vestigial — it is the primary evidence that this non-canonicality was recognized and left unresolved.

---

### 1. `levelpull` is fully stubbed out — structural height is never reduced

`backend/genf.c:318-342`:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/*
    if (!isfullcrum (fullcrumptr))  ...
    if (fullcrumptr->numberofsons > 1)
        return;
    if (fullcrumptr->height <= 1)
        return;
    ptr = (typecuc *) findleftson (fullcrumptr);
    dspadd (&fullcrumptr->cdsp, &ptr->cdsp, &fullcrumptr->cdsp, fullcrumptr->cenftype);
    disown (ptr);
    fullcrumptr->height--;
    transferloaf (ptr, fullcrumptr);
    setwispupwards (fullcrumptr,1);
    freecrum (ptr);
*/
}
```

The entire real implementation is commented out. `levelpull` is called from both `recombineseq` (`recombine.c:67`) and `recombinend` (`recombine.c:130`) whenever the fullcrum is the apex — but it always returns 0 immediately. Its job would have been: after deletions reduce a fullcrum to a single child, collapse that redundant level. Since it never runs, a tree that grew to height N during heavy insertions keeps that height even after deletions reduce it to a structure that could fit in height N−1 or lower. Two equivalent states (same content, different tree depths) are thus permanently representable.

---

### 2. `recombineseq` has a hard height floor and a single-pair-per-pass limit

`backend/recombine.c:38-68`:

```c
int recombineseq(typecuc *father) /** zzz reg 1999 this recombines too much */
{
  typecuc *ptr;
    if (father->height < 3 || !father->modified) {
        return(0);
    }
    ...
    for (ptr = (typecuc *)getleftson(father); ptr && ptr->rightbro;
         ptr = (typecuc *)findrightbro((typecorecrum *)ptr)) {
        if (ptr->leftson && roomformoresons(ptr)) {
            if (...combined sons fit...) {
                eatbrossubtreeseq(ptr);
                break;              // ← exits after ONE merge
            } else {
                takeovernephewsseq(ptr);
                break;              // ← exits after ONE partial transfer
            }
        }
    }
    if (father->isapex)
        levelpull(father);  // ← dead, see §1
}
```

Two structural defects here:

- **Height guard**: `if (father->height < 3) return(0)`. Granfilades with height ≤ 2 — including the common case of a shallow document — are **never recombined at all**. Adjacent siblings that could be merged into one are left split indefinitely.

- **Single merge per call**: The `break` after both `eatbrossubtreeseq` and `takeovernephewsseq` means each invocation of `recombineseq` consolidates at most one adjacent pair. A series of insertions that left five under-full siblings where two could be merged would require five separate operation cycles before they converge — and only if the tree has height ≥ 3 at each point.

---

### 3. `recombinend` (2D) has the same height floor and an inert probability gate

`backend/recombine.c:104-131`:

```c
int recombinend(typecuc *father)
{
    if (father->height < 2 || !father->modified)
        return(0);
    ...
    for (i = 0; i < n-1; i++) {
        for (j = i+1; sons[i] && j < n; j++) {
            if (i != j && sons[j] && ishouldbother(sons[i], sons[j])) {
                takeovernephewsnd(&sons[i], &sons[j]);
            }
        }
    }
    if (father->isapex)
        levelpull(father);  // ← dead
}
```

The 2D variant guards on `height < 2`: height-1 parents (direct parents of bottom crums) are never recombined. And the `ishouldbother` gate contains the remnant of a probabilistic policy:

`backend/recombine.c:132-163`:

```c
bool randomness(float probability)
{
  static float i = 0;
  return(TRUE);
  /*
    i += probability;
    if (i >= 1.) { while (i>1) { i -= 1.; } return(TRUE); }
    else { return FALSE; }
  */
}

bool ishouldbother(typecuc *dest, typecuc *src)
{
    ...
    return (dest->numberofsons + src->numberofsons <= (...capacity...) && randomness(.3));
}
```

The probabilistic body is commented out; `randomness` unconditionally returns `TRUE`. The `.3` argument is now dead. The comment `.3` (30% probability) reveals that the original design intentionally allowed non-canonical states — merging was a probabilistic background compaction, not a correctness invariant. Although the probability is now always 1.0, the height guard still prevents leaf-level parents from ever consolidating.

---

### 4. Insert-time extension check is opportunistic, not canonical

`backend/insertnd.c:249-258` (`insertcbcnd`):

```c
for (ptr = findleftson(father); ptr; ptr = findrightbro(ptr)) {
    if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd(&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
        ivemodified(ptr);
        setwispupwards(father, 1);
        return(FALSE);
    }
}
```

`isanextensionnd` (`insertnd.c:301-309`) returns TRUE only when the new content's origin precisely equals the reach (end point) of an existing bottom crum — i.e., an exact adjacency on the V axis. This is the one canonicalization path: a suffix-contiguous insertion extends an existing crum rather than creating a new one. But this covers only the append-to-tail case and only at the time of insertion. Deletions, out-of-order insertions, and copy operations that introduce new spans do not trigger this path, leaving fragmented states that are never subsequently merged at the height-1 level.

---

### 5. `recombine` call sites confirm the reactive, non-exhaustive pattern

Three call sites exist:

- `edit.c:27`: `recombine(findfather((typecorecrum*)ptr))` — after `deleteseq`, called on the *direct parent only*, not the fullcrum.
- `edit.c:75`: `recombine(father)` — after `deletend`, on the local intersection father.
- `insertnd.c:76`: `recombine(fullcrumptr)` — after `insertnd`, on the fullcrum.

None of these repeatedly invoke `recombine` to convergence. There is no fixpoint loop; a single call is made and the structure is accepted as-is. In the granfilade case the single call does at most one merge per level (due to the `break`); in the 2D case, height-1 nodes are never touched.

---

### Summary

| Mechanism | Code | Effect on canonicality |
|---|---|---|
| `levelpull` | `genf.c:318` — fully commented out | Unnecessary height levels persist after deletions |
| `recombineseq` height guard | `recombine.c:41` — `height < 3` | Shallow granfilades never recombine |
| `recombineseq` single-pair limit | `recombine.c:58` — `break` after first merge | Multiple under-full siblings coexist indefinitely |
| `recombinend` height guard | `recombine.c:112` — `height < 2` | Leaf-parent nodes never recombine in 2D enfilades |
| `randomness()` stub | `recombine.c:134` — `return(TRUE)` with probabilistic body commented out | Originally a 30%-chance background compaction, not a correctness guarantee |
| `isanextensionnd` | `insertnd.c:250` | Canonicalizes only exact suffix-contiguous insertions |

The comment `/** zzz reg 1999 this recombines too much */` on `recombineseq` (`recombine.c:38`) is the developer's own acknowledgment that the merge behavior was under active uncertainty in 1999. The concern was over-consolidation, not insufficient consolidation — meaning canonical minimality was not the design invariant. Combined with `levelpull`'s permanent stub, the implementation unambiguously tolerates non-canonical forms: the same document state can be represented by enfilade trees of different node count and different height.
