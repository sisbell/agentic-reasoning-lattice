## Question 11 [gregory]

> The `isanextensionnd` coalescing check uses reach-equals-origin adjacency to merge a new insertion into an existing bottom crum — does this coalescing ever fire across a prior DELETE boundary, where two formerly non-adjacent I-spans became adjacent in V-space after intervening content was removed?

## KB Synthesis

No. `isanextensionnd` coalescing cannot fire across a DELETE boundary. Here is why each part of the mechanism prevents it.

---

## What the coalescing check actually tests

From [ST-INSERT] (Findings 0046, 0062): `isanextensionnd` fires only when two conditions hold simultaneously:

1. The new content has the same **homedoc** as the candidate crum
2. The new content's **I-address origin** equals the candidate crum's **I-address reach**

This is an **I-space adjacency test**, not a V-space adjacency test. Two crums can become V-adjacent after DELETE without triggering coalescing, because what matters is whether the new content's allocated I-address picks up exactly where an existing crum leaves off.

---

## Why DELETE cannot create that I-space condition

**I-address allocation is monotonically increasing and non-reusing** [INV-MONOTONIC], [INV-NO-IADDR-REUSE] (Findings 0033, 0061): Every new INSERT draws from `max_iaddr(granf) + 1`. Deleted I-addresses remain permanently allocated in the granfilade [FC-GRANF-ON-DELETE] — DELETE never modifies the granfilade, so the allocation frontier never retreats.

Consider the concrete scenario:

```
INSERT "ABCDE" → crum₁: V[1.1, 1.6) → I.1..I.5, reach = I.6
DELETE [1.3, 1.6) → removes right half of crum₁
  granfilade: still contains I.1..I.5 (frontier = I.5)
  POOM: only crum₂: V[1.1, 1.3) → I.1, I.2, reach = I.3

INSERT "X" at V 1.3:
  Allocates I.6 (next after granfilade max I.5)
  isanextensionnd: I.6 == crum₂.reach(I.3)? → NO
```

The deleted content (I.3–I.5) is still allocated in the granfilade, so the next INSERT gets I.6, not I.3. The surviving crum's reach (I.3) will never equal a future allocation because the frontier has already passed it.

**I-addresses of surviving crums are immutable** [INV-IADDR-IMMUTABILITY] (Finding 0030, 0064). The reach of `crum₂` remains I.3 regardless of subsequent operations. And since all future allocations are strictly greater than the current granfilade maximum (I.5), and I.5 > I.3, no future new content can produce an origin equal to I.3.

---

## The one case coalescing does fire

Coalescing fires only when new content is allocated at exactly the point where the previous allocation ended — i.e., **consecutive inserts with no intervening I-address-consuming operation** [ST-INSERT] (Finding 0062, 0063). CREATELINK breaks this by advancing the frontier [INT-LINK-INSERT] (Finding 0063). DELETE cannot create such an opportunity because it consumes no I-addresses and cannot rewind the frontier.

---

## Summary

The monotonic, non-reusing I-address allocator is the decisive constraint. After DELETE, the granfilade maximum reflects all I-addresses ever allocated (including deleted content), so any subsequent INSERT gets an address above that maximum. A surviving crum's reach is always below that maximum (it was set when those I-addresses were allocated). The two values cannot meet, so `isanextensionnd` cannot fire across a DELETE boundary.

**Relevant entries:** [ST-INSERT], [INV-MONOTONIC], [INV-NO-IADDR-REUSE], [INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE], [INT-LINK-INSERT]

---

## Code Exploration

I have all I need. Here is the full analysis.

---

## Does `isanextensionnd` Coalescing Fire Across a Prior DELETE Boundary?

**Short answer: Yes — but only when a subsequent INSERT arrives at a position whose 2D reach-coordinates exactly match an existing crum, and the V-adjacency was created by the delete. The delete itself causes no spontaneous coalescing.**

---

### 1. The Function

**`insertnd.c:301-309`**

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must both hold:

1. **Homedoc match** (`insertnd.c:305`): `tumblereq` on the home-document ISA of the existing crum vs the new insertion's `infoptr->homedoc`.
2. **Full 2D reach-equals-origin** (`insertnd.c:308`): `lockeq` walks `dspsize(ptr->cenftype)` tumblers.

For POOM and SPAN, `DSPSIZEPM = DSPSIZESP = 2` (`wisp.h:24-26`), and the axes are `I=0`, `V=1` (`wisp.h:19-20`). So `lockeq` checks **both** `reach.dsas[I] == originptr->dsas[I]` AND `reach.dsas[V] == originptr->dsas[V]` simultaneously.

`prologuend` computes reach as `offset + cdsp + cwid` in both dimensions (`retrie.c:334-338`):

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach) {
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`lockeq` itself (`wisp.c:261-266`):

```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize) {
    while (loxize--)
           if (!tumblereq (lock1++, lock2++))
                    return(FALSE);
    return (TRUE);
}
```

The coalescing site is `insertcbcnd` (`insertnd.c:249-258`): it scans all bottom-crum siblings of the insertion point, and on the first hit widens the existing crum in place:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  // insertnd.c:251
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

---

### 2. What DELETE Does to the Tree

`dodeletevspan` (`do1.c:158-167`) calls `deletevspanpm` (`orglinks.c:145-152`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr) {
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` is called with `index = V`. It cuts the tree, then for each surviving bottom crum at the intersection (`edit.c:47-73`):

```c
switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
  case 1:  disown (...); subtreefree (...); break;          // entirely inside range — gone
  case 2:  tumblersub (&ptr->cdsp.dsas[index], width,       // edit.c:63
                       &ptr->cdsp.dsas[index]);             // V-origin shifted LEFT by width
           break;
}
```

**`index = V`, so only `cdsp.dsas[V]` is modified. `cdsp.dsas[I]` is left untouched.**

After the loop, `deletend` calls `recombine(father)` (`edit.c:75`).

---

### 3. What `recombine` Does (and Does NOT Do) After Delete

`recombine` dispatches to `recombinend` for POOM/SPAN (`recombine.c:22-34`). `recombinend` (`recombine.c:104-131`):

```c
int recombinend(typecuc *father) {
    if (father->height < 2 || !father->modified) return(0);
    for (ptr = getleftson(father); ptr; ptr = getrightbro(ptr))
        recombinend(ptr);                                   // recurse
    getorderedsons(father, sons);
    n = father->numberofsons;
    for (i = 0; i < n-1; i++)
        for (j = i+1; ...; j++)
            if (ishouldbother(sons[i], sons[j]))
                takeovernephewsnd(&sons[i], &sons[j]);      // structural rebalance only
    if (father->isapex) levelpull(father);
}
```

`ishouldbother` checks only capacity: `dest->numberofsons + src->numberofsons <= MAX2DBCINLOAF` (`recombine.c:162`). `takeovernephewsnd` / `eatbrossubtreend` / `takenephewnd` move **internal nodes** between parents — they adjust `cdsp` offsets and re-adopt subtrees, but they never inspect homedoc fields or call `isanextensionnd`. **`recombinend` is structural tree-balancing, not semantic I-span merging.**

**Consequence: after `deletend`, two bottom crums that are now geometrically adjacent remain as separate crums. There is no post-delete coalescing pass.**

---

### 4. Can Coalescing Fire Across the DELETE Boundary?

**Yes — on a subsequent INSERT, under the right geometry.**

The critical constraint is that `lockeq` (`insertnd.c:308`) checks **all two dimensions** of `reach` vs `origin`. A V-delete (`index = V`) shifts only `cdsp.dsas[V]`, never `cdsp.dsas[I]`. So for coalescing to fire after a delete:

- **V-adjacency** must be created by the delete (the rightward crum's V-origin shifts into contact with the leftward crum's V-reach).
- **I-adjacency** must independently hold (the two crums must already have matching I-reach / I-origin, since the delete never alters I-coordinates).

**Concrete geometry:**

Before delete, let two crums exist with the same homedoc H:
- Crum A: `cdsp=(3,1)`, `cwid=(2,2)` → I=[3,5), V=[1,3), reach=(5,3)
- Crum C (intervening, homedoc≠H): `cdsp=(5,3)`, `cwid=(2,2)` → V=[3,5)
- Crum B: `cdsp=(5,5)`, `cwid=(2,2)` → I=[5,7), V=[5,7), homedoc=H, grasp=(5,5)

Note A.reach_I = 5 = B.grasp_I (already I-adjacent), but A.reach_V = 3 ≠ 5 = B.grasp_V (V-non-adjacent due to C).

**After `deletevspanpm` at V=[3,5):**
- C is entirely within the deleted V-range → `case 1` → removed
- B falls to the right of the deleted range → `case 2`: `cdsp.dsas[V] -= 2` → B is now `cdsp=(5,3)`, `cwid=(2,2)` → I=[5,7), V=[3,5)

Post-delete state:
- A: reach = **(5, 3)**
- B: grasp = **(5, 3)**  ← now both V-adjacent AND I-adjacent to A

**A and B remain two separate bottom crums.** `recombine` does not merge them.

**A new INSERT at V=3, I=5, homedoc=H with any width** now calls `insertcbcnd`, which loops over bottom-crum siblings and calls `isanextensionnd` on A:
- `tumblereq(H, A.homedoc)` → TRUE
- `prologuend(A, offset, &grasp, &reach)` → reach = (5, 3)
- `lockeq(reach.dsas, origin.dsas, 2)`: compares (5,3) vs (5,3) → **TRUE**

**Coalescing fires.** A's `cwid` is extended in place (`insertnd.c:251`). No new crum is created.

---

### 5. What Does NOT Happen

- **No homedoc bypass**: if the new insert has `homedoc ≠ H`, the first guard (`insertnd.c:305`) returns FALSE regardless of geometry.
- **No auto-merge of A and B after delete**: they remain separate until an INSERT explicitly arrives at (5,3) with homedoc=H.
- **No memory of the delete in the tree**: the POOM after delete accurately reflects surviving content. The coalescing check has no knowledge of what was deleted; it operates purely on current geometric coordinates.
- **No re-coalescing of B itself**: the `insertcbcnd` loop exits after finding the first match (`return(FALSE)` at `insertnd.c:257`). After coalescing with A, B is not re-evaluated for merging into the now-wider A.

---

### 6. Summary Table

| Condition | Effect on coalescing |
|---|---|
| V-delete removes intervening content between V-adjacent A and B | B's `cdsp.dsas[V]` shifts left; A's `cdsp.dsas[I]` unchanged |
| After delete, A.reach_I == B.grasp_I AND A.reach_V == B.grasp_V | Geometric precondition for coalescing is met |
| `recombine` called by `deletend` (`edit.c:75`) | Structural only — does NOT merge A and B |
| Subsequent INSERT at A's exact 2D reach, same homedoc | `isanextensionnd` → TRUE; A widens in place |
| I-coordinates not I-adjacent after delete | `lockeq` fails on `dsas[I]`; no coalescing even if V-adjacent |

**The coalescing CAN fire across a prior DELETE boundary**, but only when a new INSERT arrives at coordinates that satisfy the simultaneous I-AND-V reach-equals-origin test. The delete itself, via `recombine`, performs no semantic coalescing — it leaves formerly non-adjacent I-spans adjacent-but-separate in the tree, and only a subsequent appropriately-positioned insert will trigger the merge.
