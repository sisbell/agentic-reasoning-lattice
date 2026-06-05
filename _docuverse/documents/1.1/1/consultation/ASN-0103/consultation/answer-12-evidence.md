## Question 12 [evidence]

> What bounded upper limit does the document-address allocation use to distinguish document tumblers from element-level tumblers within the account's I-address range?

## KB Synthesis

The document-address allocation algorithm uses the **next sibling of the parent account** as its upper bound.

From [SS-ADDRESS-ALLOC] (Finding 0021), `findisatoinsertnonmolecule` computes:

```
upperbound = tumblerincrement(hintisa, depth-1, 1)
```

For `ACCOUNT → DOCUMENT` allocation, `depth = 2`, so `depth-1 = 1`. Applied to account `1.1.0.2`, this produces `1.1.0.3` — the next account sibling. The search for the highest existing address is bounded to the half-open interval `[1.1.0.2, 1.1.0.3)`.

This range contains **both** document tumblers (e.g., `1.1.0.2.0.1`) and element tumblers (e.g., `1.1.0.2.0.1.0.2.1`). The mechanism that distinguishes them is the **truncation step**: after `findpreviousisagr` returns the highest address in range (potentially a deep element address), the algorithm truncates it to document level and increments — producing the next document-level sibling.

[PRE-ADDRESS-ALLOC] (Finding 0021) documents the bug this guards against: without a containment check after `findpreviousisagr`, the search could return `1.1.0.1.0.1` (under a *different* account) and incorrectly increment to `1.1.0.1.0.2` — violating account isolation (Bug 0013, [INV-ACCOUNT-ISOLATION]).

For comparison, element-level (molecule) allocation uses a tighter, document-scoped bound: `tumblerincrement(docISA, 2, atomtype+1)`, which confines allocation to within the document's element subspace [SS-ADDRESS-ALLOC] Finding 0065.

---

## Code Exploration

---

## Document vs. Element Tumbler Distinction: The `ATOM = 4` Upper Bound

### The Type Hierarchy

The I-address space has four levels, defined in `backend/xanadu.h:140-143`:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

These are not just names — they are the numeric level indices used by the granfilade allocator to determine *where* in the tumbler tree a new address should be placed.

---

### The `typehint` Struct

`backend/xanadu.h:148-153` defines the allocation hint:

```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

A hint specifies a range `[supertype, subtype]` in the type hierarchy. The allocator navigates to the `hintisa` tumbler and creates a new address one or two levels below it, depending on whether `supertype == subtype`.

---

### The Hard Upper Bound: `ATOM = 4`

`validhint()` in `backend/do2.c:86-97` enforces the constraint explicitly:

```c
int validhint(typehint *hintptr)
{
    if (
          (hintptr->supertype < NODE)
       || (hintptr->supertype > DOCUMENT)
       || (hintptr->subtype < ACCOUNT)
       || (hintptr->subtype > ATOM)            // ← hard upper limit
       || (hintptr->atomtype < 0)
       || (hintptr->atomtype > 2)
       || (hintptr->subtype < hintptr->supertype)
       || ((hintptr->subtype - hintptr->supertype) > 1)
       || ((hintptr->subtype == ATOM) == !hintptr->atomtype) ) {
```

The line `(hintptr->subtype > ATOM)` at `do2.c:92` is the authoritative bound. **No hint can specify a subtype greater than `ATOM (4)`**. There is no level 5.

The final constraint at `do2.c:97` enforces that `atomtype` must be non-zero *if and only if* `subtype == ATOM`, coupling element-level allocation directly to atom typing.

---

### How the Distinction Is Made at Allocation Time

In `backend/granf2.c:209`, the allocator computes depth:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Then at `granf2.c:213`:

```c
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

- **`depth = 1`** (`supertype == subtype`): allocates *at the same level* as the hint — used for document-level operations (new version of a document).
- **`depth = 2`** (`supertype < subtype`, i.e., `subtype - supertype == 1`): allocates *one level below* — used to create a child of a different type.

---

### The Two Allocation Patterns in Practice

**Document tumblers** (level 3, DOCUMENT):

- `backend/do1.c:239`: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);`  
  → subtype=`DOCUMENT(3)`, allocates a new document under the account.
- `backend/do1.c:271`: `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);`  
  → depth=1, allocates a new version of a document at the same document level.

**Element-level tumblers** (level 4, ATOM):

- `backend/do1.c:117`: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);`  
  → subtype=`ATOM(4)`, allocates text atoms *within* a document.
- `backend/do1.c:180`: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);`  
  → subtype=`ATOM(4)`, allocates link atoms within a document.

---

### Answer

The bounded upper limit is **`ATOM = 4`** (`backend/xanadu.h:143`).

Within an account's I-address range, the type hierarchy runs NODE(1) → ACCOUNT(2) → DOCUMENT(3) → ATOM(4). Document tumblers are allocated at level 3 (`subtype == DOCUMENT`); element-level tumblers are allocated at level 4 (`subtype == ATOM`). The `validhint()` function at `backend/do2.c:92` enforces `ATOM` as the strict upper bound — no hint may specify a subtype exceeding 4, and any hint with `subtype == ATOM` *must* carry a non-zero `atomtype` (`do2.c:97`), making the document/element boundary structurally enforced rather than merely conventional.
