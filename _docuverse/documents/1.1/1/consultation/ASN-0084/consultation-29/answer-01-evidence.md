## Question 1 [evidence]

> Does the udanax-green implementation fix the text subspace at depth 2, or does it permit (or instantiate) text subspaces with m_1 > 2?

## KB Synthesis

The implementation fixes text content at **mantissa[0] = 1 exclusively**. No text subspace with m_1 > 1 is intentionally instantiated, and m_1 > 2 is not used for any content type other than link type endpoints.

## What the KB shows

**Three fixed subspaces, no more:**

[SS-SUBSPACE-CONVENTION] (Finding 0038) establishes the complete partition: mantissa[0] = 1 for text, 2 for link references, 3 for link type endpoints. `setlinkvsas()` hardcodes digit-0 values of 1, 2, and 3 for the FROM, TO, and THREE endpoints respectively. No subspace at digit 4 or higher is ever instantiated.

**Text is fixed to m_1 = 1 by the operational layer:**

[SS-DUAL-ENFILADE] (Finding 0009) confirms: V-position `1.x` is the text subspace; `doinsert` writes only there. [SS-LINK-SUBSPACE] (Finding 0052) confirms links start at `2.1` via `findnextlinkvsa`. The type endpoint at `3.x` comes from `setlinkvsas()` — never used for text.

**The knife generalizes, but callers don't:**

[SS-TWO-BLADE-KNIFE] (Finding 0054) documents that `findaddressofsecondcutforinsert()` computes `(N+1).1` for any insertion at `N.x`, making INSERT at `4.x` or `5.x` structurally isolated in principle. But no calling code places text at N ≥ 2 intentionally.

**Convention, not enforcement:**

[PRE-INSERT] (Finding 0049) shows text CAN land at `2.x` through a misbehaving INSERT, and [PRE-REARRANGE] (Finding 0051) shows REARRANGE can shift text into `2.x` or `3.x`. These are invariant violations, not intended subspaces. The backend enforces nothing — `acceptablevsa()` always returns TRUE [SS-SUBSPACE-CONVENTION] (Finding 0010).

## Summary

The text subspace is fixed at **m_1 = 1** with no intended instantiation at m_1 ≥ 2. Subspace m_1 = 3 belongs to type endpoints, not text. The generalized knife in `findaddressofsecondcutforinsert()` could handle higher subspaces structurally, but the system defines only three named subspaces ({1,2,3}) and never allocates a fourth for any purpose.

---

## Code Exploration

Now I have all the information needed to give a precise, code-grounded answer. Let me compile it.

---

## Answer: Text Subspace Depth in udanax-green

### Short answer

The implementation **fixes the text subspace at a hardcoded offset of exactly 2 positions** from the document ISA in the granfilade. The subspace selector digit for text is always `TEXTATOM = 1`. No code path permits or instantiates text with a subspace selector greater than 1; no code permits any atom type with selector greater than 2 (LINKATOM). The "depth 2" is structurally enforced by a hardcoded constant in `findisatoinsertmolecule`. m_1 > 2 (understood as a subspace selector digit > 2) is impossible in this implementation.

---

### The ISA Address Hierarchy

Tumblers are structured as variable-length sequences of non-negative integers separated by zeros. The granfilade (permascroll) uses ISAs to address all stored content. `nstories()` [tumble.c:249] and `tumblerlength()` [tumble.c:259] measure depth:

```c
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories(tumblerptr) - tumblerptr->exp);   // tumble.c:261
}
```

The ISA hierarchy under a single root node follows a fixed pattern enforced by `findisatoinsertnonmolecule` [granf2.c:203]:

```
root:        "1"             (depth 1 — single NODE)
account:     "1.1"           (depth 2 — placed 2 from root: depth = 2 for NODE→ACCOUNT)
document:    "1.1.0.1"       (depth 4 — placed 2 from account: depth = 2 for ACCOUNT→DOCUMENT)
version:     "1.1.0.1.1"     (depth 5 — placed 1 from document: depth = 1 for DOCUMENT→DOCUMENT)
sub-version: "1.1.0.1.1.1"   (depth 6)
```

The choice between depth 1 and depth 2 for non-molecule types is at [granf2.c:209]:

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

Same type → depth 1 (version chains). Different types → depth 2 (documents under accounts).

---

### Where Text Atoms Get Their ISA

Text atoms are placed by `findisatoinsertmolecule` [granf2.c:158-181]. This function is reached from `doinsert` [do1.c:117] via:

```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);   // do1.c:117
ret = inserttextingranf(taskptr, granf, &hint, textset, &ispanset)  // do1.c:118
```

Inside `findisatoinsertmolecule`:

```c
// granf2.c:162 — search upper bound: doc_isa offset by 2, digit = atomtype+1
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);

// granf2.c:165 — if same depth as hintisa (document node already exists):
if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
    tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);  // place at +2, digit=TEXTATOM
    tumblerincrement (isaptr, 1, 1, isaptr);                        // then +1 more for character
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   // subsequent chars: just increment
```

The **hardcoded `2`** in `tumblerincrement(&hintptr->hintisa, 2, ...)` is the rightshift argument. It positions the text atom at exactly **2 positions to the right of the document ISA's last non-zero digit**.

Concretely, for document "1.1.0.1" (4-deep, last non-zero at index 3):
- TEXTATOM=1 is placed at mantissa[3+2=5]
- Character offset k is placed at mantissa[5+1=6]
- First text character ISA: `"1.1.0.1.0.1.1"` (depth 7)
- Second: `"1.1.0.1.0.1.2"`, etc.

For a versioned document "1.1.0.1.1" (5-deep, last non-zero at index 4):
- TEXTATOM=1 at mantissa[4+2=6]
- First text: `"1.1.0.1.1.0.1.1"` (depth 8)

The text subspace is always exactly 2 positions below the document ISA — regardless of how deep the document is in the version tree.

---

### The Atom Type Constants Are Fixed

From [xanadu.h:144-146]:

```c
/* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

All call sites in do1.c use these constants exclusively:

| Call site | Location | Atom type |
|-----------|----------|-----------|
| `doinsert` | do1.c:117 | `TEXTATOM` |
| `domakelink` | do1.c:180 | `LINKATOM` |
| `docreatelink` | do1.c:207 | `LINKATOM` |

There is no call to `makehint` with atomtype > 2, and no mechanism in the protocol or internal logic to create one.

---

### `validhint` Confirms the Constraint — But Is Never Called

`validhint` [do2.c:86-108] enforces:

```c
|| (hintptr->atomtype > 2)    // do2.c:94
```

This explicitly documents that atomtype > 2 is invalid. However, `validhint` is defined but **never called** anywhere in the codebase — all call sites invoke `makehint` directly without validation. The constraint is structurally enforced by the code (only TEXTATOM and LINKATOM are ever used) but not dynamically checked.

---

### `acceptablevsa` Does Not Constrain V-Addresses

The document V-address (where text sits within a document's virtual address space) is supplied by the client. The backend's `acceptablevsa` [do2.c:110-113] is a stub:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr) {
    return (TRUE);
}
```

This means clients can place text at any V-position. The convention is text at V=1.x, links at V=2.x (enforced by `findnextlinkvsa` [do2.c:157]), but the backend will not reject text at V=3.x or higher.

---

### The Link Subspace for Completeness

Link references within a document's V-space are placed starting at V=2.1 [do2.c:157-166]:

```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // mantissa[1] = 1 → "2.1"
```

Within a link orgl, the from/to/three endpoint V-positions are hardcoded by `setlinkvsas` [do2.c:169-182]:
- fromvsa = "1.1" (LINKFROMSPAN)
- tovsa = "2.1" (LINKTOSPAN)
- threevsa = "3.1" (LINKTHREESPAN, for 3-way links)

These are all hardcoded constants, with no mechanism for m_1 > 2 at the link endpoint level either.

---

### Summary

| Property | Value | Enforced by |
|----------|-------|-------------|
| Text atom depth offset from document ISA | exactly **2** (hardcoded) | `findisatoinsertmolecule`, granf2.c:162 |
| Text subspace selector digit | always **TEXTATOM = 1** | xanadu.h:145; do1.c:117 |
| Link subspace selector digit | always **LINKATOM = 2** | xanadu.h:146; do1.c:180, 207 |
| Maximum atom type | **2** (LINKATOM) | defined constants; validhint do2.c:94 (uncalled) |
| V-address constraints on text | **none** — `acceptablevsa` always returns TRUE | do2.c:110-113 |

**The implementation fixes the text subspace at exactly depth 2 (hardcoded offset) from the document ISA, with subspace selector digit TEXTATOM=1. It neither permits nor instantiates text with a subspace selector > 1, and no atom type > 2 (LINKATOM) exists or can be created.**
