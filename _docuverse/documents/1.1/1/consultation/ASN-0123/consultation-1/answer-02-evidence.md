## Question 2 [evidence]

> Do udanax-green's document- and version-creation paths enforce that every new document tumbler lies under an existing account (e.g., session or account checks at creation), or is there any code path that can create a document not covered by an account?

## KB Synthesis

## Document/Version Creation and Account Enforcement

The KB gives a clear picture, though it reveals a gap between containment enforcement and account legitimacy enforcement.

---

### Document Creation

The allocation uses the session's current account address as the parent hint, with depth=2 (`ACCOUNT → DOCUMENT`). From [SS-ADDRESS-ALLOC] and [PRE-ADDRESS-ALLOC] (Finding 0021):

- `findisatoinsertnonmolecule` computes an upper bound as the next sibling of the parent account, then calls `findpreviousisagr` to find the highest existing address below that bound.
- **Bug 0013** revealed that without a containment check, the search can cross account boundaries — allocating `1.1.0.1.0.2` when the intent was to allocate under `1.1.0.2`. The fix adds a prefix-match check via `tumblertruncate` + `tumblereq` to verify the candidate is actually under the intended parent.

This containment check enforces that the *allocated address* lands under the *session's configured account*. It does **not** validate that the configured account address corresponds to any registered or existing entity in the granfilade. The session's account context is set by the front end via an `account()` call, and the backend trusts it.

---

### Version Creation

Version allocation has an ownership-sensitive split ([SS-VERSION-ADDRESS], [ST-VERSION-OWNERSHIP], Finding 0068):

```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

- **Owned document**: version allocated as a child of the source document (`depth=1`, e.g., `1.1.0.1.0.1.1`)
- **Unowned document**: version allocated under `wheretoputit` — the creating session's configured account (`depth=2`, same as CREATE)

In the unowned case, the allocation falls back to the same account-relative path as document creation, with the same containment guarantee and the same absence of account-legitimacy validation.

---

### What Is and Is Not Enforced

| Property | Enforced? | Mechanism |
|---|---|---|
| New document address is under session's configured account | **Yes** | Containment check (`tumblertruncate` + `tumblereq`), Bug 0013 fix [PRE-ADDRESS-ALLOC] |
| Allocated address is strictly greater than all existing siblings | **Yes** | Monotonic query-and-increment [INV-MONOTONIC] |
| Session's configured account address corresponds to an existing/registered account | **No** | Not described in KB |
| Cross-account pollution at allocation time | **Yes (post-Bug-0013)** | The containment check prevents the allocator from wandering into a sibling account's namespace [PRE-ADDRESS-ALLOC] |

The allocation is entirely stateless with respect to account registration: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1`. The algorithm queries the granfilade tree for the current maximum child under the parent and increments — it has no concept of an "account registry" to validate against [SS-ADDRESS-SPACE], [SS-ADDRESS-ALLOC] (Finding 0077).

---

### Implication

There is no backend enforcement that the account tumbler the session uses was legitimately allocated. A non-compliant front-end that sets an arbitrary tumbler as its account via `account(some_tumbler)` and then calls `create_document` would receive a document allocated under `some_tumbler.0.1`, with the containment check satisfied. The BERT layer ([SS-BERT], Finding 0014) covers access to *existing* documents, not the legitimacy of account addresses used at creation time. The [INT-BERT-FEBE] entry (Finding 0050) confirms that the backend treats the FEBE contract as a cooperative protocol, not an enforced gate.

In short: the creation paths enforce *intra-account containment* rigorously, but account *existence* or *ownership* is a front-end responsibility that the backend does not verify.

---

## Code Exploration

I now have all the code I need. Here is my complete answer.

---

## Account Enforcement on Document and Version Creation in udanax-green

### Short answer

There is **no meaningful enforcement**. The account under which a new document is created is controlled entirely by a client-supplied tumbler, and the one validation hook (`validaccount`) is a stub that always returns `TRUE`. Multiple code paths can produce documents that are not covered by any real account node.

---

## Path 1 — `CREATENEWDOCUMENT`

**Call chain:**

```
fns.c:276  createnewdocument(taskptr)
  get1.c:158  getcreatenewdocument()         ← empty function, reads nothing
  do1.c:234  docreatenewdocument(taskptr, &newdocisa)
    do2.c:78   makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)
    granf1.c:50  createorglingranf(taskptr, granf, &hint, isaptr)
      granf2.c:111  createorglgr(...)
        granf2.c:130  findisatoinsertgr(...)   ← allocates next ISA under hintisa
```

The document's tumbler is allocated directly under `taskptr->account` [`do1.c:239`]:

```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

So the question becomes: **who controls `taskptr->account`?**

---

## Where `taskptr->account` comes from

### Single-user backend (`be.c`)

At startup, `be.c:37` declares:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```
and `be.c:88` sets it:
```c
movetumbler(&defaultaccount, &task.account);
```

This is the only initialization. The FEBE `XACCOUNT` command can change it at any time.

### Multi-user daemon (`socketbe.c`)

In `socketbe.c:110–114`, when a new connection arrives:
```c
if (!establishprotocol(taskptr->inp, taskptr->outp)) {
    break;
}
//getxaccount(taskptr, &(player[*n_playersp].account));
//logaccount(&(player[*n_playersp].account));
```

The `getxaccount` call is **commented out**. `player[n].account` is never initialized for new connections. Until the client sends `XACCOUNT`, `taskptr->account` contains whatever was in the allocated struct memory — effectively zero or garbage. Any `CREATENEWDOCUMENT` before `XACCOUNT` creates a document under a zero tumbler.

### `XACCOUNT` sets the account unconditionally

The FEBE handler is `fns.c:364–373`:
```c
void xaccount(typetask *taskptr)
{
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```

`getxaccount` is `get1.c:190–204`:
```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();

     gettumbler (taskptr, accountptr)
  && validaccount(taskptr, accountptr);   // ← result is DISCARDED
   taskptr->account = *accountptr;        // ← executes unconditionally
   fprintf(stderr,"in get xaccount \n");
   return(TRUE);                          // ← always succeeds
}
```

The expression on lines 199–200 is a statement whose value is thrown away. Even if `validaccount` returned FALSE, nothing would stop the assignment on line 201 or the unconditional `return(TRUE)` on line 203. A client can send any tumbler as its account — real, fictional, or another user's document ISA.

`validaccount` itself is `get2.c:157–160`:
```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return(TRUE);
}
```

It is a stub. No check is made that the tumbler refers to an existing account node in the granfilade.

---

## Path 2 — `CREATENEWVERSION`

**Call chain:**

```
fns.c:289  createnewversion(taskptr)
  get1.c:76  getcreatenewversion(taskptr, &originaldocisa)  ← reads doc ISA from client
  do1.c:260  docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

The critical branch in `do1.c:270–276`:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Because `fns.c:296` passes **the same pointer for both `isaptr` and `wheretoputit`**:
```c
docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

`tumbleraccounteq(isaptr, wheretoputit)` compares the tumbler to itself and always returns `TRUE`. So the branch is decided entirely by `isthisusersdocument`.

`isthisusersdocument` (`be.c:171–176`):
```c
int isthisusersdocument(tumbler *tp)
{
  bool result = tumbleraccounteq(tp, &taskptrx->account);
  return result;
}
```

This checks whether the document ISA starts with `taskptrx->account` — the same account that `XACCOUNT` can set to anything.

**When the check fails (original doc belongs to a different account):**

```c
makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
```

Here `wheretoputit` points to `originaldocisa` — the original document's ISA, not an account ISA. `createorglingranf` treats this as if it were an account and allocates the new version two tumbler-levels below the original document's own address. The new document is placed outside the current session's account entirely.

**Contrast with the `bert.c` (open-mode) path:**

`doopen` in `bert.c:274,290,296` correctly passes `&taskptr->account` as `wheretoputit`:
```c
docreatenewversion(taskptr, tp, &taskptr->account, newtp);
```

That path does anchor versions under the session's account. The FEBE `CREATENEWVERSION` command does not.

---

## Summary of enforcement gaps

| Gap | Location | Effect |
|-----|----------|--------|
| `validaccount` is a no-op stub | `get2.c:157–160` | Any tumbler accepted as a valid account |
| `getxaccount` discards validation result | `get1.c:199–201` | Assignment and success are unconditional |
| `player[n].account` never initialized on connection | `socketbe.c:114` (commented out) | First `CREATENEWDOCUMENT` in daemon mode uses uninitialized account |
| `CREATENEWVERSION` passes the document ISA as `wheretoputit` | `fns.c:296`, `do1.c:275` | New version of another user's document is placed outside the current session's account |
| `inittask` does not initialize `account` | `task.c:24` (commented out) | No safe default in code path that misses `be.c`'s startup init |

There is no point in either the `CREATENEWDOCUMENT` or `CREATENEWVERSION` path where the backend verifies that the target account actually exists as a node in the granfilade. The account tumbler is used directly as a hint to the address allocator (`findisatoinsertnonmolecule`, `granf2.c:203`), which will happily allocate an address rooted there whether or not any account node was ever created at that parent ISA.
