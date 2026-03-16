## Question 14 [gregory]

> Can a user delegate a sub-range of their tumbler space to another entity — for example, granting `1.1.0.2.0.100` through `1.1.0.2.0.200` to a collaborator — or is address-space authority strictly one level deep (node delegates to user, user delegates to documents, no further)?

## KB Synthesis

The KB does not describe any sub-range delegation mechanism. Based on what is documented, address space authority is strictly structural and follows the tumbler hierarchy — there is no way to carve out a sub-range and grant another entity allocation rights within it.

**What the hierarchy actually is:**

[SS-ADDRESS-SPACE] (Finding 0021) documents the `makehint` depth table:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| NODE | NODE | 1 | Node under node |
| ACCOUNT | DOCUMENT | 2 | Document under account |
| DOCUMENT | DOCUMENT | 1 | Version under document |

Documents are allocated directly under accounts — there is no intermediate "sub-account" or "delegated range" level in the hierarchy.

**How ownership is determined:**

VERSION allocation (Finding 0068) uses `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` — a binary account-level prefix comparison. You either own the account prefix or you don't. There is no predicate of the form "this entity is authorized over the range `account.0.100` through `account.0.200`."

**What BERT provides instead:**

[SS-BERT] (Finding 0014) provides document-level access control (READBERT / WRITEBERT) over individual documents, not over address ranges. This lets a connection *operate on* existing documents in another account's space, but does not grant the ability to *allocate* new addresses within it.

**Conclusion:**

The KB describes no delegation mechanism. Address space authority follows the structural hierarchy: a session's account context (set per-session, per [SS-SESSION-STATE]) determines where new documents are allocated, and the allocation algorithm ([SS-ADDRESS-ALLOC]) always places new addresses under the current session's account. Granting a collaborator the ability to allocate within `1.1.0.2.0.100–200` would require giving them the account `1.1.0.2` context — there is no finer-grained mechanism documented. Whether such a mechanism *could* be built on top of the tumbler containment predicate [SS-TUMBLER-CONTAINMENT] is a design question, not an implementation fact answerable from this KB.

---

## Code Exploration

I now have everything needed to answer the question. Let me compile the full code-grounded analysis.

---

## Can a User Delegate a Sub-Range of Tumbler Space?

**Short answer: No. The ownership model is structurally capped at one level below the account, and `tumbleraccounteq` — the sole ownership test — cannot represent a sub-range delegation. The `validaccount` function is also an unimplemented stub that returns `TRUE` unconditionally, meaning there is no server-side verification of account identity at all.**

---

### 1. The Account Tumbler IS the Authority Token

Each connected session has a single account tumbler stored in the `PLAYER` struct (`players.h:20`):

```c
typedef struct _player {
    ...
    tumbler account;    /* xanadu host and account tumbler */
} PLAYER;
```

This tumbler is set during the `XACCOUNT` handshake (`get1fe.c:213-226`):

```c
bool getxaccount(typetask *taskptr, typeisa *accountptr)
{
    ...
    gettumbler(taskptr, accountptr) && validaccount(taskptr, accountptr);
    player[user].account = *accountptr;
    taskptr->account = *accountptr;
    return(TRUE);
}
```

Critically, `validaccount` in both `get2.c:157-160` and `get2fe.c:338-341` is a stub:

```c
bool validaccount(typetask *taskptr, typeisa *accountptr)
{
    return (TRUE);
}
```

**There is no server-side authentication of account identity.** Any client can claim any account tumbler.

---

### 2. The Ownership Test: `tumbleraccounteq`

`isthisusersdocument` in `socketbe.c:197-201` (and `be.c:171-176`) performs the sole ownership check:

```c
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account) !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

`tumbleraccounteq` in `tumble.c:38-70` compares a document tumbler (aptr) against the session account tumbler (bptr):

```c
for (j_b = 0, i = 0; i < NPLACES; i++) {
    if (bptr->mantissa[i] == 0) {
        /* Account has a zero - check if it's the terminator (second zero) */
        if (++j_b == 2) {
            return(TRUE);  /* Account terminated, document is under this account */
        }
        /* First zero in account - document can have any value here */
    } else {
        /* Account has non-zero - document must match exactly */
        if (aptr->mantissa[i] != bptr->mantissa[i]) {
            return(FALSE);
        }
    }
}
return (TRUE);
```

The algorithm terminates the comparison as soon as it encounters **two zeros in the account tumbler's mantissa**. For account `1.1.0.2` with mantissa `[1, 1, 0, 2, 0, 0, ...]`:

| index | account mantissa | action |
|-------|-----------------|--------|
| 0 | 1 | doc[0] must == 1 |
| 1 | 1 | doc[1] must == 1 |
| 2 | 0 | first zero → j_b=1, skip |
| 3 | 2 | doc[3] must == 2 |
| **4** | **0** | **second zero → j_b=2 → return TRUE** |

The comparison terminates at the second zero — positions 5 and beyond in the document are never examined.

---

### 3. Why Sub-Range Delegation Fails Structurally

The question is whether a sub-range account like `1.1.0.2.0.100` (mantissa `[1, 1, 0, 2, 0, 100, 0, ...]`) could be used to restrict a collaborator to only the range `1.1.0.2.0.100.*`.

Tracing `tumbleraccounteq` with account `1.1.0.2.0.100`:

| index | account mantissa | action |
|-------|-----------------|--------|
| 0 | 1 | doc[0] must == 1 |
| 1 | 1 | doc[1] must == 1 |
| 2 | 0 | first zero → j_b=1, skip |
| 3 | 2 | doc[3] must == 2 |
| **4** | **0** | **second zero → j_b=2 → return TRUE immediately** |
| 5 | 100 | **(never reached)** |

**The digit `100` at position 5 is never checked.** Account `1.1.0.2.0.100` is ownership-equivalent to account `1.1.0.2` — both claim exactly the same set of documents. A collaborator given account `1.1.0.2.0.100` would own all documents under `1.1.0.2`, not just the sub-range.

---

### 4. Document Address Allocation Uses Account as Hint

`docreatenewdocument` (`do1.c:234-241`) places new documents relative to the current session's account:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

In `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// ACCOUNT(2) != DOCUMENT(3), so depth = 2
...
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
// First doc under 1.1.0.2 → mantissa[3+2] = mantissa[5] = 1
// Result: 1.1.0.2.0.1
```

If the session account were set to `1.1.0.2.0.100`, documents would be created at `1.1.0.2.0.100.0.1`, `1.1.0.2.0.100.0.2`, etc. — these ARE in the sub-space. But the ownership check would still permit that account to open/modify any document under `1.1.0.2`, not just those sub-addresses. The sub-space confinement for creation is not matched by sub-space confinement for access.

---

### 5. The `CREATENODE_OR_ACCOUNT` Mechanism Does Not Add Delegation

`docreatenode_or_account` (`do1.c:243-258`) uses `makehint(NODE, NODE, ...)`, which allocates sub-nodes with depth=1 (since supertype == subtype). This creates new entries in the granfilade one level deeper than the hint, but it does not establish any delegation relationship. The ownership check is still `tumbleraccounteq`, which cannot represent sub-range authority.

`docreatenewversion` (`do1.c:260-298`) explicitly calls `isthisusersdocument` for its branching logic (`do1.c:270`), but again only at the account level.

---

### 6. The Hardcoded Default Account

`socketbe.c:35` and `be.c:37` define:

```c
// socketbe.c
tumbler defaultaccount = {0,0,0,0,  1,1,0,14,0};  // 1.1.0.14
// be.c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

These are used as fallback accounts. The fact that both implementations use flat three-level accounts (`1.1.0.N`) confirms the design intent: the hierarchy is Node → Account → Documents, with no intended sub-account level.

---

## Summary

The authority model in udanax-green is **strictly one level deep** at the user layer:

```
Node (1.1)
  └── Account (1.1.0.N)         ← one XACCOUNT per session, self-reported, unverified
        └── Documents (1.1.0.N.0.M)  ← owned iff tumbleraccounteq matches
```

**There is no sub-range delegation** because:

1. **`tumbleraccounteq` terminates at the second zero** in the account mantissa — any digits beyond that in a "sub-account" are never examined (`tumble.c:54-68`).
2. A hypothetical sub-range account like `1.1.0.2.0.100` would claim ownership of ALL documents under `1.1.0.2`, not just the sub-range `1.1.0.2.0.100.*`.
3. **`validaccount` is a stub** returning `TRUE` unconditionally (`get2fe.c:338-341`, `get2.c:157-160`), so there is no server-side enforcement of which account a client is entitled to claim.
4. The protocol's `XACCOUNT` request (`get1fe.c:213-226`) simply stores whatever tumbler the client sends; there is no challenge/response or cryptographic binding.

To support sub-range delegation, the codebase would require at minimum: a new ownership predicate that can check sub-range containment (not just the two-zero termination logic), plus server-side verification that the account presented is one the client is authorized to use.
