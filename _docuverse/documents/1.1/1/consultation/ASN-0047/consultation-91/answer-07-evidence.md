## Question 7 [evidence]

> In the udanax-green node-allocation path (single global granfilade with query-and-increment dispatch), what mechanism enforces freshness of node addresses? Is there a registry of allocated nodes, or is uniqueness enforced by the dispatch protocol itself?

## KB Synthesis

## Freshness Enforcement in udanax-green Node Allocation

There is no explicit registry of allocated nodes. Uniqueness is enforced entirely by the **dispatch protocol operating against the granfilade tree itself**, relying on three interlocking mechanisms:

---

### 1. The Granfilade IS the Registry

`findisatoinsertgr` dispatches to either `findisatoinsertmolecule` (content/text atoms) or `findisatoinsertnonmolecule` (document orgls, link orgls) depending on entity type. Both call `findpreviousisagr`, which traverses the granfilade B-tree to find the current maximum address in the target subtree, then `tumblerincrement` produces `max + 1` as the new address. [SS-ADDRESS-ALLOC, SS-ADDRESS-SPACE Finding 0061]

There is no counter, no free-list, no bitmap — the granfilade tree structure *is* the allocation record. The query-and-increment pattern is:

```
next_addr(granf, parent) = findpreviousIsaGr(granf, upperbound(parent)) + 1
```

---

### 2. Append-Only Granfilade Makes Reuse Structurally Impossible

The granfilade is never modified by DELETE or REARRANGE — only INSERT, COPY, and CREATELINK append to it [FC-GRANF-ON-DELETE, INV-NO-IADDR-REUSE]. Deleted I-addresses remain in the granfilade tree permanently. Since `findpreviousIsaGr` always returns the current maximum (including "deleted" addresses), the allocator never falls back into previously occupied ranges. [INV-MONOTONIC Finding 0061]

---

### 3. Single-Threaded Sequential Dispatch Eliminates Races

The `bed.c` event loop runs each FEBE operation to completion via `select()` + sequential `xanadu()` dispatch before processing the next request. There is no threading, no preemption, and no concurrent allocation. [INV-ATOMICITY Finding 0042, INV-SEQUENTIAL-DISPATCH] This means query-and-increment is inherently safe without locking — no two allocations can interleave.

---

### 4. Containment Check for Hierarchy Isolation

For non-molecule (document/link orgl) allocation, `findisatoinsertnonmolecule` adds a prefix-containment check after `findpreviousIsaGr`: the candidate address must actually be under the target parent via `tumblertruncate`/`tumblereq` comparison. Without this, the search can return addresses from sibling accounts [PRE-ADDRESS-ALLOC Finding 0021, Bug 0013]. This enforces namespace isolation within the same freshness mechanism. [SS-TUMBLER-CONTAINMENT]

---

### Summary

| Property | Mechanism |
|----------|-----------|
| Uniqueness | Query granfilade for current max, allocate max+1 |
| No reuse | Granfilade is append-only; deleted addresses persist as allocation barriers |
| Race-free | Single-threaded run-to-completion event loop |
| Namespace isolation | Containment check after tree query |

The protocol is stateless with respect to any session — `next_iaddr(granf)` is a pure function of the current granfilade state, with no hidden session-local counters. [SS-ADDRESS-SPACE Finding 0061, Finding 0077]

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Node Address Freshness in udanax-green: Mechanism Analysis

### The Single Global Granfilade

There is one global granfilade, declared in `xanadu.h:14`:
```c
extern typegranf granf;
```
It is created at startup in `entexit.c:42–44`:
```c
initkluge ((typecuc**)&granf, (typecuc**)&spanf);   // restore from disk, or
granf = (typegranf) createenf (GRAN);               // create fresh
```
Every node, account, document, and link address allocation goes through this single tree.

---

### The Allocation Path

All address-creating operations follow the same chain:

1. **FEBE handler** (`fns.c`) receives the request and calls a `do*` function.
2. **`do*` function** (`do1.c`) calls `makehint` and then `createorglingranf`.

For node/account creation (`do1.c:243–258`, `docreatenode_or_account`):
```c
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
```

For document creation (`do1.c:234–241`, `docreatenewdocument`):
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

`makehint` (`do2.c:78–84`) simply populates a `typehint` struct:
```c
hintptr->supertype = typeabove;   // e.g. NODE or ACCOUNT
hintptr->subtype   = typebelow;   // e.g. NODE or DOCUMENT
hintptr->atomtype  = typeofatom;
movetumbler (isaptr, &hintptr->hintisa);  // the parent address
```

3. **`createorglingranf`** (`granf1.c:50`) → **`createorglgr`** (`granf2.c:111`) calls `findisatoinsertgr` to determine the new address, then inserts:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);   // granf2.c:125
```

---

### The Address-Generation Function

`findisatoinsertgr` (`granf2.c:130–156`) dispatches on subtype:
- **ATOM** (text/link content within a document) → `findisatoinsertmolecule`
- **DOCUMENT, ACCOUNT, NODE** → `findisatoinsertnonmolecule`

For NODE allocation, `supertype == subtype == NODE`, so `depth = 1` in `findisatoinsertnonmolecule` (`granf2.c:209`).

**`findisatoinsertnonmolecule`** (`granf2.c:203–242`) is the core mechanism:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);

// Compute upper bound: hintisa incremented by depth-1 at depth-1
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);

clear (&lowerbound, sizeof(lowerbound));

// Query the granfilade for the highest existing address below upperbound
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

// If nothing under this hint, create first child as hintisa.0.1
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // granf2.c:237
} else {
    // Otherwise: truncate to hint depth, increment by 1
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);  // granf2.c:240
}
```

After this, `tumblerjustify(isaptr)` (`granf2.c:154`) normalizes the tumbler.

---

### `findpreviousisagr`: The Granfilade as Registry

`findpreviousisagr` (`granf2.c:255–278`) is a recursive tree walk:

```c
if (crumptr->height == 0) {
    findlastisaincbcgr ((typecbc*)crumptr, offset);   // granf2.c:264
    return(0);
}
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (
     (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
    || tmp == ONMYRIGHTBORDER
    || !ptr->rightbro) {
        findpreviousisagr (ptr, upperbound, offset);  // recurse
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate offset
    }
}
```

This traverses the B-tree structure of the enfilade to find the rightmost (highest) address stored in the subtree bounded by `upperbound`. The accumulated `offset` from `tumbleradd` calls is the cumulative address of that highest node.

---

### Uniqueness and Freshness: The Mechanism

**There is no separate registry of allocated node addresses.** Uniqueness is enforced structurally by the enfilade itself through three properties:

1. **Query-and-increment dispatch.** Every allocation queries `findpreviousisagr` against the live granfilade to find the current maximum occupant, then produces `max + 1`. The new address is guaranteed greater than all existing addresses under the hint.

2. **Permanent insertion.** `insertseq` writes the new address into the granfilade at `granf2.c:125`. Once inserted, it will be found as the lower bound by all future `findpreviousisagr` calls, advancing the allocation frontier monotonically.

3. **Non-recycling of deleted addresses.** `deleteversion` in `bert.c:349` is a no-op stub with no body:
   ```c
   int deleteversion(tumbler *tp)
   {
   #ifndef DISTRIBUTION
   fprintf(stderr,"deleteversion: tp = ");dumptumbler(tp);fprintf(stderr,"\n");
   #endif
   }
   ```
   Even when a document is marked for deletion via `removefromopen` (`bert.c:154–173`), the granfilade entry is never removed. Deleted addresses remain in the tree permanently, so they can never be re-allocated.

---

### The BERT Table Is Not Address Allocation

The `berttable` in `bert.c:29` is a hash table of `bertentry` records keyed by tumbler, tracking *open* documents (connection, access type, reference count, created/modified flags). `checkforopen` (`bert.c:52–87`) is called by `findorgl` (`granf1.c:22`) to enforce read/write access control on existing addresses — it plays no role in allocating new ones.

---

### Summary

The freshness mechanism is the **enfilade structure itself acting as an implicit registry**. The single global `granf` (initialized in `entexit.c:44`) is both storage and address space. Each allocation:
1. Queries `findpreviousisagr` to find the highest occupied address under the hint namespace (`granf2.c:217`).
2. Returns `max + 1` as the new address (`granf2.c:237–241`).
3. Inserts the new address into the enfilade, advancing the frontier (`granf2.c:125`).

There is no counter, no bitmap, no separate registry. Uniqueness is a monotonic structural property of the sorted enfilade: once an address is in the tree, it raises the floor for all future allocations in its namespace.
