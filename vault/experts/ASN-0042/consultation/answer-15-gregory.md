## Question 15 [gregory]

> When a user creates a version of a document they do NOT own, the version is allocated under the versioning user's account — does this mean the versioning user now owns that version's entire sub-tree, including the right to create sub-versions and allocate further addresses beneath it?

## KB Synthesis

Yes — a user who versions an unowned document owns the resulting version and gains full authority over its sub-tree.

## Mechanism

From [SS-VERSION-ADDRESS] (Finding 0068), when the ownership check fails:

```c
makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)
```

This sets `depth=2`, placing the version as a direct child of the creating user's **account** rather than a child of the source document. The result is structurally identical to a fresh document creation under that user's account.

Example from the KB:
- User A's doc: `1.1.0.1.0.1`
- User B (account `1.1.0.2`) versions it → version at `1.1.0.2.0.1`

The address `1.1.0.2.0.1` is a descendant of `1.1.0.2` — User B's account.

## Ownership of the New Version

The ownership check in `docreatenewversion` is:

```c
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

When User B subsequently operates on `1.1.0.2.0.1`:
- `tumbleraccounteq` compares the document's account prefix with the current user's account → **match** (both `1.1.0.2`)
- `isthisusersdocument` checks document ownership → **true** (it was allocated under User B's account)

So the owned-document path applies, and sub-versions are allocated as children of the version: `1.1.0.2.0.1.1`, `1.1.0.2.0.1.2`, etc. [SS-ADDRESS-ALLOC, Finding 0068]

## Address Containment = Authority Boundary

From [INV-ACCOUNT-ISOLATION] and [SS-TUMBLER-CONTAINMENT]: account ownership is defined purely by address prefix containment — `contains(account, doc_address)` via tumbler truncation/comparison. Since `1.1.0.2.0.1` and all addresses beneath it are descendants of `1.1.0.2`, they fall entirely within User B's account namespace. The hierarchical address allocation algorithm ([ST-ADDRESS-ALLOC]) will correctly scope all further allocations under `1.1.0.2.0.1` to User B's account, satisfying [INV-ACCOUNT-ISOLATION].

## Practical Implication

The cross-user version severs the address-based lineage chain. User A's version tree is:
```
1.1.0.1.0.1          (User A's doc)
└── 1.1.0.1.0.1.1    (User A's own versions)
```

User B's fork lives separately:
```
1.1.0.2.0.1          (User B's fork of User A's doc)
├── 1.1.0.2.0.1.1    (User B's sub-version)
└── 1.1.0.2.0.1.2    (another sub-version)
```

Content identity is shared (via the text I-address copying in `docopyinternal` [ST-VERSION-CREATE, Finding 0046]), but address lineage is not. `compare_versions` can still detect shared content [SS-COMPARE-VERSIONS], but there is no address-structural relationship linking `1.1.0.2.0.1` to `1.1.0.1.0.1`.

**Summary:** The versioning user owns the cross-user version completely. They can create sub-versions, allocate addresses beneath it, and the entire sub-tree is isolated within their account namespace.

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## Answer: Cross-User Versioning and Sub-Tree Ownership in udanax-green

### The Short Answer

**It depends entirely on which code path created the version.** There are two paths through `docreatenewversion`, and they produce radically different results. The stated premise — that the version lands under the versioning user's account — is **only true in the `doopen` access-control path**, not in the direct FEBE `createnewversion` protocol path. Where the premise does hold, the versioning user gains full recursive sub-tree ownership by the mechanics of tumbler-prefix matching.

---

### Code Path 1: `doopen` (BERTMODECOPY / BERTMODECOPYIF)

**This is the path where the premise holds.**

`bert.c:264–298`:
```c
bool doopen(typetask *taskptr, tumbler *tp, tumbler *newtp, int type, int mode, int connection)
{
   if (mode == BERTMODECOPY) {
       docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // bert.c:274
       addtoopen(newtp, connection, TRUE, type);
       return 1;
   }
   ...
   case BERTMODECOPYIF:
       if (openState == -1) {
           docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // bert.c:290
```

Here, the third argument `wheretoputit` is `&taskptr->account` — **user B's own account tumbler** (e.g., `1.1.0.2`), not the original document's address.

---

### Code Path 2: Direct FEBE `createnewversion`

**This path does NOT place the version under the versioning user's account.**

`fns.c:289–299`:
```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))  // fns.c:296
        putcreatenewversion (taskptr, &newdocisa);
```

Both `isaptr` and `wheretoputit` are `&originaldocisa`. The new version is allocated *relative to user A's document address*, not user B's account.

---

### The Branching Logic in `docreatenewversion`

`do1.c:260–298`:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    /* ECH 7-13 introduced test for ownership to do right thing for explicit creation
       of new version of someone else's document */
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);  // do1.c:271
    } else {
        /* This does the right thing for new version of someone else's document, as it
           duplicates the behavior of docreatenewdocument */
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);  // do1.c:275
    }
```

The condition at `do1.c:270` gates on two tests:

**`tumbleraccounteq(isaptr, wheretoputit)`** — `tumble.c:38–70`:
> Checks whether `isaptr` falls under the account described by `wheretoputit`, by treating two consecutive zeros in `wheretoputit` as the account-boundary terminator.

**`isthisusersdocument(isaptr)`** — `socketbe.c:197–201`:
```c
int isthisusersdocument(tumbler *tp)
{
    return tumbleraccounteq(tp, &(player[user].account));
}
```
> Ownership is purely whether the document's tumbler address has the current user's account as a prefix. **Address IS ownership.**

When user B calls `docreatenewversion` on user A's document:
- Path A (`doopen`): `wheretoputit = &taskptr->account` (user B's account `1.1.0.2`). `tumbleraccounteq(user_A_doc, user_B_account)` = **FALSE** → `else` branch with hint `(ACCOUNT, DOCUMENT, user_B_account)`. New version allocated under user B's account.
- Path B (direct FEBE): `wheretoputit = &originaldocisa = user_A_doc`. `tumbleraccounteq(user_A_doc, user_A_doc)` = **TRUE**, but `isthisusersdocument(user_A_doc)` = **FALSE** → `else` branch with hint `(ACCOUNT, DOCUMENT, user_A_doc)`. New version allocated within user A's document address space.

---

### Address Allocation Mechanics

The hint type determines the depth at which the new address is generated — `granf2.c:209`:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

| supertype → subtype | depth | Example |
|--------------------|-------|---------|
| `DOCUMENT, DOCUMENT` | 1 | Self-versioning: `1.1.0.1.0.1` → `1.1.0.1.0.1.1` |
| `ACCOUNT, DOCUMENT` | 2 | New doc under account: `1.1.0.2` → `1.1.0.2.0.1` |

- **Path A** (`doopen`, hint = `ACCOUNT, DOCUMENT, user_B_account`): depth=2, new version = `1.1.0.2.0.1` — under user B's account.
- **Path B** (FEBE, hint = `ACCOUNT, DOCUMENT, user_A_doc`): depth=2, new version = `1.1.0.1.0.1.0.0.1` — inside user A's document's address space.

Finding 0021 and finding 0007 confirm this structure:
> "Original: 1.1.0.1.0.1 / Version: 1.1.0.1.0.1.1" (depth=1 for self-versioning via DOCUMENT,DOCUMENT hint)

---

### Sub-Tree Ownership for Path A (the Premise Holds)

Given user B's copy is at `1.1.0.2.0.1` and user B's account is `1.1.0.2`:

**1. Immediate ownership.** `isthisusersdocument(1.1.0.2.0.1)` calls `tumbleraccounteq(1.1.0.2.0.1, 1.1.0.2)`. The algorithm in `tumble.c:54–69` scans mantissa, matches `1`, `1`, `0`, `2`, then hits two zeros → returns TRUE. User B "owns" the version.

**2. Write access without copying.** `checkforopen` at `bert.c:81`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // "not open, but can open"
}
```
When user B tries to write to `1.1.0.2.0.1` and it's not open, `isthisusersdocument` returns TRUE → `checkforopen` returns 0 → `doopen` adds a BERT entry without creating another copy. User B writes in place.

**3. Sub-versioning allocates within the sub-tree.** When user B calls `createnewversion` on their own copy (`1.1.0.2.0.1`):
- `isaptr = wheretoputit = 1.1.0.2.0.1`
- `tumbleraccounteq(1.1.0.2.0.1, 1.1.0.2.0.1)` = TRUE
- `isthisusersdocument(1.1.0.2.0.1)` = TRUE (user B owns it)
- → **TRUE branch**: `makehint(DOCUMENT, DOCUMENT, 0, 1.1.0.2.0.1, &hint)` with depth=1
- Sub-version allocated at `1.1.0.2.0.1.1` — still under `1.1.0.2`

**4. Recursive.** Any address nested beneath `1.1.0.2.0.1` — e.g., `1.1.0.2.0.1.1`, `1.1.0.2.0.1.1.1`, etc. — will satisfy `tumbleraccounteq(addr, 1.1.0.2)` because `1.1.0.2` is a prefix of all of them. Ownership extends to arbitrary depth with no additional mechanism required.

---

### What User A Can (and Cannot) Do to User B's Copy

`checkforopen` for user A trying to access `1.1.0.2.0.1`:
- No BERT entry for user A on this document
- `isthisusersdocument(1.1.0.2.0.1)` with user A's account `1.1.0.1` = FALSE
- For `READBERT`: `!foundnonread && type == READBERT` = TRUE → returns 0 → **user A can open for reading**
- For `WRITEBERT`: `!foundnonread && isthisusersdocument(tp)` = FALSE → returns -1 → **user A must create a new version** (which would land under `1.1.0.1`)

**User A can read user B's copy but cannot write to it without forking again.**

---

### The Path B Anomaly (Direct FEBE, Premise Does Not Hold)

In Path B, user B's "version" of user A's document is allocated at `1.1.0.1.0.1.0.0.1` — inside user A's address space:
- `isthisusersdocument(1.1.0.1.0.1.0.0.1)` for user B = FALSE (prefix `1.1.0.1` ≠ user B's `1.1.0.2`)
- `checkforopen` for user B WRITE → returns -1 → user B cannot write to the thing they just created without triggering another copy
- Sub-versioning by user B would again fork → the chain spirals into user A's address space at increasing depth

This is likely a latent bug or an incomplete code path. The comment at `do1.c:273` says it "duplicates the behavior of docreatenewdocument," but `docreatenewdocument` uses `&taskptr->account` [do1.c:239], not `&originaldocisa`. The direct FEBE path passes `wheretoputit = &originaldocisa`, which is semantically different.

---

### Summary

| Condition | New version address | User B owns it? | Can sub-version? |
|-----------|--------------------|--------------------|------------------|
| Via `doopen` BERTMODECOPY/COPYIF (`wheretoputit = &taskptr->account`) | `user_B_account.0.N` | **Yes** — `isthisusersdocument` = TRUE | **Yes** — recursively under user B's account |
| Via direct FEBE `createnewversion` (`wheretoputit = &originaldocisa`) | `user_A_doc.0.0.N` | **No** — inside user A's space | **No** — would fork again into user A's space |

**Where the premise holds (Path A), the answer is an unqualified yes.** Tumbler-prefix IS ownership. Once an address is allocated under user B's account, all further addresses generated from it (sub-versions, content atoms) inherit that prefix. `isthisusersdocument` returns TRUE for all of them. The versioning user owns the entire sub-tree transitively, to arbitrary depth, with no additional mechanism required and no mechanism available for user A to reclaim it.

The ownership model is not a policy rule enforced by an ACL — it is structural. The tumbler address space *is* the ownership space. Whoever holds the account address holds the namespace.
