## Question 1 [evidence]

> In udanax-green, how is the link allocator under a document seeded — is there a real ISA allocation that produces the link-prefix base, or does the implementation treat the link subspace as having a virtual starting point?

## KB Synthesis

The link allocator uses a **virtual starting point** — no real ISA allocation seeds the prefix base.

From [SS-ADDRESS-SPACE] Finding 0065, `MAKELINK` calls `findisatoinsertmolecule` with a document-scoped upper bound computed as `tumblerincrement(docISA, 2, LINKATOM+1)`, which bounds the search to the document's link element subspace. The allocation logic then has two branches:

1. **First link case** — `findpreviousisagr` finds nothing in the link range (i.e., `lowerbound < docISA.0.2.2`). The code directly returns `docISA.0.2.1` as the first link I-address. No prior ISA at `docISA.0.2` needs to exist.

2. **Subsequent links** — increments `0.1` from the highest found `lowerbound`.

The address `docISA.0.2.1` is computed purely arithmetically from the document ISA and the `LINKATOM = 2` constant baked into the hint via `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` [SS-ADDRESS-SPACE] Finding 0065. There is no orgl or atom allocated at `docISA.0.2` itself; the `.0.2` field separator is a tumbler hierarchy convention [SS-TUMBLER] Finding 0001, not a pointer to a real granfilade object.

This matches the same pattern as text atoms (element field 3): first text atom at `docISA.0.3.1`, no base object at `docISA.0.3`. Both subspaces are virtual namespaces whose starting addresses are computed from the document ISA + element-field constant, not from any prior allocation. The monotonic-increment invariant [INV-MONOTONIC] then takes over for all subsequent allocations within that subspace.

---

## Code Exploration

Now I have all the data I need with verified line numbers. Here is the complete answer.

---

## How the Link Allocator is Seeded Under a Document

The question has two parts: the **link's ISA** (its address in the global granfilade tree) and the **link's VSA** (its position inside the document's own virtual address space). The code treats these very differently.

---

### Part 1 — The Link ISA: Real Allocation Derived from the Document ISA

`docreatelink` starts by constructing a hint and calling `createorglingranf`:

**`backend/do1.c:207–209`**
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
```

`makehint` (`do2.c:78–84`) packs the hint with:
- `supertype = DOCUMENT`, `subtype = ATOM`, `atomtype = LINKATOM` (= 2, from `xanadu.h:146`)
- `hintisa = *docisaptr` — **the document's own ISA is the hint anchor**

`createorglingranf` → `createorglgr` (both thin wrappers) → `findisatoinsertgr` (`granf2.c:130–156`). Because `hintptr->subtype == ATOM`, it routes to `findisatoinsertmolecule`:

**`backend/granf2.c:130–156`**
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) {
        ...
        return (FALSE);
    }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
```

The guard at line 136 requires that the document ISA **already exists** in the granfilade before a link can be allocated under it — link atoms are children of real document nodes.

Inside `findisatoinsertmolecule` (`granf2.c:158–181`), the `LINKATOM` branch:

**`backend/granf2.c:170–175`**
```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
    if (tumblercmp (&lowerbound, isaptr) == LESS)
        tumblerincrement (isaptr, 1, 1, isaptr);
    else
        tumblerincrement (&lowerbound , 0, 1, isaptr);
}
```

The seed for the link ISA is `docISA.2.2` — formed by incrementing the document's ISA at depth 2 by `LINKATOM = 2`. If no prior link exists under this document, `lowerbound` is zero, which is `LESS` than `docISA.2.2`, so the first link ISA becomes `docISA.2.2.0.1` (one further increment at depth 1). Each subsequent link is allocated by finding the previous link ISA and incrementing from it.

**Conclusion for ISA:** The link-prefix base is a **real structural allocation** in the granfilade, computed as a child of the document's ISA using the hardcoded `LINKATOM = 2` level offset. There is no pre-seeded placeholder; the allocation is live and tracked by the enfilade.

---

### Part 2 — The Link VSA: Fixed Virtual Starting Point

After the link ISA is obtained, `docreatelink` calls `findnextlinkvsa` to place the link inside the document's virtual address space:

**`backend/do2.c:151–167`**
```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
	tumblerclear (&firstlink);
	tumblerincrement (&firstlink, 0, 2, &firstlink);   // mantissa[0] = 2
	tumblerincrement (&firstlink, 1, 1, &firstlink);   // mantissa[1] = 1
	                                                    // → firstlink = 2.1 (hardcoded)

	(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
	tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
	if (tumblercmp (&vspanreach, &firstlink) == LESS)
		movetumbler (&firstlink, vsaptr);
	else
		movetumbler (&vspanreach, vsaptr);
	return (TRUE);
}
```

`firstlink` is **not derived from `docisaptr` at all** — it is a literal constant `2.1` assembled from two `tumblerincrement` calls. This is the floor for link VSAs: a link may never be placed before VSA `2.1` in any document, regardless of the document's own ISA or content.

The runtime check then picks the larger of `2.1` and the end of the document's current content (`vspanreach`), so links always fall at or beyond `2.1` but never overlap existing content.

The link's ISA is then stored at that VSA via `docopy` (`do1.c:212`), recording the link reference in the document's POOM.

---

### Part 3 — The Link Endpoint VSAs: Also Fixed

`setlinkvsas` sets the VSA positions for the link's from/to/three endsets within the link's own POOM:

**`backend/do2.c:169–183`**
```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
	tumblerclear (fromvsaptr);
	tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // fromVSA = 1.1
	tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
	tumblerclear (tovsaptr);
	tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // toVSA = 2.1
	tumblerincrement (tovsaptr, 1, 1, tovsaptr);
	if (threevsaptr) {
		tumblerclear (threevsaptr);
		tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // threeVSA = 3.1
		tumblerincrement (threevsaptr, 1, 1, threevsaptr);
	}
	return (TRUE);
}
```

Every link, in every document, has its three endpoint slots at VSA `1.1`, `2.1`, and `3.1`. These are absolute constants with no relationship to any ISA. The spanfilade span-type constants that index into these (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`, `xanadu.h:36–38`) parallel this layout directly.

---

### Final Answer

The implementation uses a **two-layer addressing scheme** for links:

| Address kind | Mechanism | Derived from doc ISA? |
|---|---|---|
| **Link ISA** (granfilade slot) | Real allocation via `findisatoinsertmolecule`; first link address is `docISA.2.2.0.1` | **Yes** — anchored at depth-2 offset `LINKATOM=2` from the document ISA |
| **Link VSA** (doc virtual space) | `findnextlinkvsa` hardcodes floor `2.1` (`do2.c:157–158`) | **No** — fixed virtual constant, uniform across all documents |
| **Endpoint VSAs** (within link's POOM) | `setlinkvsas` hardcodes `1.1`, `2.1`, `3.1` (`do2.c:169–183`) | **No** — fixed virtual constants |

The **link-prefix base in the ISA space is real**, derived by formula from the document's own ISA. But the **link subspace in VSA space is virtual** — seeded from the hardcoded constant `2.1` with no document-specific derivation. Every document shares the same `2.1` floor for its link subspace; only the subsequent allocation increment (`vspanreach` vs `firstlink`) varies based on whether the document already has content.
