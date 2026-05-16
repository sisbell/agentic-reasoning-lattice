## Question 12 [gregory]

> If you insert at a V-position beyond the current document extent (e.g., document spans V:[1.1,1.5] and you insert at V:1.100), does `makegappm` still execute a shift pass over all POOM entries, or does it detect the absence of entries at or beyond the target and skip shifting?

## KB Synthesis

## Behavior: Insert Beyond Document Extent

The POOM traversal still executes, but **shifting is completely bypassed** — not because a detection optimization exists, but because two independent guards both fire.

### Guard 1: `makegappm` early exit

From **[SS-WHEREONCRUM]** / **[PRE-INSERT]** Finding 0062, `makegappm` has a compound early-exit at its top:

```c
if (iszerotumbler(&fullcrumptr->cwid.dsas[V])
    || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS
    || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);
```

The third clause fires when `origin >= reach`. For any existing crum covering `[1.1, 1.5)` with reach `= 1.5`, inserting at `1.100` satisfies `1.100 > 1.5`, so `tumblercmp(1.100, 1.5) != LESS` is TRUE. `makegappm` returns 0 immediately — **no knife is constructed, no cuts are scheduled**.

### Guard 2: `insertcutsectionnd` case classification

Even if the knife were constructed, from **[ST-INSERT]** / **[FC-SUBSPACE]** Finding 0054, the two-blade knife would have:
- `blade[0]` = 1.100 (insertion point)
- `blade[1]` = 2.1 (next subspace boundary)

`insertcutsectionnd` classifies all existing crums (which sit at positions `< 1.100`) as **case 0** (before `blade[0]`). Case 0 means: no shift. The shift formula `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` is never called.

### What does happen

The B-tree traversal proceeds normally to find the insertion position. `isanextensionnd()` **[ST-INSERT]** Finding 0062 checks whether `new_origin == existing_crum.reach`. Since `1.100 ≠ 1.5`, no coalescing occurs. A **new bottom crum** is allocated at `[1.100, 1.100 + insert_width)`, becoming a new sibling of the existing crums.

From **[SS-ENFILADE-TREE]** Finding 0058, this may trigger `splitcrumupwards` if the parent exceeds its branching limit, but that is purely structural — no content shifting.

### Net result

Inserting beyond the current document extent:
1. Creates a gap in V-space (positions 1.5 through 1.100 are unoccupied)
2. Performs **zero shift operations** on existing crums
3. Allocates a new crum at the target position

The document's vspanset will subsequently report two separate spans: the original `[1.1, 1.5)` and the new `[1.100, ...]`, not a single consolidated span — because **[INV-VSPAN-CONSOLIDATION]** only consolidates spans that are actually contiguous in both V-space and I-space.

---

## Code Exploration

I have everything needed to answer definitively. Here is the full analysis.

---

## Answer: `makegappm` Detects Out-of-Range Origin and Returns Early — No Shift Pass Executes

### The Guard Clause

`makegappm` [`insertnd.c:124`] opens with a three-part early-return condition evaluated **before** it does any work:

```c
/* insertnd.c:138-143 */
clear (&offset, sizeof(offset)); /* fullcrum always has zero offset */
prologuend ((typecorecrum*)fullcrumptr, &offset, &grasp, &reach);
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    return(0);    /* this if for extensions to bc without calling cut*/
```

### What `prologuend` Computes

`prologuend` [`makeroom.c:334-339`] is:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

Called with `offset = 0`:
- `grasp = 0 + fullcrumptr->cdsp` → the **V-start** of the document (e.g., V:1.1)
- `reach = grasp + fullcrumptr->cwid` → the **V-end** of the document (e.g., V:1.5, exclusive upper bound)

### Applying the Guard to Your Scenario

Document spans V:[1.1, 1.5]; insert origin = V:1.100 (second tumbler digit 100 >> 5).

| Sub-condition | Evaluation | Why |
|---|---|---|
| `iszerotumbler(&fullcrumptr->cwid.dsas[V])` | FALSE | Document has non-zero width |
| `tumblercmp(&origin[V], &grasp[V]) == LESS` | FALSE | V:1.100 > V:1.1 (100 > 1 in 2nd digit) |
| `tumblercmp(&origin[V], &reach[V]) != LESS` | **TRUE** | V:1.100 > V:1.5 (100 > 5 in 2nd digit), so result is `GREATER`, and `GREATER != LESS` |

The third sub-condition fires. The `if` is true. `makegappm` executes `return(0)` at line 143.

### What Is Skipped

Everything after line 143 does not execute:

- `makecutsnd` [`insertnd.c:148`] — no cuts are made at the insertion point
- `newfindintersectionnd` [`insertnd.c:149`] — no father node is found
- The sibling loop [`insertnd.c:151-169`] — **no shift pass runs**
- `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], ...)` [`insertnd.c:162`] — no displacement adjustments are applied

### Why This Is Correct

The comment names it precisely: _"this if for extensions to bc without calling cut"_. An insertion **beyond** the current document's reach is a pure extension — no existing POOM entry sits at or to the right of V:1.100, so there is nothing to shift rightward. Shifting is only needed when inserting **within** `[grasp, reach)`. The guard encodes exactly that interval check: the shift pass is gated by `origin ∈ [grasp, reach)`. Origin at or past `reach` → unconditional early return.

### Summary

**Yes — `makegappm` detects the absence.** It does so via an explicit range check at [`insertnd.c:140-143`]: if `origin ≥ reach` (i.e., beyond the current document's V-extent), it returns 0 immediately. The entire shift pass — cuts, intersection finding, and sibling displacement — is skipped. No POOM entries are touched.
