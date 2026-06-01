## Question 2 [evidence]

> When CREATENEWVERSION/docreatenewversion is invoked on a document that already has a version, does it produce the next version as a sibling-increment on the existing version chain, and is the operation uniform across first and subsequent versions?

## KB Synthesis

Yes, with precision on what "sibling increment on the version chain" means.

**Every call to CREATENEWVERSION allocates a new child of the document you pass as the argument**, using the same stateless query-and-increment mechanism regardless of whether prior versions exist.

From [SS-ADDRESS-ALLOC] Finding 0068, the algorithm for owned documents:

1. Compute upper bound: `tumblerincrement(source_doc, depth=0, 1)` — the next sibling of the source (e.g., `1.1.0.1.0.2` for source `1.1.0.1.0.1`)
2. `findpreviousisagr` finds the highest existing address below that bound
3. Containment check verifies the found address is actually under the source document
4. No children exist → allocate `source_doc.1`; children exist → truncate-and-increment to next sibling

So calling CREATENEWVERSION twice on the **same original**:
```
1.1.0.1.0.1.1   (first call: no prior children → allocates .1)
1.1.0.1.0.1.2   (second call: finds .1 → increments to .2)
```

These are **siblings** under the original. Calling CREATENEWVERSION on the **version** instead produces a grandchild: `1.1.0.1.0.1.1.1` [SS-VERSION-ADDRESS, Finding 0032].

The operation is structurally uniform — no special-casing for first vs. subsequent versions. The `findisatoinsertnonmolecule` code path is identical; the allocation result differs only because `findpreviousisagr` finds a pre-existing child in the subsequent case [ST-VERSION, [SS-ADDRESS-SPACE] Finding 0077].

---

## Code Exploration

I now have complete, verified source citations. Here is the full answer.

---

## `CREATENEWVERSION` / `docreatenewversion`: Version Addressing Analysis

### 1. FEBE Entry Point — `fns.c:289–300`

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  bool getcreatenewversion(), docreatenewversion();

    if (
       getcreatenewversion (taskptr, &originaldocisa)
    && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion (taskptr, &newdocisa);
      else
        putrequestfailed (taskptr);
}
```

The handler reads **one ISA** from the wire and passes it as **both** `isaptr` and `wheretoputit` to `docreatenewversion`. The third parameter `wheretoputit` is the same value as the source document — it is only distinct when called via some other code path (not exposed by the current FEBE surface).

---

### 2. `docreatenewversion` — `do1.c:260–299`

**Signature:**
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
```

The function does four things in sequence:

1. **Builds an allocation hint** (controls where in the granfilade the new ISA falls) [`do1.c:268–276`]
2. **Allocates the new ORGL** at the computed ISA via `createorglingranf()` [`do1.c:277`]
3. **Retrieves the source document's vspan** via `doretrievedocvspanfoo()` [`do1.c:281`]
4. **Copies content** to the new version and closes it [`do1.c:292–296`]

---

### 3. The Ownership Branch — `do1.c:268–276`

```c
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Two cases:

| Condition | Hint type | `supertype` | `subtype` |
|-----------|-----------|-------------|-----------|
| Same account, own document | `DOCUMENT, DOCUMENT` | DOCUMENT | DOCUMENT |
| Cross-account or other's doc | `ACCOUNT, DOCUMENT` | ACCOUNT | DOCUMENT |

The hint type controls `depth` in the address allocation below.

---

### 4. New Version ISA Computation — `granf2.c:203–242`

The call chain is: `createorglingranf → createorglgr` [`granf2.c:111`] `→ findisatoinsertgr` [`granf2.c:130`] `→ findisatoinsertnonmolecule` [`granf2.c:203`].

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound, truncated;
  INT depth, hintlength;
  bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;   // (*)
    hintlength = tumblerlength (&hintptr->hintisa);
    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        // Nothing under this hint — first allocation
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);      // (**)
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr,tumblerlength(isaptr)==hintlength?depth:0,1,isaptr); // (***)
    }
}
```

`(**)` `tumblerincrement(aptr, rightshift, bint, cptr)` [`tumble.c:599`] adds `bint` to the mantissa slot at `lastNonZeroIdx + rightshift`. For `rightshift=depth=1`, this appends a new trailing component, creating a child address.

#### For the own-document path (`DOCUMENT, DOCUMENT`, depth=1):

Let the document address be `D` with `hintlength = n`.

- **`upperbound`** = `tumblerincrement(D, 0, 1)` = `D` with last component incremented = the next sibling document's address.
- **`findpreviousisagr(upperbound)`** finds the highest ISA in the granfilade strictly below `upperbound`. On first versioning this returns `D` itself (the document entry). On subsequent versioning it returns the most recent version `D.K`.
- **First version** (lowerbound is `D`, `tumblertruncate(D, n) == D`, so `lowerbound_under_hint = TRUE`, goes to `else`): `tumblertruncate(D, n+1) = D` (already shorter than n+1), then `tumblerlength(D)==n` so `tumblerincrement(D, 1, 1)` → `D.1`.
- **Subsequent versions** (lowerbound is `D.K`): `tumblertruncate(D.K, n+1) = D.K`, then `tumblerlength(D.K)=n+1 ≠ n`, so `tumblerincrement(D.K, 0, 1)` → `D.K+1`.

**Version sequence:** `D.1`, `D.2`, `D.3`, …

Each new version is a **sibling-increment** of the previous version: same depth, last component incremented by 1. The versions are children of the document address, not siblings of it.

#### For the cross-account path (`ACCOUNT, DOCUMENT`, depth=2):

This is identical to `docreatenewdocument` [`do1.c:234–241`], which uses the same hint type. The new ISA is allocated as a fresh document-level address under the account (`account.0.1`, `account.0.2`, …). This is **not** a version child of the original document — it creates an independent document address whose content happens to be a copy.

---

### 5. Uniformity Across First and Subsequent Versions

There is **no special case** in `docreatenewversion` for "first version." The function unconditionally calls `createorglingranf → findisatoinsertnonmolecule`. The branching inside that function (zero lowerbound vs. existing lowerbound) handles both first and subsequent allocations with the **same arithmetic** — both produce the next available child address under `D`. The behavior is entirely uniform from the caller's perspective.

No persistent counter or "latest version" pointer exists. The allocation is determined each time by scanning the granfilade with `findpreviousisagr` to find the current maximum, then incrementing.

---

### 6. What Gets Written

| Step | Code | Effect |
|------|------|--------|
| New ORGL in granfilade | `do1.c:277` `createorglingranf(...)` | Inserts new ORGL node at the computed ISA |
| Open in BERT table | `do1.c:292` `addtoopen(newisaptr, user, TRUE, WRITEBERT)` | Registers as owned, created, writable |
| Content copy | `do1.c:293` `docopyinternal(...)` | Copies source vspan into new version |
| Modified flag | `do1.c:295` `logbertmodified(newisaptr, user)` | Prevents deletion on close |
| Close | `do1.c:296` `doclose(...)` | Removes from open set; retains because modified |

---

### Summary

**Yes**, invoking `CREATENEWVERSION` on a document that already has versions produces the next version as a sibling-increment on the existing version chain: version `N+1` is created at address `D.N+1` by finding `D.N` via `findpreviousisagr` and incrementing its last component [`granf2.c:239–240`]. Version addresses are children of the document address (one level deeper in the tumbler hierarchy), not siblings of the document itself.

**Yes**, the operation is uniform across first and subsequent invocations. `findisatoinsertnonmolecule` handles both cases without caller awareness: first-version allocations fall into the `iszerotumbler || !lowerbound_under_hint` branch and produce `D.1`; subsequent allocations fall into the `else` branch and produce `D.K+1`. The arithmetic is the same `tumblerincrement` call with `rightshift=0` on an already-sized address.

The one non-uniform behavior is the **ownership branch** at `do1.c:270–276`: versioning another user's document uses `ACCOUNT, DOCUMENT` hint (depth=2), making the "version" an independent document-level address rather than a child of the original — effectively a copy, not a version in the same address subtree.
