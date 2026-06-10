## Question 4 [evidence]

> When a FEBE operation takes a document argument (e.g., the home document in link creation), does udanax-green validate that document's existence unconditionally before any other processing, or only on the execution paths that actually use it — and what happens to the request when validation fails?

## KB Synthesis

## Document Validation in FEBE Operations

Validation is **not** performed unconditionally before processing. It happens inside the `doXXX` execution path, and — for most mutations — the success response has already been sent before validation runs.

### The General Pattern: Response Before Check

For state-modifying operations (INSERT, DELETEVSPAN, REARRANGE, COPY), the FEBE handler follows this sequence:

1. `getXXX()` — parse the request
2. `putXXX()` — **send success response to front end**
3. `doXXX()` — attempt the operation, which calls `findorgl(..., WRITEBERT)` to validate the document

[EC-RESPONSE-BEFORE-CHECK] documents this directly. When `findorgl` returns FALSE (document doesn't exist, isn't open, or access is denied), the operation is silently abandoned. The front end has already received a success code and has no way to detect the failure. The back end prints to stderr and continues.

The practical consequence is documented in [PRE-INSERT] (Finding 0050): a front end that inserts into a non-existent or non-open document receives a success response, but the document state is unchanged.

### The `findorgl` Mechanism

Validation itself is performed by `findorgl`, which checks [PRE-OPEN-DOC]:
- the document orgl is present in the granfilade (document exists)
- the document is in the current session's open list
- the requested access level (READBERT=1 or WRITEBERT=2) is satisfied per the BERT table

These checks are **not** separated — document existence and open-state are tested together in a single call. There is no pre-flight existence check before the open-state check.

### The Exception: CREATELINK Validates Before Responding

[EC-RESPONSE-BEFORE-CHECK] explicitly identifies CREATELINK as the correct outlier: `fns.c:100-115` checks `getcreatelink() && docreatelink()` before calling `putcreatelink()`. If the home document doesn't exist or isn't writable, `putrequestfailed()` is sent. The home document is validated (via `findorgl` inside `docreatelink`) before any response goes to the client.

### Query Operations

For read operations like RETRIEVE_CONTENTS, validation failure produces a backend error response rather than a silent skip, because the result data IS the response — the two cannot be decoupled the way they can for mutation acknowledgments [PRE-RETRIEVE-CONTENTS].

### Summary Table

| Operation class | Validation timing | On failure |
|---|---|---|
| Mutations (INSERT, DELETE, etc.) | After success response sent | Silent no-op; client gets false success |
| CREATELINK | Before any response | `putrequestfailed` sent |
| Queries (RETRIEVE, etc.) | During result computation | Error response sent |

The BERT access control layer [INV-WRITE-EXCLUSIVITY], [INT-BERT-FEBE] is therefore a **cooperative protocol**, not an enforced gate. The back end maintains BERT state for front-end coordination, but for most mutations the validation outcome does not affect what the client observes.

---

## Code Exploration

I now have enough to answer the question fully. Here is the complete analysis.

---

## Document Validation in udanax-green FEBE Operations

### The Validation Mechanism

Validation is not performed at the FEBE parsing layer. The `get*` functions in `get1fe.c` simply read tumblers and specsets off the wire with no existence or open-state check. `getcreatelink` at `get1fe.c:75-84` reads the home document tumbler as raw bytes:

```c
return (
   gettumbler (taskptr, docisaptr)
&& getspecset (taskptr, fromspecsetptr)
...
```

The sole validation mechanism is `findorgl` in `granf1.c:17-41`, which gates on `checkforopen`:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  int temp;
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            *orglptr = NULL;
            return FALSE;   // [granf1.c:34-36]
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` (`bert.c:52-87`) checks only the **in-memory bert open table** (`berttable`), not disk. A non-existent document and a document that exists but isn't open are indistinguishable: both produce a return value ≤ 0. The `type` argument controls what is required (`NOBERTREQUIRED=0`, `READBERT=1`, `WRITEBERT=2` from `common.h:165-167`).

---

### Validation is Lazy and Per-Operation

#### `createlink` / `docreatelink` — validation on 4th step, after a side effect

`fns.c:createlink` uses the correct short-circuit pattern:

```c
if (getcreatelink(taskptr, &docisa, ...) && docreatelink(taskptr, &docisa, ...))
    putcreatelink(taskptr, &linkisa);
else
    putrequestfailed(taskptr);   // [fns.c:106-111]
```

Inside `docreatelink` (`do1.c:195-221`), the home document `docisaptr` is not validated until the **4th step**:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   // step 1: link node allocated — NO BERT CHECK
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)         // step 2: no bert check
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)           // step 3: validation called but DISCARDED
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // step 4: findorgl(WRITEBERT) — REAL CHECK
```

At step 3, `findnextlinkvsa` (`do2.c:151-167`) calls `doretrievedocvspan` → `findorgl(READBERT)` — but its return value is explicitly discarded:

```c
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);   // [do2.c:160] — result thrown away
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);    // operates on uninit data if doc not open
```

If the document isn't open, `vspan` is uninitialized and `linkvsa` is computed from garbage — but `findnextlinkvsa` still returns `TRUE`.

The first validation that can **abort the chain** is at step 4, inside `docopy` (`do1.c:53-64`):

```c
specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)  // no bert check
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)    // [do1.c:55] — HERE
```

**Critical side effect**: Step 1 (`createorglingranf`) has already created and allocated the link node in the granfilade before validation runs. If step 4 fails, the link node exists as an orphan.

#### `copy` / `docopy` — same: validation is step 2, short-circuit propagated

`docopy` validates the home document at `findorgl(WRITEBERT)` (`do1.c:55`), and the `copy` handler in `fns.c:35-47` properly propagates failure to `putrequestfailed`.

#### `insert`, `deletevspan`, `rearrange` — validation **decoupled from response**

These three operations use a different pattern in `fns.c`. The success response is **sent before the operation runs**:

```c
// insert [fns.c:84-98]
(void) getinsert (taskptr, &docisa, &vsa, &textset);
putinsert (taskptr);                    // SUCCESS RESPONSE SENT HERE
if (!doinsert (taskptr, &docisa, &vsa, textset))
    fprintf(stderr,"requestfailed in insert\n");  // dev build only

// deletevspan [fns.c:333-347]
(void) getdeletevspan (taskptr, &docisa, &vspan);
putdeletevspan (taskptr);               // SUCCESS RESPONSE SENT HERE
if (!dodeletevspan (taskptr, &docisa, &vspan))
    fprintf(stderr,"deletevspan failed \n");  // dev build only
```

`doinsert` → `docopy` → `findorgl(WRITEBERT)`, and `dodeletevspan` → `findorgl(WRITEBERT)` — validation does run, but its failure is never communicated to the client. In `DISTRIBUTION` builds the `fprintf` is compiled out entirely (the `else` branch is `;`). The client already received a success response and has no indication the operation failed.

#### `createnewversion` — source document bypasses bert

In `docreatenewversion` (`do1.c:260-299`), the source document is accessed via `doretrievedocvspanfoo` → `findorgl(NOBERTREQUIRED)` (`do1.c:307`). `NOBERTREQUIRED` causes `checkforopen` to return 1 unconditionally (`bert.c:59-61`). No bert check is performed on the source document's open state. The new version is registered directly via `addtoopen` (`do1.c:292`).

---

### What Happens When Validation Fails

| Operation | Response handling | On validation failure |
|-----------|-------------------|-----------------------|
| `createlink` | correct short-circuit | `putrequestfailed` sent; orphan link node left in granfilade |
| `copy` | correct short-circuit | `putrequestfailed` sent |
| `createnewversion` | correct short-circuit | `putrequestfailed` sent |
| `retrievedocvspan/set` | correct short-circuit | `putrequestfailed` sent |
| `retrievev` | correct short-circuit | `putrequestfailed` sent |
| `insert` | **inverted** — success first | failure logged to stderr (dev) or silently discarded (dist); client gets success |
| `deletevspan` | **inverted** — success first | same |
| `rearrange` | **inverted** — success first | same |

---

### The `isxumain` Bypass

`findorgl` contains a bypass specifically for the `xumain` (front-end process):

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) {          // [granf1.c:24, 33]
        return FALSE;
    }
    // if isxumain == TRUE: fall through and fetch the orgl anyway
}
```

`isxumain` is `FALSE` in `be.c:29` and `bed.c:35` (daemon mode, where the test harness connects), and `TRUE` only in `xumain.c:23`. When running as the FEBE backend daemon, bert validation is always enforced in `findorgl`.

---

### `specset2ispanset` — Per-Document Validation in Specsets

When specsets contain multiple V-specs (content from different documents), `specset2ispanset` (`do2.c:14-46`) calls `findorgl` per spec item:

```c
if (!(
  findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
  && (ispansetptr = vspanset2ispanset(...)))) {
    return (FALSE);   // [do2.c:34-38]
}
```

The `type` passed down from callers determines whether this is a real check. For `createlink`'s from/to/three specsets, all three calls use `NOBERTREQUIRED` (`do1.c:214-216`), meaning documents referenced in link endpoints are never validated for open state.

---

### Conclusion

Validation is **lazy and path-dependent**, not unconditional at request entry. The document argument is only validated when a `findorgl(READBERT|WRITEBERT)` call happens on the execution path that actually needs to open it. For `createlink`, this first meaningful check is the 4th step in `docreatelink`, by which time a link node has already been allocated. For `insert`, `deletevspan`, and `rearrange`, the decoupled response/operation pattern means validation failure is never reported back to the client — the success response has already been sent by the time `findorgl` runs.
