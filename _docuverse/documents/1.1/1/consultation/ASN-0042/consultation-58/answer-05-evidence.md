## Question 5 [evidence]

> Does udanax-green provide an allocation path by which a node-level principal (a session whose account tumbler has `zeros = 0`) creates a content-bearing address in a single allocation call, analogous to `docreatenewversion`'s `makehint(ACCOUNT, DOCUMENT, ...)` for account-level principals?

## KB Synthesis

No. The KB documents no such path.

The `makehint` table from [SS-ADDRESS-ALLOC / Finding 0021] lists only four supertype→subtype combinations:

| supertype | subtype | depth |
|-----------|---------|-------|
| NODE | NODE | 1 |
| ACCOUNT | DOCUMENT | 2 |
| DOCUMENT | DOCUMENT | 1 |
| DOCUMENT | ATOM | — |

There is no `NODE → DOCUMENT` entry. The only documented allocation originating from a node-level principal (`zeros = 0` in mantissa) is `NODE → NODE` at depth=1, which creates another node — not a content-bearing document orgl.

The analog you describe — `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` in `docreatenewversion`'s unowned-version path [SS-VERSION-ADDRESS / Finding 0068] — works because `ACCOUNT` and `DOCUMENT` are different types (depth=2, crossing one `.0.` boundary). For a node-level principal to reach document depth, two `.0.` boundaries would need to be crossed, which would require a depth=3 invocation of `findisatoinsertnonmolecule`. No such call appears in the KB.

The concrete implication: a node-level session wanting a content-bearing address must proceed in at least two allocation steps — first obtain an account-level address under the node (NODE→NODE at depth=1 producing something like `1.1.1`... or an undocumented NODE→ACCOUNT path), then allocate a document under that account. No single-call shortcut equivalent to the account-level `ACCOUNT→DOCUMENT` is documented anywhere in the KB.

---

## Code Exploration

I now have all the source I need. Here is my full answer.

---

## No: There Is No Node-Level Analog to `makehint(ACCOUNT, DOCUMENT, ...)`

### The Reference Path (Account-Level Principal)

`docreatenewversion` [`do1.c:260`] dispatches on ownership:

```c
// do1.c:270-276
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The ACCOUNT branch at `do1.c:275` calls `createorglingranf` once. In `findisatoinsertnonmolecule` [`granf2.c:203`]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

`ACCOUNT ≠ DOCUMENT` so `depth = 2`. Starting from an account-level address like `1.2.0.50` (one zero separator, `tumblerlength = 4`), the first available slot is placed at `depth = 2` positions below — e.g., `1.2.0.50.0.1` — a proper document-level address with **two zero separators**.

### The Node-Level Path: `docreatenode_or_account`

The only allocation call designed for node-level principals is [`do1.c:243–258`]:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    ...
}
```

This is FEBE request `CREATENODE_OR_ACCOUNT = 38` [`requests.h:45`].

`NODE == NODE` so `depth = 1` in `findisatoinsertnonmolecule`. Starting from a node-level address like `1.1` (zero separators, `tumblerlength = 2`), the result is one position below — e.g., `1.1.1` — a **node-level address with zero zero separators**. The produced orgl is structurally a POOM (via `createenf(POOM)` at `granf2.c:120`) but lives at the wrong semantic depth to function as a document.

### What "Zeros = 0" Means Here

The tumbler struct [`common.h:59–64`] has no field named `zeros`. The term refers to the count of zero-digit field separators in the significant mantissa positions. `tumbleraccounteq` [`tumble.c:38`] terminates when it finds the **second consecutive zero in the account tumbler's mantissa** — that's the structural boundary of an account's sub-space. A node-level address (e.g., `1.1`) has no zero separator yet; `tumbleraccounteq` exits at the first trailing zero pair without having crossed any field boundary, causing `isthisusersdocument` [`be.c:171`, `socketbe.c:197`] to return TRUE for any address beginning with `1.1.*`. This means access control is permissive for node-level principals across their whole subtree — but it has no bearing on whether a correct-depth address is allocated.

### Why the Analog Is Absent

All existing `makehint` call sites:

| Call site | hint | depth | Resulting level |
|-----------|------|-------|-----------------|
| `do1.c:117` | `(DOCUMENT, ATOM, TEXTATOM, ...)` | 2 | atom (3 zeros) |
| `do1.c:180`, `207` | `(DOCUMENT, ATOM, LINKATOM, ...)` | 2 | link atom (3 zeros) |
| `do1.c:239` | `(ACCOUNT, DOCUMENT, 0, &taskptr->account, ...)` | 2 | document (2 zeros) |
| `do1.c:251` | **(NODE, NODE, 0, &isa, ...)** | **1** | **sub-node (0 zeros)** |
| `do1.c:271` | `(DOCUMENT, DOCUMENT, 0, isaptr, ...)` | 1 | sub-document (2 zeros) |
| `do1.c:275` | `(ACCOUNT, DOCUMENT, 0, wheretoputit, ...)` | 2 | document (2 zeros) |

`makehint` is defined at [`do2.c:78–84`]:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

There is no call to `makehint(NODE, DOCUMENT, ...)` or `makehint(NODE, ACCOUNT, ...)` anywhere in the codebase. Bridging from node to document in one step would require `depth = 4` (node → zero → account → zero → document), but `findisatoinsertnonmolecule` only computes `depth ∈ {1, 2}` based on the `supertype == subtype` test. No allocation function calls `createorglingranf` with a NODE-origin hint that produces a two-zero-separator document address.

### What a Node-Level Principal Can Actually Do

`docreatenewdocument` [`do1.c:234`] uses `&taskptr->account` unconditionally:

```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

If a node-level principal's `taskptr->account` is `1.1` (zero zeros), `findisatoinsertnonmolecule` with `depth = 2` produces `tumblerincrement(1.1, 2, 1)` = `1.1.0.1` — one zero separator — an **account-level** address. This is mechanically a single call but produces the wrong semantic depth; it replicates what should be a node→account transition, not node→document.

To reach a proper document-level address, a node-level principal requires **two** `createorglingranf` calls:

1. `CREATENODE_OR_ACCOUNT` (request 38) → allocates account orgl at `1.1.1` (or similar sub-node address, `makehint(NODE, NODE, ...)`, depth 1)
2. `CREATENEWDOCUMENT` (request 11) with `taskptr->account` updated to the newly created address → allocates document orgl at `1.1.1.0.1` (`makehint(ACCOUNT, DOCUMENT, ...)`, depth 2)

**There is no single-call path for a node-level principal that produces a content-bearing document address (two zero separators) equivalent to what `docreatenewversion`'s `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` produces for account-level principals.**
