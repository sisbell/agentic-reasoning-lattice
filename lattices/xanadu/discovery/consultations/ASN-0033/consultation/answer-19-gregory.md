## Question 19 [gregory]

> What is the structural relationship between a node tumbler and the account tumblers it contains — does the system enforce that account `N.0.A` can only allocate documents under `N.0.A.0.D`, or is the nesting purely conventional with no backend check preventing an account from writing outside its node's prefix?

## KB Synthesis

The relationship is enforced algorithmically within the allocation function, but there is no authorization layer preventing a session from claiming arbitrary account prefixes.

**What the allocation algorithm enforces**

Address allocation in `findisatoinsertnonmolecule` takes the session's current account tumbler as a hint and bounds the search explicitly. The post-Bug 0013 fix adds a containment check: after `findpreviousisagr` finds the highest existing address below the upper bound, the code verifies the result is actually under the target parent via tumbler truncation/comparison (`tumblertruncate` + `tumblereq`). Without this, the allocator crossed account boundaries — it would find `1.1.0.1.0.1` when allocating under `1.1.0.2`, increment it, and produce `1.1.0.1.0.2` (under the wrong account). [PRE-ADDRESS-ALLOC], [INV-ACCOUNT-ISOLATION]

The `.0.` hierarchy is encoded as a depth parameter to `makehint`. The NODE→NODE case uses depth=1 (no `.0.` crossing), while ACCOUNT→DOCUMENT uses depth=2 (crosses one `.0.` boundary). This is what produces `1.1.0.2.0.1` under account `1.1.0.2` rather than `1.1.0.2.1`. [SS-ADDRESS-SPACE] Finding 0021

**What is not enforced**

The session freely declares its current account via a SET_ACCOUNT call. Per-session state is isolated — each session has its own `current_account` — but there is no cross-session authorization check that a session is *permitted* to use a particular account prefix. Session A can set account `1.1.0.1` and session B can set the same account with no conflict; they each allocate sequentially under that namespace. [SS-SESSION-STATE], [FC-SESSION-ACCOUNT-ISOLATION]

The BERT system governs document-level read/write access once a document exists, but it does not gate account namespace selection. [SS-BERT], [PRE-OPEN-DOC]

**Summary**

- Account→document nesting is structurally enforced by the allocation algorithm's containment check — the backend prevents a document from being created outside the hint account's address subtree
- But account selection itself is self-declared by the session; any session can claim any account prefix
- The node→account hierarchy (e.g., node `1.1` containing account `1.1.0.2`) follows the same `.0.` separator convention and the same containment predicate, but is equally unguarded at the session-claim level

The invariant `INV-ACCOUNT-ISOLATION` holds only because well-behaved sessions use the correct account hint — the backend confirmed it requires explicit maintenance, not automatic enforcement from the flat storage structure. [INV-ACCOUNT-ISOLATION]

---

## Code Exploration

Now I have everything I need. Here is my full answer.

---

## Structural Relationship Between Node Tumblers and Account Tumblers

The short answer: **The nesting is real but only partially enforced. The backend checks that documents fall within a declared account prefix (via `tumbleraccounteq`), but it does NOT verify that the declared account tumbler itself falls within the connected node's prefix. `validaccount` is a stub that accepts any tumbler unconditionally.**

---

### 1. The Tumbler Hierarchy (`xanadu.h:140-143`)

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

The intended structure is hierarchical: node ⊃ account ⊃ document ⊃ atom, with zero-delimited tumbler digits at each level. An account `N.0.A` is supposed to live under node `N`, and a document `N.0.A.0.D` is supposed to live under that account.

---

### 2. The Ownership Function: `tumbleraccounteq` (`tumble.c:38-70`)

This is the only real structural enforcement in the system. It checks whether a document tumbler `aptr` falls within an account prefix `bptr`:

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
            /* First zero — document can have any value at this position */
        } else {
            /* Non-zero — document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The logic: scan both mantissas in parallel. Whenever the account has a non-zero digit, the document must match exactly. Zeros in the account are level-separators — the **first** zero is skipped (the document may have any digit at that position, including sub-addressing), but the **second** zero terminates the account prefix and returns `TRUE`. For account `N.0.A` (mantissa `[N, 0, A, 0, 0, ...]`):

- Position 0: account=`N`, document must equal `N`
- Position 1: account=`0` → first zero, skip match check
- Position 2: account=`A`, document must equal `A`
- Position 3: account=`0` → second zero → `return TRUE`

So a document `N.0.A.0.D` (mantissa `[N, 0, A, 0, D, ...]`) would pass, and `N.0.B.0.D` would fail at position 2.

---

### 3. `isthisusersdocument` — All Three Implementations Are Identical

`isthisusersdocument` is the caller of `tumbleraccounteq`. All three build variants do the same thing:

- `be.c:171-176`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `socketbe.c:197-201`: `return tumbleraccounteq(tp, &(player[user].account));`
- `xumain.c:198-201`: `return tumbleraccounteq(tp, &taskptrx->account);`

This function answers: "Does this document tumbler fall within the current session's declared account prefix?"

---

### 4. Where Ownership Is Checked (`bert.c:81`)

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;   /* can open without being in bert table */
} else {
    return -1;
}
```

If no conflicting open exists AND the document falls under the user's declared account, it can be opened for writing without entering the BERT table. This is the gating check that uses `tumbleraccounteq`.

Also at `do1.c:270`, in `docreatenewversion`:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

The ownership check determines whether a new version is created as a sibling of the original (if the user owns it) or as a fresh document under their account (if they don't).

---

### 5. Document Allocation Uses the Declared Account (`do1.c:234-241`)

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
  return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`createorglingranf` → `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203-242`) places the new document at `hintisa.0.N` — that is, `taskptr->account.0.N`, the next available document slot under the declared account. This is real structural placement: documents are genuinely allocated under the account prefix in the granfilade.

---

### 6. The Critical Gap: `validaccount` Is a Stub

The account tumbler itself is set by the `XACCOUNT` protocol command. In `fns.c:364-373`:

```c
void xaccount(typetask *taskptr) {
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```

`getxaccount` in `get1.c:190-204` reads a tumbler from the wire then calls `validaccount`:

```c
gettumbler (taskptr, accountptr)
&& validaccount(taskptr, accountptr);
taskptr->account = *accountptr;
return(TRUE);
```

And `validaccount` in **both** `get2.c:157-160` and `get2fe.c:338-341`:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

**No validation is performed.** Any tumbler sent by the client is accepted as a valid account. There is no check that `N.0.A` shares the node prefix `N` with the node the client is connected to, no check that the account exists in the granfilade, no check of any kind.

---

### Summary

| Enforcement | Mechanism | Where | Result |
|---|---|---|---|
| Document → Account prefix | `tumbleraccounteq` | `bert.c:81`, `do1.c:270` | **Enforced** |
| Account → Node prefix | `validaccount` | `get2.c:157`, `get2fe.c:338` | **Not enforced — stub returns TRUE** |
| Document allocation under account | `makehint(ACCOUNT, DOCUMENT, ...)` | `do1.c:239` | Correct by construction if account is valid |
| Account validity | `validaccount` | `get1.c:200`, `get1fe.c:222` | **Not enforced — stub returns TRUE** |

**The backend enforces that documents fall under a declared account prefix** (via `tumbleraccounteq`). It does **not** enforce that the declared account falls under the node the client is attached to. A client could send `XACCOUNT 9.0.7` while connected to node `1`, and the backend would accept `9.0.7` as the account, allocate all documents under `9.0.7.0.*`, and the ownership checks would use `9.0.7` as the trust anchor. The node-to-account nesting is entirely conventional — there is no backend check preventing an account from writing outside its node's prefix.
