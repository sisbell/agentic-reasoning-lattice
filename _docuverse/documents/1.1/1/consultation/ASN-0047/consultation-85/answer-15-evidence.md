## Question 15 [evidence]

> Does the udanax-green granfilade allocator hardcode a single bootstrap node address (e.g., `[1]`), or does it admit multiple sibling root nodes — and if the latter, by what mechanism are cross-root collisions prevented?

## KB Synthesis

The KB gives a partial but coherent answer.

**Single physical root, multiple logical address siblings**

The granfilade has exactly one physical root — the apex node stored at the fixed disk offset `GRANFDISKLOCATION` (`coredisk.h:117-120`). Every address in the system lives in this single tree [SS-UNIFIED-STORAGE].

Logically, however, the address space permits multiple sibling root-level nodes. The `makehint` depth table for NODE→NODE uses `depth=1`, meaning consecutive node addresses share no `.0.` boundary (e.g., `1.1`, `1.2`, `1.3`). Nothing in the allocator constrains the first digit to a single value [SS-ADDRESS-SPACE, Finding 0021].

**Collision prevention mechanism**

The allocator (`findisatoinsertnonmolecule`) is stateless query-and-increment, not counter-based:

1. Compute `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the address just past the parent's sibling range.
2. Call `findpreviousisagr` to find the highest existing address below that bound.
3. Containment-check the result (Bug 0013 fix — without this, allocation crosses account boundaries).
4. Increment to produce the next sibling [SS-ADDRESS-ALLOC, Finding 0021].

Since `findpreviousisagr` queries the live granfilade tree, any address already allocated is visible, making the new address strictly greater. Concurrent races are structurally impossible: the single-threaded `select()` event loop processes operations one at a time, so two allocations under the same parent can never interleave [INV-SEQUENTIAL-DISPATCH, INV-ATOMICITY].

**What the KB cannot answer**

The KB does not state whether the initial bootstrap node (`1.1` or similar) is hardcoded during `createenf`/initialization or dynamically allocated on first use. [EC-NO-STARTUP-VALIDATION] notes that startup performs no consistency check and simply reads whatever is in `enf.enf` — implying the bootstrap state is pre-seeded, not generated at runtime — but the seeding mechanism itself is not described in any finding.

---

## Code Exploration

I now have all the evidence needed. Let me compile the final answer.

---

## Answer: Granfilade Allocator — Bootstrap and Multi-Root Collision Behavior

### Short answer

The granfilade allocator does **not** hardcode a single bootstrap node address. It admits an unbounded number of sibling root nodes at any client-specified hint address. Collision prevention is handled by an explicit **under-hint guard** in `findisatoinsertnonmolecule`, not by any global serialization scheme.

---

### 1. No hardcoded bootstrap node

When the backend starts fresh, `entexit.c:44` runs:

```c
granf = (typegranf) createenf(GRAN);
```

This creates an **empty** granfilade enfilade. No seed node, no address `[1]`, no bootstrap item is inserted. The tree is truly empty.

The `getaccount` call in `xumain.c:49` calls [task.c:28–41]:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
    tumblerclear(accountptr);
    return(TRUE);
}
```

This zeros the account tumbler — a degenerate default. The real account is set by the client via the `XACCOUNT` protocol command, implemented in `get1fe.c:213–225`:

```c
gettumbler(taskptr, accountptr)
&& validaccount(taskptr, accountptr);
player[user].account = *accountptr;
taskptr->account = *accountptr;
```

Any tumbler value sent by the client becomes the session's account root. There is no constraint to a specific value.

---

### 2. Multiple sibling roots are fully supported

The two entry points that create granf entries are:

- **Documents** [do1.c:239]: `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` → uses session account as hint
- **Nodes/Accounts** [do1.c:251]: `makehint(NODE, NODE, 0, &isa, &hint)` → uses client-provided `isa` from `getcreatenode_or_account` [get1fe.c:228–234]

`makehint` [do2.c:78–84] simply copies the `isaptr` into `hintptr->hintisa`:

```c
hintptr->supertype = typeabove;
hintptr->subtype = typebelow;
hintptr->atomtype = typeofatom;
movetumbler(isaptr, &hintptr->hintisa);
```

Allocation is then fully relative to whatever `hintisa` is. Golden test `account_switch.json` confirms this empirically:

- Account `1.1.0.1` → first doc at `1.1.0.1.0.1`, second at `1.1.0.1.0.2`
- Account `1.1.0.2` → first doc at `1.1.0.2.0.1` (completely independent namespace)

And `create_multiple_nodes.json` shows sequential sibling allocation under one root:

- Hint `1.1.0.1` → nodes `1.1.0.1.1`, `1.1.0.1.2`, `1.1.0.1.3` (depth=1 for NODE,NODE)

---

### 3. Collision prevention mechanism: the under-hint guard

The critical function is `findisatoinsertnonmolecule` [granf2.c:203–242]. It works in four steps:

**Step 1 — Depth calculation** [granf2.c:209]:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```
- `NODE,NODE` or `DOCUMENT,DOCUMENT` → `depth=1` (children are one level below hint)
- `ACCOUNT,DOCUMENT` → `depth=2` (documents are two levels below account hint)

**Step 2 — Bounded search** [granf2.c:213–217]:
```c
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);
clear(&lowerbound, sizeof(lowerbound));
findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```
`findpreviousisagr` [granf2.c:255–278] returns the rightmost granf item strictly less than `upperbound`. Since `upperbound = hintisa + 1` at the hint's own depth, this conceptually bounds the search to the hint's subtree. However, `findpreviousisagr` has **no internal subtree filter** — it can return an item from a different root if that item happens to be the global predecessor of `upperbound`.

**Step 3 — The under-hint guard** [granf2.c:228–237] — this is the collision blocker:
```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```

If `findpreviousisagr` returned an address from a **different** account's subtree (e.g., `1.1.0.1.0.1` when allocating under `1.1.0.2`), the guard detects this by truncating `lowerbound` to `hintlength` digits and comparing with `hintisa`. They won't match, so `lowerbound_under_hint = FALSE` and the allocator resets to `hintisa.0.1` — producing `1.1.0.2.0.1`, not `1.1.0.2.0.2`. Cross-root contamination is blocked.

**Step 4 — Sequential allocation when same root** [granf2.c:239–240]:
```c
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```
When the predecessor is genuinely within the hint's subtree, it truncates to the appropriate depth and increments by 1 to get the next sequential child address.

---

### 4. `tumblerincrement` semantics confirm the pattern

`tumblerincrement(aptr, rightshift, bint, cptr)` [tumble.c:599–623]:

For a **zero tumbler** (empty granf, first item ever):
```c
if (iszerotumbler(aptr)) {
    cptr->exp = -rightshift;
    cptr->mantissa[0] = bint;
}
```
With `depth=2, bint=1`: produces `{exp=-2, mantissa[0]=1}` — the tumbler `0.0.1` in print notation, i.e. a value two levels below the origin.

For a **non-zero tumbler** `hintisa`:
```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
cptr->mantissa[idx + rightshift] += bint;
```
`idx` is the position of the last non-zero digit; `rightshift` pushes it further right. For `hintisa=1.1.0.1` with `depth=2`: result is `1.1.0.1.0.1`. This matches the golden test exactly.

---

### Summary table

| Mechanism | Where | What it does |
|---|---|---|
| Empty granf creation | `entexit.c:44` | No bootstrap node; tree starts empty |
| Client-specified root | `get1fe.c:221–224` | Any tumbler becomes the session account root |
| Depth-relative placement | `granf2.c:209,237` | Children placed at `hintisa.depth.1` |
| Under-hint guard | `granf2.c:228–237` | Detects cross-root predecessors; resets to first-child |
| Sequential same-root | `granf2.c:239–240` | Increments within same subtree safely |

**The granfilade is a general-purpose tree with an open root set.** No address is privileged. The allocator places any new item relative to its `hintisa` parent, and the explicit under-hint check at `granf2.c:231–233` is the sole mechanism preventing cross-root address contamination. There is no global lock, no reserved address, no bootstrap magic constant.
