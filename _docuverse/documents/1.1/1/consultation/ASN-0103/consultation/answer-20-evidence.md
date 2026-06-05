## Question 20 [evidence]

> Does the new document address satisfy INV-IADDR-MONOTONIC under its account parent — strictly exceeding all previously allocated document tumblers even if intervening documents were never populated?

## KB Synthesis

**Yes** — the new document address strictly exceeds all previously allocated document tumblers under the account parent, including those for never-populated or deleted documents.

## Mechanism

The allocator in `findisatoinsertnonmolecule` works by querying the granfilade for the current maximum, then incrementing [SS-ADDRESS-ALLOC]. Specifically:

1. Computes `upperbound = tumblerincrement(parent, depth-1, 1)` — the next sibling of the parent
2. Calls `findpreviousisagr` to find the **highest existing address** below that bound in the granfilade tree
3. Truncates and increments to produce the next sibling

The critical property is that `findpreviousisagr` operates on the **actual granfilade tree state**, and the granfilade is **append-only** — allocated addresses are never removed [INV-NO-IADDR-REUSE]. This applies equally to document addresses and content I-addresses [FC-GRANF-ON-DELETE].

## Never-populated documents

A document address that was allocated but never had content written is still present in the granfilade tree. `findpreviousisagr` will find it, and the new address will be allocated above it.

## Deleted/versioned documents

Finding 0068 explicitly confirms this via example: deleting version `1.1.0.1.0.1.1` does **not** free its address — a subsequent VERSION allocates `1.1.0.1.0.1.2`, not `.1` again [INV-MONOTONIC, FC-GRANF-ON-DELETE]. The granfilade retains the deleted address permanently.

## The invariant

`∀ alloc_a, alloc_b under parent P : time(a) < time(b) ⟹ addr(b) > addr(a)` holds unconditionally — there is no mechanism to create gaps that later get reused [INV-MONOTONIC]. This is identical to how content I-address allocation is monotonic [INV-NO-IADDR-REUSE].

The only edge case is cross-account allocation contamination (Bug 0013), which PRE-ADDRESS-ALLOC addresses with a containment check — but that prevents wrong-account allocation, not monotonicity within the correct parent [PRE-ADDRESS-ALLOC].

---

## Code Exploration

Now I have everything needed to answer definitively. Let me trace the exact logic.

---

## INV-IADDR-MONOTONIC: Does a new document address strictly exceed all previously allocated document tumblers under the same account parent, even if intervening documents were never populated?

**Answer: Yes, INV-IADDR-MONOTONIC is satisfied under normal operation — but the mechanism rests on a critical design property that must be understood precisely.**

---

### The Allocation Call Chain

`docreatenewdocument` [do1.c:234-241]:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);  // do1.c:239
return (createorglingranf(taskptr, granf, &hint, isaptr));  // do1.c:240
```

`createorglingranf` [granf1.c:50-55] is a pure wrapper:
```c
return (createorglgr(taskptr, granfptr, hintptr, isaptr));  // granf1.c:54
```

---

### The Atomic Find-and-Insert in `createorglgr`

The decisive code is in `createorglgr` [granf2.c:111-128]:

```c
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))  // line 117: find next address
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);          // line 120: create empty POOM
reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);              // line 125: IMMEDIATELY INSERT
```

**Allocation and insertion are atomic within a single function call.** There is no API to "reserve" an address without inserting it. The return value `isaptr` is placed into the granule tree on line 125 before the function returns.

---

### How the Next Address is Computed: `findisatoinsertnonmolecule`

For DOCUMENT hints (non-ATOM), `findisatoinsertgr` [granf2.c:152] calls `findisatoinsertnonmolecule` [granf2.c:203-242]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // line 209
// For ACCOUNT→DOCUMENT: depth = 2

tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);  // line 213

clear(&lowerbound, sizeof(lowerbound));                           // line 215

findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // line 217
// Reads the granule tree; finds the highest item ≤ upperbound
```

Then two bug fixes [granf2.c:219-233] — `BUG FIX #2` explicitly ensures the found `lowerbound` actually belongs to the target account (prevents cross-account address bleeding):

```c
lowerbound_under_hint = FALSE;
if (!iszerotumbler(&lowerbound)) {
    tumblertruncate(&lowerbound, hintlength, &truncated);         // line 231
    lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);  // line 232
}
```

Then the final allocation [granf2.c:235-241]:
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // line 237: first child = hintisa.0.1
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);  // line 239: truncate lowerbound
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);  // line 240: +1
}
```

`tumblerincrement` [tumble.c:599-623] with `bint=1` adds 1 at position `idx + rightshift` in the mantissa [tumble.c:621], always producing a strictly greater value.

---

### What `findpreviousisagr` Reads

`findpreviousisagr` [granf2.c:255-278] traverses the live in-memory granule tree:

```c
if (crumptr->height == 0) {
    findlastisaincbcgr((typecbc*)crumptr, offset);  // line 264: last item in leaf
    return(0);
}
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (...THRUME || ...ONMYRIGHTBORDER || !ptr->rightbro) {
        findpreviousisagr(ptr, upperbound, offset);  // line 272: recurse rightmost path
        return(0);
    } else {
        tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // line 275: accumulate
    }
}
```

This reads **only items that have been inserted via `insertseq`**. Since `createorglgr` inserts immediately (line 125), every previously created document — including empty, unpopulated ones — is present in this tree.

---

### Why "Never Populated" Does Not Create Gaps

"Never populated" means a document was created via `docreatenewdocument` but no content was added via `doinsert`/`docopy`. This is semantically meaningful but structurally irrelevant to address allocation, because:

1. `createorglgr` inserts an **empty `GRANORGL` entry** (pointing to a freshly created `POOM` enfilade, `createenf(POOM)` at line 120) into the granule tree at line 125.
2. This empty entry has the allocated address as its granule position.
3. `findpreviousisagr` will find this empty entry and return its address as `lowerbound`.
4. The next allocation computes `lowerbound + 1`, strictly exceeding the empty document's address.

The granule tree records document existence (the GRANORGL node), not document content. Population affects the document's own POOM enfilade, not its presence in the granule tree.

---

### Single-Threaded Event Loop Guarantees No Races

From `bed.c`, the main loop [bed.c:103-149] uses `select()` and processes one user request at a time. `xanadu()` [bed.c:153-172] handles a complete request and returns before the next request is dispatched. There is no preemption between `findisatoinsertgr` (line 117) and `insertseq` (line 125) inside `createorglgr`.

---

### One Edge Case: Crash Between Find and Insert

There is a narrow failure scenario: if the backend crashes after `findisatoinsertgr` computes `isaptr` (line 117) but before `insertseq` runs (line 125), the address was returned to the client but never written to the granule tree. On restart, `findpreviousisagr` would not see it, and the next allocation would reuse the same address.

This is not exploitable through normal operation — it requires an abnormal termination between two consecutive lines of C within a single synchronous call — but it means INV-IADDR-MONOTONIC is a property of normal execution, not a crash-safe invariant.

---

### Summary

| Mechanism | Location | Effect |
|---|---|---|
| Address computation reads granule tree | `findpreviousisagr`, granf2.c:217 | Sees all previously created documents, including empty ones |
| Allocation = immediate insertion | `createorglgr`, granf2.c:117+125 | No "reserved but not inserted" addresses exist |
| Increment always produces strictly greater value | `tumblerincrement`, tumble.c:621 | new\_addr > max\_existing is guaranteed |
| Account boundary check enforces correct scope | `findisatoinsertnonmolecule`, granf2.c:231-232 | Cross-account bleed is prevented |
| Single-threaded event loop | `bed.c:111`, `xanadu` at bed.c:128 | No concurrent allocation races |

**INV-IADDR-MONOTONIC holds**: every new document address strictly exceeds all previously allocated document addresses under the same account parent, including documents that were created but never populated, because creation unconditionally inserts an empty GRANORGL into the granule tree, making the address visible to all future allocations.
