## Question 11 [gregory]

> In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, is ownership a pure structural predicate — i.e., can the system determine "user U owns tumbler T" solely by comparing tumbler prefixes, without consulting any separate ownership table?

## KB Synthesis

Yes — ownership is a pure structural predicate. The KB gives enough evidence to conclude this firmly.

## The structural ownership mechanism

From [SS-TUMBLER-CONTAINMENT], the containment primitive is:

```
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);  // TRUE if A is under B
```

This is pure tumbler arithmetic. No table lookup, no side channel.

From [ST-VERSION-OWNERSHIP] / [SS-VERSION-ADDRESS] Finding 0068, the actual ownership check for VERSION is:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

where `wheretoputit` is the current session's account tumbler (stored in per-session state per [SS-SESSION-STATE]).

`tumbleraccounteq` compares the account-component of two tumblers — structural. `isthisusersdocument` checks whether the document falls under the session's account — also structural, given:

- The address hierarchy encodes the owner directly: `1.1.0.2` (account) → `1.1.0.2.0.1` (first doc under that account). [SS-ADDRESS-SPACE] Finding 0021
- Allocation itself is verified by containment check: after `findpreviousisagr`, the result is validated against the parent via prefix truncation. [PRE-ADDRESS-ALLOC]
- No ownership table exists anywhere in the KB — [SS-BERT] is an access-control table for *open sessions*, not an ownership registry

## What makes this work

Because documents are allocated under the owning account's tumbler prefix by construction ([ST-ADDRESS-ALLOC], [SS-ADDRESS-ALLOC]), ownership is encoded at allocation time and readable forever after by prefix comparison. The address space is the ownership table.

## The one caveat the KB leaves open

The internals of `isthisusersdocument` are not fully spelled out — the KB names it but doesn't expand it. However, given:
- No ownership table appears anywhere in the 78-finding KB
- All allocation, validation, and access control uses tumbler comparison or tree search
- The function name aligns with a simple prefix check against session account state

the structural interpretation is strongly supported. If `isthisusersdocument` did anything beyond tumbler prefix comparison, that would be a significant architectural departure that would appear in the KB.

**Answer:** Ownership is a pure structural predicate. `user U owns tumbler T` iff `tumbler_contains(U.account, T)`, implemented via `tumbleraccounteq` and related prefix operations — no separate ownership table exists or is consulted. [SS-TUMBLER-CONTAINMENT], [ST-VERSION-OWNERSHIP], [PRE-ADDRESS-ALLOC], [SS-SESSION-STATE]

---

## Code Exploration

I now have everything needed for a complete answer.

---

## Answer: Ownership Is a Pure Structural Predicate

**Yes.** In udanax-green, "user U owns document T" is determined entirely by comparing tumbler digits — no separate ownership table, registry, or persistent user-to-document mapping is consulted. The check reduces to a single function call on two tumblers.

---

### The Call Chain

**Entry point** — `bert.c:81`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

When a document is not already open by any connection with write access, the system falls through to `isthisusersdocument(tp)`.

---

### `isthisusersdocument` — Three Implementations, One Body

All three backend entry-point files implement the function identically:

**`be.c:171-176`** (single-user backend):
```c
int isthisusersdocument(tumbler *tp)
{
  bool result = tumbleraccounteq(tp, &taskptrx->account);
  return result;
}
```

**`socketbe.c:197-201`** (multi-user socket backend):
```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**`xumain.c:198-201`** (X-window backend):
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp,&taskptrx->account);
}
```

Every path leads to `tumbleraccounteq`. No table lookup, no file I/O, no external call.

---

### `tumbleraccounteq` — The Structural Predicate

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
  if (aptr->sign != bptr->sign) { return(FALSE); }

  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) {
        return(TRUE);  /* Account terminated, document is under this account */
      }
      /* First zero: document may continue to sub-address, skip mismatch check */
    } else {
      /* Account has non-zero: document must match exactly */
      if (aptr->mantissa[i] != bptr->mantissa[i]) {
        return(FALSE);
      }
    }
  }
  return (TRUE);
}
```

The comment at `tumble.c:53-59` is explicit about the semantics: the account tumbler is treated as a prefix pattern. Its non-zero digits must match the document tumbler exactly at the same positions; a pair of consecutive zeros terminates the account's address space, and whatever follows in the document tumbler doesn't matter. This is exactly the "prefix ownership" implied by the hierarchy `Node.0.User.0.Doc.0.Element`.

---

### `berttable` Is Not an Ownership Table

`bert.c:29`:
```c
static conscell *berttable[NUMBEROFBERTTABLE];
```

This is searched first in `checkforopen` (`bert.c:63-78`), but it is **not** an ownership registry. It is a session-scoped, in-memory hash table that tracks which documents are currently **open** by which connections and in what mode (READ/WRITE). Its contents are created by `addtoopen`, destroyed by `removefromopen` and `exitbert`, and never persisted to disk. It supports locking and copy-on-write versioning, not ownership.

---

### The Account Tumbler Is Self-Asserted

The account tumbler (the "U" side of the comparison) is obtained by reading from the network:

**`get1.c:190-203`** (`getxaccount`):
```c
gettumbler(taskptr, accountptr)
&& validaccount(taskptr, accountptr);
taskptr->account = *accountptr;
return(TRUE);
```

**`get2.c:157-160`** (`validaccount` — the only validation hook):
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

`validaccount` returns `TRUE` unconditionally in both implementations (`get2.c:157` and `get2fe.c:338`). No cross-check against any table or registry. The client asserts its own account tumbler and the backend accepts it.

In the single-user `be.c` backend, the account is not even negotiated — it defaults to a hardcoded tumbler (`be.c:37`):
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```
...and is copied directly into the task at `be.c:88`.

---

### Also Used in `docreatenewversion`

The same structural test appears in `do1.c:270`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    /* This does the right thing for new version of someone else's document */
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The comment labels this an "ownership test" explicitly. It is resolved purely by tumbler comparison, selecting how the new version's address is allocated in the granfilade.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Is ownership a pure structural predicate? | **Yes** | `isthisusersdocument` calls only `tumbleraccounteq` — no table |
| What is the predicate? | Prefix match: account's non-zero digits must match document at same positions; two zeros terminate account prefix | `tumble.c:38-70` |
| Is there any persistent ownership table? | **No** | `validaccount` returns `TRUE` unconditionally; `berttable` is session-local open-tracking only |
| How is the user's account tumbler established? | Client-asserted, read from wire by `gettumbler`, accepted without verification | `get1.c:190`, `get2.c:157`, `get2fe.c:338` |
| Is the `berttable` an ownership table? | **No** — it tracks open documents for locking/versioning | `bert.c:29`, `addtoopen`, `removefromopen` |

**The system determines "user U owns tumbler T" solely by asking: does the account tumbler U.account, treated as a prefix pattern, match T?** That is the complete ownership check. The tumbler hierarchy is the ownership hierarchy, and the predicate is computable by digit comparison alone.
