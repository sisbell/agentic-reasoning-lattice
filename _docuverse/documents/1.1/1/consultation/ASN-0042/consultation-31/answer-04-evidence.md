## Question 4 [evidence]

> When a principal `π` requests baptism of a sub-account position and the lower-numbered siblings under `pfx(π)` have been delegated to other principals (so are not in `π`'s effective ownership), what does `docreatenewdocument`/`getnewtumbler` do — proceed to the next available value, fail, or require those sub-delegates' participation?

## KB Synthesis

## Allocation Proceeds Independently — No Sub-Delegate Participation Required

The KB gives a clear answer: `findisatoinsertnonmolecule` is **ownership-blind**. It sees only the granfilade tree; delegation state lives nowhere in that tree.

### What the allocator actually does

From [SS-ADDRESS-ALLOC]:

1. Compute `upperbound = tumblerincrement(pfx(π), depth-1, 1)` — the next sibling of the parent prefix, bounding the search to that account's namespace.
2. Call `findpreviousisagr` to find the **highest existing address** below `upperbound` anywhere in the tree.
3. Apply a containment check: verify the candidate is actually under `pfx(π)` via tumbler truncation/equality ([SS-TUMBLER-CONTAINMENT], [PRE-ADDRESS-ALLOC]).
4. If candidate passes: truncate to the appropriate length and increment by 1 → that is the new address.
5. If nothing found under the parent: allocate first child `pfx(π).0.1`.

The word "existing" in step 2 covers **all** previously allocated addresses under `pfx(π)` — including those delegated to other principals. The algorithm does not distinguish why a slot is occupied, only *that* it is occupied.

**Concrete example:**
```
pfx(π) = 1.1.0.2
Existing sub-accounts: 1.1.0.2.0.1 (delegated to A), 1.1.0.2.0.2 (delegated to B)

findpreviousisagr → 1.1.0.2.0.2  (highest under pfx(π))
Containment check: truncate to length 4 → 1.1.0.2  ✓
Increment → 1.1.0.2.0.3  ← allocated for π
```

Delegates A and B are not consulted; their addresses are simply "already in the tree," advancing the high-water mark.

### Why no failure, no participation

- [INV-MONOTONIC]: allocation is a pure function of `max_iaddr(granf)` within the scoped subtree — it only ever moves forward.
- [INV-NO-IADDR-REUSE]: addresses are never freed, so `findpreviousisagr` reliably returns the true maximum regardless of what operations have touched delegated sub-accounts.
- [INV-ACCOUNT-ISOLATION]: the containment guard (added to fix Bug 0013 per [PRE-ADDRESS-ALLOC]) ensures the result lands under `pfx(π)`, not that it avoids delegated siblings — those are already properly "under" the parent.
- The allocation mechanism has **no access to BERT, no ownership table, no delegation registry** — only the granfilade tree.

### Summary

`getnewtumbler` proceeds to the next available value past all occupied siblings, delegated or not. It cannot fail due to delegation (only genuine exhaustion of the tumbler address space could block it, which is practically unreachable). Sub-delegates' participation is entirely irrelevant to the mechanical allocation — their positions are simply entries the allocator steps over.

---

## Code Exploration

Now I have a complete, verified picture. Here is the full answer.

---

## What `docreatenewdocument`/`getnewtumbler` does with delegated siblings

**Short answer: it proceeds to the next available value. No delegation check occurs during address allocation. Sub-delegates' participation is not required and the call does not fail.**

---

### Complete Call Chain

```
fns.c:276  createnewdocument(taskptr)
  do1.c:234  docreatenewdocument(taskptr, &newdocisa)
    do1.c:239    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)
    do1.c:240    createorglingranf(taskptr, granf, &hint, isaptr)
      granf1.c:54  createorglgr(taskptr, granf, hintptr, isaptr)
        granf2.c:117   findisatoinsertgr(fullcrumptr, hintptr, isaptr)
          granf2.c:152   findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr)
            granf2.c:217     findpreviousisagr(fullcrumptr, &upperbound, &lowerbound)
            granf2.c:235-241  compute new address
        granf2.c:125   insertseq(fullcrumptr, isaptr, &locinfo)
```

---

### Step 1 — Build the hint (`do1.c:239`)

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

`hintptr->hintisa` is set to `taskptr->account` — the requesting principal's own account tumbler (e.g. `1.1.0.1`). This is the *only* principal identity consulted at this point.

---

### Step 2 — Compute the upper-bound and scan for the highest sibling (`granf2.c:203-242`)

`findisatoinsertnonmolecule` drives the address computation:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // ACCOUNT→DOCUMENT → depth=2
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound); // upperbound = hintisa.0+1 = 1.1.0.2
clear(&lowerbound, sizeof(lowerbound));
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // granf2.c:217
```

`findpreviousisagr` (granf2.c:255-278) then traverses the granfilade tree to find the highest-addressed item whose address is less than `upperbound`:

```c
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr(ptr, upperbound, offset);  // recurse
            return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate width
    }
}
```

**Critical observation:** `whereoncrum()` is a pure tumbler interval comparison — it has no knowledge of ownership, bert entries, or delegation state. There is **no call to `checkforopen`** anywhere inside `findpreviousisagr` or `findisatoinsertnonmolecule`. The scan traverses every existing item in the tree unconditionally, whether owned by `π` or by a third-party delegatee.

---

### Step 3 — Assign the new address (`granf2.c:235-241`)

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing under this hint — first child is hintisa.0.1
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

The comment at granf2.c:225-227 explicitly calls out the cross-account edge case:

> "Also check if lowerbound is actually under hintisa. If the found item is from a different account (e.g., `1.1.0.1.0.1` when creating under `1.1.0.2`), treat it as if nothing was found."

This guards against bleed across account boundaries, but does **not** distinguish between items owned by `π` versus items delegated *within* `pfx(π)` to another principal. Both are just nodes in the granfilade tree, and both are incremented past identically.

---

### Where `checkforopen` *does* live — and why it's not here

`checkforopen` (bert.c:52-87) is only called from **`findorgl`** (granf1.c:22):

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        ...
        return FALSE;
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`findorgl` is the path for **opening an existing document** (for read or write access). The `createnewdocument` path does not go through `findorgl` at all. Document creation in `createorglgr` (granf2.c:111-128) calls `findisatoinsertgr` → address arithmetic → `insertseq` directly, bypassing the bert table entirely.

---

### Conclusion

When principal `π` requests baptism of a new sub-account document and lower-numbered siblings under `pfx(π)` are delegated to other principals:

1. `findpreviousisagr` finds the **highest existing sibling** (including delegated ones) below the upper-bound address — solely by traversing the enfilade tree with tumbler arithmetic.
2. The new document address is assigned as **`lowerbound + 1`** — the next integer in the sequence, past whatever the highest existing entry is, regardless of who owns it.
3. **No delegation check occurs.** The bert table (`bert.c`) is not consulted during address allocation.
4. **No failure mode.** The call succeeds as long as the granfilade traversal finds a position.
5. **Sub-delegates' participation is not required** and is not solicited.

The ownership model is enforced orthogonally: once a document exists at its address, `findorgl`/`checkforopen` gates all subsequent *access* to it through the bert table. But the *allocation* of new addresses is purely a structural walk of the enfilade, blind to ownership.
