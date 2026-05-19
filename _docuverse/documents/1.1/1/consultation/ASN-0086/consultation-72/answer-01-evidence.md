## Question 1 [evidence]

> Does udanax-green's link allocator deposit link addresses exclusively on the per-document A_L sibling chain enumeration (matching ChainMembershipForOrigin), or does it expose any link-emission path that produces L1c-conforming but off-chain addresses (e.g., deeper element fields, alternative child-spawn patterns under d)?

## KB Synthesis

## Link Address Allocation: Strictly On-Chain

The KB is unambiguous: udanax-green's link allocator produces only flat sibling-chain addresses within each document's element-field-2 namespace. There are no off-chain paths.

### The Allocation Mechanism

From [SS-ADDRESS-ALLOC] Finding 0065, `MAKELINK` uses `findisatoinsertmolecule` with a document-scoped bound:

1. `upperbound = docISA.2.3` — search bounded to element field 2 only; field 3 (type endpoints) is excluded
2. `findpreviousisagr` finds the highest existing link address below that bound
3. If none exist: allocate at `docISA.2.2.1` (first child of element field 2)
4. Otherwise: `tumblerincrement(&lowerbound, 0, 1, isaptr)` — increment by 1 at rightshift=0, producing the next sibling

The result is strictly `d.0.2.1`, `d.0.2.2`, `d.0.2.3`, … — a monotonically increasing flat chain under `d.0.2`.

### No Child-Spawn or Deeper-Field Paths

The `tumblerincrement(..., 0, 1, ...)` call increments only the terminal digit (rightshift=0), which produces siblings, never children. The code path for child allocation (`findisatoinsertnonmolecule`, depth=1) is used for document addresses [SS-ADDRESS-ALLOC Finding 0068] but **not** for link orgls. `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` routes exclusively to the molecule path [SS-ADDRESS-SPACE Finding 0065, `do1.c:211`].

### Single Emission Path

From [SS-ADDRESS-SPACE] Finding 0077: document addresses (`findisatoinsertnonmolecule`) and content I-addresses (`findisatoinsertmolecule`) occupy separate allocation dispatches. All link orgl creation goes through `docreatelink` → `createorglingranf` with `LINKATOM` — there is no secondary emission route.

### Bounds Prevent Escape

The upper bound `docISA.2.3` is a hard ceiling. No link address can reach element field 3 (type endpoints, which occupy `d.0.3.x`) or escape to deeper element fields. The per-document independence is confirmed: Document A's links (`d_A.0.2.1`, `d_A.0.2.2`) and Document B's links (`d_B.0.2.1`, `d_B.0.2.2`) are allocated independently from separate bounded searches [SS-ADDRESS-ALLOC Finding 0065 concrete example].

**Conclusion:** The link allocator is strictly confined to the per-document `d.0.2.*` sibling chain via the molecule allocation path with hard upper bounds. No path exists to produce L1c-conforming addresses via deeper element fields or child-spawn patterns.

---

## Code Exploration

I now have all the source evidence needed. Let me compile the full answer.

---

## Answer: Link Allocator Address Confinement

The link allocator in udanax-green deposits link ISAs **exclusively on the per-document A_L chain** `docisa.0.2.N` (N = 1, 2, 3, …). There is no emission path that produces L1c-conforming but off-chain addresses. Here is the complete code trace.

---

### Entry Points: Two Paths, One Allocator

Both FEBE-visible link creation functions route through identical allocation logic:

**`docreatelink`** (`do1.c:195–221`):
```c
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)
  ...
```

**`domakelink`** (`do1.c:169–193`) is identical through this step. Only the endpoint count differs; the ISA allocator call is the same.

**There is one and only one granf ISA allocation per link**: `createorglingranf` at `do1.c:209` (and `do1.c:182`).

---

### Type Constants

From `xanadu.h:145–146`:
```c
#define TEXTATOM  1
#define LINKATOM  2
```

`makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` (`do2.c:78–84`) sets:
- `hint.supertype = DOCUMENT = 3`
- `hint.subtype   = ATOM = 4`
- `hint.atomtype  = LINKATOM = 2`
- `hint.hintisa   = *docisaptr`

---

### Allocator Chain

`createorglingranf` → `createorglgr` (`granf2.c:111–128`):
```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
    return (FALSE);
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

`findisatoinsertgr` (`granf2.c:130–156`):
```c
if (hintptr->subtype == ATOM) {
    if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { ... return FALSE; }
    findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);  // ← taken for links
} else {
    findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
}
tumblerjustify(isaptr);
```

Since `hint.subtype == ATOM`, the `findisatoinsertmolecule` branch is always taken for link ISA allocation.

---

### The Allocator Core: `findisatoinsertmolecule` (`granf2.c:158–181`)

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    // For LINKATOM=2: upperbound = docisa @ (idx+2, digit=3) = docisa.0.3
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // lowerbound = largest granf entry < docisa.0.3

    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        // Case 1: no atoms exist yet — lowerbound IS docisa
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
        // = docisa.0.2 then docisa.0.2.1
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
        // base = docisa.0.2 — anchored to docisa, not lowerbound
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
            // first link: docisa.0.2.1
        else
            tumblerincrement (&lowerbound, 0, 1, isaptr);
            // nth link: lowerbound + 1 = docisa.0.2.(N+1)
    }
}
```

#### `tumblerincrement` semantics (`tumble.c:599–623`)

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

`rightshift` extends beyond the last non-zero digit. For `docisa = [1,1,0,1,0,1,0,...]` (mantissa representation of `1.1.0.1.0.1`, last non-zero at idx=5):

- `tumblerincrement(docisa, 2, 2, isaptr)` → `mantissa[7] += 2` → `[1,1,0,1,0,1,0,2,0,...]` = `docisa.0.2`
- `tumblerincrement(docisa.0.2, 1, 1, isaptr)` → `mantissa[8] += 1` → `[1,1,0,1,0,1,0,2,1,0,...]` = `docisa.0.2.1`

**This matches the golden output exactly** (finding 0065):

| Link | Document | ISA |
|------|----------|-----|
| L1 | `1.1.0.1.0.1` | `1.1.0.1.0.1.0.2.1` |
| L2 | `1.1.0.1.0.2` | `1.1.0.1.0.2.0.2.1` |
| L3 | `1.1.0.1.0.1` | `1.1.0.1.0.1.0.2.2` |

The A_L chain for each document: `docisa.0.2.1`, `docisa.0.2.2`, …, `docisa.0.2.N`.

---

### Why There Are No Off-Chain Addresses

**1. The LINKATOM branch anchors to `docisa`, not `lowerbound`.**

The critical line is `granf2.c:171`:
```c
tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // base = docisa.0.2
```

This uses `hintptr->hintisa` (= docisa from `makehint`). Even in the `else` branch where `lowerbound >= docisa.0.2`, the increment is `lowerbound + 1`, and `lowerbound` must be a `docisa.0.2.N` address (the only things in granf in range `[docisa.0.2, docisa.0.3)`). There is no route to produce an address with a different document prefix.

**2. The search boundary confines `lowerbound` to the link subspace.**

`upperbound = docisa.0.3`. `findpreviousisagr` returns the largest granf entry strictly less than this. All text ISAs are `docisa.0.1.N < docisa.0.2 < docisa.0.3`, so they are candidates but will trigger `lowerbound < docisa.0.2`, taking the `tumblerincrement(isaptr, 1, 1, isaptr)` branch that always produces `docisa.0.2.1` (first link). No out-of-band address can surface here.

**3. Case 1 (`lowerbound` same length as `docisa`) is safe.**

This branch fires when no atoms yet exist under `docisa`. In that case `lowerbound = docisa` itself (since `docisa` IS stored in granf and is the largest entry of equal tumbler length below `docisa.0.3`; any sibling document `docisa' > docisa` would be ≥ `docisa.0.3` and thus excluded). The result is `tumblerincrement(docisa, 2, 2, ...) + (.1)` = `docisa.0.2.1`. Same chain.

**4. Endpoint VSAs (`setlinkvsas`, `do2.c:169–183`) are internal, not ISAs.**

```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // 1.1 — from-endpoint V-pos within link orgl
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
tumblerincrement (tovsaptr, 0, 2, tovsaptr);      // 2.1 — to-endpoint V-pos within link orgl
tumblerincrement (tovsaptr, 1, 1, tovsaptr);
tumblerincrement (threevsaptr, 0, 3, threevsaptr);// 3.1 — three-endpoint V-pos
tumblerincrement (threevsaptr, 1, 1, threevsaptr);
```

These are V-coordinates **inside the link's own POOM** (used by `insertendsetsinorgl`, `do1.c:218`). They are not granf ISAs and produce no new entries in the A_L address space.

**5. `findnextlinkvsa` (`do2.c:151–167`) assigns V-position, not ISA.**

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = 2.1
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);  // first link: V = 2.1
else
    movetumbler (&vspanreach, vsaptr);
```

This computes the link's **V-address** (position in the owning document's POOM, link subspace V = 2.x). It is passed to `docopy` which stores the link ISA at that V-position in the document's enfilade. No new granf ISA is created here.

---

### No Alternative Child-Spawn Under d

`insertendsetsinorgl` (`do2.c`, called at `do1.c:218`) writes into the **existing link orgl** identified by `linkisaptr`. It calls `insertpm` on the link's own orgl enfilade (not granf). No new ISA is emitted in granf.

`insertendsetsinspanf` writes into the **spanfilade** (link endpoint index), not granf. No ISA.

`tumbler2spanset` (`do2.c:48–61`, called at `do1.c:210`) wraps the already-allocated `linkisaptr` into an ispan structure — no new allocation.

---

### Conclusion

The link allocator deposits ISAs **exclusively** on the chain:

```
docisa.0.2.1,  docisa.0.2.2,  …,  docisa.0.2.N
```

This chain is per-document (confirmed by golden output: intervening link creation on a different document does not advance the counter, finding 0065). The `0` in `.0.2.N` is a mantissa field separator (T4 convention), not a subspace identifier; the element field is `2` (LINKATOM), and the element number is N.

There is no off-chain emission path. The LINKATOM branch of `findisatoinsertmolecule` (`granf2.c:170–175`) unconditionally derives its base address from `hintptr->hintisa` (= `docisa`), not from `lowerbound`. No deeper element field, no alternative child spawn pattern under `d`, and no endpoint VSA path can produce a granf ISA outside `docisa.0.2.N`.
