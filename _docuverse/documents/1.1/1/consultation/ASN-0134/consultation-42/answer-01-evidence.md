## Question 1 [evidence]

> In udanax-green, how is a new document/orgl tumbler allocated under an account — is it drawn from a frontier-style sub-allocator so two concurrent same-account creations would collide on one address (as content allocations do), and what becomes of the loser?

## KB Synthesis

## Document Address Allocation in udanax-green

The short answer: document orgl allocation uses the **same stateless query-and-increment mechanism** as content allocation, but collision is impossible in practice because the event loop fully serializes all allocations.

---

### The Allocation Mechanism

Document addresses are allocated by `findisatoinsertnonmolecule` in `granf2.c`. The algorithm [ST-ADDRESS-ALLOC]:

1. Compute an upper bound: `tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent account
2. Call `findpreviousisagr` to find the highest existing address currently under the account in the granfilade tree
3. If nothing exists under the account yet, allocate the first child: `account.0.1`
4. Otherwise, truncate and increment: `account.0.2`, `.0.3`, etc.

This is explicitly **not** a frontier cursor or a cached counter. Finding 0061 and 0077 both confirm: "There is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`." [INV-MONOTONIC] The granfilade tree itself is the authoritative state; each allocation queries it fresh.

This is structurally identical to content allocation (`findisatoinsertmolecule`). Both functions are dispatched from `findisatoinsertgr` based on the `MOLECULE` flag; both query the same granfilade tree; both apply `tumblerincrement` to the result of `findpreviousisagr`. The only difference is the tumbler range each one searches within [SS-ADDRESS-SPACE, Finding 0077].

---

### Would Two Concurrent Same-Account Creations Collide?

No — and the reason is not a lock or a per-account mutex. It is the event loop.

Finding 0042 establishes `INV-SEQUENTIAL-DISPATCH` and `INV-ATOMICITY`: the `bed.c` event loop calls `xanadu(&task)` for each ready file descriptor and **blocks** until that call returns before looping back to `select()`. Every FEBE operation — including CREATE_DOCUMENT — runs to completion before the next begins. There is no interleaving at the operation level.

From Finding 0061: "This is safe without locking because the single-threaded event loop guarantees no concurrent allocations."

So for two simultaneous CREATE_DOCUMENT requests from different sessions under the same account:

- FE1's request is dispatched first. `findpreviousisagr` reads the tree, finds (say) `1.1.0.1.0.3` as the current maximum, allocates `1.1.0.1.0.4`, and the operation completes atomically — the new orgl is now in the tree before control returns to `select()`.
- FE2's request is dispatched next. `findpreviousisagr` now finds `1.1.0.1.0.4` as the maximum and allocates `1.1.0.1.0.5`.

[INV-GLOBAL-ADDRESS-UNIQUENESS] confirms the outcome: "Document addresses are globally unique even when multiple sessions use the same account... concurrent `create_document()` calls from different sessions on the same account produce distinct, sequential addresses."

---

### There Is No Loser

Because operations are serialized, there is no race and no loser. The "second" request simply gets the next address in sequence. This is the same protection content allocation receives — `findisatoinsertmolecule` is equally safe under the same event-loop guarantee, for the same reason [Finding 0061, PRE-CONCURRENT-INSERT].

The structural risk described in PRE-CONCURRENT-INSERT (unsynchronized adoption of right-brother nodes leading to lost `numberofsons` updates) is real at the enfilade level, but it is a hypothetical about what would happen *if* concurrent writes occurred — not a description of what the system actually permits. The single-threaded run-to-completion scheduler forecloses that scenario entirely [INV-SEQUENTIAL-DISPATCH].

---

## Code Exploration

I have all the code I need. Here is the complete answer with full citations.

---

## Orgl Tumbler Allocation in udanax-green

### The Call Chain

Every new document creation enters through `createnewdocument` [`fns.c:276`], which calls `docreatenewdocument` [`do1.c:234`]:

```c
// do1.c:239-240
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

`makehint` [`do2.c:78-84`] constructs:

```c
hintptr->supertype = ACCOUNT;   // 2
hintptr->subtype   = DOCUMENT;  // 3
hintptr->atomtype  = 0;
movetumbler (isaptr, &hintptr->hintisa);  // the user's account tumbler
```

`createorglingranf` [`granf1.c:50`] immediately wraps `createorglgr` [`granf2.c:111`]:

```c
// granf2.c:117-127
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

So the sequence is: **find address → create empty POOM enfilade → insert at that address in the global granfilade**.

---

### Where the Address Comes From: `findisatoinsertnonmolecule`

`findisatoinsertgr` [`granf2.c:130`] routes based on `hintptr->subtype`. Since DOCUMENT is not ATOM [`granf2.c:135`], it calls `findisatoinsertnonmolecule` [`granf2.c:203`]:

```c
// granf2.c:209
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

ACCOUNT (2) ≠ DOCUMENT (3), so `depth = 2`.

```c
// granf2.c:211-217
hintlength = tumblerlength (&hintptr->hintisa);
tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr` [`granf2.c:255-278`] traverses the entire in-memory granfilade tree to find the greatest ISA strictly less than `upperbound` — that is, the highest document address already existing under this account.

Then:

```c
// granf2.c:235-241
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    // Nothing yet — first document gets account.0.1
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

**There is no stored frontier counter.** The "next address" is reconstructed on every call by scanning the tree for the current maximum and adding 1. For an account at `1.1.0.1`, the first document gets `1.1.0.1.0.1`, the second `1.1.0.1.0.2`, and so on — each by re-reading the tree's state.

---

### The Global Granfilade: No Per-Account Sub-Allocator

The granfilade is declared as a single global [`xanadu.h:14`]:

```c
#define typegranf INT *
extern typegranf granf;
```

Both `docreatenewdocument` [`do1.c:240`] and `inserttextingranf` [`do1.c:118`] pass the same `granf` to their respective routines. There is no per-account frontier, no sub-allocator keyed by account, no stored "high-water mark". The next address is always derived by a fresh `findpreviousisagr` traversal of the single global tree.

---

### Why Two Concurrent Same-Account Creations Cannot Collide

The backend is **strictly single-threaded**. The event loop in `bed.c:103-149`:

```c
// bed.c:111-143
select(nfds+1, &inputfds2, 0, 0, &timeout);
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        task.account = player[user].account;
        xanadu(&task);       // synchronous: runs to completion
    }
}
```

`select()` may return multiple ready file descriptors at once, but `xanadu()` is called synchronously for each in sequence. `xanadu` dispatches `(*requestfns[request])(taskptr)` [`bed.c:162`] and `sendresultoutput` before the loop index advances. The entire path from `docreatenewdocument` through `findpreviousisagr` through `insertseq` completes — updating the in-memory enfilade — before the next FD is served.

There are zero threading primitives anywhere in the backend (no `pthread_mutex_lock`, no `sem_wait`, no `fork` for request handling — confirmed by exhaustive source search). Serialization is structural, not synchronized.

---

### What Would Happen If They Did Run Concurrently

`findisatoinsertnonmolecule` has a classic read-modify-write TOCTOU shape:

1. **Read**: `findpreviousisagr` scans the tree → returns `lowerbound`
2. **Compute**: increment to get `isaptr`
3. **Write**: `insertseq` places the new orgl at `isaptr`

If two handlers ran steps 1–2 simultaneously, both would see the same `lowerbound` and compute the same `isaptr`. Then both would call `insertseq` at that address. `insertseq` [`insert.c:17`] has no "slot occupied" guard for GRANORGL — it simply creates a new crum:

```c
// insert.c:43-52
reserve ((typecorecrum*)ptr);
new = createcrum (0,(INT)ptr->cenftype);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
ivemodified (new);
if (info->infotype == GRANORGL){
    info->granstuff.orglstuff.orglptr->leftbroorfather = new;
}
moveinfo (info, &((typecbc *)new)->cinfo);
```

The second write would silently overwrite the enfilade slot, losing the first caller's orgl. There is no detection, no error return to the "loser" — it would succeed from the caller's perspective but the first document's orgl handle would be orphaned and the address doubly claimed. The loser in this hypothetical would be whichever `insertseq` call landed second; there is no code to detect or recover from the collision.

---

### Contrast with Content (`ATOM`) Allocation

For text insertion, `findisatoinsertgr` routes to `findisatoinsertmolecule` [`granf2.c:158`] instead, which searches the document's sub-range (the molecule) for the next content address. The mechanism is structurally identical: read the tree to find the frontier, compute next, write. The same single-threaded event loop provides the same implicit serialization. The two allocators are not architecturally different — neither has a stored counter.

---

### Summary

| Question | Answer |
|---|---|
| Is there a frontier-style per-account sub-allocator? | **No.** The next address is computed fresh each time by `findpreviousisagr` scanning the global granfilade. |
| Could two concurrent same-account creations collide? | **Not in practice.** The `select`-loop event model [`bed.c:111-143`] is strictly single-threaded; each request runs to completion before the next is dispatched. |
| If they *could* run concurrently, what happens to the loser? | The second `insertseq` [`insert.c:43-52`] would silently overwrite the first's orgl at the same address. No error is returned; the first document's orgl is orphaned with no recovery path. |
| Is orgl allocation different from content allocation? | No. Both use `findisatoinsertgr` → tree scan → increment → `insertseq`, with no locking at either level. |
