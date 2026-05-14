## Question 1 [evidence]

> When `docreatenewversion` routes a fork through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)`, what depth tumbler does the resulting allocation produce — document-level, element-level, or something else — and does the trajectory involve one allocation call or multiple?

## KB Synthesis

## Unowned VERSION allocation: depth, structure, and call count

### Depth and address structure

`makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` sets depth=2 because `supertype ≠ subtype` (ACCOUNT vs. DOCUMENT) [SS-ADDRESS-ALLOC Finding 0021]. With `wheretoputit` as the creating user's account address, the allocation computes:

```
upperbound = tumblerincrement(account_addr, depth-1=1, 1)
```

This bounds the search to the next sibling account, and `findpreviousisagr` finds the highest existing address strictly within the user's account namespace. The result is a **document-level address** — exactly the `account.0.N` pattern crossing one `.0.` boundary. This is structurally identical to regular CREATEDOCUMENT behavior [SS-VERSION-ADDRESS Finding 0068]:

> User B (account `1.1.0.2`) versions User A's doc `1.1.0.1.0.1` → version at `1.1.0.2.0.1`

The owned path (`DOCUMENT, DOCUMENT`, depth=1) by contrast produces `doc.N` — no additional `.0.` boundary, child under the source document. The unowned path produces a sibling of existing documents under the creating account, not a child of the source document at all. Address lineage is broken.

### Number of allocation calls

**One** allocation call: `docreatenewversion` routes through `createorglingranf` which calls `findisatoinsertnonmolecule` once [ST-VERSION Finding 0077]. The full CREATENEWVERSION effect is two operations total — (1) the single address allocation and (2) `docopyinternal` to populate the version's text content — but address allocation itself is a single `findisatoinsertnonmolecule` invocation using the stateless query-and-increment mechanism [SS-ADDRESS-ALLOC Finding 0068].

### Summary

The unowned fork allocates at **document level** (depth=2, `account.0.N` form) in **one allocation call**, producing an address structurally indistinguishable from a freshly created document under the user's account. The version-to-source address relationship that encodes lineage in the owned case is absent entirely.

---

## Code Exploration

I now have all the source evidence needed. Here is the complete answer.

---

## Tracing `docreatenewversion` → `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)`

---

### The branch that fires

`docreatenewversion` contains a fork at `do1.c:270-275`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The `ACCOUNT, DOCUMENT` call fires whenever the new version is going into a *different* account than the source document — the "fork to another user's space" case. `wheretoputit` is the destination account-level ISA.

---

### What `makehint` does

`makehint` is defined at `do2.c:78-84`:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;      // ACCOUNT
    hintptr->subtype = typebelow;        // DOCUMENT
    hintptr->atomtype = typeofatom;      // 0
    movetumbler (isaptr, &hintptr->hintisa);  // copies wheretoputit verbatim
}
```

It records three type fields and copies `wheretoputit` (an account-level ISA) verbatim into `hint.hintisa`. No arithmetic yet.

---

### The call chain to allocation

`do1.c:277` immediately calls `createorglingranf(taskptr, granf, &hint, newisaptr)`.

`createorglingranf` (at `granf1.c:50-54`) is a one-line wrapper:

```c
return (createorglgr(taskptr, (typecuc*)granfptr, hintptr, isaptr));
```

`createorglgr` (at `granf2.c:111-128`) is where both the tumbler computation and the allocations happen:

```c
bool createorglgr(...)
{
    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))  // granf2.c:117 — computes isaptr
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf(POOM);           // granf2.c:120 — ALLOCATION 1
    reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    ...
    insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);              // granf2.c:125 — ALLOCATION 2
    ...
    return (TRUE);
}
```

---

### Tumbler depth calculation in `findisatoinsertgr` → `findisatoinsertnonmolecule`

`findisatoinsertgr` at `granf2.c:130-156` dispatches to `findisatoinsertnonmolecule` because `hintptr->subtype == DOCUMENT`, not `ATOM` — the atom branch requires a pre-existing document; the non-molecule path handles DOCUMENT and ACCOUNT placements.

Inside `findisatoinsertnonmolecule` at `granf2.c:203-242`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // granf2.c:209
```

`supertype = ACCOUNT`, `subtype = DOCUMENT` — they are not equal, so **`depth = 2`**.

```c
hintlength = tumblerlength(&hintptr->hintisa);  // granf2.c:211
```

`hintisa` holds the account-level `wheretoputit`, so `hintlength` is the component count of that address.

Then for the empty-subtree case (no document yet under this account):

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // granf2.c:237
```

The comment in the surrounding block (granf2.c:220) states the intent explicitly:

> "create the first child address as hintisa.0.1"

For the non-empty case:

```c
tumblertruncate(&lowerbound, hintlength + depth, isaptr);          // granf2.c:239
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);  // granf2.c:240
```

Both paths produce a tumbler of length `hintlength + depth = hintlength + 2`. The two appended levels (`depth = 2`) navigate from account level down to **document level** — exactly one structural tier below the account in the granfilade.

**The result placed into `newisaptr` is a document-level tumbler.**

---

### Allocation call count

The trajectory involves **two distinct allocation operations**, with a total of **three `createcrum` calls**:

**Allocation 1: `createenf(POOM)`** at `granf2.c:120`

`createenf` (at `credel.c:492-516`) is not a single-crum call:

```c
typecuc *createenf(INT enftype)
{
    fullcrumptr = (typecuc *) createcrum(1, enftype);          // credel.c:497 — apex crum
    ...
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);  // credel.c:501 — son crum
    ...
    return (fullcrumptr);
}
```

`createenf` itself makes **two `createcrum` calls** — one for the apex node, one for its son — building the empty POOM enfilade that will hold the new document's content.

**Allocation 2: `insertseq`** at `granf2.c:125`, which calls `createcrum` at `insert.c:44`:

```c
new = createcrum(0, (INT)ptr->cenftype);  // insert.c:44
```

This inserts a new crum node as a right brother at the granfilade's document-level slot corresponding to `isaptr`.

---

### Summary

| Question | Answer |
|---|---|
| **Tumbler depth** | **Document-level.** `findisatoinsertnonmolecule` computes `depth = 2` (ACCOUNT ≠ DOCUMENT), then calls `tumblerincrement(hintisa, 2, 1, isaptr)`, appending `.0.1` to the account-level hint address. The resulting ISA has two more components than the input account address — placing it at document level in the granfilade. |
| **Number of allocation calls** | **Two high-level operations; three `createcrum` calls.** First: `createenf(POOM)` at `granf2.c:120`, which internally calls `createcrum` twice (apex + son, `credel.c:497` and `credel.c:501`). Second: `insertseq` at `granf2.c:125`, which calls `createcrum` once at `insert.c:44` to insert the new slot into the granfilade. |
