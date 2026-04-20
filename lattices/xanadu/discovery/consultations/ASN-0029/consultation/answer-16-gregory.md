## Question 16 [gregory]

> Can a user create a document under another user's account range (e.g., user `1.1.0.2` creating doc `1.1.0.3.0.5`), or does the backend enforce that document allocation stays within the creating user's own account subtree?

## KB Synthesis

The KB does not contain a finding that directly tests cross-account document creation (e.g., session with current account `1.1.0.2` attempting to allocate under `1.1.0.3`). But the architectural evidence across several entries points clearly to: **no, the backend does not enforce account ownership at allocation time.**

## What the KB says

**Account is session-local state, set by command.**
[SS-SESSION-STATE] describes `account` as per-session state. Any session can call `account(X)` for any `X`. There is no documented authentication or authorization check on that call.

**The allocation algorithm follows the hint, not the user.**
[SS-ADDRESS-ALLOC] / [PRE-ADDRESS-ALLOC] (Finding 0021): `findisatoinsertnonmolecule` takes a hint ISA derived from `makehint(ACCOUNT, DOCUMENT, ...)`. The hint is the *current session account* (`wheretoputit`). Bug 0013's fix added a *containment check* — after finding the candidate address, verify it is under the target parent. This check ensures correctness of placement within the specified account, not that the session is authorized to use that account.

**BERT is advisory, not enforced.**
[INT-BERT-FEBE] and [EC-RESPONSE-BEFORE-CHECK] (Finding 0050): The BERT access-control machinery is a cooperative protocol between front end and back end. For mutations, the back end sends the success response *before* executing the operation. A non-compliant front end can perform mutations on any document regardless of BERT state. The KB explicitly states: "system_correct ↔ (backend_correct ∧ all_frontends_compliant)."

**The subspace and account conventions are caller-enforced throughout.**
[INV-ACCOUNT-ISOLATION] (Finding 0021) is stated as an invariant maintained by the allocation algorithm, not by authorization logic. [INV-SUBSPACE-CONVENTION] is similarly caller-enforced with no runtime check. The pattern is consistent: the back end trusts the front end.

## Synthesis

If a session calls `account(1.1.0.3)`, the hint ISA becomes `1.1.0.3`, and the allocation algorithm will correctly place the new document at `1.1.0.3.0.1` (or the next available child). No check verifies that the session "belongs to" account `1.1.0.3`. The containment fix from Bug 0013 ensures the allocation is *internally correct* (the new address is genuinely under the specified account), but this is a correctness property of the allocator, not an access control gate.

The KB does not provide a golden test confirming this behavior, so the above is strong architectural inference rather than direct observation. If this matters for spec, a finding explicitly testing cross-account allocation would be needed to confirm.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Answer: No Enforcement — Account Boundaries Are Not Checked

The backend does **not** enforce that a user creates documents within their own account subtree. The claim can be verified by tracing the full execution path from the `createnewdocument` request through to address allocation.

---

### Call Chain: `createnewdocument`

**`fns.c:276-286`**
```c
void createnewdocument(typetask *taskptr)
{
    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
    ...
}
```

`getcreatenewdocument()` takes **no parameters from the wire** — it is an empty stub in both `get1.c:158-160` and `get1fe.c:132`. The document address is never requested from the client here; it is derived entirely from `taskptr->account`.

**`do1.c:234-241`**
```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

The new document is allocated **as a child of `taskptr->account`** — whatever that is. The `hint` with `supertype=ACCOUNT`, `subtype=DOCUMENT` tells `findisatoinsertnonmolecule` (`granf2.c:203-242`) to find the next free slot under that account tumbler.

---

### How `taskptr->account` Is Populated

**`bed.c:123`**
```c
task.account = player[user].account;
```

Every time a request is dispatched, `task.account` is loaded from `player[user].account`. That field is set by the `XACCOUNT` command.

**`fns.c:364-373`**
```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr,&(player[user].account))) {
        putxaccount(taskptr);
    }
    ...
}
```

**`get1fe.c:213-225`** (and identically `get1.c:190-203`)
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    gettumbler (taskptr, accountptr)
    && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The client sends **any tumbler it wants** over the wire. `validaccount` is called, but:

**`get2.c:157-160`** (and `get2fe.c:338-341`)
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

**`validaccount` is a stub that unconditionally returns `TRUE`.** No check is made against the current user's identity. The supplied account tumbler is accepted as-is and stored into `player[user].account`.

---

### The `isthisusersdocument` Check — Only Used for BERT Open State, Not Creation

`isthisusersdocument` appears in two places:

**`bert.c:81`**
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

**`do1.c:270`**
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Both versions of `isthisusersdocument` compare a document's address against the current `player[user].account`:

**`socketbe.c:197-201`**
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**`be.c:171-176`**
```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

But since `player[user].account` was set from the **user-supplied** `XACCOUNT` payload — with no validation — the "this user's document" check is trivially bypassed. Set `account = 1.1.0.2` via `XACCOUNT`, and `isthisusersdocument` will return true for all documents under `1.1.0.2`.

---

### `tumbleraccounteq` — What "Ownership" Means

**`tumble.c:38-70`**
```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // Returns true if aptr's address falls under bptr's account subtree
    // by matching all non-zero positions of bptr against aptr
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);  // Account terminated
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);
        }
    }
    return (TRUE);
}
```

This is a correct prefix-match — but it only enforces the check against `player[user].account`, which the user controls.

---

### Conclusion

**A user can create documents under any account subtree.** The mechanism that should prevent this — `validaccount` — is an **unconditional stub** (`return TRUE`) in every compilation path (`get2.c:157`, `get2fe.c:338`). Since `XACCOUNT` accepts any tumbler and stores it as the user's account, a client sending `XACCOUNT 1.1.0.2` followed by `createnewdocument` will allocate a document at e.g. `1.1.0.2.0.1` — inside user `1.1.0.2`'s address space — regardless of who is actually connected.

The access-control infrastructure (`checkforopen`, `isthisusersdocument`, `tumbleraccounteq`) is architecturally correct in design but operates entirely against the user-supplied, unvalidated account tumbler, making it ineffective as a security boundary.
