## Question 2 [evidence]

> Does udanax-green allocate node addresses through a mechanism distinct from the granfilade/document state, and if so, what registry or structure tracks allocated node addresses?

## KB Synthesis

Node addresses in udanax-green are **not** allocated through any mechanism distinct from the granfilade. The granfilade itself is the registry.

## Single Unified Allocation Tree

All persistent state — document addresses, version addresses, link orgl ISAs, and content I-addresses — lives in the same global granfilade tree [SS-UNIFIED-STORAGE]. There is no separate node registry, address table, or counter.

[SS-ADDRESS-ALLOC] (Finding 0077) makes this explicit:

> "There is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`."

## Allocation Mechanism

`findisatoinsertnonmolecule` (for document/node addresses) operates:
1. Compute upper bound from parent address: `tumblerincrement(hintisa, depth-1, 1)`
2. Call `findpreviousisagr` — traverse the granfilade tree to find the highest existing address below that bound
3. Containment check: verify the found address is actually under the target parent [PRE-ADDRESS-ALLOC]
4. Allocate: truncate and increment by 1, or use first-child convention `parent.0.1` if none exist

[SS-ADDRESS-ALLOC] (Finding 0061) confirms: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

## Address Space Partitioning Within the Granfilade

Document addresses and content I-addresses share the same tree but occupy different tumbler ranges [SS-ADDRESS-SPACE] (Finding 0077):

```
1.1.0.1                      ← account
├── 1.1.0.1.0.1              ← document (via findisatoinsertnonmolecule, depth=2)
│   └── 1.1.0.1.0.1.1        ← version (depth=1, child of doc)
└── 1.1.0.1.0.1.3.0.1.1      ← content I-address (via findisatoinsertmolecule)
```

The dispatcher `findisatoinsertgr` routes to either the molecule (content) or non-molecule (document/node) allocator based on entity type.

## Invariants

Because the granfilade is append-only [FC-GRANF-ON-DELETE], allocated addresses persist permanently. Deleted addresses are never reused [INV-NO-IADDR-REUSE], and all allocations are strictly monotonically increasing within each namespace [INV-MONOTONIC].

---

## Code Exploration

I now have all the source evidence needed. Here is the complete answer:

---

## Node Address Allocation in Udanax-Green

### Short Answer

There is **no separate registry** for node addresses. The granfilade tree (`granf`) *is* the address registry. Every allocated address exists as a node in that tree; allocation works by scanning the tree for the highest existing address under a hint location, then incrementing by one.

---

### Address Representation

`typeisa` is defined as simply:

```c
typedef tumbler typeisa;   /* xanadu.h:23 */
```

A tumbler is a multi-precision rational stored as exponent + mantissa:

```c
typedef struct structtumbler {
    humber xvartumbler;
    ...
} tumbler;   /* common.h:59-65 */
```

---

### The `typehint` Structure

All address allocation is driven by a hint (`xanadu.h:140-153`):

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2

typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

The hint tells the allocator: "I want to insert something of this type at approximately this address." `makehint` constructs it (`do2.c:78-84`):

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

---

### Call Chain for Every Allocation

| Operation | Hint args | Site |
|-----------|-----------|------|
| Create node/account | `(NODE, NODE, 0, isa)` | `do1.c:251` |
| Create document | `(ACCOUNT, DOCUMENT, 0, account)` | `do1.c:239` |
| Create new version | `(DOCUMENT, DOCUMENT, 0, isa)` | `do1.c:271` |
| Insert text | `(DOCUMENT, ATOM, TEXTATOM, doc)` | `do1.c:117` |
| Create link | `(DOCUMENT, ATOM, LINKATOM, doc)` | `do1.c:207` |

All paths converge on `createorglingranf` or `inserttextingranf` (`granf1.c:50,44`), which delegate to `granf2.c`.

---

### The Allocation Heart: `findisatoinsertgr` (`granf2.c:130`)

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) return (FALSE);
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

Two code paths:

**For non-molecules (NODE/ACCOUNT/DOCUMENT)** — `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing yet — first child: hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    /* Increment the highest existing address */
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

**For atoms (text/link content)** — `findisatoinsertmolecule` (`granf2.c:158-181`): same pattern but with molecule-specific depth arithmetic.

---

### Tree Search: `findpreviousisagr` (`granf2.c:255-278`)

This recursively walks the granfilade tree to find the **highest ISA address below a given upper bound**:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (whereoncrum (ptr, offset, upperbound, WIDTH) == THRUME || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```

There is no free-list, no counter. The tree walk itself is the address-space scan.

---

### `tumblerincrement` (`tumble.c:599-623`)

The primitive that mints a new address by adding an integer at a shifted position in the mantissa:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    if (aptr != cptr) movetumbler(aptr,cptr);
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

No global state is touched.

---

### What Does Track State (And What Doesn't)

**`berttable[1327]` in `bert.c:29`** — a hash table of `bertentry` structs:

```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;

static conscell *berttable[NUMBEROFBERTTABLE];   /* bert.c:29 */
```

This tracks **open documents** (read/write locks per connection), **not** the set of all allocated addresses. It is in-memory only; it is not persisted to disk and is rebuilt each session as documents are opened.

**`currentaccount` in `bed.c:43`** — logs the current active user session, unrelated to address allocation.

**`granf` and `spanf`** — global pointers to the roots of the granfilade and spanfilade trees. These ARE persisted. On startup (`entexit.c:41-46`):

```c
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

On shutdown, `writeenfilades()` serializes the entire tree to disk. This is the only persistence mechanism for address state.

---

### Conclusion

**Node addresses are not tracked by any structure distinct from the granfilade tree.** The granfilade itself is the address registry:

1. Every allocated address is a node in the tree.
2. Allocation works by calling `findpreviousisagr` to scan the tree for the current maximum address under a hint location, then calling `tumblerincrement` to derive the next address.
3. There is no global counter, no free-list, no pre-allocated range, and no separate persistent address table.
4. The `bert.c` hash table tracks open-document locks per session — a distinct concern from address allocation.
5. Address state persists across restarts solely through the granfilade tree written by `writeenfilades()` and reloaded by `initenffile()`.
