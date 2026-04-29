## Question 13 [gregory]

> `makehint` (do2.c:78-84) branches version allocation based on whether the caller "owns" the source document — what exact comparison does it perform to determine ownership, and at which level of the tumbler hierarchy does it match (node, user, or document prefix)?

## KB Synthesis

The KB has this directly, across two findings.

**The comparison (`do1.c:272-280`):**

```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

Both conditions must be true for the "owned" path to fire. [SS-VERSION-ADDRESS, Finding 0068]

**What each check does:**

`tumbleraccounteq(isaptr, wheretoputit)` compares at the **account (user) level** — the prefix up to the first `.0.` boundary. For a document at `1.1.0.1.0.1`, the account field is `1.1.0.1`. It asks: does the source document's account prefix match `wheretoputit` (the current session's account)? [ST-VERSION-OWNERSHIP]

`isthisusersdocument(isaptr)` then verifies the document is actually registered under the current session's user, not merely address-compatible. The two checks together close the gap between "structurally under my account" and "actually mine."

**The hierarchy level:**

Account level — one `.0.` boundary deep. From the address table [SS-ADDRESS-SPACE, Finding 0021]:

| Address | Level |
|---------|-------|
| `1.1.0.1` | account |
| `1.1.0.1.0.1` | document under that account |
| `1.1.0.1.0.1.1` | version (child of document) |

The comparison truncates to the account prefix (depth-2 field), not the document prefix. This is why cross-user versioning falls through to the `ACCOUNT` path in `makehint`: if User B (account `1.1.0.2`) tries to version User A's document `1.1.0.1.0.1`, `tumbleraccounteq` sees `1.1.0.1 ≠ 1.1.0.2` and the owned-path condition fails. The version is then allocated under User B's account (`1.1.0.2.0.1`) via `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` with depth=2 — same as a fresh document creation. [SS-VERSION-ADDRESS, Finding 0068; ST-VERSION-OWNERSHIP]

---

## Code Exploration

---

## Answer

`makehint` at `do2.c:78-84` is itself a **pure setter** — it performs no comparison. The ownership branch happens in its caller, `docreatenewversion`, immediately before the two `makehint` calls.

---

### The branch site — `do1.c:268-276`

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

Two conditions must both be true for the "owned" path:

1. **`tumbleraccounteq(isaptr, wheretoputit)`** — source document and destination share the same account prefix
2. **`isthisusersdocument(isaptr)`** — source document belongs to the current user's account

---

### `isthisusersdocument` — `socketbe.c:197-201`

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

It delegates entirely to `tumbleraccounteq`, comparing the document tumbler `tp` against the current user's account tumbler `player[user].account`. (There's a bug note in the comment — the original code used `n_players` instead of `user`, which was wrong.) Identical implementations also appear in `be.c:171-176` and `xumain.c:198-201` for different build targets.

---

### The actual comparison — `tumble.c:38-70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }
    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero in account - skip mismatch check */
        } else {
            /* Account has non-zero - document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm:
- Iterates mantissa slots left to right
- For each **non-zero** slot in the account tumbler (`bptr`): the document tumbler (`aptr`) must match exactly — **or return FALSE**
- A zero in the account tumbler means "end of this component" — it is skipped without requiring a match
- When **two consecutive zeros** appear in the account tumbler, the account address has terminated → return TRUE (the document lives beneath this account prefix, regardless of what follows)

---

### What hierarchy level does it match?

The match operates at the **ACCOUNT prefix level** — specifically the account component of the tumbler, which ends at the double-zero terminator. The document tumbler can have arbitrary content beyond that boundary (VERSION, DOCUMENT, sub-address components). Only the account portion must agree.

The first call in the condition — `tumbleraccounteq(isaptr, wheretoputit)` — checks that both the source document and the caller-supplied destination share the same account prefix (i.e., same "owner account"). The second call inside `isthisusersdocument` checks that prefix against `player[user].account`, the currently-authenticated user's own account tumbler.

---

### What each branch does

| Condition | `makehint` call | Effect |
|---|---|---|
| Both true: same account, user owns it | `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` | Allocate new version within the existing document's address space — a true versioning operation |
| Either false: different account, or user doesn't own source | `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` | Allocate a fresh document under the account — mirrors `docreatenewdocument` [`do1.c:239`] |

The asymmetry in the hint type (`DOCUMENT,DOCUMENT` vs `ACCOUNT,DOCUMENT`) controls how `createorglingranf` routes the address allocation — either threading into an existing document's granfilade node or creating a new root entry under the account.
