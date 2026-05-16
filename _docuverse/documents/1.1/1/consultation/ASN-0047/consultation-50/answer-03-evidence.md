## Question 3 [evidence]

> Does udanax-green provide any account- or node-level analog of `docreatenewversion` (do1.c:271) — i.e., does any FEBE/BEBE operation produce account-shaped or node-shaped addresses via depth-1 tumbler extension from an existing account or node address?

## KB Synthesis

Based on the KB, **no** — there is no documented account-level or node-level analog of `docreatenewversion`.

**What the KB does establish about depth-1 extension:**

`makehint` encodes these depth rules [SS-ADDRESS-ALLOC, Finding 0021]:

| supertype | subtype | depth | meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | node under node |
| ACCOUNT | DOCUMENT | 2 | document under account |
| DOCUMENT | DOCUMENT | 1 | version under document |

So the allocation *mechanism* (`findisatoinsertnonmolecule`) is generic and can produce NODE→NODE or DOCUMENT→DOCUMENT children. The depth-1 path for NODE→NODE does exist in the allocation code.

**Why no account/node VERSION analog is documented:**

`docreatenewversion` [ST-VERSION-CREATE, Finding 0032] does three things atomically: allocate a child address, retrieve the source vspan, and copy content via `docopyinternal`. The KB records no FEBE opcode that does the equivalent for account or node addresses — no "copy this account's structure and branch it as a child" operation. The only versioning opcode documented is CREATENEWVERSION (opcode 13), which is document-scoped only [SS-VERSION-ADDRESS, Finding 0068].

**The NODE→NODE depth-1 path** is used for allocation of sibling nodes in the address hierarchy (e.g., `1.1.0.1.1`, `1.1.0.1.2`), but this is standard `CREATEDOCUMENT`-style allocation, not a copy-and-branch version operation [SS-ADDRESS-SPACE, Finding 0021].

The KB does not contain findings about any FEBE/BEBE opcode that produces account- or node-shaped addresses by depth-1 extension from an *existing* account or node in a VERSION-like (content-copying) sense. If such an operation exists in the implementation, it is outside the scope of what has been extracted.

---

## Code Exploration

I now have everything I need. Here is the complete answer.

---

## Does udanax-green have an account- or node-level analog of `docreatenewversion`?

### How `docreatenewversion` allocates via depth-1 extension

`docreatenewversion` [do1.c:260-299] calls:
```c
makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);   /* [do1.c:271] */
```
when the document is owned by the calling user, or:
```c
makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  /* [do1.c:275] */
```
for a foreign document.

`makehint` [do2.c:78-84] is simple — it just stores `supertype`, `subtype`, `atomtype`, and the hint address into `typehint`:
```c
hintptr->supertype = typeabove;
hintptr->subtype   = typebelow;
...
movetumbler (isaptr, &hintptr->hintisa);
```

The hint is consumed by `createorglgr` [granf2.c:111] → `findisatoinsertgr` [granf2.c:130] → `findisatoinsertnonmolecule` [granf2.c:203]. The critical line:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   /* [granf2.c:209] */
```

When `supertype == subtype` (both `DOCUMENT=3`), `depth=1`. The new address is found by:
```c
tumblerincrement (&hintptr->hintisa, depth, 1, isaptr);   /* first-child case [granf2.c:237] */
```
`tumblerincrement(aptr, rightshift, val, cptr)` [tumble.c:599] locates the highest non-zero mantissa slot `idx` of `aptr` and writes `val` into `cptr->mantissa[idx + rightshift]`. With `rightshift=depth=1`, this appends exactly one new tumbler component to the hint address — a depth-1 extension.

For the owned-document path of `docreatenewversion`, the new version address = `docaddr` with one additional tumbler component.

---

### NODE-level analog: YES — `CREATENODE_OR_ACCOUNT` (FEBE request #38)

`docreatenode_or_account` [do1.c:243-258]:
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
  typeisa isa;
  typehint hint;
  ...
  tumblercopy(isaptr, &isa);
  makehint (NODE, NODE, 0, &isa, &hint);          /* [do1.c:251] */
  result = createorglingranf (taskptr, granf, &hint, &isa);
  if (result) { tumblercopy(&isa, isaptr); }
  return result;
}
```

`makehint(NODE, NODE, ...)` sets `supertype = subtype = NODE = 1`.

Back in `findisatoinsertnonmolecule` [granf2.c:209]:
```c
depth = (NODE == NODE) ? 1 : 2;   →  depth = 1
```

The result is identical in structure to the `DOCUMENT, DOCUMENT` path: a new granfilade orgl is inserted at a depth-1 tumbler extension of the input node address. The new node address has exactly one more tumbler component than the hint address.

This function is wired into the FEBE dispatch table as:

- `CREATENODE_OR_ACCOUNT = 38` [requests.h:45]
- `requestfns[CREATENODE_OR_ACCOUNT] = createnode_or_account;` [init.c:65]
- `fns.c:375` handles the protocol: reads one tumbler via `getcreatenode_or_account` [get1fe.c:228-236], calls `docreatenode_or_account`, and returns the newly allocated tumbler via `putcreatenode_or_account` [putfe.c:375-379].

**`CREATENODE_OR_ACCOUNT` is the exact structural analog of `docreatenewversion` at the NODE level.** Both use `supertype == subtype` in `makehint`, both produce a depth-1 tumbler extension of the given address, and both are exposed as first-class FEBE operations.

---

### ACCOUNT-level analog: NO

No call to `makehint(ACCOUNT, ACCOUNT, ...)` exists anywhere in the codebase (confirmed by exhaustive grep of all `makehint` call sites in `do1.c` and `do2.c`). The complete set of `makehint` calls is:

| Site | Call | supertype==subtype? | depth |
|---|---|---|---|
| do1.c:117 | `(DOCUMENT, ATOM, TEXTATOM, ...)` | NO | ATOM path |
| do1.c:180, 207 | `(DOCUMENT, ATOM, LINKATOM, ...)` | NO | ATOM path |
| do1.c:239 | `(ACCOUNT, DOCUMENT, 0, ...)` | NO | 2 |
| **do1.c:251** | **`(NODE, NODE, 0, ...)`** | **YES** | **1** |
| do1.c:271 | `(DOCUMENT, DOCUMENT, 0, ...)` | YES | 1 |
| do1.c:275 | `(ACCOUNT, DOCUMENT, 0, ...)` | NO | 2 |

The `XACCOUNT` FEBE operation (request #34, `fns.c:364-373`) does not create anything; it only reads back the calling user's pre-provisioned account address from `player[user].account`.

**There is no FEBE or BEBE operation that allocates a new account address via depth-1 tumbler extension from an existing account address.** Account creation at the NODE→ACCOUNT level (which would require `makehint(NODE, ACCOUNT, ...)`, depth=2) is also absent. Account addresses in the running system are established at backend initialization, not through any FEBE-accessible operation.

---

### `validhint` is dead code — does not gate the NODE path

For completeness: `validhint` [do2.c:86-108] would reject `subtype=NODE=1` because it checks `subtype < ACCOUNT` (i.e., `1 < 2 = TRUE` → error). But `validhint` is **never called** in the allocation path (`createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertnonmolecule`). It is an unreachable validation stub. The `makehint(NODE, NODE, ...)` hint therefore works at runtime, even though `validhint` would classify it as ill-formed.

---

### Summary

| Level | Analog of `docreatenewversion`? | Mechanism |
|---|---|---|
| DOCUMENT | **IS** `docreatenewversion` itself | `makehint(DOCUMENT, DOCUMENT, ...)` [do1.c:271], depth=1 |
| NODE | **YES** — `CREATENODE_OR_ACCOUNT` (req #38) | `makehint(NODE, NODE, ...)` [do1.c:251], depth=1 |
| ACCOUNT | **NO** | No `makehint(ACCOUNT, ACCOUNT, ...)` exists anywhere |

The node-level depth-1 extension operation exists and is a live FEBE endpoint. The account-level equivalent does not exist.
