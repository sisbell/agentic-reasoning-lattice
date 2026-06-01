## Question 2 [evidence]

> After a document's link subspace is fully cleared, does the implementation re-pin the link-subspace depth from scratch on the next link insertion, or does it preserve/reuse the document's original link-subspace depth?

## KB Synthesis

## Re-pinning After Link Subspace Clearance

The KB is sufficient to answer this, though by inference across entries rather than a direct finding.

**The implementation re-pins from `2.1` on the next link insertion.**

### Mechanism

`findnextlinkvsa` (`do2.c:151-167`) is a **dynamic computation against current POOM state**, not a cached counter [SS-LINK-SUBSPACE, Finding 0052]. It:
1. Initializes `firstlink` by incrementing to `2.1` as the floor
2. Uses `vspanreach` — the current document extent — to position subsequent links

`vspanreach` reads the live POOM tree. When all `2.x` entries are removed via DELETEVSPAN, the POOM has no 2.x crums [FC-LINK-DELETE-ISOLATION, Finding 0040]. The reach in the `2.x` subspace collapses to zero, so `findnextlinkvsa` falls back to the `2.1` floor — identical to first-ever link creation.

### Important asymmetry

The V-position re-pins to `2.1`, but the **I-address allocation does not reset**. Link orgl I-addresses are allocated monotonically via `findisatoinsertmolecule` querying the granfilade maximum [INV-MONOTONIC, SS-ADDRESS-ALLOC]. The cleared link orgls still occupy their I-addresses in the granfilade permanently [INV-LINK-PERMANENCE], so the next link receives `docISA.2.(N+1)` in I-space — it does not reuse `.2.1`.

This means the same V-position (`2.1`) can be occupied by a different link orgl I-address after a clear-and-recreate cycle. The POOM depth is re-derived; the permascroll depth is not.

### Caveat

No KB finding directly tests "delete all links then create new link." The above is an inference from [SS-LINK-SUBSPACE], [FC-LINK-DELETE-ISOLATION], [INV-MONOTONIC], and [SS-ADDRESS-ALLOC]. The EC-EMPTY-DOC finding (0058) warns that delete-everything leaves empty intermediate POOM nodes without bottom crums — whether this causes `firstinsertionnd` issues for the 2.x subspace specifically is not documented.

---

## Code Exploration

I have all the data I need. Let me write the final answer.

---

## Answer: Link-Subspace Depth After Full Clear

The implementation **re-derives the link-subspace depth completely from scratch** on the next insertion. There is no stored "original depth" anywhere in the data structures. Two independent mechanisms confirm this.

---

### Mechanism 1 — V-address placement (`findnextlinkvsa`)

`docreatelink` [do1.c:195–221] calls `findnextlinkvsa` at line 211 to determine where in the document's V-space the link ISA reference will be placed.

`findnextlinkvsa` [do2.c:151–167] is:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // line 157: firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // line 158: firstlink = 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);            // line 160
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);             // line 161
    if (tumblercmp (&vspanreach, &firstlink) == LESS)                  // line 162
        movetumbler (&firstlink, vsaptr);                              // line 163
    else
        movetumbler (&vspanreach, vsaptr);                             // line 165
    return (TRUE);
}
```

From `tumblerincrement` [tumble.c:599–623], starting from a zero tumbler:
- `tumblerincrement(zero, 0, 2)` → `mantissa[0]=2, exp=0` → tumbler `2`
- `tumblerincrement(2, 1, 1)` → `mantissa[0]=2, mantissa[1]=1` → tumbler `2.1`

So `firstlink` is the **hardcoded constant `2.1`** — it is never read from any stored state.

The function returns `max(vspanreach, firstlink)`. When the link subspace is fully cleared, the document's vspan covers only the text content. Text lives at V ≥ 1.x. Since `abscmp` [tumble.c:87–111] compares mantissa arrays from index 0, any tumbler of the form `1.x` is `LESS` than `2.1` (mantissa[0]: 1 < 2). Therefore:

- `tumblercmp(&vspanreach, &firstlink) == LESS` → TRUE
- `movetumbler(&firstlink, vsaptr)` [line 163]: placement = **`2.1`**

This is **identical** to a document that has never had any links. The constant `firstlink = 2.1` acts as a floor, resetting placement every time the subspace is cleared.

---

### Mechanism 2 — ISA allocation (`findisatoinsertmolecule`, LINKATOM branch)

`createorglingranf` (called at do1.c:209) invokes `createorglgr` → `findisatoinsertgr` [granf2.c:130–156] → `findisatoinsertmolecule` [granf2.c:158–181] for the `LINKATOM` case.

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);  // line 162
    // LINKATOM: atomtype=2, so upperbound = docISA.0.0.3

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);      // line 164
    // Finds last granfilade entry before docISA.0.0.3

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        ...
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);                        // line 171
        // isaptr = docISA.0.0.2
        if (tumblercmp (&lowerbound, isaptr) == LESS)                              // line 172
            tumblerincrement (isaptr, 1, 1, isaptr);                               // line 173
            // isaptr = docISA.0.0.2.0.1   ← the first-link address
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);                         // line 175
    }
```

After all links (which lived at `docISA.0.0.2.*`) are deleted, `findpreviousisagr` searches for the last entry before `docISA.0.0.3`. It finds the last **text** atom at some address like `docISA.0.0.1.0.K`.

The comparison at line 172: `tumblercmp(docISA.0.0.1.0.K, docISA.0.0.2)`. At the third mantissa component, `1 < 2` → `LESS`. So the branch at line 173 executes:

```
isaptr = docISA.0.0.2.0.1
```

This is the **same ISA address** the very first link would receive in a brand-new document. The granfilade sees no prior link atoms and re-starts the sequence from the bottom.

---

### No Stored Depth Field

Searching the entire structure definitions confirms there is no persisted depth marker. `acceptablevsa` [do2.c:110–113] is a stub that unconditionally returns `TRUE` and reads nothing:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

The enfilade `typecuc`/`typecbc` nodes [referenced in granf2.c] track tree structure (`height`, `cwid`, `cdsp`) but carry no field encoding "link-subspace depth from original creation."

---

### Conclusion

After a document's link subspace is fully cleared:

1. **`findnextlinkvsa`** computes V-placement as `max(vspanreach, 2.1)`. With only text remaining, `vspanreach < 2.1`, so the result is the hardcoded constant **`2.1`** — identical to a fresh document. [do2.c:156–165]

2. **`findisatoinsertmolecule`** scans the granfilade, finds no prior link atoms, and allocates **`docISA.0.0.2.0.1`** — the same first-link ISA as an unlinked document. [granf2.c:170–173]

Both placements are derived entirely from **current document state** via live granfilade scans. No depth is preserved. The system re-pins from scratch.
