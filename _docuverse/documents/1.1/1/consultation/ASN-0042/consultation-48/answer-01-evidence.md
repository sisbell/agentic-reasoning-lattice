## Question 1 [evidence]

> In udanax-green, when a new account is admitted (via findpreviousisagr / the granfilade insertion path), is the account's tumbler always a fresh slot baptized in that same operation, or can an account be bound to an address that was previously baptized as a non-account sub-position under the parent's prefix?

## KB Synthesis

The KB is clear enough to answer this directly.

**Account addresses are always fresh — they cannot reuse a previously baptized sub-position.**

The allocation via `findisatoinsertnonmolecule` works by finding the highest existing address below the upper bound, then **truncating to account depth and incrementing** [SS-ADDRESS-ALLOC, Finding 0021]. This means:

1. The search for "next account under node `1.1`" may find a deep sub-address like `1.1.0.2.0.3.1` (a version under account 2, doc 3). That address is then **truncated** to account-level depth (`1.1.0.2`) and incremented to `1.1.0.3`.

2. Since all non-account entities (documents, versions, content atoms, link orgls) are allocated at **strictly greater depth** than account addresses — e.g., `1.1.0.2.0.1` for documents, `1.1.0.1.0.1.3.0.1.1` for content [SS-ADDRESS-SPACE, Finding 0077] — no entity has ever been allocated at the 4-digit account-level address `1.1.0.3` before it is assigned as an account.

3. [INV-MONOTONIC] and [INV-NO-IADDR-REUSE] guarantee the granfilade never reallocates any position.

The one failure mode was **Bug 0013** [PRE-ADDRESS-ALLOC, Finding 0021]: without the containment check, `findpreviousisagr` could return an address from a sibling account's namespace, causing the truncate+increment to land in the wrong account's prefix. The fix (verify the found address is under the target parent via `tumblertruncate`/`tumblereq`) restores the invariant.

So: new account = always fresh; re-baptism of a prior sub-position is structurally impossible given the depth hierarchy.

---

## Code Exploration

Now I have everything needed to give a complete, code-grounded answer.

---

## Answer

**The account's tumbler is always a fresh slot baptized in that same `insertseq` call. An account address cannot be bound to a previously baptized non-account sub-position.** The guarantee comes from the combination of `tumblertruncate`, `findpreviousisagr`, and the depth arithmetic. Here is the full trace.

---

### The Call Chain

**`fns.c:375–386` — `createnode_or_account`**

```c
void createnode_or_account(typetask *taskptr)
{
  tumbler t;
  bool getcreatenode_or_account(), docreatenode_or_account();

    if( getcreatenode_or_account(taskptr,&t)
         && docreatenode_or_account(taskptr,&t)) {
        putcreatenode_or_account(taskptr,&t);
```

**`get1fe.c:228–235` — `getcreatenode_or_account`**

```c
int getcreatenode_or_account(typetask *taskptr, tumbler *tp)
{
    ...
    gettumbler(taskptr,tp);
    return(TRUE);
}
```

The tumbler read from the FEBE stream is the **parent node's address** — the hint origin.

**`do1.c:243–258` — `docreatenode_or_account`**

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;
  ...
    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);   // write new address back out
    }
    return result;
}
```

`makehint(NODE=1, NODE=1, 0, ...)` sets `supertype=1`, `subtype=1`, `atomtype=0`, `hintisa=parent`. Note: `validhint` (`do2.c:86`) would call `gerror` on `subtype < ACCOUNT(2)`, but `validhint` is **never called** in this path — `createorglgr` calls `findisatoinsertgr` directly.

**`granf2.c:111–128` — `createorglgr`**

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);   // first baptism
```

`insertseq` is the actual baptism: it writes a `GRANORGL` crumb into the granfilade at `*isaptr`. The address in `*isaptr` was just computed by `findisatoinsertgr` — there is no prior entry at that address.

---

### Address Computation: `findisatoinsertgr` → `findisatoinsertnonmolecule`

**`granf2.c:130–156`**

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        ...
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        // NODE, ACCOUNT, DOCUMENT — all go here
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

`NODE ≠ ATOM`, so `findisatoinsertnonmolecule` is called.

**`granf2.c:203–242` — the slot computation**

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

For `NODE, NODE`: `supertype = subtype = 1` → **`depth = 1`**.

```c
    hintlength = tumblerlength (&hintptr->hintisa);

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
```

`depth-1 = 0`, so `tumblerincrement(hintisa, 0, 1)` — this adds 1 at position 0 (the most-significant slot), yielding the **next sibling** of the parent node. Everything strictly below `upperbound` and at-or-below `hintisa` is searched.

```c
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr` [granf2.c:255–278] traverses the granfilade enfilade and accumulates offsets, stopping at the leaf containing the highest crumb address strictly less than `upperbound`. The result `lowerbound` is the highest address actually baptized anywhere under the parent's subtree.

```c
    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        // Nothing under this hint — baptize first child
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
    }
```

The critical line is `tumblertruncate(&lowerbound, hintlength + depth, isaptr)`. With `depth=1`, this truncates to `hintlength + 1` — **exactly one component below the parent**. This is the direct-child level.

`tumblertruncate` [tumble.c:625–639] zeros all mantissa slots beyond position `bint`, then justifies. After the truncation, `*isaptr` holds the **highest occupied direct-child projection** of the parent. The subsequent `tumblerincrement` steps it forward by 1, yielding the **next unused direct-child slot**.

---

### Why No Previously-Baptized Non-Account Can Collide

The type hierarchy enforces strict depth segregation:

| Content type | Hint | `depth` | Address depth below parent |
|---|---|---|---|
| Account/node | `NODE, NODE` | 1 | `hintlength + 1` |
| Document | `ACCOUNT, DOCUMENT` | 2 | `hintlength + 2` |
| Text atoms | ATOM subtype | via `findisatoinsertmolecule` | deeper |
| Link atoms | ATOM subtype | via `findisatoinsertmolecule` | deeper |

A tumbler with `n` significant components cannot equal one with `m ≠ n` significant components. Accounts live at depth `hintlength + 1`; all other content lives at depth `≥ hintlength + 2`. These sets are structurally disjoint.

The `tumblertruncate` at [granf2.c:239] ensures this invariant: even if `findpreviousisagr` finds a deep descendant address (e.g., a document at `parent.0.3.0.1`), the truncation projects it back to depth 1 (`parent.0.3`), and the new account lands at `parent.0.4` — an address with no prior granfilade crumb.

---

### The One Subtle Effect

`findpreviousisagr` can discover deep descendants and cause a **slot to be silently skipped**. If documents exist at `parent.0.3.0.1` but no account crumb exists at `parent.0.3`, the truncation maps `lowerbound` to `parent.0.3`, and the new account goes to `parent.0.4`. Slot `parent.0.3` is "implied" by its children but was never itself baptized. The new account still lands at a fresh address (`parent.0.4`) — but in theory an account slot was burned. This cannot happen through normal operation (you can't create a document without first creating an account at depth 1), but the arithmetic would handle such a corrupt state by skipping rather than colliding.

---

### Summary

The new account's tumbler is **always baptized fresh in the `insertseq` call inside `createorglgr`** [granf2.c:125]. The address is computed by projecting the highest existing granfilade entry under the parent to depth `hintlength + 1` and incrementing. No prior crumb — account or non-account — exists at that exact address. The structural depth separation (`depth=1` for accounts vs `depth=2` for documents) makes collision between account addresses and previously-baptized non-account sub-positions arithmetically impossible under the tumbler representation.
