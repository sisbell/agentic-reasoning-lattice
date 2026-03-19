## Question 18 [gregory]

> In a multi-node topology, does ownership of a tumbler prefix on node `1.1` imply anything about that user's authority on node `1.2`, or is ownership strictly local to the node prefix — meaning the same human would have separate ownership roots on each node?

## KB Synthesis

The KB doesn't explicitly document multi-node ownership policy, but the structural mechanics make the answer clear: **ownership is strictly local to the node prefix**.

Here's the reasoning from the KB:

**Ownership is purely prefix-based.** [SS-TUMBLER-CONTAINMENT] defines the containment predicate as: truncate address A to the length of prefix B, compare for equality. `1.1.0.1.0.x` is under `1.1.0.1`. `1.2.0.1.0.x` is NOT under `1.1.0.1` — those address spaces are disjoint siblings under the docuverse root.

**The ownership check uses account prefix matching.** [SS-ADDRESS-SPACE] Finding 0068 shows that the ownership test is `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`. `tumbleraccounteq` compares the account-level components of two tumbler addresses. A user with session account `1.1.0.1` fails this test against any address rooted at `1.2.x`.

**Address allocation is namespace-bounded.** [SS-ADDRESS-ALLOC] Finding 0021 documents that `findisatoinsertnonmolecule` computes `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent — and searches only within that range. Document creation under account `1.1.0.1` is bounded to `[1.1.0.1, 1.1.0.2)`. Nothing in `1.2` is reachable.

**Version creation reinforces this.** [SS-VERSION-ADDRESS] Finding 0068: when a user versions a document they don't own, the version is allocated under `children(user.account)`, not under the document. This confirms the session account establishes the user's home namespace, and that namespace is their specific account address, not a broader node-level authority.

**Conclusion:** The same human would need independent account addresses on each node — `1.1.0.k` for node `1.1`, `1.2.0.k` for node `1.2`. There is no cross-node authority inheritance in the implementation. Ownership is per-account-prefix, and node prefixes (`1.1` vs `1.2`) are sibling subtrees with no containment relationship.

The KB does not document any higher-level policy mechanism (e.g., a node operator granting cross-node authority), so that question is unanswerable from the KB alone.

---

## Code Exploration

I now have everything needed for a precise answer. Here it is.

---

## Answer: Ownership is Strictly Local — No Cross-Node Authority Propagation

The code contains zero mechanism for cross-node authority. Ownership of a tumbler prefix on node `1.1` implies nothing about authority on node `1.2`. Here is the full chain of evidence.

---

### 1. The Tumbler Structure: A Flat Mantissa With No Node Layer

`common.h:59-65` defines the tumbler:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;
    short exp;
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

A tumbler is a 16-digit rational number. Conventional xanadu address notation like `1.1.0.1.0.1` maps directly onto `mantissa[0]=1, mantissa[1]=1, mantissa[2]=0, mantissa[3]=1, ...`. The digits at positions 0–1 (the "node" prefix `1.1`) are just leading digits in the mantissa — no special field, no special treatment. There is no struct member for "node" separate from the rest. The representation is uniform.

---

### 2. User Identity: One Account Tumbler Per Player

`players.h:13-21`:

```c
typedef struct _player {
    char    *name;
    INT      userid;
    INT      wantsout;
    INT      socket;
    FILE    *inp;
    FILE    *outp;
    tumbler  account;    /* xanadu host and account tumbler */
} PLAYER;
```

Every connected user has exactly one `account` tumbler. There is no per-node account table, no list of accounts, and no node-keyed map. A user is their account.

---

### 3. The Ownership Test: Pure Prefix Match on the Mantissa

The sole ownership predicate is `tumbleraccounteq()` in `tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    if (aptr->sign != bptr->sign) return(FALSE);

    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);   // account terminated; document is under it
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);
        }
    }
    return (TRUE);
}
```

The function asks: does document tumbler `aptr` begin with account prefix `bptr`? It scans digit by digit, stopping when `bptr` reaches its double-zero terminator. It has no knowledge of "node boundaries." It does not treat position 0 or 1 as special. A user whose account is `1.1.0.1.0.0` owns anything whose mantissa starts with `1,1,0,1` before the terminating zeros — and that test is applied uniformly whether the leading digits are `1.1` or `1.2` or anything else.

---

### 4. `isthisusersdocument()` — Three Implementations, Same Logic

In `socketbe.c:197-201` (multi-user daemon):

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

In `be.c:171-176` (single-process backend) and `xumain.c:198-201` (xumain variant):

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

All three compare the document against the **current session's single account tumbler**. No node lookup, no multi-node check, no delegation table.

---

### 5. How `checkforopen()` Uses Ownership — The Permission Gate

`bert.c:52-87` is the only place access is gated before a write operation:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
    // ...scan bert table for existing open by this connection...

    if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
        return 0;   // open allowed
    } else {
        return -1;  // must create a new version under your own account
    }
}
```

The permission logic is: you may write to a document if either (a) you are opening it for read, or (b) `isthisusersdocument()` returns true — i.e., your single account tumbler is a prefix of the document's address. There is no "same node" bonus, no "node admin" override, no cross-node delegation path.

---

### 6. What Happens When You Try to Write Another User's Document

`do1.c:268-276`:

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // same document address
} else {
    /* This does the right thing for new version of someone else's document */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // new doc under your account
}
```

If you do not own the target document, the system creates a **new document under your account** (`wheretoputit` is `taskptr->account`). It never escalates to ask whether you might own a parent node. The account mismatch path leads directly to `ACCOUNT`-scoped creation — a copy under your own space.

---

### 7. Node Creation Is Address Allocation, Not Authority Delegation

`do1.c:243-258`:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    tumblercopy(isaptr, &isa);
    makehint (NODE, NODE, 0, &isa, &hint);
    result = createorglingranf (taskptr, granf, &hint, &isa);
    // ...
}
```

`CREATENODE_OR_ACCOUNT` is a granfilade address allocation call — it registers a new numeric prefix in the enfilade so subsequent inserts know where to place content. It does **not** grant the creating user authority over that prefix. Authority still derives from whether your `account` tumbler is a prefix of the target document — not from who created the node address.

`granf2.c:224-227` makes this concrete with a bug fix comment:

```
BUG FIX #2: Also check if lowerbound is actually under hintisa. If the
found item is from a different account (e.g., 1.1.0.1.0.1 when creating
under 1.1.0.2), treat it as if nothing was found. Otherwise documents
get created under the wrong account.
```

Accounts `1.1.0.1` and `1.1.0.2` — both living under the `1.1` node — are treated as entirely distinct namespaces. The code treats any "bleed" across them as a bug to be eliminated.

---

### 8. No Multi-Node Networking Layer

`rcfile.c:19-32` shows the only network configuration the backend reads:

```c
#define HOSTMETANAME  "host"
// ...
char hostname[256] = "localhost";
```

`bed.c` runs a single `select()` loop over local socket file descriptors. There is no code for routing requests to remote nodes, no code for querying another node's ownership table, and no internode trust model.

---

## Conclusion

**Ownership in udanax-green is strictly local to the account tumbler prefix, not the node prefix.**

The ownership check is a single-function call — `tumbleraccounteq(document, user_account)` — which tests whether the user's account tumbler is a numeric prefix of the document's address. The node digits (e.g., `1.1` vs `1.2`) are not distinguished from any other digits in this comparison. There is no concept of "node administrator," no cross-node authority, and no federation of identity between nodes.

The same human would need **separate account tumblers** on each node — e.g., `1.1.0.1.0.0` on node `1.1` and `1.2.0.1.0.0` on node `1.2` — and those accounts have completely independent authority scopes. Ownership of everything under `1.1.0.1` says nothing about `1.2` because the permission check at `bert.c:81` is a pure prefix match against a single `account` field in the current session, with no cross-node lookup path in the code at all.
