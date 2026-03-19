## Question 15 [gregory]

> The Node.0.User.0.Doc tumbler hierarchy implies a two-level ownership model — is the node address (`1.1`) assigned at server startup and fixed, and is the user account address (`1.1.0.N`) allocated at account creation time, or can these be assigned dynamically?

## KB Synthesis

The KB describes the tumbler hierarchy and allocation mechanisms in detail, but does not contain findings that directly address how node addresses (`1.1`) are assigned or when account addresses (`1.1.0.N`) are created.

**What the KB does say:**

The `Node.0.User.0.Doc.0.Element` structure is a docuverse convention, not type enforcement — tumblers are unconstrained digit sequences and the `.0.` separators are purely positional semantics [SS-TUMBLER, Finding 0001].

The address hierarchy is encoded by `.0.` boundary count:
- Node address: `1.1` (no `.0.`)
- Account under node: `1.1.0.2` (one `.0.` boundary)
- Document under account: `1.1.0.2.0.1` (two `.0.` boundaries)

[SS-ADDRESS-SPACE, Finding 0021]

The allocation algorithm (`findisatoinsertnonmolecule`) with `depth=1` handles NODE→NODE and DOCUMENT→DOCUMENT placement, while `depth=2` handles ACCOUNT→DOCUMENT. This tells us how children are allocated under existing parents, but says nothing about how the root node addresses (`1.1`, `1.2`, etc.) are established [SS-ADDRESS-ALLOC, Finding 0021].

**What the KB cannot answer:**

There are no findings covering:
- Whether node addresses are pre-configured at server initialization vs. dynamically allocated
- The bootstrapping mechanism for the initial node (`1.1`) and its account children
- Whether multiple nodes (e.g., `1.2`, `1.3`) can coexist or how they'd be created

The KB's coverage begins at the account level and below. The node-level bootstrapping is not answerable from available findings.

---

## Code Exploration

Now I have all the evidence I need. Here is my complete analysis.

---

## Tumbler Address Assignment: Node, User Account, and Document

### The Hierarchy in Brief

The actual addresses seen in practice are:

| Level | Example | Context |
|-------|---------|---------|
| Node | `1.1` | Client-chosen root prefix |
| Account/User | `1.1.0.N` | Client passes; server allocates N |
| Document | `1.1.0.N.0.D` | Server allocates D sequentially |
| Sub-node | `1.1.0.N.K` | Server allocates K sequentially |

This is confirmed explicitly in `febe/scenarios/accounts.py:7` ("Xanadu tumbler structure: Node.0.User.0.Doc.0.Element") and by the golden test results.

---

### Is the Node Address `1.1` Fixed at Startup?

**No.** The node address `1.1` is not assigned or initialized anywhere in the backend at startup. There is no hardcoded node bootstrap.

At startup, `xumain.c:49` calls:

```c
getaccount(&task, &task.account);
```

The implementation in `task.c:28-41` simply zeroes the account tumbler:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr) {
    tumblerclear(accountptr);
    return(TRUE);
    /* ...prompt and gettumbler code is commented out... */
}
```

The **client** is entirely responsible for establishing what node address to operate under. It does so via the `XACCOUNT` command (opcode 34). `fns.c:364-373` handles it:

```c
void xaccount(typetask *taskptr) {
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    }
}
```

And `get1.c:190-204` (or `get1fe.c:213-226`) reads the tumbler from the wire:

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr) {
    gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
    taskptr->account = *accountptr;
    return(TRUE);
}
```

The backend's `validaccount()` in `get2fe.c:338-341` performs **no validation**:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr) {
    return(TRUE);
}
```

So the client can pass any tumbler as its operating account. The `1.1` prefix is a **client-side convention** — the default from `febe/scenarios/common.py:12`:

```python
DEFAULT_ACCOUNT = Address(1, 1, 0, 1)
```

The only hardcoded `1.1`-containing value in the entire backend is the **unused** `socketbe.c:35`:

```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};
```

This declares a default of `1.1.0.14`, but the code that would have used it (`socketbe.c:113-115`) is commented out.

---

### Is Account Address `1.1.0.N` Allocated Dynamically?

**Yes, but with a dual mechanism**: the base prefix (`1.1.0`) comes from the client-supplied hint; the `N` component is allocated sequentially by the server.

The `CREATENODE_OR_ACCOUNT` command (opcode 38) handles creation. The call path:

1. `fns.c:375-386`: reads the client-supplied hint tumbler via `getcreatenode_or_account()`
2. `get1.c:208-212`: `gettumbler(taskptr, tp)` — the hint comes off the wire
3. `do1.c:243-258`:

```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);
    result = createorglingranf(taskptr, granf, &hint, &isa);
    if (result) { tumblercopy(&isa, isaptr); }
    return result;
}
```

The `makehint(NODE, NODE, ...)` sets both `supertype` and `subtype` to `NODE` [do2.c:78-84]. This matters critically inside `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Since `NODE == NODE`, **depth = 1**. The server finds the last-allocated child of the hint and increments by one position:

```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   // for the empty case
```

With `depth=1` and hint `1.1.0.1`, the first call appends `.1` → result is `1.1.0.1.1`. The second appends `.2` → `1.1.0.1.2`. Confirmed by `golden/accounts/create_multiple_nodes.json`:

```json
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.1"},
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.2"},
{"op": "create_node", "account": "1.1.0.1", "result": "1.1.0.1.3"}
```

---

### Document Addresses Under Accounts

For comparison: documents use `makehint(ACCOUNT, DOCUMENT, ...)` in `do1.c:239`:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

Here `ACCOUNT != DOCUMENT`, so **depth = 2** — the server inserts a `.0.` separator before the sequential number. Account `1.1.0.1` → first document `1.1.0.1.0.1`, second `1.1.0.1.0.2`. Confirmed by `golden/accounts/account_switch.json`.

The `.0.` separator is not a conceptual zero — it is a structural artifact of the `depth=2` increment: `tumblerincrement(hintisa, 2, 1, isaptr)` appends at two places past the last digit.

---

### The Hierarchy Is Arbitrarily Deep

The `node_then_documents.json` golden test proves the address hierarchy is recursive, not hardcoded to two levels:

```
account = 1.1.0.1
create_node(1.1.0.1) → 1.1.0.1.1     ← depth=1, single increment
account = 1.1.0.1.1
create_document() → 1.1.0.1.1.0.1    ← depth=2, adds .0.N
create_document() → 1.1.0.1.1.0.2
```

Any tumbler can serve as an account. The address space can nest arbitrarily: a "node" returned by `create_node` can itself be passed as an account to create sub-nodes or documents under it.

---

### Summary

| Question | Answer |
|----------|--------|
| Is `1.1` the node address fixed at server startup? | **No.** The backend initializes the account to zero at startup [`task.c:31`]. `1.1` is a client-supplied convention sent via `XACCOUNT`. |
| Is `1.1.0.N` allocated at account creation time? | **Partly.** The `1.1.0` prefix is client-supplied as a hint; the server appends the sequential `N` using `findisatoinsertnonmolecule` with `depth=1` (NODE/NODE) [`granf2.c:209`]. |
| Can these be assigned dynamically? | **Yes, fully.** There is no hardcoded root node. The backend is address-agnostic; `validaccount()` always returns `TRUE` [`get2fe.c:340`]. The server's only role is sequential allocation under whatever hint the client provides. |

The `Node.0.User.0.Doc` structure is not a two-level fixed schema enforced by the server. It is an emergent pattern from the combination of the client-supplied `1.1.0.N` account tumbler and the server's depth-1 (for nodes) vs. depth-2 (for documents) sequential allocation strategy in `findisatoinsertnonmolecule` [`granf2.c:203`].
