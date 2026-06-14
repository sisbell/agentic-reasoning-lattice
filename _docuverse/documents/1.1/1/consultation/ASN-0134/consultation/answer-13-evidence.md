## Question 13 [evidence]

> At what exact point in the event loop does an operation's effect become visible to other FEBE sessions — at `insertnd`/`deletend` mutation time, at grim-reaper eviction, or only at session-end `writeenfilades` — i.e., where is the linearization point relative to `INT-MULTI-SESSION`?

## KB Synthesis

## Linearization Point for Inter-Session Visibility

The linearization point is at **`insertnd`/`deletend` mutation time** — specifically at the completion of the `xanadu(&task)` call that wraps the mutation. Grim-reaper eviction and `writeenfilades` are purely about disk durability, not inter-session visibility.

### Why Mutation Time Is the Linearization Point

Three structural facts from the KB combine to establish this:

**1. The in-memory enfilade IS the shared canonical state — not a per-session copy.**

[SS-CACHE-MECHANISM] states: "the in-memory enfilade tree IS the cache." There is no per-session state for document content. The global variables `granf` and `spanf` (typed `typegranf` / `typespanf`) are singletons shared across every concurrent connection [SS-SESSION-STATE] (Finding 0022: "Global state — enfilades, document storage, link storage, content identity/SPORGL — is shared across all connected sessions"). When `insertnd` writes a modified crum into this shared tree, that write is immediately in the shared address space.

**2. The event loop is strictly single-threaded with run-to-completion semantics.**

[INV-ATOMICITY] (Finding 0042): "`bed.c`'s event loop processes each FEBE operation atomically via run-to-completion scheduling. The `xanadu(&task)` call executes the entire operation — request parsing, state mutation, response sending, and memory cleanup — before returning to `select()`." [INV-SEQUENTIAL-DISPATCH]: "Even when multiple frontends have requests ready simultaneously, the event loop processes them strictly sequentially."

Therefore: there is no window during which a partially-executed mutation is visible. Either the full mutation (including all `insertnd`/`deletend` calls inside `xanadu`) has completed, or none of it has.

**3. The empirical confirmation from multi-session behavior.**

[ST-LINK-GLOBAL-VISIBILITY] (Finding 0022): "Links created in any session are immediately visible to all other sessions. `find_links()` from session B returns links created by session A without any synchronization or coordination step." No flush, no explicit sync — the visibility is immediate once session A's `xanadu()` returns.

### What Grim-Reaper Eviction and `writeenfilades` Govern

These two mechanisms are orthogonal to visibility; they govern **disk durability** only:

- **Grim-reaper eviction** ([SS-CACHE-MECHANISM], Finding 0059): When memory pressure occurs, crums with `age >= OLD` and `modified = TRUE` are written to disk and freed from RAM. This makes individual crums durable against crashes, but they were already visible to other sessions in-memory. The eviction may actually *remove* a crum from the shared cache, forcing subsequent sessions to re-read from disk — but the logical content is unchanged.

- **`writeenfilades()`** ([SS-DURABILITY-BOUNDARY], Finding 0059): Called only at daemon shutdown (`bed.c:134`). This is the "all-or-nothing at session boundary" durability guarantee. A crash before this call loses in-RAM modifications that weren't evicted. But all of those modifications were already visible to other sessions the moment they were written to the in-memory tree.

[ST-INSERT] (Finding 0059) states the postcondition precisely: "after INSERT, `RETRIEVE(addr)` returns the text (from cache), but `crash(); restart(); RETRIEVE(addr)` may fail." The cache-hit case is the inter-session case — visibility is from the cache, durability is from the disk.

### Summary

```
xanadu(&task) begins
  ↓
insertnd / deletend mutates in-memory crums         ← LINEARIZATION POINT
  (shared granf/spanf, no per-session isolation)
  ↓
xanadu(&task) returns, response sent to FE
  ↓
select() iterates to next ready FD
  ↓
Session B's xanadu() sees the mutation immediately  ← VISIBLE TO OTHER SESSIONS
  ↓
                    [later, opportunistic]
grim-reaper eviction → partial disk durability
                    [at daemon exit]
writeenfilades()  → full disk durability
```

The system provides **sequential consistency** for in-memory state: operations are totally ordered by the event loop, each operation's effects are atomically visible at completion, and no session ever observes a partial mutation. The durability story is weaker: session-boundary-level, not operation-level.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer:

---

## Linearization Point in INT-MULTI-SESSION: Full Analysis

### Architecture: One Process, One Thread, Shared Globals

The daemon is a **single Unix process running a single thread** [`bed.c:47`]. All sessions share one address space. The enfilade state lives in two global pointers:

```c
typegranf granf;   // corediskout.c:21
typespanf spanf;   // corediskout.c:22
```

These are the **only** copy of the enfilade in the system during normal multi-session operation. There is no per-session copy.

---

### The Event Loop (`bed.c:103–148`)

```c
for (;;) {
    if (n_players < 1) {
        diskflush();           /* bed.c:105 — write+reload when no sessions */
        new_players(..., TRUE, ...);
    }
    inputfds2 = inputfds;
    if (select(nfds+1, &inputfds2, 0, 0, &timeout) < 0) { ... }
    else {
        for (i = 0; i <= nfds; i++) {
            if ((1<<i) & inputfds2) {
                user = fdtoplayer[i];
                /* set up task for this session */
                xanadu(&task);     /* bed.c:128 — ONE request, then return */
                ...
            }
        }
    }
    leave(player, &n_players);
    new_players(..., FALSE, ...);
}
```

**Critical:** `xanadu()` is called sequentially for each ready file descriptor. The inner `for` loop over `i` continues to the next descriptor only after `xanadu()` returns for the current one. No other session's request can be dispatched until `xanadu()` has returned for the current session.

---

### The Dispatch: `xanadu()` (`bed.c:153–172`)

```c
int xanadu(typetask *taskptr)
{
    if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);   // handler from fns.c — does mutation AND response staging
        sendresultoutput(taskptr);          // putfe.c:85: fflush(taskptr->outp)
    }
    tfree(taskptr);
    ...
}
```

`sendresultoutput()` is a plain `fflush` [`putfe.c:85`]. It does not cause mutation. Mutations happen inside `(*requestfns[request])()`.

---

### Two Handler Patterns in `fns.c`

#### Pattern A — INSERT, DELETEVSPAN, REARRANGE

```c
void insert(typetask *taskptr)         // fns.c:84–98
{
    (void) getinsert(taskptr, &docisa, &vsa, &textset);
    putinsert(taskptr);           // fns.c:91 — stages opcode in FILE buffer
    if (!doinsert(taskptr, &docisa, &vsa, textset))  // fns.c:92 — MUTATES granf+spanf
        fprintf(stderr, "requestfailed in insert\n");
}
```

`putinsert()` writes `INSERT` opcode to `taskptr->outp` via `putnumber()` [`putfe.c:243–246`]. This is a **buffered** C FILE — nothing is flushed to the wire yet. The flush happens in `sendresultoutput()` back in `xanadu()`, which runs **after** `insert()` returns — and therefore **after** `doinsert()` has already mutated `granf`/`spanf`.

Same structure for `deletevspan()` [`fns.c:333–347`] and `rearrange()` [`fns.c:159–173`].

#### Pattern B — COPY, CREATELINK, CREATENEWVERSION, CREATENEWDOCUMENT

```c
void copy(typetask *taskptr)           // fns.c:35–47
{
    if (   getcopy(taskptr, &docisa, &vsa, &localspecset)
        && docopy(taskptr, &docisa, &vsa, localspecset))   // mutates first
        putcopy(taskptr);
    else
        putrequestfailed(taskptr);
}
```

Mutation before response staging. Same observable ordering as Pattern A because both patterns flush via `sendresultoutput()`.

---

### The Wire-Delivery Order (Both Patterns)

1. Parse request (`getX`)
2. **Mutate** `granf`/`spanf` in-core (`doX`)
3. `fflush` → client receives opcode on the wire (`sendresultoutput`)

This ordering holds for both patterns because `putX` writes only to a buffered FILE, and `sendresultoutput` is the sole flush point, called after the handler returns.

---

### The Linearization Point

**The exact linearization point is: the return of the mutation function (`doinsert`, `dodeletevspan`, `dorearrange`, `docopy`, etc.) inside `xanadu()`.**

From any other session's observable perspective, the linearization point is the **exit of `xanadu()`** — because:

1. `xanadu()` completes the entire request: parse → mutate → flush.
2. Only after `xanadu()` returns does the outer `for` loop in `main()` advance to the next ready file descriptor.
3. Therefore, no other session can receive service until the mutation is fully committed to `granf`/`spanf`.

This is a strict total order on requests: the single thread processes one at a time, and the in-core state after each `xanadu()` call is the consistent state visible to all subsequent calls from any session.

---

### The Grim Reaper: Not a Visibility Gate

The grim reaper (`grimlyreap()`, `credel.c:106–162`) is triggered by memory pressure inside `ealloc()` [`credel.c:70–75`]:

```c
INT *ealloc(unsigned nbytes)            // credel.c:54–77
{
    for (;;) {
        if (ret = allocfromqueue(...)) { return ret; }
        ret = falloc(...);
        if (ret) { return ret; }
        if (grimreaper == NULL) { xgrabmorecore(); continue; }
        grimlyreap();      // <-- triggered by memory pressure, not by request boundaries
    }
}
```

When triggered, `grimlyreap()` scans the crum ring list for a crum with `age >= OLD` and `age != RESERVED` [`credel.c:144–159`]. `RESERVED` crums (flagged by `reserve()` [`credel.c:364–379`]) are protected. `reap()` then calls either `orglwrite()` [`credel.c:309`] or `subtreewrite()` [`credel.c:329`] to write the crum to disk and free it from core.

**The reaper is purely a memory management mechanism.** It may fire mid-mutation (since `ealloc` is called by `createcrum` inside `doinsert` etc.), but this has no effect on cross-session visibility:

- Mutations are visible in-core as soon as the in-memory tree nodes are modified — not after the reaper writes them to disk.
- Reaped crums are written to disk and freed; subsequent reads call `inloaf()` / `inorgl()` which read back the already-mutated on-disk state.
- The reaper never runs between sessions (the event loop is single-threaded and cooperative).

---

### `writeenfilades()` and `diskflush()`: Durability, Not Visibility

`writeenfilades()` (`corediskout.c:68–88`) serializes the full `granf` and `spanf` trees to disk blocks (`writeloaf` → `actuallywriteloaf`). It is called in three places:

1. **`diskflush()`** (`corediskout.c:58–64`), called at `bed.c:105` when `n_players < 1`:
   ```c
   if (n_players < 1) {
       diskflush();    // bed.c:105
       new_players(..., TRUE, ...);  // block until next session
   }
   ```
   After `writeenfilades()`, `initkluge()` is called which **reloads** `granf` and `spanf` from the just-written disk blocks [`corediskin.c:18–41`]. This is the **between-sessions handoff point** — it only happens when the session count drops to zero.

2. **`diskexit()` → `indiskexit()`** (`corediskout.c:30–54`): on QUIT or process exit.

3. **`flagquitting()`** (`bed.c:175–188`): on SIGINT.

**`writeenfilades()` is for durability across process restarts, not for making mutations visible to concurrent sessions.** Concurrent sessions share the same in-core `granf`/`spanf` globals directly; they never need to go through disk to observe each other's changes.

---

### Summary Table

| Point in time | What happens | Cross-session effect |
|---|---|---|
| `doinsert()` / `dodeletevspan()` / `docopy()` returns | `granf`/`spanf` nodes mutated in-core | Mutation is committed to shared memory |
| `xanadu()` exits | Mutation done + response flushed | **Earliest moment any other session can be dispatched** |
| Grim reaper fires | Old crums written to disk, freed | No new visibility — already in-core; subsequent reads go to disk and back |
| `diskflush()` (n_players < 1) | Full tree written to disk, `granf`/`spanf` reloaded from disk | Next reconnecting session reads from disk checkpoint |
| `writeenfilades()` / `diskexit()` | Full tree written to disk | Durability for process restart only |

**The linearization point for INT-MULTI-SESSION is: the exit of `xanadu()` on the writing session.** Specifically, the mutation is applied at mutation-function-return time, but it is not reachable by any other session until the cooperative event loop returns from `xanadu()` and `select()` picks the next ready descriptor. The grim reaper and `writeenfilades()` are orthogonal to this — they are memory-pressure and durability mechanisms respectively, neither of which gates cross-session observability.
