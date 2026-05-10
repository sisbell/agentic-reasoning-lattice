## Question 19 [gregory]

> When multiple FEBE sessions have the same document open with READBERT, and one session upgrades to WRITEBERT, does `checkforopen` reject the upgrade while other readers hold the document, or is there no upgrade path (must close and reopen)?

## KB Synthesis

Based on the KB, there is **no upgrade path** — the session must close and reopen.

From [PRE-OPEN-DOC] Finding 0014, `checkforopen` returns -1 (denied) for:

> **WRITE request on a document open for READ by any connection → -1 (denied)**

The rule says "any connection" with no carve-out for same-connection upgrades. When other sessions hold READBERT, a WRITE request from the upgrading session still hits this rule and is denied.

Finding 0006 in [PRE-OPEN-DOC] confirms the consequence:

> "To change access mode, the document must be closed and reopened."

The only asymmetric case is the reverse direction: READ requests from the same connection that holds WRITE get silently upgraded to WRITE (`checkforopen` returns WRITE). The downgrade/upgrade path in the opposite direction (READ→WRITE) does not exist.

Combined with [INV-WRITE-EXCLUSIVITY]: write requires that no other connection holds any access. So even if only the requesting session holds READBERT, upgrading in-place to WRITEBERT is not supported by the access matrix — the session must close its READ handle first, after which `checkforopen` can issue the WRITE token if no other readers remain.

---

## Code Exploration

---

## Answer: READBERT-to-WRITEBERT Upgrade in `checkforopen`

**There is no upgrade path.** `checkforopen` rejects same-connection WRITEBERT requests when READBERT is already held, and the data model has no mechanism to promote an existing entry. A session must close and reopen.

Here is the full code trace.

---

### 1. The `bertentry` struct has a fixed `type` field

`bert.c:13–19`:
```c
typedef struct {
    int connection;
    tumbler documentid;
    char created,modified;
    int type;          // READBERT=1 or WRITEBERT=2
    int count;
} bertentry;
```

`addtoopen` (`bert.c:128`) creates a new entry with a fixed type. There is no `upgradeopen`, `modifyopen`, or mutation of `bert->type` anywhere in the codebase — the type is immutable after creation.

---

### 2. Same connection: `checkforopen` returns -1 for WRITEBERT when READBERT is held

`bert.c:66–72`:
```c
if (connection == bert->connection) {
    switch (bert->type) {
        case READBERT:
            return (type == READBERT) ? READBERT : /* WRITE */ -1;
        case WRITEBERT:
            return WRITEBERT;
    }
}
```

When the **same connection** that holds READBERT calls `checkforopen(..., WRITEBERT, connection)`:
- `connection == bert->connection` → TRUE
- `bert->type == READBERT` → matches `case READBERT`
- `type == READBERT` is FALSE (requesting WRITEBERT)
- Returns **-1** ("new version should be made")

This is also confirmed by the inline comment table at `bert.c:44–50`:
```
type         Open READ  conn==   →  WRITE request → -1
```

---

### 3. What `-1` means in `doopen` — no in-place upgrade, only version fork

`bert.c:279–299`:
```c
openState = checkforopen(tp, type, connection);

if (openState == 0) {
    addtoopen(tp, connection, FALSE, type);   // normal open
    return 1;
}

switch (mode) {
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, ...);  // forks a new version
        addtoopen(newtp, connection, TRUE, type);
    }
    ...
case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) {
        return 0;   // FAIL — no upgrade, no fork
    }
```

- **`BERTMODECOPYIF` + -1**: triggers `docreatenewversion`, opening a *new document version* as WRITEBERT. The original READBERT entry is untouched.
- **`BERTMODEONLY` + -1**: returns 0 (failure). The `myopen` handler in `fns.c:394–401` then sends `putrequestfailed`.

Neither path promotes the existing READBERT entry to WRITEBERT. There is no fork-free upgrade.

---

### 4. Cross-connection case: readers don't block a different writer (if owner)

When **other** connections hold READBERT and a **different** connection requests WRITEBERT:

`bert.c:73–77`:
```c
} else {
    if (bert->type != READBERT) {
        foundnonread = TRUE;
    }
}
```

Other connections' READBERT entries are silently skipped — they do **not** set `foundnonread`. After the loop:

`bert.c:81–85`:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;
}
```

`isthisusersdocument` (`socketbe.c:197–201`) checks `tumbleraccounteq(tp, &(player[user].account))` — whether the document's tumbler account matches the requesting user's account.

- **Document is owned by requester**: returns 0 → `doopen` calls `addtoopen(..., WRITEBERT)`, creating a *new* independent WRITEBERT entry alongside the existing READBERT entries. **Both entries coexist in the bert table** — there is no reader/writer mutual exclusion enforced at this layer.
- **Document not owned by requester**: returns -1 → COPYIF creates a fork, ONLY fails.

---

### 5. No `upgradeopen` anywhere

A complete grep confirms there is no function that mutates `bert->type`:
- `addtoopen` (`bert.c:128`): sets type at creation, never modifies it
- `incrementopen` (`bert.c:112`): only touches `bert->count`
- `removefromopen` (`bert.c:154`): removes the entry entirely
- `exitbert` (`bert.c:195`): bulk cleanup on disconnect

---

### Summary

| Scenario | `checkforopen` result | Outcome |
|---|---|---|
| Same connection holds READBERT, requests WRITEBERT | -1 | COPYIF: new version forked as WRITEBERT. ONLY: failure. |
| Different connection holds READBERT, same user requests WRITEBERT | 0 (if owner) | New WRITEBERT entry added; READBERT entry remains — no mutual exclusion |
| Different connection holds READBERT, different user requests WRITEBERT | -1 | COPYIF: new version. ONLY: failure. |

**The answer is: there is no upgrade path.** `checkforopen` returns -1 when the same connection already holds READBERT and requests WRITEBERT (`bert.c:69`). The only way to hold WRITEBERT is to either (a) close the READBERT first and reopen as WRITEBERT with a fresh `doopen` call, or (b) use `BERTMODECOPYIF` which forks an entirely new document version rather than upgrading in place.
