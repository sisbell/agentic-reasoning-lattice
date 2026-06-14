## Question 19 [evidence]

> Are the dense contiguous allocation chains of `SS-IADDRESS-ALLOCATION`/`ASN-0093` a property of the data model itself, or do they hold only because the single event loop serializes every query-and-increment — i.e., would a truly concurrent allocator break contiguity even with unique addresses preserved?

## KB Synthesis

## Contiguity: Data Model Property vs. Serialization Artifact

**Short answer**: Contiguity is an artifact of serialization, not a data model property. A truly concurrent allocator would break contiguity of type-specific subsequences even while preserving uniqueness and global monotonicity.

---

### What the data model actually guarantees

The allocation invariants in the KB are layered:

- **INV-MONOTONIC** [SS-ADDRESS-SPACE Finding 0061]: Every allocation is strictly greater than all prior allocations. This is guaranteed at the abstract level and holds regardless of concurrency if uniqueness is enforced.
- **INV-NO-IADDR-REUSE** [SS-ADDRESS-SPACE Finding 0061]: Once allocated, addresses are permanent. The granfilade is append-only.
- **Contiguity of text I-addresses** [SS-ADDRESS-SPACE Finding 0033]: Sequential single-character inserts produce a *single contiguous I-span*. This is presented as a property of the allocation mechanism, not the abstract data model.

The data model only specifies the first two. Contiguity is what falls out when you apply the allocation rule (`findpreviousisagr` + increment-by-1) with no interleaving.

---

### The serialization does the work

[INV-SEQUENTIAL-DISPATCH Finding 0042] establishes the mechanism: the `bed.c` event loop processes each FEBE operation atomically via run-to-completion scheduling — no threads, no preemption. Each INSERT executes all four internal steps (allocate I-address, insert text, insert DOCISPAN, update POOM) before any other operation can query the granfilade.

[SS-ADDRESS-SPACE Finding 0061] makes the allocation's statelessness explicit: `next_iaddr(granf) = max_iaddr(granf) + 1`, a pure function of current tree state with no session-local counter. Because the event loop ensures no other allocation runs between `findpreviousisagr` and the write, each text insert finds the previous text insert's address as the maximum and allocates exactly one above it.

---

### Contiguity breaks even in single-threaded operation

The crucial counterexample is already in the KB. [INT-LINK-INSERT Finding 0063] shows that CREATELINK — even in the fully serialized single-threaded model — breaks text I-address contiguity:

- INSERT "ABC" → allocates I.1, I.2, I.3
- CREATELINK → link orgl allocated at ~I.2.0 (same granfilade allocation path via `createorglingranf`)
- INSERT "DEF" → `findpreviousisagr` returns the link orgl's I-address as maximum → allocates at I.2.1+

Result: `compare_versions` reports **two** shared span pairs, not one. The text addresses are non-contiguous because they share the allocation namespace with non-text entities.

[SS-ADDRESS-SPACE Finding 0077] confirms this explicitly: "There is no single global 'next' counter (no Σ.next). Allocation is a family of independent functions partitioned by tumbler range." Both text molecules (`findisatoinsertmolecule`) and document orgls (`findisatoinsertnonmolecule`) query the same physical granfilade tree, just with different search bounds.

---

### What a concurrent allocator would break

[PRE-CONCURRENT-INSERT Finding 0041] establishes that concurrent insertion is structurally unsafe (pointer races in `adopt`, lost updates in `father->numberofsons`). [INV-ENFILADE-CONFLUENCE Finding 0041] adds that logical confluence holds — same query results regardless of serialization order — but only at the abstraction boundary, not at the physical tree level.

Suppose we fixed the structural races (with CAS or locks). Two concurrent text inserts from different sessions would both call `findpreviousisagr`, both see max = I.10, and race to allocate I.11. With proper synchronization, one wins I.11 and the other retries and gets I.12 — **still contiguous** for that pair. But:

1. If a third concurrent CREATELINK runs between the two text inserts, the link orgl claims an address in the text range, and the second text insert allocates above it — **gap created**, exactly as in the single-threaded CREATELINK case.
2. Concurrent inserts across *different documents* would have their own per-document bounds (Finding 0065 for links, Finding 0077 for content), so they wouldn't collide on addresses — but they'd interleave in the shared allocation tree, and the relative ordering of their allocations would be indeterminate.

The data model therefore provides:
- **Uniqueness**: guaranteed by allocation semantics (each allocation is strictly above the current maximum)
- **Global monotonicity**: guaranteed — INV-MONOTONIC holds per-document, per-element-type
- **Contiguity of text-only subsequences**: NOT guaranteed — this requires that no non-text allocation interleaves, which the event loop provides but the data model does not specify

---

### Summary

Contiguous I-address allocation for text is a property of **uninterrupted same-type sequential allocation under the run-to-completion event loop**. The data model specifies only monotonicity and uniqueness. Even in the current single-threaded implementation, CREATELINK can break text contiguity [Finding 0063]. A truly concurrent allocator would preserve uniqueness and global monotonicity but would lose text-contiguity whenever allocations of different types (or the same type from concurrent sessions) interleave in the shared granfilade tree.

---

## Code Exploration

Now I have all the pieces. Let me compile the complete answer.

---

## Are Dense Contiguous I-Address Chains a Data Model Property or a Serialization Artifact?

**Short answer:** The chains are an emergent product of two cooperating mechanisms. Monotonicity and uniqueness are data-model properties that would survive a properly-serialized concurrent allocator. Dense contiguity — no gaps between consecutive same-session INSERTs — is a serialization artifact that would break under true concurrency even if unique addresses were preserved.

---

### The Allocator Mechanism

The allocation sequence lives in `findisatoinsertmolecule` at `backend/granf2.c:158-181`:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);   // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);        // line 164
    ...
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);  // line 169 — lowerbound + 1
```

Three steps: (1) compute an upper bound for this subspace, (2) traverse the granfilade tree to find the highest existing I-address below that bound, (3) add 1 to produce the next address. The result is immediately inserted into the tree by `insertseq` (`granf2.c:99`) before `inserttextgr` returns.

There is no counter, no free list, no lock. The "current maximum" is a read from the live tree state, not a cached variable.

---

### What Is a Data Model Property

**Monotonicity** is a data model property: `alloc(n+1) > alloc(n)` for all n. This follows directly from the `findpreviousisagr → +1` formula. As long as each individual allocation is serialized (the `findpreviousisagr` read and the `insertseq` write complete atomically as a unit), subsequent allocations will always exceed prior ones.

**No reuse** is a data model property: the granfilade is write-only for content. `deletevspanpm` in `edit.c` modifies only the spanfilade — the granfilade entry at the deleted I-address remains permanently. `findpreviousisagr` will always find it as a candidate for the maximum. Deleted addresses continue to "push" subsequent allocations forward forever. This is confirmed in `kb-analysis/0061.md` (INV-NO-IADDR-REUSE) and verified by the `interleaved_insert_delete` golden test.

**Within-subspace isolation** is a data model property: the `upperbound` computation uses `atomtype + 1` as a separator. For `TEXTATOM=1` (`xanadu.h:145`), text allocation searches below `hintisa.0.2` — only the text subspace. For `LINKATOM=2`, link allocation searches below `hintisa.0.3`. These bounds are encoded in the allocator logic, not in runtime state.

---

### What Depends on Serialization

**Dense contiguity within a single session** depends entirely on the event loop serializing all requests.

The `bed.c` main loop:

```c
// bed.c:111-140
if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) {
    ...
} else {
    for (i = 0; i <= nfds; i++) {
        if ((1<<i) & inputfds2) {
            user = fdtoplayer[i];
            task.inp = player[user].inp;
            ...
            xanadu(&task);     // line 128 — ONE complete request, then loop continues
```

`select()` collects a bitmask of ALL ready file descriptors. The for loop then processes every ready FD sequentially: `xanadu()` is called for FD[i] and runs to completion before FD[i+1] is touched. There is no threading, no preemption, no concurrent access to the granfilade. Even if ten clients send requests at the same instant, the backend serializes them into a queue that the single event loop drains one at a time.

Within this constraint, Session A's INSERT-1 and INSERT-2 are guaranteed to be adjacent in the global processing order unless Session A itself interposes an operation. No other session can inject an allocation between them.

---

### Why a Concurrent Allocator Would Break Contiguity

The `findpreviousisagr → insertseq` sequence has **no atomic wrapper**. There is no CAS, no mutex, no lock around lines 164 and 99 of `granf2.c`.

**Collision scenario (no serialization):**
1. Session A: `findpreviousisagr` returns max = N
2. Session B: `findpreviousisagr` returns max = N (before A has written)
3. Session A: `insertseq` at N+1
4. Session B: `insertseq` at N+1 → **collision**, two entries at the same I-address

This breaks uniqueness entirely. The single event loop is what prevents this.

**Gap scenario (serialized per-allocation CAS, but not per-session serialization):**

Even with a proper compare-and-swap making each individual allocation atomic:

1. Session A: INSERT-1 → allocates N+1
2. Session B: INSERT → allocates N+2 (interleaved between A's two INSERTs)
3. Session A: INSERT-2 → allocates N+3 (not N+2)

Session A's allocation chain is now `{N+1, N+3}` — monotonic and unique, but not dense. The `isanextensionnd` check at `insertnd.c:250-258` would fail for Session A's second insert:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc*)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));  // reach == origin?
}
```

The check `reach == origin` (the existing crum's I-end equals the new insertion's I-start) would fail because Session B filled N+2. The coalescing that produces single I-spans from sequential single-char inserts — the behavior documented in SS-IADDRESS-ALLOCATION as "sequential single-character inserts produce contiguous I-addresses that consolidate into one I-span" — would break. Session A would now accumulate two separate POOM crums instead of one extended crum, raising crum count beyond the `c ≤ 1 + 2C + 3R + 3P` bound.

---

### The CREATELINK Gap Is an Intra-Session Exception That Proves the Rule

Even within the fully serialized system, there is one known source of gaps: CREATELINK. The golden test `insert_link_insert_iaddress_gap.json` shows INSERT "ABC" → CREATELINK → INSERT "DEF" produces two I-span ranges instead of one contiguous range. The link orgl allocation advances the granfilade state, and `findpreviousisagr` for the next text INSERT finds a higher maximum than the last text character, producing a gap (finding 0063, `do1.c:207-209`):

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf (taskptr, granf, &hint, linkisaptr)
```

This gap exists DESPITE perfect serialization — it is caused by the allocator's stateless query seeing the link's granfilade entry when computing the next text address. This is the one case where the data model itself produces non-dense chains: the link's I-address lands within or adjacent to the search range used by subsequent text allocation, even though the two subspaces are nominally separated by the `atomtype`-based upper bounds.

This exception also demonstrates that the dense chains in the CREATELINK-free case are NOT a deeper structural invariant — they are a consequence of the absence of interleaving allocations, whether that absence is enforced by the event loop (across sessions) or simply by the absence of cross-type operations (within a session).

---

### Summary

| Property | Source | Survives True Concurrency? |
|---|---|---|
| I-addresses always increase | Data model: `findpreviousisagr + 1` | Yes, with per-allocation atomics |
| Deleted I-addresses never reused | Data model: granfilade is write-only | Yes |
| Text/link subspace isolation | Data model: `upperbound = hintisa.0.(atomtype+1)` | Yes |
| Dense chains (no inter-session gaps) | Serialization: `bed.c:128` sequential `xanadu()` | **No** — would break |
| No I-address collision | Serialization: `bed.c:128` (no atomics in allocator) | **No** — would produce collisions, not just gaps |
| `isanextensionnd` coalescing | Serialization: each insert completes before next begins | **No** — concurrent inserts would fail coalescing |

The dense contiguous chains observed in SS-IADDRESS-ALLOCATION hold because the single event loop makes the `findpreviousisagr → insertseq` pair effectively atomic at the system level. A truly concurrent allocator — even one that preserved unique addresses via CAS — would allow foreign allocations to interpose between any session's consecutive INSERTs, producing monotonically-increasing but non-dense chains, and breaking the `isanextensionnd` coalescing that consolidates them into single I-spans. The data model guarantees ordering and permanence; the event loop at `bed.c:128` guarantees density.
