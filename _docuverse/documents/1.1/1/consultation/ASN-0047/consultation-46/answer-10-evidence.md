## Question 10 [evidence]

> In udanax-green, how does the document-level allocation machinery structure content-address and link-address production — does the implementation maintain a parent element-field allocator with distinct content and link sub-allocators, or are content and link addresses produced by independent allocators each rooted at the document's prefix?

## KB Synthesis

The implementation uses **independent allocators rooted at different tumbler ranges** within a single shared granfilade — not a parent element-field allocator with distinct sub-allocators.

## Allocation Mechanism

Both text content and link orgl allocation use the same stateless query-and-increment function (`findisatoinsertmolecule` or `findisatoinsertnonmolecule`), differing only in the `upperbound` parameter that restricts which granfilade subtree is searched. There is no parent allocator object; the element-field distinction is encoded in the bounds passed at call time.

From [SS-ADDRESS-ALLOC] Finding 0077: "Allocation is a family of independent functions partitioned by tumbler range: `next_doc_addr(granf, parent)` and `next_content_addr(granf, doc)`. Both query the same granfilade tree but search different subtrees."

## Address Space Partitioning

Link orgls and text content occupy distinct tumbler ranges within the document's address namespace [SS-ADDRESS-ALLOC] Finding 0065:

```
account.0.document.0.element_field.element_number
                               ^2 = links
                               ^3 = text
```

- **Link addresses**: MAKELINK sets `upperbound = docISA.0.2.3`, bounding search to element field 2. First link allocates at `docISA.0.2.1`; subsequent ones increment monotonically within that range.
- **Text addresses**: INSERT's hint targets element field 3 (in the permascroll subtree), with a different upper bound.

## Critical Interaction: Allocators Are Not Isolated

Despite targeting different subtrees, the allocators share the global granfilade's maximum-address state. `findpreviousisagr` finds the highest I-address below the upper bound — and when a CREATELINK allocates a link orgl, that address becomes visible to subsequent text allocation searches if the text bound encompasses it.

[INV-MONOTONIC] Finding 0063 documents this directly:

```
INSERT "ABC" → text I-addresses I.1, I.2, I.3
CREATELINK   → link orgl consumes range up to ~I.2.0
INSERT "DEF" → findpreviousisagr returns link orgl's address as max
               → allocates at 2.1, 2.2, 2.3 (gap in text sequence)
```

`compare_versions` then reports **two** shared span pairs instead of one, because the text I-addresses for "ABC" and "DEF" are non-contiguous.

By contrast, CREATENEWVERSION does **not** break contiguity: it allocates only a document-level address (via `findisatoinsertnonmolecule`, targeting a different subtree) and never calls the content allocator [INV-MONOTONIC] Finding 0077.

## Summary

The implementation has no parent element-field allocator. There is one global granfilade, one stateless allocation mechanism, and two logically independent (but physically coupled) allocation ranges: `docISA.0.2.x` for links and a separate permascroll range for text. Their independence is a property of the bounds passed to the allocator, not of separate allocator state — which is why CREATELINK can fragment subsequent text I-address contiguity despite targeting a nominally separate range.

---

## Code Exploration

I now have everything I need. Here is the full analysis with direct source citations.

---

## Document-Level Allocation Machinery in Udanax-Green

### Short Answer

Neither framing quite fits. The implementation uses **one allocation function (`findisatoinsertmolecule`) rooted at the document ISA**, with `atomtype` arithmetically partitioning the tumbler address space into distinct content and link sub-ranges. There is no runtime sub-allocator object and no pair of independent allocators — just a single coordinate-finding algorithm that branches on `atomtype` to produce addresses in non-overlapping ISA sub-ranges.

---

### The Type Hierarchy (xanadu.h:140–146)

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4

#define TEXTATOM  1
#define LINKATOM  2
```

`ATOM` is the leaf level — one step below `DOCUMENT`. Content and links are both atoms, distinguished only by `atomtype`.

---

### The Hint: Shared Root, Different Discriminator

Both operations call `makehint` (do2.c:78–84) with the same document ISA but different `atomtype`:

**Text insertion** (`do1.c:117`):
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
```

**Link creation** (`do1.c:207`):
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

`makehint` itself (do2.c:78–84) simply copies `docisaptr` into `hintptr->hintisa`:
```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

The document ISA is the **single shared root** for both content and link allocation. The only difference is `atomtype`: 1 for text, 2 for links.

---

### The Shared Allocation Function: `findisatoinsertmolecule`

`findisatoinsertgr` (granf2.c:130–156) dispatches all `ATOM`-subtype hints into one function:

```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // ← both text AND links
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
```

**Both text and link addresses are computed by the same function** `findisatoinsertmolecule` at granf2.c:158–181:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {        // line 165
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);              // line 166
        tumblerincrement (isaptr, 1, 1, isaptr);                                   // line 167
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);                          // line 169
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                        // line 171
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);                               // line 173
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                         // line 175
    }
}
```

#### How `tumblerincrement` works (tumble.c:599–623)

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    // finds idx = array index of rightmost non-zero mantissa digit
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

`tumblerincrement(a, n, b, c)` adds `b` at `n` positions to the right of `a`'s least significant digit — effectively appending `n` zero components followed by `b`.

---

### The Address Spaces Produced

Let `D` denote the document ISA (e.g., `1.1.0.1.0.1` — 6 components). The **upperbound scan** at line 162 bounds each atomtype's region:

| atomtype | `atomtype + 1` | `upperbound` |
|---|---|---|
| TEXTATOM = 1 | 2 | `D.0.2` |
| LINKATOM = 2 | 3 | `D.0.3` |

`findpreviousisagr` scans the granfilade for the highest existing ISA below `upperbound`. This is the **prior allocation** within this atomtype's slot.

#### First allocation ever (line 165 branch: `tumblerlength(hintisa) == tumblerlength(lowerbound)`)

The document orgl itself is stored at the document ISA `D`. `findpreviousisagr(upperbound=D.0.2)` returns `lowerbound = D` (the document itself, same length as `hintisa`). So:

```
tumblerincrement(D, 2, atomtype, isaptr)   → D.0.atomtype
tumblerincrement(D.0.atomtype, 1, 1, isaptr) → D.0.atomtype.0.1
```

- **First text atom**: `D.0.1.0.1`
- **First link atom**: `D.0.2.0.1`

#### Subsequent text atoms (line 169 branch: TEXTATOM, prior exists)

```
tumblerincrement(lowerbound, 0, 1, isaptr)   → lowerbound + 1
```

Addresses increment monotonically: `D.0.1.0.1`, `D.0.1.0.2`, `D.0.1.0.3`, …

#### Subsequent link atoms (lines 171–175 branch: LINKATOM, prior exists)

```
tumblerincrement(D, 2, 2, isaptr)    → D.0.2   (lower bound of link space)
if (lowerbound < D.0.2):             → tumblerincrement(D.0.2, 1, 1) → D.0.2.0.1
else:                                → tumblerincrement(lowerbound, 0, 1) → lowerbound + 1
```

Addresses: `D.0.2.0.1`, `D.0.2.0.2`, `D.0.2.0.3`, …

---

### The Two Sub-Namespaces

| Type | ISA range | First address |
|---|---|---|
| Text content | `[D.0.1.0.1 … D.0.2)` | `D.0.1.0.1` |
| Link orgl | `[D.0.2.0.1 … D.0.3)` | `D.0.2.0.1` |

The second position-2 component (`0.1` for text, `0.2` for links) **is the `atomtype` value itself encoded directly into the ISA**. There is no separate counter per type — the address space is partitioned by the tumbler arithmetic, and the "counter" is implicit in the coordinate of the last allocated atom, recovered by `findpreviousisagr`.

---

### No Independent Allocators: Shared `findpreviousisagr` Scan

There is no hidden per-type counter. `findpreviousisagr` (granf2.c:255–278) traverses the enfilade tree to find the highest occupied coordinate below the upper bound:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ((tmp= whereoncrum (ptr, (typewid*)offset, upperbound, WIDTH)) == THRUME
         || tmp == ONMYRIGHTBORDER || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);
        }
    }
}
```

The previous-address scan is type-agnostic — it just walks the enfilade. `upperbound` is the only thing that constrains which sub-space is searched. Text and links use different `upperbound` values, so their scans are mutually exclusive.

---

### Link V-Address Allocation (The Permascroll Dimension)

Separate from the ISA (granfilade) address, each link's reference in the containing document also needs a V-address (virtual stream position in the document orgl). `findnextlinkvsa` (do2.c:151–167) computes this:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // → 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // → 2.0.1
```

So the first link V-position is `2.0.1`. This places all link references in V-space `< 1.0` (i.e., `0.x` in V-space), clearly distinct from text content which occupies V ≥ 1.0. This is confirmed by the `filter_vspanset_to_text_subspace` guard at do1.c:386–411, which explicitly strips spans with `stream < 1.0` (link subspace) from content comparisons.

`setlinkvsas` (do2.c:169–183) further partitions the link orgl's internal V-address space by endpoint role:
```c
// FROM endpoint → V-position 1.1
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // → 1
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // → 1.0.1

// TO endpoint → V-position 2.1
tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // → 2
tumblerincrement (tovsaptr, 1, 1, tovsaptr);      // → 2.0.1

// THREE endpoint → V-position 3.1
tumblerincrement (threevsaptr, 0, 3, threevsaptr);
tumblerincrement (threevsaptr, 1, 1, threevsaptr); // → 3.0.1
```

---

### Spanfilade Indexing: Four Named Ranges

`insertspanf` (spanf1.c:22) prefixes each span index entry with a type tag:

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

The `spantype` constants are:
- `LINKFROMSPAN` = 1
- `LINKTOSPAN` = 2  
- `LINKTHREESPAN` = 3
- `DOCISPAN` = 4

`prefixtumbler` (tumble.c:641–651) prepends `spantype` as a new most-significant digit, creating separate spanfilade regions. Text content uses `DOCISPAN=4`; link endpoint indices use 1/2/3. These are the index-side complement of the ISA-side partitioning.

---

### Conclusion

The implementation does **not** maintain a parent element-field allocator object with distinct sub-allocator children. Nor are content and link addresses produced by fully independent allocators with their own roots.

Instead: **a single function `findisatoinsertmolecule` (granf2.c:158–181) serves as the unified allocator for all atom-level ISAs under a document.** The document ISA is the shared prefix/root for both. The `atomtype` field (TEXTATOM=1, LINKATOM=2) is encoded **arithmetically into the ISA** at the second-to-last position (`D.0.atomtype.*`), partitioning the tumbler address space into non-overlapping sub-ranges without any runtime sub-allocator object. The "next free address" in each sub-range is recovered dynamically by scanning the enfilade (`findpreviousisagr`) rather than maintained in a counter. Text atoms live in `D.0.1.*`; link atoms live in `D.0.2.*` — both under the same document ISA `D`, allocated by the same code path, separated only by the arithmetic encoding of `atomtype` in the tumbler coordinates.
