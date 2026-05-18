## Question 5 [evidence]

> When udanax-green emits a link via `findisatoinsertmolecule`, does the implementation require intermediate addresses along the T10a producer chain (from document seed to the emitted link's address) to be physically allocated/resident, or does it only verify reachability in the abstract allocator hierarchy without materializing the chain?

## KB Synthesis

The KB is unambiguous on this: **no intermediate addresses need to be physically allocated**. The allocation is a flat key-range search, not a hierarchical traversal.

From [SS-ADDRESS-ALLOC] (Finding 0021): "The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by **bounding searches to the parent's address range**" — hierarchy is imposed via arithmetic bounds on a flat B-tree, not via physically materialized ancestor nodes.

From [SS-ADDRESS-ALLOC] (Finding 0065), the concrete steps in `findisatoinsertmolecule` for link allocation are:

1. Compute `upperbound = tumblerincrement(docISA, 2, atomtype+1)` — purely arithmetic, no granfilade read
2. Call `findpreviousisagr` — a flat B-tree traversal looking for the highest key below `upperbound`
3. If no key found below the document's link subspace threshold: allocate at `docISA.2.2.1`
4. Otherwise: `lowerbound + 0.1`

The intermediate addresses in the hierarchy (e.g., `1.1`, `1.1.0.1`, `1.1.0.1.0.1.0.2`) are never queried or required to be resident. The `upperbound` derivation is arithmetic-only.

From [SS-ADDRESS-ALLOC] (Finding 0061, confirmed by Finding 0077): "The allocation is purely derived from current tree state — there is no cached 'next available' pointer" and "allocation is a family of independent functions partitioned by tumbler range: `next_content_addr(granf, doc) = max_content(granf, doc) + 1`."

The only structural requirement is that the **document's own orgl** be registered in the granfilade (so `findorgl` can validate write access before the allocation call), but the ancestors of that document address need not be.

---

## Code Exploration

I now have all the code necessary to give a complete answer. Here it is.

---

## Answer: `findisatoinsertmolecule` — Chain Allocation Analysis

**Short answer: No. Only the immediate `hintisa` (the document address) must be physically resident. No intermediate chain entries are materialized or checked.**

---

### Call Chain for Link Creation

`docreatelink` [do1.c:207]:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)  // ← allocates link at computed address
  && ...
);
```

`createorglingranf` → `createorglgr` [granf2.c:111–128]:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);   // ← physically places the link in granfilade
```

---

### Where the Chain Check Actually Happens

`findisatoinsertgr` [granf2.c:130–156] is the gate:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {   // ← ONLY check
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
}
```

`isaexistsgr` [granf2.c:244–253]:

```c
context = retrieve (crumptr, isaptr, WIDTH);
ret = tumblereq ((tumbler*)&context->totaloffset, isaptr);
contextfree (context);
return (ret);
```

This is a **single-point presence check**: it calls `retrieve` → `findcbcseq` to walk the existing granfilade and asks only whether the returned `totaloffset` exactly equals `hintisa`. **Only the document's own address is verified. Nothing between the document and the eventual link address is examined.**

---

### Inside `findisatoinsertmolecule` [granf2.c:158–181]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // pure arithmetic
    clear (&lowerbound, sizeof(lowerbound));                                        // no allocation
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);       // granfilade traversal
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);           // base = docisa.0.2
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                  // or increment
        else
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    }
}
```

Every operation is either tumbler arithmetic (no allocation, no I/O) or a call to `findpreviousisagr`.

---

### `findpreviousisagr` [granf2.c:255–278] — Tree Traversal, Not Allocation

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);   // reads existing CBC leaf
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(...)) == THRUME || ... || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);  // recurse into existing nodes
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate offsets
        }
    }
}
```

`findpreviousisagr` walks **already-allocated enfilade structural nodes** (`typecorecrum`, `typecbc`). It reads their `cwid.dsas[WIDTH]` width fields and their link pointers (`leftson`, `rightbro`). It creates nothing and allocates nothing. The result is a tumbler value representing the largest address in the granfilade that falls below `upperbound`.

---

### `insertseq` [insert.c:17–70] — Direct Insertion, No Chain Materialization

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
{
    context = retrievecrums (fullcrumptr, address, WIDTH);   // find existing neighbor
    ptr = context->corecrum;                                 // existing CBC node
    ...
    new = createcrum (0, (INT)ptr->cenftype);                // one new CBC node at target address
    adopt (new, RIGHTBRO, (typecorecrum*)ptr);               // splice in as right sibling
    ...
    tumblersub (&nextaddress, &offset.dsas[WIDTH], &ptr->cwid.dsas[WIDTH]);  // adjust widths
    ...
    if (splitsomething) recombine (fullcrumptr);             // rebalance enfilade
}
```

The granfilade is a **linearly-ordered sequence** of CBC leaf nodes inside an enfilade tree. Any tumbler address can be inserted between any two existing entries — the enfilade structure only tracks widths (distances between adjacent entries). There is no parent-pointer hierarchy of named intermediate entries. `insertseq` creates **exactly one new CBC node** at the computed address; no intermediate tumblers are created.

---

### Summary

| Step | What happens | Allocates? | Intermediate chain checked? |
|------|-------------|-----------|----------------------------|
| `isaexistsgr(hintisa)` [granf2.c:245] | Verifies document address exists in granfilade | No | **Only `hintisa` itself** |
| `findpreviousisagr(...)` [granf2.c:255] | Walks existing granfilade tree to find nearest address | No | None — reads structural nodes only |
| Tumbler arithmetic in `findisatoinsertmolecule` [granf2.c:162–175] | Computes link's address from `hintisa` and the found lower-bound | No | None |
| `createenf(POOM)` [granf2.c:120] | Creates the link's internal POOM enfilade | Yes — the link orgl | N/A |
| `insertseq(fullcrumptr, isaptr, &locinfo)` [insert.c:17] | Inserts one CBC record at the computed address | Yes — one CBC node | None |

The T10a hierarchy (e.g., document `1.1.0.1.0.1` → link at `1.1.0.1.0.1.0.2`) is **purely a naming convention**. The intermediate address `1.1.0.1.0.1.0` never needs to be a granfilade entry. The implementation verifies only that the parent document exists [granf2.c:136], then inserts the link directly at the freshly computed leaf address [insert.c:44–69]. The producer chain is abstract — only its endpoints matter.
