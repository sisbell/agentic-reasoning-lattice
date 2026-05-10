## Question 15 [gregory]

> Does the system distinguish between "owns this specific tumbler" and "has allocation rights under this tumbler prefix"? For example, can an account own document `1.1.0.2.0.5` without having the right to create `1.1.0.2.0.6`?

## KB Synthesis

The KB does not support such a distinction. The system conflates "owns this document" with "holds allocation rights under this account prefix" — they are the same predicate applied at different granularities.

**Account = allocation namespace.** New documents are allocated by `findisatoinsertnonmolecule` with the session's current account as the parent hint [SS-ADDRESS-ALLOC Finding 0021]. The algorithm finds the highest existing child under the account and increments it: if `1.1.0.2.0.5` exists, the next call allocates `1.1.0.2.0.6`. The right to do so flows entirely from the session's current account context, not from any per-document ownership claim.

**Ownership check is prefix-based, not registry-based.** `isthisusersdocument(isaptr)` is used to decide version-allocation strategy — "is the source document mine?" [SS-VERSION-ADDRESS Finding 0068]. This is implemented as `tumbleraccounteq(isaptr, wheretoputit)`: a tumbler-prefix comparison between the document's address and the session's account address. Any document whose address is contained under your account prefix passes this check. There is no separate per-document ownership registry.

**Consequence for your example.** If your session account is `1.1.0.2`, you pass `isthisusersdocument` for *any* document under `1.1.0.2`, and the allocation algorithm will allocate `1.1.0.2.0.6` the next time you create a document. There is no mechanism to hold `1.1.0.2.0.5` without implicitly holding allocation rights to all siblings under `1.1.0.2.0.*`.

**What BERT adds.** BERT [SS-BERT Finding 0014] provides per-document READ/WRITE access control, but this governs *mutation access* to existing documents, not the right to *create new siblings* under an account. A WRITEBERT token on `1.1.0.2.0.5` does not affect whether you can allocate `1.1.0.2.0.6`.

**KB gap.** The KB is silent on whether the bootstrap configuration or any higher-level protocol restricts account membership itself (i.e., preventing a session from calling `account(1.1.0.2)` if it doesn't "own" that account). The allocation and ownership machinery assumes the caller already has legitimate account access; it doesn't model how that access was granted.

---

## Code Exploration

I now have all I need to answer comprehensively.

---

## Answer: Ownership vs. Allocation Rights in udanax-green

**No. The system does not distinguish between "owns this specific tumbler" and "has allocation rights under this tumbler prefix." They are the same thing, implemented by a single predicate.**

---

### The Sole Ownership Predicate: `isthisusersdocument`

All three runtime implementations of `isthisusersdocument` reduce to one call:

- `be.c:173`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:200`: `return tumbleraccounteq(tp, &(player[user].account));`
- `xumain.c:199`: `return tumbleraccounteq(tp, &taskptrx->account);`

There is no separate "allocation rights" check. The same function gates both **access to existing documents** and **placement of new ones**.

---

### What `tumbleraccounteq` Actually Tests

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr = account tumbler (the "prefix")
    // aptr = document tumbler (the one being tested)
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  // Account terminated, document is under this account
            }
            // First zero: document may continue to sub-address. Skip check.
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

**This is a prefix match, not an exact match.** The account tumbler terminates when two consecutive zeros appear. Any document whose mantissa matches the account's non-zero digits up to that terminator is considered "owned" by that account. The document's mantissa may continue arbitrarily beyond that point.

So if your account tumbler represents `1.1.0.2`, then *both* `1.1.0.2.0.5` and `1.1.0.2.0.6` return TRUE — they are both "your documents" under identical logic.

---

### How Ownership Gates Access

`bert.c:52-87`, `checkforopen`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // document can be opened
} else {
    return -1;  // must create new version
}
```

The open-state table (`bert.c:37-50`) shows that for an unregistered document, `isthisusersdocument` is the deciding factor. If TRUE, you may open it. If FALSE and it's a write, you get `-1` (must create new version).

There is no additional "may create siblings" check at any level.

---

### How New Document Allocation Works

`do1.c:234-241`, `docreatenewdocument`:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

The hint's `hintisa` is `taskptr->account` — the current user's account tumbler. `granf2.c:203-241`, `findisatoinsertnonmolecule`, then searches for the **highest existing document under that prefix** and increments it:

```c
// If something already exists under hint prefix:
tumblertruncate(&lowerbound, hintlength + depth, isaptr);
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```

So `1.1.0.2.0.1`, `1.1.0.2.0.2`, ..., `1.1.0.2.0.5`, `1.1.0.2.0.6` are all sequentially allocated under the same account `1.1.0.2`. The counter is implicit in the enfilade — whatever already exists at that level, the next allocation increments past it.

---

### The `docreatenewversion` Branch

`do1.c:270-278`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);  // version under same doc prefix
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // new doc under account
}
```

Both conditions use `tumbleraccounteq` / `isthisusersdocument` — the same prefix test — to decide whether the new version falls under the existing document's sub-address space or under the account's top-level document space. No finer-grained authorization concept is consulted.

---

### Direct Answer to the Example

> Can an account own document `1.1.0.2.0.5` without having the right to create `1.1.0.2.0.6`?

**No.** Here is why:

If your account tumbler is `1.1.0.2`, then `tumbleraccounteq` returns TRUE for any document starting with `1.1.0.2`. You "own" all of `1.1.0.2.0.5` and `1.1.0.2.0.6` simultaneously. New document allocation calls `docreatenewdocument`, which pins the hint to `&taskptr->account` — so it always creates the next document in your entire account space, including at `.0.6`.

The only way to own `1.1.0.2.0.5` but *not* `1.1.0.2.0.6` would be if your account tumbler were `1.1.0.2.0.5` itself. In that case, `tumbleraccounteq(1.1.0.2.0.6, 1.1.0.2.0.5)` would return FALSE at the `5` vs `6` comparison. But then you also couldn't create `1.1.0.2.0.6` via `docreatenewdocument` — because the new document hint is your account prefix `1.1.0.2.0.5`, and new allocations go under *it* (e.g., `1.1.0.2.0.5.0.1`), not at the same level as it.

**The system has no concept of "leaf ownership without sibling allocation rights."** Ownership *is* a prefix, and a prefix defines both which existing objects you can open and where new objects are allocated. The two are inseparable.
