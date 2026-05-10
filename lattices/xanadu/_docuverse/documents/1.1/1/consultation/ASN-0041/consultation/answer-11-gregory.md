## Question 11 [gregory]

> Is ownership of a tumbler position determined structurally from the tumbler hierarchy (e.g., `1.1.0.2` is owned by whoever owns the `1.1.0.2` account prefix), or is there a separate ownership table or data structure that records who owns what?

## KB Synthesis

Ownership is determined **structurally from the tumbler hierarchy** — there is no separate ownership table.

The evidence is explicit in [ST-VERSION-OWNERSHIP] (Finding 0068):

> The ownership check uses `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`. **Ownership is determined by account prefix matching, not by an explicit permissions table.**

`tumbleraccounteq` compares the account component of two tumbler addresses — i.e., it checks whether the document's address prefix matches the current session's account address. The session's current account (set via the `account()` operation, isolated per-session per [FC-SESSION-ACCOUNT-ISOLATION]) establishes the ownership context for each operation.

Supporting structure from [SS-TUMBLER-CONTAINMENT]:

> Containment of address A under prefix B is checked by truncating A to the length of B and comparing for equality.

So `isthisusersdocument(isa)` amounts to: truncate the document's ISA to account-depth, compare against the current session's account address. If they match, the session owns it.

The BERT table ([SS-BERT]) is a related but distinct mechanism — it records `(connection, document) → access_level` during an open session, tracking read/write access control. BERT is session-scoped access control, not persistent ownership. The address hierarchy is ownership; BERT is current-access-state.

**Summary:** Ownership is a structural property — a document is owned by whoever's account address is a prefix of the document's address. The address hierarchy encodes ownership directly; no ownership registry exists.

---

## Code Exploration

I now have everything needed to answer the question fully.

---

## Ownership Is Purely Structural — Tumbler Prefix Matching

There is no separate ownership table. Ownership of a tumbler position is determined entirely by **structural prefix matching** between the document's tumbler and the current user's account tumbler.

---

### The Core Function: `tumbleraccounteq`

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  /* Compare until account (bptr) terminates with two zeros.
     Document (aptr) may continue beyond the account's address space. */
  for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
      if (++j_b == 2) {
        return(TRUE);  /* Account terminated, document is under this account */
      }
    } else {
      if (aptr->mantissa[i] != bptr->mantissa[i]) {
        return(FALSE);
      }
    }
  }
  return (TRUE);
}
```

**Algorithm**: Walk the account tumbler (the shorter one, `bptr`). For each non-zero digit, the document must match exactly. When the account's mantissa terminates with two consecutive zeros, the document is considered "under" that account prefix — regardless of what it has in those positions. A document like `1.1.0.2.3` is owned by account `1.1.0.2` because the two trailing zeros of the account signal the boundary.

---

### `isthisusersdocument` — Three Implementations, Same Logic

The ownership check is invoked as `isthisusersdocument(tp)` and all three backend variants delegate directly to `tumbleraccounteq`:

- `xumain.c:200`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:200`: `return tumbleraccounteq(tp, &(player[user].account));`
- `be.c:173`: `return tumbleraccounteq(tp, &taskptrx->account);`

No table lookup, no index, no registry. Pure arithmetic comparison.

---

### Where the Account Tumbler Comes From

The current user's account tumbler is **self-declared** by the client over the FEBE protocol:

`get1fe.c:213-225`:
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    gettumbler(taskptr, accountptr)
    && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The client sends an `XACCOUNT` message with its account tumbler. The server stores it in `player[user].account` (defined as `tumbler account` in `players.h:20`) and copies it into the active `task` struct at `bed.c:123`:

```c
task.account = player[user].account;
```

### `validaccount` Always Returns TRUE

`get2.c:157-160` and `get2fe.c:338-341`:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

There is **no server-side validation** of the claimed account. The server accepts whatever tumbler the client sends as its account identity.

---

### The Bert Table Is NOT an Ownership Table

`bert.c:29`:
```c
static conscell *berttable[NUMBEROFBERTTABLE];
```

The `berttable` hash table (1327 buckets) tracks **open documents** (active read/write locks per connection), not ownership. Each `bertentry` records `{connection, documentid, type, count}`. It answers "is this document open by this connection?" — not "does this connection own this address space?"

---

### The Ownership Decision Path in `checkforopen`

`bert.c:81`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

When no bert entry exists for a document and no other connection has it open for write, the fallback is `isthisusersdocument(tp)` — which is pure tumbler prefix matching against `task.account`. That's the entire ownership model.

---

### Summary

Ownership is **entirely structural**: a document tumbler is owned by whoever's account tumbler is a prefix of it, as computed by `tumbleraccounteq`. There is no ownership registry, no ownership table, no server-side mapping. The account tumbler is self-reported by the client via the `XACCOUNT` FEBE message, and `validaccount` accepts it unconditionally. The granfilade (`granf`) tracks document addresses, and the bert open-table tracks session locks — but neither serves as an ownership ledger. Ownership falls directly out of the tumbler's numeric structure.
