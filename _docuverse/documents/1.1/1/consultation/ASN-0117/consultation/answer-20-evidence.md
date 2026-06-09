## Question 20 [evidence]

> After a DELETE that removes all of a document's content, does the enfilade retain intermediate nodes from prior growth (since `levelpull` is disabled), leaving the empty tree structurally taller than a freshly created empty tree while query results stay identical?

## KB Synthesis

Yes, exactly. The evidence is direct.

**`levelpull` is permanently disabled** [SS-ENFILADE-TREE, Finding 0058]: the function at `genf.c:318-342` immediately returns 0 without executing the collapse logic. Height can only increase via `levelpush`; it never decreases.

**After delete-everything** [ST-DELETE, Finding 0058]: `deletend` Case 1 calls `disown` + `subtreefree` on all bottom nodes, then `recombinend` calls `levelpull` on the apex — which is a no-op. The result is a tree of height H (whatever it reached during content growth) with empty intermediate nodes (`numberofsons=0`) and no bottom crums at all.

**Two structurally distinct empty states** [EC-EMPTY-DOC, Finding 0058]:

| State | Height | Fullcrum sons | Bottom nodes |
|-------|--------|---------------|--------------|
| `createenf()` (never filled) | 1 | 1 (zero-width bottom) | 1 |
| After delete-everything | H from prior growth | 2+ (empty intermediates) | 0 |

**Query results are identical** [INV-ENFILADE-MINIMALITY]: both return zero-width content on retrieve; `isemptyenfilade` on the 2D case checks `cwid = 0 AND cdsp = 0`, which holds for both [EC-EMPTY-DOC, Finding 0066].

**A concrete consequence**: the delete-everything state causes INSERT/VCOPY to crash (Bug 0019) because `firstinsertionnd` assumes a bottom crum exists and dereferences NULL when `findleftson()` returns nothing [EC-EMPTY-DOC, Finding 0058]. The never-filled state does not have this problem. So "empty by query" does not mean "equivalent to initial state."

The formal postcondition is: `delete_all(doc) ⟹ dom(poom(doc)) = ∅ ∧ enf.height(doc) = enf.height_before(doc)` [ST-DELETE, Finding 0058].

---

## Code Exploration

I now have all the evidence needed. Let me compile the full answer.

---

## Answer

**Yes, on all three counts — and the disabled `levelpull` has a sharper consequence than the question implies.**

---

### 1. `levelpull` is definitively disabled

`genf.c:318-342` — the entire function body is commented out:

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

The commented-out body would have absorbed the single remaining child into the apex and decremented `height`. Without it, the function is a no-op.

---

### 2. `levelpull` is the only mechanism that shrinks tree height

Both `recombineseq` and `recombinend` call `levelpull` as their final step — and only there:

- `recombine.c:66-67`:
  ```c
  if (father->isapex)
      levelpull (father);
  ```
- `recombine.c:129-130`:
  ```c
  if (father->isapex)
      levelpull (father);
  ```

Since the function returns immediately, tree height can only ever increase (via `levelpush` in `split.c:29`) — never decrease.

---

### 3. The delete path confirms intermediate nodes survive

`dodeletevspan` → `deletevspanpm` (`orglinks.c:149`) → `deletend` (`edit.c:31-76`).

`deletend` iterates over the **children of the intersection node** (not bottom crums directly). For a delete covering all content, the intersection node is the apex. All its children fall in case 1:

```c
case 1:
    disown ((typecorecrum*)ptr);
    subtreefree ((typecorecrum*)ptr);
    break;
```

This frees entire subtrees. After the loop:

```c
setwispupwards (father,1);
recombine (father);
```

`setwispupwards` propagates zeroed widths upward. `recombine` is called — but with the apex now having 0 sons and `levelpull` disabled, `recombinend` exits without further structural change (`recombine.c:112`):

```c
if (father->height < 2 || !father->modified)
    return(0);
```

For a height-2 apex: continues, but finds no children to merge and calls the no-op `levelpull`. **The apex retains its pre-deletion height with 0 sons.**

---

### 4. Tree grows to height > 1 with very few inserts

`enf.h:27-28`:
```c
#define MAXBCINLOAF    1
#define MAX2DBCINLOAF  4
```

`toomanysons` (`genf.c:244`) for a POOM height-1 apex:

```c
return (ptr->numberofsons > (ptr->height > 1 ? MAXUCINLOAF : (is2dcrum(...) ? MAX2DBCINLOAF : MAXBCINLOAF)));
```

Since POOM is a 2D crum, height 1 triggers at `MAX2DBCINLOAF = 4`. After 5 inserts, `levelpush` (`genf.c:263`) increments `fullcrumptr->height` and creates a new height-1 intermediate node. The tree is now height 2.

---

### 5. Query results are height-independent

`isemptyenfilade` (`genf.c:97-116`) checks only field values, not structure:

```c
case SPAN :
case POOM :
    return (
       iszerolock(ptr->cwid.dsas, (unsigned)widsize(ptr->cenftype))
    && iszerolock(ptr->cdsp.dsas, (unsigned)dspsize(ptr->cenftype)));
```

All traversal functions (`findcbcnd`, `findcbcinarea2d`, `crumqualifies2d` in `retrie.c`) terminate early when cwid is zero. An empty height-2 tree and a freshly created height-1 tree return identical query results: nothing.

---

### 6. Latent crash: re-insertion into an emptied tree of height > 1

When a document is empty, `doinsertnd` (`insertnd.c:191-196`) detects this via `isemptyenfilade` and calls `firstinsertionnd`. That function creates a new bc (height 0) and adopts it:

```c
ptr = createcrum (0, (INT)father->cenftype);
adopt (ptr, SON, (typecorecrum*)father);
```

`enf.h:137`: `#define SON LEFTMOSTSON`.

`adopt` (`genf.c:489-500`) enforces:

```c
if (father->height != new->height +1) {
    qerror ("height mismatch in adopt\n");
}
```

With apex at height 2 and new bc at height 0: `2 ≠ 0+1` → `qerror` → `abort()`.

This means: the disabled `levelpull` does not merely leave a "taller-but-identical" tree. After inserting at least 5 items into a POOM document, deleting all of them, and inserting again, the backend crashes. The empty height-2 apex cannot accept a height-0 bc without a structural collapse that only `levelpull` would have provided.

---

### Summary

| Claim | Verdict | Key evidence |
|-------|---------|--------------|
| `levelpull` is disabled | **Yes** | `genf.c:318-321` — body commented out, `return(0)` |
| Intermediate nodes persist after delete-all | **Yes** | `deletend` frees subtrees, `recombine` can't shrink height |
| Empty post-delete tree is taller than fresh tree | **Yes** | `levelpush` at 5 inserts; no matching pull |
| Query results identical | **Yes** | `isemptyenfilade`, `findcbcnd` check cwid, not height |
| Re-insertion is safe | **No** | `adopt` height check crashes when apex height > 1 |

The disabled `levelpull` is not a benign optimization tradeoff — it creates a state from which re-insertion is impossible after delete-all on any document that grew past its initial height.
