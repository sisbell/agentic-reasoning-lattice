## Question 3 [evidence]

> When `findisatoinsertmolecule` allocates a link address under the `LINKATOM` hint, does the resulting element field carry both a fixed link-subspace component and a separate within-subspace ordinal — i.e., is the element-field depth always at least 2?

## KB Synthesis

Yes — the element field always carries exactly depth 2: a fixed link-subspace component and a separate within-subspace ordinal.

## Evidence

**From [SS-ADDRESS-SPACE] Finding 0065** — the canonical source:

> First link in A: `1.1.0.1.0.1.0.2.1` (element field 2, element number 1)
> Second link in A: `1.1.0.1.0.1.0.2.2`

The full address decomposes as:

```
1.1.0.1 .0. 1 .0. 2 . 1
└─acct──┘   └doc┘   └─── element portion ───┘
                     type  ordinal
```

The `.0.` after the document number is the hierarchical boundary; then `2` is the fixed link-subspace identifier (LINKATOM), and `1` (or `N`) is the monotonically increasing ordinal.

## Mechanism confirms depth = 2

The `findisatoinsertmolecule` call uses [SS-ADDRESS-SPACE] Finding 0065:

```c
tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)
```

- `rightshift = 2` — the upper bound is placed 2 digits right of the document ISA, bounding the entire `(element_field, element_number)` subspace
- `atomtype + 1 = LINKATOM + 1 = 3` — upper bound excludes the text element field (3), so links occupy `[2, 3)` in the first element digit
- The first-link condition checks `lowerbound < docISA.0.2.2` and allocates at `docISA.0.2.1` — showing the ordinal as a second, independent digit

## Summary

Per [SS-ADDRESS-SPACE] Finding 0065: "element_field = 2 for links … and element_number is allocated monotonically within each (document, element_field) pair." The two components are structurally independent: the subspace digit (2) is fixed by `LINKATOM`, while the ordinal digit is what `findpreviousisagr` + `tumblerincrement(..., 0, 1, ...)` increments per allocation. Depth is always exactly 2 within the element portion — never 1, never 3.

---

## Code Exploration

Now I have everything needed to answer the question precisely. Let me trace all code paths through `findisatoinsertmolecule` for the LINKATOM case.

---

## Analysis: `findisatoinsertmolecule` under `LINKATOM` hint

### Entry point

`docreatelink` (and `docreatenewversion`) call `makehint` at `do1.c:180` and `do1.c:207`:

```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
```

`makehint` at `do2.c:78–84` simply stores:
- `hint.subtype = ATOM`
- `hint.atomtype = LINKATOM = 2` (`xanadu.h:146`)
- `hint.hintisa = *docisaptr` (the document's ISA, length *L*)

`findisatoinsertgr` at `granf2.c:130–156` routes to `findisatoinsertmolecule` because `hint.subtype == ATOM`.

---

### `findisatoinsertmolecule` — full code, `granf2.c:158–181`

```c
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
clear (&lowerbound, sizeof(lowerbound));
findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164

if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {        // line 165
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
    tumblerincrement (isaptr, 1, 1, isaptr);
} else if (hintptr->atomtype == TEXTATOM) {                                    // line 168
    tumblerincrement (&lowerbound, 0, 1, isaptr);
} else if (hintptr->atomtype == LINKATOM) {                                    // line 170
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                        // line 171
    if (tumblercmp (&lowerbound, isaptr) == LESS)                              // line 172
        tumblerincrement (isaptr, 1, 1, isaptr);                               // line 173 — B1
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);                         // line 175 — B2
}
```

---

### `tumblerincrement` mechanics — `tumble.c:599–623`

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = index of last non-zero digit in aptr
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

`rightshift` pushes the new digit that many positions to the right of the last existing non-zero. A zero at `idx+1` acts as a separator; the new non-zero digit lands at `idx+rightshift`. `tumblerlength = nstories - exp` counts meaningful mantissa slots (`tumble.c:259–262`).

---

### Three LINKATOM paths and their resulting depths

Let *L* = `tumblerlength(&hintptr->hintisa)`. Let `idx` = last non-zero position of `hintisa` in the mantissa array.

**Path 1 — first branch (line 165):**
Triggered when `tumblerlength(lowerbound) == L` (lowerbound at document-level depth, e.g. `hintisa` itself).

| Step | Call | Position written | mantissa suffix | Δ depth |
|---|---|---|---|---|
| 1 | `tumblerincrement(&lowerbound, 2, 2, isaptr)` | `idx+2` | `…,0,2,…` | +2 → L+2 |
| 2 | `tumblerincrement(isaptr, 1, 1, isaptr)` | `idx+3` | `…,0,2,1,…` | +1 → **L+3** |

**Path B1 — LINKATOM else-if, line 173:**
Triggered when `lowerbound < hintisa.[0].2` (no existing links, or lowerbound falls below the link subspace base).

| Step | Call | Position written | mantissa suffix | Δ depth |
|---|---|---|---|---|
| 1 | `tumblerincrement(&hintisa, 2, 2, isaptr)` | `idx+2` | `…,0,2,…` | +2 → L+2 |
| 2 | `tumblerincrement(isaptr, 1, 1, isaptr)` | `idx+3` | `…,0,2,1,…` | +1 → **L+3** |

When `lowerbound` is the zero tumbler (no items at all), `tumblercmp(zero, hintisa.[0].2)` returns `LESS` (`tumble.c:74–78`), so this path is taken for the very first link — it never falls through to B2 on an empty tree.

**Path B2 — LINKATOM else-if, line 175:**
Triggered when `lowerbound ≥ hintisa.[0].2` (existing link addresses are present).

```c
tumblerincrement (&lowerbound, 0, 1, isaptr);
```

`lowerbound` was found by `findpreviousisagr` scanning for the highest ISA < `hintisa.[0].(LINKATOM+1) = hintisa.[0].3`. Any previously-allocated link address is of the form `hintisa.[0].2.N` (mantissa `…,0,2,N,…`), which has depth L+3. Incrementing the last digit: position written = `idx+3`, result = `…,0,2,N+1,…`, depth = **L+3**.

---

### Fixed subspace component + within-subspace ordinal

The mantissa of a LINKATOM ISA always has this layout relative to `hintisa`'s last non-zero digit at `idx`:

```
position:  …  idx  │ idx+1 │ idx+2 │ idx+3 │ …
value:         X   │   0   │   2   │   N   │ 0 …
                   │ ←sep→ │ ←LINK │ ←ord→ │
                            subspace  inal
```

- **Position `idx+1` = 0**: separator zero, mandatory by `rightshift=2` in `tumblerincrement`.
- **Position `idx+2` = 2 (= LINKATOM)**: the **fixed link-subspace component**. Hardcoded `bint=2` at `granf2.c:171`. This digit is the same for every link within the document.
- **Position `idx+3` = N**: the **within-subspace ordinal**. N=1 for the first link (paths 1 and B1), N+1 for each subsequent link (path B2). This digit varies per link.

Both components are always present. There is no code path through `findisatoinsertmolecule` for LINKATOM that writes only the subspace component without the ordinal.

---

### Depth conclusion

`tumblerlength(result) - tumblerlength(hintisa)` for all LINKATOM paths:

| Path | Depth from `hintisa` |
|---|---|
| Path 1 (line 165–167) | **3** |
| Path B1 (line 173) | **3** |
| Path B2 (line 175) | **≥ 3** (= 3 for sequential ordinals, more if address space has grown) |

The minimum is **3 extra mantissa positions** beyond `hintisa`'s last non-zero, not 2. In semantic terms this is **depth 2** beyond the document: one non-zero group for the subspace designator (`2`) and one non-zero group for the ordinal (`N`), separated from the document by a single zero at `idx+1`.

So the answer to the question is: **yes**, the element field always carries both a fixed link-subspace component (`2` = LINKATOM, at `idx+2`) and a separate within-subspace ordinal (N, at `idx+3`), and the depth is always at least 2 (exactly 3 extra mantissa positions, which encodes two distinct non-zero components after the separator zero). The depth is never less than 2, and in current practice is never greater than 3 unless prior allocations have grown the link address space beyond `hintisa.[0].2.N` addresses — but even then, all invariants hold.
