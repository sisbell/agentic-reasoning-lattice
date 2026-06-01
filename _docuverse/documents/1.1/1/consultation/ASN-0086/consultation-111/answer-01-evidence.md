## Question 1 [evidence]

> Does udanax-green's link allocator guarantee a fresh key when it increments the maximum same-home address, relying only on that address being T4-valid, or does its freshness depend on the realized chain being contiguous/conforming?

## KB Synthesis

The allocator's freshness guarantee relies solely on finding the maximum address within the bounded range and incrementing it — it does **not** depend on the realized chain being contiguous.

## Mechanism

From [SS-ADDRESS-ALLOC] (Finding 0065), `findisatoinsertmolecule` works in three steps:

1. Compute `upperbound = docISA.2.3` — bounding to the document's link element subspace
2. Call `findpreviousisagr` — a granfilade tree traversal that returns the **highest existing address below the bound**, regardless of any gaps in the sequence
3. Increment the result by `0.1` (rightshift=0): `tumblerincrement(&lowerbound, 0, 1, isaptr)`

The freshness invariant is: `new_addr = max_existing + 1 > max_existing ≥ all_existing`, which holds whether the existing chain is `{2.2.1}`, `{2.2.1, 2.2.2, 2.2.3}`, or hypothetically gappy. The allocator doesn't assume contiguity; it queries the tree each time.

## Why T4-validity is the load-bearing property

The bounds `docISA.2.2` (lower, first-link sentinel) and `docISA.2.3` (upper, exclusive) are T4-valid tumbler boundaries. The `.0.` field separator convention ensures that `docISA.2.2.1` is within element-subspace 2 of the document, and incrementing digit-0 from there stays within that subspace. The allocator trusts that these bounds carve out a valid, document-scoped address range — not that everything between them is occupied.

## The granfilade monotonicity does the real work

[INV-MONOTONIC] (Finding 0061) and [INV-NO-IADDR-REUSE] are the actual freshness guarantors: the granfilade is append-only, so `findpreviousisagr` always returns the true maximum, and no previously-allocated address is ever recycled. Even if link orgls were deleted from the POOM, their I-addresses persist in the granfilade tree and continue to be found by `findpreviousisagr`, preventing reuse. The conformance of the chain is irrelevant to this guarantee.

**Bottom line**: Freshness depends on T4-valid bound construction (`docISA.2.2`/`docISA.2.3`) plus granfilade monotonicity — the chain being contiguous is neither assumed nor required.

---

## Code Exploration

I now have all the code citations needed. Here is the full answer:

---

## Link Allocator Freshness: Source Analysis

### The Allocation Call Chain

`docreatelink` [`do1.c:195`] is the entry point. It constructs a hint with:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);   // do1.c:207
```

`LINKATOM == 2` [`xanadu.h:146`]. Then the first thing in the return chain is:

```c
createorglingranf (taskptr, granf, &hint, linkisaptr)    // do1.c:209
```

This calls into `findisatoinsertgr` [`granf2.c:130`], which dispatches to `findisatoinsertmolecule` [`granf2.c:158`] because `hintptr->subtype == ATOM`.

---

### The Molecule Allocator — `findisatoinsertmolecule` [`granf2.c:158–181`]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound); // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);     // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);             // line 166
        tumblerincrement (isaptr, 1, 1, isaptr);                                 // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);                        // line 169
    } else if (hintptr->atomtype == LINKATOM) {                                  // line 170
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                      // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                             // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                       // line 175
    }
}
```

**Step by step for LINKATOM:**

1. **`upperbound`** = `docisa.2.(LINKATOM+1)` = `docisa.2.3` — the exclusive ceiling of the link subspace.
2. **`findpreviousisagr`** [`granf2.c:255`] traverses the enfilade tree to find the highest ISA already stored that is less than `upperbound`. This is a live tree query, not a cached value.
3. **LINKATOM branch** [`granf2.c:170`]:
   - Compute a floor: `isaptr = hintisa.2.2` — the minimum valid link address.
   - If `lowerbound < floor` (no link exists yet, or all existing entries are below the floor): allocate `floor + 0.1`, i.e., `docisa.2.2.1` [`granf2.c:173`].
   - Otherwise (a previous link exists at or above the floor): allocate `lowerbound + 0.1` [`granf2.c:175`] — strictly one step past the current maximum.

---

### `findpreviousisagr` — The Max-Finding Engine [`granf2.c:255–278`]

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);          // line 264
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if (
         (tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
        || tmp == ONMYRIGHTBORDER
        || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);         // line 272 (recursive)
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // line 275
        }
    }
}
```

This recursively descends into the enfilade to find the rightmost (maximum) leaf ISA below `upperbound`. It is a direct tree traversal — there is no caching, no hint, no assumption about the chain's structure.

---

### `tumblerincrement` — The Increment Primitive [`tumble.c:599–623`]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    if (iszerotumbler (aptr)) { ... }          // zero special case
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);                     // line 622
}
```

`tumblerjustify` [`tumble.c:289–313`] only normalizes leading zeros — it left-shifts the mantissa until `mantissa[0] != 0` and adjusts `exp`. It performs **no T4-validity check**; the commented-out `tumblercheck` call at `tumble.c:311–312` was never enabled:

```c
/*  if (!tumblercheck (tumblerptr))
        qerror ();
*/
```

---

### Answer to the Question

**The link allocator does not rely on T4-validity, and it does not require or assume a contiguous/conforming chain.**

The freshness guarantee is purely **structural monotonicity via live tree query**:

1. `findpreviousisagr` [`granf2.c:255`] finds the true maximum existing ISA in the granfilade below the link subspace ceiling (`docisa.2.3`). This is authoritative — it reads actual tree state, not a cached counter.
2. `tumblerincrement(&lowerbound, 0, 1, isaptr)` [`granf2.c:175`] produces a value strictly greater than that maximum.
3. The result is fresh because enfilade nodes are never physically removed (deletions are logical), so the maximum is stable and monotonically non-decreasing.

**T4-validity of the result is incidental**, not a precondition. The allocated ISA is T4-valid because it is computed by incrementing an already-valid tumbler (an existing tree entry), and `tumblerjustify` keeps the mantissa normalized — but neither `findisatoinsertmolecule` nor `tumblerincrement` checks validity as a freshness criterion.

**Chain contiguity is irrelevant.** Gaps in the sequence (e.g., `docisa.2.2.1`, `docisa.2.2.3` with `docisa.2.2.2` never allocated or logically deleted) do not affect correctness: `findpreviousisagr` will report `docisa.2.2.3` as the maximum, and the next allocation will be `docisa.2.2.4`. The allocator is agnostic to whether the sequence is dense or sparse.

**In one sentence:** Freshness is guaranteed by `findpreviousisagr` reading the actual maximum from the enfilade tree and `tumblerincrement` adding one — a structural, not semantic, guarantee, with no T4 check and no conformity requirement anywhere in the path.
