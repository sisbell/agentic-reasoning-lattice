## Question 6 [evidence]

> In udanax-green, how is node-address uniqueness guaranteed across nodes, and what is the contract the implementation assumes about node identifiers?

## KB Synthesis

## Node-Address Uniqueness in udanax-green

### Allocation Mechanism

All node-level addresses — documents, versions, link orgls, and content atoms — are allocated through a stateless **query-and-increment** scheme [SS-ADDRESS-ALLOC, Finding 0021]:

1. Compute an upper bound from the parent address: `upperbound = tumblerincrement(parent, depth-1, 1)` (the next sibling of the parent)
2. Call `findpreviousisagr` to find the highest existing address strictly below that bound in the granfilade tree
3. If none exists under the parent, allocate the first child: `parent.0.1`
4. Otherwise, truncate the found address to the parent's length and increment by 1

There is no cached "next available" pointer. The allocation is a pure function of current granfilade state: `next_addr(granf, parent) = max_child(granf, parent) + 1` [SS-ADDRESS-ALLOC, Finding 0077].

### Guarantees That Enforce Uniqueness

**Monotonicity** [INV-MONOTONIC]: Every allocation produces a strictly greater address than all prior allocations within the same namespace. This holds across all entity types — text atoms, link orgls, document addresses — because they all share the same granfilade tree and the same allocator. Operations like DELETE and REARRANGE never touch the granfilade, so deleted addresses remain in the tree and continue to influence future allocation bounds [FC-GRANF-ON-DELETE].

**No address reuse** [INV-NO-IADDR-REUSE]: Once allocated, an address persists permanently in the granfilade regardless of subsequent deletions. The allocator always queries the current maximum; gaps left by deletions are never reclaimed.

**Single-threaded dispatch** [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]: The backend event loop processes one FEBE request at a time via run-to-completion scheduling (`bed.c` iterates sequentially over ready file descriptors, calling `xanadu()` synchronously per request). This makes the query-and-increment sequence atomic — no two allocations can observe the same granfilade maximum.

**Containment check** [PRE-ADDRESS-ALLOC, SS-TUMBLER-CONTAINMENT]: After `findpreviousisagr` returns a candidate, the allocator verifies the result is actually a descendant of the target parent via prefix-match (`tumblertruncate` + `tumblereq`). Without this, the search can cross account boundaries and allocate addresses under the wrong parent (Bug 0013 was exactly this failure).

**Independent per-namespace counters** [SS-ADDRESS-SPACE, Finding 0077]: There is no single global counter. The allocation is partitioned by tumbler range — document addresses search under their account/document parent, content I-addresses search under their document's content subspace, link I-addresses search under `docISA.2.x`. Each namespace grows independently without interference [INV-GLOBAL-ADDRESS-UNIQUENESS].

### Implicit Contract

The implementation assumes:

| Assumption | Source |
|---|---|
| Single-threaded access — no concurrent allocations can interleave | [INV-SEQUENTIAL-DISPATCH] |
| The granfilade is the sole authoritative source of existing addresses | [SS-ADDRESS-ALLOC] |
| Allocated addresses are never externally removed from the granfilade | [INV-NO-IADDR-REUSE] |
| Callers supply the correct parent address for containment scoping | [PRE-ADDRESS-ALLOC] |

There is no locking, no transaction log, and no cross-check against an external registry. Uniqueness is a consequence of the monotonic append-only granfilade combined with single-threaded execution. If those two structural properties hold, uniqueness follows automatically — the next allocated address is always strictly greater than the current maximum, and the maximum is never decremented.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## Node-Address Uniqueness in udanax-green

There are two distinct kinds of "node" in this codebase, and their uniqueness mechanisms are entirely different.

---

### 1. ISAs — The Permanent, Globally Unique Addresses

The **ISA** (`typeisa`, which is just a `tumbler`) is the persistent address of a document, account, link, or node in the Xanadu address space. This is what the system truly means by "node address." ISA uniqueness is the primary contract.

#### The Tumbler Data Type

All addresses are **tumblers** — variable-precision quasi-decimal numbers [`common.h:59-65`]:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;   /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

`NPLACES` is 16 [`common.h:53`], giving the mantissa 16 decimal places. Tumblers encode hierarchical addresses (e.g., `1.1.0.1.0.1` for a document under account `1.1`) by stacking digits at successively deeper positions.

#### How ISAs Are Allocated

Every new document, account, or node passes through `findisatoinsertgr` → `findisatoinsertnonmolecule` in `granf2.c`. The algorithm [`granf2.c:203-242`] is:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    hintlength = tumblerlength(&hintptr->hintisa);

    tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    ...
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // first child: hint.0.1
    } else {
        tumblertruncate(&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
    }
}
```

Step by step:
1. **Find the `hintisa`**: The caller provides a hint — the parent address (an account tumbler from `taskptr->account`, or a document ISA for child items). [`do1.c:239`]: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)`.
2. **Scan for the predecessor**: `findpreviousisagr` walks the single global granfilade and finds the largest ISA already allocated strictly below the upper bound [`granf2.c:255-278`].
3. **Increment**: The predecessor's address is truncated to the correct depth and incremented by 1.

**Uniqueness guarantee**: Because all ISAs live in one global granfilade (a sorted, non-overlapping tree), and `findpreviousisagr` always finds the exact highest predecessor before the upper bound, the incremented result cannot equal any existing ISA. This is essentially an implicit monotone counter per scope, maintained by the structure of the granfilade rather than by an explicit integer.

**No concurrent access**: The event loop in `bed.c` is single-threaded; there is no mutex needed because only one request runs at a time.

#### The `typehint` — The Scope Contract

ISA allocation is scoped by a `typehint` struct [`xanadu.h:148-153`]:

```c
typedef struct {
    INT supertype;   // NODE, ACCOUNT, DOCUMENT, ATOM
    INT subtype;
    INT atomtype;
    typeisa hintisa; // The parent address
} typehint;
```

`supertype`/`subtype` determine the address depth (1 level for same-type nesting, 2 levels for cross-type), ensuring that documents under account `1.1` get addresses `1.1.0.1`, `1.1.0.2`, etc., structurally isolated from documents under `1.2`.

---

### 2. POOM Crums — In-Memory Tree Nodes

These are the C structs (`type2dcbc`, `typecuc`) that form the in-memory enfilade. They are **not** Xanadu document nodes — they are positional intervals in a B-tree-like structure, identified by their `(cwid, cdsp)` pair.

#### The Crum Structure

Every crum has [`enf.h:47-48, 71-72`]:

```c
typewid cwid;   // content width — the size of the address range this node covers
typedsp cdsp;   // content displacement — relative offset from parent
```

Both `typewid` and `typedsp` are `struct { tumbler dsas[MAXLOXIZE]; }` — for POOM, two tumblers: `dsas[I]` (horizontal) and `dsas[V]` (vertical) [`wisp.h:19-20, 50-54`].

#### Node Creation — No Identity Assigned at Allocation

`createcruminternal` (`credel.c:541-595`) is the only allocation site. It zeroes both fields:

```c
clear(&ptr->cdsp, sizeof(ptr->cdsp));   // credel.c:580
clear(&ptr->cwid, sizeof(ptr->cwid));   // credel.c:581
```

The `++crumnumber` at line 594 is a **statistics counter only**, not a unique identifier.

#### Identity Assigned at Insertion

A crum receives its address only when inserted. For POOM:

- `makegappm` (`insertnd.c:124-172`) cuts the existing V-space to make room, then shifts displaced crums: `tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V])` [`insertnd.c:162`].
- `firstinsertionnd` (`insertnd.c:199-217`) stamps a fresh crum's position directly from the client-provided `origin` and `width`: `movewisp(origin, &ptr->cdsp)` and `movewisp(width, &ptr->cwid)`.
- `insertcbcnd` (`insertnd.c:242-275`) checks adjacency via `isanextensionnd` before creating a new crum, allowing contiguous content to coalesce rather than proliferate crums.

**Uniqueness in the tree** is guaranteed structurally: two crums at the same level cannot have overlapping intervals because insertion splits (via `makecutsnd`) and shifts before placing new content. The parent's `cwid` is updated by `setwispupwards` as the aggregate of children, maintaining the invariant bottom-up.

---

### 3. The Contract the Implementation Assumes

The backend makes several explicit and implicit assumptions:

| Assumption | Where enforced |
|---|---|
| Width is never zero | `insertnd.c:48-49`: `if (iszerotumbler(&width->dsas[index])) gerror("zero width in insertnd\n")` |
| Tumblers are positive and normalized | `tumble.c:169-226`: `tumblercheckptr` validates sign, mantissa, and exp fields |
| The hint ISA belongs to the calling user's account | `do1.c:270`: `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` checked before version creation |
| Client provides valid V-space coordinates for insert | `makegappm` silently no-ops if `origin` is out of the crum's range [`insertnd.c:140-143`]: `if (iszerotumbler(&fullcrumptr->cwid.dsas[V]) || tumblercmp(&origin->dsas[V], &grasp.dsas[V]) == LESS || tumblercmp(&origin->dsas[V], &reach.dsas[V]) != LESS) return(0)` |
| Single global granfilade serializes ISA allocation | `granf1.c`/`granf2.c`: no locking because the event loop is non-concurrent |
| Tumblers are hierarchically structured | Hierarchy in mantissa encodes parent/child relationships; `tumbleraccounteq` (`tumble.c:38-70`) exploits this structure to check ownership |

**The backend does not implement a collision-detection table.** Uniqueness of ISAs is an emergent property of the granfilade's sorted structure plus monotone increment. Uniqueness of POOM crum intervals is an emergent property of the cut-and-shift insertion protocol. Neither is backed by a hash set or sequence number.

---

### Summary

Node-address uniqueness in udanax-green operates at two levels:

**ISA level**: Guaranteed by scan-then-increment in a single global granfilade (`findisatoinsertnonmolecule`, `granf2.c:203-242`). The sorted structure makes collision structurally impossible; the single-threaded event loop eliminates races. The assumed contract is: the caller provides a valid `hintisa` (an account tumbler) and the backend allocates the next available child address.

**POOM crum level**: Guaranteed by the cut-before-insert protocol (`makegappm`, `insertnd.c:124-172`). Crums have no intrinsic identity at allocation time — they acquire positional identity only when placed. The assumed contract is: the caller provides `origin` and `width` tumblers that describe a valid, non-zero region inside the existing enfilade's address range.
