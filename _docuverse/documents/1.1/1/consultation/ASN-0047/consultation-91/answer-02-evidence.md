## Question 2 [evidence]

> In `docreatenewversion` (do1.c), does the implementation perform a lookup or membership check on the version-base tumbler `t` before calling `makehint(DOCUMENT, DOCUMENT, depth=1)`, or does it operate purely on the tumbler structure without verifying that `t` was previously allocated as a document entity?

## KB Synthesis

Based on the KB, `docreatenewversion` operates **purely on tumbler structure** before the `makehint` call — no granfilade membership check occurs at that point.

The ownership predicate gating the `makehint` call is:

```
tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)
```

[ST-VERSION-OWNERSHIP / Finding 0068] describes `tumbleraccounteq` as a tumbler account-prefix comparison and `isthisusersdocument` as a user-ownership check — structural/account-level predicates, not granfilade lookups. Neither queries whether `isaptr` exists as an allocated document entity in the granfilade tree.

The granfilade does get consulted, but later in the call chain:

1. `makehint(DOCUMENT, DOCUMENT, depth=1, isaptr, &hint)` — called based on ownership result, no prior existence check
2. `createorglingranf` → `findisatoinsertnonmolecule` → `findpreviousisagr` — this *is* a granfilade tree traversal, but its purpose is to determine where to allocate the *new* version's address, not to verify the source exists
3. `doretrievedocvspanfoo` — retrieves the source's V-span, which would involve an orgl lookup of `isaptr` in granf, but this comes **after** `makehint` and address allocation

[ST-VERSION / Finding 0077] confirms the call chain: `docreatenewversion` → `createorglingranf` (new doc address) → `doretrievedocvspanfoo` (source V-span lookup) → `docopyinternal`. The `makehint` computation feeds into step 1; the source document lookup is step 2.

Consequence: if `isaptr` is a well-formed tumbler belonging to the user's account but not actually allocated in the granfilade, `makehint` will still be called with `DOCUMENT/DOCUMENT/depth=1`. The containment check inside `findpreviousisagr` [PRE-ADDRESS-ALLOC / Finding 0021] would then find no child under `isaptr`, falling back to allocating `isaptr.1` as the first child — proceeding without error. The failure (if any) would surface later at `doretrievedocvspanfoo` when the source orgl cannot be found.

---

## Code Exploration

I now have all the evidence needed to answer fully.

---

## Answer

**`docreatenewversion` does not perform any granfilade lookup or membership check on the version-base tumbler `t` before `makehint` is called. It operates purely on tumbler arithmetic.**

---

### Execution path, with citations

#### 1. The guard before `makehint` — pure tumbler arithmetic only

`do1.c:270`:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Both predicates are purely structural:

- **`tumbleraccounteq`** [`tumble.c:38-70`]: Compares two tumblers' mantissa arrays positionally, stopping when the account tumbler terminates with two zeros. No I/O, no data structure traversal — pure arithmetic.

- **`isthisusersdocument`** [`be.c:171-176`]: Is itself just `tumbleraccounteq(tp, &taskptrx->account)` — another pure tumbler comparison against the current user's account address.

Neither predicate queries the granfilade. They determine *which hint to build* (DOCUMENT-under-DOCUMENT vs. DOCUMENT-under-ACCOUNT), but say nothing about whether `t` exists as an allocated document entity.

#### 2. `makehint` itself — pure struct initialization

`do2.c:78-84`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

No lookup. `makehint` is a pure field-copy — it stamps `DOCUMENT, DOCUMENT, 0` into `hint` and copies `isaptr`'s tumbler value into `hint.hintisa`.

#### 3. Where the existence check *would* live — and why it's bypassed

The first code in the call chain that *can* query the granfilade is `findisatoinsertgr` [`granf2.c:130-156`], reached after `makehint` via:

```
createorglingranf [do1.c:277]
  → createorglgr [granf2.c:117]
      → findisatoinsertgr [granf2.c:130]
```

`findisatoinsertgr` contains the only `isaexistsgr` call in the new-entity path:

```c
// granf2.c:135-142
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        // ...
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
```

`isaexistsgr` [`granf2.c:244-253`] is the real membership test — it calls `retrieve()` on the crum tree and checks whether the returned `totaloffset` equals `isaptr`. But this guard **only fires when `subtype == ATOM`** (i.e., when inserting text or link content that must have a parent document).

Because `makehint(DOCUMENT, DOCUMENT, 0, ...)` sets `subtype = DOCUMENT`, `findisatoinsertgr` unconditionally takes the `else` branch and calls `findisatoinsertnonmolecule` — **no existence check on `t`**.

`findisatoinsertnonmolecule` [`granf2.c:203-242`] only looks for the highest previously-allocated ISA *under the hint namespace* (to compute the next available address), using `findpreviousisagr`. It does not verify that the hint ISA itself (i.e., `t`) is an allocated entity.

#### 4. The first real check on `t` — happens *after* the new document is created

`do1.c:281-283`:
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
```

`doretrievedocvspanfoo` calls `findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)` [`do1.c:307`], which is a genuine granfilade lookup on `isaptr` (the version-base `t`). This is the first point that would fail if `t` does not exist — but by this line, `createorglingranf` has already written the new version document into the granfilade at line 277. The ordering is:

1. Build `hint` from `t` (pure arithmetic) — line 271  
2. **Allocate and insert the new version document** via `createorglingranf` — line 277  
3. **Then** look up `t` to copy its content into the new version — line 281

---

### Conclusion

The function operates **purely on the tumbler structure** before and during `makehint`. The two conditions at `do1.c:270` check account-prefix membership via tumbler arithmetic, not granfilade membership. No `isaexistsgr`, `findorgl`, or `retrieve` call occurs before `makehint`. The DOCUMENT-subtype path through `findisatoinsertgr` explicitly skips the `isaexistsgr` guard that would verify `t` was previously allocated. A caller that passes an unallocated tumbler as `t` will successfully create a new version document under a nonexistent parent; the failure (if any) comes later at `doretrievedocvspanfoo` when the system tries to copy `t`'s content — not at the allocation step.
