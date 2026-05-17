## Question 1 [evidence]

> In udanax-green's link-emission path (`docreatelink`, `findisatoinsertmolecule`, granf2.c:170–175), is the allocator-state evolution (`Act(s)`, `n_s` updates per allocator on the L1c chain) atomic with the link-store deposit, or are there observable intermediate states between the allocator updates and the deposit?

## KB Synthesis

## Allocator-State Atomicity in `docreatelink`

**Short answer:** The allocator-state update and the link-store deposit are sequentially coupled within a single uninterruptible dispatch unit — so they are **externally atomic** under normal operation, but **not transactionally atomic** against crashes, and there are observable intermediate states *within* the call chain.

---

### What the call chain does

`docreatelink` executes three steps in sequence [ST-CREATE-LINK]:

1. **`createorglingranf()`** — allocates the link orgl I-address via `findisatoinsertmolecule` (granf2.c:158–181). This is the allocator-state update: the granfilade's maximum I-address advances, and the new link orgl node is inserted into the granfilade B-tree. After this step, `findpreviousisagr` would return the new maximum.

2. **`docopy()`** — places the link orgl's ISA into the document's `2.x` V-subspace via `insertpm`.

3. **`insertendsetsinspanf()`** — indexes the from/to/type endpoint I-addresses into the spanfilade. This is the "deposit" into the discoverable link store.

Between steps 1 and 3 there is a genuine intermediate state: the link orgl exists in the granfilade and the allocator position has advanced, but `find_links` would not yet find the link because the spanfilade entry does not yet exist.

---

### Why external observers cannot see it

Per [INV-ATOMICITY] and [INV-SEQUENTIAL-DISPATCH], the `bed.c` event loop is single-threaded and runs each FEBE operation to completion before returning to `select()`. No other session or operation can interleave with `docreatelink` mid-execution. From any external client's view, the three-step sequence is atomic: either all three steps have completed or none of them have.

---

### The allocator update is NOT atomic with the deposit against crashes

Per [INV-DUAL-ENFILADE-CONSISTENCY]:

> "there is no transactional mechanism documented — if the sequence is interrupted partway, the enfilades can desynchronize."

A crash between steps 1 and 3 would leave the granfilade containing a link orgl at its allocated I-address (advancing `n_s`) while the spanfilade has no corresponding endpoint index. The link would be unreachable via `find_links` but the I-address slot would be permanently consumed. Per [EC-CRASH-MID-WRITE], the system has no recovery mechanism for this state.

---

### Allocator-state independence from the deposit

The allocator's state (`findpreviousisagr` returning the new maximum) is updated when the granfilade B-tree node is written in step 1 [SS-ADDRESS-SPACE, Finding 0061]:

> "the allocation is purely derived from current tree state — there is no cached 'next available' pointer"

This means a subsequent text INSERT after a `docreatelink` step 1 (hypothetically, in a crashed/resumed state) would allocate above the link orgl's I-address, creating an I-address gap — the same phenomenon documented in [INT-LINK-INSERT, Finding 0063] for interleaved CREATELINK/INSERT sequences.

---

### Summary

| Property | Holds? |
|---|---|
| External atomicity (concurrent sessions) | **Yes** — run-to-completion event loop [INV-ATOMICITY] |
| Internal intermediate states exist | **Yes** — granf updated before spanf, no rollback [ST-CREATE-LINK] |
| Crash-safe atomicity | **No** — no transaction log [INV-DUAL-ENFILADE-CONSISTENCY, EC-CRASH-MID-WRITE] |
| Allocator advances before deposit completes | **Yes** — `createorglingranf` runs before `insertendsetsinspanf` |

---

## Code Exploration

I have all the code I need. Here is the complete analysis.

---

## Atomicity of Allocator-State Evolution vs. Link-Store Deposit in udanax-green

### 1. The Complete Call Chain for `docreatelink`

**`docreatelink` [do1.c:195–221]** executes an `&&`-chained sequence:

```
do1.c:209  createorglingranf(taskptr, granf, &hint, linkisaptr)
do1.c:210  tumbler2spanset(taskptr, linkisaptr, &ispanset)
do1.c:211  findnextlinkvsa(taskptr, docisaptr, &linkvsa)
do1.c:212  docopy(taskptr, docisaptr, &linkvsa, ispanset)
do1.c:213  findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
do1.c:214  specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
do1.c:215  specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
do1.c:216  specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
do1.c:217  setlinkvsas(&fromvsa, &tovsa, &threevsa)
do1.c:218  insertendsetsinorgl(taskptr, linkisaptr, link, ...)
do1.c:219  insertendsetsinspanf(taskptr, spanf, linkisaptr, ...)
```

The "link-store deposit" proper is **do1.c:219 `insertendsetsinspanf`** — the call that makes the link findable by endpoint in the spanfilade. The allocator-state evolution is the `cwid.dsas[WIDTH]` propagation up the L1c chain inside `insertseq`, called from `createorglingranf` at do1.c:209.

These are separated by **nine other function calls** (do1.c:210–218). They are demonstrably not atomic with each other.

---

### 2. The Allocator-State Read and ISA Computation

**`createorglingranf`** [granf1.c:50–55] delegates immediately to **`createorglgr`** [granf2.c:111–128]:

```c
// granf2.c:117
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
// granf2.c:120–124: set up locinfo (GRANORGL, create POOM enf)
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);          // granf2.c:120
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);              // granf2.c:125
```

**`findisatoinsertgr`** [granf2.c:130–156] — for a LINKATOM — calls **`findisatoinsertmolecule`** [granf2.c:158–181]:

```c
// granf2.c:162–163: compute address bounds
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
clear (&lowerbound, sizeof(lowerbound));
// granf2.c:164: READ current allocator state from the tree
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
// granf2.c:170–175: LINKATOM branch — compute new ISA
if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound, 0, 1, isaptr);
}
```

**`findpreviousisagr`** [granf2.c:255–278] traverses the tree, accumulating `cwid.dsas[WIDTH]` values from sibling crums along the path:

```c
// granf2.c:274–276: for each sibling to the left of the descent path:
tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
```

This is the **allocator-state read** — it reads `n_s` (the accumulated width) at each node on the L1c chain. The ISA is computed from this accumulated value. **This read happens entirely before any mutation of the tree.**

---

### 3. Intermediate States Within `insertseq`

After the ISA is computed, **`insertseq`** [insert.c:17–70] executes the deposit. It does so in stages that are **not atomic**:

```c
// insert.c:28: find the insertion-point crum
context = retrievecrums (fullcrumptr, address, WIDTH);
ptr = context->corecrum;

// insert.c:44–46: FIRST MUTATION — structural deposit
reserve ((typecorecrum*)ptr);
new = createcrum (0,(INT)ptr->cenftype);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);      // << new crum linked into sibling chain

// insert.c:47–48: split check BEFORE widths updated
ivemodified (new);
splitsomething = splitcrumupwards (findfather (new));  // << may structurally rebalance

// insert.c:49–51: set internal pointer for GRANORGL
if (info->infotype == GRANORGL)
    info->granstuff.orglstuff.orglptr->leftbroorfather = new;

// insert.c:52–59: write content and adjust sibling's width field
moveinfo (info, &((typecbc *)new)->cinfo);
// ... ptr->cwid.dsas[WIDTH] adjusted here ...

// insert.c:61–63: SECOND MUTATION — width propagation up L1c chain
ivemodified ((typecorecrum*)ptr);
setwispupwards (findfather ((typecorecrum*)ptr), 0);  // << n_s update, no assertion
setwispupwards (findfather ((typecorecrum*)new),  1);  // << n_s update + tree assert
```

**`setwispupwards`** [wisp.c:83–111] walks up the tree from the insertion point, calling `setwisp` / `setwidseq` [wisp.c:150–168] on each ancestor. `setwidseq` recomputes a parent's `cwid.dsas[WIDTH]` by summing all children's `cwid` values:

```c
// wisp.c:160–166
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr))
    widopseq (&sum, &ptr->cwid, &sum);
movewisp (&sum, &father->cwid);   // << writes n_s for this level
```

The gap between `adopt()` [insert.c:46] and the two `setwispupwards` calls [insert.c:62–63] is the **internal intermediate state**: the new crum exists in the sibling chain, its content is written (`moveinfo`, insert.c:52), but no ancestor's `cwid.dsas[WIDTH]` has been updated yet. Any tree traversal that reads `cwid.dsas[WIDTH]` at an ancestor node during this window would see the pre-insertion width value.

---

### 4. Intermediate States Between Granfilade Deposit and Spanfilade Link-Store Deposit

At the `docreatelink` level, once `createorglingranf` [do1.c:209] returns:

- The granfilade has a new crum at `*linkisaptr` with `infotype = GRANORGL` and a fresh empty POOM enfilade [granf2.c:119–126].
- `linkisaptr` has been set to the newly allocated ISA.
- The L1c chain widths (`n_s`) are fully propagated — `setwispupwards` has returned.

But the link is **not findable** in the spanfilade yet. That requires `insertendsetsinspanf` [do1.c:219]. Between do1.c:209 and do1.c:219, nine operations execute, including `docopy` [do1.c:212] (which records the link's virtual-space address in the document's POOM) and `insertendsetsinorgl` [do1.c:218] (which writes the endpoint sporgl-sets into the link's own orgl). Both of these deposit data into the tree structures, each with their own internal `setwispupwards` propagation sequences, creating further intermediate states in the granfilade and POOM structures.

A hypothetical read of `findlinksfromtothreesp` after do1.c:209 but before do1.c:219 would traverse the spanfilade and find nothing — the link slot exists in the granfilade but has no spanfilade index entry.

---

### 5. Why This Is Not Externally Observable

**`bed.c`** runs a single-process, non-threaded event loop. The main loop uses `select()` [bed.c:74] to gate on incoming FEBE requests. One request is processed fully to completion before the event loop returns to `select()`. There is no preemption, no threading, and no concurrent request processing. The intermediate states described above exist only **within the execution of a single request handler**. No external query can observe them.

---

### Conclusion

**No, the allocator-state evolution is not atomic with the link-store deposit.** There are at least two classes of intermediate state:

1. **Within `insertseq` [insert.c:46–63]**: `adopt()` splices the new crum into the tree before `setwispupwards` propagates `n_s` updates up the L1c chain. During the window between those calls, any `findpreviousisagr` traversal reads stale (pre-insertion) `cwid.dsas[WIDTH]` values at ancestor nodes. If a second `findisatoinsertmolecule` call ran during that window it could compute a duplicate ISA. Conversely, the immediately preceding `splitcrumupwards` call [insert.c:48] may rebalance tree structure before the width accounting is corrected — a further intermediate.

2. **Between `createorglingranf` [do1.c:209] and `insertendsetsinspanf` [do1.c:219]**: The link's granfilade slot is fully allocated and the L1c widths updated, but the link is invisible to spanfilade queries for its entire construction phase. `insertendsetsinorgl` [do1.c:218] also introduces intermediate POOM state where endpoint sporgl-sets are partially deposited.

Both categories of intermediate state are **inert in practice** because udanax-green is strictly single-threaded — the event loop never re-enters the tree between these operations. But they are structurally observable intermediate states in the in-memory enfilade representation. The implementation trades atomicity for simplicity, relying entirely on the single-threaded execution model as its isolation guarantee.
