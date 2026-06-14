## Question 15 [evidence]

> Does `WRITEBERT` exclusivity in `checkforopen` actually prevent a second session from holding write access to the same document's POOM concurrently, or does it only gate `findorgl` at access time while leaving the `EC-BERT-ENFORCEMENT` response-before-check gap to admit a racing writer?

## KB Synthesis

## WRITEBERT Exclusivity vs. Concurrent POOM Writes

The short answer: `checkforopen` does gate access *within each request*, but it is not what prevents concurrent POOM writes. The architectural guarantee comes from the sequential event loop, not BERT.

### What `checkforopen` actually does

`checkforopen` (invoked via `findorgl(..., WRITEBERT)` inside `doXXX()`) enforces the BERT table invariant: if connection A holds WRITEBERT, all other connections are denied WRITEBERT. This prevents the BERT table from ever granting WRITEBERT to two connections simultaneously. [INV-WRITE-EXCLUSIVITY]

### The response-before-check gap

For INSERT, DELETEVSPAN, REARRANGE, and COPY, the handler pattern is:

1. `getXXX()` — parse request  
2. `putXXX()` — **send success response to front end**  
3. `doXXX()` — attempt operation (calls `findorgl(..., WRITEBERT)`)

If step 3's BERT check fails, the mutation is silently skipped — but the front end already received success. [EC-RESPONSE-BEFORE-CHECK]

This gap admits *silent failures*, not concurrent writes. A front end that bypasses BERT gets a false success acknowledgment while the POOM is unchanged.

### Why concurrent POOM writes are impossible regardless

The `EC-RESPONSE-BEFORE-CHECK` gap does **not** create a window for racing writers, because the event loop is strictly sequential:

> `select()` returns → `xanadu(&task)` executes the **entire** operation (parse → respond → mutate) → loop back to `select()`

No two `doXXX()` calls can interleave. [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH] Even if multiple FDs are ready simultaneously, they are processed one at a time. [Finding 0042]

This means the question of whether WRITEBERT "actually prevents concurrent POOM writes" has a structural answer: **concurrent POOM writes are architecturally excluded by the single-threaded run-to-completion event loop**, not by WRITEBERT. WRITEBERT's role is cooperative coordination among compliant front ends, not enforcement against malicious ones.

### The real threat model

What WRITEBERT cannot prevent — and what the response-before-check gap exposes — is a non-compliant front end sending mutations without ever acquiring WRITEBERT. Such a front end receives false success signals while actual POOM mutations are silently dropped. This is the INT-BERT-FEBE point: [INT-BERT-FEBE]

> `system_correct ↔ (backend_correct ∧ all_frontends_compliant)`

Within the compliant-front-end model, WRITEBERT exclusivity holds in the BERT table and `findorgl` gates actual POOM mutations at call time. The response-before-check gap is a protocol error signal issue, not a concurrency issue.

### Summary

| Concern | Mechanism | Status |
|---------|-----------|--------|
| Two sessions writing POOM simultaneously | Sequential event loop (INV-ATOMICITY) | **Structurally impossible** |
| BERT table admitting two WRITEBERT grants | `checkforopen` in BERT table | **Enforced** |
| Non-compliant front end mutating without WRITEBERT | Advisory only; `doXXX` silently skips | **Not enforced** — silent data loss |
| False success on BERT-failed mutation | Response-before-check gap | **Known gap** — front end misled |

---

## Code Exploration

I now have all the source I need to answer definitively. Let me trace every relevant path.

---

## Answer

### 1. The Event Loop Is Single-Threaded

`bed.c` runs a `select(2)` event loop that dispatches **one full request to completion** before the next session's request can begin:

```c
// bed.c:118-141
for (i = 0; i <= nfds; i++) {
    if ((1<<i) & inputfds2) {
        user = fdtoplayer[i];
        task.inp = player[user].inp;
        task.outp = player[user].outp;
        ...
        xanadu(&task);       // blocks until this request is fully handled
    }
}
```

`xanadu()` itself runs the handler to completion before `sendresultoutput` and before returning to `select`:

```c
// bed.c:153-172
int xanadu(typetask *taskptr) {
    ...
    } else if (getrequest(taskptr, &request)) {
        (*requestfns[request])(taskptr);    // handler runs to completion
        sendresultoutput(taskptr);
    }
```

There is no OS-level concurrency between sessions. Session B **cannot execute any code** while session A's handler is running.

---

### 2. `WRITEBERT` Exclusivity Is Real

`checkforopen` [bert.c:52-87] correctly blocks a second connection from acquiring write access when one already holds it:

```c
} else {
    if (bert->type != READBERT) {
        foundnonread = TRUE;     // bert.c:74-76
    }
}
...
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;    // bert.c:83-85 — blocked
}
```

When session A holds `WRITEBERT` on document D:
- Session B sends OPEN for D with `WRITEBERT`
- `doopen` calls `checkforopen` [bert.c:279]
- B's connection != A's connection, A's type != `READBERT` → `foundnonread = TRUE`
- `checkforopen` returns -1
- `doopen` returns FALSE → `putrequestfailed` → B is denied

The bert table (`berttable[NUMBEROFBERTTABLE]` at bert.c:29) is a flat hash table with no locks needed because the backend is single-threaded. Once A's `addtoopen` [bert.c:128] commits the entry, it is visible to any subsequent check before A calls `removefromopen`.

---

### 3. The `findorgl` Check Is a Second Gate, Not the Primary Lock

`findorgl` [granf1.c:17-41] re-checks bert at operation time:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        ...
        return FALSE;    // granf1.c:28-31
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

Every mutating operation passes `WRITEBERT` here:
- `dorearrange` [do1.c:40]: `findorgl(..., WRITEBERT)`
- `docopy` [do1.c:55]: `findorgl(..., WRITEBERT)` — called by `doinsert` [do1.c:119] and `docreatelink`
- `dodeletevspan` [do1.c:164]: `findorgl(..., WRITEBERT)`

This is defense-in-depth: the bert state checked at `findorgl` is the same global table that `doopen`/`addtoopen` modified. Since the event loop is single-threaded, that table cannot have changed between OPEN and the operation.

---

### 4. The Response-Before-Check Gap Is Real, But Is a Protocol Bug, Not a Concurrency Bug

Three handlers in `fns.c` send their response **before** executing the operation (and thus before `findorgl` checks bert):

```c
// fns.c:84-98
void insert(typetask *taskptr) {
    (void) getinsert (taskptr, &docisa, &vsa, &textset);
    putinsert (taskptr);                             // ← SUCCESS RESPONSE SENT
    if (!doinsert (taskptr, &docisa, &vsa, textset)) // ← BERT CHECKED HERE
        fprintf(stderr,"requestfailed in insert\n"); // too late
}
```

Same pattern at `rearrange` [fns.c:165-166] and `deletevspan` [fns.c:339-341].

The original safe-pattern functions (`createlink`, `copy`, `createnewversion`) do it correctly — check first, respond only on success [fns.c:106-112, 41-46, 294-299].

**Why this does NOT admit a racing writer from a second session:**

Within one `xanadu()` dispatch, the gap between `putinsert` and `doinsert` is a sequential gap inside a single-threaded process. No second session's code runs during that gap. Session B is blocked in `select` until session A's entire `xanadu()` call (including the `sendresultoutput` flush) returns to the event loop [bed.c:128].

**What this gap DOES cause:**

If a client sends INSERT without having previously opened the document for write, the execution is:
1. `putinsert(taskptr)` — client receives "success"
2. `doinsert` → `docopy` → `findorgl(WRITEBERT)` → `checkforopen` returns 0 (not open) or -1
3. `findorgl` returns FALSE [granf1.c:28-31]
4. `doinsert` returns FALSE
5. `insert()` logs to stderr, discards the failure silently

The client has a success response for an operation that was never applied to the POOM. This is a **client-server state divergence bug**, not a concurrency bug.

---

### 5. Direct Answer to the Question

**Does `WRITEBERT` exclusivity prevent a second session from holding write access concurrently?**

Yes. `checkforopen` [bert.c:74-76] detects any non-`READBERT` entry from a different connection and returns -1. `doopen` [bert.c:279-321] enforces this before calling `addtoopen`. Because `addtoopen` [bert.c:128-151] and `removefromopen` [bert.c:154-193] only execute during explicit OPEN/CLOSE/QUIT requests — each of which runs to completion before the next — the bert table correctly serializes write access across sessions.

**Does the response-before-check gap admit a racing writer?**

No. The gap between `putinsert`/`putrearrange`/`putdeletevspan` and their corresponding `do*` call is intra-request, inside a single-threaded event loop. Session B cannot inject a request during that window because `select` is not called again until `xanadu()` returns [bed.c:128, 146].

**What the gap does admit:**

The gap is a protocol integrity hole: a client that issues a mutating command without a valid bert open will receive a false success. The POOM is not modified, but the client believes it was. This is the actual enforcement failure — not a concurrency race, but a client-observable lie about operation outcome.
