## Question 11 [evidence]

> When CREATENEWVERSION allocates the version's document address as a child of the source (e.g., `1.1.0.1.0.1.0.1`), does `findisatoinsertnonmolecule` derive the child number purely from the current maximum existing child under `docISA` in the granfilade, so that deleting nothing but forking twice always yields `.0.1` then `.0.2`?

## KB Synthesis

Yes, with one notational correction: the allocation is purely granfilade-state-driven, and two sequential forks with no deletions yield `docISA.1` then `docISA.2` — not `docISA.0.1` / `docISA.0.2`. The `.0.` separator only appears at depth=2 crossings (e.g., account→document); VERSION uses depth=1 (DOCUMENT→DOCUMENT), which produces no intermediate `.0.` field.

## Mechanism

`findisatoinsertnonmolecule` performs a stateless query-and-increment against the granfilade tree on every call [SS-ADDRESS-ALLOC, Finding 0061]:

1. Compute `upperbound = tumblerincrement(docISA, 0, 1)` — the next sibling of `docISA` (e.g., `1.1.0.1.0.2` for source `1.1.0.1.0.1`).
2. Call `findpreviousisagr` to find the highest existing address below that bound.
3. Apply containment check: verify the found address is actually under `docISA`.
4. If no child exists → allocate `docISA.1` (first child).
5. If a child exists → truncate to child length, increment by 1 → next sibling.

There is no cached counter or session-local state. The function reads live granfilade tree state each time [SS-ADDRESS-ALLOC, Finding 0061]: "There is no cached 'next available' pointer. This means allocation is stateless with respect to the session."

## Sequential Fork Behavior

For two forks in sequence with no deletions between them:

- **First fork**: `findpreviousisagr` finds nothing under `docISA` (no children) → allocates `docISA.1`
- **Second fork**: `findpreviousisagr` finds `docISA.1` (highest existing child) → truncate + increment → allocates `docISA.2`

The KB concrete example confirms this exactly [SS-ADDRESS-ALLOC, Finding 0068]:
```
Second version of 1.1.0.1.0.1:
  findpreviousisagr finds 1.1.0.1.0.1.1 (first version)
  truncate to length 7 → 1.1.0.1.0.1.1, increment → 1.1.0.1.0.1.2
```

And from [SS-VERSION-ADDRESS, Finding 0032]:
```
Original:            1.1.0.1.0.1
First version:       1.1.0.1.0.1.1   (child, depth=1, no .0. boundary)
Second version:      1.1.0.1.0.1.2
Version of version:  1.1.0.1.0.1.1.1 (grandchild)
```

## Permanence Guarantees

This mechanism is unconditionally monotonic. Version addresses, once allocated, persist permanently in the granfilade — "deleting a version does not remove its address from the granfilade. The version's address persists permanently and continues to influence subsequent version allocation" [FC-GRANF-ON-DELETE, Finding 0068]. This is the same no-reuse guarantee as for I-addresses [INV-NO-IADDR-REUSE]: the granfilade never shrinks, so `findpreviousisagr` always returns the true historical maximum.

## The `.0.` Notation Discrepancy

The `makehint` depth parameter controls whether a `.0.` boundary is inserted [SS-ADDRESS-SPACE, Finding 0021]:

| supertype | subtype | depth | format |
|-----------|---------|-------|--------|
| ACCOUNT | DOCUMENT | 2 | `account.0.N` (crosses one `.0.` boundary) |
| DOCUMENT | DOCUMENT | 1 | `document.N` (no `.0.` boundary) |

VERSION for an owned document uses `makehint(DOCUMENT, DOCUMENT, ...)` with depth=1 [SS-VERSION-ADDRESS, Finding 0068], so the child gets no `.0.` separator — it is `docISA.N`, not `docISA.0.N`. The `.0.` form (`docISA.0.1`) would indicate a depth=2 allocation, which applies to the unowned-document branch (where the version lands under the creating user's account instead).

---

## Code Exploration

Now I have everything needed. Here is the complete answer.

---

## Answer

### Call Chain

`createnewversion()` [fns.c:289] calls `docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)` [fns.c:296] — both the source and destination point to the same address (the original document's ISA).

Inside `docreatenewversion` [do1.c:260]:

```c
// do1.c:270–271 — normal case: user's own document
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
```

`makehint(DOCUMENT, DOCUMENT, 0, D, &hint)` sets `supertype=3, subtype=3` [do2.c:78–84]. This hint is passed to `createorglingranf()` [do1.c:277] → `createorglgr()` [granf1.c:54] → `findisatoinsertgr()` [granf2.c:117].

---

### Through `findisatoinsertgr`

At [granf2.c:135], since `hintptr->subtype == DOCUMENT != ATOM`, it takes the else branch [granf2.c:152] and calls `findisatoinsertnonmolecule()`, then `tumblerjustify()`.

---

### Inside `findisatoinsertnonmolecule` [granf2.c:203–242]

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // DOCUMENT==DOCUMENT → depth=1
hintlength = tumblerlength (&hintptr->hintisa);           // stories in D
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound); // D with last digit +1
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

**The search:** `findpreviousisagr` [granf2.c:256] traverses the enfilade to find the last key in the entire granfilade that is strictly less than `upperbound`. Because `upperbound = D + 1` (the last mantissa digit of D incremented), this range captures everything "inside" D: version children like `D.1`, `D.2` and also atom content like text at `D.0.1.N` and links at `D.0.2.N`.

**The `lowerbound_under_hint` guard** [granf2.c:228–233] then truncates whatever was found to `hintlength` digits and checks equality with D:

```c
tumblertruncate(&lowerbound, hintlength, &truncated);
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
```

This correctly rejects a lowerbound from a different account's subtree.

**The branch:**

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // First child: nothing under D yet
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // depth=1
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);  // strip to version level
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

---

### The Tumbler Arithmetic — What `.N` Actually Means

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599]:

```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;
```

With `depth=1` and `rightshift=1`:
- `idx` = position of last non-zero digit in D's mantissa
- Sets `mantissa[idx + 1] += 1`

This appends **one** mantissa digit. For `D = 1.1.0.1.0.1` (mantissa `[1,1,0,1,0,1,0,…]`, last non-zero at idx=5), the result is mantissa[6]=1 → printed as `1.1.0.1.0.1.1`.

The double-component `.0.N` pattern only occurs with `depth=2` (ACCOUNT→DOCUMENT, where `ACCOUNT != DOCUMENT` [granf2.c:209]). That is how documents are placed under accounts: `tumblerincrement(account, 2, 1)` = `account.0.1`. For DOCUMENT→DOCUMENT versioning, `depth=1` produces the single-suffix pattern.

`puttumbler` [put.c:26–46] confirms: it prints `mantissa[0]` through `mantissa[last_nonzero]` separated by dots, verbatim. So mantissa `[1,1,0,1,0,1,1,0,…]` prints as `1.1.0.1.0.1.1`.

---

### What Golden Tests Confirm

`golden/versions/version_address_allocation.json`:

```
doc1            → 1.1.0.1.0.1
first fork      → 1.1.0.1.0.1.1   (comment: "If child: doc1.1  If sibling: account.0.2")
second fork     → 1.1.0.1.0.1.2   (comment: "shows monotonic allocation")
version of doc2 → 1.1.0.1.0.2.1
version of v1   → 1.1.0.1.0.1.1.1
```

`golden/versions/multiple_versions_same_source.json` corroborates: two forks of `1.1.0.1.0.1` yield `1.1.0.1.0.1.1` then `1.1.0.1.0.1.2`.

---

### Direct Answer to the Question

**Yes, `findisatoinsertnonmolecule` derives the child number purely from the current maximum existing entry under `docISA` in the granfilade.** The mechanism is:

1. `findpreviousisagr` finds the last granfilade key below `D + 1` [granf2.c:217]
2. `tumblertruncate` strips sub-version content down to the version level (`hintlength + depth` digits) [granf2.c:239]
3. The last digit of that truncated address is incremented [granf2.c:240]

Content atoms inserted into D (text at `D.0.1.N`, links at `D.0.2.N`) are found by step 1 but collapsed back to `D` by step 2 (their leading version digit is zero, which `tumblerjustify` strips as trailing zeros), causing step 3 to fall back to `tumblerincrement(D, depth, 1)` — producing the first child, same as the empty case.

**However, the suffix pattern is `.1` then `.2`, not `.0.1` then `.0.2`.** With `depth=1`, `tumblerincrement` appends a single mantissa slot, not two. The `.0.N` double pattern belongs to `depth=2` allocation (account→document). So if source is `D = 1.1.0.1.0.1`:

- First fork (no prior children): `1.1.0.1.0.1.1` — not `1.1.0.1.0.1.0.1`
- Second fork (v1 exists): `1.1.0.1.0.1.2` — not `1.1.0.1.0.1.0.2`

The address `1.1.0.1.0.1.0.1` cited in the question would only appear as a CHILD OF A VERSION (e.g., a version of `1.1.0.1.0.1.1` producing `1.1.0.1.0.1.1.1`), not as the direct first version of a six-component document address.

The invariant **"forking twice yields child 1 then child 2"** holds exactly — it is purely granfilade-derived with no global counter. But the dot-notation suffix is `.N` (one component) rather than `.0.N` (two components).
