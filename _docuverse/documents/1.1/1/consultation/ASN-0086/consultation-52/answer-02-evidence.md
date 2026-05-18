## Question 2 [evidence]

> Does `findisatoinsertmolecule` (or any udanax-green link allocation path) ever produce link addresses with element-field length > 2, and if so under what conditions?

## KB Synthesis

Based on the KB, `findisatoinsertmolecule` produces link addresses with element-field depth of exactly 2, not more. Here is the full analysis.

## Link Address Structure

From [SS-ADDRESS-SPACE] Finding 0065, `MAKELINK` allocates within a document-scoped region:

```
upperbound = tumblerincrement(docISA, rightshift=2, bint=LINKATOM+1=3)
           = docISA.0.3
```

The first link is placed at `docISA.0.2.1` (when `lowerbound < docISA.0.2`); subsequent links use `tumblerincrement(lowerbound, rightshift=0, bint=1)` — incrementing the last significant mantissa digit by 1. For document `1.1.0.1.0.1`:

| Allocation | Address | Element-field slots |
|------------|---------|-------------------|
| Link 1 | `1.1.0.1.0.1.0.2.1` | type=2, N=1 |
| Link 2 | `1.1.0.1.0.1.0.2.2` | type=2, N=2 |
| Link N | `1.1.0.1.0.1.0.2.N` | type=2, N=N |

The element-field portion (past the `.0.` separator) always occupies exactly **2 mantissa slots**: one for the LINKATOM type identifier (value 2) and one for the sequential number N.

## Why It Stays at Depth 2

`rightshift=0` in `tumblerincrement` means the increment touches only the *last* significant digit [SS-TUMBLER] Finding 0031. Since mantissa digits can hold integer values well above 9 (Finding 0033 shows `.3.10`, `.3.11`, etc. from 950-byte bulk inserts), N can grow large without carry propagation.

If N ever *does* trigger a carry into the type-digit position (value 2 → 3), the resulting address is `docISA.0.3` — the upper bound itself — meaning allocation falls outside the link subspace and breaks. There is no path that introduces a third non-separator mantissa slot within the legal range.

## No Other Allocation Path Produces Depth > 2

The only other link-adjacent allocator is `findisatoinsertnonmolecule` (used for document and link *orgl* addresses) [SS-ADDRESS-ALLOC] Finding 0065. It uses `depth=1` with `makehint(DOCUMENT, ATOM, LINKATOM, ...)`, keeping the allocation depth the same. No allocation path uses `rightshift > 0` on a link element address in a way that would append additional sub-levels.

## Summary

Under all normal conditions, link addresses produced by `findisatoinsertmolecule` have element-field length exactly 2. A third element-field level would only arise from arithmetic carry through the type digit, which simultaneously pushes the address to the upper bound, violating the document-scoped invariant from [SS-ADDRESS-SPACE] Finding 0065.

---

## Code Exploration

I now have all the code I need. Here is the complete analysis.

---

## Does `findisatoinsertmolecule` ever produce link addresses with element-field length > 2?

**Short answer: No. The function always produces link addresses with element-field length exactly equal to 2. The structure is invariant.**

---

### The full call chain for link allocation

Every link creation goes through one of two entry points, both in `do1.c`:

- `domakelink` [do1.c:180]: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)`
- `docreatelink` [do1.c:207]: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)`

`makehint` [do2.c:78–84] simply copies fields into a `typehint`:
```c
hintptr->supertype = DOCUMENT;
hintptr->subtype = ATOM;
hintptr->atomtype = LINKATOM;   // LINKATOM = 2  [xanadu.h:146]
movetumbler(isaptr, &hintptr->hintisa);   // hintisa = docisaptr
```

Both then call `createorglingranf` → `createorglgr` [granf2.c:111] → `findisatoinsertgr` [granf2.c:130]:

```c
// [granf2.c:135-155]
if (hintptr->subtype == ATOM) {
    // ATOM subtype always takes this path for links
    findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
} else { ... }
tumblerjustify(isaptr);
```

---

### `findisatoinsertmolecule` dissected [granf2.c:158–181]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    // Step 1: Build the exclusive upper search bound
    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    // For LINKATOM (2): places value 3 at mantissa[idx+2], where idx = last non-zero of docisa
    // upperbound = docisa.0.3 (in element notation)

    clear (&lowerbound, sizeof(lowerbound));

    // Step 2: Find largest existing ISA below upperbound
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        // Branch A: lowerbound is at the same depth as the document
        // (happens on first atom allocation, when only the document orgl is in the granfilade)
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // place LINKATOM=2 at idx+2
        tumblerincrement (isaptr, 1, 1, isaptr);                       // place 1 at idx+3
        // Result: docisa.0.2.1  →  element field = [2, 1]  →  length 2

    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
        // Only reached for text atoms; not relevant to links

    } else if (hintptr->atomtype == LINKATOM) {
        // Branch C: previous link(s) exist; lowerbound = last link address
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
        // candidate: docisa.0.2   (value 2 = LINKATOM at idx+2)

        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
            // lowerbound is before candidate → first link, serial starts at 1
            // Result: docisa.0.2.1  →  element field = [2, 1]  →  length 2
        else
            tumblerincrement (&lowerbound, 0, 1, isaptr);
            // lowerbound is at or after candidate → increment last digit of prior link
            // lowerbound was docisa.0.2.N → result is docisa.0.2.(N+1)
            // element field = [2, N+1]  →  length 2
    }
}
```

---

### `tumblerincrement` mechanics [tumble.c:599–623]

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // finds idx = index of last non-zero mantissa digit of aptr
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    // adds bint at mantissa[idx + rightshift]
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

For a document address `D = [d1, d2, 0, d3, 0, d4, 0, 0, ...]` with last non-zero at `idx=5`:

| Call | Effect | Mantissa result |
|------|--------|-----------------|
| `tumblerincrement(docisa, 2, 2, isaptr)` | places `2` at `mantissa[5+2=7]` | `[d1,d2,0,d3,0,d4, 0, 2, 0,...]` |
| `tumblerincrement(isaptr, 1, 1, isaptr)` | places `1` at `mantissa[7+1=8]` | `[d1,d2,0,d3,0,d4, 0, 2, 1, 0,...]` |

The element field is mantissa positions 7 and 8: values `[2, 1]`. No zero sits between positions 7 and 8, so they form a single 2-element field. Length = **2**.

Every subsequent link increments only the value at position 8 (`tumblerincrement(&lowerbound, 0, 1, isaptr)` adds 1 to the last non-zero, which is at position 8). The element field structure stays `[2, N]` for all N ≥ 1. Length remains **2**.

---

### Can it ever be > 2?

No, for the following structural reasons:

1. **Branch A** (first allocation): builds `[LINKATOM, 1]` at `[idx+2, idx+3]` — exactly 2 positions.

2. **Branch C, first-link sub-case** (lowerbound < candidate): builds `[2, 1]` at `[idx+2, idx+3]` — exactly 2 positions.

3. **Branch C, serial-increment sub-case** (lowerbound ≥ candidate): applies `tumblerincrement(..., 0, 1, ...)` to the last non-zero of the prior link address, which is at `idx+3`. That increments the digit at `idx+3` by 1; it does **not** shift to a new position. Always exactly 2 positions.

4. **No other granfilade insertion path exists for links.** The only route through `insertseq` for link-type entries is via `createorglgr` [granf2.c:119–128], which is only reached through `findisatoinsertgr`.

---

### What element-field length = 2 means concretely

Given a document with ISA `1.1.0.1.0.1`, the link address sequence is:

| Link # | Granfilade ISA | Element field |
|--------|----------------|---------------|
| 1st | `1.1.0.1.0.1.0.2.1` | `[2, 1]` |
| 2nd | `1.1.0.1.0.1.0.2.2` | `[2, 2]` |
| Nth | `1.1.0.1.0.1.0.2.N` | `[2, N]` |

The `2` at mantissa position `idx+2` is the `LINKATOM` type discriminator [xanadu.h:146]. The serial at `idx+3` starts at 1 and increments monotonically with each new link in the document. No zero ever appears between them, so they constitute a single element field of width exactly 2.

**Conclusion:** `findisatoinsertmolecule` — and the entire link allocation path — invariably produces link addresses with element-field length exactly 2. The design hardcodes this: the type discriminator occupies one mantissa slot (`LINKATOM = 2` at `idx+2`) and the serial occupies the immediately adjacent slot (`idx+3`). There is no condition, regardless of document address depth or prior link count, that causes a third slot to be occupied.
