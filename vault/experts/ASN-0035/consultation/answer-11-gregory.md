## Question 11 [gregory]

> In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, what concrete entity does the node field (e.g., `1.1`) represent — a running backend instance, a persistent address partition, or something else?

## KB Synthesis

The KB describes the node field's structural role clearly but does not characterize what real-world entity it represents.

**What the KB does say:**

The tumbler pattern `1.1` is the top level of the docuverse address hierarchy [SS-TUMBLER, Finding 0001]. Accounts (users) live *under* nodes, separated by a `.0.` boundary — so `1.1.0.1` is account 1 under node `1.1`, and `1.1.0.2` is account 2 under the same node [SS-ADDRESS-SPACE, Finding 0021].

The `makehint` depth table [SS-ADDRESS-SPACE, Finding 0021] shows `NODE → NODE` with depth=1, meaning nodes can be nested under other nodes (no `.0.` crossing for node-under-node). This recursive nesting is structurally identical to version chains under documents [SS-VERSION-ADDRESS, Finding 0068].

The address layout from [SS-ADDRESS-SPACE, Finding 0077] places the node prefix `1.1` above accounts and never elaborates on what instantiated the node. The containment predicate [SS-TUMBLER-CONTAINMENT, Finding 0021] treats node addresses the same as any other prefix — purely as a tumbler hierarchy level.

**What the KB does not say:**

The KB contains no finding that identifies whether node addresses correspond to running backend processes, persistent administrative partitions, hardware machines, or something else. The backend is described as a single daemon ([SS-SESSION-STATE, Finding 0022]), but there is no finding connecting that daemon's identity to the `1.x` node prefix in any explicit way.

The node field's real-world semantics — whether it represents a server in a distributed docuverse network, a logical partition, or an installation-time constant — is not answerable from the KB as written.

---

## Code Exploration

Here is the full answer:

---

## What the Node Field (`1.1`) Represents

**Short answer:** The node field is a **persistent, statically-assigned address prefix** for a server/site in the Xanadu distributed address space — the top-level namespace partition. In udanax-green it is hardcoded to `1.1` and never changes at runtime.

---

### The Tumbler Structure

`common.h:59-67`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];  /* NPLACES = 16 */
} tumbler;

#define ZEROTUMBLER  {0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
```

The mantissa is a flat array of integers. **Zero is a level separator.** So the tumbler `1.1.0.1.0.1` is stored as `mantissa[] = {1, 1, 0, 1, 0, 1, 0, 0, ...}`.

The four hierarchy levels are named in `xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

These are not runtime IDs — they are constants used as arguments to `makehint()` to describe what kind of address to allocate.

---

### Node = `1.1` Is Hardcoded

`be.c:37` (single-connection backend):
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

`socketbe.c:35` (multi-connection backend):
```c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};
```

In both cases the mantissa starts `[1, 1, 0, ...]`. The comment `/* 1.1.0.1 */` confirms the encoding: node = mantissa positions 0–1 = `1.1`, separator = `0`, account = `1`.

This value is placed directly into `task.account` at startup (`be.c:88`):
```c
movetumbler(&defaultaccount, &task.account);
```

And in the multi-user backend, it is populated per-connection from the `player[]` array (`bed.c:123`):
```c
task.account = player[user].account;
```

There is **no code that assigns a node ID based on the running process, socket, PID, or network**. No node configuration exists in `.backendrc` either — `rcfile.c` supports configuring `port`, `host`, `allocsize`, directory names, but has no `node` key.

---

### How Node-Level Addresses Are Created

`do1.c:243-258`:
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr)
{
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);
    result = createorglingranf(taskptr, granf, &hint, &isa);
    if (result) {
        tumblercopy(&isa, isaptr);
    }
    return result;
}
```

The `makehint(NODE, NODE, ...)` call means: *allocate a new address at the node level, within an existing node's subtree*. The hint tumbler `isa` (passed in from the frontend) is used as the parent. `findisatoinsertnonmolecule` (`granf2.c:203-241`) then finds the highest existing address at that level and increments it, returning the newly allocated node address.

The comment at `granf2.c:150-151` makes the format explicit:
> "making the first document get the account address itself (`1.1.0.1` instead of `1.1.0.1.0.1`)"

So a full document address has the form: **`Node.0.Account.0.Document.0.Atom`** = e.g. `1.1.0.1.0.1.0.1`.

---

### What the Node Field Concretely Is

The node field was designed as the **globally unique persistent identifier for a Xanadu server/site** in a federated network. The two-component form (`1.1`) mirrors how Xanadu originally envisioned multi-level server hierarchies (think of it as a org-level + server-level address, analogous to how IP addresses were conceived for networks).

In udanax-green's actual implementation:

| Hypothesis | Verdict | Evidence |
|---|---|---|
| Running backend instance | **No** | Node is hardcoded; multiple instances would all say `1.1` |
| Persistent address partition | **Yes** | Same value survives restarts; hardcoded in source |
| Configurable per-site | **Intended yes, implemented no** | No node key in `.backendrc`; no command-line argument |
| Network-assigned in federated Xanadu | **Intended yes** | Design artifact of the distributed Xanadu vision |

In udanax-green as shipped, **the node field is a permanently fixed, hardcoded namespace prefix** — a vestige of the distributed-Xanadu architecture. Every document address on this server starts with `1.1.0.`. The concept of distinct nodes (`2.1`, `3.4`, etc.) exists in the address space and allocation logic, but no running instance of this codebase ever claims any node other than `1.1`.
