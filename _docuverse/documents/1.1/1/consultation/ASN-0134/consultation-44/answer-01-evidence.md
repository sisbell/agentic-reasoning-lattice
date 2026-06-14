## Question 1 [evidence]

> Does udanax-green allocate document/orgl addresses by reading a shared per-account frontier and depositing contiguously (so two same-account creations read one frontier and compute the same address), or by a freshness-test that admits gaps in document numbering?

## KB Synthesis

Udanax-green uses **stateless query-and-increment on the live granfilade tree** — there is no shared per-account frontier variable.

## Mechanism

Every address allocation calls `findisatoinsertgr` (dispatching to `findisatoinsertnonmolecule` for document/orgl addresses), which executes two steps every time [SS-ADDRESS-ALLOC Finding 0021]:

1. Compute an upper bound: `upperbound = tumblerincrement(parentISA, depth-1, 1)` — the next sibling of the parent, bounding the search to the parent's subtree.
2. Call `findpreviousisagr` to walk the granfilade tree and return the highest existing address strictly below that bound.
3. If nothing found under the parent → allocate `parent.0.1` (first child). Otherwise → truncate the found address and increment by 1.

There is **no cached counter**. Finding 0061 is explicit: "The allocation is purely derived from current tree state — there is no cached 'next available' pointer." Finding 0077 confirms: "There is no single global Σ.next counter. Allocation is a family of independent functions partitioned by tumbler range: `next_doc_addr(granf, parent) = max_child(granf, parent) + 1`." [SS-ADDRESS-SPACE Finding 0077]

## Concurrency: why two same-account creations can't race to the same address

The system is strictly single-threaded via a `select()`-based run-to-completion event loop. Every FEBE operation runs to full completion — including granfilade tree modification — before the next operation's handler begins [INV-ATOMICITY Finding 0042, INV-SEQUENTIAL-DISPATCH Finding 0042]. There is no interleaving. The second CREATEDOCUMENT will call `findpreviousisagr` after the first has already written its document address to the tree, so it will see the first's address and allocate the next consecutive value.

## Do gaps occur?

**For pure document allocation sequences: no.** Under normal same-account document creation (no unusual allocation patterns), documents are numbered consecutively (`account.0.1`, `account.0.2`, `account.0.3`, …) because the tree query always finds the current maximum.

**However, interleaved allocations of a different type can create apparent gaps in the text I-address subsequence.** CREATELINK allocates a link orgl via the same `findisatoinsertgr` mechanism, consuming I-address space. After INSERT "ABC" (I.1–I.3) → CREATELINK → INSERT "DEF", the text I-addresses are non-contiguous because the link orgl sits between them [INT-LINK-INSERT Finding 0063]. This is not a gap in *document* numbering but in *content* I-address numbering within a document.

Link orgls live at `docISA.0.2.x` and version addresses live at `docISA.x`, both under the document — not under the account. Document addresses (`accountISA.0.x`) occupy a distinct tumbler subtree, so link orgl allocation does not interfere with account-level document numbering [SS-ADDRESS-SPACE Finding 0077].

**The Bug 0013 scenario** [PRE-ADDRESS-ALLOC] shows the other risk: without the containment check fix, `findpreviousisagr` could return an address from a *sibling account* as the "highest below upperbound," causing the allocator to increment from the wrong base and produce an address in the wrong account's subtree. With the fix, a post-query containment check (`tumbleraccounteq` / prefix-match) rejects out-of-scope results and falls back to the first-child `parent.0.1` convention.

## Summary

The allocator is a **freshness-test** approach (query-and-increment on live tree state), not a deposited frontier. In single-threaded sequential execution, this produces consecutive document numbers with no gaps. Gaps in the *content* I-address space can appear when CREATELINK interleaves with INSERT, because both use the same monotonic allocator; but document-level address numbering is isolated in its own tumbler subtree and remains gap-free under normal operation.

---

## Code Exploration

I now have a complete picture of the allocation path. Let me compile the full answer.

---

## How udanax-green Allocates Document/Orgl Addresses

### Answer: Freshness-test against the live enfilade tree — no shared frontier variable, gaps theoretically possible but structurally suppressed

---

### The Call Chain

**`createnewdocument` [fns.c:276–286]** dispatches to `docreatenewdocument`.

**`docreatenewdocument` [do1.c:234–241]** builds the hint and delegates:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return createorglingranf(taskptr, granf, &hint, isaptr);
```

`taskptr->account` is the account tumbler loaded from the session's `player[user].account` [bed.c:123]. This is the **parent address** used to bound the search. Nothing is read from a frontier variable.

**`makehint` [do2.c:78–84]** just copies the account tumbler into `hint.hintisa`:

```c
hintptr->supertype = typeabove;  // ACCOUNT = 2
hintptr->subtype   = typebelow;  // DOCUMENT = 3
hintptr->atomtype  = typeofatom; // 0
movetumbler(isaptr, &hintptr->hintisa);
```

**`createorglingranf` [granf1.c:50–55]** → `createorglgr`.

**`createorglgr` [granf2.c:111–128]** calls `findisatoinsertgr` to compute the new address, then immediately commits it:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
    return FALSE;
// ... build locinfo ...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);   // [granf2.c:125]
```

`insertseq` [insert.c:17] writes the new crum into the in-memory enfilade tree synchronously — it does not return a bool and has no deferred path. The tree is updated before `createorglgr` returns.

---

### The Address Computation: `findisatoinsertnonmolecule`

For `ACCOUNT→DOCUMENT` the subtype is not `ATOM`, so `findisatoinsertgr` [granf2.c:130–156] routes to `findisatoinsertnonmolecule`:

```c
if (hintptr->subtype == ATOM) {
    findisatoinsertmolecule(...);
} else {
    findisatoinsertnonmolecule(...);  // taken for DOCUMENT creation
}
tumblerjustify(isaptr);
```

**`findisatoinsertnonmolecule` [granf2.c:203–242]** in full:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ACCOUNT(2) != DOCUMENT(3)  → depth = 2

hintlength = tumblerlength(&hintptr->hintisa);

tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);
// upperbound = account address + 1 at level (depth-1=1) — one story above documents
// This bounds the search to "all documents of this account"

clear(&lowerbound, sizeof(lowerbound));

findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// Tree walk: sets lowerbound = highest ISA in tree strictly below upperbound

/* BUG FIX #2: verify lowerbound is actually under this account */
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
}

if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this account → first document */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    // e.g. account 1.1.0.1  →  new doc 1.1.0.1.0.1
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr) == hintlength ? depth : 0, 1, isaptr);
    // Strip sub-document content positions, then increment the document digit
    // e.g. lowerbound 1.1.0.1.0.1.some.text  →  truncated 1.1.0.1.0.1  →  next 1.1.0.1.0.2
}
```

**`findpreviousisagr` [granf2.c:255–278]** does a recursive descent of the enfilade tree, accumulating WIDTH spans to find the last stored ISA before `upperbound`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp = whereoncrum(ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
            || tmp == ONMYRIGHTBORDER
            || !ptr->rightbro) {
            findpreviousisagr(ptr, upperbound, offset);   // descend
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate
        }
    }
}
```

This reads the **live in-memory enfilade** (`granf`). There is no frontier variable, no cached counter. The "frontier" is whatever is actually in the tree at the moment of the call.

---

### Why Two Same-Account Creations Cannot Get the Same Address

The backend is a **single-threaded `select`-based event loop** [bed.c:103–149]:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                task.account = player[user].account;   // [bed.c:123]
                xanadu(&task);                         // [bed.c:128] — one complete request
            }
        }
    }
}
```

`xanadu(&task)` [bed.c:153–172] processes one full request — including `findpreviousisagr`, the address computation, and `insertseq` that commits to the tree — **before the next file descriptor is serviced**. The inner loop is not re-entrant. When the second creation runs, the first creation's orgl is already in the tree; `findpreviousisagr` will find it and produce the next sequential address.

There is no scenario in which two creations read the same tree state before either commits. The question's premise — "two same-account creations read one frontier and compute the same address" — is structurally impossible because the frontier is not a cached value; it is the current tree state, which is already updated by the time any second creation runs.

---

### Gap Analysis

**Normal sequential operation:** strictly contiguous. Each document gets `prev + 1` at the document digit level. First document is `account.0.1`, second is `account.0.2`, etc.

**Potential gaps exist only in these cases:**

1. **`klugefindisatoinsertnonmolecule` [granf2.c:183–201]:** This dead-code path (guarded by `#ifdef UnDeFIned`, never compiled) simply copied `hintisa` as the new address — which would place the first document at the account address itself. It was replaced by the corrected `findisatoinsertnonmolecule`. No operational gap risk.

2. **Different accounts' documents interspersing:** If account A creates doc `1.1.0.1.0.1` and then account B (address `1.1.0.2`) creates, `findpreviousisagr` might return account A's document as `lowerbound`. BUG FIX #2 [granf2.c:228–233] guards against this: it checks `lowerbound_under_hint` by truncating `lowerbound` to `hintlength` and comparing to the account address. If the found item is from a different account, it's treated as if nothing exists, and account B correctly gets `1.1.0.2.0.1`.

3. **Content addresses within a document:** When `findpreviousisagr` returns a `lowerbound` that includes sub-document content positions (e.g., `account.0.1.some.text`), `tumblertruncate` [granf2.c:239] strips those back to just the document address before incrementing. No gap is introduced.

---

### Summary

| Question | Answer |
|----------|--------|
| Is there a shared per-account frontier variable? | **No.** The frontier is computed fresh every call by walking the live enfilade tree via `findpreviousisagr` [granf2.c:255] |
| Can two same-account creations read the same frontier? | **No.** The event loop [bed.c:128] is single-threaded and sequential; the first creation's `insertseq` [granf2.c:125] commits to the tree before the second creation's `findpreviousisagr` runs |
| Are addresses contiguous? | **Yes**, under normal operation. Each new document address is `prev_document + 1` at the document digit level |
| Can gaps occur? | **Theoretically no** under the current code. The dead `kluge` path and cross-account contamination are both guarded away. Gaps would require concurrent access, which the single-threaded model prevents |
