## Question 11 [gregory]

> When a brand-new document is created (not via CREATENEWVERSION), how is its document-level tumbler address allocated — does `findisatoinsertnonmolecule` walk the granfilade under the user's account range (e.g., `1.1.0.2`) to find max+1, or is there a separate document counter?

## KB Synthesis

## Document Address Allocation for CREATEDOCUMENT

The answer is: **`findisatoinsertnonmolecule` walks the granfilade tree under the account's address range to find max+1. There is no separate document counter.**

### Mechanism

[SS-ADDRESS-ALLOC Finding 0021] describes the algorithm directly:

1. `makehint(ACCOUNT, DOCUMENT, 0, account_isa, &hint)` sets `depth=2` (encoding the `.0.` boundary between account and document)
2. `upperbound = tumblerincrement(account_isa, depth-1=1, 1)` — produces the next sibling of the account (e.g., `1.1.0.3` for account `1.1.0.2`)
3. `findpreviousisagr` traverses the granfilade tree to find the highest existing address **below** that upper bound
4. A containment check (added after Bug 0013) verifies the found address is actually under the target account prefix
5. If no child exists: allocate first child at `account_isa.0.1` (e.g., `1.1.0.2.0.1`)
6. If a child exists: truncate to the appropriate length and increment (e.g., `1.1.0.2.0.1` → `1.1.0.2.0.2`)

### No Separate Counter

[SS-ADDRESS-SPACE Finding 0077] makes this explicit:

> "There is no single global 'next' counter (no Σ.next). Instead, allocation is a family of independent functions partitioned by tumbler range: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1`"

[SS-ADDRESS-SPACE Finding 0061] confirms: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

The same `findisatoinsertnonmolecule` path handles CREATE, VERSION, and all non-content address allocation — distinguished only by what hint (`ACCOUNT→DOCUMENT` vs `DOCUMENT→DOCUMENT`) is passed. The granfilade tree itself is the implicit counter.

The [INV-GLOBAL-ADDRESS-UNIQUENESS] observation that addresses are globally unique across sessions is an emergent consequence of this scheme: all sessions query the same shared granfilade tree, so each call sees the current maximum and allocates above it.

---

## Code Exploration

I have traced the full call chain. Here is the complete answer.

---

## How brand-new document tumbler addresses are allocated

**Short answer:** There is no separate document counter. `findisatoinsertnonmolecule` performs a live walk of the granfilade via `findpreviousisagr` to find the current maximum document address under the user's account, then returns `max + 1`. The granfilade *is* the counter.

---

### Call chain (traced from the protocol handler down)

**1. Entry: `docreatenewdocument`** — `do1.c:234–241`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`makehint` (`do2.c:78–83`) fills `hint.supertype = ACCOUNT(2)`, `hint.subtype = DOCUMENT(3)`, `hint.atomtype = 0`, and copies `taskptr->account` into `hint.hintisa`. The hint carries the user's account address — e.g. `1.1.0.2` — as the anchor for searching.

No counter is read or written here.

---

**2. `createorglingranf` → `createorglgr`** — `granf1.c:50–55`, `granf2.c:111–128`

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    ...
}
```

`findisatoinsertgr` is called first — it fills `*isaptr` with the new address. Only then is the node inserted. No counter is consulted before or after.

---

**3. `findisatoinsertgr` dispatches on `subtype`** — `granf2.c:130–156`

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
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

`subtype = DOCUMENT(3)` ≠ `ATOM(4)`, so the path goes to `findisatoinsertnonmolecule`. The comment in `granf2.c:144–152` confirms this handles `DOCUMENT`, `ACCOUNT`, and `NODE` types.

---

**4. The allocation engine: `findisatoinsertnonmolecule`** — `granf2.c:203–242`

This is the complete function:

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

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - create first child as hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
    }
}
```

Step by step for account `A = 1.1.0.2` (`hintlength = 4` stories, `depth = 2` because `ACCOUNT ≠ DOCUMENT`):

- **`upperbound`** = `tumblerincrement(A, depth-1=1, 1)` → `A.0.1` = `1.1.0.2.0.1`. This is a strict upper bound for the search: "find me the last document address below `1.1.0.2.0.1`."
- **`findpreviousisagr(granf, upperbound, &lowerbound)`** — walks the granfilade tree recursively (see below) to find the highest existing ISA < `upperbound` under this account.
- **If nothing found** (`lowerbound` is zero or not under `A`): `tumblerincrement(A, depth=2, 1)` → `mantissa[idx+2] += 1` where `idx=3` (the `2` in `1.1.0.2`) → result is `1.1.0.2.0.1`. That is the first document.
- **If something found** (e.g. previous doc = `1.1.0.2.0.3`): truncate lowerbound to `hintlength + depth = 6` stories → still `1.1.0.2.0.3`, then `tumblerincrement(isa, 0, 1)` increments the last component → `1.1.0.2.0.4`.

---

**5. The granfilade walk: `findpreviousisagr`** — `granf2.c:255–278`

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
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

This is a recursive descent through the granfilade enfilade tree. It accumulates `offset` by summing crum widths leftward, then descends into the rightmost subtree that could contain the answer. At height 0 (a leaf), `findlastisaincbcgr` (`granf2.c:280–284`) reads the actual last ISA from the bottom crum. The result is the highest address stored in the granfilade that is less than `upperbound`. There is no counter — the tree *is* the authoritative source.

---

### No counter exists

Checking `init.c` confirms that initialization (`init.c:25–79`) sets up only a dispatch table (`requestfns[]`). No document counter is initialized, stored, or consulted anywhere in the code. The granfilade serves as both the storage structure and the canonical record of what addresses have been allocated. Each `CREATENEWDOCUMENT` call reads the current maximum from the tree and returns `max + 1`.

---

### Summary

| Stage | File | What happens |
|-------|------|--------------|
| `docreatenewdocument` | `do1.c:234–241` | Constructs hint `(supertype=ACCOUNT, subtype=DOCUMENT, hintisa=account_addr)` |
| `createorglgr` | `granf2.c:111–128` | Calls `findisatoinsertgr` to get address, then inserts into granfilade |
| `findisatoinsertgr` | `granf2.c:130–156` | Routes to `findisatoinsertnonmolecule` because `subtype ≠ ATOM` |
| `findisatoinsertnonmolecule` | `granf2.c:203–242` | Computes `upperbound`, calls `findpreviousisagr`, returns `max+1` (or first child) |
| `findpreviousisagr` | `granf2.c:255–278` | Recursive granfilade tree walk — finds the highest existing ISA below `upperbound` |

The `depth = 2` value (because `ACCOUNT ≠ DOCUMENT`) means the document address is exactly 2 mantissa-stories deeper than the account address, producing the `.0.N` suffix: account `1.1.0.2` → documents `1.1.0.2.0.1`, `1.1.0.2.0.2`, etc., each produced by incrementing the granfilade's own maximum.
