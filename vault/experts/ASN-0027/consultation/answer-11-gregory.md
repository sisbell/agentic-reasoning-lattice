## Question 11 [gregory]

> When `findisatoinsertmolecule` allocates a new I-address as max+1, is there any scenario — concurrent sessions, CREATELINK interleaving, or version creation — where two distinct content insertions could receive the same I-address?

## KB Synthesis

No. Two distinct content insertions cannot receive the same I-address. Here is the synthesis:

## The Allocation Mechanism

`findisatoinsertmolecule` is stateless — it queries the granfilade tree for the current maximum I-address via `findpreviousisagr`, then returns max+1 [SS-ADDRESS-SPACE, Finding 0061]. There is no cached counter; allocation is a pure function of the in-memory granfilade state at call time.

## Why Collision Is Impossible

**1. Sequential dispatch eliminates interleaving.**

The `bed.c` event loop processes every FEBE operation via run-to-completion scheduling. `xanadu(&task)` — which includes request parsing, the full `doXXX` path (allocation + granfilade write + POOM update), response emission, and cleanup — completes entirely before `select()` is called again [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH, Finding 0042].

Even when multiple sessions have simultaneous pending requests, the loop iterates over ready file descriptors sequentially. Session A's INSERT runs to completion — including writing the new I-address into the granfilade — before session B's INSERT begins. When B calls `findpreviousisagr`, it reads the live in-memory granfilade and sees A's I-address as the new maximum. B allocates max+1, which is strictly greater.

**2. I-addresses are never reused.**

The granfilade is append-only. DELETE and REARRANGE modify only the POOM (V-to-I mappings) and never touch the granfilade [FC-GRANF-ON-DELETE, Finding 0061]. Since `findpreviousisagr` returns the highest I-address present in the granfilade — including those of content deleted from V-space — no gap created by deletion can be filled by a subsequent allocation [INV-NO-IADDR-REUSE].

**3. CREATELINK does not cause collision — only non-contiguity.**

CREATELINK allocates a link orgl I-address from the same granfilade via `createorglingranf`. This advances the allocation ceiling, so a subsequent text INSERT receives an I-address above the link orgl's — creating a gap in the text I-address subsequence [INT-LINK-INSERT, Finding 0063]. But because CREATELINK runs to completion atomically before any subsequent INSERT begins, the two allocations are strictly ordered and cannot produce the same value. Contiguity is broken; uniqueness is not.

**4. CREATENEWVERSION is irrelevant.**

VERSION allocates only a document address (via `findisatoinsertnonmolecule` for non-molecules). It does NOT call `findisatoinsertmolecule` or any content I-address allocator [ST-VERSION, Finding 0077]. It leaves the content allocation ceiling untouched, so it cannot interfere with text I-address allocation at all.

## Summary

| Scenario | Can it cause I-address collision? | Why |
|---|---|---|
| Concurrent sessions | No | Sequential dispatch: operations never interleave |
| CREATELINK interleaving | No | CREATELINK completes atomically before next INSERT; only breaks contiguity |
| Version creation | No | Does not allocate content I-addresses |
| DELETE between INSERTs | No | Granfilade is append-only; max only increases |

The monotonic invariant `∀ alloc_a, alloc_b : time(a) < time(b) ⟹ iaddr(b) > iaddr(a)` holds unconditionally [INV-MONOTONIC]. Combined with sequential dispatch [INV-SEQUENTIAL-DISPATCH] and no I-address reuse [INV-NO-IADDR-REUSE], uniqueness of allocated I-addresses is guaranteed across all scenarios.

---

## Code Exploration

I now have everything needed. Here is the complete analysis.

---

## Can `findisatoinsertmolecule` Produce Duplicate I-Addresses?

**Short answer: No.** Three independent properties of the implementation jointly guarantee uniqueness. Here is the proof from source.

---

### 1. The Event Loop Is Strictly Single-Threaded

`bed.c:103-143` shows the main loop:

```c
for (;;) {
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                ...
                xanadu(&task);          // [bed.c:128]
```

`xanadu()` at `bed.c:153-172` processes **one request to full completion** — including `sendresultoutput` — before the outer `for` loop re-enters `select`. There are no OS threads, no coroutines, and no preemption. The global `int user` at `bed.c:28` is a single value, not per-thread.

**Consequence:** No two invocations of `findisatoinsertmolecule` from different sessions can interleave. "Concurrent sessions" in this backend means *multiplexed serial*, not parallel.

---

### 2. Allocation Is Immediately Committed to the Enfilade Before Any Return

`findisatoinsertmolecule` is the allocation function. Its two callers — `inserttextgr` and `createorglgr` — both call `insertseq()` as the very next operation after the allocation completes:

**`createorglgr` [granf2.c:111-128]:**
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
...
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);  // ← immediate commit
```

**`inserttextgr` [granf2.c:92-101]:**
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);
for (; textset; textset = textset->next) {
    ...
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);  // ← immediate commit
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // advance, not re-allocate
}
```

Note that multi-chunk text insertions do not re-call `findisatoinsertmolecule` — `lsa` is incremented directly and `insertseq` is called for each chunk. So there is no re-entry into the allocator within a single `inserttextgr` call.

**`insertseq` [insert.c:17-60]** modifies the in-memory enfilade tree immediately:

```c
reserve ((typecorecrum*)ptr);
new = createcrum (0,(INT)ptr->cenftype);
reserve (new);
adopt (new, RIGHTBRO, (typecorecrum*)ptr);
ivemodified (new);
splitsomething = splitcrumupwards (findfather (new));
...
moveinfo (info, &((typecbc *)new)->cinfo);
```

This is entirely synchronous in-memory tree restructuring. There is no write buffer, no journal, no deferred phase. The node is inserted into the live tree before `insertseq` returns.

---

### 3. `findpreviousisagr` Always Reads the Live In-Memory Tree

The "find max" step in `findisatoinsertmolecule` [granf2.c:164]:

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
```

`findpreviousisagr` [granf2.c:255-278] recursively traverses the enfilade using `findleftson` / `findrightbro` (via `genf.c`), which call `rejuvinate` to page in nodes from disk on demand. The in-memory tree is always the authoritative current state — any I-address committed via `insertseq` in a prior call is already in this tree and will be found as `lowerbound`, causing the next allocation to increment past it.

---

### 4. No Single Request Calls the Allocator Twice for the Same Namespace

Tracing every path that reaches `findisatoinsertmolecule` through the ATOM branch of `findisatoinsertgr` [granf2.c:135-143]:

| Request handler | Calls into allocator |
|---|---|
| `doinsert` [do1.c:87] | `inserttextingranf` once → `inserttextgr` → allocates text I-span; then `docopy` → `insertpm` + `insertspanf` (no allocator call) |
| `docreatelink` [do1.c:195] | `createorglingranf` once → `createorglgr` → allocates link orgl; then `tumbler2spanset`, `findnextlinkvsa`, `docopy` (no allocator call) |
| `docreatenewdocument` [do1.c:234] | `createorglingranf` once (DOCUMENT hint, non-ATOM path via `findisatoinsertnonmolecule`) |
| `docreatenewversion` [do1.c:260] | `createorglingranf` once; then `docopyinternal` → `insertpm` + `insertspanf` (no allocator call) |

No request triggers two ATOM-path allocations in the same document namespace without committing between them.

---

### 5. The LINKATOM Branch: Structurally Safe But Subtle

The LINKATOM allocation branch [granf2.c:170-175]:

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // base = doc.0.2
if (tumblercmp (&lowerbound, isaptr) == LESS)
    tumblerincrement (isaptr, 1, 1, isaptr);            // → doc.0.2.0.1
else
    tumblerincrement (&lowerbound , 0, 1, isaptr);      // → prev + {0:1}
```

Text atoms occupy `doc.0.1.x` and link atoms occupy `doc.0.2.x` (both are `tumblerincrement(&hintisa, 2, atomtype, ...)` where `TEXTATOM=1`, `LINKATOM=2`). When `lowerbound` is a text entry at `doc.0.1.x`, it is numerically LESS than `doc.0.2`, so the first link always lands at `doc.0.2.0.1`. Subsequent links find a `lowerbound` at `doc.0.2.x` which is GREATER-OR-EQUAL to the base, taking the `else` branch: `lowerbound + {0:1}`.

This is safe because `lowerbound` is freshly queried from the live tree each time.

---

### Conclusion

There is **no scenario** — including concurrent sessions, CREATELINK interleaving, or version creation — where two distinct content insertions receive the same I-address. The guarantee rests on three interlocking facts:

1. **Single-threaded serial dispatch** [`bed.c:103-143`]: The `select`-based event loop processes requests one at a time. "Concurrent sessions" means queued, not parallel.

2. **Immediate in-memory commit** [`granf2.c:99`, `granf2.c:125`]: `insertseq` places the allocated address into the live enfilade tree synchronously. When the next request runs, `findpreviousisagr` will find it.

3. **No re-entrant allocation within a request** [`do1.c:87-122`, `do1.c:195-220`]: Every request calls the allocator at most once per document namespace before committing. Subsequent operations (`insertpm`, `insertspanf`, `docopy`) work with already-allocated I-addresses and do not call `findisatoinsertmolecule`.

The only scenario that *could* produce a collision would require OS-level threading (absent: single process, no `pthread_create`) or a deferred allocation buffer (absent: `insertseq` is synchronous in-memory tree surgery). Neither exists in this codebase.
