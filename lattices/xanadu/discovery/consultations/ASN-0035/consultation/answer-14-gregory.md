## Question 14 [gregory]

> Is the node set fixed at system genesis, or can new nodes enter the docuverse after initial startup — and if so, what mechanism registers them and ensures their tumbler prefix doesn't collide with existing nodes?

## KB Synthesis

The KB does not describe a mechanism for adding new top-level nodes after system genesis, nor does it document any inter-server federation or registration protocol. Here is what the KB does and doesn't say:

---

## What the KB says about node structure

Tumbler addresses encode a strict containment hierarchy [SS-ADDRESS-SPACE, Finding 0021]:

```
Node:    1.1
Account: 1.1.0.2   (Node.0.Account — depth=2 crossing)
Document: 1.1.0.2.0.1
```

The `makehint` dispatch table includes a `NODE → NODE` case with `depth=1` (no `.0.` boundary), meaning nodes can be allocated as children of existing nodes. This is the same stateless query-and-increment mechanism used for all address allocation [SS-ADDRESS-ALLOC, Finding 0021]: find the highest existing address under the parent via `findpreviousisagr`, then increment.

## Collision prevention within the system

Within the single deployed system, collisions are structurally impossible because:

1. **Single granfilade** — all persistent state lives in one `enf.enf` file [SS-UNIFIED-STORAGE, Finding 0059]. There is one global allocator.
2. **Monotonic allocation** — `findisatoinsertmolecule` / `findisatoinsertnonmolecule` always allocate strictly above the current maximum [INV-MONOTONIC, Findings 0033, 0061]. No address is ever reused [INV-NO-IADDR-REUSE].
3. **Containment check** — allocation under a parent verifies the candidate address is actually under that parent before accepting it [PRE-ADDRESS-ALLOC, Finding 0021]. This is the fix for Bug 0013, which caused cross-account allocation pollution.
4. **Sequential dispatch** — the event loop is single-threaded with run-to-completion semantics [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY, Finding 0042], so no concurrent allocation races are possible.

## What the KB cannot answer

The KB has no evidence of:

- A node registration or bootstrapping protocol that admits new top-level nodes (`1.1`, `1.2`, …) from outside the existing deployment
- Inter-server communication, federation, or docuverse-wide coordination
- A global node registry distinct from the local granfilade

The system as documented is a single-server daemon. The `1.x` address prefix where `1` is the root appears fixed at deployment time. The only node-addition mechanism in the KB is the local `NODE → NODE` allocation, which adds subnodes under an existing node within the same granfilade — it is not a mechanism for incorporating a new independent server.

**Bottom line:** Within udanax-green as documented, the node set is effectively fixed at system genesis. The collision prevention is total within the single granfilade by monotonic allocation plus containment checking. How a new peer node would enter a multi-server docuverse — the Nelson-vision scenario — is not answered by this implementation.

---

## Code Exploration

I now have everything needed. Here is the full answer.

---

## Are Nodes Fixed at Genesis?

**No.** The node set is not sealed at startup. New nodes can enter the docuverse at any time through a live FEBE request. There is no genesis block or pre-assigned node table baked into initialization.

---

## What Happens at Startup

`bed.c:92` calls `init(1)`, which at `init.c:42-65` does nothing but fill the `requestfns[]` dispatch table:

```c
for (i = 0; i < NREQUESTS; ++i)
    requestfns[i] = nullfun;
/* ... */
requestfns[CREATENODE_OR_ACCOUNT] = createnode_or_account;   /* init.c:65 */
```

No node objects are created. The persistent enfilade tree is loaded from disk by `initmagicktricks()` (`bed.c:95`). After that the daemon sits in its `select()` loop waiting for frontend connections (`bed.c:103-148`). The granfilade on disk is the only authoritative record of which nodes exist.

`bert.c` is not a node registry — it is a per-connection document open/close lock table (`bert.c:13-29`). It knows nothing about node addresses.

---

## The Registration Mechanism

A client registers a new node by sending FEBE request 38 (`requests.h:45: #define CREATENODE_OR_ACCOUNT 38`) with one argument: a tumbler that serves as the desired parent (hint) address.

**Layer 1 — wire decode** (`get1.c:208-212`):
```c
int getcreatenode_or_account(typetask *taskptr, tumbler *tp) {
    gettumbler(taskptr, tp);
    return(TRUE);
}
```
The client supplies exactly one tumbler — its desired namespace prefix.

**Layer 2 — FEBE handler** (`fns.c:375-386`):
```c
void createnode_or_account(typetask *taskptr) {
    tumbler t;
    if (getcreatenode_or_account(taskptr, &t)
     && docreatenode_or_account(taskptr, &t))
        putcreatenode_or_account(taskptr, &t);
    else
        putrequestfailed(taskptr);
}
```

**Layer 3 — implementation** (`do1.c:243-258`):
```c
bool docreatenode_or_account(typetask *taskptr, typeisa *isaptr) {
    typeisa isa;
    typehint hint;
    tumblercopy(isaptr, &isa);
    makehint(NODE, NODE, 0, &isa, &hint);           /* do1.c:251 */
    result = createorglingranf(taskptr, granf, &hint, &isa);  /* do1.c:252 */
    if (result) tumblercopy(&isa, isaptr);
    return result;
}
```

`makehint(NODE, NODE, 0, ...)` (`do2.c:78-84`) sets `supertype=NODE(1)`, `subtype=NODE(1)`, `atomtype=0`, with the client-supplied tumbler as `hintisa`. This is a self-referential node hint — it says "allocate a NODE-level object in the NODE namespace rooted at this address."

**Layer 4 — granfilade allocation chain**:

`createorglingranf()` (`granf1.c:50-55`) is a thin wrapper:
```c
bool createorglingranf(typetask *taskptr, typegranf granfptr,
                       typehint *hintptr, typeisa *isaptr) {
    return createorglgr(taskptr, granfptr, hintptr, isaptr);
}
```

`createorglgr()` (`granf2.c:111-128`):
1. Calls `findisatoinsertgr()` to compute the new node's address
2. Calls `createenf(POOM)` to allocate a fresh POOM enfilade for the node's content
3. Calls `insertseq()` to register the node in the granfilade tree

---

## How Tumbler Addresses Are Generated (Collision Prevention)

`findisatoinsertgr()` (`granf2.c:130-156`) dispatches to `findisatoinsertnonmolecule()` for NODE/ACCOUNT/DOCUMENT types.

`findisatoinsertnonmolecule()` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  /* granf2.c:209 */
```

For NODE→NODE, `depth = 1`. For ACCOUNT→DOCUMENT, `depth = 2`.

```c
tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);  /* granf2.c:213 */
clear(&lowerbound, sizeof(lowerbound));
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  /* granf2.c:217 */
```

`findpreviousisagr()` (`granf2.c:255-278`) recursively walks the enfilade tree to find the highest-addressed existing object with an address strictly less than `upperbound`. This is a tree walk — the entire history of allocated addresses is encoded in the enfilade's node structure.

Then two guard conditions (added as Bug Fix #2 in the comment at `granf2.c:224-227`):

```c
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);  /* granf2.c:232 */
}
```

This verifies the found neighbor actually shares the same hint prefix. Without this check, an existing node at `1.2.0.1` would pollute allocation under a hint at `1.3` — exactly the cross-account collision scenario.

Finally, the address is assigned:

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);   /* granf2.c:237 — first child */
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr); /* granf2.c:240 */
}
```

- **No prior nodes under this hint:** address = `hintisa` with `depth` extra components, last one = 1. E.g., for hint `1.0`, node gets `1.0.1`.
- **Prior nodes exist:** truncate the predecessor to `hintlength + depth` components, then increment. Each subsequent node gets the next sequential address in the namespace.

The new address is then planted into the granfilade by `insertseq()` (`granf2.c:125`), making it part of the persistent sorted tree that all future `findpreviousisagr()` walks will see.

---

## Summary

| Question | Answer | Citation |
|----------|--------|----------|
| Fixed at genesis? | No — open, on-demand creation | `init.c:42-65` (no node creation at startup) |
| Registration entry point | FEBE request 38: `CREATENODE_OR_ACCOUNT` | `requests.h:45`, `init.c:65` |
| Wire protocol | Client sends one tumbler (hint prefix) | `get1.c:208-212` |
| Hint type used | `makehint(NODE, NODE, 0, hint_tumbler)` | `do1.c:251` |
| Address computation | `findisatoinsertnonmolecule()` with `depth=1` | `granf2.c:203-242` |
| Collision avoidance | Tree walk finds highest prior address; prefix check ensures it's in the same namespace; then sequential increment | `granf2.c:217, 229-232, 237-240` |
| Persistence | `insertseq()` writes into the granfilade; survives across restarts | `granf2.c:125` |
| Offline allocation | Not supported — server is authoritative; no merge protocol exists | (absence of any such mechanism) |

The collision guarantee is entirely structural: the granfilade tree is the authoritative record of all allocated addresses, `findpreviousisagr()` reads it on every allocation, and `tumblerincrement()` always produces a strictly larger address. As long as all allocations go through the live server, uniqueness is guaranteed by construction. There is no separate node-ID registry, no genesis list, and no offline pre-allocation protocol.
