## Question 12 [gregory]

> When `findisatoinsertmolecule` computes the next I-address as max+1, does the system guarantee that a failed or partially-completed INSERT (e.g., process crash mid-operation) can never leave the granfilade in a state where the same I-address could be allocated twice on restart?

## KB Synthesis

## Analysis: I-Address Double-Allocation After Failed INSERT

The short answer: **the system cannot guarantee against re-allocation of I-addresses that were partially written to disk but not integrated into the reachable tree.** However, this does not corrupt any committed state.

---

### The Allocation Mechanism Is Reachability-Bounded

`findisatoinsertmolecule` works by querying the granfilade tree via `findpreviousisagr` — a tree traversal from the root finding the highest existing I-address in a bounded subtree [SS-ADDRESS-ALLOC, Finding 0061]. Critically:

> "The allocation is purely derived from current tree state — there is no cached 'next available' pointer."

This means **the allocator only sees I-addresses reachable from the root**. Orphaned crums (written to disk but whose parents weren't updated) are invisible to it.

---

### Three Failure Scenarios

**Scenario 1: Crash before any eviction (crum in RAM only)**

INSERT allocates I.5 in an in-memory crum. Crash occurs. RAM lost. On restart, `findpreviousisagr` scans the on-disk tree, which never received the I.5 allocation. Next INSERT re-allocates I.5.

This is **semantically correct**: the first allocation was never committed. Re-use is not a violation — there is no prior committed data at I.5.

**Scenario 2: Crash during partial disk write** [EC-CRASH-MID-WRITE]

`subtreewriterecurs` writes bottom-up. If Leaf (with I.5) is written to disk but the parent isn't updated before crash:

- The on-disk root still references the old tree
- The new leaf is on disk but orphaned (unreachable from root)
- On restart, `findpreviousisagr` traverses the OLD reachable tree
- I.5 is not found → it is re-allocated by the next INSERT

This **violates INV-NO-IADDR-REUSE** in the raw disk sense — I.5 occupies a disk block and also gets freshly allocated. But:
- The orphaned block's data is inaccessible (no root path leads to it)
- The only live allocation of I.5 is the new one
- No simultaneously-reachable state ever contains I.5 twice

**Scenario 3: Grim reaper evicts completed subtrees** [SS-CACHE-MECHANISM, EC-CROSS-ENFILADE-EVICTION]

If the grim reaper evicted a completed subtree (all levels including parent updates written) before the crash, the I-address is fully integrated into the reachable tree and `findpreviousisagr` will find it. No re-allocation occurs. This is the safe case.

---

### What the System Lacks to Prevent This

- **No transaction log**: There is no write-ahead journal to roll back partial writes [SS-DURABILITY-BOUNDARY]
- **No startup validation**: `initenffile` loads whatever is on disk with no consistency check [EC-NO-STARTUP-VALIDATION]
- **No fsync**: `write()` syscalls go to OS buffers without forced sync [SS-DURABILITY-BOUNDARY]
- **No atomic multi-block commit**: The bottom-up write order is a partial mitigation but not a guarantee [EC-CRASH-MID-WRITE]

---

### The Precise Invariant

INV-NO-IADDR-REUSE [Finding 0061] holds **only over reachable I-addresses**:

> "Deleted I-addresses are never reused... the granfilade is never modified by DELETE, and allocation always queries the granfilade for the current maximum."

The invariant is conditional on the granfilade being in a consistent state. After a crash mid-write, the reachable granfilade tree is the **last fully-committed state**, and within that state the invariant holds. An I-address that exists only in an orphaned (unreachable) crum is effectively uncommitted and may be re-allocated — but this produces no logical duplication in the committed address space.

The system provides **session-level durability** (all-or-nothing at clean shutdown), not **operation-level durability** (each INSERT atomically committed). The re-allocation risk exists only in the gap between those two granularities.

---

## Code Exploration

I now have all the information needed to answer the question definitively. Let me trace every link in the chain.

---

## Answer

**No, the system does not guarantee this. A crash between I-address allocation and disk flush can cause the same I-address to be allocated twice across restarts.** Here is the full trace.

---

### 1. How `findisatoinsertmolecule` allocates an I-address

`findisatoinsertmolecule` [granf2.c:158-181] works by querying the **live in-memory granfilade**:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);  // [granf2.c:164]
    ...
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);  // max + 1  [granf2.c:169]
    }
```

`findpreviousisagr` [granf2.c:255-278] traverses the in-memory enfilade tree to find the highest existing I-address below `upperbound`. The returned `lowerbound` is that highest address. The new address is `lowerbound + (0, 1)` — i.e., max+1 **from whatever the tree currently holds in memory**.

The caller `inserttextgr` [granf2.c:83-109] then passes this address to `insertseq` [granf2.c:99] which modifies the in-memory tree.

`insertseq` [insert.c:17-70] calls `ivemodified()` at lines [insert.c:39, 47, 61] to flag the modified crums. `ivemodified` [genf.c:522-544] sets `ptr->modified = TRUE` and propagates it upward through `leftbroorfather` links.

**At this point the mutation is entirely in memory. No disk write has occurred.**

---

### 2. The persistence model: batch checkpointing, no WAL

The only functions that write in-memory state to disk are:

- **`writeenfilades()`** [corediskout.c:68-88] — writes the granfilade and spanfilade to disk at fixed locations (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`). It calls `orglwrite()` → `subtreewriterecurs()` which walks nodes with `modified == TRUE`.
- **`diskflush()`** [corediskout.c:58-64] — calls `writeenfilades()`.

These are called only at specific moments:

```c
// bed.c:105 — only when no frontend is connected:
if (n_players < 1) {
    diskflush();
```
```c
// bed.c:134 — on QUIT after current request finishes:
writeenfilades();
closediskfile();
exit(0);
```
```c
// bed.c:183 — on SIGINT, only if mightbeblocked:
writeenfilades();
closediskfile();
exit(0);
```
```c
// corediskout.c:44 — on normal single-user exit via diskexit():
writeenfilades();
```

**There is no write-ahead log. There is no per-operation fsync. There is no journaling.** Every INSERT, COPY, or CREATELINK modifies the in-memory tree and returns; the disk is only updated in bulk on the above events.

---

### 3. What happens on restart

On startup, `initmagicktricks()` [entexit.c:41-46] calls `initkluge()` [corediskin.c:18-41] if a disk file exists:

```c
void initkluge(typecuc **granfptr, typecuc **spanfptr)
{
    tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
    inorgl (tempcbc);           // reads granf from disk
    *granfptr = tempcbc->cinfo.granstuff.orglstuff.orglptr;
```

`inorgl` → `inorglinternal` [corediskin.c:175-231] deserializes the on-disk loaf into fresh in-memory crums. Crucially, at [corediskin.c:148] in `varunpackloaf` and [corediskin.c:223] in `inorglinternal`:

```c
ptr->modified = FALSE;   // [corediskin.c:148, 223]
```

The restored tree **only reflects what was last written to disk**. Any in-memory mutations from the previous session that were not flushed are gone.

---

### 4. The crash scenario: duplicate I-address

Here is the precise failure sequence:

1. **Session A**: Granfilade on disk has highest text I-address = N−1. Process starts; `initkluge()` loads this state.
2. INSERT arrives. `findisatoinsertmolecule` calls `findpreviousisagr` on the in-memory tree → `lowerbound = N−1`. Returns `isaptr = N`.
3. `insertseq` [granf2.c:99] adopts a new bottom crum at address N into the in-memory tree. `ivemodified()` marks it dirty.
4. **Process crashes** (SIGKILL, segfault, power failure) — `writeenfilades()` never runs.
5. **Session B starts**. `initkluge()` reads from disk. Disk still has N−1 as highest address (N was never written).
6. Another INSERT arrives. `findisatoinsertmolecule` → `findpreviousisagr` on the freshly-loaded tree → `lowerbound = N−1` → `isaptr = N`.
7. **Address N is allocated again for different content.** The previous use of N is lost; the new use of N occupies the same I-address.

---

### 5. The `putinsert`-before-`doinsert` aggravation

In `fns.c:84-98`, the INSERT handler has this ordering:

```c
void insert(typetask *taskptr)
{
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);           // response sent BEFORE operation [fns.c:91]
    if (!doinsert (taskptr, &docisa, &vsa, textset)) ...
}
```

Compare the commented-out original version [fns.c:69-82] and the pattern used by `createnewdocument`, `createnewversion`, `createlink` — all of which send the response *after* the operation completes. The current `insert` sends `putinsert` before `doinsert`, meaning the client's acknowledgment window precedes even the in-memory write, further decoupling protocol-level confirmation from durable state.

---

### 6. Within-session safety (no concurrent hazard)

Within a single uninterrupted session, allocations are safe. The event loop in `bed.c:103-148` processes one request per `select()` iteration [bed.c:118-142]. `findpreviousisagr` always queries the live tree, which already contains the address allocated by the prior `insertseq`. No two concurrent insertions can read the same `lowerbound`.

---

### Summary

The system provides **no crash-safety guarantee** for I-address uniqueness across restarts. The failure mode is structural:

| Property | What the code does |
|---|---|
| I-address source | Computed as `max(current in-memory tree) + 1` [granf2.c:164-169] |
| When memory → disk | Only on idle flush, QUIT, or SIGINT [bed.c:105, 134; corediskout.c:44] |
| On restart | In-memory tree rebuilt strictly from last disk state [corediskin.c:18-41] |
| Missing: | Write-ahead log, per-operation fsync, persistent address counter, crash recovery |

If the process is killed between `insertseq()` modifying the tree [insert.c:17] and `writeenfilades()` flushing it [corediskout.c:68], the allocated I-address exists nowhere on disk. On restart, `findisatoinsertmolecule` will compute the same max+1 and hand the identical I-address to new content. This is a fundamental property of the architecture: a memory-resident enfilade with periodic bulk checkpointing, not a durably-logged transactional store.
