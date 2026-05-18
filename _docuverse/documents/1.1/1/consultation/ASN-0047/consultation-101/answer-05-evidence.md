## Question 5 [evidence]

> In udanax-green, when a node or account is created in the granfilade, are the account or document sub-allocators under it immediately available to accept inc-emissions, or is there a separate activation/registration step before the first child can be allocated?

## KB Synthesis

## No Separate Activation Step

The granfilade has no sub-allocator registration or activation mechanism. Child allocation under a new account or document address is immediately possible.

### Why: The Allocation Algorithm Handles the Zero-Children Case Inline

[SS-ADDRESS-ALLOC] / Finding 0021 describes `findisatoinsertnonmolecule`:

1. Compute upper bound: `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent
2. Call `findpreviousisagr` — find the highest existing address below that bound
3. **If nothing found under the parent → allocate first child at `hintisa.0.1`**
4. If something found → truncate and increment to produce the next sibling

Step 3 is the key: the empty-children case is handled inline without any prerequisite registration. The algorithm detects "nothing exists here yet" and synthesizes the first child address directly.

### Why: There Are No Sub-Allocators

[SS-ADDRESS-SPACE] / Finding 0021 confirms:

> "The entire granf (global address enfilade) is a single flat tree; the allocation algorithm enforces hierarchical structure by bounding searches to the parent's address range."

[SS-ADDRESS-SPACE] / Finding 0077 further states:

> "There is no single global 'next' counter (no Σ.next). Allocation is stateless query-and-increment on different tumbler ranges via `findpreviousisagr`."

There are no per-account or per-document counters, registries, or sub-trees — just one flat granfilade. The hierarchy is enforced by the search bounds passed to `findpreviousisagr`, not by any registered sub-space.

### The Containment Check Is Purely Structural

[SS-TUMBLER-CONTAINMENT] / Finding 0021 shows the containment predicate is `tumblertruncate(A, length(B)) == B` — a tumbler string comparison. It does not verify that the parent address itself has an existing orgl entry. The parent address functions as a namespace prefix immediately upon being specified as a hint.

### Confirmed Across Allocation Variants

This zero-children behavior holds for all allocation types:
- **Documents under accounts**: `findpreviousisagr` finds nothing → allocates `account.0.1` [SS-ADDRESS-ALLOC] / Finding 0021
- **Versions under documents**: "If no child exists: allocates first child as `source_doc.1`" [SS-ADDRESS-ALLOC] / Finding 0068
- **Links under documents**: "If no links exist yet (`lowerbound < docISA.2.2`), allocate at `docISA.2.2.1`" [SS-ADDRESS-ALLOC] / Finding 0065

In all cases, the first-child path is a direct fallback within the allocation function — no registration step precedes it.

---

## Code Exploration

I now have everything needed to give a complete answer.

---

## Answer: Granfilade Sub-Allocator Activation in udanax-green

There are **two distinct subsystems** to separate: *granfilade address allocation* (ISA emission) and *content access* (the BERT gate). They behave differently after creation.

---

### 1. Creating a Node/Account in the Granfilade

Both creation paths converge on `createorglgr` (`granf2.c:111-128`):

**Account/document creation** (`do1.c:234-241`):
```c
makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf (taskptr, granf, &hint, isaptr));
```

**Node creation** (`do1.c:243-258`):
```c
makehint (NODE, NODE, 0, &isa, &hint);
result = createorglingranf (taskptr, granf, &hint, &isa);
```

Both call `createorglgr` (`granf2.c:111-128`), which does:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
reserve ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
locinfo.granstuff.orglstuff.orglincore = TRUE;
locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
rejuvinate ((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
return (TRUE);
```

This **atomically inserts a GRANORGL crumb** into the granfilade. The embedded POOM enfilade is freshly allocated in-core (`orglincore = TRUE`, `diskblocknumber = DISKPTRNULL`). There is **no call to `addtoopen`** — the node exists in the granfilade but is unregistered in BERT.

---

### 2. Sub-Allocator Address Emission — Immediately Available

After creation, can the new node accept a child address allocation (inc-emission)? **Yes, immediately.** The allocation path does not touch BERT at all.

Entry point: `findisatoinsertgr` (`granf2.c:130-156`):

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { ... return (FALSE); }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

For non-ATOM hints (creating documents under an account, or sub-nodes), `findisatoinsertnonmolecule` (`granf2.c:203-242`) is called. It computes the next child address purely by granfilade traversal:

```c
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // first child: hintisa.0.1
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr,...,1,isaptr);  // next child: increment highest
}
```

`findpreviousisagr` (`granf2.c:255-278`) is pure enfilade traversal — no `checkforopen`, no BERT lookup. The sub-allocator is live the moment `insertseq` returns in `createorglgr`.

For **ATOM subtypes** (text/link content into a document), there is one existence check at `granf2.c:136`:
```c
if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { return (FALSE); }
```
`isaexistsgr` (`granf2.c:244-253`) uses `retrieve` on the granfilade — again purely granfilade state, not BERT. The parent document just needs to be present as a crumb.

---

### 3. Content Operations — Require Separate Activation

Although address allocation is immediate, any operation that *accesses the orgl* (content insertion, retrieval, rearrange, delete) must pass through `findorgl` (`granf1.c:17-41`):

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            *orglptr = NULL;
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`checkforopen` (`bert.c:52-87`) consults the BERT hash table. For a freshly created, unregistered node with `type == READBERT` or `WRITEBERT`, the result for the owning user is:

```c
// bert.c:81 — no table entry found, foundnonread == FALSE
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;   // "open required"
}
```

`0 <= 0` is true, so `findorgl` returns `FALSE` in daemon mode (`!isxumain`). Every path that writes content — `doinsert` → `docopy` → `findorgl(WRITEBERT)` [`do1.c:55`], `dorearrange` → `findorgl(WRITEBERT)` [`do1.c:40`], `doretrievedocvspan` → `findorgl(READBERT)` [`do1.c:318`] — fails until BERT is satisfied.

**The activation step is `doopen`** (`bert.c:264-322`) via the FEBE `OPEN` command (`fns.c:388-401`):

```c
bool doopen(...) {
    ...
    openState = checkforopen(tp, type, connection);
    if (openState == 0) {
        addtoopen(tp, connection, FALSE, type);   // registers in BERT table
        tumblercopy(tp, newtp);
        return 1;
    }
    ...
}
```

`addtoopen` (`bert.c:128-151`) allocates a `bertentry` and inserts it into the hash table, making subsequent `checkforopen` calls return a positive value.

**One exception**: `docreatenewversion` (`do1.c:260-299`) bypasses `doopen` entirely and calls `addtoopen` directly after `createorglingranf`:

```c
addtoopen(newisaptr, user, TRUE, WRITEBERT);   // do1.c:292
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
logbertmodified(newisaptr, user);
doclose(taskptr, newisaptr, user);
```

This is the only creation path that self-activates — it opens the new version internally, copies content, then closes it, all within `docreatenewversion`. Neither `docreatenewdocument` nor `docreatenode_or_account` do this.

---

### Summary

| Capability | Available Immediately After `createorglgr`? |
|---|---|
| Granfilade address allocation (ISA/inc-emission) via `findisatoinsertnonmolecule` | **Yes** — pure granfilade traversal, no BERT consulted |
| Parent existence check for ATOM allocation (`isaexistsgr`) | **Yes** — granfilade `retrieve`, not BERT |
| Content access via `findorgl` (insert, retrieve, copy, rearrange) | **No** — requires prior `doopen` → `addtoopen` (BERT registration) |

After `createorglgr` returns, the node's sub-allocator can immediately emit child ISAs to callers of `findisatoinsertgr`. No separate registration is needed for address space allocation. However, before the first content operation can succeed on the newly created node or any child document, the FEBE `OPEN` command must be sent, which registers the address in the BERT table via `addtoopen`. Without that step, `findorgl` returns FALSE and all content operations fail silently in daemon mode.
