## Question 5 [evidence]

> What does docreatenewversion (do1.c:271) require of the base document — must the base ISA exist in storage, and does the implementation enforce sequential version numbers?

## KB Synthesis

Two distinct questions — here are the answers from the KB.

---

**Must the base ISA exist in storage?**

Yes, implicitly. `docreatenewversion` has three sequential steps [ST-VERSION-CREATE, Finding 0032]:

1. **Allocate** new orgl via `createorglingranf` (calls `findisatoinsertnonmolecule`)
2. **Retrieve** the source document's V-span via `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`
3. **Copy** content via `docopyinternal` → `insertspanf`

Step 2 reads the source document's root POOM node (`cdsp.dsas[V]`, `cwid.dsas[V]`). If the base ISA doesn't exist as a real orgl in the granfilade, this read returns zeros or uninitialised state, silently producing an empty version rather than failing loudly [ST-VERSION-CREATE, Finding 0043 — `retrievedocumentpartofvspanpm` is self-described as "a kluge"]. The KB states the precondition is "simply that the source document exists" but notes no explicit runtime assertion enforces this [ST-VERSION-CREATE, Finding 0032].

Step 1 also needs the base ISA present for the ownership check — `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)` — which governs whether the new address lands under the source doc or the creating account [SS-VERSION-ADDRESS, Finding 0068].

---

**Does the implementation enforce sequential version numbers?**

Not by a dedicated counter. Sequentiality is an emergent property of the query-and-increment allocation mechanism [SS-ADDRESS-ALLOC, Finding 0068]:

1. `findpreviousisagr` walks the granfilade tree to find the **highest existing child address** under the source document.
2. `tumblerincrement` adds 1 to produce the next address.

Because the granfilade is append-only and addresses are never freed [INV-NO-IADDR-REUSE, INV-MONOTONIC, Finding 0068], deleting a version does not recover its slot. The concrete result: versions emerge as `.1`, `.2`, `.3`, ... monotonically without gaps under normal use. But this is a structural consequence of the persistent tree state, not a sequence counter the implementation "enforces" — concurrent allocations from two sessions on the same account would each query the same tree and produce distinct sequential addresses [INV-GLOBAL-ADDRESS-UNIQUENESS, Finding 0022].

**Summary:** The base ISA must exist for semantically correct results (the implementation doesn't fail loudly if it doesn't). Sequential version numbers are guaranteed by the monotonic query-and-increment allocator operating on a never-shrinking granfilade, not by explicit enforcement.

---

## Code Exploration

I now have all the information needed. Let me compile the complete answer.

---

## `docreatenewversion` — Base ISA and Version Number Analysis

### Function Signature and Call Context

`docreatenewversion` [do1.c:260] has four parameters:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
```

When invoked via the FEBE handler `createnewversion` [fns.c:295-297], the same address is passed for both `isaptr` and `wheretoputit`:
```c
docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa)
```

---

### Question 1: Must the Base ISA Exist in Storage?

**Yes — the base ISA must exist as a live orgl in granfilade storage. This is enforced by a required retrieval of the base document's vspan. The base does NOT need to be open in the bert table.**

#### Execution trace

**Step 1 — Allocate the new ISA** [do1.c:277-279]:
```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
    return (FALSE);
}
```
This creates a new orgl entry in the granfilade tree for the new version.

**Step 2 — Retrieve the base document's vspan** [do1.c:281-283]:
```c
if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan)) {
    return FALSE;
}
```
If this fails, the function returns FALSE immediately. The critical path is through `doretrievedocvspanfoo` [do1.c:301-309]:
```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), retrievedocumentpartofvspanpm();
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

**Step 3 — `findorgl` with `NOBERTREQUIRED`** [granf1.c:17-41]:
```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        // ...return FALSE (only if !isxumain)
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

`NOBERTREQUIRED` causes `checkforopen` [bert.c:59-61] to return `1` unconditionally, bypassing all bert open-table logic:
```c
if (type == NOBERTREQUIRED) {
    return 1;  /* Random > 0 */
}
```

So the bert table is **never consulted** for the base document. The function proceeds to `fetchorglgr`.

**Step 4 — `fetchorglgr` checks the granfilade tree** [granf2.c:22-81]:
```c
typeorgl fetchorglgr(typetask *taskptr, typegranf fullcrumptr, typeisa *address)
{
    if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
        return (NULL);
    if ((context = retrievecrums ((typecuc*)fullcrumptr, address,  WIDTH)) == NULL)
        return NULL;
    if (!tumblereq((tumbler*)&context->totaloffset, address)) {
        crumcontextfree(context);   
        return (NULL);  
    }
    // ...loads the orgl and returns it
}
```

Three failure conditions, any of which returns `NULL` if the base ISA doesn't exist:
1. The address is beyond the granfilade's total width
2. `retrievecrums` finds no node at that position
3. The retrieved node's `totaloffset` doesn't exactly match the requested ISA

If `fetchorglgr` returns `NULL`, `findorgl` returns `FALSE`, `doretrievedocvspanfoo` returns `FALSE`, and `docreatenewversion` returns `FALSE` at [do1.c:282].

#### The orphan problem

There is a structural hazard here. When the base ISA doesn't exist:
1. `createorglingranf` [do1.c:277] **has already succeeded** — a new orgl entry was written into the granfilade for `newisaptr`
2. `doretrievedocvspanfoo` [do1.c:281] then fails
3. The function returns `FALSE` — but `addtoopen`, `logbertmodified`, and `doclose` [do1.c:292-296] are **never reached**

Since `addtoopen` was never called for `newisaptr`, there is no bert entry for the new version, and `removefromopen` → `deleteversion` is never triggered. The orphaned orgl sits in granfilade storage with no content and no cleanup path.

---

### Question 2: Does the Implementation Enforce Sequential Version Numbers?

**No explicit enforcement exists. Sequential addresses are a consequence of the allocation algorithm, not a validated invariant.**

#### How the new ISA is chosen

Both hint paths lead to `findisatoinsertgr` [granf2.c:130-156] → `findisatoinsertnonmolecule` [granf2.c:203-242], since the hint subtype is `DOCUMENT` (not `ATOM`).

**Which hint is used** is determined by the ownership check at [do1.c:270-276]:
```c
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
} else {
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

`isthisusersdocument` [socketbe.c:197-201] checks:
```c
int isthisusersdocument(tumbler *tp) {
    return tumbleraccounteq(tp, &(player[user].account));
}
```

**Case A — Own document** (`DOCUMENT, DOCUMENT` hint, `hintisa = base ISA`):
- `depth = 1` because `supertype == subtype` [granf2.c:209]
- `upperbound = tumblerincrement(hintisa, 0, 1)` — increments the last digit of `hintisa` [granf2.c:213]
- `findpreviousisagr` finds the highest existing ISA strictly below `upperbound`
- On first version: finds the base doc itself (e.g., `1.1.0.1`); new version = `1.1.0.1.1` (a sub-address)
- On second version: finds `1.1.0.1.1`; new version = `1.1.0.1.2`
- On Nth version: new version = `1.1.0.1.N`

**Case B — Someone else's document** (`ACCOUNT, DOCUMENT` hint, `hintisa = current user's account`):
- `depth = 2` because `ACCOUNT != DOCUMENT` [granf2.c:209]
- Behaves identically to `docreatenewdocument` [do1.c:239]: allocates a fresh document under the current user's account, unrelated to the base document's ISA sequence

#### The allocation mechanism

`findisatoinsertnonmolecule` [granf2.c:235-241] does:
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  /* first child */
} else {
    tumblertruncate (&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

This always finds the current maximum and increments by 1. There is:
- **No counter variable** tracking version numbers
- **No assertion** that `newisaptr` must equal any specific value relative to `isaptr`
- **No check** that the caller requested a valid "next" version

The sequential property holds only because `findpreviousisagr` always returns the highest existing sibling, so each new allocation lands one position higher. If the tree were modified externally to create gaps or remove entries, the next allocation would simply append after whatever is currently the maximum — not necessarily what would be expected as "the next version."

---

### Summary Table

| Property | Enforced? | Mechanism | Notes |
|---|---|---|---|
| Base ISA must exist in storage | **Yes** | `fetchorglgr` returns `NULL` if ISA not found in granfilade [granf2.c:31-40] | Enforced by `doretrievedocvspanfoo` at [do1.c:281] |
| Base ISA must be open (bert) | **No** | `NOBERTREQUIRED` bypasses `checkforopen` [bert.c:59-61] | Only existence in granfilade is required |
| Version numbers are sequential | **De facto** | `findpreviousisagr` + `tumblerincrement` always yields `max + 1` | No invariant enforced; no counter maintained |
| Own-doc versions are siblings | **No** | With `DOCUMENT,DOCUMENT` hint, `depth=1`, new ISA is a **child** of base (e.g., `1.1.0.1.1`) | Not a sibling at the same level |
| Orphan prevention on partial failure | **No** | If `createorglingranf` succeeds but `doretrievedocvspanfoo` fails, the new orgl is never closed or deleted | Structural leak; no cleanup path |
