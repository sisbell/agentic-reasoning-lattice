## Question 14 [gregory]

> Is there a delegation mechanism where an owner of a tumbler range can grant another account the right to allocate new children within that range — for example, a node operator granting a new user the right to create documents under their allocated account prefix?

## KB Synthesis

The KB contains no evidence of a delegation mechanism of this kind. Here is what the KB does say about address allocation and access control, and what it leaves silent:

## What address allocation actually checks

[SS-ADDRESS-ALLOC] describes `findisatoinsertnonmolecule` as a pure stateless query-and-increment over the granfilade tree. The allocator's only inputs are:

1. The `hintisa` (parent address) passed by the caller
2. The current maximum address found under that parent in the granfilade

There is no permission predicate of the form "may caller C allocate under prefix P?" The allocator is agnostic to who is asking.

## The only ownership check in the allocation path

[SS-VERSION-ADDRESS, Finding 0068] documents the sole instance where something resembling ownership enters allocation: `CREATENEWVERSION` checks `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` to decide *where* to allocate (under the source document vs. under the creating session's own account). This is a routing decision — it determines which parent address to pass to the allocator — not a gatekeeping decision about whether allocation is permitted at all.

## BERT controls document mutation, not address-space allocation

[SS-BERT, PRE-OPEN-DOC] establishes that BERT tokens govern read/write access to existing documents. BERT has no concept of "right to allocate children under prefix P." Opening a document for WRITE means you can modify its content — it says nothing about whether you can create new documents under its address.

## Account isolation is enforced by allocation, not by permission checks

[INV-ACCOUNT-ISOLATION] notes that documents must be proper descendants of their account's address, and that Bug 0013 showed this was violated by the original allocation algorithm when containment checking was missing. The fix added a prefix-match check to keep allocations within the correct parent range. This is a correctness guard on the allocator itself, not a delegation permission system.

## Conclusion

The KB describes no delegation mechanism. There is no data structure, no operation, and no protocol element that would let account A authorize account B to allocate new addresses within A's tumbler range. The system's session model ([SS-SESSION-STATE]) ties each session to a single current account, and all allocations happen within that account's namespace. Granting another account allocation rights within your prefix would require support that simply does not appear anywhere in the KB.

If such a mechanism existed, it would need to be threaded through `findisatoinsertnonmolecule` as an additional check, or handled at the session/account-setup level before the allocator is invoked. Neither is described.

---

## Code Exploration

## Answer: No Delegation Mechanism in udanax-green

**Short answer: No.** There is no delegation mechanism. The system uses strict account-based namespace partitioning with no support for one owner granting another rights to allocate within their tumbler range.

---

### How Ownership Actually Works

Ownership is determined by prefix matching via `tumbleraccounteq()` in `backend/tumble.c:38-70`. An account is a tumbler terminated by **two consecutive zeros** in the mantissa. Any document tumbler whose leading non-zero digits match the account prefix is "owned" by that account:

```c
// backend/tumble.c:58-67
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);  /* Account terminated, document is under this account */
        }
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);
        }
    }
}
```

The check happens at the `checkforopen()` gate in `backend/bert.c:52-87` via `isthisusersdocument()`, which compares the requested document's tumbler against `player[user].account`.

---

### Access Control Model

`findorgl()` in `backend/granf1.c:22` calls `checkforopen()` before fetching any document. The only paths to success are:

1. The document is open in the BERT table for this connection (`bert->connection == user`)
2. No write-lock exists elsewhere **and** the operation is a read or `isthisusersdocument()` returns true

```c
// backend/bert.c:81
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

There is no third path — no "granted by owner" check.

---

### New Document Allocation

`docreatenewdocument()` at `backend/do1.c:234-241` always passes `taskptr->account` as the hint for the granfilade allocator:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return createorglingranf(taskptr, granf, &hint, isaptr);
```

`docreatenewversion()` at `backend/do1.c:260-299` makes this even explicit — if you're versioning someone else's document, the new version is forced into **your own** namespace:

```c
// backend/do1.c:268-275
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    /* new version of someone else's document goes under YOUR account */
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

---

### No ACL Structures

The BERT entry in `backend/bert.c:13-24` contains only:

```c
typedef struct {
    int connection;      /* which user has it open */
    tumbler documentid;  /* which document */
    char created, modified;
    int type;            /* READBERT or WRITEBERT */
    int count;
} bertentry;
```

No grantor, no permission flags, no delegation chain. The BERT is a **session lock table**, not an ACL.

---

### Account Assignment

Accounts are set via `xaccount` in `backend/fns.c:364-373`, which calls `getxaccount()` in `backend/get1.c:190-204`. The account tumbler comes directly from the client request with **no validation** that the user is authorized to claim that account — it's a protocol-level assumption. There is no "create user under my prefix" operation anywhere in the FEBE protocol.

---

### Conclusion

The access control model in udanax-green is a simple **namespace partition** scheme:

- Each user has an `account` tumbler (a fixed prefix)
- All documents under that prefix are owned by that user
- No user can allocate in another user's prefix
- There is no way for a user to grant a sub-range to another party
- There are no ACLs, capability tokens, or delegation records anywhere in the codebase

A "node operator granting a new user the right to create documents under their allocated account prefix" would require new protocol operations, a new data structure for delegation records, and changes to the `checkforopen()` / `isthisusersdocument()` ownership chain — none of which exist.
