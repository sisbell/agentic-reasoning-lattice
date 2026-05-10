## Question 12 [gregory]

> In `makehint`, what exact predicate determines whether the current session "owns" the source document — is it a tumbler prefix match between the session's account address and the document's I-address, or something else?

## KB Synthesis

The ownership predicate is a conjunction of two checks, not a single predicate:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

**`tumbleraccounteq(isaptr, wheretoputit)`** — yes, this is an account-level prefix match. `isaptr` is the source document's I-address; `wheretoputit` is the session's current account address. The function extracts and compares the account component of the document address against the session account. So it checks: does this document's address fall under the current session's account? [SS-VERSION-ADDRESS, Finding 0068]

**`isthisusersdocument(isaptr)`** — a secondary predicate confirming the document belongs to the current user. The KB doesn't detail its implementation, but it's applied conjunctively with the prefix match.

Both must be true for the "owned" path (`makehint(DOCUMENT, DOCUMENT, ...)` → version under source document). If either fails, the "unowned" path is taken (`makehint(ACCOUNT, DOCUMENT, ...)` → version under session's account). [ST-VERSION-OWNERSHIP]

The KB characterizes this as "account prefix matching, not an explicit permissions table" — the tumbler address hierarchy encodes ownership structurally. An explicit ACL table plays no role. [SS-TUMBLER-CONTAINMENT, ST-VERSION-OWNERSHIP]

One caveat: the KB notes `wheretoputit` in the code without fully specifying how the session's account address is materialized into that variable. It's reasonable to infer it's the session's currently-set account (from `SETACCOUNT`), but the KB doesn't confirm this at code level for the `wheretoputit` argument specifically.

---

## Code Exploration

I now have all the evidence needed. Here is the complete answer.

---

## Answer: The ownership predicate in `makehint`

### Short answer

`makehint` itself contains **no ownership test**. It is a pure structure initializer. The ownership predicate lives in the *callers* — specifically in `docreatenewversion` [`do1.c:270`] — and it is a **tumbler prefix match**, implemented by `tumbleraccounteq`. But the match is not a simple prefix: it is a match up to the point where the account tumbler's mantissa terminates (two consecutive zero slots), while the document's mantissa may continue freely beyond that boundary.

---

### `makehint` itself — `do2.c:78–84`

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`makehint` does exactly four things: writes three type integers into a `typehint` struct, then copies the ISA tumbler into `hintptr->hintisa` via `movetumbler`. There is no conditional, no comparison, no ownership check anywhere in the function body.

---

### Where the ownership decision actually lives — `do1.c:268–276`

The only caller that performs an ownership test before choosing which `makehint` call to make is `docreatenewversion`:

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The branch taken determines the `supertype` passed to `makehint`:

- **Own document** → `supertype = DOCUMENT, subtype = DOCUMENT` (version within the same document)  
- **Someone else's document** → `supertype = ACCOUNT, subtype = DOCUMENT` (new document under the session's own account)

The guard is a **conjunction of two predicates**:

1. `tumbleraccounteq(isaptr, wheretoputit)` — the source document and the target address are in the same account  
2. `isthisusersdocument(isaptr)` — the source document belongs to the current session's account

---

### The actual predicate: `tumbleraccounteq` — `tumble.c:38–70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    INT i, j_b;
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);   /* account terminated → doc is under this account */
            }
            /* first zero: skip mismatch check, doc may continue freely */
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:

1. Signs must match.
2. Walk both mantissa arrays in lockstep. The **account** tumbler (`bptr`) is treated as the pattern.
3. When `bptr->mantissa[i] != 0`: the document's mantissa must match exactly at that position — any mismatch returns `FALSE`.
4. When `bptr->mantissa[i] == 0`: this marks a "hole" in the account address. A **second** consecutive zero is the terminator — at that point we return `TRUE` regardless of what the document's mantissa holds beyond.
5. The first zero is not a terminator; the document is allowed to have any value there.

So the predicate is **not** a simple byte-by-byte prefix match. It is: _the document's tumbler shares all non-zero mantissa components with the account tumbler, up to the account's double-zero terminator_. This allows the tumbler encoding of hierarchical account address spaces where zeros are structural separators, not just padding.

---

### `isthisusersdocument` — the session binding

`isthisusersdocument` in the socket server (`socketbe.c:197–201`) is:

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

And in the standalone/batch backends (`be.c:171–175`, `xumain.c:198–200`):

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

Both delegate entirely to `tumbleraccounteq`. The `player[user].account` comment annotates a historical bug fix — a previous version used `n_players` (the count) instead of `user` (the current session index), which would have compared against the wrong account.

---

### Summary

The predicate determining whether the session "owns" the source document is:

> **`tumbleraccounteq(document_isa, session_account)`** — returns true iff the document's I-address tumbler begins with the same non-zero mantissa components as the session's account tumbler, continuing until the account tumbler's double-zero terminator is reached. The document may extend further; only the non-zero prefix of the account is required to match exactly.

It is not a plain prefix match on raw bytes. It is an account-aware prefix match that treats each zero in the account mantissa as a structural boundary marker, and requires a **second zero** to confirm termination before declaring the document belongs to the account.
