## Question 16 [gregory]

> Is there a structural boundary between "this is my address space" and "this is someone else's" that the backend enforces, or is the ownership boundary purely conventional — could user `1.1.0.2` in principle write a POOM entry under `1.1.0.3`'s document range if no check prevents it?

## KB Synthesis

The boundary is **structurally weak at the access level and entirely absent at the mutation level**. Here's the breakdown:

## Address Allocation: Structurally Enforced

When *creating* new documents or links, the allocation algorithm in `findisatoinsertnonmolecule` bounds its search to the parent's address range and applies a containment check via `tumblertruncate`/`tumblereq`. Without a passing containment check, the allocator falls back to the correct first-child address. [PRE-ADDRESS-ALLOC], [SS-TUMBLER-CONTAINMENT]

This is real structural enforcement — a session acting as account `1.1.0.2` cannot accidentally (or even intentionally through normal operations) *allocate* a new document address under `1.1.0.3`. Bug 0013 demonstrated exactly this: the pre-fix allocator crossed account boundaries, and the fix added the containment check. [ST-ADDRESS-ALLOC]

## Writing to Existing Documents: Advisory Only

For *accessing and mutating* existing documents, the BERT table is the intended enforcement mechanism. `checkforopen` does distinguish "owned" vs. "unowned" documents and returns -1 (denied) for write requests on unowned documents. [PRE-OPEN-DOC, SS-BERT]

However, this enforcement is architecturally broken in two ways:

**1. Response-before-check:** For INSERT, DELETEVSPAN, REARRANGE, and COPY, the backend sends the success response (`putXXX`) *before* executing the operation (`doXXX`). The BERT check inside `findorgl(..., WRITEBERT)` runs after the front end has already received success. A failing check causes the operation to be silently skipped — but the caller believes it succeeded. [EC-RESPONSE-BEFORE-CHECK]

**2. Protocol trust, not enforcement:** The BERT table is a coordination tool for compliant front ends. A non-compliant front end that acquires a WRITEBERT token without following the protocol, or that submits mutations without a token, cannot be structurally stopped. [INT-BERT-FEBE]

> "The back end trusts the front end to: (1) acquire BERT tokens before mutations, (2) respect write exclusivity, (3) release tokens when done."

## The POOM Specifically

`insertpm` is called from `docopy` only *after* `findorgl` returns true. If `findorgl` returns false (BERT check fails), `doinsert` returns and nothing is written. But this is the honest path. Nothing in the POOM machinery itself checks address-space ownership — it receives a document orgl pointer and writes into it. [SS-POOM-MUTABILITY]

Similarly, `acceptablevsa()` — which was presumably intended to validate V-positions against document structure — unconditionally returns TRUE. There is no subspace check, no account check, nothing. [PRE-INSERT, PRE-SUBSPACE-CONVENTION]

## Summary

| Layer | Enforcement |
|-------|------------|
| Address *allocation* | Structurally enforced via containment check |
| Document *access* (BERT) | Intended but advisory — response-before-check bug breaks it |
| POOM *mutation* | No ownership check at all; relies entirely on front-end compliance |

So yes: user `1.1.0.2` could in principle write a POOM entry under `1.1.0.3`'s document if they bypass BERT token acquisition — the backend would silently accept it (or rather, silently do nothing via the `findorgl` check failing and the response already sent). The system's security model requires trusting the front end. [INT-BERT-FEBE, INV-WRITE-EXCLUSIVITY]

---

## Code Exploration

Now I have the complete picture. Here is the full analysis.

---

## Ownership Boundary Analysis: Structural Enforcement vs. Convention

**Short answer:** There is a real, code-enforced ownership boundary, but it is a *software fence* — not a cryptographic or hardware boundary. It can be bypassed by code paths that pass `NOBERTREQUIRED`, and it is absent entirely in the single-user (xumain) build mode.

---

### 1. How Ownership Is Encoded in the Tumbler Address

The tumbler is a hierarchical address. A user's *account tumbler* (e.g., `1.1.0.2`) is the prefix for all documents they own. The key function is `tumbleraccounteq` in `tumble.c:38`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr is the account, aptr is the document being tested
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) return(TRUE);  // two zeros = account terminated, doc is under it
            // first zero: doc can have any value here, skip mismatch check
        } else {
            if (aptr->mantissa[i] != bptr->mantissa[i]) return(FALSE);  // must match exactly
        }
    }
    return(TRUE);
}
```

This is a prefix match: the account address terminates with two zeros; any document whose mantissa matches the account's non-zero positions is considered to *belong* to that account. A document with address starting `1.1.0.3` will fail this match against account `1.1.0.2`.

---

### 2. `isthisusersdocument` — The Ownership Predicate

There are three implementations depending on build mode, all equivalent. From `socketbe.c:197`:

```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```

And `be.c:171`:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

The `player[user].account` tumbler is set at session initialization time. The check is: does the document's address fall under the current user's account prefix?

---

### 3. The BERT Table: The Gatekeeper for Write Access

The BERT (open document registry) is the primary access control mechanism. `checkforopen` in `bert.c:52` is the gate:

```c
int checkforopen(tumbler *tp, int type, int connection)
{
    // ... search the BERT table ...
    
    if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
        return 0;   // not open yet, but can be opened
    } else {
        return -1;  // blocked: someone else has it for write, or not your document
    }
}
```

**[bert.c:81]**: If a document is not in the BERT table, write access (`WRITEBERT`) is only possible if `isthisusersdocument(tp)` is true. Read access is allowed to anyone whose document is not already open for write by another. An attempt to write to a document with address `1.1.0.3` by user `1.1.0.2` falls through to `isthisusersdocument` → `tumbleraccounteq` → **FALSE** → `checkforopen` returns -1.

---

### 4. `findorgl` — Where the Gate Is Applied

Every write operation goes through `findorgl` in `granf1.c:17`, which calls `checkforopen` before touching any data:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            return FALSE;   // block the operation
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

**[granf1.c:22]**: The guard fires for any `type != NOBERTREQUIRED`. Core operations that use `WRITEBERT`:
- `dorearrange` → `findorgl(..., WRITEBERT)` [do1.c:40]
- `docopy` → `findorgl(..., WRITEBERT)` [do1.c:55]
- `dodeletevspan` → `findorgl(..., WRITEBERT)` [do1.c:164]

---

### 5. New Document Allocation Enforces Ownership By Construction

`docreatenewdocument` [do1.c:234]:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

The hint's `hintisa` is set to the *requesting user's own account*. The enfilade address allocator (`findisatoinsertgr` → `findisatoinsertnonmolecule`) finds the next available slot *within that account's sub-space*. Users have no mechanism to pass someone else's account address as the hint — the `taskptr->account` is taken from the server-managed `player[user]` struct, not from the client.

For `docreatenewversion` [do1.c:260], the ownership check is explicit:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);   // version within same doc space
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // fork into requester's space
}
```

**[do1.c:270–275]**: A new version of *someone else's* document is automatically placed in the requester's *own* account space, not in the original owner's space. This is semantically correct and structurally enforced by where the allocator is told to look.

---

### 6. The Bypass: `NOBERTREQUIRED`

Several internal call paths explicitly opt out of ownership checking:

- `dofinddocscontaining` → `specset2ispanset(..., NOBERTREQUIRED)` [do1.c:21]
- `docopy` → `specset2ispanset(..., NOBERTREQUIRED)` [do1.c:54] (the source document)
- `docreatelink` → `findorgl(..., NOBERTREQUIRED)` [do1.c:213]
- `doretrievedocvspanfoo` → `findorgl(..., NOBERTREQUIRED)` [do1.c:307]
- `docopyinternal` → all calls use `NOBERTREQUIRED` [do1.c:74-80]

These are meant for *internal server operations* where the server itself is acting on behalf of an operation it already authorized. But they represent gaps: if a code path reaches one of these with an attacker-controlled document ISA, no ownership check fires.

---

### 7. The `isxumain` Bypass

**[granf1.c:31–36]**: The `findorgl` check is skipped entirely in single-user (xumain) mode:

```c
if (!isxumain) {
    return FALSE;
}
```

In xumain mode, *all* operations proceed regardless of BERT state or ownership. There is no ownership enforcement in this build mode.

---

### Verdict: Structural, But Not Hardened

| Property | Enforced? | Mechanism |
|---|---|---|
| Address space defined by tumbler prefix | Yes | `tumbleraccounteq` in `tumble.c:38` |
| Write to another user's open document | Blocked | BERT `foundnonread` check, `bert.c:74` |
| Write to another user's unopened document | Blocked | `isthisusersdocument` in `bert.c:81` |
| New doc allocated outside your space | Blocked | `makehint` uses `taskptr->account`, `do1.c:239` |
| New version of foreign doc allocated in their space | Blocked | `tumbleraccounteq` branch in `do1.c:270` |
| Internal operations with `NOBERTREQUIRED` | **Not checked** | Design gap, `granf1.c:22`, multiple sites |
| Single-user (xumain) mode | **Not checked** | `isxumain` bypass, `granf1.c:31` |

**User `1.1.0.2` cannot, through the normal FEBE protocol, write a POOM entry into `1.1.0.3`'s document space.** The chain `findorgl` → `checkforopen` → `isthisusersdocument` → `tumbleraccounteq` would return FALSE at every write operation, blocking it cleanly.

However, the boundary is a *software convention enforced by a gate in `findorgl`*, not an architectural invariant in the enfilade data structures themselves. The enfilade tree has no concept of ownership — it is purely positional. Nothing in `insertpm`, `insertnd`, or the enfilade core would reject an insertion at a foreign address if `findorgl` were bypassed (via `NOBERTREQUIRED` or `isxumain`). The fence lives only at the access-control layer, not in the storage model.
