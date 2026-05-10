## Question 18 [gregory]

> Is the set of valid node addresses fixed at system genesis (a finite, pre-allocated set), or can new node addresses be minted at runtime — and if so, what operation creates a new node entry?

## KB Synthesis

The KB does not describe a fixed, pre-allocated node address set. Node addresses are minted at runtime via the same stateless query-and-increment mechanism used for all non-molecule (structural) allocations.

**The allocation mechanism** is `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC, Finding 0021]. When allocating a node under another node, `makehint(NODE, NODE, depth=1, parent_isa, &hint)` is used. The algorithm:

1. Computes `upperbound = tumblerincrement(parent_isa, depth-1, 1)` — the next sibling of the parent
2. Calls `findpreviousisagr` to find the highest existing address under the parent
3. If none found: allocates first child as `parent.1` (e.g., `1.1.1` under node `1.1`)
4. Otherwise: truncates and increments to get the next sibling

The depth formula `depth = (supertype == subtype) ? 1 : 2` means NODE→NODE uses depth=1, producing sibling addresses without a `.0.` boundary (e.g., `1.1.0.1.1`, `1.1.0.1.2` under node `1.1.0.1`) [SS-ADDRESS-SPACE, Finding 0021].

**Runtime minting is confirmed by several invariants:**

- [INV-MONOTONIC]: All structural allocations are strictly monotonically increasing — new addresses are always added, never reused
- [INV-NO-IADDR-REUSE]: The granfilade is append-only; once an address exists, it persists permanently
- [SS-ENFILADE-TREE]: The granfilade starts empty (`createenf` produces a minimal height-1 tree), not pre-populated

**What the KB does not answer:** Whether there is a user-facing FEBE opcode for "create node" is not documented. The `makehint(NODE, NODE, ...)` case exists in the allocation dispatch, but the KB covers primarily document, link, and version creation operations. The genesis/bootstrap state (e.g., what node addresses exist at first startup) is also not described.

In summary: node addresses are **not fixed at genesis** — they follow the same demand-allocated, monotonically-growing address space as all other structural entities in the granfilade.

---

## Code Exploration

I now have everything needed from the source. Here is my complete answer.

---

## Are Node Addresses Fixed at Genesis or Minted at Runtime?

**New node addresses are minted at runtime.** There is no finite, pre-allocated address pool. Every new entry — account, document, node, link, or text span — receives a fresh tumbler computed on demand by searching the existing tree and incrementing past the highest occupied address.

---

## The Tumbler: What a "Node Address" Is

All addresses in udanax-green are **tumblers** — multi-part hierarchical numbers stored as a struct with a 16-place mantissa and an exponent:

```c
/* common.h:59-65 */
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`NPLACES` is 16 [`common.h:53`], explicitly increased from 11 "to support deeper version chains." The address space is effectively unbounded within these 16 positions.

The type hierarchy is defined as integer constants:

```c
/* xanadu.h:140-143 */
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

A `typehint` packages the parent address and the desired type transition to guide allocation:

```c
/* xanadu.h:148-153 */
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;     /* anchor address */
} typehint;
```

---

## The Minting Call Chain

Every creation operation follows this path:

### Layer 1: FEBE operation functions (`do1.c`)

**`docreatenewdocument()`** [`do1.c:234-241`]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```
The caller's account tumbler becomes the `hintisa` — the parent anchor. The returned `isaptr` is the freshly minted document address.

**`docreatenode_or_account()`** [`do1.c:243-258`]:
```c
tumblercopy(isaptr, &isa);
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
if (result) {
    tumblercopy(&isa, isaptr);
}
```
The input `isaptr` acts as the hint anchor (the parent node), and the output is the newly allocated node address.

**`docreatelink()` / `domakelink()`** [`do1.c:180-221`]:
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr)
```
Links get addresses minted under the owning document using the ATOM subtype path.

### Layer 2: Granfilade creation (`granf2.c`)

**`createorglingranf()`** [`granf2.c:111-128`]:
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```
This function does three things: (1) mint the address, (2) allocate a new enfilade structure in memory, (3) register the address→enfilade mapping in the tree.

**`findisatoinsertgr()`** [`granf2.c:130-156`] routes to the right minting sub-function:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
```

### Layer 3: The core mint — `findisatoinsertnonmolecule()` [`granf2.c:203-242`]

This is where the address is actually computed:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

It asks: *what is the highest existing address below `upperbound`?*

```c
/* BUG FIX comments explain the logic: */
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* line 237 */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);  /* line 240 */
}
```

Two cases:
- **First child under a parent**: the new address is `hintisa` extended by `depth` zero-separators and `1` (e.g., if hint is `1.1.0.1`, new doc is `1.1.0.1.0.1`).
- **Nth sibling**: take the highest existing sibling, truncate to the appropriate prefix length, and add 1.

### Layer 4: `tumblerincrement()` [`tumble.c:599-623`]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {
        tumblerclear (cptr);
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    if (aptr != cptr) movetumbler(aptr,cptr);
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    if (idx + rightshift >= NPLACES)
        gerror ("tumblerincrement overflow\n");
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

This is pure arithmetic — no global counter, no registry. It adds `bint` at the position `idx + rightshift` in the mantissa of the existing tumbler. The only error condition is mantissa overflow (consuming all 16 places).

---

## Summary

| Question | Answer |
|----------|--------|
| Fixed at genesis? | **No.** No pre-allocated pool exists anywhere in the source. |
| Minted at runtime? | **Yes.** Every create operation computes a fresh tumbler. |
| Operation that creates a new node entry? | `createorglingranf()` [`granf2.c:111`], called by `docreatenewdocument()`, `docreatenode_or_account()`, `docreatelink()`, and `docreatenewversion()` in `do1.c`. |
| Core address-generation function? | `findisatoinsertnonmolecule()` [`granf2.c:203`], which walks the granfilade tree for the highest occupied sibling and increments past it via `tumblerincrement()`. |
| What limits the space? | Only the 16-place tumbler mantissa (`NPLACES=16`, `common.h:53`) and available memory. There is no logical ceiling imposed by the system. |

The address space is **open-ended and grows monotonically**: new addresses are always strictly greater than all previously issued siblings under the same parent. No address is ever reused (deletions remove enfilade entries but the granfilade address is not reclaimed for reuse). The system is self-indexing — the tree itself is the oracle for "what addresses have been issued."
