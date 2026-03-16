## Question 12 [gregory]

> How is a user's tumbler range initially established on a node — does the node allocate a `Node.0.User` prefix via the same `findisatoinsertnonmolecule` max+1 mechanism used for documents, or is there a separate user-provisioning path?

## KB Synthesis

The KB does not contain findings that document the user-provisioning path directly. Here is what can be inferred, and where the gap is.

## What the KB documents

The `findisatoinsertnonmolecule` mechanism is described for two cases [SS-ADDRESS-SPACE, Finding 0021]:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |
| DOCUMENT | DOCUMENT | 1 | Version under document |

The depth formula is `depth = (supertype == subtype) ? 1 : 2`. The mechanism itself is stateless query-and-increment: compute upper bound from parent address, find the highest existing child via `findpreviousisagr`, increment by 1 [SS-ADDRESS-ALLOC, Finding 0021].

The `makehint` table in the KB shows no `NODE | ACCOUNT` entry — the case that would govern allocating a user's account address (`1.1.0.2`) under a node (`1.1`).

## What can be inferred (not confirmed)

By structural analogy, a `NODE | ACCOUNT` allocation would use depth=2 (different types), which crosses one `.0.` boundary — consistent with the address form `Node.0.User` (e.g., `1.1.0.2`). This would use the same `findisatoinsertnonmolecule` machinery with a hint of type `(NODE, ACCOUNT)`.

However, user provisioning may involve a separate administrative path entirely — not a runtime `findisatoinsertnonmolecule` call triggered by the FEBE protocol, but a bootstrapping or configuration step. The KB contains no findings that observe account creation in action, and no finding covers `init.c` or startup provisioning logic beyond `createenf` for the empty enfilade.

## The honest answer

**The KB cannot answer this question.** The mechanism for establishing `Node.0.User` ranges is outside the scope of findings 0001–0078. To answer definitively, you would need to examine `init.c`, the bootstrap document setup, and any administrative FEBE opcodes that are absent from the current finding set.

---

## Code Exploration

---

## Answer: How User Tumbler Ranges Are Established

**The short answer: there is no server-side user provisioning path.** The backend does not allocate user account tumblers via `findisatoinsertnonmolecule` or any other allocation mechanism. The client asserts its own account tumbler, and the backend stores it unconditionally.

---

### The Provisioning Path (or lack thereof)

#### Step 1 — Process startup: account is zeroed

At startup, `xumain.c:49` calls:

```c
getaccount(&task, &task.account);
```

`getaccount()` in `task.c:28-41` is:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  tumblerclear (accountptr);
  return (TRUE);
  /* gettumbler / validaccount was commented out */
}
```

The active code is just `tumblerclear(accountptr)` — the account starts as a zero tumbler. The original interactive-prompt code (`gettumbler` / `validaccount`) is commented out [`task.c:37-40`].

---

#### Step 2 — Client sends XACCOUNT: backend accepts unconditionally

The actual account is set when the client sends an `XACCOUNT` FEBE request. The handler in `fns.c:364-373`:

```c
void xaccount(typetask *taskptr)
{
  bool getxaccount();
  if (getxaccount(taskptr, &(player[user].account))) {
      putxaccount(taskptr);
  } else {
      putrequestfailed(taskptr);
  }
}
```

`getxaccount()` in `get1fe.c:213-226`:

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  logstuff = TRUE;
  if (interfaceinput)
      fprintf(interfaceinput, "%d~", XACCOUNT);

  gettumbler(taskptr, accountptr)          // read client-supplied tumbler
  && validaccount(taskptr, accountptr);    // return value DISCARDED
  player[user].account = *accountptr;      // store it unconditionally
  taskptr->account = *accountptr;
  return(TRUE);                            // always succeeds
}
```

Key observations:
- `gettumbler` reads whatever tumbler the client sends over the wire.
- The `&&` expression with `validaccount()` is **a statement whose return value is discarded** — the result is not captured in any variable.
- `player[user].account = *accountptr` is assigned regardless.
- The function returns `TRUE` unconditionally.

`validaccount()` in `get2fe.c:338-341` is itself a complete stub:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

No validation occurs.

---

#### What `createnode_or_account` actually does

The FEBE handler `createnode_or_account` (`fns.c:375-386`) calls `docreatenode_or_account` (`do1.c:243-258`):

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;
  tumblercopy(isaptr, &isa);
  makehint(NODE, NODE, 0, &isa, &hint);   // NODE under NODE
  result = createorglingranf(taskptr, granf, &hint, &isa);
  if (result) tumblercopy(&isa, isaptr);
  return result;
}
```

This does invoke `findisatoinsertnonmolecule` — but only for allocating a **NODE under a NODE**. The depth parameter for `NODE→NODE` is `1` (same supertype/subtype, `granf2.c:209`), so the child address is `hint.0.1`, `hint.0.2`, etc.

Critically: there is no `makehint(NODE, ACCOUNT, ...)` anywhere in the codebase. There is no path that allocates an ACCOUNT address via the max+1 mechanism. The "or_account" in the function name appears to be vestigial — the implementation only creates NODEs.

---

### How `findisatoinsertnonmolecule` *is* used (for comparison)

For documents, `docreatenewdocument` (`do1.c:234-241`) uses:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

`depth = 2` (ACCOUNT ≠ DOCUMENT), so the first document under account `1.1.0.1` becomes `1.1.0.1.0.1`, the second `1.1.0.1.0.2`, etc. This is the allocation mechanism the question references — but it **only runs after the account tumbler is already established by the client**.

---

### Summary

| Mechanism | What it allocates | Who drives it |
|---|---|---|
| `findisatoinsertnonmolecule` (depth=2) | DOCUMENT under ACCOUNT | Backend, from client's pre-asserted account |
| `findisatoinsertnonmolecule` (depth=1) | NODE under NODE | Backend, from client-supplied parent hint |
| `XACCOUNT` request path | Account tumbler | **Client asserts its own identity** |
| `validaccount()` | Nothing — stub returning TRUE | No-op |

**The user's account tumbler is entirely client-provided.** The node (server) does not allocate a `Node.0.User` prefix via any mechanism. There is no user-provisioning path — whoever the client claims to be (via `XACCOUNT`), the server believes them. The `findisatoinsertnonmolecule` max+1 mechanism only runs *within* the context of an already-asserted account to allocate documents and structural nodes beneath it.
