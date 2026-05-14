## Question 3 [evidence]

> In udanax-green, does the code at the zeros(t)=1 hierarchy level use "user", "account", or some other terminology (e.g., in `tumbleraccounteq`, baptism routines, identifiers)?

## KB Synthesis

The KB contains two relevant data points on this question.

**"Account" is the primary code-level term.** The `makehint` dispatch table uses `ACCOUNT` as a named constant for this hierarchy level [SS-ADDRESS-SPACE Finding 0021]:

| supertype | subtype | depth |
|-----------|---------|-------|
| `ACCOUNT` | `DOCUMENT` | 2 |

The function `tumbleraccounteq` also uses "account" in its name, and the per-session state is described as the "current account" [SS-SESSION-STATE Finding 0022].

**But "user" co-exists at the same level.** The ownership check in `docreatenewversion` explicitly pairs both terms [SS-VERSION-ADDRESS Finding 0068]:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

So `tumbleraccounteq` (account equality check) and `isthisusersdocument` (ownership predicate) operate on the same hierarchy level using different vocabulary. "Account" appears in structural/addressing functions; "user" appears in ownership/access predicates.

**The KB contains no information about baptism routines.** That term does not appear anywhere in the knowledge base, so I cannot answer that part of the question from the available evidence.

---

## Code Exploration

Here is the complete answer:

---

## Terminology at the zeros(t)=1 Hierarchy Level in udanax-green

The code uses **"account"** — consistently and exclusively — for the zeros(t)=1 hierarchy level. There is no "baptism" terminology anywhere in the backend source.

---

### 1. The `PLAYER` struct — where the level is stored

`backend/players.h:20`:
```c
tumbler account; 	/* xanadu host and account tumbler */
```

The field is named `account`. The comment makes the intent explicit: it holds the "xanadu host and account tumbler" — the zeros(t)=1 prefix that scopes all of a user's address space.

Alongside it, `players.h:15`:
```c
INT     userid;         /* player's user id number      */
```

This shows the distinction: `userid` is an integer index for the current *player* (session slot); `account` is the *tumbler* that identifies their address space.

---

### 2. The `typetask` struct

`backend/common.h:102`:
```c
tumbler account;
```

Every task carries a `tumbler account` field — the account tumbler that scopes all operations in the task.

---

### 3. The comparison function: `tumbleraccounteq`

`backend/tumble.c:38–69`:
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space.

       Key insight: When account has a zero, it marks the boundary of the
       account's address space. The document can have any value there
       (continuing to sub-addresses). We only check for exact match on
       non-zero account positions. */
    ...
            return(TRUE);  /* Account terminated, document is under this account */
    ...
}
```

The function tests whether a document tumbler falls under a given account tumbler — "under this account" is exactly the zeros(t)=1 prefix match.

---

### 4. The type constant

`backend/xanadu.h:140–142`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
```

`ACCOUNT` is the symbolic constant passed to `makehint()` when allocating a new address in an account's address space. Used at `do1.c:239`:
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

And the node/account creation path at `do1.c:251`:
```c
makehint (NODE, NODE, 0, &isa, &hint);
```

---

### 5. The FEBE protocol request codes

`backend/requests.h:41,45`:
```c
#define XACCOUNT 34
#define CREATENODE_OR_ACCOUNT 38
```

The wire protocol speaks "account" — `XACCOUNT` sets/gets the current account tumbler; `CREATENODE_OR_ACCOUNT` allocates a new node or account in the granfilade.

---

### 6. The FEBE handler functions

`backend/fns.c:364–382`:
```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}

void createnode_or_account(typetask *taskptr)
{
    ...
    if( getcreatenode_or_account(taskptr,&t)
         && docreatenode_or_account(taskptr,&t)) {
        putcreatenode_or_account(taskptr,&t);
    } ...
}
```

---

### 7. The default account value

`backend/be.c:37`:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

The default account is tumbler `1.1.0.1` — three non-zero mantissa positions followed by the double-zero terminator that `tumbleraccounteq` uses to detect the end of the account prefix.

`backend/socketbe.c:35`:
```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};
```

The socket backend uses `1.1.0.14` as its default account.

---

### 8. The account file

`backend/rcfile.c:23,35`:
```c
#define ACCOUNTFILEMETANAME      "accountfile"
...
char accountfilename[256] =   "accountfile";
```

Persistent account data is stored in a file literally named `accountfile` — the term is structural, not just a variable name.

---

### Summary

| Term | Role |
|------|------|
| `account` (tumbler) | The zeros(t)=1 prefix — address space identifier for a player |
| `ACCOUNT` (#define 2) | Type constant for `makehint()`, signals "allocate at account level" |
| `XACCOUNT` / `CREATENODE_OR_ACCOUNT` | FEBE protocol opcodes |
| `tumbleraccounteq()` | Prefix-match test: "does this document belong to this account?" |
| `user` (INT) | Session slot index (integer) — *not* a tumbler concept |

**No "baptism" terminology exists anywhere in the backend source.** The word "user" does appear, but only as an integer index into the `player[]` array — it identifies which connected session is active, not the tumbler hierarchy level. The zeros(t)=1 level is uniformly called **"account"** in every layer: struct fields, function names, protocol opcodes, file names, and comments.
