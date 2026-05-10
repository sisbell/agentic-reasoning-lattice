## Question 8 [gregory]

> Must baptism at a child level (e.g., `1.1.0.2`) be preceded by baptism of the parent position (`1.1`) — is there a strict hierarchical prerequisite chain?

## KB Synthesis

Based on the KB, the allocation algorithm does **not** enforce a strict hierarchical prerequisite chain where each ancestor must be formally registered before a child can be created. Here is what the evidence supports:

## How Address Allocation Actually Works

The allocation algorithm (`findisatoinsertnonmolecule`, [SS-ADDRESS-ALLOC] Finding 0021) takes the intended parent address as a **boundary hint**, not as a required existing entry:

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent
2. Call `findpreviousisagr` to find the highest address in the **existing** granfilade tree below that bound
3. If nothing is found under the parent: allocate first child as `parent.0.1`
4. If something is found: truncate and increment to produce the next sibling

The critical point: `findpreviousisagr` searches the existing tree for entries in the bounded range. If no entries exist under `1.1` yet, the search returns nothing and `1.1.0.1` is allocated as the first child — without requiring `1.1` to itself be present as a granfilade entry.

## What Bug 0013 Reveals

The containment-check fix documented in [PRE-ADDRESS-ALLOC] Finding 0021 shows the algorithm operates purely on **tumbler arithmetic and tree search**, not on ancestor existence:

> When allocating under account `1.1.0.2`, the search found `1.1.0.1.0.1` (under a different account) and incorrectly incremented from it, producing `1.1.0.1.0.2`.

The bug was in *cross-boundary* search, not in missing-ancestor detection. The fix adds a prefix-match check on the *found* candidate — it does not add any check that the parent address exists.

## Implicit Dependencies That Do Exist

The KB does document *some* prerequisites, but they are operational rather than structural:

- **Session account context** ([SS-SESSION-STATE] Finding 0022): To allocate under an account, your session must have that account set. This is access control, not a granfilade-existence check.
- **Source document existence for VERSION** ([ST-VERSION-OWNERSHIP] Finding 0068): `docreatenewversion` calls `findorgl` on the source document, which does require the document to exist as an open orgl. But this is because you are *copying* from it, not merely naming it as a parent.
- **Ownership check for VERSION** ([SS-VERSION-ADDRESS] Finding 0068): The `tumbleraccounteq && isthisusersdocument` check determines allocation path (child-of-doc vs. child-of-account), but failure does not reject the operation — it redirects to a different parent.

## What the KB Does Not Address

The KB has no findings that document:
- A formal "account creation" or "node registration" operation that would constitute baptism of a parent address
- Any check in `findisatoinsertnonmolecule` or `findisatoinsertmolecule` that verifies ancestor existence
- Any notion of an address being "invalid" simply because its parent has no granfilade entry

## Summary

The allocation mechanism is **tolerant of unregistered ancestors**. Allocating `1.1.0.2` requires only that the session context names `1.1` as the intended parent — not that `1.1` appears as an entry in the granfilade. The tree search simply finds no existing children and allocates `1.1.0.1` as the first, with no error or prerequisite check. A strict hierarchical prerequisite chain of baptisms is **not required** by the implementation as documented in the KB.

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Does Child-Level Baptism Require Prior Parent Baptism?

The word "baptism" does not appear in the udanax-green source. The concept maps to **granfilade entry creation** — the moment an entity receives a permanent tumbler address in the granfilade tree. The answer is: **it depends on the type of entity being created, and the check is asymmetric.**

---

### The Two Allocation Paths

All baptism flows through `findisatoinsertgr` in `granf2.c:130-156`, which branches immediately on whether the new entity is an ATOM (content: text or links) or a structural entity (DOCUMENT, ACCOUNT, NODE):

```c
// granf2.c:135-153
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        fprintf (stderr,"nothing at hintisa for atom\n");
        return (FALSE);                           // HARD GATE: parent doc must exist
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr); // NO parent check
}
```

**ATOM path** (content insertion): `isaexistsgr` is called on `hintptr->hintisa` — the owning document's address. If that document is not registered in the granfilade, the call returns `FALSE` immediately. **The parent must exist.**

**Non-ATOM path** (document/account/node creation): `findisatoinsertnonmolecule` is called with no such check. The parent address in `hintptr->hintisa` is used purely as an **arithmetic anchor** for computing the child's address — it is never verified to exist.

---

### How `findisatoinsertnonmolecule` Allocates Without a Parent Check

`granf2.c:203-242`:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

// BUG FIX #2: lowerbound must be under hintisa, not from another account
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr); // → hintisa.0.1
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

For an `ACCOUNT→DOCUMENT` creation (depth=2) with `hintisa = 1.1`:
- `upperbound = tumblerincrement(1.1, 1, 1)` = `1.1.1` (the search ceiling)
- `findpreviousisagr` finds the largest granfilade entry strictly below `1.1.1`
- If nothing is under `1.1` (i.e., `1.1` itself has never been registered), BUG FIX #2 catches it and produces: `tumblerincrement(1.1, 2, 1)` = `1.1.0.1`
- On the second call: the existing `1.1.0.1` is found → result is `1.1.0.2`

The BUG FIX #2 comment [granf2.c:224-226] is explicit about this scenario:
> "Also check if lowerbound is actually under hintisa. If the found item is from a different account (e.g., 1.1.0.1.0.1 when creating under 1.1.0.2), treat it as if nothing was found."

This confirms `1.1.0.2` is treated as an account address in this codebase, and the system explicitly handles the case where nothing yet exists under it — without ever requiring `1.1.0.2` to be pre-registered.

---

### The `makehint` Setup: No Existence Validation

`makehint` at `do2.c:78-84` simply copies the hint's tumbler fields:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);   // just copies, no existence check
}
```

`validhint` [do2.c:86-108] validates the *type* fields (e.g., subtype must be ≥ supertype, difference ≤ 1), but never queries the granfilade for the `hintisa` address.

---

### Three Creation Functions and What They Require

**`docreatenewdocument`** [do1.c:234-241]:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```
Hint: `hintisa = taskptr->account`. No check that the account exists in the granfilade.

**`docreatenode_or_account`** [do1.c:243-258]:
```c
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
```
Hint: `hintisa = isa` (client-supplied address). No check that the parent node exists. `depth = 1` (NODE→NODE).

**`docreatenewversion`** [do1.c:260-299]:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // hintisa = source doc
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint); // hintisa = target account
}
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) return FALSE;  // ← implicit gate
```

Here there IS an implicit dependency: `doretrievedocvspanfoo` calls `findorgl` [granf1.c:17-41], which calls `checkforopen` [bert.c:52-87]. The **source document must be open in BERT** or the operation fails. But this is a gate on the *source document being open*, not on any ancestor being baptized.

---

### `isthisusersdocument` and `tumbleraccounteq`

`xumain.c:198-201`:
```c
int isthisusersdocument(tumbler *tp) {
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

`tumbleraccounteq` [tumble.c:38-70] checks whether `tp` (a document address) **falls within** the account's address space by comparing the account's non-zero mantissa positions. This is a **namespace containment check**, not a "parent is registered" check. The account address is just a prefix that defines ownership semantics.

---

### Conclusion

**No, there is no strict hierarchical prerequisite chain for structural entity baptism (documents, accounts, nodes).** The granfilade allocation logic in `findisatoinsertnonmolecule` [granf2.c:203-242] treats the parent's hint address purely arithmetically — it is never verified to exist via `isaexistsgr`. BUG FIX #2 specifically hardens this against the case where the parent position is empty: if nothing has been allocated under the hint yet, the allocator computes `hintisa.0.1` directly.

**There IS a prerequisite chain for content (ATOM) insertion** [granf2.c:135-140]: inserting text or links requires the owning document to already exist in the granfilade (`isaexistsgr` is called and returns `FALSE` if it does not). This means the practical FEBE sequence — create account → create document → insert content — does impose ordering, but only at the ATOM level, and it is the document (not its parent account) that must pre-exist.

The baptism of `1.1.0.2` (an account address) requires only that you invoke `docreatenode_or_account` or a similar creation function with `hintisa = 1.1` and the right type flags. Whether `1.1` itself has previously been baptized is irrelevant to the granfilade allocator.
