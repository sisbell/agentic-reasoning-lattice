## Question 2 [evidence]

> When udanax-green's docreatenewversion spawns a version chain under document t, does the granfilade machinery treat t itself as a member of the spawning allocator's tracked domain, or is t only the "parent" pointer with its membership tracked elsewhere?

## KB Synthesis

The granfilade machinery treats `t` purely as a **structural reference anchor** (parent pointer), not as a tracked domain member in any allocator-local sense. Here is the synthesis:

**`t` is already in the granfilade from its own creation.** When version spawning begins, `t`'s node exists in the flat granfilade tree. The version allocator does not register `t` — it was registered at `t`'s own creation by a prior `findisatoinsertnonmolecule` call [SS-ADDRESS-ALLOC].

**The spawning allocator uses `t` only to compute two bounds.** From [SS-ADDRESS-ALLOC] (Finding 0068):
1. `upperbound = tumblerincrement(t, depth-1=0, 1)` — the next sibling of `t` (e.g., `1.1.0.1.0.2` for `t = 1.1.0.1.0.1`)
2. A containment check: the found candidate must satisfy `prefix_match(candidate, t)`

`findpreviousisagr` then searches the existing granfilade tree for the highest address below `upperbound`. The containment check (added to fix Bug 0013 [PRE-ADDRESS-ALLOC]) verifies the candidate actually lives under `t`, preventing cross-account pollution.

**The granfilade tree IS the tracking domain.** From [SS-ADDRESS-SPACE] (Finding 0077): "There is no single global Σ.next counter. Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`." There is no separate allocator object with its own membership list. The granfilade tree holds `t` and all its version children as nodes; the allocation algorithm just queries that tree bounded by `t`.

**`t`'s own membership is tracked no differently from any other node.** It is an entry in the flat granfilade tree. What the version-spawning call does is search *within `t`'s subtree* for the highest existing child, then allocate the next sequential address under `t` [ST-ADDRESS-ALLOC]. `t` participates as a search boundary, not as an element of some spawner-local registry.

In short: `t` is the parent pointer. The granfilade tree is the sole domain tracker.

---

## Code Exploration

I now have all the information needed to give a complete answer. Let me synthesize:

---

## Answer: `t` is the Hint Anchor, Not a Domain Member

When `docreatenewversion` creates a new version of document `t`, the granfilade machinery does **not** treat `t` as a member of the spawning allocator's tracked domain. `t` functions solely as the `hintisa` address anchor. Here is the full trace.

---

### 1. Hint construction — two branches, one using `t` as `hintisa`

`docreatenewversion` [do1.c:260–299] immediately branches on ownership:

```c
// do1.c:270-276
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint(DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

`makehint` [do2.c:78–84] merely populates the `typehint` struct fields:

```c
hintptr->supertype = typeabove;  // DOCUMENT or ACCOUNT
hintptr->subtype   = typebelow;  // DOCUMENT
hintptr->atomtype  = typeofatom; // 0
movetumbler(isaptr, &hintptr->hintisa); // copy of t's tumbler (own-version case)
```

`typehint` [xanadu.h:148–153]:
```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;   // <-- t's address goes here
} typehint;
```

In the own-version case, `hintisa = t`. In the cross-user case, `hintisa = wheretoputit` (the target account), and `t` does not appear in the hint at all.

---

### 2. `createorglingranf` → `createorglgr` — only `newisaptr` is inserted

`createorglingranf` [granf1.c:50–55] calls `createorglgr` [granf2.c:111–128]:

```c
// granf2.c:117-127
if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);
// ...
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);  // isaptr = newisaptr
```

`isaptr` here is `newisaptr` — the output parameter for the new address. `t` is not touched. Only `newisaptr` is written into the granfilade.

---

### 3. `findisatoinsertnonmolecule` — t is the address anchor, not a registrant

Because `hintptr->subtype == DOCUMENT` (not `ATOM`), `findisatoinsertgr` [granf2.c:130–156] skips `isaexistsgr` entirely and goes straight to:

```c
// granf2.c:152
findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
```

Inside `findisatoinsertnonmolecule` [granf2.c:203–242]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
// Own version: DOCUMENT==DOCUMENT => depth=1
// Cross-user:  ACCOUNT!=DOCUMENT  => depth=2
```

For the **own-version case** (`depth=1`, `hintisa = t`):

```c
// granf2.c:213
tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);
// depth-1 = 0: upperbound = t + 1 at t's top level (next sibling address)
```

`findpreviousisagr` [granf2.c:255–278] then walks the granfilade tree to find the last ISA below `upperbound`. If no version of `t` exists yet, `lowerbound` comes back as `t` itself.

```c
// granf2.c:235-241
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    // depth=1: new addr = t.0.1 (one level nested under t)
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
    // subsequent version: t.0.2, t.0.3, ...
}
```

`tumblerincrement` [tumble.c:599–623] adds `bint` at position `last_nonzero_index + rightshift`. With `rightshift=1` (depth=1), the new digit is appended one position to the right of `t`'s last digit, creating a **tumbler-child** of `t` in the address space. The first version gets address `t.0.1`, the second `t.0.2`, etc.

**Critically: `t` is not re-inserted here.** `t`'s own granfilade entry was created when `t` was first created (by its own call to `createorglingranf`). `findisatoinsertnonmolecule` is read-only with respect to `t` — it only reads `t`'s position to navigate the address space.

---

### 4. Bert table (runtime tracked domain) — only `newisaptr` is enrolled

After the granfilade insertion, `docreatenewversion` [do1.c:292–296]:

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);   // do1.c:292
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
logbertmodified(newisaptr, user);              // do1.c:295
doclose(taskptr, newisaptr, user);             // do1.c:296
```

`addtoopen` [bert.c:128–151] inserts a `bertentry` for `newisaptr` keyed by its tumbler hash. `t` is not added, not incremented, not touched. The only access to `t`'s data is via `doretrievedocvspanfoo` [do1.c:281–308], which calls `findorgl` with `NOBERTREQUIRED` [do1.c:307] — bypassing the bert check entirely.

`addtoopen`'s `bertentry` struct [bert.c:13–19]:
```c
typedef struct {
    int connection;
    tumbler documentid;  // newisaptr, not t
    char created, modified;
    int type;
    int count;
} bertentry;
```

---

### 5. Summary

| Layer | Role of `t` | Role of `newisaptr` |
|---|---|---|
| `typehint.hintisa` | Address anchor (own-version case only) | Target of allocation |
| Granfilade (`insertseq`) | Not touched | Inserted as `GRANORGL` |
| Address computation | Parent in tumbler hierarchy (`t.0.1`, `t.0.2`, …) | New leaf address |
| Bert table | Not enrolled | Added via `addtoopen` |

**`t` is purely the parent pointer in the tumbler address hierarchy.** Its granfilade membership — the `GRANORGL` node at `t`'s own address — was established when `t` was created and is never re-registered here. The granfilade has no concept of "spawning allocator domain membership" as a separate tracking mechanism: domain membership is implicit in tumbler address structure (nesting depth and prefix). `t`'s membership is tracked by its own granfilade leaf, not by anything `docreatenewversion` does. Only `newisaptr` is both inserted into the granfilade (`insertseq`, granf2.c:125) and enrolled in the bert table (`addtoopen`, do1.c:292).
