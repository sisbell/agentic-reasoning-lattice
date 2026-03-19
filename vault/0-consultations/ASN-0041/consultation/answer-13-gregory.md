## Question 13 [gregory]

> Does ownership of a node-level tumbler (e.g., `1.1`) automatically confer ownership of all descendant tumblers beneath it (accounts `1.1.0.x`, documents `1.1.0.x.0.y`), or is each level independently assigned?

## KB Synthesis

The KB does not fully answer this question, but provides partial evidence.

## What the KB says

**Ownership is checked at the account level, not node level.**

[SS-VERSION-ADDRESS] (Finding 0068) describes the ownership predicate as:
```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```
where `wheretoputit` is the session's current account address. This comparison is account-scoped — it checks whether the document's account prefix matches the session's active account. There is no mention of node-level (`1.1`) ownership as a separate concept.

**Address hierarchy is structural, not access-control.**

[SS-TUMBLER-CONTAINMENT] and [SS-ADDRESS-SPACE] describe containment (prefix matching via `tumblertruncate` + `tumblereq`) as the mechanism for address hierarchy — e.g., `1.1.0.2.0.1` is *under* `1.1.0.2`. This is used for allocation bounds, not for access grants.

**Account isolation is enforced per-account, not per-node.**

[INV-ACCOUNT-ISOLATION] states documents allocated under one account must have addresses that are proper descendants of that account's address. The unit of isolation is the account (e.g., `1.1.0.2`), not the node (`1.1`).

**Access control is tracked per-document, per-connection.**

[SS-BERT] (Finding 0014) records access at the `(connection, document)` granularity — not at the node or account level.

## What the KB cannot answer

The `isthisusersdocument` function is cited in [ST-VERSION-OWNERSHIP] but not defined in the KB. Whether this function checks node-level containment (i.e., whether owning `1.1` confers ownership of `1.1.0.2.0.1`) cannot be determined from available findings.

**The KB does not describe node-level tumbler ownership as a concept.** The node address (`1.1`) appears only as the top of the hierarchy; the KB's access control entries all operate at account and document levels. Whether `1.1` ownership is independently assigned or derived from higher-level authority is not answerable from this KB.

---

## Code Exploration

I now have everything needed to answer the question definitively. Here is the full analysis:

---

## Tumbler Ownership and Descendant Inheritance in udanax-green

### Short Answer

**Yes**, ownership of a node-level tumbler (e.g., `1.1`) automatically confers ownership of all descendant tumblers beneath it. Each level is **not** independently assigned — ownership is purely hierarchical, determined entirely by a prefix-matching algorithm encoded in `tumbleraccounteq`.

---

### The Ownership Check Chain

Every ownership decision in the backend traces through two functions:

**1. `isthisusersdocument` — the ownership predicate**

Three implementations exist (for different runtime modes), all semantically identical:

- `socketbe.c:197-201`: `return tumbleraccounteq(tp, &(player[user].account));`
- `be.c:171-176`: `return tumbleraccounteq(tp, &taskptrx->account);`
- `xumain.c:198-201`: `return tumbleraccounteq(tp, &taskptrx->account);`

The user's identity is encoded in a single tumbler — the "account tumbler" stored in `player[user].account` (set by `xaccount` via `getxaccount` in `get1fe.c:213-226`). This is an arbitrary tumbler provided by the client; `validaccount` (`get2fe.c:338-341`) always returns `TRUE` — there is no validation.

**2. `tumbleraccounteq` — the core algorithm**

`tumble.c:38-70`:

```c
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    // bptr = account tumbler (the "owner")
    // aptr = document tumbler being tested
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  // two zeros = end of account space → document is owned
            }
            // first zero: skip (account boundary separator)
        } else {
            // non-zero: document must match exactly
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The algorithm is a **prefix matcher with a double-zero terminator**. The account tumbler's mantissa is scanned; when **two consecutive zeros** are encountered, the function returns `TRUE` unconditionally — meaning all remaining digits of the document tumbler are irrelevant. The document is owned.

---

### How the Tumbler Hierarchy Encodes Levels

From `xanadu.h:140-143`:
```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

Zeros act as level separators in the mantissa array. The address space structure is:

| Level    | Example address | Mantissa layout         |
|----------|-----------------|-------------------------|
| Node     | `1.1`           | `[1, 1, 0, 0, ...]`     |
| Account  | `1.1.0.1`       | `[1, 1, 0, 1, 0, 0, ...]` |
| Document | `1.1.0.1.0.1`   | `[1, 1, 0, 1, 0, 1, 0, 0, ...]` |

---

### Node `1.1` Owns Everything Beneath It

Trace `tumbleraccounteq` with:
- `bptr` = node `1.1` → mantissa `[1, 1, 0, 0, ...]`
- `aptr` = document `1.1.0.1.0.3` → mantissa `[1, 1, 0, 1, 0, 3, ...]`

```
i=0: bptr[0]=1, aptr[0]=1 → match (j_b=0)
i=1: bptr[1]=1, aptr[1]=1 → match (j_b=0)
i=2: bptr[2]=0 → j_b=1 (first zero, skip)
i=3: bptr[3]=0 → j_b=2 → return TRUE  ← triggered immediately
```

The double-zero in the node tumbler fires at positions 2–3 before any account or document digits are examined. **Every tumbler that begins with `1.1` is owned**, regardless of what follows.

---

### Account `1.1.0.1` Owns Only Its Documents

Trace with:
- `bptr` = account `1.1.0.1` → mantissa `[1, 1, 0, 1, 0, 0, ...]`
- `aptr` = document `1.1.0.1.0.3` → mantissa `[1, 1, 0, 1, 0, 3, ...]`

```
i=0: bptr[0]=1, aptr[0]=1 → match
i=1: bptr[1]=1, aptr[1]=1 → match
i=2: bptr[2]=0 → j_b=1 (skip)
i=3: bptr[3]=1, aptr[3]=1 → match (j_b still 1)
i=4: bptr[4]=0 → j_b=2 → return TRUE
```

And with sibling account `1.1.0.2`'s document:
- `bptr` = `1.1.0.1` → `[1, 1, 0, 1, ...]`
- `aptr` = `1.1.0.2.0.1` → `[1, 1, 0, 2, ...]`

```
i=3: bptr[3]=1, aptr[3]=2 → MISMATCH → return FALSE
```

Account `1.1.0.1` does NOT own documents under `1.1.0.2`.

---

### Where This Check Is Applied

`bert.c:81` — the fallback in `checkforopen` (the document-open access gate):

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // allowed to open
}
```

If no bert entry exists for the document (it's not already locked by another connection) and either the request is READ-only or the document is owned, the open is permitted.

`do1.c:270` — `docreatenewversion` uses the same check to decide the address hint strategy:

```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Own document → allocate under it. Someone else's → allocate under your own account.

---

### No Independent Level Assignment

There is no mechanism to grant or restrict ownership at individual levels below the account tumbler. The account tumbler in `player[user].account` is set once per session via `xaccount` (`fns.c:368`, `get1fe.c:223-224`), and all subsequent ownership checks are derived purely from `tumbleraccounteq` prefix matching against that single stored value.

**Summary:** Ownership cascades downward through the double-zero terminator rule. A node tumbler `1.1` contains two consecutive zeros in positions 2–3 of its mantissa; `tumbleraccounteq` hits them immediately and returns TRUE for any descendant. An account tumbler `1.1.0.x` contains its terminating zeros one level deeper; it owns documents under it but not those under sibling accounts. Each level is **not** independently assigned — the entire hierarchy is implicit in the prefix structure of a single tumbler.
