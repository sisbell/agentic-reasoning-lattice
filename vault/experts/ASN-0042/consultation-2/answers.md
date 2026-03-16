# Revision Consultation — ASN-0042

**Review:** review-2.md
**Date:** 2026-03-15 20:26

## Summary

4 REVISE items analyzed: 3 internal, 1 consulted (1 nelson, 1 gregory)

## Consultation Results

### Issue 1: Account-level permanence corollary does not follow from O1a

**Category:** BOTH
**Reason:** Whether account-level prefixes can nest depends on Nelson's design intent for "forevermore" and on whether the implementation's account allocation ever produces multi-component user fields that could create nesting.

**Nelson question:** Did you intend that an account holder's "full control forevermore" could be superseded by delegating a sub-account with a longer user field at the same structural level, or must account-level prefixes be non-nesting?

**Nelson's Answer:**

The short answer: account prefixes nest by design, and no, delegation does not supersede the delegator's control. These are non-conflicting because they operate on different subtrees.

## The Forking Mechanism Is a Tree

Forking is the fundamental growth mechanism of the docuverse. The relationship between parent and child is explicit:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Account 3.2 is *under* Account 3, not beside it. The User field is a tree, not a flat namespace. This nesting is intentional and structural — it's how the entire address space grows:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

## "Full Control Forevermore" Applies to Your Own Subtree

The quote you're probing:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This means: User 3 controls the *allocation* of 3.1, 3.2, 3.3 — the act of baptism. Once 3.2 is baptized and assigned, User 3.2 has full control over their own subdivision (3.2.1, 3.2.2, ...) forevermore.

These two authorities do not conflict because they operate on disjoint subtrees:

- **User 3** controls: allocation of children directly under 3 (i.e., baptizing 3.1, 3.2, 3.3...)
- **User 3.2** controls: everything under 3.2 (documents, sub-accounts, content)

User 3 cannot modify User 3.2's documents. The ownership guarantee is clear:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

Documents created under account 3.2 are owned by 3.2. Account 3 has no write authority over them.

## Nesting Enables Search, Not Authority

The nesting *is* visible to the search and span mechanisms:

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

A span covering all of Account 3's address range includes everything under 3.2. This is correct for *read* operations — discovery, link search, transclusion. But search is not modification. Finding content is not owning it.

## Can a Parent Revoke a Sub-Account?

This is the harder question, and I did not specify it explicitly. But the architecture implies the answer is **no**, for two reasons:

First, permanence. Addresses, once assigned, are permanent:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

If 3.2 has been baptized and content created under it, revoking 3.2 would invalidate those addresses — violating the fundamental permanence guarantee.

Second, other users may have linked to content under 3.2. Published documents cannot be withdrawn precisely because others depend on them:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

Revoking a sub-account would break others' links — the same reason documents cannot be withdrawn.

## Summary

Account prefixes **nest** — that is by design, not a defect. But nesting creates a *tree of delegation*, not a *hierarchy of authority*. The parent controls baptism (allocation); the child controls content (everything under their address). Neither supersedes the other. Delegation is irrevocable because addresses are permanent.

NEED_RAW: 4/21 — the forking section continues there and may contain additional detail about the parent-child relationship in forking that I have not extracted.

**Gregory question:** Does the account allocation mechanism ever produce multi-component user fields (e.g., user=[2,3] via inc), and does `tumbleraccounteq` distinguish between a single-component account [1,0,2] and a nested multi-component account [1,0,2,3]?

**Gregory's Answer:**

## KB Synthesis

The KB does not contain sufficient information to answer either part of this question definitively.

**Part 1: Multi-component user fields via increment**

The allocation mechanism is documented in [SS-ADDRESS-ALLOC] / [SS-TUMBLER] and related findings, but the KB does not describe carry-overflow behavior in `tumblerincrement`. Concrete examples in the KB only show single-digit user fields (`1.1.0.1`, `1.1.0.2`). The tumbler representation stores each digit as a single decimal digit in a 16-digit mantissa [SS-TUMBLER Finding 0031], and `tumblerincrement` is cited at `tumble.c:599-623`, but its behavior when incrementing past digit `9` (carry propagation) is not captured in any KB entry. Whether a 10th account under a node would produce `1.1.0.10` (as a two-digit mantissa field) or some other representation is not answerable from the KB.

**Part 2: `tumbleraccounteq` discrimination**

`tumbleraccounteq` is mentioned only once in the KB — in [SS-VERSION-ADDRESS Finding 0068] as the ownership predicate used in `docreatenewversion`. The KB records its use (`tumbleraccounteq(isaptr, wheretoputit)`) but does not document its implementation. The containment check is documented separately via `tumblertruncate` + `tumblereq` [SS-TUMBLER-CONTAINMENT], but whether `tumbleraccounteq` uses exact equality of the full account address or prefix matching — and thus whether it treats `1.1.0.2` and `1.1.0.2.3` as distinct accounts — is not stated in any KB entry.

You would need to read `tumble.c` directly to answer both questions.

---

## Code Exploration

Now I have all the evidence needed. Let me compile the full answer.

---

## Account Allocation Mechanism and `tumbleraccounteq` Behavior

### 1. Does allocation ever produce multi-component user fields via `tumblerincrement`?

**The account tumbler itself is never produced by `tumblerincrement`.** The account stored in `player[user].account` is set only two ways:

**a) Hardcoded default** — `be.c:37`:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```
This is immediately copied into `task.account` at `be.c:88`:
```c
movetumbler(&defaultaccount, &task.account);
```

**b) Client-supplied XACCOUNT request** — `fns.c:364–373`:
```c
void xaccount(typetask *taskptr) {
    if (getxaccount(taskptr, &(player[user].account))) {
        putxaccount(taskptr);
    ...
```
`getxaccount` at `get1.c:190–204` simply reads whatever tumbler the client sends off the wire:
```c
gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
taskptr->account = *accountptr;
return(TRUE);
```
There is no internal call to `tumblerincrement` to synthesize a new account tumbler.

**What `tumblerincrement` does produce** are *document addresses*. The path is:

`docreatenewdocument` (`do1.c:234`) → `makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint)` (`do1.c:239`) → `createorglingranf` → `findisatoinsertnonmolecule` (`granf2.c:203`).

In `findisatoinsertnonmolecule`, `depth = 2` when `supertype ≠ subtype` (e.g., ACCOUNT→DOCUMENT) — `granf2.c:209`:
```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```
Then for the first document under account `1.1.0.1` (mantissa=[1,1,0,1,...]):
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  /* granf2.c:237 */
```
`tumblerincrement` (`tumble.c:599`) finds the last non-zero mantissa index (idx=3), then sets `mantissa[3+2] = mantissa[5] += 1`, yielding `1.1.0.1.0.1`. Each subsequent document increments mantissa[5], giving `1.1.0.1.0.2`, `1.1.0.1.0.3`, etc.

**`docreatenode_or_account`** (`do1.c:243`) is the one path that CAN produce a new node-like address via `tumblerincrement`. It uses `makehint(NODE, NODE, 0, ...)` (`do1.c:251`), so `depth=1`, and produces e.g. `1.1.0.1.1`. But the resulting tumbler is returned to the *client*; the client must then issue a separate `XACCOUNT` command to adopt it as their session account — the backend does not do this automatically.

**Conclusion:** `tumblerincrement` produces multi-component *document* addresses, never multi-component *user account* tumblers. The user's account tumbler is always externally supplied or hardcoded.

---

### 2. Does `tumbleraccounteq` distinguish `[1,0,2]` from `[1,0,2,3]`?

**Yes, it does.** The algorithm at `tumble.c:38–70` counts consecutive zeros in the **account** (bptr) mantissa; when it sees the **second** zero, it returns TRUE:

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        if (++j_b == 2) {
            return(TRUE);  /* terminated */
        }
        /* first zero: document may continue here, skip */
    } else {
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);  /* mismatch on non-zero position */
        }
    }
}
```

**Account `[1,0,2]`** (bptr->mantissa = `[1,0,2,0,0,...]`):

| i | bptr->mantissa[i] | action |
|---|---|---|
| 0 | 1 | check aptr[0] == 1 |
| 1 | 0 | j_b=1, skip |
| 2 | 2 | check aptr[2] == 2 |
| 3 | 0 | j_b=2 → **return TRUE** |

The function terminates at position 3. It checks only that aptr[0]==1 and aptr[2]==2.

**Account `[1,0,2,3]`** (bptr->mantissa = `[1,0,2,3,0,...]`):

| i | bptr->mantissa[i] | action |
|---|---|---|
| 0 | 1 | check aptr[0] == 1 |
| 1 | 0 | j_b=1, skip |
| 2 | 2 | check aptr[2] == 2 |
| 3 | 3 | check aptr[3] == 3 |
| 4 | 0 | j_b=2 → **return TRUE** |

This additionally requires aptr[3]==3.

**Direct consequence:** A document `[1,X,2,5,0,1]` (aptr[3]=5) is *inside* account `[1,0,2]` but *outside* account `[1,0,2,3]` — the function returns FALSE at i=3 because 5≠3. These accounts are distinct and the function correctly distinguishes them.

**Corollary asymmetry:** `[1,0,2,3]` is itself *inside* account `[1,0,2]` — when you call `tumbleraccounteq([1,0,2,3], [1,0,2])`, it hits the second zero at i=3 and returns TRUE after confirming positions 0 and 2 match. So `[1,0,2,3]` is effectively a *sub-account* of `[1,0,2]`. The boundary conditions are encoded in how many non-zero components appear between the two zeros.

---

### Summary

| Question | Answer | Key source |
|---|---|---|
| Does allocation produce multi-component account tumblers? | **No** — accounts are always client-supplied via `XACCOUNT` or hardcoded; `tumblerincrement` only produces document/content addresses | `fns.c:368`, `get1.c:190`, `be.c:37` |
| Does `tumblerincrement` ever produce a deeper ISA that looks like a sub-account? | **Yes** — via `docreatenode_or_account` with `depth=1`, yielding e.g. `1.1.0.1.1` — but the backend never automatically assigns this as the session account | `do1.c:251`, `granf2.c:237` |
| Does `tumbleraccounteq` distinguish `[1,0,2]` from `[1,0,2,3]`? | **Yes** — the second-zero terminator fires at different positions (i=3 vs i=4), so `[1,0,2,3]` adds an additional non-zero constraint at position 3 that `[1,0,2]` does not | `tumble.c:54–68` |
