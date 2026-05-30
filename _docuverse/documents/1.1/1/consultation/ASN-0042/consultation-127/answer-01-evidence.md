## Question 1 [evidence]

> Does udanax-green contain any mechanism that selects the longest matching account prefix among multiple covering principals, or does ownership resolution stop at the binary `tumbleraccounteq` containment check with no longest-match arbitration anywhere?

## KB Synthesis

The KB contains no evidence of any longest-match arbitration. Ownership resolution is a single binary decision.

The only ownership check in the system appears in VERSION allocation [SS-VERSION-ADDRESS, Finding 0068]:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

This is a binary predicate — either the document's address falls under the current user's account prefix, or it doesn't. [ST-VERSION-OWNERSHIP] confirms: "ownership is determined by account prefix matching, not by an explicit permissions table." There are exactly two paths: `allocate_under(doc)` if owned, `allocate_under(user.account)` if not.

The underlying containment primitive [SS-TUMBLER-CONTAINMENT] is equally binary:

```c
tumblertruncate(&A, tumblerlength(&B), &truncated);
tumblereq(&truncated, &B);  // TRUE or FALSE, no ordering among candidates
```

The KB describes no concept of "multiple covering principals." There is no principal list, no candidate ranking, no longest-prefix selection loop anywhere in the ownership or allocation paths. The system models one current account per session [SS-SESSION-STATE], so the question of arbitrating among multiple covering principals simply never arises architecturally — there is only ever one account context to check against.

---

## Code Exploration

I now have everything needed for a complete answer.

---

## Answer

**udanax-green contains no longest-match arbitration. Ownership resolution is a single binary `tumbleraccounteq` call against one account and stops there.**

---

### The full call chain

#### 1. Entry point: `checkforopen` — `bert.c:52–87`

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  …
  for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) {   // exact equality, not prefix
      …
    }
  }

  if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {  // bert.c:81
    return 0;
  } else {
    return -1;
  }
}
```

The bert-table loop uses `tumblereq` (exact equality) to find already-open sessions. If no open session is found for this document, the fallback at `bert.c:81` is a single call to `isthisusersdocument`.

---

#### 2. `isthisusersdocument` — three backend variants, all identical in shape

**`socketbe.c:197–201`** (socket backend):
```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**`be.c:171–176`** (embedded backend):
```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

**`xumain.c:198–201`** (main backend):
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &taskptrx->account);
}
```

Every variant: one call, one account. No loop, no candidate list.

---

#### 3. `tumbleraccounteq` — `tumble.c:38–70`

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
  INT i, j_b;
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  // account terminated — document is under this account
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

This is a prefix-containment predicate: it returns TRUE if the document tumbler `aptr` falls within the account address space of `bptr`. The "double-zero" rule identifies where the account prefix ends. It is capable of testing containment at different prefix depths — but it is **always called with exactly one account**, so there is no comparison of specificity between multiple candidates.

---

#### 4. One account per connection — `players.h:13–21`

```c
typedef struct _player {
    char    *name;
    INT     userid;
    INT     wantsout;
    INT     socket;
    FILE    *inp;
    FILE    *outp;
    tumbler account;     // one tumbler per player
} PLAYER;
```

The `PLAYER` struct carries exactly **one** `tumbler account`. There is no array of principals, no ACL, no group-membership list. The system architecture presupposes one account per connection.

---

#### 5. `docreatenewversion` — `do1.c:268–276`

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The one other call site for `tumbleraccounteq` — still a binary test against a single account, not a multi-principal selection.

---

### Conclusion

There is **no longest-match arbitration anywhere in udanax-green**. The ownership resolution path is:

```
checkforopen (bert.c:63–79)   — exact tumblereq match on open sessions
    ↓ (no hit)
isthisusersdocument (bert.c:81)
    ↓
tumbleraccounteq(tp, single_account)   — binary yes/no
```

`tumbleraccounteq` implements what *could* be the query half of a longest-match algorithm — it tests whether a document falls within an account's prefix. But it is never called in a loop over multiple candidate accounts and never returns a match-length score. It is a pure binary predicate, invoked once against the single account of the currently connected user. No code in the codebase iterates over a set of principals and selects the most specific covering match.
