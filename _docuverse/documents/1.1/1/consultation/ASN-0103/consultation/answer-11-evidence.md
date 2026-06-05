## Question 11 [evidence]

> When CREATEDOCUMENT allocates a new document address under an account, does `findisatoinsertnonmolecule` query the granfilade for the current maximum document tumbler under that account's `Node.0.User` parent and return max+1?

## KB Synthesis

Yes, that is exactly what happens. The mechanism is documented across [SS-ADDRESS-ALLOC] and [ST-ADDRESS-ALLOC].

**The allocation sequence for CREATEDOCUMENT:**

1. **Compute upper bound:** `tumblerincrement(account_addr, depth-1, 1)` where depth=2 (ACCOUNT→DOCUMENT). For account `1.1.0.2`, this yields `1.1.0.3` — the next sibling account.

2. **Query granfilade:** `findpreviousisagr` searches the granfilade tree for the highest existing address below `1.1.0.3`.

3. **Containment check:** After Bug 0013 fix [PRE-ADDRESS-ALLOC], the found address is verified to be under the target account via tumbler truncation+comparison. Without this, the search could cross account boundaries and produce addresses under the wrong account.

4. **Allocate:**
   - No documents under account yet → first child: `account_addr.0.1`
   - Existing documents present → truncate found address to document level, increment by 1

**Key properties from [SS-ADDRESS-SPACE] / Finding 0077:** There is no cached "next" counter. The allocation is a pure function of current granfilade state: `next_doc_addr(granf, account) = max_child(granf, account) + 1`. Multiple allocation sub-namespaces (document addresses vs. content I-addresses) are independent — they search different tumbler subtrees via `findpreviousisagr` with different bounds.

**Concrete:** Account `1.1.0.2`, existing document `1.1.0.2.0.1` → allocates `1.1.0.2.0.2`.

---

## Code Exploration

The actual source code is now confirmed. Here is the complete, verified answer:

---

## CREATEDOCUMENT → `findisatoinsertnonmolecule`: Full Trace

### Entry Point: `fns.c`

`createnewdocument()` [`fns.c:276–286`] calls `docreatenewdocument()` in `do1.c`.

### Document Hint Construction: `do1.c:234–241`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`makehint` sets `hint.supertype = ACCOUNT`, `hint.subtype = DOCUMENT`, `hint.hintisa = taskptr->account` (the caller's account tumbler — the `Node.0.User` address). The call chain continues to `createorglingranf` → `createorglgr` [`granf2.c:111–128`] → `findisatoinsertgr` [`granf2.c:130–156`].

### Router: `granf2.c:130–156`

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  bool isaexistsgr();

    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

Since `subtype = DOCUMENT ≠ ATOM`, execution falls through to `findisatoinsertnonmolecule`.

### Core Allocation: `granf2.c:203–242`

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;

    hintlength = tumblerlength (&hintptr->hintisa);

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);

    clear (&lowerbound, sizeof(lowerbound));

    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    /* BUG FIX #1: If nothing exists under the hint (lowerbound is zero after
       findpreviousisagr), create the first child address as hintisa.0.1.
       ...
       BUG FIX #2: Also check if lowerbound is actually under hintisa. ... */
    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr);
    }
}
```

Step by step, with `hint.supertype = ACCOUNT`, `hint.subtype = DOCUMENT`:

| Step | Expression | Effect |
|------|-----------|--------|
| **depth** | `ACCOUNT ≠ DOCUMENT` → `depth = 2` | Two tumbler levels down for document under account |
| **hintlength** | `tumblerlength(&hintptr->hintisa)` | Length of account address, e.g. 4 for `1.1.0.1` |
| **upperbound** | `tumblerincrement(hintisa, depth-1=1, 1)` | Next sibling account — the exclusive upper search bound |
| **granfilade query** | `findpreviousisagr(fullcrumptr, &upperbound, &lowerbound)` | **Traverses granfilade tree for the rightmost ISA less than `upperbound`** |
| **scope check** | Truncate `lowerbound` to `hintlength`, compare to `hintisa` | Verifies found ISA actually belongs under this account, not a different one |
| **first doc** | `iszerotumbler(&lowerbound) \|\| !lowerbound_under_hint` → `tumblerincrement(hintisa, depth=2, 1)` | No prior docs: returns `account.0.1` |
| **subsequent doc** | `tumblertruncate(lowerbound, hintlength+depth)` then `tumblerincrement(...)` | Truncates to document-level precision, then +1 |

### Granfilade Traversal: `granf2.c:255–278`

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{ RECURSIVE
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```

This recursively descends the enfilade tree, accumulating the running offset by adding each node's `cwid.WIDTH` until it finds the rightmost leaf whose range contains `upperbound`. At height 0, `findlastisaincbcgr` [`granf2.c:280–284`] returns the last ISA in that bottom-level block. The result in `lowerbound` is the **current maximum document address under the account**.

### The Old Kluge (now dead code): `granf2.c:183–201`

```c
static int klugefindisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
/*  typeisa upperbound, lowerbound;
  ...
    findpreviousisagr (fullcrumptr, &upperbound, &lowerbound);
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr,...,1,isaptr);
*/
    tumblercopy(&hintptr->hintisa,isaptr);
}
```

The kluge simply copied `hintisa` (the account address) straight into `isaptr` — no granfilade query at all. The comment in `findisatoinsertgr` [`granf2.c:144–151`] records why it was wrong: *"just copied hintisa unchanged, making the first document get the account address itself (1.1.0.1 instead of 1.1.0.1.0.1)."*

---

## Answer

**Yes**, but with precise qualification:

`findisatoinsertnonmolecule` [`granf2.c:203`] calls `findpreviousisagr` [`granf2.c:217`] to query the granfilade for the **current maximum document ISA** whose value falls below the next sibling account (the `upperbound`). That is the maximum document tumbler under the account's `Node.0.User` address. It then returns **max+1** via:

- **First document** (`lowerbound` is zero or not under this account): `tumblerincrement(hintisa, depth=2, 1)` → `account.0.1` [`granf2.c:237`]
- **Subsequent documents** (existing max found): truncate `lowerbound` to `hintlength + depth`, then `tumblerincrement` by 1 [`granf2.c:239–240`]

The `depth = 2` (because `ACCOUNT ≠ DOCUMENT` [`granf2.c:209`]) ensures each new document address is separated from the account address by the `.0.` tumbler spacer — making the first document `Node.0.User.0.1`, the second `Node.0.User.0.2`, and so on. The scope check at [`granf2.c:229–232`] guards against the edge case where `findpreviousisagr` returns a maximum from a *different* account (lower-numbered) that happens to fall under the same `upperbound`, which would otherwise cause documents to be allocated under the wrong account.
