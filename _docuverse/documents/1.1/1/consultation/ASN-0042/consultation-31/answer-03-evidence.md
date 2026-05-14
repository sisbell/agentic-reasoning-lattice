## Question 3 [evidence]

> Does the udanax-green allocator's `next(B, p, d)` operation require all preceding sibling values `1, 2, ..., u-1` to be baptized before `u` can be produced at a given (parent, depth), or can it baptize `u` independently of intermediate siblings?

## KB Synthesis

The allocator **cannot** produce `u` independently. It strictly requires `u-1` to be the current maximum, meaning all of `1, 2, ..., u-1` must already exist.

The mechanism is spelled out in [SS-ADDRESS-ALLOC] / [ST-ADDRESS-ALLOC] (Finding 0021):

1. Compute upper bound: `tumblerincrement(parent, depth-1, 1)` — the next sibling of the parent
2. Call `findpreviousisagr` to find the **highest existing** address strictly below that bound and under the parent
3. If nothing found: allocate `parent.0.1` (first child)
4. If found: truncate to sibling length, increment by 1 → that is the new allocation

Step 2 is key: the search returns the **maximum** existing sibling. The new address is always `max_existing + 1`. To produce `u`, the algorithm must find `u-1` as the maximum. There is no mechanism to skip ahead.

This is confirmed across all allocation sites:
- **Text I-addresses** [SS-ADDRESS-ALLOC Finding 0061]: `findpreviousisagr` returns highest, then `tumblerincrement(..., 0, 1, isaptr)` — strictly next
- **Link I-addresses** [ST-ADDRESS-ALLOC Finding 0065]: "increment from `lowerbound` (the highest existing) by `0.1`"
- **Version addresses** [ST-ADDRESS-ALLOC Finding 0068]: second version of `.0.1` finds `.0.1.1` as max, produces `.0.1.2` — never `.0.1.5`

Because the granfilade is append-only ([INV-NO-IADDR-REUSE], [INV-MONOTONIC]), once siblings `1..u-1` are allocated they persist permanently. So "all predecessors baptized" and "all predecessors exist in the granfilade" are equivalent conditions.

**Conclusion**: The allocator is strictly sequential — `next(B, p, d) = max_child(B, p, d) + 1`. Producing `u` requires `u-1` to be the current maximum, which in turn required `u-2`, and so on. No intermediate sibling can be skipped.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Does `next(B, p, d)` require sequential baptism of all preceding siblings?

**No. `next(B, p, d)` does not require any preceding sibling to be baptized. It baptizes the next address by finding the highest existing sibling and incrementing it — predecessors are neither checked nor required.**

---

### The Implementation

The operation maps onto `findisatoinsertnonmolecule()` in `backend/granf2.c:203–242`, called from `findisatoinsertgr()` at `granf2.c:152`.

#### Step 1 — Compute the search upper bound

```c
// granf2.c:209-213
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

`depth` is 1 for same-type (e.g., document inside account) or 2 for cross-type allocation. `upperbound` is the parent address incremented by 1 at position `depth-1` — it marks the exclusive ceiling: no sibling at `(p, d)` can be ≥ `upperbound`.

#### Step 2 — Find the highest existing sibling below the upper bound

```c
// granf2.c:215-217
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr()` (`granf2.c:255–278`) traverses the enfilade tree:

```c
// granf2.c:267-277
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (
     (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER
    || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);   // descend into the right child
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate width
    }
}
```

It accumulates the widths of all left-of-bound subtrees and descends into the rightmost one that contains the bound. It returns the **largest address that exists in the tree below `upperbound`** — whatever that happens to be. It makes no check that all intervening addresses exist.

At the leaf level (`height == 0`), `findlastisaincbcgr()` (`granf2.c:280–284`) records the last character of a text run if present:

```c
if (ptr->cinfo.infotype == GRANTEXT)
    tumblerincrement (offset, 0, (INT) ptr->cinfo.granstuff.textstuff.textlength - 1, offset);
```

#### Step 3 — Validate that the found address is actually under this parent

```c
// granf2.c:228-233
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}
```

This guards against the case where the highest address in the whole granfilade belongs to a sibling parent (e.g., searching under account `1.1.0.2` finds `1.1.0.1.0.1` from account `1.1.0.1`). If `lowerbound` does not share the parent's prefix, it is treated as absent. **This is a gap-detection guard, not a sequential check.**

#### Step 4 — Produce the next address

```c
// granf2.c:235-241
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing under this hint — create first child as hintisa.0.1
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

Two cases:

- **Empty slot**: if nothing exists under the parent, the new address is `hintisa` incremented at position `depth` → i.e., `hintisa.0.1` (the first child).
- **Non-empty slot**: truncate the found maximum to `hintlength + depth` digits, then increment its last digit by 1. This produces max+1 directly — no scan of the range `[1, max)`.

`tumblerincrement(aptr, rightshift, bint, cptr)` (`tumble.c:599–623`) appends `bint` at `rightshift` positions past the last non-zero mantissa digit — pure arithmetic addition, no predecessor lookup.

---

### What This Means Concretely

Suppose documents `{1, 3, 7}` have been baptized at `(parent=p, depth=d)` and sibling slots `{2, 4, 5, 6}` were never allocated. Calling `next(B, p, d)`:

1. `findpreviousisagr` finds `7` (the highest existing value below `upperbound`).
2. Truncate and increment → produces `8`.

Slots `{2, 4, 5, 6}` remain permanently unallocated. The allocator will never backfill them; they are not visible to the algorithm at all. Each call to `next` monotonically advances from the current maximum.

---

### Summary

| Property | Value |
|---|---|
| Predecessor check? | **None.** `findpreviousisagr` finds the global maximum, not the minimum gap. |
| Sequential invariant? | Only: result > all existing siblings at `(p, d)`. |
| Gaps possible? | **Yes.** Any sibling addresses skipped by earlier calls (or never created) become permanent holes. |
| Independence? | **Full.** `u` is produced solely from max(`existing`) + 1, irrespective of which intermediate values exist. |

The algorithm is "find the ceiling, climb one step" — not "enumerate and fill." Preceding siblings need not be baptized.
