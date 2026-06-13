## Question 13 [evidence]

> Can `findisatoinsertnonmolecule` allocate a successor link as a child of the original link's ISA (e.g., `docISA.0.2.N.0.1`), analogous to how version addresses nest under a source document, or does the bounded upper limit (`docISA.2.3`) and the per-document link counter force all successors to be flat siblings at `2.N+1`?

## KB Synthesis

`findisatoinsertnonmolecule` is not the function used for link allocation, and the flat sibling pattern is enforced by a different mechanism than the bounded upper limit. Here is the full picture.

## Link allocation uses `findisatoinsertmolecule`, not `findisatoinsertnonmolecule`

[SS-ADDRESS-ALLOC] Finding 0065 is explicit: MAKELINK dispatches through `findisatoinsertmolecule` (the molecule/atom path), not `findisatoinsertnonmolecule` (the document/version path). The distinction is made in `findisatoinsertgr` at `backend/granf2.c:130-156`, which dispatches to the molecule branch for link orgls.

`findisatoinsertnonmolecule` handles document and version addresses. If it were called with a link ISA as the parent hint and `depth=1`, it would produce a child at `docISA.0.2.N.1`, `docISA.0.2.N.2`, etc. — analogous to how `VERSION(doc)` produces `doc.1`, `doc.2`. But this path is never taken for links.

## What forces flat siblings: the `0.1` increment, not the upper bound

The molecule allocation algorithm ([SS-ADDRESS-ALLOC] Finding 0065):

1. Set `upperbound = docISA.0.2.3` — the next element-field boundary (text atoms occupy element_field=3)
2. Call `findpreviousisagr` to find the highest existing address below that bound
3. **If no links exist:** allocate at the hardcoded first position `docISA.0.2.1`
4. **Otherwise:** call `tumblerincrement(&lowerbound, 0, 1, isaptr)` — increment the rightmost significant digit by 1

Step 4 is the structural constraint. `rightshift=0` always extends the last digit: `docISA.0.2.1 → docISA.0.2.2 → docISA.0.2.3...` These are flat siblings at the `...0.2.N` level. Producing a nested child like `docISA.0.2.N.0.1` would require adding a new `.0.` field separator, which `tumblerincrement` at `rightshift=0` cannot do — it only increments existing digit positions.

## The upper bound does not prevent children numerically

From [INV-TUMBLER-TOTAL-ORDER] and the tumbler ordering rules: `docISA.0.2.1.0.1` is numerically less than `docISA.0.2.2`, which is less than `docISA.0.2.3` (the upper bound). So a nested child address would not be excluded by the bound. The bound only prevents escaping into the text atom territory at element_field ≥ 3.

However, because no link is ever allocated at `docISA.0.2.N.0.1`, `findpreviousisagr` never finds such an address, and the increment-by-`0.1` from `docISA.0.2.N` always produces `docISA.0.2.N+1`.

## Version-style nesting would require `findisatoinsertnonmolecule`

[SS-ADDRESS-ALLOC] Finding 0068 documents how version allocation uses `findisatoinsertnonmolecule` with `depth=1` (DOCUMENT→DOCUMENT) to produce child addresses under the source document. If MAKELINK used this path instead — with a prior link's ISA as the parent hint — it would produce `docISA.0.2.1.1`, `docISA.0.2.1.2`, etc. But this path is never taken. The allocation type (DOCUMENT, ATOM, LINKATOM) recorded in the hint is what drives the dispatch, and LINKATOM always routes to the molecule path.

## Summary

All successor links are forced to flat siblings at `docISA.0.2.N+1` by the `tumblerincrement(&lowerbound, 0, 1, isaptr)` call in `findisatoinsertmolecule`, not by the upper bound `docISA.0.2.3`. The upper bound prevents leaking into text-atom territory but permits arbitrary depth numerically. The hierarchical nesting mechanism that version allocation uses (`findisatoinsertnonmolecule` with depth=1) is architecturally separate and is never invoked for link creation.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## Answer

### The Premise Needs Correction: Links Never Reach `findisatoinsertnonmolecule`

The routing gate at `findisatoinsertgr` [granf2.c:130-156] completely separates the two allocation paths by `hintptr->subtype`:

```c
if (hintptr->subtype == ATOM) {
    ...
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);   // ← links go HERE
} else {
    findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr); // ← documents, accounts, nodes
}
```

`ATOM = 4` [xanadu.h:143], `LINKATOM = 2` [xanadu.h:146]. Every `docreatelink` call sets `subtype = ATOM` via:

```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do1.c:207
```

So **`findisatoinsertnonmolecule` never sees a link**. The question is actually about `findisatoinsertmolecule`.

---

### What `findisatoinsertmolecule` Does for Links

```c
// granf2.c:158-181
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // docISA+(2,3)
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        // lowerbound is the document itself — no links yet
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);  // docISA+(2,2)
        tumblerincrement(isaptr, 1, 1, isaptr);                       // docISA+(2,2)+(1,1)
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);           // base = docISA+(2,2)
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);                   // base+(1,1)
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);              // flat: lowerbound+(0,1)
    }
}
```

Breaking this down for LINKATOM (`atomtype=2`) with `docISA` whose last nonzero mantissa index is `k`:

| Situation | Computation | Semantic |
|---|---|---|
| No links exist | `tumblerincrement(docISA, 2, 2)` → `tumblerincrement(_, 1, 1)` | `docISA.0.0.2.0.1` style: two levels deep |
| `lowerbound < docISA+(2,2)` | `tumblerincrement(docISA+(2,2), 1, 1)` | same depth, one more right |
| `lowerbound >= docISA+(2,2)` | `tumblerincrement(lowerbound, 0, 1)` | **flat sibling**: add 1 to last nonzero of existing address |

The search ceiling — `tumblerincrement(docISA, 2, atomtype+1)` = `docISA+(2,3)` [granf2.c:162] — is passed to `findpreviousisagr`. This bounds the scan strictly **within** the per-document link range. No link can ever be allocated at or past this bound, and `findpreviousisagr` never returns an address outside it.

**The successor increment is always `tumblerincrement(lowerbound, 0, 1)`** [granf2.c:175]: rightshift=0, so it adds 1 to the last nonzero digit of the previous link address. This is definitionally a **flat sibling** — it stays at the same mantissa depth, just with a higher trailing digit. It is never `tumblerincrement(lowerbound, N>0, 1)`, which would extend to a child.

---

### What `findisatoinsertnonmolecule` Does (for Documents/Versions)

This is where the nested-child behavior actually lives [granf2.c:203-242]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;  // DOCUMENT,DOCUMENT → 1
hintlength = tumblerlength(&hintptr->hintisa);
tumblerincrement(&hintptr->hintisa, depth - 1, 1, &upperbound);  // sibling ceiling
findpreviousisagr(fullcrumptr, &upperbound, &lowerbound);
...
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // ← FIRST CHILD
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
}
```

For `docreatenewversion` with `makehint(DOCUMENT, DOCUMENT, 0, docISA, &hint)` [do1.c:271]:

- `depth=1`, ceiling = `tumblerincrement(docISA, 0, 1)` = docISA's last digit +1 (its sibling, not its child range)
- **First new version**: `tumblerincrement(docISA, 1, 1)` [granf2.c:237] — rightshift=1, meaning one position *past* the last nonzero: genuinely a **child** address
- **Subsequent versions**: `tumblertruncate(lowerbound, hintlength+1)` then the conditional increment. When `tumblerlength(truncated) == hintlength`, it applies `tumblerincrement(_, depth=1, 1)` again — another child. When the truncation already has child digits, it applies `tumblerincrement(_, 0, 1)` — a flat sibling of the existing child

This produces the document-version nesting the question describes: version 1 is `docISA.0.1`, version 2 is `docISA.0.2`, etc. — all children of `docISA`, not of each other.

---

### Direct Answer to the Question

**No, `findisatoinsertnonmolecule` does not allocate successor links at all**, and therefore cannot nest them as children like `docISA.0.2.N.0.1`. The routing at `findisatoinsertgr` [granf2.c:135] ensures every link — first or Nth — goes to `findisatoinsertmolecule`.

In `findisatoinsertmolecule`, two structural constraints together guarantee **all successor links are flat siblings**:

1. **The bounded upper limit** `tumblerincrement(docISA, 2, 3)` [granf2.c:162] passed to `findpreviousisagr` confines the search to the per-document link space and prevents successor allocation from escaping above the ceiling.

2. **The successor increment** `tumblerincrement(lowerbound, 0, 1)` [granf2.c:175] — rightshift=0 — adds 1 to the *last nonzero digit of the previous link's address*, producing a sibling at the same depth, never a child.

The nested-child pattern (analogous to `docISA.0.2.N.0.1`) **does not occur for links**. It is the exclusive behavior of `findisatoinsertnonmolecule` when creating new document versions, where the `tumblerincrement(hintisa, depth, 1)` call with `depth >= 1` extends into child address space. That path is structurally unreachable from any link creation call site (`docreatelink` / `domakelink`), both of which hard-code `subtype=ATOM`.
