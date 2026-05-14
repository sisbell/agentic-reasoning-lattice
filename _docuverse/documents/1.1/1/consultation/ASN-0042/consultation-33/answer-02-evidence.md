## Question 2 [evidence]

> In udanax-green, when a sub-account is delegated (via the granfilade entry-creation path used by account allocation), is the sub-account's prefix entered into the granfilade/baptismal registry as part of the same operation, and does `findpreviousisagr` therefore see delegated sub-account prefixes when computing the next slot?

## KB Synthesis

The KB does not describe a "delegation" operation or "baptismal registry" as named concepts — those terms don't appear in any KB entry. I can reason from what IS described, but cannot give a definitive answer.

## What the KB tells us

**The granfilade is the single address registry.** All orgls — content atoms, document orgls, and (based on the allocation code path) any structured address entries — live in the one flat granfilade B-tree. [SS-ADDRESS-ALLOC / Finding 0021]

**`findpreviousisagr` searches the granfilade globally, bounded by an upper limit.** The upper bound is set to `tumblerincrement(parent_isa, depth-1, 1)` — the next sibling of the parent address. Any orgl whose address falls below that ceiling and passes the containment check is visible. [ST-ADDRESS-ALLOC / Finding 0021, Finding 0068]

**The containment check was added precisely because the search crosses address subtree boundaries.** Bug 0013 showed that without truncation-and-comparison, `findpreviousisagr` would find addresses under a different account and use them as the increment base. The fix verifies that the found address is actually under the target parent. [PRE-ADDRESS-ALLOC / Finding 0021]

**There is no separate "next slot" counter — allocation is purely a function of current granfilade state.** Whoever allocated last is what `findpreviousisagr` finds. [SS-ADDRESS-SPACE / Finding 0061, Finding 0077]

## What follows from these facts

If sub-account delegation writes an orgl into the granfilade via the same `createorglingranf` path used for documents, then yes — that sub-account's address would be visible to `findpreviousisagr` during the next allocation under the same parent. The next slot would be computed relative to that delegated prefix, not the slot before it.

However, **the KB does not describe the delegation operation itself** — its call path, whether it uses `createorglingranf` or something else, or whether a delegated sub-account's address appears in the granfilade as an independent orgl vs. only implicitly through its children. This is not answerable from the KB as provided.

---

## Code Exploration

Now I have all the code I need. Let me trace the complete call chain for the answer.

---

## Answer

### The Short Answer

**Yes** on both counts — but with precise caveats about what "same operation" means and what the depth arithmetic implies.

---

### Full Trace

#### 1. Entry point: `CREATENODE_OR_ACCOUNT` request

```
fns.c:375  createnode_or_account()
do1.c:243  docreatenode_or_account()
granf1.c:50  createorglingranf()
granf2.c:111  createorglgr()
```

`docreatenode_or_account` [do1.c:251] calls:

```c
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
```

`NODE = 1` [xanadu.h:140].

---

#### 2. Address computation path

`createorglgr` [granf2.c:111–128] does two things in sequence:

1. Compute the address:
   ```c
   if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))   // granf2.c:117
       return (FALSE);
   ```

2. Insert into the granfilade:
   ```c
   locinfo.infotype = GRANORGL;                                       // granf2.c:119
   locinfo.granstuff.orglstuff.orglptr = createenf (POOM);           // granf2.c:120
   // ...
   insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);               // granf2.c:125
   ```

`insertseq` [insert.c:17] is not deferred or async — it directly modifies the in-memory enfilade tree:
- Calls `retrievecrums` to find insertion point
- Calls `adopt(new, RIGHTBRO, ptr)` — splices a new leaf into the tree
- Calls `setwispupwards` twice — propagates widths up the tree
- Optionally calls `recombine` — rebalances

There is **no write-back queue, no epoch, no epoch commit**. The tree is mutated in place. After `insertseq` returns, the new crum is live in the same in-memory tree pointed to by `fullcrumptr` (the global `granf`).

---

#### 3. `findisatoinsertgr` dispatch for NODE hint

`findisatoinsertgr` [granf2.c:130–156]:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(...);       // for text/link content
} else {
    findisatoinsertnonmolecule(...);    // for DOCUMENT, ACCOUNT, NODE
}
```

`NODE != ATOM`, so it goes to `findisatoinsertnonmolecule` [granf2.c:203].

---

#### 4. Depth arithmetic in `findisatoinsertnonmolecule`

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // granf2.c:209
// NODE == NODE → depth = 1
```

```c
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);  // granf2.c:213
// rightshift = depth-1 = 0
// This places upperbound at the *same* level as hintisa, +1
// e.g. hintisa=1 → upperbound=2 (next sibling account)
```

Then:

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // granf2.c:217
```

---

#### 5. What `findpreviousisagr` finds

`findpreviousisagr` [granf2.c:255–278] traverses the in-memory enfilade to find the **largest stored isa that is strictly less than `upperbound`**. It traverses via `findleftson`/`findrightbro` and accumulates widths with `tumbleradd`.

Because `insertseq` already modified the same tree, **any previously delegated sub-account prefix (e.g., `1.1`, `1.2`, …) that was inserted by a prior `CREATENODE_OR_ACCOUNT` operation is present in the tree and will be found here.**

The returned `lowerbound` is then checked:

```c
tumblertruncate(&lowerbound, hintlength, &truncated);              // granf2.c:231
lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);  // granf2.c:232
```

If `lowerbound` is under the hint (same account prefix), the next slot is:

```c
tumblertruncate (&lowerbound, hintlength + depth, isaptr);         // granf2.c:239
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);  // granf2.c:240
```

Example: if `hintisa = 1` (length 1), `depth = 1`, and `lowerbound = 1.1` (the previously inserted sub-account):
- truncate to length 2 → `isaptr = 1.1`
- `tumblerlength(1.1) = 2 ≠ hintlength(1)` → rightshift = 0
- `tumblerincrement(1.1, 0, 1, isaptr)` → `isaptr = 1.2`

`tumblerincrement` at [tumble.c:599]: `idx` = last non-zero digit index (1 for `1.1`), adds at `idx + rightshift = 1 + 0 = 1`, yielding `[1, 2, 0, …]` = `1.2`.

---

#### 6. The truncation is robust across deeply-nested children

If `lowerbound` is a document address like `1.1.0.1`, the `tumblertruncate` to `hintlength+depth = 2` still yields `1.1`, and incrementing still gives `1.2`. So even if documents or links are the highest-addressed entries in the granfilade, the sub-account allocation correctly advances the sub-account counter, not the document counter.

---

### Summary

| Claim | Verdict | Evidence |
|---|---|---|
| Sub-account prefix is entered into granfilade as part of the same `CREATENODE_OR_ACCOUNT` operation | **Yes** | `createorglgr` [granf2.c:117+125]: computes address with `findisatoinsertgr`, then immediately calls `insertseq` with `GRANORGL` type |
| `insertseq` modifies the shared in-memory tree | **Yes** | `insert.c:17–70`: `adopt`, `setwispupwards`, `recombine` all operate on `fullcrumptr` directly, no deferred commit |
| `findpreviousisagr` sees previously delegated sub-account prefixes when computing the next slot | **Yes** | `granf2.c:217`: `findpreviousisagr` walks the same in-memory tree; any prior `insertseq` is already there |
| The depth=1 arithmetic correctly scopes the search to sibling sub-accounts | **Yes** | `granf2.c:209+213+239–240`: `depth=1` for `NODE→NODE`, `upperbound` is next sibling, truncate+increment gives the next sub-account address |

The granfilade acts as both the baptismal registry and the address allocator for the `CREATENODE_OR_ACCOUNT` path. A single `createorglgr` call atomically (within a single-threaded request handler) computes the new address via `findpreviousisagr`, then registers it via `insertseq`, making it visible to all subsequent allocations.
