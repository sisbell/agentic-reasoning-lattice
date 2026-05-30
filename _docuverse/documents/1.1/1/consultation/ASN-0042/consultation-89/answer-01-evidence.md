## Question 1 [evidence]

> Does the account-allocation path (findpreviousisagr / the ISA choke point) only ever produce the next contiguous sibling of a baptized stream, or can it baptize an arbitrary strictly-extending prefix in one step?

## KB Synthesis

## Allocation Path: Strictly Next-Sibling Only

The allocation path produces **only** the next contiguous sibling — it cannot baptize an arbitrary strictly-extending prefix in one step.

### The Mechanism

`findisatoinsertnonmolecule` always executes the same two-step pattern [SS-ADDRESS-ALLOC, Finding 0021]:

1. Call `findpreviousisagr` to find the **highest existing address** below the computed upper bound
2. Truncate that address to the appropriate depth, then `tumblerincrement(..., 1)` — always by exactly 1

The first-child case is degenerate but consistent: when `findpreviousisagr` finds nothing under the parent, the allocator emits `parent.0.1` (or `parent.1` for depth=1 version allocation). This is just "zero + 1" — still a unit step.

### Why No Arbitrary Jumps

From Finding 0065 (link allocation): "increment from `lowerbound`... by `0.1`." From Finding 0068 (version allocation): `tumblerincrement(source_doc, 0, 1)`. From Finding 0033 (content allocation): `tumblerincrement(&lowerbound, 0, 1, isaptr)`. The increment is hardcoded to 1 in every call site [INV-MONOTONIC].

There is no code path that takes a caller-supplied target address, nor any that skips positions. The only degree of freedom is the parent hint (which namespace to allocate under), not the position within that namespace.

### Consequence

If the highest existing address under account `1.1.0.2` is `1.1.0.2.0.5`, the next allocation is unconditionally `1.1.0.2.0.6`. The allocator cannot emit `1.1.0.2.0.10` in one step. Gaps cannot be created intentionally through the normal allocation path — only through the CREATELINK granfilade interaction that displaces the content I-address counter [EC-FIND-LINKS-GLOBAL, Finding 0063], and even that still increments by 1 from the new maximum.

The monotonic, gap-free property is unconditional [INV-NO-IADDR-REUSE, INV-MONOTONIC].

---

## Code Exploration

Now I have all the code I need to answer the question. Let me trace the exact execution paths.

---

## Account-Allocation Path Analysis: `findpreviousisagr` / ISA Choke Point

### The Call Chain

Every ISA allocation routes through `findisatoinsertgr` [granf2.c:130-156], which dispatches on `hintptr->subtype`:

- `subtype == ATOM` → `findisatoinsertmolecule` [granf2.c:158-181]  
- `subtype != ATOM` (DOCUMENT, ACCOUNT, NODE) → `findisatoinsertnonmolecule` [granf2.c:203-242]

Account→document allocation uses `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` [do1.c:239], so `subtype == DOCUMENT`, routing to `findisatoinsertnonmolecule`.

---

### `findisatoinsertnonmolecule` in Full [granf2.c:203-242]

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;            // [209]

    hintlength = tumblerlength (&hintptr->hintisa);                     // [211]

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);   // [213]

    clear (&lowerbound, sizeof(lowerbound));                            // [215]

    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // [217]

    lowerbound_under_hint = FALSE;                                      // [228]
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);           // [231]
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa); // [232]
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);          // [237] — first child
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);      // [239]
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr); // [240]
    }
}
```

---

### What `findpreviousisagr` Actually Returns [granf2.c:255-278]

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr((typecbc*)crumptr, offset);  // [264] — leaf: last ISA in this node
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);  // [271] — recurse into subtree
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset); // [275] — accumulate width
        }
    }
}
```

The accumulated `offset` is the **sum of widths of all left siblings** at each level — this equals the ISA of the rightmost leaf strictly before `upperbound`. The function is a rightward enfilade walk; it returns the **globally maximum existing ISA below the bound**. There is no path through this function that can skip values or return a non-contiguous result.

---

### The Two Allocation Branches

**Branch 1 — Nothing under hint (empty account or wrong account)** [granf2.c:237]:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```

`tumblerincrement(A, depth, 1)` [tumble.c:599-623] finds the last nonzero mantissa position `idx` in `A`, then writes `+1` at `idx + depth`. For `depth=2` (ACCOUNT→DOCUMENT), this appends two new mantissa slots, producing the canonical first child: `hintisa.0.1`.

This **is** a strictly-extending prefix produced in a single step — but it is **the one fixed child address**, not arbitrary. There is no parameter for which sub-address to create.

**Branch 2 — Items already exist under hint** [granf2.c:239-240]:

```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

`tumblertruncate` [tumble.c:625-639] zeros out all mantissa positions at index ≥ `hintlength + depth`, then re-justifies. For lowerbound at depth `hintlength + depth` (the normal case), this is a no-op and `tumblerlength(isaptr) = hintlength + depth ≠ hintlength`, so:

```c
tumblerincrement(isaptr, 0, 1, isaptr)
```

This increments the last digit by exactly 1: `max_existing_address + 1`. That is always the **next contiguous sibling** — nothing else.

The `tumblerlength(isaptr)==hintlength` sub-branch handles the degenerate case where `lowerbound` is shallower than expected after truncation, but in practice for granfilade keys (which are all at the same depth within a hint), this also produces a single-step increment.

---

### Can It Skip? Can It Baptize an Arbitrary Prefix?

**No, on both counts.**

1. **Cannot skip**: `findpreviousisagr` returns the maximum existing ISA. The only write is `+1` at one mantissa position [tumble.c:621: `cptr->mantissa[idx + rightshift] += bint`]. There is no mechanism for gap-jumping — the allocator cannot assign address N+2 when N+1 hasn't been used.

2. **Cannot baptize an arbitrary strictly-extending prefix**: The first-child formula is hardcoded as `tumblerincrement(hintisa, depth, 1)` [granf2.c:237], which always produces `hintisa.0.1`. The caller cannot request `hintisa.0.K` for K>1, nor `hintisa.0.0.1`, nor any other extension shape. The `depth` parameter is locked by the `supertype/subtype` pair at the `makehint` call site [do1.c:239, do2.c:78-84], not by the caller of `findisatoinsertgr`.

3. **The `lowerbound_under_hint` guard** [granf2.c:229-233] further constrains this: if the maximum existing ISA is not a descendant of `hintisa` (e.g., it belongs to a different account), the function falls through to the first-child branch regardless, producing `hintisa.0.1`. It cannot return any address that is not either `hintisa.0.1` or `existing_max + 1`.

---

### Summary

The account-allocation path through `findpreviousisagr` / `findisatoinsertnonmolecule` is a **purely sequential allocator with one input degree of freedom**:

| Condition | Result | Form |
|-----------|--------|------|
| Tree empty under hint | `hintisa.0.1` | First child — a fixed strictly-extending prefix |
| Tree non-empty under hint | `max_existing + 1` at last digit | Next contiguous sibling |

The "strictly-extending prefix" case — `hintisa.0.1` when the account has no documents yet — is produced in one step, but it is **the unique canonical first child**, not any arbitrary prefix. The allocator has no facility to choose a depth, skip levels, or jump to a non-contiguous address. Every call advances the counter by exactly one.
