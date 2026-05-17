## Question 1 [evidence]

> Does udanax-green's link-emission path (`docreatelink` / the `LINKATOM` branch of `findisatoinsertmolecule`) ever deposit a link at an address that is a tumbler-prefix-descendant of an existing link, or is it structurally constrained to sibling-frontier positions only?

## KB Synthesis

## Link Address Allocation: Sibling-Frontier Only

The link-emission path is structurally constrained to sibling-frontier positions. It cannot produce a tumbler-prefix-descendant of an existing link. Here is the reasoning from the KB.

### The allocation algorithm

[SS-ADDRESS-ALLOC / Finding 0065] gives the LINKATOM branch of `findisatoinsertmolecule`:

1. `upperbound = tumblerincrement(docISA, 2, LINKATOM+1)` — bounds the search to the document's link element-type range (e.g., `docISA.0.2.*` but not `docISA.0.3.*`)
2. `findpreviousisagr` returns the highest existing link address below that bound
3. If none found: allocate at `docISA.0.2.1` (the first child of element-field 2)
4. Otherwise: `tumblerincrement(lowerbound, rightshift=0, inc=1)` — increment at the last significant digit

### Why rightshift=0 enforces sibling-only allocation

From [SS-TUMBLER / Finding 0031], `tumblerincrement` with `rightshift=0` adds `inc` to the last significant mantissa digit. Applied to `docISA.0.2.1`:

```
tumblerincrement(docISA.0.2.1, 0, 1)  →  docISA.0.2.2
```

This is always a **sibling** — same digit depth, last digit incremented. The operation never appends new digits, so it cannot produce a descendant like `docISA.0.2.1.1`.

A descendant would require a separate `makehint(ATOM, ATOM, ...)` depth parameter that descends further into the tree. The link path uses `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [Finding 0065, `do1.c:211`], which scopes allocation to the document's atom-level namespace, not below any individual link.

### The upperbound does not exclude descendants

One subtlety: `docISA.0.2.1.1` *is* less than `docISA.0.2.2` in tumbler order [INV-TUMBLER-TOTAL-ORDER], so it falls within the upperbound `docISA.0.2.3`. If such a descendant address already existed in the granfilade, `findpreviousisagr` could return it, and the next allocation would be `docISA.0.2.1.2` — a sibling of the descendant, not of the original link. But this is a hypothetical: the allocation algorithm itself never produces a descendant in the first place, so the granfilade never contains one under a prior link's address.

### Monotonic confirmation

[INV-MONOTONIC / Finding 0065] confirms the sequence is flat and monotone within each document:

> Link I-address allocation within a document is strictly monotonically increasing. Each MAKELINK on document D produces an I-address greater than all previous link I-addresses in D.

The concrete example: `docA.0.2.1`, `docA.0.2.2`, `docA.0.2.3`, … — siblings at fixed depth, never branching deeper.

### Conclusion

The path `docreatelink` → `findisatoinsertmolecule` (LINKATOM branch) always emits links at sibling-frontier positions `docISA.0.2.N` for monotonically increasing N. The `rightshift=0` increment is the structural enforcer: it extends the flat sequence rather than descending under any existing link.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is.

---

## Does the link-emission path deposit links as prefix-descendants of existing links?

**Short answer**: No — the LINKATOM branch of `findisatoinsertmolecule` is structurally constrained to produce sibling-frontier addresses. No explicit collision check is performed; the guarantee comes from the tumbler arithmetic itself. However, the invariant is not *asserted* — it is silently assumed, and a single sub-entry under an existing link ISA in the granfilade would break it.

---

### The Emission Chain

```
fns.c:createlink
  → do1.c:docreatelink             [line 207: makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)]
    → granf1.c:createorglingranf   [line 51: wrapper]
      → granf2.c:createorglgr      [line 117: calls findisatoinsertgr]
        → granf2.c:findisatoinsertgr  [line 135: routes to findisatoinsertmolecule]
          → granf2.c:findisatoinsertmolecule  [line 158: computes the address]
```

**`do1.c:207`** — the hint is built with `supertype=DOCUMENT, subtype=ATOM, atomtype=LINKATOM=2, hintisa=docisaptr`:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

**`xanadu.h:145–146`** — the constants:

```c
#define TEXTATOM  1
#define LINKATOM  2
```

**`granf2.c:134–156`** — `findisatoinsertgr` dispatches on `subtype == ATOM` to `findisatoinsertmolecule`:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { return (FALSE); }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
return (TRUE);
```

---

### The LINKATOM Address Computation (granf2.c:158–181)

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // D.0.3
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);        // Line 171: isaptr = D.0.2
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);               // Line 173: Case A
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);         // Line 175: Case B
    }
}
```

The `upperbound` is `D.0.(LINKATOM+1)` = `D.0.3`. `findpreviousisagr` returns the largest granfilade ISA strictly less than `D.0.3`. That's the frontier of everything deposited so far under this document.

---

### What `tumblerincrement` does (tumble.c:599–623)

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    ...
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

`idx` is the index of the **last non-zero mantissa position**. `rightshift` controls how many positions to the right of that last digit the increment lands:

| `rightshift` | Effect |
|---|---|
| 0 | Increment the last existing component — creates a **sibling** |
| 1 | Add one component beyond the last — creates a **child** |
| 2 | Add two components beyond the last — creates a **grandchild** |

For document D with mantissa `[1,0,3,0,0,0,...]` (idx=2):
- `tumblerincrement(D, 2, LINKATOM=2)` → mantissa[2+2]=mantissa[4]+=2 → `D.0.2` (the **link subspace base**)

---

### Case Analysis

Let D be the document ISA (e.g., `1.0.3`), depth 3.

**Case A** — `lowerbound < D.0.2` (granf2.c:173):

Fires when no links exist yet; `lowerbound` is either zero (empty document) or a text atom at `D.0.1.N`.

```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);   // isaptr = D.0.2
tumblerincrement (isaptr, 1, 1, isaptr);               // isaptr = D.0.2.1
```

The first `tumblerincrement(D, 2, 2)` sets `isaptr` to `D.0.2`. The second `tumblerincrement(D.0.2, 1, 1)` finds idx=4 (last non-zero in `D.0.2`), adds 1 at `mantissa[4+1]=mantissa[5]`, giving `D.0.2.1`.

Result: **`D.0.2.1`** — the first link, no existing link to collide with.

**Case B** — `lowerbound >= D.0.2` (granf2.c:175):

Fires when at least one link exists; `lowerbound` is the most recently inserted link address.

```c
tumblerincrement (&lowerbound , 0, 1, isaptr);
```

`rightshift=0` increments the last mantissa digit of `lowerbound`. If `lowerbound = D.0.2.K` (last non-zero at mantissa[5] = K), the result is `D.0.2.(K+1)`.

`D.0.2.(K+1)` and `D.0.2.K` differ only at their final component — they are **siblings**. `D.0.2.K` is NOT a prefix of `D.0.2.(K+1)`.

---

### Why No Prefix-Descendant Relationship Can Arise (Under Current Code)

The invariant rests on one fact: **all granfilade entries for a document's links are at the same tumbler depth** — specifically depth `len(D)+3`, i.e., `D.0.2.N` for successive N.

This holds because `docreatelink` (do1.c:195–221) stores link endpoint data in the link's **`orgl` enfilade** (via `insertendsetsinorgl` at line 218), not as granfilade sub-entries. `insertendsetsinspanf` (line 219) writes to the spanfilade. Neither creates granfilade nodes below the link's own ISA.

Therefore `findpreviousisagr`, bounded by `D.0.3`, always returns `lowerbound = D.0.2.K` (flat, same depth) — never `D.0.2.K.0.M`. Case B's `tumblerincrement(lowerbound, 0, 1)` stays at the same depth.

---

### The One Structural Vulnerability

There is **no defensive check** in `findisatoinsertmolecule` that verifies the computed `isaptr` is not a prefix-descendant of any existing granfilade entry. The function trusts the invariant blindly.

If any operation ever deposited a granfilade entry at `D.0.2.K.0.1` (one level below an existing link ISA), `findpreviousisagr` with `upperbound=D.0.3` would return that entry as `lowerbound`. Case B would then compute:

```
tumblerincrement(D.0.2.K.0.1, 0, 1) = D.0.2.K.0.2
```

`D.0.2.K.0.2` IS a tumbler-prefix-descendant of the existing link `D.0.2.K`, because `D.0.2.K` is a proper prefix of `D.0.2.K.0.2` (truncating `D.0.2.K.0.2` to depth `len(D)+3` yields `D.0.2.K`).

**No existing code path in `docreatelink` or its callees triggers this.** The invariant is maintained purely by the discipline of storing link internals in the orgl, not by any assertion or guard in the address-allocation logic itself.

---

### Summary

| | |
|---|---|
| **Can LINKATOM branch produce a prefix-descendant of an existing link?** | No, under all reachable code paths. |
| **Is this enforced by an explicit check?** | No. `findisatoinsertmolecule` performs no such check. |
| **What maintains the invariant?** | All link data goes into the `orgl` (POOM), not as granfilade sub-addresses. `findpreviousisagr` therefore always finds `lowerbound` at flat sibling depth. |
| **What would break it?** | Any operation that wrote a granfilade entry at depth `D.0.2.K.*` — one level below a link ISA. |
| **Relevant lines** | `granf2.c:158–181` (address logic), `tumble.c:599–623` (`tumblerincrement`), `do1.c:207–221` (call site), `xanadu.h:145–146` (constants) |
