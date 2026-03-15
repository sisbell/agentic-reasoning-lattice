## Question 7 [gregory]

> What constitutes "baptizing" a tumbler position — is it the first successful allocation at that level via query-and-increment, or is there a distinct registration step that precedes allocation?

## KB Synthesis

The KB does not use the term "baptism" explicitly, so I'll synthesize what the allocation evidence implies about when a tumbler position becomes "established" in the system.

## The Allocation Mechanism Is the Only Registration Step

Based on the evidence in the KB, there is no distinct registration step prior to allocation. The query-and-increment write into the granfilade **is** the singular act that establishes a tumbler position:

**Document addresses** — `createorglingranf` calls `findisatoinsertnonmolecule`, which:
1. Computes upper bound via `tumblerincrement(hintisa, depth-1, 1)`
2. Calls `findpreviousisagr` to find the highest existing address below that bound
3. Checks containment under the parent (Bug 0013 fix)
4. Writes the new orgl node into the granfilade tree

The moment the node is written, the address exists in the tree and influences all subsequent allocations in that range. [SS-ADDRESS-ALLOC]

**Content I-addresses** — `inserttextingranf` similarly calls `findisatoinsertmolecule`, finds the previous maximum, increments by 1, then writes. [SS-ADDRESS-SPACE / Finding 0061]

**Link I-addresses** — `domakelink` uses the same pattern scoped to `docISA.2.2–docISA.2.3`. [SS-ADDRESS-ALLOC / Finding 0065]

## Why There Is No Separate Registration

Three properties make a prior registration step unnecessary:

1. **Stateless allocation** — There is no cached "next available" pointer. Every allocation queries the live granfilade tree for the current maximum. The tree itself is the canonical registry. [Finding 0061]

2. **Monotonic uniqueness** — Because allocation always takes `max + 1` and the granfilade is append-only, no address is ever reused. Existence in the tree is both necessary and sufficient for an address to be "established." [INV-MONOTONIC, INV-NO-IADDR-REUSE]

3. **Partitioned namespaces** — Each tumbler range (document addresses, text I-addresses, link I-addresses) is allocated independently via `findisatoinsertgr` dispatching to molecule vs. non-molecule paths. Each partition's "baptism" is scoped: `next_doc_addr(granf, parent)` and `next_content_addr(granf, doc)` are independent functions of tree state. [Finding 0077]

## The Distinction That May Matter

What could be called "baptism" at the account/document hierarchy level is the first-child allocation: when no children exist under a parent, the algorithm allocates `parent.0.1` rather than incrementing from a prior maximum. This first-child creation is the only structurally distinct case — subsequent allocations simply increment the sibling counter. [SS-ADDRESS-ALLOC / Finding 0021]

```
Parent account 1.1.0.2, no existing documents:
  findpreviousisagr returns nothing under parent
  → allocates 1.1.0.2.0.1  ← "baptism": first child
  
Same account, existing document 1.1.0.2.0.1:
  findpreviousisagr returns 1.1.0.2.0.1
  → allocates 1.1.0.2.0.2  ← ordinary increment
```

The granfilade write is the single moment of establishment in both cases — the query-and-increment process has no predecessor registration step separate from the write itself.

---

## Code Exploration

Now I have everything needed for a complete answer. Here it is:

---

## "Baptizing" a Tumbler Position in udanax-green

The word **"baptize" does not appear anywhere in the source code.** However, the concept maps precisely onto the two-phase address allocation + insertion sequence. Here is the exact code trace.

---

### Phase 0: Hint Construction — The Pre-Condition

Before any address is computed, the caller constructs a `typehint` that encodes *where* the new item should live and *what kind of thing* it is.

**`do2.c:78`** — `makehint`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`typehint` is defined at **`xanadu.h:148-153`**:
```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

`hintisa` is the *parent address* — the account or document under which the new item will be allocated. For example:

- `do1.c:239` — creating a new document: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` — parent is the current account
- `do1.c:117` — inserting text: `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)` — parent is the open document
- `do1.c:251` — creating a node: `makehint(NODE, NODE, 0, &isa, &hint)` — parent is the node itself

This is **not** allocation. It sets up the context for the forthcoming query.

---

### Phase 1: Address Computation — Query-and-Increment

The entry point is **`granf2.c:130`** — `findisatoinsertgr`:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
            return (FALSE);
        }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);   // granf2.c:154
    return (TRUE);
}
```

#### For documents/accounts/nodes — `findisatoinsertnonmolecule` (`granf2.c:203`)

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // :209
hintlength = tumblerlength (&hintptr->hintisa);           // :211
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // :213 — compute search ceiling
clear (&lowerbound, sizeof(lowerbound));                  // :215
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound); // :217 — QUERY
```

`findpreviousisagr` (`granf2.c:255`) descends the tree to find the **highest existing address** strictly below `upperbound`. Nothing is written here.

Then, at `granf2.c:235-241`, the new address is computed:
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing exists under this parent yet — first child
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // :237
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr); // :239
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr); // :240
}
```

`tumblerincrement` (`tumble.c:599`) is the arithmetic primitive:
```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) {           // :603
        tumblerclear (cptr);
        cptr->exp = -rightshift;
        cptr->mantissa[0] = bint;
        return(0);
    }
    // ...
    cptr->mantissa[idx + rightshift] += bint;  // :621
    tumblerjustify (cptr);                     // :622
}
```

**At this point, the address exists only as bits in a local variable `isaptr`.** Nothing has been written to the granfilade tree.

#### For text/link atoms — `findisatoinsertmolecule` (`granf2.c:158`)

Same pattern: `tumblerincrement` computes an `upperbound`, `findpreviousisagr` queries the tree for the highest existing atom, then a `tumblerincrement` on the result yields the new address. Still nothing is written.

---

### Phase 2: Insertion — The Moment of "Baptism"

The address returned by `findisatoinsertgr` is not yet real. It becomes real only when it is *inserted* into the enfilade.

#### For documents and links — `createorglgr` (`granf2.c:111`):

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))  // :117 — compute address
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);           // :120 — create new POOM
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);              // :125 — WRITE to tree
    ...
}
```

`insertseq` at `:125` is the actual insertion into the granfilade. This is the moment the address is committed — it can now be found by `findpreviousisagr` or `isaexistsgr`.

#### For text — `inserttextgr` (`granf2.c:83`):

```c
bool inserttextgr(...) {
    if (!findisatoinsertgr (..., hintptr, &lsa))  // :92 — compute starting address
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        ...
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);              // :99 — WRITE each chunk
        tumblerincrement (&lsa, 0, textset->length, &lsa);             // :100 — advance address
    }
    ...
}
```

The starting address is computed once; each chunk is inserted via `insertseq` at an address that advances by `textset->length` after each call.

---

### The Direct Answer

**There is no distinct "registration step" that precedes allocation.** The sequence is:

1. `makehint` — builds context (parent ISA, type relationship)
2. `findisatoinsertgr` → `findisatoinsertnonmolecule` / `findisatoinsertmolecule` — **query-and-increment**: reads the tree, computes the next available address, returns it in a local variable. Nothing is written.
3. `insertseq` (called from inside `createorglgr` or `inserttextgr`) — **writes the node** at the computed address into the granfilade tree.

**"Baptism" is `insertseq`, not the query-and-increment.** The query-and-increment produces a *candidate* address that exists only in memory. If you called `findisatoinsertgr` twice without `insertseq` in between, both calls would return the **same address** — because the tree has not changed and `findpreviousisagr` would find the same highest existing node both times.

The address is not a permanent, system-visible fact until it is inserted into the enfilade at `granf2.c:99` (text) or `granf2.c:125` (orgl). That insertion is what makes the address discoverable by all subsequent queries — it is the act that "baptizes" the position into the coordinate space.
